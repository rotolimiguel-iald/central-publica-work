"""Local contract tests for observe_stream. All sources and bindings are synthetic."""
import ast
import codecs
from contextlib import contextmanager
from contextvars import ContextVar
import json
from pathlib import Path
import re


class FixtureRefusal(Exception):
    rules = ["synthetic"]
    text_sha16 = "fixture"
    where = "fixture"


def load_observer(path):
    source = Path(path).read_bytes()
    names = {"bound", "current", "canonical", "_record_refusal", "observe_stream"}
    body = [n for n in ast.parse(source).body if getattr(n, "name", "") in names]
    assert {n.name for n in body} == names
    ns = dict(json=json, re=re, codecs=codecs, ConfidentialContent=FixtureRefusal,
              contextmanager=contextmanager, _CURRENT=ContextVar("fixture", default=None))
    exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"), ns)
    return ns


class Binding:
    def __init__(self, request_id="synthetic", *, reject=False):
        self.request_id = request_id
        self.rows, self.finishes, self.uncertain_count = [], [], 0
        self.reject = reject

    def append(self, label, text, **meta):
        if self.reject and label == "response":
            raise FixtureRefusal()
        self.rows.append((label, text, meta))

    def finish(self, value):
        self.finishes.append(value)

    def uncertain(self):
        self.uncertain_count += 1


def event(value, sep="\n"):
    data = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return "data: " + data + sep + sep


def content(text):
    return {"choices": [{"delta": {"content": text}}]}


def stream(ns, parts, binding, closed):
    def source():
        try:
            for part in parts:
                assert ns["current"]() is binding
                yield part
        finally:
            assert ns["current"]() is binding
            closed.append(binding.request_id)
    return ns["observe_stream"](source(), binding)


def consume(ns, parts, *, binding=None, error=None, cancel_after=None):
    binding = binding or Binding()
    closed, output = [], []
    flow = stream(ns, parts, binding, closed)
    try:
        for piece in flow:
            assert piece is parts[len(output)]  # type, identity, bytes and boundaries
            output.append(piece)
            assert ns["current"]() is None
            if cancel_after == len(output):
                break
        assert error is None, "Expected a visible failure"
    except (UnicodeDecodeError, ValueError, TypeError) as exc:
        if error is None or not isinstance(exc, error):
            raise
    finally:
        flow.close()
    if error is None:
        assert len(output) == (len(parts) if cancel_after is None else cancel_after)
    assert closed == [binding.request_id] and ns["current"]() is None
    return binding


def completed(binding, expected):
    assert [row[0] for row in binding.rows] == ["response"]
    assert binding.rows[0][1] == expected
    assert binding.finishes == [{"content": expected, "status": "DECLARADO"}]
    assert binding.uncertain_count == 0


def uncertain(binding, *, label="response_uncertain", partial=None):
    assert not binding.finishes and binding.uncertain_count == 1
    assert [row[0] for row in binding.rows] == [label]
    if partial is not None:
        value = json.loads(binding.rows[0][1])
        assert value["partial_response"] == partial and value["automatic_retry"] is False


def run(path):
    ns = load_observer(path)
    text = "medição β 🟡"
    done = event("[DONE]")
    frame = event(content(text))
    counts = {}

    for name, sep in (("LF", "\n"), ("CRLF", "\r\n")):
        wire = (event(content(text), sep) + event("[DONE]", sep)).encode()
        for cut in range(1, len(wire)):
            completed(consume(ns, [wire[:cut], wire[cut:]]), text)
        counts["all_single_cuts_" + name] = len(wire) - 1
        completed(consume(ns, [bytes((b,)) for b in wire]), text)
        counts["one_byte_at_a_time_" + name] = 1

    # The native proxy uses iter_content(256). Align an actual multi-byte scalar.
    prefix = event(content("|")).index("|")
    aligned = "a" * (255 - prefix) + "β"
    raw = (event(content(aligned)) + done).encode()
    assert raw[255:257] == "β".encode()
    completed(consume(ns, [raw[:256], raw[256:]]), aligned)
    counts["native_256_boundary"] = 1

    end = done.encode()
    completed(consume(ns, [frame[:4], frame[4:].encode(), "", b"", done]), text)
    completed(consume(ns, [frame[:4].encode(), frame[4:], end]), text)
    completed(consume(ns, [frame, "data: [DONE]\r", "\n\r".encode(), "\n"]), text)
    counts["mixed_valid"] = 3
    start, tail = frame.encode().split("β".encode())
    completed(consume(ns, [start + b"\xce", "", b"\xb2" + tail, done]), text)
    counts["empty_text_inside_pending_bytes"] = 1
    uncertain(consume(ns, [start + b"\xce", "intervening"], error=ValueError), partial="")
    uncertain(consume(ns, [frame, b"\xff"], error=UnicodeDecodeError), partial=text)
    uncertain(consume(ns, [frame, b"\xf0\x9f"], error=UnicodeDecodeError), partial=text)
    counts["invalid_mixed_or_utf8"] = 3

    for parts in ([frame], [frame, done.rstrip("\n")], [frame, "data: [DONE]\r\n\r"]):
        uncertain(consume(ns, parts), partial=text)
    counts["unterminated"] = 3
    for refusal in ({"iald_aviso": {"tipo": "falha_motor"}}, {"error": "fixture"}):
        uncertain(consume(ns, [frame, event(refusal), done]), label="response_refused")
    uncertain(consume(ns, [done]), label="response_refused")
    uncertain(consume(ns, [frame, done], binding=Binding(reject=True)), label="refused.response")
    counts["typed_refusal_empty_or_store_refusal"] = 4

    uncertain(consume(ns, [frame, done], cancel_after=1), partial=text)
    completed(consume(ns, [frame, done, ":keepalive\n\n"], cancel_after=2), text)
    counts["cancel_before_and_after_done"] = 2
    completed(consume(ns, [frame + done + event(content("second")) + done]), text)
    completed(consume(ns, [frame, done, event(content("second")), done]), text)
    counts["duplicate_done_and_tail"] = 2

    alternatives = {"choices": [{"index": i, "delta": {"content": str(i)}} for i in (0, 1)]}
    uncertain(consume(ns, [event(alternatives), done]), label="response_refused")
    other = {"choices": [alternatives["choices"][1]]}
    uncertain(consume(ns, [frame, event(other), done]), label="response_refused")
    counts["alternatives_never_joined"] = 2

    # Two suspended generators on one thread; inspect identity at every boundary.
    a, b = Binding("one"), Binding("two")
    closed = []
    one, two = event(content("A")), event(content("B"))
    fa = stream(ns, [one, done], a, closed)
    fb = stream(ns, [two, done], b, closed)
    try:
        for flow, part in ((fa, one), (fb, two), (fa, done), (fb, done)):
            assert next(flow) is part and ns["current"]() is None
        completed(a, "A")
        completed(b, "B")
    finally:
        fa.close()
        fb.close()
    assert closed == ["one", "two"] and ns["current"]() is None
    counts["interleaved_bindings"] = 1
    return counts

