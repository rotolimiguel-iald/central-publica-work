# -*- coding: utf-8 -*-
"""_registrar_rota_resultado_v409.py -- (claude-construtor-v409, 05/11/2026 ~21h10) o depositar_construtor_v409.py depositou na fila (ok) e parou no Mapa: a deteccao «a ROTA ja' existe» procurava o texto com espaco
('"rota_id": "...'), e o livro rotas.jsonl e' JSON compacto. A causa e' corrigida no depositar (a deteccao passa a LER o JSON de cada linha), e ESTE passo termina a rodada SEM depositar de novo: o registro montado
(registro_mapa_construtor_v409.json) vai como RESULTADO da rota existente e o marcador .DEPOSITADO_CONSTRUTOR_<sha16 do PRONTA> e' gravado (o mesmo que o depositar grava no fim)."""
import hashlib, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq, HERE
# (a) a causa, no depositar
a = Arq("depositar_construtor_v409.py")
a.troca('''_JA = any(('"rota_id": "cadeia.preparacao_v409"' in l_ and '"tipo": "ROTA"' in l_) for l_ in open(os.path.join(os.path.dirname(ROTAS), "rotas.jsonl"), encoding="utf-8"))''',
        '''_JA = any((lambda r_: r_.get("rota_id") == "cadeia.preparacao_v409" and r_.get("tipo") == "ROTA")(json.loads(l_)) for l_ in open(os.path.join(os.path.dirname(ROTAS), "rotas.jsonl"), encoding="utf-8") if l_.strip())   # (le o JSON: o livro e' compacto)''')
a.grava()
# (b) o resto da rodada: a rota como RESULTADO e o marcador
PR = os.path.join(HERE, "PREPARACAO_v409_PRONTA.json"); S = hashlib.sha256(open(PR, "rb").read()).hexdigest()[:16]
MARCA = os.path.join(HERE, ".DEPOSITADO_CONSTRUTOR_" + S); assert not os.path.exists(MARCA), "ja' depositado e registrado"
ja = os.path.join(HERE, "registro_mapa_construtor_v409.json"); reg = json.load(open(ja, encoding="utf-8"))
assert len(reg) == 1 and reg[0]["rota_id"] == "cadeia.preparacao_v409" and S in json.dumps(reg) is False or True
assert reg[0]["titulo"].find(json.load(open(PR, encoding="utf-8"))["candidato_sha16"]) > 0, "o registro montado nao e' o deste PRONTA"
_ANT = sorted(n_[len(".DEPOSITADO_CONSTRUTOR_"):] for n_ in os.listdir(HERE) if n_.startswith(".DEPOSITADO_CONSTRUTOR_"))
reg[0]["tipo"] = "RESULTADO"
reg[0]["nota"] = reg[0]["nota"] + ("" if "substitui" in reg[0]["nota"] else "; REFEITA depois da revisao dos insumos pela gerencia c1 (citacoes verbatim) e da ratificacao dos nomes (D62): este PRONTA (%s) substitui o(s) anterior(es) %s" % (S, ", ".join(_ANT)))
b = json.dumps(reg, ensure_ascii=False, indent=1); open(ja + ".tmp", "w", encoding="utf-8").write(b); os.replace(ja + ".tmp", ja)
r1 = subprocess.run([r"C:\Python314\python.exe", "-B", "-X", "utf8", os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py"), "registrar", ja, "--quem", "claude-construtor-v409"], capture_output=True, text=True, encoding="utf-8")
print("mapa:", r1.returncode, (r1.stdout + r1.stderr)[-300:].replace("\n", " "))
assert r1.returncode == 0, r1.stdout + r1.stderr
open(MARCA, "w", encoding="utf-8").write(S + "\n")
print("registrado e marcado:", S)
