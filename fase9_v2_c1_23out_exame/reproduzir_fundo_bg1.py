# -*- coding: utf-8 -*-
"""reproduzir_fundo_bg1.py -- auditoria c1 (23/10/2026), item 3: roda o fornecedor REAL do fundo BG1 (Bancada: Planck comprimido + DESI DR2; nenhum
centro local de H0) a partir do modulo pinado do pacote, confere E2 e os pinos da Bancada, e testa que a divergencia INTERROMPE (BackgroundError).
Escreve so' nesta pasta. python -P -E -B -X utf8 reproduzir_fundo_bg1.py"""
import sys, os, json, hashlib, copy, time
sys.dont_write_bytecode = True
PK = r"C:\IALD\Central de Patentes\work\fase9_v2_c1_23out"
sys.path.insert(0, os.path.join(PK, "runner"))
import f9v2_background as BG
spec = json.load(open(os.path.join(PK, "spec", "PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json"), encoding="utf-8"))["spec"]
q = json.load(open(os.path.join(PK, "testes", "QUALIFICACAO_FORNECEDOR_REAL.json"), encoding="utf-8"))
ped = json.load(open(os.path.join(PK, "PEDIDO_DE_CONGELAMENTO.json"), encoding="utf-8"))
t0 = time.time(); P = BG.BancadaBackgroundProvider(); bg = P.compute(); dt = time.time() - t0
pin = spec["fundos"]["BG1"]; tol = spec["runner_contract"]["tolerancias"]
R = {"kind": bg["kind"], "segundos": round(dt, 1), "H0": bg["bg1"]["H0"], "sigma": bg["bg1"]["sigma_H0"], "pino_spec": [pin["H0"], pin["sigma"]], "tol": [tol["BG1_H0_abs"], tol["BG1_sigma_abs"]],
     "igual_a_qualificacao": {"H0": abs(bg["bg1"]["H0"] - q["fundo"]["bg1"]["H0"]), "sigma": abs(bg["bg1"]["sigma_H0"] - q["fundo"]["bg1"]["sigma_H0"]),
                              "fundo_livre_H0": abs(bg["fundo_livre"]["H0"] - q["fundo"]["fundo_livre"]["H0"]), "lnZ": abs(bg["fundo_livre"]["lnZ_bg_ratio_laplace"] - q["fundo"]["fundo_livre"]["lnZ_bg_ratio_laplace"])}}
R["E2"] = BG.check_reproduction(bg, pin["H0"], pin["sigma"], tol["BG1_H0_abs"], tol["BG1_sigma_abs"])
neg = {}
for nome, mut in (("H0_mais_0.011", lambda b: b["bg1"].__setitem__("H0", b["bg1"]["H0"] + 0.011)), ("sigma_mais_0.006", lambda b: b["bg1"].__setitem__("sigma_H0", b["bg1"]["sigma_H0"] + 0.006)),
                  ("H0_nan", lambda b: b["bg1"].__setitem__("H0", float("nan")))):
    b2 = copy.deepcopy(bg); mut(b2)
    try:
        BG.check_reproduction(b2, pin["H0"], pin["sigma"], tol["BG1_H0_abs"], tol["BG1_sigma_abs"]); neg[nome] = "NAO INTERROMPEU"
    except BG.BackgroundError as e:
        neg[nome] = "INTERROMPE: " + str(e)[:90]
R["divergencia"] = neg
cur = BG.bancada_pins(); pp = ped["o_recibo_pinara"]["bancada"]
R["bancada_pinos_iguais_ao_pedido"] = {k: cur[k]["sha256"] == v["sha256"] for k, v in pp.items()}
R["bancada_pinos_iguais_a_qualificacao"] = cur == q["bancada_pins"]
print(json.dumps(R, ensure_ascii=False, indent=1))
json.dump(R, open("REPRODUCAO_FUNDO_BG1.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
