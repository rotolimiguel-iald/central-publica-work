# -*- coding: utf-8 -*-
"""editar_gerar_candidato.py -- (gerencia c1, rodada 2) aplica as edicoes de integracao em gerar_candidato_v392.py (backup de bytes feito antes). Uso unico."""
import os, shutil, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(HERE, "gerar_candidato_v392.py")
shutil.copyfile(p, p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_integracao")
s = open(p, encoding="utf-8", newline="").read()


def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (old[:70], s.count(old))
    s = s.replace(old, new)


# 1) erratas E01/A03 sobre o v391 puro, antes de tudo
rep('T = raw.decode("utf-8")\n',
    'T = raw.decode("utf-8")\nimport patches_erratas_v392 as ER  # noqa: E402\nT, ER_LOG = ER.aplicar(T, True)   # E01 (comentarios no codigo) + A03 (erratas ao lado no artigo): dados, aplicados com assert de contagem sobre a v391\n'
    'import json as _json\nKHJ = _json.load(open(os.path.join(KD, "KH_N1_v392.json"), encoding="utf-8"))\n')
# KD so' e' definido antes? garantir ordem: KD definido na linha 18 (antes de T)
# 2) montagem do runtime com os registros por spec
rep('RT = PINS.rstrip("\\n") + "\\n\\n\\n" + RT_LOGIC\n',
    'RC_PINS, RC_INFO = MR.montar()\n'
    'KH_PIN = "_V392_KH = " + repr({"nao_lidas": KHJ["nao_lidas_pelo_regex_do_umpy"], "decl_minimo": KHJ["linha_TOTAL"]["decl"]}) + "\\n"\n'
    'MOTOR = open(os.path.join(HERE, "registros_motor_v392.py"), encoding="utf-8").read()\n'
    'RT = PINS.rstrip("\\n") + "\\n" + KH_PIN + "\\n" + RC_PINS + "\\n\\n" + GP.GUARDA_V392_SRC + "\\n\\n" + RT_LOGIC.rstrip("\\n") + "\\n\\n\\n" + MOTOR\n')
# 3) chamada dos registros: um segundo bloco try, etiquetado v392
rep("""       '    print("   [v392] as 13 pedras do kernel: %s | varredura recursiva e detector de sorry: %s" % (core["pedras_v392"]["verdict"], core["varredura_e_sorry_v392"]["verdict"]))']""",
    """       '    print("   [v392] as %d pedras do kernel: %s | varredura recursiva e detector de sorry: %s" % (len(_V392_PEDRAS), core["pedras_v392"]["verdict"], core["varredura_e_sorry_v392"]["verdict"]))',
       '    try:   # v392: os registros por spec (erratas, cunhagens, Bancada, atrator, neutrinos, cobertura): excecao vira AVISO visivel',
       '        _n392 = _v392_rodar_registros(core)',
       '        print("   [v392] registros por spec: %d (selados %d)" % (len(_n392), sum(1 for k_ in _n392 if (core.get(k_) or {}).get("all_verified") is True)))',
       '    except Exception as _e392b:',
       '        print("   [v392] AVISO: os registros por spec nao rodaram: %r" % (_e392b,))']""")
# 4) selo: um bloco resumo
rep("""        '            "varredura_e_sorry_v392": {k_: (core.get("varredura_e_sorry_v392") or {}).get(k_) for k_ in ("verdict", "all_verified", "varredura", "detector_de_sorry", "ao_lado_v362")},']""",
    """        '            "varredura_e_sorry_v392": {k_: (core.get("varredura_e_sorry_v392") or {}).get(k_) for k_ in ("verdict", "all_verified", "varredura", "detector_de_sorry", "ao_lado_v362")},',
        '            "registros_v392": {n_: {k_: (core.get(n_) or {}).get(k_) for k_ in ("verdict", "all_verified")} for n_ in _V392_NOMES_REGISTROS},']""")
# 5) K13: cobertura do axiom_report no kernel
rep('    res["axiom_report"] = axioms\r\n', '    res["axiom_report"] = axioms\r\n', 0) if False else None
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok: integracao parte 1")
