# -*- coding: utf-8 -*-
"""Comparacao TEXTUAL dos `#check` R1 x R2 da auditoria de tipos propria (logs/AUD_TIPOS_saida.txt), por linhas
(um bloco comeca em coluna 0 com `TGLExt.<ns>.<nome> :`; continuacoes sao indentadas), namespace normalizado.
A defeq ja foi provada em Lean (type_of% nos dois sentidos, EXIT 0). Uso: ... <saida.json>"""
import json
import re
import sys

A = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\5_R2\3_AUD_REPRO"
lines = open(A + r"\logs\AUD_TIPOS_saida.txt", encoding="utf-8").read().splitlines()
r1, r2 = {}, {}
cur = None
for ln in lines:
    m = re.match(r"^@?TGLExt\.(TheTimeHasNoRank|TheTimeIsNotAPost)\.([A-Za-z0-9_'.]+) :(.*)", ln)
    if m:
        ns, nome, rest = m.groups()
        cur = (ns, nome)
        (r1 if ns == "TheTimeHasNoRank" else r2)[nome] = rest
    elif cur and ln.startswith(" "):
        ns, nome = cur
        (r1 if ns == "TheTimeHasNoRank" else r2)[nome] += " " + ln.strip()
    else:
        cur = None
REN = {"time_is_the_modular_flow": "modular_flow_is_a_kms_group", "the_time_has_no_rank": "the_time_is_not_a_post",
       "probe_the_time_has_no_rank": "probe_the_time_is_not_a_post",
       "optical_attractor_is_the_absolute_one": "half_identity_is_absoluteRho_two",
       "optical_attractor_clock_stops": "half_identity_clock_stops"}
REF = {"purityR_modular", "clock_reads_modulo_period", "the_two_regimes_of_time", "probe_bounded_spectral_translation"}


def norm(s, ns):
    return re.sub(r"\s+", " ", s.replace("TGLExt.%s." % ns, "TGLExt.<NS>.")).strip()


ident, difs = 0, []
for a, t in r1.items():
    b = REN.get(a, a)
    if b not in r2:
        difs.append({"R1": a, "R2": b, "motivo": "sem #check R2"})
        continue
    if norm(t, "TheTimeHasNoRank") == norm(r2[b], "TheTimeIsNotAPost"):
        ident += 1
    else:
        difs.append({"R1": a, "R2": b, "reforco_esperado": a in REF,
                     "tipo_R1": norm(t, "TheTimeHasNoRank"), "tipo_R2": norm(r2[b], "TheTimeIsNotAPost")})
out = {"n_check_R1": len(r1), "n_check_R2": len(r2), "identicos_textualmente": ident, "diferentes": len(difs),
       "todos_os_diferentes_sao_reforcos": all(d.get("reforco_esperado") for d in difs) and len(difs) == 4,
       "diferentes_detalhe": difs,
       "nota": ("defeq provada em Lean (type_of% nos dois sentidos, EXIT 0) para os 122 pares; comparacao TEXTUAL do #check "
                "por linhas, namespace normalizado; os 4 reforcos TEM de diferir (E5.09, E5.11, E5.12) e a R2 implica a R1 "
                "(provado em AuditTiposAud.lean)")}
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "diferentes_detalhe"}, ensure_ascii=False, indent=1))
for d in difs:
    print("DIF", d["R1"], "->", d["R2"], "| reforco esperado:", d.get("reforco_esperado"))
