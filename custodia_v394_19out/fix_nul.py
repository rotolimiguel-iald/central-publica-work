# Troca o caractere NUL (gravado por engano pelo heredoc) pelo escape de texto \0 no script do espelho v394.
import os, py_compile
p = r"C:\IALD\Site\tgl\v3.0_bancada\tools\custodia_v394_espelho.py"
b = open(p, "rb").read()
n = b.count(b"\x00")
assert n == 1, n
b = b.replace(b"\x00", b"\\0")
open(p + ".tmp", "wb").write(b)
os.replace(p + ".tmp", p)
py_compile.compile(p, doraise=True)
s = open(p, encoding="utf-8").read()
i = s.find('split("')
print("NUL trocado:", n, "| trecho:", s[i:i + 12])
j = s.find('_ja = [_r for _r')
print(s[j:j + 120])
k = s.find('"caminho_no_espelho": str(_dst.relative_to(TB))')
print(s[k:k + 90])
