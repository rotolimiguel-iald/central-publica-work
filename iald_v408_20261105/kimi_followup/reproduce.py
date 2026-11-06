"""Public Kimi v408 incident. Read-only metadata and offline worker regression."""
import ast
from contextlib import closing
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import queue
import sqlite3
import sys
import threading
import time
from types import SimpleNamespace
from unittest.mock import Mock, patch
import uuid

HERE = Path(__file__).resolve().parent
WORK = HERE.parent
APP = Path("C:/IALD/projetos_pyhton/IALD")
MODULE = "iald_app_providers.py"
JOB = "f1c1c585-1570-45ec-bebe-bd8261a07bbd"
TURN = "1f322121ac944cce9dd630f535a6c02d"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def metadata():
    def connect(name):
        uri = (APP / ".iald_runtime" / name).as_uri() + "?mode=ro"
        db = sqlite3.connect(uri, uri=True)
        db.row_factory = sqlite3.Row
        db.execute("pragma query_only=on")
        return closing(db)

    with connect("chat_jobs/jobs.sqlite3") as db:
        row = db.execute("select id,status,created,updated,cancel_requested,seq from jobs where id=? and owner=?",
                         (JOB, sha(b"iald-chat-job:luiz"))).fetchone()
        assert row and row["status"] == "failed"
        job = dict(row)
    for field in ("created", "updated"):
        job[field] = datetime.fromtimestamp(job[field], timezone.utc).isoformat()
    with connect("app_evaluation/metrics.sqlite3") as db:
        rows = db.execute("""select id,json_extract(data,'$.utc') utc,
          json_extract(data,'$.memory_sha256') prefix_sha256,json_extract(data,'$.model') model,
          json_extract(data,'$.status') status,json_extract(data,'$.error_type') error_type,
          json_extract(data,'$.error_code') error_code,json_extract(data,'$.elapsed_seconds') elapsed,
          json_array_length(data,'$.calls') calls,json_extract(data,'$.first_text_seconds') first_text
          from turns where json_extract(data,'$.provider')='kimi'
          and julianday(json_extract(data,'$.utc')) between julianday(?) and julianday(?) limit 2""",
                          (job["created"], job["updated"])).fetchall()
        assert len(rows) == 1 and rows[0]["id"] == TURN and rows[0]["calls"] == 0
        assert rows[0]["error_type"] == "ValueError" and rows[0]["error_code"] == "transport_or_unclassified"
        return job, dict(rows[0])


def worker(path, messages, expected_prompt):
    """Run the real stream worker with in-memory save/projection/wallet and fake CLI."""
    source = path.read_bytes()
    tree = ast.parse(source)
    names = {"Evaluation", "ProtocolError", "sse", "usage_cost", "check_window", "admission_input_bound",
             "scoped_task_names"}
    constants = {"WINDOW", "MODELS", "TOOL_NAMES"}
    nodes = [n for n in tree.body if getattr(n, "name", "") in names or
             isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in constants]
    execute = Mock(return_value={"text": "OK", "usage": dict(prompt_tokens=1, completion_tokens=1, total_tokens=2)})
    ns = dict(Path=Path, json=json, uuid=uuid, threading=threading, queue=queue, time=time,
              datetime=datetime, timezone=timezone, TASK_TOOL_NAMES=set(), reject_worker_media=lambda *a, **k: None,
              contains_refs=lambda _: False, routing_metrics=SimpleNamespace(stamp=lambda *a: None),
              router_media_view=SimpleNamespace(project_system_messages=lambda m: m),
              app_memory=SimpleNamespace(project_messages=lambda m: m, thread_target=lambda f: f,
                                         call=lambda label, f, *a, **kw: f(*a, **kw)),
              adapter=lambda name: SimpleNamespace(execute=execute),
              wallet_runtime=SimpleNamespace(threaded=lambda f: (f, lambda: None),
                                             subscription_begin=lambda _: "synthetic", subscription_end=lambda _: None))
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), "exec"), ns)
    engine = ns["Evaluation"](HERE)
    records = []
    engine.save = lambda r: records.append(deepcopy(r))
    with patch.dict(sys.modules, {"iald_orcamento": SimpleNamespace(BudgetError=type("BudgetError", (Exception,), {}))}):
        list(engine.stream("kimi", messages, [], None, memory_sha256="synthetic"))
    if execute.called:
        assert execute.call_count == 1 and execute.call_args.args == (expected_prompt,)
    rec = records[-1]
    return dict(status=rec["status"], error_type=rec.get("error_type"), error_code=rec.get("error_code"),
                calls_marked=len(rec["calls"]), fake_cli_entries=execute.call_count)


def serialize(messages):
    return json.dumps(dict(instructions=messages[0]["content"], conversation=messages[1:]), ensure_ascii=False)


def main():
    assert __debug__
    job, turn = metadata()
    public = (WORK / "app/packages/shared/prefix.md").read_bytes()
    assert sha(public) == turn["prefix_sha256"]
    science = public.decode("utf-8")
    cap = 1048576 - 131072 - 4096
    raw_min = serialize([dict(role="system", content=science)])
    original, candidate = APP / MODULE, HERE / "staged" / MODULE
    cases = {}
    def measure(label, messages, expect_before, expect_after):
        prompt = serialize(messages)
        old = worker(original, messages, prompt)
        new = worker(candidate, messages, prompt)
        assert old["fake_cli_entries"] == expect_before and new["fake_cli_entries"] == expect_after
        for value in (old, new):
            assert value["calls_marked"] == value["fake_cli_entries"]
            assert value["status"] == ("completed" if value["fake_cli_entries"] else "failed_or_uncertain")
        cases[label] = dict(cli_bytes=len(prompt.encode()), wrapper_bytes=len(json.dumps({"prompt": prompt}, ensure_ascii=False).encode()),
                            before=old, after=new)
    messages = [dict(role="system",content=science),dict(role="user",content="Qual é a versão pública?")]
    measure("public_prefix_synthetic_question",messages,0,1)
    small = [dict(role="system",content="fixture"),dict(role="user",content="β")]
    measure("short",small,1,1)
    small[-1]["content"] += "a" * (cap-len(serialize(small).encode()))
    assert len(serialize(small).encode()) == cap
    measure("exact_limit",small,0,1)
    small[-1]["content"] += "x"
    measure("one_byte_over",small,0,0)
    assert cases["one_byte_over"]["after"]["error_code"] == "kimi_cli_input_envelope_exceeded"
    print(json.dumps(dict(author="Codex, subagente de diagnóstico Kimi", job=job, evaluation=turn,
        correlation="Única avaliação Kimi iniciada no intervalo do job; sem chave estrangeira comum.",
        immutable_prefix_bytes=len(public), input_limit_bytes=cap, minimum_cli_bytes=len(raw_min.encode()),
        minimum_legacy_bytes=len(json.dumps({"prompt":raw_min},ensure_ascii=False).encode()), cases=cases,
        source=str(candidate), destination=str(original), baseline_sha256=sha(original.read_bytes()),
        staged_sha256=sha(candidate.read_bytes()), patch_sha256=sha((HERE/"kimi_cli_input.patch").read_bytes()),
        fixture_sha256=sha(Path(__file__).read_bytes()), real_provider_calls=0, deployed=False), ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()

