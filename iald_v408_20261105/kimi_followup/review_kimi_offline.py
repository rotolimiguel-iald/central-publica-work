"""Independent offline review. Run with python -B -X utf8. No application/queue startup."""
import ast
import copy
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from datetime import datetime, timezone
from types import ModuleType, SimpleNamespace as NS
from unittest.mock import patch
import uuid
from urllib.parse import urlparse

W = Path(__file__).resolve().parent
APP = Path(r"C:\IALD\projetos_pyhton\IALD")
ADAPTER = Path(r"C:\IALD\Central de Patentes\Chatgpt\IALD_ORQUESTRACAO_20260923\iald_orchestrator")
CAND = W / "staged/iald_app_providers.py"
INST = APP / CAND.name
WEB = APP / "iald_web_server.py"
KIMI = ADAPTER / "kimi.py"
LAUNCH = ADAPTER / "kimi_stdin.mjs"
MEM = APP / "iald_app_memory.py"
PREFIX = APP / ".iald_runtime/haiku/prefix.md"
E = json.loads((W/"EVIDENCIA.json").read_bytes())
CAP = 1048576 - 131072 - 4096


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path):
    return digest(path.read_bytes())


def selected(path, names, **env):
    tree = ast.parse(path.read_bytes())
    nodes = [n for n in tree.body if getattr(n, "name", None) in names or
             isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in names]
    exec(compile(ast.Module(nodes, []), str(path), "exec"), env)
    return env


def encode(obj):
    return json.dumps(obj, ensure_ascii=False).encode("utf-8")


def definitions():
    public = selected(WEB, {"PUBLIC_TOOLS"})["PUBLIC_TOOLS"]
    memory = selected(MEM, {"tool_definitions"})["tool_definitions"]()
    result = []
    for module in ("iald_kernel.py", "iald_core_indexado.py", "iald_fontes_publicas.py"):
        src = APP / module
        funcs = selected(src, {"tool_definitions", "catalog"}, __file__=str(src), Path=Path, json=json, urlparse=urlparse)
        result.extend(funcs["tool_definitions"]())
    allowed = selected(CAND, {"TOOL_NAMES"})["TOOL_NAMES"]
    tools = {t["function"]["name"]: t for t in result + public + memory if t["function"]["name"] in allowed}
    return list(tools.values())


def transport(folder, prompt):
    # Run the real adapter's execute() and real launcher, with a stand-in for the
    # official CLI entry. Only the disposable process below can be started.
    folder.mkdir()
    scripts = folder / "iald_orchestrator"
    scripts.mkdir()
    (folder / "state").mkdir()
    shutil.copyfile(LAUNCH, scripts/LAUNCH.name)
    probe = scripts/"observe.mjs"
    probe.write_text("""
import fs from 'node:fs'; import {syncBuiltinESMExports} from 'node:module';
import {createHash} from 'node:crypto';
const read = fs.readFileSync;
fs.readFileSync = function(fd, ...args) {
 if (fd !== 0) return read.call(this, fd, ...args);
 const b = read.call(this, fd);
 globalThis.wire = [b.length, createHash('sha256').update(b).digest('hex')];
 return b.toString('utf8');
};
syncBuiltinESMExports(); await import('./kimi_stdin.mjs');
""", encoding="utf-8")
    entry = folder/"clients/node_modules/@moonshot-ai/kimi-code/dist/main.mjs"
    entry.parent.mkdir(parents=True)
    entry.write_text("""
import {createHash} from 'node:crypto';
const arg=process.argv[process.argv.indexOf('-p')+1]; const b=Buffer.from(arg,'utf8');
const text=JSON.stringify({wire:globalThis.wire, cli:[b.length,createHash('sha256').update(b).digest('hex')]});
console.log(JSON.stringify({type:'system.version',version:'2.0.2'}));
console.log(JSON.stringify({role:'assistant',content:text}));
console.log(JSON.stringify({type:'session.resume_hint',session_id:'session_00000000-0000-0000-0000-000000000000'}));
""", encoding="utf-8")
    profile = folder/"dummy"
    provider_stub = ModuleType("probe.providers")
    provider_stub.ProviderLimitError = RuntimeError
    node = shutil.which("node.exe")
    assert node
    provider_stub.client_command = lambda name: [node]
    limited_env = {"SystemRoot": os.environ["SystemRoot"], "KIMI_CODE_HOME": str(profile)}
    import re
    env = selected(KIMI, {"execute", "parse_stdout", "MODEL", "CONTEXT_WINDOW", "OUTPUT_RESERVE",
                           "MAX_INPUT_BYTES", "MAX_RESPONSE_BYTES"}, __package__="probe", json=json, time=time,
                   re=re, Path=Path, subprocess=subprocess, tempfile=tempfile, LAUNCHER=probe, BASE=folder,
                   PROFILE=profile, client_environment=lambda _: limited_env.copy(), preflight=lambda: None,
                   session_evidence=lambda _: {})
    assert env["MAX_INPUT_BYTES"] == CAP
    with patch.dict(sys.modules, {"probe.providers": provider_stub}):
        result = json.loads(env["execute"](prompt)["text"])
    assert result["wire"] == [len(encode(prompt)), digest(encode(prompt))]
    assert result["cli"] == [len(prompt.encode()), digest(prompt.encode())]
    return result


def worker(path, messages, projection, deny=None):
    trace = []
    captured = []
    records = []

    def allow():
        trace.append("authorize")
        if deny == "authorize":
            raise PermissionError("Synthetic revocation")

    def begin(model):
        trace.append("subscription_begin")
        if deny == "wallet":
            raise PermissionError("Synthetic wallet refusal")
        return "event"

    def execute(prompt, **kwargs):
        trace.append("adapter")
        captured.append(prompt)
        return {"text":"OK", "usage":{"prompt_tokens":1,"completion_tokens":1,"total_tokens":2}}

    wallet = NS(threaded=lambda f: (f, lambda:None), subscription_begin=begin,
                subscription_end=lambda event:trace.append("settle") if event else None)
    ns = selected(path, {"Evaluation","ProtocolError","sse","usage_cost","check_window","admission_input_bound",
                         "scoped_task_names","WINDOW","MODELS","TOOL_NAMES"}, Path=Path, json=json, queue=queue,
                  time=time, threading=threading, datetime=datetime, timezone=timezone, uuid=uuid, TASK_TOOL_NAMES=set(),
                  reject_worker_media=lambda *a,**k:None, contains_refs=lambda _:False, routing_metrics=NS(stamp=lambda *a:None),
                  router_media_view=NS(project_system_messages=lambda m:m), wallet_runtime=wallet,
                  app_memory=NS(project_messages=projection, thread_target=lambda f:f, call=lambda label,fn,*a,**k:fn(*a,**k)),
                  adapter=lambda name:NS(execute=execute))
    assert ns["WINDOW"] - ns["MODELS"]["kimi"]["output"] - 4096 == CAP
    engine=ns["Evaluation"](W)
    engine.save=lambda r:records.append(copy.deepcopy(r))
    with patch.dict(sys.modules, {"iald_orcamento":NS(BudgetError=type("BudgetError",(Exception,),{}))}):
        list(engine.stream("kimi", messages, [], None, memory_sha256="fixture", authorize=allow))
    return records[-1], trace, captured


def review():
    assert __debug__
    base = INST.read_bytes()
    staged = CAND.read_bytes()
    ident = json.loads((W.parent/"integration_review/PATCH_PLAN_R2.json").read_bytes())
    assert pin(INST)==E["baseline_sha256"] and pin(CAND)==E["staged_sha256"]
    assert all(pin(Path(row["destination"]))==row["sha256"] for row in ident["files"])
    old = b"                    check_window({'prompt': prompt}, spec['output'])"
    new = (b"                    # The CLI decodes its stdin JSON before measuring the actual prompt.\n"
           b"                    if len(prompt.encode('utf-8')) > WINDOW - spec['output'] - 4096:\n"
           b"                        raise ProtocolError('kimi_cli_input_envelope_exceeded')")
    nl = b"\r\n" if b"\r\n" in base else b"\n"
    assert base.count(old)==1 and base.replace(old,new.replace(b"\n",nl))==staged
    import reproduce as fixture
    assert pin(W/"reproduce.py")==E["fixture_sha256"]
    science = PREFIX.read_bytes().decode("utf-8")
    assert pin(PREFIX)==E["evaluation"]["prefix_sha256"]==pin(W.parent/"app/packages/shared/prefix.md")
    body = WEB.read_text(encoding="utf-8")
    route = next(n for n in ast.parse(body).body if getattr(n,"name","")=="_chat_avaliacao")
    lines = [n.value for n in ast.walk(route) if isinstance(n,ast.Constant) and isinstance(n.value,str)]
    note = next(x for x in lines if x=="Modelo de inferência: ")+"Kimi K3"+next(x for x in lines if x.startswith(". Preserve o regime"))+next(x for x in lines if x.startswith("Use LaTeX"))
    heading = next(x for x in lines if x.startswith("\nFONTES RECUPERADAS"))
    suffix = next(x for x in lines if x.startswith("\nNesta chamada Kimi"))
    assert "app_providers.check_window(admission, reserve)" in ast.unparse(route)
    tools = definitions()
    identity = lambda m:m
    acom = selected(MEM, {"project_messages","_START","_END"},copy=copy,
                    current=lambda:NS(projection=lambda **k:{"text":"memória sintética β\n"*64}))["project_messages"]
    fmt=fixture.serialize
    question="Como ler β? 🧪\r\n“teste” \\ \""
    rguidance="Diretiva sintética do seletor."
    excerpt="fonte 🧪\n"*1536
    wire = selected(CAND, {"wire_messages"}, reject_worker_media=lambda *a,**k:None,
                    contains_refs=lambda _:False,app_memory=NS(project_messages=acom),
                    router_media_view=NS(project_system_messages=identity))["wire_messages"]
    m=wire([dict(role="user",content=question)],science,note+"\n"+rguidance,provider="kimi")
    m[0]["content"]+=heading+excerpt+suffix
    prompt=fmt(acom(m))
    assert prompt.count("<IALD_COMMON_MEMORY_V1>")==1 and json.loads(prompt)["instructions"].startswith(science)
    normal,trace,cap=worker(CAND,m,acom)
    assert normal["status"]=="completed" and cap==[prompt] and trace==["authorize","subscription_begin","adapter","settle"]
    oldcase=worker(INST,m,acom)
    assert oldcase[0]["status"]=="failed_or_uncertain" and not oldcase[2]
    with tempfile.TemporaryDirectory(dir=W, prefix="review_probe_") as tmp:
        assert Path(tmp).resolve().parent == W
        observed=transport(Path(tmp)/"boundary",prompt)
    checks={}
    for denial in ("wallet","authorize"):
        rec,events,got=worker(CAND,m,acom,denial)
        assert not got and rec["status"]=="failed_or_uncertain"
        assert events==(["authorize","subscription_begin"] if denial=="wallet" else ["authorize"])
        checks[denial]=events
    upstream=selected(CAND,{"admission_input_bound","check_window","WINDOW"},json=json)["check_window"]
    def websize(msgs):return len(encode({"messages":msgs,"tools":tools}))
    web_actual=upstream({"messages":m,"tools":tools},131072)
    assert web_actual==websize(m)
    plain=[{"role":"system","content":science+"\n\n"+note+heading+"{}"+suffix},{"role":"user","content":question}]
    fixed=len(fmt(plain).encode())
    exact=copy.deepcopy(plain);exact[-1]["content"]+="x"*(CAP-fixed)
    accepted=worker(CAND,exact,identity)
    assert accepted[2]==[fmt(exact)] and len(accepted[2][0].encode())==CAP
    overflow=copy.deepcopy(exact);overflow[-1]["content"]+="é"
    refused=worker(CAND,overflow,identity)
    assert not refused[1] and refused[0]["error_code"]=="kimi_cli_input_envelope_exceeded"
    try:upstream({"messages":exact,"tools":tools},131072)
    except ValueError:pass
    else:raise AssertionError("Expected distinct web admission bound")
    return dict(status="PASS",STATUS="PASS",scope="Correção da reserialização no worker Kimi. Validação local; promoção exclusiva deste delta sobre a baseline medida.",
        reviewer="codex-f03-v408-staging",reviewed_at=datetime.now(timezone.utc).isoformat(),
        installed_sha256=pin(INST),candidate_sha256=pin(CAND),module=str(INST),candidate=str(CAND),
        tests={"exact_delta_only":True,"v408_operational_r2_destinations_pinned":len(ident["files"]),
               "v408_fixed_science_prefix_bytes":len(science.encode()),"v408_science_sha256":pin(PREFIX),
               "same_synthetic_call":{"before":oldcase[0]["error_type"],"after":normal["status"],"trace":trace,
               "raw_stdin_then_CLI_arg_bytes_and_sha256":observed,"pre_worker_web_bytes":web_actual,
               "legacy_worker_count":len(encode({"prompt":prompt})),"unused_cli_bytes":CAP-len(prompt.encode())},
               "web_tool_definition_count":len(tools),"manual_short_question_fixed_server_notes_empty_excerpt_cli_bytes":fixed,
               "prefix_alone_no_turn_cli_bytes":len(fmt([{"role":"system","content":science}]).encode()),
               "exact_byte_limit_admitted_by_worker":CAP,"multi_byte_over_rejected_before_authorization_wallet_adapter":CAP+2,
               "denied_dispatch_hooks":checks,"output_reserve":131072,"safety_margin":4096},
        finding={"severity":"LOW","scope":"Residual preexistente da admissão HTTP, fora do delta do worker",
                 "source":str(WEB),"function":"_chat_avaliacao","worker_cli_bytes":CAP,"web_count_same_messages":websize(exact),
                 "consequence":"No limite, a rota web recusa uma mensagem que caberia no CLI porque inclui descritores de ferramentas ausentes de -p. A pergunta sintética com ciência, orientação, recuperação e projeção ACOM passou em ambas as admissões após o patch."},
        limits=["O tamanho histórico com diretiva JEV, perfil, acolhimento, ACOM, excerto e histórico depende do turno e não foi observado. O teto de 24.000 do excerto conta caracteres antes de escape e UTF-8.",
                "O launcher real passou o argumento a uma entrada Node substituta. O preflight autenticado, a política do fornecedor, os tokens do prompt completo com agent-file e o uso remoto ficaram fora do ensaio.",
                "Hooks da carteira exercitados com recusa e liquidação sintéticas; nenhum ledger real. O status dispatched pode preceder uma recusa de autorização/carteira no código preexistente."],
        files={str(p):pin(p) for p in (Path(__file__),KIMI,LAUNCH,ADAPTER/"kimi_text_agent.md",WEB,MEM,APP/"iald_wallet_runtime.py",W/"reproduce.py",W/"kimi_cli_input.patch",W/"EVIDENCIA.json",W.parent/"integration_review/PATCH_PLAN_R2.json")},
        provider_calls=0,live_queries=0,installation=False)


if __name__=="__main__":
    report=review()
    target=W/"REVIEW.json"
    print(json.dumps(report,ensure_ascii=False,indent=2))
    with target.open("x",encoding="utf-8") as out:
        json.dump(report,out,ensure_ascii=False,indent=2)

