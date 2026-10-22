# -*- coding: utf-8 -*-
"""SO PARA O ENSAIO: prepara <destino>\\conferir_rito_v384_ENSAIO.py = o conferir_rito_v384.py do pacote com UMA linha trocada (o NOS fixo vira
os.environ["V384_NOS"], que tem de ser um Nos SINTETICO), e copia byte a byte os arquivos que ele le de HERE (ESPERADOS_v384.json; o log do lancador
rito_servidor_v384.log e o rito_v384_sinal.txt, se existirem). Confere: as copias batem byte a byte; o diff contra o original e' exatamente uma linha.
A cadeia REAL nunca usa esta copia: ela copia o conferidor do pacote sem mudar um byte e o roda contra o Nos real.
uso: python preparar_conferidor_ensaio_v384.py <destino>"""
import hashlib, os, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import ambiente_v384 as A
dst = os.path.abspath(sys.argv[1])
assert dst.lower().startswith(HERE.lower() + os.sep), 'o destino tem de estar dentro de v384_selo'
os.makedirs(dst, exist_ok=True)
src = os.path.join(A.PK, 'conferir_rito_v384.py')
o = open(src, 'rb').read().decode('utf-8')
LINHA = 'NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")'
assert o.count(LINHA) == 1, 'a linha do NOS mudou no conferidor do pacote'
n = o.replace(LINHA, 'NOS = os.environ["V384_NOS"]; assert os.path.exists(os.path.join(NOS, "SINTETICO_ENSAIO_V384.txt")), "ENSAIO: so com o Nos SINTETICO"   # ENSAIO (unica linha trocada)')
dif = [(a, b) for a, b in zip(o.split('\n'), n.split('\n')) if a != b]
assert len(dif) == 1 and len(o.split('\n')) == len(n.split('\n'))
p = os.path.join(dst, 'conferir_rito_v384_ENSAIO.py')
open(p, 'wb').write(n.encode('utf-8'))
cop = []
for f in ('ESPERADOS_v384.json', 'rito_servidor_v384.log', 'rito_v384_sinal.txt'):
    s = os.path.join(A.PK, f)
    if os.path.exists(s):
        shutil.copyfile(s, os.path.join(dst, f)); assert open(s, 'rb').read() == open(os.path.join(dst, f), 'rb').read(); cop.append(f)
    elif os.path.exists(os.path.join(dst, f)):
        os.remove(os.path.join(dst, f))   # nada velho fica no lugar do que o pacote nao tem
print('conferidor de ENSAIO:', p, '| sha16 do original', hashlib.sha256(o.encode('utf-8')).hexdigest()[:16], '| linhas trocadas: 1 |', 'copias byte a byte:', cop)
