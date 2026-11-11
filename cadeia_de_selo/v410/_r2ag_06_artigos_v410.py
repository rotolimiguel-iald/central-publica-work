# -*- coding: utf-8 -*-
"""_r2ag_06_artigos_v410.py -- R2 (D99; M e B3 e B4): os snippets do artigo PT/EN: a clausula EXATA do ADENDO 4 ao lado de «a decisao em tempo finito do ciclo, linear nos bits» (a formula em modo matematico, o resto pelo mesmo escape do snippet), Z(s) DEFINIDA na primeira
ocorrencia do artigo (a secao da IALD2), a ressalva dos seis nomes, o item do Tetelestai (o limiar; «passos = ciclo» e' leitura do dicionario [INPUT]), a costura do tempo ([INPUT/dicionario] e maiuscula) e a regra do poder do teste da razao de Hubble etiquetada [INPUT, D96]."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _r2ag_lib_v410 import aplicar

HELPER = '''    _ca410 = _V410_AESCALA_CONTRACT
    _zx410 = {"Z(s) = Σ_x e^(−s·c(x))": r"$Z(s)=\\sum_x e^{-s\\cdot c(x)}$", "2^n": r"$2^n$", "n·ln 2": r"$n\\cdot\\ln 2$"}   # (R2, D99: a clausula do ADENDO 4, lida do contrato; a formula vai em modo matematico, o resto pelo mesmo escape do snippet; nada de Unicode cru fora do que o pdflatex aceita)
    _zl410 = lambda t_: "".join((_zx410[p_] if p_ in _zx410 else _ta410(p_)) for p_ in re.split("(" + "|".join(re.escape(k_) for k_ in _zx410) + ")", t_))
'''

# ---------------- PT
T = [("    _ca410 = _V410_AESCALA_CONTRACT\n", HELPER, 1),
     ('''foram ratificados por ele: «ratifico tudo». Os " + str(_ca410["n_nomes_novos"])''',
      '''foram ratificados por ele: «ratifico tudo». Ressalva: " + _ta410(_ca410["frase_seis_nomes_pt"]) + r". Os " + str(_ca410["n_nomes_novos"])''', 1),
     (r'''os passos são o ciclo até o Tetelestai (\texttt{os\_passos\_sao\_o\_ciclo\_ate\_o\_tetelestai}): "''',
      r'''o limiar do Tetelestai (\texttt{os\_passos\_sao\_o\_ciclo\_ate\_o\_tetelestai}): "''', 1),
     (r'''e, sem solução, $Z(s)<1$, a decisão em tempo finito do ciclo, linear nos bits; a mentira lida''',
      r'''e, sem solução, $Z(s)<1$: $Z(s)$ separa o sim do não, a decisão em tempo finito do ciclo, linear nos bits (" + _zl410(_ca410["clausula_z_pt"]) + r"); que os passos sejam o ciclo até o Tetelestai é a leitura do dicionário \textsf{[INPUT]}; a mentira lida''', 1),
     (r'''\textbf{O tempo.} " + _ta410(_ca410["frase_tempo_pt"]) + r". "''',
      r'''\textbf{O tempo.} \textsf{[INPUT/dicionário]} " + _ta410(_ca410["frase_tempo_pt_costurada"]) + r". "''', 1)]
aplicar("artigo_pt_aescala_v410.pysnip", T, parse=False)

# ---------------- EN
T = [("    _ca410 = _V410_AESCALA_CONTRACT\n", HELPER, 1),
     ('''were ratified by him (our translation: I ratify everything). The " + str(_ca410["n_nomes_novos"])''',
      '''were ratified by him (our translation: I ratify everything). Caveat: " + _ta410(_ca410["frase_seis_nomes_en"]) + r". The " + str(_ca410["n_nomes_novos"])''', 1),
     (r'''the steps are the cycle up to the Tetelestai (\texttt{os\_passos\_sao\_o\_ciclo\_ate\_o\_tetelestai}): "''',
      r'''the threshold of the Tetelestai (\texttt{os\_passos\_sao\_o\_ciclo\_ate\_o\_tetelestai}): "''', 1),
     (r'''and, without a solution, $Z(s)<1$, the decision in finite time of the cycle, linear in the bits; a lie read as a lie is truth''',
      r'''and, without a solution, $Z(s)<1$: $Z(s)$ separates the yes from the no, the decision in finite time of the cycle, linear in the bits (" + _zl410(_ca410["clausula_z_en"]) + r"); that the steps are the cycle up to the Tetelestai is the dictionary's reading \textsf{[INPUT]}; a lie read as a lie is truth''', 1),
     (r'''\textbf{Time.} " + _ta410(_ca410["frase_tempo_en"]) + r". "''',
      r'''\textbf{Time.} \textsf{[INPUT/dicionário]} " + _ta410(_ca410["frase_tempo_en_costurada"]) + r". "''', 1)]
aplicar("artigo_en_aescala_v410.pysnip", T, parse=False)

# ---------------- a definicao de Z(s) na PRIMEIRA ocorrencia do artigo (a secao da IALD2, que vem antes da A Escala)
aplicar("artigo_pt_v410.pysnip", [(r'''que lê a trava da fórmula inscrita como $Z(s)/2^n$ (\texttt{o\_algoritmo\_iald})''',
                                   r'''que lê a trava da fórmula inscrita como $Z(s)/2^n$, com $Z(s)=\sum_x e^{-s\cdot c(x)}$ a função de partição do hamiltoniano oculto (a soma, sobre os $2^n$ pixels, dos pesos de Boltzmann do custo $c$) (\texttt{o\_algoritmo\_iald})''', 1)], parse=False)
aplicar("artigo_en_v410.pysnip", [(r'''which reads the lock of the inscribed formula as $Z(s)/2^n$ (\texttt{o\_algoritmo\_iald})''',
                                   r'''which reads the lock of the inscribed formula as $Z(s)/2^n$, with $Z(s)=\sum_x e^{-s\cdot c(x)}$ the partition function of the hidden Hamiltonian (the sum, over the $2^n$ pixels, of the Boltzmann weights of the cost $c$) (\texttt{o\_algoritmo\_iald})''', 1)], parse=False)

# ---------------- B4(c): a regra do poder do teste da razao de Hubble e' [INPUT, D96], nao [REAL]
aplicar("artigo_pt_h0dn_v410.pysnip", [(r'''\textsf{[REAL]} " + _th410(_V410_H0DN_CONTRACT["frase_poder_pt"])''', r'''\textsf{[INPUT, D96]} " + _th410(_V410_H0DN_CONTRACT["frase_poder_pt"])''', 1)], parse=False)
aplicar("artigo_en_h0dn_v410.pysnip", [(r'''\textsf{[REAL]} " + _th410(_V410_H0DN_CONTRACT["frase_poder_en"])''', r'''\textsf{[INPUT, D96]} " + _th410(_V410_H0DN_CONTRACT["frase_poder_en"])''', 1)], parse=False)
