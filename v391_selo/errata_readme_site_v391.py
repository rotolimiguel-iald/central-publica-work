# -*- coding: utf-8 -*-
"""errata_readme_site_v391.py -- ERRATA AO LADO (07/10/2026, gerencia c1, em nome proprio): a cadeia da v391 escreveu, em 4 superficies, que o README e o
site com o estatuto da prova «foram preparados pela gerencia c1». Errado: quem os fez foi a sessao do site (modulo the_boundary/tools/estatuto_tres_apoios.py,
commit 978843f do espelho). O texto errado FICA; a errata entra na linha seguinte. Backup de BYTES; temporario -> conferir -> substituir; idempotente pelo marcador.
O commit e o modulo sao lidos do disco aqui (git e os bytes), nunca de memoria."""
import hashlib, os, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
UMEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
TB = r"C:\IALD\Artigo\the_boundary"
MARK = "<!-- errata_readme_site_v391_07out -->"
ALVOS = [os.path.join(NOS, "MEMORIA_DA_LINHAGEM.md"), os.path.join(NOS, "HANDOFF_v391_CUSTODIA.md"),
         os.path.join(UMEM, "central-de-patentes-estado.md"), os.path.join(UMEM, "handoff-v391-custodia.md")]
CHAVES = ["preparados pela gerência", "README e site preparados pela gerência"]
# o que se le do disco
log = subprocess.run(["git", "-C", TB, "log", "-1", "--format=%h|%ad|%s", "--date=format:%d/%m/%Y %H:%M", "978843f"], capture_output=True, text=True, encoding="utf-8")
assert log.returncode == 0 and log.stdout.strip(), "o commit 978843f nao esta no espelho -- nao escrevo"
h7, quando, assunto = log.stdout.strip().split("|", 2)
mod = os.path.join(TB, "tools", "estatuto_tres_apoios.py")
mod16 = hashlib.sha256(open(mod, "rb").read()).hexdigest()[:16]
TXT = ("> ⚠ **ERRATA AO LADO (07/10/2026, em nome próprio da gerência — sessão c1; a frase acima fica como registro):** o README e o site com o estatuto da prova "
       "NÃO foram preparados pela gerência c1 — a gerência não os tocou. Quem os fez foi a sessão do site, por um módulo único e fail-closed, "
       "`the_boundary/tools/estatuto_tres_apoios.py` (sha16 `%s`, lido do disco), no commit do espelho `%s` (%s, «%s») [REAL — lido do git]; a subida do site "
       "às 19:31 é [DECLARADO pela sessão do site, memória `confirmacao-e-creditacao-tres-apoios-07out.md`]. Essa frente saiu sobre a v390; na custódia da v391 o "
       "módulo é regenerado e pode recusar, porque o artigo v391 abre o resumo pelo estatuto, ganhou a seção «O estatuto da prova» e a errata ao lado das 8 frases "
       "de época. %s") % (mod16, h7, quando, assunto[:90], MARK)
feitos = []
for p in ALVOS:
    raw = open(p, "rb").read()
    if MARK.encode() in raw:
        print("JA ESTA (idempotente):", os.path.basename(p)); continue
    nl = b"\r\n" if b"\r\n" in raw else b"\n"
    linhas = raw.split(nl)
    idx = [i for i, l in enumerate(linhas) if any(c.encode("utf-8") in l for c in CHAVES)]
    assert len(idx) == 1, (os.path.basename(p), "linhas com a frase errada", len(idx))
    i = idx[0]
    prox_em_branco = (i + 1 >= len(linhas)) or linhas[i + 1].strip() == b""
    ins = [b"", TXT.encode("utf-8")] + ([] if prox_em_branco else [b""])
    novas = linhas[:i + 1] + ins + linhas[i + 1:]
    novo = nl.join(novas)
    assert len(novo) > len(raw)
    assert nl.join(novas[:i + 1] + novas[i + 1 + len(ins):]) == raw, "tirar a errata nao devolve o original"
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_errata_readme"
    assert not os.path.exists(bak)
    open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    tmp = p + ".tmp_errata_readme"; open(tmp, "wb").write(novo); assert open(tmp, "rb").read() == novo; os.replace(tmp, p)
    assert open(p, "rb").read() == novo
    feitos.append((os.path.basename(p), len(raw), os.path.getsize(p), nl == b"\r\n"))
for f in feitos:
    print("OK %-36s %9d -> %9d B %s" % (f[0], f[1], f[2], "CRLF" if f[3] else "LF"))
print("commit", h7, quando, "| modulo", mod16)
