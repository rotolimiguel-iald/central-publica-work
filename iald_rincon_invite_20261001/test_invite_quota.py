from pathlib import Path
import hashlib,json,sys,unittest
from datetime import datetime,timezone
from types import SimpleNamespace
W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
sys.path[:0]=[str(W/'stage'),str(R)]
import iald_motores as m
import iald_auto_router as router
from claude_server_selection import policy_for

class Ledger:
 def __init__(self,**overrides):
  self.state=dict(gasto_global=0,gasto_plano=0,gasto_conta=0,usd_dia_cota=0,tokens_dia=10**12,tokens_mes=10**13)
  self.state.update(overrides)
 def leitura_de_cota(self,*args):return self.state.copy()
 def relogio(self):return datetime.now(timezone.utc)
class Rate:
 def __init__(self,ok=True):self.ok=ok
 def permitir(self,u):return self.ok

class QuotaTests(unittest.TestCase):
 def setUp(self):
  self.base=m.carregar_config(lambda name,default='':default)
  self.record=dict(admin=False,plano=m.ASSINANTE,tokens_sem_limite=True,motor='automatico')
  self.cfg=m.config_da_conta(self.base,self.record)
 def permission(self,cfg=None,ledger=None,rate=None):
  return m.verificar_permissao(cfg or self.cfg,ledger or Ledger(),rate or Rate(),'acs.rincon',False,
   plano=m.ASSINANTE,chave_cota='acs.rincon',detalhado=True)
 def test_authorized_tokens_unlimited(self):
  self.assertTrue(self.permission()[0]);l=m.limites_do_plano(self.cfg,m.ASSINANTE)
  self.assertIsNone(l['tokens_dia']);self.assertIsNone(l['tokens_mes'])
 def test_ordinary_account_retains_quota(self):
  cfg=m.config_da_conta(self.base,dict(admin=False,plano=m.ASSINANTE))
  self.assertEqual(self.permission(cfg)[2],'tokens_dia')
 def test_flag_requires_boolean(self):
  for value in ['true',1,'1',None,False]:
   cfg=m.config_da_conta(self.base,dict(self.record,tokens_sem_limite=value))
   self.assertFalse(cfg.tokens_sem_limite)
 def test_blocked_not_exempt(self):
  for flag in ['bloqueado','acesso_bloqueado']:
   self.assertFalse(m.config_da_conta(self.base,dict(self.record,**{flag:True})).tokens_sem_limite)
 def test_global_money_limit_preserved(self):
  self.assertEqual(self.permission(ledger=Ledger(gasto_global=self.cfg.cota_global_usd))[2],'global')
 def test_individual_money_limit_preserved(self):
  lim=m.limites_do_plano(self.cfg,m.ASSINANTE)['usd_dia']
  self.assertEqual(self.permission(ledger=Ledger(usd_dia_cota=lim))[2],'usd_dia')
 def test_rate_limit_preserved(self):self.assertEqual(self.permission(rate=Rate(False))[2],'minuto')
 def test_state_has_null_not_infinity(self):
  state=m.estado_da_cota(self.cfg,Ledger(),'acs.rincon',m.ASSINANTE,'acs.rincon')
  self.assertIsNone(state['tokens_dia']['limite']);self.assertIsNone(state['tokens_mes']['limite'])
  self.assertIsNotNone(state['usd_dia']['limite']);json.dumps(state,allow_nan=False)
 def test_output_maximum_preserved(self):
  s=m.SaldoDoPedido(self.cfg,Ledger(),'acs.rincon',m.ASSINANTE,'acs.rincon',SimpleNamespace(usos=[]),0,lambda p:10000000)
  payload={'max_completion_tokens':4096};self.assertEqual(s.antes_da_chamada(payload),payload)
  self.assertEqual(payload['max_completion_tokens'],4096)
  with self.assertRaises(m.CotaEsgotada):s.antes_da_chamada({})
 def test_no_admin_or_manual_grant(self):
  self.assertFalse(self.cfg.somente_limite_global);self.assertFalse(self.record['admin'])
  self.assertTrue(router.default_for(self.record,'acs.rincon'))
  self.assertFalse(router.manual_allowed(self.record,'acs.rincon'))
 def test_base_immutable_and_other_account_recomputed(self):
  self.assertFalse(getattr(self.base,'tokens_sem_limite',False))
  self.assertFalse(m.config_da_conta(self.cfg,dict(admin=False)).tokens_sem_limite)

if __name__=='__main__':
 result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(QuotaTests))
 data=dict(passed=result.wasSuccessful(),tests=result.testsRun,paid_calls=0,
  stage_sha256=hashlib.sha256((W/'stage/iald_motores.py').read_bytes()).hexdigest())
 (W/'tests.json').write_bytes(json.dumps(data,indent=2).encode())
 sys.exit(0 if result.wasSuccessful() else 1)
