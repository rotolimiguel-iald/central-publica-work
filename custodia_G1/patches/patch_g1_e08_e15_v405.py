# -*- coding: utf-8 -*-
"""Patch de G1 (gerencia c1, 02/11/2026, custodia v405, G1 parado): licoes 24 e 27 da v402, que voltaram a parar a custodia.
24: o E08 auditava llms-full e index.md, que so o E15 escreve; cada passo passa a auditar o que ele mesmo escreve. 27: o ultimo gerar_portas do laco deixava o carimbo fora do indice."""
import datetime, os, py_compile
from pathlib import Path

TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_c1"
C = Path("C:/IALD/Central de Patentes")
E = [
 (C / "tools/custodia_g1/espelho.py", [
  ('CANDIDATAS_CITADAS = ("TB:read-brief.md", "SITE:read-brief.md", "SITE:llms.txt", "SITE:llms-full.txt", "SITE:index.md", "TB:llms.txt")\n',
   'CANDIDATAS_CITADAS = ("TB:read-brief.md", "SITE:read-brief.md", "SITE:llms.txt", "SITE:llms-full.txt", "SITE:index.md", "TB:llms.txt")\n'
   '# 02/11/2026 (lição 24 da v402, que parou de novo a v405): llms-full e index.md só o E15 escreve; cada passo audita o que ele mesmo escreve, e `custodiar auditar` audita todas\n'
   'CITADAS_DO_E15 = ("SITE:llms-full.txt", "SITE:index.md")\n'
   'CITADAS_DO_E08 = tuple(x for x in CANDIDATAS_CITADAS if x not in CITADAS_DO_E15)\n'),
  ('def auditar_numeros_citados(ctx):\n', 'def auditar_numeros_citados(ctx, superficies=CANDIDATAS_CITADAS):\n'),
  ('    for ref in CANDIDATAS_CITADAS:\n', '    for ref in superficies:\n'),
  ('    d = auditar_numeros_citados(ctx)\n    l3 = rotulo_do_teste_no_readme(ctx)\n    if d or l3:\n',
   '    d = auditar_numeros_citados(ctx, CITADAS_DO_E08)\n    l3 = rotulo_do_teste_no_readme(ctx)\n    if d or l3:\n'),
  ('    d = auditar_numeros_citados(ctx)\n    f += ["número citado defasado',
   '    d = auditar_numeros_citados(ctx, CITADAS_DO_E08)\n    f += ["número citado defasado'),
  ('        exigir_rc0(_tb(ctx, "gerar_portas.py"), "gerar_portas.py (hash final)")\n        sig = _assinatura(ctx)\n',
   '        exigir_rc0(_tb(ctx, "gerar_portas.py"), "gerar_portas.py (hash final)")\n'
   '        exigir_rc0(_rodar_git(ctx, "add", "-A"), "git add -A")      # 02/11/2026 (lição 27 da v402): o gerar_portas regrava o carimbo gerado_utc; sem isto a pré-condição do E10 para\n'
   '        sig = _assinatura(ctx)\n'),
 ]),
 (C / "tools/custodia_g1/site.py", [
  ('from .espelho import _banc, exigir_rc0, _historica\n', 'from .espelho import _banc, exigir_rc0, _historica, auditar_numeros_citados, CITADAS_DO_E15\n'),
  ('    if not faltam:\n        return aplicado("llms-full.txt, index.md e o cartão de estado trazem %s" % ctx.pin16)\n',
   '    if not faltam:\n'
   '        d = auditar_numeros_citados(ctx, CITADAS_DO_E15)\n'
   '        if d:\n'
   '            return falta("%d números citados defasados: %s" % (len(d), "; ".join("%s cita %s=%s, real %s" % (x["superficie"], x["arquivo"], x["citado"], x["real"]) for x in d[:3])))\n'
   '        return aplicado("llms-full.txt, index.md e o cartão de estado trazem %s; 0 números citados defasados" % ctx.pin16)\n'),
  ('def _ja_e16(ctx):\n',
   'def _ja_e16(ctx):\n'),
  ('# =================================================================== E16 — sitemap e manifesto de subida\n',
   'def _conf_e15(ctx):\n'
   '    ctx._cache_t.clear()\n'
   '    ctx._cache_j.clear()\n'
   '    return ["número citado defasado: %s cita %s=%s, real %s" % (x["superficie"], x["arquivo"], x["citado"], x["real"]) for x in auditar_numeros_citados(ctx, CITADAS_DO_E15)]\n'
   '\n\n'
   '# =================================================================== E16 — sitemap e manifesto de subida\n'),
  ('_ja_e15, aplicar=_ap_e15, fase="B", escreve=', '_ja_e15, aplicar=_ap_e15, conferir=_conf_e15, fase="B", escreve='),
 ]),
 (C / "work/custodia_G1/testes/testes_g1.py", [
  ('(\"SITE:llms.txt\", \"secoes/07-o-programa-um-py.md\", 11762, 11731)], d\n',
   '(\"SITE:llms.txt\", \"secoes/07-o-programa-um-py.md\", 11762, 11731)], d\n'
   '    assert [x["superficie"] for x in espelho.auditar_numeros_citados(ctx, espelho.CITADAS_DO_E08)] == ["SITE:llms.txt"], "o E08 audita o que ele escreve; o index.md é do E15 (lição 24)"\n'
   '    assert [x["superficie"] for x in espelho.auditar_numeros_citados(ctx, espelho.CITADAS_DO_E15)] == ["SITE:index.md"]\n'),
  ('    assert so[-1] == "gerar_portas.py", "a última coisa de cada passada é o gerar_portas (hash final do read-brief)"\n',
   '    assert so[-1] == "gerar_portas.py", "a última coisa de cada passada é o gerar_portas (hash final do read-brief)"\n'
   '    assert seq[-1] == "git add", "depois do último gerar_portas vem o git add -A: o carimbo gerado_utc não fica fora do índice (lição 27)"\n'),
 ]),
]
novos = []
for p, eds in E:
    b = p.read_bytes()
    t = b.decode("utf-8")
    crlf = "\r\n" in t
    assert not crlf or t.count("\n") == t.count("\r\n"), ("fim de linha misto", p)
    for old, new in eds:
        if old == new:
            continue
        if crlf:
            old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
        assert t.count(old) == 1, (p.name, old[:70], t.count(old))
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
