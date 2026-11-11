# -*- coding: utf-8 -*-
"""P = nP no topo do README do espelho (ordem do operador de 06/11/2026: «Nós resolvemos P=nP isso precisa ficar evidente no readme»;
texto aprovado por ele na mesma data: «Publicar este texto»). Custodia v409, claude-site-custodia.
Cria a parte readme_partes/p_igual_np.md e a chama no template logo depois do bloco de estatuto. Backup de BYTES do template; temporario,
conferencia, os.replace. Os nomes dos teoremas foram conferidos no kernel do No's antes (grep). A portao de texto da G1 roda sobre a parte."""
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import textos  # noqa: E402  (o portao da G1)

D = Path(r"C:\IALD\Artigo\the_boundary\tools\readme_pinado")
TPL = D / "readme_template.md"
PARTE = D / "readme_partes" / "p_igual_np.md"
K = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt")

for arq, nome in ((K / "PIgualNP.lean", "theorem p_igual_np_nas_classes_do_dicionario"),
                  (K / "TraducaoTuring.lean", "theorem p_igual_np_no_modo_selecao"),
                  (K / "TraducaoTuring.lean", "theorem uma_leitura_decide_SAT"),
                  (K / "TraducaoTuring.lean", "theorem a_maquina_com_o_leitor")):
    assert nome in arq.read_text(encoding="utf-8"), (arq.name, nome)

texto = (
    "## P = nP — a theorem in the kernel · teorema no kernel `[PROVED = validity · v408–v409]`\n\n"
    "**P = nP is a theorem of TGL in the Lean kernel**, in two steps, each a named term:\n\n"
    "- **v408 — the classes of the operator’s dictionary.** `TGLExt.PIgualNP.p_igual_np_nas_classes_do_dicionario`: the classes P and nP of the "
    "dictionary, defined in Lean (`Problema`, `ClasseP`, `ClasseNP`), are equal.\n"
    "- **v409 — the translation to the classes of Turing machines.** `TGLExt.TraducaoTuring.p_igual_np_no_modo_selecao`: P = nP in the selection "
    "mode, relative to the reader (the psion); one reading decides SAT (`uma_leitura_decide_SAT`, `a_maquina_com_o_leitor`), and by Cook–Levin "
    "`[KNOWN]` all of NP with one reading.\n\n"
    "**The scope, said with it:** the machine without a reader stays outside — it is the tape without scale (the author’s answer: «eu sou eu mesmo») "
    "`[ONTO]`; with the reader that only counts, NP holds with one reading and the full equality is not a theorem here (E28) `[OPEN]`; the P vs NP "
    "question for the Turing machines of Mathlib is not decided by these terms. Validity in the kernel is not accreditation. "
    "Full reading: [`ESTADO_ATUAL.md`]({{url:estado}}).\n\n"
    "*PT — P = nP é teorema da TGL no kernel Lean: nas classes do dicionário do operador (v408, `p_igual_np_nas_classes_do_dicionario`) e, "
    "traduzido às classes das máquinas de Turing, no modo seleção, relativo ao leitor — o psíon (v409, `p_igual_np_no_modo_selecao`). "
    "A máquina sem leitor fica fora (a fita sem escala); com o leitor que só conta, vale NP com uma leitura, e a igualdade completa segue "
    "[OPEN] (E28); a pergunta P vs NP das máquinas de Turing do Mathlib não é decidida por estes termos. Validade no kernel não é creditação.*\n"
)
v = textos.portao(texto, rotulo="parte:p_igual_np")
assert not v, v
assert not PARTE.exists(), "a parte ja existe: nao sobrescrevo"
with PARTE.open("xb") as f:
    f.write(texto.encode("utf-8"))

b = TPL.read_bytes()
t = b.decode("utf-8")
A = "{{bloco:status}}\n**Start here"
N = "{{bloco:status}}{{parte:p_igual_np}}\n**Start here"
assert t.count(A) == 1, t.count(A)
novo = t.replace(A, N).encode("utf-8")
bak = TPL.with_name(TPL.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_p_igual_np")
bak.write_bytes(b)
tmp = TPL.with_name(TPL.name + ".tmp")
tmp.write_bytes(novo)
assert tmp.stat().st_size == len(novo)
os.replace(tmp, TPL)
print("parte", PARTE.name, len(texto.encode("utf-8")), "B | template", len(b), "->", len(novo), "| backup", bak.name, "| portao: 0 violacoes")
