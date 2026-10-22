"""Independent W-only probes; never execute parent tests importing ROOT."""
import ast, copy, hashlib, io, json, math, socket, sys, unittest
from pathlib import Path
from types import SimpleNamespace as NS
from datetime import datetime, timezone
sys.dont_write_bytecode=True
def blocked(*a,**kw):raise AssertionError('Network forbidden')
socket.create_connection=blocked;socket.socket.connect=blocked
W=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(W))
from claude_native_account import NativeAccount,usage_amount
from claude_route_bridge import RouteBridge
from claude_profiles import HAIKU
from haiku_s4_agent_patcher import patch_stage
STAGE=W/'claude_routes_stage_20260922_145545_134624/iald_web_server.py'
paths=[W/n for n in ('claude_native_account.py','claude_route_bridge.py','claude_server_selection.py','stage_claude_routes.py','test_claude_native_account.py','test_claude_route_bridge.py')]+[STAGE,Path(__file__).parent/'haiku_s4_agent_patcher.py']
pins={p:p.read_bytes() for p in paths}
evidence={}
class BudgetError(ValueError):pass
budget=NS(RESERVATION_MARGIN=1.15,WindowError=BudgetError,BudgetError=BudgetError)
def tokens(u,prefix):return u['completion_tokens']+max(0,u['prompt_tokens']-max(prefix,u.get('prompt_tokens_details',{}).get('cached_tokens',0)))
motors=NS(GRATUITO='gratuito',tokens_contados=tokens,claude_configurado=lambda cfg:True)
class Guard:
    def __init__(self):self.res=[];self.settled=[]
    def check(self,*a):pass
    def reserve(self,*a,**kw):self.res.append((a,kw));return str(len(self.res))
    def settle(self,*a,**kw):self.settled.append((a,kw))
class Ledger:
    def __init__(self):self.rows=[];self.fail=False;self.attempts=0
    def registrar(self,*a,**kw):
        self.attempts+=1
        if self.fail:raise OSError('synthetic ledger unavailable')
        self.rows.append((a,kw))
def cfg(rates=(1,.1,5,1.25)):
    return NS(janela=200000,cota_global_usd=15,cota_usuario_usd=1,cota_operador_usd=1,
              cota_global_gratuito_usd=5,fator_tokens=99,precos=lambda model:rates,
              cache_ttl='5m',contas={'luiz'})
def account(ledger=None):
    return NativeAccount(motors=motors,budget=budget,guard=Guard(),ledger=ledger or Ledger(),cfg=cfg(),
                         user='fixture',admin=False,model=HAIKU.model,quota_key='fixture',plan='gratuito',prefix_tokens=183135,count_request=lambda p:184609)
payload={'max_completion_tokens':4096,'model':HAIKU.model}
class Probes(unittest.TestCase):
    def test_default_public_policy_off_and_limits_explicit(self):
        b=RouteBridge(motors=motors,base_config=cfg(),package_loader=lambda:object(),enabled=True)
        self.assertEqual(b.options({'plano':'gratuito'},'fixture'),[])
        for v in (None,True,float('nan'),0,.02):
            b.public_daily_usd=v;b.public_group_daily_usd=5
            self.assertEqual(b.options({'plano':'gratuito'},'fixture'),[])
        b.public_daily_usd=1
        self.assertEqual(b.public_budget(),(1,5))
        evidence['default_off']=True

    def test_exact_split_and_native_hold(self):
        a=account();a.iniciar_chamada(dict(payload))
        cap=(math.ceil(184609*1.15)*1.25+4096*5)/1e6
        self.assertAlmostEqual(a.pending['cap'],cap)
        u={'prompt_tokens':184609,'completion_tokens':100,'prompt_tokens_details':{'cached_tokens':100000,'cache_write_tokens':83135}}
        a.uso(u);a.fechar()
        self.assertAlmostEqual(a.ledger.rows[0][0][5],(1474+10000+83135*1.25+500)/1e6)
        b=account();b.iniciar_chamada(dict(payload));b.fechar()
        self.assertEqual(b.guard.settled,[(('1',),{})])
        self.assertEqual(b.ledger.rows[0][1]['tokens'],5570)
        evidence['native_no_factor_and_hold']=True

    def test_ledger_failure_makes_close_permanently_skip_records(self):
        l=Ledger();a=account(l);a.iniciar_chamada(dict(payload))
        a.uso({'prompt_tokens':184609,'completion_tokens':100})
        l.fail=True
        with self.assertRaises(OSError):a.fechar()
        self.assertTrue(a.closed)
        l.fail=False;a.fechar()
        self.assertEqual(l.rows,[]);self.assertEqual(l.attempts,1)
        evidence['N1']={'closed_after_failed_ledger':True,'rows_after_recovery_and_second_close':0,'settlements':len(a.guard.settled),'record_attempts':l.attempts}

    def test_pending_uncertainty_not_visible_to_outer_balance_check(self):
        a=account();a.iniciar_chamada(dict(payload))
        # Simulates only documented ContaComSaldo ordering, not the parent chat.
        before=sum(tokens(u,183135) for u in a.usos)
        second=dict(payload)
        second['max_completion_tokens']=min(4096,8000-before-(184609-183135))
        a.iniciar_chamada(second)
        first=sum(tokens(u,183135) for u in a.usos)
        possible=first+1474+second['max_completion_tokens']
        self.assertEqual(before,0);self.assertEqual(first,5570);self.assertGreater(possible,8000)
        evidence['N2']={'prior_usage_visible_before_start':before,'prior_hold_tokens_after_start':first,'second_output':second['max_completion_tokens'],'two_calls_possible_tokens':possible,'quota_fixture':8000,'scope':'Ordering reproduction with injected guards; no assertion that normal chat continues after an interrupted SSE.'}

    def test_budget_readiness_ignores_configured_output_rate(self):
        b=RouteBridge(motors=motors,base_config=cfg((1,.1,1000,1.25)),package_loader=lambda:object(),enabled=True,public_daily_usd=1,public_group_daily_usd=5)
        self.assertEqual(b.public_budget(),(1,5))
        cap=(math.ceil(184609*1.15)*1.25+4096*1000)/1e6
        self.assertGreater(cap,1)
        evidence['N3']={'budget_accepted':[1,5],'configured_output_rate':1000,'native_fixture_reservation_usd':cap,'daily_limit':1,'scope':'Synthetic configured tariff, not actual provider price.'}

    def test_counter_state_cache_in_stage_ast(self):
        source=pins[STAGE].decode('utf-8-sig');t=ast.parse(source)
        chat=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_chat_externo')
        state=[n for n in ast.walk(chat) if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id=='estado_claude' for x in n.targets)]
        counter=next(n for n in ast.walk(chat) if isinstance(n,ast.FunctionDef) and n.name=='count_haiku_wire')
        saldo=next(n for n in ast.walk(chat) if isinstance(n,ast.FunctionDef) and n.name=='tokens_para_saldo')
        self.assertEqual(len(state),1);self.assertLess(state[0].lineno,counter.lineno)
        self.assertIn('estado=estado_claude',ast.unparse(saldo))
        self.assertIn('counter=count_haiku_wire',source)
        evidence['shared_state_counter']={'state_assignments':1,'state_line':state[0].lineno,'counter_line':counter.lineno,'both_uses_verified_statically':True}

    def test_s4_patcher_real_stage_in_memory_only(self):
        original=pins[STAGE].decode('utf-8-sig');changed=patch_stage(original)
        self.assertIn('if gratuito and not haiku and usar_agente',changed)
        tree=ast.parse(changed)
        chat=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_chat_externo')
        block=next(n for n in ast.walk(chat) if isinstance(n,ast.If) and ast.unparse(n.test)=='haiku' and 'usar_agente = True' in ast.unparse(n))
        for image in (True,False):
            env={'haiku':True,'permitidas':[{}]*7,'tem_imagem':image,'cfg':NS(memoria_modo='prompt'),'_precisa_ferramentas':lambda _:False,'ultima':''}
            exec(compile(ast.Module(body=[block],type_ignores=[]),'<isolated S4>','exec'),env)
            self.assertTrue(env['usar_agente'])
        with self.assertRaises(ValueError):patch_stage(changed)
        evidence['s4_agent']={'in_memory_patch':True,'haiku_agent_true':True,'excluded_cpt_heuristic':True,'double_apply_rejected':True}

if __name__=='__main__':
    log=io.StringIO();r=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Probes))
    for p,b in pins.items():assert p.read_bytes()==b,'Source changed: '+str(p)
    out=W/'adversarial_memory_review'/('native_account_review_'+datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f'));out.mkdir()
    findings=[{'id':'N1','severity':'P2','file':'claude_native_account.py','location':'fechar','title':'Falha do razão torna fechamento irrecuperável','fix':'Não concluir closed antes de persistir todas as linhas; usar marcador por chamada/idempotência para retomar sem duplicar as já gravadas. SQLite liquidado não substitui tokens/cotas do razão.'},
              {'id':'N2','severity':'P2','file':'claude_native_account.py','location':'iniciar_chamada/_finish_pending','title':'Saldo externo consulta usos antes de finalizar a chamada pendente','fix':'Finalizar hold pendente antes de SaldoDoPedido.antes_da_chamada, ou recusar nova chamada enquanto houver pending; não depender da finalização tardia dentro da conta.'},
              {'id':'N3','severity':'P2','file':'claude_route_bridge.py','location':'public_budget','title':'Disponibilidade usa saída fixa5 ignorando preço configurado','fix':'Validar quatro preços finitos/não negativos e calcular mínimo com as mesmas tarifas efetivas usadas pela NativeAccount, incluindo saída e leitura.'}]
    report={'status':'MUDANCAS_NECESSARIAS','pins':{str(p):hashlib.sha256(b).hexdigest() for p,b in pins.items()},'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'findings':findings,'evidence':evidence,'limits':['Somente W; testes pais que importam ROOT foram lidos, não executados. Não revalida SQLite/razão reais; guards/ledger injetados.','Não executado stage_claude_routes.py; integração inspecionada em AST do stage existente. Sem completo_chat_externo.','Orçamentos1/5/15 usados apenas como fixtures, sem autorização/ativação presumida.','S4 patcher é construção não aprovada pelo próprio autor; somente transforma texto recebido.']}
    for name,text in [('review.json',json.dumps(report,ensure_ascii=False,indent=2)),('tests.txt',log.getvalue())]:
        b=text.encode();tmp=out/(name+'.tmp')
        with tmp.open('xb') as f:f.write(b)
        assert tmp.read_bytes()==b;tmp.rename(out/name)
    print(json.dumps({'report':str(out/'review.json'),'tests':r.testsRun,'passed':r.wasSuccessful()},ensure_ascii=False))
    if not r.wasSuccessful():print(log.getvalue());sys.exit(1)
