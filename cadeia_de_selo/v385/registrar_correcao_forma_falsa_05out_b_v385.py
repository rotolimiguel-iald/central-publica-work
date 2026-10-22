# -*- coding: utf-8 -*-
"""A CORRECAO DO OPERADOR (05/10/2026, 14:35 UTC, verbatim, lida do transcrito por script): «não é que "a forma falsa deixa de ter conteúdo" é que ela passa a
ter qualquer conteúdo (superposição em relação ao posto) menos o conteúdo verdadeiro, o do posto». A leitura (b) da gerencia (a forma falsa = o ponto fixo 0,
«a leitura devolve nada») fica RETRATADA: a forma falsa e' o COMPLEMENTO do posto, 1 - P -- qualquer conteudo menos o verdadeiro --, e o ponto fixo 0 da
leitura e' outro objeto (a testemunha falsa, estatica). Gravado AO LADO (marcador; so acrescimo; backup de BYTES; temporario -> conferir -> substituir;
idempotente) na memoria do posto, no Atlas e no handoff da v384; o registro JSON do scratchpad ganha a correcao ao lado."""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MP = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes"); UMEM = os.path.join(MP, "memory")
TR = os.path.join(MP, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
MARCA = "correcao_forma_falsa_05out_b_v385"
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
        if t and t.strip().startswith("tem uma coisa errada no que vc prop"):
            assert m is None, "mais de uma mensagem"
            m = (d.get("timestamp"), t.strip())
assert m, "a correcao nao foi achada no transcrito"
TS, T = m
assert "qualquer conteúdo (superposição em relação ao posto) menos o conteúdo verdadeiro, o do posto" in T
LEITURA2 = (
    "**Leitura da gerência REFEITA, [ONTO], a ratificar — o que a pedra dá à correção:** a forma falsa é o COMPLEMENTO do posto, 1 − P: ela carrega qualquer conteúdo "
    "menos o do posto. (i) Não tem o conteúdo verdadeiro: (1 − P)P = 0 (`compl_mul_post`) e P(1 − P) = 0 (`post_mul_compl`). (ii) Mas é uma forma, e não nada: "
    "(1 − P)(1 − P) = 1 − P (`compl_mul_compl`: o complemento é idempotente). (iii) «Superposição em relação ao posto»: todo estado se decompõe em parte no posto "
    "e parte no complemento, 1 = P + (1 − P) — identidade algébrica trivial (sem termo próprio; não precisa de um), que o fluxo lê separando as duas partes: "
    "F(t) = P + e^(−t)(1 − P) (`axiomFlow`), F(t)P = P (`axiomFlow_fixes_the_post`), F(t)(1 − P) = e^(−t)(1 − P) (`axiomFlow_gradient`). "
    "(iv) O ponto fixo 0 da leitura radical (√0 = 0) é OUTRO objeto — a testemunha FALSA, estática, o zero absoluto (`the_zero_is_the_false_witness`) —, "
    "não a forma falsa; a frase retratada da leitura (b), «a leitura da forma falsa devolve nada», ligava os dois indevidamente. "
    "O que fica da frase do operador de 14:21 («a forma falsa, deixa de ter conteúdo por construção») lê-se, por ele, como «deixa de ter o conteúdo VERDADEIRO» "
    "— e isso é exatamente (1 − P)P = 0. PROVADA ≠ CONFIRMADA; a pedra prova a álgebra; «forma falsa», «posto», «superposição em relação ao posto» são leituras do operador [INPUT/ONTO].")
BLOCO = ("<!-- %s -->\n### 05/10/2026 (tarde) — A correção do operador: a forma falsa não «deixa de ter conteúdo»; ela tem qualquer conteúdo menos o do posto\n\n"
         "**O OPERADOR (05/10/2026, %s UTC, verbatim):** «%s» [INPUT/ONTO]. **Retratação da gerência, em nome próprio:** a leitura (b) do bloco "
         "`decisoes_operador_05out_b_v385` (a forma falsa = o ponto fixo 0; «a leitura devolve nada») estava ERRADA e fica retratada; vale a correção do operador.\n\n%s" % (MARCA, TS, T, LEITURA2))
BLOCO_HANDOFF = ("<!-- %s -->\n**CORREÇÃO DO OPERADOR (05/10/2026, %s UTC, verbatim):** «%s» [INPUT/ONTO] — a leitura (b) da gerência fica retratada; a leitura refeita "
                 "(a forma falsa = o complemento 1 − P) está em [[um-posto-jamais-pressuposto-e-h2-17set]] (bloco `%s`), [ONTO], a ratificar." % (MARCA, TS, T, MARCA))
st = time.strftime("%Y%m%d_%H%M%S")
for p, bloco in ((os.path.join(UMEM, "um-posto-jamais-pressuposto-e-h2-17set.md"), BLOCO), (ATLAS, BLOCO), (os.path.join(UMEM, "handoff-v384-custodia.md"), BLOCO_HANDOFF)):
    raw = open(p, "rb").read()
    if ("<!-- %s -->" % MARCA).encode() in raw:
        print("JA ESTA", os.path.basename(p)); continue
    nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"
    corpo = (nl + nl + bloco.replace("\n", nl) + nl).encode("utf-8")
    if not raw.endswith(nl.encode()):
        corpo = nl.encode() + corpo
    novo = raw + corpo
    bak = p + ".bak_" + st + "_corrff"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw); os.replace(p + ".tmp", p); assert open(p, "rb").read()[:len(raw)] == raw
    print("OK", os.path.basename(p), len(raw), "->", len(novo))
J = os.path.join(HERE, "decisoes_operador_05out_b_v385.json")
R = json.load(open(J, encoding="utf-8"))
R["correcao_do_operador_14h35"] = {"quando": TS, "verbatim": T, "leitura_refeita_ONTO": LEITURA2, "marca": MARCA, "retratada": "a leitura (b) original (a forma falsa = o ponto fixo 0)"}
open(J + ".bak_" + st, "wb").write(open(J, "rb").read())
json.dump(R, open(J + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(J + ".tmp", J)
print("registro:", os.path.basename(J))
