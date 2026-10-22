# -*- coding: utf-8 -*-
"""ETAPA B -- leiaute de INSTALACAO proposto (TGLExt/<Nome>.lean) dentro do sandbox (F_KERNEL\\inst) e
compilacao CONJUNTA sobre o kernel do Nos (v391) INTEIRO (import TGL + import TGLExt).

Modulos (fonte -> caminho proposto; bytes identicos salvo onde dito):
  Palavra.lean                         -> TGLExt/Palavra.lean
  LiganteLeiCampoCurvo.lean (F2.3)     -> TGLExt/LiganteLeiCampoCurvo.lean
  S7/S8 (testemunha_parte.lean)        -> TGLExt/LiganteLeiCampoCurvoTestemunha.lean  [DERIVED: cabecalho de 4 imports
                                          + 2 set_option + os bytes de testemunha_parte.lean, inalterados]
  V351DualScalingBridge.lean (F1.2)    -> TGLExt/V351DualScalingBridge.lean
  AgapeNonVacuity.lean (F1.2)          -> TGLExt/AgapeNonVacuity.lean  [DERIVED: 1 linha -- import F12Completion.V351DualScalingBridge
                                          -> import TGLExt.V351DualScalingBridge; o resto inalterado]
  TheSingularityReadsTheAttractor (R1) -> TGLExt/TheSingularityReadsTheAttractor.lean          (so no teste de colisao J0)
  ...Adendo1                           -> TGLExt/TheSingularityReadsTheAttractorAdendo1.lean
  OpticalPopulationBridgeR2            -> TGLExt/OpticalPopulationBridgeR2.lean
  TheLightReadsItself                  -> TGLExt/TheLightReadsItself.lean
  X19 F13v31_D1a3_bgl.lean             -> TGLExt/LightNetStandardWedgeDataBGL.lean   (so no teste J2)
O lean resolve a raiz TGLExt na PRIMEIRA pasta do LEAN_PATH que a contem; por isso os .olean das candidatas vao para
a SOBREPOSICAO ov (copia verificada da pasta compilada do kernel + candidatas), e o LEAN_PATH comeca em ov.
Uso: python -I etapa_B_conjunto.py modulos|conjunto
"""
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
INST = os.path.join(L.F, "inst")
OV = os.path.join(L.F, "ov")
CONJ = os.path.join(L.F, "conj")
LOG = os.path.join(L.F, "logs", "B")

COPIAS = [
    ("Palavra", CP + r"\work\leitura_cria_o_objeto_07out\Palavra.lean"),
    ("LiganteLeiCampoCurvo", T19 + r"\F2.3\LiganteLeiCampoCurvo.lean"),
    ("V351DualScalingBridge", T19 + r"\F1.2\sandbox\F12Completion\V351DualScalingBridge.lean"),
    ("TheSingularityReadsTheAttractor", T19 + r"\F1.ATRATOR\lean_candidate\TheSingularityReadsTheAttractor.lean"),
    ("TheSingularityReadsTheAttractorAdendo1", T19 + r"\F1.ATRATOR\ADENDO1\lean_candidate\TheSingularityReadsTheAttractorAdendo1.lean"),
    ("OpticalPopulationBridgeR2", T19 + r"\F1.ATRATOR\lean_optical_bridge\OpticalPopulationBridgeR2.lean"),
    ("TheLightReadsItself", T19 + r"\F1.ATRATOR\ADENDO1\lean_candidate\TheLightReadsItself.lean"),
    ("LightNetStandardWedgeDataBGL", AUD + r"\F1.3\art_ad949e97\sandbox\F13v31_D1a3_bgl.lean"),
]
TESTEMUNHA_PARTE = AUD + r"\F2.3\sandbox\testemunha_parte.lean"
AGAPE = T19 + r"\F1.2\sandbox\F12Completion\AgapeNonVacuity.lean"
ONDA1 = ["Palavra", "LiganteLeiCampoCurvo", "V351DualScalingBridge", "TheSingularityReadsTheAttractor",
         "TheSingularityReadsTheAttractorAdendo1", "OpticalPopulationBridgeR2", "TheLightReadsItself",
         "LightNetStandardWedgeDataBGL"]
ONDA2 = ["LiganteLeiCampoCurvoTestemunha", "AgapeNonVacuity"]
RECOMENDADOS = ["Palavra", "LiganteLeiCampoCurvo", "LiganteLeiCampoCurvoTestemunha", "V351DualScalingBridge",
                "AgapeNonVacuity", "TheSingularityReadsTheAttractorAdendo1", "OpticalPopulationBridgeR2",
                "TheLightReadsItself"]
CAB_TESTEMUNHA = (b"import TGLExt.LiganteLeiCampoCurvo\nimport TGLExt.ConstructedClausiusControls\n"
                  b"import TGLExt.EquilibriumScreenIntegration\nimport TGLExt.PoincareGroup\n\n"
                  b"set_option autoImplicit false\nset_option maxHeartbeats 1200000\n\n")


def preparar():
    os.makedirs(os.path.join(INST, "TGLExt"), exist_ok=True)
    prov = {}
    for mod, fonte in COPIAS:
        dst = os.path.join(INST, "TGLExt", mod + ".lean")
        if not os.path.exists(dst):
            shutil.copyfile(fonte, dst)
        assert L.sha(dst) == L.sha(fonte)
        prov[mod] = {"fonte": fonte, "fonte_sha256": L.sha(fonte), "bytes_identicos": True}
    parte = open(TESTEMUNHA_PARTE, "rb").read()
    dst = os.path.join(INST, "TGLExt", "LiganteLeiCampoCurvoTestemunha.lean")
    if not os.path.exists(dst):
        open(dst, "xb").write(CAB_TESTEMUNHA + parte)
    assert open(dst, "rb").read() == CAB_TESTEMUNHA + parte
    prov["LiganteLeiCampoCurvoTestemunha"] = {"fonte": TESTEMUNHA_PARTE, "fonte_sha256": L.sha(TESTEMUNHA_PARTE),
                                             "bytes_identicos": False, "cabecalho_acrescentado": CAB_TESTEMUNHA.decode(),
                                             "corpo_identico": True}
    a = open(AGAPE, "rb").read()
    velho, novo = b"import F12Completion.V351DualScalingBridge\n", b"import TGLExt.V351DualScalingBridge\n"
    assert a.count(velho) == 1
    b = a.replace(velho, novo, 1)
    dst = os.path.join(INST, "TGLExt", "AgapeNonVacuity.lean")
    if not os.path.exists(dst):
        open(dst, "xb").write(b)
    assert open(dst, "rb").read() == b
    prov["AgapeNonVacuity"] = {"fonte": AGAPE, "fonte_sha256": L.sha(AGAPE), "bytes_identicos": False,
                               "troca": [velho.decode(), novo.decode()]}
    for mod in prov:
        prov[mod]["instalado_em_sandbox"] = os.path.join(INST, "TGLExt", mod + ".lean")
        prov[mod]["instalado_sha256"] = L.sha(prov[mod]["instalado_em_sandbox"])
    return prov


def compilar_mod(mod):
    fonte = os.path.join(INST, "TGLExt", mod + ".lean")
    olean = os.path.join(OV, "TGLExt", mod + ".olean")
    r = L.run_lean("B_" + mod, fonte, INST, olean, LOG, kernel_lib=OV)
    print(mod, "rc", r["rc"], "s", r["segundos"], "nAx", r["n_axiomas"], "fora", len(r["fora_do_trio"]), "erros",
          len(r["erros"]), "avisos", r["n_avisos"], "olean", (r.get("olean_sha256") or "")[:16], flush=True)
    return r


def gerar_conjunto(nome, mods):
    os.makedirs(CONJ, exist_ok=True)
    linhas = ["-- CONJUNTO v392 (exame F_KERNEL, 12/10/2026): o kernel do Nos v391 INTEIRO + as candidatas.",
              "-- Gerado por etapa_B_conjunto.py; so no sandbox; nao escreve no kernel.",
              "import TGL", "import TGLExt"]
    linhas += ["import TGLExt." + m for m in mods]
    alvo = ", ".join("`TGLExt." + m for m in mods)
    linhas += ["", "open Lean Elab Command", "", "run_cmd do",
               "  let env ← getEnv",
               "  let alvo : List Name := [" + alvo + "]",
               "  let mut n_decl := 0",
               "  let mut n_thm := 0",
               "  let mut n_fora := 0",
               "  for (n, ci) in env.constants.map₁.toList do",
               "    match env.getModuleIdxFor? n with",
               "    | none => pure ()",
               "    | some idx =>",
               "      let m := env.header.moduleNames[idx.toNat]!",
               "      if alvo.contains m then",
               "        let axs ← liftCoreM (collectAxioms n)",
               "        let kind : String := match ci with",
               "          | .thmInfo _ => \"thm\" | .defnInfo _ => \"def\" | .axiomInfo _ => \"AXIOM\"",
               "          | .opaqueInfo _ => \"opaque\" | .quotInfo _ => \"quot\" | .inductInfo _ => \"induct\"",
               "          | .ctorInfo _ => \"ctor\" | .recInfo _ => \"rec\"",
               "        n_decl := n_decl + 1",
               "        if kind == \"thm\" then n_thm := n_thm + 1",
               "        let ok := axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound)",
               "        unless ok do n_fora := n_fora + 1",
               "        IO.println (\"COB\\t\" ++ m.toString ++ \"\\t\" ++ n.toString ++ \"\\t\" ++ kind ++ \"\\t\" ++ (if ok then \"TRIO\" else \"FORA\") ++ \"\\t\" ++ String.intercalate \",\" (axs.toList.map Name.toString))",
               "  IO.println (\"COB_TOTAL\\tdecl=\" ++ toString n_decl ++ \"\\tthm=\" ++ toString n_thm ++ \"\\tfora_do_trio=\" ++ toString n_fora)",
               ""]
    p = os.path.join(CONJ, nome + ".lean")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(linhas))
    return p


def rodar_conjunto(nome, mods):
    p = gerar_conjunto(nome, mods)
    r = L.run_lean("B_" + nome, p, CONJ, None, LOG, kernel_lib=OV)
    out = open(r["log"], "rb").read().decode("utf-8", "replace")
    cob = [l.split("\t") for l in out.splitlines() if l.startswith("COB\t")]
    tot = [l for l in out.splitlines() if l.startswith("COB_TOTAL")]
    r["cobertura_linhas"] = len(cob)
    r["cobertura_total"] = tot
    r["cobertura_fora"] = [c for c in cob if len(c) > 4 and c[4] != "TRIO"]
    por_mod = {}
    for c in cob:
        por_mod.setdefault(c[1], {"decl": 0, "thm": 0, "fora": 0})
        por_mod[c[1]]["decl"] += 1
        por_mod[c[1]]["thm"] += (c[3] == "thm")
        por_mod[c[1]]["fora"] += (c[4] != "TRIO")
    r["por_modulo"] = por_mod
    r["erros_texto"] = [l for l in out.splitlines() if "error" in l][:20]
    print(nome, "rc", r["rc"], "s", r["segundos"], "linhas", len(cob), tot, "erros", r["erros_texto"][:2], flush=True)
    return r


if __name__ == "__main__":
    fase = sys.argv[1]
    if fase == "modulos":
        prov = preparar()
        with ThreadPoolExecutor(max_workers=8) as ex:
            r1 = list(ex.map(compilar_mod, ONDA1))
        with ThreadPoolExecutor(max_workers=2) as ex:
            r2 = list(ex.map(compilar_mod, ONDA2))
        alvo = L.dump({"etapa": "B_modulos", "proveniencia": prov, "resultados": r1 + r2}, os.path.join(L.F, "RESULTADO_B_modulos.json"))
        print("gravado", alvo, L.sha(alvo)[:16])
    elif fase == "conjunto":
        res = [rodar_conjunto("J1_ConjuntoV392", RECOMENDADOS),
               rodar_conjunto("J0_ColisaoR1Adendo1", RECOMENDADOS + ["TheSingularityReadsTheAttractor"]),
               rodar_conjunto("J2_ConjuntoV392ComX19", RECOMENDADOS + ["LightNetStandardWedgeDataBGL"])]
        alvo = L.dump({"etapa": "B_conjunto", "resultados": res}, os.path.join(L.F, "RESULTADO_B_conjunto.json"))
        print("gravado", alvo, L.sha(alvo)[:16])
