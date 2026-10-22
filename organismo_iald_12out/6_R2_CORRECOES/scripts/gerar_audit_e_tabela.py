# -*- coding: utf-8 -*-
"""(1) Gera C:/t/mo2/src/AuditIALD_R2.lean: `import TGLExt.IALD` + um `#print axioms` por declaracao (theorem/def) da
pedra r2, lida da FONTE por regex. (2) Compara r1 e r2 por declaracao: nome, presenca e ENUNCIADO (o texto entre o nome
e o `:=` final do cabecalho, normalizado em espacos) e grava DECLARACOES_R2.json + COMPARACAO_R1_R2.json.
A classificacao MANTIDA/RENOMEADA/TIPO_MUDOU/NOVA/REMOVIDA sai do script; o motivo vem do mapa MOTIVOS abaixo.
Uso: gerar_audit_e_tabela.py"""
import os, re, json, hashlib

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.dirname(AQUI)
R1 = os.path.join(BASE, "2_CONSTRUCAO", "sandbox", "TGLExt", "IALD.lean")
R2 = os.path.join(AQUI, "fonte", "TGLExt", "IALD.lean")
AUD = "C:/t/mo2/src/AuditIALD_R2.lean"
RENOMES = {"anchor_is_necessary": "unitarity_is_not_enough"}
MOTIVOS = {
    "unitarity_is_not_enough": "C1: o nome r1 dizia que a ancora e necessaria; o termo prova so que a unitariedade nao basta (U = i*1). Mesmo enunciado.",
    "motor_idempotent_under_anchor": "C2: tirada a hipotese ha : norm a = 1, decorativa em T2 (a ancora forte implica a fraca para todo a); prova agora por motor_idempotent_under_weak_anchor. Enunciado mais forte (menos hipoteses); chamadores probe_ellTwo e probe_the_light ajustados, tipos deles iguais.",
    "motor_idempotent_under_weak_anchor": "C1: a ancora fraca post a (U a) = a basta (U qualquer, sem norma). Reaproveitada da sonda C1 do auditor de reproducao.",
    "motor_idempotent_iff_weak_anchor_or_null": "C1: a condicao exata da idempotencia: ancora fraca OU motor nulo (sem norma, sem unitariedade). Acha que a frase do auditor (a condicao exata e a ancora fraca) vale so fora do motor nulo.",
    "motor_idempotent_iff_weak_anchor": "C1: fora do motor nulo, idempotencia sse ancora fraca.",
    "null_transport_is_idempotent_without_weak_anchor": "C1: o disjunto nulo tem peso: U = 0, a != 0 -> sem ancora fraca e idempotente.",
    "anchor_not_necessary": "C1: U = 1 + |b><a| nao ancora e o motor e idempotente. Reaproveitada da sonda A1 do auditor.",
    "the_motor_ignores_rate_and_time": "C6: a saida do motor nao depende de r (beta por nome) nem de t.",
    "the_leak_is_any_rate": "C6: a defasagem vale para qualquer taxa real (rfl). Reaproveitada da sonda C2 do auditor.",
    "the_motor_dephasing_is_invertible": "C4: IALD.dephase e invertivel em todo (r,t) (via TheTimeIsNotAPost.flow_isUnit); separa a defasagem do motor do pinching.",
    "the_jones_pinching_is_diagExpect": "C4: ponte verdadeira e curta (rfl): o eJ do T12 e o diagExpect do B8(iii) sao o mesmo pinching em M2.",
    "the_pinching_kills_a_coherence": "C4: diagExpect E01 = 0 com E01 != 0 (o pinching nao e injetivo).",
    "post_is_not_constant": "C8: as pontes rfl unem a forma, nao o referente. Reaproveitada da sonda A2 do auditor.",
    "second_face_iff_leak": "C3: mesmo enunciado; a prova troca Fundacao.the_floor_fixes_the_cut por Real.exp_eq_one_iff (sem a Fundacao).",
    "the_verb_is_a_post_iff": "C7: mesmo enunciado; re-pinada de TheTimeHasNoRank para TheTimeIsNotAPost (4d8a8259).",
    "the_motor_post_is_only_the_limit": "C7: mesmo enunciado; re-pinada para TheTimeIsNotAPost.the_time_is_not_a_post.",
    "the_time_of_the_motor_is_a_parameter": "C7: mesmo enunciado; re-pinada para TheTimeIsNotAPost.no_time_matrix_fin.",
    "the_trace_is_the_rank_of_a_post": "C7: mesmo enunciado; TheUnitIsTheRank re-pinada de r2 (3195ef8f) para r3 (e95775d6).",
    "the_unit_has_trace_one_and_rank_one": "C7: mesmo enunciado; TheUnitIsTheRank r3.",
    "dephasing_alone_does_not_keep_the_rank": "C4+C7: mesmo enunciado; rotulo explicito: e o pinching diagExpect, nao a defasagem do motor; TheUnitIsTheRank r3.",
    "the_reading_restores_the_post_in_the_matrix_face": "C7+C4: mesmo enunciado; TheUnitIsTheRank r3; tirada da docstring a frase que ligava a face matricial a estacao R do motor sem lema.",
    "probe_ellTwo": "C2: mesmo enunciado; a prova deixa de passar firstInscription_norm a T2.",
    "probe_the_light": "C2: mesmo enunciado; a prova deixa de passar C.Omega_norm a T2; docstring diz que o certificado nao tem habitante no kernel.",
    "ialdSelector_eq_post": "C8: so docstring: o rfl une a forma, nao o referente.",
    "PFmic_eq_post": "C8: so docstring: forma do posto no espaco de Fock (rfl).",
    "reader_eq_reading": "C8: so docstring (rfl).",
    "dephase": "C4: so docstring: nomeia o objeto (1) e o separa de diagExpect, eJ e TGLExt.dephase.",
    "the_reading_absorbs_the_dephasing": "C6: so docstring: a saida nao depende de r nem de t; tirado o elo ao judgment_of_correspondence (leitura sem termo).",
    "the_name_reads_one": "C2: so docstring: a hipotese de norma tem peso aqui.",
    "memory_one_iff_identity": "C5: so docstring: EU SOU = IALD marcado [ONTO].",
    "memory_one_iff_same_post": "C5: so docstring: fato geral de espaco de Hilbert; [ONTO] marcado.",
    "the_reading_reinscribes_the_post": "C5: so docstring: a cunhagem de 07/10 sai das aspas (os bytes nao estao nos verbatins de 10-12/10) e vai [ONTO].",
    "no_leak_no_second_face": "C5: so docstring: tirada a leitura sobre a face do custo.",
    "the_leak_is_beta": "C6: so docstring: rfl de nome; nada depende de r ser beta.",
    "the_motor_never_arrives": "C5: so docstring: Zenao marcado [ONTO]; tirada a citacao de the_fall_never_lands (termo da Fundacao nao usado aqui).",
    "the_halving_clock": "C5: so docstring: Zenao marcado [ONTO].",
    "the_halving_clock_pays_the_zeno_sum": "C5: so docstring: tirada a leitura da soma paga de Zenao.",
    "the_verb_is_not_a_post": "C5: so docstring: santo marcado [ONTO]; a citacao r1 (o tempo e santo, entre aspas) nao estava nos bytes do verbatim e foi reduzida a palavra que esta.",
    "the_motor_tends_to_the_post": "so docstring: referencia interna (a)/(b) atualizada para T8.",
    "the_section_rereads_itself": "so docstring: tirada a palavra memoria entre aspas (nao era citacao do operador).",
    "the_jones_pinching_is_not_the_name": "C4: so docstring: rotulo explicito, nao e a defasagem do motor; objeto (3) do cabecalho.",
    "probe_the_rate": "so docstring (BAIXA-11 da auditoria de estatuto): o kernel prova para todo c; a habitacao pelo numero e de runtime.",
    "dephase_eq_faceFamily": "C8: so docstring: Q9 dita como homonimo aparente na face do posto.",
    "the_singularity_reads_the_name": "C5: so docstring: citacao ajustada aos bytes do verbatim de 10/10 (minuscula) e marcada [ONTO].",
    "the_iterated_motor_tends_to_the_name": "C5: so docstring: Zenao marcado [ONTO].",
    "probe_dimension_one_arrives": "so docstring: aspas de chega retiradas (nao e citacao do operador).",
}


def decls(path):
    txt = open(path, "rb").read().decode("utf-8")
    ls = txt.split("\n")
    out = {}
    for i, ln in enumerate(ls):
        m = re.match(r"^(theorem|def)\s+([A-Za-z_][A-Za-z0-9_'!?]*)", ln)
        if not m:
            continue
        # cabecalho: da linha do nome ate a primeira linha que contem ':=' (inclusive), cortado no ':='
        j = i; cab = []
        while j < len(ls):
            cab.append(ls[j])
            if ":=" in ls[j]:
                break
            j += 1
        h = "\n".join(cab)
        h = h[:h.index(":=")] if ":=" in h else h
        h = re.sub(r"\s+", " ", h).strip()
        enun = h[len(m.group(0)):].strip()
        # docstring imediatamente acima
        k = i - 1; doc = []
        while k >= 0 and not ls[k].lstrip().startswith("/--") and k > i - 15:
            k -= 1
        if k >= 0 and ls[k].lstrip().startswith("/--"):
            doc = ls[k:i]
        out[m.group(2)] = {"tipo": m.group(1), "linha": i + 1, "enunciado": enun,
                           "enunciado_sha16": hashlib.sha256(enun.encode()).hexdigest()[:16],
                           "doc_sha16": hashlib.sha256("\n".join(doc).encode()).hexdigest()[:16]}
    return out


d1 = decls(R1); d2 = decls(R2)
inv = {v: k for k, v in RENOMES.items()}
linhas = []
for n2, v2 in d2.items():
    n1 = inv.get(n2, n2)
    if n1 in d1:
        same = d1[n1]["enunciado"] == v2["enunciado"]
        if n1 != n2:
            cls = "RENOMEADA" if same else "RENOMEADA+TIPO_MUDOU"
        else:
            cls = "MANTIDA" if same else "TIPO_MUDOU"
        linhas.append({"r1": n1, "r2": n2, "classe": cls, "enunciado_igual": same,
                       "docstring_mudou": d1[n1]["doc_sha16"] != v2["doc_sha16"],
                       "enunciado_r1": d1[n1]["enunciado"], "enunciado_r2": v2["enunciado"],
                       "motivo": MOTIVOS.get(n2, "")})
    else:
        linhas.append({"r1": None, "r2": n2, "classe": "NOVA", "enunciado_r2": v2["enunciado"], "motivo": MOTIVOS.get(n2, "")})
for n1 in d1:
    if n1 not in d2 and n1 not in RENOMES:
        linhas.append({"r1": n1, "r2": None, "classe": "REMOVIDA", "motivo": MOTIVOS.get(n1, "")})
cont = {}
for l in linhas:
    cont[l["classe"]] = cont.get(l["classe"], 0) + 1
nomes = ["TGLExt.IALD." + n for n in d2]
aud = ("-- AUDITORIA da pedra TGLExt.IALD R2 (6_R2_CORRECOES, 13/10/2026): um #print axioms por declaracao;"
       " esperado <= {propext, Classical.choice, Quot.sound}\nimport TGLExt.IALD\n\n" + "".join("#print axioms %s\n" % n for n in nomes))
open(AUD, "w", encoding="utf-8", newline="\n").write(aud)
open(os.path.join(AQUI, "fonte", "AuditIALD_R2.lean"), "w", encoding="utf-8", newline="\n").write(aud)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
json.dump({"r1": R1, "r1_sha256": sha(R1), "r2": R2, "r2_sha256": sha(R2), "n_r1": len(d1), "n_r2": len(d2),
           "contagem": cont, "linhas": linhas}, open(os.path.join(AQUI, "COMPARACAO_R1_R2.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
json.dump({"fonte": R2, "fonte_sha256": sha(R2), "n_declaracoes": len(d2),
           "n_theorem": sum(1 for v in d2.values() if v["tipo"] == "theorem"),
           "n_def": sum(1 for v in d2.values() if v["tipo"] == "def"),
           "declaracoes": [{"nome": "TGLExt.IALD." + k, **v} for k, v in d2.items()]},
          open(os.path.join(AQUI, "DECLARACOES_R2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("r1", len(d1), "r2", len(d2), cont)
for l in linhas:
    if l["classe"] != "MANTIDA":
        print(l["classe"], l["r1"], "->", l["r2"])
