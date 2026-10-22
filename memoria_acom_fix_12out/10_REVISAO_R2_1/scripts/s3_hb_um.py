# -*- coding: utf-8 -*-
"""Roda UMA vez o teste ORIGINAL test_sixty_beats_in_process_zero_or_one_memory_event (nao alterado) e separa o
resultado do CORPO do teste do resultado do tearDown: envolve HeartbeatD3Tests.tearDown so para registrar
self._outcome.success (o veredito do corpo ANTES do tearDown) e a excecao do tearDown, se houver; depois chama o
tearDown original. Imprime uma linha JSON. Uso: python s3_hb_um.py <pasta hb/tests>"""
import json
import sys
import traceback
import unittest

HB = sys.argv[1]
sys.path.insert(0, HB)
import test_heartbeat_v2 as T  # noqa: E402

info = {'corpo_ok': None, 'teardown_exc': None}
orig = T.HeartbeatD3Tests.tearDown


def td(self):
    # o corpo ja terminou: uma falha dele ja foi registrada no TestResult (o _outcome.success e reiniciado a True
    # pelo executor do tearDown, por isso nao serve)
    oc = getattr(self, '_outcome', None)
    r = getattr(oc, 'result', None)
    info['corpo_ok'] = (len(r.failures) + len(r.errors) == 0) if r is not None else None
    try:
        orig(self)
    except BaseException as exc:  # noqa: BLE001
        info['teardown_exc'] = type(exc).__name__ + ': ' + str(exc)[:160]
        raise


T.HeartbeatD3Tests.tearDown = td
suite = unittest.TestSuite([T.HeartbeatD3Tests('test_sixty_beats_in_process_zero_or_one_memory_event')])
res = unittest.TestResult()
suite.run(res)
msgs = [tb.strip().splitlines()[-1][:200] for _, tb in res.failures + res.errors]
onde = ['tearDown' if 'in tearDown' in tb else 'corpo' for _, tb in res.failures + res.errors]
print(json.dumps({'ok': res.wasSuccessful(), 'corpo_ok': info['corpo_ok'], 'teardown_exc': info['teardown_exc'],
                  'n_fail': len(res.failures), 'n_error': len(res.errors), 'msgs': msgs, 'onde': onde}, ensure_ascii=False))
