"""Focused offline reviewer: no TTS/network; all transport calls mocked."""
from pathlib import Path
import ast,copy,hashlib,importlib.util,io,json,subprocess,time,uuid
from unittest.mock import patch
V=Path(__file__).resolve().parent.parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
spec=importlib.util.spec_from_file_location("narr",V/"audio/build_narration.py");n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
base=V/"replay"/("audio_delta_fixtures_"+uuid.uuid4().hex);base.mkdir()
auth=base/"authorization.json"
auth.write_bytes(n.encoded({"status":"AUTHORIZED_BY_HUMAN","origin":"direct_user_reply_this_thread","answer_verbatim":"Autorizar até duas tentativas por fala","maximum_new_attempts_per_failed_utterance":2}))
context=n.load_bounded_authorization(auth);voice=n.VOICES["en"];text="Synthetic reviewer fixture";key=n.cache_key(voice,text);cases={}
def fail(*a,**kw):return subprocess.CompletedProcess(a,1,b"",b"synthetic failure; no network")
def invoke(cache):return n.bounded_tts(cache,voice,text,"synthetic-plan",base,"BLOCKED_NODE",context)
cache=base/"exhausted";cache.mkdir();original=n.encoded({"key":key,"state":"uncertain"});(cache/(key+".json")).write_bytes(original)
with patch.object(n.subprocess,"run",side_effect=fail) as mock:
 try:invoke(cache)
 except n.PendingUtterance:pass
 assert mock.call_count==2
 before=mock.call_count
 try:invoke(cache)
 except n.PendingUtterance:pass
 assert mock.call_count==before
 assert (cache/(key+".json")).read_bytes()==original
 slots=list(cache.rglob("attempt.json"));assert len(slots)==2 and len({read(p)["attempt_id"] for p in slots})==2
cases["two_new_attempts_then_zero_on_rerun_preserve_original"]=True
cache=base/"inflight";cache.mkdir();(cache/(key+".json")).write_bytes(n.encoded({"key":key,"state":"intent"}))
with patch.object(n.subprocess,"run",side_effect=AssertionError("network forbidden")):
 try:invoke(cache);raise AssertionError("inflight accepted")
 except n.PendingUtterance:pass
cases["inflight_refused_no_transport"]=True
cache=base/"success";cache.mkdir()
with patch.object(n.subprocess,"run",return_value=subprocess.CompletedProcess([],0,b"SYNTHETIC_NOT_REAL_MP3",b"")) as mock:
 result=invoke(cache);assert mock.call_count==1;assert invoke(cache)==result and mock.call_count==1
cases["completed_reused_no_duplicate"]=True
result.write_bytes(b"tampered")
with patch.object(n.subprocess,"run",side_effect=AssertionError("network forbidden")):
 try:invoke(cache);raise AssertionError("tamper accepted")
 except ValueError as exc:assert "CACHE_INTEGRITY" in str(exc)
cases["cache_tamper_refused"]=True
auth.write_bytes(n.encoded({"status":"AUTHORIZED_BY_HUMAN","origin":"direct_user_reply_this_thread","answer_verbatim":"Autorizar até duas tentativas por fala","maximum_new_attempts_per_failed_utterance":3}))
with patch.object(n.subprocess,"run",side_effect=AssertionError("network forbidden")):
 try:invoke(cache);raise AssertionError("changed authorization accepted")
 except ValueError as exc:assert "BOUNDED_LIMIT" in str(exc)
cases["changed_authorization_refused"]=True
# Execute the actual audio-validation nodes only: encode/loop completion is not ready.
tree=ast.parse((V/"make_v7.py").read_text(encoding="utf8"))
fn=copy.deepcopy(next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=="validate_encodes"))
loop=next(x for x in fn.body if isinstance(x,ast.For) and ast.unparse(x.target)=="n")
start=next(i for i,x in enumerate(loop.body) if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="tl" for t in x.targets))
loop.body=loop.body[start:]
fn.body=fn.body[:fn.body.index(loop)+1]+[ast.Return(ast.Constant(True))]
ns={"ROOT":V,"read":read,"sha":sha,"run":lambda *a,**kw:n.make_plan(V,V/"audio/script_templates.json")}
exec(compile(ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[])),"audio-validation-actual-AST","exec"),ns)
real_build=read(V/"audio/NARRATION_BUILD.json");real_tl={i:read(V/f"data/film{i}_narration_timeline.json") for i in [1,2]}
def fixture(mutator):
 build=copy.deepcopy(real_build);tls=copy.deepcopy(real_tl);mutator(build,tls)
 def reader(p):
  if p.name=="NARRATION_BUILD.json":return build
  return tls[int(p.name[4])]
 ns["read"]=reader
 try:return bool(ns["validate_encodes"]({})),None
 except (ValueError,KeyError) as e:return False,str(e)
make_cases={}
make_cases["real_cache_only"]=fixture(lambda b,t:None)
make_cases["pending"]=fixture(lambda b,t:b.update(pending={"x":"missing"}))
make_cases["inflight"]=fixture(lambda b,t:b.update(tts_inflight=True))
make_cases["stale_plan"]=fixture(lambda b,t:b.update(plan_sha256="0"*64))
make_cases["unmeasured_film2"]=fixture(lambda b,t:b["reports"]["film2"].update(status="PLANNED_NO_AUDIO"))
make_cases["timeline_plan"]=fixture(lambda b,t:t[1].update(plan_sha256="0"*64))
make_cases["measurement_mismatch"]=fixture(lambda b,t:t[1]["loudness"]["en"]["after"].update(input_i="-2"))
def both(b,t,value):
 for x in [b["reports"]["film1"],t[1]]:x["loudness"]["en"]["after"]["input_i"]=value
make_cases["out_of_range"]=fixture(lambda b,t:both(b,t,"-12"))
make_cases["nonfinite_nan"]=fixture(lambda b,t:both(b,t,"NaN"))
def badpin(b,t):
 for x in [b["reports"]["film1"],t[1]]:x["loudness"]["en"]["aac"]["sha256"]="0"*64
make_cases["aac_pin"]=fixture(badpin)
assert make_cases["real_cache_only"][0]
assert all(not result[0] for name,result in make_cases.items() if name not in ["real_cache_only","nonfinite_nan"])
cli=subprocess.run(["C:/Python314/python.exe","-B",str(V/"make_v7.py"),"--narration-cache-only","--bounded-retry-authorization","unused"],capture_output=True,text=True)
assert cli.returncode==2 and "not allowed with argument" in cli.stderr
make_cases["exclusive_cli_flags"]=[False,"argparse exit2 as expected"]
# Read/measure existing audio, never build or synthesize.
ff=V.parent/"node_modules/@ffmpeg-installer/win32-x64/ffmpeg.exe";audio=[]
for film in [1,2]:
 tl=real_tl[film];assert tl["plan_sha256"]==real_build["plan_sha256"] and tl["status"]=="AUDIO_MEASURED"
 for lang in ["en","pt-BR"]:
  cues=tl["cues"][lang];assert all(0<=c["start"]<c["end"]<=tl["total_seconds"] for c in cues)
  assert all(cues[i]["end"]<=cues[i+1]["start"] for i in range(len(cues)-1))
  for c in cues:
   segment=next(s for s in tl["segments"] if s["index"]==c["scene"]);assert segment["start"]<=c["start"]<c["end"]<=segment["end"]
  for ext in ["wav","m4a"]:
   p=V/f"audio/film{film}/{lang}.{ext}";expected=tl["loudness"][lang]["sha256"] if ext=="wav" else tl["loudness"][lang]["aac"]["sha256"];assert sha(p)==expected
   measure=n.loud_measure(ff,p);assert abs(float(measure["input_i"])+16)<=1
   if ext=="wav":assert abs(n.wav_duration(p)-tl["total_seconds"])<.05
   audio.append({"file":str(p.relative_to(V)),"sha256":sha(p),"lufs":float(measure["input_i"]),"true_peak":float(measure["input_tp"]),"cues":len(cues)})
report={"bounded_cases":cases,"make_audio_delta_cases":make_cases,"audio":audio,"pins":{str(p.relative_to(V)):sha(p) for p in [V/"make_v7.py",V/"audio/build_narration.py",V/"audio/NARRATION_BUILD.json",V/"audio/NARRATION_PLAN_v399_final.json"]},"scope":"Actual functions with synthetic transport mocked; actual audio hashes/timings and local loudness measurements. No external calls, encode/render or listening test. AST audit excludes pending E encode/loop checks; not whole-pipeline acceptance.","fixture_directory":str(base)}
p=V/"replay/AUDIO_DELTA_CHECKS.json";p.write_bytes(n.encoded(report));print(json.dumps(report))
