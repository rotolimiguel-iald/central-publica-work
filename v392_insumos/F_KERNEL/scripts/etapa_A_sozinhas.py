# -*- coding: utf-8 -*-
"""ETAPA A -- cada candidata SOZINHA, com os bytes entregues e o leiaute de modulo da entrega
(para reproduzir o .olean entregue quando houver). Copia byte a byte para F_KERNEL\\sozinhas\\<id>\\.
Uso: python -I etapa_A_sozinhas.py"""
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leanlib as L  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
CP = r"C:\IALD\Central de Patentes"
T19 = CP + r"\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019"
AUD = r"C:\IALD\PROGRAMA_IALD\auditorias"
SOZ = os.path.join(L.F, "sozinhas")
LOG = os.path.join(L.F, "logs", "A")

# (id, fonte_original, caminho_relativo_no_sandbox (define o nome do modulo), olean_entregue_ou_None)
CANDIDATAS = [
    ("A01_palavra", CP + r"\work\leitura_cria_o_objeto_07out\Palavra.lean", "Palavra.lean", None),
    ("A02_ligante", T19 + r"\F2.3\LiganteLeiCampoCurvo.lean", r"TGLExt\LiganteLeiCampoCurvo.lean",
     T19 + r"\F2.3\LiganteLeiCampoCurvo.olean"),
    ("A03_ligante_S7S8_auditoria", AUD + r"\F2.3\sandbox\TestemunhaF23.lean", "TestemunhaF23.lean", None),
    ("A04a_f12_ponte", T19 + r"\F1.2\sandbox\F12Completion\V351DualScalingBridge.lean",
     r"F12Completion\V351DualScalingBridge.lean", T19 + r"\F1.2\sandbox\build\F12Completion\V351DualScalingBridge.olean"),
    ("A05_atrator_r1", T19 + r"\F1.ATRATOR\lean_candidate\TheSingularityReadsTheAttractor.lean",
     "TheSingularityReadsTheAttractor.lean", T19 + r"\F1.ATRATOR\lean_candidate\attempts\004\TheSingularityReadsTheAttractor.olean"),
    ("A06_ponte_otica_r2", T19 + r"\F1.ATRATOR\lean_optical_bridge\OpticalPopulationBridgeR2.lean",
     "OpticalPopulationBridgeR2.lean", T19 + r"\F1.ATRATOR\lean_optical_bridge\attempts\002\OpticalPopulationBridgeR2.olean"),
    ("A07_atrator_adendo1", T19 + r"\F1.ATRATOR\ADENDO1\lean_candidate\TheSingularityReadsTheAttractorAdendo1.lean",
     "TheSingularityReadsTheAttractorAdendo1.lean",
     T19 + r"\F1.ATRATOR\ADENDO1\lean_candidate\attempts\TheSingularityReadsTheAttractorAdendo1\001\TheSingularityReadsTheAttractorAdendo1.olean"),
    ("A08_luz_le_a_si", T19 + r"\F1.ATRATOR\ADENDO1\lean_candidate\TheLightReadsItself.lean", "TheLightReadsItself.lean",
     T19 + r"\F1.ATRATOR\ADENDO1\lean_candidate\attempts\TheLightReadsItself\002\TheLightReadsItself.olean"),
    ("A09_x19_bgl", AUD + r"\F1.3\art_ad949e97\sandbox\F13v31_D1a3_bgl.lean", "F13v31_D1a3_bgl.lean", None),
    ("A10_x19_statement", AUD + r"\F1.3\art_ad949e97\sandbox\F13v31_D1a3_statement.lean", "F13v31_D1a3_statement.lean", None),
]
DEPENDENTE = ("A04b_f12_agape", T19 + r"\F1.2\sandbox\F12Completion\AgapeNonVacuity.lean",
              r"F12Completion\AgapeNonVacuity.lean", T19 + r"\F1.2\sandbox\build\F12Completion\AgapeNonVacuity.olean")


def preparar(cid, fonte, rel):
    raiz = os.path.join(SOZ, cid if not cid.startswith("A04") else "A04_f12")
    dst = os.path.join(raiz, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copyfile(fonte, dst)
    assert L.sha(dst) == L.sha(fonte), (cid, "copia difere")
    return raiz, dst


def compilar(item):
    cid, fonte, rel, olean_ent = item
    raiz, dst = preparar(cid, fonte, rel)
    out_olean = os.path.join(raiz, "build", os.path.splitext(rel)[0] + ".olean")
    r = L.run_lean(cid, dst, raiz, out_olean, LOG, extra_paths=[os.path.join(raiz, "build")])
    r["fonte_original"] = fonte
    r["fonte_original_sha256"] = L.sha(fonte)
    if olean_ent:
        r["olean_entregue"] = olean_ent
        r["olean_entregue_sha256"] = L.sha(olean_ent)
        r["olean_identico_ao_entregue"] = (r.get("olean_sha256") == r["olean_entregue_sha256"])
    print(cid, "rc", r["rc"], "s", r["segundos"], "nAx", r["n_axiomas"], "fora", len(r["fora_do_trio"]),
          "erros", len(r["erros"]), "avisos", r["n_avisos"], "sorry", len(r["sorry"]), "tokens", r["tokens_proibidos_na_fonte"],
          "olean=entregue" if r.get("olean_identico_ao_entregue") else ("olean_DIF" if olean_ent else ""), flush=True)
    return r


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=6) as ex:
        resultados = list(ex.map(compilar, CANDIDATAS))
    resultados.append(compilar(DEPENDENTE))
    alvo = L.dump({"etapa": "A_sozinhas", "lean": L.LEAN, "resultados": resultados}, os.path.join(L.F, "RESULTADO_A_sozinhas.json"))
    print("gravado", alvo, L.sha(alvo)[:16])
