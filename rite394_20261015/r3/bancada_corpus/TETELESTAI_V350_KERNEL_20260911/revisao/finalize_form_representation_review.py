"""Append the bounded independent opinion. No author code is executed."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
sha = lambda raw: hashlib.sha256(raw).hexdigest()
readj = lambda p: json.loads(p.read_bytes())
runs = {s: Path((REVIEW / (s + "_latest_run.txt")).read_text(encoding="utf-8"))
        for s in ["form_upper_bound", "form_variational", "form_representation"]}
RUN = runs["form_representation"]
CAP = max(RUN.glob("final_integrated_*"))
V = readj(CAP / "verification.json")
SUP = readj(CAP / "supplemental_verification.json")
M = readj(RUN / "manifest.json")
report = REVIEW / "REVIEW_DUAL_FORM_REPRESENTATION.md"
prior = REVIEW / "REVIEW_DUAL_ENERGY_AND_SQUARE_ROOT.md"
old = report.read_bytes()
assert sha(old) == M["previous_reviews"][str(report)]
assert all(sha(Path(p).read_bytes()) == h for p, h in M["previous_reviews"].items())
assert V["all_hashes_match"] and V["all_exit_zero"] and V["exact_expected_file_set"]
assert V["python_ast_outside_embedded_unchanged"] and V["gate_extension_byte_identical_to_41"]
assert SUP["independent_and_author_axioms_match_on_printed_targets"]
assert SUP["all_six_open_flags_false"] and SUP["recorder_matches_reviewed_snapshot"]
assert sha((ROOT / "um.py").read_bytes()) == V["um_sha256"]
assert sha((ROOT / "record_form_representation_progress.py").read_bytes()) == SUP["recorder_sha256"]
source_rows = []
for run in runs.values():
    manifest, compilation = readj(run / "manifest.json"), readj(run / "compilation.json")
    assert all(compilation[k] is True for k in ["complete", "all_exit_zero", "full_audit_names_exact",
               "all_axioms_allowed", "sources_unchanged", "dependencies_unchanged", "previous_reviews_preserved"])
    for rel, row in manifest["sources"].items():
        assert sha(Path(row["path"]).read_bytes()) == row["sha256"] == sha(Path(row["snapshot"]).read_bytes())
        source_rows.append((rel, row, run))
last = readj(RUN / "compilation.json")["records"][-1]
assert len(last["axioms"]) == 16
assert all(set(a) == {"propext", "Classical.choice", "Quot.sound"} for a in last["axioms"].values())
custody = readj(ROOT / "square_root_custody.json")
prior_sha = sha(prior.read_bytes())
assert prior_sha == custody["review_sha256"]

def link(label, path, line=None):
    suffix = ":" + str(line) if line else ""
    return "[" + label + "](<" + Path(path).as_posix() + suffix + ">)"

def source(name, line):
    return link(name + ".lean:" + str(line), ROOT / "kernel/TGLV350" / (name + ".lean"), line)

now = datetime.datetime.now().astimezone()
stamp = now.strftime("%Y%m%d_%H%M%S_%f")
backup = report.with_name(report.name + ".bak_" + stamp)
table = "\n".join("| " + link(Path(rel).name, row["snapshot"]) + " | " + str(len(row["declarations"]))
                  + " | `" + row["sha256"] + "` |" for rel, row, run in source_rows)
comp_links = "; ".join(link(s, run / "compilation.json") for s, run in runs.items())
text = f"""

---

Adendo final — {now.isoformat(timespec='seconds')} — três módulos, representação completa da forma.

[REAL — revisão independente concluída no escopo autorizado] **Nenhum achado P0–P2 nas três fontes finais ou no conteúdo matemático da minuta.** Foram conferidos os 16 enunciados, suas hipóteses, coerções e composição. A conclusão agora inclui **`D(q_A)=D(S)` no suporte `K=closure(D(q_A))` e `q_A(x)=ENNReal.ofReal(‖Sx‖²)` para todo `x∈D(S)`**, com equivalência de finitude também no Hilbert ambiente. O existencial final constrói os mesmos `R,T,S` a partir de `P` e de `A≥0` pertencente ao mesmo core regular. Não entrega esses operadores ou a igualdade de domínios como premissas.

Este adendo encerra as pendências de leitura, inclusão inversa, energia, minuta e integração registradas no primeiro estrato deste arquivo. O texto datado anterior permanece como histórico, com seus bytes intactos; seu backup imediato é {link(backup.name, backup)}. O parecer anterior de quatro módulos continua separado e custodiado.

Fontes recompiladas e hashes lidos dos bytes, iguais aos snapshots e logs finais do autor:

| Snapshot independente | Alvos | SHA-256 da fonte dev |
| --- | ---: | --- |
{table}

Pontos decisivos da revisão adicional:

- **Constante ótima e fase complexa — {source('DualFormVariationalBound', 17)}.** A quantificação é sobre todos os vetores. Testar escalas reais produz o discriminante não positivo; testar `conj(⟨w,v⟩) • v` na segunda entrada transforma a parte real em `|⟨w,v⟩|²`, de acordo com a convenção complexa de Lean. O caso de módulo zero é separado antes de cancelar seu quadrado. O resultado é `|⟨w,v⟩|≤sqrt(c)‖Bv‖`, sem perda de constante ou troca da parte real pelo módulo sem prova.
- **Preimagem efetivamente construída — {source('DualFormVariationalBound', 56)}.** A extensão `LinearMap.extendOfNorm` recebe densidade de `Ran B` e a estimativa de limitação. O funcional é linear na segunda entrada. Riesz e a auto-adjunção de `B` dão `Bz=w`; a isometria de Riesz fornece a cota de norma. Densidade isolada não é usada como sobrejetividade, nem a existência de preimagem é assumida. Trata-se da extensão contínua pela imagem densa, não de uma hipótese de extensão arbitrária. A aplicação posterior passa **`sqrt(c)`** como constante deste lema.
- **Sem circularidade e sem perder infinito — {source('DualFormVariationalBound', 76)}.** A desigualdade dual vem da minimalidade já provada em `Rv` e da identidade de energia anterior. Tanto `q_A(w)` quanto `q_A(Rv)` são provadas finitas antes das operações `toReal`; as parcelas de norma são não negativas. Cancelam-se as normas e os termos internos com a orientação correta. Esta derivação não usa a nova igualdade de domínios ou a nova representação completa.
- **Cota inversa — {source('DualFormRepresentation', 14)}, {source('DualFormRepresentation', 27)} e {source('DualFormRepresentation', 39)}.** `R≥0` e `R≤I` justificam as duas raízes limitadas e `‖Bz‖²+‖Cz‖²=‖z‖²`, com `B=√R`, `C=√(I−R)`. Para `f(w)<∞`, a estimativa anterior constrói `Bz=w` com `‖z‖²≤‖w‖²+f(w).toReal`; daí `‖Cz‖²≤f(w).toReal`. O levantamento de grafo tem vetor subjacente exatamente `w` e saída exatamente `Cz`. A volta a ENNReal usa explicitamente a finitude, sem identificar `∞.toReal` com uma energia finita.
- **Mesmo suporte e igualdade dos representantes — {source('DualFormRepresentation', 73)}, {source('DualFormRepresentation', 89)} e {source('DualFormRepresentation', 102)}.** A aplicação usa `R_K` no mesmo `K` da forma `q_A`; positividade, injetividade no suporte e `R_K≤I` são resultados fornecidos pela construção anterior para o mesmo limite. A cota superior por epígrafo e densidade, já revisada no primeiro estrato, dá finitude em `D(S)`. A cota inversa dá a outra inclusão; `Subtype.ext` identifica os testemunhos do domínio antes de juntar as desigualdades. A energia vale em **todo `D(S)`**, além do domínio anterior `D(T)`.
- **Ambiente e composição existencial — {source('DualFormRepresentation', 117)} e {source('DualFormRepresentation', 137)}.** Um vetor ambiente de energia finita pertence a `D(q_A)⊆K`, permitindo seu levantamento em `K` e então em `D(S)`. O teorema final especializa a representação regular em `L²(ℝ,TowerHilbert P)` com medida de Lebesgue, conserva o mesmo core, os mesmos cortes normalizados e o mesmo limite forte `R`. Constrói `T,S : K →ₗ.[ℂ] K` com fechamento, densidade em **K**, auto-adjunção, positividade de `S`, igualdade `partialOperatorSquare S=T` incluindo domínio, energia e equação resolvente `x=Ru`, `x+Tx=u`. O vínculo não é apenas uma coincidência de nomes. `hlim` permanece explícito nos lemas condicionais e é produzido dentro do existencial final.

Os oito enunciados do terceiro módulo incluem os dois auxiliares de energia das raízes, as cotas inversas abstrata e dual, equivalência de domínio no suporte, igualdade de energia, equivalência ambiente e composição existencial. Juntamente com os três do segundo e os cinco do primeiro, todos constam do auditor cumulativo. Não restou hipótese residual de igualdade de domínios, preimagem ou representação completa a ser demonstrada fora dessa composição.

[REAL — recompilação própria] **3 módulos + 3 auditores, 6/6 processos rc0**, realizados nas três árvores independentes: {comp_links}. O auditor final contém `#check` e `#print axioms` dos **16 nomes exatos**; todos retornaram exatamente `propext`, `Classical.choice`, `Quot.sound`. {link('Auditor cumulativo', RUN / 'sources/FormRepresentationFullAudit.lean')}; {link('tipos elaborados e axiomas completos', RUN / 'logs/FormRepresentationFullAudit.stdout.txt')}. Não há alvo omitido ou axioma adicional nesses resultados.

O ambiente final contém **{len(M['dependencies'])} dependências de projeto congeladas**, com fontes e binários pinados, reutilizando os resultados próprios dos estratos anteriores. O `LEAN_PATH` usa o build independente e os pacotes em leitura; exclui os builds de projeto vivos do autor/canônico. Compilador, comandos, hashes e proveniência estão no {link('manifesto final', RUN / 'manifest.json')}. As quatro dependências da etapa anterior e os pacotes não foram recompilados. Mathlib e demais pacotes permanecem parte da base de confiança; não foram congelados nem auditados integralmente. Não se alega reconstrução independente de toda a biblioteca.

[REAL — inspeção independente da integração; execuções integradas pertencem ao autor] O {link('snapshot de verificação', CAP / 'verification.json')} confronta diretamente os **{V['integrated_modules']} hashes de fontes e `.olean`** com os registros rc0. São **{len(V['reused_same_binary_and_source_as_41'])} registros reutilizados com os mesmos bytes** do estrato 41 e cinco compilações novas, correspondentes aos três módulos e às duas raízes. Os três arquivos `TGLExt/V350*.lean` coincidem com os dev congelados após somente substituir os caminhos de import; seus bytes coincidem com os textos embutidos. As mudanças antigas se limitam às raízes `TGLExt.lean` e `TGL/Audit.lean`, com os imports e os 16 alvos adicionais conferidos.

O monólito foi lido por hash e AST/literal de dados, sem importação ou execução. **SHA-256 medido: `{V['um_sha256']}`; {V['embedded_files']} arquivos embutidos.** O hash coincide com `integration.json` e `gate_tests.json`. O AST Python fora do dicionário embutido é igual ao estrato anterior, e `gate_extension.py` é byte a byte idêntico. Não há arquivo embutido removido.

Os logs do autor registram **{V['gate_checks_count']}/{V['gate_checks_count']} controles aprovados e {V['audit_distinct']} declarações distintas no Audit**, todas com axiomas contidos no trio; os 16 alvos desta revisão têm os mesmos axiomas no auditor próprio e no integrado. O {link('suplemento de inspeção', CAP / 'supplemental_verification.json')} confronta o relatório de axiomas de `kernel_incremental_evidence.json` com o stdout efetivo do Audit. As seis flags abertas estão falsas. O único controle adicional verifica a presença dos quatro resultados finais e que essas flags continuam falsas; esse controle registra a fronteira do gate, sem constituir nova prova de peso ou traço. **Não reexecutei testes Python, raízes integradas ou runtime do monólito** nesta inspeção final; 44/57/6052 não designa recompilação integral própria.

[REAL — conferência documental] A minuta {link('record_form_representation_progress.py congelado', RUN / 'final_recorder/record_form_representation_progress.py')}, SHA-256 `{SUP['recorder_sha256']}`, foi lida integralmente e analisada como texto/AST, sem execução. Seu conteúdo matemático distingue densidade em K, forma vetorial com valores estendidos, mesma construção R/T/S e obrigações futuras da base/peso. Está compatível com os enunciados conferidos. Não se certifica a execução futura do recorder ou das atualizações de memória.

Limites efetivos do parecer:

- A igualdade de domínios usa a inclusão natural de K no ambiente. K pode ser zero ou próprio; não há alegação de densidade de `D(S)` no Hilbert ambiente inteiro nem identificação com uma projeção finita `P_F`. Isso é compatível com o caso já estabelecido de `q_I` finita somente no zero e não invalida o teorema.
- A energia é ENNReal em todo o ambiente. A equivalência de finitude, combinada com a igualdade em `D(S)`, determina o valor infinito fora da imagem desse domínio como consequência lógica; não foi acrescentado nesta revisão um novo teorema Lean de fórmula por casos.
- **[OPEN]** Cone ampliado/peso com valores na base, semifinitude e domínio/ideal do peso na álgebra, traço, Three Locks e hipóteses físicas. O domínio **vetorial** da forma não quita essas obrigações. Unicidade abstrata da raiz, cálculo espectral não limitado completo e identificação Fourier da normalização continuam fora do resultado. Não se atribui avanço às flags nem aprovação de QG.
- O runtime integral permanece pendente. O escopo matemático solicitado dos três módulos, recompilação própria, auditoria dos 16 alvos, minuta e inspeção integrada está **concluído**, sem análise delimitada remanescente.

[REAL — preservação] O parecer anterior de quatro módulos permanece com SHA-256 `{prior_sha}`, igual à custódia lida. Fontes do autor, monólito, originais, logs e memórias foram preservados; toda escrita desta revisão ocorreu em `revisao/`. As evidências anteriores e os backups permanecem disponíveis.
"""
newline = "\r\n" if b"\r\n" in old else "\n"
new = old + text.replace("\r\n", "\n").replace("\n", newline).encode("utf-8")
assert new.startswith(old) and len(new) > len(old)
with backup.open("xb") as f:
    f.write(old)
assert backup.read_bytes() == old
temp = report.with_name(report.name + ".tmp_" + stamp)
with temp.open("xb") as f:
    f.write(new)
assert temp.stat().st_size == len(new) and temp.read_bytes() == new
temp.replace(report)
assert report.read_bytes() == new
other_reviews_preserved = all(sha(Path(p).read_bytes()) == h for p, h in M["previous_reviews"].items() if Path(p) != report)
assert other_reviews_preserved and sha(prior.read_bytes()) == prior_sha
receipt = {
    "timestamp": now.isoformat(), "review": str(report), "review_sha256": sha(new),
    "review_bytes": len(new), "previous_review_bytes": len(old), "immediate_backup": str(backup),
    "backup_is_exact_bytes": backup.read_bytes() == old,
    "historical_prefix_unchanged": new.startswith(old), "other_reviews_preserved": other_reviews_preserved,
    "prior_custodied_review_sha256": prior_sha, "complete_delimited_scope": True,
    "findings_P0_P1_P2": [], "independent_modules": 3, "independent_auditors": 3,
    "all_six_processes_rc0": True, "independent_targets": len(last["axioms"]),
    "integrated_inspection": str(CAP), "integrated_records": V["integrated_modules"],
    "author_test_count": V["gate_checks_count"], "author_Audit_distinct": V["audit_distinct"],
    "working_um_sha256": V["um_sha256"], "recorder_not_executed": True,
    "full_runtime_not_executed": True,
}
out = RUN / ("review_final_delivery_" + stamp + ".json")
with out.open("xb") as f:
    f.write(json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf-8"))
assert readj(out) == receipt
print(json.dumps(receipt, ensure_ascii=False, indent=2))
