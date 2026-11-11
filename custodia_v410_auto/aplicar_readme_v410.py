# -*- coding: utf-8 -*-
"""Aplica ao README pinado do espelho os dois blocos do handoff da v410 (ordem do operador de 09/11: o Clay, a AEscala e o H0DN evidentes no README;
convencoes combinadas com a gerencia c1 em 10/11):
  <!-- INICIO_README_FRENTE_v410 --> ... <!-- FIM_README_FRENTE_v410 -->     -> conteudo novo de readme_partes/p_igual_np.md (EN e PT; {{url:estado}})
  <!-- INICIO_README_O_QUE_SAI_v410 --> ... <!-- FIM_README_O_QUE_SAI_v410 --> -> a linha-ponteiro (com {{url:abstract}}) no lugar de {{parte:abstract}}
                                                                               e da nota «Read the Abstract below under the current ruler» do template
A Abstract (readme_partes/abstract.md) sai VERBATIM para ABSTRACT.md na raiz do espelho, com a nota em cima (nada se corta); o primordial.py ganha a
chave «abstract» (URL gerada a partir das portas). Confere: um bloco de cada; README_FRENTE <= 4.600 B; so os marcadores esperados; o portao da G1.
Backups de BYTES; temporario, conferencia, os.replace. Sem --aplicar: modo seco (mostra o que faria). --handoff ARQ e --espelho DIR para ensaio."""
import argparse
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import textos  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--handoff", default=r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\HANDOFF_v410_CUSTODIA.md")
ap.add_argument("--espelho", default=r"C:\IALD\Artigo\the_boundary")
ap.add_argument("--primordial", default=r"C:\IALD\Central de Patentes\tools\custodia_g1\primordial.py")
ap.add_argument("--aplicar", action="store_true")
a = ap.parse_args()
TB = Path(a.espelho)
D = TB / "tools" / "readme_pinado"
TPL, PARTE, ABS_P, ABS_RAIZ, PRIM = D / "readme_template.md", D / "readme_partes" / "p_igual_np.md", D / "readme_partes" / "abstract.md", TB / "ABSTRACT.md", Path(a.primordial)
LIMITE = 4600

h = Path(a.handoff).read_text(encoding="utf-8")


def bloco(nome):
    rx = re.compile(r"<!--\s*INICIO_%s_v410\s*-->\s*\n(.*?)\n\s*<!--\s*FIM_%s_v410\s*-->" % (nome, nome), re.S)
    ms = rx.findall(h)
    assert len(ms) == 1, ("o bloco %s nao aparece exatamente uma vez no handoff" % nome, len(ms))
    return ms[0].strip("\n") + "\n"


frente, sai_bloco = bloco("README_FRENTE"), bloco("README_O_QUE_SAI")
nb = len(frente.encode("utf-8"))
assert nb <= LIMITE, "README_FRENTE com %d B (limite %d)" % (nb, LIMITE)
assert set(re.findall(r"\{\{[^{}]*\}\}", frente)) <= {"{{url:estado}}"}, re.findall(r"\{\{[^{}]*\}\}", frente)
# AO LADO (11/11, custodia v410): o bloco do handoff traz um preambulo de instrucoes da c1 e, depois, a linha-ponteiro pronta
# («vai da linha `## Abstract` ate o fim deste bloco»). So esse trecho entra no README; o preambulo e instrucao, nao texto publicado.
ms_abs = list(re.finditer(r"^## Abstract[ \t]*$", sai_bloco, re.M))
assert len(ms_abs) == 1, ("a linha «## Abstract» nao aparece exatamente uma vez no README_O_QUE_SAI", len(ms_abs))
sai = sai_bloco[ms_abs[0].start():]
assert re.findall(r"\{\{[^{}]*\}\}", sai) == ["{{url:abstract}}"], re.findall(r"\{\{[^{}]*\}\}", sai)
assert sai.lstrip().startswith("## Abstract"), "o README_O_QUE_SAI deve comecar na linha «## Abstract»"
conhecidos = set(re.findall(r"\b[0-9a-f]{16}\b|\b[0-9a-f]{64}\b", h))      # o portao do S6d ja rodou sobre o handoff inteiro
v = textos.portao(frente, conhecidos, rotulo="README_FRENTE_v410") + textos.portao(sai_bloco, conhecidos, rotulo="README_O_QUE_SAI_v410")
assert not v, v

t = TPL.read_text(encoding="utf-8")
m_nota = re.search(r"^> \*\*Read the Abstract below under the current ruler\.\*\*[^\n]*\n", t, re.M)
assert m_nota, "a nota «Read the Abstract below» nao esta no template"
nota = m_nota.group(0)
alvo = nota + "{{parte:abstract}}"
assert t.count(alvo) == 1, ("nota + {{parte:abstract}} nao encontrados juntos uma vez", t.count(alvo))
t_novo = t.replace(alvo, sai.rstrip("\n") + "\n\n", 1)
assert "{{parte:abstract}}" not in t_novo and "Read the Abstract below" not in t_novo

abs_txt = ABS_P.read_text(encoding="utf-8")
assert "{{" not in abs_txt, "a parte abstract tem marcador do molde: nao pode virar arquivo estatico"
raiz_txt = ("# Abstract · resumo\n\n" + nota + "\n" + abs_txt.rstrip("\n") + "\n\n"
            "*(Moved verbatim from the README on the custody of v410, to keep the README under 40.960 bytes; the README points here.)*\n")
assert abs_txt.strip("\n") in raiz_txt

p = PRIM.read_text(encoding="utf-8")
CH_A = '        "citing": "CITING.md",'
CH_N = CH_A + '\n        "abstract": "ABSTRACT.md",   # AO LADO (v410, custodia): a Abstract saiu do README (teto L01) para ABSTRACT.md'
ja_tem = '"abstract": "ABSTRACT.md"' in p
assert ja_tem or p.count(CH_A) == 1, "a chave citing nao esta no primordial.py: rever"
p_novo = p if ja_tem else p.replace(CH_A, CH_N, 1)

print("README_FRENTE: %d B (limite %d) | README_O_QUE_SAI: %d B | portao: 0 violacoes" % (nb, LIMITE, len(sai.encode("utf-8"))))
print("template: %d -> %d B | ABSTRACT.md: %d B | primordial.py: %s" % (len(t.encode()), len(t_novo.encode()), len(raiz_txt.encode()), "ja tinha a chave" if ja_tem else "ganha a chave abstract"))
if not a.aplicar:
    print("MODO SECO: nada foi escrito")
    sys.exit(0)
ts = time.strftime("%Y%m%d_%H%M%S")


def troca(path, novo, rot):
    b = path.read_bytes()
    path.with_name(path.name + ".bak_" + ts + "_" + rot).write_bytes(b)
    nbts = novo.encode("utf-8")
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(nbts)
    assert tmp.stat().st_size == len(nbts)
    os.replace(tmp, path)


troca(PARTE, frente, "readme_frente_v410")
troca(TPL, t_novo, "abstract_sai_v410")
if not ja_tem:
    troca(PRIM, p_novo, "chave_abstract_v410")
assert not ABS_RAIZ.exists(), "ABSTRACT.md ja existe: nao sobrescrevo"
with ABS_RAIZ.open("xb") as f:
    f.write(raiz_txt.encode("utf-8"))
print("aplicado: p_igual_np.md, readme_template.md, primordial.py, ABSTRACT.md (a parte abstract.md fica no disco, sem chamada no template)")
