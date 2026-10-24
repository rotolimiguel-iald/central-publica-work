# -*- coding: utf-8 -*-
"""comparar_codigo.py -- prova que a versao nova de AfinacaoDasCordas.lean difere da ANTERIOR (revisada) so em COMENTARIOS (docstrings): o codigo fora de
/- ... -/ e de `--` e' byte a byte o mesmo (imports, set_option, enunciados, provas, #print axioms). E, se existirem termos_antes.txt e termos_depois.txt
(hash estrutural do TIPO e do VALOR de cada uma das 59 declaracoes do .olean, antes e depois da recompilacao), compara os dois. So leitura;
grava conferencia_codigo_identico.json. Uso: python -I -B -X utf8 comparar_codigo.py [sha16_da_versao_anterior]   (padrao: 23a6c93d6dc84319, a revisada)
"""
import glob
import hashlib
import json
import os
import re
import sys

W = r"C:\IALD\Central de Patentes\work\afinacao_das_cordas_v398"
ANTERIOR16 = sys.argv[1] if len(sys.argv) > 1 else "23a6c93d6dc84319"
NOVA = os.path.join(W, "AfinacaoDasCordas.lean")
SBNOVA = r"C:\t\k398b\TGLExt\AfinacaoDasCordas.lean"


def sem_comentarios(t):
    t = re.sub(r"/-.*?-/", "", t, flags=re.S)  # blocos (/-! ... -/ e /-- ... -/); sem aninhamento (conferido: /- e -/ em igual numero)
    t = re.sub(r"--[^\n]*", "", t)
    return t


def sha16(b):
    return hashlib.sha256(b).hexdigest()[:16]


antiga = None
for p in sorted(glob.glob(os.path.join(W, "AfinacaoDasCordas.lean.bak_*"))):
    b = open(p, "rb").read()
    if sha16(b) == ANTERIOR16:
        antiga = (p, b)
        break
assert antiga, f"nenhum backup com sha16 {ANTERIOR16}"
nova_b = open(NOVA, "rb").read()
assert nova_b == open(SBNOVA, "rb").read(), "a nova difere da copia do sandbox"
ta, tn = antiga[1].decode("utf-8"), nova_b.decode("utf-8")
ca, cn = sem_comentarios(ta), sem_comentarios(tn)
assert ta.count("/-") == ta.count("-/") and tn.count("/-") == tn.count("-/"), "comentarios desbalanceados"
R = {
    "anterior": {"arquivo": antiga[0], "sha16": sha16(antiga[1]), "bytes": len(antiga[1]), "linhas": ta.count("\n")},
    "nova": {"arquivo": NOVA, "sha16": sha16(nova_b), "bytes": len(nova_b), "linhas": tn.count("\n"), "igual_a_copia_do_sandbox": True},
    "codigo_fora_dos_comentarios": {
        "identico": ca == cn, "anterior_sha16": hashlib.sha256(ca.encode("utf-8")).hexdigest()[:16], "nova_sha16": hashlib.sha256(cn.encode("utf-8")).hexdigest()[:16],
        "bytes_anterior": len(ca.encode("utf-8")), "bytes_nova": len(cn.encode("utf-8")),
    },
    "blocos_de_comentario": {"anterior": ta.count("/-"), "nova": tn.count("/-")},
}
assert ca == cn, "o codigo fora dos comentarios DIFERE"

# termos do kernel (tipo e valor de cada declaracao), antes e depois da recompilacao
fa, fd = os.path.join(W, "termos_antes.txt"), os.path.join(W, "termos_depois.txt")
if os.path.exists(fa) and os.path.exists(fd):
    def ler(p):
        d = {}
        for ln in open(p, encoding="utf-8"):
            m = re.search(r"TERMO\|(.*)$", ln.rstrip("\r\n"))
            if m:
                nome, th, vh = m.group(1).split("|")
                d[nome] = (th, vh)
        return d
    A, D = ler(fa), ler(fd)
    diff = sorted(n for n in set(A) | set(D) if A.get(n) != D.get(n))
    R["termos_do_kernel"] = {
        "n_antes": len(A), "n_depois": len(D), "diferentes": diff, "identicos": (A == D),
        "antes_sha16": hashlib.sha256(open(fa, "rb").read()).hexdigest()[:16], "depois_sha16": hashlib.sha256(open(fd, "rb").read()).hexdigest()[:16],
        "nota": "hash estrutural (Expr.hash, 32 bits) do TIPO e do VALOR de cada declaracao do modulo, lido do .olean antes e depois da recompilacao; docstrings nao entram no termo",
    }
    assert A == D, diff
json.dump(R, open(os.path.join(W, "conferencia_codigo_identico.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
