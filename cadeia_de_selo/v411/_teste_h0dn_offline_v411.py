# -*- coding: utf-8 -*-
"""_teste_h0dn_offline_v411.py -- ENSAIO OFFLINE do registro h0dn_bg1_v411 (DESENHO_v411 secao 2) ANTES do gerador: monta o contrato, o texto e os insumos (registros_h0dn_v411), carrega do um.py da v410 selada (base_v410, por
trecho, base_um_v410.py) as funcoes que o registro usa no rito (a funcao congelada veredito_h0dn, o contrato e os insumos da v410, as guardas P18 e de frases, o vigia de arquivos, _v398_beta), executa o bloco autoral
runtime_h0dn_v411.py no MESMO namespace e roda h0dn_bg1_v411 sobre uma COPIA do core da v410 selada. Imprime as 16 checagens e o veredito. CONTROLES NEGATIVOS (a recusa e' resultado; cada um TEM de recusar):
insumo adulterado; gate trocado; escada trocada; resultado embutido adulterado (com o pino refeito, para chegar a c6); texto com frase proibida; beta errado; caminho tocado na pasta do Kimi; K da v410 trocado; Z nao finito.
Grava TESTE_H0DN_OFFLINE_v411.json. uso: python -B -X utf8 _teste_h0dn_offline_v411.py   (sem -I: numpy e scipy estao no site do usuario)"""
import base64, copy, hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
import registros_h0dn_v411 as RH  # noqa: E402
import base_um_v410 as B  # noqa: E402
t0 = time.time()
core0 = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto.json"), encoding="utf-8"))["core"]
selo0 = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto_selo.json"), encoding="utf-8"))
ns = B.carregar(["_v392_guarda_texto", "_v410_guarda_frases", "veredito_h0dn", "_v410_h0dn_cabeca", "_v410_h0dn_vigia_arquivos", "_V410_H0DN_CONTRACT", "_V410_H0DN_INSUMOS", "_v398_beta",
                  "SEALED_CODATA_ALPHA", "_v376_same_alpha_literal"])
import math as _math  # noqa: E402
ns["_m398"] = _math   # (no um.py: `import math as _m398`, de topo)
ns["__file__"] = B.UM   # (_v376_same_alpha_literal le o literal do proprio um.py: aqui, o da v410 selada)
B.chamar_resolvendo(ns, "_v410_guarda_frases", "aquecimento")
assert B.chamar_resolvendo(ns, "_v398_beta", copy.deepcopy(core0))[3] is True, "beta em runtime nao confere com o core da base"
exec(compile(open(os.path.join(HERE, "runtime_h0dn_v411.py"), encoding="utf-8").read(), os.path.join(HERE, "runtime_h0dn_v411.py"), "exec"), ns)
base_sha = hashlib.sha256(open(B.UM, "rb").read()).hexdigest()
CONTR = RH.contrato_h0dn_v411(core0, selo0, ns["_V410_H0DN_CONTRACT"], base_sha); TXT = RH.texto_h0dn_v411()
INS = RH.insumos_embutidos(ns["_V410_H0DN_CONTRACT"]["insumos"])
ns["_V411_H0DN_CONTRACT"] = CONTR; ns["_V411_H0DN_TEXT"] = TXT; ns["_V411_H0DN_INSUMOS"] = INS
print("contrato: n_checks", CONTR["n_checks"], "| insumos", len(CONTR["insumos"]), "(reuso %d)" % sum(1 for v in INS.values() if "reuso_v410" in v), "| b64 total", sum(len(v.get("b64", "")) for v in INS.values()), "B")


def rodar(core_, contr_=None, txt_=None, ins_=None):
    ns["_V411_H0DN_CONTRACT"] = contr_ or CONTR; ns["_V411_H0DN_TEXT"] = txt_ or TXT; ns["_V411_H0DN_INSUMOS"] = ins_ or INS
    try:
        return ns["h0dn_bg1_v411"](core_)
    finally:
        ns["_V411_H0DN_CONTRACT"] = CONTR; ns["_V411_H0DN_TEXT"] = TXT; ns["_V411_H0DN_INSUMOS"] = INS


out = rodar(copy.deepcopy(core0))
_pr = os.path.join(HERE, "TESTE_H0DN_OFFLINE_v411_registro.json")   # (a saida do registro, para o ensaio do quadro e da secao: _teste_quadro_v411.py)
open(_pr + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1, default=str)); os.replace(_pr + ".tmp", _pr)
print("veredito:", out["verdict"]); print("all_verified:", out["all_verified"], "| runtime_executed:", out["runtime_executed"], "| erro:", out.get("error"))
falhas = [c for c in (out.get("mechanics") or {}).get("checks") or [] if not c["ok"]]
for c in (out.get("mechanics") or {}).get("checks") or []:
    print("  %-4s %s  %s" % (c["id"], "OK  " if c["ok"] else "FAIL", c["descricao"][:140]))
v = out.get("values") or {}
print("primario:", {k: v.get("primario", {}).get(k) for k in ("z_null", "z_tgl", "D", "p_unilateral", "ramo", "outcome")})
print("cefeidas livres:", {k: v.get("cefeidas_livres", {}).get(k) for k in ("z_null", "z_tgl", "D", "ramo", "outcome")})
print("lei km/s/Mpc:", v.get("lei_em_km_s_Mpc")); print("c6 max dif:", v.get("c6_max_dif"), "| c9 max dif:", v.get("c9_max_dif")); print("atos:", v.get("atos"))
print("emenda (a):", (v.get("a_emenda_as_claras") or {}).get("a"), "| (b) folhas que mudam:", ((v.get("a_emenda_as_claras") or {}).get("b") or {}).get("folhas_que_mudam"), "| (c) ramos:", ((v.get("a_emenda_as_claras") or {}).get("c") or {}).get("ramos"))
print("finitude:", v.get("guarda_de_finitude")); print("n ressalvas:", v.get("n_ressalvas"), "| frases:", v.get("frases_violacoes"), "| p18:", v.get("p18_violacoes"), "| caminhos tocados:", v.get("n_caminhos_tocados"))
for r in v.get("esperado_pelos_agregados") or []:
    print("  agregados:", r)

# ---------------- CONTROLES NEGATIVOS
neg = {}
ins_b = copy.deepcopy(INS); b_ = base64.b64decode(ins_b["vetor_y255.npz"]["b64"]); ins_b["vetor_y255.npz"]["b64"] = base64.b64encode(b_[:-1] + bytes([b_[-1] ^ 1])).decode("ascii")
o = rodar(copy.deepcopy(core0), ins_=ins_b); neg["insumo_adulterado"] = {"verdict": o["verdict"], "recusou": not o["all_verified"] and "REFUSED" in o["verdict"]}
cg = copy.deepcopy(core0); cg["qg_closure"]["gate"]["verdict"] = "TGL_OUTRO_GATE"; o = rodar(cg)
neg["gate_trocado"] = {"verdict": o["verdict"], "recusou": not o["all_verified"], "falhas": [c["id"] for c in o["mechanics"]["checks"] if not c["ok"]]}
c387 = copy.deepcopy(core0); c387["three_stress_tests_v387"]["verdict"] = c387["three_stress_tests_v387"]["verdict"].replace("P2_NOT_DETERMINED", "P2_OUTRA_COISA"); o = rodar(c387)
neg["v387_sem_o_token_selado"] = {"recusou": not o["all_verified"] and o.get("p2_ao_lado_da_v387") is None, "falhas": [c["id"] for c in o["mechanics"]["checks"] if not c["ok"]]}
ce = copy.deepcopy(core0); ce["external_ladder"]["n_theorems_expected"] = int(ce["external_ladder"]["n_theorems_expected"]) + 1; o = rodar(ce)
neg["escada_trocada"] = {"recusou": not o["all_verified"], "falhas": [c["id"] for c in o["mechanics"]["checks"] if not c["ok"]]}
res_b = json.loads(base64.b64decode(INS["RESULTADO_DA_ABERTURA_V411.json"]["b64"]).decode("utf-8")); res_b["resultado"]["estatistica"]["z_null"][0] += 1e-6
rb_ = (json.dumps(res_b, ensure_ascii=False, indent=1) + "\n").encode("utf-8"); ins_r = copy.deepcopy(INS); ins_r["RESULTADO_DA_ABERTURA_V411.json"] = {"b64": base64.b64encode(rb_).decode("ascii")}
contr_r = copy.deepcopy(CONTR); contr_r["insumos"]["RESULTADO_DA_ABERTURA_V411.json"].update(sha256=hashlib.sha256(rb_).hexdigest(), bytes=len(rb_))
o = rodar(copy.deepcopy(core0), contr_=contr_r, ins_=ins_r); neg["resultado_adulterado_1e-6_no_z"] = {"recusou": not o["all_verified"], "falhas": [c["id"] for c in o["mechanics"]["checks"] if not c["ok"]]}
txt_b = copy.deepcopy(TXT); txt_b["diz"] = list(txt_b["diz"]) + ["o teste tem poder certificado e e' um teste cego"]; o = rodar(copy.deepcopy(core0), txt_=txt_b)
neg["texto_com_frase_proibida"] = {"recusou": not o["all_verified"], "falhas": [c["id"] for c in o["mechanics"]["checks"] if not c["ok"]]}
toc = ["C:\\IALD\\Central de Patentes\\work\\h0dn_bg1_v410_09nov\\kimi\\qualquer.json"]
m = ns["v411_h0dn_mechanics"](ns["_v398_beta"](core0)[0], copy.deepcopy(core0), CONTR, TXT, INS, None, toc); neg["caminho_na_pasta_do_kimi"] = {"recusou": not m["passed"], "falhas": [c["id"] for c in m["checks"] if not c["ok"]]}
m = ns["v411_h0dn_mechanics"](ns["_v398_beta"](core0)[0] * 1.01, copy.deepcopy(core0), CONTR, TXT, INS, None, []); neg["beta_errado"] = {"recusou": not m["passed"], "falhas": [c["id"] for c in m["checks"] if not c["ok"]]}
ck = copy.deepcopy(core0); ck["h0dn_bg1_v410"]["values"]["K"] = ck["h0dn_bg1_v410"]["values"]["K"] * (1 + 1e-9); o = rodar(ck)
neg["K_da_v410_trocado"] = {"recusou": not o["all_verified"], "falhas": [c["id"] for c in o["mechanics"]["checks"] if not c["ok"]]}
fin = {}
for nome_, a_, b2_ in (("nan", float("nan"), 0.0), ("inf", 1.0, float("inf")), ("menos_inf", float("-inf"), 0.0)):
    try:
        ns["_v411_h0dn_guarda_finitude"](a_, b2_); fin[nome_] = False
    except ValueError:
        fin[nome_] = True
neg["z_nao_finito_no_involucro"] = {"recusou": all(fin.values()), "casos": fin}
gf = {"poder certificado": "o teste tem poder certificado", "teste cego": "foi um teste cego", "erro de montagem": "o vetor fora do suporte e' erro de montagem", "evidencia independente": "e' evidencia independente das fases",
      "descoberta": "a descoberta do H0DN", "descoberta do rito": "o rito fez a descoberta do numero", "beta literal": "beta = 0,0120313", "a palavra": "a TGL foi confirmada", "F67 sem obrigacoes": "o primario do H0DN fica a 6,11 contra o nulo"}
gfr = {k_: bool(ns["_v411_guarda_frases"](t_)) for k_, t_ in gf.items()}
ok_frases = {"teste nao cego": "o teste nao e' cego", "com as quatro": "o primario do H0DN, sob o modelo de erros publicado, fica a 6,11 contra o nulo; ao lado, as Cefeidas livres leem 4,38; retrodição sem ajuste, teste não cego; validade, não creditação",
             "negada": "nao e' evidencia independente", "nao descobre": "o rito confere a conta, nao descobre um numero novo", "o criterio": "o que passa do degrau de 5σ, o critério de descoberta da física acadêmica",
             "the threshold": "the 5σ discovery threshold, the discovery criterion of academic physics"}
gfl = {k_: ns["_v411_guarda_frases"](t_) for k_, t_ in ok_frases.items()}
neg["guarda_de_frases_controle"] = {"proibidas_recusadas": gfr, "certas_passam": {k_: not v_ for k_, v_ in gfl.items()}, "violacoes_nas_certas": {k_: v_ for k_, v_ in gfl.items() if v_}}
P2 = out.get("p2_ao_lado_da_v387") or {}
print("p2 ao lado da v387:", P2)
p2_ok = bool(P2 and P2.get("rotulo") and "P2_NOT_DETERMINED" in (P2.get("rotulo_selado_da_v387") or "") and "P2_NOT_DETERMINED" not in P2["rotulo"] and P2.get("canal") and P2.get("nota")
             and neg["v387_sem_o_token_selado"]["falhas"] == ["c14"] and ((v.get("c14_inclui_o_p2_da_v387") or {}).get("ok") is True))
tudo = (p2_ok and out["all_verified"] and not falhas and all(x.get("recusou") for k, x in neg.items() if k != "guarda_de_frases_controle") and all(gfr.values()) and all(not v_ for v_ in gfl.values()))
rep = {"contrato": "TESTE_H0DN_OFFLINE_v411", "quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "duracao_s": round(time.time() - t0, 1), "veredito": out["verdict"], "all_verified": out["all_verified"],
       "checks": [(c["id"], c["ok"]) for c in (out.get("mechanics") or {}).get("checks") or []], "n_ok": sum(1 for c in (out.get("mechanics") or {}).get("checks") or [] if c["ok"]),
       "primario": v.get("primario"), "cefeidas_livres": v.get("cefeidas_livres"), "lei_em_km_s_Mpc": v.get("lei_em_km_s_Mpc"), "c6_max_dif": v.get("c6_max_dif"), "c9_max_dif": v.get("c9_max_dif"),
       "atos": v.get("atos"), "emenda": v.get("a_emenda_as_claras"), "finitude": v.get("guarda_de_finitude"), "agregados": v.get("esperado_pelos_agregados"), "ressalvas": v.get("ressalvas_secao8"),
       "frases": v.get("frases_violacoes"), "p18": v.get("p18_violacoes"), "caminhos_tocados": v.get("caminhos_tocados"), "controles_negativos": neg, "erro": out.get("error"), "p2_ao_lado_da_v387": P2, "p2_ok": p2_ok, "TUDO_PASSOU": bool(tudo)}
p = os.path.join(HERE, "TESTE_H0DN_OFFLINE_v411.json")
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(rep, ensure_ascii=False, indent=1, default=str)); os.replace(p + ".tmp", p)
print(json.dumps(neg, ensure_ascii=False, indent=1)[:4000])
print("TUDO PASSOU" if tudo else "FALHOU", "| %.1f s" % (time.time() - t0))
sys.exit(0 if tudo else 1)
