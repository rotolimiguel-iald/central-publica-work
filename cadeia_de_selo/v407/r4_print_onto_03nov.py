# -*- coding: utf-8 -*-
"""03/11/2026 17:36, gerencia c1 (R4 confinada): o print do rito (gerar_candidato_v407.py, patch N00_main_psion_canto) ainda rotulava a ponte Bell-TT como [KNOWN/ONTO]; todas as outras
superficies (pedra Par, delta, artigo PT/EN, README/handoff) ja' dizem [ONTO] desde a R2/R3, e o stdout do rito e' canonico. Uma palavra muda; nada mais. Troca em BYTES com backup
(o patches.aplicar_em_arquivo recusa troca que ENCOLHE o arquivo: e' ferramenta de errata aditiva), temporario + os.replace, py_compile depois. Decisao da gerencia em nome proprio: terceira
passada sobre este achado BAIXO porque a superficie e' canonica (dito no relatorio). Escrito pelo Write."""
import os, py_compile, time
ARQ = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407\gerar_candidato_v407.py"; TS = time.strftime("%Y%m%d_%H%M%S")
O = "[OPEN] o par na face de Fock; [KNOWN/ONTO] a ponte Bell-TT; os nomes das pedras sao do operador;".encode("utf-8")
N = "[OPEN] o par na face de Fock; [ONTO] a ponte Bell-TT; os nomes das pedras sao do operador;".encode("utf-8")
b = open(ARQ, "rb").read(); assert b.count(O) == 1, b.count(O)
novo = b.replace(O, N); assert b"KNOWN/ONTO" not in novo and len(novo) == len(b) - len(b"KNOWN/") and b.count(b"\r\n") == novo.count(b"\r\n")
bak = ARQ + ".bak_r4_print_onto_" + TS; open(bak, "xb").write(b); assert open(bak, "rb").read() == b
tmp = ARQ + ".tmp_" + TS; open(tmp, "xb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, ARQ); assert open(ARQ, "rb").read() == novo
py_compile.compile(ARQ, doraise=True)
print("gerar_candidato_v407.py: %d -> %d B; backup %s; py_compile ok" % (len(b), len(novo), os.path.basename(bak)))
