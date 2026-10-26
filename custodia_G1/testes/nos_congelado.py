# -*- coding: utf-8 -*-
"""Uma VISTA do Nós em que a v398 está PRONTA e CONGELADA: hardlinks para os arquivos do Nós vivo (nada é copiado), junctions para as pastas, mas
  - todo arquivo do Nós que o cofre `um_unificado_v398` também guarda (selados, capturas, diário, handoff, stdout) é hardlink para a CÓPIA DO COFRE (os do selo, com o sha256 conferido);
  - o `tgl_kernel` é uma árvore de hardlinks para o kernel selado `tgl_kernel_v398` do cofre (o Nós vivo já mexe em TGLExt.lean e TGL/Audit.lean para a v399).
Só para REPETIR a suíte (e compor o TESTES.md) com o Nós congelado na v398 (G1_RAIZ_NOS=<vista>) quando outra sessão o põe em obra. Nada do Nós vivo é tocado
(hardlinks e junctions só leem; nenhum arquivo do Nós é aberto para escrita).
  python nos_congelado.py criar     -> imprime o caminho da vista
  python nos_congelado.py remover   -> desfaz (rmdir nas junctions e unlink nos hardlinks; NUNCA rmtree através de junction)
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
RAIZ = Path(r"C:\tmp\g1_nosview")
VISTA = RAIZ / "Nós"
COFRE = Path(r"C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v398")
KCOFRE = Path(r"C:\IALD\Central de Patentes\vault\originals_copy\tgl_kernel_v398")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def junction(link, alvo):
    r = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(alvo)], capture_output=True)
    if r.returncode != 0:
        raise SystemExit("mklink /J falhou: %r %r" % (r.stdout, r.stderr))


def criar():
    selo = json.loads((COFRE / "um_absoluto_selo.json").read_text(encoding="utf-8"))
    assert selo["um_version"] == "v398", selo["um_version"]
    pin = selo["sha256"]["um.py"]
    assert sha256(COFRE / "um.py") == pin, "o um.py do cofre não é o v398 do selo"
    if RAIZ.exists():
        raise SystemExit("a vista já existe: %s (rode 'remover')" % RAIZ)
    VISTA.mkdir(parents=True)
    n_f = n_d = n_k = n_s = 0
    selados = set(selo["sha256"]) | {"um_absoluto_selo.json"}
    for e in sorted(os.scandir(NOS), key=lambda e: e.name):
        dest = VISTA / e.name
        if e.name == "tgl_kernel":
            for raiz, dirs, files in os.walk(KCOFRE):
                rel = Path(raiz).relative_to(KCOFRE)
                (dest / rel).mkdir(parents=True, exist_ok=True)
                for f in files:
                    if rel == Path(".") and f == "CUSTODY_MANIFEST.json":
                        continue                 # é do cofre, não do kernel
                    os.link(Path(raiz) / f, dest / rel / f)
                    n_k += 1
        elif not e.is_dir() and (COFRE / e.name).is_file():
            if e.name in selo["sha256"]:
                assert sha256(COFRE / e.name) == selo["sha256"][e.name], "o cofre não tem o %s selado" % e.name
            os.link(COFRE / e.name, dest)        # o artefato da v398 como o cofre o guardou (selados, capturas, diário, handoff, stdout): congelado
            n_s += 1
        elif e.is_dir():
            junction(dest, e.path)
            n_d += 1
        else:
            os.link(e.path, dest)
            n_f += 1
    junction(RAIZ / "cache", NOS.parent / "cache")
    print("vista criada: %d arquivos do Nós vivo (hardlink), %d selados do cofre, %d arquivos do kernel selado, %d pastas (junction)" % (n_f, n_s, n_k, n_d), file=sys.stderr)
    return VISTA


def remover():
    if not RAIZ.exists():
        print("nada a remover")
        return

    def limpar(base):
        for e in list(os.scandir(base)):
            p = Path(e.path)
            if os.path.isjunction(p):
                os.rmdir(p)                      # só a junction, nunca o alvo
            elif e.is_dir(follow_symlinks=False):
                limpar(p)                        # pasta REAL da vista (a do kernel): só hardlinks dentro
                p.rmdir()
            else:
                os.unlink(p)
    limpar(RAIZ)
    RAIZ.rmdir()
    print("vista removida")


if __name__ == "__main__":
    r = {"criar": criar, "remover": remover}[sys.argv[1]]()
    if r:
        print(r)
