# -*- coding: utf-8 -*-
"""_teste_hms13_offline_v410.py -- ENSAIO OFFLINE do registro documental HMS/13 (D80) antes do gerador: monta o contrato (lendo os pinos do HANDOFF e da ORDEM do Kimi, como o build fara), o texto e os insumos (registros_hms13_v410), injeta as guardas herdadas
(como gerar_candidato faz), roda h0dn_bg1_v410 e depois h0dn_fontes_hms13_v410 sobre uma COPIA do core da v409 selada (base_v409) com beta em runtime; imprime as 12 checagens e o veredito. Controles negativos: um insumo embutido adulterado; um ID a mais no contrato;
um campo obrigatorio trocado; o gate trocado; o h0dn ausente do core (nao e' posterior a nada); um caminho sob a pasta vedada tocado; um numero proibido plantado no mapa. Grava TESTE_HMS13_OFFLINE_v410.json. uso: python -B -X utf8 _teste_hms13_offline_v410.py (sem -I: numpy e' do site do usuario)"""
import base64, copy, hashlib, json, math, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402   (injeta no runtime_v410 as guardas herdadas)
import registros_h0dn_v410 as RH  # noqa: E402
import registros_hms13_v410 as RF  # noqa: E402
import runtime_h0dn_v410 as RTH  # noqa: E402
import runtime_hms13_v410 as RTF  # noqa: E402
RT = GF.RT
j = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto.json"), encoding="utf-8")); core0 = j["core"]
selo0 = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto_selo.json"), encoding="utf-8"))
CONTR_H = RH.contrato_h0dn(core0, selo0); TXT_H = RH.texto_h0dn(); INS_H = RH.insumos_embutidos()
CONTR_F = RF.contrato_hms13(core0, selo0, CONTR_H); TXT_F = RF.texto_hms13(); INS_F = RF.insumos_embutidos_hms13()
print("contrato HMS13: n_checks", CONTR_F["n_checks"], "| insumos", {k: v["bytes"] for k, v in CONTR_F["insumos"].items()}, "| pinos do build", len(CONTR_F["pinos_build"]), "| ids", len(CONTR_F["ids_calibradores"]), "| fontes", len(CONTR_F["fontes_primarias"]), "| guarda numerica", CONTR_F["guarda_numerica_no_build"]["permitidos"], CONTR_F["guarda_numerica_no_build"]["chaves_permitidas_vistas"])
# os runtimes usam as funcoes do bloco v410 (guarda das frases, _v398_beta, P18) como no um.py: injeta-as nos modulos
import ast, re  # noqa: E402
T0 = open(os.path.join(HERE, DL.BASE_DIR, "um.py"), encoding="utf-8").read()
alpha = ast.literal_eval(re.search(r"^SEALED_CODATA_ALPHA = ([0-9.e-]+)", T0, re.M).group(1)); beta_rt = alpha * math.sqrt(math.e)
_beta = lambda core_: (beta_rt, abs(beta_rt - core_.get("beta", beta_rt)) / beta_rt, True, abs(beta_rt - core_.get("beta", beta_rt)) <= 1e-9 * beta_rt)
RTH._V410_H0DN_CONTRACT = CONTR_H; RTH._V410_H0DN_TEXT = TXT_H; RTH._V410_H0DN_INSUMOS = INS_H; RTH._v410_guarda_frases = RT._v410_guarda_frases; RTH._v392_guarda_texto = RT._v392_guarda_texto; RTH._v398_beta = _beta
RTF._V410_HMS13_CONTRACT = CONTR_F; RTF._V410_HMS13_TEXT = TXT_F; RTF._V410_HMS13_INSUMOS = INS_F; RTF._v410_guarda_frases = RT._v410_guarda_frases; RTF._v392_guarda_texto = RT._v392_guarda_texto; RTF._v398_beta = _beta
RTF._v410_h0dn_decode = RTH._v410_h0dn_decode; RTF._v410_h0dn_vigia_arquivos = RTH._v410_h0dn_vigia_arquivos; RTF.veredito_h0dn = RTH.veredito_h0dn
core = copy.deepcopy(core0)
outH = RTH.h0dn_bg1_v410(core); assert outH["all_verified"] is True, outH["verdict"]
out = RTF.h0dn_fontes_hms13_v410(core)
print("veredito:", out["verdict"]); print("all_verified:", out["all_verified"], "| runtime_executed:", out["runtime_executed"], "| observed_vector_read:", out["observed_vector_read"], "| le_em_rito:", out["le_em_rito"])
for c in (out.get("mechanics") or {}).get("checks") or []:
    print("  %-4s %s  %s" % (c["id"], "OK " if c["ok"] else "FAIL", c["descricao"][:150]))
if out.get("error"):
    print("ERRO:", out["error"])
v = out.get("values") or {}
print("ids:", v.get("ids_calibradores")); print("fontes:", v.get("n_fontes_primarias"), "| estados:", sorted(set((v.get("estados_cobertura") or {}).values()))); print("numeros:", {k: (x if not isinstance(x, list) else len(x)) for k, x in (v.get("numeros") or {}).items()}); print("tocados:", v.get("n_caminhos_tocados"), "sob vedada:", v.get("sob_pasta_vedada"))
print("frases:", v.get("frases_violacoes"), "| p18:", v.get("p18_violacoes"))
# ---- controles negativos (a recusa e' resultado)
R = {}
_f = lambda r_: [c_["id"] for c_ in ((r_.get("mechanics") or {}).get("checks") or []) if not c_["ok"]]
INS_bad = copy.deepcopy(INS_F); INS_bad["VALIDACAO_FONTES_13.json"]["b64"] = INS_bad["VALIDACAO_FONTES_13.json"]["b64"][:-4] + "AAA="
RTF._V410_HMS13_INSUMOS = INS_bad; r_ = RTF.h0dn_fontes_hms13_v410(copy.deepcopy(core)); R["insumo_adulterado"] = (r_["verdict"], _f(r_)); RTF._V410_HMS13_INSUMOS = INS_F
C2 = copy.deepcopy(CONTR_F); C2["ids_calibradores"] = C2["ids_calibradores"] + ["SN_FALSA"]; RTF._V410_HMS13_CONTRACT = C2; r_ = RTF.h0dn_fontes_hms13_v410(copy.deepcopy(core)); R["id_a_mais_no_contrato"] = (r_["verdict"], _f(r_)); RTF._V410_HMS13_CONTRACT = CONTR_F
C4 = copy.deepcopy(CONTR_F); C4["campos"]["physical_covariance_closed"] = True; RTF._V410_HMS13_CONTRACT = C4; r_ = RTF.h0dn_fontes_hms13_v410(copy.deepcopy(core)); R["campo_obrigatorio_trocado"] = (r_["verdict"], _f(r_)); RTF._V410_HMS13_CONTRACT = CONTR_F
c9 = copy.deepcopy(core); c9["qg_closure"]["gate"]["verdict"] = "TGL_OUTRO"; r_ = RTF.h0dn_fontes_hms13_v410(c9); R["gate_trocado"] = (r_["verdict"], _f(r_))
c10 = copy.deepcopy(core); c10.pop("h0dn_bg1_v410", None); r_ = RTF.h0dn_fontes_hms13_v410(c10); R["h0dn_ausente"] = (r_["verdict"], _f(r_))
_vig0 = RTF._v410_h0dn_vigia_arquivos
def _vig_falso():
    t_, rest_ = _vig0(); t_.append(os.path.join(DL.H0DN_PASTA_VEDADA, "y_obs.npz")); return t_, rest_
RTF._v410_h0dn_vigia_arquivos = _vig_falso; r_ = RTF.h0dn_fontes_hms13_v410(copy.deepcopy(core)); R["caminho_sob_a_pasta_vedada"] = (r_["verdict"], _f(r_)); RTF._v410_h0dn_vigia_arquivos = _vig0
mapa = json.loads(base64.b64decode(INS_F["MAPA_FONTES_E_COVARIANCIA_13.json"]["b64"]).decode("utf-8")); mapa["objects"][0]["local"]["mu_mag"] = 31.5
b_ = json.dumps(mapa, ensure_ascii=False).encode("utf-8"); INS_num = copy.deepcopy(INS_F); INS_num["MAPA_FONTES_E_COVARIANCIA_13.json"] = {"b64": base64.b64encode(b_).decode("ascii"), "sha256": hashlib.sha256(b_).hexdigest(), "bytes": len(b_), "rel": "MAPA_FONTES_E_COVARIANCIA_13.json"}
Cn = copy.deepcopy(CONTR_F); Cn["insumos"]["MAPA_FONTES_E_COVARIANCIA_13.json"].update({"sha256": hashlib.sha256(b_).hexdigest(), "bytes": len(b_)}); Cn["pinos_build"]["MAPA_FONTES_E_COVARIANCIA_13.json"].update({"sha256": hashlib.sha256(b_).hexdigest(), "bytes": len(b_)})
RTF._V410_HMS13_CONTRACT = Cn; RTF._V410_HMS13_INSUMOS = INS_num; r_ = RTF.h0dn_fontes_hms13_v410(copy.deepcopy(core)); R["numero_proibido_plantado_no_mapa"] = (r_["verdict"], _f(r_)); RTF._V410_HMS13_CONTRACT = CONTR_F; RTF._V410_HMS13_INSUMOS = INS_F
for k, (vd, fl) in R.items():
    print("controle negativo (%s): %s | falhos %s" % (k, vd[:70], fl))
esp = {"insumo_adulterado": "RUNTIME_ERROR", "id_a_mais_no_contrato": ["c2"], "campo_obrigatorio_trocado": ["c4"], "gate_trocado": ["c9"], "h0dn_ausente": ["c10", "c12"], "caminho_sob_a_pasta_vedada": ["c7"], "numero_proibido_plantado_no_mapa": ["c1", "c6"]}
ok_neg = all(("RUNTIME_ERROR" in R[k][0]) if e == "RUNTIME_ERROR" else (R[k][1] == e and "MECHANICS_CHECK_FAILED" in R[k][0]) for k, e in esp.items())
_tudo = bool(out["all_verified"] and ok_neg and outH["all_verified"])
print("TUDO PASSOU" if _tudo else "FALHOU", "| controles negativos como esperado:", ok_neg)
J = {"tudo_passou": _tudo, "veredito": out["verdict"], "all_verified": out["all_verified"], "n_checks": (out.get("mechanics") or {}).get("n_checks"), "checks": [(c["id"], c["ok"]) for c in (out.get("mechanics") or {}).get("checks") or []], "controles_negativos": {k: {"verdict": vd, "falhos": fl, "esperado": esp[k]} for k, (vd, fl) in R.items()},
     "pinos_build": CONTR_F["pinos_build"], "guarda_numerica": CONTR_F["guarda_numerica_no_build"], "ratificacao_sha256": CONTR_F["ratificacao"]["sha256"], "nota": "teste OFFLINE do registro sobre o core da v409 selada (nao e' o rito nem o ensaio); " + DL.FRASE_HMS13_OBRIGATORIA_PT}
p = os.path.join(HERE, "TESTE_HMS13_OFFLINE_v410.json"); open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(J, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
