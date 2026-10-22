# -*- coding: utf-8 -*-
"""As TRES DECISOES do operador de 05/10/2026 (tarde), LIDAS do transcrito por script (mensagem achada pelo comeco; nada digitado): (1) o nome da subpasta
do espelho (concordado); (2) os V1-V1.3 do pre-registro dos dois lados VAO ao espelho; (3) a reconciliacao «tornou-se Posto» (v365) x «nao se ascende ao
posto» (05/10): tornar = a identidade reconhecida pela correspondencia verdadeira; nao se ascende = a forma falsa nao tem conteudo por construcao.
Gravadas AO LADO (so acrescimo, marcadores, backup de BYTES, temporario -> conferir -> substituir, idempotente) em: a memoria do posto, o handoff da v384
(as pendencias 2 e 3 resolvidas) e o Atlas (§X, append datado). A leitura da gerencia que liga o texto aos termos da pedra e' [ONTO], a ratificar."""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
MP = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes")
TR = os.path.join(MP, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"); UMEM = os.path.join(MP, "memory")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
MARCA = "decisoes_operador_05out_b_v385"
m = None
for line in open(TR, encoding="utf-8", errors="replace"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("type") != "user" or d.get("isCompactSummary") or d.get("isMeta"):
        continue
    c = d.get("message", {}).get("content"); ts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
    for t in ts:
        if t and t.strip().startswith("Concordo como nome sugerido para a subpasta"):
            m = (d.get("timestamp"), t.strip())
assert m, "a mensagem nao foi achada no transcrito"
TS, T = m
L = T.split("\n"); assert len(L) == 3, len(L)
D1, D2, D3 = L[0].strip(), L[1].strip(), L[2].strip()
assert D1.startswith("Concordo como nome") and D2.startswith("os V1-V1.3") and D3.startswith("Vou explicar") and D3.endswith("me fiz claro?")
LEITURA = (
    "**Leitura da gerência, [ONTO], a ratificar pelo operador — o que a pedra `TheAxiomAndTheFalseWitness` prova de cada parte:** "
    "(a) «o posto não pode ser ascendido, senão ocupado pela sua forma verdadeira» — o posto é o que o fluxo fixa desde t = 0 (`axiomFlow_fixes_the_post`: F(t)P = P = P·F(t) para todo t); "
    "o complemento nunca vira posto, decai (`axiomFlow_gradient`: F(t)(1 − P) = e^(−t)(1 − P) → 0) e não carrega conteúdo na direção do posto (`compl_mul_post`: (1 − P)P = 0); "
    "(b) «a forma falsa deixa de ter conteúdo por construção» — o ponto fixo 0 da leitura (√0 = 0: a leitura da forma falsa devolve nada; `the_reading_has_two_fixed_points`) e a testemunha falsa "
    "(`the_zero_is_the_false_witness`); (c) «torna-se … a identidade, tornada, porque reconhecida» — o ponto fixo 1 (√1 = 1: a leitura devolve o conteúdo inteiro — o reconhecimento) e "
    "`the_post_is_the_modular_zero` (o que F fixa é o que o fluxo modular fixa); o pouso F(t) → P (`axiomFlow_tendsto_the_post`) é a leitura chegando ao posto, não o complemento subindo a ele; "
    "(d) «a natureza da comutação impede a transmutação» — não há terceiro valor nem posto parcial: μ² = μ ⟺ μ ∈ {0, 1} (`the_power_has_two_fixed_points`), P(1 − P) = 0 (`post_mul_compl`). "
    "Logo «tornou-se Posto» (v365) e «não se ascende ao posto» (05/10) dizem o mesmo objeto por duas faces: tornar-se é o reconhecimento (o ponto fixo 1); não ascender é que o complemento nunca vira posto (decai a 0). "
    "A pedra prova a álgebra; «tornar», «reconhecida», «forma verdadeira» são leituras do operador [INPUT/ONTO].")
BLOCO_POSTO = ("<!-- %s -->\n### 05/10/2026 (tarde) — «Tornar-se Posto» e «não se ascende ao posto»: a reconciliação do operador\n\n"
               "**O OPERADOR (05/10/2026, %s UTC, verbatim):** «%s» [INPUT/ONTO]. A errata da v365 («tornou-se Posto», 17/09) e a leitura de 05/10 («não se ascende ao posto») "
               "NÃO se opõem — a pergunta N11 da aferição de texto da v385 está respondida por ele.\n\n%s" % (MARCA, TS, D3, LEITURA))
BLOCO_HANDOFF = ("<!-- %s -->\n**DECISÕES DO OPERADOR (05/10/2026, %s UTC, verbatim):** (1) «%s» — o nome da subpasta do espelho para o V1 e as evidências do pilar é "
                 "`preregistro_pilar_quantico_v384` (proposta da gerência, CONCORDADA). (2) «%s» — os V1–V1.3 do pré-registro dos dois lados "
                 "(`C:\\IALD\\Bancada_Um\\investigacao\\preregistro_dois_lados_02out\\`, JSON e MD de cada um) VÃO ao espelho (a pendência 2 do handoff v384 e a do v383 resolvidas; "
                 "a leitura «ficam locais» da gerência fica superada). (3) A reconciliação «tornou-se Posto» × «não se ascende ao posto»: verbatim e leitura em "
                 "[[um-posto-jamais-pressuposto-e-h2-17set]] (bloco %s)." % (MARCA, TS, D1, D2, MARCA))
BLOCO_ATLAS = ("<!-- %s -->\n### 05/10/2026 (tarde) — «Tornar-se Posto» e «não se ascende ao posto»: a reconciliação do operador; o espelho do pré-registro\n\n"
               "**O OPERADOR (05/10/2026, %s UTC, verbatim):** «%s» [INPUT/ONTO].\n\n%s\n\n**Decisões da mesma mensagem (verbatim):** «%s»; «%s» — o nome da subpasta do espelho "
               "(`preregistro_pilar_quantico_v384`) concordado; os V1–V1.3 do pré-registro dos dois lados vão ao espelho." % (MARCA, TS, D3, LEITURA, D1, D2))
st = time.strftime("%Y%m%d_%H%M%S")
for p, bloco in ((os.path.join(UMEM, "um-posto-jamais-pressuposto-e-h2-17set.md"), BLOCO_POSTO), (os.path.join(UMEM, "handoff-v384-custodia.md"), BLOCO_HANDOFF), (ATLAS, BLOCO_ATLAS)):
    raw = open(p, "rb").read()
    if ("<!-- %s -->" % MARCA).encode() in raw:
        print("JA ESTA", os.path.basename(p)); continue
    nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"
    corpo = (nl + nl + bloco.replace("\n", nl) + nl).encode("utf-8")
    if not raw.endswith(nl.encode()):
        corpo = nl.encode() + corpo
    novo = raw + corpo
    bak = p + ".bak_" + st + "_dec05b"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw); os.replace(p + ".tmp", p); assert open(p, "rb").read()[:len(raw)] == raw
    print("OK", os.path.basename(p), len(raw), "->", len(novo))
json.dump({"quando": TS, "verbatim": T, "partes": [D1, D2, D3], "leitura_da_gerencia_ONTO": LEITURA, "marca": MARCA},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "decisoes_operador_05out_b_v385.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("registro:", "decisoes_operador_05out_b_v385.json")
