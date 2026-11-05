# -*- coding: utf-8 -*-
"""_adapt_forkB_x_post_v408.py -- (claude-construtor-v408, fork B, 04/11/2026) correcao por troca de CONTAGEM EXATA em gerar_x_custodia_v408.py, achada no ensaio a seco das guardas (scratch, numeros ficticios):
a ressalva (10) de delta_v408.RESSALVAS_V408 cita o 4,44 da Fase 9 V2, e o post NAO pode traze-lo (a regra da ordem e' do quadro; o proprio script o assevera): as ressalvas que citam o numero do quadro ficam FORA do post e o post diz quantas ficaram no registro do core.
Backup de bytes; temporario -> conferir -> substituir; ast.parse; LF preservado (o molde era LF). Escrito pelo Write."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")
P = os.path.join(HERE, "gerar_x_custodia_v408.py"); raw = open(P, "rb").read(); t = raw.decode("utf-8")
A1 = 'ress = "; ".join("(%d) %s" % (i + 1, curto(x)) for i, x in enumerate(tt["ressalvas"]))\n'
B1 = ('_sem_quadro = [x for x in tt["ressalvas"] if "4,44" not in x and "4.44" not in x and "z_disc" not in x]   # a ressalva que cita o numero do quadro NAO entra no post (a regra da ordem e\' do quadro); o post diz quantas ficaram no registro\n'
      'n_fora = len(tt["ressalvas"]) - len(_sem_quadro)\n'
      'ress = "; ".join("(%d) %s" % (i + 1, curto(x)) for i, x in enumerate(_sem_quadro)) + (" (mais %d ressalva(s) sobre o teste com a natureza, que ficam no registro do core: o número do quadro só se cita com a regra da ordem)" % n_fora if n_fora else "")\n')
assert t.count(A1) == 1, t.count(A1)
t = t.replace(A1, B1); novo = t.encode("utf-8"); ast.parse(t)
bak = P + ".bak_" + TS + "_adapt"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
tmp = P + ".tmp_adapt"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, P); assert open(P, "rb").read() == novo
print("gerar_x_custodia_v408.py: %d -> %d B sha16 %s -> %s (LF %s; ast ok; backup %s)" % (len(raw), len(novo), hashlib.sha256(raw).hexdigest()[:16], hashlib.sha256(novo).hexdigest()[:16], novo.count(b"\r\n") == 0, os.path.basename(bak)))
