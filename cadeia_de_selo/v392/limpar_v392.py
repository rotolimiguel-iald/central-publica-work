# -*- coding: utf-8 -*-
"""limpar_v392.py -- apaga SO' o que a preparacao criou e e' grande: C:\t\k392 (sandboxes do kernel, arvore so-fontes, scratch) e dry_v392\tgl_kernel. Lista antes, recusa caminho fora das duas raizes,
nao segue juncao. Mantem logs e recibos (todos em cadeia_de_selo\v392). Uso: python -I -B -X utf8 limpar_v392.py [--apagar]"""
import json, os, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
alvos = [os.path.join("C:" + os.sep, "t", "k392"), os.path.join(HERE, "dry_v392", "tgl_kernel")]
ok_raiz = [os.path.normcase(os.path.realpath(a)) for a in alvos]
rel = {"alvos": [], "apagou": False}
for a in alvos:
    if not os.path.exists(a):
        continue
    assert os.path.normcase(os.path.realpath(a)) in ok_raiz and not os.path.islink(a)
    n = 0; b = 0; juncoes = []
    for r, ds, fs in os.walk(a):
        for d in list(ds):
            p = os.path.join(r, d)
            if os.path.islink(p) or (getattr(os.lstat(p), "st_file_attributes", 0) & 0x400):
                juncoes.append(p); ds.remove(d)
        for f in fs:
            n += 1; b += os.lstat(os.path.join(r, f)).st_size
    rel["alvos"].append({"pasta": a, "arquivos": n, "bytes": b, "juncoes": juncoes})
    assert not juncoes, ("juncao dentro do alvo: nao apago", juncoes[:3])
print(json.dumps(rel, ensure_ascii=False, indent=1))
if "--apagar" in sys.argv:
    for a in alvos:
        if os.path.exists(a):
            shutil.rmtree(chr(92) * 2 + "?" + chr(92) + a, onexc=lambda fn_, p_, e_: (os.chmod(p_, 0o700), fn_(p_)))   # .git do pacote copiado tem arquivos somente-leitura
    rel["apagou"] = True
    json.dump(rel, open(os.path.join(HERE, "LIMPEZA_v392.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("apagado:", [os.path.exists(a) for a in alvos])
