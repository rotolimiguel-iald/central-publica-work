"""W-only N1/N2/N3 regressions; no stage, ROOT, environment or provider."""
import sys, socket, hashlib, json, math, io, unittest
from pathlib import Path
from types import SimpleNamespace as NS
from datetime import datetime, timezone
sys.dont_write_bytecode=True
def blocked(*a,**k):raise AssertionError('Network forbidden')
socket.create_connection=blocked;socket.socket.connect=blocked;socket.socket.connect_ex=blocked
W=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(W))
names=['claude_native_account.py','claude_route_bridge.py','claude_profiles.py','claude_server_selection.py','claude_account_policy.py','test_claude_native_account.py','test_claude_route_bridge.py']
before={W/n:(W/n).read_bytes() for n in names}
from claude_native_account import NativeAccount,DeferredStartAccount
from claude_route_bridge import RouteBridge
from claude_profiles import HAIKU
class Error(ValueError):pass
class Guard:
    def __init__(self):self.res=[];self.settlements=[]
    def check(self,*a):pass
    def reserve(self,*a,**kw):self.res.append((a,kw));return str(len(self.res))
    def settle(self,*a,**kw):self.settlements.append((a,kw))
class Ledger:
    def __init__(self,fail_at=None):self.rows=[];self.attempts=0;self.fail_at=fail_at
    def registrar(self,*a,**kw):
        self.attempts+=1
        if self.attempts==self.fail_at:raise OSError('fixture failure BEFORE commit')
        self.rows.append((a,kw))
def tokens(u,p):return u['completion_tokens']+max(0,u['prompt_tokens']-max(p,u.get('prompt_tokens_details',{}).get('cached_tokens',0)))
motors=NS(GRATUITO='gratuito',tokens_contados=tokens,claude_configurado=lambda cfg:True)
def cfg(rates=(1,.1,5,1.25)):
    return NS(janela=200000,cota_global_usd=15,cota_usuario_usd=1,cota_operador_usd=1,
              cota_global_gratuito_usd=5,cache_ttl='5m',contas={'luiz'},precos=lambda model:rates)
def account(l):
    seen=[]
    a=NativeAccount(motors=motors,budget=NS(BudgetError=Error,WindowError=Error,RESERVATION_MARGIN=1.15),guard=Guard(),ledger=l,cfg=cfg(),user='fixture',admin=False,model=HAIKU.model,quota_key='fixture',plan='gratuito',prefix_tokens=183135,count_request=lambda p:seen.append(dict(p)) or 184609)
    return a,seen
payload={'model':HAIKU.model,'max_completion_tokens':4096}
evidence={}
class Regression(unittest.TestCase):
    def test_N1_first_and_later_failure_resume(self):
        evidence['N1']=[]
        for fail_at in (1,2):
            l=Ledger(fail_at);a,_=account(l)
            for output in (5,6,7):
                a.iniciar_chamada(dict(payload));a.uso({'prompt_tokens':184609,'completion_tokens':output})
            with self.assertRaises(OSError):a.fechar()
            self.assertFalse(a.closed);self.assertEqual(a._persisted,fail_at-1)
            a.fechar();a.fechar()
            self.assertTrue(a.closed);self.assertEqual(a._persisted,3)
            self.assertEqual([row[0][4] for row in l.rows],[5,6,7])
            self.assertEqual(len(a.guard.settlements),3)
            evidence['N1'].append({'fail_before_commit_at':fail_at,'rows_after_retry':3,'no_duplicate_rows':True,'closed_after_success':True})

    def test_N2_pending_refuses_before_counter_or_new_reserve(self):
        a,seen=account(Ledger());a.iniciar_chamada(dict(payload))
        with self.assertRaises(Error):a.iniciar_chamada(dict(payload))
        self.assertEqual(len(seen),1);self.assertEqual(len(a.guard.res),1)
        self.assertEqual(a.guard.settlements,[(('1',),{})])
        self.assertEqual(tokens(a.usos[0],183135),5570)
        a.fechar();self.assertEqual(len(a.ledger.rows),1)
        evidence['N2']={'counter_calls':1,'reservations':1,'hold_settled_without_discount':True,'estimated_quota_tokens':5570}

    def test_N3_effective_read_and_output_rates(self):
        for rates in ((1,.1,1000,1.25),(1,1000,5,1.25)):
            b=RouteBridge(motors=motors,base_config=cfg(rates),package_loader=lambda:object(),enabled=True,public_daily_usd=1,public_group_daily_usd=5)
            with self.assertRaises(ValueError):b.public_budget()
            self.assertEqual(b.options({'plano':'gratuito'},'fixture'),[])
        evidence['N3']={'high_output_and_read_prices_disable_public':True}

    def test_N3_invalid_prices_and_ttl_defaults(self):
        for rates in ((1,.1,5),(-1,.1,5,1.25),(1,float('nan'),5,1.25),(True,.1,5,1.25),(1,.1,float('inf'),1.25)):
            b=RouteBridge(motors=motors,base_config=cfg(rates),package_loader=lambda:object())
            with self.assertRaises(ValueError):b.haiku_rates()
        for ttl,write in [('5m',1.25),('1h',2)]:
            c=cfg(None);c.cache_ttl=ttl
            b=RouteBridge(motors=motors,base_config=c,package_loader=lambda:object())
            self.assertEqual(b.haiku_rates(),(1,.1,5,write))

    def test_public_default_off(self):
        b=RouteBridge(motors=motors,base_config=cfg(),package_loader=lambda:object(),enabled=True)
        self.assertEqual(b.options({'plano':'gratuito'},'fixture'),[])
        evidence['public_default_off']=True

    def test_deferred_wrapper_has_no_early_reservation(self):
        a,seen=account(Ledger());d=DeferredStartAccount(a)
        p=dict(payload);d.iniciar_chamada(p)
        self.assertEqual(seen,[]);self.assertEqual(a.guard.res,[])
        p['tool_choice']='none';a.iniciar_chamada(p)
        self.assertEqual(len(seen),1);self.assertEqual(seen[0]['tool_choice'],'none')
        d.descartar_ultima_chamada();d.fechar()
        self.assertTrue(a.closed)
        evidence['defer_unit_only']={'early_reservation':False,'final_choice_seen':'none','delegation':True}

if __name__=='__main__':
    stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Regression))
    for path,data in before.items():assert path.read_bytes()==data,'Source drift: '+str(path)
    out=W/'adversarial_memory_review'/('native_finance_recheck_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'));out.mkdir()
    report={'status':'CORRECOES_N1_N2_N3_VERIFICADAS_NO_ESCOPO_UNITARIO' if r.wasSuccessful() else 'FALHA',
       'pins':{str(p):hashlib.sha256(b).hexdigest() for p,b in before.items()},'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'evidence':evidence,'remaining_reproduced_findings':[],
       'limits':['W only. No stage/JS comparison pending final parent stage; S3/S4 integration remains pending.',
                 '6 independent unit tests with injected guard/ledger. Parent 18 SQLite/bridge tests read but not rerun because importing ROOT is out of scope.',
                 'Cursor recovery verified for exceptions BEFORE ledger commit within same account instance. Does not establish exactly-once after ambiguous post-commit failure/process crash or across SQLite and JSON ledger.',
                 'Pending second call refused before another counter/reserve. No claim of permanent account lock; later explicit calls are outside that tested transition.',
                 'Deferred wrapper tested in isolation only. Final stage must start real account exactly once on final payload before send.',
                 'No budget activation/approval, production change, provider measurement or network.']}
    md='# Reavaliação N1–N3\n\nCorreções verificadas no escopo unitário; sem achados remanescentes reproduzidos nesses três casos.\n\nN1: falha antes da gravação na primeira ou segunda linha permite retomada, sem duplicar linhas já concluídas; closed só após sucesso. N2: chamada pendente é liquidada pelo hold e impede segunda contagem/reserva nessa tentativa. N3: disponibilidade usa entrada/leitura/saída/escrita efetivas e recusa tarifas inválidas.\n\n6 testes focais independentes passaram. Política pública sem orçamento explícito permanece desligada. Wrapper defer não reserva antes da chamada final, em teste isolado.\n\nNão reexecutados os18 testes do pai que importam ROOT. Cursor em memória não certifica exactly-once após falha ambígua posterior ao commit/process crash. Integração do stage/S3/S4 aguarda versão final; JS/app não inspecionados. Sem alteração de produção, API ou ativação. Hashes em review.json.\n'
    for name,text in [('review.json',json.dumps(report,ensure_ascii=False,indent=2)),('REVIEW.md',md),('tests.txt',stream.getvalue())]:
        raw=text.encode('utf-8');tmp=out/(name+'.tmp')
        with tmp.open('xb') as f:f.write(raw)
        assert tmp.read_bytes()==raw;tmp.rename(out/name)
    print(json.dumps({'report':str(out/'review.json'),'tests':r.testsRun,'passed':r.wasSuccessful()},ensure_ascii=False))
    if not r.wasSuccessful():print(stream.getvalue());sys.exit(1)
