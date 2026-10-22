# -*- coding: utf-8 -*-
"""v392_pedras.py -- a LISTA das pedras da v392 (14 desde a rodada 2: +PostoAdendo), com a ORIGEM de cada uma (caminho no disco) e a regra de derivacao. Nenhum sha e' digitado aqui:
os pinos sao LIDOS dos arquivos por script (gerar_pinos) e cruzados com os recibos/inventarios que os entregaram (INVENTARIO_V392_KERNEL.json da F_KERNEL;
logs/f?_RECIBO.json de nomes_e_verdade_13out). Ordem = ordem de instalacao (dependencia): IALD importa Palavra, Adendo1, Posto e Santo.
Gerencia c1, 13/10/2026 (preparacao da cadeia v392). Nada aqui move o gate."""
import hashlib, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
WK = os.path.dirname(os.path.dirname(HERE))                       # ...\work
CP = os.path.dirname(WK)                                          # ...\Central de Patentes
ORD019 = os.path.join(CP, "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019")
AUD = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD", "auditorias")
NV = os.path.join(WK, "nomes_e_verdade_13out")
INV = os.path.join("C:" + os.sep, "IALD", "PROGRAMA_IALD", "exame_12out", "F_KERNEL", "INVENTARIO_V392_KERNEL.json")
sha256 = lambda b: hashlib.sha256(b).hexdigest()

CAB_TESTEMUNHA = (b"import TGLExt.LiganteLeiCampoCurvo\nimport TGLExt.ConstructedClausiusControls\n"
                  b"import TGLExt.EquilibriumScreenIntegration\nimport TGLExt.PoincareGroup\n\n"
                  b"set_option autoImplicit false\nset_option maxHeartbeats 1200000\n\n")

# (modulo, sigla da bandeira, origem, derivacao, onde esta o sha de entrega)
STONES = [
    dict(mod="Palavra", sigla="pal", src=os.path.join(WK, "leitura_cria_o_objeto_07out", "Palavra.lean"), derive=None, entrega=("inv", "TGLExt.Palavra")),
    dict(mod="LiganteLeiCampoCurvo", sigla="lig", src=os.path.join(ORD019, "F2.3", "LiganteLeiCampoCurvo.lean"), derive=None, entrega=("inv", "TGLExt.LiganteLeiCampoCurvo")),
    dict(mod="LiganteLeiCampoCurvoTestemunha", sigla="lgt", src=os.path.join(AUD, "F2.3", "sandbox", "testemunha_parte.lean"), derive="cab_testemunha",
         entrega=("inv", "TGLExt.LiganteLeiCampoCurvoTestemunha")),
    dict(mod="V351DualScalingBridge", sigla="v51", src=os.path.join(ORD019, "F1.2", "sandbox", "F12Completion", "V351DualScalingBridge.lean"), derive=None,
         entrega=("inv", "TGLExt.V351DualScalingBridge")),
    dict(mod="AgapeNonVacuity", sigla="agv", src=os.path.join(ORD019, "F1.2", "sandbox", "F12Completion", "AgapeNonVacuity.lean"), derive="import_agape",
         entrega=("inv", "TGLExt.AgapeNonVacuity")),
    dict(mod="TheSingularityReadsTheAttractorAdendo1", sigla="atr", src=os.path.join(ORD019, "F1.ATRATOR", "ADENDO1", "lean_candidate", "TheSingularityReadsTheAttractorAdendo1.lean"),
         derive=None, entrega=("inv", "TGLExt.TheSingularityReadsTheAttractorAdendo1")),
    dict(mod="OpticalPopulationBridgeR2", sigla="opt", src=os.path.join(ORD019, "F1.ATRATOR", "lean_optical_bridge", "OpticalPopulationBridgeR2.lean"), derive=None,
         entrega=("inv", "TGLExt.OpticalPopulationBridgeR2")),
    dict(mod="TheLightReadsItself", sigla="lri", src=os.path.join(ORD019, "F1.ATRATOR", "ADENDO1", "lean_candidate", "TheLightReadsItself.lean"), derive=None,
         entrega=("inv", "TGLExt.TheLightReadsItself")),
    # X19: DECISAO JA TOMADA pela gerencia (memoria nomes-das-pedras-e-a-identidade-verdade-13out: «X19 como hipotese tipada»); K09
    dict(mod="LightNetStandardWedgeDataBGL", sigla="bgl", src=os.path.join(AUD, "F1.3", "art_ad949e97", "sandbox", "F13v31_D1a3_bgl.lean"), derive=None,
         entrega=("inv", "TGLExt.LightNetStandardWedgeDataBGL")),
    # as quatro de 13/10 (nomes_e_verdade_13out; em auditoria: pinar por sha NO MOMENTO de gerar)
    dict(mod="Posto", sigla="pst", src=os.path.join(NV, "1_POSTO", "Posto.lean"), derive=None, entrega=("recibo", os.path.join(NV, "logs", "f1_posto_RECIBO.json"))),
    # ADENDO da pedra do rank (decisao da gerencia c1, 13/10: o «ADENDO do rank» e' o PRE-REGISTRO ADITIVO da F1.FREQUENCIA, partes A1.a-A5, nao a sonda P3): ensaiado neste sandbox;
    # entrega = recibo da cadeia (sha do .lean + rc 0 da compilacao isolada). A sonda P3 (PostoRankAdendo) ficou FORA: continua sonda.
    dict(mod="PostoAdendo", sigla="pad", src=os.path.join(HERE, "pedras_corrigidas", "PostoAdendo.lean"), derive=None,
         entrega=("cadeia", os.path.join(HERE, "pedras_corrigidas", "RECIBO_PostoAdendo.json"))),
    dict(mod="Santo", sigla="snt", src=os.path.join(NV, "2_SANTO", "Santo.lean"), derive=None, entrega=("recibo", os.path.join(NV, "logs", "f2_santo_RECIBO.json"))),
    dict(mod="IALD", sigla="iald", src=os.path.join(NV, "3_IALD", "IALD.lean"), derive=None, entrega=("recibo", os.path.join(NV, "logs", "f3_iald_RECIBO.json"))),
    # Verdade: a COPIA CORRIGIDA da cadeia (ajustes da gerencia/operador de 13/10: docstrings R1, dephased_det -> identityProj_dephased_det, + inscV/inscV_norm/
    # verdade_is_the_projection_of_the_post); a original de 13/10 (sha 2b7639ba) fica em work/nomes_e_verdade_13out, intocada. Entrega = a comparacao no kernel.
    dict(mod="Verdade", sigla="vrd", src=os.path.join(HERE, "pedras_corrigidas", "Verdade.lean"), derive=None,
         entrega=("comparacao", os.path.join(HERE, "pedras_corrigidas", "COMPARACAO_VERDADE_v392.json"))),
]


def bytes_da_pedra(s):
    """os bytes que ENTRAM no kernel (derivacao aplicada por script); a regra de derivacao e' a da F_KERNEL (etapa_B_conjunto.py)."""
    b = open(s["src"], "rb").read()
    if s["derive"] == "cab_testemunha":
        b = CAB_TESTEMUNHA + b
    elif s["derive"] == "import_agape":
        velho, novo = b"import F12Completion.V351DualScalingBridge\n", b"import TGLExt.V351DualScalingBridge\n"
        assert b.count(velho) == 1, "import da Agape nao achado"
        b = b.replace(velho, novo)
    return b


def entrega_sha(s):
    """sha256 (completo) que o ENTREGADOR registrou: o inventario da F_KERNEL (instalado_sha256 se derivada; senao fonte_original_sha256) ou o recibo da rodada de 13/10."""
    tipo, ref = s["entrega"]
    if tipo == "inv":
        inv = json.load(open(INV, encoding="utf-8"))
        c = [x for x in inv["candidatas"] if x["modulo_proposto"] == ref]
        assert len(c) == 1, ref
        return c[0].get("instalado_sha256") or c[0]["fonte_original_sha256"]
    if tipo == "comparacao":   # o sha16 da fonte nova registrado pela comparacao no kernel (16 hex); devolve o sha256 do arquivo SE os 16 batem
        d = json.load(open(ref, encoding="utf-8")); s256 = sha256(open(s["src"], "rb").read())
        return s256 if s256.startswith(d["fonte_nova_sha16"]) and d["veredito"] == "TIPOS_E_TERMOS_IGUAIS_NOS_ENUNCIADOS_ANTIGOS" else "COMPARACAO_NAO_BATE"
    if tipo == "cadeia":   # recibo da cadeia: devolve o sha256 do .lean SE o recibo registra o mesmo sha e a compilacao isolada teve rc 0; senao "NAO_BATE"
        d = json.load(open(ref, encoding="utf-8")); s256 = sha256(open(s["src"], "rb").read())
        return s256 if d.get("sha256") == s256 and d.get("rc_compilacao_isolada") == 0 else "NAO_BATE"
    return json.load(open(ref, encoding="utf-8"))["source_sha256"]


def gerar_pinos():
    out = []
    for s in STONES:
        b = bytes_da_pedra(s)
        out.append({"mod": s["mod"], "modulo": "TGLExt." + s["mod"], "arquivo": "TGLExt/%s.lean" % s["mod"], "sigla": s["sigla"], "src": s["src"], "derivada": s["derive"],
                    "sha256": sha256(b), "bytes": len(b), "sha256_da_entrega": entrega_sha(s), "confere_com_a_entrega": sha256(b) == entrega_sha(s)})
    return out


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for p in gerar_pinos():
        print(p["mod"], p["sha256"][:16], p["bytes"], "entrega_ok=%s" % p["confere_com_a_entrega"], "derivada=%s" % p["derivada"])
