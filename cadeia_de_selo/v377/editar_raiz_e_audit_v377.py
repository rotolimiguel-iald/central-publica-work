# -*- coding: utf-8 -*-
"""editar_raiz_e_audit_v377.py -- no kernel CANDIDATO (../v376/kernel_src = o kernel da v376 selada + as duas pedras novas; NUNCA o canonico): + as pedras da
v377 na raiz TGLExt.lean e no topo do Audit, + #print axioms de todas as declaracoes das pedras. As pedras vem de PEDRAS_v377.json: [[arquivo, ns, n_decls], ...].
IDEMPOTENTE POR PEDRA. Grava AUDIT_NOMES_v377.json. O `sorry` e conferido FORA de comentarios; a prova definitiva e o build (extrair_axiomas_v377)."""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
KS = os.path.join(os.path.dirname(HERE), "v376", "kernel_src")
NOVAS = [tuple(x) for x in json.load(open(os.path.join(HERE, "PEDRAS_v377.json"), encoding="utf-8"))]


def rd(p): return open(p, "r", encoding="utf-8", newline="").read()


def wr(p, t):
    tmp = p + ".tmp"; open(tmp, "w", encoding="utf-8", newline="").write(t); os.replace(tmp, p)


def sem_comentarios(src):
    src = re.sub(r"/-.*?-/", "", src, flags=re.S)
    return re.sub(r"--[^\n]*", "", src)


decl = re.compile(r"^(?:theorem|lemma|def|noncomputable def|structure|abbrev)\s+([A-Za-z_][A-Za-z0-9_'.]*)", re.M)
nomes_path = os.path.join(HERE, "AUDIT_NOMES_v377.json")
nomes = json.load(open(nomes_path, encoding="utf-8")) if os.path.exists(nomes_path) else {}
root = os.path.join(KS, "TGLExt.lean"); t = rd(root)
assert t.count("import TGLExt.TheWholeIsOne") == 1, "a raiz nao e a da v376"
nl = "\r\n" if "\r\n" in t else "\n"
aud = os.path.join(KS, "TGL", "Audit.lean"); a = rd(aud)
nla = "\r\n" if "\r\n" in a else "\n"
add_root, add_aud_imp, add_prints, pulados = [], [], [], []
for f, ns, n in NOVAS:
    src = rd(os.path.join(KS, "TGLExt", f + ".lean"))
    assert "sorry" not in sem_comentarios(src), "sorry (fora de comentario) em " + f
    assert "axiom " not in sem_comentarios(src), "axiom em " + f
    found = [ns + x for x in decl.findall(src)]
    assert len(found) == n, (f, len(found), found)
    nomes[f] = found
    imp = "import TGLExt.%s" % f
    if imp in t:
        assert imp in a, "raiz tem %s mas o Audit nao" % f
        assert all(("#print axioms %s" % x) in a for x in found), "Audit sem os prints de " + f
        pulados.append(f); continue
    add_root.append(imp); add_aud_imp.append(imp); add_prints += found
todos = [x for f, _, _ in NOVAS for x in nomes[f]]
assert len(todos) == len(set(todos)), "nome repetido entre as pedras"
for x in add_prints:
    assert ("#print axioms %s" % x) not in a, "print ja presente: " + x
if add_root:
    t = t.rstrip("\r\n") + nl + "".join(i + nl for i in add_root)
    wr(root, t)
    k = a.index("import ")
    a = a[:k] + "".join(i + nla for i in add_aud_imp) + a[k:]
    a = a.rstrip("\r\n") + nla + ("-- 2026-09-30, v377 (ordens do operador: «pode rodar»; «essa lei chama-se dissipação [dephasing = lei do fluxo = vazamento]»; "
                               "«não precisa nomear como hipótese, vc consegue realizar a prova e cunhar»; «o leitor é a sombra»; «defina física»): %s (a gerencia; %d nomes)"
                               % (", ".join(f for f, _, _ in NOVAS if f not in pulados), len(add_prints))) + nla
    a += "".join("#print axioms %s%s" % (x, nla) for x in add_prints)
    wr(aud, a)
json.dump(nomes, open(nomes_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("raiz +%d imports; Audit +%d imports, +%d prints; pedras ja aplicadas puladas: %s; total de nomes v377: %d"
      % (len(add_root), len(add_aud_imp), len(add_prints), pulados or "nenhuma", len(todos)))
