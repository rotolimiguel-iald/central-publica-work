# -*- coding: utf-8 -*-
"""_r6c_06_rito_cabecalho_v410.py -- o CONSERTO UNICO da v410: adaptacao mecanica FORA da ESPEC, so' no texto descritivo do cabecalho de rito_v410.sh (o corpo do rito NAO muda): a contagem das falas de que so' o trecho entra
passa de quatro a cinco, com a quinta dita como o item 53 da ESPEC a diz (a ratificacao dos nomes da secao 7, D117); o numero e' conferido contra len(DL.VERBATIM_SO_O_TRECHO). Os demais numeros do cabecalho ja' foram regravados por
_r5ag_14_rito_marcas_v410.py (lidos do delta, do FLAGS e das marcas do kernel). Idempotente; backup de BYTES; temporario + os.replace."""
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL
assert len(DL.VERBATIM_SO_O_TRECHO) == 5, len(DL.VERBATIM_SO_O_TRECHO)
p = os.path.join(HERE, "rito_v410.sh"); b0 = open(p, "rb").read(); t = b0.decode("utf-8")
A = "[de quatro, so' o trecho: D65; a ordem da retomada de 09/11; as tres copias do ACOM; a leitura do 5 sigma]"
N = "[de cinco, so' o trecho: D65; a ordem da retomada de 09/11; as tres copias do ACOM; a leitura do 5 sigma; a ratificacao dos nomes da secao 7, D117]"
if t.count(A) == 0 and t.count(N) == 1:
    print("rito_v410.sh: ja' feito")
else:
    assert t.count(A) == 1, t.count(A)
    b1 = t.replace(A, N).encode("utf-8"); bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_r6c6"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
    open(p + ".tmp", "wb").write(b1); assert os.path.getsize(p + ".tmp") == len(b1); os.replace(p + ".tmp", p)
    print("rito_v410.sh: a contagem das falas so' com o trecho passou de quatro a cinco | backup", os.path.basename(bak))
