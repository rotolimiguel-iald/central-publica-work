# -*- coding: utf-8 -*-
"""aplicar_R7a_pino_v405.py -- liga a errata R7 das pedras (gerencia c1, 01/11/2026, 20:57, segunda revisao de terceiro) no gerador do pino. Uso unico. Backup de BYTES; temporario -> conferir -> os.replace; cada ancora exatamente 1x."""
import os, time

HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")
p = os.path.join(HERE, "gerar_pino_das_pedras_v405.py")
b = open(p, "rb").read()
s = b.decode("utf-8")
SUBS = [
    ("""Reexecutavel: se o JSON ja existe e e' igual, fica; se difere, aborta. uso:""",
     """AO LADO (errata R7 da gerencia, 20:57 de 01/11, a segunda revisao de terceiro): a FONTE VIGENTE agora e' RECIBO_ERRATA_PEDRAS_R7_01nov.json (oito pedras; tres mudaram: PontoZeroDoPsion com codigo, LeiDoDiminuto e TonicaDoHamiltoniano so' docstring). Mesma leitura da R6: a pedra mudada e' a de depois diferente da anterior. Na PontoZeroDoPsion seis teoremas foram rebatizados (RENOMES_R7), tres sao novos (NOVOS_R7) e os lemas do lock mudaram de assinatura, com o nome; a contagem e' MEDIDA da fonte.
Reexecutavel: se o JSON ja existe e e' igual, fica; se difere, aborta. uso:"""),
    ("""assert R6["codigo_mudado"] == [], ("a ordem diz que a R6 nao mudou codigo; o recibo diz outra coisa", R6["codigo_mudado"])
""",
     """assert R6["codigo_mudado"] == [], ("a ordem diz que a R6 nao mudou codigo; o recibo diz outra coisa", R6["codigo_mudado"])
# ---- a errata R7 (20:57 de 01/11/2026, gerencia c1, a segunda revisao de terceiro): a FONTE VIGENTE. O R6 fica como elo da cadeia de custodia.
R7_P = os.path.join(E0, "RECIBO_ERRATA_PEDRAS_R7_01nov.json")
R7 = json.load(open(R7_P, encoding="utf-8"))
assert len(R7["pedras"]) == 8 and sorted(R7["pedras"]) == sorted(R6["pedras"]), sorted(R7["pedras"])
MUDOU_R7 = sorted(k_ for k_, v_ in R7["pedras"].items() if v_["sha256_depois"] != R6["pedras"][k_]["sha256_depois"])
assert MUDOU_R7 == ["LeiDoDiminuto", "PontoZeroDoPsion", "TonicaDoHamiltoniano"], MUDOU_R7
assert len(R7["codigo_mudado"]) == 1 and R7["codigo_mudado"][0].startswith("PontoZeroDoPsion:") and all(n_ in R7["codigo_mudado"][0] for n_ in ("retidoNoAngulo", "tempoDoRetido", "lockDe", "o_gap_com_unidade", "o_retido_e_o_valor_esperado_do_lock", "HminMic_e_o_lock", "the_gap_closes")), ("o recibo R7 nao diz a mudanca de codigo que a ordem deu", R7["codigo_mudado"])
_PZP = "TGLExt.PontoZeroDoPsion."
RENOMES_R7 = {_PZP + a_: _PZP + b_ for a_, b_ in {"o_gap_e_lido_do_angulo_de_miguel": "o_retido_e_lido_do_angulo_de_miguel", "a_tonica_e_o_gap_sobre_alpha": "a_tonica_e_o_retido_sobre_alpha", "a_massa_e_a_projecao_do_gap": "a_massa_e_a_projecao_do_retido", "o_psion_e_raiz_de_dois_gaps": "o_psion_e_raiz_de_dois_retidos", "o_ponto_zero_autoconsistente_e_o_gap": "o_ponto_zero_autoconsistente_e_o_retido", "o_relogio_do_gap": "o_relogio_do_retido"}.items()}
NOVOS_R7 = {"PontoZeroDoPsion": [_PZP + n_ for n_ in ("o_gap_com_unidade", "o_retido_e_o_valor_esperado_do_lock", "HminMic_e_o_lock")]}
"""),
    ("""    e6_ = R6["pedras"][nome]; e5_ = R5["pedras"][nome]; e4_ = R4["pedras"][nome]; e3_ = R3["pedras"][nome]; e2_ = R2["pedras"][nome]     # a FONTE VIGENTE (R6): o arquivo manda e tem de bater com sha256_depois
    assert os.path.normcase(os.path.normpath(e6_["arquivo"])) == os.path.normcase(os.path.normpath(arq)), ("a errata R6 aponta outro arquivo", nome, e6_["arquivo"], arq)
    assert e6_["sha256_depois"] == h and e6_["sha16_depois"] == h[:16], ("o arquivo da pedra DIVERGE do recibo R6 (sha256_depois)", nome, h[:16], e6_["sha256_depois"][:16])
    if nome in MUDOU_R6:
        assert e6_["sha256_antes"] == e5_["sha256_depois"] and e6_["bytes_depois"] == len(b), ("a cadeia de custodia rompeu: R6.sha256_antes != R5.sha256_depois", nome)
    else:
        assert e5_["sha256_depois"] == h, ("a pedra inalterada na R6 difere do recibo R5", nome)
""",
     """    e7_ = R7["pedras"][nome]; e6_ = R6["pedras"][nome]; e5_ = R5["pedras"][nome]; e4_ = R4["pedras"][nome]; e3_ = R3["pedras"][nome]; e2_ = R2["pedras"][nome]     # a FONTE VIGENTE (R7): o arquivo manda e tem de bater com sha256_depois
    assert os.path.normcase(os.path.normpath(e7_["arquivo"])) == os.path.normcase(os.path.normpath(arq)), ("a errata R7 aponta outro arquivo", nome, e7_["arquivo"], arq)
    assert e7_["sha256_depois"] == h and e7_["sha16_depois"] == h[:16], ("o arquivo da pedra DIVERGE do recibo R7 (sha256_depois)", nome, h[:16], e7_["sha256_depois"][:16])
    if nome in MUDOU_R7:
        assert e7_["sha256_antes"] == e6_["sha256_depois"] and e7_["bytes_depois"] == len(b), ("a cadeia de custodia rompeu: R7.sha256_antes != R6.sha256_depois", nome)
    else:
        assert e6_["sha256_depois"] == h, ("a pedra inalterada na R7 difere do recibo R6", nome)
    if nome in MUDOU_R6:
        assert e6_["sha256_antes"] == e5_["sha256_depois"], ("a cadeia de custodia rompeu: R6.sha256_antes != R5.sha256_depois", nome)
    else:
        assert e5_["sha256_depois"] == e6_["sha256_depois"], ("a pedra inalterada na R6 difere do recibo R5", nome)
"""),
    ("""    for n_ in NOVOS_R2.get(nome, []) + NOVOS_R3.get(nome, []) + NOVOS_R4.get(nome, []) + NOVOS_R5.get(nome, []):   # os teoremas novos da R2 e da R3 entram com axiomas por medir: quem mede e' o Audit do kernel (a contagem sobe por MEDIDA, nao por presuncao)
        th[n_] = []; n_teor += 1
""",
     """    for n_ in NOVOS_R2.get(nome, []) + NOVOS_R3.get(nome, []) + NOVOS_R4.get(nome, []) + NOVOS_R5.get(nome, []) + NOVOS_R7.get(nome, []):   # os teoremas novos da R2 em diante entram com axiomas por medir: quem mede e' o Audit do kernel (a contagem sobe por MEDIDA, nao por presuncao); os nomes da R4 rebatizados na R7 entram com o nome vigente
        th[RENOMES_R7.get(n_, n_)] = []; n_teor += 1
"""),
    ("""                  "errata_r6": {"recibo": os.path.basename(R6_P),""",
     """                  "errata_r7": {"recibo": os.path.basename(R7_P), "recibo_sha256": hashlib.sha256(open(R7_P, "rb").read()).hexdigest(), "mudou_na_r7": nome in MUDOU_R7, "sha256_depois": R7["pedras"][nome]["sha256_depois"]},
                  "errata_r6": {"recibo": os.path.basename(R6_P),"""),
]
for a, c in SUBS:
    n = s.count(a)
    assert n == 1, (n, a[:100])
    s = s.replace(a, c)
open(p + ".bak_" + TS + "_R7", "wb").write(b)
t = p + ".tmp_R7"
open(t, "wb").write(s.encode("utf-8"))
assert open(t, "rb").read() == s.encode("utf-8")
os.replace(t, p)
print("ok gerar_pino_das_pedras_v405.py", len(SUBS), TS)
