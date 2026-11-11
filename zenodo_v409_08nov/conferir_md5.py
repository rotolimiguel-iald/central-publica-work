# -*- coding: utf-8 -*-
"""Confere os 15 arquivos do deposito Zenodo da v409 (10.5281/zenodo.24053883, publicado pelo operador em 2026-11-08) por md5 contra os arquivos do
No's (selados) e as portas do espelho (por commit). Os md5 do Zenodo vieram da API do registro; aqui so se calcula e compara. Somente leitura."""
import hashlib
import json
import subprocess
from pathlib import Path

NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
TB = Path(r"C:\IALD\Artigo\the_boundary")
ZEN = {
    "um_absoluto_en.pdf": "6c9f310d2253966db5e52cc90e209a75", "MEMORIA_DA_LINHAGEM.md": "13d4916bfd77702d1a3b93309c13da47",
    "um_absoluto_pt.pdf": "9caea6c42b8204e551ad8af685a5b2be", "um_absoluto_pilar_quantico.json": "5843d995e8b19fd0bf0e6d78cb75f997",
    "PORTA.md": "44e55e8a4a3b36e97be8fad269c15a4e", "um_absoluto_en.txt": "323b77ee7e6e4da96170c2563c4674cb",
    "um_absoluto_pt.txt": "67a95fb359e104c6d675a4147f518f96", "um_absoluto.json": "85bc0b120824231e8506f51ec692ef03",
    "um_absoluto_manifest.md": "e4870f52875a172626fa4138dab5acdf", "PORTA.json": "cc1e4d27453db82f6978f7c2e1a32aac",
    "A_PROVA_DA_QG_TGL_arvore.md": "b12c93e8f19a072ee0ff7c52b7aef3f1", "DESENHO_DO_FECHAMENTO_QG.md": "f87ddc98075a3c91f96ea9b55cdf3dea",
    "um.py": "6775bfccd922c16e61550564d377c275", "um_absoluto_forma_canonica.md": "743099b1452c0df01d528a5cd7ae2edd",
    "um_absoluto_selo.json": "8265f08357322ad7b419c9d2c9e8158b",
}


def md5(b):
    return hashlib.md5(b).hexdigest()


res = {}
for nome, esp in ZEN.items():
    p = NOS / nome
    if nome.startswith("PORTA"):
        continue
    res[nome] = {"onde": "Nós", "existe": p.is_file(), "bate": p.is_file() and md5(p.read_bytes()) == esp}
# as duas portas: procurar o commit do espelho cujo arquivo de raiz tem o md5 depositado
commits = subprocess.run(["git", "-C", str(TB), "log", "--format=%h", "-n", "12", "--", "PORTA.md"], capture_output=True, text=True).stdout.split()
for nome in ("PORTA.md", "PORTA.json"):
    achado = None
    for c in commits:
        r = subprocess.run(["git", "-C", str(TB), "show", "%s:%s" % (c, nome)], capture_output=True)
        if r.returncode == 0 and md5(r.stdout) == ZEN[nome]:
            achado = c
            break
    atual = md5((TB / nome).read_bytes()) == ZEN[nome]
    res[nome] = {"onde": "espelho (raiz)", "commit_que_bate": achado, "bate_no_disco_hoje": atual}
print(json.dumps(res, ensure_ascii=False, indent=1))
nos_ok = [k for k, v in res.items() if v["onde"] == "Nós" and v["bate"]]
print("Nós batem:", len(nos_ok), "de", sum(1 for v in res.values() if v["onde"] == "Nós"))
print("portas batem em algum commit:", [k for k, v in res.items() if v["onde"] != "Nós" and (v["commit_que_bate"] or v["bate_no_disco_hoje"])])
