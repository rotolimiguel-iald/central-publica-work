# -*- coding: utf-8 -*-
r"""Commit separado da errata do timeout do C18 da G1 (11/11/2026, claude-site-custodia), no molde de commit_ferramentas_g1_11nov.py:
pathspec explicito (so tools/custodia_g1/publica.py; o resto da arvore, alheio, nao entra), mensagem pelo portao de texto, push sem forca.
Sem --aplicar: so mostra."""
import subprocess
import sys

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import motor, textos, util  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402

APLICAR = "--aplicar" in sys.argv
ORD = r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_11nov_central_publica_copia_vira_referencia_verbatim.txt"
ctx = motor.Ctx(c=Caminhos({}), versao="v410", data=None, sessao="site", ordem=ORD, coautor="Claude Opus 5.5 <noreply@anthropic.com>", rede=True,
                publicar=True, ensaio=False, aceitar_molde=False, saida=None, anterior=None, ator="claude-site-custodia",
                trabalho=r"C:\IALD\Central de Patentes\work\custodia_v410_11nov")
cen = ctx.c.CEN
PATHS = ["tools/custodia_g1/publica.py"]
mod = set(util.git(cen, "diff", "HEAD", "--name-only", "--", *PATHS).splitlines())
assert mod == set(PATHS), ("o caminho nao esta modificado", sorted(set(PATHS) - mod))
msg = ("ferramentas(11/11): C18 da G1 - o timeout da primeira chamada do encadeador sobe de 4 h para 8 h\n\n"
       "Na v410 a chamada ate subir_ensaio levou 14.322 s (work/central_publica_22out/rodadas/20261111_052005.json), 78 s abaixo do\n"
       "limite de 14.400 s. No timeout, util.rodar mata so o encadeador; o git push que ele abriu segue orfao e a tentativa seguinte\n"
       "o encontraria no meio. A v411 tambem traz o passo novo referenciar_copias (a copia vira referencia, decisao do operador de 11/11).\n\n"
       "PROVADA = validade; a creditacao segue recusada; o gate nao se moveu.\n\n"
       "Co-Authored-By: %s\n") % ctx.coautor
viol = textos.portao(msg, set(textos.conhecidos_da_rodada(ctx)), rotulo="commit")
assert not viol, viol
print(msg)
if not APLICAR:
    print("MODO SECO")
    sys.exit(0)
mp = ctx.W / "commit_ferramentas_g1_timeout_c18_11nov.txt"
util.escrever_atomico(mp, msg.encode("utf-8"), backup=True)
r = subprocess.run(["git", "-C", str(cen), "commit", "-q", "-F", str(mp), "--"] + PATHS, capture_output=True, text=True, encoding="utf-8", errors="replace")
assert r.returncode == 0, (r.stdout + r.stderr)[-600:]
h = util.git(cen, "rev-parse", "--short=9", "HEAD")
toc = util.git(cen, "show", "--name-only", "--format=", "HEAD").splitlines()
assert sorted(toc) == sorted(PATHS), toc
print("commit:", h, "|", len(toc), "caminhos")
p = util.rodar(["git", "-C", str(cen), "push", "origin", "main"], timeout=900)
assert p["rc"] == 0, p["saida"][-300:]
print("push ok:", util.git(cen, "rev-parse", "--short=9", "HEAD"), util.git(cen, "rev-parse", "--short=9", "origin/main"))
