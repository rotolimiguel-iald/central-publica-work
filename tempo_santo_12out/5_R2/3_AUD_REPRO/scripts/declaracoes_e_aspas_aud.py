# -*- coding: utf-8 -*-
"""Tabela de declaracoes R1 -> R2 (parser PROPRIO do auditor) + conferencia de aspas/frases proibidas (propria).
Compara com TABELA_DECLARACOES_R2.json do construtor. So leitura. Uso: ... <saida.json>"""
import hashlib
import json
import re
import sys

W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
R1 = W + r"\3_KERNEL\sandbox\TheTimeHasNoRank.lean"
R2 = W + r"\5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.lean"
TAB = W + r"\5_R2\1_PEDRA\saidas\TABELA_DECLARACOES_R2.json"
PRE = W + r"\1_PREREGISTRO\PREREGISTRO.json"
VERB = {
    "12out_rank_e_tempo_santo": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
    "05out_VERBO": r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\VERBO_operador_05out.txt",
    "05out_RESPOSTAS": r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\RESPOSTAS_operador_05out.txt",
    "10out_POSTO_RANK": r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt",
}
RENOMES = {"time_is_the_modular_flow": "modular_flow_is_a_kms_group", "the_time_has_no_rank": "the_time_is_not_a_post",
           "probe_the_time_has_no_rank": "probe_the_time_is_not_a_post",
           "optical_attractor_is_the_absolute_one": "half_identity_is_absoluteRho_two",
           "optical_attractor_clock_stops": "half_identity_clock_stops"}
REMOVIDAS = {"the_absolute_one_has_no_clock"}
DECL = re.compile(r"^(?:noncomputable\s+)?(theorem|def|lemma|instance|abbrev|structure)\s+([^\s:({\[]+)", re.M)


def decls(path):
    txt = open(path, encoding="utf-8").read()
    out = []
    for m in DECL.finditer(txt):
        out.append((m.group(2), m.group(1), txt.count("\n", 0, m.start()) + 1))
    return txt, out


t1, d1 = decls(R1)
t2, d2 = decls(R2)
n1 = {n: (k, l) for n, k, l in d1}
n2 = {n: (k, l) for n, k, l in d2}
classes = {"mantida": [], "renomeada": [], "removida": [], "nova": []}
for n in n1:
    if n in n2:
        classes["mantida"].append(n)
    elif n in RENOMES and RENOMES[n] in n2:
        classes["renomeada"].append((n, RENOMES[n]))
    else:
        classes["removida"].append(n)
cobertas = set(n1) | set(RENOMES.values())
for n in n2:
    if n not in cobertas:
        classes["nova"].append(n)
tab = json.load(open(TAB, encoding="utf-8"))["tabela"]
tab_cls = {}
for e in tab:
    tab_cls.setdefault(e["classe"].split(" ")[0], []).append(e.get("R2") or e.get("R1"))
res = {"R1": {"arquivo": R1, "sha256": hashlib.sha256(open(R1, "rb").read()).hexdigest(), "n_declaracoes_nomeadas": len(d1),
              "n_examples": len(re.findall(r"^example", t1, re.M)), "n_print_axioms": t1.count("#print axioms ")},
       "R2": {"arquivo": R2, "sha256": hashlib.sha256(open(R2, "rb").read()).hexdigest(), "n_declaracoes_nomeadas": len(d2),
              "n_examples": len(re.findall(r"^example", t2, re.M)), "n_print_axioms": t2.count("#print axioms ")},
       "classes_proprias": {"mantida": len(classes["mantida"]), "renomeada": len(classes["renomeada"]),
                            "removida": len(classes["removida"]), "nova": len(classes["nova"])},
       "renomeadas_proprias": classes["renomeada"], "removidas_proprias": classes["removida"], "novas_proprias": sorted(classes["nova"]),
       "classes_do_construtor": {k: len(v) for k, v in tab_cls.items()}}
res["renomeadas_batem_com_ADENDO"] = sorted(a for a, _ in classes["renomeada"]) == sorted(RENOMES)
res["removidas_batem_com_ADENDO"] = set(classes["removida"]) == REMOVIDAS
res["novas_batem_com_construtor"] = sorted(classes["nova"]) == sorted(tab_cls.get("nova", []))
res["mantidas_batem_com_construtor"] = sorted(classes["mantida"]) == sorted(tab_cls.get("mantida", []))
# todo nome com #print axioms na R2 e declaracao nomeada da R2, e vice-versa
pa2 = set(re.findall(r"^#print axioms TGLExt\.TheTimeIsNotAPost\.(\S+)", t2, re.M))
res["print_axioms_R2_cobre_todas_as_nomeadas"] = pa2 == set(n2)
res["print_axioms_R2_faltantes"] = sorted(set(n2) - pa2)
res["print_axioms_R2_extras"] = sorted(pa2 - set(n2))
# o que o ADENDO manda: ausencia de 'True' como tipo de probe_bounded_spectral_translation; _hd; kappa ne 0 em clock_reads_modulo_period
res["E5.09_probe_bounded_spectral_translation_True_ausente"] = "theorem probe_bounded_spectral_translation : True" not in t2
res["E5.11__hd_ausente_em_purityR_modular"] = re.search(r"theorem purityR_modular[^\n]*\n?[^\n]*_hd", t2) is None
m = re.search(r"theorem clock_reads_modulo_period([^:]*):", t2)
res["E5.12_clock_reads_modulo_period_assinatura"] = m.group(1).strip() if m else None
res["E5.12_sem_kappa_ne_0"] = (m is not None) and ("≠ 0" not in m.group(1))
res["E5.10_re_export_duplicado_ausente"] = "the_absolute_one_has_no_clock" not in t2
res["grep_sorry"] = len(re.findall(r"\bsorry\b", t2))
res["grep_admit_"] = len(re.findall(r"\badmit\b", t2))
res["grep_native_decide"] = t2.count("native_decide")
res["grep_axiom_decl"] = len(re.findall(r"^axiom\s", t2, re.M))
res["namespace_R2"] = re.findall(r"^namespace (\S+)", t2, re.M)
# cobertura dos alvos do PREREGISTRO.json (theorem/def) sob o mapa de renomes
pre = json.load(open(PRE, encoding="utf-8"))
alvos = set(re.findall(r"`([A-Za-z_][A-Za-z0-9_']*)`", json.dumps(pre, ensure_ascii=False)))
alvos_decl_R1 = sorted(a for a in alvos if a in n1)
faltam = [a for a in alvos_decl_R1 if not (a in n2 or RENOMES.get(a) in n2 or a in REMOVIDAS)]
res["alvos_PREREGISTRO_que_eram_declaracoes_R1"] = len(alvos_decl_R1)
res["alvos_sem_correspondente_na_R2"] = faltam
# aspas « » na R2: substrings de bytes dos verbatins
vb = {k: open(p, "rb").read() for k, p in VERB.items()}
res["verbatins_sha16"] = {k: hashlib.sha256(v).hexdigest()[:16] for k, v in vb.items()}
aspas = sorted(set(re.findall(r"«([^»]+)»", t2)))
asp = []
for a in aspas:
    ab = a.encode("utf-8")
    hits = {k: v.count(ab) for k, v in vb.items()}
    asp.append({"aspa": a, "achada": any(hits.values()), "nos_verbatins": hits})
res["aspas_R2"] = asp
res["n_aspas_R2"] = len(aspas)
res["aspas_nao_achadas"] = [a["aspa"] for a in asp if not a["achada"]]
proib = ["o tempo é o Verbo", "não o Nome", "O tempo não tem posto", "o tempo não tem posto", "O relógio mede a sombra",
         "o relógio mede a sombra", "o atrator é onde o tempo repousa", "TheTimeHasNoRank", "the_time_has_no_rank", "no_rank", "CONFIRMED"]
res["frases_proibidas_R2"] = {p: t2.count(p) for p in proib}
res["aspas_R1_para_comparar"] = len(set(re.findall(r"«([^»]+)»", t1)))
json.dump(res, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in res.items() if k not in ("aspas_R2",)}, ensure_ascii=False, indent=1))
