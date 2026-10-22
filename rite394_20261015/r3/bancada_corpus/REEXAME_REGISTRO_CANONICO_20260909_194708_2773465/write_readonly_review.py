"""Read current canonical artifacts and write a new scoped review only."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import re

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
HOUSE = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
KERNEL = HOUSE / "tgl_kernel/TGLExt"


def pin(path):
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def new(path, raw):
    assert OUT.is_relative_to(BASE) and path.resolve().is_relative_to(OUT) and not path.exists()
    tmp = path.with_name(path.name + ".tmp")
    with tmp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    os.rename(tmp, path)
    assert path.read_bytes() == raw


program = HOUSE / "um.py"
proof_path = HOUSE / "tgl_kernel_proof_manifest.json"
seal_path = HOUSE / "um_absoluto_selo.json"
proof = json.loads(proof_path.read_bytes())
seal = json.loads(seal_path.read_bytes())
tree = ast.parse(program.read_bytes().decode("utf-8"))
tables = [ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
          and any(isinstance(target, ast.Name) and target.id == "_EMBEDDED_KERNEL_FILES" for target in node.targets)]
assert len(tables) == 1
table = tables[0]
modules = ["SelectedGravitationalAtlas", "GeneralAngularTensorCodec", "CanonicalSelectorBorn",
           "SelectorRecordReconstruction", "AngularSelectorIntertwining", "RelativePhaseCharacter",
           "TransverseGibbsResponse", "MixedQuadraticGibbsResponse", "ProbeResponseRecord",
           "MixedGibbsGravitationalBridge", "FiniteCommutatorEvolution", "SmallTimeLocalDynamics"]
presence = {name: "TGLExt/" + name + ".lean" in table for name in modules}
selected_sources = [KERNEL / name for name in ["TheSelectionIsTheBallast.lean", "TheNameIsTheCharacterization.lean",
                   "CollapseCostAndAttestation.lean", "QuantumCollapseWitness.lean"]]
source_checks = []
for path in selected_sources:
    current = pin(path)
    expected = proof["formal_files_sha256"].get("TGLExt/" + path.name)
    source_checks.append({"source": current, "manifest_sha256": expected,
                          "manifest_pin_matches": current["sha256"] == expected})
terms = ["TGLExt.fair_superposition_selects_forty_five", "TGLExt.the_selection_is_the_ballast",
         "TGLExt.reading_characterizes_the_configuration", "TGLExt.the_name_is_the_characterization",
         "ChatgptAudit.Collapse057.typed_collapse_content", "ChatgptAudit.Collapse057.no_self_attestation",
         "ChatgptAudit.Collapse057.opposite_phases_same_reduction"]
axioms = {name: proof["axiom_report"].get(name) for name in terms}
assert all(value is not None and set(value) <= {"propext", "Classical.choice", "Quot.sound"} for value in axioms.values())
capture_checks = []
for label in ("build", "audit"):
    path = HOUSE / ("tgl_kernel_" + label + "_capture.txt")
    text = path.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
    count = int(re.search(r"len\(stdout\)=(\d+)", text).group(1))
    body = text.split("--- STDOUT ---\n", 1)[1]
    assert body[count:].startswith("\n--- STDERR ---\n")
    measured = hashlib.sha256(body[:count].encode("utf-8")).hexdigest()
    capture_checks.append({"file": pin(path), "returncode": int(re.search(r"# returncode: (\d+)", text).group(1)),
                           "stdout_length": count, "measured_stdout_sha256": measured,
                           "manifest_stdout_sha256": proof[label + "_stdout_sha256"],
                           "stdout_hash_matches": measured == proof[label + "_stdout_sha256"]})

delivery = BASE / "TUNEL/DO_CHATGPT/ENTREGA_063_ESPONTANEA_resposta_Gibbs_dinamica_extensiva.md"
copy83 = BASE / "COPIA_INTEGRADA_20260909_192248_937671/um.py"
prior_note = BASE / "ESTABILIDADE_CARATER_GLOBAL_20260909_193729_5618013/NOTA_ESTABILIDADE_CARATER_GLOBAL.md"
read_paths = [program, proof_path, seal_path, HOUSE / "MEMORIA_DA_LINHAGEM.md",
              HOUSE / "DESENHO_DO_FECHAMENTO_QG.md", delivery, copy83, prior_note] + selected_sources
input_pins = [pin(path) for path in read_paths] + [row["file"] for row in capture_checks]
current = pin(program)
note = f'''# Reexame de registro, colapso, fase e precisão finita

[REAL — leitura atual, sem execução] O caminho canônico examinado continua na versão v337: {current['bytes']:,} bytes, SHA256 `{current['sha256']}`. A tabela embutida tem {len(table)} arquivos. É o mesmo arquivo medido antes da entrega063; não apareceu avanço nesse caminho. Esta constatação não identifica onde a outra sessão eventualmente está trabalhando.

[REAL — fontes e recibos existentes] A linhagem e o desenho terminam no adendo v337 de 09/09 às14:12; selo e manifesto trazem timestamp14:09:22. O recibo informa rodada intermediária com nove ritos reaproveitados. A entrega063 existe no túnel **de saída da bancada**, com instrução de incorporação futura; não é recibo de incorporação canônica. No túnel de entrada examinado, a ordem mais recente continua ORDEM010 de06/09.

**Registro e fase.** O canônico contém a tipagem do colapso, `selectionAngle`, a reconstrução da matriz-S pelo peso e o bicondicional de leitura exata da configuração. [O enunciado dos ramos justos](<{(KERNEL/'TheSelectionIsTheBallast.lean').as_posix()}:139>) continua dando o mesmo peso½ e ânguloπ/4 para ambos os valores de `outcome`. O [ramo normalizado](<{(KERNEL/'QuantumCollapseWitness.lean').as_posix()}:153>) recebe o rótulo `outcome`; o peso comum isolado não o distingue. [Fases opostas](<{(KERNEL/'QuantumCollapseWitness.lean').as_posix()}:75>) continuam colidindo sob a redução não seletiva.

Os módulos de bancada `CanonicalSelectorBorn`, `SelectorRecordReconstruction`, `RelativePhaseCharacter`, `SelectedGravitationalAtlas` e `GeneralAngularTensorCodec`, assim como todas as seis folhas da entrega063, **não estão na tabela embutida canônica examinada**. Estão na cópia83, cujo hash medido é `{pin(copy83)['sha256']}`. A compilação conjunta e a auditoria da cópia83 não devem ser descritas como nova rodada desse canônico.

**Colapso e atestação.** O protocolo atual [continua contendo](<{(KERNEL/'CollapseCostAndAttestation.lean').as_posix()}:96>) `externallyValidated` e a distinção entre produtor e registrador. O próprio [selo](<{seal_path.as_posix()}:401>) registra `OPEN_PHYSICAL_PROVENANCE_NOT_RECEIVED`, `physical_collapse_proven=false` e pagamento `NOT_MEASURED`. Isso é o estado declarado pelo artefato atual. A tipagem e os teoremas condicionais não são, sozinhos, uma nova ocorrência física ou um pagamento medido.

**Precisão finita.** Nenhuma hipótese nova foi encontrada que cubra a [obstrução de estabilidade](<{prior_note.as_posix()}>). Como o canônico permanece idêntico, a diferença em relação a v337 é zero nesse ponto. O caráter de cortes racionais pertence à bancada posterior: nela, a igualdade exata reconstrói a classe, mas bumps suaves mostram falha de continuidade inversa para métricas gerais. Esse controle não refuta a injetividade e não afirma que os bumps satisfaçam as hipóteses físicas de área/Einstein. O que precisaria mudar é a classe admissível e seu controle uniforme de regularidade, amostragem e erro; não foi localizada tal extensão canônica.

**O que foi efetivamente conferido dos recibos formais.** Os hashes atuais dos quatro módulos canônicos examinados coincidem com `formal_files_sha256`. Sete termos relevantes constam no relatório de axiomas, todos no trio permitido. A captura de auditoria registra returncode0 e seu stdout, extraído pelo comprimento e formato escritos pelo programa nas linhas118960–118975, tem hash igual ao manifesto. Isso sustenta o vínculo da auditoria existente com esses registros; nenhuma recompilação foi feita aqui.

[OPEN — divergência de recibo] A captura de build também registra returncode0, mas seu stdout atual tem SHA256 `{capture_checks[0]['measured_stdout_sha256']}`, enquanto o manifesto declara `{capture_checks[0]['manifest_stdout_sha256']}`. O hash foi calculado do stdout extraído, não do arquivo com cabeçalho. A causa não foi determinada; não se atribui fraude, falha de compilação ou alteração de fonte. Esse vínculo específico permanece sem confirmação e está separado da captura de auditoria que conferiu.

Conclusão de escopo: não há incorporação nova verificável no canônico e nos recibos examinados. A incorporação da cópia83, sua rodada canônica e uma teoria de estabilidade com precisão finita continuam sem evidência nova nesta leitura. Originais intactos; nenhum `um.py` executado/importado.
'''
note_path = OUT / "REEXAME_REGISTRO_FASE_PRECISAO.md"
new(note_path, note.encode("utf-8"))
assert all(pin(Path(item["path"])) == item for item in input_pins)
manifest = {"status": "CURRENT_CANONICAL_UNCHANGED__SCOPED_READONLY_REVIEW",
            "created_utc": datetime.now(timezone.utc).isoformat(), "canonical": current,
            "canonical_mtime": datetime.fromtimestamp(program.stat().st_mtime).isoformat(),
            "embedded_count": len(table), "target_module_presence": presence,
            "selected_source_checks": source_checks, "selected_axiom_rows": axioms,
            "capture_checks": capture_checks, "input_pins": input_pins,
            "input_pins_unchanged_after_review": True, "note": pin(note_path),
            "script": pin(Path(__file__).resolve()), "um_py_executed_or_imported": False,
            "compiler_executed": False, "originals_written": False,
            "scope": "No fresh canonical change located in examined paths; not a claim about another session's unobserved working state."}
new(OUT / "MANIFESTO_REEXAME_REGISTRO.json", (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"status": manifest["status"], "note": pin(note_path), "manifest": pin(OUT / "MANIFESTO_REEXAME_REGISTRO.json"),
                  "all_target_modules_absent": not any(presence.values()),
                  "capture_hash_matches": {row["file"]["path"]: row["stdout_hash_matches"] for row in capture_checks}}, ensure_ascii=False))
