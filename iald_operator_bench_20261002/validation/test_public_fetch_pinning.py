"""Real HTTP formatting over fake sockets; no DNS, TLS server or network."""
import ast
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import socket
import ssl
import sys
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch
from urllib.parse import urlparse, urljoin
import zlib
import ipaddress

HERE = Path(__file__).resolve().parent
STAGE = HERE.parent / 'stage'
path = STAGE / 'iald_public_fetch.py'
spec = importlib.util.spec_from_file_location('iald_public_fetch', path)
transport = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = transport
spec.loader.exec_module(transport)


def response(body=b'ok', status=200, extra=''):
    return (f'HTTP/1.1 {status} Test\r\nContent-Length: {len(body)}\r\n'
            f'Content-Type: text/plain; charset=utf-8\r\n{extra}\r\n').encode() + body


class FakeSocket:
    def __init__(self, raw, fail=False):
        self.raw = raw
        self.fail = fail
        self.sent = []
        self.closed = False
        self.address = None

    def settimeout(self, timeout):
        self.timeout = timeout

    def connect(self, address):
        self.address = address
        if self.fail:
            raise OSError('Synthetic connect failure')

    def sendall(self, data):
        self.sent.append(bytes(data))

    def makefile(self, mode):
        return io.BytesIO(self.raw)

    def close(self):
        self.closed = True


class PinningTests(unittest.TestCase):
    def setUp(self):
        self.sockets = []
        self.responses = [response()]
        self.failures = []
        self.resolutions = []
        self.answers = [['8.8.8.8']]
        self.tls_names = []
        self.tls_protocols = []
        self.tls_failure = False
        self.native_context = ssl.SSLContext
        self.stack = []
        for target, name, value in [
            (socket, 'socket', self.socket),
            (socket, 'getaddrinfo', lambda *a, **k: self.fail('Second DNS resolution')),
            (ssl, 'SSLContext', self.context),
        ]:
            item = patch.object(target, name, value)
            item.start()
            self.addCleanup(item.stop)

    def socket(self, family, kind):
        sock = FakeSocket(self.responses.pop(0), self.failures.pop(0) if self.failures else False)
        sock.family = family
        self.sockets.append(sock)
        return sock

    def context(self, protocol):
        actual = self.native_context(protocol)
        self.tls_protocols.append((protocol, actual.verify_mode, actual.check_hostname))
        def wrap(sock, server_hostname):
            self.tls_names.append(server_hostname)
            if self.tls_failure:
                raise ssl.SSLCertVerificationError('Synthetic invalid certificate')
            return sock
        return NS(load_default_certs=lambda: None,
                  set_alpn_protocols=lambda protocols: self.assertEqual(protocols, ['http/1.1']),
                  wrap_socket=wrap)

    def resolve(self, host, port):
        self.resolutions.append((host, port))
        return self.answers.pop(0)

    @staticmethod
    def allowed(address):
        ip = ipaddress.ip_address(address)
        return ip.is_global and not ip.is_multicast

    def get(self, url, headers=None):
        return transport.get_public(url, headers=headers or {'User-Agent': 'offline-audit'},
                                    timeout=3, resolve=self.resolve, is_public=self.allowed)

    def web(self):
        path = STAGE / 'iald_web_server.py'
        names = {'UrlRecusada', '_ip_publico', '_url_permitida', '_buscar_url_segura', '_ler_corpo_limitado'}
        nodes = [n for n in ast.parse(path.read_text(encoding='utf-8-sig')).body
                 if isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in names]
        env = dict(ipaddress=ipaddress, urlparse=urlparse, urljoin=urljoin,
                   _resolver_ips=self.resolve, FETCH_MAX_REDIRECIONAMENTOS=5,
                   FETCH_TETO_BYTES=2_000_000,
                   req_lib=NS(get=lambda *a, **k: self.fail('Unpinned requests path')))
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(path), 'exec'), env)
        return env

    def test_rebinding_resolves_once_then_connects_numeric_public_ip(self):
        self.answers = [['8.8.8.8'], ['127.0.0.1']]
        result = self.get('http://research.invalid:18765/api/universe/event')
        self.assertEqual(list(result.iter_content()), [b'ok'])
        result.close()
        self.assertEqual(self.resolutions, [('research.invalid', 18765)])
        self.assertEqual(self.sockets[0].address, ('8.8.8.8', 18765))
        self.assertIn(b'Host: research.invalid:18765\r\n', b''.join(self.sockets[0].sent))
        self.assertTrue(self.sockets[0].closed)

    def test_https_original_hostname_sni_verification_and_host(self):
        result = self.get('https://research.invalid:8443/a?b=1')
        result.close()
        self.assertEqual(self.tls_names, ['research.invalid'])
        self.assertEqual(self.tls_protocols, [(ssl.PROTOCOL_TLS_CLIENT, ssl.CERT_REQUIRED, True)])
        self.assertEqual(self.sockets[0].address, ('8.8.8.8', 8443))
        self.assertIn(b'Host: research.invalid:8443\r\n', b''.join(self.sockets[0].sent))

    def test_certificate_failure_sends_no_http_and_closes_socket(self):
        self.tls_failure = True
        with self.assertRaises(ssl.SSLCertVerificationError):
            self.get('https://research.invalid/')
        self.assertFalse(self.sockets[0].sent)
        self.assertTrue(self.sockets[0].closed)

    def test_ipv6_numeric_connect_and_bracketed_host(self):
        self.answers = [['2606:4700:4700::1111']]
        result = self.get('http://[2606:4700:4700::1111]:8080/')
        result.close()
        self.assertEqual(self.sockets[0].address, ('2606:4700:4700::1111', 8080, 0, 0))
        self.assertEqual(self.sockets[0].family, socket.AF_INET6)
        self.assertIn(b'Host: [2606:4700:4700::1111]:8080\r\n', b''.join(self.sockets[0].sent))

    def test_any_nonpublic_dns_answer_refuses_before_connect(self):
        for denied in ('127.0.0.1', '10.0.0.1', '169.254.169.254', '::1', '::ffff:127.0.0.1'):
            self.answers = [['8.8.8.8', denied]]
            with self.subTest(address=denied), self.assertRaises(transport.FetchRefused):
                self.get('http://research.invalid/')
        self.assertFalse(self.sockets)

    def test_malformed_url_or_credentials_refused_before_resolution(self):
        for url in ('file:///etc/passwd', 'http://user:password@research.invalid/',
                    'http://research.invalid:70000/', 'http://research.invalid:0/',
                    'http://research.invalid/\r\nInjected: value', 'http://[fe80::1%25eth0]/'):
            with self.subTest(url=url), self.assertRaises(transport.FetchRefused): self.get(url)
        self.assertFalse(self.sockets)
        self.assertFalse(self.resolutions)

    def test_environment_proxy_and_caller_auth_headers_are_not_forwarded(self):
        with patch.dict(os.environ, {'HTTP_PROXY': 'http://127.0.0.1:18765',
                                    'HTTPS_PROXY': 'http://127.0.0.1:18766',
                                    'ALL_PROXY': 'http://127.0.0.1:8082'}):
            result = self.get('http://research.invalid/', {'Host': '127.0.0.1',
                'Authorization': 'SYNTHETIC', 'Cookie': 'SYNTHETIC', 'Proxy-Authorization': 'SYNTHETIC'})
            result.close()
        sent = b''.join(self.sockets[0].sent)
        self.assertNotIn(b'SYNTHETIC', sent)
        self.assertIn(b'Host: research.invalid\r\n', sent)
        self.assertEqual(self.sockets[0].address[0], '8.8.8.8')

    def test_public_address_failover_only_before_request(self):
        self.answers = [['8.8.8.8', '1.1.1.1']]
        self.responses = [response(), response()]
        self.failures = [True, False]
        result = self.get('http://research.invalid/')
        result.close()
        self.assertFalse(self.sockets[0].sent)
        self.assertTrue(self.sockets[0].closed)
        self.assertEqual(self.sockets[1].address, ('1.1.1.1', 80))
        self.assertEqual(len(self.resolutions), 1)

    def test_redirect_to_loopback_is_refused_without_second_connection(self):
        self.responses = [response(status=302, extra='Location: http://127.0.0.1:18765/api/runs\r\n')]
        self.answers = [['8.8.8.8'], ['127.0.0.1']]
        env = self.web()
        with self.assertRaises(env['UrlRecusada']):
            env['_buscar_url_segura']('http://research.invalid/', {}, 3)
        self.assertEqual(len(self.sockets), 1)
        self.assertTrue(self.sockets[0].closed)

    def test_redirect_revalidates_same_host_and_preserves_https_identity(self):
        self.responses = [response(status=302, extra='Location: /next\r\n'), response()]
        self.answers = [['8.8.8.8'], ['1.1.1.1']]
        result, final = self.web()['_buscar_url_segura']('https://research.invalid/start', {}, 3)
        result.close()
        self.assertEqual(final, 'https://research.invalid/next')
        self.assertEqual(self.tls_names, ['research.invalid', 'research.invalid'])
        self.assertEqual([s.address[0] for s in self.sockets], ['8.8.8.8', '1.1.1.1'])
        self.assertTrue(all(s.closed for s in self.sockets))

    def test_gzip_and_deflate_decode_in_bounded_chunks(self):
        original = b'public data' * 12000
        for encoding, encoded in [('gzip', gzip.compress(original)),
                                  ('deflate', zlib.compress(original)),
                                  ('deflate', zlib.compress(original, wbits=-zlib.MAX_WBITS))]:
            with self.subTest(encoding=encoding, bytes=len(encoded)):
                self.responses = [response(encoded, extra=f'Content-Encoding: {encoding}\r\n')]
                self.answers = [['8.8.8.8']]
                result = self.get('http://research.invalid/')
                chunks = list(result.iter_content(1024))
                result.close()
                self.assertEqual(b''.join(chunks), original)
                self.assertLessEqual(max(map(len, chunks)), 1024)

    def test_existing_body_limit_encoding_and_close_contract(self):
        self.responses = [response(gzip.compress(b'x' * 3000000), extra='Content-Encoding: gzip\r\n')]
        env = self.web()
        result, _ = env['_buscar_url_segura']('http://research.invalid/', {}, 3)
        text = env['_ler_corpo_limitado'](result)
        self.assertGreaterEqual(len(text), 2_000_000)
        self.assertLess(len(text), 2_000_000 + 65536)
        self.assertTrue(self.sockets[0].closed)

    def test_unicode_url_path_and_idna_host(self):
        result = self.get('https://b\u00fccher.invalid/caf\u00e9 aberto?q=ma\u00e7\u00e3 verde')
        result.close()
        self.assertEqual(self.resolutions[0][0], 'xn--bcher-kva.invalid')
        self.assertEqual(self.tls_names[0], 'xn--bcher-kva.invalid')
        self.assertIn(b'/caf%C3%A9%20aberto?q=ma%C3%A7%C3%A3%20verde', b''.join(self.sockets[0].sent))


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PinningTests)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    print(json.dumps(dict(tests=result.testsRun, passed=result.wasSuccessful(),
        failures=[(str(t), message) for t, message in result.failures],
        errors=[(str(t), message) for t, message in result.errors], network=False,
        source_sha256={name:hashlib.sha256((STAGE/name).read_bytes()).hexdigest()
                       for name in ('iald_public_fetch.py','iald_web_server.py')})))
    sys.exit(not result.wasSuccessful())
