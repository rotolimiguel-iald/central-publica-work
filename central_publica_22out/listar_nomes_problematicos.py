# -*- coding: utf-8 -*-
"""SÓ LEITURA: num preparo, os arquivos que o git do Windows não consegue abrir por caminho normal — nome terminado em ponto ou espaço,
nome reservado (CON, NUL, COM0–9, LPT0–9…), caractere proibido — testando abrir cada um pelo caminho comum (sem o prefixo \\\\?\\)."""
import os, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RES = re.compile(r"(?i)^(con|prn|aux|nul|com[0-9¹²³]|lpt[0-9¹²³]|conin\$|conout\$)(\..*)?$")
for base in sys.argv[1:]:
    raiz = "\\\\?\\" + str(Path(base).resolve())
    ruins = []
    for dp, dns, fns in os.walk(raiz):
        dns[:] = [x for x in dns if x != ".git"]
        for f in fns:
            rel = os.path.relpath(os.path.join(dp, f), raiz).replace(os.sep, "/")
            partes = rel.split("/")
            if any(p.endswith((".", " ")) for p in partes) or any(RES.match(p) for p in partes) or re.search(r'[<>:"|?*\x00-\x1f]', rel):
                ruins.append(rel)
    print("%s: %d nomes problemáticos %s" % (Path(base).name, len(ruins), ruins[:8]))
