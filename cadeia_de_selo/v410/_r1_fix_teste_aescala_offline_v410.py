# -*- coding: utf-8 -*-
"""_r1_fix_teste_aescala_offline_v410.py -- R1 (BAIXO 5): o teste offline do a_escala_v410 passa a dar ao registro a raiz embutida (TGLExt.lean do sandbox, com o import do modulo) e ganha dois controles negativos: o kernel nao verificado (c2) e a raiz sem o import (c3).
Backup de BYTES; temporario -> substituir; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); p = os.path.join(HERE, "_teste_aescala_offline_v410.py"); b0 = open(p, "rb").read(); t = b0.decode("utf-8"); assert b"\r\n" not in b0
BS = chr(92); NL = BS + "n"


def tr(a, b, n=1):
    global t
    c = t.count(a); assert c == n, (c, a[:90]); t = t.replace(a, b)


tr('("_EMBEDDED_KERNEL_FILES", {rel: pedra_t})', '("_EMBEDDED_KERNEL_FILES", {rel: pedra_t, "TGLExt.lean": RAIZ})')
tr('RT._V410_VERBATINS2 = VERB\n', 'RT._V410_VERBATINS2 = VERB\nRAIZ = open(os.path.join(DL.SANDBOX, "TGLExt.lean"), encoding="utf-8").read(); assert ("import " + CONTR["mod"]) in RAIZ   # (R1, BAIXO 5: a raiz do kernel do sandbox, com o import do modulo)\n')
tr('RTA._EMBEDDED_KERNEL_FILES = {rel: pedra_t + "' + NL + '-- adulterada' + NL + '"}', 'RTA._EMBEDDED_KERNEL_FILES = {rel: pedra_t + "' + NL + '-- adulterada' + NL + '", "TGLExt.lean": RAIZ}')
tr('RTA._EMBEDDED_KERNEL_FILES = {rel: pedra_t}\n', 'RTA._EMBEDDED_KERNEL_FILES = {rel: pedra_t, "TGLExt.lean": RAIZ}\n')
tr('for k, (vd, fl) in R.items():\n    print("controle negativo',
   'c8 = core_de_ensaio(); c8["kernel_formalization"]["all_verified"] = False; r_ = RTA.a_escala_v410(c8); R["kernel_nao_verificado"] = (r_["verdict"], _f(r_))   # (R1, BAIXO 5)\n'
   'RTA._EMBEDDED_KERNEL_FILES = {rel: pedra_t, "TGLExt.lean": RAIZ.replace("import " + CONTR["mod"], "-- retirado")}; r_ = RTA.a_escala_v410(core_de_ensaio()); R["raiz_sem_o_import"] = (r_["verdict"], _f(r_)); RTA._EMBEDDED_KERNEL_FILES = {rel: pedra_t, "TGLExt.lean": RAIZ}\n'
   'for k, (vd, fl) in R.items():\n    print("controle negativo')
tr('"escada_um_a_menos": ["c1"]}', '"escada_um_a_menos": ["c1"], "kernel_nao_verificado": ["c2"], "raiz_sem_o_import": ["c3"]}')
tr('and R["frase_vedada_plantada"][1] == ["c9"]', 'and R["frase_vedada_plantada"][1] == ["c9"] and R["kernel_nao_verificado"][1] == ["c2"] and R["raiz_sem_o_import"][1] == ["c3"]')
ast.parse(t); open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_pre_r1", "wb").write(b0); open(p + ".tmp", "wb").write(t.encode("utf-8")); os.replace(p + ".tmp", p); print("ok")
