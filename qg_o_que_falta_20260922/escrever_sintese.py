import hashlib, os, sys

NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
OUT = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\qg_falta\SINTESE.md"
EXPECT = {"um.py": "d9f5bd5dffc3333d", "um_absoluto.json": "456f0ab149bb13f6", "um_absoluto_selo.json": "18db1bbd8462c3be"}
for f, h in EXPECT.items():
    got = hashlib.sha256(open(os.path.join(NOS, f), "rb").read()).hexdigest()[:16]
    if got != h:
        sys.exit("FALHA: %s tem sha16 %s, esperado %s -- a sintese nao se escreve" % (f, got, h))

TEXT = open(os.path.join(os.path.dirname(OUT), "SINTESE_corpo.md"), "rb").read().decode("utf-8")
tmp = OUT + ".tmp"
with open(tmp, "wb") as fh:
    fh.write(TEXT.encode("utf-8"))
if os.path.getsize(tmp) != len(TEXT.encode("utf-8")) or os.path.getsize(tmp) < 5000:
    sys.exit("FALHA: temporario com tamanho inesperado")
os.replace(tmp, OUT)
b = open(OUT, "rb").read()
print("OK", len(b), hashlib.sha256(b).hexdigest()[:16])
