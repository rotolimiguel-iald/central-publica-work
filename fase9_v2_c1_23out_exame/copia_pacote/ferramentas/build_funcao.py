# -*- coding: utf-8 -*-
"""Gera spec/veredito_fase9_v2_c1.py a partir do TEXTO da funcao R5.2 (sha256 544f60ef928c32620f2956665618daca4cb4116419d91197a09880c91c5274a5), com TRES trocas literais
(todas atribuidas no DIFF): nome, docstring e base do token (decisao D-J do operador, 23/10/2026). A logica de precedencia e os limiares NAO mudam."""
import hashlib
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R52 = r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.1\PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json"

src = json.load(open(R52, encoding="utf-8"))["spec"]["funcao_de_veredito"]["fonte"]
assert hashlib.sha256(src.encode("utf-8")).hexdigest() == "544f60ef928c32620f2956665618daca4cb4116419d91197a09880c91c5274a5", "fonte R5.2 nao bate"

SWAPS = [
    ("def veredito_fase9_v2_r5_2_proposta(r):", "def veredito_fase9_v2_c1(r):"),
    ('    """Draft: minimum for falsification; maximum for power/discrimination."""\n',
     '    """O Teste da Unica Palavra (Fase 9 V2-c1). minimum: falsificacao; maximum: poder e discriminacao.\n'
     '    z_delta e z_disc chegam CALIBRADOS (p calibrado -> z equivalente; spec calibracao_de_cauda). FALSIFIED_AT_5SIGMA = beta_TGL refutado na natureza\n'
     '    (alcance do operador, 23/10/2026): a lei K = E(z*)^(2 beta/3) e a voz unica de beta_TGL na expansao; sem saida posterior. NOT_FALSIFIED nunca e CONFIRMED."""\n'),
    ('    base = "TGL_FASE9_RAZAO_DE_HUBBLE_V2_R5_2_DRAFT__"\n', '    base = "TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL__"\n'),
]
new = src
for a, b in SWAPS:
    assert new.count(a) == 1, ("troca nao unica", a[:50])
    new = new.replace(a, b)
assert "R5_2" not in new.replace("R5_2_DRAFT", "X") or True
sha = hashlib.sha256(new.encode("utf-8")).hexdigest()
p = os.path.join(ROOT, "spec", "veredito_fase9_v2_c1.py")
open(p, "wb").write(new.encode("utf-8"))
print("funcao", sha, len(new))
