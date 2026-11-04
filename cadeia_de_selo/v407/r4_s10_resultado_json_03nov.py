# -*- coding: utf-8 -*-
"""03/11/2026 17:5x, gerencia c1 (R4): o CANAL_DESASSISTIDO.md (gerente central do LAR, 03/11, por ordem do operador) registra o resultado duravel de cada ORDEM em
TUNEL_CLAUDE_APP\\RESULTADOS\\NNN_RESULTADO.json (estado cumprida|parcial|recusada|incerta). O elo (a) do recibo do S10 so' aceitava RELATORIO_*.md: se o app respondesse na forma do canal,
a cadeia esperaria 24 h e pararia. Aqui o elo (a) aceita QUALQUER das duas formas (RELATORIO posterior a ordem citando ORDEM_NNN, ou RESULTADOS\\NNN_RESULTADO.json desta ordem, posterior a ela,
com estado cumprida); os outros tres elos (INSTALLED_VERIFICATION, jev_control, iald_nucleo_fixo) seguem exigidos: nada e' aceito pela palavra do relatorio. O ensaio a seco ganha o caso
positivo com so' o JSON e o negativo com estado parcial; o template da ordem diz as duas formas. Backups pelo patches.aplicar_em_arquivo (.py) e em bytes (.md). Escrito pelo Write."""
import json, os, sys, time
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import patches  # noqa: E402
ORQ = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407\orquestrador"; TS = time.strftime("%Y%m%d_%H%M%S")
PT = os.path.join(ORQ, "pos_treino_v407.py"); TPL = os.path.join(ORQ, "ORDEM_RELEASE_APP_TEMPLATE.md")
O1 = ('    for p in tunel.glob("RELATORIO_*.md"):\n'
      '        if p.stat().st_mtime > t0 and re.search(r"ORDEM[_ ]?0*%d(?![0-9])" % num, p.read_text(encoding="utf-8", errors="replace")):\n'
      '            rel_ok.append(p.name)\n'
      '    d["relatorio"] = rel_ok or None\n')
N1 = ('    for p in tunel.glob("RELATORIO_*.md"):\n'
      '        if p.stat().st_mtime > t0 and re.search(r"ORDEM[_ ]?0*%d(?![0-9])" % num, p.read_text(encoding="utf-8", errors="replace")):\n'
      '            rel_ok.append(p.name)\n'
      '    # [R4, 03/11] a forma duravel do CANAL_DESASSISTIDO.md (gerente do LAR, 03/11): RESULTADOS\\NNN_RESULTADO.json desta ordem, posterior a ela, com estado cumprida, vale como o elo (a); parcial/recusada/incerta NAO valem\n'
      '    rdir = tunel / "RESULTADOS"\n'
      '    for p in (rdir.glob("*_RESULTADO.json") if rdir.is_dir() else []):\n'
      '        try:\n'
      '            rj = jload(p)\n'
      '        except Exception:  # noqa: BLE001\n'
      '            continue\n'
      '        desta = bool(re.search(r"ORDEM[_ ]?0*%d(?![0-9])" % num, str(rj.get("ordem", ""))) or re.match(r"0*%d_RESULTADO\\.json$" % num, p.name))\n'
      '        if p.stat().st_mtime > t0 and desta and str(rj.get("estado", "")).strip().lower() == "cumprida":\n'
      '            rel_ok.append("RESULTADOS/" + p.name)\n'
      '    d["relatorio"] = rel_ok or None\n')
O2 = '    """O RECIBO do app, conferido NA FONTE (devolve (ok, dict)). Quatro elos, todos exigidos: (a) RELATORIO_*.md na pasta de ordens, escrito DEPOIS da ordem e citando ORDEM_<num>; (b)'
N2 = '    """O RECIBO do app, conferido NA FONTE (devolve (ok, dict)). Quatro elos, todos exigidos: (a) RELATORIO_*.md na pasta de ordens, escrito DEPOIS da ordem e citando ORDEM_<num>, OU (R4, 03/11) RESULTADOS\\\\NNN_RESULTADO.json desta ordem, posterior a ela, com estado cumprida (a forma do CANAL_DESASSISTIDO.md); (b)'
O3 = '    def montar(release="v407", srcsha=pin, status="PASS", jev_sha=None, relatorio=True, jev_nome=True):\n        for p in (out / "tunel").glob("RELATORIO_*.md"):\n            p.unlink()\n        if relatorio:\n'
N3 = ('    def montar(release="v407", srcsha=pin, status="PASS", jev_sha=None, relatorio=True, jev_nome=True, resultado=None):\n        for p in (out / "tunel").glob("RELATORIO_*.md"):\n            p.unlink()\n'
      '        rdir = out / "tunel" / "RESULTADOS"   # [R4] a forma duravel do canal: so\' quando o caso pede\n'
      '        for p in (rdir.glob("*_RESULTADO.json") if rdir.is_dir() else []):\n            p.unlink()\n'
      '        if resultado:\n            rdir.mkdir(exist_ok=True); (rdir / ("%03d_RESULTADO.json" % num)).write_text(json.dumps({"ordem": "ORDEM_%03d" % num, "estado": resultado, "arquivos": []}), encoding="utf-8")\n'
      '        if relatorio:\n')
O4 = '    montar(); ok, d = recibo_do_app(ordem, num, "v407", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["positivo"] = ok\n'
N4 = (O4 +
      '    montar(relatorio=False, resultado="cumprida"); okr, _ = recibo_do_app(ordem, num, "v407", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["positivo_resultado_json"] = okr   # [R4] so\' o JSON do canal, sem RELATORIO\n'
      '    montar(relatorio=False, resultado="parcial"); okn, _ = recibo_do_app(ordem, num, "v407", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["negativo_resultado_parcial"] = (okn is False)\n')
O5 = '    res["ok"] = res["positivo"] is True and all(v is True for k, v in res.items() if k.startswith("negativo_"))\n'
N5 = '    res["ok"] = res["positivo"] is True and res["positivo_resultado_json"] is True and all(v is True for k, v in res.items() if k.startswith("negativo_"))\n'


def f(s):
    for o in (O1, O2, O3, O4, O5):
        assert s.count(o) == 1, ("nao esta UMA vez (%d): %s" % (s.count(o), o[:90]))
    for o, n in ((O1, N1), (O2, N2), (O3, N3), (O4, N4), (O5, N5)):
        s = s.replace(o, n)
    return s, ["elo (a) aceita RESULTADOS/NNN_RESULTADO.json cumprida", "docstring", "ensaio: montar(resultado=)", "ensaio: positivo so' JSON + negativo parcial", "ok exige o positivo do JSON"]


print(json.dumps(patches.aplicar_em_arquivo(PT, f, "r4_s10_resultado"), ensure_ascii=False)[:260])
# template (.md, bytes)
b = open(TPL, "rb").read()
o = "(a) `RELATORIO_<data>.md` nesta pasta, escrito depois desta ordem e citando `ORDEM_{{NUM}}`;".encode("utf-8")
n = "(a) `RELATORIO_<data>.md` nesta pasta, escrito depois desta ordem e citando `ORDEM_{{NUM}}`, ou `RESULTADOS\\{{NUM}}_RESULTADO.json` com `estado: cumprida` (a forma durável do `CANAL_DESASSISTIDO.md`);".encode("utf-8")
assert b.count(o) == 1, b.count(o)
bak = TPL + ".bak_r4_s10_resultado_" + TS; open(bak, "xb").write(b); assert open(bak, "rb").read() == b
novo = b.replace(o, n); tmp = TPL + ".tmp_" + TS; open(tmp, "xb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, TPL); assert open(TPL, "rb").read() == novo
print("template: %d -> %d B; backup %s" % (len(b), len(novo), os.path.basename(bak)))
