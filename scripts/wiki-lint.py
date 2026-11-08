#!/usr/bin/env python3
"""Check wiki metadata, index coverage, citations, and local Markdown links."""
import hashlib, re, sys
from pathlib import Path
from urllib.parse import unquote
ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / 'docs/wiki'
REQUIRED = ('id','title','summary','domain','tags','owner','status','created','updated','source','lang','sensitivity','related')
CITE = re.compile(r'\[source: ([^\]#]+)#L(\d+) @([0-9a-f]{8})\]')
def blob(data): return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()[:8]
def main():
    errors=[]
    pages=sorted((WIKI/'pages').rglob('*.md'))
    index=(WIKI/'index.md').read_text(encoding='utf-8')
    for p in [WIKI/'SCHEMA.md', WIKI/'index.md', WIKI/'log.md', *pages]:
        text=p.read_text(encoding='utf-8')
        if not text.startswith('---\n') or '\n---\n' not in text[4:]:
            errors.append(f'{p}: missing front matter'); continue
        front, body=text[4:].split('\n---\n',1)
        for key in REQUIRED:
            if not re.search(r'^'+key+r':\s*\S',front,re.M): errors.append(f'{p}: missing {key}')
        if re.search(r'^sensitivity:\s*["\']?secret',front,re.M|re.I): errors.append(f'{p}: secret page')
        if p not in pages: continue
        rel=p.relative_to(WIKI).as_posix()
        if len(re.findall(r'\]\('+re.escape(rel)+r'(?:#[^)]*)?\)',index)) != 1: errors.append(f'{p}: index entry missing or duplicated')
        in_code=False
        for n,line in enumerate(body.splitlines(),1):
            s=line.strip()
            if s.startswith('```'): in_code=not in_code; continue
            if not s or s.startswith('#') or in_code: continue
            if not CITE.search(s): errors.append(f'{p}:{n}: uncited content')
        for source,line,sha in CITE.findall(body):
            target=(ROOT/source).resolve()
            if not target.is_relative_to(ROOT) or not target.is_file(): errors.append(f'{p}: missing source {source}'); continue
            data=target.read_bytes()
            if blob(data)!=sha: errors.append(f'{p}: stale source {source}')
            if int(line)<1 or int(line)>len(data.splitlines()): errors.append(f'{p}: invalid line {source}#L{line}')
    listed = re.findall(r'\]\((pages/[^)#]+\.md)(?:#[^)]*)?\)', index)
    if len(listed) != len(pages): errors.append('index page count does not match pages')
    for p in [WIKI/'index.md',WIKI/'SCHEMA.md',WIKI/'log.md',*pages]:
        for dest in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            dest=unquote(dest)
            if re.match(r'^[a-z]+:',dest): continue
            path, _, anchor = dest.partition('#')
            target=(p.parent/path).resolve() if path else p
            if not target.exists(): errors.append(f'{p}: broken link {dest}'); continue
            if anchor and target.is_file() and target.suffix.lower() == '.md':
                headings=re.findall(r'^#{1,6}\s+(.+?)\s*#*$', target.read_text(encoding='utf-8'), re.M)
                slugs=[re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in headings]
                if anchor not in slugs: errors.append(f'{p}: broken anchor {dest}')
    for e in errors: print(e)
    print('FAIL' if errors else f'PASS ({len(pages)} pages)')
    return bool(errors)
if __name__=='__main__': sys.exit(main())
