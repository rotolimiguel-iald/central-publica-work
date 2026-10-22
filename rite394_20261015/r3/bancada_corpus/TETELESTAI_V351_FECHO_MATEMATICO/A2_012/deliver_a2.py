from pathlib import Path
import hashlib,json,datetime,os,re
ROOT=Path(__file__).resolve().parent
CHAT=ROOT.parents[1]; V=CHAT/'REVISAO_A2_012'; D=V/'DELTA01'; OUT=CHAT/'TUNEL/DO_CHATGPT'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def put(p,b):
    assert p.is_relative_to(CHAT) and not p.exists() and b
    t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)

seal=load(D/'SELO_DELTA01.json')
assert seal['decision']=='DELTA01_VERIFICADO__33_PRESERVADOS__P2_01_QUITADO'
for item in seal['files']:assert pin(Path(item['path']))==item
run=load(ROOT/'delta01_build/RESULT.json')
assert run['all_compiled'] and run['all_axioms_allowed'] and run['public_names']==33
plan=load(ROOT/'AUDIT_NAMES_DELTA01.json')
for item in plan['sources']:assert pin(Path(item['path']))=={k:item[k] for k in ['path','bytes','sha256']}
files=[Path(s['path']) for s in plan['sources']]
files += [ROOT/n for n in ['REAPROVEITAMENTO_A2.md','REAPROVEITAMENTO_A2.json','AUDIT_NAMES_DELTA01.json',
    'DELTA01_PODA.json','delta01_build/RESULT.json','AUDITORIA_A2_AUTORAL.json',
    'author_controls/20260915_125804_093873/SEMANTIC_RECLASSIFICATION.json',
    'PROVENIENCIA_CORE_SUPPORT.json','src/TGL/CoreSupport.lean','src/TGLExt/AuditA2RegularSupport.lean',
    'dev_lean.py','ENTREGA_A2_CORPO.md']]
files += [V/n for n in ['RECIBO_REVISAO_A2.md','AUDITORIA_A2_INDEPENDENTE.json','SELO_A2.json']]
files += [D/n for n in ['RECIBO_REVISAO_A2_DELTA01_33.md','AUDITORIA_DELTA01.json','BUILD_DELTA01.json',
    'DELTA_COMPARISON.json','INTEGRIDADE_DELTA01.json','MANIFESTO_DELTA01.json','SELO_DELTA01.json']]
counts=[]
for item in plan['sources']:
    p=Path(item['path']);s=p.read_text(encoding='utf8')
    counts.append(dict(**pin(p),theorems=len(re.findall(r'^theorem\s+\w+',s,re.M)),
        definitions=len(re.findall(r'^def\s+\w+',s,re.M))))
assert sum(c['theorems']+c['definitions'] for c in counts)==33
manifest=OUT/'ENTREGA_011_A2_suporte_split_e_parede_manifesto.json'
put(manifest,json.dumps(dict(timestamp=datetime.datetime.now().astimezone().isoformat(),
    status='PARTIAL_A2_KERNEL_CHECKED_AND_INDEPENDENTLY_REVIEWED',public_names=33,
    counts=counts,files=[pin(p) for p in files],review=seal['decision'],
    three_locks_core_data_constructed=False,full_witness_constructed=False,
    reticular_susy_instantiated=False,gate_changed=False),ensure_ascii=False,indent=2).encode('utf8'))
body=(ROOT/'ENTREGA_A2_CORPO.md').read_text(encoding='utf8')
body+='\n\n## Recibo final do delta e arquivos\n\n'
body+='[REAL] Revisão independente do delta concluída: P0=0, P1=0, P2=0 neste delta; P2-01 quitado. Oito módulos matemáticos e dois auditores recompilados na raiz própria do revisor; os 33 nomes foram impressos por ambos os auditores. Isso não altera os itens NÃO PAGO da tabela.\n\n'
for c in counts:
    p=Path(c['path']);body+=f"- [{p.name}](<{p.as_posix()}>) — {c['theorems']} theorem, {c['definitions']} def; SHA256 `{c['sha256']}`.\n"
for p in files[len(plan['sources']):]:
    data=pin(p);body+=f"- [{p.name}](<{p.as_posix()}>) — SHA256 `{data['sha256']}`.\n"
record=pin(manifest);body+=f"\nManifesto: [{manifest.name}](<{manifest.as_posix()}>) — SHA256 `{record['sha256']}`.\n"
target=OUT/'ENTREGA_011_A2_suporte_split_e_parede.md';put(target,body.encode('utf8'))
print(json.dumps(pin(target),ensure_ascii=False))
