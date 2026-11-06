"""Record the observed synthetic chat, matching only the authorized job and its metrics."""
from contextlib import closing
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
STATE = Path(r"C:\IALD\projetos_pyhton\IALD\.iald_runtime")
JOB = "4217a481-9af4-459b-ae71-f0ff4968c754"


def connect(name):
    db = sqlite3.connect((STATE / name).as_uri() + "?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    db.execute("pragma query_only=on")
    return closing(db)


def main():
    observation = json.load(sys.stdin)
    with connect("chat_jobs/jobs.sqlite3") as db:
        owner = hashlib.sha256(b"iald-chat-job:luiz").hexdigest()
        job = dict(db.execute("select id,status,created,updated from jobs where id=? and owner=?",
                              (JOB, owner)).fetchone())
    assert job["status"] in {"failed", "completed"}
    for key in ("created", "updated"):
        job[key] = datetime.fromtimestamp(job[key], timezone.utc).isoformat()
    with connect("app_evaluation/metrics.sqlite3") as db:
        metrics = db.execute("""select id,json_extract(data,'$.model') model,
            json_extract(data,'$.status') status,json_extract(data,'$.memory_sha256') memory_sha256,
            json_extract(data,'$.error_code') error_code,json_array_length(data,'$.calls') calls,
            json_extract(data,'$.elapsed_seconds') elapsed_seconds from turns
            where json_extract(data,'$.provider')='kimi' and julianday(json_extract(data,'$.utc'))
            between julianday(?) and julianday(?)""", (job["created"],job["updated"])).fetchall()
    overlay = WORK.parent / "iald_owner_notice_20261105" / "INSTALLED.json"
    assert json.loads(overlay.read_bytes())["status"] == "PASS"
    report = dict(observation, job=job, metrics_matched_by_time=[dict(x) for x in metrics],
                  observed_at=datetime.now().astimezone().isoformat(), model="Kimi K3 (assinatura)",
                  previous_terminal_refusal=str(HERE / "EVIDENCIA.json"), prior_job_retried=False,
                  backend_overlay=str(overlay), overlay_sha256=hashlib.sha256(overlay.read_bytes()).hexdigest(),
                  scope="Pergunta sintética no chat web autenticado. Medição de recuperação documental.",
                  release="v408")
    out = WORK / "NON_PAID_CHAT_VERIFICATION.json"
    with out.open("x", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(job["status"], len(metrics), out.name)


if __name__ == "__main__":
    main()
