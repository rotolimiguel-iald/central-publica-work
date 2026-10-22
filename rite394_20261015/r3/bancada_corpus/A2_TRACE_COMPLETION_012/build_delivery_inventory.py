from pathlib import Path
import datetime, hashlib, json, os, re
root=Path(__file__).resolve().parent
chat=root.parent
old=chat/'TETELESTAI_V351_FECHO_MATEMATICO/A2_012'
susy=chat/'A2_SUSY_012'
review=chat/'REVISAO_A2_012/TRACE_COMPLETION_012/COMPATIBILIDADE_7'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def verified(p,expected):
    measured=pin(p)
    assert measured['sha256']==expected['sha256'],(p,expected,measured)
    if 'bytes' in expected:assert measured['bytes']==expected['bytes']
    return measured

d=json.loads((review/'AUDITORIA_FINAL_INDEPENDENTE.json').read_bytes())
assert all(d['gates'].values()) and not any(d['counts'].values())
fresh=[]
for name,row in d['modules'].items():
    file=name.split('.')[-1]+'.lean'
    source=root/'src/TGLExt'/file
    if not source.exists():source=susy/'src/TGLExt'/file
    verified(Path(row['source']['path']),row['source'])
    author=verified(source,row['source'])
    for key in ['object','stdout','stderr']:verified(Path(row[key]['path']),row[key])
    fresh.append({'module':name,'source':author,'reviewed_source':row['source'],
                  'reviewed_object':row['object'],'review_returncode':row['returncode'],
                  'imports':re.findall(r'^import (\S+)',source.read_text(encoding='utf8'),re.M)})
main_names=json.loads((root/'AUDIT_NAMES_FULL.json').read_bytes())['names']
susy_names=json.loads((susy/'AUDIT_NAMES.json').read_bytes())['names']
old_inventory=json.loads((old/'AUDIT_NAMES_DELTA01.json').read_bytes())
old_names=old_inventory['names']
current_names=sorted(set(main_names)|set(susy_names))
assert len(main_names)+len(susy_names)-len(current_names)==11
assert not set(old_names)&set(current_names)

delta_manifest=json.loads((chat/'TUNEL/DO_CHATGPT/ENTREGA_011_A2_suporte_split_e_parede_manifesto.json').read_bytes())
def findpins(value):
    if isinstance(value,dict):
        if isinstance(value.get('path'),str) and isinstance(value.get('sha256'),str):yield value
        for v in value.values():yield from findpins(v)
    elif isinstance(value,list):
        for v in value:yield from findpins(v)
old_pins={str(Path(p['path'])).lower():p for p in findpins(delta_manifest)}
old_sources=[]
for source in sorted((old/'src/TGLExt').glob('V354*.lean')):
    expected=old_pins.get(str(source).lower());assert expected,source
    old_sources.append({'module':'TGLExt.'+source.stem,'source':verified(source,expected),
                        'status':'reused_accepted_delta01_33',
                        'imports':re.findall(r'^import (\S+)',source.read_text(encoding='utf8'),re.M)})
assert len(old_sources)==8 and len(fresh)==11
modules={r['module']:r for r in old_sources+fresh}
ordered=[];pending=dict(modules)
while pending:
    ready=sorted(k for k,v in pending.items() if all(i not in pending for i in v['imports']))
    assert ready,'import cycle'
    for k in ready:ordered.append(pending.pop(k))
data={'timestamp':datetime.datetime.now().astimezone().isoformat(),
      'status':'INTEGRATION_INVENTORY_SOURCE_HASHES_RECHECKED_NOT_CANONICAL_EXECUTION',
      'counts':{'new_modules_this_delivery':len(fresh),'reused_A2_modules':len(old_sources),
                'all_unique_A2_modules':len(ordered),'new_explicit_names':len(current_names),
                'additional_reviewed_exports':len(d['additional_exports']),
                'reused_A2_explicit_names':len(old_names),'all_unique_explicit_names':len(set(old_names)|set(current_names))},
      'source_order':ordered,
      'audit_names_explicit':sorted(set(old_names)|set(current_names)),
      'additional_reviewed_exports':d['additional_exports'],
      'exact_type_checks':pin(root/'src/TGLExt/AuditReaderContracts012.lean'),
      'previous_A2_delivery_manifest':pin(chat/'TUNEL/DO_CHATGPT/ENTREGA_011_A2_suporte_split_e_parede_manifesto.json'),
      'base':'A1 v354 accepted by management, plus CoreSupport and pre-existing wedge/realization types; use the pinned baseline manifests in PROVENIENCIA_* and independent review.',
      'shared_polar':'Only one V354BoundedPolar source; main and SUSY bytes identical.',
      'canonical_source_read':json.loads((root/'CANONICAL_READERS_PROVENANCE.json').read_bytes())['canonical_source'],
      'do_not_embed':['Good/Bad probes','Audit* modules as theorem modules','dev runners or delivery scripts'],
      'delivery_includes_no_numeric_sigma':True}
assert pin(root/'src/TGLExt/V354BoundedPolar.lean')['sha256']==pin(susy/'src/TGLExt/V354BoundedPolar.lean')['sha256']
p=root/'INTEGRACAO_A2_INVENTARIO.json';assert not p.exists()
b=json.dumps(data,ensure_ascii=False,indent=2).encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
print(json.dumps({'path':str(p),'counts':data['counts']},ensure_ascii=False))
