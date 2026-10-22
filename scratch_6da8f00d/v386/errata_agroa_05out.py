# -*- coding: utf-8 -*-
"""ERRATA AO LADO (gerência, em nome próprio): nas leituras gravadas em 05/10 (registrar_respostas_05out.py) a frase do operador foi citada entre «» como
«o resto vc consegue responder tudo agora»; o verbatim (RESPOSTAS_operador_05out.txt, sha256 b49b0d9e…) é «o resto vc consegue responder tudo agroa».
Achado das aferições do pacote v386 (lentes texto e kernel/V1). Só acréscimo; backup de bytes; marcador idempotente; nas memórias do Verbo e do ramo B,
no Atlas e nos dois handoffs v385 (onde a frase entrou). Também a ordem do operador sobre a APRESENTAÇÃO do artigo (o teste na GPU; o sumário) fica
registrada, verbatim lida do transcrito, com o que foi medido."""
import hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SESS = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes")
TR = os.path.join(SESS, "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"); UMEM = os.path.join(SESS, "memory")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
ATLAS = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory", "TGL_ATLAS.md")
st = time.strftime("%Y%m%d_%H%M%S"); agora = time.strftime("%Y-%m-%d %H:%M:%S")
MARCA = "errata_agroa_e_ordem_gpu_05out"
T = open(os.path.join(HERE, "RESPOSTAS_operador_05out.txt"), encoding="utf-8", newline="").read()
assert T.endswith("o resto vc consegue responder tudo agroa")
# a ordem do operador sobre o artigo (verbatim do transcrito)
hit = None
for line in open(TR, encoding="utf-8", errors="replace"):
    try:
        d = json.loads(line)
    except ValueError:
        continue
    if d.get("isCompactSummary") or d.get("isMeta") or d.get("type") != "user":
        continue
    c = d.get("message", {}).get("content"); ts = [c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]
    for t in ts:
        if t and t.strip().startswith("verifique se a apresentação do artigo"):
            hit = (d.get("timestamp"), t.strip())
assert hit, "ordem do artigo nao achada"
TS_O, T_O = hit; UTC_O = re.match(r"\d{4}-\d{2}-\d{2}T(\d{2}:\d{2}:\d{2})", TS_O).group(1) + " UTC"
# o medido no artigo selado v385 (por script, agora)
pt = open(os.path.join(NOS, "um_absoluto_pt.txt"), encoding="utf-8", errors="replace").read().splitlines()
cab = "\n".join(pt[:23]); n_gpu_cab = len(re.findall(r"GPU", cab)); n_tr = sum(1 for l in pt if re.search(r"tempo real", l))
toc = open(os.path.join(NOS, "um_absoluto_pt.toc"), encoding="utf-8", errors="replace").read(); n_toc = toc.count("GPU"); n_toc_l = toc.count("\\contentsline")
first_gpu = next((i + 1 for i, l in enumerate(pt) if "GPU" in l), None)
BL = ("<!-- %s -->\n**ERRATA AO LADO (05/10/2026, %s; gerência, em nome próprio; achado das aferições do pacote v386):** onde as leituras de 05/10 acima citam entre «» "
      "«o resto vc consegue responder tudo agora», leia-se o verbatim «o resto vc consegue responder tudo agroa» [sic] (RESPOSTAS_operador_05out.txt, sha256 `%s`). "
      "A delegação vale como está; só a grafia dentro das «» estava normalizada.\n\n**E a ORDEM do operador sobre o artigo (%s, verbatim):** «%s» — MEDIDO no artigo selado v385 "
      "(`um_absoluto_pt.txt`): nas 23 linhas do cabeçalho (apresentação, resumo, palavras-chave) «GPU» tem %d ocorrência(s); «tempo real» tem %d no artigo inteiro; a primeira "
      "menção à GPU está na linha %d (corpo); o sumário (`um_absoluto_pt.toc`, %d entradas) tem %d «GPU» — as seções do pilar são `section*` (sem numeração). "
      "Correção na v386: patch W10 (apresentação, «O método», palavras-chave e `\\addcontentsline` no sumário, PT e EN; números lidos do core em runtime)."
      % (MARCA, agora, hashlib.sha256(T.encode("utf-8")).hexdigest(), UTC_O, T_O, n_gpu_cab, n_tr, first_gpu, n_toc_l, n_toc))


def nl_de(raw):
    return "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else "\n"


for p in (os.path.join(UMEM, "verbo-selecao-da-acao-05out.md"), os.path.join(UMEM, "ramo-b-reaberto-05out.md"), ATLAS,
          os.path.join(UMEM, "handoff-v385-custodia.md"), os.path.join(NOS, "HANDOFF_v385_CUSTODIA.md")):
    raw0 = open(p, "rb").read()
    if MARCA.encode() in raw0:
        print("JA ESTA", os.path.basename(p)); continue
    nl = nl_de(raw0); corpo = (nl + nl + BL.replace("\n", nl) + nl).encode("utf-8")
    if not raw0.endswith(nl.encode()):
        corpo = nl.encode() + corpo
    novo = raw0 + corpo
    bak = p + ".bak_" + st + "_agroa"; open(bak, "wb").write(raw0); assert open(bak, "rb").read() == raw0
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw0); os.replace(p + ".tmp", p)
    assert open(p, "rb").read()[:len(raw0)] == raw0
    print("OK", os.path.basename(p), len(raw0), "->", len(novo))
print("medido: GPU no cabecalho", n_gpu_cab, "| tempo real", n_tr, "| 1a GPU linha", first_gpu, "| toc entradas", n_toc_l, "GPU", n_toc)
print("FIM", agora)
