# -*- coding: utf-8 -*-
"""O estatuto do H0DN aberto no E04 da G1 (12/11/2026, claude-site-custodia; de acordo da gerência c1, 12/11/2026). Edição por bytes de
dois arquivos CRLF, com backup de bytes, temporário, compilação conferida e crescimento:
  - espelho.py: o E04 chama h0dn.estatuto_e04 (os onze marcadores ESTATUTO_*, o remendo dos dois geradores e tools/estatuto_h0dn.json) com o
    registro aberto; a marca do E04 passa a contar «estatuto_h0dn»; o pré do E04 bloqueia marcador do H0DN ausente mesmo com --aceitar-molde;
  - textos.py: os onze marcadores ESTATUTO_* entram no que a E04 pede com o H0DN aberto.
Sem registro aberto no core da versão, nada muda."""
import os, time

G1 = r"C:\IALD\Central de Patentes\tools\custodia_g1"
STAMP = time.strftime("%Y%m%d_%H%M%S")
AO = "AO LADO (12/11/2026, claude-site-custodia; de acordo da gerencia c1)"

ESPELHO = [
    ("from . import nos, recibos, textos, util\n",
     "from . import nos, recibos, textos, util\nfrom . import h0dn   # " + AO + ": o teste H0DN x BG1 aberto\n"),
    ("    if not _historica(ctx):\n        m[\"CITATION\"] = (\"(%s on\" % v) in ctx.ler(c.TB / \"CITATION.cff\")\n    return m\n",
     "    if not _historica(ctx):\n        m[\"CITATION\"] = (\"(%s on\" % v) in ctx.ler(c.TB / \"CITATION.cff\")\n"
     "    if h0dn.registro_aberto(textos._core_da_versao(ctx)):   # " + AO + "\n"
     "        m[\"estatuto_h0dn\"] = h0dn.estatuto_marca_ok(c.TB, v)\n"
     "    return m\n"),
    ("    if a[\"faltam\"] and not ctx.aceitar_molde:\n        f.append(\"o handoff não traz estes marcadores",
     "    if a[\"faltam\"] and (not ctx.aceitar_molde or any(k.rsplit(\"_\", 1)[0] in h0dn.TODOS for k in a[\"faltam\"])):   # " + AO + ": o do H0DN nao tem molde\n"
     "        f.append(\"o handoff não traz estes marcadores"),
    ("    saidas = {}\n    gea = c.TB / \"tools\" / \"gerar_estado_atual.py\"\n",
     "    saidas = {}\n"
     "    ab_h = h0dn.registro_aberto(textos._core_da_versao(ctx))   # " + AO + ": os onze textos do estatuto\n"
     "    if ab_h:\n"
     "        try:\n"
     "            Vh = h0dn.valores(ab_h[1])\n"
     "        except ValueError as e:\n"
     "            raise Parar(str(e))\n"
     "        for k_, e_ in h0dn.estatuto_e04(c.TB, ctx.handoff.corpos, v, ab_h[0], Vh, T.conhecidos, ts).items():\n"
     "            saidas[\"h0dn:\" + k_] = e_\n"
     "    gea = c.TB / \"tools\" / \"gerar_estado_atual.py\"\n"),
]

TEXTOS = [
    ("            precisa.add(h0dn.MARCADOR_NOTA)\n",
     "            precisa.add(h0dn.MARCADOR_NOTA)\n"
     "            precisa |= set(h0dn.MARCADORES_ESTATUTO)   # " + AO + ": os onze textos do estatuto (E04)\n"),
]


def aplicar(nome, eds):
    P = os.path.join(G1, nome)
    b = open(P, "rb").read()
    assert b.count(b"\n") == b.count(b"\r\n") > 0, "%s não é todo CRLF" % nome
    pares = [(a.replace("\n", "\r\n").encode("utf-8"), d.replace("\n", "\r\n").encode("utf-8")) for a, d in eds]
    for a, _ in pares:
        assert b.count(a) == 1, "o trecho mudou em %s - PARAR: %r" % (nome, a[:90])
    bak = P + ".bak_%s_h0dn_estatuto" % STAMP
    open(bak, "wb").write(b)
    assert open(bak, "rb").read() == b
    novo = b
    for a, d in pares:
        novo = novo.replace(a, d)
    compile(novo.decode("utf-8"), P, "exec")
    assert novo.count(b"\n") == novo.count(b"\r\n"), "fim de linha misturado em %s" % nome
    t = P + ".tmp_errata"
    open(t, "wb").write(novo)
    assert os.path.getsize(t) == len(novo) > len(b)
    os.replace(t, P)
    print("ok:", nome, len(b), "->", len(novo), "| backup", os.path.basename(bak))


aplicar("espelho.py", ESPELHO)
aplicar("textos.py", TEXTOS)
