"""Correct pre-seal052 documentary metadata and refresh the delivery hashes."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, re

ROOT = Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def revise(path, raw, stamp):
    old = path.read_bytes()
    assert old and raw and raw != old
    backup = path.with_name(path.name + ".bak_" + stamp)
    with backup.open("xb") as stream:
        stream.write(old)
        stream.flush()
        os.fsync(stream.fileno())
    assert backup.read_bytes() == old
    temporary = path.with_name(path.name + ".tmp_" + stamp)
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == raw and path.read_bytes() == old
    os.replace(temporary, path)
    assert path.read_bytes() == raw and backup.read_bytes() == old

def main():
    assert not (ROOT / "CONTINUACAO052_MANIFESTO.json").exists()
    auditor = ROOT / "audit_continuation052.py"
    review = ROOT / "CONTINUACAO052_REVISAO_INDEPENDENTE.md"
    report = ROOT / "CONTINUACAO052_PARECER.md"
    delivery = ROOT / "TUNEL/DO_CHATGPT/ENTREGA_052_setor_horizontal_e_area.md"
    atext = auditor.read_text(encoding="utf-8")
    ast.parse(atext)
    assert "Finite optical balance, Riccati invariants" not in atext
    assert digest(auditor) in review.read_text(encoding="utf-8")
    old_delivery = delivery.read_text(encoding="utf-8")
    pattern = re.compile(r"\| \[[^\]]+\]\(<([^>]+)>\) \| (\d+) \| ([a-f0-9]{64}) \|")
    matches = list(pattern.finditer(old_delivery))
    assert len(matches) == 19
    paths = [Path(m.group(1)) for m in matches]
    assert len(set(paths)) == 19
    for match, path in zip(matches, paths):
        assert path.resolve().is_relative_to(ROOT)
        if path not in {auditor, review}:
            assert path.stat().st_size == int(match.group(2))
            assert digest(path) == match.group(3)
    timestamp = datetime.now(timezone.utc)
    stamp = timestamp.strftime("%Y%m%d_%H%M%S_%f")
    note = (
        "\n\n## Adendo documental antes do selo052\n\n"
        "[REAL — correção de metadados] UTC: " + timestamp.isoformat() + ". "
        "A primeira tentativa de selagem foi interrompida antes da criação do manifesto ou de seu temporário: "
        "o auditor ainda continha a descrição de escopo e quatro limitações herdadas da051. "
        "Foram corrigidas somente essas strings, sem alteração da lógica de auditoria, das fontes Lean, "
        "do runner ou do build. A revisão independente registra o achado e a correção ao lado. "
        "Os documentos anteriores permanecem em backups exatos de bytes; os hashes da entrega foram atualizados.\n\n"
        "Auditor corrigido SHA256: " + digest(auditor) + "\n\n"
        "Revisão atualizada SHA256: " + digest(review) + "\n"
    )
    old_report = report.read_bytes()
    assert b"Adendo documental antes do selo052" not in old_report
    revise(report, old_report + note.encode("utf-8"), stamp)
    paths.append(Path(__file__).resolve())
    rows = ["| [" + path.name + "](<" + path.as_posix() + ">) | "
            + str(path.stat().st_size) + " | " + digest(path) + " |" for path in paths]
    updated = (old_delivery[:matches[0].start()] + "\n".join(rows)
               + old_delivery[matches[-1].end():] + note)
    revise(delivery, updated.encode("utf-8"), stamp)
    final_matches = list(pattern.finditer(delivery.read_text(encoding="utf-8")))
    assert len(final_matches) == 20
    for match in final_matches:
        path = Path(match.group(1))
        assert path.stat().st_size == int(match.group(2)) and digest(path) == match.group(3)
    print(json.dumps({"status": "DOCUMENTARY_CORRECTION_PASS", "artifact_rows": 20,
        "report_bytes": report.stat().st_size, "report_sha256": digest(report),
        "delivery_bytes": delivery.stat().st_size, "delivery_sha256": digest(delivery)}))

if __name__ == "__main__":
    main()
