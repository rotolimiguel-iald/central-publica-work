# -*- coding: utf-8 -*-
"""preparar_proposta2_d19c.py -- DELTA 19/10 (rodada d19c): prepara a PROPOSTA 2 para pos_rito\\textos_v394.py (NAO aplicada; so' escreve em delta_19out\\pos_rito_proposta2 e no .diff ao lado). Achado do harness dos textos:
`_num` diz «nenhum registro novo além dos cinco fixos» embora o candidato final tenha um SEXTO registro novo (criterio_binario_de_parada_v394); a causa e' `_extras`, que compara os registros novos do core com `V["reg_todos"]`
(os cinco fixos + os de ESPERADOS), em que o sexto ja' entra. A correcao de UMA linha compara com `V["reg394"]` (os cinco fixos): o sexto passa a ser dito pelo nome. Nada digitado: o nome vem do core/ESPERADOS.
uso: python -I -B -X utf8 preparar_proposta2_d19c.py"""
import difflib, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE)
ATUAL = os.path.join(V, "pos_rito", "textos_v394.py")
D = os.path.join(HERE, "pos_rito_proposta2"); os.makedirs(D, exist_ok=True)
raw = open(ATUAL, "rb").read(); s = raw.decode("utf-8")
VELHA = '    ex = [k for k in V["registros_novos"] if k not in V["reg_todos"]]\n'
NOVA = ('    # d19 (proposta 2): os registros novos ALEM DOS CINCO FIXOS (V["reg394"] tem so\' os cinco), ditos pelo nome: o sexto, criterio_binario_de_parada_v394, entra aqui\n'
        '    ex = [k for k in V["registros_novos"] if k not in V["reg394"]]\n')
assert s.count(VELHA) == 1, s.count(VELHA)
novo = s.replace(VELHA, NOVA)
open(os.path.join(D, "textos_v394.py.ANTES"), "wb").write(raw)
open(os.path.join(D, "textos_v394.py.PROPOSTA2"), "wb").write(novo.encode("utf-8"))
dif = list(difflib.unified_diff(s.splitlines(), novo.splitlines(), "pos_rito/textos_v394.py (ANTES, sha16 %s)" % hashlib.sha256(raw).hexdigest()[:16], "pos_rito/textos_v394.py (PROPOSTA2, sha16 %s)" % hashlib.sha256(novo.encode("utf-8")).hexdigest()[:16], lineterm="", n=3))
open(os.path.join(HERE, "pos_rito_PROPOSTA2_delta19.diff"), "w", encoding="utf-8", newline="\n").write("\n".join(dif) + "\n")
print("\n".join(dif))
