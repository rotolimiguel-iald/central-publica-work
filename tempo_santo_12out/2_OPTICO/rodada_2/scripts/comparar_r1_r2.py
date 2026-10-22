"""Comparacao (so leitura) da rodada 1 com a rodada 2 da face otica F1.TEMPO.
Nao altera nenhum veredito; nao substitui a rodada 1. Uso:
  python -E -P -X utf8 comparar_r1_r2.py <R1_RESULTADO.json> <R2_RESULTADO.json> <saida.json>"""
import hashlib
import json
import os
import sys


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


p1, p2, saida = sys.argv[1:4]
r1 = json.load(open(p1, encoding="utf-8"))
r2 = json.load(open(p2, encoding="utf-8"))
out = {"documento": "COMPARACAO rodada 1 x rodada 2 — F1.TEMPO, face otica",
       "estatuto": "[REAL — lido dos dois arquivos de resultado por script]; nenhuma das rodadas substitui a outra; as duas se preservam",
       "rodada_1": {"arquivo": os.path.abspath(p1), "sha256": sha(p1)},
       "rodada_2": {"arquivo": os.path.abspath(p2), "sha256": sha(p2)},
       "subitens": {}, "controles": {}, "por_afirmacao_face_otica": {}, "numeros_chave": {}}
for sid in sorted(set(r1["subitens_oticos"]) | set(r2["subitens_oticos"])):
    a, b = r1["subitens_oticos"].get(sid, {}), r2["subitens_oticos"].get(sid, {})
    out["subitens"][sid] = {
        "r1": a.get("resultado"), "r2": b.get("resultado"), "mesmo_resultado": a.get("resultado") == b.get("resultado"),
        "r1_n_criterios": a.get("n_criterios"), "r2_n_criterios": b.get("n_criterios"),
        "r1_fora_da_tolerancia": [c["nome"] for c in a.get("criterios", []) if not c.get("ok")],
        "r2_fora_da_tolerancia": [c["nome"] for c in b.get("criterios", []) if not c.get("ok")]}
for cid in sorted(set(r1["controles_oticos"]) | set(r2["controles_oticos"])):
    a, b = r1["controles_oticos"].get(cid, {}), r2["controles_oticos"].get(cid, {})
    out["controles"][cid] = {"r1": a.get("comportou_se_como_registrado"), "r2": b.get("comportou_se_como_registrado"),
                             "iguais": a.get("comportou_se_como_registrado") == b.get("comportou_se_como_registrado")}
for af in sorted(set(r1["por_afirmacao_face_otica"]) | set(r2["por_afirmacao_face_otica"]), key=lambda s: int(s[1:])):
    a, b = r1["por_afirmacao_face_otica"].get(af, {}), r2["por_afirmacao_face_otica"].get(af, {})
    out["por_afirmacao_face_otica"][af] = {"r1": a.get("resultado_da_face_otica"), "r2": b.get("resultado_da_face_otica"),
                                           "iguais": a.get("resultado_da_face_otica") == b.get("resultado_da_face_otica")}
k = out["numeros_chave"]
k["beta_runtime"] = {"r1": r1["beta"]["beta_runtime"], "r2": r2["beta"]["beta_runtime"]}
k["beta_bits_iguais"] = r1["beta"]["beta_runtime"] == r2["beta"]["beta_runtime"]
k["T_do_modelo"] = {"r1": r1["modelo"]["T"], "r2": r2["modelo"]["T"], "bits_iguais": r1["modelo"]["T"] == r2["modelo"]["T"]}
c1 = r1["subitens_oticos"]["T9.o"]["medidas"]["c"]
c2 = r2["subitens_oticos"]["T9.o"]["medidas"]["c"]
k["T9.o(c) entradas: max_k<=10^4 max_ij dif"] = {"r1": c1.get("entradas_max_dif"), "r2": c2.get("entradas_max_dif"),
                                                 "bits_iguais": c1.get("entradas_max_dif") == c2.get("entradas_max_dif"),
                                                 "k_do_max": {"r1": c1.get("k_do_max"), "r2": c2.get("k_do_max")}}
k["T9.o(c) s_min rel max (k<=500)"] = {"r1": c1.get("sv_rel_max"), "r2": c2.get("sv_rel_max_k<=500")}
i1 = r1["subitens_oticos"]["T9.o"]["informativo_sem_veredito"]
i2 = r2["subitens_oticos"]["T9.o"]["informativo_sem_veredito"]
k["T9.o informativo: primeiro k com posto numerico 1"] = {"r1": i1.get("c_primeiro_k_posto_numerico_cai_a_1"),
                                                         "r2": i2.get("(c) primeiro k em que o posto numerico cai a 1 [sem veredito]")}
j1 = r1["subitens_oticos"]["T8.o"]["informativo_sem_veredito"]
j2 = r2["subitens_oticos"]["T8.o"]["informativo_sem_veredito"]
k["T8.o informativo: primeiro k com c_k < 1e-15"] = {"r1": j1.get("b_primeiro_k_contraste_float64_abaixo_de_1e-15"),
                                                     "r2": j2.get("(b) primeiro k com c_k < 1e-15 em float64 [sem veredito]")}
k["impressao_digital_kernel_iguais"] = {"r1": r1["impressao_digital_kernel"]["iguais"], "r2": r2["impressao_digital_kernel"]["iguais"],
                                        "mesma_meta_e_src": r1["impressao_digital_kernel"]["fim"]["meta_sha256"] == r2["impressao_digital_kernel"]["fim"]["meta_sha256"]
                                        and r1["impressao_digital_kernel"]["fim"]["src_sha256"] == r2["impressao_digital_kernel"]["fim"]["src_sha256"]}
out["todos_os_subitens_com_mesmo_resultado"] = all(v["mesmo_resultado"] for v in out["subitens"].values())
out["todos_os_controles_iguais"] = all(v["iguais"] for v in out["controles"].values())
out["todas_as_afirmacoes_iguais"] = all(v["iguais"] for v in out["por_afirmacao_face_otica"].values())
tmp = saida + ".tmp"
json.dump(out, open(tmp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
os.replace(tmp, saida)
print(json.dumps({x: out[x] for x in ("todos_os_subitens_com_mesmo_resultado", "todos_os_controles_iguais", "todas_as_afirmacoes_iguais")}))
print(json.dumps(out["numeros_chave"], ensure_ascii=False)[:2500])
