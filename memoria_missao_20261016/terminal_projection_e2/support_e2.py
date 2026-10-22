"""Delivery helpers for the measured terminal-handle projection correction."""
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

BASE=Path(__file__).resolve().parent
CENTRAL=Path(r'C:\IALD\Central de Patentes')
CORE=Path(r'C:\IALD\MEMORIA_IALD')
REF=BASE.parent/'FECHO_MISSION_REFERENCE.json'
ACTOR={'id':'codex-gerente-tgl','kind':'agent'}
TASK='M2_TERMINAL_PROJECTION'
UNIT='F9.MEMORIA_MISSAO_20261016'
OUT=CENTRAL/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'

def new(name,value):
    p=BASE/name
    raw=value if isinstance(value,bytes) else (json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf-8')
    if p.exists(): raise FileExistsError(p)
    tmp=p.with_name(p.name+'.tmp_'+uuid.uuid4().hex)
    with tmp.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==raw
    tmp.rename(p)
    return p

def pin(p):
    p=Path(p).resolve()
    return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())

def command(args,name,payload=None):
    process=subprocess.run([sys.executable,'-B','-X','utf8',*map(str,args)],
        input=None if payload is None else json.dumps(payload,ensure_ascii=False),
        text=True,encoding='utf-8',capture_output=True)
    try:r=json.loads(process.stdout)
    except ValueError:r={'stdout':process.stdout}
    p=new(name+'.json',dict(command=list(map(str,args)),request=payload,exit_code=process.returncode,
                          result=r,stderr=process.stderr))
    if process.returncode or r.get('ok') is False:raise RuntimeError(str(p))
    return r

def call(cli,payload,name):return command([CORE/cli],name,payload)['result']
def project(name,budget=200000):return call('mission_cli.py',dict(operation='project',reference=str(REF),max_chars=budget),name)
def args(p):return dict(reference=str(REF),actor=ACTOR,expected_revision=p['receipt']['revision'],projection_sha256=p['projection_sha256'])

def preflight(name):
    p=project(name+'_PROJECT')
    t=next(t for t in p['projection']['active'] if t['id']==TASK)
    call('mission_cli.py',dict(args(p),operation='check',task_id=TASK,lease_id=t['lease']['id']),name+'_CHECK')
    return p

def update_agent(name,agent_id,status,evidence=None):
    snap=call('session_memory.py',dict(operation='get',reference=str(REF)),name+'_GET')
    handles=snap['p']['handles']
    old=next((h for h in handles if h['id']==agent_id),None)
    if old is None:
        old=dict(id=agent_id,kind='agent',task_id=TASK,no_repeat=True)
        handles.append(old)
    old['status']=status
    if evidence:old['evidence']=pin(evidence)
    return call('session_memory.py',dict(operation='transition',reference=str(REF),actor=ACTOR,
        expected_revision=snap['revision'],event_id=name,
        changes=dict(flow=dict(handles=handles))),name+'_UPDATE')

def load_tools():
    path=CENTRAL/'Chatgpt/IALD_ORQUESTRACAO_20260923/iald_orchestrator/mission_bridge.py'
    spec=importlib.util.spec_from_file_location('e2_bridge',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    class Registry:
        def __init__(self):self.tools={}
        def tool(self):
            def add(fn):self.tools[fn.__name__]=fn;return fn
            return add
    reg=Registry();mod.register_tools(reg);return reg.tools
