# -*- coding: utf-8 -*-
"""_r1_a5_citacoes_pedras_v410.py -- R1, A5 (licao da D91; MEDIO 2 da revisao de terceiro): o conferir_citacoes_v410.py passa a VARRER AS PEDRAS de modo ESTRITO e fail-closed: toda passagem entre aspas angulares em pedra\\*.lean tem de ser fala VERBATIM do operador,
com a MESMA normalizacao de work\\pedras_candidatas_09nov\\R2_aspas\\requote_aescala_v410.py (espacos colapsados, minusculas, reticencias toleradas por pedaco; o corpus sao os arquivos de fala OPERADOR_*.txt de work\\cunhagens_13out mais as copias duraveis em insumos\\cunhagens).
Rotulo, parafrase ou citacao de docstring entre aspas angulares REPROVA (nao ha' mais lista de apontadas que desculpe). Controle negativo: um trecho que o operador nunca disse tem de reprovar e um trecho de fala tem de passar; se o controle falhar, o conferidor reprova.
Com as pedras de HOJE (antes da R3) esta varredura reprova de proposito; passa a valer com as pedras da parte B. Backup de BYTES; temporario -> substituir; ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(HERE, "conferir_citacoes_v410.py"); BS = chr(92)
b0 = open(P, "rb").read(); crlf = b0.count(b"\r\n") > 0; t = b0.decode("utf-8").replace("\r\n", "\n")
a = 'ok = ok and not R["varredura_das_pedras"]["reprovadas"] and R["varredura_das_pedras"]["citacoes_conferidas"] > 0\n'
assert t.count(a) == 1, t.count(a)
novo = a + (
    '# (i-bis) [R1, 09/11/2026: D91 e MEDIO 2 da revisao de terceiro] VARREDURA ESTRITA DAS PEDRAS, fail-closed: toda passagem entre aspas angulares em pedra' + BS + BS + '*.lean tem de ser fala VERBATIM do operador (a casa reserva as angulares a fala verbatim);\n'
    '# a normalizacao e\' a do requote da gerencia (work' + BS + BS + 'pedras_candidatas_09nov' + BS + BS + 'R2_aspas' + BS + BS + 'requote_aescala_v410.py): espacos colapsados, minusculas, reticencias toleradas por pedaco; rotulo, parafrase e docstring citada NAO passam.\n'
    'import glob as _glob_r1\n'
    '_CUN_R1 = os.path.normpath(os.path.join(HERE, "..", "..", "cunhagens_13out"))\n'
    '_arqs_r1 = sorted(_glob_r1.glob(os.path.join(_CUN_R1, "OPERADOR_*.txt"))) + sorted(_glob_r1.glob(os.path.join(HERE, "insumos", "cunhagens", "*.txt")))\n'
    '_norm_r1 = lambda s_: re.sub(r"' + BS + 's+", " ", s_).strip().lower()\n'
    '_NC_R1 = _norm_r1("' + BS + 'n".join(open(p_, encoding="utf-8", errors="replace").read() for p_ in _arqs_r1))\n'
    '\n'
    '\n'
    'def _verbatim_r1(q_):\n'
    '    n_ = _norm_r1(q_).rstrip(".,;: ")\n'
    '    partes_ = [x_.strip(" .,;:") for x_ in re.split(r"' + BS + 'u2026|' + BS + '[' + BS + '.' + BS + '.' + BS + '.' + BS + ']|' + BS + '.' + BS + '.' + BS + '.", n_) if x_.strip(" .,;:")]\n'
    '    return bool(partes_) and all(pt_ in _NC_R1 for pt_ in partes_)\n'
    '\n'
    '\n'
    '_RX_R1 = re.compile(chr(0xAB) + "([^" + chr(0xBB) + "]{1,400})" + chr(0xBB))\n'
    '_ped_r1 = sorted(_glob_r1.glob(os.path.join(HERE, "pedra", "*.lean")))\n'
    '_rep_r1 = []; _n_r1 = 0\n'
    'for _pp in _ped_r1:\n'
    '    for _q in _RX_R1.findall(open(_pp, encoding="utf-8").read()):\n'
    '        _n_r1 += 1\n'
    '        if not _verbatim_r1(_q):\n'
    '            _rep_r1.append({"pedra": os.path.basename(_pp), "trecho": re.sub(r"' + BS + 's+", " ", _q)[:160]})\n'
    '_ctl_r1 = {"trecho_que_o_operador_nunca_disse_reprova": not _verbatim_r1("isto o operador nunca disse nesta casa xyzzy 4711"), "fala_do_operador_passa": _verbatim_r1(DL.FRASE_RATIFICO_TUDO) and _verbatim_r1(DL.FRASE_DEI_A_ESCALA),\n'
    '           "reticencias_por_pedaco": _verbatim_r1(DL.FRASE_DEI_A_ESCALA + " ... " + DL.FRASE_RATIFICO_TUDO) and not _verbatim_r1(DL.FRASE_DEI_A_ESCALA + " ... xyzzy 4711"), "corpus_nao_vazio": len(_arqs_r1) >= 23 and len(_NC_R1) > 1000,\n'
    '           "as_pedras_do_bundle_foram_varridas": sorted(os.path.basename(p_) for p_ in _ped_r1) == sorted(os.path.basename(r_) for r_ in DL.BUNDLE_RELS)}\n'
    'R["varredura_estrita_das_pedras_r1"] = {"n_pedras": len(_ped_r1), "n_passagens": _n_r1, "n_verbatim": _n_r1 - len(_rep_r1), "reprovadas": _rep_r1, "controle_negativo": _ctl_r1, "corpus_arquivos": len(_arqs_r1),\n'
    '                                        "regra": "toda passagem entre aspas angulares nas pedras e\' fala verbatim do operador (espacos colapsados, minusculas, reticencias por pedaco); o resto usa aspas tipograficas"}\n'
    'ok = ok and not _rep_r1 and _n_r1 > 0 and all(_ctl_r1.values())\n')
t = t.replace(a, novo)
nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8"); ast.parse(nb)
open(P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_pre_r1_a5", "wb").write(b0)
open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb) > len(b0); os.replace(P + ".tmp", P)
print("conferir_citacoes_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(b0).hexdigest()[:16], "->", hashlib.sha256(nb).hexdigest()[:16])
