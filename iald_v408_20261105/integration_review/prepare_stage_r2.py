"""Reproduce both offline regressions and issue a staging-only plan."""
import contextlib
import io
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
APP = Path("C:/IALD/projetos_pyhton/IALD")
FIXTURES = ROOT / "fixtures"
R1 = runpy.run_path(str(ROOT / "prepare_stage.py"))
sha, require = R1["sha"], R1["require"]
write_once, evidence = R1["write_once"], R1["evidence"]


def pin(path):
    return {"path": str(path), "sha256": sha(path.read_bytes())}


def main():
    require(__debug__ and sys.dont_write_bytecode, "Run without optimization and with -B")
    first_plan = ROOT / "PATCH_PLAN.json"
    r1 = json.loads(first_plan.read_bytes())
    reference = ROOT.parent / "SESSION_REFERENCE.json"
    require(sha(reference.read_bytes()) == r1["authority_sha256"], "Authority reference changed")
    # The original recipe verifies the whole first hunk and runs the original
    # eight cases against both files, plus the separate cross-round ID control.
    with contextlib.redirect_stdout(io.StringIO()):
        R1["main"]()
    path = APP / "iald_app_memory.py"
    original = path.read_bytes()
    first_measure = json.loads((ROOT / "RESULTADO.json").read_text(encoding="utf-8-sig"))
    require(sha(original) == first_measure["pins"][path.name], "Memory baseline changed")
    require(b"\r" not in original, "Review the original line endings")
    staged = ROOT / "staged" / path.name
    diff = ROOT / "observe_stream.patch"
    with tempfile.TemporaryDirectory(dir=FIXTURES) as scratch:
        temp = Path(scratch) / path.name
        temp.write_bytes(original)
        subprocess.run(["git", "-c", "core.autocrlf=false", "apply", "--no-index", str(diff)],
                       cwd=scratch, check=True, env=dict(os.environ, GIT_CEILING_DIRECTORIES=str(FIXTURES)))
        candidate = temp.read_bytes()
    require(b"\r" not in candidate, "Unexpected line-ending drift")
    compile(candidate, str(staged), "exec")
    write_once(staged, candidate)
    probe = FIXTURES / "stream_cases.py"
    counts = runpy.run_path(str(probe))["run"](staged)
    receipt = ROOT / "STAGED_TESTS_R2.json"
    results = dict(status="PASS", provider_batch_tests=pin(ROOT / "STAGED_TESTS.json"),
                   original_measurement=pin(ROOT / "RESULTADO.json"), stream_fixture=pin(probe),
                   observer_cases=counts, observer_total=sum(counts.values()),
                   observer_baseline_sha256=sha(original), observer_staged_sha256=sha(staged.read_bytes()),
                   observer_patch=pin(diff), network_calls=0, installation=False,
                   coverage="Métodos extraídos das fontes e bindings sintéticos; identidade dos objetos entregues verificada.")
    files = [dict(r1["files"][0], patch=r1["patch"]),
             dict(source=str(staged), destination=str(path), baseline_sha256=sha(original),
                  sha256=sha(candidate), baseline_bytes=len(original), bytes=len(candidate), patch=pin(diff))]
    for entry in files:
        require(sha(Path(entry["destination"]).read_bytes()) == entry["baseline_sha256"], "Destination drift")
        require(sha(Path(entry["source"]).read_bytes()) == entry["sha256"], "Staging drift")
    evidence(receipt, results)
    plan_path = ROOT / "PATCH_PLAN_R2.json"
    plan = dict(schema="iald.integration-review.operational-patch.v2", status="PREPARED_OFFLINE",
                authority_reference=pin(reference), parent_plan=pin(first_plan),
                files=files, tests=pin(receipt), recipe=pin(Path(__file__).resolve()),
                command='C:\\Python314\\python.exe -I -B -X utf8 "' + str(Path(__file__).resolve()) + '"',
                limits=["ID único apenas dentro de um lote de ferramentas.",
                        "Observador de uma resposta: encaminha cada objeto original; recusa/ausência de terminador impede concluir; uma conclusão por fluxo.",
                        "Sem medição de latência, custo, tráfego de produção ou inferência."],
                integration=["Revisar os dois diffs separadamente. Este plano é operacional e não integra o plano científico.",
                             "Na mesma janela controlada, conferir TODOS os destinos e baselines antes da primeira substituição. Divergência interrompe a instalação.",
                             "Guardar e conferir os dois backups de bytes; instalar atomicamente por destino e conferir ambos os hashes antes de liberar o serviço.",
                             "Se a segunda troca falhar, reverter somente arquivos já trocados que ainda tenham o pino staged e conferir as duas baselines; manter a janela até reconciliar.",
                             "Verificar o processo efetivamente carregado em recibo próprio da integração."])
    evidence(plan_path, plan)
    print(json.dumps(dict(plan=pin(plan_path), observer_cases=results["observer_total"],
                          batch_cases=8, extra_scope_control=1, files=files), ensure_ascii=False))


if __name__ == "__main__":
    main()

