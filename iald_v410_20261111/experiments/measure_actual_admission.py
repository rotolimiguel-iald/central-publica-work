from pathlib import Path
import sys,json,os,hashlib
W=Path(__file__).resolve().parent.parent;sys.dont_write_bytecode=True;sys.path.insert(0,str(W/'app'))
def guard(event,args):
 if event in ('socket.connect','socket.getaddrinfo','subprocess.Popen','os.system'):raise RuntimeError('Offline only')
 if event=='open' and not isinstance(args[0],int):
  p=Path(os.fsdecode(args[0])).resolve()
  if p.name in ('.env','iald_stack_v7.py','iald_psion_state.json'):raise RuntimeError('Confidential access forbidden')
sys.addaudithook(guard)
import verify_d53 as v
p=v.providers;tools=v.iald_kernel.tool_definitions()+v.iald_fontes_publicas.tool_definitions()+v.iald_core_indexado.tool_definitions()+v.iald_app_memory.tool_definitions()
reports=[]
for file in [W/'app/packages/shared/prefix.md',W/'experiments/candidate_fine.txt',W/'experiments/candidate_typed.txt',W/'experiments/candidate_whole.txt']:
 text=file.read_text(encoding='utf8');rows={}
 for provider in ('kimi','mimo','deepseek'):
  spec=p.MODELS[provider];messages=[{'role':'system','content':text},{'role':'user','content':'Explique o alcance documentado da v410.'}]
  if provider=='kimi':
   prompt=json.dumps({'instructions':text,'conversation':messages[1:]},ensure_ascii=False)
   used=len(prompt.encode());reserve=spec['output'];slack=p.WINDOW-used-reserve-4096
   rows[provider]=dict(input_bound=used,configured_max_output=reserve,effective_output=reserve,remaining_input_bytes=slack,admitted=slack>=0,check='Exact CLI JSON envelope; no history/activity projection')
  else:
   body=dict(messages=messages,tools=tools,model=spec['model'],stream=True,stream_options={'include_usage':True},thinking={'type':'enabled'})
   if provider=='deepseek':body['reasoning_effort']='max'
   used=p.admission_input_bound(body)
   try:
    reserve=p.output_budget(body,spec['output']);body['max_tokens' if provider=='deepseek' else 'max_completion_tokens']=reserve;used=p.check_window(body,reserve);ok=True
   except ValueError:reserve=None;ok=False
   rows[provider]=dict(input_bound=used,configured_max_output=spec['output'],effective_output=reserve,minimum_output=min(16384,spec['output']),remaining_input_bytes_at_min=p.WINDOW-used-min(16384,spec['output'])-4096-128,admitted=ok)
 reports.append(dict(path=str(file),disk_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),runtime_text_bytes=len(text.encode()),providers=rows))
r=dict(status='MEASURED_EXPERIMENTS_NOT_INSTALLABLE',window=p.WINDOW,scope='Runtime existing admission, synthetic one-turn public request, no real history/activity, no network/generation; not tokenizer counts. Whole-text candidate inadmissible on semantic readability grounds independently of size.',reports=reports)
(W/'experiments/ACTUAL_ADMISSION_EXPERIMENTS.json').write_bytes(json.dumps(r,ensure_ascii=False,indent=2).encode());print(json.dumps(r,ensure_ascii=False))
