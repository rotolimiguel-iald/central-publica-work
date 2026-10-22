"""Monta RESULTADO.md a partir do modelo + dados (numeros e hashes inseridos por script, nunca digitados).

Uso: python montar_resultado.py <dir_work>
"""
import csv
import hashlib
import json
import os
import statistics
import sys

W = sys.argv[1]
S = os.path.join(W, "saida_rodada")


def rd(p):
    return list(csv.DictReader(open(p, encoding="utf-8", newline="")))


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


casos = rd(os.path.join(S, "n_req_por_caso.csv"))
ver = json.load(open(os.path.join(W, "veredito.json"), encoding="utf-8"))
pr = json.load(open(os.path.join(W, "PREREGISTRO.json"), encoding="utf-8"))
mc = rd(os.path.join(S, "verificacao_mc.csv"))
rob = rd(os.path.join(S, "robustez_numerica.csv"))
amb = json.load(open(os.path.join(S, "AMBIENTE_RODADA.json"), encoding="utf-8"))
der = {r["case_id"]: r for r in rd(os.path.join(W, "derivados_KK_por_caso.csv"))}
tabelas = open(os.path.join(W, "tabelas.md"), encoding="utf-8").read()
modelo = open(os.path.join(W, "ferramentas", "resultado_modelo.md"), encoding="utf-8").read()
arnaud_pdf = "C:\\Users\\rotol\\.claude\\projects\\c--IALD-Central-de-Patentes\\6da8f00d-d44f-4888-a88d-fc9f73eead3d\\tool-results\\webfetch-1792660207056-7q49ff.pdf"


def ns(fam, ell=None):
    return sorted(int(r["n_req"]) for r in casos if r["familia"] == fam and r["n_req"] != "" and (ell is None or float(r["ell_km"]) == ell))


p1, p2, p3 = ns("P1"), ns("P2"), ns("P3")
nalc = ver["regra"]["N_alcancavel_neutrinos_esperados"]
b2 = min((r for r in casos if r["familia"] == "P2"), key=lambda r: (int(r["n_req"]), r["case_id"]))
d2 = der[b2["case_id"]]
med20_n = ns("P2", 20)[len(ns("P2", 20)) // 2]
med20_case = sorted((r for r in casos if r["familia"] == "P2" and float(r["ell_km"]) == 20 and int(r["n_req"]) == med20_n), key=lambda r: r["case_id"])[0]
dm = der[med20_case["case_id"]]
nkl = [int(r["n_req"]) * float(r["kl_h1_h0_cap"]) for r in casos if r["familia"] == "P2"]
q1 = [float(r["q1_sat"]) for r in casos if r["familia"] == "P1"]
dc = [abs(float(r["c_hat_mc"]) - float(r["c_lattice"])) for r in mc if r.get("c_hat_mc") not in ("", None, "nan")]
dp = [abs(float(r["poder_mc"]) - float(r["poder_lattice"])) for r in mc if r.get("poder_mc") not in ("", None)]
dn = [abs(int(r["n_req_variante"]) - int(r["n_req_base"])) for r in rob if r.get("n_req_variante") not in ("", None)]
dcr = [abs(float(r["c_variante"]) - float(r["c_base"])) for r in rob if r.get("c_variante") not in ("", None)]
um = amb["um_py"]
gates = ver["gates"]


def pct(x):
    return (f"{100 * x:.0f}%" if x >= 0.095 else f"{100 * x:.1f}%").replace(".", ",")


def sci(x):
    m, e = f"{x:.1e}".split("e")
    sup = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return f"{m.replace('.', ',')}×10{str(int(e)).translate(sup)}"


# ---- artefatos
papeis = {
    "PREREGISTRO.json": "pre-registro (familias, estatistica, numerica, taxa K-K, veredito, limites)",
    "PREREGISTRO.sha256": "sha256 de PREREGISTRO.json e veredito.py",
    "PINS.json": "pinos (sha256 do pre-registro e dos 4 scripts); a rodada e o veredito recusam divergencia",
    "veredito.py": "veredito pinado (sem limiar proprio)",
    "veredito.json": "veredito aplicado + portas + resumos",
    "derivados_KK_por_caso.csv": "fusoes, exposicao, D_max, massa, eventos/seculo por caso (formulas pinadas em veredito.py)",
    "tabelas.md": "tabelas A-G geradas dos dados crus",
    "checagem_continua.json": "checagem independente KL tempo continuo x celulas (pos-rodada, sem alterar nada)",
    "ANCORAS_LITERATURA.json": "frases-ancora localizadas por script (pagina + trecho)",
    "registro_mapa_rito9_poder_realista.json": "registro PRONTO para o mapa (nao registrado)",
    "rodada_oficial_stdout.txt": "log da rodada oficial",
    "saida_rodada/n_req_por_caso.csv": "DADOS CRUS: n_req e diagnosticos por caso (483)",
    "saida_rodada/varredura_n.csv": "DADOS CRUS: c_n, poder, mediana por (caso, n) avaliado",
    "saida_rodada/verificacao_mc.csv": "DADOS CRUS: simulacao por importancia x rede",
    "saida_rodada/robustez_numerica.csv": "DADOS CRUS: variantes numericas",
    "saida_rodada/perfis.csv": "definicao dos perfis (picos w, mu, sigma)",
    "saida_rodada/testes_nucleo.json": "testes analiticos do nucleo",
    "saida_rodada/AMBIENTE_RODADA.json": "ambiente, um.py lido, semente, amostra",
    "saida_rodada/MANIFEST_RODADA.json": "sha256 de cada saida da rodada",
}
linhas = ["## Artefatos (sha256 lidos por script; 16 primeiros hex)\n", "| arquivo | sha256[:16] | papel |", "|---|---|---|"]
arqs = []
for raiz, dirs, files in os.walk(W):
    dirs[:] = [d for d in dirs if d not in ("__pycache__", "dev_dry")]
    for fn in files:
        if fn == "RESULTADO.md":
            continue
        rel = os.path.relpath(os.path.join(raiz, fn), W).replace("\\", "/")
        arqs.append(rel)
for rel in sorted(arqs):
    papel = papeis.get(rel)
    if papel is None:
        if rel.startswith("ferramentas/"):
            papel = "script/modelo"
        elif rel.startswith("fontes_extraidas/"):
            papel = "texto extraido de PDF (dado nao confiavel, lido com pypdf em python -I)"
        elif rel.startswith("fontes_baixadas/"):
            papel = "PDF baixado (K-K, arXiv:1710.05922v3)"
        else:
            papel = ""
    linhas.append(f"| `{rel}` | `{sha(os.path.join(W, rel))[:16]}` | {papel} |")
linhas.append("")
linhas.append(f"Pino: PREREGISTRO.json = `{sha(os.path.join(W, 'PREREGISTRO.json'))}`; veredito.py = `{sha(os.path.join(W, 'veredito.py'))}`.")
linhas.append(f"PDF Cusinato (tool-results, dado nao confiavel) = `{pr['fontes_literatura']['cusinato2022']['sha256_pdf']}`; PDF Arnaud et al. = `{sha(arnaud_pdf)}`. "
              "`dev_dry/` guarda so os ensaios do pipeline em perfis FORA das familias (nao fazem parte do estudo).")
artefatos = "\n".join(linhas)

K = {
    "VEREDITO": ver["veredito"],
    "SHA_VEREDITO_PY": sha(os.path.join(W, "veredito.py")),
    "SHA_PREREG": sha(os.path.join(W, "PREREGISTRO.json")),
    "SHA_PINS": sha(os.path.join(W, "PINS.json")),
    "NALC": f"{nalc:g}".replace(".", ","),
    "P1_MIN": p1[0], "P1_MAX": p1[-1], "P2_MIN": p2[0], "P2_MAX": p2[-1], "P2_MED20": med20_n, "P3_MIN": p3[0], "P3_MAX": p3[-1],
    "FATOR_P1": f"{p1[0] / nalc:,.0f}".replace(",", "."), "FATOR_P2": f"{p2[0] / nalc:,.0f}".replace(",", "."),
    "N_GATES": len(gates), "N_GATES_OK": sum(1 for v in gates.values() if v), "N_CASOS": ver["n_casos"],
    "P2B_FUSOES": f"{float(d2['fusoes_necessarias_ate_Deff']):,.0f}".replace(",", "."),
    "P2B_ANOS": f"{float(d2['anos_com_detector_declarado']):,.0f}".replace(",", "."),
    "P2B_D": f"{float(d2['Dmax_um_evento_Mpc']):.2f}".replace(".", ","),
    "P2B_ID": b2["case_id"],
    "P2B_EXPO": f"{float(d2['exposicao_Mt_ano']):,.0f}".replace(",", "."),
    "P2B_MASSA": f"{float(d2['massa_detector_Mt_para_max_eventos']):,.0f}".replace(",", "."),
    "P2B_EVSEC": sci(float(d2["eventos_por_seculo_dentro_de_Dmax"])),
    "P2M_FUSOES": f"{float(dm['fusoes_necessarias_ate_Deff']):,.0f}".replace(",", "."),
    "P1B_ID": ver["melhor_caso_realista"]["case_id"],
    "N_P2": len(p2),
    "NKL_MIN": f"{min(nkl):.1f}".replace(".", ","), "NKL_MAX": f"{max(nkl):.1f}".replace(".", ","),
    "Q1SAT_MIN": pct(min(q1)), "Q1SAT_MAX": pct(max(q1)), "Q1SAT_MED": pct(statistics.median(q1)),
    "ALPHA_LINHA": um["linha"], "ALPHA_TXT": um["texto"], "SHA_UM": um["sha256"], "SHA_UM16": um["sha256"][:8],
    "BETA": f"{amb['beta_runtime']!r}".replace(".", ","),
    "MC_PONTOS": len(mc), "MC_CASOS": len(set(r["case_id"] for r in mc)),
    "MC_MAXDC": f"{max(dc):.3f}".replace(".", ","), "MC_MAXDP": f"{max(dp):.4f}".replace(".", ","),
    "ROB_N": len(rob), "ROB_MAXDN": max(dn), "ROB_MAXDC": f"{max(dcr):.4f}".replace(".", ","),
    "SHA_ARNAUD16": sha(arnaud_pdf)[:16],
    "SEQS": ", ".join(str(s) for s in pr["mapa_de_rotas"]["seqs_do_historico"]),
    "MAPA_N": f"{pr['mapa_de_rotas']['n_registros']:,}".replace(",", "."), "MAPA_CABECA": pr["mapa_de_rotas"]["cabeca"],
    "TABELAS": tabelas,
    "ARTEFATOS": artefatos,
}
txt = modelo
for k, v in K.items():
    txt = txt.replace("{{" + k + "}}", str(v))
assert "{{" not in txt, "placeholder nao resolvido: " + txt[txt.index("{{"): txt.index("{{") + 40]
assert txt.splitlines()[0] == "RITO 9 — PODER REALISTA — 22/10"
with open(os.path.join(W, "RESULTADO.md"), "x", encoding="utf-8", newline="\n") as f:
    f.write(txt)
print("RESULTADO.md escrito:", len(txt), "caracteres")
