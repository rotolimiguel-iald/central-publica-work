"""Isolated pip installer; Windows curl HTTPS for PyPI file transport.

Python OpenSSL EOFs on files.pythonhosted.org on this host; Schannel curl
successfully verifies that same public endpoint. No TLS verification bypass.
"""
import io
import os
import pathlib
import subprocess
import sys
import tempfile
import zipfile
import hashlib
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parent
os.environ['PIP_CONFIG_FILE'] = os.devnull
from pip._internal.network.session import PipSession
from pip._vendor.requests import Response

original_send = PipSession.send

def public_send(self, request, **kwargs):
    if urlsplit(request.url).hostname != 'files.pythonhosted.org':
        return original_send(self, request, **kwargs)
    assert request.method in ('GET', 'HEAD')
    assert urlsplit(request.url).scheme == 'https'
    url = request.url
    metadata = url.endswith('.whl.metadata')
    if metadata:
        url = url[:-len('.metadata')]
    cache = ROOT / 'public_downloads'
    cache.mkdir(exist_ok=True)
    target = cache / hashlib.sha256(url.encode()).hexdigest()
    if not target.exists():
        partial = target.with_suffix('.part')
        cmd = ['curl.exe', '-q', '--fail', '--silent', '--show-error',
               '--location', '--proto', '=https', '--proto-redir', '=https',
               '--max-time', '600', '--output', str(partial), url]
        if request.method == 'HEAD':
            cmd.insert(2, '--head')
        subprocess.run(cmd, check=True)
        partial.replace(target)
    payload = target.read_bytes()
    if metadata:
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            name = next(n for n in archive.namelist() if n.endswith('.dist-info/METADATA'))
            payload = archive.read(name)
    response = Response()
    response.status_code = 200
    response.url = request.url
    response.request = request
    response.headers['Content-Length'] = str(len(payload))
    response.raw = io.BytesIO(payload)
    response._content = payload
    return response

PipSession.send = public_send
from pip._internal.cli.main import main
raise SystemExit(main(['--isolated', '--disable-pip-version-check', '--cache-dir',
                      str(ROOT / 'pip_cache'), 'install', '--index-url',
                      'https://pypi.org/simple', '--retries', '0', '--log',
                      str(ROOT / 'install_public.log'), *sys.argv[1:]]))
