# -*- coding: utf-8 -*-
"""Constroi spec/REGISTRO_DH_V2_C1.json: o REGISTRO D-H (admissao das fontes pelo operador em 23/10/2026) com as FONTES PINADAS por sha256 e as REGRAS DE EXTRACAO.
Cada regra e' TESTADA contra os bytes (exatamente 1 ocorrencia) e o resultado e' comparado com o centro declarado no spec V2 R5.2 (tolerancia 1e-9).
Rodar:  python -P -E -X utf8 ferramentas/build_registro_dh.py   (dado nao confiavel: so leitura de bytes; nenhum calculo estatistico)."""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "runner"))
import f9v2_extract as X  # noqa: E402

R52 = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.1\PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json"
OP = r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_23out_fase9_decisoes_unica_palavra_verbatim.txt"

HTML = "html"
RULES = {
    "L1_sh0es_r22": dict(file="fontes/L1_sh0es_r22_arxiv_2112.04510/sh0es_2022.html", kind=HTML, fonte="Riess et al. 2022, ApJL 934, L7 (arXiv:2112.04510), resumo",
        regex=r"Our baseline result from the Cepheid-SN sample is H0=(?P<H0>\d+\.\d+)\+-(?P<sig>\d+\.\d+) km/s/Mpc",
        H0_group="H0", sigma_rule=dict(kind="direct", group="sig")),
    "L1b_sh0es_r25": dict(file="fontes/L1b_riess2025_arxiv_2509.01667/abs_2509.01667.html", kind=HTML, fonte="Riess et al. 2025 (arXiv:2509.01667), resumo — baixado em 23/10/2026",
        regex=r"Combining JWST Cepheid measurements in 19 hosts \(24 SNe Ia\) with HST data \(37 hosts, 42 SNe Ia\) yields H0 = (?P<H0>\d+\.\d+) \+/- (?P<sig>\d+\.\d+) km/s/Mpc",
        H0_group="H0", sigma_rule=dict(kind="direct", group="sig")),
    "L2_cchp": dict(file="fontes/L2_cchp_arxiv_2408.06153v3/cchp_2025_v3.html", kind=HTML, fonte="Freedman et al. 2025 (arXiv:2408.06153v3), resumo",
        regex=r"\$H_0\$ = (?P<H0>\d+\.\d+) \$\\pm\$ (?P<stat>\d+\.\d+) \(stat\) \$\\pm\$ (?P<sys>\d+\.\d+) \(sys\) \$\\pm\$ (?P<sn>\d+\.\d+) \(\$\\sigma_\{SN\}\$\), based on the TRGB method alone, with a total of 24 SN Ia calibrators",
        H0_group="H0", sigma_rule=dict(kind="quadrature", groups=["stat", "sys", "sn"])),
    "L3_sbf": dict(file="fontes/L3_sbf_arxiv_2502.15935v2/sbf_2502.15935v2.html", kind=HTML, fonte="Jensen et al. 2025 (arXiv:2502.15935v2), resumo",
        regex=r"updated value of \$H_0 = (?P<H0>\d+\.\d+)\\pm (?P<stat>\d+\.\d+)\$ \(statistical\) \$\\pm (?P<sys>\d+\.\d+)\$~\(systematic\) km/s/Mpc",
        H0_group="H0", sigma_rule=dict(kind="quadrature", groups=["stat", "sys"])),
    "L4_masers_5": dict(file="fontes/L4_masers_arxiv_2001.09213v2/masers_2001.09213v2.pdf", kind="pdf", page=6, fonte="Pesce et al. 2020 (arXiv:2001.09213v2), PDF, Tabela 2, tratamento (1), linha NGC 4258 (jackknife: cinco masers sem NGC 4258)",
        regex=r"NGC 4258 (?P<H0>\d+ ?\.\d+)\+(?P<plus>\d+\.\d+) -(?P<minus>\d+\.\d+) Fit using all galaxies: (?P<H6>\d+\.\d+)\+(?P<s6p>\d+\.\d+) -(?P<s6m>\d+\.\d+) \(2\) Fit for",
        H0_group="H0", sigma_rule=dict(kind="mean_asym", plus="plus", minus="minus")),
    "L4_masers_6": dict(file="fontes/L4_masers_arxiv_2001.09213v2/masers_2001.09213v2.pdf", kind="pdf", page=6, fonte="Pesce et al. 2020 (arXiv:2001.09213v2), PDF, Tabela 2, tratamento (1), 'Fit using all galaxies' (seis masers) — diagnostico",
        regex=r"NGC 4258 (?P<H5>\d+ ?\.\d+)\+(?P<p5>\d+\.\d+) -(?P<m5>\d+\.\d+) Fit using all galaxies: (?P<H0>\d+\.\d+)\+(?P<plus>\d+\.\d+) -(?P<minus>\d+\.\d+) \(2\) Fit for",
        H0_group="H0", sigma_rule=dict(kind="mean_asym", plus="plus", minus="minus")),
    "L5_tdcosmo": dict(file="fontes/L5_tdcosmo_arxiv_2506.03023v4/tdcosmo_2025_v4.html", kind=HTML, fonte="TDCOSMO 2025 (arXiv:2506.03023v4), resumo",
        regex=r"we find \$H_0=(?P<H0>\d+\.\d+)\^\{\+(?P<plus>\d+\.\d+)\}_\{-(?P<minus>\d+\.\d+)\}\$ km s\$\^\{-1\}\$ Mpc\$\^\{-1\}\$\.",
        H0_group="H0", sigma_rule=dict(kind="mean_asym", plus="plus", minus="minus")),
    "L6_sirenes": dict(file="fontes/L6_lvk_o4a_arxiv_2509.04348/abs_2509.04348v1.html", kind=HTML, fonte="LVK, GWTC-4.0 cosmologia (arXiv:2509.04348v1, O4a), resumo — baixado em 23/10/2026; v1 e v2 trazem 76,6; a v3 (publicada) traz 75,4 e fica ao lado",
        regex=r"we estimate \$H_0 = (?P<H0>\d+\.\d+)\^\{\+(?P<plus>\d+\.\d+)\}_\{-(?P<minus>\d+\.\d+)\} \(",
        H0_group="H0", sigma_rule=dict(kind="mean_asym", plus="plus", minus="minus")),
}
PAPEL = {
    "L1_sh0es_r22": "primary_ladder", "L1b_sh0es_r25": "R_r25_replacement_only (replica ao lado de L1; nunca somada)", "L2_cchp": "CCHP_TRGB_only_24_SN_Ia",
    "L3_sbf": "TRGB_to_SBF", "L4_masers_5": "primary_decision_reader", "L4_masers_6": "six_maser_diagnostic_only",
    "L5_tdcosmo": "time_delay_lenses", "L6_sirenes": "S_com_sirenes_diagnostic_only (fora do composto)",
}
AO_LADO = [
    ("fontes/L6_lvk_o4a_arxiv_2509.04348/abs_2509.04348v2.html", "L6 v2: mesmo 76,6 +13,0/-9,5 da v1"),
    ("fontes/L6_lvk_o4a_arxiv_2509.04348/abs_2509.04348_v3_ao_lado.html", "L6 v3 (publicada, ApJL 2026): 75,4 +12,8/-9,1 — NAO admitida; diagnostico fora do composto; registrada para que a troca de versao fique visivel"),
    ("fontes/L6_lvk_o4a_arxiv_2509.04348/arxiv_2509.04348_v3_ao_lado.pdf", "L6 v3 PDF integral (confirma 75,4 +12,8/-9,1 no texto)"),
]
DOWNLOADS = [
    dict(arquivo="fontes/L1b_riess2025_arxiv_2509.01667/abs_2509.01667.html", url="https://arxiv.org/abs/2509.01667", http=200),
    dict(arquivo="fontes/L6_lvk_o4a_arxiv_2509.04348/abs_2509.04348v1.html", url="https://arxiv.org/abs/2509.04348v1", http=200),
    dict(arquivo="fontes/L6_lvk_o4a_arxiv_2509.04348/abs_2509.04348v2.html", url="https://arxiv.org/abs/2509.04348v2", http=200),
    dict(arquivo="fontes/L6_lvk_o4a_arxiv_2509.04348/abs_2509.04348_v3_ao_lado.html", url="https://arxiv.org/abs/2509.04348", http=200),
    dict(arquivo="fontes/L6_lvk_o4a_arxiv_2509.04348/arxiv_2509.04348_v3_ao_lado.pdf", url="https://arxiv.org/pdf/2509.04348", http=200),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    spec = json.load(open(R52, encoding="utf-8"))["spec"]
    readers = spec["leitores"]
    op = open(OP, "rb").read()
    out_readers = {}
    for rid, rule in RULES.items():
        raw = open(os.path.join(ROOT, *rule["file"].split("/")), "rb").read()
        r = dict(rule)
        r["sha256"], r["bytes"] = sha(raw), len(raw)
        ext = X.extract_reader({k: r[k] for k in ("kind", "regex", "H0_group", "sigma_rule") if k in r} | ({"page": r["page"]} if "page" in r else {}), raw)
        d = readers[rid]
        dH0, dsig = d["H0"], d["sigma"]
        ok = abs(ext["H0"] - dH0) < 1e-9 and abs(ext["sigma"] - dsig) < 1e-9
        r["extraido_no_build"] = {"H0": ext["H0"], "sigma": ext["sigma"], "trecho": ext["trecho"]}
        r["declarado_no_spec_R5_2"] = {"H0": dH0, "sigma": dsig}
        r["extraido_igual_ao_declarado_1e-9"] = ok
        r["papel"] = PAPEL[rid]
        r["admitido_pelo_operador"] = True
        r["verificacao_documental"] = "REAL_DOCUMENTARY_HASH_ONLY"
        out_readers[rid] = r
        print(rid, "OK" if ok else "DIVERGE", ext["H0"], ext["sigma"], "| declarado", dH0, dsig)
        if not ok:
            raise SystemExit("extracao diverge do declarado: " + rid)
    side = []
    for rel, nota in AO_LADO:
        raw = open(os.path.join(ROOT, *rel.split("/")), "rb").read()
        side.append({"file": rel, "sha256": sha(raw), "bytes": len(raw), "nota": nota, "admitido_pelo_operador": False})
    dls = []
    for d in DOWNLOADS:
        raw = open(os.path.join(ROOT, *d["arquivo"].split("/")), "rb").read()
        dls.append({**d, "sha256": sha(raw), "bytes": len(raw), "baixado_em": "2026-10-23", "por": "gerencia c1 (subagente), curl, download autorizado pelo operador"})
    reg = {
        "schema": "F9V2C1_REGISTRO_DH_V1",
        "id": "REGISTRO_DH_V2_C1_23OUT2026",
        "decisao_do_operador": {
            "data": "2026-10-23", "item": "D-H",
            "texto": "admite os cinco leitores + masers_5 (PDF); L1b (Riess et al. 2025, arXiv:2509.01667) e L6 (sirenes LVK O4a, resumo de cosmologia do LVK) ENTRAM, com os bytes baixados e pinados por sha256 antes de congelar; papeis tipados mantidos (L1b replica ao lado de L1, nunca somada; L6 diagnostico fora do composto)",
            "fonte_verbatim": {"path": OP, "sha256": sha(op), "bytes": len(op), "frase": "de resto concordo com tudo, e acho que com isso eu também respondi todas as suas perguntas"},
            "leitura_da_gerencia": "o conteudo de (a)-(d) e' o da proposta da gerencia c1, aceita pelo operador em 23/10/2026 («de resto concordo com tudo, e acho que com isso eu tambem respondi todas as suas perguntas»); o ato D-H esta registrado na nota de 23/10 da memoria fase9-razao-de-hubble-05out.md",
            "estatuto": "[INPUT] decisao do operador; [REAL] bytes pinados; [DERIVED] regras de extracao testadas contra os bytes",
        },
        "admitidos": sorted(out_readers),
        "leitores": out_readers,
        "ao_lado_nao_admitidos": side,
        "downloads": dls,
        "n_alvos_declarados_predicado": "NOT gate_verified AND NOT operator_admitted_in_pinned_D_H_register, sobre o inventario V1.x inteiro (8 leitores)",
        "fundos_BG2_BG3": "diagnosticos fora do veredito; seguem [KNOWN]/[DECLARADO] (BG2 Planck 2018 67,36 +/- 0,54; BG3 68,5 +/- 0,6 sem fonte em disco); este registro admite LEITORES, nao fundos",
        "limites": [
            "SBF secao III.3 e TDCOSMO secao VIII.2.1: texto integral nao em disco (so resumo pinado); os centros vem do resumo",
            "L6: o resumo v1/v2 (76,6) e' o declarado desde V1; a v3 publicada diz 75,4; a troca nao altera o veredito (L6 fora do composto)",
        ],
    }
    p = os.path.join(ROOT, "spec", "REGISTRO_DH_V2_C1.json")
    b = json.dumps(reg, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    open(p + ".tmp", "wb").write(b)
    assert os.path.getsize(p + ".tmp") == len(b)
    os.replace(p + ".tmp", p)
    print("REGISTRO_DH", sha(b)[:16], len(b))


if __name__ == "__main__":
    main()
