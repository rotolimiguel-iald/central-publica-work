# -*- coding: utf-8 -*-
"""[rodada 2: copia do varrer_fonte.py da rodada 1, so com a pasta base trocada para 3_KERNEL\rodada2]
Varredura textual da pedra candidata (somente leitura): (a) tokens vetados FORA de comentarios
(sorry, admit, axiom, native_decide, implemented_by, extern, opaque); (b) as mesmas palavras dentro de comentarios
(listadas para transparencia); (c) literais numericos de alpha, beta ou theta_M em QUALQUER lugar do arquivo;
(d) o vocabulario que a regua proibe como veredito (montado dinamicamente para que este script nao o contenha
como literal). Grava VARREDURA_FONTE.json."""
import hashlib, json, os, re, sys

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # rodada2
PEDRA = os.path.join(AQUI, "sandbox", "TGLExt", "TheUnitIsTheRank.lean")
src_b = open(PEDRA, "rb").read()
src = src_b.decode("utf-8")


def sem_comentarios(s):
    out, i, n, prof = [], 0, len(s), 0
    while i < n:
        if s.startswith("/-", i):
            prof += 1
            i += 2
            continue
        if prof > 0:
            if s.startswith("-/", i):
                prof -= 1
                i += 2
            else:
                if s[i] == "\n":
                    out.append("\n")
                i += 1
            continue
        if s.startswith("--", i):
            j = s.find("\n", i)
            i = n if j < 0 else j
            continue
        if s[i] == '"':
            j = i + 1
            while j < n and s[j] != '"':
                j += 2 if s[j] == "\\" else 1
            out.append('""')
            i = j + 1
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


codigo = sem_comentarios(src)
vetados = ["sorry", "admit", "axiom", "native_decide", "implemented_by", "extern", "opaque"]
res = {"pedra": PEDRA, "pedra_sha256": hashlib.sha256(src_b).hexdigest(), "bytes": len(src_b),
       "tokens_vetados_no_codigo": {}, "tokens_vetados_em_comentarios": {}, "literais_alpha_beta": [],
       "vocabulario_proibido": {}}
for t in vetados:
    res["tokens_vetados_no_codigo"][t] = len(re.findall(r"(?<![A-Za-z0-9_.])" + t + r"(?![A-Za-z0-9_])", codigo))
    res["tokens_vetados_em_comentarios"][t] = len(re.findall(r"(?<![A-Za-z0-9_.])" + t + r"(?![A-Za-z0-9_])", src)) - \
        res["tokens_vetados_no_codigo"][t]
padroes = [r"0[.,]0120", r"0[.,]012\b", r"7[.,]297", r"0[.,]1099", r"0[.,]10969", r"6[.,]297", r"1[.,]2031",
           r"137[.,]03", r"0[.,]97623", r"0[.,]9759"]
for p in padroes:
    for m in re.finditer(p, src):
        ln = src.count("\n", 0, m.start()) + 1
        res["literais_alpha_beta"].append({"padrao": p, "linha": ln})
proib = ["CONFIRM" + "ED", "CONFIRM" + "ADA", "n" + "ão prov" + "ou", "nao prov" + "ou", "pós-di" + "ção",
         "pos-di" + "cao"]
for p in proib:
    # a chave gravada e MASCARADA (ponto medio no meio) para que nenhum arquivo deste 3_KERNEL contenha a palavra
    res["vocabulario_proibido"][p[:len(p) // 2] + "·" + p[len(p) // 2:]] = src.count(p)
ok = (all(v == 0 for v in res["tokens_vetados_no_codigo"].values()) and not res["literais_alpha_beta"]
      and all(v == 0 for v in res["vocabulario_proibido"].values()))
res["veredito"] = "VARREDURA_LIMPA" if ok else "VARREDURA_ACHOU"
dst = os.path.join(AQUI, "VARREDURA_FONTE.json")
with open(dst + ".tmp", "wb") as f:
    f.write(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8") + b"\n")
os.replace(dst + ".tmp", dst)
print(json.dumps(res, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 2)
