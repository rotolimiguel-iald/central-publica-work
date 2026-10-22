import unittest,json,tempfile,hashlib
from pathlib import Path
from test_public_budgets import PublicAccount,BudgetError,providers
class SharedBudget(unittest.TestCase):
    def test_deepseek_reserves_settles_and_shares_mimo_daily_limit(self):
        with tempfile.TemporaryDirectory() as tmp:
            key=hashlib.sha256(b'public-user').hexdigest()
            a=PublicAccount(tmp,key,.6,.7,2)
            body={'model':providers.MODELS['deepseek']['model'],'max_tokens':393216,'messages':[{'role':'user','content':'synthetic'}]}
            a.before('deepseek',body,50000)
            a.settle({'input_tokens':50000,'output_tokens':393216,'cached_tokens':0,'cost_estimate_usd':(50000*.3+393216*1.2)/1e6});a.close()
            b=PublicAccount(tmp,key,.6,.7,2)
            mimo={'model':providers.MODELS['mimo']['model'],'max_completion_tokens':131072,'messages':[]}
            with self.assertRaises(BudgetError):b.before('mimo',mimo,50000)
            b.close()
    def test_unknown_or_wrong_wire_limit_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            a=PublicAccount(tmp,hashlib.sha256(b'user').hexdigest(),1,2,3)
            for provider in ('deepseek','mimo'):
                body={'model':providers.MODELS[provider]['model'],'max_tokens':1,'max_completion_tokens':1}
                with self.assertRaises(BudgetError):a.before(provider,body,1000)
            with self.assertRaises(BudgetError):a.before('kimi',{},1000)
            a.close()
