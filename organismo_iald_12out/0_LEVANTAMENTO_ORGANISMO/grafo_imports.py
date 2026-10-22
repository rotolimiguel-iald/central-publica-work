"""Grafo de imports (nível de módulo) entre as peças do organismo no tgl_kernel do Nós.
Só leitura do kernel; escreve GRAFO_IMPORTS_KERNEL.json nesta pasta. Levantamento do organismo, 12/10/2026."""
import os, re, json, hashlib, sys

ROOT = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GRAFO_IMPORTS_KERNEL.json")

mods = {}
for dp, dn, fn in os.walk(os.path.join(ROOT, "TGLExt")):
    for f in fn:
        if f.endswith(".lean"):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, ROOT).replace(os.sep, "/")[:-5].replace("/", ".")
            b = open(p, "rb").read()
            imps = re.findall(r"^import\s+([\w.]+)", b.decode("utf-8", "replace"), flags=re.M)
            mods[rel] = {"imports": imps, "sha16": hashlib.sha256(b).hexdigest()[:16], "bytes": len(b)}

PIECES = [
    "TGLExt.AbsoluteOne", "TGLExt.LightIsJ", "TGLExt.HajaLuz", "TGLExt.TheAngleIsTheProjection",
    "TGLExt.TheObserverReadsTheAngle", "TGLExt.NameIsTheContent", "TGLExt.IALDJones", "TGLExt.IALDGraviton",
    "TGLExt.IALDRhoStar", "TGLExt.LightRhoStar", "TGLExt.QGSolutionComplete", "TGLExt.TetelestaiOneObject",
    "TGLExt.TheWholeIsOne", "TGLExt.PhysicsIsTheReading", "TGLExt.TheMatrixRule", "TGLExt.TheLedgerOfCharges",
    "TGLExt.TheVerbSelectsTheAction", "TGLExt.TheCouplingRunsBoundedBelow", "TGLExt.Fundacao",
    "TGLExt.TheIALDSelector", "TGLExt.TheIALDInTheTower", "TGLExt.TheGreatAttractor", "TGLExt.TheExplosion",
    "TGLExt.TheNameOperator", "TGLExt.TheKeyIsTheReader", "TGLExt.TheIdentityOfIdentity", "TGLExt.TheAtomOfIdentity",
    "TGLExt.TheLivingWord", "TGLExt.ContinuousModularZero", "TGLExt.UmPostoRelacao", "TGLExt.UmPostoInscription",
    "TGLExt.TheTerminalRankOne", "TGLExt.TheWeightIsNotTheRank", "TGLExt.FirstCurvature", "TGLExt.AnsatzEinstein",
    "TGLExt.TracialDissipativeTorsion", "TGLExt.TheAxiomAndTheFalseWitness", "TGLExt.QGReaderUVLock",
    "TGLExt.ThePsionAndTheViscosity", "TGLExt.SMatrix", "TGLExt.TheCorrespondence", "TGLExt.TheRootOfTheProofTree",
    "TGLExt.O16.RotationGeneratorBridges", "TGLExt.ModularFlow", "TGLExt.BisognanoWichmann", "TGLExt.PowersLadder",
    "TGLExt.TheTower", "TGLExt.TheSelectionIsTheBallast", "TGLExt.CollapseContract", "TGLExt.TheNameIsTheInstrument",
    "TGLExt.TheEquationOfTruth", "TGLExt.TheElementaryReason", "TGLExt.ExactWitness", "TGLExt.WordExistence",
    "TGLExt.InfiniteWord", "TGLExt.TheRecordOfTheCut", "TGLExt.TheFalseHasNoGeometry", "TGLExt.TheDarkSplit",
    "TGLExt.EmergenceTriad", "TGLExt.TriadMaster", "TGLExt.PsiEmergence", "TGLExt.TheModularFlowIsAHorizon",
    "TGLExt.ThreeLocksCorner", "TGLExt.GlobalLiftLadder", "TGLExt.TheDischargedOath", "TGLExt.TheVerbalCoupling",
    "TGLExt.TheTraceIsNotErasable", "TGLExt.FractalUnitarity", "TGLExt.TheSingularExpectation",
]
missing = [p for p in PIECES if p not in mods]

memo = {}
def closure(m, stack=()):
    if m in memo:
        return memo[m]
    s = set()
    for i in mods.get(m, {}).get("imports", []):
        if i.startswith("TGLExt") or i.startswith("TGL."):
            s.add(i)
            if i in mods and i not in stack:
                s |= closure(i, stack + (m,))
    memo[m] = s
    return s

out = {}
for p in PIECES:
    if p in mods:
        out[p] = {
            "sha16": mods[p]["sha16"], "bytes": mods[p]["bytes"], "imports": mods[p]["imports"],
            "reaches_pieces": sorted([q for q in PIECES if q != p and q in closure(p)]),
            "n_transitive_TGLExt_or_TGL": len(closure(p)),
        }
direct = {p: [q for q in PIECES if q in mods.get(p, {}).get("imports", [])] for p in PIECES if p in mods}
rev = {p: sorted([m for m, v in mods.items() if p in v["imports"]]) for p in PIECES}

# pares que falam do mesmo objeto: alcançabilidade mútua (nenhum dos dois alcança o outro = sem lema possível entre eles)
PAIRS = [
    ("TGLExt.TheCouplingRunsBoundedBelow", "TGLExt.Fundacao"),            # Zenão: dicotomia vs abismo
    ("TGLExt.TheCouplingRunsBoundedBelow", "TGLExt.TheAxiomAndTheFalseWitness"),  # zeno vs absolute_zero_unreachable
    ("TGLExt.TheIALDSelector", "TGLExt.IALDRhoStar"),                       # IALD: firstAtom vs e (Jones)
    ("TGLExt.TheIALDSelector", "TGLExt.LightRhoStar"),                      # IALD: firstAtom vs PFmic
    ("TGLExt.IALDRhoStar", "TGLExt.LightRhoStar"),                          # ρ* finito vs ρ* na luz
    ("TGLExt.TheVerbSelectsTheAction", "TGLExt.TheIALDSelector"),           # post a vs ialdSelector
    ("TGLExt.TheVerbSelectsTheAction", "TGLExt.IALDJones"),                 # reading vs jonesReading
    ("TGLExt.TheVerbSelectsTheAction", "TGLExt.TheTerminalRankOne"),        # post (posto 1) vs terminal rank one
    ("TGLExt.TheVerbSelectsTheAction", "TGLExt.UmPostoRelacao"),            # post vs UmPosto
    ("TGLExt.UmPostoRelacao", "TGLExt.UmPostoInscription"),                 # dois Um posto
    ("TGLExt.TheWeightIsNotTheRank", "TGLExt.TheTerminalRankOne"),          # rank
    ("TGLExt.TheMatrixRule", "TGLExt.TheVerbSelectsTheAction"),             # regra matriz vs verbo
    ("TGLExt.TheMatrixRule", "TGLExt.Fundacao"),
    ("TGLExt.QGSolutionComplete", "TGLExt.TheWholeIsOne"),
    ("TGLExt.QGSolutionComplete", "TGLExt.Fundacao"),
    ("TGLExt.TheObserverReadsTheAngle", "TGLExt.IALDJones"),                # observing_adds_nothing vs jonesReading_idem
    ("TGLExt.TheObserverReadsTheAngle", "TGLExt.TheIALDSelector"),
    ("TGLExt.FirstCurvature", "TGLExt.TracialDissipativeTorsion"),          # Riemann1001 vs riemann (Cartan)
    ("TGLExt.AnsatzEinstein", "TGLExt.TracialDissipativeTorsion"),
    ("TGLExt.IALDJones", "TGLExt.TheExplosion"),                             # memória: jonesReading_idem vs E²=E
    ("TGLExt.TheGreatAttractor", "TGLExt.IALDRhoStar"),                     # atrator: diagFlow vs Ttgl/jonesU
    ("TGLExt.TheGreatAttractor", "TGLExt.IALDJones"),
    ("TGLExt.LightIsJ", "TGLExt.TheVerbSelectsTheAction"),
    ("TGLExt.NameIsTheContent", "TGLExt.ExactWitness"),                     # Nome=conteúdo vs Nome=palavra normalizada
    ("TGLExt.ContinuousModularZero", "TGLExt.Fundacao"),                    # III₁ contínuo vs escala dual
    ("TGLExt.ContinuousModularZero", "TGLExt.TheCouplingRunsBoundedBelow"),
    ("TGLExt.AbsoluteOne", "TGLExt.TheIALDSelector"),
]
pairs = []
for a, b in PAIRS:
    ca, cb = closure(a), closure(b)
    pairs.append({"a": a, "b": b, "a_reaches_b": b in ca, "b_reaches_a": a in cb,
                  "common_TGLExt_ancestors": len(ca & cb),
                  "ligacao_possivel_por_import": (b in ca) or (a in cb)})

res = {"gerado": "levantamento do organismo, 12/10/2026 (leitura; nada compilado)",
       "kernel_root": ROOT, "n_modulos_TGLExt": len(mods), "pecas_ausentes_do_kernel": missing,
       "pecas": out, "imports_diretos_entre_pecas": direct, "importado_por": rev, "pares_mesmo_objeto": pairs}
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("modulos", len(mods), "| ausentes:", missing)
for pr in pairs:
    print(("LIGA " if pr["ligacao_possivel_por_import"] else "SEM-IMPORT ") + pr["a"].split(".")[-1] + " <-> " + pr["b"].split(".")[-1],
          "| a->b", pr["a_reaches_b"], "| b->a", pr["b_reaches_a"], "| ancestrais comuns", pr["common_TGLExt_ancestors"])
print("---")
for p in PIECES:
    if p in out:
        print(p.split("TGLExt.")[-1], "| imports:", [i.replace("TGLExt.", "") for i in out[p]["imports"] if i != "Mathlib"],
              "| importado por:", [m.replace("TGLExt.", "") for m in rev[p][:6]], ("..." if len(rev[p]) > 6 else ""))
