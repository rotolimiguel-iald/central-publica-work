from review_a2 import *

data=json.loads((ROOT/'INPUTS.json').read_text(encoding='utf-8'))
failure=ROOT/'failed_setup'/stamp()
for p in (ROOT/'build_logs').rglob('*'):
    if p.is_file(): write(failure/p.relative_to(ROOT/'build_logs'),p.read_bytes())
links=[]
for row in data['accepted_objects']:
    src=Path(row['hardlink']['path']); dst=OUT/src.relative_to(CACHE)
    assert dst.resolve().is_relative_to(OUT) and not dst.exists()
    dst.parent.mkdir(parents=True,exist_ok=True)
    os.link(src,dst)
    assert os.path.samefile(src,dst)
    links.append(dict(source=row['source'],compiled_namespace_link=info(dst)))
for m in MODULES:
    assert not (OUT/Path(*m.split('.'))).with_suffix('.olean').exists()
record(ROOT/'READONLY_NAMESPACE_LINKS.json',dict(links=links,count=len(links),
    explanation='Lean resolves a module family under the first matching namespace directory; accepted dependencies therefore need immutable links beside new outputs',
    failed_attempt=str(failure),accepted_modules_rebuilt=False,source_files_changed=False))
print('Immutable namespace links:',len(links))
