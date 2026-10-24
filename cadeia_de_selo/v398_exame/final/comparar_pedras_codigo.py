# -*- coding: utf-8 -*-
"""comparar_pedras_codigo.py -- exame final v398 (c1, 23/10/2026): as pedras que vao no kernel (Sonico a317094e, AfinacaoDasCordas 66e28e61) contra as versoes que a
revisao independente APROVOU (13386223 e 23a6c93d): tira-se TODO comentario Lean (/- ... -/ aninhado, /-- ... -/, /-! ... -/, -- ...), normaliza-se espaco em branco e
compara-se o CODIGO; o que mudou nos comentarios e' listado por diff de linhas. So le; grava so' o JSON nesta pasta."""
import difflib, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
H = os.path.dirname(os.path.abspath(__file__))
PARES = {"Sonico": (r"C:\IALD\Central de Patentes\work\sonico_v398\Sonico.lean.bak_20261023_195041", r"C:\t\k398c\final\TGLExt\Sonico.lean", "1338622344dd80c7", "a317094e337fd8b7"),
         "AfinacaoDasCordas": (r"C:\IALD\Central de Patentes\work\afinacao_das_cordas_v398\AfinacaoDasCordas.lean.bak_20261023_204818", r"C:\t\k398c\final\TGLExt\AfinacaoDasCordas.lean", "23a6c93d6dc84319", "66e28e61086cc6ba")}
def strip_comments(s):
    out = []; i = 0; n = len(s); depth = 0
    while i < n:
        if depth == 0 and s.startswith("/-", i):
            depth = 1; i += 2; continue
        if depth > 0:
            if s.startswith("/-", i): depth += 1; i += 2; continue
            if s.startswith("-/", i): depth -= 1; i += 2; continue
            i += 1; continue
        if s.startswith("--", i):
            j = s.find("\n", i); i = n if j < 0 else j; continue
        out.append(s[i]); i += 1
    t = "".join(out)
    return "\n".join(l.rstrip() for l in t.splitlines() if l.strip())
R = {}
for nome, (a, b, ha, hb) in PARES.items():
    sa, sb = open(a, "rb").read(), open(b, "rb").read()
    ok_h = (hashlib.sha256(sa).hexdigest()[:16] == ha, hashlib.sha256(sb).hexdigest()[:16] == hb)
    ca, cb = strip_comments(sa.decode("utf-8")), strip_comments(sb.decode("utf-8"))
    dcode = [l for l in difflib.unified_diff(ca.splitlines(), cb.splitlines(), lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    dall = [l for l in difflib.unified_diff(sa.decode("utf-8").splitlines(), sb.decode("utf-8").splitlines(), lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    R[nome] = {"aprovada_sha16_confere": ok_h[0], "final_sha16_confere": ok_h[1], "codigo_identico_sem_comentarios": ca == cb, "n_linhas_codigo": (len(ca.splitlines()), len(cb.splitlines())),
               "diff_codigo": dcode[:20], "n_linhas_diff_total": len(dall), "diff_comentarios_amostra": [l[:220] for l in dall][:40]}
json.dump(R, open(os.path.join(H, "COMPARACAO_PEDRAS_APROVADAS_vs_FINAIS.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in R.items():
    print(k, {x: v[x] for x in v if x not in ("diff_comentarios_amostra", "diff_codigo")}, "| diff_codigo:", v["diff_codigo"][:6])
    for l in v["diff_comentarios_amostra"]: print("   ", l[:200])
