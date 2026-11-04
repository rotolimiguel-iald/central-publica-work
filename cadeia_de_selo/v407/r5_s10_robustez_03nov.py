# -*- coding: utf-8 -*-
"""03/11/2026 18:4x, gerencia c1 (R5 confinada ao orquestrador): dois BAIXOS novos da revisao R4 sobre o elo (a) do recibo do S10 (RESULTADOS\\NNN_RESULTADO.json):
(1) um JSON valido que NAO e' objeto (lista, string) derrubava o S10 com AttributeError: fail-closed, mas encerrava a espera de 24 h e o orquestrador inteiro; agora e' ignorado (nao e' resultado);
(2) o nome do arquivo bastava mesmo com o campo `ordem` apontando OUTRA ordem; agora, se o campo existe, ele manda; o nome so' vale sem o campo. O ensaio a seco ganha os dois casos negativos.
Backup pelo patches.aplicar_em_arquivo; py_compile; --ensaio em seguida. Escrito pelo Write."""
import json, sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import patches  # noqa: E402
PT = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407\orquestrador\pos_treino_v407.py"
O1 = ('        try:\n            rj = jload(p)\n        except Exception:  # noqa: BLE001\n            continue\n'
      '        desta = bool(re.search(r"ORDEM[_ ]?0*%d(?![0-9])" % num, str(rj.get("ordem", ""))) or re.match(r"0*%d_RESULTADO\\.json$" % num, p.name))\n')
N1 = ('        try:\n            rj = jload(p)\n        except Exception:  # noqa: BLE001\n            continue\n'
      '        if not isinstance(rj, dict):   # [R5, 03/11] JSON valido que NAO e\' objeto (lista, string): nao e\' resultado; nunca derruba a espera\n            continue\n'
      '        _ord = str(rj.get("ordem", "") or "").strip()\n'
      '        desta = bool(re.search(r"ORDEM[_ ]?0*%d(?![0-9])" % num, _ord)) if _ord else bool(re.match(r"0*%d_RESULTADO\\.json$" % num, p.name))   # [R5] com o campo ordem, ele manda; o nome so\' vale sem o campo\n')
O2 = '    def montar(release="v407", srcsha=pin, status="PASS", jev_sha=None, relatorio=True, jev_nome=True, resultado=None):\n'
N2 = '    def montar(release="v407", srcsha=pin, status="PASS", jev_sha=None, relatorio=True, jev_nome=True, resultado=None, resultado_json=None):\n'
O3 = ('        if resultado:\n            rdir.mkdir(exist_ok=True); (rdir / ("%03d_RESULTADO.json" % num)).write_text(json.dumps({"ordem": "ORDEM_%03d" % num, "estado": resultado, "arquivos": []}), encoding="utf-8")\n'
      '        if relatorio:\n')
N3 = ('        if resultado:\n            rdir.mkdir(exist_ok=True); (rdir / ("%03d_RESULTADO.json" % num)).write_text(json.dumps({"ordem": "ORDEM_%03d" % num, "estado": resultado, "arquivos": []}), encoding="utf-8")\n'
      '        if resultado_json is not None:   # [R5] o texto bruto do RESULTADO desta ordem (casos malformados)\n            rdir.mkdir(exist_ok=True); (rdir / ("%03d_RESULTADO.json" % num)).write_text(resultado_json, encoding="utf-8")\n'
      '        if relatorio:\n')
O4 = '    montar(relatorio=False, resultado="parcial"); okn, _ = recibo_do_app(ordem, num, "v407", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["negativo_resultado_parcial"] = (okn is False)\n'
N4 = (O4 +
      '    montar(relatorio=False, resultado_json=json.dumps(["cumprida"])); okn, _ = recibo_do_app(ordem, num, "v407", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["negativo_resultado_nao_objeto"] = (okn is False)   # [R5] JSON valido que nao e\' objeto: ignorado, sem excecao\n'
      '    montar(relatorio=False, resultado_json=json.dumps({"ordem": "ORDEM_%03d" % (num + 18), "estado": "cumprida"})); okn, _ = recibo_do_app(ordem, num, "v407", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["negativo_resultado_ordem_divergente"] = (okn is False)   # [R5] o nome e\' desta ordem, o campo diz outra: o campo manda\n')


def f(s):
    for o in (O1, O2, O3, O4):
        assert s.count(o) == 1, ("nao esta UMA vez (%d): %s" % (s.count(o), o[:90]))
    for o, n in ((O1, N1), (O2, N2), (O3, N3), (O4, N4)):
        s = s.replace(o, n)
    return s, ["RESULTADO nao-objeto ignorado", "campo ordem manda sobre o nome", "montar(resultado_json=)", "dois casos negativos no ensaio"]


print(json.dumps(patches.aplicar_em_arquivo(PT, f, "r5_s10_robustez"), ensure_ascii=False)[:260])
