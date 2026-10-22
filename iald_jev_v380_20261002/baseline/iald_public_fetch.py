"""Public GET transport: pin validated addresses without a second DNS lookup.

No requests Session, environment proxies, cookies, redirects, or HTTP retries.
The original hostname is retained for Host, SNI and certificate verification.
"""
import gzip
import http.client
import ipaddress
import socket
import ssl
from urllib.parse import quote, urlsplit
import zlib


class FetchRefused(ValueError):
    pass


def _target(url, resolve, is_public):
    if not isinstance(url, str) or any(ord(c) < 32 or ord(c) == 127 for c in url):
        raise FetchRefused('URL malformada')
    try:
        parsed = urlsplit(url)
        if parsed.scheme not in ('http', 'https'):
            raise FetchRefused('só http e https')
        if parsed.username is not None or parsed.password is not None:
            raise FetchRefused('URL com credencial')
        host = parsed.hostname
        if not host or '%' in host or '\\' in host or any(c.isspace() for c in host):
            raise FetchRefused('endereço inválido')
        host = host.encode('idna').decode('ascii')
        port = parsed.port if parsed.port is not None else (443 if parsed.scheme == 'https' else 80)
        if not 1 <= port <= 65535:
            raise FetchRefused('porta inválida')
        addresses = tuple(dict.fromkeys(str(ipaddress.ip_address(ip)) for ip in resolve(host, port)))
    except FetchRefused:
        raise
    except (OSError, ValueError, UnicodeError, TypeError) as exc:
        raise FetchRefused('endereço não resolvido ou inválido') from exc
    if not addresses or not all(is_public(ip) for ip in addresses):
        raise FetchRefused('endereço interno ou não público')
    path = quote(parsed.path or '/', safe="/%:@!$&'()*+,;=-._~")
    if parsed.query:
        path += '?' + quote(parsed.query, safe="/%?:@!$&'()*+,;=-._~[]")
    return parsed.scheme, host, port, addresses, path


def _connect(addresses, port, timeout):
    # Canonical numeric literals go directly to connect(), never getaddrinfo().
    # Address failover is allowed only before any HTTP request has been sent.
    last_error = None
    for address in addresses:
        ip = ipaddress.ip_address(address)
        family = socket.AF_INET6 if ip.version == 6 else socket.AF_INET
        connection = socket.socket(family, socket.SOCK_STREAM)
        try:
            connection.settimeout(timeout)
            target = (str(ip), port, 0, 0) if ip.version == 6 else (str(ip), port)
            connection.connect(target)
            return connection
        except OSError as exc:
            last_error = exc
            connection.close()
    raise last_error or OSError('No validated public address')


class _PinnedHTTP(http.client.HTTPConnection):
    def __init__(self, host, port, timeout, addresses):
        super().__init__(host, port=port, timeout=timeout)
        self.addresses = addresses

    def connect(self):
        self.sock = _connect(self.addresses, self.port, self.timeout)


class _PinnedHTTPS(_PinnedHTTP):
    default_port = 443

    def connect(self):
        # PROTOCOL_TLS_CLIENT enables CERT_REQUIRED and hostname verification.
        # Construct explicitly: create_default_context may enable SSLKEYLOGFILE.
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_default_certs()
        context.set_alpn_protocols(['http/1.1'])
        raw = _connect(self.addresses, self.port, self.timeout)
        try:
            self.sock = context.wrap_socket(raw, server_hostname=self.host)
        except BaseException:
            raw.close()
            raise


class PublicResponse:
    """Only the requests-compatible fields used by the public page reader."""
    def __init__(self, connection, response):
        self.connection = connection
        self.response = response
        self.status_code = response.status
        self.headers = response.headers
        self.encoding = response.headers.get_content_charset()
        if self.encoding is None and response.headers.get_content_type().startswith('text/'):
            self.encoding = 'ISO-8859-1'

    def close(self):
        try:
            self.response.close()
        finally:
            self.connection.close()

    def iter_content(self, chunk_size=65536):
        encoding = self.headers.get('Content-Encoding', '').strip().lower()
        if encoding in ('', 'identity', 'gzip', 'x-gzip'):
            stream = gzip.GzipFile(fileobj=self.response) if encoding in ('gzip', 'x-gzip') else self.response
            try:
                while data := stream.read(chunk_size):
                    yield data
            finally:
                if stream is not self.response:
                    stream.close()
        elif encoding == 'deflate':
            first = self.response.read(2)
            if len(first) < 2:
                raise OSError('Incomplete deflate response')
            wrapped = first[0] & 15 == 8 and int.from_bytes(first, 'big') % 31 == 0
            decoder = zlib.decompressobj(zlib.MAX_WBITS if wrapped else -zlib.MAX_WBITS)
            data = first
            while data:
                pending = data
                while pending:
                    decoded = decoder.decompress(pending, chunk_size)
                    pending = decoder.unconsumed_tail
                    if decoded:
                        yield decoded
                data = self.response.read(chunk_size)
            if not decoder.eof:
                raise OSError('Incomplete deflate response')
        else:
            raise OSError('Unrequested content encoding')


def get_public(url, *, headers, timeout, resolve, is_public):
    scheme, host, port, addresses, path = _target(url, resolve, is_public)
    connection_type = _PinnedHTTPS if scheme == 'https' else _PinnedHTTP
    connection = connection_type(host, port, timeout, addresses)
    # Only the fixed caller headers survive. Host is generated from the original
    # hostname, not the pinned IP; no ambient authentication or proxy is consulted.
    wire_headers = {k: v for k, v in headers.items() if k.lower() not in
                    {'host', 'connection', 'accept-encoding', 'authorization', 'proxy-authorization', 'cookie'}}
    wire_headers.update({'Accept-Encoding': 'gzip, deflate', 'Connection': 'close'})
    try:
        connection.request('GET', path, headers=wire_headers)
        return PublicResponse(connection, connection.getresponse())
    except BaseException:
        connection.close()
        raise
