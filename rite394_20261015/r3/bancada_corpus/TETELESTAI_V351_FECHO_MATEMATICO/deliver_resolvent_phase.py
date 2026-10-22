from pathlib import Path
import json,hashlib,datetime,re,os,sys
R=Path(__file__).absolute().parent
OUT=R.parent/'TUNEL/DO_CHATGPT'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def new(p,data):
 assert not p.exists(),p
 if isinstance(data,str):data=data.encode('utf8')
 q=p.with_name(p.name+'.tmp');q.write_bytes(data)
 assert q.read_bytes()==data and data
 os.replace(q,p)
def pin(p):return dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p))
def jsnew(p,d):new(p,json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ap=R/'AUDITORIA_A1_POTENCIAS_IMAGINARIAS.json';a=json.loads(ap.read_bytes())
reviewp=R/'revisao/REVIEW_A1_FASE_RESOLVENTE_FINAL.json'
reportp=reviewp.with_suffix('.md')
rr=json.loads(reviewp.read_bytes())
assert rr['P0']==rr['P1']==rr['P2']==0 and rr['findings']==[]
compath=Path(sys.argv[1]);assert compath.is_relative_to(R/'revisao')
assert str(compath)==rr['compilation']['path'] and sha(compath)==rr['compilation']['sha256']
assert sha(reportp)==rr['report']['sha256']
c=json.loads(compath.read_bytes())
assert c['all_exit_zero'] and c['exact_targets']==39 and c['trio_only']
assert c['all_binary_byte_equal_to_author'] and c['pins_preserved']
assert c['independent_module_compilations']==5 and c['independent_auditors']==1
assert not c['new_module_bytes_imported_from_author_build'] and not c['project_author_build_in_lean_path']
files=[ap,reviewp,reportp,compath,Path(__file__).absolute(),R/'audit_resolvent_phase.py',
 R/'prepare_resolvent_phase.py',R/'compile_a1.py',R/'ADENDO_A1_POTENCIAS_IMAGINARIAS.md',
 R/'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.md',R/'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json',
 R/'BUSCA_A1_FASE_RESOLVENTE.txt',R/'DEPENDENCIAS_A1_FASE_RESOLVENTE.json',
 R/'ADENDO_REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json',R/'document_resolvent_phase_types.py',
 R/'CUSTODIA_A1_FUNCIONAIS_CANONICO_ATUAL.json',
 R/'revisao/CONSULTA_A1_IMPLEMENTACAO_MODULAR_MESMO_GNS.md',R/'revisao/CONSULTA_A1_IMPLEMENTACAO_MODULAR_MESMO_GNS.json']
total_thm=0;total_def=0;failed=[]
for m in a['modules']:
 src=Path(m['source']);obj=Path(m['object'])
 assert sha(src)==m['source_sha256'] and sha(obj)==m['object_sha256']
 assert any(cr['object']['sha256']==sha(obj) and cr['source']['sha256']==sha(src) for cr in c['modules'])
 text=src.read_text(encoding='utf8');total_thm+=len(re.findall(r'^theorem ',text,re.M));total_def+=len(re.findall(r'^def ',text,re.M))
 files.extend([src,obj])
 stems={m['module'],m['module']+'Rejected'}
 for folder in sorted((R/'attempts').iterdir()):
  snaps=[p for p in folder.glob('*.lean') if p.stem in stems]
  if not snaps or not (folder/'run.json').exists():continue
  run=json.loads((folder/'run.json').read_bytes());files+=snaps+[folder/'run.json',folder/'stdout.txt',folder/'stderr.txt']
  if run['returncode']!=0:failed.append(dict(attempt=str(folder),returncode=run['returncode'],source_sha256=run['source_sha256'],accepted=False))
assert total_thm+total_def==a['checked_declarations']==39
for n in a['negatives']:
 p=Path(n['probe']);assert sha(p)==n['sha256'] and n['returncode']!=0 and n['real_elaboration_failure']
 files.extend([p,p.with_suffix('.stdout.txt'),p.with_suffix('.stderr.txt')])
for prev in a['prior_manifests_verified']:
 p=Path(prev['path']);assert sha(p)==prev['sha256']
 for f in json.loads(p.read_bytes())['files']:assert sha(Path(f['path']))==f['sha256']
 files.append(p)
# Own independent evidence is pinned. Reused old binary copies remain covered by its manifest.
files += [p for p in compath.parent.iterdir() if p.is_file()]
files += [p for p in (compath.parent/'author_final').rglob('*') if p.is_file()]
for m in a['modules']:
 files += [compath.parent/'kernel/TGLExt'/(m['module']+'.lean'),compath.parent/'build/TGLExt'/(m['module']+'.olean')]
files += [compath.parent/'kernel/AuditResolventPhase39.lean',compath.parent/'build/AuditResolventPhase39.olean']
dp=R/'DEPENDENCIAS_A1_FASE_RESOLVENTE.json';deps=json.loads(dp.read_bytes())
for d in deps:assert sha(Path(d['source']))==d['source_sha256'] and sha(Path(d['object']))==d['object_sha256']
assert sha(Path(a['program']['path']))==a['program']['sha256']
stamp=datetime.datetime.now().astimezone().isoformat()
unique={str(p):p for p in files}
manifest=dict(timestamp=stamp,status='ACTUAL_TOMITA_IMAGINARY_GROUP_VERIFIED__MODULAR_ACTION_AND_A1B_OPEN',goal='ACTIVE',
 acceptance={'a':'PAGO_ANTERIOR_PRESERVADO','b':'NAO_PAGO','c':'PAGO_NESTAS_39_DECLARACOES'},
 modules=a['modules'],declarations=39,theorems=total_thm,definitions=total_def,
 independent_review=pin(reviewp),independent_compilation=pin(compath),negative_controls=2,
 inherited_dependency_pairs=len(deps),failed_attempts=failed,program=a['program'],
 canonical_custody='Snapshot dated in CUSTODIA_A1_FUNCIONAIS_CANONICO_ATUAL.json; not remeasured here; no current byte equality claimed.',
 files=[pin(p) for _,p in sorted(unique.items())])
mp=R/'MANIFESTO_A1_POTENCIAS_IMAGINARIAS.json';jsnew(mp,manifest)
text='''[REAL — grupo unitário fortemente contínuo do mesmo S* S verificado; OPEN — ação modular e A1(b), traço, ainda não quitados]

# Entrega 011 · A1 — potências imaginárias do Tomita do peso concreto

Responde à ORDEM_011, apenas A1. Incorporação é da gerência; este delta não acende bandeiras de realização completa e não move o gate.

| Critério | Estado | Evidência |
|---|---|---|
| A1(a), contrato forte e recusa do zero | PAGO, preservado | manifestos anteriores reconferidos |
| A1(b), habitante concreto ou impossibilidade tipada | NÃO PAGO | falta identificar a ação modular, construir gerador positivo e traço |
| A1(c), axiomas | PAGO no delta | 39 declarações no trio, reprodução independente |

'''
text+='Data: '+stamp+'\n\n'+(R/'ADENDO_A1_POTENCIAS_IMAGINARIAS.md').read_text(encoding='utf8')
text+='\n\n## Revisão e arquivos\n\n'
text+=f'Reprodução independente concluída: cinco compilações e auditor próprio das 39 declarações, objetos idênticos, sem avisos, nenhum P0/P1/P2. Parecer: `{reportp}`. JSON: `{reviewp}`, SHA256 `{sha(reviewp)}`. Compilação: `{compath}`, SHA256 `{sha(compath)}`. Foram herdados e conferidos {len(deps)} pares de dependências; não foram todos recompilados.\n\n'
for m in a['modules']:
 text+=f"- `{m['source']}` — SHA256 `{m['source_sha256']}`; objeto `{m['object_sha256']}`; {len(m['declarations'])} declarações; execução `{m['attempt']}`.\n"
text+=f'\nManifesto `{mp}` — SHA256 `{sha(mp)}`. Total: {total_thm} teoremas e {total_def} definições. As fontes finais estão congeladas; todos os hashes vêm dos bytes efetivos.\n'
text+='\n## Reprodução\n\n```powershell\n'
for m in a['modules']:
 text+=f"& C:\\Python314\\python.exe -X utf8 -B '{R/'compile_a1.py'}' kernel/TGLExt/{m['module']}.lean\n"
text+='```\n\nEssa ordem respeita os imports. O compilador cria tentativas novas; os scripts de registro são de execução única. Para os dois controles em probes/TGLExt, o resultado esperado é rc1 por erro matemático de elaboração, sem falha de import. Axiomas de todas as declarações aceitas: propext, Classical.choice, Quot.sound.\n'
text+='\n## Escopo de custódia\n\nA cópia local do monólito permaneceu intacta; não foi executada. Não houve nova rodada integral porque só módulos Lean foram produzidos. O canônico já havia mudado externamente na leitura datada de CUSTODIA_A1_FUNCIONAIS_CANONICO_ATUAL.json; naquele confronto os 922 fontes embutidos coincidiam. Essa leitura não é uma afirmação de versão corrente nem igualdade atual dos monólitos. Aplicar as fontes sobre a versão corrente após auditoria da gerência.\n'
text+='\n## Ficha de aproveitamento anexa\n\n'+(R/'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.md').read_text(encoding='utf8')
text+='\n```json\n'+(R/'REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json').read_text(encoding='utf8')+'\n```\n'
text+='\nEnunciados completos dos fornecedores, em suplemento documental datado posterior ao código (a ficha original anterior permanece intacta):\n\n```json\n'+(R/'ADENDO_REAPROVEITAMENTO_A1_FASE_RESOLVENTE.json').read_text(encoding='utf8')+'\n```\n'
dest=OUT/'ENTREGA_011_A1_potencias_imaginarias_mesmo_tomita.md';new(dest,text)
for f in manifest['files']:assert sha(Path(f['path']))==f['sha256'] and Path(f['path']).stat().st_size==f['bytes']
receipt=dict(timestamp=stamp,status='DELIVERED_PARTIAL__GOAL_ACTIVE',delivery=pin(dest),manifest=pin(mp),verified_files=len(manifest['files']),declarations=39,theorems=total_thm,definitions=total_def,acceptance=manifest['acceptance'])
jsnew(R/'RECIBO_A1_POTENCIAS_IMAGINARIAS.json',receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))
