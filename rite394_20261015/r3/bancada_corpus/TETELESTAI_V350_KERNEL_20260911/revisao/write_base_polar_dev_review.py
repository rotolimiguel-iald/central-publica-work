"""Consolidate completed reviewer builds and publish the bounded DEV verdict only."""
from pathlib import Path
import ast,datetime,hashlib,json,re
REV=Path(__file__).resolve().parent;ROOT=REV.parent
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
link=lambda label,p:'['+label+'](<'+str(p).replace(chr(92),'/')+'>)'
def save(p,b):
 assert p.resolve().is_relative_to(REV)
 assert not p.exists(),p
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b)
 assert t.read_bytes()==b;t.replace(p);assert p.read_bytes()==b
F=load(ROOT/'base_polar_draft_status.json');P=load(ROOT/'matrix_polar_custody.json')
assert len(F['modules'])==4 and len(F['targets'])==19
assert F['parent_custody_sha256']==hf(ROOT/'matrix_polar_custody.json')
assert hf(ROOT/F['report_path'])==F['report_sha256']
assert not any(F[k] for k in ['integrated','gate_changed','KMS_proved','modular_square_flow_identified','full_goal_complete'])
assert all(hf(ROOT/n)==pin for n,pin in P['artifacts'].items())
assert hf(ROOT/'um.py')==F['integrated_working_sha256']==P['working_sha256']
assert all(hf(p)==pin for p,pin in P['review_sha256'].items())
assert all(hf(p)==pin for p,pin in P['surface_sha256'].items())
allowed={'propext','Classical.choice','Quot.sound'}
runs=[];own={};hist=[];axes={}
for pointer in ['level_expectation_bound_latest_run.txt','local_base_polar_latest_run.txt','base_polar_latest_run.txt']:
 run=Path((REV/pointer).read_text().strip());m=load(run/'manifest.json');c=load(run/'compilation.json')
 assert c['complete'] and c['all_exit_zero'] and c['all_axioms_allowed'] and c['dependencies_preserved']
 for row in c['records']:
  assert row['returncode']==0 and row['axioms_allowed'] and row['exact_targets']
  assert hf(row['stdout'])==row['stdout_sha256'] and hf(row['stderr'])==row['stderr_sha256']
  assert hf(row['command'][2])==row['output_sha256'] and hf(row['command'][3])==row['source_sha256']
  assert all(set(a)<=allowed for a in row['axioms'].values())
  if row['module'] in m['sources']:
   assert row['binary_equals_author']
   name=Path(row['module']).stem;assert name not in own;own[name]={'run':str(run),**row}
 for n,d in m['dependencies'].items():
  assert hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256']
 for p,h in m['origins'].items():
  assert hf(Path(p)/'manifest.json')==h['manifest_sha256'] and hf(Path(p)/'compilation.json')==h['compilation_sha256']
 history=load(run/'author_history.json');hist.extend(history)
 runs.append({'path':str(run),'manifest_sha256':hf(run/'manifest.json'),'compilation_sha256':hf(run/'compilation.json'),
  'dependencies':len(m['dependencies']),'Lean_calls':len(c['records']),'auditor_targets':len(c['records'][-1]['axioms']),
  'all_exit_zero':True,'all_axioms_allowed':True,'dependencies_preserved':True})
assert len(own)==4 and sum(r['Lean_calls'] for r in runs)==7
last=Path(runs[-1]['path']);lm=load(last/'manifest.json');lc=load(last/'compilation.json')
assert {n:sorted(a) for n,a in lc['records'][-1]['axioms'].items()}==F['targets']
stdout=Path(lc['records'][-1]['stdout']).read_text(encoding='utf-8')
assert all(re.search(r'^'+re.escape(n)+r'(?:[.\s])',stdout,re.M) for n in F['targets'])
for name,pin in F['modules'].items():
 src=ROOT/'kernel/TGLV350'/(name+'.lean');bn=ROOT/'build/TGLV350'/(name+'.olean');log=Path(pin['final_log']);ar=load(log)
 assert hf(src)==pin['source_sha256']==ar['sha256']==own[name]['source_sha256']
 assert hf(bn)==pin['binary_sha256']==ar['output_sha256']==own[name]['output_sha256']
 assert hf(log)==pin['final_log_sha256'] and ar['returncode']==ar['lean_returncode']==0
 assert ar['output_exists'] and ar['source_unchanged_during_compile']
 assert hf(ar['stdout'])==pin['stdout_sha256'] and hf(ar['stderr'])==pin['stderr_sha256']
 assert len(own[name]['axioms'])==pin['targets']
 assert sorted(str(Path(h['log'])) for h in hist if h['module']==name and h['returncode'])==pin['failed_attempts']
axes={n:sorted(a) for n,a in lc['records'][-1]['axioms'].items()}
bootstrap=[n for n,d in lm['dependencies'].items() if d.get('canonical_and_author_binary_equal')]
assert len(bootstrap)==150
helpers=['make_base_polar_helpers.py','prepare_base_polar_stage.py','record_base_polar_progress.py','verify_base_polar_custody.py']
for n in helpers:ast.parse((ROOT/n).read_bytes())
assert all(not (ROOT/n).exists() for n in ['base_polar_custody.json','base_polar_custody_verification.json','RELATORIO_CONJUGACAO_POLAR_BASE_INTEGRADA.md'])
e=load(ROOT/'kernel_incremental_evidence.json');flags={k:e[k] for k in P['remaining_flags']}
assert all(x is False for x in flags.values())
v={'timestamp':datetime.datetime.now().astimezone().isoformat(timespec='seconds'),'mode':'SCOPED_INDEPENDENT_DEV_REVIEW_COMPLETE__INTEGRATION_PENDING',
 'modules':list(F['modules']),'targets':axes,'own_runs':runs,'own_Lean_calls':7,'source_builds':4,'auditors':3,
 'four_binaries_equal_author':True,'source_log_stream_pins_match':True,'all_19_types_checked_with_universes':True,
 'final_dependencies':607,'newly_frozen_historical_dependencies_not_recompiled':bootstrap,
 'historical_provenance':'Source equals custodied original embedded text and canonical Lean source; local and canonical binary/sidecar bytes matched before isolated copy. No canonical project build directory in LEAN_PATH.',
 'author_failed_attempts_excluded':sum(bool(h['returncode']) for h in hist),'historical_attempts':hist,
 'all_parent_artifacts_unchanged':True,'parent_sha256':hf(ROOT/'matrix_polar_custody.json'),'working_sha256':hf(ROOT/'um.py'),
 'previous_reviews_unchanged':True,'34_memory_surfaces_match_parent':True,'six_flags':flags,
 'author_helpers_executed':False,'monolith_executed_or_imported':False,'integration_review_performed':False,
 'helper_static_review_only':True,'P0':[],'P1':[],'P2':[],
 'artifact_pins':{n:hf(ROOT/n) for n in ['base_polar_draft_status.json','RELATORIO_CONJUGACAO_POLAR_BASE_DEV.md']+helpers}}
save(last/'verification.json',(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
lines=['# Revisão DEV — conjugação polar de toda a álgebra-base','', 'BASE_POLAR_DEV_REVIEW','',
f"{v['timestamp']}. **[REAL] Revisão delimitada concluída, sem achados P0, P1 ou P2.** Quatro módulos/19 alvos (6+5+5+3), lidos integralmente, recompilados em árvore própria e auditados em tipos/universos e axiomas. Integração ainda pendente.",'',
'Com M=`theFactorObject P`, N=`regularCoreAlgebra P`, ι=`regularCoreEmbedding P`, π=`scalarGNSRepresentation P` e J=`scalarTomitaPolarFactor P`, o resultado efetivo é:', '',
'`Commute (J · π(ι(x)) · J⁻¹) (π(y))`, para **todo x∈M e todo y∈N**, no mesmo `ScalarGNSHilbert P`.', '',
'**Conferência semântica e hipóteses.**', '',
'- '+link('LevelExpectationUniformBound.lean:16',ROOT/'kernel/TGLV350/LevelExpectationUniformBound.lean:16')+': `levelPositiveMap` é ℂ-linear, positivo para a ordem herdada dos operadores e restrito ao fator. A positividade usa explicitamente pertinência a M. A unidade vem de `expectation_fixes`. O lema genérico de norma (linha 35) decompõe x em quatro positivos de norma ≤‖x‖ e trata inclusive codomínio trivial. A cota final é uniforme em N, sem afirmar optimalidade.',
'- '+link('LevelExpectationUniformBound.lean:57',ROOT/'kernel/TGLV350/LevelExpectationUniformBound.lean:57')+': fechamento em norma decorre do duplo centralizador. A raiz positiva permanece na mesma subálgebra via `cfcₙ_mem`; isso prova `StarOrderedRing` para a ordem já herdada. As instâncias de fechamento/completude necessárias são obtidas internamente; o teorema final não recebe hipótese nova sobre P ou completude do fator.',
'- '+link('LevelExpectationStrongLimit.lean:16',ROOT/'kernel/TGLV350/LevelExpectationStrongLimit.lean:16')+': a cota 4‖A‖ e E_N(A)Ω→AΩ satisfazem as hipóteses reais de `bounded_omega_tendsto`. As pontes seguintes são `fibre_tendsto_of_uniformly_bounded` e `scalarGNSRepresentation_tendsto_of_uniformly_bounded`, com a mesma inclusão/representação. Não há hipótese residual de limite forte, nem uso de `ExpectationInput`. O limite é forte em vetores; não se afirma convergência na norma de operadores.',
'- '+link('LocalBasePolarCommutation.lean:21',ROOT/'kernel/TGLV350/LocalBasePolarCommutation.lean:21')+': a conjugação antiunitária transforma c em `star c`. A indução matricial genérica cobre todos os coeficientes; a aplicação concreta compõe `localBaseCore` e a mesma π. O caso unidade coincide por definição com `matrixUnitRightData`, sem encadear operadores apenas pelo nome.',
'- '+link('BasePolarStrongLimit.lean:13',ROOT/'kernel/TGLV350/BasePolarStrongLimit.lean:13')+': transporte por U/U⁻¹ fixos usa continuidade em vetores. O lema de comutação exige `[NeBot l]` para unicidade e mantém B fixo. A aplicação final (linha 39) resolve essa hipótese em `atTop : Filter ℕ` e usa `expectationMatrix` para identificar exatamente a aproximação local. Não usa continuidade SOT irrestrita do adjunto ou de produtos com dois fatores variáveis.', '',
'**Evidência própria e pins.** As quatro fontes foram compiladas uma vez cada nesta revisão. Houve três auditores acumulativos de 6, 16 e 19 alvos: sete chamadas Lean, todas rc0. Todos os 19 conjuntos de axiomas são exatamente o trio `propext`, `Classical.choice`, `Quot.sound`; os quatro `.olean` próprios são byte a byte iguais aos finais autorais. Nenhum pacote foi recompilado.', '',
'| Fonte DEV | SHA256 fonte | SHA256 .olean próprio = autoral |','|---|---|---|']
for n,pin in F['modules'].items():lines.append(f"| {n} | `{pin['source_sha256']}` | `{pin['binary_sha256']}` |")
lines+=['','| Estrato próprio | Compilações rc0 | Auditor | SHA256 compilation.json |','|---|---|---|---|']
for r in runs:lines.append(f"| {link(Path(r['path']).name,Path(r['path'])/'compilation.json')} | {r['Lean_calls']} | {r['auditor_targets']} alvos | `{r['compilation_sha256']}` |")
lines+=['',
'Proveniência: 281 dependências reutilizadas no primeiro estrato, 605 no segundo e 607 no último. A importação de `ExpectationContinuity` exigiu congelar 150 dependências históricas ainda ausentes da árvore selecionada. Seus textos foram comparados aos embutidos da cópia-base custodiada e às fontes canônicas; binários/arquivos auxiliares locais e canônicos foram comparados antes da cópia. **Esses 150 binários são herança verificada por bytes, não recompilações independentes desta rodada.** Os manifestos individualizam essa origem. O `LEAN_PATH` contém somente o build próprio e oito diretórios de pacotes externos readonly; nenhum diretório de build autoral/canônico de projeto. As dependências anteriores e seus pressupostos permanecem herdados.', '',
f"As {v['author_failed_attempts_excluded']} tentativas autorais rc1 estão preservadas em `author_history` nos três estratos e excluídas da aceitação. Algumas imprimem `sorryAx`; somente os logs finais dos bytes pinados, confirmados pela reprodução própria, contam como evidência. Não há `sorry`/`axiom`/`unsafe` nas quatro fontes aceitas.", '',
'**Manifesto, relatório e helpers.** Manifesto e relatório DEV foram lidos inteiros e seus pins confrontados com fonte, binário, log e streams. Os quatro helpers foram apenas lidos/parseados. O preparador planeja os quatro módulos, batch 444→463 e um grupo negativo. Recorder/verifier mantêm mãe única `matrix_polar_custody`, 34 superfícies, backups dos bytes imediatamente anteriores, append/prefixos e troca atômica; exigem também o parecer integrado futuro. A redação define Δ=S†S e conserva Δ^it/KMS como obrigação aberta. Essa inspeção estática não declara preparação, integração, nova custódia ou execução dos helpers. As contagens 882/180/95/6820 são previsões da próxima integração, não resultados deste DEV.', '',
'| Documento/helper | SHA256 lido |','|---|---|']
for n,h in v['artifact_pins'].items():lines.append(f'| {link(n,ROOT/n)} | `{h}` |')
lines+=['',
f"Mãe lida: `{v['parent_sha256']}`; cópia integrada preservada: `{v['working_sha256']}`. Artefatos integrados, seis flags falsas e 34 superfícies continuam iguais à mãe. Original-base local e fontes históricas foram consultados somente para leitura; nenhum monólito, helper autoral ou recorder foi executado/importado e nenhuma memória foi escrita.", '',
f"Evidência consolidada: {link('verification.json',last/'verification.json')} (SHA256 `{hf(last/'verification.json')}`); {link('auditor próprio dos 19 tipos/axiomas',Path(lc['records'][-1]['stdout']))}; fontes congeladas, logs e manifestos nos estratos acima. Os pareceres anteriores não foram modificados.", '',
'**Limites:** o pacote fornece Jπ(ι(M))J⁻¹⊆π(N)′. Não demonstra Jπ(N)J=π(N)′, inclusão inversa/global, identificação de Δ^it com o fluxo do peso, KMS, traço, Three Locks, H1–H3, física ou consumo pelo gate. `LevelExpectationFamily` continua distinta do contrato centralizante `ExpectationInput`. Nenhuma análise DEV necessária desses quatro módulos ficou pendente; a integração será escopo posterior.','']
save(REV/'REVIEW_BASE_POLAR_DEV.md','\n'.join(lines).encode('utf-8'))
print(str(REV/'REVIEW_BASE_POLAR_DEV.md'));print(hf(REV/'REVIEW_BASE_POLAR_DEV.md'));print(hf(last/'verification.json'))
