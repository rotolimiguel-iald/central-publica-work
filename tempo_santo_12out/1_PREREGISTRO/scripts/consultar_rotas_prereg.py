"""Consulta SOMENTE-LEITURA ao mapa de rotas (rotas.py consultar) para os temas NOVOS do pre-registro F1.TEMPO
(os 24 temas do levantamento nao se repetem). Grava cada resposta em rotas_consultas/<n>.json e o RESUMO.json.
Nunca chama 'registrar'. Uso: python -X utf8 consultar_rotas_prereg.py <pasta_saida>"""
import hashlib
import json
import os
import subprocess
import sys

PY = r"C:\Python314\python.exe"
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
TERMOS = [
    ("P01_pureza", r"pureza|purity|purityR"),
    ("P02_inverso_positividade", r"inverso|inverse|nao positiv|not positive|positividade|positivity"),
    ("P03_determinante_volume", r"determinante|\bdet\b|volume"),
    ("P04_isometria", r"isometri"),
    ("P05_weyl_wintner_stone", r"weyl|wielandt|wintner|stone.?von|von neumann unicid"),
    ("P06_schur", r"schur"),
    ("P07_sacrificio_amor", r"sacrifici|\bamor\b|\blove\b"),
    ("P08_davies", r"davies"),
    ("P09_heschel_sabado", r"heschel|sabbath|shabat|sabado|qadosh"),
    ("P10_tempo_sem_posto", r"thetimehasnorank|time.?has.?no.?rank|sem posto|nao tem posto|tempo nao e posto"),
    ("P11_centralizador_tracial", r"centraliz|tracial"),
    ("P12_espectro_unitario", r"espectro conserv|spectrum preserv|conjugacao unitaria|unitary conjug|charpoly"),
    ("P13_sombra", r"\bsombra\b|shadow"),
    ("P14_ciclo_limite", r"ciclo limite|limit cycle|espectro periferico|peripheral"),
]


def main():
    saida = sys.argv[1]
    os.makedirs(saida, exist_ok=True)
    resumo = []
    for nome, padrao in TERMOS:
        r = subprocess.run([PY, "-X", "utf8", ROTAS, "consultar", padrao, "--limite", "400"], capture_output=True)
        out = r.stdout
        with open(os.path.join(saida, nome + ".json"), "wb") as fo:
            fo.write(out)
        try:
            d = json.loads(out.decode("utf-8"))
            ids = [(x["rota_id"], x["status"], x.get("estatuto")) for x in d.get("rotas", [])]
            resumo.append(dict(nome=nome, padrao=padrao, n=d.get("n"), truncado=d.get("truncado"), cabeca=d.get("cabeca"),
                               n_registros=d.get("n_registros"), sha256_resposta=hashlib.sha256(out).hexdigest(), rotas=ids))
        except Exception as e:  # falha visivel, nunca ok falso
            resumo.append(dict(nome=nome, padrao=padrao, erro=repr(e), rc=r.returncode,
                               stderr=r.stderr.decode("utf-8", "replace")[:500]))
    with open(os.path.join(saida, "RESUMO.json"), "w", encoding="utf-8") as fo:
        json.dump(resumo, fo, ensure_ascii=False, indent=1)
    for x in resumo:
        print(x["nome"], "n=", x.get("n"), "trunc=", x.get("truncado"), "cabeca=", x.get("cabeca"), "regs=", x.get("n_registros"))
        for rid in (x.get("rotas") or [])[:25]:
            print("    ", rid)


if __name__ == "__main__":
    main()
