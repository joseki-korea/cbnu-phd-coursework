#!/usr/bin/env python3
"""Validate the 23-key folder metadata contract and repo-local navigation."""
import argparse
import datetime
import json
from pathlib import Path, PurePosixPath
import subprocess

KEYS=set('schema_version id title kind section_code content_state canonical_path migration_state status summary enter_when exit_when keywords projects owner authority availability updated_at source_uri aliases legacy_names children related'.split())


def read_yaml(path):
    command=['ruby','-ryaml','-rjson','-e',
             'puts JSON.generate(YAML.safe_load(File.read(ARGV[0]), aliases: false))',str(path)]
    try:
        result=subprocess.run(command,capture_output=True,text=True,check=True)
    except FileNotFoundError as exc:
        raise RuntimeError('Ruby with its standard YAML parser is required for this check') from exc
    return json.loads(result.stdout)


def validate(root):
    root=root.resolve();errors=[];ids=[];children=0;related=0;canonical=0
    metas=sorted(root.rglob('meta.yaml'))
    for path in metas:
        rel=path.relative_to(root).as_posix();value=read_yaml(path)
        def require(condition,message):
            if not condition:errors.append(rel+': '+message)
        require(set(value)==KEYS,'keys must match the 23-key standard exactly')
        ids.append(value.get('id'))
        for name in ['summary','enter_when','exit_when','keywords','projects','aliases','children','related']:
            require(isinstance(value.get(name),list),name+' must be a list')
        require(1<=len(value['summary'])<=3,'summary needs 1-3 lines')
        require(3<=len(value['keywords'])<=8,'keywords need 3-8 domain terms')
        require(bool(value['projects']) and bool(value['enter_when']) and bool(value['exit_when']),'routing/project fields must be populated')
        require(bool(value.get('source_uri')),'source_uri must identify the PR/source')
        try:datetime.datetime.fromisoformat(value['updated_at'].replace('Z','+00:00'))
        except (ValueError,TypeError):require(False,'updated_at must be an ISO date or datetime')
        require(value['content_state'] in ('empty','populated','external'),'invalid content_state')
        require(value['migration_state'] in ('planned','indexed','migrated','verified'),'invalid migration_state')
        if value['content_state']=='empty':require(value['migration_state']=='indexed','empty sections must be indexed, not migrated')
        require((path.parent/'README.md').is_file(),'README is required')
        target=(root/value['canonical_path']).resolve();canonical+=1
        require(target==path.parent,'canonical_path must point to this folder from repo root')
        if path.parent==root:require(not any('상위 README' in line for line in value['exit_when']),'root must not route to a parent README')
        for item in value['children']:
            children+=1;p=PurePosixPath(item['path'])
            require(not p.is_absolute() and '..' not in p.parts,'children must stay inside their folder')
            require((path.parent/item['path']).exists(),'missing child '+item['path'])
        for item in value['related']:
            related+=1;target=(path.parent/item['path']).resolve()
            require(target==root or root in target.parents,'related must remain inside the repository')
            require(target.exists(),'missing related '+item['path'])
    if len(metas)!=15:errors.append('expected exactly 15 root/section meta files')
    if len(set(ids))!=len(ids):errors.append('duplicate metadata ids')
    keyword_sets={tuple(read_yaml(p)['keywords']) for p in metas}
    if len(keyword_sets)!=15:errors.append('folder keywords must not be copied boilerplate')
    return {'status':'PASS' if not errors else 'FAIL','metadata_files':len(metas),
            'required_keys':len(KEYS),'children_paths_checked':children,'related_paths_checked':related,
            'canonical_paths_checked':canonical,'unique_keyword_sets':len(keyword_sets),'errors':errors}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=validate(args.root)
    if args.output:args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
    raise SystemExit(0 if result['status']=='PASS' else 1)
