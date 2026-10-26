"""Byte pins of all local code, data and fonts used by the renderer."""
from pathlib import Path
import hashlib, re, os

def collect(root):
    root=Path(root).resolve(); cinema=root/'cinema'
    names=['cinema-scene.mjs','render-support.mjs','cinema-composition.mjs','timeline.mjs','studio.mjs','index.html']
    paths={cinema/n for n in names}
    paths.update(root/'data'/n for n in ['hud.json','frames.json','scene.json','film1.json','film2.json'])
    paths.add(root/'web/fonts.css')
    paths.update(p for p in (root/'web/fonts').iterdir() if p.is_file() and '.bak_' not in p.name)
    queue=[p for p in paths if p.suffix in ['.js','.mjs']]; seen=set()
    while queue:
        p=queue.pop()
        if p in seen: continue
        seen.add(p); source=re.sub(r'/\*.*?\*/','',p.read_text(encoding='utf-8'),flags=re.S)
        for ref in re.findall(r'(?:from\s*|import\s*\(?)\s*[\'\"]([^\'\"]+)[\'\"]',source):
            if not ref.startswith('.'): raise ValueError('Non-local render dependency: '+ref)
            q=(p.parent/ref).resolve()
            if not q.is_relative_to(root) or not q.is_file(): raise ValueError('Missing render dependency: '+ref)
            paths.add(q)
            if q.suffix in ['.js','.mjs']: queue.append(q)
    return {os.path.relpath(p,cinema).replace('\\','/'):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(paths)}
