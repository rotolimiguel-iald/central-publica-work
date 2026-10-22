from pathlib import Path
import datetime
import hashlib
import json

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "dual_weight_latest_run.txt").read_text(encoding="utf-8"))
M = json.loads((RUN / "manifest.json").read_bytes())
C = json.loads((RUN / "compilation.json").read_bytes())
ADDENDUM = sorted(RUN.glob("exhaustion_addendum_*"))[-1]
AM = json.loads((ADDENDUM / "manifest.json").read_bytes())
AC = json.loads((ADDENDUM / "compilation.json").read_bytes())
FINAL = sorted(RUN.glob("final_integrated_*"))[-1]
F = json.loads((FINAL / "verification.json").read_bytes())

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def link(label, path, line=None):
    return "[" + label + "](<" + Path(path).as_posix() + ((":" + str(line)) if line else "") + ">)"

def ref(module, declaration):
    rel = "TGLV350/" + module + ".lean"
    snapshot = Path(AM["snapshot"]) if module == "DualWeightExhaustion" else Path(M["sources"][rel]["snapshot"])
    lines = snapshot.read_text(encoding="utf-8").splitlines()
    n = next(i+1 for i, text in enumerate(lines) if any(word + " " + declaration in text for word in ["def", "theorem", "structure"]))
    return link(module + ".lean:" + str(n), ROOT / "kernel" / rel, n)

si = lambda n: ref("StrongOperatorIntegral", n)
dc = lambda n: ref("DualWeightCuts", n)
df = lambda n: ref("DualWeightForm", n)
de = lambda n: ref("DualWeightExhaustion", n)
assert C["all_exit_zero"] and C["full_audit_names_exact"] and C["all_axioms_allowed"]
assert AC["all_exit_zero"] and AC["audit_names_exact"] and all(r["axioms_allowed"] for r in AC["records"])

rows = []
for rel, row in M["sources"].items():
    record = next(r for r in C["records"] if r["module"] == rel)
    rows.append("| " + link(Path(rel).name, row["snapshot"]) + " | " + str(row["lines"]) + " | " + str(record["returncode"]) + " | `" + row["sha256"] + "` |")
rows.append("| " + link("DualWeightExhaustion.lean — adendo", AM["snapshot"]) + " | " + str(AM["source_lines"]) + " | " + str(AC["records"][0]["returncode"]) + " | `" + AM["source_sha256"] + "` |")
integrated_rows = ["| " + name + " | `" + row["integrated_sha256"] + "` |" for name, row in F["source_matches"].items()]
preserved = {p: sha(Path(p).read_bytes()) == h for p, h in M["previous_reviews"].items()}
assert all(preserved.values())
source_status = {rel: sha(Path(row["path"]).read_bytes()) == row["sha256"] for rel, row in M["sources"].items()}
source_status["TGLV350/DualWeightExhaustion.lean"] = sha(Path(AM["source"]).read_bytes()) == AM["source_sha256"]
assert all(source_status.values())
dependency_status = all(sha(Path(row["frozen_binary"]).read_bytes()) == row["sha256"] and sha(Path(row["frozen_source"]).read_bytes()) == row["source_sha256"] for row in M["dependencies"].values())
assert dependency_status

report = f'''# Revisão independente — cortes da ação dual e avaliação integral ENNReal

Data: 11/09/2026. Bancada: `{ROOT}`.

**Parecer delimitado [REAL]: nenhum defeito substantivo bloqueante encontrado nas quatro fontes estabilizadas, nos tipos e nas composições examinadas.** Os três módulos inicialmente autorizados foram recompilados independentemente. `DualWeightExhaustion` foi recompilado posteriormente, após o aviso de estabilidade e a ampliação expressa do escopo, em adendo separado. As quatro recompilações terminaram com exit 0.

A auditoria própria cobriu **44 declarações escritas e seis declarações geradas por `Family`, totalizando 50**, sem axiomas além de `propext`, `Classical.choice` e `Quot.sound`. Três conferências adicionais de identidade/tipagem também passaram.

O resultado é uma construção de **operadores de corte por integrais vetoriais**, com positividade e monotonicidade dos cortes positivos, e de **avaliações escalares estendidas em ENNReal**, incluindo sua exaustão por cortes. Não é construção do cone ampliado da base, de um peso dual canônico ou de um traço. O parecer não atribui esses resultados a flags de core, canto ou testemunha completa.

## 1. Evidência e achados priorizados

**P0/P1/P2 — nenhum defeito concreto encontrado no incremento delimitado.** Em particular, não encontrei integração Bochner indevida na norma de B(H), integrabilidade assumida implicitamente, troca do bicomutante, uso da aditividade de `ENNReal.ofReal` sem positividade, perda do fator constante, sinal incompatível na composição da ação, ou substituição de um supremo escalar infinito por um operador limitado.

Os seguintes limites são parte do enunciado e **não são classificados como bugs**:

- Os cortes positivos exigem `R ≥ 0` e `A ≥ 0`. A monotonicidade em raio exige também `R ≤ S`. A família integral genérica exige continuidade forte e uma cota global de norma explicitamente fornecida.
- A avaliação ENNReal é definida em todo operador `A`, mas as leis de aditividade e de identificação com a avaliação do corte têm hipóteses de positividade. Não foi provada uma aplicação linear sobre todos os operadores.
- O fator `(2π)⁻¹` é uma constante escolhida e positiva. O vínculo dessa escolha com uma convenção de Fourier/Plancherel não é um teorema Lean deste pacote.
- A exaustão vive em ENNReal para cada vetor. Não produz um elemento do cone ampliado, um supremo limitado em B(H), semifinitude ou um traço.

**Modalidades efetivamente realizadas:** inspeção semântica das fontes e dos tipos impressos; recompilação independente das quatro fontes; auditoria própria dos 50 nomes; três conferências próprias de tipos; inspeção estática e conferência de hashes da integração final do autor. As raízes integradas e os 48 controles Python não foram reexecutados por este revisor nesta etapa.

## 2. `StrongOperatorIntegral`: integração em vetores e mesmo bicomutante

{si('Family')} fornece `op : ℝ → (H →L[ℂ] H)`, continuidade de `t ↦ op t v` para cada vetor e `‖op t‖ ≤ bound`, com `bound ≥ 0`. Não contém hipótese de continuidade em norma de operadores nem uma hipótese de integrabilidade Bochner com valores em B(H).

{si('vectorIntegral')} tem valor em **H**: `∫ t in a..b, F.op t v`. A continuidade vetorial dá `IntervalIntegrable` em cada intervalo compacto, utilizada explicitamente na aditividade e na passagem de aplicações lineares pela integral. Assim, a construção não depende da convenção de integral nula para um integrando não integrável. A linearidade complexa e a estimativa

`‖vectorIntegral F a b v‖ ≤ (F.bound * |b-a|) * ‖v‖`

permitem a construção efetiva de `H →L[ℂ] H` por `mkContinuous` em {si('operatorIntegral')}. A estimativa de norma do operador é comprovada em {si('operatorIntegral_norm_le')}. A integral pode ser orientada para quaisquer `a,b`; a positividade só é afirmada quando `a ≤ b`.

{si('operatorIntegral_commutes')} move um **operador fixo limitado B** através da integral vetorial. Se B comuta com todos os integrandos, comuta com o operador resultante. {si('operatorIntegral_mem')} aplica esse fato a cada elemento do comutante da mesma `VonNeumannAlgebra N` e usa `N'' = N`. A orientação da igualdade de comutação é ajustada por simetria, sem trocar N por um modelo isomorfo. Essa prova usa diretamente o bicomutante; não precisa construir somas de Riemann ou supor integral em norma de operadores.

As identidades de produtos internos em {si('inner_operatorIntegral')}, {si('re_inner_operatorIntegral')} e {si('operatorIntegral_inner')} respeitam a convenção complexa: linearidade na segunda entrada e conjugação na primeira. A prova de positividade em {si('operatorIntegral_nonneg')} verifica simetria e não negatividade da forma quadrática. A monotonicidade em {si('operatorIntegral_mono_interval')} assume `c ≤ a ≤ b ≤ d` e positividade de todos os integrandos; conclui a ordem de Loewner entre os dois operadores integrados. Não confunde ordem de operadores com comparação de normas.

## 3. `DualWeightCuts`: a órbita dual efetivamente construída

{dc('dualIntegralFamily')} usa exatamente `dualAmbient s A`, com continuidade forte já fornecida para todos os vetores e cota `‖A‖` obtida da isometria do automorfismo unitário. O operador é aquele do espaço `RegularHilbert H = Lp H 2 (volume : Measure ℝ)`; para a torre, `H = TowerHilbert P`.

{dc('dualWeightCut')} define `T_R(A)` pelo intervalo orientado `(-R)..R`. {dc('dualWeightCut_norm_le')} prova `‖T_R(A)‖ ≤ ‖A‖ |2R|` para todo R. A positividade exige `R ≥ 0` e `A ≥ 0`, em {dc('dualWeightCut_nonneg')}. A monotonicidade provada em {dc('dualWeightCut_mono_radius')} é **em relação ao raio**: `0 ≤ R ≤ S` implica `T_R(A) ≤ T_S(A)` para A positivo. Não a relato como um teorema separado de monotonicidade em A, que não foi escrito nesse módulo.

{dc('dualWeightCut_mem')} vale para todo `A ∈ regularCoreAlgebra P`, não apenas para os geradores. O pertencimento dos integrandos é extraído de `(regularDualAction P s ⟨A,hA⟩).property`. A coerção dessa ação restrita coincide definicionalmente com `dualAmbient`; essa identidade foi ainda conferida em um exemplo próprio, com a integral inteira escrita usando `regularDualAction` no mesmo subtipo. O resultado permanece no mesmo bicomutante concreto.

{dc('dualWeightCut_fibre')} dá `T_R(fibre A) = (2R) • fibre A` porque a ação dual fixa essa amplificação. {dc('dualWeightCut_one')} especializa para a unidade. Essas igualdades conservam o comprimento do intervalo; não são médias divididas por `2R`. Elas também não dizem que todos os cortes de todo A pertencem à imagem da base: o pertencimento provado é à álgebra regular gerada.

## 4. `DualWeightForm`: constante, positividade, invariância e avaliação

**Normalização.** {df('dualHaarFactor')} é literalmente `(2 * Real.pi)⁻¹ : ℝ`; {df('dualHaarFactor_pos')} prova positividade estrita. {df('normalizedDualCut')} multiplica o corte por essa constante fixa, não por um fator dependente de R. A passagem entre escalares reais e sua coerção complexa nas provas de positividade e pertencimento conserva o mesmo CLM. Uma conferência própria confirmou por `rfl` a fórmula com `(2π)⁻¹`.

O pacote prova positividade e pertencimento do corte normalizado em {df('normalizedDualCut_nonneg')} e {df('normalizedDualCut_mem')}. A monotonicidade dos cortes normalizados segue matematicamente da positividade do escalar e da monotonicidade dos cortes crus; não há um teorema separado com esse nome na fonte, e não o conto como declaração adicional compilada.

**Domínio da avaliação.** {df('dualQuadraticIntegrand')} é

`ENNReal.ofReal (Re ⟨v, dualAmbient s A v⟩)`.

{df('dualQuadraticIntegral')} define

`q_A(v) = ENNReal.ofReal ((2π)⁻¹) * ∫⁻ s, dualQuadraticIntegrand A v s`.

O alvo é ENNReal, com infinito permitido, e a medida é Lebesgue. A definição total para A arbitrário aplica o truncamento de `ofReal` à parte real; não é, por isso só, uma forma quadrática estendida com todas as leis usuais. A mensurabilidade é comprovada por continuidade da avaliação escalar, inclusive para A não positivo.

**Aditividade positiva.** {df('dualQuadraticIntegral_add')} declara explicitamente `(hA : 0 ≤ A)` e `(hB : 0 ≤ B)`. {df('dualQuadratic_nonneg')} assegura não negatividade das duas avaliações antes de usar `ENNReal.ofReal_add`. A soma passa pela integral não negativa usando mensurabilidade. Nenhuma hipótese de finitude dos integrais é usada, nem subtração de infinitos. As leis de zero para A e para v também foram auditadas.

**Invariância dual e composição.** {df('dualQuadraticIntegral_dual_invariant')} vale até para A arbitrário, porque a transformação é uma translação da função já truncada: `dualAmbient s (dualAmbient r A)` corresponde a `dualAmbient (r+s) A`. O lema `dualAmbient_add` usa `StarAlgEquiv.trans` nessa ordem; a fonte não confunde a ordem de composição. `lintegral_add_left_eq_self` usa a invariância de Lebesgue por translação. Isso prova `q_(θ_r A)(v) = q_A(v)`; não é uma lei de escala tracial nem uma construção de um objeto operadorial fixo na base.

**Corte restrito.** {df('dualWeightCut_quadratic')} afirma, para `R ≥ 0` e `A ≥ 0`,

`ofReal (Re ⟨v, T_R(A)v⟩) = ∫⁻ s in Ioc (-R) R, dualQuadraticIntegrand A v s`.

O lado esquerdo avalia o operador vetorial anteriormente construído. A prova move o funcional pela integral, usa a orientação correta e aplica `ofReal_integral_eq_lintegral_ofReal` com integrabilidade real e não negatividade demonstradas. O conjunto formal é **(-R,R]**, compatível com a integral de intervalo de Lean; a notação informal de corte fechado não deve apagar essa precisão. Seus extremos não afetam a integral de Lebesgue.

{df('dualWeightCut_quadratic_le')} conserva o fator `ofReal dualHaarFactor` ao comparar o corte com o integral total. É uma desigualdade escalar em ENNReal, não uma comparação com um operador ilimitado já construído.

**Unidade infinita.** {df('dualQuadraticIntegral_one')} exige `v ≠ 0`. A ação preserva 1, a avaliação constante é `‖v‖² > 0` e `volume univ = ∞`; os dois fatores positivos não nulos permitem concluir `q_1(v)=∞`. O caso v=0 é tratado pela lei `dualQuadraticIntegral_zero_vector`, com resultado zero. Não houve uso de cancelamento inválido em `0 * ∞`.

## 5. Adendo autorizado após estabilização — `DualWeightExhaustion`

O manifesto inicial dos três módulos permanece intacto e conserva a exclusão que vigorava ao criá-lo. O aviso posterior autorizou este adendo, cuja fonte, log do autor, manifesto e compilação estão em diretório separado. Não se recompilou o arquivo enquanto permanecia declarado editável pelo pai.

Os três enunciados adicionais foram inspecionados e recompilados:

1. {de('lintegral_eq_iSup_symmetric_cuts')} assume somente `f : ℝ → ENNReal` mensurável. Define `g_n = 1_{{(-n,n]}} f`, prova a mensurabilidade e monotonicidade dos indicadores e demonstra pontualmente `sup_n g_n = f`. Para cada s escolhe n com `|s| < n`, preservando o extremo esquerdo estrito; portanto não perde pontos na união. `lintegral_iSup` aplica convergência monótona à sequência, inclusive para valor infinito. Não usa convergência dominada nem limite em norma de operadores.
2. {de('dualQuadraticIntegral_eq_iSup_cuts')} exige A positivo e aplica a identidade anterior ao integrando já mensurável. `ENNReal.mul_iSup` transporta o fator fixo através do supremo, e a igualdade de avaliação dos cortes identifica cada termo. O supremo é sobre `n : ℕ`, com raio `(n : ℝ)`; n=0 dá intervalo vazio e não prejudica a exaustão. A conclusão é `q_A(v) = sup_n [(2π)⁻¹ * avaliação_ENN(T_n(A),v)]`.
3. {de('dual_unit_cut_supremum_infinite')} combina a identidade com `q_1(v)=∞` para `v ≠ 0`. O resultado afasta a interpretação dos cortes como uma família de médias que preserva a unidade, sem pretender construir um supremo limitado de operadores.

Os termos normalizados no supremo estão escritos como `ofReal dualHaarFactor * ofReal (Re ⟨v,T_n(A)v⟩)`. São avaliações escalares com o fator constante; a fonte não muda o tipo do supremo para uma álgebra ou um cone ampliado. A exaustão usa uma sequência cofinal de raios para esta integral, não uma nova afirmação de normalidade para redes arbitrárias de operadores.

## 6. Recompilação independente: arquivos, hashes e base de confiança

Compilador: `{M['lean_version']}`. Executável, hash, `LEAN_PATH` e comandos completos constam dos manifestos e registros.

| Fonte efetivamente recompilada | Linhas medidas | Exit | SHA-256 da fonte |
| --- | ---: | ---: | --- |
{chr(10).join(rows)}

Foram congeladas **{len(M['dependencies'])} dependências de projeto**, com cópias de fontes e binários e hashes conferidos. O `LEAN_PATH` começa pela árvore própria e exclui os builds vivos do projeto pai e do projeto canônico. `DualWeightCuts` usa o `StrongOperatorIntegral` recompilado aqui; `DualWeightForm` usa esses binários próprios; o adendo usa o `DualWeightForm` recompilado aqui. Não se reutilizou o parecer anterior como prova dos módulos novos.

Os pacotes de biblioteca instalados, incluindo Mathlib, foram usados em modo de leitura. **Limite da independência:** o compilador e a biblioteca Mathlib não foram reconstruídos nem tiveram a árvore integral de binários duplicada nesta etapa. O congelamento/hash por módulo aqui declarado cobre as dependências de projeto; não é uma auditoria integral da implementação de Lean/Mathlib.

O primeiro grupo auditou 41 declarações escritas, incluindo `Family`, e seis nomes gerados: construtor e projeções. O adendo auditou três teoremas. A lista efetiva de axiomas coincidiu com todos os nomes esperados; nenhum ficou fora do trio permitido. Os dois arquivos próprios de auditoria também compilaram com exit 0. No adendo, três exemplos adicionais verificaram a mesma ação restrita sob a integral, o fator constante e o codomínio vetorial da integral.

Evidência reproduzível:

- {link('Manifesto dos três módulos e das 314 dependências', RUN/'manifest.json')}.
- {link('Compilações independentes e auditoria dos primeiros 47 nomes', RUN/'compilation.json')} e {link('tipos e axiomas impressos', RUN/'logs/DualWeightFullAudit.stdout.txt')}.
- {link('Manifesto separado do adendo', ADDENDUM/'manifest.json')} e {link('compilação/auditoria do adendo e três conferências de tipos', ADDENDUM/'compilation.json')}.
- {link('Fonte própria da auditoria e das conferências do adendo', ADDENDUM/'sources/ExhaustionFullAudit.lean')}.

## 7. Integração final do autor: evidência inspecionada, não recompilação das raízes pelo revisor

**SHA-256 do monólito experimental lido e conferido:** `{F['um_sha256']}`.

O hash coincide com `integration.json` e `gate_tests.json`. A análise estática do dicionário embutido encontrou {F['embedded_files']} fontes, sem execução ou importação de `um.py`. Os quatro fontes integrados coincidem com os snapshots dev exceto pelas substituições previstas de caminhos de importação; seus bytes também coincidem com o conteúdo embutido:

| Módulo integrado | SHA-256 da fonte integrada |
| --- | --- |
{chr(10).join(integrated_rows)}

**Conferido em arquivos/logs do autor:** {F['integrated_modules']}/{F['integrated_modules']} registros Lean com exit 0, todos com hash de fonte e `.olean` correspondentes; {F['gate_checks_count']}/{F['gate_checks_count']} controles Python marcados aprovados; {F['audit_distinct']} declarações distintas no Audit, sem axiomas fora do trio. O conjunto de registros coincide com os módulos acrescentados e as duas raízes descritos na integração. Não declaro ter executado essas 25 compilações integradas ou os 48 controles: executei as quatro recompilações dev e as auditorias próprias acima.

O estrato anterior, 21 módulos/46 controles/5.897 alvos, foi preservado. A comparação mostrou 19 módulos anteriores com os mesmos hashes de fonte e binário; as seis compilações novas correspondem aos quatro módulos desta etapa e às duas raízes. Entre os fontes antigos embutidos, mudaram apenas `TGLExt.lean` e `TGL/Audit.lean`. O AST Python fora do dicionário embutido é idêntico ao backup do estrato 21, de hash `{F['previous_um_sha256']}`; `gate_extension.py` é byte a byte idêntico ao daquele estrato.

Os dois controles novos registrados são `extended_dual_integral_is_not_a_canonical_trace_certificate` e `infinite_unit_does_not_supply_a_finite_three_locks_corner`. Seus resultados foram lidos no relatório do autor; não foram reexecutados aqui. A extensão do gate continua com escopo modular e não recebeu os novos nomes como quitação de core, traço ou Three Locks.

Evidência congelada: {link('verificação independente dos hashes e comparação entre estratos', FINAL/'verification.json')}, {link('compilações integradas do autor', FINAL/'integrated_compile.json')}, {link('controles Python do autor', FINAL/'gate_tests.json')} e {link('nomes/axiomas extraídos do Audit', FINAL/'axioms.json')}.

## 8. Limitações e preservação

A nota {link('DUAL_WEIGHT_CONSTRUCTION.md', RUN/'research_note/DUAL_WEIGHT_CONSTRUCTION.md')} foi consultada como roteiro de construção e de convenções, não como prova Lean. Não certifiquei nesta revisão suas etapas de Fourier, identificação de pontos fixos com a imagem da base, teoria espectral de cones ampliados, densidade de domínio finito, peso dual canônico, semifinitude, Stone/afiliação ou passagem ao traço.

O pacote não formaliza todas as propriedades de uma forma quadrática estendida ou de um peso operadorial. Ter uma avaliação ENNReal aditiva em A positivo, invariância pela ação e uma expressão por supremos escalares não fornece, sozinho, essas estruturas. A divergência na unidade é compatível com a necessidade de permitir infinito; não prova, isoladamente, nem refuta semifinitude.

Não ficou pendente uma análise específica identificada dos quatro enunciados/módulos delimitados. A revisão não afirma exaustividade de todo o kernel, não repete a revisão semântica das 5.922 declarações e não executa o runtime monolítico. Não houve ampliação para construir o traço.

Todos os pareceres anteriores identificados no manifesto foram preservados por hash. Fontes do autor e originais permaneceram somente leitura; logs e snapshots anteriores foram mantidos. Somente scripts, snapshots, binários próprios, logs próprios e este relatório foram gravados sob `revisao`. Nenhuma memória global, raiz de implementação, integração ou monólito foi alterado pelo revisor. Não há aprovação de QG, quitação de core/canto ou autorização de transposição ao canônico neste parecer.
'''

path = REVIEW / "REVIEW_DUAL_WEIGHT_CUTS.md"
raw = report.encode("utf-8")
backup_path = None
if path.exists():
    before = path.read_bytes()
    backup_path = path.with_name(path.name + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    backup_path.write_bytes(before)
    assert backup_path.read_bytes() == before
temp = path.with_name(path.name + ".tmp")
temp.write_bytes(raw)
assert temp.stat().st_size == len(raw) and temp.read_bytes() == raw
temp.replace(path)
assert path.read_bytes() == raw
print(json.dumps({"report": str(path), "bytes": len(raw), "sha256": sha(raw),
                  "backup": str(backup_path) if backup_path else None,
                  "sources_unchanged": all(source_status.values()), "dependencies_unchanged": dependency_status,
                  "previous_reviews_preserved": all(preserved.values())}))
