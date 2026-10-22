"""Consolidate measured receipts after a completed build; never import/execute um.py."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
BASE=Path(r'C:\IALD\Central de Patentes\Chatgpt')
OUT=Path(__file__).resolve().parent
WORK=BASE/'INTEGRADOR_LOCAL_GERAL_20260909_170426_647362'
BUILD=WORK/'BUILD_SUCCESSOR_20260909_171052_146967'
COPY=BASE/'COPIA_INTEGRADA_20260909_170914_653192'
AUDIT=BASE/'AUDITORIA_INTEGRACAO_72_20260909_171311_522844'/'AUDITORIA_INTEGRACAO_72.json'
ARAKI=BASE/'ESTADO_ARAKI_20260909'
REVIEW=BASE/'REVISAO_FINAL_ARAKI_20260909_170730_304080'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def record(p):
    b=p.read_bytes()
    return dict(path=p.as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def new(p,b):
    assert p.resolve().is_relative_to(BASE) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True)
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:
        f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b
    os.rename(t,p)
    assert p.read_bytes()==b
def write_json(p,x):new(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def link(label,p):return '['+label+'](<'+p.as_posix()+'>)'
result_path=BUILD/'TRANSPOSED_RESULT.json'
result=read(result_path)
plan_path=BUILD/'BUILD_PLAN.json'
plan=read(plan_path)
static=read(AUDIT)
integration_path=COPY/'INTEGRATION_RESULT.json'
integration=read(integration_path)
config_path=WORK/'CONFIG_NOVE_APROVADA.json'
config=read(config_path)
assert result['status']=='PASS_TRANSPOSED_SCOPE'
assert result['plan']==record(plan_path)
assert result['input_boundary_unchanged'] and result['cached_boundary_unchanged']
assert len(result['runs'])==12 and all(r['valid'] and r['exit_code']==0 and r['warning_lines']==0 for r in result['runs'])
assert all(set(row['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in result['runs'] for row in r['axiom_rows'])
assert static['status']=='PASS_STATIC_INTEGRATION_SCOPE'
assert static['counts']['checks']==static['counts']['passed_checks'] and not static['failed_checks']
assert result['counts']==plan['counts']
assert static['counts']['total']==plan['counts']['all_declarations']
assert plan['integrated_copy']==integration['integrated_copy']==record(COPY/'um.py')
canonical=Path(static['current_canonical']['path'])
assert record(canonical)==static['current_canonical'], 'Canonical changed; reexamination must be rebased.'
assert integration['source_um']==record(Path(integration['source_um']['path']))
rows={r['module']:r for r in result['runs']}
assert len(rows['NewModulesAudit']['axiom_rows'])==plan['counts']['all_declarations']
boundary=[record(canonical),record(COPY/'um.py'),record(AUDIT),record(result_path),record(plan_path),
    record(OUT/'REEXAME_ATUALIZADO.md'),record(ARAKI/'DEDUCAO_ESTADO_PERTURBADO_ARAKI.md')]
inventory=[]
for m in integration['modules']:
    source=Path(m['source']['path'])
    assert record(source)==m['source']
    conf=next(c for c in config['modules'] if Path(c['source'])==source)
    receipt=Path(conf['build_result'])
    individual=read(receipt)
    assert record(receipt)['sha256']==conf['build_result_sha256']
    assert individual['status']=='PASS_COMPILED_SCOPE'
    assert m['source'] in individual['sources']
    boundary.extend([record(source),record(receipt)])
    inventory.append(dict(module=m['module'],source=record(source),individual_receipt=record(receipt),
        transposed_source=record(BUILD/m['key']),
        transposed_binary=record((BUILD/m['key']).with_suffix('.olean')),
        theorems=sum(d['kind']=='theorem' for d in m['declarations']),
        other_declarations=sum(d['kind']!='theorem' for d in m['declarations']),
        fresh_joint_run=rows[m['module']]))
delta_t=sum(m['theorems'] for m in inventory)
delta_o=sum(m['other_declarations'] for m in inventory)
assert len(inventory)==9 and delta_t==116 and delta_o==22
assert all(record(Path(r['path']))==r for r in boundary)
write_json(OUT/'INVENTARIO_NOVE_FONTES.json',dict(new_modules=len(inventory),theorems=delta_t,
    other_declarations=delta_o,modules=inventory))
counts=plan['counts']
full_rows=len(rows['FullTGLAudit']['axiom_rows'])
text=f'''# Validação e incorporação — entrega 061

09/09/2026. **[REAL] PASS da compilação conjunta: 12/12 processos**, sendo nove folhas novas, raiz TGLExt e duas auditorias. Zero avisos; axiomas restritos a propext, Classical.choice e Quot.sound. A auditoria dedicada verificou {counts['all_declarations']} declarações, incluindo sete instâncias nomeadas; FullTGLAudit emitiu {full_rows} linhas de axiomas.

O lote novo contém {delta_t} teoremas e {delta_o} outras declarações. A cópia cumulativa contém {counts['total_modules']} módulos da bancada, {counts['theorems']} teoremas e {counts['other_declarations']} outras declarações. A auditoria estática independente aprovou {static['counts']['passed_checks']}/{static['counts']['checks']} verificações.

## Artefato para a sessão que mantém o programa

{link('Cópia integrada do um.py',COPY/'um.py')}: {record(COPY/'um.py')['bytes']} bytes, SHA-256 `{record(COPY/'um.py')['sha256']}`.

O `um_ORIGINAL_SNAPSHOT.py` desta nova pasta é a cópia63 predecessora preservada byte a byte. A cadeia até o canônico foi conferida separadamente: {static['current_canonical']['bytes']} bytes, SHA-256 `{static['current_canonical']['sha256']}`. O canônico atual continuou igual no fechamento desta entrega.

Somente fontes embutidas, imports da raiz e auditoria receberam acréscimos. Código fora da tabela, flags, sentinelas e gate foram preservados. Não há novas flags JSON individuais. Nenhum `um.py`, original ou cópia, foi executado ou importado.

## Aplicação de Araki para incorporação

{link('Dedução matemática',ARAKI/'DEDUCAO_ESTADO_PERTURBADO_ARAKI.md')} e {link('parecer independente final',REVIEW/'PARECER_FINAL_ARAKI.md')} distinguem a prova Lean de unicidade/fase central da aplicação DERIVED + KNOWN da perturbação limitada. Registrar explicitamente o estado, Z, o sinal, a fase de Connes e KMS com esse estatuto. Não converter a importação documentada em novo axioma Lean nem em alegação de construtor analítico já formalizado.

A nova cópia embute as nove folhas; não implementa um construtor analítico novo de Araki, nem emite uma nova rodada física. A execução do programa e a incorporação canônica seguem com a sessão autorizada que mantém o acervo. Se a base avançar, refazer o delta sobre a nova base antes de incorporar.

## Escopo dos binários reutilizados

Os 63 módulos anteriores foram reutilizados do PASS anterior após igualdade exata das fontes e conferência da proveniência. Essa proveniência é composta: 18 módulos então compilados e 45 já reutilizados de outro PASS. Os hashes atuais dos binários foram medidos na reutilização e os pins históricos disponíveis foram comparados. Não se afirma que todos os binários tinham hash registrado na compilação original.

A raiz e as duas auditorias foram recompiladas carregando o conjunto de 72 módulos. Dependências canônicas e Mathlib existentes não foram integralmente recompiladas; não se afirma hash de toda dependência transitiva externa. As fronteiras declaradas de entrada e cache permaneceram iguais antes e depois. Nenhuma tentativa FAIL anterior foi contada como PASS.

{link('Recibo da compilação conjunta',result_path)} · {link('Auditoria estática independente',AUDIT)} · {link('Inventário das nove fontes',OUT/'INVENTARIO_NOVE_FONTES.json')}.
'''
new(OUT/'VALIDACAO_E_INCORPORACAO.md',text.encode('utf-8'))
consolidated=dict(status='PASS_CONSOLIDATED_SCOPE',created_utc=datetime.now(timezone.utc).isoformat(),
    canonical=record(canonical),integrated_copy=record(COPY/'um.py'),integration_result=record(integration_path),
    joint_build=record(result_path),joint_plan=record(plan_path),static_audit=record(AUDIT),
    counts=counts,delta=dict(modules=9,theorems=delta_t,other_declarations=delta_o),
    full_audit_rows=full_rows,dedicated_audit_rows=len(rows['NewModulesAudit']['axiom_rows']),
    reexamination=record(OUT/'REEXAME_ATUALIZADO.md'),validation=record(OUT/'VALIDACAO_E_INCORPORACAO.md'),
    inventory=record(OUT/'INVENTARIO_NOVE_FONTES.json'),
    araki_deduction=record(ARAKI/'DEDUCAO_ESTADO_PERTURBADO_ARAKI.md'),
    araki_leaf_manifest=record(ARAKI/'MANIFESTO_ESTADO_ARAKI.json'),
    araki_independent_review=record(REVIEW/'PARECER_FINAL_ARAKI.md'),
    araki_review_evidence=record(REVIEW/'EVIDENCIA_REVISAO_FINAL.json'),
    evidence_boundary=boundary,um_py_executed_or_imported=False,canonical_changes=False,
    all_transitive_dependencies_rebuilt=False,all_transitive_dependencies_hashed=False,
    araki_analytic_constructor_fully_formalized=False,empirical_rites_rerun=False,
    quantum_gravity_confirmed_or_resolved_claim=False)
write_json(OUT/'RECIBO_CONSOLIDADO.json',consolidated)
tunnel=BASE/'TUNEL'/'DO_CHATGPT'/'ENTREGA_061_ESPONTANEA_estado_Araki_interacao_geral_atlas_suave.md'
assert not tunnel.exists(), 'Delivery slot occupied; inspect rather than overwrite.'
delivery=f'''# Entrega 061 — estado perturbado, interação geral e atlas suave

09/09/2026. Base canônica v337 novamente conferida em leitura. A bancada acrescenta nove módulos: **116 teoremas + 22 outras declarações**. Cópia cumulativa72: **972 teoremas + 264 outras declarações**, sete instâncias nomeadas.

**[REAL]** PASS conjunto12/12, sem avisos: nove folhas, raiz e duas auditorias. Dedicado1236termos; FullTGLAudit{full_rows}linhas. **[REAL]** Auditoria independente {static['counts']['passed_checks']}/{static['counts']['checks']}. O cache63 e o alcance das dependências estão descritos no recibo; não é uma recompilação integral de toda a árvore.

**[REAL]** A interação local somável admite termos não comutativos, com testemunha explícita. Unicidade: mesmo potencial sse mesmo cociclo. A fase central Z^(−it) preserva a dinâmica e muda o gerador para i(V−logZ·I). A colagem suave selecionada deriva a transformação de Einstein dos dados de transição e conclui Λ global único sob suas hipóteses.

**[DERIVED + KNOWN]** A existência do estado fiel normal e sua identificação modular/KMS para a classe local construída estão justificadas pela aplicação precisa de Araki. A estimativa em norma liga o expansional ao cociclo real da bancada. O construtor analítico de Araki não foi introduzido como axioma ou apresentado como nova implementação Lean.

**Pendências atualizadas:** correspondência física seletor–registro; realização de matéria/conservação/área para os mesmos dados; atlas físico compatível; extensão além da classe globalmente limitada, anomalias e UV. O lote geométrico usa Levi-Civita sem torção. Não reabrir JS, H3/tela fundada, injetividade ou os falsificadores já existentes por desatualização.

{link('Reexame completo',OUT/'REEXAME_ATUALIZADO.md')}

{link('Dedução para incorporação de Araki',ARAKI/'DEDUCAO_ESTADO_PERTURBADO_ARAKI.md')}

{link('Cópia integrada',COPY/'um.py')}

{link('Validação e instruções de incorporação',OUT/'VALIDACAO_E_INCORPORACAO.md')}

{link('Recibo consolidado',OUT/'RECIBO_CONSOLIDADO.json')}

SHA-256 da cópia integrado medido: `{record(COPY/'um.py')['sha256']}`. Nenhum original, Atlas, índice ou memória canônica foi modificado; nenhum um.py foi executado/importado; nenhum rito físico ou gate foi promovido.
'''
new(tunnel,delivery.encode('utf-8'))
assert all(record(Path(r['path']))==r for r in boundary)
write_json(OUT/'RECIBO_ENTREGA_FINAL.json',dict(status='DELIVERED_061',created_utc=datetime.now(timezone.utc).isoformat(),
    tunnel=record(tunnel),consolidated=record(OUT/'RECIBO_CONSOLIDADO.json'),
    report=record(OUT/'REEXAME_ATUALIZADO.md'),validation=record(OUT/'VALIDACAO_E_INCORPORACAO.md'),
    input_boundary_stable=True))
print(json.dumps(dict(status='DELIVERED_061',copy=record(COPY/'um.py'),counts=counts,
    full_audit_rows=full_rows,report=(OUT/'REEXAME_ATUALIZADO.md').as_posix(),tunnel=tunnel.as_posix()),ensure_ascii=False))
