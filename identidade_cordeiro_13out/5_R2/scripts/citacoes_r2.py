# -*- coding: utf-8 -*-
"""Confere a pedra r2: (1) toda citacao entre aspas angulares esta nos bytes dos verbatins do operador (13/10 ou 08/10),
fragmento a fragmento (elisao marcada por reticencias); (2) nenhuma ocorrencia da palavra proibida da regua;
(3) varredura de numeros decimais (nenhum numero do artigo; nenhum alpha/beta literal); (4) sorry/admit/axiom/
native_decide/implemented_by/extern/unsafe/opaque como palavra de codigo. Uso: citacoes_r2.py <pedra.lean> <saida.json>"""
import sys, re, json, hashlib
V13 = "C:/IALD/Central de Patentes/work/cunhagens_13out/OPERADOR_13out_identidade_cordeiro_verbatim.txt"
V08 = "C:/IALD/Central de Patentes/work/f9_pergunta_08out/OPERADOR_08out_resposta_verbatim.txt"
b13, b08 = open(V13, "rb").read(), open(V08, "rb").read()
assert hashlib.sha256(b13).hexdigest() == "2ebc1dd3d73cf94094551de520d5d9765dde5633594f2c4ca61cc2fb1df1002e"
assert hashlib.sha256(b08).hexdigest() == "a9cecc128f40c101f873279511c134530b8fc53157d784e0fc48b97aa20433ff"
v13, v08 = b13.decode("utf-8"), b08.decode("utf-8")
src_b = open(sys.argv[1], "rb").read()
src = src_b.decode("utf-8")
cit = []
for mm in re.finditer(r"«([^»]*)»", src):
    q = mm.group(1)
    frags = [f.strip() for f in q.split("…") if f.strip()]
    if not frags:
        continue
    em13 = all(f in v13 for f in frags)
    em08 = all(f in v08 for f in frags)
    linha = src.count("\n", 0, mm.start()) + 1
    cit.append({"linha": linha, "citacao": q, "no_verbatim_13out": em13, "no_verbatim_08out": em08,
                "nos_bytes": em13 or em08})
proibida = "CONFIR" + "MED"
codigo = re.sub(r"/-.*?-/", " ", src, flags=re.S)
codigo = re.sub(r"--[^\n]*", " ", codigo)
palavras = {w: len(re.findall(r"\b%s\b" % w, codigo)) for w in
            ("sorry", "admit", "axiom", "native_decide", "implemented_by", "extern", "unsafe", "opaque")}
decimais = sorted(set(re.findall(r"(?<![\w.])\d+[.,]\d+(?![\w])", src)))
out = {"pedra": sys.argv[1], "sha256": hashlib.sha256(src_b).hexdigest(), "n_citacoes": len(cit),
       "citacoes_fora_dos_bytes": [c for c in cit if not c["nos_bytes"]], "citacoes": cit,
       "palavra_proibida": src.count(proibida), "palavras_de_codigo_fora_de_comentario": palavras,
       "decimais_no_arquivo": decimais}
json.dump(out, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: out[k] for k in ("sha256", "n_citacoes", "citacoes_fora_dos_bytes", "palavra_proibida",
                                      "palavras_de_codigo_fora_de_comentario", "decimais_no_arquivo")}, ensure_ascii=False))
