# -*- coding: utf-8 -*-
"""03/11/2026 15:2x, gerencia c1 (R2): o patch C19b do gerar_candidato_v407.py trocava so' um PREFIXO da linha do fock_face.reading da testemunha; por precedencia
(`A + B if C else D` == `(A + B) if C else D`) o prefixo «since v407 the lemma ... kept as record:» ficava so' no ramo com habitante. Aqui OLD_RD vira a LINHA INTEIRA da base
(lida do base_v406/um.py pelo prefixo atual, unica) e NEW_RD a linha inteira nova: `"reading": ((<prefixo> if _v407_elo_lido(kf_) else "") + (<IfExp antigo, verbatim>)),` -- o prefixo
envolve os dois ramos e a frase antiga e' o operando direito, igual no AST (e' o que o comparar R2 confere). As duas atribuicoes sao substituidas pelo segmento de fonte (ast), com repr.
Backup de bytes; py_compile. Escrito pelo Write."""
import ast, json, os, sys
sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import patches  # noqa: E402
V7 = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v407"
ARQ = os.path.join(V7, "gerar_candidato_v407.py")
src = open(ARQ, encoding="utf-8").read(); tree = ast.parse(src)
seg = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id in ("OLD_RD", "NEW_RD"):
        seg[node.targets[0].id] = (ast.get_source_segment(src, node), ast.literal_eval(node.value))
assert set(seg) == {"OLD_RD", "NEW_RD"}
old_prefix, new_prefix = seg["OLD_RD"][1], seg["NEW_RD"][1]
base = open(os.path.join(V7, "base_v406", "um.py"), encoding="utf-8").read().split("\n")
linhas = [l.rstrip("\r") for l in base if l.rstrip("\r").startswith(old_prefix)]
assert len(linhas) == 1, ("a linha do reading tem de ser unica na base", len(linhas))
OLD_LINE = linhas[0]
cab = '             "reading": ('
assert OLD_LINE.startswith(cab) and OLD_LINE.endswith("),"), OLD_LINE[:40] + " ... " + OLD_LINE[-10:]
inner_old = OLD_LINE[len(cab):-2]                      # `"the Fock face ..." if _hab406t_ else "..."`
assert inner_old.count(" if _hab406t_ else ") == 1
marca = ' + "the Fock face'
assert new_prefix.startswith(cab) and new_prefix.count(marca) == 1
prefix_expr = new_prefix[len(cab):new_prefix.index(marca)]   # `("since v407 ..." if _v407_elo_lido(kf_) else "")`
assert prefix_expr.startswith('("since v407 the lemma of the two faces') and prefix_expr.endswith(' if _v407_elo_lido(kf_) else "")'), prefix_expr[-60:]
NEW_LINE = cab + prefix_expr + " + (" + inner_old + ")),"
ast.parse("x = " + NEW_LINE.strip()[len('"reading": '):].rstrip(","))   # a expressao nova e' Python valido
print("OLD_LINE:", len(OLD_LINE), "B | NEW_LINE:", len(NEW_LINE), "B")


def f(s):
    o1, o2 = seg["OLD_RD"][0], seg["NEW_RD"][0]
    assert s.count(o1) == 1 and s.count(o2) == 1
    n1 = "OLD_RD = " + repr(OLD_LINE) + "   # [R2, 03/11] a LINHA INTEIRA da base (antes era so' o prefixo; a precedencia deixava o prefixo novo so' no ramo com habitante)"
    n2 = "NEW_RD = " + repr(NEW_LINE) + "   # [R2, 03/11] prefixo (quando o lema e' lido) + (o IfExp antigo, verbatim, como operando direito)"
    return s.replace(o1, n1).replace(o2, n2), ["OLD_RD linha inteira", "NEW_RD linha inteira"]


print(json.dumps(patches.aplicar_em_arquivo(ARQ, f, "r2_c19b_linha"), ensure_ascii=False)[:300])
