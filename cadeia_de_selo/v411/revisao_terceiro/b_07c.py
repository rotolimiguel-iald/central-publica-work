import re
t = open(r"C:\IALD\CLAUDE.md", encoding="utf-8", errors="replace").read().replace("**", "")
nrm = lambda s: " ".join(s.split())
ger = "A confirmação é ato do observador humano"   # frase da gerencia (CLAUDE.md), nao fala do operador
print("trecho de texto da gerencia presente no corpus _CASA (substring, como _corpus_um):", nrm(ger).lower() in nrm(t).lower())
src = open(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\conferir_citacoes_v411.py", encoding="utf-8").read()
i = src.index("_corpus_um = lambda"); print(src[i:i+330])
