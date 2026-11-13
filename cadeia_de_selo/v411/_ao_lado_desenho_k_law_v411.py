# -*- coding: utf-8 -*-
"""_ao_lado_desenho_k_law_v411.py -- acrescenta AO LADO, no FIM do DESENHO_v411.md (so' acrescimo; backup de BYTES antes; CRLF respeitado), as decisoes da gerencia c1 de 12/11/2026 sobre os desvios da Etapa 1, escritas pelo
claude-construtor-v411 em nome proprio (registro), a pedido da gerencia. Idempotente: se o marcador ja' estiver, nao acrescenta. uso: python -B -X utf8 _ao_lado_desenho_k_law_v411.py"""
import datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "DESENHO_v411.md")
MARCA = "<!-- ao_lado_decisoes_etapa1_12nov -->"
b = open(P, "rb").read()
if MARCA.encode("utf-8") in b:
    print("ja' registrado"); raise SystemExit(0)
txt = ("\r\n\r\n## AO LADO (12/11/2026, claude-construtor-v411, em nome proprio; registro das decisoes da gerencia c1 sobre os desvios da Etapa 1) " + MARCA + "\r\n\r\n"
       "- **(a) O veredito de maquina:** a faixa de |Z contra K| ganha o PREFIXO FIXO `K_LAW_`, para a frase se ler sozinha: `...AGAINST_THE_NULL__K_LAW_CONSISTENT_WITHIN_1SIGMA__BRANCH_4...`. O texto da faixa continua LIDO do literal "
       "(`RAMOS_V411.json`); so' o prefixo e' fixo. A secao 2 (o molde do meio) fica como esta: o prefixo entra antes do marcador da faixa.\r\n"
       "- **(b)** F54 fora; da F56 sai so' “o teste aberto / a abertura feita”; F60 a F67: aprovado.\r\n"
       "- **(c) A P18 e a cabeca do teste:** excecao ESTREITA: uma funcao so', usada por todos os conferidores; ela retira apenas a cadeia EXATA que a c7 monta do literal; controle negativo: uma cabeca com um caractere trocado NAO e' retirada "
       "e a P18 recusa; a excecao fica dita no relatorio e na NOTA do handoff a custodia.\r\n"
       "- **(d)** o resumo do que o teste nao decide: aprovado. **(e)** as traducoes EN ficam, marcadas para a revisao. **(g)** a tolerancia segue 1e-9; o 0,0 medido e' relatado.\r\n")
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(bak, "wb").write(b); assert open(bak, "rb").read() == b
novo = b + txt.encode("utf-8")
open(P + ".tmp", "wb").write(novo); assert os.path.getsize(P + ".tmp") == len(novo); os.replace(P + ".tmp", P)
assert os.path.getsize(P) > len(b) and open(P, "rb").read().startswith(b)
print("AO LADO acrescentado | backup", os.path.basename(bak), "|", len(b), "->", len(novo), "B")
