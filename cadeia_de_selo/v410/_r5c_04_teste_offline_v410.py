# -*- coding: utf-8 -*-
"""_r5c_04_teste_offline_v410.py -- a REVISAO DO CONSTRUTOR, parte 4 (10/11/2026): um controle negativo a mais em _teste_aescala_offline_v410.py para a regra nova da c8 (a errata E36, no nucleo do texto, vem sempre com a clausula do limite na mesma folha):
tirar a clausula da folha do «diz» que traz a E36 tem de reprovar a c8, e so' ela. Idempotente; backup de BYTES; temporario + os.replace; ast.parse."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")
p = os.path.join(HERE, "_teste_aescala_offline_v410.py"); b0 = open(p, "rb").read(); t = b0.decode("utf-8")
NOVO = ('T40 = copy.deepcopy(TXT); _i40 = [i_ for i_, x_ in enumerate(T40["diz"]) if DL.FRASE_E36_PT in x_]; assert len(_i40) == 1 and DL.CLAUSULA_Z_PT in T40["diz"][_i40[0]]; T40["diz"][_i40[0]] = DL.FRASE_E36_PT   # (revisao do construtor) a E36 sozinha na folha, sem a clausula do limite\n'
        'RTA._V410_AESCALA_TEXT = T40; r_ = RTA.a_escala_v410(core_de_ensaio()); R["r5_errata_e36_sem_a_clausula_do_limite_na_folha"] = (r_["verdict"], _f(r_)); RTA._V410_AESCALA_TEXT = TXT\n')
ANC = "for k, (vd, fl) in R.items():\n"
if "r5_errata_e36_sem_a_clausula_do_limite_na_folha" not in t:
    nl = "\r\n" if "\r\n" in t else "\n"
    anc = ANC.replace("\n", nl); assert t.count(anc) == 1, t.count(anc)
    t = t.replace(anc, NOVO.replace("\n", nl) + anc)
    a2 = '"r5_um_ratificado_retirado": ["c11"]}'; assert t.count(a2) == 1
    t = t.replace(a2, '"r5_um_ratificado_retirado": ["c11"], "r5_errata_e36_sem_a_clausula_do_limite_na_folha": ["c8"]}')
    a3 = "ok_neg = all(set(esp[k]) & set(R[k][1]) and \"MECHANICS_CHECK_FAILED\" in R[k][0] for k in esp) and "; assert t.count(a3) == 1
    t = t.replace(a3, a3 + 'R["r5_errata_e36_sem_a_clausula_do_limite_na_folha"][1] == ["c8"] and ')
b1 = t.encode("utf-8")
if b1 != b0:
    ast.parse(t); bak = p + ".bak_" + TS + "_r5c4"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
    tmp = p + ".tmp_r5c"; open(tmp, "wb").write(b1); assert os.path.getsize(tmp) == len(b1) > 0; os.replace(tmp, p); assert open(p, "rb").read() == b1
print("_teste_aescala_offline_v410.py:", "MUDOU" if b1 != b0 else "igual")
