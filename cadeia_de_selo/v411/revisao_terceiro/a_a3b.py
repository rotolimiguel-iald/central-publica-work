"""A3 parte 2: mais controles negativos sobre o codigo embutido (dado alterado de verdade; codigo publicado adulterado com pinos refeitos; funcao congelada trocada; texto proibido; beta; gate; caminho vedado)."""
import copy, io, json, base64, sys, time
src = open("a_a3.py", encoding="utf-8").read().split("rep = {}")[0]
exec(compile(src, "a_a3_head", "exec"))
import numpy as np
rep = {}


def reg(nome, o):
    rep[nome] = resumo(o); print(nome, rep[nome]); sys.stdout.flush()


b = blob("vetor_y255.npz")
chave = json.loads(blob("PINOS_DE_PRODUCAO.json").decode("utf-8"))["vetor"]["chave"]
npz = np.load(io.BytesIO(b), allow_pickle=False); arr = {k: npz[k] for k in npz.files}
y = np.array(arr[chave], dtype=float); y[3] += 1e-3; a2 = dict(arr); a2[chave] = y
buf = io.BytesIO(); np.savez(buf, **a2)
Cc, I = trocar_blob("vetor_y255.npz", buf.getvalue())
reg("N1c_vetor_com_um_elemento_mudado_pinos_refeitos", rodar(copy.deepcopy(core0), contr_=Cc, ins_=I))
# N5: a abertura PUBLICADA adulterada (soma 1e-3 ao z_null), pinos refeitos de ponta a ponta -> o recalculo roda o codigo embutido
ab = blob("abertura_v411.py").decode("utf-8")
ab2 = ab + "\n\n_orig_abrir_revA = abrir\n\ndef abrir(*a, **k):\n    r = _orig_abrir_revA(*a, **k)\n    r['estatistica']['z_null'][0] = float(r['estatistica']['z_null'][0]) + 1e-3\n    return r\n"
Cc, I = trocar_blob("abertura_v411.py", ab2.encode("utf-8"))
reg("N5_abertura_publicada_adulterada_pinos_refeitos", rodar(copy.deepcopy(core0), contr_=Cc, ins_=I))
# N5b: sem refazer os pinos -> recusa no decode
Cc, I = trocar_blob("abertura_v411.py", ab2.encode("utf-8"), refrescar_pinos=False, refrescar_contrato=False)
reg("N5b_abertura_adulterada_sem_refazer_pinos", rodar(copy.deepcopy(core0), contr_=Cc, ins_=I))
# N6: o veredito pinado adulterado (devolve sempre o ramo 5) com pinos refeitos
ve = blob("veredito_v411.py").decode("utf-8")
ve2 = ve + "\n\n_orig_ver_revA = veredito_h0dn_v411\n\ndef veredito_h0dn_v411(*a, **k):\n    r = list(_orig_ver_revA(*a, **k))\n    r[2] = 5\n    return tuple(r)\n"
Cc, I = trocar_blob("veredito_v411.py", ve2.encode("utf-8"))
reg("N6_veredito_pinado_adulterado_pinos_refeitos", rodar(copy.deepcopy(core0), contr_=Cc, ins_=I))
# N8: a funcao CONGELADA da v410 trocada por uma que devolve o ramo 4 para tudo (c11 (a) tem de cair)
reg("N8_funcao_congelada_da_v410_trocada", rodar(copy.deepcopy(core0), trocar={"veredito_h0dn": (lambda *a, **k: ("X", "NOT_FALSIFIED", 4))}))
# N9: texto proibido no texto do registro
txt_b = copy.deepcopy(TXT); txt_b["diz"] = list(txt_b["diz"]) + ["o teste tem poder certificado e e' um teste cego"]
reg("N9_texto_com_frase_proibida", rodar(copy.deepcopy(core0), txt_=txt_b))
txt_b = copy.deepcopy(TXT); txt_b["diz"] = list(txt_b["diz"]) + ["beta = 0,0120313"]
reg("N9b_texto_com_beta_literal", rodar(copy.deepcopy(core0), txt_=txt_b))
txt_b = copy.deepcopy(TXT); txt_b["diz"] = list(txt_b["diz"]) + ["a TGL foi confirmada"]
reg("N9c_texto_com_a_palavra_da_creditacao", rodar(copy.deepcopy(core0), txt_=txt_b))
# N10: beta do core trocado
cb = copy.deepcopy(core0); cb["beta"] = cb["beta"] * 1.01
reg("N10_beta_do_core_trocado", rodar(cb))
# N11: gate trocado; escada trocada
cg = copy.deepcopy(core0); cg["qg_closure"]["gate"]["verdict"] = "TGL_OUTRO_GATE"
reg("N11_gate_trocado", rodar(cg))
ce = copy.deepcopy(core0); ce["external_ladder"]["n_theorems_expected"] = int(ce["external_ladder"]["n_theorems_expected"]) + 1
reg("N11b_escada_trocada", rodar(ce))
# N12: caminho tocado sob a pasta vedada (chamada direta da mecanica)
bt = f.chamar(ns, "_v398_beta", copy.deepcopy(core0))[0]
toc = ["C:\\IALD\\Central de Patentes\\work\\h0dn_bg1_v410_09nov\\kimi\\qualquer.json"]
m = f.chamar(ns, "v411_h0dn_mechanics", bt, copy.deepcopy(core0), CONTR, TXT, None, None, toc)
rep["N12_caminho_sob_kimi"] = {"passed": m["passed"], "falhas": [c["id"] for c in m["checks"] if not c["ok"]], "recusou": not m["passed"]}; print("N12", rep["N12_caminho_sob_kimi"])
m = f.chamar(ns, "v411_h0dn_mechanics", bt, copy.deepcopy(core0), CONTR, TXT, None, None, None)
rep["N12b_tocados_none"] = {"passed": m["passed"], "falhas": [c["id"] for c in m["checks"] if not c["ok"]], "recusou": not m["passed"]}; print("N12b", rep["N12b_tocados_none"])
# N13: ressalvas: o pre-registro embutido sem a secao 8 numerada -> as 7 ressalvas nao saem (passed exige 7); e o K da v410 trocado
ck = copy.deepcopy(core0); ck["h0dn_bg1_v410"]["values"]["K"] = ck["h0dn_bg1_v410"]["values"]["K"] * (1 + 1e-9)
reg("N13_K_da_v410_trocado_1e-9", rodar(ck))
# N14: sem o registro da v410 no core (c10/c14)
cs = copy.deepcopy(core0); cs.pop("h0dn_bg1_v410", None)
reg("N14_sem_o_registro_h0dn_v410_no_core", rodar(cs))
# N15: v387 sem o token selado
c3 = copy.deepcopy(core0); c3["three_stress_tests_v387"]["verdict"] = c3["three_stress_tests_v387"]["verdict"].replace("P2_NOT_DETERMINED", "P2_OUTRA_COISA")
o = rodar(c3); reg("N15_v387_sem_o_token", o); rep["N15_v387_sem_o_token"]["p2_ao_lado"] = o.get("p2_ao_lado_da_v387")
json.dump(rep, open(os.path.join(a_lib.OUT, "a3_parte2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("fim parte 2")
