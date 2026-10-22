from pathlib import Path
W=Path(__file__).resolve().parent
OLD=W.parent/'iald_app_models_20260930'
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
for name in ['test_evaluation.py','test_routes.py']:
    s=(OLD/name).read_text('utf-8')
    if name=='test_evaluation.py':
        s=s.replace('sys.path.insert(0,str(ROOT))', "sys.path[:0]=[str(ROOT),r'C:\\IALD\\projetos_pyhton\\IALD']")
        start=s.index('    def test_only_operator(');end=s.index('    def test_consent_separation',start)
        s=s[:start]+'''    def test_provider_access_matrix(self):
        for name in ('luiz','alanacaroline','liana'):
            for provider in p.MODELS:
                self.assertTrue(p.allowed({'admin':False},name,provider))
        for name in ('guest','iald_beta','Luiz'):
            self.assertTrue(p.allowed({'plano':'gratuito'},name,'mimo'))
            for provider in ('kimi','deepseek'):
                self.assertFalse(p.allowed({'admin':True},name,provider))
        for provider in p.MODELS:
            for record in ({},{'bloqueado':True},{'acesso_bloqueado':True}):
                self.assertFalse(p.allowed(record,'luiz',provider))
        self.assertFalse(p.allowed({'admin':True},'guest','unknown'))
        for name in ('alanacaroline','liana','guest'):
            with self.assertRaises(PermissionError):
                select_fields('claude-sonnet',{'admin':False},name,haiku_ready=True,sonnet_ready=True)

'''+s[end:]
    else:
        s=s.replace("sys.path.insert(0,str(Path(__file__).parent/'stage'))", "sys.path[:0]=[str(Path(__file__).parent/'stage'),r'C:\\IALD\\projetos_pyhton\\IALD']")
        s=s.replace("for provider in providers.MODELS:\n            self.assertEqual(self.select(provider).status_code,403)", "for provider in ('kimi','deepseek'):\n            self.assertEqual(self.select(provider).status_code,403)")
        pos=s.index('    def test_consent_stale_and_revoke')
        s=s[:pos]+'''    def test_public_mimo_still_needs_own_consent(self):
        self.login('guest')
        self.assertEqual(self.select('mimo').status_code,200)
        data={'messages':[{'role':'user','content':'oi'}],'stream':True}
        self.assertEqual(self.client.post('/v1/chat/completions',json=data).get_json()['iald_aviso']['tipo'],'consentimento_ia')
        self.assertFalse(self.sent)
        self.assertEqual(self.consent('mimo').status_code,200)
        self.assertEqual(self.client.post('/v1/chat/completions',json=data).status_code,200)
        self.assertEqual(len(self.sent),1)
        self.assertIn('account_key',self.sent[0][1])

    def test_family_access_and_guest_forgery(self):
        for user in ('alanacaroline','liana'):
            self.users[user]={'admin':False,'motor':'openai'};self.login(user)
            for provider in providers.MODELS:
                self.assertEqual(self.select(provider).status_code,200)
            self.assertEqual(self.client.get('/admin/api/avaliacao-modelos').status_code,403)

'''+s[pos:]
    (W/name).write_text(s,encoding='utf-8')
print('Test fixtures prepared')
