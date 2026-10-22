# -*- coding: utf-8 -*-
"""R2.1: no iald_web_server.py do candidato, nova tentativa curta e limitada nos os.replace/os.remove do heartbeat
(psion, health, rotação da telemetria) e remoção do tempário quando a troca falha. O psion é caminho OPACO: o
script não lê nem imprime nada do arquivo de estado; só envolve as trocas. Fins de linha CRLF preservados.
Nada do arquivo é impresso (ele carrega uma chave de API de produção)."""
from pathlib import Path

P = Path(__file__).resolve().parents[1] / 'candidato_r2_1' / 'C' / 'IALD' / 'projetos_pyhton' / 'IALD' / 'iald_web_server.py'
raw = P.read_bytes()
n_crlf, n_lf, n_cr = raw.count(b'\r\n'), raw.count(b'\n'), raw.count(b'\r')
assert n_crlf == n_lf == n_cr, 'fins de linha mistos'
s = raw.decode('utf-8').replace('\r\n', '\n')


def sub(old, new, count=1):
    global s
    assert s.count(old) == count, ('trecho não encontrado exatamente %d vez(es)' % count, old[:60])
    s = s.replace(old, new)


# 1) constante + helpers (antes de _load_psion_state)
sub('''HEARTBEAT_PSION_DAILY_BAK = True                      # uma cópia de bytes por dia: <psion>.bak_<AAAAMMDD> (D3c)
''', '''HEARTBEAT_PSION_DAILY_BAK = True                      # uma cópia de bytes por dia: <psion>.bak_<AAAAMMDD> (D3c)
HEARTBEAT_REPLACE_RETRY_S = 3.0                       # R2.1: espera máxima de uma troca/remoção do heartbeat
''')

sub('''def _load_psion_state():
''', '''def _heartbeat_retry(fn, *args):
    """R2.1 (13/10/2026, revisão R2 §3): os.replace/os.remove com nova tentativa curta e LIMITADA.

    Um leitor externo (antivírus em tempo real, indexador) que abre o arquivo sem FILE_SHARE_DELETE faz a troca
    falhar com PermissionError (WinError 5/32) por alguns milissegundos; a batida virava psion_error (+2 eventos
    na memória comum) e o tempário ficava órfão. Espera 10 ms, dobrando até 200 ms, por no máximo
    HEARTBEAT_REPLACE_RETRY_S segundos; depois a exceção sobe como antes (falha visível).
    """
    deadline = time.monotonic() + HEARTBEAT_REPLACE_RETRY_S
    delay = 0.01
    while True:
        try:
            return fn(*args)
        except PermissionError:
            if time.monotonic() >= deadline:
                raise
            time.sleep(delay)
            delay = min(delay * 2, 0.2)


def _heartbeat_discard_temp(path):
    """Remove o tempário que ESTA escrita criou e que nunca virou o arquivo (R2.1). Nunca levanta."""
    try:
        if os.path.exists(path):
            _heartbeat_retry(os.remove, path)
    except OSError as exc:
        print(f"[Heartbeat] tempário não removido ({type(exc).__name__}): {os.path.basename(path)}", flush=True)


def _load_psion_state():
''')

# 2) _save_psion_state: as duas trocas com nova tentativa; o tempário de uma troca que falhou é removido
sub('''            tmp_bak = bak + ".tmp_" + secrets.token_hex(4)
            with open(tmp_bak, "wb") as out:
                out.write(old)
                out.flush()
                os.fsync(out.fileno())
            with open(tmp_bak, "rb") as chk:
                if chk.read() != old:
                    os.remove(tmp_bak)
                    raise OSError("Psion daily byte copy did not verify")
            os.replace(tmp_bak, bak)
    tmp = target + ".tmp_" + secrets.token_hex(4)
    with open(tmp, "wb") as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    with open(tmp, "rb") as chk:
        if chk.read() != raw:
            os.remove(tmp)
            raise OSError("Psion state write did not verify")
    os.replace(tmp, target)
''', '''            tmp_bak = bak + ".tmp_" + secrets.token_hex(4)
            try:
                with open(tmp_bak, "wb") as out:
                    out.write(old)
                    out.flush()
                    os.fsync(out.fileno())
                with open(tmp_bak, "rb") as chk:
                    if chk.read() != old:
                        raise OSError("Psion daily byte copy did not verify")
                _heartbeat_retry(os.replace, tmp_bak, bak)          # R2.1: nova tentativa curta
            except BaseException:
                _heartbeat_discard_temp(tmp_bak)                     # R2.1: sem tempário órfão
                raise
    tmp = target + ".tmp_" + secrets.token_hex(4)
    try:
        with open(tmp, "wb") as out:
            out.write(raw)
            out.flush()
            os.fsync(out.fileno())
        with open(tmp, "rb") as chk:
            if chk.read() != raw:
                raise OSError("Psion state write did not verify")
        _heartbeat_retry(os.replace, tmp, target)                    # R2.1: nova tentativa curta
    except BaseException:
        _heartbeat_discard_temp(tmp)                                 # R2.1: sem tempário órfão
        raise
''')

# 3) rotação da telemetria
sub('''    oldest = f"{path}.{HEARTBEAT_TELEMETRY_KEEP}"
    if os.path.exists(oldest):
        os.remove(oldest)
    for i in range(HEARTBEAT_TELEMETRY_KEEP - 1, 0, -1):
        src = f"{path}.{i}"
        if os.path.exists(src):
            os.replace(src, f"{path}.{i + 1}")
    if os.path.exists(path):
        os.replace(path, f"{path}.1")
''', '''    oldest = f"{path}.{HEARTBEAT_TELEMETRY_KEEP}"
    if os.path.exists(oldest):
        _heartbeat_retry(os.remove, oldest)                          # R2.1: nova tentativa curta
    for i in range(HEARTBEAT_TELEMETRY_KEEP - 1, 0, -1):
        src = f"{path}.{i}"
        if os.path.exists(src):
            _heartbeat_retry(os.replace, src, f"{path}.{i + 1}")
    if os.path.exists(path):
        _heartbeat_retry(os.replace, path, f"{path}.1")
''')

# 4) health
sub('''    tmp = HEARTBEAT_HEALTH_FILE + ".tmp_" + secrets.token_hex(4)
    with open(tmp, "wb") as out:
        out.write(raw)
        out.flush()
        os.fsync(out.fileno())
    os.replace(tmp, HEARTBEAT_HEALTH_FILE)
''', '''    tmp = HEARTBEAT_HEALTH_FILE + ".tmp_" + secrets.token_hex(4)
    try:
        with open(tmp, "wb") as out:
            out.write(raw)
            out.flush()
            os.fsync(out.fileno())
        _heartbeat_retry(os.replace, tmp, HEARTBEAT_HEALTH_FILE)     # R2.1: nova tentativa curta
    except BaseException:
        _heartbeat_discard_temp(tmp)                                 # R2.1: sem tempário órfão
        raise
''')

out = s.replace('\n', '\r\n').encode('utf-8')
assert out.count(b'\r\n') == out.count(b'\n') == out.count(b'\r')
P.write_bytes(out)
print('ok bytes', len(raw), '->', len(out))
