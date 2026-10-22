# -*- coding: utf-8 -*-
"""carrega _EMBEDDED_KERNEL_FILES de um um.py SEM executa-lo (ast.literal_eval do literal do dict)."""
import ast, hashlib, sys
def carregar(path):
    raw = open(path, "rb").read()
    text = raw.decode("utf-8")
    lines = text.splitlines(keepends=True)
    i0 = [i for i, l in enumerate(lines) if l.startswith("_EMBEDDED_KERNEL_FILES = {")]
    assert len(i0) == 1, i0
    i0 = i0[0]
    j = i0 + 1
    while lines[j].rstrip("\r\n") != "}":
        j += 1
    src = "".join(lines[i0:j + 1]).split("=", 1)[1]
    d = ast.literal_eval(src.strip())
    return d, i0 + 1, j + 1, hashlib.sha256(raw).hexdigest()[:16]
if __name__ == "__main__":
    d, a, b, h = carregar(sys.argv[1])
    print(h, len(d), a, b)
