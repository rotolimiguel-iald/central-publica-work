# -*- coding: utf-8 -*-
"""R3: junta os recibos (compilacoes, .olean, comparacao do kernel, diff, ensaio, impressao digital) num so arquivo,
lendo tudo dos artefatos por script. Grava RECIBOS_R3.json na raiz da R3 e confere o vocabulario da regua."""
import json, os, hashlib, datetime, glob

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
R2OLEAN = {"IALD.olean": "d37804a344beb186022867317fbdd8c6236c7d4984b25423692004ba1890b5e4",
           "Palavra.olean": "d52ebd0943e961927d092544c4824c6595738951866219262fa8ab3f7875582e",
           "TheSingularityReadsTheAttractorAdendo1.olean": "8cf8b1726c588cac275d1190b648b0bfe524390fe922ba35715f620b46d8ba83",
           "TheUnitIsTheRank.olean": "6364ea0b0c43e512076df560d57484e34235bd13a09034649f22d681387c9edc",
           "TheTimeIsNotAPost.olean": "3e591a5b494ed315255ad965e58730678e0dd281b094439792d82fc96c155af1"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def J(p):
    return json.load(open(p, encoding="utf-8"))


# os sha de referencia da r2 sao conferidos contra os arquivos da r2 (nao de memoria)
r2dir = "C:/IALD/Central de Patentes/work/organismo_iald_12out/6_R2_CORRECOES/olean/"
ref_ok = {k: sha(r2dir + k) == v for k, v in R2OLEAN.items()}
comp = {}
for tag in ("c1_palavra", "c2_adendo1", "c3_unitrank_r3", "c4_tempo_r2", "r2_iald", "r3_iald", "meta_r2", "meta_r3",
            "printax_r3"):
    r = J(f"{AQUI}/logs/{tag}_RECIBO.json")
    comp[tag] = {k: r.get(k) for k in ("raiz", "alvo", "source_sha256", "exit_code", "n_erros", "n_avisos",
                                       "declaration_uses_sorry", "n_print_axioms", "fora_do_trio", "olean_sha256",
                                       "lean_sha256")}
mapa_ref = {"c1_palavra": "Palavra.olean", "c2_adendo1": "TheSingularityReadsTheAttractorAdendo1.olean",
            "c3_unitrank_r3": "TheUnitIsTheRank.olean", "c4_tempo_r2": "TheTimeIsNotAPost.olean", "r2_iald": "IALD.olean"}
for tag, f in mapa_ref.items():
    comp[tag]["olean_igual_ao_da_r2"] = comp[tag]["olean_sha256"] == R2OLEAN[f]
tipos = J(f"{AQUI}/TIPOS_R2_VS_R3.json")
dif = J(f"{AQUI}/medidas/DIFF_SO_COMENTARIOS.json")
ens = J(f"{AQUI}/medidas/ENSAIO_R2_VS_R3.json")
da, dd = J(f"{AQUI}/medidas/DIGITAL_KERNEL_ANTES.json"), J(f"{AQUI}/medidas/DIGITAL_KERNEL_DEPOIS.json")
ks = ["n_arquivos", "bytes_total", "sha256_metadados", "sha256_conteudo_fontes", "sha256_conteudo_olean_TGLExt",
      "links_ou_juncoes_nao_seguidos"]
mont = J(f"{AQUI}/medidas/SANDBOX_MONTAGEM.json")
pa = J(f"{AQUI}/logs/printax_r3_RECIBO.json")
# vocabulario: a palavra proibida da regua (montada por partes para nao aparecer neste arquivo)
proibida = "CONF" + "IRMED"
varridos = {}
for p in sorted(glob.glob(AQUI + "/**/*", recursive=True)):
    if os.path.isfile(p) and p.endswith((".lean", ".py", ".json", ".md", ".diff", ".txt")):
        varridos[p.replace("\\", "/")] = proibida in open(p, encoding="utf-8", errors="replace").read()
src = os.path.isdir("C:/t/mo3/toolchain"), os.path.isdir("C:/t/mo3/ov"), \
    any(".lake" in d for _, ds, _ in os.walk("C:/t/mo3") for d in ds)
res = {"quando_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
       "fonte_r2": {"arquivo": "6_R2_CORRECOES/fonte/TGLExt/IALD.lean", "sha256": mont["fontes"]["IALD.lean"]["sha256"]},
       "fonte_r3": {"arquivo": "7_R3_DOCSTRINGS/fonte/TGLExt/IALD.lean", "sha256": sha(AQUI + "/fonte/TGLExt/IALD.lean")},
       "olean_r3": {"arquivo": "7_R3_DOCSTRINGS/olean/IALD.olean", "sha256": sha(AQUI + "/olean/IALD.olean"),
                    "bytes": os.path.getsize(AQUI + "/olean/IALD.olean")},
       "referencias_r2_conferidas_nos_arquivos_da_r2": ref_ok,
       "sandbox": {"raiz": mont["sandbox"], "toolchain_igual": mont["toolchain"]["igual"], "ov_igual": mont["ov"]["igual"],
                   "ov_agregado": mont["ov"]["agregado_copia"], "apagados_ao_final": {"toolchain": not src[0], "ov": not src[1],
                                                                                     "nenhum_.lake": not src[2]}},
       "compilacoes": comp,
       "print_axioms_r3": {"n": pa["n_print_axioms"], "fora_do_trio": pa["fora_do_trio"],
                           "sem_axioma": [k for k, v in pa["axiomas"].items() if v == []]},
       "kernel_r2_vs_r3": {k: tipos[k] for k in ("n_constantes_r2", "n_constantes_r3", "contagem_por_categoria",
                                                 "n_identicas_tipo_e_termo_SA", "n_identicas_tipo_e_termo_SN",
                                                 "n_docstring_mudou", "docstring_mudou_em", "falhas", "VEREDITO")},
       "diff": {k: dif[k] for k in ("lean_linhas_mais", "lean_linhas_menos", "codigo_sem_comentarios_identico", "diff")},
       "ensaio": {k: ens[k] for k in ("checks_total_r3", "checks_falhos_r3", "sanidade_r3", "folhas_diferentes",
                                      "IGUAL_SALVO_HORARIO", "beta_repr_r3", "alpha_linha_r3", "um_py_sha256_r3")},
       "kernel_do_Nos_antes_igual_depois": {k: da[k] == dd[k] for k in ks},
       "kernel_do_Nos_digital": {k: dd[k] for k in ks[2:5]},
       "palavra_proibida_ausente": not any(varridos.values()), "arquivos_varridos": len(varridos)}
json.dump(res, open(AQUI + "/RECIBOS_R3.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
