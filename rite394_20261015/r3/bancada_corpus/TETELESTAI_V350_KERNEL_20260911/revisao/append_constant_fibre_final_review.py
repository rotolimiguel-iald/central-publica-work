"""Append the independent seven-module verdict without rewriting the first stratum."""
from pathlib import Path
import datetime, hashlib, json, sys

sys.stdout.reconfigure(encoding="utf-8")
REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "constant_fibre_identification_latest_run.txt").read_text(encoding="utf-8"))
M = json.loads((RUN / "manifest.json").read_bytes())
C = json.loads((RUN / "compilation.json").read_bytes())
FIRST = Path(M["previous_run"])
FM = json.loads((FIRST / "manifest.json").read_bytes())
FC = json.loads((FIRST / "compilation.json").read_bytes())
CAP = max(p for p in RUN.glob("final_integrated_*") if (p / "supplemental_verification.json").exists())
V = json.loads((CAP / "verification.json").read_bytes())
S = json.loads((CAP / "supplemental_verification.json").read_bytes())
sha = lambda b: hashlib.sha256(b).hexdigest()

assert all(C[k] for k in ("complete", "all_exit_zero", "full_audit_names_exact", "all_axioms_allowed",
                         "sources_unchanged", "dependencies_unchanged", "previous_reviews_preserved"))
assert len(C["records"]) == 4 and len(C["records"][-1]["axioms"]) == 26
assert len(M["all_named_declarations"]) == 37
assert all(V[k] for k in ("exact_expected_file_set", "all_exit_zero", "all_hashes_match",
                          "gate_checks_all_passed", "um_matches_gate_report", "um_matches_integration_report",
                          "python_ast_outside_embedded_unchanged", "gate_extension_byte_identical_to_63",
                          "previous_reviews_preserved", "evidence_axioms_equal_log", "recorder_ast_parse_ok"))
assert not V["audit_unexpected_axioms"] and all(v is False for v in V["six_flags"].values())
assert all(S[k] for k in ("integration_build_ok", "own_auditor_equals_integrated_new_axioms",
                          "integrated_new_compilations_sources_unchanged", "all_integrated_sources_equal_embedded",
                          "next_stage_not_embedded", "all_26_printed_by_Audit", "new_root_imports_present",
                          "all7_sources_still_frozen", "original_matches_base_and_integration",
                          "historical_inventory_unchanged", "inventory_not_runtime_clearance"))
assert S["legacy_gate_changed"] is False and S["full_plan_complete"] is False
assert (V["integrated_modules"], V["gate_checks_count"], V["audit_distinct"], V["embedded_files"]) == (70, 64, 6218, 772)
assert C["records"][-1]["axioms"] == V["new_targets_axioms"]
assert sha((ROOT / "um.py").read_bytes()) == V["um_sha256"]
for name, row in V["source_matches"].items():
    assert row["dev_still_frozen"] and row["same_except_import_paths"] and row["embedded_matches"]
for row in {**FM["sources"], **M["sources"]}.values():
    assert sha(Path(row["path"]).read_bytes()) == row["sha256"]
for row in M["dependencies"].values():
    assert sha(Path(row["frozen_source"]).read_bytes()) == row["source_sha256"]
    assert sha(Path(row["frozen_binary"]).read_bytes()) == row["sha256"]
for p, h in M["previous_reviews"].items():
    assert sha(Path(p).read_bytes()) == h
for name in ["MINUTA_FIBRA_CONSTANTE.md", "record_constant_fibre_progress.py"]:
    assert (ROOT / name).read_bytes() == (CAP / name).read_bytes(), "Documentary change requires a literal diff: " + name

stamp = datetime.datetime.now().astimezone()
table = "\n".join(f'| `{Path(n).stem}` | {len(r["declarations"])} | `{r["sha256"]}` |'
                  for n, r in M["sources"].items())
builds = "\n".join(f'| `{Path(r["module"]).name}` | rc0 | {r["seconds"]} s | `{r["output_sha256"]}` |'
                   for r in C["records"])
integrated = "\n".join(f'| `V350{n}.lean` | `{r["integrated_sha256"]}` |'
                       for n, r in V["source_matches"].items())
logs = "; ".join("`" + Path(r["author_log"]).name + "`" for r in M["sources"].values())
artifacts = "\n".join(f'- `{n}`: `{V["artifact_sha256"][n]}`.' for n in
                       ["integration.json", "integrated_compile.json", "gate_tests.json", "kernel_incremental_evidence.json"])
report = REVIEW / "REVIEW_UNIT_INTERVAL_PROJECTION.md"
old = report.read_bytes()
assert sha(old) == json.loads((FIRST / "source_review_receipt.json").read_bytes())["report_sha256"]
body = f'''

---

## Adendo final — identificação global da fibra, sete módulos / 26 alvos

{stamp.isoformat(timespec="seconds")}. **[REAL — revisão independente concluída no escopo autorizado] Nenhum P0/P1 ou defeito matemático P2 encontrado nas sete fontes. Um P2 documental permanece em `MINUTA_FIBRA_CONSTANTE.md:23–24`, descrito abaixo.** O estrato anterior de quatro fontes permanece literalmente preservado; este adendo encerra os nove alvos adicionais e a inspeção integrada/documental dos 26. A igualdade global, que era OPEN no primeiro estrato, agora foi conferida. C∈M e F=base continuam OPEN.

### Achado documental P2

**`MINUTA_FIBRA_CONSTANTE.md:23–24` — “integrais de conjuntos finitos” não expressa a hipótese usada.** Substituir por **“integrais sobre conjuntos mensuráveis de medida finita”**. Sob Lebesgue, conjuntos finitos têm medida zero; testar somente esses integrais não detectaria uma função L² não nula. Em contraste, `L2CutIntegral.lean:61–68` quantifica corretamente sobre S mensurável com `volume S < ∞` e fornece sua integrabilidade. A correção é documental, sem necessidade matemática de editar Lean ou repetir compilações.

Minuta efetivamente lida e congelada, ainda com essa frase: SHA **`{V['artifact_sha256']['MINUTA_FIBRA_CONSTANTE.md']}`**. O recorder lê essa minuta por `.format`, portanto o texto incorreto seria transportado ao relatório se executado nessa versão. A ocorrência foi comunicada ao autor; não alterei a minuta. O snapshot original do achado está preservado na árvore própria.

### Composição e tipos dos nove alvos adicionais

**`L2CutIntegral.lean:12–49` (quatro lemas).** A fórmula de recorte restringe a integral a S∩T, usando igualdade ae e `Measure.restrict_restrict` com a mensurabilidade de T. A primeira identidade não precisa supor S mensurável nem integrabilidade: é uma igualdade das mesmas funções/medidas restritas, não uma inferência de nulidade a partir do valor totalizado de uma integral. A fórmula seguinte usa o adjunto já construído e identifica ∫_S P_I f com e*(P_S f). Para passar C pela integral sobre I, a prova fornece explicitamente integrabilidade de f∈L² em I de medida finita. `fibre_commutes_measurableCut` é uma igualdade de CLMs no quociente L², para todo recorte mensurável S; a prova combina apenas as quatro igualdades ae referentes ao C, S e f fixados.

**`L2CutIntegral.lean:53–69` (nulidade local).** Para cada f, a prova aplica `Lp.ae_eq_zero_of_forall_setIntegral_eq_zero` a P_I Af com p=2, justificando p≠0 e p≠∞. Para **cada conjunto mensurável S de medida finita**, fornece L¹ local por `integrableOn_Lp_of_measure_ne_top`, transforma o integral em e*P_S Af, usa P_S A=A P_S e termina com a hipótese e*A=0, válida para todo vetor L². Assim, o valor zero não provém da convenção de integral de função não integrável. O resultado é primeiro nulidade ae e depois igualdade no quociente por `Lp.ext`, fornecendo P_I A=0 como operador.

O lema primário Mathlib foi lido em `MeasureTheory/Function/AEEqOfIntegral.lean:229–240,284–320`: a separabilidade usada internamente é da **imagem essencial de cada função fortemente mensurável**, deduzida de sua integrabilidade; não é uma hipótese de separabilidade de H. Também não se intersectam conjuntos de medida plena indexados por todos os recortes ou por todos os vetores.

**`ZeroFromTranslatedCuts.lean:14–49`.** A comutação S_t A=A S_t transporta P_I A=0 para P_I S_n Af=0, com S_n f(x)=f(x−n). Após as identidades ae do recorte e da translação, a mudança y=x+n preserva Lebesgue e dá `x+n∈(0,1] → Af(x)=0` quase sempre, para cada n∈ℤ. `ae_all_iff` reúne **somente a família enumerável ℤ**, depois de fixado f. A escolha n=1−⌈x⌉ satisfaz 0<x+n≤1, inclusive nos pontos inteiros (que caem no extremo 1). `Lp.ext` e a extensionalidade de CLMs concluem A=0. Não há um conjunto excepcional comum não enumerável, continuidade pontual de representantes L², ou substituição do grupo contínuo por um modelo discreto.

**`ConstantFibreIdentification.lean:15–39`.** B é um único CLM em L²(ℝ,H), e C=`fibreCandidate B`=e*Be é um único CLM em H. Para A=B−fibre(C), a comutação com todos os S_t vem de `hshift` e `shift_commutes_fibre`; a comutação com todos os P_S vem de `hchar` pela localidade já provada e da comutação da amplificação com recortes. A identidade e*A=0 usa e*B=C e* e e*fibre(C)=C e*. Os dois lemas de nulidade anteriores dão A=0, logo **B=fibre(C) em todo L²**, não apenas em e(H). As hipóteses dos auxiliares foram efetivamente satisfeitas; não sobra uma premissa residual de nulidade ou de decomposição constante.

**`ConstantFibreIdentification.lean:41–59`.** A unicidade é entre todos C:H→L[ℂ]H, obtida pela injetividade da mesma amplificação. A especialização a B∈`dualFixedCore P` fornece as duas comutações para o mesmo `TowerHilbert P` e conclui B=fibre(e*Be). Não muda a representação, o parâmetro P, a medida de Lebesgue ou a convenção dos caracteres. Não há hipótese de positividade, auto-adjunção ou unitariedade de B, nem de H não trivial. **C é elemento de B(H), não a álgebra B(H) nem um elemento de M já demonstrado.** A fonte assinala expressamente essa última obrigação em suas linhas 51–53.

### Recompilação própria e herança delimitada

| Fonte adicional em `kernel/TGLV350` | Alvos | SHA-256 dev lido |
|---|---|---|
{table}

Logs rc0 do autor conferidos com as fontes congeladas e seus binários: {logs}. Esses registros foram copiados como evidência do autor; os processos abaixo são novos processos do revisor.

O segundo build está em `{RUN.name}`. Reutiliza **{len(M['dependencies'])} dependências de projeto** congeladas: as 346 do primeiro estrato e seus quatro módulos já recompilados. Os bytes das fontes e dos `.olean` foram pinados; o manifest registra a origem de cada dependência e sua concordância com a fonte viva. **As quatro fontes anteriores não foram recompiladas novamente.** Pacotes externos instalados permanecem somente para leitura e não foram reconstruídos nem recertificados como biblioteca inteira. O LEAN_PATH começa exclusivamente pelo build próprio, seguido dos pacotes; os builds do projeto do autor não participam desse caminho.

| Processo novo executado pelo revisor | Resultado | Tempo | SHA-256 `.olean` próprio |
|---|---|---|---|
{builds}

Os três binários adicionais coincidem com os do autor. No conjunto de sete, seis coincidem; permanece a diferença de hash em `UnitIntervalProjection` explicitada no primeiro estrato. Sua causa não foi determinada, portanto **não reivindico reprodutibilidade binária 7/7**. Isso não foi ocultado nem tratado como prova falsa: a mesma fonte recompilou rc0 no ambiente pinado, e os tipos e axiomas foram examinados. Não houve falha Lean própria.

O auditor adicional executou **37 `#check` e 26 `#print axioms`**: os 28 tipos do primeiro estrato, mais os nove novos; 11 auxiliares são conferidos por tipo e transitivamente, sem inflar a contagem de alvos impressos. Seu stdout foi lido integralmente. Os **26 alvos distintos** têm apenas `propext`, `Classical.choice`, `Quot.sound`, e o mapa completo coincide com o Audit integrado. No total desta revisão: **sete compilações de módulos e dois auditores próprios, nove processos rc0**. [Manifest do adendo](<{(RUN/'manifest.json').as_posix()}>) e [resultados próprios](<{(RUN/'compilation.json').as_posix()}>).

### Integração e controles: inspeção, sem repetir a execução do autor

Snapshot final medido: **`{V['um_sha256']}`**, **{V['embedded_files']} arquivos embutidos**. O monólito foi tratado por `ast.parse` e `ast.literal_eval` do dicionário Lean, nunca executado ou importado.

| Evidência | O que foi efetivamente conferido pelo revisor |
|---|---|
| 70 registros Lean rc0 | Leitura do relatório e dos logs; hashes atuais das 70 fontes e dos 70 `.olean`, correspondentes aos registros. Não fiz um rebuild próprio dessas raízes/70 módulos. |
| 61 reutilizados + 7 módulos e 2 raízes recompilados | Comparação de fontes/binários com a captura da localidade anterior; os nove novos registros indicam fonte inalterada durante a compilação. |
| 64/64 controles | Leitura do relatório do autor; todos `passed=true`. Não reexecutei esses testes. O controle novo exige os lemas centrais presentes e as seis flags falsas. |
| Audit: 6.218 declarações distintas | Extração do stdout do autor; axiomas no trio e igualdade do mapa com `kernel_incremental_evidence.json`. Os 26 novos também foram auditados em processo próprio. |
| Integração das sete fontes | Dev igual ao integrado com **somente a reescrita dos imports** `TGLV350.`→`TGLExt.V350`; bytes das fontes integradas iguais aos embutidos. Imports das raízes e impressão dos 26 alvos presentes. |

| Fonte integrada | SHA-256 lido |
|---|---|
{integrated}

A diferença do dicionário em relação ao snapshot anterior contém exatamente as sete fontes novas e as alterações em `TGLExt.lean`/`TGL/Audit.lean`; não há remoção. O AST Python fora do dicionário permaneceu igual ao backup de SHA `{V['previous_um_sha256']}`. `gate_extension.py` permaneceu byte a byte igual ao estrato anterior. `legacy_gate_changed=false` e `full_plan_complete=false` estão em **`gate_tests.json.frontier`**; a extração inicial tentou a raiz desses JSON e registrou null, corrigido pela leitura do caminho efetivo em `supplemental_verification.json`. Null não foi interpretado como false.

As seis flags maiores permanecem falsas; `full_monolithic_runtime_run=false`. O original e a cópia-base foram lidos novamente e têm SHA **`{S['original_sha256']}`**, concordante com `integration.json`. Não foram escritos. Evidências congeladas: [verificação de integração](<{(CAP/'verification.json').as_posix()}>) e [conferências complementares](<{(CAP/'supplemental_verification.json').as_posix()}>).

Hashes dos relatórios efetivamente lidos:

{artifacts}

### Minuta, recorder e limites finais

`record_constant_fibre_progress.py` foi lido integralmente e analisado por AST, SHA **`{V['artifact_sha256']['record_constant_fibre_progress.py']}`**. A minuta também foi lida integralmente, no hash indicado no P2. Exceto pela expressão “conjuntos finitos”, a narrativa acompanha os tipos: existência e unicidade de C∈B(H), mesmas e/Q/P_I/C, identidade no L² inteiro e C∈M/F=base abertos. Não converte integração vetorial em integral em norma de B(H), nem a cobertura inteira em discretização do core.

O recorder prevê 19 superfícies de append (17 locais e dois índices globais), backups de bytes, temporário verificado e condição `--review-read`. Inspecionei esse mecanismo, **não o executei** e não atesto uma custódia futura como já realizada. Os resultados herdados que constam de seu dicionário de custódia não foram reprovados nesta etapa. O inventário I/O é corretamente mantido histórico: SHA `{S['historical_inventory_sha256']}`, referente à cópia `{S['historical_inventory_source_sha256']}`; não libera o runtime do snapshot atual.

**Limite efetivo:** a etapa provou a ação constante global e única B=fibre(C) para B∈F. Ainda não provou C∈M/F=base, a correspondência geral espectral/predual, a interface padrão de peso operatorial, estado/gerador/perturbação e traço canônico, semifinitude/Three Locks/H1–H3/física, contrato ampliado ou runtime. Esses limites não são bugs das provas reivindicadas. `StrongOperatorField` e `OperatorFieldFaithfulness` foram verificados apenas quanto à ausência do dicionário integrado; suas fontes e teoremas **não foram revisados**.

**Parecer encerrado:** matemática, recompilações próprias, integração por inspeção e análise documental concluídas para **sete módulos/26 alvos**. Sem P0/P1 ou P2 matemático; **P2 documental aberto na versão da minuta examinada**. Não há outra análise específica pendente neste escopo. A divergência binária isolada está declarada como limite de reprodutibilidade, sem causa atribuída. Não aprovo F=base, traço, gate, QG ou runtime. Somente este parecer e a árvore própria em `revisao/` receberam escrita; pareceres custodiados, memórias, fontes do autor e logs originais permanecem intactos.
'''

marker = "## Adendo final — identificação global da fibra, sete módulos / 26 alvos"
assert marker.encode("utf-8") not in old
backup = report.with_name(report.name + ".bak_" + stamp.strftime("%Y%m%d_%H%M%S_%f"))
with backup.open("xb") as handle:
    handle.write(old)
assert backup.read_bytes() == old
raw = old + body.encode("utf-8")
tmp = report.with_name(report.name + ".tmp_" + stamp.strftime("%Y%m%d_%H%M%S_%f"))
with tmp.open("xb") as handle:
    handle.write(raw)
assert tmp.read_bytes() == raw and len(raw) > len(old) and raw.startswith(old)
tmp.replace(report)
assert report.read_bytes() == raw and backup.read_bytes() == old
receipt = {"timestamp": stamp.isoformat(), "report": str(report), "report_sha256": sha(raw),
           "report_bytes": len(raw), "backup": str(backup), "backup_sha256": sha(old),
           "old_prefix_exact": raw.startswith(old), "review_complete": True,
           "independent_module_compiles": 7, "independent_auditor_compiles": 2,
           "all_own_exit_zero": True, "cumulative_printed_targets": 26, "checked_named_types": 37,
           "integrated_modules_inspected": 70, "author_controls_read_not_rerun": 64,
           "integrated_audit_distinct": 6218, "working_sha256": V["um_sha256"],
           "P0": [], "P1": [], "P2_mathematical": [],
           "P2_documentary": [{"file": "MINUTA_FIBRA_CONSTANTE.md", "line": 23,
                               "status": "OPEN", "text": "conjuntos finitos -> conjuntos mensuráveis de medida finita"}],
           "binary_reproducibility": "6/7 MATCH; UnitIntervalProjection differs, cause not determined",
           "author_sources_preserved": True, "other_reviews_preserved": True,
           "runtime_or_recorder_executed": False, "F_equals_base_proved": False}
with (RUN / "final_report_receipt.json").open("xb") as handle:
    handle.write(json.dumps(receipt, indent=2, ensure_ascii=False).encode("utf-8"))
print(json.dumps(receipt, indent=2, ensure_ascii=False))
