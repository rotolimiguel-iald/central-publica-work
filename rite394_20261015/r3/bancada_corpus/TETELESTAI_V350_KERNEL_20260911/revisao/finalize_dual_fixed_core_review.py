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
        for n in ["minimizer_uniqueness", "dual_resolvent_fixed", "dual_fixed_core"]}
RUN = runs["dual_fixed_core"]
CAP = max(RUN.glob("final_integrated_*"))
V, SUP = readj(CAP / "verification.json"), readj(CAP / "supplemental_verification.json")
M = readj(RUN / "manifest.json")
report = REVIEW / "REVIEW_DUAL_FIXED_RESOLVENT.md"
old = report.read_bytes()
assert sha(old) == M["previous_reviews"][str(report)]
assert all(sha(Path(p).read_bytes()) == h for p, h in M["previous_reviews"].items())
assert V["all_exit_zero"] and V["all_hashes_match"] and V["exact_expected_file_set"]
assert V["python_ast_outside_embedded_unchanged"] and V["gate_extension_byte_identical_to_44"]
assert V["gate_checks_all_passed"] and not V["audit_unexpected_axioms"]
assert SUP["all_six_open_flags_false"] and SUP["recorder_matches_reviewed_snapshot"]
assert SUP["evidence_axioms_equal_actual_Audit_log"] and SUP["independent_and_author_axioms_match_on_printed_targets"]
assert sha((ROOT / "um.py").read_bytes()) == V["um_sha256"]
assert sha((ROOT / "record_fixed_resolvent_progress.py").read_bytes()) == SUP["recorder_sha256"]
rows = []
for run in runs.values():
    m, c = readj(run / "manifest.json"), readj(run / "compilation.json")
    assert all(c[k] is True for k in ["complete", "all_exit_zero", "full_audit_names_exact",
               "all_axioms_allowed", "sources_unchanged", "dependencies_unchanged", "previous_reviews_preserved"])
    for rel, row in m["sources"].items():
        assert sha(Path(row["path"]).read_bytes()) == row["sha256"] == sha(Path(row["snapshot"]).read_bytes())
        rows.append((rel, row, run))
audit = readj(RUN / "compilation.json")["records"][-1]
assert len(audit["axioms"]) == 16
assert all(set(a) == {"propext", "Classical.choice", "Quot.sound"} for a in audit["axioms"].values())
previous = REVIEW / "REVIEW_DUAL_FORM_REPRESENTATION.md"
custody = readj(ROOT / "form_representation_custody.json")
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

Adendo final — {now.isoformat(timespec='seconds')} — três módulos, 16 alvos.

[REAL — revisão independente delimitada concluída] **Nenhum achado P0–P2 nas fontes finais, na composição dos enunciados ou no conteúdo matemático da minuta.** O resolvente dos mesmos cortes normalizados é fixo pela ação dual para todo parâmetro real. Foi construído o VNA concreto `F=N∩{{D_s | s∈ℝ}}'`, com caracterização exata de pertinência, inclusão da base amplificada e composição com os mesmos `R,T,S` da representação completa da forma. **Não foi provada a igualdade F=base original ou a afiliação completa de T/S a F.**

Este adendo encerra as pendências de fontes finais, recompilação, minuta e integração do primeiro estrato. Seu texto permanece intacto como histórico, com {link('backup imediato de bytes', backup)}. Nenhum parecer custodiado anterior foi alterado.

| Fonte congelada e recompilada | Alvos | SHA-256 dev medido |
| --- | ---: | --- |
{table}

Achados substantivos: **P0: nenhum; P1: nenhum; P2: nenhum**. Pontos críticos efetivamente conferidos, além da unicidade já detalhada no primeiro estrato:

- **Transporte e unicidade — {loc('DualResolventFixed', 15)} e {loc('DualResolventFixed', 32)}.** `e` é uma equivalência isométrica linear complexa, portanto dispõe da inversa necessária para testar o competidor `e.symm w`. A hipótese `Q(e w)=Q(w)` vale para todo w, inclusive com valor infinito. O mínimo transportado tem centro `e v`, o mesmo centro do mínimo `R(e v)`; a unicidade então dá `R(e v)=e(Rv)`. A linearidade de R não é pressuposta no lema abstrato. Na aplicação concreta, a minimalidade é a já demonstrada para o limite dos cortes, sem uma nova premissa residual de comutação.
- **Mesmo funcional e sinal — {loc('DualResolventFixed', 41)} e {loc('DualResolventFixed', 51)}.** A forma é exatamente `dualQuadraticIntegral A`, e `e` é exatamente o implementador `D_s=characterMultiplier s`. A invariância vetorial usada vem da lei anterior de transporte, com o parâmetro negativo tratado nessa dependência. Resulta `R D_s = D_s R` para todo `s:ℝ`. A extensão pontual a CLMs usa a simetria correta para obter `D_s R=R D_s`; `dualAmbient s R=D_s R D_s*` reduz então a R por `D_s D_s*=I`. Não se afirma que o A de entrada seja fixo.
- **Comutante e existência — {loc('DualResolventFixed', 61)} e {loc('DualResolventFixed', 78)}.** O lema com U exige explicitamente que U comute com **todo** o mesmo core regular N; positividade e pertinência de A fornecem a invariância da forma pela dependência auditada. O existencial recebe apenas P e A positivo em N, obtém R e seu `hlim` da construção anterior e acrescenta sua fixação. Não introduz a fixação como hipótese nem presume densidade de domínio da forma no ambiente.
- **VNA e fechamento por adjunto — {loc('DualFixedCore', 14)}, {loc('DualFixedCore', 31)} e {loc('DualFixedCore', 38)}.** O `StarSubalgebra.centralizer` de Mathlib é o comutante de `S∪S*`, não apenas o comutante ordinário de um conjunto arbitrário sem seus adjuntos. O campo de bicomutante do VNA é efetivamente provado. Para `S=N'∪{{D_s}}`, `N'` é fechado por adjunto e `D_s*=D_(-s)`, já incluído pela quantificação sobre todos os reais. Na direção inversa do `mem_iff`, a prova fornece explicitamente ambas as comutações exigidas. Na direção direta, `N''=N` recupera a pertinência ao **mesmo N**. Assim o objeto não fica maior por falta de uma restrição a N, nem menor por uma condição de adjunto omitida. {link('Definições Mathlib consultadas e hashes', RUN / 'references/manifest.json')}.
- **Equivalência de fixação — {loc('DualFixedCore', 18)}.** Multiplicar `D_s R D_s*=R` à direita por `D_s` cancela `D_s*D_s=I`; a recíproca cancela `D_s D_s*=I`. Os dois lados da unitariedade são usados nos sentidos corretos. O enunciado vale para todo operador limitado R, sem positividade implícita nesse lema.
- **Inclusão e mesmos testemunhos — {loc('DualFixedCore', 62)}, {loc('DualFixedCore', 68)} e {loc('DualFixedCore', 77)}.** A inclusão demonstrada é `fibre(B)∈F` para B na base original; não há prova da inclusão inversa. A pertinência do resolvente a F combina sua pertinência a N e sua fixação, ambas fornecidas para o mesmo limite. `exists_dualFixedFormRepresentation` decompõe **uma só** testemunha de `exists_dualFormRepresentation` em R,T,S e conserva literalmente o restante da conjunção. Mantém limite forte, positividade/contratividade de R, operadores fechados e auto-adjuntos densos em K, positividade de S, `partialOperatorSquare S=T` com domínio, equivalência do domínio finito no ambiente, energia em todo D(S) e a equação resolvente. Não junta existências independentes sem vínculo.

[REAL — execução independente] **3 módulos e 3 auditores, 6/6 processos rc0.** Registros completos: {comp_links}. O {link('auditor cumulativo próprio', RUN / 'sources/DualFixedCoreFullAudit.lean')} contém `#check` e `#print axioms` dos **16 alvos (3+6+7), incluindo as duas definições**; todos retornaram exatamente `propext`, `Classical.choice`, `Quot.sound`. {link('Tipos elaborados e axiomas', RUN / 'logs/DualFixedCoreFullAudit.stdout.txt')}. Nenhum alvo omitido ou axioma extra.

O último ambiente contém **{len(M['dependencies'])} dependências de projeto congeladas** com hashes de fontes e binários. O `LEAN_PATH` usa o build próprio e os pacotes em leitura, sem builds vivos de projeto do autor/canônico. Dependências já conferidas foram reutilizadas, sem recompilação. Compilador, comandos, hashes e proveniência estão no {link('manifesto', RUN / 'manifest.json')}. Mathlib e demais pacotes não foram integralmente congelados ou recompilados; seguem como base de confiança. A definição VNA usada é a concreta por bicomutante, sem reivindicar uma construção de predual.

[REAL — inspeção da integração; compilações e controles integrados executados pelo autor] {link('Verificação congelada', CAP / 'verification.json')}: **{V['integrated_modules']} registros rc0**, com hashes atuais de cada fonte e `.olean` correspondentes aos registros; **{len(V['reused_same_binary_and_source_as_44'])}** fontes/binários idênticos ao estrato 44, mais os três módulos e duas raízes novos. As cópias `TGLExt/V350*.lean` coincidem com os dev congelados salvo os imports, e seus textos coincidem com os bytes embutidos. As alterações antigas se restringem às duas raízes, cujos imports e alvos foram conferidos.

**SHA-256 medido do monólito: `{V['um_sha256']}`; {V['embedded_files']} arquivos embutidos.** O hash coincide com os relatórios de integração e controles. A análise AST foi somente leitura/literal de dados: o corpo Python fora do dicionário embutido permanece igual ao estrato anterior, e `gate_extension.py` é byte a byte idêntico. Não houve importação ou execução do monólito.

Os registros do autor mostram **{V['gate_checks_count']}/{V['gate_checks_count']} controles aprovados e {V['audit_distinct']} declarações distintas no Audit**, sem axioma fora do trio. Os 16 alvos têm os mesmos axiomas no auditor próprio e no integrado. {link('Suplemento de verificação', CAP / 'supplemental_verification.json')} confronta o relatório de axiomas com o stdout efetivo do Audit e confirma as seis flags abertas falsas. O controle adicional registra a presença dos resultados e a permanência dessas flags; não prova identificação da base, peso ou traço. Não reexecutei controles Python ou raízes integradas; essas contagens são evidência do autor inspecionada, distinta das seis execuções próprias.

[REAL — revisão documental] A minuta {link('record_fixed_resolvent_progress.py congelado', RUN / 'final_recorder/record_fixed_resolvent_progress.py')}, SHA-256 `{SUP['recorder_sha256']}`, foi lida integralmente e analisada como texto/AST, **sem execução**. O relatório e o adendo projetados distinguem corretamente unicidade condicional de existência, F da base original, K do ambiente e finitude vetorial de semifinitude de peso. Não foi encontrado exagero matemático nos estatutos. As futuras escritas nas 13 superfícies e a custódia do autor não são certificadas como executadas por esta revisão.

Limites preservados: **[OPEN]** F=base amplificada, afiliação completa de T/S à álgebra fixa/base com setor infinito, cone ampliado e peso operadorial, semifinitude na álgebra, traço, Three Locks, hipóteses físicas e runtime integral. K continua `closure(D(q_A))`, possivelmente zero ou próprio; não é P_F. A fixação do resolvente limitado não fornece, por si só, todas essas construções. Não se reivindica unicidade abstrata da raiz, cálculo espectral não limitado completo ou confirmação física/QG. Nenhuma flag é quitada pelo parecer.

[REAL — preservação e encerramento] O parecer anterior `REVIEW_DUAL_FORM_REPRESENTATION.md` continua com SHA-256 `{previous_sha}`, igual à custódia lida. O escopo autorizado — três fontes finais, 16 alvos, recompilações próprias, minuta e inspeção dos artefatos integrados — está **concluído**, sem verificação substantiva remanescente. Fontes, originais, logs, monólito, memórias e pareceres custodiados foram preservados. Toda escrita desta revisão ficou em `revisao/`.
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
           "independent_auditors": 3, "all_six_processes_rc0": True, "independent_targets": 16,
           "integrated_inspection": str(CAP), "integrated_records": V["integrated_modules"],
           "author_test_count": V["gate_checks_count"], "author_Audit_distinct": V["audit_distinct"],
           "working_um_sha256": V["um_sha256"], "recorder_not_executed": True,
           "full_runtime_not_executed": True}
out = RUN / ("review_final_delivery_" + stamp + ".json")
with out.open("xb") as f:
    f.write(json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf-8"))
assert readj(out) == receipt
print(json.dumps(receipt, ensure_ascii=False, indent=2))
