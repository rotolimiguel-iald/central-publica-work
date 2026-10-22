# -*- coding: utf-8 -*-
"""emular_soma_textos.py -- DELTA 19/10: a checagem de SOMA que os textos do pos-rito (pos_rito\\textos_v394.py::_d) fazem sobre os ESPERADOS, emulada em modo ensaio, SO' LEITURA (nao importa nem toca pos_rito):
  (a) a formula ORIGINAL:  n_out_flags = n_bandeiras_novas - (n_formais.tempo + n_formais.quadratica + n_formais.rede);  assert n_out_flags >= 0 and (n_out_flags == 0 or houver modulo de outro grupo)
  (b) a formula PROPOSTA (pos_rito_PROPOSTA_delta19.diff): as bandeiras POR GRUPO (ESPERADOS.n_bandeiras_por_grupo) somam n_bandeiras_novas.
Tambem emula as outras contagens de _d: modulos novos == pedras == ESPERADOS.kernel.modulos_novos; cdx.decl == n_formais.tempo; rede_fontes == modulos F1Fecho394 da lista; e a escada: 7045 + n_bandeiras_novas == escada.
uso: python -I -B -X utf8 emular_soma_textos.py"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
esp = json.load(open(os.path.join(V, "ESPERADOS_v394.json"), encoding="utf-8")); nf = esp["n_formais"]
cdx_decl = json.load(open(os.path.join(V, "insumos", "RESULTADO_V394_CANDIDATA_R2.json"), encoding="utf-8"))["counts"]["new_formal_declarations"]
mods = ["TGLExt." + p[len("TGLExt/"):-len(".lean")].replace("/", ".") for p in esp["pedras_sha256"]]
tg = [m for m in mods if m.startswith("TGLExt.TimeGraviton")]; rq = [m for m in mods if m == "TGLExt.RuleQuadraticResidual"]; f1 = [m for m in mods if m.startswith("TGLExt.F1Fecho394.")]
outros = [m for m in mods if m not in tg + rq + f1]
R = {"modulos": {"total": len(mods), "tempo": len(tg), "quadratica": len(rq), "rede": len(f1), "outros": outros, "esperados_kernel_modulos_novos": esp["kernel"]["modulos_novos"],
                 "fecha": len(tg) + len(rq) + len(f1) + len(outros) == len(mods) == esp["kernel"]["modulos_novos"] and len(rq) == 1 and len(f1) == nf["rede_fontes"] and cdx_decl == nf["tempo"]}}
n_out_orig = esp["n_bandeiras_novas"] - (nf["tempo"] + nf["quadratica"] + nf["rede"])
R["formula_original"] = {"n_bandeiras_novas": esp["n_bandeiras_novas"], "n_formais(contrato do Codex)": {k: nf[k] for k in ("tempo", "quadratica", "rede")}, "n_out_flags": n_out_orig, "assert_passa": bool(n_out_orig >= 0 and (n_out_orig == 0 or outros)),
                         "nota": "com a politica so'-nomeadas as bandeiras (%d) deixam de coincidir com as declaracoes de contrato do Codex (%d); a formula original da' negativo e o assert recusa" % (esp["n_bandeiras_novas"], nf["tempo"] + nf["quadratica"] + nf["rede"])}
bg = esp.get("n_bandeiras_por_grupo")
R["formula_proposta"] = {"n_bandeiras_por_grupo": bg, "soma": sum(bg.values()) if bg else None, "assert_passa": bool(bg and sum(bg.values()) == esp["n_bandeiras_novas"] and bg["outros"] >= 0 and (bg["outros"] == 0 or outros) and bg["outros"] == len(outros) * 1)}
R["escada"] = {"v393": esp["escada_v393_e_v394"][0], "bandeiras_novas": esp["n_bandeiras_novas"], "soma": esp["escada_v393_e_v394"][0] + esp["n_bandeiras_novas"], "escada_esperada": esp["escada"][1], "fecha": esp["escada_v393_e_v394"][0] + esp["n_bandeiras_novas"] == esp["escada"][1]}
R["h8"] = {"entradas": esp["h8_entradas"], "residuais": esp["h8_residuais_do_nos"], "embutidos": esp["formal_files_n"], "fecha": esp["h8_entradas"] == esp["formal_files_n"] + len(esp["h8_residuais_do_nos"])}
json.dump(R, open(os.path.join(V, "delta_19out", "SOMA_TEXTOS_POS_RITO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1))
sys.exit(0 if (R["modulos"]["fecha"] and R["formula_proposta"]["assert_passa"] and R["escada"]["fecha"] and R["h8"]["fecha"]) else 1)
