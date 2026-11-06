# -*- coding: utf-8 -*-
"""_adapt_relatorio_v409_b.py -- (claude-construtor-v409, 05/11/2026) dois avisos a mais no gerar_relatorio_v409.py, ditos: (1) o fim_de_cadeia_v409.sh parou no passo 2 porque o p00 do B(n) deu
NENHUMA FALHA com 1 PENDENTE (o pino do memoria.py, ato da gerencia) e o script exige TODAS PASSARAM; os passos 3 a 7 rodaram a mao com os MESMOS comandos (fim_de_cadeia_passos3a7_out_v409.txt);
(2) o conferidor do servico (conferir_exigencias_servico_v409.py) so' lia o AUT do orquestrador como literal, e o AUT da v409 e' montado do delta: corrigido na causa (a expressao avaliada com o delta; a checagem e' a mesma)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("gerar_relatorio_v409.py")
a.troca('''    "duas outras causas do ensaio corrigidas na fonte (nenhum teste relaxado):''', '''    "o fim_de_cadeia_v409.sh PAROU no passo 2 (B(n) pre-selo: RC_BN=0, BATERIA_PASSA, producao intacta) porque o p00 que ele roda deu NENHUMA FALHA com 1 PENDENTE (o pino do memoria.py, PINO_MEMORIA_PY_v409.json, ato da gerencia) e o script exige TODAS PASSARAM; os passos 3 a 7 (servico estatico, derivacao do pos-rito, os dois harnesses, a previa do X) rodaram a mao com os MESMOS comandos do script (saida em fim_de_cadeia_passos3a7_out_v409.txt); o script nao foi mudado",
    "o conferidor do servico da Bancada (bancada_B3_servico/conferir_exigencias_servico_v409.py) so' lia o AUT do orquestrador como literal; o AUT da v409 e' MONTADO do delta (o prefixo de sha16 da ordem e a frase): corrigido na causa (so' a expressao do AUT e' avaliada, com o delta desta pasta, sem builtins); a checagem seguinte e' a mesma (o sha16 CALCULADO do arquivo da fala esta' no AUT); 37/37 e o controle negativo pegou toda mutacao",
    "duas outras causas do ensaio corrigidas na fonte (nenhum teste relaxado):''')
a.grava()
