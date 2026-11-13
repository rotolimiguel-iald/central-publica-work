import copy, json, sys
src = open("a_a3.py", encoding="utf-8").read().split("rep = {}")[0]
exec(compile(src, "a_a3_head", "exec"))
ab = blob("abertura_v411.py").decode("utf-8")
rep = {}
for nome, campo, val in (("N16_abrir_devolve_z_null_NaN", "z_null", "float('nan')"), ("N17_abrir_devolve_z_tgl_inf", "z_tgl", "float('inf')"), ("N18_abrir_devolve_z_null_menos_inf", "z_null", "float('-inf')")):
    ab2 = ab + "\n\n_orig_abrir_revA = abrir\n\ndef abrir(*a, **k):\n    r = _orig_abrir_revA(*a, **k)\n    r['estatistica']['%s'][0] = %s\n    return r\n" % (campo, val)
    Cc, I = trocar_blob("abertura_v411.py", ab2.encode("utf-8"))
    o = rodar(copy.deepcopy(core0), contr_=Cc, ins_=I)
    rep[nome] = resumo(o); print(nome, rep[nome])
    v = (o.get("values") or {}).get("guarda_de_finitude")
    print("    guarda_de_finitude:", v)
json.dump(rep, open(os.path.join(a_lib.OUT, "a3_parte3.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
