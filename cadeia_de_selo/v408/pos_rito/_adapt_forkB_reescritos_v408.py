# -*- coding: utf-8 -*-
"""_adapt_forkB_reescritos_v408.py -- (claude-construtor-v408, fork B, 04/11/2026) os TRES arquivos do pos_rito que a v408 REESCREVE por inteiro (o corpo bumpado era o da v407, o psion):
registrar_mapa_v408.py, gerar_x_custodia_v408.py e textos_custodia_handoff_v408.py (nome de D52: `textos_custodia_handoff_v408.py`, sem sufixo de data; a subida mecanica o chamava textos_custodia_handoff_v408_03nov.py).
Dois passos, chamados pela gerencia na ordem:
  --backup : copia de BYTES de cada arquivo antigo para <arquivo>.bak_<TS>_adapt; o _03nov.py e' RENOMEADO para o seu .bak (nao fica duplicado: um arquivo so'); nada mais e' escrito.
  --crlf   : depois de os tres novos serem gravados (pelo Write, com LF), converte cada um para CRLF (o molde e' CRLF), confere ast.parse, imprime bytes antes -> depois e sha16. Idempotente.
Escrito pelo Write (o heredoc do Bash colapsa barras). Nada e' executado alem do ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")
NOVOS = ("registrar_mapa_v408.py", "gerar_x_custodia_v408.py", "textos_custodia_handoff_v408.py")
ANTIGO_RENOMEADO = "textos_custodia_handoff_v408_03nov.py"
s16 = lambda b: hashlib.sha256(b).hexdigest()[:16]


def backup():
    for n in ("registrar_mapa_v408.py", "gerar_x_custodia_v408.py"):
        p = os.path.join(HERE, n); raw = open(p, "rb").read()
        bk = p + ".bak_" + TS + "_adapt"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
        print("backup %-36s %7d B sha16 %s -> %s" % (n, len(raw), s16(raw), os.path.basename(bk)))
    p = os.path.join(HERE, ANTIGO_RENOMEADO)
    if os.path.exists(p):
        raw = open(p, "rb").read(); bk = p + ".bak_" + TS + "_adapt"
        os.replace(p, bk); assert open(bk, "rb").read() == raw and not os.path.exists(p)
        print("renomeado %-33s %7d B sha16 %s -> %s (o nome da v408 e' o de D52: textos_custodia_handoff_v408.py)" % (ANTIGO_RENOMEADO, len(raw), s16(raw), os.path.basename(bk)))
    else:
        print("aviso: %s nao existe (ja' renomeado?)" % ANTIGO_RENOMEADO)


def crlf():
    for n in NOVOS:
        p = os.path.join(HERE, n); raw = open(p, "rb").read()
        t = raw.decode("utf-8")
        ast.parse(t)
        novo = t.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8")
        if novo != raw:
            tmp = p + ".tmp_crlf"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, p); assert open(p, "rb").read() == novo
        print("%-36s %7d B -> %7d B (CRLF %d linhas) sha16 %s ast ok" % (n, len(raw), len(novo), novo.count(b"\r\n"), s16(novo)))


if __name__ == "__main__":
    if "--backup" in sys.argv:
        backup()
    elif "--crlf" in sys.argv:
        crlf()
    else:
        raise SystemExit("uso: --backup | --crlf")
