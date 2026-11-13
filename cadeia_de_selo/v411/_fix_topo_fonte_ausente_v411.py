# -*- coding: utf-8 -*-
"""_fix_topo_fonte_ausente_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado do ensaio a seco do CANDIDATO real (16871a350670d80c): na VARIANTE herdada da v410 sem o
registro teste_de_veracidade_fase9_v397 (o artigo tem de compilar e dizer «NÃO selou»), o topo ratificado levanta ValueError (⟨z_disc⟩ <- teste_de_veracidade_fase9_v397.lido.z_disc_calibrado ausente) e DERRUBA o
build_pt inteiro: um registro que nao grava faria o rito perder o artigo. A causa: a fonte AUSENTE no core era tratada como erro de emissao. O conserto (contido no _v411_topo_texto): fonte AUSENTE (None) => o topo NAO
diz o resultado e diz por que, visivel (o mesmo padrao de quando o registro do H0DN nao sela); valor PRESENTE mas nao numerico ou nao finito, marcador que sobra no texto e o livro de cobrancas que nao sustenta a frase seguem
PARAR (ValueError), como a gerencia escreveu. Backup de BYTES antes; ancora unica; ast.parse. uso: python -B -X utf8 _fix_topo_fonte_ausente_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "quadro_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
a = ('        if isinstance(x_, bool) or not isinstance(x_, (int, float)) or x_ != x_ or x_ in (float("inf"), float("-inf")):\n'
     '            raise ValueError("marcador do topo sem fonte resolvida no core (%s <- %s): PARAR" % (mk_, ".".join(d_["caminho"])))\n')
n = ('        if x_ is None:   # (fonte AUSENTE: um registro nao gravou nesta rodada) o topo NAO diz o resultado e diz por que, visivel, sem derrubar o artigo (o padrao de quando o registro do H0DN nao sela)\n'
     '            return ((r"\\textbf{O texto do topo não é dito nesta rodada: a fonte de um marcador (\\texttt{%s}) não está no core.} " if lang_ == "pt" else r"\\textbf{The top text is not stated this round: the source of a marker (\\texttt{%s}) is not in the core.} ")\n'
     '                    % _v411_tt(".".join(d_["caminho"]))) if tex_ else ""\n'
     '        if isinstance(x_, bool) or not isinstance(x_, (int, float)) or x_ != x_ or x_ in (float("inf"), float("-inf")):   # (valor PRESENTE mas nao numerico ou nao finito: PARAR)\n'
     '            raise ValueError("marcador do topo sem fonte resolvida no core (%s <- %s): PARAR" % (mk_, ".".join(d_["caminho"])))\n')
assert t.count(a) == 1, t.count(a)
t = t.replace(a, n); ast.parse(t)
t = t.replace("Marcador sem fonte resolvida, numero nao finito ou marcador que sobre no texto = PARAR (ValueError).", "Marcador com fonte AUSENTE no core => o topo nao diz o resultado e diz por que (visivel; fork C, 12/11); numero nao finito ou nao numerico, ou marcador que sobre no texto = PARAR (ValueError).", 1)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc_real"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
