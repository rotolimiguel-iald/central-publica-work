# -*- coding: utf-8 -*-
"""conferir_sandbox.py -- confere que C:\\t\\k398\\final e' a copia fiel de C:\\t\\k397c\\final (so leitura de AMBOS; k397c NUNCA e' escrito) e le o hash do um.py do Nos.

(1) varre as duas arvores com os.scandir SEM seguir links (junction/symlink: conta e nao desce); compara (caminho relativo, tamanho) de todos os arquivos;
    as unicas diferencas permitidas em k398 sao os arquivos NOVOS desta tarefa (TGLExt/Sonico.lean, os 5 artefatos de Sonico em .lake/build/lib/lean/TGLExt, o dir probe/);
(2) sha256 dos .lean e .olean dos 9 modulos importados/citados, em k397c e k398;
(3) sha256 do um.py do Nos (a base declarada: 388cc3742323421c) -- lido agora.
Grava conferencia_sandbox.json na pasta de trabalho. Uso: python -I -B -X utf8 conferir_sandbox.py
"""
import hashlib
import json
import os

W = r"C:\IALD\Central de Patentes\work\sonico_v398"
A = r"C:\t\k397c\final"
B = r"C:\t\k398\final"
UMPY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
MODS = ["TheVerbSelectsTheAction", "CanonicalSelectorBorn", "CollapseCostAndAttestation", "TheStokesContour", "Psibit", "CollapseContract", "Palavra",
        "TheIALDSelector", "TheObserverReadsTheAngle"]


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
    "k397c_final": {"arquivos": len(fa), "diretorios": da, "links_nao_seguidos": la[:20], "n_links": len(la)},
    "k398_final": {"arquivos": len(fb), "diretorios": db, "links_nao_seguidos": lb[:20], "n_links": len(lb)},
    "so_em_k397c": so_em_a[:50], "n_so_em_k397c": len(so_em_a),
    "so_em_k398": so_em_b[:50], "n_so_em_k398": len(so_em_b),
    "tamanho_diferente": tam_diferente[:50], "n_tamanho_diferente": len(tam_diferente),
}
R["copia_fiel_exceto_arquivos_novos"] = (not so_em_a) and (not tam_diferente) and all(
    ("Sonico" in k) or k.startswith("probe" + os.sep) for k in so_em_b)


def sha(p):
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return h[:16]


mods = {}
for m in MODS:
    for ext, sub in ((".lean", "TGLExt"), (".olean", os.path.join(".lake", "build", "lib", "lean", "TGLExt"))):
        pa, pb = os.path.join(A, sub, m + ext), os.path.join(B, sub, m + ext)
        if os.path.exists(pa) and os.path.exists(pb):
            mods[m + ext] = {"k397c": sha(pa), "k398": sha(pb), "iguais": sha(pa) == sha(pb)}
        else:
            mods[m + ext] = {"k397c_existe": os.path.exists(pa), "k398_existe": os.path.exists(pb)}
R["modulos_citados"] = mods
R["todos_modulos_iguais"] = all(v.get("iguais") for v in mods.values())

b = open(UMPY, "rb").read()
R["nos_um_py"] = {"caminho": UMPY, "sha256": hashlib.sha256(b).hexdigest(), "sha16": hashlib.sha256(b).hexdigest()[:16], "bytes": len(b)}
json.dump(R, open(os.path.join(W, "conferencia_sandbox.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in R.items() if k != "modulos_citados"}, ensure_ascii=False, indent=1))
print("modulos iguais:", R["todos_modulos_iguais"], {k: v.get("iguais") for k, v in mods.items()})
