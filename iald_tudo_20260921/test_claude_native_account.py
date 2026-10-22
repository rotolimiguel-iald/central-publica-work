"""Real local ledgers/SQLite, synthetic usage; no key/provider/network."""
import importlib, json, math, sqlite3, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import Mock
from test_claude_route_bridge import motors, ROOT
from claude_profiles import HAIKU
from claude_native_account import NativeAccount, usage_amount
sys.path.insert(0, str(ROOT))
budget = importlib.import_module('iald_orcamento')


class AccountTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.guard = budget.SpendingGuard(str(Path(self.temp.name)/'reserve.db'))
        self.ledger = motors.RazaoDeUso(str(Path(self.temp.name)/'usage.json'))
        self.cfg = motors.Config(provedor='claude', modelo=HAIKU.model, janela=200000,
            cota_global_usd=15, cota_usuario_usd=1, cota_operador_usd=1,
            cota_global_gratuito_usd=5, fator_tokens=1.77,
            precos_tabela={HAIKU.model:(1,.1,5,1.25)})
        self.counter = Mock(return_value=184609)
        self.account = self.new_account()
        self.payload = {'model':HAIKU.model,'messages':[], 'max_completion_tokens':4096}

    def new_account(self):
        return NativeAccount(motors=motors,budget=budget,guard=self.guard,
            ledger=self.ledger,cfg=self.cfg,user='fixture',admin=False,model=HAIKU.model,
            quota_key='fixture',plan='gratuito',prefix_tokens=183135,count_request=self.counter)

    def test_native_reservation_ignores_legacy_factor_and_settles_split(self):
        self.account.iniciar_chamada(self.payload)
        expected = (math.ceil(184609*1.15)*1.25 + 4096*5)/1e6
        self.assertAlmostEqual(self.guard.used_today(),expected)
        usage={'prompt_tokens':184609,'completion_tokens':100,
               'prompt_tokens_details':{'cached_tokens':0,'cache_write_tokens':183135}}
        self.account.uso(usage);self.account.fechar()
        exact=(1474+183135*1.25+100*5)/1e6
        self.assertAlmostEqual(self.guard.used_today(),exact)
        self.assertAlmostEqual(self.ledger.gasto_hoje('fixture')[0],exact,places=7)
        self.assertEqual(self.ledger.leitura_de_cota('fixture','fixture','gratuito')['tokens_dia'],1574)

    def test_tool_turn_recounts_and_warm_cache_uses_read_price(self):
        self.counter.side_effect=[184609,186000]
        self.account.iniciar_chamada(self.payload)
        self.account.uso({'prompt_tokens':184609,'completion_tokens':50})
        second=dict(self.payload,messages=[{'role':'tool','content':'new result'}])
        self.account.iniciar_chamada(second)
        self.account.uso({'prompt_tokens':186000,'completion_tokens':100,
                         'prompt_tokens_details':{'cached_tokens':183135,'cache_write_tokens':1000}})
        self.account.fechar()
        expected=(184609+50*5+1865+183135*.1+1000*1.25+100*5)/1e6
        self.assertAlmostEqual(self.guard.used_today(),expected)
        self.assertEqual(self.counter.call_count,2)
        self.assertEqual(self.counter.call_args.args[0],second)

    def test_missing_usage_keeps_bound_and_native_tokens_for_next_turn(self):
        self.account.iniciar_chamada(self.payload)
        held=self.guard.used_today()
        self.account.texto('partial')
        self.account._finish_pending()
        self.assertEqual(self.account.usos[0]['prompt_tokens'],184609)
        self.assertEqual(self.account.usos[0]['completion_tokens'],4096)
        self.assertEqual(self.guard.summary()[0]['status'],'estimated_upper_bound')
        self.account.fechar();self.account.fechar()
        self.assertAlmostEqual(self.guard.used_today(),held)
        quota=self.ledger.leitura_de_cota('fixture','fixture','gratuito')
        self.assertEqual(quota['tokens_dia'],184609-183135+4096)

    def test_count_failure_and_overflow_make_no_reservation(self):
        self.counter.side_effect=ValueError('count unavailable')
        with self.assertRaises(ValueError):self.account.iniciar_chamada(self.payload)
        self.assertEqual(self.guard.used_today(),0)
        self.counter.side_effect=None;self.counter.return_value=195000
        with self.assertRaises(budget.WindowError):self.account.iniciar_chamada(self.payload)
        self.assertEqual(self.guard.used_today(),0)

    def test_known_free_refusal_releases_hold_and_ledger(self):
        self.account.iniciar_chamada(self.payload)
        self.account.descartar_ultima_chamada();self.account.fechar()
        self.assertEqual(self.guard.used_today(),0)
        self.assertEqual(self.ledger.gasto_hoje('fixture')[0],0)

    def test_invalid_usage_does_not_release_reservation(self):
        self.account.iniciar_chamada(self.payload);held=self.guard.used_today()
        with self.assertRaises(budget.BudgetError):
            self.account.uso({'prompt_tokens':3,'completion_tokens':10,
                             'prompt_tokens_details':{'cached_tokens':2,'cache_write_tokens':2}})
        self.account.fechar()
        self.assertEqual(self.guard.used_today(),held)

    def test_existing_global_group_user_guards_still_apply(self):
        for field,reason in [('cota_global_usd','global'),('cota_global_gratuito_usd','global_gratuito'),
                             ('cota_usuario_usd','usd_dia')]:
            old=getattr(self.cfg,field);setattr(self.cfg,field,0)
            with self.subTest(field=field), self.assertRaises(budget.BudgetError) as exc:
                self.new_account().iniciar_chamada(self.payload)
            self.assertEqual(exc.exception.bloqueado_por,reason)
            setattr(self.cfg,field,old)
        self.assertEqual(self.guard.used_today(),0)

    def test_uncertain_previous_call_cannot_start_another_tool_turn(self):
        self.account.iniciar_chamada(self.payload)
        with self.assertRaises(budget.BudgetError):self.account.iniciar_chamada(self.payload)
        self.assertEqual(len(self.guard.summary()),1)
        self.assertEqual(self.guard.summary()[0]['calls'],1)
        self.assertEqual(len(self.account.usos),1)

    def test_ledger_failure_can_resume_without_duplicating_completed_rows(self):
        for count in [184609,185000]:
            self.account.iniciar_chamada(self.payload)
            self.account.uso({'prompt_tokens':count,'completion_tokens':5})
        original=self.ledger.registrar
        attempts=[]
        def flaky(*args,**kwargs):
            attempts.append(args)
            if len(attempts)==2:raise OSError('fixture before write')
            return original(*args,**kwargs)
        self.ledger.registrar=flaky
        with self.assertRaises(OSError):self.account.fechar()
        self.assertFalse(self.account.closed)
        self.account.fechar();self.account.fechar()
        self.assertEqual(len(attempts),3)
        self.assertTrue(self.account.closed)


if __name__=='__main__':unittest.main()
