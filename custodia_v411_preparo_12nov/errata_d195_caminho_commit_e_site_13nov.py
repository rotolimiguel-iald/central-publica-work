# -*- coding: utf-8 -*-
"""D195 parte B (13/11/2026, claude-site-custodia; decisão da gerência c1, palavras exatas dela): a linha de caminho para as sete ressalvas
nas superfícies que mostram o resultado e não têm caminho nenhum.
(1) G1 textos.py: a mensagem do commit do espelho ganha, com o H0DN aberto, a linha EN como ÚLTIMA linha do corpo (antes do trailer
    Co-Authored-By, que o git exige no fim). A linha vai em UTF-8, exata (× e aspas curvas): o resto do corpo segue ASCII por convenção;
    o git recebe o arquivo por -F em UTF-8.
(2) site gerar_secoes.py: a seção 06 (o estatuto) ganha, com o H0DN aberto (lido do core selado do espelho), a linha EN logo depois da
    linha de estado EN e a PT logo depois da PT, com `ESTADO_ATUAL.md` em link para a URL que o TUNEL.json traz (gerada por script).
Edição por bytes; backup de cada arquivo; temporário; compilação; os arquivos têm de crescer; fim de linha preservado.
Uso: python -X utf8 <este> [PASTA_DA_G1] [ARQUIVO_gerar_secoes.py]"""
import os, sys, time

G1 = sys.argv[1] if len(sys.argv) > 1 else r"C:\IALD\Central de Patentes\tools\custodia_g1"
GS = sys.argv[2] if len(sys.argv) > 2 else r"C:\IALD\Site\tgl\v3.0_bancada\tools\gerar_secoes.py"
STAMP = time.strftime("%Y%m%d_%H%M%S")

TEXTOS = [
    ('def _commit_espelho(ctx, F, mods, nb, grupos, marcador, bd):\n',
     'def _commit_espelho(ctx, F, mods, nb, grupos, marcador, bd, caminho_h0dn=False):\n'),
    ('    corpo += ["", "PROVADA = validade; a creditacao segue recusada; o gate nao se moveu."]\n    if ctx.coautor:\n',
     '    corpo += ["", "PROVADA = validade; a creditacao segue recusada; o gate nao se moveu."]\n'
     '    if caminho_h0dn:   # AO LADO (13/11/2026, claude-site-custodia; D195 da gerencia c1): o caminho para as sete ressalvas, ultima linha do corpo (UTF-8, exata)\n'
     '        corpo += ["", h0dn.caminho_ressalvas("en")]\n'
     '    if ctx.coautor:\n'),
    ('    T.commit_espelho = Item(_commit_espelho(ctx, F, mods, nb, grupos, mk, bd), ',
     '    T.commit_espelho = Item(_commit_espelho(ctx, F, mods, nb, grupos, mk, bd, caminho_h0dn=bool(ab)), '),
]
SITE = [
    ("    for i, f in enumerate(cfg, 1):\n        assert f.get('aprovado') is True, 'fatia não aprovada pelo verificador: ' + f['slug']\n",
     "    # AO LADO (13/11/2026, claude-site-custodia; D195 da gerência c1, palavras exatas dela): com o H0DN aberto no core selado do espelho, a\n"
     "    # seção 06 (o estatuto) mostra o resultado; nenhuma superfície o mostra sem o caminho para as sete ressalvas. A linha é gerada, separada\n"
     "    # dos textos ratificados; o nome do arquivo vira o link que o TUNEL.json traz (URL gerada por script, nunca digitada).\n"
     "    from estatuto_tres_apoios import _h0dn_registro_aberto as _h0dn_ab\n"
     "    _h0dn_caminho = None\n"
     "    if _h0dn_ab(mundo.get('core') or {}):\n"
     "        assert 'ESTADO_ATUAL.md' in arq, 'ESTADO_ATUAL.md ausente do TUNEL.json (o link do caminho das sete ressalvas)'\n"
     "        _u_est = arq['ESTADO_ATUAL.md']['url']\n"
     "        _tit = 'The H0DN \\u00d7 BG1 test: the seven reservations and what the test does not decide'\n"
     "        _h0dn_caminho = {'en': 'The seven reservations and what the test does not decide: [`ESTADO_ATUAL.md`](%s), section \\u201c%s\\u201d.' % (_u_est, _tit),\n"
     "                         'pt': 'As sete ressalvas e o que o teste n\\u00e3o decide: [`ESTADO_ATUAL.md`](%s), se\\u00e7\\u00e3o \\u201c%s\\u201d.' % (_u_est, _tit)}\n"
     "    for i, f in enumerate(cfg, 1):\n        assert f.get('aprovado') is True, 'fatia não aprovada pelo verificador: ' + f['slug']\n"),
    ("            L += ['**Status, read from the core of %s by script (07/10/2026):** %s' % (versao, _E['linha_06_en']), '']\n",
     "            L += ['**Status, read from the core of %s by script (07/10/2026):** %s' % (versao, _E['linha_06_en']), '']\n"
     "            if _h0dn_caminho:   # AO LADO (13/11/2026, D195): o caminho para as sete ressalvas, logo depois do resultado\n"
     "                L += [_h0dn_caminho['en'], '']\n"),
    ("            L += ['**Estatuto, lido do core da %s por script (07/10/2026):** %s' % (versao, _E['linha_06_pt']), '']\n",
     "            L += ['**Estatuto, lido do core da %s por script (07/10/2026):** %s' % (versao, _E['linha_06_pt']), '']\n"
     "            if _h0dn_caminho:   # AO LADO (13/11/2026, D195)\n"
     "                L += [_h0dn_caminho['pt'], '']\n"),
]


def aplicar(P, eds, rot):
    b = open(P, "rb").read()
    crlf = b"\r\n" in b
    if crlf:
        assert b.count(b"\r\n") == b.count(b"\n"), "fim de linha misto em %s - PARAR" % P
    conv = (lambda s: s.replace("\n", "\r\n")) if crlf else (lambda s: s)
    pares = [(conv(a).encode("utf-8"), conv(d).encode("utf-8")) for a, d in eds]
    for a, _ in pares:
        assert b.count(a) == 1, "o trecho mudou em %s - PARAR: %r" % (P, a[:90])
    bak = P + ".bak_%s_%s" % (STAMP, rot)
    open(bak, "wb").write(b)
    assert open(bak, "rb").read() == b
    novo = b
    for a, d in pares:
        novo = novo.replace(a, d)
    compile(novo.decode("utf-8"), P, "exec")
    t = P + ".tmp_d195"
    open(t, "wb").write(novo)
    assert os.path.getsize(t) == len(novo) > len(b)
    os.replace(t, P)
    print("ok: %s %d -> %d (%s) | backup %s" % (os.path.basename(P), len(b), len(novo), "CRLF" if crlf else "LF", os.path.basename(bak)))


aplicar(os.path.join(G1, "textos.py"), TEXTOS, "d195_caminho")
aplicar(GS, SITE, "d195_caminho")
