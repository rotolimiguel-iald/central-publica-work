# -*- coding: utf-8 -*-
"""Commit e push do espelho com o bloco P = nP no README (ordem e texto aprovados pelo operador em 06/11/2026: «Publicar este texto»).
Roda antes, com as funcoes da propria G1: as verificacoes do E09 (portas e guarda do selo) e as pre-condicoes do E10 (nada fora do indice,
nada sensivel staged). Commit com o trailer do coautor; push; confere HEAD == origin/main."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import espelho, motor  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402

TB = Path(r"C:\IALD\Artigo\the_boundary")
W = Path(r"C:\IALD\Central de Patentes\work\custodia_v409_06nov")
ctx = motor.Ctx(c=Caminhos({}), versao="v409", data=None, sessao="site",
                ordem=r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_05nov_energia_caiu_de_novo_continue_ate_v409_publicada_verbatim.txt",
                coautor="Claude Opus 5.5 <noreply@anthropic.com>", rede=True, publicar=True, ensaio=False, aceitar_molde=False, saida=None,
                anterior=None, ator="claude-site-custodia", trabalho=r"work\custodia_v409_06nov")
print("E09:", espelho._ap_e09(ctx))
pre = espelho._pre_e10(ctx)
if pre:
    sys.exit("pre-condicao do commit falhou: %s" % pre)
msg = W / "commit_espelho_v409_p_igual_np.txt"
msg.write_text(
    "custodia(v409): P = nP no topo do README - bloco proprio (teorema no kernel, v408-v409, com o alcance) e o BibTeX dos artigos em CITING.md\n\n"
    "Ordem do operador (06/11/2026): \"Nos resolvemos P=nP isso precisa ficar evidente no readme\"; texto aprovado por ele.\n"
    "P = nP: p_igual_np_nas_classes_do_dicionario (v408) e p_igual_np_no_modo_selecao (v409), relativo ao leitor; a maquina sem leitor fica fora;\n"
    "com o leitor que so conta, NP com uma leitura (E28, OPEN); P vs NP das maquinas de Turing do Mathlib nao decidido por estes termos.\n"
    "Validade no kernel nao e creditacao. O README pinado tem teto de 40.960 B (L01): o BibTeX saiu verbatim para CITING.md.\n\n"
    "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n", encoding="utf-8")


def git(*a, timeout=900):
    r = subprocess.run(["git", "-C", str(TB), *a], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        sys.exit("git %s falhou: %s" % (" ".join(a), (r.stderr or r.stdout)[-600:]))
    return r.stdout.strip()


git("commit", "-q", "-F", str(msg))
print("commit:", git("log", "-1", "--format=%h %s")[:140])
git("push", "origin", "main")
h, o = git("rev-parse", "HEAD"), git("rev-parse", "origin/main")
assert h == o, (h, o)
print("push ok: HEAD == origin/main", h[:8])
