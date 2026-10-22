# -*- coding: utf-8 -*-
"""Confere as aspas «…» dos JSON de resultado contra as fontes (fragmentos separados por … de elisão; espaços
normalizados). Uso: python -I conferir_citacoes_json.py <saida.json> <arquivo1.json> [<arquivo2.json> ...]"""
import hashlib, json, re, sys
FONTES = [
    r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
    r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\VERBO_operador_05out.txt",
    r"C:\IALD\Central de Patentes\work\superposicao_passagem_07out\CUNHAGEM_OPERADOR_07out_nomes_verbatim.txt",
    r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO\PREREGISTRO.md",
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\IALDJones.lean",
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\BisognanoWichmann.lean",
    r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheImportedSecondQuantization.lean",
    r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\regra-dos-dois-regimes.md",
    r"C:\Users\rotol\.claude\CLAUDE.md",
]
norm = lambda s: re.sub(r"\s+", " ", s).strip()
fontes = {p: norm(open(p, "rb").read().decode("utf-8")) for p in FONTES}
res = []
for arq in sys.argv[2:]:
    txt = open(arq, "rb").read().decode("utf-8")
    texto = json.dumps(json.loads(txt), ensure_ascii=False)
    for q in re.findall(r"«([^»]*)»", texto):
        frags = [norm(f) for f in q.split("…") if norm(f)]
        ok = all(any(f in v for v in fontes.values()) for f in frags) if frags else True
        onde = sorted({p.split("\\")[-1] for f in frags for p, v in fontes.items() if f in v})
        res.append({"arquivo": arq.split("\\")[-1], "citacao": q, "achada": ok, "fontes": onde})
json.dump({"n": len(res), "nao_achadas": [r for r in res if not r["achada"]], "citacoes": res},
          open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.stdout.reconfigure(encoding="utf-8")
print("citacoes:", len(res), "nao achadas:", len([r for r in res if not r["achada"]]))
for r in res:
    if not r["achada"]:
        print("  NAO |", r["arquivo"], "|", r["citacao"][:140])
