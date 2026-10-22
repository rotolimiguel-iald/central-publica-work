# -*- coding: utf-8 -*-
"""controles_g1.py -- CONTROLES NEGATIVOS proprios do grupo G1 (alem dos do testar_registros_v392.py: fonte e verbatim adulterados). Para cada adulteracao do core/kernel de ENSAIO
(copia em memoria; nada e' gravado), o registro afetado TEM de recusar (all_verified False) e dizer o motivo no veredito. So' leitura. Uso: python -B -X utf8 controles_g1.py"""
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
base = json.load(open(NOS + "/um_absoluto.json", encoding="utf-8"))["core"]
LOG = open(os.path.join(V, "kernel", "build_full.log"), encoding="utf-8", errors="replace").read(); AX = {}
for m in re.finditer(r"'([\w.']+)' depends on axioms: \[([^\]]*)\]", LOG, re.S):
    AX[m.group(1)] = [a.strip() for a in m.group(2).replace("\n", " ").split(",") if a.strip()]
for m in re.finditer(r"'([\w.']+)' does not depend on any axioms", LOG):
    AX.setdefault(m.group(1), [])
FL = json.load(open(os.path.join(V, "kernel", "FLAGS_v392.json"), encoding="utf-8"))["flags"]


def novo_core():
    c = copy.deepcopy(base); kf = c["kernel_formalization"]
    for f, n, mod, kind in FL:
        kf[f] = True; kf["axiom_report"][n] = AX.get(n, [])
    c["pedras_v392"] = {"all_verified": True}; c["varredura_e_sorry_v392"] = {"all_verified": True}
    return c


specs = {s["nome"]: s for s in ns["_V392_SPECS"]}
casos = []


def caso(nome, alvo, mexe, falha_esperada):
    c = novo_core(); mexe(c)
    r = ns["_v392_registro"](specs[alvo], c)
    ok = (r["all_verified"] is False) and (falha_esperada in r["verdict"])
    casos.append((nome, alvo, ok, r["verdict"][-160:]))


# a base tem de passar
for n, s in specs.items():
    r = ns["_v392_registro"](s, novo_core()); casos.append(("BASE passa", n, r["all_verified"] is True, r["verdict"][-60:]))
caso("bandeira da PALAVRA apagada", "palavra_v392", lambda c: c["kernel_formalization"].pop("ext_pal_the_face_does_not_close_kernel_proved"), "KERNEL_BANDEIRAS")
caso("bandeira False do ligante", "lei_de_campo_curvo_v392", lambda c: c["kernel_formalization"].__setitem__("ext_lig_NamedAtlasH3_kernel_checked", False), "KERNEL_BANDEIRAS")
caso("axioma fora do trio na ponte V351", "agape_nao_vacua_v392", lambda c: c["kernel_formalization"]["axiom_report"].__setitem__("F12Completion.agape_on_v351_core", ["propext", "sorryAx"]), "KERNEL_DECLARACOES")
caso("declaracao do BGL ausente do axiom_report", "x19_bgl_tipo_v392", lambda c: c["kernel_formalization"]["axiom_report"].pop("AuditF13v31.tomitaSquare_unique"), "KERNEL_DECLARACOES")
for alvo in specs:
    caso("pedras_v392 recusou", alvo, lambda c: c["pedras_v392"].__setitem__("all_verified", False), "CHECK_")
    caso("o gate mudou de veredito", alvo, lambda c: c["qg_closure"].__setitem__("verdict", "QG_CLOSURE_GATE__ALGO_DIFERENTE"), "CHECK_")
caso("token antigo ausente do core", "lei_de_campo_curvo_v392", lambda c: c["fundacao_v390"].__setitem__("verdict", "TGL_FUNDACAO_V390__SEM_O_TOKEN"), "CHECK_lc2")
caso("QGSolutionComplete alterada no kernel do rito", "x19_bgl_tipo_v392", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/QGSolutionComplete.lean", "0" * 64), "CHECK_x1a")
caso("QGSolutionComplete alterada no kernel do rito (raiz do fecho)", "lei_de_campo_curvo_v392", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/QGSolutionComplete.lean", "0" * 64), "CHECK_lc34")
caso("TheObserverReadsTheAngle alterada", "palavra_v392", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/TheObserverReadsTheAngle.lean", "0" * 64), "CHECK_pa27")
caso("Fundacao alterada", "agape_nao_vacua_v392", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/Fundacao.lean", "0" * 64), "CHECK_ag16")
caso("not_claimed[1] da Fundacao reescrito", "agape_nao_vacua_v392", lambda c: c["fundacao_v390"]["not_claimed"].__setitem__(1, "outra frase"), "CHECK_ag2")
# guarda de texto: um spec com a palavra recusada tem de ser barrado
s_ruim = copy.deepcopy(specs["palavra_v392"]); s_ruim["diz"] = s_ruim["diz"] + ["a singularidade converge ao atrator"]
r = ns["_v392_registro"](s_ruim, novo_core()); casos.append(("guarda P18: texto proibido", "palavra_v392", r["all_verified"] is False and "GUARDA_P18" in r["verdict"], r["verdict"][-80:]))
ok_all = all(c[2] for c in casos)
for c in casos:
    print(("OK    " if c[2] else "FALHA ") + c[0].ljust(62) + c[1].ljust(26) + c[3][-90:])
print("controles:", sum(c[2] for c in casos), "de", len(casos), "->", "TODOS OK" if ok_all else "HA FALHA")
sys.exit(0 if ok_all else 1)
