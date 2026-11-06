"""Offline regression across the provider SSE parser, tool batch and memory observer."""
import ast
from contextlib import nullcontext
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import threading
import time
from types import SimpleNamespace
from unittest.mock import Mock, patch

APP = Path("C:/IALD/projetos_pyhton/IALD")
HERE = Path(__file__).resolve().parent
PATCH = HERE.parent / "tool_batch.patch"
TARGET = "iald_app_providers.py"


def selected(source, names, namespace):
    """Compile actual definitions without importing the app, its clients or services."""
    body = [node for node in ast.parse(source).body if getattr(node, "name", None) in names]
    assert {node.name for node in body} == set(names)
    exec(compile(ast.Module(body=body, type_ignores=[]), "<offline-source>", "exec"), namespace)
    return namespace


def provider(source):
    stubs = SimpleNamespace(
        http_call=lambda label, send, *args, **kw: send(*args, **kw),
        project_messages=lambda messages: messages,
        call=lambda label, fn, *args: fn(*args),
        tool_result=Mock(),
    )
    ns = dict(json=json, threading=threading, time=time, Path=Path,
              MODELS={"mimo": dict(model="fixture", url="offline", output=16384, rates=(0, 0, 0))},
              router_media_view=SimpleNamespace(project_system_messages=lambda messages: messages),
              app_memory=stubs, adapter=lambda _: SimpleNamespace(load_mimo=lambda: "fixture"),
              contains_media=lambda _: False, encode_task_result=lambda r: json.dumps(r),
              TASK_TOOL_NAMES={"create_artifact"}, TOOL_NAMES=set(), WINDOW=1048576)
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            key = node.targets[0].id
            if key in {"MAX_TOOLS", "MAX_PARSED_TOOLS", "MAX_ROUNDS"}:
                ns[key] = ast.literal_eval(node.value)
    names = ["Evaluation", "ProtocolError", "scoped_task_names", "usage_cost", "check_window",
             "admission_input_bound", "output_budget", "transport_tool_options"]
    selected(source, names, ns)
    instance = ns["Evaluation"](HERE)
    instance.save = Mock()  # never open a metrics database
    return instance


def call(index, name="create_artifact", args="{}", call_id=None):
    return dict(index=index, id=f"id-{index}" if call_id is None else call_id,
                function=dict(name=name, arguments=args))


class Wire:
    status_code = 200

    def __init__(self, calls, done=True):
        self.calls, self.done = calls, done

    def iter_lines(self, **_):
        delta = {"content": "ok"} if self.calls is None else {"tool_calls": self.calls}
        choice = dict(delta=delta, finish_reason="stop" if self.calls is None else "tool_calls")
        data = dict(model="fixture", choices=[choice],
                    usage=dict(prompt_tokens=2, completion_tokens=1, total_tokens=3))
        yield b"data: " + json.dumps(data).encode()
        if self.done:
            yield b"data: [DONE]"

    def close(self):
        pass


def exercise(instance, calls, done=True, *, repeat_in_next_batch=False):
    replies = [Wire(calls, done)]
    if repeat_in_next_batch:
        replies.append(Wire(calls, done))
    send = Mock(side_effect=[*replies, Wire(None)])
    executor = Mock(return_value={"status": "fixture"})
    messages = [{"role": "user", "content": "fixture"}]
    record = {"calls": [], "first_text_seconds": None}
    tools = [{"type": "function", "function": {"name": "create_artifact"}}]
    error = None
    try:
        with patch.dict(sys.modules, {"requests": SimpleNamespace()}):
            instance._api("mimo", messages, tools, executor, lambda _: None, threading.Event(),
                          [], record, time.monotonic(), send, authorize=lambda: None,
                          task_tool_names=["create_artifact"])
    except ValueError as exc:
        error = getattr(exc, "code", type(exc).__name__)
    outputs = [m for m in messages if m.get("role") == "tool"]
    return dict(tool_effects=executor.call_count, simulated_model_calls=send.call_count, error=error,
                result_ids=[m["tool_call_id"] for m in outputs])


def batches(source):
    instance = provider(source)
    cases = {
        "late_invalid_json": [call(0), call(1, args="{")],
        "late_unoffered_name": [call(0), call(1, name="unoffered")],
        "late_missing_id": [call(0), call(1, call_id="")],
        "late_nonobject": [call(0), call(1, args="[]")],
        "duplicate_id": [call(0), call(1, call_id="id-0")],
        "valid_two": [call(0), call(1)],
        "valid_five": [call(i) for i in range(5)],
    }
    result = {name: exercise(instance, items) for name, items in cases.items()}
    result["missing_done"] = exercise(instance, [call(0)], done=False)
    return result


def observer_probe():
    source = (APP / "iald_app_memory.py").read_text(encoding="utf-8")
    observe = selected(source, ["observe_stream"], dict(json=json, canonical=json.dumps,
                       bound=lambda _: nullcontext(), ConfidentialContent=PermissionError))["observe_stream"]
    text = "medição β 🟡"
    data = dict(choices=[{"delta": {"content": text}}])
    event = "data: " + json.dumps(data, ensure_ascii=False)
    wire = (event + "\r\n\r\ndata: [DONE]\r\n\r\n").encode()

    def run(parts):
        binding = Mock(request_id="fixture")
        error = None
        try:
            returned = b"".join(observe(iter(parts), binding))
        except (ValueError, UnicodeError) as exc:
            returned, error = None, type(exc).__name__
        return dict(exact=returned == b"".join(parts), error=error,
                    complete=binding.finish.call_count == 1 and
                    binding.finish.call_args.args[0]["content"] == text,
                    uncertain=binding.uncertain.called)

    whole = run([wire])
    assert whole["exact"] and whole["complete"] and not whole["uncertain"]
    counts = {}
    for split in range(1, len(wire)):
        obs = run([wire[:split], wire[split:]])
        category = "correct" if obs == whole else obs["error"] or "lost_completion"
        counts[category] = counts.get(category, 0) + 1
    truncated = run([(event + "\r\n\r\n").encode()])
    assert truncated["uncertain"] and not truncated["complete"]
    return dict(bytes=len(wire), whole_frame=whole, all_two_chunk_splits=counts, no_done=truncated)


def signature_probe():
    source = (APP / "holographic_memory.py").read_text(encoding="utf-8")
    cls = next(n for n in ast.parse(source).body if getattr(n, "name", "") == "HolographicMemory")
    node = next(n for n in cls.body if getattr(n, "name", "") == "_sentence_signature")
    signature = selected(ast.get_source_segment(source, node), [node.name], dict(re=re))[node.name]
    prefix = "A" * 90
    pairs = {"decimal": ("Medida 1.25.", "Medida 9.50."), "suffix": (prefix + " ativo", prefix + " revogado"),
             "turn": ("Decisão do turno 17", "Decisão do turno 18"), "repeat": ("mesmo", "mesmo")}
    return {key: signature(None, a) == signature(None, b) for key, (a, b) in pairs.items()}


def main():
    original = (APP / TARGET).read_bytes()
    source = original.decode("utf-8")
    before = batches(source)
    with tempfile.TemporaryDirectory(dir=HERE) as scratch:
        scratch = Path(scratch)
        copy = scratch / TARGET
        copy.write_bytes(source.replace("\r\n", "\n").encode())
        # A disposable, independent directory. Never apply to the application.
        subprocess.run(["git", "apply", "--no-index", str(PATCH)], cwd=scratch, check=True,
                       env=dict(os.environ, GIT_CEILING_DIRECTORIES=str(HERE)))
        after = batches(copy.read_text(encoding="utf-8"))
    for key in ("late_invalid_json", "late_unoffered_name", "late_missing_id", "late_nonobject", "duplicate_id"):
        assert before[key]["tool_effects"] > 0
        assert after[key]["tool_effects"] == 0 and after[key]["error"]
        assert after[key]["simulated_model_calls"] == 1
    for key, count in (("valid_two", 2), ("valid_five", 4), ("missing_done", 0)):
        assert after[key] == before[key] and after[key]["tool_effects"] == count
    assert after["valid_five"]["result_ids"] == [f"id-{i}" for i in range(5)]
    assert after["missing_done"]["error"] == "incomplete_stream"
    result = dict(pins={f: hashlib.sha256((APP / f).read_bytes()).hexdigest() for f in
                        (TARGET, "iald_app_memory.py", "holographic_memory.py")},
                  patch_sha256=hashlib.sha256(PATCH.read_bytes()).hexdigest(),
                  before=before, after=after, observer=observer_probe(), signature_collision=signature_probe())
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

