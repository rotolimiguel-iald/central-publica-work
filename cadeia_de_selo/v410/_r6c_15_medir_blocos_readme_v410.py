# -*- coding: utf-8 -*-
"""_r6c_15_medir_blocos_readme_v410.py -- ADITIVO 2: mede (so' leitura) os dois blocos do README do gerador do handoff, como o teste sem candidato o faz (a parte que COMPOE os textos, com numeros sinteticos):
os bytes em UTF-8 do README_FRENTE, do README_O_QUE_SAI e do ponteiro, e o resultado de guardas_dos_textos sobre cada bloco SOZINHO (a guarda das frases da v410, o portao do G1 e as regras de forma). Grava _r6c_BLOCOS_README_v410.json."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
PKG = os.path.dirname(os.path.abspath(__file__)); HERE = os.path.join(PKG, "pos_rito")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(PKG))), "tools")); sys.path.insert(0, PKG)
from custodia_g1 import textos as TX  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402
import delta_v410 as DL  # noqa: E402
src = open(os.path.join(HERE, "textos_custodia_handoff_v410.py"), encoding="utf-8").read().replace("\r\n", "\n")
i0 = src.index("REV_EN = "); i1 = src.index("# ------------------------------------------------------------------ 3. as guardas")
FJ = json.load(open(os.path.join(PKG, "kernel", "FLAGS_v410.json"), encoding="utf-8"))
NF_I = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.IALD2"); NF_A = sum(1 for f_ in FJ["flags"] if f_[2] == "TGLExt.AEscala")
N = {"modulos": DL.N_BUNDLE, "modulos_ok": DL.N_BUNDLE, "bandeiras": NF_I + NF_A, "bandeiras_iald2": NF_I, "bandeiras_aescala": NF_A, "ancoras": len(DL.ANCORAS), "ancoras_aescala": len(DL.ANCORAS_AESCALA), "nomes_aescala": len(DL.NOMES_AESCALA), "nomes_novos": len(DL.NOMES_NOVOS_AESCALA), "campos_novos": len(DL.CAMPOS_NOVOS_AESCALA),
     "ea_checks": DL.N_CHECKS_AESCALA, "hm_checks": DL.N_CHECKS_HMS13, "fontes": DL.HMS13_CAMPOS["fontes_primarias"], "calibradores": DL.HMS13_CAMPOS["calibradores"], "checks": DL.N_CHECKS_FECHO, "const": 12345, "teor": 6789, "falas": DL.N_FALAS_V410, "escada_a": 12187, "escada_b": 12264,
     "pin": "0123456789abcdef", "respostas": len(DL.RESPOSTAS_DO_OPERADOR), "inst_n": DL.INSTANCIA_SIM["n"], "inst_atr": 2 ** DL.INSTANCIA_SIM["n"], "inst_sol": 1, "nao_sol": 0, "per": "06 a 10/11/2026", "n_trecho": len(DL.VERBATIM_SO_O_TRECHO), "h0dn_checks": DL.N_CHECKS_H0DN, "h0dn_pinos": DL.N_PINOS_FREEZE_R2 + 2, "h0dn_ramos": 6, "h0dn_p1": "00,0 %", "h0dn_p2": "00,0 %"}
G = {"REV": None, "N": N, "DL": DL, "GF": GF, "TX": TX, "re": re}
exec(compile(src[i0:i1], "textos_custodia_handoff_v410.py[textos]", "exec"), G)
out = {"contrato": "R6c_BLOCOS_README_v410", "blocos": {}}
for ident, t in list(G["BLOCOS_README"]) + [("README_PONTEIRO_ABSTRACT (parte do README_O_QUE_SAI; medido a parte)", G["README_PONTEIRO_ABSTRACT"])]:
    g, f = G["guardas_dos_textos"]([(ident.split(" ")[0], t)], {N["pin"]}); r = g[ident.split(" ")[0]]
    out["blocos"][ident] = {"bytes_utf8": len(t.encode("utf-8")), "chars": len(t), "sha256": hashlib.sha256(t.encode("utf-8")).hexdigest(), "guarda_frases_v410": r["guarda_frases_v410"], "portao_g1": r["portao_g1"], "forma": r["forma"], "limpo": not f}
    print("%-22s %5d B em UTF-8 | guarda das frases: %s | portao do G1: %s | forma: %s" % (ident.split(" ")[0], len(t.encode("utf-8")), r["guarda_frases_v410"] or "limpa", r["portao_g1"] or "limpo", r["forma"] or "limpa"))
out["teto_b"] = G["README_FRENTE_TETO_B"]; out["montado_no_handoff_chars"] = len(G["montar_blocos"](G["TEXTOS"], G["README_EVIDENTE"], G["BLOCOS_README"], "v410"))
p = os.path.join(PKG, "_r6c_BLOCOS_README_v410.json"); open(p + ".tmp", "w", encoding="utf-8", newline="\n").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
print("teto do README_FRENTE:", out["teto_b"], "B | todos limpos:", all(v["limpo"] for v in out["blocos"].values()))
