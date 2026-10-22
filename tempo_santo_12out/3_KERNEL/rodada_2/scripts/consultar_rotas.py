# -*- coding: utf-8 -*-
"""Consultas SÓ DE LEITURA ao mapa de rotas (rotas.py consultar) para os temas novos da rodada 2 do kernel F1.TEMPO.
Nada é registrado (proibido pela tarefa). O livro rotas.jsonl é hasheado antes e depois.
Uso: python -I consultar_rotas.py <pasta_saida>
"""
import hashlib
import json
import os
import subprocess
import sys

ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
LIVRO = r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl"
TEMAS = {
    "R2_01_identity_flow_not_kms": "identity_flow_not_kms",
    "R2_02_theSpecificAQFTWitness": "theSpecificAQFTWitness",
    "R2_03_omega_not_tracial": "omega_not_tracial",
    "R2_04_FockCertificate": "FockCertificate",
    "R2_05_TheTimeHasNoRank": "TheTimeHasNoRank",
    "R2_06_F1_TEMPO": "F1.TEMPO",
    "R2_07_tempo_santo": "tempo santo",
    "R2_08_absoluteRho_posto": "absoluteRho posto",
    "R2_09_KMS_face_finita": "KMS face finita",
    "R2_10_pedra_corrigida": "pedra corrigida",
}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main(outdir):
    os.makedirs(outdir, exist_ok=True)
    antes = sha(LIVRO)
    resumo = {"livro": LIVRO, "livro_sha256_antes": antes, "consultas": []}
    for nome, tema in TEMAS.items():
        r = subprocess.run([sys.executable, "-X", "utf8", ROTAS, "consultar", tema], capture_output=True, timeout=300)
        out = r.stdout + (b"\n--- STDERR ---\n" + r.stderr if r.stderr else b"")
        p = os.path.join(outdir, nome + ".txt")
        with open(p, "wb") as f:
            f.write(out)
        txt = out.decode("utf-8", "replace")
        resumo["consultas"].append({"tema": tema, "arquivo": p, "bytes": len(out), "sha256": hashlib.sha256(out).hexdigest(),
                                    "exit": r.returncode, "primeiras_linhas": txt.splitlines()[:6]})
    resumo["livro_sha256_depois"] = sha(LIVRO)
    resumo["livro_inalterado"] = resumo["livro_sha256_antes"] == resumo["livro_sha256_depois"]
    with open(os.path.join(outdir, "RESUMO.json"), "w", encoding="utf-8") as f:
        json.dump(resumo, f, ensure_ascii=False, indent=1)
    sys.stdout.reconfigure(encoding="utf-8")
    for c in resumo["consultas"]:
        print(c["tema"], "|", c["bytes"], "B |", " / ".join(c["primeiras_linhas"][:3])[:300])
    print("livro inalterado:", resumo["livro_inalterado"])


if __name__ == "__main__":
    main(sys.argv[1])
