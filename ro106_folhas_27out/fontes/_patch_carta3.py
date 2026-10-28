import pathlib
F = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
p = F / 'carta.py'
s = p.read_text(encoding='utf-8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:80], s.count(a))
    s = s.replace(a, b)


# 3(c) parametrizado (MQC fica com o texto de sempre: congelado)
rep("(c) todos os números, letras e sinais de referência com altura mínima de 0,32 cm; (d) %s; (e) folhas A4 com as margens da Regra 11.6, sem molduras; (f) disposição das figuras e dos painéis nas folhas, e número de folhas, ajustados ao tamanho das letras. %s\\n' % (d['comum_d'], d['extra']))",
    "(c) %s; (d) %s; (e) folhas A4 com as margens da Regra 11.6, sem molduras; (f) disposição das figuras e dos painéis nas folhas, e número de folhas, ajustados ao tamanho das letras. %s\\n' % (d.get('comum_c', 'todos os números, letras e sinais de referência com altura mínima de 0,32 cm'), d['comum_d'], d['extra']))")
rep("(c) todos os números, letras e sinais de referência com altura mínima de 0,32 cm; (d) %s; (e) folhas A4 com as margens da Regra 11.6, sem molduras; (f) disposição das figuras e dos painéis nas folhas, e número de folhas, ajustados ao tamanho das letras. %s' % (esc(d['comum_d']),",
    "(c) %s; (d) %s; (e) folhas A4 com as margens da Regra 11.6, sem molduras; (f) disposição das figuras e dos painéis nas folhas, e número de folhas, ajustados ao tamanho das letras. %s' % (esc(d.get('comum_c', 'todos os números, letras e sinais de referência com altura mínima de 0,32 cm')), esc(d['comum_d']),")
rep("    anexo='FOLHAS_SUBSTITUTIVAS_050576.pdf (6 folhas)',",
    "    comum_c='algarismos, maiúsculas e letras com haste com altura mínima de 0,32 cm (inclusive nos sinais de referência)',\n    anexo='FOLHAS_SUBSTITUTIVAS_050576.pdf (6 folhas)',")
rep("                anexo='folha 1/6 de ALTERNATIVA_FOLHA_1_050576_PHOT.pdf e folhas 2/6 a 6/6 de FOLHAS_SUBSTITUTIVAS_050576.pdf (6 folhas)',",
    "                anexo='FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf (6 folhas; só a folha 1/6 difere das folhas principais)',")
# linha da Fig. 3: «VACUUM 6 bits» de horizontal para vertical
rep("rótulos de região sem fundo branco, com a grade pontilhada interrompida ao redor deles; legenda acima do quadro; letras de corpo 15 pt',",
    "rótulos de região sem fundo branco, com a grade pontilhada interrompida ao redor deles; «VACUUM 6 bits» passou da horizontal para a vertical (mesmo texto); legenda acima do quadro; letras de corpo 15 pt',")
# so gera o que for pedido (MQC congelado)
rep("if __name__ == '__main__':\n    for d in (APR, APR_PHOT, MQC):",
    "if __name__ == '__main__':\n    alvo = (APR, APR_PHOT) + ((MQC,) if 'mqc' in sys.argv else ())\n    for d in alvo:")
rep("import json, pathlib, subprocess, re, shutil, copy", "import json, pathlib, subprocess, re, shutil, copy, sys")
p.write_text(s, encoding='utf-8')

q = F / 'prancha.py'
t = q.read_text(encoding='utf-8')
old = "for k, filed in (('050576', W / 'entrada/aprendizado/04_DESENHOS_como_depositado.pdf'), ('050579', W / 'entrada/mqc/04_DESENHOS_CINZA_como_depositado.pdf')):"
assert old in t
t = t.replace(old, "import sys\nfor k, filed in [x for x in (('050576', W / 'entrada/aprendizado/04_DESENHOS_como_depositado.pdf'), ('050579', W / 'entrada/mqc/04_DESENHOS_CINZA_como_depositado.pdf')) if x[0] in sys.argv[1:]]:")
q.write_text(t, encoding='utf-8')

m = F / 'montar_conferencia.py'
u = m.read_text(encoding='utf-8')
old = "    for k in ('050576', '050579'):\n        doc = montar(k)"
assert old in u
u = u.replace(old, "    import sys\n    for k in [x for x in ('050576', '050579') if x in sys.argv[1:]]:\n        doc = montar(k)")
m.write_text(u, encoding='utf-8')
print('ok')
