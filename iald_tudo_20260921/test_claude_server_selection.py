import unittest
from types import SimpleNamespace
from claude_server_selection import select_fields,selected_model,option_rows,config_for_model
from claude_profiles import HAIKU,SONNET

class SelectionTests(unittest.TestCase):
    def setUp(self):self.flags=dict(haiku_ready=True,sonnet_ready=True)
    def test_public_account_gets_only_haiku_without_native_grant(self):
        record={'plano':'gratuito'}
        self.assertEqual([o['id']for o in option_rows(record,'testador',**self.flags)],['claude-haiku'])
        fields=select_fields('claude-haiku',record,'testador',**self.flags)
        self.assertEqual(fields,{'motor':'claude','modelo_claude':HAIKU.model})
        self.assertEqual(record,{'plano':'gratuito'})
    def test_luiz_can_select_both_and_legacy_stays_sonnet(self):
        self.assertEqual(len(option_rows({'admin':True},'luiz',**self.flags)),2)
        self.assertEqual(selected_model({'motor':'claude'},'luiz',**self.flags),SONNET.model)
    def test_public_sonnet_forgery_rejected(self):
        with self.assertRaises(PermissionError):select_fields('claude-sonnet',{'admin':True},'other',**self.flags)
        with self.assertRaises(PermissionError):selected_model({'modelo_claude':SONNET.model},'other',**self.flags)
    def test_blocked_empty_and_missing_users_denied(self):
        for record in ({},{'bloqueado':{'em':'now'}},None):
            self.assertEqual(option_rows(record,'luiz',**self.flags),[])
    def test_unready_haiku_never_falls_back_to_sonnet(self):
        with self.assertRaises(PermissionError):
            select_fields('claude-haiku',{'admin':True},'luiz',haiku_ready=False,sonnet_ready=True)
    def test_config_copies_output_without_changing_quotas(self):
        cfg=SimpleNamespace(modelo=SONNET.model,modelo_operador=SONNET.model,max_saida=16000,
            max_saida_pensar=16000,janela=560000,sucessor_automatico=True,
            cota_global_usd=15,somente_limite_global=True,precos=lambda model:(1,.1,5,1.25))
        result=config_for_model(cfg,HAIKU.model)
        self.assertEqual(result.max_saida,4096);self.assertEqual(result.janela,200000)
        self.assertEqual(cfg.max_saida,16000);self.assertTrue(result.somente_limite_global)
        self.assertEqual(result.cota_global_usd,15)
    def test_no_price_blocks_model(self):
        with self.assertRaises(ValueError):config_for_model(SimpleNamespace(precos=lambda _:None),HAIKU.model)

if __name__=='__main__':unittest.main()
