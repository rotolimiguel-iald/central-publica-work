# -*- coding: utf-8 -*-
"""aplicar_R6_v405.py -- liga a errata R6 das pedras (gerencia c1, 01/11/2026, 19:02: uma docstring da Tonica) na cadeia v405.
Uso unico. Backup de BYTES de cada arquivo antes (.bak_<ts>_R6); temporario -> conferir -> os.replace; cada ancora tem de aparecer exatamente 1x.
Nao toca nas pedras: quem as copia e' copiar_pedras_v405.py, a partir do pino. Nenhum teorema novo: a R6 nao muda codigo."""
import os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")


def patch(nome, subs):
    p = os.path.join(HERE, nome)
    b = open(p, "rb").read()
    s = b.decode("utf-8")
    for a, c in subs:
        n = s.count(a)
        assert n == 1, (nome, n, a[:110])
        s = s.replace(a, c)
    assert s != b.decode("utf-8")
    open(p + ".bak_" + TS + "_R6", "wb").write(b)
    t = p + ".tmp_R6"
    open(t, "wb").write(s.encode("utf-8"))
    assert open(t, "rb").read() == s.encode("utf-8") and len(s) >= len(b.decode("utf-8")) - 200
    os.replace(t, p)
    print("ok", nome, len(subs))


patch("gerar_pino_das_pedras_v405.py", [
    ("""Reexecutavel: se o JSON ja existe e e' igual, fica; se difere, aborta. uso:""",
     """AO LADO (errata R6 da gerencia, 19:02 de 01/11: uma docstring da Tonica, reprovada pela guarda F12): a FONTE VIGENTE agora e' RECIBO_ERRATA_PEDRAS_R6_01nov.json. Esse recibo repete as entradas do R5 (com o `sha256_antes` do R5) e so' a Tonica tem depois novo; logo a pedra mudada na R6 e' a de depois diferente do R5, e nao a que tem `sha256_antes`. Cadeia: R6.sha256_antes == R5.sha256_depois na mudada; R6.depois == R5.depois nas demais. Nenhum teorema novo.
Reexecutavel: se o JSON ja existe e e' igual, fica; se difere, aborta. uso:"""),
    ("""NOVOS_R5 = {"LeiDoDiminuto": ["TGLExt.LeiDoDiminuto.modular_mantem_a_escala"]}
""",
     """NOVOS_R5 = {"LeiDoDiminuto": ["TGLExt.LeiDoDiminuto.modular_mantem_a_escala"]}
# ---- a errata R6 (19:02 de 01/11/2026, gerencia c1: uma docstring da Tonica): a FONTE VIGENTE. O R5 fica como elo da cadeia de custodia.
R6_P = os.path.join(E0, "RECIBO_ERRATA_PEDRAS_R6_01nov.json")
R6 = json.load(open(R6_P, encoding="utf-8"))
assert len(R6["pedras"]) == 8 and sorted(R6["pedras"]) == sorted(R5["pedras"]), sorted(R6["pedras"])
MUDOU_R6 = sorted(k_ for k_, v_ in R6["pedras"].items() if v_["sha256_depois"] != R5["pedras"][k_]["sha256_depois"])
assert MUDOU_R6 == ["TonicaDoHamiltoniano"], MUDOU_R6
assert R6["codigo_mudado"] == [], ("a ordem diz que a R6 nao mudou codigo; o recibo diz outra coisa", R6["codigo_mudado"])
"""),
    ("""    e5_ = R5["pedras"][nome]; e4_ = R4["pedras"][nome]; e3_ = R3["pedras"][nome]; e2_ = R2["pedras"][nome]     # a FONTE VIGENTE (R5): o arquivo manda e tem de bater com sha256_depois
    assert os.path.normcase(os.path.normpath(e5_["arquivo"])) == os.path.normcase(os.path.normpath(arq)), ("a errata R5 aponta outro arquivo", nome, e5_["arquivo"], arq)
    assert e5_["sha256_depois"] == h and e5_["sha16_depois"] == h[:16], ("o arquivo da pedra DIVERGE do recibo R5 (sha256_depois)", nome, h[:16], e5_["sha256_depois"][:16])
    if nome in INALTERADAS_R5:
        assert e4_["sha256_depois"] == h, ("a pedra dita inalterada na R5 difere do recibo R4", nome)
""",
     """    e6_ = R6["pedras"][nome]; e5_ = R5["pedras"][nome]; e4_ = R4["pedras"][nome]; e3_ = R3["pedras"][nome]; e2_ = R2["pedras"][nome]     # a FONTE VIGENTE (R6): o arquivo manda e tem de bater com sha256_depois
    assert os.path.normcase(os.path.normpath(e6_["arquivo"])) == os.path.normcase(os.path.normpath(arq)), ("a errata R6 aponta outro arquivo", nome, e6_["arquivo"], arq)
    assert e6_["sha256_depois"] == h and e6_["sha16_depois"] == h[:16], ("o arquivo da pedra DIVERGE do recibo R6 (sha256_depois)", nome, h[:16], e6_["sha256_depois"][:16])
    if nome in MUDOU_R6:
        assert e6_["sha256_antes"] == e5_["sha256_depois"] and e6_["bytes_depois"] == len(b), ("a cadeia de custodia rompeu: R6.sha256_antes != R5.sha256_depois", nome)
    else:
        assert e5_["sha256_depois"] == h, ("a pedra inalterada na R6 difere do recibo R5", nome)
    if nome in INALTERADAS_R5:
        assert e4_["sha256_depois"] == e5_["sha256_depois"], ("a pedra dita inalterada na R5 difere do recibo R4", nome)
"""),
    ("""        assert e5_["sha256_antes"] == e4_["sha256_depois"] and e5_["bytes_depois"] == len(b), ("a cadeia de custodia rompeu: R5.sha256_antes != R4.sha256_depois", nome)
""",
     """        assert e5_["sha256_antes"] == e4_["sha256_depois"], ("a cadeia de custodia rompeu: R5.sha256_antes != R4.sha256_depois", nome)
"""),
    ("""                  "errata_r5": {"recibo": os.path.basename(R5_P),""",
     """                  "errata_r6": {"recibo": os.path.basename(R6_P), "recibo_sha256": hashlib.sha256(open(R6_P, "rb").read()).hexdigest(), "mudou_na_r6": nome in MUDOU_R6, "sha256_depois": R6["pedras"][nome]["sha256_depois"]},
                  "errata_r5": {"recibo": os.path.basename(R5_P),"""),
])

patch("copiar_insumos_v405.py", [
    ("""(os.path.basename(RG.RECIBO_ERRATA_R5_ARQ), RG.RECIBO_ERRATA_R5_ARQ),""",
     """(os.path.basename(RG.RECIBO_ERRATA_R5_ARQ), RG.RECIBO_ERRATA_R5_ARQ), (os.path.basename(RG.RECIBO_ERRATA_R6_ARQ), RG.RECIBO_ERRATA_R6_ARQ),"""),
])

patch("registros_v405.py", [
    ("""RECIBO_ERRATA_R5_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R5_01nov.json")
""",
     """RECIBO_ERRATA_R5_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R5_01nov.json")
CHAVE_RECIBO_ERRATA_R6 = "recibo_errata_r6_das_pedras_01nov"
RECIBO_ERRATA_R6_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R6_01nov.json")
"""),
    ("""          {"chave": CHAVE_RECIBO_ERRATA_R5, "arquivo": os.path.join(INS, os.path.basename(RECIBO_ERRATA_R5_ARQ)), "papel": "o recibo da ERRATA R5 DAS PEDRAS (gerencia c1, 01/11/2026, a escala e' o que fica parado): os oito sha256 vigentes, quatro mudaram; codigo novo""",
     """          {"chave": CHAVE_RECIBO_ERRATA_R6, "arquivo": os.path.join(INS, os.path.basename(RECIBO_ERRATA_R6_ARQ)), "papel": "o recibo da ERRATA R6 DAS PEDRAS (gerencia c1, 01/11/2026, uma docstring da Tonica): os oito sha256 vigentes, um mudou; nenhum codigo mudou [DECLARADO na origem; o sha256 de cada pedra e os termos sao conferidos pelo gerador e pelo kernel do rito]"},
          {"chave": CHAVE_RECIBO_ERRATA_R5, "arquivo": os.path.join(INS, os.path.basename(RECIBO_ERRATA_R5_ARQ)), "papel": "o recibo da ERRATA R5 DAS PEDRAS (gerencia c1, 01/11/2026, a escala e' o que fica parado): oito sha256, quatro mudaram; codigo novo"""),
    ("""    cks2.append(CH("n%d" % m, "o recibo da errata R5 das pedras (fonte pinada, a vigente) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R5, ["pedras"], "tamanho_igual", 8)); m += 1
""",
     """    cks2.append(CH("n%d" % m, "o recibo da errata R6 das pedras (fonte pinada, a vigente) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R6, ["pedras"], "tamanho_igual", 8)); m += 1
    cks2.append(CH("n%d" % m, "o recibo da errata R5 das pedras (fonte pinada) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R5, ["pedras"], "tamanho_igual", 8)); m += 1
"""),
    ("""CHAVE_RECIBO_ERRATA_R5, CHAVE_RECIBO_IDENTIDADE, CHAVE_RECIBO_OBSERVADOR], "verbatins": [CH_DE(N_NOMES),""",
     """CHAVE_RECIBO_ERRATA_R5, CHAVE_RECIBO_ERRATA_R6, CHAVE_RECIBO_IDENTIDADE, CHAVE_RECIBO_OBSERVADOR], "verbatins": [CH_DE(N_NOMES),"""),
    ("""        "fontes": [CHAVE_DE_FONTE["psion"], CHAVE_RECIBO_ERRATA_R5], "verbatins": [CH_DE(N_MODULA)],""",
     """        "fontes": [CHAVE_DE_FONTE["psion"], CHAVE_RECIBO_ERRATA_R6], "verbatins": [CH_DE(N_MODULA)],"""),
])

patch("derivar_encanamento_v405_regrasE1_p00.py", [
    ("""_cad = [(_rec_r5, _rec_r4), (_rec_r4, _rec_r3), (_rec_r3, _rec_r2)]
""",
     """_rec_r6 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R6_01nov.json"))
_cad = [(_rec_r6, _rec_r5), (_rec_r5, _rec_r4), (_rec_r4, _rec_r3), (_rec_r3, _rec_r2)]
"""),
    ("""chk("[v405] as pedras sao as da ERRATA R5 da gerencia: o sha256 de cada arquivo == o sha256_depois do recibo vigente (oito arquivos), e a cadeia de custodia fecha: em R5 -> R4 -> R3 -> R2, antes == depois do recibo anterior (a inalterada: depois == depois) e R2.antes == R1.depois (sete arquivos); os recibos antigos ficam como registro", all(sha(rd(os.path.join(HERE, "pedra", k_ + ".lean"))) == v_["sha256_depois"] for k_, v_ in _rec_r5["pedras"].items()) and len(_rec_r5["pedras"]) == 8 and all(all((n_["pedras"][k_].get("sha256_antes") or n_["pedras"][k_]["sha256_depois"]) == v_["sha256_depois"] for k_, v_ in a_["pedras"].items()) for n_, a_ in _cad) and""",
     """chk("[v405] as pedras sao as da ERRATA R6 da gerencia: o sha256 de cada arquivo == o sha256_depois do recibo vigente (oito arquivos), e a cadeia de custodia fecha: em R6 -> R5 -> R4 -> R3 -> R2, cada pedra ou segue igual (depois == depois) ou tem antes == depois do recibo anterior, e R2.antes == R1.depois (sete arquivos); os recibos antigos ficam como registro", all(sha(rd(os.path.join(HERE, "pedra", k_ + ".lean"))) == v_["sha256_depois"] for k_, v_ in _rec_r6["pedras"].items()) and len(_rec_r6["pedras"]) == 8 and all(all(v_["sha256_depois"] in (n_["pedras"][k_].get("sha256_antes"), n_["pedras"][k_]["sha256_depois"]) for k_, v_ in a_["pedras"].items()) for n_, a_ in _cad) and"""),
    ("""and len(_rec_err["arquivos"]) == 7, len(_rec_r5["pedras"]))""",
     """and len(_rec_err["arquivos"]) == 7, len(_rec_r6["pedras"]))"""),
])

patch("gerar_relatorio_v405.py", [
    ("""             "recibo_vigente_das_pedras": "RECIBO_ERRATA_PEDRAS_R5_01nov.json",""",
     """             "recibo_vigente_das_pedras": "RECIBO_ERRATA_PEDRAS_R6_01nov.json","""),
    ("""RECIBO_ERRATA_PEDRAS_R5_01nov.json`, cadeia de custódia R5 → R4 → R3 → R2 → primeira errata)""",
     """RECIBO_ERRATA_PEDRAS_R6_01nov.json`, cadeia de custódia R6 → R5 → R4 → R3 → R2 → primeira errata)"""),
    ("""e um achado desta preparação mudou quatro (`..._R5_01nov.json`, a referência vigente: a escala é o que fica parado); o resto foi refeito aqui,""",
     """um achado desta preparação mudou quatro (`..._R5_01nov.json`: a escala é o que fica parado); e a guarda desta preparação pegou uma docstring da Tônica (`..._R6_01nov.json`, a referência vigente); o resto foi refeito aqui,"""),
    ("""| R5: a escala | a escala é a musical, o que fica parado; o que era escala de energia é valor absoluto e valor relativo à tônica;""",
     """| R5 e R6: a escala | a escala é a musical, o que fica parado; onde o texto fala do acorde ou da Lei do Diminuto, e nos textos novos, o que era escala de energia é valor absoluto e valor relativo à tônica; fora disso «escala» como escala de energia é permitida, e a guarda só pega a colisão (F10, F11, F12);"""),
])

fp = os.path.join(HERE, "fechar_preparacao_v405.py")
b = open(fp, "rb").read()
s = b.decode("utf-8")
assert s.count("R2 a R5") == 3, s.count("R2 a R5")
open(fp + ".bak_" + TS + "_R6", "wb").write(b)
t = fp + ".tmp_R6"
open(t, "wb").write(s.replace("R2 a R5", "R2 a R6").encode("utf-8"))
os.replace(t, fp)
print("ok fechar_preparacao_v405.py 3")

patch("delta_v405.py", [
    ("""16:45, 17:21, 18:41 e 18:56; recibos RECIBO_ERRATA_PEDRAS_01nov.json e _R2, _R3, _R4 e _R5)""",
     """16:45, 17:21, 18:41, 18:56 e 19:02; recibos RECIBO_ERRATA_PEDRAS_01nov.json e _R2, _R3, _R4, _R5 e _R6)"""),
])
print("FEITO", TS)
