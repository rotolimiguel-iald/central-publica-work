# -*- coding: utf-8 -*-
"""_r1_reparos_de_texto_v410.py -- dois reparos de TEXTO no delta, apontados pelo agente de adaptacao da R4 e feitos pelo construtor ANTES da cadeia (que roda uma vez so'): na D96 a frase obrigatoria do teste vinha solta, em minuscula, depois de ponto;
na leitura da fala dos passos a forma vigente do tempo vinha em minuscula depois de ponto. So' a costura muda: as frases (constantes) ficam identicas. Backup de BYTES; temporario -> substituir; ast.parse; import e guarda de conferencia."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "delta_v410.py"); b0 = open(P, "rb").read(); t = b0.decode("utf-8"); assert b"\r\n" not in b0
for a, b in (('o comando ao executor sobre o que falta. " + FRASE_H0DN_OBRIGATORIA_PT + ". "', 'o comando ao executor sobre o que falta (o teste segue " + FRASE_H0DN_OBRIGATORIA_PT + "). "'),
             ('sem solução, Z(s) < 1. " + FRASE_TEMPO_PT,', 'sem solução, Z(s) < 1; a forma vigente do tempo: " + FRASE_TEMPO_PT,')):
    c = t.count(a); assert c == 1, (c, a); t = t.replace(a, b)
nb = t.encode("utf-8"); ast.parse(nb)
open(P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_pre_reparos_de_texto", "wb").write(b0)
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("delta_v410.py sha16", hashlib.sha256(b0).hexdigest()[:16], "->", hashlib.sha256(nb).hexdigest()[:16])
sys.path.insert(0, HERE)
import delta_v410 as DL, guarda_frases_v410 as GF
RT = GF.RT; G = lambda x: [v[0] for v in GF.violacoes(x)] + [str(v)[:60] for v in RT._v392_guarda_texto(x)]
print("D96:", G(DL.DECISOES["D96"]), "| leituras:", {k: G(str(v)) for k, v in DL.LEITURA_V410.items() if "forma vigente do tempo" in str(v)})
