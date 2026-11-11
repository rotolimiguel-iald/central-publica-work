# -*- coding: utf-8 -*-
r"""Commit complementar da custodia v410 na Central (11/11/2026, claude-site-custodia): os arquivos da propria custodia que o C14 deixou no indice
(rodada 7 parou depois do `git add`; rodada 8 os tomou por alheios). Usa as funcoes da G1: caminhos_a_commitar (ja com a errata contra o HEAD),
o portao de texto, commitar_so_a_lista (pathspec explicito, lista negra, nada fora da lista) e o push. Sem --aplicar: so mostra a lista."""
import sys
from pathlib import Path

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import central, motor, textos, util  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402

APLICAR = "--aplicar" in sys.argv
ORD = r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_10nov_v410_atualize_e_publique_tudo_desassistido_verbatim.txt"
ctx = motor.Ctx(c=Caminhos({}), versao="v410", data=None, sessao="site", ordem=ORD, coautor="Claude Opus 5.5 <noreply@anthropic.com>", rede=True,
                publicar=True, ensaio=False, aceitar_molde=False, saida=None, anterior=None, ator="claude-site-custodia",
                trabalho=r"C:\IALD\Central de Patentes\work\custodia_v410_11nov")
cen = ctx.c.CEN
ps, notas = central.caminhos_a_commitar(ctx)
staged = util.git(cen, "diff", "--cached", "--name-only").splitlines()
no_escopo = [x for x in staged if central._no_escopo(x, ps)]
fora = [x for x in staged if not central._no_escopo(x, ps)]
print("lista de permissao: %d caminhos | no indice e no escopo: %d | no indice e fora do escopo: %d | notas: %s" % (len(ps), len(no_escopo), len(fora), notas))
print("  Atlas no escopo:", "memory/TGL_ATLAS.md" in ps, "| patents no escopo:", sum(1 for x in no_escopo if x.startswith("patents/")))
assert not fora, fora[:10]
assert not [x for x in no_escopo if central.LISTA_NEGRA.search(x)]
anterior = central._commit_central(ctx)
msg = ("custodia(v410): complemento - resultados e selos dos 16 dispositivos de 11/11 e o Atlas (so acrescimo)\n\n"
       "O commit anterior da custodia (%s) deixou estes %d arquivos no indice: a rodada 7 do C14 fez git add e parou na lista negra\n"
       "(um temporario .tmp da cadeia de selo copiado para o cofre); a rodada 8 nao os via (git diff contra o indice) e os preservou\n"
       "como alheios. Errata ao lado no G1: caminhos_a_commitar compara contra o HEAD. O .tmp fica no cofre em disco e fora do git.\n\n"
       "PROVADA = validade; a creditacao segue recusada; o gate nao se moveu.\n\nCo-Authored-By: %s\n") % (anterior[:9], len(no_escopo), ctx.coautor)
viol = textos.portao(msg, set(textos.conhecidos_da_rodada(ctx)) | {anterior[:9], anterior[:8], anterior}, rotulo="commit")
assert not viol, viol
print(msg)
if not APLICAR:
    print("MODO SECO")
    sys.exit(0)
mp = ctx.W / "commit_central_v410_complemento.txt"
util.escrever_atomico(mp, msg.encode("utf-8"), backup=True)
cm = central.commitar_so_a_lista(cen, ps, mp, ctx.W)
print("commit:", cm["commit"], "| alheios preservados:", len(cm["alheios_preservados"]))
p = util.rodar(["git", "-C", str(cen), "push", "origin", "main"], timeout=900)
assert p["rc"] == 0, p["saida"][-300:]
print("push ok:", util.git(cen, "rev-parse", "--short", "HEAD"), util.git(cen, "rev-parse", "--short", "origin/main"))
