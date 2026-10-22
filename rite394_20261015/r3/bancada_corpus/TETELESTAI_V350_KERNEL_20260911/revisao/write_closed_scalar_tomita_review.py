"""Publish the independent closed scalar Tomita DEV review; no author writes."""
from pathlib import Path
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
REVIEW=Path(__file__).resolve().parent;ROOT=REVIEW.parent
RUN=Path((REVIEW/'closed_scalar_tomita_latest_run.txt').read_text(encoding='utf-8'))
read=lambda p:json.loads(p.read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
M,C,V,S=(read(RUN/n) for n in ['manifest.json','compilation.json','verification_dev.json','source_structure.json'])
D=read(RUN/'author_tomita_closed_draft_status.json')
K=read(RUN/'gns_cut_maps_custody.json')
G=V['generic_dependency_recompiled'];GEN=Path(G['run']);GC=read(GEN/'compilation.json')
for k in ['complete','all_exit_zero','full_audit_names_exact','all_axioms_allowed','sources_unchanged','dependencies_unchanged','previous_reviews_preserved']:
    assert C[k],k
for k in ['three_compiles_rc0','exact_target_set','axioms_match_status','all_axioms_allowed','dependencies_frozen_preserved','author_project_builds_excluded','status_unchanged','report_equals_status_and_frozen','custody_equals_status','previous_gns_cut_maps_review_equals_custody','previous_reviews_preserved','parent_gaussian_review_matches_status','parent_gaussian_status_matches_pin']:
    assert V[k],k
for row in V['records'].values():
    for k in ['source_equals_status_and_frozen','author_log_equals_status_hash','author_log_identical_to_frozen','author_log_rc0_source_unchanged','author_binary_equals_status_and_log','own_binary_equals_compilation_record','own_binary_equals_author','target_names_exact','author_streams_frozen_equal']:
        assert row[k],k
for k in ['rc0','axioms_allowed','unchanged_source','same_binary_used_in_main_build']:
    assert G[k],k
for row in M['sources'].values():
    assert sha(Path(row['path']))==sha(Path(row['snapshot']))==row['sha256']
for row in M['dependencies'].values():
    assert sha(Path(row['frozen_source']))==row['source_sha256']
    assert sha(Path(row['frozen_binary']))==row['sha256']
for p,h in M['previous_reviews'].items():assert sha(Path(p))==h,p
assert sha(ROOT/'tomita_closed_draft_status.json')==V['status_sha256']
assert sha(ROOT/'RELATORIO_TOMITA_FECHADO_DEV.md')==V['report_sha256']
assert sha(ROOT/'gaussian_closability_draft_status.json')==V['parent_gaussian_status_sha256']
assert sha(REVIEW/'REVIEW_GAUSSIAN_CLOSABILITY.md')==V['parent_gaussian_review_sha256']
assert sha(ROOT/'gns_cut_maps_custody.json')==V['custody_sha256']
assert sha(ROOT/'um.py')==M['initial_um_sha256']==D['working_sha256']==K['working_sha256']
assert len(M['declarations'])==len(M['all_named_declarations'])==24
paths=M['lean_path'].split(os.pathsep)
assert len(paths)==9 and paths[0]==str(RUN/'build') and all('\\.lake\\packages\\' in p for p in paths[1:])
assert not any(row['unsafe_patterns'] for row in S.values())
assert all(Path(row['stderr']).stat().st_size==0 and 'warning:' not in Path(row['stdout']).read_text(encoding='utf-8') for row in C['records']+GC['records'])

def write_new(p,b):
    assert p.resolve().is_relative_to(REVIEW) and not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b and t.stat().st_size==len(b)>0
    t.replace(p);assert p.read_bytes()==b
def link(p,label=None,line=None):
    return '['+(label or p.name)+'](<'+p.as_posix()+(':'+str(line) if line else '')+'>)'
src=lambda name,line:link(ROOT/'kernel/TGLV350'/(name+'.lean'),name+'.lean:'+str(line),line)
now=datetime.datetime.now().astimezone()
source_table='\n'.join('| '+n+' | '+str(len(M['sources']['TGLV350/'+n+'.lean']['declarations']))+' | `'+r['source_sha256']+'` | `'+r['own_binary_sha256']+'` |' for n,r in V['records'].items())
log_table='\n'.join('| '+link(Path(r['author_log']))+' | `'+r['author_log_sha256']+'` |' for r in V['records'].values())
time_table='\n'.join('| '+r['module']+' | 0 | '+str(r['seconds'])+' |' for r in GC['records']+C['records'])
target_table='\n'.join('| '+Path(rel).stem+' | '+', '.join('`'+n.split('.')[-1]+'`' for n in r['declarations'])+' |' for rel,r in M['sources'].items())
ex=V['dependency_comment_only_exceptions']['TGLV350.DualSemifiniteIdeal']
hist=V['historical_custody_counts']
old=V['original_graph_dependency']
report=f'''# Revisão independente — operador escalar de Tomita fechado

{now.isoformat(timespec='seconds')}. **DEV concluído, sem achados P0–P2.**

[REAL — leitura integral e recompilação própria] Foram lidos os dois módulos finais, o relatório autoral e toda a dependência existente `TGLExt/ClosedAntilinearStandardSubspace.lean`. **Dois DEV + auditor próprio passaram rc0**, com os 24 tipos e 24 conjuntos de axiomas conferidos. Somente `propext`, `Classical.choice`, `Quot.sound`; os dois `.olean` próprios coincidem byte a byte com os autorais pinados. A dependência genérica também foi recompilada separadamente em árvore própria, rc0, para evitar uso de binário autoral de projeto. Nenhuma análise DEV necessária deste escopo permanece pendente.

O pacote constrói uma aplicação antilinear S no domínio denso D do **fecho do gráfico original**, prova igualdade de seu gráfico com esse fecho, invariância do domínio, involução e extensão da estrela do núcleo I∩I*. Constrói no mesmo H_I o subespaço real padrão K=Fix S, com D=K+iK e S(h+ik)=h−ik. Não identifica K com Fix J, o domínio com n_ν ou os dados polares/KMS do peso.

## Domínio, escolha e gráfico

**Objetos preservados.** H_I é `ScalarGNSHilbert P`, o subespaço fechado anterior do L² de órbitas. `scalarTomitaGraph P` continua a imagem de A∈`finiteDualStarCore P` pelo par `(scalarGNSStarEmbedding P A, scalarGNSStarEmbedding P (star A))`. Essa declaração herdada mantém fonte `{old['source_sha256']}` e binário próprio `{old['sha256']}`. Não foi reconstruída com outro espaço, vetor, peso ou ideal. A fechabilidade/univalência usada é a do pacote gaussiano anterior, conferido separadamente; não é uma nova premissa colocada sobre P.

**Instâncias locais — {src('ScalarClosedTomita',12)} (12–24).** `scalarStarCoreAdd` usa o `AddCommGroup` do `NonUnitalRing` herdado da subálgebra sem unidade. `scalarStarCoreSMul` aplica c ao operador subjacente e usa `smul_mem` para recolocá-lo no subtipo. Essas são as operações do subobjeto; não alteram adição ou escala no H_I. Os lemas de inscrição reduzem às leis `map_add` e `map_smul` da mesma Λ sobre I. As identidades de estrela em zero, soma e escala são verificadas por `Subtype.ext` no operador subjacente. As duas instâncias são locais, não axiomas; seus usos são cobertos transitivamente pelos alvos auditados. Não foram contadas como dois novos alvos além dos 24 solicitados.

**Estrutura do gráfico — {src('ScalarClosedTomita',26)} (26–85).** A inscrição de zero, a aditividade e a lei de estrela dão a estabilidade do gráfico por soma e por **(x,y)↦(cx,conj(c)y)**. Não se trata o gráfico antilinear como um subespaço complexo com escala idêntica nas duas coordenadas. O conjugado é efetivamente `starRingEnd ℂ`.

A aditividade do fecho é provada em duas aplicações de `closure_minimal`, fixando alternadamente cada somando e usando continuidade da adição. Escala conjugada e swap passam ao fecho pela continuidade das aplicações correspondentes no produto H_I×H_I. Não se invocam continuidade de S, limitação de S ou fechamento prévio do domínio.

**Domínio e escolha — {src('ScalarClosedTomita',88)} (88–117).** O carrier de D é exatamente

`{{x : H_I | ∃ y : H_I, (x,y) ∈ closure (scalarTomitaGraph P)}}`.

As operações de submódulo complexo em D são construídas a partir das testemunhas no fecho: y+w para x+z e conj(c)y para cx. `Classical.choose x.property` é aplicado a uma existência contida no tipo de x; `choose_spec` prova que o valor escolhido está sobre x no fecho. Não há escolha em um conjunto possivelmente vazio.

`scalarClosedTomita` tem tipo **D→ₛₗ[starRingEnd ℂ]H_I**, uma aplicação semilinear, não uma CLM. As leis de soma e escala são demonstradas comparando dois pontos do fecho com a mesma primeira coordenada e aplicando a univalência já provada. Assim a escolha não introduz uma hipótese de linearidade nem ambiguidade no valor de S.

**Igualdade de gráfico e fechamento — {src('ScalarClosedTomita',119)} (119–147).** A inclusão do gráfico de S no fecho decorre de `choose_spec`. Para o sentido inverso, de p=(x,y) no fecho constrói-se x como elemento de D usando y como testemunha; a univalência obriga Sx=y. Portanto a igualdade é efetiva:

`range (fun x : D => ((x : H_I), S x)) = closure (scalarTomitaGraph P)`.

O fecho é tomado no produto **H_I×H_I**, com a primeira coordenada incluída no ambiente, e não apenas no produto do domínio com H_I. Da igualdade segue `IsClosed` desse gráfico ambiente. A densidade de D vem da inclusão do domínio inicial denso no domínio do fecho. Não se declara D=H_I, D fechado ou D completo; não se aplica indevidamente o teorema do gráfico fechado para obter limitação de S.

**Involução e extensão — {src('ScalarClosedTomita',149)} (149–168).** O swap de (x,Sx) fornece (Sx,x) no fecho, daí Sx∈D. A univalência na fibra sobre Sx dá S(Sx)=x, com a pertinência de Sx ao domínio explicitamente carregada no subtipo. É uma involução no domínio invariante, não uma operação definida em todo H_I. Para A∈I∩I*, o par inicial pertence ao fecho; isso fornece Λ(A)∈D e, novamente pela univalência, SΛ(A)=Λ(A*). Não se substitui I∩I* pelo domínio escalar máximo.

## Dependência genérica e subespaço padrão

A dependência {link(ROOT/'kernel/TGLExt/ClosedAntilinearStandardSubspace.lean')} foi lida inteira, inclusive suas provas de linhas 44–221. O cabeçalho contém história de outras entregas; essas contagens e interpretações não foram tomadas como nova evidência deste pacote. Os passos utilizados são:

| Trecho da dependência | Conferência |
|---|---|
| 48–86: `fixedRealSubmodule`, `fixedRealSubmodule_closed`, `fixedClosedSubmodule` | Fix S é um submódulo **real**, com condição x∈D explícita. Sua fechadura vem da preimagem diagonal x↦(x,x) do gráfico fechado ambiente; não exige D fechado. A escala real é compatível porque o conjugado de um real é ele mesmo. |
| 89–139: `domainConjugation`, `domain_fixed_decomposition` | A hipótese de domínio invariante permite codrestringir S a D. Com involução, h=(x+Sx)/2 e k=−i(x−Sx)/2 são fixos; o cálculo usa conj(−i/2)=i/2 e dá simultaneamente x=h+ik e Sx=h−ik. Os sinais e o fator 1/2 são algébricos. |
| 141–158: `mem_domain_iff_fixed_sum`, `fixed_sum_tomita` | As duas inclusões de D=K+iK são efetivas. A volta usa h,k∈D e o fato de D ser submódulo complexo; a ação em h+ik vem da antilinearidade e dos valores fixos. |
| 160–185: `fixed_subspace_separating` | De x∈K∩iK, antilinearidade e as duas condições de fixação dão ix=−ix, logo x=0 porque 2i≠0. Não há operador J ou hipótese polar nessa prova. |
| 187–221: `fixed_subspace_cyclic`, `closedAntilinearStandardSubspace` | A decomposição inclui D no supremo de K e iK no reticulado de submódulos reais fechados; a densidade de D obriga esse supremo a ser todo H. As quatro hipóteses usadas são gráfico fechado, domínio invariante, involução e densidade. |

As linhas 178–184 da definição instalada de Mathlib `Analysis/InnerProductSpace/StandardSubspace.lean` também foram consultadas: a estrutura contém `toClosedSubmodule : ClosedSubmodule ℝ H`, `IsSeparating : K ⊓ K.mulI = ⊥` e `IsCyclic : K ⊔ K.mulI = ⊤`. O supremo aqui é de **submódulos fechados**. Assim a propriedade cíclica diz fecho(K+iK)=H; não diz que a soma algébrica já é fechada ou igual a H.

**Aplicação aos mesmos D e S — {src('ScalarTomitaStandardSubspace',12)} (12–39).** As quatro hipóteses genéricas são fornecidas pelas quatro provas concretas do primeiro módulo. O tipo impresso é `StandardSubspace (ScalarGNSHilbert P)`. O teste de pertinência é definicionalmente `∃ hx:x∈D, S⟨x,hx⟩=x`, de modo que K é Fix **S** no mesmo H_I. Os teoremas seguintes dão D=K+iK como soma algébrica e a decomposição conjunta x=h+ik, Sx=h−ik. Não se muda de Hilbert, não se insere um antiunitário J e não se usa identificação modular do peso para preencher algum campo.

## Alvos e evidência própria

| Módulo | 24 alvos novos conferidos |
|---|---|
{target_table}

Árvore principal: {link(RUN)}. Ela usa **{len(M['dependencies'])} dependências de projeto pinadas**: 398 reaproveitadas da árvore gaussiana própria {link(Path(M['previous_run']))}, mais a dependência genérica recompilada nesta revisão. A árvore dessa recompilação é {link(GEN)}. Seus 12 `#print axioms` existentes ficaram no trio; não são somados aos 24 alvos novos.

Genérica recompilada: fonte `{G['source_sha256']}`, `.olean` próprio `{G['olean_sha256']}`. Esse mesmo `.olean` foi copiado para o build principal e seu hash conferido. Registro próprio: {link(GEN/'compilation.json')}, SHA256 `{G['compilation_json_sha256']}`. Não se utilizou o binário autoral dessa dependência.

O `LEAN_PATH` principal tem somente seu build de projeto, seguido de oito caminhos de pacotes externos readonly. O build genérico também é próprio; pacotes/compiler foram apenas lidos. Nenhum build autoral de projeto integrou a resolução de módulos. TMP/TEMP são próprios. Compilador: `{M['lean_version']}`, SHA256 `{M['compiler_sha256']}`. Não houve rebuild de bibliotecas ou dos módulos cíclicos/gaussianos anteriores.

Permanece a exceção histórica de comentário em `DualSemifiniteIdeal`: fonte própria `{ex['source_sha256']}`, binário herdado `{ex['sha256']}`, fonte autoral atual `{ex['live_source_sha256']}`. A diferença literal foi novamente conferida como somente a errata documental já revisada. As limitações binárias herdadas permanecem as dos pareceres anteriores; a coincidência com os binários autorais aqui declarada é a dos dois DEV novos.

| Módulo DEV | Alvos | SHA256 fonte final lida | SHA256 `.olean` próprio = autoral |
|---|---|---|---|
{source_table}

| Processo executado nesta revisão | rc | Segundos |
|---|---|---|
{time_table}

Total: **quatro processos próprios**, incluindo a genérica, os dois DEV e o auditor. Todos ficaram sem warnings e com stderr vazio. Auditor novo: fonte `{V['own_auditor_source_sha256']}`, `.olean` `{V['own_auditor_binary_sha256']}`, stdout `{V['own_auditor_stdout_sha256']}`. Os 24 `#check` com universos e os 24 `#print axioms` cobrem exatamente a lista do status, sem pressupostos adicionados ao auditor. Nenhum `sorryAx` ou axioma fora do trio apareceu.

| Log autoral final inspecionado | SHA256 JSON |
|---|---|
{log_table}

Fontes, binários, logs JSON e streams autorais foram comparados aos pins e aos snapshots. Os logs aceitos registram rc0 e fonte inalterada; tentativas autorais anteriores não foram apagadas nem usadas como êxito. **Execução própria** em {link(RUN/'compilation.json')}; **hashes e comparação com o autor** em {link(RUN/'verification_dev.json')}; **deps, comandos e LEAN_PATH** em {link(RUN/'manifest.json')}; **tipos e axiomas completos** em {link(RUN/'logs/ClosedScalarTomitaAudit.stdout.txt')}. Nenhum teste, recorder, integrador ou monólito autoral foi executado/importado.

A leitura de todas as fontes e a inspeção adicional {link(RUN/'source_structure.json')} conferem as duas instâncias locais e somente as opções `autoImplicit`, `linter.unusedSectionVars`, `maxHeartbeats`. Não há `axiom`, `sorry`, `admit`, declaração `unsafe`, atributo de redutibilidade ou relaxamento de transparência nos novos arquivos. Essa inspeção é complementar à recompilação e à auditoria transitiva de axiomas.

## Documentação, preservação e limites

`RELATORIO_TOMITA_FECHADO_DEV.md` foi lido integralmente, SHA256 **`{V['report_sha256']}`**, igual ao pin e ao snapshot. Suas afirmações sobre D, escolha, antilinearidade, fecho, involução, extensão, Fix S e soma K+iK correspondem às provas. Os limites relativos a Fix J, domínio máximo e dados polares estão corretamente explicitados. Nenhum P2 documental encontrado; o estatuto de revisão pendente é o do arquivo congelado antes deste parecer.

Status `tomita_closed_draft_status.json`: `{V['status_sha256']}`. Parecer gaussiano pai `{V['parent_gaussian_review_sha256']}` e status gaussiano `{V['parent_gaussian_status_sha256']}` coincidem com os pins. A custódia integrada anterior `gns_cut_maps_custody.json` permanece `{V['custody_sha256']}`. As contagens **{hist['integrated_records']}/{hist['controls']}/{hist['audit_declarations']}** e a cópia `{M['initial_um_sha256']}` são do estrato integrado anterior, lido da custódia; o hash da cópia foi conferido novamente ao encerrar. Não houve inspeção de integração nova ou soma destes DEV àquelas contagens.

Os {len(M['previous_reviews'])} pareceres anteriores mantiveram seus hashes, inclusive os cíclicos e gaussianos ainda aguardando integração. Fontes autorais, originais, monólito, memórias, status e custódias permaneceram intocados. Todas as saídas foram gravadas em `revisao/`.

**Conclusão delimitada:** dois módulos/24 alvos e a dependência genérica conferidos, com recompilação própria, sem P0, P1 ou P2. Está construído S antilinear, fechado e densamente definido no domínio do fecho do gráfico original, involutivo no domínio invariante e estendendo a estrela de I∩I*. K=Fix S é um subespaço real padrão do mesmo H_I; D=K+iK e S(h+ik)=h−ik. Não se concluem I=n_ν, identificação de domínio máximo, adjunto/decomposição polar modular, Fix J, KMS, traço, escala física, Three Locks/H1–H3, consumo pelo gate ou runtime. **Nenhuma análise DEV necessária resta neste escopo.**
'''
p=REVIEW/'REVIEW_CLOSED_SCALAR_TOMITA.md';write_new(p,report.encode('utf-8'))
closure={'timestamp':now.isoformat(timespec='seconds'),'status':'DEV_COMPLETE_NO_P0_P1_P2','review_path':str(p),'review_sha256':sha(p),'review_bytes':p.stat().st_size,'new_modules':2,'new_targets':24,'type_checks':24,'new_modules_and_auditor_rc0':3,'additional_existing_dependency_recompiled_rc0':1,'own_processes_rc0':4,'new_bins_equal_author':True,'project_dependencies':len(M['dependencies']),'previous_reviews_preserved':all(sha(Path(p))==h for p,h in M['previous_reviews'].items()),'integrated_inspection_performed':False,'author_programs_executed':False,'working_sha256_at_close':sha(ROOT/'um.py'),'findings':[],'necessary_dev_analysis_remaining':False}
write_new(RUN/'closure_dev.json',json.dumps(closure,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(closure,ensure_ascii=False,indent=2))
