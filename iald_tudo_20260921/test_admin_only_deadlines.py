import ast, sys, unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock,patch
from flask import Flask,jsonify
W=Path(__file__).resolve().parent
STAGE=W/'admin_only_deadlines_20260922_150455_620479'

class AdminOnlyTests(unittest.TestCase):
    def setUp(self):
        self.app=Flask('deadline_test');self.guard=Mock(return_value=None)
        self.snapshot=Mock(return_value={'items':[{'label':'fixture','expires_at':None}]})
        import os
        env={'app':self.app,'jsonify':jsonify,'require_admin':self.guard,'os':os,'SERVE_DIR':'fixture'}
        source=(STAGE/'iald_web_server.py').read_text(encoding='utf8')
        tree=ast.parse(source)
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('api_alertas','admin_prazos')]
        self.assertEqual(len(nodes),2)
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'staged_routes','exec'),env)
        self.fake=patch.dict(sys.modules,{'iald_deadlines':SimpleNamespace(snapshot=self.snapshot)})
        self.fake.start();self.addCleanup(self.fake.stop)
        self.client=self.app.test_client()

    def test_consumer_route_has_no_internal_data_even_for_operator(self):
        response=self.client.get('/api/alertas')
        self.assertEqual(response.json,{'alertas':[]});self.snapshot.assert_not_called()

    def test_administration_guard_runs_before_reading(self):
        self.guard.return_value=({'error':'denied'},403)
        response=self.client.get('/admin/api/prazos')
        self.assertEqual(response.status_code,403);self.snapshot.assert_not_called()

    def test_internal_panel_retains_dates_and_no_store(self):
        response=self.client.get('/admin/api/prazos')
        self.assertIn('prazos',response.json)
        self.assertEqual(response.headers['Cache-Control'],'no-store')
        source=(STAGE/'iald_web_server.py').read_text(encoding='utf8')
        self.assertIn("fetch('/admin/api/prazos'",source)

    def test_client_has_no_internal_alert_fetch_or_render(self):
        source=(STAGE/'app/iald.js').read_text(encoding='utf8')
        for word in ['renderDeadlines','/api/alertas','verificarAlertas','operational_deadlines.js']:
            self.assertNotIn(word,source)

if __name__=='__main__':unittest.main()
