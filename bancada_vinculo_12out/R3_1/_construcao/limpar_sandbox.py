# -*- coding: utf-8 -*-
"""limpar_sandbox.py (R3.1, 13/10/2026) -- apaga o sandbox curto C:/t/vb* SEM seguir juncao nem link: cada juncao/link e desfeito com
os.rmdir no proprio link (nunca no alvo) antes do rmtree; confere que nenhuma sobrou. Imprime a lista da producao antes e depois.
uso: limpar_sandbox.py <raiz C:/t/vb*>"""
import sys
sys.dont_write_bytecode = True
import json, os, re, shutil
from pathlib import Path

RAIZ = Path(sys.argv[1])
assert RAIZ.parent == Path("C:/t") and re.match(r"^vb[0-9A-Za-z_-]*$", RAIZ.name), "so C:/t/vb*"
PROD = Path("C:/IALD/Bancada_Um")
antes = sorted(os.listdir(PROD))
desfeitas = []
if RAIZ.exists():
    pilha = [str(RAIZ)]
    while pilha:
        d = pilha.pop()
        with os.scandir(d) as it:
            for e in it:
                if e.is_junction() or e.is_symlink():
                    if e.is_dir(follow_symlinks=False) or e.is_junction() or os.path.isdir(e.path):
                        os.rmdir(e.path)
                    else:
                        os.unlink(e.path)
                    desfeitas.append(e.path)
                elif e.is_dir(follow_symlinks=False):
                    pilha.append(e.path)
    restam = []
    for dp, dns, fns in os.walk(RAIZ, followlinks=False):
        for n in dns + fns:
            p = os.path.join(dp, n)
            if os.path.islink(p) or Path(p).is_junction():
                restam.append(p)
    assert not restam, restam
    shutil.rmtree(RAIZ)
depois = sorted(os.listdir(PROD))
assert antes == depois, "a lista da producao mudou"
print(json.dumps(dict(raiz=str(RAIZ), juncoes_desfeitas=desfeitas, existe_depois=RAIZ.exists(), producao_lista_igual=antes == depois), ensure_ascii=False))
