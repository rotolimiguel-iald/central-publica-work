# -*- coding: utf-8 -*-
"""Patch do nucleo publico (gerencia c1, 02/11/2026, custodia v405): caminho acima do limite do Windows sai da copia com motivo dito e caminho listado, em vez de derrubar a rodada.
Medido na v405: 2 arquivos, duas falas em insumos/cunhagens no cofre; as duas estao por sha256 no mapa do espelho (fontes_pinadas/caminho_longo)."""
import datetime, os, py_compile
from pathlib import Path

TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_c1"
W = Path("C:/IALD/Central de Patentes/work/central_publica_22out")
E = [
 ('LOCAL_EXCL = {}\n',
  'LOCAL_EXCL = {}\n'
  'CAMINHO_LONGO = "caminho acima do limite do Windows (listado; as fontes pinadas seguem no MAPA_FONTES_PINADAS do the_boundary)"\n'),
 ('        return "backup de sessão"\n    return None\n',
  '        return "backup de sessão"\n'
  '    if len(str(DST / t)) > 255:      # 02/11/2026 (v405): nome longo de cunhagem no cofre; o write_bytes falharia e derrubaria a rodada\n'
  '        return CAMINHO_LONGO\n'
  '    return None\n'),
 ('LISTAVEIS = {"documento de protocolo ou pagamento", "acima de 95 MB (índice apenas)", "backup de sessão"}\n',
  'LISTAVEIS = {"documento de protocolo ou pagamento", "acima de 95 MB (índice apenas)", "backup de sessão", CAMINHO_LONGO}\n'),
]
novos = []
for nome in ("construir_nucleo_incremental.py", "construir_nucleo_publico.py"):
    p = W / nome
    b = p.read_bytes()
    t = b.decode("utf-8")
    crlf = "\r\n" in t
    assert not crlf or t.count("\n") == t.count("\r\n"), ("fim de linha misto", nome)
    for old, new in E:
        if crlf:
            old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
        assert t.count(old) == 1, (nome, old[:60], t.count(old))
        t = t.replace(old, new)
    novos.append((p, b, t.encode("utf-8")))
for p, b, nb in novos:
    bak = p.with_name(p.name + ".bak_" + TS)
    with open(bak, "xb") as f:
        f.write(b)
    assert bak.read_bytes() == b
    tmp = p.with_name(p.name + ".tmp_" + TS)
    with open(tmp, "xb") as f:
        f.write(nb)
    py_compile.compile(str(tmp), cfile=str(tmp) + ".pyc", doraise=True)
    os.remove(str(tmp) + ".pyc")
    os.replace(tmp, p)
    print("ok", p.name, len(b), "->", len(nb))
