"""Record the five-source independent review without touching prior custody."""
from pathlib import Path
import datetime, hashlib, json, sys

sys.stdout.reconfigure(encoding="utf-8")
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "fixed_core_base_latest_run.txt").read_text(encoding="utf-8"))
M = json.loads((RUN / "manifest.json").read_bytes())
C = json.loads((RUN / "compilation.json").read_bytes())
FIRST = Path(M["previous_run"])
FM = json.loads((FIRST / "manifest.json").read_bytes())
FC = json.loads((FIRST / "compilation.json").read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()
sources = {**FM["sources"], **M["sources"]}
records = FC["records"] + C["records"]
for c in [FC, C]:
    assert all(c[k] for k in ("complete", "all_exit_zero", "full_audit_names_exact", "all_axioms_allowed",
                             "sources_unchanged", "dependencies_unchanged", "previous_reviews_preserved"))
assert len(sources) == 5 and len(C["records"][-1]["axioms"]) == 23 and len(M["all_named_declarations"]) == 26
for rel, q in sources.items():
    assert sha(Path(q["path"]).read_bytes()) == q["sha256"]
    assert next(x for x in records if x["module"] == rel)["output_sha256"] == q["author_binary_sha256"]
for q in M["dependencies"].values():
    assert sha(Path(q["frozen_source"]).read_bytes()) == q["source_sha256"]
    assert sha(Path(q["frozen_binary"]).read_bytes()) == q["sha256"]
for p, h in M["previous_reviews"].items():
    assert sha(Path(p).read_bytes()) == h
custody_raw = (ROOT / "constant_fibre_custody.json").read_bytes()
custody = json.loads(custody_raw)
assert sha((REVIEW / "REVIEW_UNIT_INTERVAL_PROJECTION.md").read_bytes()) == custody["review_sha256"]
document = max(RUN.glob("documentary_*"))
for name in ["MINUTA_BASE_FIXA.md", "record_fixed_base_progress.py"]:
    assert (ROOT / name).read_bytes() == (document / name).read_bytes()
table = "\n".join(f'| `{Path(n).stem}` | {len(q["declarations"])} | `{q["sha256"]}` |' for n, q in sources.items())
builds = "\n".join(f'| `{Path(q["module"]).name}` | rc0 | {q["seconds"]} s | `{q["output_sha256"]}` |' for q in records)
author_logs = "\n".join(f'- `{Path(q["author_log"]).name}`.' for q in sources.values())
stamp = datetime.datetime.now().astimezone()
report = REVIEW / "REVIEW_FIXED_CORE_BASE.md"
assert not report.exists()
text = f'''# Revisão independente — identificação da álgebra fixa com a base amplificada

{stamp.isoformat(timespec="seconds")}. **[REAL — fontes, tipos e recompilação independente] Cinco módulos e 23 alvos conferidos; nenhum achado P0, P1 ou P2.** A composição prova C∈M para a fibra extraída e **B∈F ↔ ∃ C∈M, B=fibre(C)**, com C único. Neste primeiro registro, a inspeção da integração final ainda aguarda os relatórios estáveis do autor; as conclusões abaixo são das fontes dev recompiladas.

“F=base” significa precisamente **igualdade de F com a imagem amplificada de M no mesmo L²**, expressa pelo critério de pertença do teorema. Não é uma igualdade literal entre álgebras que atuam em Hilberts distintos. Aqui H=`TowerHilbert P`, M=`theFactorObject P`, N=`regularCoreAlgebra P`, F=`dualFixedCore P` e L²=`Lp H 2 (volume : Measure ℝ)`. O parâmetro P e o fluxo são os mesmos ao longo da cadeia.

## Revisão das provas e das hipóteses

**`StrongOperatorField.lean:15–30,32–73`.** O campo recebe exatamente `StrongIntegral.Family`: cada F(x) é um CLM complexo, x↦F(x)v é contínua para todo v, e há uma única cota global não negativa para ‖F(x)‖. Essa cota fornece Lipschitz uniforme na variável vetorial e, combinada à continuidade forte na variável real, dá continuidade conjunta de (v,x)↦F(x)v. Não é assumida continuidade de x↦F(x) em norma de operadores.

Para f∈L², o par (f(x),x) é ae fortemente mensurável, e sua composição com a aplicação conjunta contínua também o é. A identidade em ℝ é fortemente mensurável pelas propriedades da própria reta; não aparece uma hipótese de separabilidade de H. A estimativa ‖F(x)f(x)‖≤bound·‖f(x)‖ fornece MemLp. `toLp`, as igualdades ae e `Lp.ext` constroem a linearidade e a cota de norma, permitindo `mkContinuous`. É **multiplicação espacial em vetores**, não integral de Bochner em B(H). O lift satisfaz a fórmula ae para cada f e norma ≤bound, incluindo o caso bound=0.

**`StrongOperatorField.lean:75–84`.** Comutação ponto a ponto com C implica comutação do lift com `fibre C`. As quatro identidades ae usadas estão relacionadas ao F, C e f fixados. Não se escolhe um conjunto excepcional comum para todos os vetores.

**`OperatorFieldFaithfulness.lean:15–42`.** O lema geral recebe F,G:ℝ→B(H), continuidade forte de ambos e igualdade ae das ações para todo teste L². Não acrescenta uma cota uniforme desnecessária a esse lema de reflexão. Para cada v fixado, usa os testes `shift n (testVector v)`, n∈ℤ, e reúne somente essa família enumerável. A escolha n=⌈y⌉−1 satisfaz y−n∈(0,1], inclusive nos extremos inteiros, logo F(y)v=G(y)v ae em toda a reta.

A passagem a **todo ponto** usa `Continuous.ae_eq_iff_eq volume`: continuidade das duas órbitas vetoriais e medida de Lebesgue positiva em abertos não vazios, com H Hausdorff. Esse lema primário e o de composição ae fortemente mensurável foram lidos nas fontes Mathlib. A igualdade para cada v é obtida antes da extensionalidade do operador; não é tomada uma interseção não enumerável sobre H. Também não é usada avaliação pontual como funcional contínuo de L². Aplicar `congrArg` a representantes de elementos L² já iguais, nas aplicações seguintes, é compatível com as identidades ae fornecidas pelo lift.

**`OperatorFieldFaithfulness.lean:44–69`.** A igualdade dos lifts satisfaz os testes anteriores e implica F.op(x)=G.op(x). A conclusão concerne aos campos de operadores, não à igualdade de estruturas `Family` com cotas possivelmente distintas. Para refletir a comutação, o lema é aplicado aos campos F(x)C e CF(x). Suas continuidades são fornecidas por F.continuous_apply(Cv) e pela composição do CLM C com F(x)v. Assim, a comutação é refletida ponto a ponto, inclusive em zero; não apenas ae.

**`TwistedCommutantField.lean:12–50`.** A conjugação modular preserva M′ porque seu inverso preserva M: para A∈M, a prova testa D contra a pré-imagem modular de A e transporta a igualdade pelo mesmo automorfismo. A invariância de M não é uma premissa residual: usa `modularConjugation_preserves_factor` já construído sobre o bicomutante da torre. Sua declaração e a ligação com o mesmo fluxo foram inspecionadas nas dependências congeladas.

A continuidade de x↦U_x D U_−x v usa continuidade conjunta do fluxo e a composição x↦(D(U_−x v),x). A norma é uniformemente ‖D‖ pela isometria da conjugação. `twistedCommutantField` pode ser definido para qualquer D∈B(H); hD∈M′ só é exigida quando se deduz pertença ao comutante regular. Não se introduz um estado, Hilbert ou fluxo alternativo.

**`TwistedCommutantField.lean:52–94`.** F_D(0)=D. A identidade crucial tem o sinal correto:

`F_D(x) U_t = U_t F_D(x−t)`, com `F_D(x)=U_x D U_−x`.

Ambos os lados reduzem a U_x D U_(t−x). Isso coincide com o unitário regular efetivamente usado, Λ_t f(x)=U_t f(x−t). Na prova da comutação do lift com Λ_t, a igualdade ae de Ff é transportada por x↦x−t, que preserva Lebesgue. O parâmetro t é fixado antes de reunir as igualdades ae. A fórmula não substitui Λ_t pela translação ordinária nem inverte o sinal do campo torcido.

**`RegularCoreCommutant.lean:13–44`.** O fechamento pelos geradores trata a estrela do operador candidato T. Para aplicar `regularCore_minimal` à álgebra `starCommutantAlgebra {{T}}`, a prova fornece comutação dos geradores tanto com T como com T*. A segunda vem da hipótese aplicada a A*∈M, seguida de adjunto, e da hipótese aplicada a Λ_−t=Λ_t*. Portanto não pressupõe T auto-adjunto, unitário ou já pertencente a N′. A minimalidade usada é a da mesma álgebra gerada N, cujo enunciado foi conferido.

**`RegularCoreCommutant.lean:46–75`.** Para cada D∈M′, a invariância modular de M′ fornece comutação do campo com toda fibre(A), A∈M; o entrelaçamento fornece a comutação com todos os Λ_t. A prova anterior coloca seu lift em N′. Se fibre(C)∈N, esse lift comuta com fibre(C); a reflexão ponto a ponto é aplicada **antes** de avaliar em zero e produz DC=CD. Como D∈M′ era arbitrário, o bicomutante da VNA M dá C∈M. A direção oposta é a inclusão geradora `amplified_factor_mem`. Não é assumida F=base nem uma decomposição constante para demonstrar essa equivalência.

**`FixedCoreBaseIdentification.lean:12–39`.** A identificação global B=fibre(e*Be) do estrato anterior é combinada com B∈F⇒B∈N e com `fibre_mem_regularCore_iff`. Isso fornece a pertença do **mesmo candidato** e*Be a M. A recíproca B=fibre(C), C∈M⇒B∈F usa a inclusão fixa já provada. A unicidade é no subtipo **C:M**, não meramente uma testemunha de B(H) sem pertinência; `Subtype.ext` e `fibre_injective` dão a igualdade. Não se trocam testemunhos ou representações. As hipóteses finais são somente P e, onde requerido, B∈F.

**Conclusão matemática delimitada:** o OPEN C∈M/F=base da custódia anterior foi resolvido na representação regular concreta. A prova não identifica o modelo com uma geometria física, não produz um traço e não quita as demais obrigações por nomenclatura.

## Evidências próprias

| Fonte em `kernel/TGLV350` | #print axioms | SHA-256 dev medido |
|---|---|---|
{table}

Logs finais do autor efetivamente confrontados com fontes e binários, distintos dos processos próprios:

{author_logs}

| Processo executado pelo revisor | Resultado | Tempo | SHA-256 `.olean` próprio |
|---|---|---|---|
{builds}

**Cinco módulos e dois auditores próprios: sete processos rc0. Os cinco binários dev coincidem em hash com os do autor.** O primeiro auditor verificou dez alvos e 13 tipos; o cumulativo verificou **23 alvos distintos e 26 tipos nomeados**, com stdout lido integralmente. Os três auxiliares de StrongOperatorField são conferidos por tipo e auditados transitivamente, sem inflar a contagem dos 23 `#print`. Todos os alvos dependem somente de **propext, Classical.choice e Quot.sound**, sem sorryAx, trustCompiler ou axiomas customizados.

O primeiro build congelou **{len(FM['dependencies'])} dependências de projeto**; o segundo congelou o fecho necessário de **{len(M['dependencies'])}**, usando os dois módulos recém-recompilados e o catálogo próprio da revisão da fibra constante para os demais imports necessários. Foram conferidos hashes de fontes e `.olean`, preservados nos manifests; fontes de dependências coincidem com as correspondentes fontes vivas no congelamento. Não recompilei as duas fontes iniciais novamente nem reconstruí dependências anteriores. Pacotes instalados são somente para leitura, sem uma recertificação integral de Mathlib.

`LEAN_PATH` contém o build próprio e os caminhos de pacotes, excluindo ambos os builds de projeto do autor. TMP/TEMP e produtos estão sob revisao. Compilador `{M['lean_version']}`, SHA lido `{M['compiler_sha256']}`. [Primeira compilação própria](<{(FIRST/'compilation.json').as_posix()}>); [compilação cumulativa](<{(RUN/'compilation.json').as_posix()}>); [manifest de dependências](<{(RUN/'manifest.json').as_posix()}>).

Uma tentativa do **script de congelamento do revisor** parou antes de chamar Lean porque sua expressão regular de namespace não aceitava CRLF; TwistedCommutantField tem finais de linha mistos. A leitura para extração dos nomes foi corrigida, conservando os bytes das fontes congeladas. A tentativa ficou na árvore própria, sem sobrescrever evidências. Isso não foi uma falha Lean. As tentativas anteriores de elaboração relatadas pelo autor tampouco são tratadas como defeitos pendentes das versões finais rc0.

## Minuta, preservação e limites

Minuta `MINUTA_BASE_FIXA.md` lida integralmente: SHA **`{sha((document/'MINUTA_BASE_FIXA.md').read_bytes())}`**. Recorder `record_fixed_base_progress.py` lido integralmente e analisado por AST: SHA **`{sha((document/'record_fixed_base_progress.py').read_bytes())}`**. A narrativa descreve corretamente F como base **amplificada**, os sinais do campo, a reflexão antes da avaliação em zero e o uso do bicomutante. Não encontrei P2 documental. Os marcadores de contagem/data são placeholders a preencher pelo recorder, não evidência de integração já conferida neste estrato.

O recorder prevê append em 20 superfícies (18 locais e dois índices globais), com backups de bytes, temporário verificado e exigência de leitura do parecer. Não o executei e não certifiquei uma custódia futura como já realizada. Resultados de etapas anteriores em seu dicionário são herdados, não recompilados nesta revisão. O inventário I/O é expressamente histórico e não fornece liberação do runtime atual.

Custódia anterior `constant_fibre_custody.json` lida, SHA `{sha(custody_raw)}`, timestamp `{custody['timestamp']}`. O parecer anterior confere com o hash custodiado **`{custody['review_sha256']}`** e permaneceu intocado, como os demais pareceres constantes dos manifests. Nenhuma escrita em memórias, fontes autorais, originais, monólito, integrações ou logs do autor.

**[OPEN]** Correspondência geral espectral/predual e interface padrão de peso operatorial; construções de estado/gerador/perturbação e traço canônico fiel, normal e semifinito; Three Locks/H1–H3 físicos, interações/BRST/QME/anomalias/UV, contrato ampliado e runtime integral. F=base amplificada não encerra esses itens. **Neste estrato resta somente a inspeção dos relatórios finais da integração/controles quando disponíveis; a revisão matemática das cinco fontes está concluída.**
'''
raw = text.encode("utf-8")
tmp = report.with_name(report.name + ".tmp")
with tmp.open("xb") as f:
    f.write(raw)
assert tmp.read_bytes() == raw and len(raw) > 0
tmp.replace(report)
assert report.read_bytes() == raw
receipt = {"timestamp": stamp.isoformat(), "report": str(report), "report_sha256": sha(raw),
           "report_bytes": len(raw), "source_review_complete": True, "integration_review_complete": False,
           "mathematical_findings": [], "documentary_findings": [], "own_module_compiles": 5,
           "own_auditor_compiles": 2, "all_exit_zero": True, "targets": 23, "named_types": 26,
           "all5_binaries_equal_author": True, "previous_reviews_preserved": True,
           "template_sha256": sha((document / "MINUTA_BASE_FIXA.md").read_bytes()),
           "recorder_sha256": sha((document / "record_fixed_base_progress.py").read_bytes())}
with (RUN / "source_review_receipt.json").open("xb") as f:
    f.write(json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf-8"))
print(json.dumps(receipt, ensure_ascii=False, indent=2))
