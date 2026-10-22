import ast
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from flask import Flask, Response

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
BASE = Path(os.environ.get('IALD_TESTE_BASE', ROOT))
sys.dont_write_bytecode = True
sys.path[:0] = [str(BASE), str(ROOT)]
import iald_motores as mt
import iald_orcamento as budget

class ModelTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.context = self.app.app_context()
        self.context.push()
        self.addCleanup(self.context.pop)
        names = {'_modelo_nativo_resposta','_identificar_resposta','_opcoes_de_motor'}
        tree = ast.parse((BASE/'iald_web_server.py').read_text(encoding='utf-8'))
        module = ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[])
        self.scope = {'json':json,'ACTIVE_MODEL_ID':'iald_nativa_v2_35b','iald_motores':mt,
                      'MOTORES_CFG':mt.Config(modelo='gpt-5.6-luna',modelo_operador='gpt-5.6-luna'),
                      '_motor_externo_indisponivel': lambda model: ''}
        exec(compile(module,'route_helpers','exec'),self.scope)

    def test_options_permissions_and_actual_labels(self):
        options = self.scope['_opcoes_de_motor']
        for account in ({'admin':True},{'acesso_nativa':True}):
            rows = options(account)
            self.assertEqual([r['id'] for r in rows],['nativa','openai'])
            self.assertEqual([r['rotulo'] for r in rows],['IALD Nativa · Qwen3.6-35B','ChatGPT 5.6 Luna'])
        self.assertEqual(options({}),[])
        self.assertEqual(options({'plano':'gratuito'}),[])
        self.assertNotIn('openai_sol',mt.MOTORES)

    def test_stream_has_server_model_and_original_chunks_unchanged(self):
        model = {'motor':'openai','id':'gpt-5.6-luna','rotulo':'ChatGPT 5.6 Luna'}
        original = [b'data: {"choices": [{"delta": {"content": "Hello"}}]}\n\n', b'data: [DONE]\n\n']
        result = self.scope['_identificar_resposta'](Response(iter(original),mimetype='text/event-stream'),model)
        chunks = list(result.response)
        self.assertEqual(json.loads(chunks[0].split(b'\n\n')[0][6:])['iald_modelo'],model)
        self.assertTrue(chunks[0].endswith(original[0]))
        self.assertEqual(chunks[1:],original[1:])
        self.assertEqual(len(chunks),len(original))

    def test_cancel_closes_provider_generator(self):
        closed = []
        def upstream():
            try:
                yield 'data: first\n\n'
                yield 'data: second\n\n'
            finally: closed.append(True)
        result = self.scope['_identificar_resposta'](Response(upstream(),mimetype='text/event-stream'),self.scope['_modelo_nativo_resposta']())
        stream = iter(result.response)
        next(stream); next(stream); stream.close()
        self.assertEqual(closed,[True])

    def test_json_model_and_errors_not_mislabeled(self):
        model = self.scope['_modelo_nativo_resposta']()
        response = Response(json.dumps({'choices':[{'message':{'content':'Hi'}}]}),mimetype='application/json')
        result = self.scope['_identificar_resposta'](response,model)
        self.assertEqual(result.get_json()['iald_modelo']['id'],'iald_nativa_v2_35b')
        error = Response('unavailable',status=503)
        self.assertIs(self.scope['_identificar_resposta'](error,model),error)
        self.assertEqual(error.get_data(),b'unavailable')

    def test_daily_costs_separate_models_and_include_reservations(self):
        with tempfile.TemporaryDirectory() as temp:
            now = [datetime(2026,9,15,12,tzinfo=timezone.utc)]
            guard = budget.SpendingGuard(Path(temp)/'costs.sqlite3',clock=lambda:now[0])
            k = guard.reserve('first','gpt-5.6-luna',.5,3,3); guard.settle(k,.2)
            guard.reserve('second','gpt-5.6-luna',.3,3,3)
            k = guard.reserve('first','test-model',.4,3,3); guard.settle(k,.1)
            rows = {r['model']:r for r in guard.by_model_today()}
            self.assertEqual(rows['gpt-5.6-luna']['usd'],.5)
            self.assertEqual(rows['test-model']['usd'],.1)
            self.assertAlmostEqual(sum(r['usd'] for r in rows.values()),guard.used_today())
            now[0] += timedelta(days=1)
            self.assertEqual(guard.by_model_today(),[])

    def test_tripled_caps_from_config_preserve_owner_global_rule(self):
        data = json.loads((Path(__file__).resolve().parent/'quota_values.json').read_text())
        cfg = mt.carregar_config(lambda key:data.get(key,''))
        self.assertEqual(cfg.cota_global_usd,3)
        self.assertEqual(cfg.cota_usuario_usd,.6)
        self.assertEqual(cfg.cota_global_gratuito_usd,2)
        for plan,day,month,usd in [('assinante',180000,2700000,.6),('gratuito',24000,180000,.06)]:
            limits = mt.limites_do_plano(cfg,plan)
            self.assertEqual((limits['tokens_dia'],limits['tokens_mes'],limits['usd_dia']),(day,month,usd))
        own = mt.config_da_conta(cfg,{'admin':True,'somente_limite_global':True})
        self.assertTrue(own.somente_limite_global)
        self.assertEqual(mt.limites_do_plano(own,'operador')['usd_dia'],3)

if __name__ == '__main__': unittest.main(verbosity=2)
