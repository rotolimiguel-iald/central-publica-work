# -*- coding: utf-8 -*-
"""G1 (25/10/2026, gerência a7), dois remendos achados na primeira custódia viva por G1 (v399+v400):
 1. RE_CAB não lia o cabeçalho do diário quando a versão não traz módulo novo («nenhum módulo novo, escada 9541 → 9541», v400):
    o título PT ficava vazio e a perna 1 parava. Agora «nenhum» conta como 0.
 2. Os marcadores de prosa (TITULO_EN, ENTROU_EN, KERNEL_LEITURA_EN, ABERTOS_EN, ARCO_EN/PT, COMMIT) só eram lidos do HANDOFF do Nós,
    que é da gerência c1 e não os traz. A prosa da custódia é da gerência do site (a7), como sempre foi nos geradores v396–v398: G1 passa a
    ler, AO LADO do handoff, um arquivo `TEXTOS_vNNN.md` na pasta de trabalho da custódia (work\\custodia_vNNN_*), com os mesmos marcadores.
    O que o handoff traz MANDA (o suplemento só preenche marcador ausente); a origem fica em `h.fontes_textos` e nos recibos; marcador
    malformado no suplemento é problema (PARA), como no handoff.
Trocas contadas; backup de bytes; py_compile."""
import os, py_compile, time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\tools\custodia_g1\nos.py")
raw = P.read_bytes(); s = raw.decode("utf-8")
if "TEXTOS_%s.md" in s:
    raise SystemExit("já aplicado")
pares = [
    (r'''"\((?P=v)\):\s*(?P<k>\d+) m[o\u00f3]dulos? novos?,\s*escada\s*(?P<a>\d+)\s*\u2192\s*(?P<b>\d+)", re.M)''',
     r'''"\((?P=v)\):\s*(?P<k>\d+|nenhum) m[o\u00f3]dulos? novos?,\s*escada\s*(?P<a>\d+)\s*\u2192\s*(?P<b>\d+)", re.M)'''),
    ('''            b.modulos_novos, b.escada_de, b.escada_para = int(mc.group("k")), int(mc.group("a")), int(mc.group("b"))''',
     '''            b.modulos_novos = 0 if mc.group("k") == "nenhum" else int(mc.group("k"))   # 25/10: «nenhum módulo novo» (v400)
            b.escada_de, b.escada_para = int(mc.group("a")), int(mc.group("b"))'''),
    ('''    problemas: list = field(default_factory=list)        # marcadores malformados/duplicados
''', '''    problemas: list = field(default_factory=list)        # marcadores malformados/duplicados
    fontes_textos: dict = field(default_factory=dict)    # id -> «handoff» | caminho do TEXTOS_vNNN.md da gerência do site (25/10/2026)
'''),
    ('''    for par in t.split("\\n\\n"):
        mm = re.match(r"\\*\\*(.+?)\\*\\*", par.strip())
        if mm:
            h.secoes.setdefault(mm.group(1).rstrip(": ").strip(), par.strip())
    return h
''', '''    for par in t.split("\\n\\n"):
        mm = re.match(r"\\*\\*(.+?)\\*\\*", par.strip())
        if mm:
            h.secoes.setdefault(mm.group(1).rstrip(": ").strip(), par.strip())
    for i in h.marcadores:
        h.fontes_textos[i] = "handoff"
    # 25/10/2026: a prosa da custódia (os marcadores opcionais) pode vir da gerência do site num TEXTOS_vNNN.md na pasta de trabalho;
    # o handoff manda; o suplemento só preenche o que falta; malformado = problema (PARA)
    for sp in sorted(c.CEN.glob("work/custodia_%s_*/TEXTOS_%s.md" % (v, v))):
        ts = util.ler_texto(sp).replace("\\r\\n", "\\n")
        a2, f2 = RE_ABRE.findall(ts), RE_FECHA.findall(ts)
        for i in sorted(set(a2) ^ set(f2)):
            h.problemas.append("marcador %s sem par INICIO/FIM em %s" % (i, sp.name))
        for m in RE_MARCADOR.finditer(ts):
            i = m.group("id")
            if i in h.marcadores:
                continue
            if not m.group("corpo").strip():
                h.problemas.append("marcador %s vazio em %s" % (i, sp.name))
                continue
            h.marcadores[i] = m.group(0)
            h.corpos[i] = m.group("corpo")
            h.fontes_textos[i] = str(sp)
    return h
'''),
]
for a, b in pares:
    n = s.count(a)
    assert n == 1, (a[:70], n)
    s = s.replace(a, b)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp"); t.write_bytes(s.encode("utf-8")); py_compile.compile(str(t), doraise=True); os.replace(t, P)
print("nos.py: «nenhum módulo novo» lido; TEXTOS_vNNN.md ao lado do handoff | %d -> %d bytes" % (len(raw), P.stat().st_size))
