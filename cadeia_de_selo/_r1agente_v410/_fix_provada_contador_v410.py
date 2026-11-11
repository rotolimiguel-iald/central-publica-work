# -*- coding: utf-8 -*-
"""_fix_provada_contador_v410.py -- (claude-construtor-v410, 06/11/2026) achado do fork A: o portao de textos do G1 (regra 2) exige o estatuto na MESMA frase da palavra de prova; nos textos da v410 a igualdade
relativizada com o contador era dita «nao esta' provada» sem o estatuto. Troca-se pela forma que a v409 ja' usava (FICA_ABERTO_IGUALDADE_COM_O_LEITOR: «NAO e' teorema aqui»), sem mudar o conteudo. Trocas com contagem exata."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v410 import aplicar
H = os.path.dirname(os.path.abspath(__file__))
aplicar(os.path.join(H, "delta_v410.py"), [
    ("a igualdade relativizada nao esta' provada para o contador)", "a igualdade relativizada nao e' teorema aqui para o contador)", 1),
    ("e a igualdade relativizada P^leitor = NP^leitor não está provada para o contador (E28)", "e a igualdade relativizada P^leitor = NP^leitor não é teorema aqui para o contador (E28)", 1),
    ("and the relativized equality P^reader = NP^reader is not proved for the counter (E28)", "and the relativized equality P^reader = NP^reader is not a theorem here for the counter (E28)", 1),
    ("e a igualdade relativizada nao esta' provada para o contador (E28)", "e a igualdade relativizada nao e' teorema aqui para o contador (E28)", 1),
    ("e a igualdade relativizada P^leitor = NP^leitor NAO esta' provada para o contador (E28)", "e a igualdade relativizada P^leitor = NP^leitor NAO e' teorema aqui para o contador (E28)", 1),
])
aplicar(os.path.join(H, "registros_v410.py"), [
    ("a igualdade relativizada nao esta' provada para o contador (E28)", "a igualdade relativizada nao e' teorema aqui para o contador (E28)", 1),
])
aplicar(os.path.join(H, "runtime_v410.py"), [
    ("a igualdade relativizada nao esta' provada\n# para o contador (E28)", "a igualdade relativizada nao e' teorema aqui\n# para o contador (E28)", 1),
])
