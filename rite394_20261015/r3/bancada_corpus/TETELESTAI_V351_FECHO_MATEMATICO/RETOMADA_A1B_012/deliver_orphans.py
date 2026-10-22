from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
OUT=R.parent.parent/'TUNEL/DO_CHATGPT/ENTREGA_011_A1_reproducao_sete_fornecedores.md'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load(p):return json.loads(p.read_text(encoding='utf8'))
def put(p,b):
 assert p.is_relative_to(R) or p==OUT
 assert not p.exists(),p
 q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b and b;os.replace(q,p)
a=load(R/'AUDITORIA_ORFAOS_A1B.json');v=load(R/'revisao/REVIEW_A1_ORPHANS_FINAL.json');c=load(Path(v['compilation']['path']));s=load(R/'INSPECAO_PRINCIPAL_ANTIUNITARIOS.json')
assert a['all_axioms_allowed'] and a['negative_controls_rejected'] and a['new_theorems']==0
assert v['status']=='A1_ORPHANS_REPLAY_ACCEPTED__REVIEW_ROLES_SEPARATED__A1_B_OPEN'
assert all(not z[k] for z in [v,s] for k in ['P0','P1','P2'])
assert c['all_accepted_builds_exit_zero'] and c['all_axioms_allowed'] and c['exact_target_count']==40
assert not c['project_objects_inherited'] and not c['project_objects_copied_from_author'] and not c['target_warnings']
assert s['status']=='PRINCIPAL_SEMANTIC_INSPECTION_COMPLETE__STANDALONE_REPLAY_PENDING'
files=set()
def accept(x):
 if isinstance(x,dict):
  if {'path','bytes','sha256'}<=x.keys():
   p=Path(x['path']);assert pin(p)=={k:x[k] for k in ['path','bytes','sha256']},p;files.add(p)
  for q in x.values():accept(q)
 elif isinstance(x,list):
  for q in x:accept(q)
for d in [a,v,c,s]:accept(d)
stamp=datetime.datetime.now().astimezone().isoformat()
approval=dict(timestamp=stamp,status='SEVEN_EXISTING_MODULES_ACCEPTED_WITH_SPLIT_AUTHORSHIP_REVIEW__A1B_TRACE_OPEN',five_scaling_semantic_review=pin(R/'revisao/REVIEW_A1_ORPHANS_FINAL.json'),two_antiunitary_semantic_review=pin(R/'INSPECAO_PRINCIPAL_ANTIUNITARIOS.json'),two_antiunitary_final_acceptance='Principal semantic inspection plus own author cold Lake and sidecar private cold Lake now both rc0; the earlier pending semantic note is preserved without overwrite.',author_audit=pin(R/'AUDITORIA_ORFAOS_A1B.json'),independent_compilation=pin(R/'revisao/compilation.json'),personal_independence='Five scaling modules: sidecar reviewed principal authorship. Two antiunitary modules: principal reviewed sidecar prior authorship. No retrospective independence is claimed for self-replay.',new_theorems=0,gate_changed=False,full_trace_constructed=False)
put(R/'ACEITE_ORFAOS_A1B.json',json.dumps(approval,ensure_ascii=False,indent=2).encode('utf8'));files.add(R/'ACEITE_ORFAOS_A1B.json')
main=[R/n for n in ['REAPROVEITAMENTO_RETORNO_A1B.md','REAPROVEITAMENTO_RETORNO_A1B.json','ALVOS_RETORNO_A1B.json','FONTES_REPLAY.json','CACHE_PROVENIENCIA.json','AUDITORIA_ORFAOS_A1B.json','INSPECAO_PRINCIPAL_ANTIUNITARIOS.md','INSPECAO_PRINCIPAL_ANTIUNITARIOS.json','ACEITE_ORFAOS_A1B.json','revisao/REVIEW_A1_ORPHANS_FINAL.md','revisao/REVIEW_A1_ORPHANS_FINAL.json','revisao/compilation.json','prepare_replay.py','run_replay.py','audit_orphans.py','inspect_antiunitary_principal.py','deliver_orphans.py']]
files.update(main)
for folder in ['attempts/20260914_173309_164705','audit_orphans']:
 files.update(p for p in (R/folder).rglob('*') if p.is_file())
mods='\n'.join(f"| `{m['name']}` | `{m['source']['sha256']}` | `{m['object']['sha256']}` |" for m in a['modules'])
axioms='\n'.join(f"| `{n}` | {', '.join(xs) or 'nenhum'} |" for n,xs in a['axioms'].items())
pins='\n'.join(f"| `{p}` | `{pin(p)['sha256']}` |" for p in main)
diffs=c['target_binary_differences'];binary='Nenhuma diferença binária histórica nos sete objetos comparados pelo revisor.' if not diffs else 'Diferenças binárias em relação aos objetos HISTÓRICOS de OLD/build: '+', '.join(d['module'] for d in diffs)+'. Fontes, tipos e axiomas foram conferidos separadamente; não se afirma reprodução byte a byte desses objetos históricos.'
same_current=sum(d.get('equal_to_author_cold') is True for d in c['target_objects'])
if same_current==0:
 same_current=sum(d.get('equal_to_author_cold') is True for d in diffs)
binary+=f' Na comparação distinta com o Lake autoral NOVO desta retomada, {same_current}/7 objetos coincidem em bytes. A comparação binária com o snapshot V353 está indisponível nos caminhos registrados e não é tratada como igualdade.'
body=f'''[REAL — sete fornecedores existentes reproduzidos por Lake isolado e aceitos com revisão distribuída segundo a autoria. Quarenta declarações existentes; zero teoremas novos. A1(b), traço concreto, permanece OPEN.]

# ENTREGA 011 / A1 — reprodução dos sete fornecedores pendentes

{stamp}

Esta entrega quita a pendência documental e de reprodução dos sete módulos de A1 nomeados na ORDEM012. **Não reescreve matemática já incorporada na v353.** As sete fontes são as mesmas, em bytes, dos19módulos V351 presentes naquele snapshot. A retomada foi aberta depois de RECIBO_B6, em RETOMADA_A1B_012, preservando a bancada B e os artefatos antigos.

## Critérios

| Critério | Resultado |
|---|---|
| Ficha antes da retomada | PAGO; consumidor `regular_dual_weight_modular_implementation`, tipos exatos e fornecedores nomeados. |
| Reaproveitar os sete sem reescrever | PAGO; 36teoremas+4definições=40declarações existentes, zero novos. |
| Lake na raiz isolada | PAGO; autor e revisor recompilaram seus próprios objetos de projeto, rc0. Caches de pacotes explicitados abaixo. |
| Tipos completos e axiomas | PAGO; quarenta #check/#print, subconjuntos do trio. |
| Adulteração recusada | PAGO; duas aplicações adulteradas recusadas por TypeMismatch, sem erro de importação ou timeout no teste aceito. |
| Revisão distinta da autoria | PAGO por divisão explícita: sidecar revê cinco módulos de escala; principal revê dois antiunitários de autoria anterior do sidecar. |
| Habitante RegularCoreTraceData | NÃO PAGO; não é consequência destes sete fornecedores isolados. |
| Integração no um.py ou gate | NÃO EXECUTADA; estes fontes já estavam incorporados, e o programa canônico não foi alterado. |

## Alcance matemático

O cálculo funcional transporta o entrelaçamento de resolventes positivos para suas potências imaginárias. Para r>0, o resolvente escalado é Q_r=T[rI+(1-r)T]⁻¹. O multiplicador de entrelaçamento é limitado e pode ser não invertível; a prova não introduz inversa limitada de T(1-T). A densidade já demonstrada da imagem amortecida permite a extensão por continuidade.

A aplicação concreta usa o mesmo `scalarTomitaResolvent P`, o mesmo `scalarTomitaImaginaryPower P t`, os multiplicadores direitos reais e todo `ScalarGNSHilbert P`. A fase é exp(+it log r). A camada antiunitária fornece **JU_tJ⁻¹=U_t**, com os dois sinais conjugados cancelando; não U_−t. A conjugação é homomorfismo real de *-álgebras, e conjuga os escalares complexos.

Esses resultados não são sozinhos uma identificação de KMS ou da ação em todo o core. O consumo à esquerda e a conjugação no core são deltas posteriores separados. Ainda não há h regular positivo afiliado construído nem a perturbação pelo seu inverso que deve fornecer o traço. A recusa do peso dual como traço permanece válida; não é parede contra existência do traço.

## Reprodução e revisão

Autor: `{a['positive_build']['path']}`. O runner `run_replay.py` executou `lake build TGLExt.AuditA1Orphans` com Lean4.31.0, LEAN_PATH removido, sem objetos TGL/TGLExt externos. As {a['source_copies_reverified']} fontes/configurações originais e copiadas foram reconferidas. Mathlib e oito pacotes vieram de cache privado pinado; a biblioteca não foi recompilada.

Revisor: `{v['run']['path']}`. Recompilação privada de {c['source_project_object_count']} objetos de projeto, sem copiar objetos autorais. Seu auditor tem os quarenta tipos completos e axiomas. Nenhum aviso nos sete alvos nem no auditor; {len(c['existing_supplier_warnings'])} avisos de fornecedores existentes preservados. {binary}

O parecer do sidecar mantém sua ressalva de autoria dos dois antiunitários. **Não o rebatizei como aprovação independente de sua própria obra.** A inspeção semântica do principal está em INSPECAO_PRINCIPAL_ANTIUNITARIOS; o aceite datado ACEITE_ORFAOS_A1B associa essa inspeção às duas reproduções agora concluídas. A nota semântica anterior, que dizia compilação pendente, sobrevive intacta.

Os negativos BadAntiunitaryPhase e BadImaginaryScaling adulteram, respectivamente, a identidade refletida por um fator2 e o sinal da fase escalada. A recusa prova que essas aplicações não fornecem o tipo requerido; não é uma nova demonstração de inexistência de outros operadores. Falhas históricas de compilação do desenvolvimento permanecem fora do conjunto aceito.

## Sete fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
{mods}

## Axiomas das quarenta declarações existentes

| Nome completo | Axiomas |
|---|---|
{axioms}

## Arquivos de entrega

| Arquivo | SHA256 |
|---|---|
{pins}

MANIFESTO_ORFAOS_A1B e RECIBO_ORFAOS_A1B ligam esta entrega aos relatórios, fontes e objetos. A incorporação da gerência e a integração de outros deltas não são simuladas por este documento. Não houve leitura experimental, alteração do D1, criação de sigma, mudança de memórias canônicas ou gate.

## Parecer do sidecar, integral e com sua ressalva

'''+(R/'revisao/REVIEW_A1_ORPHANS_FINAL.md').read_text(encoding='utf8')+'\n\n## Inspeção do principal dos dois antiunitários\n\n'+(R/'INSPECAO_PRINCIPAL_ANTIUNITARIOS.md').read_text(encoding='utf8')+'\n\n## Ficha anterior, integral\n\n'+(R/'REAPROVEITAMENTO_RETORNO_A1B.md').read_text(encoding='utf8')
put(OUT,body.encode('utf8'));files.add(OUT)
m=dict(timestamp=stamp,status=approval['status'],new_theorems=0,files=[pin(p) for p in sorted(files,key=str)])
put(R/'MANIFESTO_ORFAOS_A1B.json',json.dumps(m,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'RECIBO_ORFAOS_A1B.json',json.dumps(dict(timestamp=stamp,delivery=pin(OUT),manifest=pin(R/'MANIFESTO_ORFAOS_A1B.json')),ensure_ascii=False,indent=2).encode('utf8'))
for f in m['files']:assert pin(Path(f['path']))==f
print(json.dumps(dict(delivery=pin(OUT),manifest=pin(R/'MANIFESTO_ORFAOS_A1B.json'),files=len(files)),ensure_ascii=False))
