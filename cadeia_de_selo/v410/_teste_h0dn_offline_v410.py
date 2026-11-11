# -*- coding: utf-8 -*-
"""_teste_h0dn_offline_v410.py -- ENSAIO OFFLINE do registro H0DN (D72) antes do gerador: monta o contrato, o texto e os insumos (registros_h0dn_v410), injeta as guardas herdadas (como gerar_candidato faz), e roda h0dn_bg1_v410
sobre uma COPIA do core da v409 selada (base_v409) com beta em runtime; imprime as 12 checagens e o veredito. Controle negativo: um pino adulterado tem de recusar; um vetor com a covariancia fechada e z_null >= 5 tem de cair no ramo 4.
Grava TESTE_H0DN_OFFLINE_v410.json (o gerar_relatorio o le, informativo). uso: python -B -X utf8 _teste_h0dn_offline_v410.py   (sem -I: numpy e' do site do usuario, D77f)"""
import copy, json, math, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402   (injeta no runtime_v410 as guardas herdadas)
import registros_h0dn_v410 as RH  # noqa: E402
import runtime_h0dn_v410 as RTH  # noqa: E402
RT = GF.RT
j = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto.json"), encoding="utf-8")); core0 = j["core"]
selo0 = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto_selo.json"), encoding="utf-8"))
CONTR = RH.contrato_h0dn(core0, selo0); TXT = RH.texto_h0dn(); INS = RH.insumos_embutidos()
print("contrato: n_checks", CONTR["n_checks"], "| insumos", {k: v["bytes"] for k, v in CONTR["insumos"].items()}, "| pinos freeze", CONTR["n_pinos_freeze"], "| vetores c6", len(CONTR["vetores_c6"]))
# o runtime do H0DN usa as funcoes do bloco v410 (guarda das frases, _v398_beta, P18) como no um.py: injeta-as no modulo
RTH._V410_H0DN_CONTRACT = CONTR; RTH._V410_H0DN_TEXT = TXT; RTH._V410_H0DN_INSUMOS = INS
RTH._v410_guarda_frases = RT._v410_guarda_frases; RTH._v392_guarda_texto = RT._v392_guarda_texto
# _v398_beta do um.py: (beta_rt, rel_diff, dois_nomes, ok); aqui o equivalente com o alfa CODATA do proprio um.py base (lido por ast), nunca literal
import ast, re  # noqa: E402
T0 = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()
alpha = ast.literal_eval(re.search(r"^SEALED_CODATA_ALPHA = ([0-9.e-]+)", T0, re.M).group(1))
beta_rt = alpha * math.sqrt(math.e)
RTH._v398_beta = lambda core_: (beta_rt, abs(beta_rt - core_.get("beta", beta_rt)) / beta_rt, True, abs(beta_rt - core_.get("beta", beta_rt)) <= 1e-9 * beta_rt)
core = copy.deepcopy(core0); core["beta"] = core0.get("beta")
out = RTH.h0dn_bg1_v410(core)
print("veredito:", out["verdict"]); print("all_verified:", out["all_verified"], "| runtime_executed:", out["runtime_executed"], "| observed_vector_read:", out["observed_vector_read"])
for c in (out.get("mechanics") or {}).get("checks") or []:
    print("  %-4s %s  %s" % (c["id"], "OK " if c["ok"] else "FAIL", c["descricao"][:150]))
if out.get("error"):
    print("ERRO:", out["error"])
v = out.get("values") or {}
print("K", v.get("K"), "| log10K", v.get("log10K"), "| z*", v.get("z_star"), "| z* um.py", v.get("z_star_fase9_v1_no_um_py"), "| K um.py", v.get("K_fase9_v1_no_um_py"))
for d in v.get("D_esperado") or []:
    print("  D", d["modelo"], d["D"], "entrega", d["D_entrega"], "| poder", d["poder_analitico"], "entrega", d["poder_analitico_entrega"], "| MC", d["poder_mc_entrega"], d["ic95_mc_entrega"])
for x in v.get("vetores_c6") or []:
    print("  c6", x["nome"], "ramo", x["ramo"], "esperado", x["ramo_esperado"], x["outcome"], "|", x["cabeca"][:90], "| ok", x["ok"])
print("fonte sha256:", v.get("veredito_h0dn_source_sha256"))
print("frases:", v.get("frases_violacoes"), "| p18:", v.get("p18_violacoes"))
# ---- controles negativos (a recusa e' resultado): (a) um pino adulterado; (b) o gate trocado
INS_bad = copy.deepcopy(INS); INS_bad["BG1.json"]["b64"] = INS_bad["BG1.json"]["b64"][:-4] + "AAA="
RTH._V410_H0DN_INSUMOS = INS_bad; core_b = copy.deepcopy(core0); out_b = RTH.h0dn_bg1_v410(core_b); print("controle negativo (pino adulterado):", out_b["verdict"], "| all_verified", out_b["all_verified"])
RTH._V410_H0DN_INSUMOS = INS; core_c = copy.deepcopy(core0); core_c["qg_closure"]["gate"]["verdict"] = "TGL_OUTRO"; out_c = RTH.h0dn_bg1_v410(core_c)
print("controle negativo (gate trocado):", out_c["verdict"], "| c9", [c["ok"] for c in out_c["mechanics"]["checks"] if c["id"] == "c9"])
core_d = copy.deepcopy(core0); core_d["hubble_ratio_v387"]["transcribed"]["z_star"] = 1100.0; out_d = RTH.h0dn_bg1_v410(core_d)
print("controle negativo (z* da Fase 9 trocado):", out_d["verdict"], "| c2", [c["ok"] for c in out_d["mechanics"]["checks"] if c["id"] == "c2"])
_tudo = bool(out["all_verified"] and not out_b["all_verified"] and not out_c["all_verified"] and not out_d["all_verified"])
print("TUDO PASSOU" if _tudo else "FALHOU")
_J = {"tudo_passou": _tudo, "quando": __import__("datetime").datetime.now().isoformat(timespec="seconds"), "veredito": out["verdict"], "all_verified": out["all_verified"], "observed_vector_read": out["observed_vector_read"], "n_checks": (out.get("mechanics") or {}).get("n_checks"), "checks": [(c["id"], c["ok"]) for c in (out.get("mechanics") or {}).get("checks") or []],
      "n_pinos": v.get("n_pinos"), "ramos_vistos": v.get("ramos_vistos"), "n_caminhos_tocados": v.get("n_caminhos_tocados"), "sob_pasta_vedada": v.get("sob_pasta_vedada"), "com_nome_vedado": v.get("com_nome_vedado"), "veredito_h0dn_source_sha256": v.get("veredito_h0dn_source_sha256"),
      "controles_negativos": {"pino_adulterado": out_b["verdict"], "gate_trocado": out_c["verdict"], "z_star_trocado": out_d["verdict"]}, "nota": "teste OFFLINE do registro sobre o core da v409 selada (nao e' o rito nem o ensaio); " + DL.FRASE_H0DN_OBRIGATORIA_PT}
_p = os.path.join(HERE, "TESTE_H0DN_OFFLINE_v410.json"); open(_p + ".tmp", "w", encoding="utf-8").write(json.dumps(_J, ensure_ascii=False, indent=1, default=str)); os.replace(_p + ".tmp", _p)
