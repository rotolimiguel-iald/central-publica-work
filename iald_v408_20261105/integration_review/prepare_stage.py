"""Prepare/check one isolated runtime candidate. Never install or contact a service."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
DESTINATION = Path("C:/IALD/projetos_pyhton/IALD/iald_app_providers.py")
STAGED = ROOT / "staged" / DESTINATION.name
PATCH = ROOT / "tool_batch.patch"
FIXTURE = ROOT / "fixtures" / "offline_review.py"
REFERENCE = ROOT.parent / "SESSION_REFERENCE.json"
PLAN = ROOT / "PATCH_PLAN.json"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def write_once(path, raw):
    path.parent.mkdir(exist_ok=True)
    if path.exists():
        require(path.read_bytes() == raw, f"Existing evidence differs: {path.name}")
        return
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
        temp = Path(tmp.name)
        tmp.write(raw)
        tmp.flush()
        os.fsync(tmp.fileno())
    try:
        require(temp.read_bytes() == raw, "Incomplete staging write")
        if os.name == "nt":
            os.rename(temp, path)  # Windows refuses an existing destination.
        else:
            os.link(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def evidence(path, data):
    write_once(path, (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode())


def check_exact_hunk(baseline, candidate):
    lines = PATCH.read_bytes().splitlines()
    header = re.fullmatch(rb"@@ -(\d+),(\d+) \+(\d+),(\d+) @@", lines[2])
    require(header is not None, "Expected one numbered diff hunk")
    first, old_count, new_first, new_count = map(int, header.groups())
    require(new_first == first, "Unexpected hunk offset")
    hunk = [line for line in lines[3:] if line]
    require(all(line[:1] in (b" ", b"-", b"+") for line in hunk), "Unexpected second hunk")
    old = [line[1:] + b"\r\n" for line in hunk if line[:1] != b"+"]
    new = [line[1:] + b"\r\n" for line in hunk if line[:1] != b"-"]
    original = baseline.splitlines(keepends=True)
    offset = first - 1
    require((len(old), len(new)) == (old_count, new_count), "Diff count mismatch")
    require(original[offset:offset + old_count] == old, "Hunk preimage mismatch")
    expected = b"".join(original[:offset] + new + original[offset + old_count:])
    require(candidate == expected, "Bytes outside the declared patch or line endings differ")


def main():
    spec = importlib.util.spec_from_file_location("offline_review", FIXTURE)
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    first = json.loads((ROOT / "RESULTADO.json").read_text(encoding="utf-8-sig"))
    baseline = DESTINATION.read_bytes()
    require(sha(baseline) == first["pins"][DESTINATION.name], "Baseline changed; re-review")
    require(sha(PATCH.read_bytes()) == first["patch_sha256"], "Patch drift")
    require(baseline.count(b"\r\n") == baseline.count(b"\n") > 0, "Recheck source line endings")
    with tempfile.TemporaryDirectory(dir=ROOT / "fixtures") as scratch:
        target = Path(scratch) / DESTINATION.name
        target.write_bytes(baseline.replace(b"\r\n", b"\n"))
        subprocess.run(["git", "apply", "--no-index", str(PATCH)], cwd=scratch, check=True,
                       env=dict(os.environ, GIT_CEILING_DIRECTORIES=str(ROOT / "fixtures")))
        patched_lf = target.read_bytes().replace(b"\r\n", b"\n")
        candidate = patched_lf.replace(b"\n", b"\r\n")
    check_exact_hunk(baseline, candidate)
    compile(candidate, str(STAGED), "exec")  # syntax only, no module initialization
    write_once(STAGED, candidate)
    staged = STAGED.read_bytes()
    before = fixture.batches(baseline.decode())
    after = fixture.batches(staged.decode())
    require(before == first["before"] and after == first["after"], "Eight-case regression failed")
    require(len(before) == len(after) == 8, "Unexpected regression inventory")
    reuse = fixture.exercise(fixture.provider(staged.decode()), [fixture.call(0)],
                             repeat_in_next_batch=True)
    require(reuse["error"] is None and reuse["tool_effects"] == 2
            and reuse["result_ids"] == ["id-0", "id-0"], "Unexpected cross-batch behavior")
    require(DESTINATION.read_bytes() == baseline, "Baseline changed during preparation")
    receipt = ROOT / "STAGED_TESTS.json"
    evidence(receipt, dict(status="PASS", cases=8, baseline=before, staged=after,
                           extra_scope_control=reuse, provider_fixture="mimo", network_calls=0,
                           sha256_baseline=sha(baseline), sha256_staged=sha(staged),
                           sha256_fixture=sha(FIXTURE.read_bytes()), sha256_patch=sha(PATCH.read_bytes()),
                           limits="Método Evaluation._api com SSE e executor sintéticos. ID único dentro de cada lote."))
    files = [dict(source=str(STAGED), destination=str(DESTINATION), baseline_sha256=sha(baseline),
                  sha256=sha(staged), bytes=len(staged), baseline_bytes=len(baseline),
                  exact_hunk_and_crlf_verified=True)]
    data = dict(schema="iald.integration-review.operational-patch.v1", status="PREPARED_OFFLINE",
                authority_reference=str(REFERENCE), authority_sha256=sha(REFERENCE.read_bytes()),
                purpose="Validar todo o lote de ferramentas antes da primeira execução.",
                files=files, patch=dict(path=str(PATCH), sha256=sha(PATCH.read_bytes())),
                tests=dict(path=str(receipt), sha256=sha(receipt.read_bytes()), cases=8,
                           extra="Mesmo ID em dois lotes sucessivos da mesma solicitação."),
                recipe=dict(path=str(Path(__file__).resolve()), sha256=sha(Path(__file__).read_bytes()),
                            fixture_path=str(FIXTURE), fixture_sha256=sha(FIXTURE.read_bytes()),
                            command='C:\\Python314\\python.exe -I -B -X utf8 "' + str(Path(__file__).resolve()) + '"'),
                integration=["Revisão independente do patch e dos testes antes da troca.",
                             "Na janela controlada da entrega, conferir destino fixo e SHA256 da baseline antes de escrever. Divergência exige nova revisão.",
                             "Conferir pinos do staged, patch e testes. Backup de bytes no destino, verificar, substituir de forma atômica e conferir SHA256 final.",
                             "Registrar o arquivo e a verificação de carregamento em recibo operacional próprio. Para reverter, conferir o pino do staged instalado e o da cópia original."],
                scope="Um módulo Python de backend. Deduplicação no lote atual. Falhas durante a execução de ferramentas válidas podem produzir efeitos parciais.")
    evidence(PLAN, data)
    print(json.dumps(dict(plan=str(PLAN), sha256_plan=sha(PLAN.read_bytes()), files=files, tests=8,
                          extra_scope=reuse, patched_live=False), ensure_ascii=False))


if __name__ == "__main__":
    main()

