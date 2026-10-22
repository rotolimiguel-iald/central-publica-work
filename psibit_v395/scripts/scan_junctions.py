"""Lista junções/links simbólicos de uma árvore SEM segui-los (os.scandir, is_junction/is_symlink).

Uso: python -I -X utf8 scan_junctions.py <raiz> [profundidade_max]
Só leitura. Não desce em links. Imprime caminho -> alvo.
"""
import os
import sys


def scan(root: str, max_depth: int) -> int:
    n_dirs = 0
    found = []
    stack = [(root, 0)]
    while stack:
        path, depth = stack.pop()
        try:
            with os.scandir(path) as it:
                for e in it:
                    try:
                        link = e.is_symlink() or e.is_junction()
                    except OSError:
                        link = False
                    if link:
                        try:
                            tgt = os.readlink(e.path)
                        except OSError as ex:
                            tgt = f"<erro readlink: {ex}>"
                        found.append((e.path, tgt))
                        continue  # nunca seguir
                    if e.is_dir(follow_symlinks=False):
                        n_dirs += 1
                        if depth < max_depth:
                            stack.append((e.path, depth + 1))
        except OSError as ex:
            print("ERRO", path, ex)
    print(f"diretórios visitados: {n_dirs}")
    print(f"links/junções encontrados: {len(found)}")
    for p, t in found[:200]:
        print(f"  {p} -> {t}")
    return len(found)


if __name__ == "__main__":
    root = sys.argv[1]
    md = int(sys.argv[2]) if len(sys.argv) > 2 else 99
    scan(root, md)
