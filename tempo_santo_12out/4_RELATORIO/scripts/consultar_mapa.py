# -*- coding: utf-8 -*-
"""Consultas SO DE LEITURA ao mapa de rotas (rotas.py consultar / ver / modelo).

Grava as saidas em 4_RELATORIO/saidas/rotas/. Confere o sha256 do livro rotas.jsonl antes e
depois (nada se registra aqui: o registro e ato da gerencia).
"""
import hashlib
import json
import os
import subprocess
import sys

ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
LIVRO = r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl"
PY = sys.executable
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "rotas")
os.makedirs(OUT, exist_ok=True)

CONSULTAS = {
    "C01_tempo_santo": "tempo.santo|tempo_santo|kadosh",
    "C02_F1_TEMPO": "F1\\.TEMPO|f1_tempo",
    "C03_operador_de_tempo_pauli": "operador de tempo|time operator|teorema de pauli|pauli.s theorem",
    "C04_liouville": "liouville",
    "C05_ciclo_limite": "ciclo limite|limit cycle|espectro periferico",
    "C06_fock_habitante": "FockCertificate|habitante",
    "C07_identity_flow_not_kms": "identity_flow_not_kms|NonKMSProbe",
    "C08_tempo_e_o_verbo": "tempo e o verbo|tempo é o verbo|o tempo e o verbo",
    "C09_atrator_repousa": "repousa|repousar",
    "C10_agape_fundacao": "agape|fundacao",
    "C11_singularidade_atrator": "singularidade_le_atrator|F1\\.ATRATOR",
    "C12_tipagem_verbo": "tipagem_do_verbo|v386",
    "C13_dual_scaling": "dual_scaling|DualScalingData",
    "C14_posto_rank": "posto.rank|POSTO=RANK|posto_rank",
    "C15_frequencia": "F1\\.FREQUENCIA|frequencia",
    "C16_fractal_dephasing": "fractal_dephasing|defasagem fractal",
    "C17_tempo_termico": "tempo termico|thermal time|connes.rovelli",
    "C18_formal_dominio": "^formal\\.",
}
VER = ["formal.tempo_santo_fluxo_e_dissipacao", "formal.singularidade_le_atrator",
       "quantica.pilar_v384_rodada_completa", "umpy.v390.selo_fundacao_agape",
       "kernel.leitura_cria_o_objeto_07out", "kernel.v386_tipagem_do_verbo",
       "formal.f1_2.dual_scaling_reuse_011", "programa.auditoria.f1_2_ponte_v351_07out",
       "quantica.inventario_gkls_um_py_kernel"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(args):
    r = subprocess.run([PY, "-B", "-X", "utf8", ROTAS] + args, capture_output=True, timeout=300)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def main():
    antes = sha(LIVRO)
    resumo = {"livro_sha256_antes": antes, "consultas": {}, "ver": {}}
    for nome, padrao in CONSULTAS.items():
        rc, txt = run(["consultar", padrao, "--limite", "200"])
        with open(os.path.join(OUT, nome + ".json"), "wb") as f:
            f.write(txt.encode("utf-8"))
        try:
            d = json.loads(txt)
            resumo["consultas"][nome] = {"padrao": padrao, "n": d.get("n"),
                                         "rotas": [(x["rota_id"], x["status"]) for x in d.get("rotas", [])][:40]}
        except Exception as e:  # falha visivel
            resumo["consultas"][nome] = {"padrao": padrao, "erro": repr(e), "rc": rc}
    for rid in VER:
        rc, txt = run(["ver", rid])
        with open(os.path.join(OUT, "VER_" + rid.replace(".", "_") + ".json"), "wb") as f:
            f.write(txt.encode("utf-8"))
        try:
            d = json.loads(txt)
            if "erro" in d:
                resumo["ver"][rid] = {"existe": False, "erro": d["erro"]}
            else:
                rot = d["rota"]
                resumo["ver"][rid] = {"existe": True, "dominio": rot.get("dominio"), "status": rot.get("status"),
                                      "titulo": rot.get("titulo"), "n_registros": len(d.get("registros", []))}
        except Exception as e:
            resumo["ver"][rid] = {"erro": repr(e), "rc": rc}
    rc, txt = run(["modelo"])
    with open(os.path.join(OUT, "MODELO.json"), "wb") as f:
        f.write(txt.encode("utf-8"))
    depois = sha(LIVRO)
    resumo["livro_sha256_depois"] = depois
    resumo["livro_inalterado"] = antes == depois
    with open(os.path.join(OUT, "RESUMO_CONSULTAS.json"), "wb") as f:
        f.write(json.dumps(resumo, ensure_ascii=False, indent=1).encode("utf-8"))
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(resumo, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
