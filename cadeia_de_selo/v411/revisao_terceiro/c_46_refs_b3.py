import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
P = V.replace("\\", "/")
alvos = ["bancada_B3_servico/recibo_parada_v411.py", "bancada_B3_servico/recibo_religamento_v411.py", "bancada_B3_servico/evento_c1_b3_v411.py", "pos_rito/textos_custodia_handoff_v411.py", "pos_rito/gerar_x_custodia_v411.py", "pos_rito/registrar_mapa_v411.py", "pos_rito/fechar_v411.py"]
pat = re.compile(r"[\"']([A-Za-z]:[\/][^\"'\n]{6,200}\.(?:py|json|md|txt|sh|jsonl))[\"']")
ausentes = {}
for a in alvos:
    t = rd(P + "/" + a)
    for ln, l in enumerate(t.split("\n"), 1):
        if l.lstrip().startswith("#"): continue
        for m in pat.finditer(l):
            p = m.group(1).replace("\\\\", "\\")
            if "%" in p or "{" in p: continue
            if not os.path.exists(p): ausentes.setdefault(p, []).append("%s:%d" % (os.path.basename(a), ln))
for p, v in sorted(ausentes.items()):
    print("AUSENTE:", p, v[:2])
print("fim", len(ausentes))
