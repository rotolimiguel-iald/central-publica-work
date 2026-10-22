# -*- coding: utf-8 -*-
"""medir_baseline.py (R3.4, 19/10/2026) -- fotografia SO DE LEITURA do que a R3.4 promete nao tocar: a Bancada de producao, o Nos, o livro de eventos, a pasta
da cadeia v394 e as pastas base_vNNN. Grava a fotografia num arquivo NOVO dentro de R3_4 (argv[1]). Nada mais e escrito.
uso: python -I -B -X utf8 medir_baseline.py <saida.json>"""
import sys
sys.dont_write_bytecode = True
import datetime, hashlib, json, os
from pathlib import Path

PROD = Path("C:/IALD/Bancada_Um")
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
EVENTOS = Path("C:/IALD/PROGRAMA_IALD/eventos.jsonl")
CADEIA = Path("C:/IALD/Central de Patentes/work/cadeia_de_selo")
V394 = CADEIA / "v394"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def listar(raiz):
    """nome relativo -> [bytes, mtime_ns] de TODO arquivo sob raiz, sem seguir juncao nem link."""
    raiz, out = Path(raiz), {}
    pilha = [raiz]
    while pilha:
        d = pilha.pop()
        with os.scandir(d) as it:
            for e in it:
                if e.is_junction() or e.is_symlink():
                    out[os.path.relpath(e.path, raiz)] = ["JUNCAO_OU_LINK", 0]
                elif e.is_dir(follow_symlinks=False):
                    pilha.append(Path(e.path))
                elif e.is_file(follow_symlinks=False):
                    st = e.stat()
                    out[os.path.relpath(e.path, raiz)] = [st.st_size, st.st_mtime_ns]
    return out


def lista_sha(l):
    return hashlib.sha256(json.dumps(l, sort_keys=True).encode("utf-8")).hexdigest()


prod = listar(PROD)
v394 = listar(V394)
nos_top = sorted(os.listdir(NOS))
chaves = ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json")
ev = EVENTOS.read_bytes()
bases = {}
for p in sorted(CADEIA.glob("v*/base_v*")):
    bases[str(p.relative_to(CADEIA))] = {f.name: dict(bytes=f.stat().st_size, sha256=sha(f)) for f in sorted(p.iterdir()) if f.is_file()}
out = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"),
           producao=dict(n_arquivos=len(prod), lista_sha256=lista_sha(prod), manifesto_sha256=sha(PROD / "canonical_contracts.json"),
                         manifesto_bytes=(PROD / "canonical_contracts.json").stat().st_size),
           nos=dict(n_itens_topo=len(nos_top), topo_sha256=hashlib.sha256(json.dumps(nos_top).encode("utf-8")).hexdigest(),
                    **{c: dict(bytes=(NOS / c).stat().st_size, sha256=sha(NOS / c), mtime_ns=(NOS / c).stat().st_mtime_ns) for c in chaves}),
           eventos=dict(bytes=len(ev), linhas=len(ev.splitlines()), sha256=hashlib.sha256(ev).hexdigest()),
           cadeia_v394=dict(n_arquivos=len(v394), lista_sha256=lista_sha(v394)),
           bases_vNNN=bases)
p = Path(sys.argv[1])
with open(p, "xb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
print(p, out["producao"]["manifesto_sha256"][:16], out["nos"]["um.py"]["sha256"][:16], out["eventos"]["linhas"], out["cadeia_v394"]["n_arquivos"])
