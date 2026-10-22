# -*- coding: utf-8 -*-
"""Biblioteca comum de implantar.py / reverter.py (conserto ACOM 12/10). Só stdlib.

Regras: hash sempre lido do artefato; cópia de BYTES conferida (tempário -> fsync -> conferência -> os.replace);
backup de bytes antes de tocar qualquer arquivo existente; nenhum apagamento (o que sai de lugar é renomeado ou
movido com sha256 conferido); recibo gravado após CADA passo; falha é visível e interrompe.
"""
from __future__ import annotations
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


class ImplantacaoError(RuntimeError):
    pass


def now_iso():
    return datetime.now(timezone.utc).isoformat()


def stamp():
    return datetime.now().strftime('%Y%m%d_%H%M%S_%f')


def sha256_file(path, chunk=1 << 22):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(chunk), b''):
            h.update(block)
    return h.hexdigest()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def stat_info(path):
    p = Path(path)
    if not p.exists():
        return {'path': str(p), 'exists': False}
    st = p.stat()
    return {'path': str(p), 'exists': True, 'bytes': st.st_size,
            'mtime': datetime.fromtimestamp(st.st_mtime).isoformat(timespec='milliseconds')}


def write_bytes_atomic(dst, data):
    """tempário -> fsync -> conferência de bytes -> os.replace. Nunca open(dst, 'w') direto."""
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + '.tmp_' + stamp())
    with open(tmp, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if tmp.read_bytes() != data:
        tmp.unlink()
        raise ImplantacaoError('tempário divergente: %s' % dst)
    os.replace(tmp, dst)
    if sha256_file(dst) != sha256_bytes(data):
        raise ImplantacaoError('conferência final divergente: %s' % dst)


def copy_file_verified(src, dst, chunk=1 << 22):
    """Cópia de bytes por blocos (arquivos grandes), fsync, sha256 da origem == sha256 do destino relido."""
    src, dst = Path(src), Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + '.part')
    h = hashlib.sha256()
    with open(src, 'rb') as fi, open(tmp, 'wb') as fo:
        for block in iter(lambda: fi.read(chunk), b''):
            h.update(block)
            fo.write(block)
        fo.flush()
        os.fsync(fo.fileno())
    digest = h.hexdigest()
    if sha256_file(tmp) != digest:
        os.replace(tmp, dst.with_name(dst.name + '.mismatch'))
        raise ImplantacaoError('cópia divergente: %s' % dst)
    os.replace(tmp, dst)
    return {'path': str(dst), 'bytes': dst.stat().st_size, 'sha256': digest}


def backup_bytes(target):
    """<arquivo>.bak_<stamp> na mesma pasta, por bytes, conferido. Devolve (caminho, sha256)."""
    target = Path(target)
    bak = target.with_name(target.name + '.bak_' + stamp())
    info = copy_file_verified(target, bak)
    return bak, info['sha256']


def mover_de_lado(path, sufixo):
    """Renomeia <path> -> <path>.<sufixo>_<stamp> (nunca apaga)."""
    path = Path(path)
    dest = path.with_name(path.name + '.' + sufixo + '_' + stamp())
    os.replace(path, dest)
    return dest


def write_json_atomic(path, payload):
    write_bytes_atomic(path, (json.dumps(payload, ensure_ascii=False, indent=1, default=str) + '\n').encode('utf-8'))


def run_python(args, cwd=None, timeout=3600, env=None):
    """Subprocesso Python (o mesmo interpretador), saída capturada; devolve dict com rc/stdout/stderr."""
    e = dict(os.environ)
    e.update(PYTHONUTF8='1', PYTHONIOENCODING='utf-8', PYTHONDONTWRITEBYTECODE='1')
    if env:
        e.update(env)
    t0 = time.time()
    proc = subprocess.run([sys.executable, '-X', 'utf8'] + [str(a) for a in args], cwd=cwd, env=e,
                          capture_output=True, timeout=timeout)
    return {'args': [str(a) for a in args], 'returncode': proc.returncode, 'seconds': round(time.time() - t0, 3),
            'stdout': proc.stdout.decode('utf-8', 'replace'), 'stderr': proc.stderr.decode('utf-8', 'replace')[-4000:]}


def run_powershell(script_text, timeout=180):
    """PowerShell 5.1 sem perfil; só usado quando a configuração pede gestão de processos."""
    t0 = time.time()
    proc = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass', '-Command', script_text],
                          capture_output=True, timeout=timeout)
    return {'returncode': proc.returncode, 'seconds': round(time.time() - t0, 3),
            'stdout': proc.stdout.decode('utf-8', 'replace'), 'stderr': proc.stderr.decode('utf-8', 'replace')[-2000:]}


def listar_processos_web(app_root):
    """Lista (só leitura) os processos do web server e dos supervisores. Devolve dict."""
    web_script = str(Path(app_root) / 'iald_web_server.py').replace('\\', '\\\\')
    ps = (
        "$w=@(Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | Where-Object { $_.CommandLine -match 'iald_web_server\\.py' } "
        "| Select-Object ProcessId,ParentProcessId,CreationDate,CommandLine);"
        "$s=@(Get-CimInstance Win32_Process -Filter \"name='powershell.exe'\" | Where-Object { $_.CommandLine -and $_.CommandLine -match 'start_iald_web\\.ps1' } "
        "| Select-Object ProcessId,ParentProcessId,CreationDate);"
        "$l=@(Get-NetTCPConnection -LocalPort 8082 -State Listen -ErrorAction SilentlyContinue | Select-Object OwningProcess);"
        "@{web=$w;supervisores=$s;listen8082=$l} | ConvertTo-Json -Depth 4 -Compress"
    )
    r = run_powershell(ps)
    try:
        data = json.loads(r['stdout']) if r['stdout'].strip() else {}
    except ValueError:
        data = {'raw': r['stdout'][-1000:]}
    for k in ('web', 'supervisores', 'listen8082'):
        v = data.get(k)
        if v is None:
            data[k] = []
        elif isinstance(v, dict):
            data[k] = [v]
    data['powershell_rc'] = r['returncode']
    return data


def parar_app(app_root, esperar_s=40):
    """Chama stop_iald_web.ps1 (supervisor primeiro, depois o filho; nunca mata outros serviços) e espera."""
    script = Path(app_root) / 'stop_iald_web.ps1'
    if not script.exists():
        raise ImplantacaoError('stop_iald_web.ps1 não encontrado em %s' % app_root)
    r = run_powershell('& "%s"' % str(script), timeout=120)
    t0 = time.time()
    while time.time() - t0 < esperar_s:
        procs = listar_processos_web(app_root)
        if not procs['web'] and not procs['supervisores'] and not procs['listen8082']:
            return {'stop_script': r, 'depois': procs, 'parado': True, 'segundos': round(time.time() - t0, 1)}
        time.sleep(2)
    return {'stop_script': r, 'depois': listar_processos_web(app_root), 'parado': False, 'segundos': esperar_s}


def iniciar_app(app_root, esperar_s=90):
    """Sobe o supervisor (start_iald_web.ps1) desacoplado e espera a porta 8082 e /login 200 (loopback)."""
    script = Path(app_root) / 'start_iald_web.ps1'
    if not script.exists():
        raise ImplantacaoError('start_iald_web.ps1 não encontrado em %s' % app_root)
    ps = ("Start-Process -FilePath powershell.exe -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File','%s') "
          "-WorkingDirectory '%s' -WindowStyle Hidden; 'started'") % (str(script), str(app_root))
    r = run_powershell(ps, timeout=60)
    t0 = time.time()
    status = None
    while time.time() - t0 < esperar_s:
        procs = listar_processos_web(app_root)
        if procs['listen8082'] and procs['web']:
            try:
                import urllib.request
                with urllib.request.urlopen('http://127.0.0.1:8082/login', timeout=3) as resp:
                    status = resp.status
            except Exception as exc:  # noqa: BLE001 - registrado, tentamos de novo
                status = repr(exc)
            if status == 200:
                return {'start': r, 'depois': procs, 'login_http': 200, 'ok': True, 'segundos': round(time.time() - t0, 1)}
        time.sleep(3)
    return {'start': r, 'depois': listar_processos_web(app_root), 'login_http': status, 'ok': False, 'segundos': esperar_s}


def sqlite_schema_version(db_path):
    conn = sqlite3.connect('file:%s?mode=ro' % Path(db_path).as_posix(), uri=True, timeout=30)
    try:
        row = conn.execute("SELECT value FROM metadata WHERE key='schema_version'").fetchone()
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        contexts = conn.execute('SELECT count(*) FROM contexts').fetchone()[0] if 'contexts' in tables else None
        events = conn.execute('SELECT count(*) FROM events').fetchone()[0] if 'events' in tables else None
        jm = conn.execute('PRAGMA journal_mode').fetchone()[0]
        return {'schema_version': row[0] if row else None, 'tables': tables, 'contexts': contexts, 'events': events,
                'journal_mode': jm}
    finally:
        conn.close()


def sqlite_writer_probe(db_path, timeout_s=30):
    """BEGIN IMMEDIATE e ROLLBACK: prova que ninguém segura escrita no banco (fail-closed se ocupado)."""
    conn = sqlite3.connect(str(db_path), timeout=timeout_s, isolation_level=None)
    try:
        conn.execute('PRAGMA busy_timeout=%d' % (timeout_s * 1000))
        conn.execute('BEGIN IMMEDIATE')
        conn.execute('ROLLBACK')
        return True
    finally:
        conn.close()


def disk_free(path):
    p = Path(path)
    while not p.exists() and p.parent != p:
        p = p.parent
    if not p.exists():
        return None
    return shutil.disk_usage(str(p)).free


def mapear(caminho_producao, raizes):
    """Traduz um caminho de produção para o alvo real pelo mapa de raízes (produção = identidade)."""
    norm = str(caminho_producao)
    for prod_root, real_root in sorted(raizes.items(), key=lambda kv: -len(kv[0])):
        if norm.lower().startswith(prod_root.lower().rstrip('\\') + '\\') or norm.lower() == prod_root.lower():
            rest = norm[len(prod_root.rstrip('\\')):].lstrip('\\')
            return Path(real_root) / rest if rest else Path(real_root)
    raise ImplantacaoError('caminho fora das raízes mapeadas: %s' % norm)
