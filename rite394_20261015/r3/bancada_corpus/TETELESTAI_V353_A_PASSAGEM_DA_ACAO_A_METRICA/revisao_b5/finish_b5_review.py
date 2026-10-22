from pathlib import Path
from datetime import datetime
import hashlib,json,os,re
R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA')
OUT=R/'revisao_b5';S=R/'s';BUILD=S/'.lake/build/lib/lean'
STAMP=datetime.now().strftime('%Y%m%d_%H%M%S_%f')
NEW=['TGLExt.TheAngleReachesTheMetric','TGLExt.AuditMetricAngle']
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_bytes())
def ck(r):assert pin(Path(r['path']))==r,r
def save(p,d,text=False):
 assert p.resolve().is_relative_to(OUT.resolve())
 b=d.encode('utf8') if text else (json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf8')
 if p.exists():
  old=p.read_bytes();bk=p.with_name(p.name+'.bak_'+STAMP);bk.write_bytes(old);assert bk.read_bytes()==old
 tmp=p.with_name(p.name+'.tmp_'+STAMP)
 with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
 assert tmp.read_bytes()==b;os.replace(tmp,p)
def norm(x):return re.sub(r'\.\{[^}]*\}','',x).strip()
def axioms(text):
 out={}
 for m in re.finditer(r"'(.+?)'\s+(?:depends on axioms:\s*\[([^]]*)\]|(does not depend on any axioms))",text,re.S):
  n=norm(m.group(1));v=[] if m.group(3) else [norm(x) for x in m.group(2).split(',') if x.strip()]
  assert n not in out or out[n]==v;out[n]=v
 return out
ptr=load(OUT/'B5_SNAPSHOT_POINTER.json');ck(ptr['snapshot']);A=Path(ptr['attempt']);snap=load(Path(ptr['snapshot']['path']))
completion=load(A/'completion.json');assert completion['status']=='BUILD_RC0__REVIEW_PENDING'
ck(completion['run']);run=load(A/'run.json');assert run['returncode']==0
for p in run['streams']+run['executables']+snap['protected_before']+snap['documents']+snap['source_configs']+[snap['own_auditor'],snap['inherited_B4_compilation']]:ck(p)
for r in snap['sources']:ck(r['source']);ck(r['copy'])
for r in snap['inherited_project_objects']:ck(r['object']);ck(r['trace'])
targets=snap['targets'];assert len(targets)==len(set(targets))==4
tracepath=BUILD/'TGLExt/ReviewMetricAngle.trace';trace=load(tracepath);ax={};types={}
for log in trace['log']:
 assert log.get('level') not in ['error','warning'],log
 if log.get('level')!='info':continue
 text=log['message']
 if 'depends on axioms:' in text or 'does not depend on any axioms' in text:ax.update(axioms(text))
 else:
  text=re.sub(r'^.*?\.lean:\d+:\d+:\s*','',text,count=1)
  for t in targets:
   if re.match(re.escape(t)+r'(?:\.\{[^}]*\})?(?:\s|$)',text):
    assert t not in types,t;types[t]=text
assert set(ax)==set(types)==set(targets)
assert all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in ax.values())
assert axioms('\n'.join(x['message'] for x in load(BUILD/'TGLExt/AuditMetricAngle.trace')['log'] if x.get('level')=='info'))==ax
objects=[];warnings=[]
for mod in NEW+['TGLExt.ReviewMetricAngle']:
 p=BUILD/(mod.replace('.','/')+'.olean');tp=p.with_suffix('.trace');tr=load(tp)
 for log in tr['log']:
  assert log.get('level')!='error',log
  if log.get('level')=='warning':warnings.append(log)
  if log.get('level')=='trace' and 'LEAN_PATH=' in log.get('message',''):
   search=log['message'].split('LEAN_PATH=',1)[1].split(' c:',1)[0]
   assert str(R/'kernel'/'.lake') not in search and str(R/'r'/'.lake') not in search and 'V351' not in search
 author=R/'kernel'/'.lake/build/lib/lean'/p.relative_to(BUILD)
 ob=dict(module=mod,own=pin(p),trace=pin(tp),author=None,equal_to_author=None)
 if mod in NEW:ob['author']=pin(author);ob['equal_to_author']=ob['own']['sha256']==ob['author']['sha256'];assert ob['equal_to_author']
 objects.append(ob)
assert not warnings
allobjects=[p for p in BUILD.rglob('*.olean') if p.relative_to(BUILD).parts[0] in ['TGL','TGLExt']]
assert len(allobjects)==120
aupath=R/'AUDITORIA_B5.json';au=load(aupath)
for p in au['sources']+au['objects']+[au['positive_build']]:ck(p)
arun=load(Path(au['positive_build']['path']));assert arun['returncode']==0
for x in arun['snapshots']:assert pin(Path(x['path']))['sha256']==x['sha256']==pin(Path(x['snapshot']))['sha256']
assert au['axioms']==ax and {r['name'] for r in au['targets']}==set(targets)
controls=[]
for c in au['commands']:
 for key in ['source','stdout','stderr']:ck(c[key])
 text=Path(c['stdout']['path']).read_text(encoding='utf8')
 if c['label']=='AuditMetricAngle':assert c['returncode']==0 and axioms(text)==ax
 else:
  assert c['returncode']!=0 and 'type mismatch' in text.lower()
  assert not any(v in text.lower() for v in ['unknown module','unknown identifier','unexpected token','unexpected identifier','object file'])
 controls.append(dict(**c,review_scope='Author execution; source/raw streams reread independently, not re-executed'))
fiche=load(R/'REAPROVEITAMENTO_B5.json');providers=[]
for pr in fiche['providers']:
 p=Path(pr['path']);assert pin(p)['sha256']==pr['sha256']
 line=p.read_text(encoding='utf-8-sig').splitlines()[pr['line']-1];assert pr['name'] in line,(pr['name'],line)
 providers.append(dict(**pr,line_read=line))
chronology=[]
for p in [R/'REAPROVEITAMENTO_B5.md',R/'REAPROVEITAMENTO_B5.json']+[Path(x['source']['path']) for x in snap['sources'] if x['module'] in NEW]:
 st=p.stat();chronology.append(dict(file=pin(p),created_local=datetime.fromtimestamp(st.st_ctime).astimezone().isoformat(),modified_local=datetime.fromtimestamp(st.st_mtime).astimezone().isoformat()))
precedes=all((R/'REAPROVEITAMENTO_B5.json').stat().st_mtime<Path(x['source']['path']).stat().st_ctime for x in snap['sources'] if x['module'] in NEW);assert precedes
order=R.parent/'TUNEL/PARA_CHATGPT/ORDEM_012_a_passagem_da_acao_a_metrica.md';lines=order.read_text(encoding='utf-8-sig').splitlines()
contract=dict(order=pin(order),lines='143-147',excerpt='\n'.join(lines[142:147]),fiche=[pin(R/'REAPROVEITAMENTO_B5.md'),pin(R/'REAPROVEITAMENTO_B5.json')],providers=providers,chronology=chronology,fiche_before_sources_by_filesystem_metadata=precedes,consumer_scope='Fiche-only proposed Python locators; no runtime, data or um.py inspection/execution',search_scope='Existing searches read; no new exhaustive search')
save(A/'contract_and_fiche.json',contract)
sem=dict(status='Four rewrite corollaries, no additional physical or differential input',
 coupling_eq_sin_sq='Actual B1 c.reflection_weight.symm is composed with SMatrix.normSq_reflection at the same thetaMiguel c.beta, giving probability sin squared, not amplitude sin.',
 the_angle_reaches_the_metric='Unfolds entropyFactor and rewrites only c.beta; real w is arbitrary and its absolute value is retained. No angle definition, free angle parameter or numeric coupling added.',
 the_passage='Uses the same B4 HubbleHorizonInput H t G (entropyFactor c w) enthalpy and actual tgl_second_friedmann_from_clausius. The negative 4piG coefficient and input prescriptions remain.',
 the_angle_reads_sector_first='Invokes B3 aggregate tgl_friedmann_from_sector_closure, extracts its first conjunct and rewrites beta. Same finite SectorFluid/H_nx, smooth positive scale factor, U open/preconnected, time domain, G>0, rhoTot>0, enthalpy>=0, explicit H_null and existential Lambda retained.',
 nonvacuity='Inherits the prior conditional theorem domains without a new hypothesis equal to the desired conclusion; no existence/calibration theorem newly claimed.',
 two_regimes='Angular identity reads the existing scalar factor. No angular law of evolution, UV behavior, transport limit, or source is constructed. No insertion in r_s/D_M/l_A/H(z) runtime.',
 scope='B5 source/auditor only; no comparison beyond B4, route selection, empirical test, A1 or integration.',findings=[])
save(A/'semantic_inspection.json',sem)
stamp=datetime.now().astimezone().isoformat()
compilation=dict(timestamp=stamp,status='INDEPENDENT_B5_LAKE_RC0',all_accepted_builds_exit_zero=True,all_attempts_exit_zero=True,all_attempts_scope='B5 Lake only',run=pin(A/'run.json'),runs=[dict(label='B5',run=pin(A/'run.json'),returncode=0)],source_snapshot=ptr['snapshot'],targets={t:dict(typecheck=types[t],axioms=ax[t]) for t in targets},exact_target_count=4,theorems=4,definitions=0,structures=0,all_axioms_allowed=True,all_target_typechecks_present=True,auditor_trace=pin(tracepath),objects=objects,new_project_object_count=3,private_project_object_count=len(allobjects),inherited_B4_compilation=snap['inherited_B4_compilation'],inherited_project_objects=snap['inherited_project_objects'],inherited_project_objects_unchanged=True,new_warnings=[],author_project_objects_copied=False,cache_inheritance=snap['cache_inheritance'],prior_protected_unchanged=True,protected_pins=snap['protected_before'])
save(OUT/'compilation.json',compilation)
evidence=dict(timestamp=stamp,status='B5_DEV_REVIEW_ACCEPTED__INTEGRATION_NOT_REVIEWED',marker='B5_DEV_REVIEW',P0=[],P1=[],P2=[],findings=[],compilation=pin(OUT/'compilation.json'),run=pin(A/'run.json'),semantic_inspection=pin(A/'semantic_inspection.json'),semantic=sem,contract_and_fiche=pin(A/'contract_and_fiche.json'),source_snapshot=ptr['snapshot'],author_audit=pin(aupath),author_positive_build=au['positive_build'],author_commands=controls,author_baseline_941_preservation='Author audit read as DECLARADO; no new broad baseline/um.py scan',new_source_object_pins=[dict(source=next(r['source'] for r in snap['sources'] if r['module']==o['module']),**o) for o in objects if o['module'] in NEW],protected_prior_reports=snap['protected_before'],prior_unchanged=True,scope='B5 rewrite-only: four theorems, no new definitions/data. No integration, B6, physical calibration or source edits.')
save(OUT/'REVIEW_B5_FINAL.json',evidence)
table='\n'.join('| '+o['module'].split('.')[-1]+' | `'+next(r['source']['sha256'] for r in snap['sources'] if r['module']==o['module'])+'` | `'+o['own']['sha256']+'` |' for o in objects if o['module'] in NEW)
md=f'''# B5 — revisão independente final

{stamp} · **B5_DEV_REVIEW**

[REAL] **Aceito no escopo B5, sem P0–P2.** Fonte e auditor lidos integralmente, ficha confrontada e reprodução Lake própria rc0. **Quatro teoremas**, sem nova definição ou estrutura; `#check` com universos e `#print axioms` próprios contêm apenas `propext`, `Classical.choice`, `Quot.sound`. Nenhum aviso novo; os dois .oleans finais são byte a byte iguais aos autorais.

## Conteúdo efetivo

- `coupling_eq_sin_sq` compõe **a mesma** `c.reflection_weight` de B1 com `normSq_reflection`. Prova `c.beta=sin(thetaMiguel c.beta)²`, sem trocar probabilidade por amplitude ou usar um J/ângulo homônimo.
- `the_angle_reaches_the_metric` apenas desdobra `entropyFactor` e substitui beta. Mantém `|1+w|`; não introduz theta como parâmetro independente, numeral beta/alpha, fonte ou hipótese dinâmica.
- `the_passage` aplica efetivamente a segunda equação de B4 ao mesmo `HubbleHorizonInput`; suas hipóteses físicas explícitas, H>0, G>0, fator positivo e sinal **−4piG** permanecem. O ângulo só reescreve o fator.
- `the_angle_reads_sector_first` chama o agregado B3, extrai a primeira equação e reescreve beta. Conserva **H_nx**, H_null, U aberto/preconexo, a suave/positivo, tempo em I, G>0, rhoTot>0, entalpia≥0 e **a constante Λ existencial**, com termo −Λ/3. Não presume a conclusão escalar como premissa.

Isso cumpre B5 como leitura da equação já demonstrada. Nenhum conteúdo de fundo adicional, evolução angular, limite ou escolha entre rotas é provado. Não houve alteração de runtime nem inserção angular em r_s/D_M/l_A/H(z); nenhuma integração desses consumidores foi revisada.

## Reprodução e limites

Raiz curta: `{S}`. Comando próprio: `lake build TGLExt.TheAngleReachesTheMetric TGLExt.AuditMetricAngle TGLExt.ReviewMetricAngle`. Run: `{A/'run.json'}`. Mesma Lean 4.31.0 pinada. Só as duas fontes B5 foram copiadas em bytes, mais auditor próprio novo; nenhum objeto de projeto autoral herdado. **Três novos objetos; 117 objetos próprios anteriores e suas traces preservados; total privado 120.** Relatórios/compilations e demais pins protegidos B1–B4 permaneceram idênticos.

Mathlib e oito pacotes auxiliares são o cache privado anteriormente pinado; não recompilados nesta revisão. LEAN_PATH não contém build autoral. A proveniência e hashes do cache/toolchain, fontes, objetos, traces e relatórios anteriores estão ligados no JSON de compilação. Nenhuma falha nesta execução Lake B5.

Ficha MD/JSON lida inteira e cinco fornecedores conferidos por hash/linha. Metadados locais medidos colocam a ficha antes das fontes; não se alega selo externo de tempo. A cláusula B5 da ORDEM 012 (linhas 143–147) é atendida como reescrita, com a distinção dos dois regimes preservada. Buscas antigas apenas lidas, sem alegação de exaustividade. Consumidores Python continuam propostos na ficha, não instalados por esta revisão.

`AUDITORIA_B5.json`, fontes e streams foram relidos: **BadAngleAmplitude** troca sin² por sin e **BadAngleFactor** omite o termo unitário. Os dois são recusados por Type mismatch com imports funcionando. São execuções autorais conferidas, não novos testes meus. O mapa autoral de quatro axiomas coincide com o próprio. A preservação de 941 fontes/um é [DECLARADO] no auditor autoral; não se repetiu inventário amplo.

## Pins e artefatos

| Arquivo | SHA256 fonte | SHA256 .olean próprio = autor |
|---|---|---|
{table}

- [Revisão JSON](<{(OUT/'REVIEW_B5_FINAL.json').as_posix()}>) — `{pin(OUT/'REVIEW_B5_FINAL.json')['sha256']}`.
- [Compilação própria](<{(OUT/'compilation.json').as_posix()}>) — `{pin(OUT/'compilation.json')['sha256']}`.
- [Run rc0](<{(A/'run.json').as_posix()}>) — `{pin(A/'run.json')['sha256']}`.
- [Snapshot](<{(A/'snapshot.json').as_posix()}>) — `{pin(A/'snapshot.json')['sha256']}`.
- [Tipos/semântica](<{(A/'semantic_inspection.json').as_posix()}>) e [ficha/contrato](<{(A/'contract_and_fiche.json').as_posix()}>).

**Escopo DEV B5 encerrado.** Não resta análise ou recompilação deste delta. Sem aceite de integração, B6, A1, gate, dados, calibração física ou confirmação empírica. Fontes autorais, memórias e revisões anteriores não foram alteradas.
'''
save(OUT/'REVIEW_B5_FINAL.md',md,True)
print(json.dumps(dict(status=evidence['status'],P0=[],P1=[],P2=[],report=pin(OUT/'REVIEW_B5_FINAL.md'),json=pin(OUT/'REVIEW_B5_FINAL.json'),compilation=pin(OUT/'compilation.json'),run=pin(A/'run.json')),ensure_ascii=False,indent=2))
