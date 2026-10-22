"""Record the actual incremental verification scope in our unexecuted reporter."""
from pathlib import Path
from datetime import datetime
import os

folder = Path(__file__).resolve().parent
path = folder / "finalize_reexamination.py"
assert folder.parent == Path(r"C:\IALD\Central de Patentes\Chatgpt")
before = path.read_bytes()
backup = path.with_name(path.name + ".bak_" + datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
with backup.open("xb") as stream:
    stream.write(before)
    stream.flush()
    os.fsync(stream.fileno())
assert backup.read_bytes() == before
text = before.decode("utf-8")
changes = [
    ('    assert len(result["runs"]) == total["modules"] + 3',
     '''    cached = result["cached_modules"]
    assert len(cached) + fresh["modules"] == total["modules"]
    assert result["cached_boundary_unchanged"]
    cached_receipt_path = Path(result["cached_build_receipt"]["path"])
    assert record(cached_receipt_path) == result["cached_build_receipt"]
    prior_build = read(cached_receipt_path)
    assert prior_build["status"] == "PASS_TRANSPOSED_SCOPE"
    assert len(prior_build["runs"]) == len(cached) + 3
    assert all(run["valid"] and run["exit_code"] == 0 and run["warning_lines"] == 0
               for run in prior_build["runs"])
    assert all(module["source_bytes_identical"] and module["prior_run"]["valid"]
               and module["prior_run"]["exit_code"] == 0 for module in cached)
    assert len(result["runs"]) == fresh["modules"] + 3
    new_names = {run["module"] for run in result["runs"][:-3]}
    cached_names = {module["module"] for module in cached}
    assert not new_names & cached_names
    assert new_names | cached_names == {module["module"] for module in integration["modules"]}'''),
    ("incluindo os {total['modules']} módulos transpostos, a raiz TGLExt e as duas auditorias.",
     "incluindo os {fresh['modules']} módulos novos transpostos, a raiz TGLExt e as duas auditorias. Os {len(cached)} módulos anteriores foram reutilizados do build aprovado de {len(prior_build['runs'])} processos, após comparação exata das fontes e dos pins de dependência. A raiz e a auditoria dedicada carregam os {total['modules']} módulos juntos; a auditoria dedicada verifica todas as {total['theorems'] + total['other_declarations']} declarações, incluindo as instâncias nomeadas."),
    ("Esta verificação usa as fontes novas transpostas e cópias de bytes de dependências locais, com os binários Mathlib existentes.",
     "Esta verificação incremental usa as fontes novas transpostas e cópias de bytes de dependências locais, com os binários Mathlib existentes. Os hashes dos binários das 45 folhas reaproveitadas foram medidos na reutilização; o recibo anterior certificava as execuções e fontes, mas não fixava hashes dos binários produzidos. As fronteiras de entrada e as cópias reutilizadas foram conferidas antes e depois. A tentativa sequencial inicial foi interrompida para esta reutilização e permanece preservada, sem ser contada como um build conjunto concluído."),
    ('    evidence = [report_path, result_path, integration_path, audit_path,',
     '    evidence = [report_path, result_path, integration_path, audit_path, cached_receipt_path,'),
    ('        "processes_passed": len(result["runs"]), "warnings": 0,',
     '        "processes_passed": len(result["runs"]), "warnings": 0,\n        "fresh_leaf_modules_compiled": fresh["modules"], "cached_leaf_modules": len(cached),\n        "cached_build_processes_passed": len(prior_build["runs"]),'),
    ("Build conjunto: {len(result['runs'])} processos PASS, zero avisos.",
     "Build incremental: {len(result['runs'])} processos novos PASS, zero avisos; {len(cached)} folhas anteriores reutilizadas com fontes idênticas. A raiz e as auditorias carregam todos os {total['modules']} módulos."),
]
for old, new in changes:
    assert text.count(old) == 1, old
    text = text.replace(old, new)
after = text.encode("utf-8")
assert len(after) > len(before)
compile(text, str(path), "exec")
temp = path.with_name(path.name + ".tmp_" + datetime.now().strftime("%H%M%S_%f"))
with temp.open("xb") as stream:
    stream.write(after)
    stream.flush()
    os.fsync(stream.fileno())
assert temp.read_bytes() == after
assert path.read_bytes() == before
os.replace(temp, path)
assert path.read_bytes() == after
print("Reporter now requires 18 fresh modules, 45 verified cached leaves and three new aggregate processes.")
