"""Confere que a revisão v1 -> v2 da pedra mudou SÓ TEXTO (comentários, docstrings, strings): o código restante é idêntico.

Remove comentários de bloco (aninhados, inclusive docstrings `/-- -/` e `/-! -/`), comentários de linha `--` e literais de string;
compara o que sobra (normalizando espaço em branco) entre o backup v1 e o arquivo atual. Só leitura.
Uso: python -I -X utf8 verifica_so_texto.py <v1.bak> <v2.lean>
"""
import hashlib
import re
import sys


def strip_comments_and_strings(s):
    out = []
    i, n, depth = 0, len(s), 0
    while i < n:
        if depth == 0 and s.startswith("/-", i):
            depth = 1
            i += 2
            continue
        if depth > 0:
            if s.startswith("/-", i):
                depth += 1
                i += 2
            elif s.startswith("-/", i):
                depth -= 1
                i += 2
            else:
                i += 1
            continue
        if s.startswith("--", i):
            j = s.find("\n", i)
            i = n if j < 0 else j
            continue
        if s[i] == '"':
            i += 1
            while i < n and s[i] != '"':
                i += 2 if s[i] == "\\" else 1
            i += 1
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


def codigo(path):
    s = open(path, "rb").read().decode("utf-8")
    c = re.sub(r"\s+", " ", strip_comments_and_strings(s)).strip()
    return s, c


s1, c1 = codigo(sys.argv[1])
s2, c2 = codigo(sys.argv[2])
print("v1: bytes", len(s1.encode("utf-8")), "| código sem comentários sha16", hashlib.sha256(c1.encode("utf-8")).hexdigest()[:16], "| chars", len(c1))
print("v2: bytes", len(s2.encode("utf-8")), "| código sem comentários sha16", hashlib.sha256(c2.encode("utf-8")).hexdigest()[:16], "| chars", len(c2))
print("CÓDIGO IDÊNTICO (só texto mudou):", c1 == c2)
if c1 != c2:
    for k, (a, b) in enumerate(zip(c1, c2)):
        if a != b:
            print("primeira diferença em", k, repr(c1[max(0, k - 80):k + 80]), "||", repr(c2[max(0, k - 80):k + 80]))
            break
