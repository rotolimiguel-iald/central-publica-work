# -*- coding: utf-8 -*-
r"""Commit separado das erratas da G1 feitas na custodia v410 (11/11/2026, claude-site-custodia), no molde de ferramentas(06/11) e (03/11):
pathspec explicito (so estes seis caminhos; o resto da arvore, alheio, nao entra), mensagem pelo portao de texto, push sem forca.
Sem --aplicar: so mostra."""
import subprocess
import sys

sys.path.insert(0, r"C:\IALD\Central de Patentes\tools")
from custodia_g1 import motor, textos, util  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402

APLICAR = "--aplicar" in sys.argv
ORD = r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_10nov_v410_atualize_e_publique_tudo_desassistido_verbatim.txt"
ctx = motor.Ctx(c=Caminhos({}), versao="v410", data=None, sessao="site", ordem=ORD, coautor="Claude Opus 5.5 <noreply@anthropic.com>", rede=True,
                publicar=True, ensaio=False, aceitar_molde=False, saida=None, anterior=None, ator="claude-site-custodia",
                trabalho=r"C:\IALD\Central de Patentes\work\custodia_v410_11nov")
cen = ctx.c.CEN
PATHS = [".gitignore", "tools/custodia_g1/fatos.py", "tools/custodia_g1/textos.py", "tools/custodia_g1/central.py",
         "tools/custodia_g1/generico/custodia_generica.py", "tools/custodia_g1/primordial.py"]
mod = set(util.git(cen, "diff", "HEAD", "--name-only", "--", *PATHS).splitlines())
assert mod == set(PATHS), ("os seis caminhos nao estao todos modificados", sorted(set(PATHS) - mod))
staged = util.git(cen, "diff", "--cached", "--name-only").splitlines()
print("ja no indice (ficam como estao, fora deste commit):", len(staged))
msg = ("ferramentas(11/11): erratas da custodia v410 na G1 - contratos de registro fora da escada (fatos.py e pedra generica, S11); "
       "CITATION aceita o sufixo de 08/11; C3 fora da faixa so com a declaracao da lista exata; C14 contra o HEAD; a chave abstract\n\n"
       "- fatos.py: contratos_de_registro - um contrato sem expected_ladder, literal Python e sem chave de conteudo de kernel (theorems, declarations,\n"
       "  declaration_sources, stone) e de REGISTRO (o pre-registro do teste H0DN e o recibo documental HMS13 da v410) e sai da conferencia da escada;\n"
       "  contrato de kernel sem a escada segue reprovando.\n"
       "- generico/custodia_generica.py (S11): a mesma regra em implementacao propria da pedra (nao importa fatos.py), e a pedra confere que a lista de\n"
       "  registro que ela acha e a declarada nos fatos. A copia instalada no runner (fronteira_tgl/runner) ja foi para o commit da custodia.\n"
       "- textos.py: a descricao do pino no CITATION.cff aceita o sufixo opcional ', the same pin' (registro do Zenodo da v409) e a troca grava a forma padrao.\n"
       "- central.py (C3): fora de +-50%% da cadeia de selo anterior, so segue com work/custodia_G1/decisoes/CADEIA_DE_SELO_FORA_DA_FAIXA_vNNN.json que\n"
       "  confira a contagem e o sha256 da lista exata de hoje; sem ela grava o candidato na pasta de trabalho e PARA. A guarda nao afrouxa.\n"
       "- central.py (C14): caminhos_a_commitar compara contra o HEAD; um C14 parado depois do git add deixava os proprios arquivos no indice e a\n"
       "  rodada seguinte os tomava por alheios (o complemento 2a371b331 levou os que tinham ficado).\n"
       "- primordial.py: a chave abstract -> ABSTRACT.md (a Abstract saiu do README pelo teto L01; saida ratificada pelo operador em 10/11).\n"
       "- .gitignore: os temporarios .tmp da cadeia de selo copiados para o cofre ficam no disco e fora do git.\n\n"
       "Suite --rapido da G1: 25 passam, 12 falham, 5 puladas - o mesmo placar de 03/11 (as falhas antigas da licao 42 mais t09).\n\n"
       "PROVADA = validade; a creditacao segue recusada; o gate nao se moveu.\n\n"
       "Co-Authored-By: %s\n") % ctx.coautor
viol = textos.portao(msg, set(textos.conhecidos_da_rodada(ctx)) | {"2a371b331"}, rotulo="commit")
assert not viol, viol
print(msg)
if not APLICAR:
    print("MODO SECO")
    sys.exit(0)
mp = ctx.W / "commit_ferramentas_g1_11nov.txt"
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
