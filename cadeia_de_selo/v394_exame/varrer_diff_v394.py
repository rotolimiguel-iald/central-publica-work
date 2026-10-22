# -*- coding: utf-8 -*-
# Exame final v394: varre as linhas ACRESCENTADAS do diff v393 -> v394 (diff_v393_v394.txt, gerado por `diff` sobre os bytes)
# atras de (a) literais numericos de beta, alfa, sqrt(e) e da forma 1/alfa; (b) a palavra proibida da regua e os tokens vizinhos
# da guarda do rito (montados por codigo de caractere: a palavra nao e' escrita aqui); (c) atribuicoes ao gate. Escreve so' em v394_exame.
import re, json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
L = open(os.path.join(H, "diff_v393_v394.txt"), encoding="utf-8", errors="replace").read().split("\n")
hdr = re.compile(r"^(\d+)(?:,(\d+))?([acd])(\d+)(?:,(\d+))?$")
add = []   # (linha_no_candidato, texto)
cur = None
for l in L:
    m = hdr.match(l)
    if m:
        cur = int(m.group(4)); continue
    if l.startswith("> ") and cur is not None:
        add.append((cur, l[2:])); cur += 1
W = "".join(chr(c) for c in (67, 79, 78, 70, 73, 82, 77, 69, 68))          # o token proibido (maiusculo)
wpt = "".join(chr(c) for c in (99, 111, 110, 102, 105, 114, 109, 97, 100))  # forma em portugues (radical)
wen = W.lower()
pats = {
    "beta_literal": re.compile(r"(?<![\w.])0[.,]0120\d*|(?<![\w.])1[.,]20\d*\s*[eE]-?0?2|(?<![\w.])0[.,]012031"),
    "alfa_literal": re.compile(r"(?<![\w.])0[.,]0072973\d*|(?<![\w.])7[.,]297\d*\s*[eE]-?0?3|(?<![\w.])137[.,]03\d*"),
    "sqrt_e_literal": re.compile(r"(?<![\w.])1[.,]6487\d*"),
    "palavra_proibida_token": re.compile(r"(?<!NOT_)(?<!UN)" + W),
    "palavra_en_minuscula": re.compile(r"(?<!not )(?<!un)" + wen),
    "palavra_pt": re.compile(wpt, re.I),
    "PROVED_BY_sem_AP": re.compile(r"(?<!AP)PROVED_BY"),
    "TGL_PROVED": re.compile(r"TGL_PROVED|CONSCIOUSNESS_PROVED"),
    "gate_atribuicao": re.compile(r"""core\[\s*['"]qg_closure['"]\s*\]\s*=|qg_closure_verdict['"]?\s*\]\s*=|\[['"]gate['"]\]\s*=|formal_flags['"]?\]\s*\[.*\]\s*=|experiment_flags.*\]\s*="""),
}
# zonas do candidato: kernel embutido (Lean), bandeiras, bloco runtime v394 (falas dentro dele), artigo
def zona(n):
    if 127784 <= n <= 127972 or n == 8982 or n == 81669: return "kernel_embutido_lean"
    if 135402 <= n <= 139109 or 147804 <= n <= 151511 or 237208 <= n <= 237397: return "bandeiras/ledger"
    if 215893 <= n <= 226711: return "bloco_v394_runtime_e_falas"
    if 175555 <= n <= 175584 or 180097 <= n <= 180126 or n == 173506: return "artigo_v394"
    return "outro"
hits = {k: [] for k in pats}
for n, t in add:
    for k, p in pats.items():
        for m in p.finditer(t):
            s = max(0, m.start() - 90); e = min(len(t), m.end() + 90)
            hits[k].append({"linha": n, "zona": zona(n), "trecho": t[s:e]})
R = {"linhas_acrescentadas": len(add), "contagens": {k: len(v) for k, v in hits.items()},
     "por_zona": {k: {z: sum(1 for h in v if h["zona"] == z) for z in sorted(set(h["zona"] for h in v))} for k, v in hits.items()}, "hits": {k: v[:60] for k, v in hits.items()}}
json.dump(R, open(os.path.join(H, "VARREDURA_DIFF_v394.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: R[k] for k in ("linhas_acrescentadas", "contagens", "por_zona")}, ensure_ascii=False, indent=1))
for k in ("beta_literal", "alfa_literal", "sqrt_e_literal", "palavra_proibida_token", "PROVED_BY_sem_AP", "TGL_PROVED", "gate_atribuicao"):
    for h in hits[k][:12]:
        print(k, h["linha"], h["zona"], "|", h["trecho"].replace("\n", " ")[:220])
for k in ("palavra_en_minuscula", "palavra_pt"):
    for h in hits[k][:25]:
        print(k, h["linha"], h["zona"], "|", h["trecho"].replace("\n", " ")[:200])
