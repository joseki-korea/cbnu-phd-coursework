#!/usr/bin/env python3
"""Generate a deterministic heading-based catalog; no content or vectors are stored."""
import fnmatch, hashlib, json, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def ignored(path):
    result = False
    for raw in (ROOT / '.ragignore').read_text(encoding='utf-8').splitlines():
        rule = raw.strip()
        if not rule or rule.startswith('#'): continue
        negated = rule.startswith('!')
        if negated: rule = rule[1:]
        rule = rule.lstrip('/')
        parts = path.split('/')
        if rule.endswith('/'):
            match = any(fnmatch.fnmatchcase('/'.join(parts[:i]), rule.rstrip('/')) or fnmatch.fnmatchcase(parts[i-1], rule.rstrip('/')) for i in range(1, len(parts)))
        elif '/' not in rule:
            match = any(fnmatch.fnmatchcase(p, rule) for p in parts)
        else:
            match = fnmatch.fnmatchcase(path, rule) or (rule.startswith('**/') and fnmatch.fnmatchcase(path, rule[3:]))
        if match: result = not negated
    return result

def blob_hash(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()[:8]

def main():
    files = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'], cwd=ROOT).decode().split('\0')
    rows = []
    for name in sorted(set(files)):
        if not name.lower().endswith('.md') or ignored(name): continue
        path = ROOT / name
        if not path.is_file() or path.is_symlink(): continue
        data = path.read_bytes()
        try: text = data.decode('utf-8')
        except UnicodeDecodeError: continue
        front = text.split('---', 2)[1] if text.startswith('---\n') and text.count('---') >= 2 else ''
        if re.search(r'^sensitivity:\s*["\']?secret\b', front, re.M | re.I): continue
        lang = re.search(r'^lang:\s*["\']?([\w-]+)', front, re.M)
        sensitivity = re.search(r'^sensitivity:\s*["\']?([\w-]+)', front, re.M)
        tags_match = re.search(r'^tags:[ \t]*\[([^\]]*)\]', front, re.M)
        if tags_match:
            tags = [x.strip().strip('\"\'') for x in tags_match.group(1).split(',') if x.strip()]
        else:
            block = re.search(r'^tags:[ \t]*\n((?:[ \t]*-[^\n]*\n?)*)', front, re.M)
            tags = [x.strip().lstrip('-').strip().strip('\"\'') for x in block.group(1).splitlines()] if block else []
        lines = text.splitlines()
        headings = []
        fenced = False
        in_front = bool(lines and lines[0] == '---')
        for n, line in enumerate(lines, 1):
            if in_front:
                if n > 1 and line == '---': in_front = False
                continue
            if re.match(r'^\s*(```|~~~)', line):
                fenced = not fenced
                continue
            if not fenced and re.match(r'^#{1,6}\s+\S', line):
                headings.append((n, line.lstrip('#').strip()))
        headings = headings or [(1, '(document)')]
        sha = blob_hash(data)
        for i, (line, heading) in enumerate(headings):
            end = headings[i+1][0]-1 if i+1 < len(headings) else len(lines)
            rows.append(dict(id=hashlib.sha256(f'{name}:{line}'.encode()).hexdigest()[:16], path=name, heading=heading, start_line=line, end_line=end, sha8=sha, tags=tags, lang=lang.group(1) if lang else 'und', sensitivity=sensitivity.group(1) if sensitivity else 'unclassified'))
    out = ROOT / 'docs/_meta/rag-manifest.jsonl'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(''.join(json.dumps(row, ensure_ascii=False, sort_keys=True)+'\n' for row in rows), encoding='utf-8')
    print(f'{len(rows)} chunks')
if __name__ == '__main__': main()
