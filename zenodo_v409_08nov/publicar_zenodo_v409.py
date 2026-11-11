# -*- coding: utf-8 -*-
"""Commit e push do espelho com o registro do deposito Zenodo da v409 (molde: commit 294e628c, zenodo(v401)). O operador depositou a v409 em 2026-11-08 e
avisou («publiquei a v409 no zenodo»). Roda antes, com as funcoes da propria G1, as verificacoes do E09 e as pre-condicoes do E10 (nada fora do indice,
nada sensivel staged). Confere HEAD == origin/main depois do push."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import espelho, motor  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402

TB = Path(r"C:\IALD\Artigo\the_boundary")
W = Path(r"C:\IALD\Central de Patentes\work\zenodo_v409_08nov")
ctx = motor.Ctx(c=Caminhos({}), versao="v409", data=None, sessao="site",
                ordem=r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_05nov_energia_caiu_de_novo_continue_ate_v409_publicada_verbatim.txt",
                coautor="Claude Sonnet 5.5 <noreply@anthropic.com>", rede=True, publicar=True, ensaio=False, aceitar_molde=False, saida=None,
                anterior=None, ator="claude-site-custodia", trabalho=r"work\custodia_v409_06nov")
print("E09:", espelho._ap_e09(ctx))
pre = espelho._pre_e10(ctx)
if pre:
    sys.exit("pre-condicao do commit falhou: %s" % pre)
msg = W / "commit_espelho_zenodo_v409.txt"
msg.write_text(
    "zenodo(v409): o deposito citavel passa a ser a v409 (10.5281/zenodo.24053883)\n\n"
    "O operador depositou a v409 no Zenodo em 08/11/2026. Os 15 arquivos do registro conferem por md5 com a API publica (lida e recalculada por script):\n"
    "13 com o Nos (um.py sha256 53284ba461ecd940..., o selo, o core, os artigos PT/EN, a forma canonica, o manifesto, o pilar quantico, o diario da\n"
    "linhagem, o desenho e a arvore da prova) e 2 portas da pasta Um (absoluto) - Grande Atrator (PORTA.md no commit 1c76ad4a; PORTA.json no 9036b439).\n"
    "CITATION.cff cita a v409 (a v401, 10.5281/zenodo.23649800, vira a versao anterior); ESTADO_ATUAL, portas, frente do README, read-brief, llms e as\n"
    "partes em secoes/ regeradas por script; o LEDGER ganha a entrada datada, so acrescimo. Um deposito e arquivo, nao creditacao; o gate nao se moveu.\n\n"
    "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>\n", encoding="utf-8")


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
