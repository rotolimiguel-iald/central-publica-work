# -*- coding: utf-8 -*-
"""_adapt_gerar_relatorio_revisao_v407.py -- faz o gerar_relatorio_v407.py LER a revisao de terceiro quando ela existe e aprova ESTE candidato (aprovada true e candidato_sha16 igual): o texto «NAO foi revisado por terceiro» so' vale ate' a revisao existir.
Sem o arquivo, ou com aprovada falsa, ou com sha16 de outro candidato, o texto antigo (trava fechada) permanece. Troca exata, backup de bytes. Escrito por Write."""
import ast
import datetime
import os

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "gerar_relatorio_v407.py")
raw = open(P, "rb").read()
open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_rev", "wb").write(raw)
t = raw.decode("utf-8")
assert "REVISAO_OK" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n)
    t = t.replace(old, new)


ancora = '_vp = (CIT.get("varredura_das_pedras") or {})'
novo = '''_REV = tenta("revisao_terceiro/REVISAO_TERCEIRO_v407.json") or {}
REVISAO_OK = bool(_REV.get("aprovada") is True and _REV.get("candidato_sha16") == CM.get("sha16") and not _REV.get("n_alto") and not _REV.get("n_medio"))
if REVISAO_OK:   # a revisao de terceiro existe e aprova ESTE candidato: o texto «NAO foi revisado» deixa de valer; o aviso novo diz o que foi e o que NAO foi examinado (nada e' inventado: tudo lido do JSON da revisao)
    NAO_REVISADO = ("este candidato (o psion, o canto e o par, v407) FOI revisado por terceiro: %s, rodada %s, aprovada, %s ALTO, %s MEDIO, %s BAIXO (revisao_terceiro/REVISAO_TERCEIRO_v407.md, sha16 %s); quem constroi nao aprova: a aprovacao e' do revisor, nao desta preparacao; "
                    "as ressalvas BAIXAS estao escritas no caderno e valem como ditas (sem terceira rodada para BAIXO); a trava do orquestrador (S1b) confere aprovada e o sha16 do candidato" % (_REV.get("revisor"), _REV.get("rodada"), _REV.get("n_alto"), _REV.get("n_medio"), _REV.get("n_baixo"), h16("revisao_terceiro/REVISAO_TERCEIRO_v407.json")))
    AVISOS = [a_ for a_ in AVISOS if "ainda nao acontece" not in a_ and "esta preparacao NAO foi revisada por terceiro" not in a_]
    AVISOS.append("revisao de terceiro (Sonnet D47): " + NAO_REVISADO)
    AVISOS.append("ressalvas BAIXAS da revisao (nenhuma trava; ver o caderno): " + " | ".join("%s" % (a_.get("onde") or "")[:70] for a_ in (_REV.get("achados") or []) if a_.get("sev") == "BAIXO"))
_vp = (CIT.get("varredura_das_pedras") or {})'''
sub(ancora, novo)
sub('"trava_do_orquestrador": "S1b (pos_treino_v407): fechada ate\' revisao_terceiro/REVISAO_TERCEIRO_v407.json aprovar ESTE candidato (revisor: Sonnet); esta preparacao nao a abre"',
    '"trava_do_orquestrador": ("S1b (pos_treino_v407): ABERTA pela revisao_terceiro/REVISAO_TERCEIRO_v407.json (aprovada, mesmo sha16 do candidato); a preparacao nao a abriu: o revisor abriu" if REVISAO_OK else "S1b (pos_treino_v407): fechada ate\' revisao_terceiro/REVISAO_TERCEIRO_v407.json aprovar ESTE candidato (revisor: Sonnet); esta preparacao nao a abre"), "revisao_de_terceiro": ({"aprovada": _REV.get("aprovada"), "rodada": _REV.get("rodada"), "n_alto": _REV.get("n_alto"), "n_medio": _REV.get("n_medio"), "n_baixo": _REV.get("n_baixo"), "candidato_sha16": _REV.get("candidato_sha16"), "sha16_do_json": h16("revisao_terceiro/REVISAO_TERCEIRO_v407.json"), "revisor": _REV.get("revisor"), "quando": _REV.get("quando")} if REVISAO_OK else None)')
ast.parse(t)
open(P, "wb").write(t.encode("utf-8"))
print("ok")
