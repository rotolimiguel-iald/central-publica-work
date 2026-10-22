# -*- coding: utf-8 -*-
"""Dois registros AO LADO (so acrescimo; marcadores; backup de BYTES; idempotentes) na memoria do posto, no Atlas e no handoff da v384:
 (A) O OPERADOR, 05/10/2026 14:40 UTC, verbatim (lido do transcrito por script): «a "forma falsa" é a projeção da testemunha falsa, sendo ela mesma a
     superposição, um estado jamais ocupado por um posto de verdade absoluta» -- com a leitura REFINADA da gerencia [ONTO], a ratificar;
 (B) ERRATA da errata (achado A1 do verificador da errata): «o proprio PFmic C e' idempotente intermediario» foi dito SEM termo na pedra -- e' derivavel de
     FockCertificate.Ω_norm e F_infinite (o verificador o compilou no sandbox, fora da pedra); o contraexemplo compilado pela lente anterior foi em ℂ × ℂ."""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MP = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes"); UMEM = os.path.join(MP, "memory")
TR = os.path.join(MP, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
MARCA_A = "forma_falsa_projecao_05out_b_v385"; MARCA_B = "errata_pfmic_05out_b_v385"
m = None
for line in open(TR, encoding="utf-8", errors="replace"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("isCompactSummary") or d.get("isMeta"):
        continue
    if d.get("type") == "user":
        c = d.get("message", {}).get("content"); ts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
    elif d.get("type") == "attachment" and (d.get("attachment") or {}).get("type") == "queued_command":
        pr = d["attachment"].get("prompt"); ts = [pr] if isinstance(pr, str) else [x.get("text", "") for x in (pr or []) if isinstance(x, dict) and x.get("type") == "text"]
    else:
        continue
    for t in ts:
        if t and t.strip().startswith('a "forma falsa" é a projeção'):
            assert m is None, "mais de uma mensagem"
            m = (d.get("timestamp"), t.strip())
assert m, "a frase nao foi achada no transcrito"
TS, T = m
assert T.endswith("posto de verdade absoluta")
LEITURA = (
    "**Leitura REFINADA da gerência, [ONTO], a ratificar:** (i) «a projeção da testemunha falsa» — a forma falsa é a PROJEÇÃO 1 − P (idempotente: `compl_mul_compl`, "
    "(1 − P)(1 − P) = 1 − P; e de posto complementar ao do Nome, 1 = P + (1 − P)); a testemunha falsa é o que se projeta nela — a estática, o zero absoluto "
    "(`the_zero_is_the_false_witness`). (ii) «sendo ela mesma a superposição» — o que está em 1 − P é qualquer conteúdo menos o do posto: todo estado se escreve "
    "Pψ + (1 − P)ψ, e a parte (1 − P)ψ é a superposição em relação ao posto. (iii) «um estado jamais ocupado por um posto de verdade absoluta» — nenhum posto "
    "verdadeiro ocupa a forma falsa: (1 − P)P = 0 (`compl_mul_post`) e P(1 − P) = 0 (`post_mul_compl`); e o fluxo não a leva ao posto — F(t)(1 − P) = e^(−t)(1 − P) "
    "(`axiomFlow_gradient`), com e^(−t) → 0 por `Real.tendsto_exp_neg_atTop_nhds_zero` (Mathlib, [KNOWN]) — o que decai é a forma falsa, não o posto. "
    "A pedra prova a álgebra; «projeção da testemunha falsa», «superposição», «posto de verdade absoluta» são leituras do operador [INPUT/ONTO]. PROVADA ≠ CONFIRMADA.")
BLOCO_A = ("<!-- %s -->\n### 05/10/2026 (tarde) — A forma falsa é a projeção da testemunha falsa, ela mesma a superposição\n\n"
           "**O OPERADOR (05/10/2026, %s UTC, verbatim):** «%s» [INPUT/ONTO].\n\n%s" % (MARCA_A, TS, T, LEITURA))
BLOCO_A_H = ("<!-- %s -->\n**O OPERADOR (05/10/2026, %s UTC, verbatim):** «%s» [INPUT/ONTO] — a leitura refinada da gerência ([ONTO], a ratificar) está em "
             "[[um-posto-jamais-pressuposto-e-h2-17set]] (bloco `%s`)." % (MARCA_A, TS, T, MARCA_A))
BLOCO_B = ("<!-- %s -->\n**ERRATA DA ERRATA (05/10/2026, tarde; gerência, em nome próprio; achado A1 do verificador da errata `errata_leitura_05out_b_v385`):** no item (4) "
           "a errata disse «idempotentes intermediários existem (o próprio `PFmic C`; …)» SEM termo na pedra que o prove. O que está provado: o contraexemplo compilado pela "
           "lente anterior foi em ℂ × ℂ (P = (1, 0)), fora da pedra; que o próprio `PFmic C` é ≠ 0 e ≠ 1 é DERIVÁVEL de `FockCertificate.Ω_norm` (‖Ω‖ = 1) e `F_infinite` "
           "(¬FiniteDimensional ℂ F) — o verificador o compilou no sandbox (`AFER_PFmic_is_intermediate_idempotent`, trio de axiomas), FORA da pedra. Leia-se, pois: "
           "«idempotentes intermediários existem (contraexemplo compilado em ℂ × ℂ; que o próprio `PFmic C` o é, é derivável de `Ω_norm` + `F_infinite`, compilado no sandbox, "
           "sem termo na pedra)». O resto do item (4) fica." % MARCA_B)
st = time.strftime("%Y%m%d_%H%M%S")
for p, blocos in ((os.path.join(UMEM, "um-posto-jamais-pressuposto-e-h2-17set.md"), (BLOCO_A, BLOCO_B)), (ATLAS, (BLOCO_A, BLOCO_B)),
                  (os.path.join(UMEM, "handoff-v384-custodia.md"), (BLOCO_A_H,))):
    raw0 = open(p, "rb").read(); raw = raw0; novo = raw0
    nl = "\r\n" if raw0.count(b"\r\n") > raw0.count(b"\n") // 2 else "\n"
    for bloco in blocos:
        marca = bloco.split("-->")[0] + "-->"
        if marca.encode() in novo:
            print("JA ESTA", os.path.basename(p), marca); continue
        corpo = (nl + nl + bloco.replace("\n", nl) + nl).encode("utf-8")
        if not novo.endswith(nl.encode()):
            corpo = nl.encode() + corpo
        novo = novo + corpo
    if novo == raw0:
        continue
    bak = p + ".bak_" + st + "_ffproj"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw0); os.replace(p + ".tmp", p); assert open(p, "rb").read()[:len(raw0)] == raw0
    print("OK", os.path.basename(p), len(raw0), "->", len(novo))
J = os.path.join(HERE, "decisoes_operador_05out_b_v385.json")
R = json.load(open(J, encoding="utf-8"))
R["forma_falsa_projecao_14h40"] = {"quando": TS, "verbatim": T, "leitura_refinada_ONTO": LEITURA, "marca": MARCA_A}
R["errata_da_errata_pfmic"] = {"texto": BLOCO_B, "marca": MARCA_B}
open(J + ".bak_" + st, "wb").write(open(J, "rb").read())
json.dump(R, open(J + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(J + ".tmp", J)
print("registro:", os.path.basename(J))
