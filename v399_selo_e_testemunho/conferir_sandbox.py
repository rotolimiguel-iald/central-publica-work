# -*- coding: utf-8 -*-
"""conferir_sandbox.py -- confere que C:\\t\\k399\\final e' a copia fiel de C:\\t\\k398c\\final (so leitura de AMBOS; k398c NUNCA e' escrito) e le o hash do um.py do Nos.

(1) varre as duas arvores com os.scandir SEM seguir links (junction/symlink: conta e nao desce); compara (caminho relativo, tamanho) de todos os arquivos;
    as unicas diferencas permitidas em k399 sao os arquivos NOVOS desta tarefa (TGLExt/Testemunho.lean e seus backups em bytes, os artefatos de
    Testemunho em .lake/build/lib/lean/TGLExt e .lake/build/ir/TGLExt, o dir probe/);
(2) sha256 dos .lean e .olean dos modulos importados/citados, em k398c e k399;
(3) sha256 do um.py do Nos (a base declarada: c632fa261ce3f538) -- lido agora.
Grava conferencia_sandbox.json na pasta de trabalho. Uso: python -I -B -X utf8 conferir_sandbox.py
"""
import hashlib
import json
import os

W = r"C:\IALD\Central de Patentes\work\v399_selo_e_testemunho"
A = r"C:\t\k398c\final"
B = r"C:\t\k399\final"
UMPY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
MODS = ["Token", "TestemunhaEstatica", "Psibit", "CollapseContract", "CollapseCostAndAttestation", "ObserverInside", "TheGreatAttractor",
        "TheObserverReadsTheAngle", "TheLightInterface", "TheVerbSelectsTheAction", "TheNucleus", "BoundaryException"]


def varre(raiz):
    arq, links, dirs = {}, [], 0
    stack = [raiz]
    while stack:
        p = stack.pop()
        try:
            with os.scandir(p) as it:
                for e in it:
                    try:
                        lk = e.is_symlink() or e.is_junction()
                    except OSError:
                        lk = False
                    if lk:
                        links.append(os.path.relpath(e.path, raiz))
                        continue
                    if e.is_dir(follow_symlinks=False):
                        dirs += 1
                        stack.append(e.path)
                    else:
                        arq[os.path.relpath(e.path, raiz)] = e.stat(follow_symlinks=False).st_size
        except OSError as ex:
            print("ERRO", p, ex)
    return arq, links, dirs


fa, la, da = varre(A)
fb, lb, db = varre(B)
so_em_a = sorted(set(fa) - set(fb))
so_em_b = sorted(set(fb) - set(fa))
tam_diferente = sorted(k for k in set(fa) & set(fb) if fa[k] != fb[k])
R = {
    "k398c_final": {"arquivos": len(fa), "diretorios": da, "links_nao_seguidos": la[:20], "n_links": len(la)},
    "k399_final": {"arquivos": len(fb), "diretorios": db, "links_nao_seguidos": lb[:20], "n_links": len(lb)},
    "so_em_k398c": so_em_a[:50], "n_so_em_k398c": len(so_em_a),
    "so_em_k399": so_em_b[:80], "n_so_em_k399": len(so_em_b),
    "tamanho_diferente": tam_diferente[:50], "n_tamanho_diferente": len(tam_diferente),
}
R["copia_fiel_exceto_arquivos_novos"] = (not so_em_a) and (not tam_diferente) and all(
    ("Testemunho" in k) or k.startswith("probe" + os.sep) for k in so_em_b)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]


mods = {}
for m in MODS:
    for ext, sub in ((".lean", "TGLExt"), (".olean", os.path.join(".lake", "build", "lib", "lean", "TGLExt"))):
        pa, pb = os.path.join(A, sub, m + ext), os.path.join(B, sub, m + ext)
        if os.path.exists(pa) and os.path.exists(pb):
            mods[m + ext] = {"k398c": sha(pa), "k399": sha(pb), "iguais": sha(pa) == sha(pb)}
        else:
            mods[m + ext] = {"k398c_existe": os.path.exists(pa), "k399_existe": os.path.exists(pb)}
R["modulos_citados"] = mods
R["todos_modulos_iguais"] = all(v.get("iguais") for v in mods.values())
# o agregador TGLExt.lean NAO foi tocado (a pedra e' CANDIDATA: instalar = importa-la ali, ato da gerencia)
pa, pb = os.path.join(A, "TGLExt.lean"), os.path.join(B, "TGLExt.lean")
R["TGLExt.lean_agregador"] = {"k398c": sha(pa), "k399": sha(pb), "iguais": sha(pa) == sha(pb), "importa_Testemunho": b"Testemunho" in open(pb, "rb").read()}

b = open(UMPY, "rb").read()
R["nos_um_py"] = {"caminho": UMPY, "sha256": hashlib.sha256(b).hexdigest(), "sha16": hashlib.sha256(b).hexdigest()[:16], "bytes": len(b)}
json.dump(R, open(os.path.join(W, "conferencia_sandbox.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k != "modulos_citados"}, ensure_ascii=False, indent=1))
print("modulos iguais:", R["todos_modulos_iguais"], {k: v.get("iguais") for k, v in mods.items()})
