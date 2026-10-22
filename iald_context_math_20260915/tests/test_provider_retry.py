import json
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import iald_motores as motor


class Response:
    def __init__(self, status=429, code='rate_limit_exceeded', headers=None, message='Rate limit reached'):
        self.status_code = status
        self.headers = headers or {}
        self.content = json.dumps({'error': {'code': code, 'message': message}}).encode()
        self.closed = False

    def close(self):
        self.closed = True

    def iter_lines(self, **kwargs):
        yield b'data: accepted'


class RetryTests(unittest.TestCase):
    def test_header_units_and_priority(self):
        for headers, expected in [({'Retry-After': '3.5'}, 3.75),
                                  ({'retry-after-ms':'1250'}, 1.5),
                                  ({'x-ratelimit-reset-tokens':'1m2.5s','x-ratelimit-reset-requests':'120ms'}, 62.75)]:
            r = Response(headers=headers)
            self.assertAlmostEqual(motor._espera_limite_provedor(r, motor.erro_de_resposta(r)), expected)

    def test_no_retry_for_quota_oversize_invalid_or_long_delay(self):
        for r in [Response(code='insufficient_quota',headers={'retry-after':'1'}),
                  Response(code='credit_balance_exhausted',headers={'retry-after':'1'}),
                  Response(message='Request too large',headers={'retry-after':'1'}),
                  Response(headers={'retry-after':'NaN'}), Response(headers={'retry-after':'121'}),
                  Response(status=500,headers={'retry-after':'1'})]:
            self.assertIsNone(motor._espera_limite_provedor(r, motor.erro_de_resposta(r)))

    def test_transient_retry_has_keepalives_and_closes_both_responses(self):
        first, second = Response(headers={'retry-after':'0'}), Response(status=200)
        with patch.object(motor, '_espera_limite_provedor', return_value=.015):
            responses = iter([first, second])
            events = list(motor.linhas_com_espera(lambda: next(responses), intervalo=.002))
        self.assertIn(('keepalive', None), events)
        self.assertIn(('linha', b'data: accepted'), events)
        self.assertTrue(first.closed and second.closed)

    def test_attempt_bound(self):
        responses = []
        def request():
            r = Response(headers={'retry-after':'0'})
            responses.append(r)
            return r
        with patch.object(motor, '_espera_limite_provedor', return_value=0):
            with self.assertRaises(motor.ErroProvedor):
                list(motor.linhas_com_espera(request, intervalo=.005))
        self.assertEqual(len(responses), 3)
        self.assertTrue(all(r.closed for r in responses))

    def test_cancel_while_waiting_prevents_another_request(self):
        calls = []
        def request():
            calls.append(1)
            return Response(headers={'retry-after':'30'})
        stream = motor.linhas_com_espera(request, intervalo=.005)
        self.assertEqual(next(stream), ('keepalive',None))
        stream.close()
        threading.Event().wait(.03)
        self.assertEqual(len(calls),1)

    def test_cancel_before_headers_reads_no_stream(self):
        arrived, release, closed = threading.Event(), threading.Event(), threading.Event()
        class LateResponse(Response):
            def close(self):
                super().close()
                closed.set()
            def iter_lines(self, **kwargs):
                raise AssertionError('Cancelled stream must not be read')
        response = LateResponse(status=200)
        def request():
            arrived.set()
            release.wait(1)
            return response
        stream = motor.linhas_com_espera(request, intervalo=.005)
        self.assertEqual(next(stream), ('keepalive', None))
        self.assertTrue(arrived.is_set())
        stream.close()
        release.set()
        self.assertTrue(closed.wait(1))

    def test_partial_stream_is_not_replayed(self):
        calls = []
        class Broken(Response):
            def iter_lines(self, **kwargs):
                yield b'data: first'
                raise ConnectionError('stream interrupted')
        def request():
            calls.append(1)
            return Broken(status=200)
        stream = motor.linhas_com_espera(request, intervalo=.01)
        self.assertEqual(next(stream), ('linha', b'data: first'))
        with self.assertRaises(ConnectionError):
            next(stream)
        self.assertEqual(len(calls),1)


if __name__ == '__main__':
    unittest.main()
