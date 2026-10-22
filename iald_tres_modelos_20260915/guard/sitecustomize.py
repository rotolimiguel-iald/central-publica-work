# -*- coding: utf-8 -*-
"""
Guarda de escrita e rede para rodar a suite antiga sem tocar arquivo real.

Carregada por PYTHONPATH em todo processo Python da rodada (inclusive filhos).
Bloqueia, na origem, via sys.addaudithook:
  * abrir arquivo para escrita/criacao fora da pasta temporaria do sistema;
  * renomear, substituir, apagar, criar pasta, truncar, copiar para fora dela;
  * sqlite3.connect em banco fora dela;
  * resolucao de nome e conexao para fora do loopback;
  * qualquer conexao a 127.0.0.1:8082 (servidor web real);
  * na porta 8081 (llama), qualquer pedido HTTP que nao seja GET (so leitura);
  * subprocess que mencione servidor, llama, taskkill ou Stop-Process.
Cada bloqueio vira uma linha JSON em GUARDA_LOG. Nada e impresso em stdout
(o teste MCP usa stdout como canal).
"""
import json
import os
import sys
import tempfile

_LOG = os.environ.get("GUARDA_LOG", "")
_PORTA_LEITURA = int(os.environ.get("GUARDA_PORTA_LEITURA", "8081"))
_PORTA_PROIBIDA = int(os.environ.get("GUARDA_PORTA_PROIBIDA", "8082"))
# sync2 (14/09 22h): a ordem diz NUNCA chamar :8081 nem :8082 -> as duas proibidas, inclusive GET.
_PORTAS_PROIBIDAS = {int(p) for p in os.environ.get("GUARDA_PORTAS_PROIBIDAS", "8081,8082").split(",") if p.strip()}
_PORTAS_PROIBIDAS.add(_PORTA_PROIBIDA)
_TEMP = os.path.normcase(os.path.abspath(tempfile.gettempdir()))
_LOOP = {"127.0.0.1", "localhost", "::1", "0.0.0.0"}
_W = os.O_WRONLY | os.O_RDWR | os.O_APPEND | os.O_CREAT | os.O_TRUNC
_dentro = [False]

_EVENTOS = {
    "open", "os.rename", "os.remove", "os.rmdir", "os.mkdir", "os.truncate",
    "os.link", "os.symlink", "os.chmod", "os.utime", "shutil.copyfile",
    "shutil.copytree", "shutil.rmtree", "shutil.move", "sqlite3.connect",
    "socket.connect", "socket.getaddrinfo", "socket.gethostbyname",
    "http.client.send", "subprocess.Popen", "os.startfile", "os.system",
}


def _registrar(evento, detalhe, bloqueado=True):
    if not _LOG:
        return
    try:
        _dentro[0] = True
        with open(_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "pid": os.getpid(), "script": os.path.basename(sys.argv[0] if sys.argv else "?"),
                "evento": evento, "bloqueado": bloqueado, "detalhe": str(detalhe)[:300],
            }, ensure_ascii=False) + "\n")
    except Exception:
        pass
    finally:
        _dentro[0] = False


def _no_temp(p):
    if p is None or isinstance(p, int):
        return True
    try:
        p = os.fsdecode(p)
    except Exception:
        return False
    if p.lower() in ("nul", "\\\\.\\nul", os.devnull.lower()):
        return True
    if p.startswith("\\\\.\\pipe\\"):
        return True
    try:
        a = os.path.normcase(os.path.abspath(p))
    except Exception:
        return False
    return a == _TEMP or a.startswith(_TEMP + os.sep)


def _negar(evento, detalhe, exc=PermissionError):
    _registrar(evento, detalhe)
    raise exc(13, "GUARDA DE TESTE: bloqueado " + evento, str(detalhe)[:200])


def _gancho(evento, args):
    if evento not in _EVENTOS or _dentro[0]:
        return
    if evento == "open":
        caminho, _modo, flags = args
        if isinstance(flags, int) and (flags & _W) and not _no_temp(caminho):
            _negar("open(escrita)", caminho)
    elif evento == "os.rename":
        if not (_no_temp(args[0]) and _no_temp(args[1])):
            _negar(evento, f"{args[0]} -> {args[1]}")
    elif evento in ("os.remove", "os.rmdir", "os.truncate", "os.chmod", "os.utime",
                    "shutil.rmtree"):
        if not _no_temp(args[0]):
            _negar(evento, args[0])
    elif evento == "os.mkdir":
        if not _no_temp(args[0]):
            try:
                existe = os.path.isdir(args[0])
            except Exception:
                existe = False
            if not existe:
                _negar(evento, args[0])
    elif evento in ("os.link", "os.symlink", "shutil.copyfile", "shutil.copytree",
                    "shutil.move"):
        if not _no_temp(args[1]) or (evento == "shutil.move" and not _no_temp(args[0])):
            _negar(evento, f"{args[0]} -> {args[1]}")
    elif evento == "sqlite3.connect":
        banco = args[0] if args else None
        nome = os.fsdecode(banco) if isinstance(banco, (str, bytes, os.PathLike)) else ""
        if nome not in ("", ":memory:") and not nome.startswith("file::memory:") \
                and not _no_temp(nome.split("?", 1)[0].replace("file:", "", 1)):
            _negar(evento, nome)
    elif evento in ("socket.getaddrinfo", "socket.gethostbyname"):
        host = args[0]
        if isinstance(host, bytes):
            host = host.decode("ascii", "replace")
        if host is not None and str(host).lower() not in _LOOP:
            _negar(evento, host, OSError)
    elif evento == "socket.connect":
        endereco = args[1]
        if isinstance(endereco, tuple) and len(endereco) >= 2:
            host, porta = str(endereco[0]).lower(), endereco[1]
            if host not in _LOOP:
                _negar(evento, endereco, ConnectionRefusedError)
            if porta in _PORTAS_PROIBIDAS:
                _negar(evento, endereco, ConnectionRefusedError)
    elif evento == "http.client.send":
        conexao, dados = args
        porta = getattr(conexao, "port", None)
        host = str(getattr(conexao, "host", "")).lower()
        if host not in _LOOP or porta in _PORTAS_PROIBIDAS:
            _negar("http(fora)", f"{host}:{porta}", ConnectionRefusedError)
        if porta == _PORTA_LEITURA:
            try:
                inicio = bytes(dados[:16]) if not isinstance(dados, str) else dados[:16].encode()
            except Exception:
                inicio = b""
            if not inicio.startswith(b"GET "):
                _negar("http(8081 nao-GET)", inicio.split(b"\r\n")[0][:60],
                       ConnectionRefusedError)
            _registrar("http(8081 GET)", inicio.split(b" ")[1][:60] if b" " in inicio else inicio,
                       bloqueado=False)
    elif evento in ("subprocess.Popen", "os.system", "os.startfile"):
        texto = " ".join(str(a) for a in args[:2]).lower()
        proibidos = ("iald_web_server", "llama", "taskkill", "stop-process", "start_iald",
                     "waitress", "restart_web", "shutdown")
        if any(p in texto for p in proibidos):
            _negar(evento, texto, PermissionError)
        _registrar(evento, texto[:200], bloqueado=False)


sys.addaudithook(_gancho)
