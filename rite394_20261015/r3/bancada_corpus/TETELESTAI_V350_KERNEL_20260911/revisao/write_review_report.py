"""Render the review from checked evidence. No implementation writes."""
from pathlib import Path
import datetime
import hashlib
import json

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "latest_run.txt").read_text(encoding="utf-8"))
manifest = json.loads((RUN / "manifest.json").read_bytes())
compilation = json.loads((RUN / "compilation.json").read_bytes())
integration = json.loads((RUN / "integration_inspection.json").read_bytes())
base = json.loads((RUN / "base_dependency_check.json").read_bytes())
probes = json.loads((RUN / "type_probes.json").read_bytes())
gate = json.loads((RUN / "independent_gate_evidence.json").read_bytes())
FINAL = sorted(RUN.glob("final_integrated_*"))[-1]
integrated = json.loads((FINAL / "verification.json").read_bytes())
assert compilation["all_exit_zero"] and not compilation["dependencies_changed"]
assert all(x["passed"] for x in probes)
assert integrated["all_hashes_match"] and integrated["all_exit_zero"] and integrated["exact_expected_file_set"]
assert not integrated["audit_unexpected_axioms"] and integrated["gate_checks_all_passed"]
assert not base["source_mismatches"] and not base["binary_mismatches"] and not base["not_in_baseline_manifest"]
assert all(gate["proof_flags"].values()) and gate["output_hashes_verified"]
assert integration["gate_passed"] == integration["gate_total"]
assert all(c["embedded_matches_file"] and c.get("same_except_import_paths", True)
           for c in integration["static"]["integrated_source_comparison"])

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def link(path, title=None, line=None):
    path = Path(path)
    suffix = ":" + str(line) if line else ""
    return "[" + (title or path.name) + "](<" + path.as_posix() + suffix + ">)"

def source(relative, line):
    return link(ROOT / relative, Path(relative).name + ":" + str(line), line)

changed = [name for name, row in manifest["snapshots"].items()
           if digest(ROOT / name) != row["sha256"]]
assert not changed, changed
assert digest(ROOT / "um.py") == integrated["um_sha256"]
timestamp = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
rows = []
for row in compilation["records"]:
    rows.append("| " + source("kernel/" + row["module"], 1) + " | " + str(row["returncode"]) + " | `" + row["source_sha256"] + "` |")
hash_table = "\n".join(rows)
text = f'''# Revisão adversarial independente — pacote modular e regular V350

Data de fechamento: {timestamp}. Pasta autorizada: `{ROOT}`. Parecer ancorado nos arquivos congelados em `{RUN.name}`.

**[REAL — revisão e recompilação delimitadas] Não encontrei defeito concreto de tipagem semântica, hipótese residual ou composição das provas nos dez módulos solicitados e na ponte modular examinada. A inclusão R′ ⊆ L′′ está provada para todo `SiteProfile`; o certificado de dualidade é habitado sem premissa de comutação. A regular é construída em Lebesgue L²(ℝ, TowerHilbert P), com o mesmo fluxo modular.**

O parecer é favorável a este pacote no escopo de **dualidade da torre produto, representação covariante unitária fortemente contínua e álgebra de von Neumann gerada com inclusão fiel e minimalidade**. Não aprova QG nem o plano ampliado. Não autoriza transposição ao canônico.

## Achados priorizados

**Nenhum achado corretivo P0, P1, P2 ou P3 demonstrado nos enunciados e na integração examinados.** Não há alteração de implementação proposta por este parecer. Os limites abaixo não foram classificados como bugs, em conformidade com a delimitação do operador.

Foram investigados e afastados os candidatos centrais: circularidade na expectativa finita, multiplicação de limites fortes sem controle uniforme, hipótese conversa remanescente no certificado, troca do Hilbert/fluxo na regular, uso de projeção de andar como `P_F` e promoção da regular a um gate mais amplo.

## Evidência e independência

| Verificação | Resultado e alcance |
|---|---|
| Recompilação desta revisão | **{len(compilation['records'])}/{len(compilation['records'])} exit 0**: os cinco módulos modulares solicitados, `V350WedgeModularData` e os cinco módulos regulares solicitados. Fontes congeladas e todos os `.olean` produzidos exclusivamente em `revisao`. |
| Auditoria nesta recompilação | **{gate['distinct_audited_declarations']} declarações distintas** impressas com axiomas contidos em `{{propext, Classical.choice, Quot.sound}}`; hashes de todos os binários produzidos reconferidos. |
| Dependências de projeto | **{base['dependencies']} fontes e binários** da cadeia importada conferem com a base registrada; zero divergências. Os binários foram copiados para a árvore da revisão antes da compilação. |
| Sondas adicionais desta revisão | `PositiveTypes.lean`: exit 0; inclusão sem premissa, certificado fechado, Hilbert de Lebesgue e covariância com o fluxo de `towerWedgeData` conferidos. `NegativeTypes.lean`: exit 1 esperado, precisamente nas duas atribuições inválidas: `True` no contrato conversa e função dependente de `False` no lugar de certificado fechado. |
| Controles Python desta revisão | **{integration['gate_passed']}/{integration['gate_total']}** decisões adversariais passaram sobre a extensão isolada. Entradas sintéticas são identificadas como controles, não como provas. Separadamente, as evidências da recompilação independente habilitam apenas as três flags modulares esperadas. |
| Rebuild integrado do implementador | **{integrated['integrated_modules']}/{integrated['integrated_modules']} exit 0**, conjunto de arquivos esperado exato e todos os hashes de fontes/`.olean` conferidos nesta revisão. Inclui as raízes `TGLExt.lean` e `TGL/Audit.lean`. Isto é **inspeção independente dos logs/binários**, não recompilação das raízes por este revisor. |
| Auditoria integrada do implementador | **{integrated['audit_distinct']} declarações distintas** recalculadas do stdout; nenhuma dependência fora do trio. **{integrated['gate_checks_count']} controles Python** registrados como aprovados no relatório final; não foram reexecutados como suíte integral por este revisor. |
| Integração no monólito | Inspeção **somente por AST como dados**. Extensão Python idêntica à fonte; avaliador legado inalterado; retorno final chama `finalize_v350_modular_frontier`; `prove_qg_closure_gate` inclui a subdecisão `kernel_frontier`. `um.py` não foi importado nem executado. |

As cinco fontes regulares `kernel/TGLV350/` foram recompiladas exatamente como solicitadas; conferi que suas versões integradas `kernel/TGLExt/V350*.lean` diferem apenas pelos caminhos de imports e coincidem com o conteúdo embutido no monólito. Não examinei nem aprovei os módulos dev posteriores ou a multiplicação por caracteres delegada em separado.

Compilador lido: `{manifest['lean_version']}`. A independência é da revisão e da nova compilação dos módulos selecionados; **Lean, Mathlib e as dependências previamente compiladas continuam sendo a base de confiança**. Não reconstruí toda essa base a partir das fontes nem executei a rodada integral do monólito.

Tentativas anteriores de preparação foram preservadas: a primeira falhou na resolução do diretório de imports; a segunda não pôde ler Mathlib sob a restrição do ambiente. A execução com leitura autorizada das dependências passou. A primeira versão da sonda positiva também precisou explicitar `.val` ao sair do subtipo da álgebra de cunha; a saída e a fonte anteriores estão em backups. A sonda corrigida passou sem qualquer mudança nos arquivos de implementação. Esses ensaios não foram contabilizados como sucessos nem como defeitos das provas.

## Provas conferidas e composição

### 1. Compressão e limite dos produtos

{source('kernel/TGLExt/V350CompressionLimit.lean', 11)}: `project_variable_tendsto` prova que, se `vₙ → z`, então `pₙ vₙ → z`. A estimativa efetivamente usada é `dist(pₙ vₙ, pₙ z) ≤ dist(vₙ, z)`, combinada com `pₙ z → z`. A contração vem da projeção ortogonal, não de hipótese adicional sobre a sequência.

{source('kernel/TGLExt/V350CompressionLimit.lean', 25)}: para `T` fixo e limitado, `compression_variable_tendsto` compõe essa estimativa com a continuidade de `T` e uma nova projeção. Prova `pₙ T pₙ vₙ → Tz` com entrada variável. O operador não é ilimitado disfarçado: seu tipo é `TowerHilbert P →L[ℂ] TowerHilbert P`.

{source('kernel/TGLExt/V350TowerDuality.lean', 42)}: as duas aplicações desse lema dão, para cada vetor `v`, `(pₙ x pₙ)(pₙ y pₙ)v → xyv` e a ordem inversa tendendo a `yxv`. A igualdade finita é transportada à igualdade dos limites por `tendsto_nhds_unique`. **Não se pressupõe continuidade conjunta irrestrita da multiplicação na topologia forte.** O controle uniforme necessário está pago pela contração das projeções e pelos operadores fixos limitados.

### 2. Comutação finita sem circularidade

{source('kernel/TGLExt/V350TowerCommutation.lean', 15)}: `right_commutant_compression` recebe somente `x ∈ R′` e um vetor do andar. A ocorrência de `expectation_mem_factor` concerne à aproximação `towerExpectation P N x`, que pertence à imagem esquerda pela sua definição; não afirma antecipadamente `x ∈ L′′`. Ver {source('kernel/TGLExt/TowerExpectation.lean', 46)} e {source('kernel/TGLExt/TowerExpectation.lean', 63)}.

{source('kernel/TGLExt/V350TowerCommutation.lean', 30)}: a compressão de `y ∈ L′` é representada por multiplicação à direita da matriz decodificada. Não importa um teorema de dualidade para produzir essa matriz: `expectationMatrix` decodifica a projeção de `yΩ` no andar.

{source('kernel/TGLExt/V350TowerDuality.lean', 23)}: `compressed_right` e `compressed_left` reduzem as duas compressões às ações esquerda/direita no mesmo andar. `left_preserves_level` e `right_preserves_level` permitem eliminar as projeções intermediárias; `rTowerPi_comm_towerPi` conclui. As identidades de projeção importadas em {source('kernel/TGLExt/ExpectationBimodule.lean', 39)} exigem redução por operador e adjunto, e ambas são demonstradas para as ações locais. No lado direito o adjunto usa o `modTwist`, não a hipótese errada de que o estado seja tracial.

### 3. Inclusão, igualdade e certificado fechado

{source('kernel/TGLExt/V350TowerDuality.lean', 64)} contém literalmente a inclusão `commutantSet (rTowerImage P) ⊆ commutantSet (commutantSet (towerImage P))`. O único parâmetro é `P : SiteProfile`. A composição termina em `tower_commutation_equality`, linha 69, juntando a direção anterior `the_easy_half_without_J`.

“Sem premissa residual” significa sem a própria inclusão, sem `hComm` e sem certificado recebido de fora. **As hipóteses estruturais de `SiteProfile` permanecem:** pesos `w(n)` estritamente entre zero e um, {source('kernel/TGLExt/TowerDefinite.lean', 53)}. O resultado diz respeito à torre produto definida nesse sistema, não a uma álgebra arbitrária.

{source('kernel/TGLExt/V350ModularCertificate.lean', 11)} fornece o campo do `ConverseClauseContract` diretamente pelo teorema. Na linha 15, `contract_iff_the_eighth_clause mixProfile` fornece a hipótese exigida pelo antigo certificado condicional; ela é produzida localmente. Os campos da estrutura são preenchidos com o mesmo `towerJ mixProfile`, incluindo ambos os sentidos de dualidade. `qgPrice_towerActIII_inhabitantConstructed` é um alias desse certificado, sem introduzir outro modelo.

{source('kernel/TGLExt/V350GateContract.lean', 8)} exige os tipos exatos: função em todo perfil para o contrato conversa e termos fechados de `ModularRealizationCertificate` para os outros dois nomes. As sondas negativas confirmam que a ponte recusa `True` e uma função que ainda requer hipótese não descarregada.

**Limite do nome:** `ModularRealizationCertificate`, {source('kernel/TGLExt/FrontierCertificate.lean', 54)}, contém conjugação antiunitária, vácuo fixo e dualidade sobre a torre `mixProfile`. Não equivale ao pacote maior de core, traço, canto e geometria física. `V350WedgeModularData`, {source('kernel/TGLExt/V350WedgeModularData.lean', 70)}, monta a camada mínima de dados de cunha usando essa torre e seu fluxo; `same_conjugation`, linha 80, amarra expressamente o mesmo `J`.

### 4. Regular sobre Lebesgue L² e mesmo fluxo

{source('kernel/TGLV350/L2OperatorLift.lean', 12)} define `RegularHilbert H := Lp H 2 (volume : Measure ℝ)`. `fibre T = T.compLpL 2 volume` é a ação constante nas fibras. As identidades são quase em toda parte, convertidas por `Lp.ext`; o adjunto é conferido pelo produto interno integral. A fidelidade, linha 100, usa vetores `1_(0,1] · v`, cujo intervalo tem medida um. Não usa funções constantes não integráveis em toda a reta.

{source('kernel/TGLV350/L2Translation.lean', 13)} define `(Sₜf)(x)=f(x−t)` por transformação preservadora de Lebesgue. Lei de grupo, inversa e adjunto são provados nas linhas 33–58. A continuidade forte, linha 78, usa a topologia usual de ℝ e continuidade da família de translações. Não há substituição por contagem, reta discreta ou espaço finito.

{source('kernel/TGLV350/L2StrongContinuity.lean', 53)} levanta uma família fortemente contínua de isometrias usando a densidade das funções simples de suporte de medida finita e constante de Lipschitz um. Na aplicação à torre a hipótese de continuidade é descarregada por `modularFlow_strongly_continuous`, {source('kernel/TGLExt/ModularFlowHilbert.lean', 104)}.

{source('kernel/TGLV350/RegularTowerRepresentation.lean', 16)} define `Uregₜ = fibre(modularFlowCLM P t) * shift t`. O tempo é o mesmo `t`, sem reparametrização. As linhas 23, 42, 54 e 73 provam grupo, unitariedade, covariância e continuidade forte. Na linha 87, `regular_covariance_on_factor` usa exatamente `V350Continuous.factorFlow P t`. A sonda positiva também verificou a formulação com `towerWedgeData.modularFlow` em `mixProfile`, explicitando apenas a saída do subtipo via `.val`.

### 5. Álgebra gerada, fidelidade e minimalidade

{source('kernel/TGLV350/RegularGeneratedAlgebra.lean', 14)} constrói a álgebra pelo duplo centralizador estelar. `generator_mem`, linha 19, trata também a condição envolvendo estrela, evitando confundir comutação simples de um conjunto arbitrário com o centralizador de uma *-álgebra. `generated_minimal`, linha 32, usa a reversão das inclusões pelo centralizador e a igualdade de bicentralizador de uma `VonNeumannAlgebra`.

Os geradores, linha 43, são a amplificação do fator da torre e os `regularUnitary P t`. `regularCoreEmbedding_injective`, linha 71, reduz a igualdade ao mapa fiel `fibre`. `regularCore_minimal`, linha 78, recebe uma álgebra de von Neumann contendo ambos os conjuntos de geradores e conclui a inclusão nela. Isso é a **minimalidade da álgebra gerada por esses operadores concretos**, não um teorema adicional de universalidade de produto cruzado.

## Gate e limites de interpretação

{source('gate_extension.py', 3)} acompanha somente os três pares termo/ponte modulares. {source('gate_extension.py', 16)} exige construção verificada, auditoria com retorno zero, `all_verified` e listas de axiomas na whitelist. {source('gate_extension.py', 58)} retorna escopo `PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT`, mantém `legacy_gate_changed = False` e `full_plan_complete = False`. Não há flag nova de regular, traço, core completo ou QG habilitada pelos resultados deste pacote.

A inspeção estática conferiu a chamada final da extensão e a inclusão da subdecisão no gate real. Os controles independentes recusam ausência de nome/ponte, falhas de auditoria, axiomas estrangeiros e flag gravitacional não coberta. A validação Python depende das evidências de compilação que recebe; a tipagem matemática é assegurada pelas pontes Lean efetivamente compiladas, não pelo texto dos nomes isoladamente.

Os seguintes pontos permanecem **[OPEN — não reivindicados por estas provas]**, sem constituir achados contra o pacote:

- Normalidade da representação em topologias de operadores, identificação completa do produto cruzado/core contínuo, ação dual e traço canônico com as propriedades pertinentes. O nome `regularCoreAlgebra` não fornece esses teoremas por si só.
- Semifinitude, classificação de tipo III₁ e realização de `ContinuousCoreData`/`ThreeLocksCoreData` no mesmo objeto. Nenhum desses contratos é preenchido aqui apenas pela álgebra gerada.
- Identificação Bisognano–Wichmann física, H1/H2/H3 no mesmo horizonte físico e setor interagente/BRST/QME/UV. A arquitetura formal local não é confirmação experimental.
- Projeção `P_F` dos Three Locks: as `levelProject P N` aqui são projeções ortogonais sobre andares crescentes e convergem fortemente à identidade, {source('kernel/TGLExt/LocalTowerProjections.lean', 52)} e linha 69. Não há identificação delas com um projetor espectral de lock nem conclusão sobre seu traço físico.

## Arquivos, hashes e rastreabilidade

Hash SHA-256 do `um.py` integrado **lido por script nesta revisão**, conferindo com os relatórios de integração e testes: `{integrated['um_sha256']}`. O hash identifica a cópia examinada; não é selo novo nem indicação de execução integral.

| Fonte recompilada independentemente | Exit | SHA-256 da fonte congelada |
|---|---:|---|
{hash_table}

Evidências locais:

- {link(RUN / 'manifest.json')}: fontes congeladas, toolchain e hashes das dependências.
- {link(RUN / 'compilation.json')}: comandos, retornos, axiomas e hashes dos `.olean` da recompilação independente.
- {link(RUN / 'base_dependency_check.json')}: comparação das {base['dependencies']} dependências com fontes e binários da base.
- {link(RUN / 'type_probes.json')}, {link(RUN / 'sources/PositiveTypes.lean')} e {link(RUN / 'sources/NegativeTypes.lean')}: sondas de enunciados e hipóteses.
- {link(RUN / 'integration_inspection.json')}: comparação AST, equivalência das fontes regulares integradas e {integration['gate_total']} controles Python independentes.
- {link(RUN / 'independent_gate_evidence.json')}: avaliação da extensão com as evidências desta recompilação, restrita às três flags modulares.
- {link(FINAL / 'verification.json')}: conferência do rebuild integrado final; cópias dos relatórios, fontes e logs estão na mesma pasta.

**Preservação:** nenhuma implementação foi editada por esta revisão; hashes das fontes acompanhadas permaneceram iguais entre congelamento e fechamento. Todas as escritas do revisor ficaram em `revisao`. Atlas e índice vivo foram apenas consultados; memórias globais não foram atualizadas. Não houve execução/importação de `um.py`, escrita no canônico ou transposição de artefatos.
'''
target = REVIEW / "REVIEW_MODULAR_AND_REGULAR.md"
raw = text.encode("utf-8")
if target.exists():
    previous = target.read_bytes()
    backup = target.with_name(target.name + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    backup.write_bytes(previous)
    assert backup.read_bytes() == previous
temporary = target.with_name(target.name + ".tmp")
temporary.write_bytes(raw)
assert temporary.stat().st_size == len(raw) and temporary.read_bytes() == raw
temporary.replace(target)
print(json.dumps({"report": str(target), "bytes": target.stat().st_size,
                  "sha256": digest(target), "implementation_sources_changed": changed}, ensure_ascii=False))
