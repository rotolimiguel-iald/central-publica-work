"""Synthetic limiter tests ONLY; no production/provider/credential integration."""
import contextlib
from decimal import Decimal
import io
import json
import socket
import sys
import threading
import unittest
from unittest.mock import patch
sys.dont_write_bytecode=True
def blocked(*a,**k):raise AssertionError('Network forbidden')
socket.create_connection=blocked;socket.socket.connect=blocked;socket.socket.connect_ex=blocked
import haiku_smoke_review as h

class SyntheticGuard:
    """Deliberately not SpendingGuard; captures calls without touching any ledger."""
    def __init__(self,factor=1):self.rows={};self.settled=[];self.factor=factor
    def check(self,*a,**k):pass
    def reserve(self,user,model,cap,user_limit,global_limit,**kw):
        key=str(len(self.rows)+1)
        self.rows[key]={'cap':float(Decimal(str(cap))*Decimal(str(self.factor))),
                        'user_limit':user_limit,'global_limit':global_limit,'kwargs':kw}
        return key
    def settle(self,*a):self.settled.append(a)

def limiter(factor=1):
    g=SyntheticGuard(factor);return h.SmokeGuard(g,read_cap=lambda key:g.rows[key]['cap']),g
def reserve(l,cap=.325,**kw):
    return l.reserve('luiz',h.MODEL,cap,15,15,quota_key='fixture',**kw)

class SmokeTests(unittest.TestCase):
    def test_dry_default_no_import_root_or_network(self):
        out=io.StringIO()
        with patch.object(sys,'argv',['harness']),patch.object(h.importlib,'import_module',side_effect=AssertionError('ROOT import forbidden')),contextlib.redirect_stdout(out):
            self.assertEqual(h.main(),0)
        data=json.loads(out.getvalue());self.assertEqual(data['status'],'DRY_RUN')
        self.assertEqual(data['generation_calls'],0)

    def test_execute_cli_blocked_no_spend(self):
        out=io.StringIO()
        with patch.object(sys,'argv',['harness','--execute']),patch.object(h.importlib,'import_module',side_effect=AssertionError('ROOT import forbidden')),contextlib.redirect_stdout(out):
            self.assertEqual(h.main(),2)
        self.assertEqual(json.loads(out.getvalue())['network_calls'],0)

    def test_specific_approval_required_before_server_access(self):
        with self.assertRaisesRegex(h.SmokeBlocked,'approval'):
            h.run_in_server(object(),execution_id='fixture_123')

    def test_per_call_before_delegate(self):
        for cap in (.325001,float('inf'),float('nan'),-1,True):
            l,g=limiter()
            with self.assertRaises((h.SmokeBlocked,ValueError)):reserve(l,cap)
            self.assertEqual(g.rows,{})

    def test_two_calls_total_and_quotas_unchanged(self):
        l,g=limiter();reserve(l);reserve(l)
        self.assertEqual(l.gross,Decimal('.65'))
        with self.assertRaises(h.SmokeBlocked):reserve(l,.01)
        self.assertEqual(len(g.rows),2)
        for row in g.rows.values():
            self.assertEqual(row['user_limit'],15);self.assertEqual(row['global_limit'],15)

    def test_parallel_attempts_at_most_two(self):
        l,g=limiter();errors=[]
        def call():
            try:reserve(l)
            except h.SmokeBlocked:errors.append(True)
        ts=[threading.Thread(target=call) for _ in range(8)]
        for t in ts:t.start()
        for t in ts:t.join()
        self.assertEqual(len(g.rows),2);self.assertEqual(len(errors),6)

    def test_free_refusal_does_not_replenish_test_allowance(self):
        l,g=limiter();key=reserve(l);l.settle(key,0);reserve(l)
        with self.assertRaises(h.SmokeBlocked):reserve(l)
        self.assertEqual(l.gross,Decimal('.65'))

    def test_uncertain_hold_delegates_without_partial_discount(self):
        l,g=limiter();key=reserve(l);l.settle(key)
        self.assertEqual(g.settled,[(key,None)])
        with self.assertRaises(h.SmokeBlocked):l.settle(key,estimate=.01)

    def test_guard_safety_factor_releases_before_send_and_stops(self):
        l,g=limiter(2)
        with self.assertRaises(h.SmokeBlocked):reserve(l,.20)
        self.assertEqual(g.settled,[('1',0)])
        self.assertTrue(l.stopped)
        with self.assertRaises(h.SmokeBlocked):reserve(l,.10)

    def test_provider_overage_recorded_but_blocks_next_call(self):
        l,g=limiter();key=reserve(l,.2);l.settle(key,.21)
        self.assertEqual(g.settled,[(key,.21)]);self.assertTrue(l.stopped)
        with self.assertRaises(h.SmokeBlocked):reserve(l,.1)

    def test_wrong_global_or_identity_rejected(self):
        l,g=limiter()
        for user,model,total in [('other',h.MODEL,15),('luiz','other',15),('luiz',h.MODEL,16)]:
            with self.assertRaises(h.SmokeBlocked):l.reserve(user,model,.1,15,total)
        self.assertEqual(g.rows,{})

if __name__=='__main__':unittest.main()
