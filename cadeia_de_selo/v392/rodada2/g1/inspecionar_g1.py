# -*- coding: utf-8 -*-
"""inspecionar_g1.py -- roda o motor sobre o grupo G1 (como testar_registros_v392.py) e IMPRIME por registro: veredito, n de checks ok, `lido`, violacoes da guarda P18, fontes, bandeiras.
So' leitura; nao escreve nada. Uso: python -B -X utf8 inspecionar_g1.py"""
import copy, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(os.path.dirname(HERE)); sys.path.insert(0, V)
import montar_registros_v392 as M  # noqa: E402
import guarda_p18_v392 as G  # noqa: E402
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s"
codigo, info = M.montar("G1")
ns = {}
exec(compile(G.GUARDA_V392_SRC, "<guarda>", "exec"), ns); exec(compile(codigo, "<pins>", "exec"), ns)
exec(compile(open(os.path.join(V, "registros_motor_v392.py"), encoding="utf-8").read(), "<motor>", "exec"), ns)
core = copy.deepcopy(json.load(open(NOS + "/um_absoluto.json", encoding="utf-8"))["core"]); kf = core["kernel_formalization"]
LOG = open(os.path.join(V, "kernel", "build_full.log"), encoding="utf-8", errors="replace").read(); AX = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", LOG, re.S):
    AX[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", LOG):
    AX.setdefault(m.group(1), [])
for f, n, mod, kind in json.load(open(os.path.join(V, "kernel", "FLAGS_v392.json"), encoding="utf-8"))["flags"]:
    kf[f] = True; kf["axiom_report"][n] = AX.get(n, [])
core.setdefault("pedras_v392", {"all_verified": True}); core.setdefault("varredura_e_sorry_v392", {"all_verified": True})
nomes = ns["_v392_rodar_registros"](core)
for n in nomes:
    r = core[n]
    print("=" * 100); print(n, "| all_verified:", r["all_verified"]); print(r["verdict"])
    print("checks:", sum(1 for c in r["checks"] if c["ok"]), "de", len(r["checks"]), "| fontes:", len(r["fontes"]), "ok:", all(f["ok"] for f in r["fontes"]), "| verbatins:", {k: v["embedded_ok"] for k, v in r["verbatim"].items()})
    print("kernel:", r["kernel"], "| guarda P18:", r["guarda_p18_violacoes"])
    print("lido:", json.dumps(r["lido"], ensure_ascii=False)[:700])
    print("n erratas:", len(r["erratas"]), "| limites:", len(r["limites"]), "| diz:", len(r["diz"]), "| nao_diz:", len(r["nao_diz"]))
    falhas = [c["descricao"] for c in r["checks"] if not c["ok"]]
    print("falhas:", falhas)
