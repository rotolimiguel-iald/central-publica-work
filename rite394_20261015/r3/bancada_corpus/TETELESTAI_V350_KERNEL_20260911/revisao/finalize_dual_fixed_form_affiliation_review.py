"""Write only the final review and its receipt after static integrated checks."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
sha = lambda b: hashlib.sha256(b).hexdigest()
readj = lambda p: json.loads(p.read_bytes())
runs = {n: Path((REVIEW / (n + "_latest_run.txt")).read_text(encoding="utf-8"))
        for n in ["resolvent_graph_transport", "dual_support_transport", "dual_fixed_form_affiliation"]}
RUN = runs["dual_fixed_form_affiliation"]
CAP = max(RUN.glob("final_integrated_*"))
V, SUP = readj(CAP / "verification.json"), readj(CAP / "supplemental_verification.json")
M = readj(RUN / "manifest.json")
report = REVIEW / "REVIEW_DUAL_FIXED_FORM_AFFILIATION.md"
old = report.read_bytes()
assert sha(old) == M["previous_reviews"][str(report)]
assert all(sha(Path(p).read_bytes()) == h for p, h in M["previous_reviews"].items())
assert V["all_exit_zero"] and V["all_hashes_match"] and V["exact_expected_file_set"]
assert V["python_ast_outside_embedded_unchanged"] and V["gate_extension_byte_identical_to_47"]
assert V["gate_checks_all_passed"] and not V["audit_unexpected_axioms"]
assert SUP["all_six_open_flags_false"] and SUP["recorder_matches_reviewed_snapshot"]
assert SUP["evidence_axioms_equal_actual_Audit_log"] and SUP["independent_and_author_axioms_match_on_printed_targets"]
assert sha((ROOT / "um.py").read_bytes()) == V["um_sha256"]
assert sha((ROOT / "record_fixed_form_affiliation_progress.py").read_bytes()) == SUP["recorder_sha256"]
rows = []
for run in runs.values():
    m, c = readj(run / "manifest.json"), readj(run / "compilation.json")
    assert all(c[k] is True for k in ["complete", "all_exit_zero", "full_audit_names_exact",
               "all_axioms_allowed", "sources_unchanged", "dependencies_unchanged", "previous_reviews_preserved"])
    for rel, row in m["sources"].items():
        assert sha(Path(row["path"]).read_bytes()) == row["sha256"] == sha(Path(row["snapshot"]).read_bytes())
        rows.append((rel, row, run))
audit = readj(RUN / "compilation.json")["records"][-1]
assert len(audit["axioms"]) == 22
assert all(set(a) == {"propext", "Classical.choice", "Quot.sound"} for a in audit["axioms"].values())
previous = REVIEW / "REVIEW_DUAL_FIXED_RESOLVENT.md"
custody = readj(ROOT / "fixed_resolvent_custody.json")
previous_sha = sha(previous.read_bytes())
assert previous_sha == custody["review_sha256"]

def link(label, path, line=None):
    suffix = ":" + str(line) if line else ""
    return "[" + label + "](<" + Path(path).as_posix() + suffix + ">)"

def loc(name, line):
    return link(name + ".lean:" + str(line), ROOT / "kernel/TGLV350" / (name + ".lean"), line)

now = datetime.datetime.now().astimezone()
stamp = now.strftime("%Y%m%d_%H%M%S_%f")
backup = report.with_name(report.name + ".bak_" + stamp)
table = "\n".join("| " + link(Path(rel).name, row["snapshot"]) + " | " + str(len(row["declarations"]))
                  + " | `" + row["sha256"] + "` |" for rel, row, run in rows)
comp_links = "; ".join(link(name, run / "compilation.json") for name, run in runs.items())
text = f"""

---

Adendo final — {now.isoformat(timespec='seconds')} — afiliação da mesma forma à álgebra fixa.

[REAL — revisão independente delimitada concluída] **Nenhum achado P0–P2 nas três fontes finais, na composição das provas ou no conteúdo matemático da minuta.** Os 22 alvos demonstram o transporte dos grafos no suporte e a invariância **`q_A(Uw)=q_A(w)` em ENNReal para todo vetor ambiente w e todo unitário U de F'**, inclusive quando a energia é infinita. O construtor entrega `AffiliatedPositiveForm (dualFixedCore P)` cuja função `value` é literalmente a mesma `dualQuadraticIntegral A`.

Este adendo encerra as pendências dos dois estratos anteriores deste parecer: terceiro módulo, quantificação pelo comutante de F, sentido inverso dos grafos, caso infinito, minuta e integração. Seus bytes permanecem como histórico, com {link('backup imediato', backup)}. Os pareceres custodiados de etapas anteriores não foram modificados.

| Fonte recompilada | Alvos | SHA-256 dev medido |
| --- | ---: | --- |
{table}

O transporte direto de grafos e a construção de U_K, já conferidos acima, permanecem válidos para U limitado que comuta com R. O terceiro módulo acrescenta precisamente a unitariedade necessária para as conclusões mais fortes:

- **Adjunto, inversa e grafos — {loc('DualFixedFormAffiliation', 13)}, {loc('DualFixedFormAffiliation', 18)} e {loc('DualFixedFormAffiliation', 28)}.** Aplicar `star` à igualdade de comutação, usando R auto-adjunto, dá a comutação com U*. As restrições U_K e (U*)_K já estão definidas no mesmo K, pois ambas preservam seu fecho. O cancelamento é provado por `Subtype.ext` a partir de U*U=I no ambiente, não introduzido como propriedade sem demonstração. O lema abstrato usa essa inversa à esquerda e os transportes diretos de ambas as aplicações para obter a equivalência de pertinência ao grafo.
- **T e S com seus domínios — {loc('DualFixedFormAffiliation', 39)} e {loc('DualFixedFormAffiliation', 55)}.** As equivalências são para os grafos efetivos de `dualSupportOperator` e `dualSupportSquareRoot`, em K×K, com os mesmos A,R,hlim e as mesmas restrições de U. A comutação com U* é derivada internamente de R≥0. Não há hipótese residual de transporte inverso ou identificação de domínio. Os lemas de grafos exigem comutação com R; quando U pertence a F', essa hipótese é fornecida pela pertinência do mesmo resolvente a F.
- **Energia finita sem supor invariância — {loc('DualFixedFormAffiliation', 73)}.** A equivalência ambiente já provada entre energia finita e D(S) fornece um testemunho x cujo vetor subjacente é exatamente w. O transporte de `(x,Sx)` produz z no mesmo domínio, com vetor subjacente Uw e `S z=U_K(S x)`. A norma de U_K nesse vetor é a norma da aplicação ambiente U, preservada pela unitariedade. As duas instâncias da igualdade de forma com `ofReal(‖S·‖²)` dão a igualdade de energias. As hipóteses A≥0, R≥0, R≤I e hlim permanecem explícitas; não se usa a própria invariância da forma como premissa.
- **Setor infinito — {loc('DualFixedFormAffiliation', 110)}.** A prova separa `q_A(w)<∞`. No caso contrário, supor `q_A(Uw)<∞` permitiria aplicar a igualdade finita a U* e Uw; o cancelamento devolveria finitude de q_A(w), contradizendo a hipótese. Assim ambos os valores são ⊤ e a igualdade é concluída diretamente em ENNReal. Não há passagem por `∞.toReal`, retirada do setor infinito ou restrição silenciosa de w ao domínio finito.
- **Todo unitário de F' e a mesma q — {loc('DualFixedFormAffiliation', 134)}, {loc('DualFixedFormAffiliation', 148)} e {loc('DualFixedFormAffiliation', 156)}.** A hipótese elaborada é `∀ B∈dualFixedCore P, U.val*B=B*U.val`, e não comutação apenas com N. A construção obtém R positivo e contrativo, com o limite dos cortes do mesmo A, e prova R∈F. Aplicar a hipótese a esse R fornece a comutação na orientação correta. O construtor reutiliza `dualClosedPositiveForm A hA`; sua lei de valor é **rfl**. R serve à prova da invariância, sem substituir a forma nem criar uma família diferente. F⊆N permite N'⊆F'; o novo resultado cobre todos os unitários deste último comutante, sem precisar afirmar que a inclusão seja estrita.

**Sentido exato de afiliação.** O tipo existente `AffiliatedPositiveForm F` reúne a forma positiva fechada com invariância por todo unitário do comutante de F. Esse é o estatuto provado para q_A sobre o mesmo Hilbert regular de Lebesgue `L²(ℝ,TowerHilbert P)`. Separadamente, os lemas de grafo demonstram as equivalências para os operadores parciais T/S no suporte construído `K=closure(D(q_A))`. Não se transforma esse dado em um operador com domínio denso no ambiente inteiro quando K é próprio ou zero, nem se entrega por isso uma estrutura completa de cone espectral ou peso.

[REAL — execução própria] **3 módulos + 3 auditores, 6/6 rc0.** Registros: {comp_links}. O {link('auditor cumulativo', RUN / 'sources/DualFixedFormAffiliationFullAudit.lean')} conferiu por `#check` e `#print axioms` os **22 nomes exatos (5+7+10, incluindo as duas definições)**, todos com exatamente `propext`, `Classical.choice`, `Quot.sound`. {link('Tipos elaborados e axiomas completos', RUN / 'logs/DualFixedFormAffiliationFullAudit.stdout.txt')}. Não houve alvo omitido ou axioma extra.

O último snapshot contém **{len(M['dependencies'])} dependências de projeto congeladas**, com fontes e binários pinados, reutilizados sem recompilação. O `LEAN_PATH` usa o build próprio e pacotes em leitura, sem builds vivos do projeto do autor/canônico. {link('Manifesto e proveniência', RUN / 'manifest.json')}. Mathlib e demais pacotes seguem como base de confiança, sem reconstrução ou congelamento integral. Os dois warnings do primeiro módulo e o rc1 histórico do segundo permanecem registrados nos estratos anteriores; não são falhas pendentes das fontes finais.

[REAL — inspeção integrada; execuções integradas pertencem ao autor] {link('Verificação final', CAP / 'verification.json')}: **{V['integrated_modules']} registros rc0**, com hashes atuais de fontes e `.olean` coincidentes com os logs; **{len(V['reused_same_binary_and_source_as_47'])}** fontes/binários iguais ao estrato 47, mais três módulos e duas raízes novos. As fontes `TGLExt/V350*.lean` coincidem com os dev congelados salvo os caminhos de import e com os textos embutidos. As mudanças antigas limitam-se aos imports e alvos das duas raízes, conferidos por diff.

**Monólito: SHA-256 `{V['um_sha256']}`, medido nos bytes; {V['embedded_files']} arquivos embutidos.** Hash correspondente a `integration.json` e `gate_tests.json`; corpo Python fora do dicionário embutido igual ao estrato anterior por AST, e `gate_extension.py` byte a byte idêntico. A leitura usou somente AST/literais de dados, sem importar ou executar o monólito.

Os logs do autor registram **{V['gate_checks_count']}/{V['gate_checks_count']} controles aprovados e {V['audit_distinct']} declarações distintas no Audit**, sem axioma fora do trio. Os 22 alvos atuais coincidem com o auditor próprio. O {link('suplemento da inspeção', CAP / 'supplemental_verification.json')} confronta o relatório de axiomas com o stdout efetivo do Audit e confirma as seis flags abertas falsas. O controle adicional registra os resultados presentes e a permanência dessa fronteira; não prova base, peso ou traço. Não reexecutei controles Python, raízes integradas ou runtime completo; suas contagens são evidência do autor inspecionada, distinta das recompilações próprias dos três módulos.

[REAL — revisão documental] A minuta {link('record_fixed_form_affiliation_progress.py congelado', RUN / 'final_recorder/record_fixed_form_affiliation_progress.py')}, SHA-256 `{SUP['recorder_sha256']}`, foi lida integralmente e analisada como texto/AST, sem execução. O relatório e o adendo projetados distinguem corretamente invariância por F', grafos no suporte, valores ENNReal incluindo infinito e as operações/obrigações ainda abertas. Nenhum exagero matemático foi encontrado. As futuras escritas nas 14 superfícies, o recorder e o verificador de sua custódia não são certificados como executados por esta revisão.

**[OPEN — fora desta conclusão]** Identificação F=base original; cone ampliado com operações/ordem e correspondência espectral geral; peso operadorial com valores na base, normalidade/semifinitude do peso e domínio na álgebra; predual; traço, Three Locks, hipóteses físicas e runtime integral. A finitude vetorial da forma e a invariância de seus grafos não substituem o domínio/ideal de um peso semifinito. K não é um projetor P_F imposto, e a afiliação da forma não aprova QG ou quita flags.

[REAL — encerramento e preservação] A revisão delimitada dos três módulos, dos 22 alvos, da minuta e da integração está **concluída**, sem análise substantiva remanescente. O parecer anterior `REVIEW_DUAL_FIXED_RESOLVENT.md` mantém SHA-256 `{previous_sha}`, igual à custódia lida. Fontes, originais, logs, monólito, memórias e pareceres custodiados foram preservados; toda escrita desta revisão ficou em `revisao/`.
"""
newline = "\r\n" if b"\r\n" in old else "\n"
new = old + text.replace("\r\n", "\n").replace("\n", newline).encode("utf-8")
assert new.startswith(old) and len(new) > len(old)
with backup.open("xb") as f:
    f.write(old)
assert backup.read_bytes() == old
tmp = report.with_name(report.name + ".tmp_" + stamp)
with tmp.open("xb") as f:
    f.write(new)
assert tmp.stat().st_size == len(new) and tmp.read_bytes() == new
tmp.replace(report)
assert report.read_bytes() == new
preserved = all(sha(Path(p).read_bytes()) == h for p, h in M["previous_reviews"].items() if Path(p) != report)
assert preserved and sha(previous.read_bytes()) == previous_sha
receipt = {"timestamp": now.isoformat(), "review": str(report), "review_sha256": sha(new),
           "review_bytes": len(new), "previous_review_bytes": len(old), "immediate_backup": str(backup),
           "backup_is_exact_bytes": backup.read_bytes() == old, "historical_prefix_unchanged": new.startswith(old),
           "other_reviews_preserved": preserved, "previous_custodied_review_sha256": previous_sha,
           "complete_delimited_scope": True, "findings_P0_P1_P2": [], "independent_modules": 3,
           "independent_auditors": 3, "all_six_processes_rc0": True, "independent_targets": 22,
           "integrated_inspection": str(CAP), "integrated_records": V["integrated_modules"],
           "author_test_count": V["gate_checks_count"], "author_Audit_distinct": V["audit_distinct"],
           "working_um_sha256": V["um_sha256"], "recorder_not_executed": True,
           "full_runtime_not_executed": True}
out = RUN / ("review_final_delivery_" + stamp + ".json")
with out.open("xb") as f:
    f.write(json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf-8"))
assert readj(out) == receipt
print(json.dumps(receipt, ensure_ascii=False, indent=2))
