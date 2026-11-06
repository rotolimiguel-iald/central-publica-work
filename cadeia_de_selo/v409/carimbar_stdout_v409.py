# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] o carimbador do stdout do rito: corpo da v408, rotulo v409
"""carimbar_stdout_v409.py -- [copia na cadeia v409, 05/11/2026, claude-construtor-v409: o corpo e' o do carimbador da v408 (sha16 do arquivo da v408, lido pelo adaptador: f6766bdbb3d3a45b); so' o rotulo da versao sobe no texto] o CARIMBADOR do stdout do rito (gerencia c1, 03/11/2026; pedido do gerente central do LAR para o filme em par; a v406 saiu sem ele).
Le o stdout do um.py em BYTES (stdin binario), grava-o IDENTICO em bytes no arquivo canonico (rodada_v409_stdout.txt) e, ao lado, um JSONL com uma linha por linha do stdout:
{"linha": n, "hora_utc": "...", "bytes": k}  (k = bytes da linha, inclusive o terminador), mais um registro final {"fim": true, "hora_utc", "linhas", "bytes_total", "sha256"} com o sha256 do
stdout ANTES do trailer RITO_RC (que o rito acrescenta depois). Nada e' decodificado, reencodado ou reordenado: o arquivo canonico sai byte a byte igual ao que o um.py escreveu. O carimbo e' o
instante em que a linha CHEGOU ao carimbador: com PYTHONUNBUFFERED=1 no ambiente do um.py (so' no subshell do rito), e' o instante em que o um.py a escreveu, a menos do pipe.
Fail-closed: se o arquivo gravado nao tiver os bytes recebidos, sai 3 (e o rito, com pipefail, le isso). Nunca toca o Nos fora dos dois arquivos que recebe por argumento.
uso (dentro do rito): echo 1 | python um.py 2>&1 | python -u carimbar_stdout_v409.py rodada_v409_stdout.txt rodada_v409_stdout_tempos.jsonl"""
import datetime, hashlib, json, os, sys

CHUNK = 65536


def agora():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def main(argv):
    if len(argv) != 3:
        sys.stderr.write("uso: carimbar_stdout_v409.py <stdout_canonico> <tempos.jsonl>\n"); return 2
    out_p, jl_p = argv[1], argv[2]
    h = hashlib.sha256(); n_lin = 0; total = 0; resto = b""
    with open(out_p, "wb") as out, open(jl_p, "w", encoding="utf-8", newline="\n") as jl:
        jl.write(json.dumps({"inicio": True, "hora_utc": agora(), "stdout": os.path.basename(out_p), "pid": os.getpid()}, ensure_ascii=False) + "\n"); jl.flush()
        src = sys.stdin.buffer
        while True:
            b = src.read1(CHUNK) if hasattr(src, "read1") else src.read(CHUNK)
            if not b:
                break
            out.write(b); out.flush(); h.update(b); total += len(b)   # os bytes vao ao canonico ANTES de qualquer carimbo: o arquivo cresce em tempo real, como antes
            t = agora(); resto += b
            while True:
                i = resto.find(b"\n")
                if i < 0:
                    break
                n_lin += 1; jl.write(json.dumps({"linha": n_lin, "hora_utc": t, "bytes": i + 1}, ensure_ascii=False) + "\n"); resto = resto[i + 1:]
            jl.flush()
        if resto:   # ultima linha sem terminador
            n_lin += 1; jl.write(json.dumps({"linha": n_lin, "hora_utc": agora(), "bytes": len(resto), "sem_terminador": True}, ensure_ascii=False) + "\n")
        jl.write(json.dumps({"fim": True, "hora_utc": agora(), "linhas": n_lin, "bytes_total": total, "sha256": h.hexdigest()}, ensure_ascii=False) + "\n"); jl.flush()
    # conferencia fail-closed: o arquivo canonico tem exatamente os bytes recebidos
    with open(out_p, "rb") as f:
        hh = hashlib.sha256(); k = 0
        while True:
            b = f.read(CHUNK)
            if not b:
                break
            hh.update(b); k += len(b)
    if k != total or hh.hexdigest() != h.hexdigest():
        sys.stderr.write("carimbador: o stdout gravado (%d B) difere do recebido (%d B)\n" % (k, total)); return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
