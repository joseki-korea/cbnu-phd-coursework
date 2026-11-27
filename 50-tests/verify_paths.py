#!/usr/bin/env python3
"""Test extracted path helpers using temporary files and guarded fallbacks using stubs.

No notebook kernel, training, network request or real Windows font installation runs.
"""
import argparse
import ast
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace

DATA_NAMES=['cwru_normal.mat','cwru_fault_inner.mat','cwru_fault_outer.mat','cwru_fault_ball.mat']


def tree(code):
    return ast.parse('\n'.join(line for line in code.splitlines() if not line.lstrip().startswith(('%','!'))))


def run_nodes(nodes,namespace):
    module=ast.fix_missing_locations(ast.Module(body=nodes,type_ignores=[]))
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(module,'<isolated-notebook-path-check>','exec'),namespace)


class ArrayStub:
    def __init__(self,shape=(120000,)):self.shape=shape
    def flatten(self):return self
    def __len__(self):return self.shape[0]
    def __mul__(self,other):return self
    __rmul__=__mul__
    def __add__(self,other):return self
    __radd__=__add__
    def __gt__(self,other):return self


def numpy_stub():
    return SimpleNamespace(pi=3.14159,sin=lambda x:x,linspace=lambda *a:ArrayStub(),
       random=SimpleNamespace(normal=lambda *a,**k:ArrayStub(k.get('size',(120000,)))))


def verify(root):
    root=root.resolve();helpers=[];fonts=[];downloads=[];cells_by_name={}
    for path in sorted((root/'10-source').glob('*.ipynb')):
        nb=json.loads(path.read_text());cells=[]
        for index,cell in enumerate(nb['cells']):
            if cell['cell_type']!='code':continue
            code=''.join(cell.get('source',[]))
            if not any(x in code for x in ('def find_data_file','C:/Windows/Fonts/malgun.ttf','def load_cwru_data')):
                continue
            parsed=tree(code);cells.append((index,code,parsed))
            for node in parsed.body:
                if isinstance(node,ast.FunctionDef) and node.name=='find_data_file':helpers.append((path.name,index,node,parsed))
                if isinstance(node,ast.FunctionDef) and node.name=='load_cwru_data':downloads.append((path.name,index,node))
                if isinstance(node,ast.If) and 'platform.system()' in ast.unparse(node.test):fonts.append((path.name,index,node))
        cells_by_name[path.name]=cells
    assert len(helpers)==4 and len(fonts)==2 and len(downloads)==2
    found=0;missing=0;fallback=0;font_checks=0;download_checks=0;foreign_ignored=0
    original_cwd=Path.cwd()
    with tempfile.TemporaryDirectory(prefix='coursework-paths-') as temporary:
        repo=Path(temporary)/'ancestor/parent/repo'
        source=repo/'10-source';data=repo/'20-assets/24-data'
        source.mkdir(parents=True);data.mkdir(parents=True)
        try:
            for name,index,node,parsed in helpers:
                namespace={'os':os};run_nodes([node],namespace);helper=namespace['find_data_file']
                for cwd,locations in [(repo,[repo,repo.parent,repo.parent.parent,data]),
                                      (source,[source,repo,repo.parent,repo.parent.parent,data])]:
                    os.chdir(cwd)
                    for filename in DATA_NAMES:
                        assert helper(filename) is None;missing+=1
                        foreign_dir=(repo.parent/'20-assets/24-data') if cwd==repo else (source/'20-assets/24-data')
                        foreign_dir.mkdir(parents=True,exist_ok=True)
                        foreign=foreign_dir/filename;foreign.write_bytes(b'outside the intended standard-data root')
                        try:
                            assert helper(filename) is None;foreign_ignored+=1
                        finally:foreign.unlink()
                        for location in locations:
                            fixture=location/filename;fixture.write_bytes(b'path-resolution-fixture; not a MATLAB payload')
                            try:
                                selected=helper(filename)
                                assert selected is not None and Path(selected).resolve()==fixture.resolve(),(name,cwd,location)
                                with open(selected,'rb') as f:assert f.read().startswith(b'path-resolution-fixture')
                                found+=1
                            finally:fixture.unlink()
                # The binary/regression missing-data branches run without SciPy/NumPy.
                condition=next(n for n in parsed.body if isinstance(n,ast.If) and 'path' in ast.unparse(n.test))
                scope={'cwru_normal_path':None,'cwru_fault_path':None,'norm_path':None,'fault_path':None,'np':numpy_stub()}
                run_nodes([condition],scope)
                if 'base_norm_rms' in scope:assert (scope['base_norm_rms'],scope['base_fault_rms'])==(0.07,0.35)
                else:assert scope['feats_norm'].shape==scope['feats_fault'].shape==(100,4)
                fallback+=1
                if 'classification' in name:
                    nb=json.loads((root/'10-source'/name).read_text())
                    multi=tree(''.join(nb['cells'][13]['source']))
                    setup=next(n for n in multi.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='file_map' for t in n.targets))
                    loop=next(n for n in multi.body if isinstance(n,ast.For))
                    scope={'find_data_file':lambda filename:None,'np':numpy_stub(),'X_multi_list':[],'y_multi_list':[]}
                    run_nodes([setup,loop],scope)
                    assert len(scope['X_multi_list'])==4 and all(a.shape==(80,4) for a in scope['X_multi_list'])
                    fallback+=1
            for name,index,node in fonts:
                for platform_name,present in [('Windows',True),('Windows',False),('Darwin',False),('Linux',False)]:
                    calls=[]
                    def rc(*a,**k):calls.append(('rc',k['family']))
                    fm=SimpleNamespace(fontManager=SimpleNamespace(addfont=lambda p:calls.append(('addfont',p))),
                         FontProperties=lambda **k:SimpleNamespace(get_name=lambda:'Malgun Gothic'))
                    scope={'platform':SimpleNamespace(system=lambda:platform_name),
                           'os':SimpleNamespace(path=SimpleNamespace(exists=lambda p:present)),
                           'fm':fm,'plt':SimpleNamespace(rc=rc,rcParams={'font.sans-serif':['sans-serif']})}
                    run_nodes([node],scope)
                    expected='Malgun Gothic' if platform_name=='Windows' else 'AppleGothic' if platform_name=='Darwin' else 'NanumGothic'
                    assert ('rc',expected) in calls
                    assert any(c[0]=='addfont' for c in calls)==(platform_name=='Windows' and present)
                    if platform_name=='Windows' and present:assert ('addfont','C:/Windows/Fonts/malgun.ttf') in calls
                    font_checks+=1
            for name,index,node in downloads:
                for cwd in [repo,source]:
                    os.chdir(cwd)
                    for mode in ['cached','network-failure']:
                        requests=[];loads=[]
                        def request(url,filename):
                            requests.append(filename)
                            raise OSError('intentional offline test')
                        def loadmat(filename):
                            assert (cwd/filename).is_file();loads.append(str((cwd/filename).resolve()))
                            return {'X097_DE_time':ArrayStub()}
                        fixtures=[cwd/'cwru_normal.mat',cwd/'cwru_fault.mat']
                        if mode=='cached':
                            for p in fixtures:p.write_bytes(b'cached path fixture; parser is stubbed')
                        scope={'os':os,'urllib':SimpleNamespace(request=SimpleNamespace(urlretrieve=request)),
                               'scipy':SimpleNamespace(io=SimpleNamespace(loadmat=loadmat)),'np':numpy_stub()}
                        try:
                            run_nodes([node],scope)
                            with contextlib.redirect_stdout(io.StringIO()):signals=scope['load_cwru_data']()
                            assert set(signals)=={'normal','fault'}
                            assert len(loads)==(2 if mode=='cached' else 0)
                            assert len(requests)==(0 if mode=='cached' else 2)
                            download_checks+=1
                        finally:
                            for p in fixtures:
                                if p.exists():p.unlink()
        finally:os.chdir(original_cwd)
    return {'status':'PASS','relative_mat_search_notebooks':len(helpers),
      'conditional_windows_font_notebooks':len(fonts),'cwd_download_notebooks':len(downloads),
      'filesystem_resolution_cases':found,'missing_data_probes':missing,'synthetic_fallback_branch_cases':fallback,
      'font_guard_cases':font_checks,'download_cache_or_offline_cases':download_checks,
      'unrelated_standard_data_directory_ignored_cases':foreign_ignored,
      'search_coverage':['current working directory','repository root','legacy parent','legacy grandparent','20-assets/24-data'],
      'scope':'temporary real files for path selection; deterministic numerical/loader/font/network stubs for guards and fallback; no real MAT parsing, downloads or training'}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();result=verify(args.root)
    if args.output:args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False))
