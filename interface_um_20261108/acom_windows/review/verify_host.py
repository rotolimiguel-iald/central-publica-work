"""Black-box HTTP probes with a synthetic selector. Emits only non-sensitive results."""
import hashlib
import http.client
import importlib.util
import json
import sys
from contextlib import contextmanager
from pathlib import Path
import threading
from time import monotonic

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
WEB = HERE / "web_fixture"
WEB.mkdir(exist_ok=True)
(WEB / "src").mkdir(exist_ok=True)
(WEB / "downloads").mkdir(exist_ok=True)
(WEB / "downloads" / "Primeira-luz.acom").write_bytes(b"ACOM fixture")
(WEB / "downloads" / "ACOM-fonte.zip").write_bytes(b"source fixture")
(WEB / "downloads" / "private.zip").write_bytes(b"hidden fixture")
(WEB / "index.html").write_text("<!doctype html><title>ACOM test</title>", encoding="utf-8")
(WEB / "src" / "sample.mp4").write_bytes(b"0123456789")
(WEB.parent / "outside.json").write_bytes(b'"OUTSIDE"')
host_path = Path(sys.argv[1]) if len(sys.argv) > 1 else BASE / "app" / "host.py"
spec = importlib.util.spec_from_file_location("native_acom_review_host", host_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

results = {}
def expect(label, result):
    results[label] = bool(result)
    return bool(result)

gate = threading.Event()
waiting = threading.Event()
observations = []
def picker(action, language):
    observations.append((action, language))
    if action == "extract":
        return {"status":"ok", "files":1, "inputBytes":297, "outputBytes":10, "message":"fixture"}
    if action == "pack-folder":
        waiting.set()
        gate.wait(timeout=5)
        raise OSError("simulated I/O failure")
    return {"status":"cancelled"}

with mod.Host(WEB, picker=picker) as host:
    thread = threading.Thread(target=host.serve_forever, daemon=True)
    thread.start()
    def req(method, path, headers=None, data=None):
        c = http.client.HTTPConnection("127.0.0.1", host.server_port, timeout=5)
        try:
            c.request(method, path, body=data, headers=headers or {})
            r = c.getresponse()
            return r.status, r.read(), dict(r.getheaders())
        finally:
            c.close()

    path = "/acom-api/action"
    get = lambda route, headers=None: req("GET", route, headers)
    want = lambda code, outcome: code == outcome[0]
    expect("wrong_host", want(403, get("/acom-api/status", {"Host":"untrusted.example"})))
    expect("cross_site_token_denied", want(403, get("/acom-api/status", {"Sec-Fetch-Site":"cross-site"})))
    expect("external_origin_token_denied", want(403, get("/acom-api/status", {"Origin":"https://missing.invalid"})))
    ticket_url = "/launch/"+host.ticket
    expect("no_credential_for_another_windows_session", want(403, get("/acom-api/status")))
    expect("bogus_ticket_denied", want(403,get("/launch/other")))
    expect("head_cannot_consume_ticket", want(403,req("HEAD",ticket_url)))
    code,_,pair = get(ticket_url)
    expect("actual_launch_redirect", code==303 and pair["Location"]=="/?ferramenta=acom" and pair.get("Referrer-Policy")=="no-referrer")
    cookie = pair["Set-Cookie"].split(";",1)[0]
    expect("scoped_session_cookie", all(term in pair["Set-Cookie"] for term in ("Path=/acom-api/","HttpOnly","SameSite=Strict")))
    expect("consumed_ticket_denied", want(403,get(ticket_url)))
    status, body, hdr = get("/acom-api/status", {"Sec-Fetch-Site":"same-origin","Cookie":cookie})
    status_obj = json.loads(body)
    expect("local_status_json", status == 200 and status_obj["native"] is True and hdr["Content-Type"].startswith("application/json"))
    expect("no_cache_on_token", hdr.get("Cache-Control") == "no-store")
    good = {"X-ACOM-Token":status_obj["token"], "Origin":host.origin, "Content-Type":"application/json","Cookie":cookie}
    def post(obj, headers=None):
        return req("POST", path, headers if headers is not None else good, json.dumps(obj))
    value = {"action":"pack-files", "lang":"ar"}
    expect("valid_token_without_browser_session_denied", want(403, post(value, {k:v for k,v in good.items() if k!="Cookie"})))
    expect("token_without_origin_denied", want(403, post(value, {k:v for k,v in good.items() if k != "Origin"})))
    expect("foreign_origin_post_denied", want(403, post(value, {**good, "Origin":"http://untrusted.invalid"})))
    expect("missing_token_denied", want(403, post(value, {k:v for k,v in good.items() if k != "X-ACOM-Token"})))
    expect("invalid_token_denied", want(403, post(value, {**good,"X-ACOM-Token":"bad"})))
    expect("future_action_denied", want(400, post({"action":"delete"})))
    expect("filename_field_denied", want(400, post({**value,"path":"unsolicited.txt"})))
    expect("nonjson_denied", want(400, post(value, {**good,"Content-Type":"text/plain"})))
    expect("oversize_denied", want(400, post({**value,"lang":"x"*650})))
    expect("schema_array_denied", want(400, post(["unexpected"])))
    expect("no_picker_for_denied_requests", not observations)
    r, body, _=post(value)
    expect("cancel_as_cancel", r == 200 and json.loads(body)["status"] == "cancelled" and observations == [("pack-files","ar")])
    r, body, _=post({"action":"extract","lang":"en-GB"})
    success=json.loads(body)
    expect("native_counts_and_language", r == 200 and success == {"status":"ok","files":1,"inputBytes":297,"outputBytes":10,"message":"fixture"} and observations[-1]==("extract","en"))
    reply = []
    worker=threading.Thread(target=lambda:reply.append(post({"action":"pack-folder","lang":"en"})))
    worker.start()
    if not waiting.wait(4): raise RuntimeError("simulated picker did not start")
    expect("active_picker_concurrency_denied", want(409, post(value)))
    gate.set()
    worker.join(timeout=6)
    expect("picker_error_visible", len(reply)==1 and json.loads(reply[0][1])["status"]=="error")
    expect("html_served", get("/?ferramenta=acom")[1].startswith(b"<!doctype"))
    expect("test_archive_served_as_attachment", get("/downloads/Primeira-luz.acom")[1]==b"ACOM fixture" and "attachment" in get("/downloads/Primeira-luz.acom")[2].get("Content-Disposition",""))
    expect("source_archive_served", get("/downloads/ACOM-fonte.zip")[1]==b"source fixture")
    expect("unrelated_download_not_served",want(404,get("/downloads/private.zip")))
    expect("no_directory_listing", want(404, get("/src/")))
    expect("no_parent_artifact", want(404, get("/src/%2e%2e/%2e%2e/outside.json")))
    expect("no_backslash_traversal", want(404, get("/src/%2e%2e%5C%2e%2e%5Coutside.json")))
    r,b,h=get("/src/sample.mp4", {"Range":"bytes=3-7"})
    expect("actual_media_range", r==206 and b==b"34567" and h.get("Content-Range")=="bytes 3-7/10")
    expect("range_invalid_end_denied", want(416, get("/src/sample.mp4", {"Range":"bytes=10-20"})))
    r,b,h=req("HEAD","/src/sample.mp4")
    expect("head_length_and_no_body", r==200 and not b and h["Content-Length"]=="10")
    expect("browser_protections", h["X-Frame-Options"]=="DENY" and h["Cross-Origin-Resource-Policy"]=="same-origin")
    additional_observation = get("/acom-api/status")[0]
    host.shutdown()
    thread.join(3)

report=dict(host_sha256=hashlib.sha256(host_path.read_bytes()).hexdigest(),checks=results,passed=sum(results.values()),total=len(results),
            raw_loopback_status_http=additional_observation,
            selector="synthetic stub, actual HTTP on IPv4 loopback")
dest=HERE/("HOST_REVIEW_"+report["host_sha256"][:12]+".json")
dest.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"passed":report["passed"],"total":len(results),"failed":[k for k,v in results.items() if not v],"receipt":str(dest)}))
sys.exit(int(not all(results.values())))

