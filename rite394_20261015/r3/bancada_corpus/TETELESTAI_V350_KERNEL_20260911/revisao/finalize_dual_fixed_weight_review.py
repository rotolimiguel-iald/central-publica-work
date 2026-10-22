"""Write the bounded independent review from frozen evidence; never execute author code."""
from pathlib import Path
import datetime
import hashlib
import json

REVIEW = Path(__file__).resolve().parent
ROOT = REVIEW.parent
RUN = Path((REVIEW / "dual_fixed_weight_latest_run.txt").read_text(encoding="utf-8"))
CONE = Path((REVIEW / "positive_form_cone_latest_run.txt").read_text(encoding="utf-8"))
CAP = max(RUN.glob("final_integrated_*"))
read = lambda p: json.loads(p.read_bytes())
sha = lambda raw: hashlib.sha256(raw).hexdigest()
M, C = read(RUN / "manifest.json"), read(RUN / "compilation.json")
M1, C1 = read(CONE / "manifest.json"), read(CONE / "compilation.json")
V = read(CAP / "verification.json")
S = read(CAP / "supplemental_verification.json")
F = read(CAP / "final_scope_verification.json")
G = read(CAP / "gate_tests.json")
DOC = F["documents"]
DATE = datetime.datetime.now().astimezone().isoformat(timespec="seconds")

def link(label, path, line=None):
    return f"[{label}](<{Path(path).as_posix()}{':' + str(line) if line else ''}>)"

def source(name, line):
    return link(name + ":" + str(line), ROOT / "kernel/TGLV350" / name, line)

for compilation in [C1, C]:
    assert all(compilation[k] for k in ["complete", "all_exit_zero", "full_audit_names_exact",
        "all_axioms_allowed", "sources_unchanged", "dependencies_unchanged", "previous_reviews_preserved"])
assert V["all_exit_zero"] and V["all_hashes_match"] and V["exact_expected_file_set"]
assert S["all_printed_targets_in_integrated_Audit"] and S["independent_and_author_axioms_match_on_printed_targets"]
assert F["original_and_base_match_integration"] and F["documents_unchanged"]
assert F["inventory_matches_historical_previous_custody"] and F["previous_custodied_review_matches"]
assert V["python_ast_outside_embedded_unchanged"] and V["gate_extension_byte_identical_to_50"]
assert S["all_six_open_flags_false"] and not G["frontier"]["full_plan_complete"]
assert not G["frontier"]["legacy_gate_changed"]
assert all(set(a) == {"propext", "Classical.choice", "Quot.sound"} for a in C["records"][-1]["axioms"].values())
assert sha((ROOT / "um.py").read_bytes()) == V["um_sha256"]
assert all(sha(Path(p).read_bytes()) == h for p, h in M["previous_reviews"].items())
assert all(sha((ROOT / n).read_bytes()) == row["sha256"] for n, row in DOC.items())
for manifest in [M1, M]:
    for row in manifest["sources"].values():
        assert sha(Path(row["path"]).read_bytes()) == row["sha256"]

table_sources = []
table_processes = []
author_logs = []
for name, manifest, compilation, run in [("PositiveFormCone", M1, C1, CONE), ("DualFixedWeightLaws", M, C, RUN)]:
    row = manifest["sources"]["TGLV350/" + name + ".lean"]
    integrated = V["source_matches"][name]
    table_sources.append(f"| {name} ({row['lines']} linhas) | `{row['sha256']}` | `{integrated['integrated_sha256']}` |")
    author_logs.append(link(Path(row["author_log"]).name, row["author_log"]))
    assert compilation["records"][0]["output_sha256"] == row["author_binary_sha256"]
    for record in compilation["records"]:
        table_processes.append(f"| {Path(record['module']).name} | {record['returncode']} | {record['seconds']:.3f} | {len(record['axioms'])} |")

text = f"""# Revisão independente — cone de formas e peso na álgebra fixa

{DATE}. **Escopo delimitado concluído. Nenhum achado P0, P1 ou P2 identificado nas duas fontes finais, na sua composição ou nas afirmações matemáticas da minuta examinada.**

[REAL — recompilação própria] Foram recompilados `PositiveFormCone.lean`, `DualFixedWeightLaws.lean` e dois auditores próprios, com quatro processos rc0. O auditor final conferiu tipos e axiomas de **{S['printed_source_targets']} alvos impressos pelo autor + 2 alvos adicionais = {S['independent_declarations_count']} declarações distintas**, todas exatamente em `propext`, `Classical.choice`, `Quot.sound`.

[REAL — inspeção de fontes/logs/hashes] A integração contém **{V['integrated_modules']} registros**, os registros dos controles indicam **{G['passed']}/{len(G['checks'])} aprovados**, o stdout integrado do Audit contém **{V['audit_distinct']} declarações distintas**, e o dicionário do monólito contém **{V['embedded_files']} arquivos**. Estas compilações integradas e estes controles são processos do autor, cujos artefatos conferi; não os reexecutei.

## Significado e composição conferidos

1. **Cone concreto, incluindo infinito.** {source('PositiveFormCone.lean', 12)} e {source('PositiveFormCone.lean', 57)} provam extensionalidade pelo valor, suficiente para antissimetria. Zero, soma, escala e pré-composição preservam os campos de `ClosedPositiveForm`: valor ENNReal, q(0)=0, homogeneidade vetorial, paralelogramo e semicontinuidade inferior. A soma usa semicontinuidade da adição; a escala usa continuidade da multiplicação por um escalar **NNReal finito**, inclusive zero. Não há passagem por `toReal`; `0·∞=0` é mantido ({source('PositiveFormCone.lean', 40)}). Não se supõe densidade do domínio finito. Para escala zero, o domínio pode tornar-se todo o espaço, sem contradição.

2. **Ordem e conjugação corretamente tipadas.** A instância em {source('PositiveFormCone.lean', 65)} é `PartialOrder (AffiliatedPositiveForm N)`, por transporte da ordem pontual: Q≤R significa ∀v, Q(v)≤R(v). Não é uma ordem invertida nem uma instância adicional afirmada para `ClosedPositiveForm`. As leis de soma/escala e sua monotonicidade estão nas linhas 101–147. As operações são definições e leis explícitas; não se afirma uma estrutura de espaço vetorial ou um cone espectral geral. A pré-composição é válida para qualquer operador limitado B. A conjugação afiliada requer B∈N e usa UB=BU, para cada unitário U do comutante de N; a simetria na linha 98 produz precisamente BUv=UBv ({source('PositiveFormCone.lean', 91)}). B não precisa ser unitário.

3. **Entrada positiva e mesma realização.** {source('DualFixedWeightLaws.lean', 15)} define efetivamente os operadores limitados A∈N, A≥0, com N=`regularCoreAlgebra P`, no mesmo H=`RegularHilbert (TowerHilbert P)`. A ordem de entrada é a ordem de operadores herdada pelo subtipo. Zero, soma e escala constroem os respectivos certificados de pertinência e positividade; a coerção r:NNReal→ℝ→ℂ na escala não troca a ação sobre H. Para B∈F, F=`dualFixedCore P`, `dualFixedCore_mem_iff` fornece B∈N e θ_s(B)=B. Assim B*AB continua sendo uma entrada positiva de N ({source('DualFixedWeightLaws.lean', 38)}).

4. **Mapa de saída concreto e leis inteiras.** Em {source('DualFixedWeightLaws.lean', 50)}, `dualFixedWeight P A` é a forma afiliada a F já construída; sua avaliação é **definicionalmente** `dualQuadraticIntegral A.val v` (linha 54). F não depende de uma nova escolha por entrada. O contrato recebe somente P e a entrada positiva; não recebe como premissa um resolvente, limite forte ou testemunha de afiliação. As igualdades de zero, soma e escala são igualdades das estruturas de saída por extensionalidade (linhas 58–76), com valores ∞ preservados. Aditividade usa expressamente a positividade de ambas as entradas. A normalização herdada permanece `(2π)⁻¹`, não uma média dependente do corte; sua identificação Fourier não ganhou aqui um teorema novo.

5. **Bimódulo sobre todo F.** {source('DualFixedWeightLaws.lean', 78)} prova q_(B*AB)(v)=q_A(Bv) usando θ_s(B)=B, multiplicatividade, preservação do adjunto e `operatorQuadratic_conjugate`. Este último tem orientação ⟨v,B*ABv⟩=⟨Bv,ABv⟩ na representação em uso. Em {source('DualFixedWeightLaws.lean', 93)}, isso fornece T(B*AB)=B*T(A)B, onde o lado direito significa a conjugação por pré-composição definida no cone. B percorre o subtipo inteiro de F, sem restrição a operadores amplificados da base. Não foi usada a igualdade F=base.

6. **Monotonicidade e fidelidade da família.** {source('DualFixedWeightLaws.lean', 100)} preserva A≤B. Em {source('DualFixedWeightLaws.lean', 105)}, T(A)=forma zero implica q_A(v)=0 **para todo v**, e então A=0 pelo lema de fidelidade anterior, com A≥0. Conferi a dependência: integral nula → integrando nulo quase sempre → nulo em todo parâmetro por continuidade e suporte pleno de Lebesgue → avaliação em s=0 e positividade. Não se confunde anulação em um vetor com anulação do operador, nem se presume finitude universal das avaliações.

7. **Normalidade em ordem, sem premissa residual SOT.** {source('DualFixedWeightLaws.lean', 118)} deriva 0≤S de 0≤A_i≤S escolhendo um índice, permitido por `Nonempty ι`. O teorema final, {source('DualFixedWeightLaws.lean', 126)}, quantifica um preordenado arbitrário com `IsDirectedOrder` e `Nonempty`, A positivo e monótono, e um `IsLUB (range A) S` **interno à mesma N**. Não exige enumerabilidade, S≥0 separado ou convergência forte como hipótese. Usa `regularDualForm_preserves_internal_isLUB`, cujo tipo e composição relidos dão q_S(v)=sup_i q_Ai(v). A cadeia anterior constrói um limite positivo limitado em norma, mantém-no em N pelo fechamento WOT, identifica-o ao supremo interno por unicidade e obtém o supremo ambiente; não pressupõe esse passo para prová-lo. As linhas 133–141 verificam tanto a propriedade de majorante quanto a minimalidade contra **qualquer forma afiliada majorante** Q. Portanto o resultado é um `IsLUB` no cone de saída, não só uma igualdade de avaliações sem relação com a ordem da estrutura.

## Recompilação e herança

Fontes congeladas byte a byte; hashes lidos dos arquivos e confrontados com os logs finais do autor:

| Módulo dev | SHA-256 dev | SHA-256 integrado TGLExt/V350 |
|---|---|---|
{chr(10).join(table_sources)}

Logs do autor: {'; '.join(author_logs)}. Os dois `.olean` produzidos pelos meus processos também coincidem em SHA-256 com os binários dev finais do autor. Hashes completos dos binários, comandos, stdout/stderr e tipos elaborados estão nos manifestos e resultados abaixo.

| Processo próprio | rc | Segundos | Alvos de axiomas na saída |
|---|---:|---:|---:|
{chr(10).join(table_processes)}

O primeiro auditor contém 18 alvos do cone e um invólucro que sintetiza e audita transitivamente sua instância anônima `PartialOrder`. O auditor final contém os 33 alvos impressos nas duas fontes, mais o `abbrev PositiveCoreInput` e esse invólucro. Não foram somadas verificações repetidas como novos teoremas. O aviso de redutibilidade do invólucro de classe pertence ao meu auditor; é benigno, sem falha de elaboração ou axioma adicional.

Usei **{len(M1['dependencies'])} pares de fonte/binário de dependências do projeto** no primeiro snapshot e **{len(M['dependencies'])}** no segundo, que acrescenta o cone recompilado por mim. As dependências anteriores vieram dos snapshots da revisão precedente, foram copiadas e conferidas por hash contra seus manifestos e fontes atuais. Não reconstruí esses módulos nem a biblioteca. `LEAN_PATH` começa no build próprio e segue somente para os pacotes existentes em leitura; não inclui o build dev/integrado do autor como alternativa para módulos do projeto. Pacotes e compilador são herança do ambiente fixado, não uma recompilação independente da Mathlib.

Compilador: `{M['lean_version']}`; SHA-256 `{M['compiler_sha256']}`. `TMP`/`TEMP`, fontes, binários novos e logs próprios ficaram em `revisao/`.

Evidência própria: {link('manifesto do cone', CONE/'manifest.json')}, {link('compilação do cone e auditor', CONE/'compilation.json')}, {link('manifesto do peso e dependências', RUN/'manifest.json')}, {link('compilação do peso e auditor final', RUN/'compilation.json')}, {link('auditor completo: tipos e axiomas', RUN/'logs/DualFixedWeightFullAudit.stdout.txt')}.

## Integração e documentação

Snapshot final lido: **`{V['um_sha256']}`**. Base original relida: `{F['original_sha256']}`, igual à cópia-base e a `integration.json`. Os 52 registros têm rc0 e hashes de fonte/`.olean` correspondentes aos arquivos presentes. São **{len(V['reused_same_binary_and_source_as_50'])} registros anteriores conservados por fonte/binário + 2 módulos novos + 2 raízes recompiladas pelo autor**. Os imports dev→TGLExt são a única diferença nas duas fontes integradas; os bytes embutidos coincidem com elas. Os agregadores só receberam os imports novos e os 33 alvos pertinentes. O stdout integrado do Audit e `kernel_incremental_evidence.json` têm o mesmo mapa de axiomas; os 33 novos coincidem com minha auditoria.

Comparação com o estrato anterior `{V['previous_um_sha256']}`: AST Python fora de `_EMBEDDED_KERNEL_FILES` idêntica; `gate_extension.py` byte a byte idêntico; nenhum embutido removido, apenas dois acrescidos e as duas raízes alteradas. O controle novo verifica presença dos alvos e manutenção das seis flags abertas falsas. Os registros mantêm `legacy_gate_changed=false`, `full_plan_complete=false` e `full_monolithic_runtime_run=false`. A leitura desses controles não equivale a executar o monólito nem a auditar todo seu runtime.

Evidências congeladas: {link('verificação da integração', CAP/'verification.json')}, {link('confronto dos controles e axiomas', CAP/'supplemental_verification.json')}, {link('hashes finais, documentação e preservação', CAP/'final_scope_verification.json')}. As alegações de frescor de dependências dos processos integrados permanecem evidência do procedimento do autor; minha inspeção acrescenta o confronto dos hashes atuais e a comparação com o estrato custodiado.

**Minuta lida integralmente:** {link('MINUTA_PESO_FORMA_FIXA.md', ROOT/'MINUTA_PESO_FORMA_FIXA.md')}, {DOC['MINUTA_PESO_FORMA_FIXA.md']['bytes']} bytes, SHA-256 **`{DOC['MINUTA_PESO_FORMA_FIXA.md']['sha256']}`**. A cópia examinada foi congelada antes do parecer. Os campos de data/contagens são marcadores do template, a serem preenchidos pelo recorder.

“**Peso normal e fiel com valores em formas afiliadas a F**” é um nome adequado ao contrato concreto explicitado nas linhas 5–36: mapa N₊→AffiliatedPositiveForm F, com aditividade, homogeneidade NNReal, bimodularidade e normalidade por `IsLUB`. O qualificativo “em formas” e o sentido de ordem da normalidade devem acompanhar o nome. Isso não certifica uma correspondência geral espectral/predual, nem identifica o mapa ao peso dual canônico da base original. A minuta preserva essas distinções e distingue domínio vetorial da forma de semifinitude do peso na álgebra. Na descrição de semifinitude, “peso finito” deve ser entendido no futuro contrato de entradas da álgebra — não como simples finitude de q_A em algum vetor ou densidade do suporte K.

A parte sobre o gate foi conferida por leitura da função `evaluate_quantum_gravity_closure`: seis entradas formais, cinco físicas e quatro experimentais; as flags de fronteira qgf/gpf não são suas entradas. A remissão ao Ward clássico-linear confere com `PhysicsCertificates.lean:292`; a H2 com pycbc é apresentada pelo próprio texto do monólito como reprodução separada que não modifica o gate. Os demais itens da rota física/traço são obrigações declaradas abertas, não uma nova auditoria de seus módulos neste parecer.

Li estaticamente `record_fixed_weight_progress.py` (SHA `{DOC['record_fixed_weight_progress.py']['sha256']}`) e `verify_fixed_weight_custody.py` (SHA `{DOC['verify_fixed_weight_custody.py']['sha256']}`). A minuta de registro mantém as mesmas limitações e prevê 15 superfícies com backups de bytes. **Não executei recorder/verifier nem certifico uma custódia ainda não executada.** O inventário I/O permanece explicitamente histórico: hash `{DOC['runtime_io_inventory.json']['sha256']}`, ligado ao snapshot anterior por `previous['working_sha256']`, com estatuto `NOT_RUNTIME_CLEARANCE`. Não o reaproveitei como auditoria da cópia atual.

## Limite do parecer

Concluídos os tipos, provas, composição, 33 alvos, dois extras de auditoria, integração estática e minuta deste incremento; não ficou análise matemática específica pendente nesse escopo. A ausência de semifinitude/traço não foi tratada como defeito destas provas.

[OPEN] Identificação F=base original; correspondência geral com cone ampliado espectral/predual; semifinitude do peso e ideal apropriado denso na álgebra; construção do traço canônico e sua escala dual; Three Locks/H1–H3 e compatibilidade física; contrato ampliado consumido pelo gate; execução integral isolada. A representação específica de q_A herdada das etapas anteriores não é um teorema geral para toda forma afiliada. Normalidade aqui é a preservação dos supremos positivos internos especificados, sem equivalência ultra-fraca/predual provada neste lote. K e domínio finito vetorial não são P_F nem um certificado de finitude do peso na álgebra.

Fontes do autor, monólito, originais, logs e memórias permaneceram intocados pelo revisor; todos os pareceres anteriores conferem seus hashes, inclusive o parecer da custódia vigente. Nenhuma aprovação de QG, flag maior, traço, runtime, publicação ou transposição ao canônico decorre desta revisão.
"""

target = REVIEW / "REVIEW_DUAL_FIXED_WEIGHT.md"
raw = text.encode("utf-8")
backup_path = None
if target.exists():
    before = target.read_bytes()
    backup_path = target.with_name(target.name + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
    with backup_path.open("xb") as f:
        f.write(before)
    assert backup_path.read_bytes() == before
temporary = target.with_name(target.name + ".tmp_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
with temporary.open("xb") as f:
    f.write(raw)
assert temporary.read_bytes() == raw and temporary.stat().st_size == len(raw) > 500
temporary.replace(target)
assert target.read_bytes() == raw
assert all(sha(Path(p).read_bytes()) == h for p, h in M["previous_reviews"].items())
receipt = {"timestamp": DATE, "report": str(target), "report_sha256": sha(raw), "report_bytes": len(raw),
    "backup": str(backup_path) if backup_path else None,
    "independent_processes_exit_zero": len(C1["records"]) + len(C["records"]),
    "independent_final_audit_distinct": len(C["records"][-1]["axioms"]),
    "author_printed_targets": S["printed_source_targets"], "working_sha256": V["um_sha256"],
    "template_sha256": DOC["MINUTA_PESO_FORMA_FIXA.md"]["sha256"],
    "findings": {"P0": [], "P1": [], "P2": []}, "bounded_review_complete": True,
    "previous_reviews_unchanged": True, "author_recorder_executed_by_reviewer": False,
    "monolith_executed_or_imported_by_reviewer": False}
out = RUN / "final_report_receipt.json"
assert not out.exists()
with out.open("xb") as f:
    f.write(json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf-8"))
print(json.dumps(receipt, ensure_ascii=False, indent=2))
