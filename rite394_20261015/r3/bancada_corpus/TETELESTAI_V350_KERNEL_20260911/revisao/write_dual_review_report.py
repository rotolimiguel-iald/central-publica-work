from pathlib import Path
import ast
import datetime
import hashlib
import json
import re

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "dual_latest_run.txt").read_text(encoding="utf-8"))
M = json.loads((RUN / "manifest.json").read_bytes())
C = json.loads((RUN / "compilation.json").read_bytes())
PROBES = json.loads((RUN / "type_probes.json").read_bytes())
DEPENDENCIES = json.loads((RUN / "dependency_source_check.json").read_bytes())
LAYERS = sorted(RUN.glob("final_integrated_*"))
L17, L18 = LAYERS[-2], LAYERS[-1]
V17 = json.loads((L17 / "verification.json").read_bytes())
V18 = json.loads((L18 / "verification.json").read_bytes())
TOPO = sorted(RUN.glob("topology_addendum_*"))[-1]
TM = json.loads((TOPO / "manifest.json").read_bytes())
TC = json.loads((TOPO / "compilation.json").read_bytes())
REUSE = json.loads((TOPO / "integration_reuse.json").read_bytes())
SCOPE = json.loads((RUN / "integration_scope_check.json").read_bytes())

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def link(p, title=None, line=None):
    p = Path(p)
    return "[" + (title or p.name) + "](<" + p.as_posix() + (":" + str(line) if line else "") + ">)"

def source(name, line):
    return link(ROOT / "kernel/TGLV350" / (name + ".lean"), name + ".lean:" + str(line), line)

assert C["all_exit_zero"] and C["full_audit_all_expected_names"] and not C["source_changes"] and not C["frozen_dependency_changes"]
assert len(TC["records"]) == 2 and all(r["returncode"] == 0 and r["axioms_allowed"] for r in TC["records"])
assert set(TC["records"][-1]["axioms"]) == set(TM["declarations"])
assert PROBES["returncode"] == 0 and not DEPENDENCIES["current_project_source_mismatches"]
assert sha(REVIEW / "REVIEW_MODULAR_AND_REGULAR.md") == M["previous_report_sha256"]
for row in M["snapshots"].values():
    assert sha(row["dev_path"]) == row["dev_sha256"] and sha(row["integrated_path"]) == row["integrated_sha256"]
assert sha(ROOT / "kernel/TGLV350/RegularTopology.lean") == TM["dev_sha256"]
assert sha(ROOT / "kernel/TGLExt/V350RegularTopology.lean") == TM["integrated_sha256"]
assert sha(ROOT / "um.py") == V18["um_sha256"] == TM["um_sha256"]
assert V17["integrated_modules"] == 17 and V18["integrated_modules"] == 18
for v in [V17, V18]:
    assert v["all_hashes_match"] and v["all_exit_zero"] and v["exact_expected_file_set"]
    assert not v["audit_unexpected_axioms"] and v["gate_checks_all_passed"]
for row in C["records"] + TC["records"]:
    assert sha(row["command"][2]) == row["output_sha256"]

# Compare the final embedded gate as AST data; no monolithic code is executed.
tree = ast.parse((ROOT / "um.py").read_bytes())
ext = ast.parse((RUN / "integration/gate_extension.py").read_bytes())
names = {n.name for n in ext.body if isinstance(n, ast.FunctionDef)} | {"_V350_MODULAR_CONTRACTS"}
def extract(t):
    return [ast.dump(n, include_attributes=False) for n in t.body if
            (isinstance(n, ast.FunctionDef) and n.name in names) or
            (isinstance(n, ast.Assign) and any(isinstance(x, ast.Name) and x.id in names for x in n.targets))]
assert extract(tree) == extract(ext) and M["gate_extension_unchanged"]
latest_gate = json.loads((L18 / "gate_tests.json").read_bytes())["frontier"]
assert latest_gate["scope"] == "PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT"
assert latest_gate["legacy_gate_changed"] is False and latest_gate["full_plan_complete"] is False

hash_rows = []
count_rows = []
for name, row in M["snapshots"].items():
    raw = (RUN / "sources/TGLV350" / (name + ".lean")).read_text(encoding="utf-8")
    count = len(re.findall(r"^(?:noncomputable\s+)?(?:def|theorem|abbrev)\s+\w+", raw, re.M))
    count_rows.append("| " + source(name, 1) + " | exit 0 | " + str(count) + " |")
    hash_rows.append("| " + name + " | `" + row["dev_sha256"] + "` | `" + row["integrated_sha256"] + "` |")
hash_rows.append("| RegularTopology | `" + TM["dev_sha256"] + "` | `" + TM["integrated_sha256"] + "` |")
timestamp = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
report = f'''# Revisão adversarial independente — ação dual, limites fortes limitados e adendo WOT

Fechamento: {timestamp}. Bancada: `{ROOT}`. Escritas restritas a `revisao`.

**[REAL — fontes, recompilação e auditoria independentes] Parecer favorável aos quatro módulos solicitados e ao adendo `RegularTopology`, nos enunciados efetivamente provados. Nenhum defeito concreto P0–P3 identificado.** `Ad(Dₛ)` restringe-se a um automorfismo da álgebra gerada inteira, fixa a inclusão do fator e satisfaz Weyl com sinal negativo e lei de grupo. A amplificação preserva limites fortes sob cota global uniforme para filtros arbitrários. O adendo prova bicomutante ⇒ fechado em WOT.

**Escopo:** esses resultados não fornecem, por si só, certificado de core tracial, traço canônico, Three Locks ou QG. Nenhum gate adicional foi habilitado. O parecer anterior {link(REVIEW / 'REVIEW_MODULAR_AND_REGULAR.md')} permanece byte a byte intacto.

## Achados priorizados

**Nenhum achado corretivo demonstrado nos cinco módulos.** Foram especificamente examinados: inversão do sinal da fase, ordem de composição de automorfismos, restrição só sobre geradores, troca da realização/Hilbert, omissão da cota uniforme, redução indevida a sequências e confusão entre WOT e norma de operador. A análise e as sondas abaixo não encontraram esses defeitos.

Ausência de normalidade formalizada, traço e demais contratos físicos não foi classificada como bug: não são conclusões reivindicadas por este pacote. Os limites de leitura são explicitados ao fim.

## Evidência independente e fronteira de confiança

| Módulo dev recompilado | Resultado | Declarações auditadas integralmente |
|---|---|---:|
{chr(10).join(count_rows)}
| {source('RegularTopology', 1)} — adendo | exit 0 | {len(TM['declarations'])} |

Os quatro módulos iniciais passaram **4/4** em uma árvore própria. `DualFullAudit.lean` passou e auditou **{len(M['all_declarations'])}/{len(M['all_declarations'])} declarações**, incluindo auxiliares não impressos nas fontes standalone. O adendo passou **1/1**, e `TopologyFullAudit.lean` auditou **3/3** teoremas. Portanto, **57 declarações dos cinco módulos** foram verificadas independentemente com axiomas contidos em `{{propext, Classical.choice, Quot.sound}}`. Os hashes dos `.olean` produzidos foram reconferidos.

As **{len(M['dependencies'])} dependências de projeto** vieram dos binários congelados e da recompilação bem-sucedida da revisão anterior. Foram copiadas para a nova árvore e conferidas por SHA-256; suas fontes atuais coincidem com as fontes congeladas. Nenhum desses binários foi modificado durante a recompilação. Não se usou o build de projeto em mutação do implementador como fallback. Lean/Mathlib instalados continuam como base de confiança, lidos em modo somente leitura; não reconstruí nem recopieI integralmente Mathlib. Compilador: `{M['lean_version']}`.

As quatro fontes dev e suas versões `TGLExt/V350*.lean` diferem apenas pelo prefixo de importação. O mesmo foi verificado para `RegularTopology`; os cinco conteúdos integrados conferem com o monólito. O monólito foi tratado apenas como dados/AST, sem execução ou importação.

**Sonda independente adicional:** {link(RUN / 'sources/DualTypeBoundary.lean')} passou, verificando conjuntamente (a) a fase negativa sobre o gerador já inserido como elemento da álgebra, (b) a inversa com tempo `−s` para qualquer elemento da álgebra, (c) a mesma inclusão fixada e (d) o lema sob `Filter ι` de universo arbitrário, sem topologia no índice e sem `NeBot`. A primeira tentativa atingiu o limite padrão de 200 mil heartbeats ao elaborar a inversa; a repetição com o orçamento de um milhão já usado nos módulos passou. Fonte, log e registro anteriores foram preservados em backups. Não houve mudança de prova na implementação.

## Conferência dos quatro módulos

### Multiplicador de caracteres e sinal de Weyl

{source('L2CharacterMultiplier', 21)} define exatamente `characterPhase s x = exp(−i s x)`. `RegularHilbert H` continua sendo Lebesgue `Lp H 2 volume`, com `H` Hilbert complexo completo. As linhas 54–74 provam integrabilidade e preservação da norma antes de construir o operador no quociente quase em toda parte. As leis lineares, grupo, inversa e adjunto são verificadas nas linhas 76–148; `star Dₛ = D₋ₛ` é o adjunto de operador, não conjugação escalar aplicada a um objeto de outro tipo.

O cálculo escalar de {source('L2CharacterMultiplier', 46)} é:

`exp(−i s x) · exp(+i s (x−t)) = exp(−i s t)`.

Isso paga precisamente {source('L2CharacterMultiplier', 160)}: `Dₛ Sₜ Dₛ* = exp(−i s t) • Sₜ`, para `(Sₜ f)(x)=f(x−t)`. A igualdade quase em toda parte da segunda fase é transportada pela translação preservadora de Lebesgue; não se pressupõe igualdade pontual de representantes de `Lp`.

{source('L2CharacterMultiplier', 179)} usa convergência dominada dos coeficientes com majorante integrável `‖f(x)‖²`. A identidade da norma ao quadrado e a raiz quadrada dão continuidade forte na linha 206. O parâmetro é ℝ com sua topologia usual. Não há afirmação de continuidade em norma de operador.

### Transporte do bicomutante e restrição completa

{source('GeneratedEquivariance', 12)} trata as duas condições do **centralizador estelar** e usa injetividade do `StarAlgEquiv` para voltar. `centralizer_image`, linha 33, usa a inversa para pagar a sobrejetividade, requisito indispensável ao transporte de todo o centralizador.

{source('GeneratedEquivariance', 48)} transporta o bicomutante aplicando esse resultado duas vezes. A prova é algébrica; não pressupõe continuidade de um automorfismo abstrato para transportar um fecho topológico. `generated_maps_into`, linha 56, usa a minimalidade da álgebra gerada para estender a preservação dos geradores a **todos** os elementos.

{source('GeneratedEquivariance', 66)} exige preservação dos geradores tanto por `e` quanto por `e.symm`. Constrói ida, volta e ambas as inversas no mesmo subtipo da álgebra gerada. Esses dois pressupostos do lema geral estão explícitos e são efetivamente descarregados em `RegularDualAction`; não ficam como dívida do resultado final.

### Ação dual no mesmo objeto

{source('RegularDualAction', 18)} define o automorfismo ambiente por conjugação pelo unitário construído `Dₛ`. A fórmula na linha 23 é literalmente `Dₛ A Dₛ*`. `dualAmbient_add`, linha 30, considera corretamente que `(eₛ.trans eₜ)(A)=eₜ(eₛ(A))`; a comutatividade do grupo aditivo permite escrever `D_(s+t)=DₜDₛ`. Não há erro de ordem disfarçado na lei de grupo.

{source('RegularDualAction', 54)} atua sobre **o mesmo** `regularUnitary P t = fibre(modularFlowCLM P t) * shift t` da revisão anterior. A fibra modular comuta com `Dₛ`, portanto o fator escalar continua `exp(−i s t)`, com os mesmos parâmetros e o mesmo `P`.

{source('RegularDualAction', 65)} preserva a primeira classe de geradores por igualdade e a segunda por multiplicação escalar dentro da *-álgebra. Na linha 76, `regularDualAction P s` tem tipo fechado:

`(regularCoreAlgebra P).toStarSubalgebra ≃⋆ₐ[ℂ] (regularCoreAlgebra P).toStarSubalgebra`.

A preservação inversa é demonstrada com `dualAmbient_symm` e o resultado para `−s`. Não se cria outra álgebra, outra cópia do fator nem uma lista formal de geradores usada como substituto da álgebra inteira. As linhas 83–114 provam a fórmula da restrição, identidade, composição e fixação da inclusão original `regularCoreEmbedding P`.

{source('RegularDualAction', 122)} aplica continuidade conjunta da família isométrica `Dₛ` ao vetor variável `A(D₋ₛ f)`. Isso justifica a continuidade forte da conjugação sem assumir continuidade conjunta irrestrita do produto de operadores na topologia forte. Na linha 144, a conclusão restringe-se a cada `A` da álgebra gerada e cada vetor `f`. O lema da linha 136 tem `s` fixo e transporta continuidade forte de famílias arbitrárias `A(z)`; não troca essa quantificação pela continuidade simultânea de todos os parâmetros.

### Amplificação e limites fortes uniformemente limitados

{source('L2BoundedStrongContinuity', 20)} usa a estimativa `‖fibre T‖ ≤ ‖T‖`. O controle de Lipschitz da linha 30 toma `max C 0`, garantindo uma constante não negativa sem supor que o índice tenha habitantes. Isso não remove a hipótese real `‖T‖ ≤ C` onde há um operador.

{source('L2BoundedStrongContinuity', 40)} prova continuidade conjunta para qualquer espaço topológico `Z`, com cota global `∀ z, ‖T z‖ ≤ C` e continuidade forte da família original. A passagem por indicadores de conjuntos de medida finita e funções simples densas usa os lemas da mesma amplificação `fibre` previamente revisada.

{source('L2BoundedStrongContinuity', 70)} é um enunciado genuinamente sobre **filtros arbitrários**:

`∀ i, ‖T i‖ ≤ C` e `∀ v, T i v →[l] S v` implicam `∀ f, fibre(T i) f →[l] fibre(S) f`.

Não há instância `TopologicalSpace ι`, primeira enumerabilidade, escolha de subsequência ou premissa `NeBot l`. Para o filtro vazio, a conclusão tem a semântica usual de convergência vacuamente verdadeira; não se afirma unicidade do limite nesse caso. `S` já é fornecido como operador linear contínuo, porém não recebe hipótese separada `‖S‖ ≤ C`.

A cota uniforme dá equicontinuidade. `Equicontinuous.isClosed_setOf_tendsto` torna fechado o conjunto de vetores para os quais a convergência vale, usando a continuidade de `fibre S`. O conjunto contém as funções simples densas, logo contém todo L². Não se intercambia um limite geral com uma integral sem hipótese de dominação nem se usa compacidade do índice. **A cota é global em todos os índices, não apenas eventual**; a versão com cota eventual não está enunciada aqui.

## Adendo — `RegularTopology.lean`

**[REAL — recompilação independente]** Fonte congelada com {TM['source_lines']} linhas; SHA-256 lido `{TM['dev_sha256']}`. O módulo e a auditoria completa passaram; os três teoremas têm somente axiomas do trio.

{source('RegularTopology', 11)} transporta o centralizador ordinário de operadores limitados para a cópia `ContinuousLinearMapWOT`, por `ofCLM`/`toCLM` e suas propriedades algébricas. A função `toCLM` é usada para identificar o portador; a prova não precisa nem reivindica sua continuidade da WOT para a norma.

{source('RegularTopology', 26)} reescreve o portador de uma `VonNeumannAlgebra` como o centralizador do seu centralizador. Após transportar o centralizador externo à cópia WOT, aplica `Set.isClosed_centralizer`. A assinatura desse lema foi conferida na auditoria: exige **multiplicação separadamente contínua** e espaço Hausdorff, não multiplicação conjuntamente contínua. A definição Mathlib de `ContinuousLinearMapWOT` foi consultada: sua topologia é induzida pelos coeficientes `y(Ax)`; trata-se efetivamente de WOT.

{source('RegularTopology', 39)} aplica a direção geral à mesma `regularCoreAlgebra P`. Não afirma a conversa “WOT fechada ⇒ bicomutante”, a existência de predual, normalidade de traço ou normalidade da inclusão. O nome `vonNeumann_wot_closed` corresponde ao enunciado efetivo. Nenhum defeito corretivo encontrado no adendo.

## Integração: estratos 17 e 18 preservados

| Estrato | Evidência conferida nesta revisão | SHA-256 do monólito lido |
|---|---|---|
| 17 módulos | 17 registros exit 0; 11 reaproveitados da etapa anterior e 6 recompilados (4 novos + 2 raízes); {V17['gate_checks_count']} controles Python registrados; {V17['audit_distinct']} declarações distintas no trio. | `{V17['um_sha256']}` |
| **18 módulos — final** | 18 registros exit 0; {REUSE['reused_count']} reaproveitados do estrato 17 e {REUSE['rebuilt_count']} recompilados (`RegularTopology` + 2 raízes); {V18['gate_checks_count']} controles Python registrados; {V18['audit_distinct']} declarações distintas no trio. | `{V18['um_sha256']}` |

Ambos os estratos tiveram o conjunto esperado de arquivos, os hashes de fontes e os hashes de `.olean` reconferidos. O estrato final embute **{TM['embedded_files']} arquivos**, com 16 arquivos novos e 2 raízes atualizadas no rebuild. As contagens de auditoria foram recalculadas dos stdout, sem depender apenas da contagem declarada no relatório. Reaproveitamento foi identificado comparando fonte, binário e registro com o estrato anterior.

Estas linhas descrevem **inspeção independente dos registros/binários do implementador**. Não são 18 recompilações feitas por este revisor. A recompilação independente aqui abrange os cinco módulos e suas auditorias; a suíte Python integral de 44 controles foi conferida pelos registros, sem ser reexecutada nesta revisão adicional.

O `gate_extension.py` permaneceu idêntico à revisão anterior e à versão embutida no monólito final, conferida por AST. O relatório final mantém escopo `PRODUCT_TOWER__J_M_J_EQUALS_COMMUTANT`, `legacy_gate_changed = False` e `full_plan_complete = False`. Nenhuma flag adicional foi habilitada por ação dual, continuidade limitada ou WOT.

## Limites que permanecem explícitos

- **Normalidade como teorema/contrato formal:** há continuidade forte da ação e preservação de limites fortes uniformemente limitados pela amplificação. Não se apresentou nesta etapa a ponte formal para preservação de supremos positivos ou continuidade ultra-fraca. Esses resultados são insumos analíticos para essa ponte; não justificam atribuir um campo formal ainda não construído.
- **Traço/core tracial:** não há construção de traço canônico normal semifinito fiel, lei de escala dual de um traço construído, predual ou pacote completo de `ContinuousCoreData`. A ação dual concreta sobre a álgebra gerada não supre esses objetos por nomenclatura.
- **Three Locks e física:** nenhum `P_F` é construído ou identificado nestes cinco arquivos. Canto finito positivo, H1–H3 compatíveis e demais requisitos físicos continuam fora das conclusões auditadas. Não há aprovação de QG.
- **Topologias:** continuidade forte pontual não é continuidade em norma de operador; fechamento em WOT não prova a conversa do teorema do bicomutante nem, sozinho, normalidade de um mapa ou de um traço.

## Hashes e evidências reproduzíveis

| Módulo | SHA-256 dev congelado | SHA-256 integrado |
|---|---|---|
{chr(10).join(hash_rows)}

- {link(RUN / 'manifest.json')} e {link(RUN / 'compilation.json')}: fontes, dependências, comandos, hashes de binários, retornos e axiomas da revisão dos quatro módulos.
- {link(RUN / 'logs/DualFullAudit.stdout.txt')}: todas as 54 assinaturas e dependências axiomáticas.
- {link(RUN / 'dependency_source_check.json')}: as 305 fontes de dependências coincidem com o congelamento anterior; inclui a versão declarada no manifesto local de Mathlib.
- {link(RUN / 'type_probes.json')} e {link(RUN / 'sources/DualTypeBoundary.lean')}: sondas de sinal, inversa inteira, inclusão e filtros.
- {link(TOPO / 'manifest.json')}, {link(TOPO / 'compilation.json')} e {link(TOPO / 'logs/TopologyFullAudit.stdout.txt')}: adendo WOT e auditoria dos três teoremas.
- {link(L17 / 'verification.json', 'Estrato 17 — conferência')} e {link(L18 / 'verification.json', 'Estrato 18 — conferência final')}: cópias dos relatórios, fontes integradas e logs de cada estrato.
- {link(RUN / 'integration_scope_check.json')} e {link(TOPO / 'integration_reuse.json')}: escopo do gate e reaproveitamento entre etapas.

**Preservação final:** SHA-256 do parecer anterior reconferido `{M['previous_report_sha256']}`; conteúdo intacto. As cinco fontes dev e integradas mantêm os hashes congelados. Esta revisão não editou implementação, memórias globais ou originais, nem executou/importou `um.py`. Todas as escritas permaneceram em `revisao`; não houve transposição ao canônico.
'''
report = report.replace("recopieI", "recopiei")
target = REVIEW / "REVIEW_DUAL_AND_BOUNDED.md"
raw = report.encode("utf-8")
if target.exists():
    old = target.read_bytes()
    backup = target.with_name(target.name + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    backup.write_bytes(old)
    assert backup.read_bytes() == old
temporary = target.with_name(target.name + ".tmp")
temporary.write_bytes(raw)
assert temporary.read_bytes() == raw and temporary.stat().st_size == len(raw)
temporary.replace(target)
print(json.dumps({"report": str(target), "bytes": len(raw), "sha256": sha(target),
                  "previous_report_preserved": sha(REVIEW / "REVIEW_MODULAR_AND_REGULAR.md") == M["previous_report_sha256"]}, ensure_ascii=False))
