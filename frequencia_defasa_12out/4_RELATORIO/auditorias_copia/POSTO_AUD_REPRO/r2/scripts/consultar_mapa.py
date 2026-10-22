# -*- coding: utf-8 -*-
"""Consultas SO-LEITURA ao mapa de rotas (rotas.py consultar), com hash do livro antes/depois."""
import hashlib, json, os, subprocess, sys

LIVRO = r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl"
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "consultas_mapa")
os.makedirs(OUT, exist_ok=True)

CONSULTAS = [
    ("m01", "F1.FREQUENCIA"),
    ("m02", "frequencia defasa|frequencia_defasa"),
    ("m03", "TheUnitIsTheRank|unidade e o rank|unit is the rank"),
    ("m04", "posto.*rank|rank.*posto|POSTO=RANK"),
    ("m05", "anticomut|anticommut"),
    ("m06", "Smat_pow|Smat_mul"),
    ("m07", "fractal_dephasing|fractal.*defas"),
    ("m08", "AUD_REPRO|auditor.*repro"),
]


def sha(p):
    with open(p, "rb") as fh:
        b = fh.read()
    return len(b), hashlib.sha256(b).hexdigest()


def main():
    antes = sha(LIVRO)
    resumo = {"livro_antes": {"bytes": antes[0], "sha256": antes[1]}, "consultas": []}
    for cid, q in CONSULTAS:
        r = subprocess.run([sys.executable, "-X", "utf8", ROTAS, "consultar", q, "--limite", "200"],
                           capture_output=True, text=True, encoding="utf-8")
        with open(os.path.join(OUT, cid + ".json"), "x", encoding="utf-8") as fh:
            fh.write(r.stdout)
        with open(os.path.join(OUT, cid + ".err"), "x", encoding="utf-8") as fh:
            fh.write(r.stderr)
        try:
            d = json.loads(r.stdout)
            n = d.get("n"); cab = d.get("cabeca"); nreg = d.get("n_registros")
            ids = [x.get("rota_id") for x in d.get("rotas", [])]
            st = [(x.get("rota_id"), x.get("status")) for x in d.get("rotas", [])]
        except Exception as e:  # falha visivel
            n, cab, nreg, ids, st = None, None, None, [], [("ERRO_PARSE", str(e))]
        resumo["consultas"].append({"id": cid, "padrao": q, "rc": r.returncode, "n": n,
                                    "n_registros": nreg, "cabeca": cab, "rotas_status": st})
    depois = sha(LIVRO)
    resumo["livro_depois"] = {"bytes": depois[0], "sha256": depois[1]}
    resumo["livro_inalterado_pelas_consultas"] = (antes == depois)
    with open(os.path.join(OUT, "RESUMO.json"), "x", encoding="utf-8") as fh:
        json.dump(resumo, fh, ensure_ascii=False, indent=1)
    print(json.dumps(resumo, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
