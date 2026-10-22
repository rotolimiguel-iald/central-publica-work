from pathlib import Path
import ast, copy, datetime, difflib, hashlib, json, os, re

ROOT=Path(__file__).resolve().parent
PREV=ROOT.parent
AUTHOR=Path(r'C:\IALD\Central de Patentes\Chatgpt\A2_TRACE_COMPLETION_012')
PAID=PREV.parent/'COMPATIBILIDADE_7'
reads=[]
checks=[]

def pin(p,b=None):
    p=Path(p); b=p.read_bytes() if b is None else b
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def read(p,purpose):
    b=Path(p).read_bytes(); reads.append(dict(**pin(p,b),purpose=purpose)); return b

def write(p,b):
    p=Path(p); assert p.resolve().is_relative_to(PREV.resolve())
    b=b.encode('utf-8') if isinstance(b,str) else b
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        backup=p.with_name(p.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(p.read_bytes()); assert backup.read_bytes()==p.read_bytes()
    t=p.with_name(p.name+'.tmp'); t.write_bytes(b); assert t.read_bytes()==b
    os.replace(t,p); assert p.read_bytes()==b

def record(p,data): write(p,json.dumps(data,ensure_ascii=False,indent=2))
def check(name,passed,evidence=None): checks.append(dict(name=name,passed=bool(passed),evidence=evidence))
def link(p): return '['+Path(p).name+'](<'+Path(p).as_posix()+'>)'

for name in ['PROPOSTA_LEITORES_EXISTENTES_V2.py','PROPOSTA_LEITORES_EXISTENTES_V2.diff',
             'PROPOSTA_MAPA_CONSUMIDORES_V2.json','TESTES_LEITORES_COPIADOS_V2.json']:
    write(ROOT/'inputs'/name,read(AUTHOR/name,'V2 fully read and copied, read-only author'))
v1=read(PREV/'inputs/PROPOSTA_LEITORES_EXISTENTES.py','sealed V1 exact-byte baseline')
v2=(ROOT/'inputs/PROPOSTA_LEITORES_EXISTENTES_V2.py').read_bytes()
old_guard=b'    verified = (built\n'
new_guard=old_guard+b'                and type(kf.get("audit_returncode")) is int\n'
check('only_delta_is_exact_rc_type_guard',v1.count(old_guard)==1 and v1.replace(old_guard,new_guard,1)==v2)
write(ROOT/'DELTA_V1_V2.diff',''.join(difflib.unified_diff(v1.decode().splitlines(True),v2.decode().splitlines(True),fromfile='PROPOSTA_LEITORES_EXISTENTES.py',tofile='PROPOSTA_LEITORES_EXISTENTES_V2.py')))

old_map=json.loads(read(PREV/'inputs/PROPOSTA_MAPA_CONSUMIDORES.json','sealed V1 map'))
new_map=json.loads((ROOT/'inputs/PROPOSTA_MAPA_CONSUMIDORES_V2.json').read_bytes())
def invariant_map(m): return {k:v for k,v in m.items() if k not in ['timestamp','candidate','diff','P2_READERS_01']}
check('contracts_consumers_scope_and_cast_requirement_unchanged',invariant_map(old_map)==invariant_map(new_map))
for key in ['candidate','diff']:
    check('V2_map_pin:'+key,pin(new_map[key]['path'])==new_map[key])
snapshot=read(PREV/'inputs/CANONICAL_READERS_SNAPSHOT.py','existing copied snapshot only, no canonical access')
expected=''.join(difflib.unified_diff(snapshot.decode().replace('\r\n','\n').splitlines(True),v2.decode().splitlines(True),fromfile='CANONICAL_READERS_SNAPSHOT.py',tofile='PROPOSTA_LEITORES_EXISTENTES_V2.py'))
check('V2_diff_matches_snapshot',expected==(ROOT/'inputs/PROPOSTA_LEITORES_EXISTENTES_V2.diff').read_text(encoding='utf-8'))
old_seal=json.loads(read(PREV/'SELO_LEITORES.json','verify V1 historical receipt preservation'))
for item in old_seal['files']:
    current=pin(item['path'],read(item['path'],'V1 sealed historical artifact'))
    check('V1_receipt_preserved:'+Path(item['path']).name,current==item)
old_manifest=json.loads((PREV/'MANIFESTO_LEITORES.json').read_bytes())
check('V1_all_manifest_artifacts_preserved',all(pin(item['path'])==item for item in old_manifest['files']))
old_author_records=json.loads((PREV/'READS.json').read_bytes())
v1_author=[item for item in old_author_records if str(AUTHOR) in item['path']]
check('V1_author_inputs_preserved',all(pin(item['path'])=={k:item[k] for k in ['path','bytes','sha256']} for item in v1_author))

def load_copied(data,name):
    tree=ast.parse(data.decode('utf-8'))
    assert all(isinstance(node,(ast.Assign,ast.FunctionDef)) for node in tree.body)
    assert not any(isinstance(node,(ast.Import,ast.ImportFrom)) for node in ast.walk(tree))
    namespace={};exec(compile(tree,name,'exec'),namespace);return namespace
old=load_copied(v1,'sealed_V1_copy')
new=load_copied(v2,'V2_copy')
audit=json.loads(read(PAID/'FINAL_AUDIT.json','reuse independent real axiom report, no Lean rebuild'))
facts=json.loads(read(PAID/'AUDITORIA_FINAL_INDEPENDENTE.json','translate paid real build metadata'))
log=audit['result']['stdout'];blob=read(log['path'],'parse sealed actual 60-name axiom report')
check('actual_axiom_log_preserved',pin(log['path'],blob)==log)
report={}
for name,ax,_ in re.findall(r"'([\w.']+)' (?:depends on axioms: \[([^]]*)\]|(does not depend on any axioms))",blob.decode(),re.S):
    assert name not in report
    report[name]=[re.sub(r'\.\{[^}]*\}','',a.strip()) for a in ax.replace('\n',' ').split(',') if a.strip()]
check('all_paid_60_names_present',set(report)==set(audit['names']) and len(report)==60)
base=dict(axiom_report=report,lake_build_ok=all(item['returncode']==0 for item in facts['modules'].values()),
          audit_returncode=audit['result']['returncode'],all_verified=all(facts['gates'].values()))
new_flags=set(new_map['typed_contracts'])
verify=new['verify_v350_modular_provenance']
check('measured_int_zero_keeps_V1_results',type(base['audit_returncode']) is int and base['audit_returncode']==0 and verify(base)==old['verify_v350_modular_provenance'](base) and {f for f,v in verify(base).items() if v}==new_flags)
cases=[('int_zero',0,True),('int_one',1,False),('int_negative',-1,False),('bool_false',False,False),('bool_true',True,False),
       ('string_zero','0',False),('string_one','1',False),('float_zero',0.0,False),('float_one',1.0,False),('none',None,False),('missing',None,False)]
case_results=[]
for label,value,accepted in cases:
    paths=[]
    for mode in ['full','verified_incremental']:
        trial=copy.deepcopy(base)
        if label=='missing':trial.pop('audit_returncode')
        else:trial['audit_returncode']=value
        if mode=='verified_incremental':trial.update(lake_build_ok=False,incremental_build_ok=True,dependency_hashes_verified=True,changed_source_hashes_verified=True)
        observed=verify(trial)
        wanted={f:bool(accepted and f in new_flags) for f in observed}
        paths.append(dict(mode=mode,actual=observed,expected=wanted,passed=observed==wanted))
    case_results.append(dict(case=label,python_type='MISSING' if label=='missing' else type(value).__name__,value=value,expected_acceptance=accepted,build_paths=paths))
    check('rc_type_boundary:'+label,all(row['passed'] for row in paths))
bad=copy.deepcopy(base);bad['audit_returncode']=False
check('inherited_P2_reproduced_V1_and_closed_V2',all(old['verify_v350_modular_provenance'](bad)[f] for f in new_flags) and not any(verify(bad).values()))
bad.update({f:True for f in new_flags})
check('callers_refuse_stale_flags_with_bool_rc',all(not new['v350_frontier_flag_has_proof'](bad,f) for f in new_flags) and not any(new['finalize_v350_modular_frontier'](copy.deepcopy(bad))[f] for f in new_flags))
author_result=json.loads((ROOT/'inputs/TESTES_LEITORES_COPIADOS_V2.json').read_bytes())
check('author_report_targets_measured_V2',author_result['proposal']==pin(AUTHOR/'PROPOSTA_LEITORES_EXISTENTES_V2.py'))
integrity=[dict(path=item['path'],unchanged=pin(item['path'])=={k:item[k] for k in ['path','bytes','sha256']}) for item in reads]
check('all_read_artifacts_unchanged_at_close',all(item['unchanged'] for item in integrity))
passed=all(item['passed'] for item in checks)
decision='VERIFICADO_V2_ATIVA_P2_READERS_01_CORRIGIDO' if passed else 'DELTA_V2_NAO_ACEITO'
counts=dict(P0=0,P1=0 if passed else 1,P2=0 if passed else 1)
data=dict(decision=decision,active_version='V2' if passed else 'V1_WITH_P2',checks=checks,count=len(checks),all_passed=passed,
          rc_cases=case_results,rc_case_count=len(cases),build_path_count=2,open_findings=counts,
          historical_observation=dict(id='P2-READERS-01',origin='Inherited from canonical snapshot; reproduced in V1',status='CORRIGIDO_NA_V2' if passed else 'OPEN',V1_receipt_preserved=True),
          lean_executions=0,canonical_executions=0,canonical_read='Not retried; previous denial and DECLARADO provenance retained',
          author_tests=dict(count=author_result['count'],reported_all_passed=author_result['all_passed'],status='READ_ONLY_NOT_RERUN'),
          reviewer=dict(name='Carver',agent_id='01a0a5b5-e12d-70c1-a68a-c6f13373e3c0',identity_status='INPUT principal',role='independent non-author'),
          active_candidate=pin(AUTHOR/'PROPOSTA_LEITORES_EXISTENTES_V2.py'),integrity=integrity)
record(ROOT/'TESTES_DELTA_V2.json',data)
record(ROOT/'LEITURAS_DELTA_V2.json',reads)
text=f'''# Adendo independente — leitores V2 ativos

**[REAL — delta verificado] {decision}. P0={counts['P0']}; P1={counts['P1']}; P2={counts['P2']} em aberto no escopo copiado.**

Carver, agent_id `01a0a5b5-e12d-70c1-a68a-c6f13373e3c0`, revisor independente e não autor; identidade fornecida pela principal [INPUT]. Este adendo torna V2 a proposta ativa para este recibo, sem integrar o canônico.

**P2-READERS-01: herdado no snapshot/V1 e corrigido na V2.** A comparação de bytes demonstra que a única alteração executável foi inserir `and type(kf.get("audit_returncode")) is int` imediatamente antes da comparação com zero. Os mapas de contratos, consumidores, escopos e a exigência dos cinco casts permanecem idênticos. Não foi acrescentada função Python ou alias Lean. A proposta V1 e todos os artefatos do seu manifesto continuam com bytes e hashes anteriores; o achado histórico não foi apagado ou reclassificado retrospectivamente.

Foram registradas {len(checks)} verificações próprias do delta, incluindo onze casos de rc nas duas vias existentes (build completo e incremental com hashes verificados). O inteiro `0` é aceito. Inteiros `1` e `-1`, booleanos `False` e `True`, strings `"0"` e `"1"`, floats `0.0` e `1.0`, `None` e campo ausente são recusados. Os dados positivos usam o axiom report real de sessenta nomes da revisão independente paga. Com rc inteiro zero, todos os resultados da V1 se preservam. Com rc booleano falso, a sonda reproduz a aceitação antiga na V1, confirma a recusa na V2 e verifica a rejeição de flags obsoletas pelos consumidores do helper.

O mapa V2 e seu diff conferem com os bytes medidos; o diff autoral é contra o snapshot, enquanto {link(ROOT/'DELTA_V1_V2.diff')} isola a linha entre V1 e V2. O relatório autoral informa {author_result['count']} checks e foi lido, sem execução ou inclusão na contagem própria. Resultados detalhados: {link(ROOT/'TESTES_DELTA_V2.json')}. Leituras, hashes e bytes: {link(ROOT/'LEITURAS_DELTA_V2.json')}.

**Nenhuma execução Lean ou canônica nesta revisão de delta.** Os cinco casts e as recusas de True já pagos permanecem válidos no escopo anterior. Continua sendo requisito de integração inserir esses casts no Audit canônico realmente executado, conservar a proveniência/hashes e manter H1 restrito ao representante mínimo. Os limites físicos, H2/H3, BW, transformação limitada padrão, adendo inteiro e gate não foram ampliados. A negativa anterior de acesso ao original não foi repetida; a proveniência canônica continua [DECLARADO — captura AST autoral], com as cópias verificadas independentemente.

Histórico preservado: {link(PREV/'PARECER_LEITORES.md')} e {link(PREV/'SELO_LEITORES.json')}. Proposta ativa: {link(AUTHOR/'PROPOSTA_LEITORES_EXISTENTES_V2.py')}; mapa ativo: {link(AUTHOR/'PROPOSTA_MAPA_CONSUMIDORES_V2.json')}.

| Entrada V2 lida integralmente | Bytes | SHA-256 |
|---|---:|---|
'''
for item in reads[:4]:text+=f"| {link(item['path'])} | {item['bytes']} | `{item['sha256']}` |\n"
write(ROOT/'RECIBO_LEITORES_V2.md',text)
record(ROOT/'SELO_LEITORES_V2.json',dict(decision=decision,open_findings=counts,files=[pin(ROOT/n) for n in ['RECIBO_LEITORES_V2.md','TESTES_DELTA_V2.json','LEITURAS_DELTA_V2.json','DELTA_V1_V2.diff','review_delta_v2.py']]))
if passed:
    record(PREV/'LEITORES_ATIVOS.json',dict(active_version='V2',active_candidate=pin(AUTHOR/'PROPOSTA_LEITORES_EXISTENTES_V2.py'),
        active_receipt=pin(ROOT/'RECIBO_LEITORES_V2.md'),active_seal=pin(ROOT/'SELO_LEITORES_V2.json'),
        supersedes_only_open_P2=pin(PREV/'PARECER_LEITORES.md'),scope='Copied readers only; no canonical integration'))
print(json.dumps(dict(decision=decision,checks=len(checks),rc_cases=len(cases),all_passed=passed,receipt=pin(ROOT/'RECIBO_LEITORES_V2.md')),ensure_ascii=False))
