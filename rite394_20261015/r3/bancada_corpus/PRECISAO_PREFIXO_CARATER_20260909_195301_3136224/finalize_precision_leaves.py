"""Collect three frozen PASS leaves and write a scoped handoff; never execute um.py."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
TRIO = {"propext", "Classical.choice", "Quot.sound"}

def pin(p):
    b = p.read_bytes()
    return {"path": p.as_posix(), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}

def new(p, b):
    assert OUT.is_relative_to(BASE) and p.resolve().is_relative_to(OUT) and not p.exists()
    t = p.with_name(p.name + ".tmp")
    with t.open("xb") as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert t.read_bytes() == b
    os.rename(t, p)
    assert p.read_bytes() == b

specs = [
    ("CharacterPrefixStability", "BUILD_20260909_200132_598834"),
    ("FiniteCharacterResolution", "BUILD_20260909_200630_996675"),
    ("RecordCharacterMeshControl", "BUILD_20260909_200841_461876")
]
modules, input_pins = [], []
for name, build in specs:
    source = OUT / (name + ".lean")
    receipt_path = OUT / build / "BUILD_RESULT.json"
    receipt = json.loads(receipt_path.read_bytes())
    source_pin, receipt_pin = pin(source), pin(receipt_path)
    assert receipt["status"] == "PASS_COMPILED_SCOPE" and receipt["boundary_unchanged"]
    assert all(run["exit_code"] == 0 for run in receipt["runs"]) and len(receipt["runs"]) == 2
    assert source_pin in receipt["sources"]
    assert all(set(row["axioms"]) <= TRIO for row in receipt["axiom_rows"])
    text = source.read_bytes().decode("utf-8")
    names = re.findall(r"(?m)^#print axioms (\w+)$", text)
    assert len(names) == len(set(names)) == len(receipt["axiom_rows"])
    logs = []
    for run in receipt["runs"]:
        log = OUT / build / (run["module"] + ".log")
        data = log.read_bytes()
        assert b"warning:" not in data and b"error:" not in data and b"sorryAx" not in data
        logs.append(pin(log))
    modules.append({"module": name, "source": source_pin, "receipt": receipt_pin,
                    "theorems": receipt["theorems"], "other_declarations": receipt["definitions"],
                    "axiom_audits": len(receipt["axiom_rows"]), "runs": len(receipt["runs"]),
                    "logs": logs, "leaf_and_importer_exit_zero": True, "zero_warnings": True,
                    "allowed_axioms_only": True})
    input_pins += [source_pin, receipt_pin] + logs
counts = {"modules": len(modules), "theorems": sum(x["theorems"] for x in modules),
          "other_declarations": sum(x["other_declarations"] for x in modules),
          "axiom_audits": sum(x["axiom_audits"] for x in modules)}
prior = BASE / "ESTABILIDADE_CARATER_GLOBAL_20260909_193729_5618013/NOTA_ESTABILIDADE_CARATER_GLOBAL.md"
note = f'''# Precisão operacional do caráter e controle por malha

[REAL — folhas compiladas] Três módulos novos: **{counts['theorems']} teoremas e {counts['other_declarations']} outras declarações**, {counts['axiom_audits']} auditorias de axiomas. Cada folha e seu importador terminaram com código0, sem avisos, somente com axiomas do trio permitido. A base é a biblioteca83 PASS; estas folhas ainda não foram integradas ao programa canônico. Todas as tentativas anteriores e backups permanecem guardados.

1. **`CharacterPrefixStability`** prova a cota |z_R−z_S|≤regularParameter(t)·2⁻ᴺ/2 quando os primeiros N bits coincidem. Define γ_N pelo mínimo dos gaps entre cada dígito e sua cauda, prova γ_N>0 para t≠0 e prova a recíproca quantitativa: |z_R−z_S|<γ_N implica o mesmo prefixo. Dois candidatos com erro≤ε frente à mesma leitura têm esse prefixo comum quando 2ε<γ_N. O último teorema liga isso diretamente aos cortes racionais de `recordBits` e `recordValue` em `SelectedGravitationalAtlas`.

2. **`FiniteCharacterResolution`** substitui o limiar com cauda infinita por uma expressão finita conservadora: δₙ=aₙ−2aₙ₊₁>0, onde aₙ=geometricContrast(t,n). O mínimo finito δ_N satisfaz 0<δ_N≤γ_N. Assim, proximidade inferior a δ_N resolve o prefixo, inclusive para candidatos ruidosos e cortes reais do registro. Para N≥1 o mínimo percorre n<N; N=0 usa a convenção do primeiro gap. O limiar contém somente um número finito de avaliações da expressão logarítmica canônica. Uma implementação numérica com arredondamento certificado não foi construída aqui.

3. **`RecordCharacterMeshControl`** usa pares de cortes racionais efetivamente dentro do prefixo resolvido para limitar o erro de valores amostrados por δ. Com uma malha finita de raio h e um limite espacial Lipschitz **uniforme L para os dois registros**, demonstra |recordValue_R(x,k)−recordValue_S(x,k)|≤δ+2Lh em todo o conjunto coberto. Isso vale para as26 componentes do registro:16 probabilidades geométricas e10 respostas. A malha, os cortes, seus índices e a regularidade são hipóteses explícitas. O teorema não recebe a desigualdade final como hipótese e não constrói uma solução gravitacional por fixar previamente g.

[OPEN — limites preservados] Esta é estabilidade quantitativa de dados do registro sob condições declaradas. Para transferir a estimativa às componentes métricas decodificadas, faltam margens uniformes das probabilidades em(0,1) e cotas do decoder; para inversas/curvatura, não degenerescência e regularidade dos jets. A origem física do registro, a lei de área e a compatibilidade com as mesmas medidas continuam assuntos distintos. Não se extrai um campo geral de um número de precisão finita sem essas condições.

A [obstrução por bumps suaves](<{prior.as_posix()}>) continua válida: a classe geral não tem o limite espacial uniforme necessário, e pode haver caracteres arbitrariamente próximos com métricas separadas num ponto. O resultado novo delimita condições suficientes e quantifica a recuperação permitida, sem transformar injetividade exata em estabilidade universal. O decoder clássico na imagem não foi substituído por um algoritmo para números ruidosos fora dela.

Nenhum `um.py` foi executado/importado. Originais e folhas PASS anteriores permaneceram intactos. Não houve publicação, atualização de gate, rodada física ou aprovação semântica independente atribuída nesta coleta.
'''
note_path = OUT / "NOTA_PRECISAO_OPERACIONAL.md"
new(note_path, note.encode("utf-8"))
assert all(pin(Path(x["path"])) == x for x in input_pins)
manifest = {"status": "THREE_FROZEN_LEAVES_PASS__NOT_INTEGRATED",
            "created_utc": datetime.now(timezone.utc).isoformat(), "modules": modules, "counts": counts,
            "note": pin(note_path), "previous_obstruction": pin(prior),
            "builder_provenance": pin(OUT / "BUILDER_PROVENANCE.json"),
            "configuration_prefix": pin(OUT / "CONFIG_BUILD.json"),
            "configuration_extensions": pin(OUT / "CONFIG_MESH.json"),
            "script": pin(Path(__file__).resolve()), "inputs_unchanged": True,
            "um_py_executed_or_imported": False, "originals_written": False,
            "independent_semantic_review": False, "joint_integration": False,
            "full_transitive_rebuild": False, "full_transitive_hash": False}
manifest_path = OUT / "MANIFESTO_PRECISAO_TRES_FOLHAS.json"
new(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"status": manifest["status"], "counts": counts, "note": pin(note_path),
                  "manifest": pin(manifest_path), "modules": [{"module": x["module"], "source": x["source"],
                  "receipt": x["receipt"]} for x in modules]}, ensure_ascii=False, indent=2))
