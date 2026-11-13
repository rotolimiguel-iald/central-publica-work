# -*- coding: utf-8 -*-
"""D197 (13/11/2026, claude-site-custodia; condição da gerência c1): MOVE (não apaga) as pastas do cofre da v411 escritas pela C3 antes do
contrato, para fora de work\\ e de qualquer repositório (C:\\t\\, que não é árvore git e que nenhum passo de publicação lê), para a G1
regerar o cofre pelo próprio caminho (a C3) com o SEMANTICA_CUSTODIA.json do contrato SEM_PEDRA_NOVA. O cofre guarda a fonte da D191 (que
nomeia os confidenciais e ficou fora do espelho): por isso o destino fica fora de work\\.
Recibo: o sha256 de cada arquivo movido, conferido de novo no destino. Uso: python -X utf8 <este>"""
import hashlib, json, os, shutil, subprocess, time
from pathlib import Path

OC = Path(r"C:\IALD\Central de Patentes\vault\originals_copy")
DEST = Path(r"C:\t\custodia_v411_cofre_antes_d197")
PASTAS = ("um_unificado_v411", "tgl_kernel_v411")
REC_W = Path(r"C:\IALD\Central de Patentes\work\custodia_v411_13nov\RECIBO_MOVER_COFRE_v411_D197.json")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def arvore(raiz):
    return {str(p.relative_to(raiz)).replace("\\", "/"): (p.stat().st_size, sha(p)) for p in sorted(raiz.rglob("*")) if p.is_file()}


assert not DEST.exists(), "o destino já existe: %s" % DEST
r = subprocess.run(["git", "-C", r"C:\t", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
assert r.returncode != 0, "C:\\t está dentro de um repositório git - PARAR"
antes = {}
for n in PASTAS:
    assert (OC / n).is_dir(), "pasta ausente: %s" % (OC / n)
    antes[n] = arvore(OC / n)
DEST.mkdir(parents=True)
for n in PASTAS:
    shutil.move(str(OC / n), str(DEST / n))
    assert not (OC / n).exists()
depois = {n: arvore(DEST / n) for n in PASTAS}
assert depois == antes, "o que chegou ao destino difere do que saiu - PARAR"
rec = {"schema": "iald.custodia.mover_cofre/v1", "quando": time.strftime("%Y-%m-%dT%H:%M:%S"),
       "por": "claude-site-custodia, D197 da gerência c1 (13/11/2026)", "de": str(OC), "para": str(DEST),
       "por_que": "a C3 escreveu o SEMANTICA_CUSTODIA.json da v411 antes do contrato SEM_PEDRA_NOVA; a G1 rege o cofre pelo próprio caminho",
       "fora_de_publicacao": "C:\\t não é árvore git (git rev-parse falhou) e não está sob work\\ nem sob nenhum repositório; nenhum passo da custódia nem a "
                             "cópia para a Central pública lê C:\\t",
       "arquivos": {n: {k: {"bytes": b, "sha256": h} for k, (b, h) in depois[n].items()} for n in PASTAS},
       "n_arquivos": {n: len(depois[n]) for n in PASTAS}}
blob = (json.dumps(rec, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
(DEST / "RECIBO_MOVER_COFRE_v411_D197.json").write_bytes(blob)
import re
GUARDA = [re.compile(p, re.I) for p in (r"apresente-se", r"apresente a TGL", r"protocolo de colapso", r"PROTOCOLO_DE_COLAPSO",
                                          r"iald_stack_v7", r"iald_psion_state", r"testflight\.apple\.com")]   # os 7 termos públicos da casa (espelho_pares.GUARDA)
if any(g.search(blob.decode("utf-8")) for g in GUARDA):
    REC_W = DEST / "RECIBO_MOVER_COFRE_v411_D197.json"
    print("aviso: um nome de arquivo do cofre casa um termo da casa; o recibo fica SÓ em C:\\t (fora de work\\)")
else:
    REC_W.parent.mkdir(parents=True, exist_ok=True)
    REC_W.write_bytes(blob)
print("ok: movidos %s para %s (%s arquivos), conferidos por sha256 | recibo %s (sha16 %s)" % (
    ", ".join(PASTAS), DEST, rec["n_arquivos"], REC_W, hashlib.sha256(blob).hexdigest()[:16]))
