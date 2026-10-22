# -*- coding: utf-8 -*-
"""As correcoes da afericao da v383 (M-1 e os BAIXOS acolhidos), por trocas exatas (count conferido):
RUNTIME -- cada rota le tambem o ROTULO PROPRIO da Fase 6 (fase6.veredito_principal / emenda_v4.vereditos_todos / emenda_v5.vereditos_todos_DEC) e o estado dele tem
de ser o mesmo (B-2); ECO_e e ECO_g leem os seus QUALIFICADORES no core (a V4 nao cega e o veredito V3 do mesmo par; a clausula V5 nao aplicada e o poder) (M-1);
as leis de maio levam [INPUT, maio/2026] no V1.4 (M-1); alpha e beta do V1.4 = os do core (B-1); as notas AO LADO sobre o V1.4 (B-1, B-2, B-6).
ARTIGO PT/EN -- os qualificadores de ECO_e e ECO_g; o estatuto da lei de maio; a R6 so no trecho que a rota usa, com a ligacao [DERIVED] (M-1, B-6); a nota da
tabela de pedras (B-3); o cabecalho (B-5). CONFERIDOR -- o controle e a v382 do Nos (B-4). INSTALAR/RITO -- os comentarios historicos voltam a v382 (B-5)."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))


def edit(n, reps, py=True):
    p = os.path.join(HERE, n); s = open(p, encoding="utf-8", newline="").read()
    for a, b in reps:
        k = s.count(a); assert k == 1, (n, k, a[:120]); s = s.replace(a, b)
    if py:
        ast.parse(s)
    open(p + ".tmp", "w", encoding="utf-8", newline="").write(s); os.replace(p + ".tmp", p); print("ok", n)


# ---------------- RUNTIME
RT = [
 ('''_V383_READINGS_RATIFIED = {''',
  '''# o ROTULO PROPRIO da Fase 6 de cada rota (o veredito da propria fase/emenda no core; o token do V1.4 e o do modulo v380 que a le) -- 3a afericao da v383, B-2
_V383_ROUTE_PHASE6_LABEL = {
    "ECO_a": [_V383_B, "fase6", "veredito_principal", "KMS|R1_peso1"], "ECO_b": [_V383_B, "fase6", "veredito_principal", "KMS|R2_peso2_2theta"],
    "ECO_c": [_V383_B, "emenda_v5", "vereditos_todos_DEC", "R1_peso1"], "ECO_d": [_V383_B, "emenda_v5", "vereditos_todos_DEC", "R2_peso2_2theta"],
    "ECO_e": [_V383_B, "emenda_v4", "vereditos_todos", "MAY", "R2_peso2_2theta"], "ECO_f": [_V383_B, "emenda_v4", "vereditos_todos", "MAY", "R1_peso1"],
    "ECO_g": [_V383_B, "emenda_v5", "vereditos_todos_DEC", "R3_quadrado"], "ECO_h": [_V383_B, "fase6", "veredito_principal", "KMS|R3_quadrado"],
    "ECO_i": [_V383_B, "emenda_v4", "vereditos_todos", "MAY", "R3_quadrado"],
}
# os QUALIFICADORES que o V1.4 da a duas rotas, LIDOS do core (M-1): ECO_e -- a exclusao vem da emenda V4, NAO cega, e o veredito V3 pre-registrado para o
# MESMO par e inconclusivo; ECO_g -- o rotulo emitido e inconclusivo pela clausula 2, e pela clausula V5 (no pre-registro, NAO aplicada pelo pipeline) a leitura
# seria sem poder e nao falsificada
_V383_ROUTE_QUALIFIERS = {
    "ECO_e": {"v3_same_pair_verdict": [_V383_B, "fase6", "veredito_principal", "MAY|R2_peso2_2theta"], "v4_blindness": [_V383_B, "emenda_v4", "cegueira"]},
    "ECO_g": {"v5_clause_applied": [_V383_B, "emenda_v5", "clausula_v5_aplicada_pelo_pipeline"], "v5_clause_in_prereg": [_V383_B, "emenda_v5", "clausula_v5_no_preregistro"],
              "power_R3": [_V383_B, "emenda_v5", "todos_DEC", "poder_R3"]},
}
_V383_READINGS_RATIFIED = {'''),
 ('''    "echo": "os nove pares do eco como copia atrasada NAO sao cobrancas da teoria''',
  '''    "R6_in_the_routes": "o V1.4 cita a R6 ratificada inteira no motivo das rotas; o trecho «o custo nao esta nele» foi corrigido ao lado depois (erratas F1/B11 e da 3a afericao da v382: que o custo esteja no ringdown e leitura [ONTO]); o que a rota usa da R6 e so «tau* = GM/c^3 poe o custo na face e contradiz a chave; M nao se nomeia», e a ligacao ao eco e [DERIVED de leitura, gerencia]",
    "alpha_in_the_preregistration": "o V1.4 registra a proveniencia de alpha pelo um.py do Nos no dia (a v382, nao custodiada); o valor e o de CODATA 2018, o mesmo da v381 -- conferido aqui (alpha e beta do V1.4 = os do core)",
    "phase6_label": "o campo rotulo_da_fase6_citado do V1.4 e o token do modulo v380 que le a Fase 6; o rotulo PROPRIO da Fase 6 (TGL_ECHO_RADICAL_V3__...) e lido aqui, ao lado, e da o mesmo estado",
    "echo": "os nove pares do eco como copia atrasada NAO sao cobrancas da teoria'''),
 ('''        routes.append({"id": rid, "id_in_v1_3": rid13, "pair": par, "core_key": chave, "phase6_label_cited": token, "verdict_path": vpath, "state": state, "state_derived": derived,
                       "label_in_core_verdict": tin, "state_ok": bool(tin and derived == state), "matches_preregistration": pre_ok,''',
  '''        lab6 = str(_v383_get(core, _V383_ROUTE_PHASE6_LABEL.get(rid) or []) or "")
        st6 = "EXCLUDED_BY_DATA" if "FALSIFIED_AT_DELAY_LAW" in lab6 else ("INCONCLUSIVE" if "INCONCLUSIVE" in lab6 else "UNREAD")
        qual = {k: _v383_get(core, p) for k, p in (_V383_ROUTE_QUALIFIERS.get(rid) or {}).items()}
        if rid == "ECO_e":
            qual_ok = "INCONCLUSIVE" in str(qual.get("v3_same_pair_verdict") or "") and str(qual.get("v4_blindness") or "").startswith("NÃO cega")
        elif rid == "ECO_g":
            qual_ok = qual.get("v5_clause_applied") is False and qual.get("v5_clause_in_prereg") is True and isinstance(qual.get("power_R3"), (int, float)) and float(qual["power_R3"]) < 5.0
        else:
            qual_ok = True
        law_txt = str((pc.get("lei_de_atraso") or {}).get("texto_e_estatuto") or "")
        law_ok = ("[INPUT, maio/2026]" in law_txt) if "MAY" in par else bool(law_txt)
        routes.append({"id": rid, "id_in_v1_3": rid13, "pair": par, "core_key": chave, "phase6_label_cited": token, "verdict_path": vpath, "state": state, "state_derived": derived,
                       "phase6_own_label": lab6, "state_from_phase6_own_label": st6, "qualifiers_read": qual, "qualifiers_ok": qual_ok, "delay_law_statute_ok": law_ok,
                       "qualifier_from_preregistration": str(pc.get("qualificador") or ""),
                       "label_in_core_verdict": tin, "state_ok": bool(tin and derived == state and st6 == state and qual_ok and law_ok), "matches_preregistration": pre_ok,'''),
 ('''    up = ((pr["json"] or {}).get("um_py") or {}); v382l = up.get("v382_so_local") or {}
    base_ok = up.get("base_versao") == "v381" and len(str(v382l.get("sha256") or "")) == 64''',
  '''    up = ((pr["json"] or {}).get("um_py") or {}); v382l = up.get("v382_so_local") or {}
    base_ok = up.get("base_versao") == "v381" and len(str(v382l.get("sha256") or "")) == 64
    # B-1: o alpha e o beta que o V1.4 registrou sao os do core (a proveniencia do V1.4 e o um.py do Nos no dia, a v382; o valor e o mesmo)
    _rg = (((pr["json"] or {}).get("estimando") or {}).get("regra") or {})
    alpha_pr_ok = isinstance(_rg.get("alpha"), (int, float)) and isinstance(_rg.get("beta_tgl"), (int, float)) and alpha > 0 and abs(float(_rg["alpha"]) / alpha - 1.0) < 1e-15 and abs(float(_rg["beta_tgl"]) / beta - 1.0) < 1e-12 if beta > 0 else False'''),
 ('''        ("RUNTIME (cruzamento real): a base declarada no V1.4 e a v381 custodiada; a v382 (sha16 %s) foi selada so no Nos e NAO e custodiada (o V1.4 o diz)" % str(v382l.get("sha256") or "AUSENTE")[:16],
         base_ok),''',
  '''        ("RUNTIME (cruzamento real): a base declarada no V1.4 e a v381 custodiada; a v382 (sha16 %s) foi selada so no Nos e NAO e custodiada (o V1.4 o diz); o alpha e o beta do V1.4 = os do core (%s)" % (str(v382l.get("sha256") or "AUSENTE")[:16], alpha_pr_ok),
         base_ok and alpha_pr_ok),
        ("RUNTIME (cruzamento real): o ROTULO PROPRIO da Fase 6 de cada rota (fase6 / emenda V4 / emenda V5, no core) da o mesmo estado (%d/%d); ECO_e: a exclusao vem da emenda V4, NAO cega, e o veredito V3 do mesmo par e %s; ECO_g: a clausula V5 esta no pre-registro (%s) e NAO foi aplicada pelo pipeline (aplicada = %s), poder de R3 = %s < 5; as leis de maio levam [INPUT, maio/2026] no V1.4" % (
            sum(1 for r in routes if r["state_from_phase6_own_label"] == r["state"]), n_rt,
            str(((next((r for r in routes if r["id"] == "ECO_e"), {}) or {}).get("qualifiers_read") or {}).get("v3_same_pair_verdict")),
            ((next((r for r in routes if r["id"] == "ECO_g"), {}) or {}).get("qualifiers_read") or {}).get("v5_clause_in_prereg"),
            ((next((r for r in routes if r["id"] == "ECO_g"), {}) or {}).get("qualifiers_read") or {}).get("v5_clause_applied"),
            ((next((r for r in routes if r["id"] == "ECO_g"), {}) or {}).get("qualifiers_read") or {}).get("power_R3")),
         all(r["state_from_phase6_own_label"] == r["state"] and r["qualifiers_ok"] and r["delay_law_statute_ok"] for r in routes) and n_rt == 9),'''),
]
edit("v383_runtime.py", RT)

# ---------------- ARTIGO
QP = r'''    _qual2 = lambda r_: ((r", a exclusão vem da emenda V4, que não é cega, e o veredito V3 pré-registrado para o mesmo par é inconclusivo" if (r_.get("id") == "ECO_e" and r_.get("qualifiers_ok")) else "")
                          + ((r", e pela cláusula V5, que está no pré-registro e não foi aplicada pelo pipeline, a leitura seria sem poder e não falsificada (poder " + _f2((r_.get("qualifiers_read") or {}).get("power_R3"), 2) + r"$\sigma$)") if (r_.get("id") == "ECO_g" and r_.get("qualifiers_ok")) else ""))
'''
QE = r'''    _qual2 = lambda r_: ((r", the exclusion comes from amendment V4, which is not blind, and the V3 verdict pre-registered for the same pair is inconclusive" if (r_.get("id") == "ECO_e" and r_.get("qualifiers_ok")) else "")
                          + ((r", and by clause V5, which is in the pre-registration and was not applied by the pipeline, the reading would be underpowered and not falsified (power " + _f2((r_.get("qualifiers_read") or {}).get("power_R3"), 2) + r"$\sigma$)") if (r_.get("id") == "ECO_g" and r_.get("qualifiers_ok")) else ""))
'''
PT = [
 ("as duas aferições da v382 acolhidas", "as aferições da v382 acolhidas"),
 ('''    _rotas2 = "; ".join(r"%s: %s com %s, %s%s" % (_tt2(r_.get("id")), _amp2.get(str((r_.get("amplitude_from_preregistration") or {}).get("leitura")), "n/d"), _lei2.get(str((r_.get("delay_law_from_preregistration") or {}).get("nome")), "n/d"), _st2.get(r_.get("state"), "n/d"), _rn2(r_)) for r_ in _ro2)''',
  QP + '''    _rotas2 = "; ".join(r"%s: %s com %s, %s%s%s" % (_tt2(r_.get("id")), _amp2.get(str((r_.get("amplitude_from_preregistration") or {}).get("leitura")), "n/d"), _lei2.get(str((r_.get("delay_law_from_preregistration") or {}).get("nome")), "n/d"), _st2.get(r_.get("state"), "n/d"), _rn2(r_), _qual2(r_)) for r_ in _ro2)'''),
 ('''a lei de dezembro é \\textsf{[DECLARADO]}, derivada por IA, não do axioma; as três leis de atraso nomeiam a massa do remanescente, e a leitura R6 ratificada diz que isso põe o custo na face; a v381 já pôs o eco como cópia atrasada fora da cadeia, e fica a definição do operador de 16/09, o eco como resposta da fronteira.''',
  '''a lei de dezembro é \\textsf{[DECLARADO]}, derivada por IA, não do axioma; a lei de maio é \\textsf{[INPUT]}, de maio de 2026; as três leis de atraso nomeiam a massa do remanescente, e pela leitura R6 ratificada $\\tau_\\star=GM/c^3$ põe o custo na face e contradiz a chave (a ligação dessa leitura ao eco é \\textsf{[DERIVED]} de leitura da gerência); a v381 já pôs o eco como cópia atrasada fora da cadeia, e fica a definição do operador de 16/09, o eco como resposta da fronteira. Na tabela de pedras, as duas pedras aparecem como da v382: foram escritas e aferidas na v382, que ficou só no Nós; são públicas a partir desta versão.'''),
]
EN = [
 ("both v382 audits accepted", "the v382 audits accepted"),
 ('''    _rotas2 = "; ".join(r"%s: %s with %s, %s%s" % (_tt2(r_.get("id")), _amp2.get(str((r_.get("amplitude_from_preregistration") or {}).get("leitura")), "n/a"), _lei2.get(str((r_.get("delay_law_from_preregistration") or {}).get("nome")), "n/a"), _st2.get(r_.get("state"), "n/a"), _rn2(r_)) for r_ in _ro2)''',
  QE + '''    _rotas2 = "; ".join(r"%s: %s with %s, %s%s%s" % (_tt2(r_.get("id")), _amp2.get(str((r_.get("amplitude_from_preregistration") or {}).get("leitura")), "n/a"), _lei2.get(str((r_.get("delay_law_from_preregistration") or {}).get("nome")), "n/a"), _st2.get(r_.get("state"), "n/a"), _rn2(r_), _qual2(r_)) for r_ in _ro2)'''),
 ('''the December law is \\textsf{[DECLARADO]}, derived by an AI, not from the axiom; the three delay laws name the remnant's mass, and the ratified reading R6 says that this puts the cost on the face; v381 already put the echo as a delayed copy outside the chain, and the operator's definition of 16/09, the echo as the boundary's response, stays.''',
  '''the December law is \\textsf{[DECLARADO]}, derived by an AI, not from the axiom; the May law is \\textsf{[INPUT]}, of May 2026; the three delay laws name the remnant's mass, and by the ratified reading R6 $\\tau_\\star=GM/c^3$ puts the cost on the face and contradicts the key (the link of that reading to the echo is \\textsf{[DERIVED]}, a reading of the management); v381 already put the echo as a delayed copy outside the chain, and the operator's definition of 16/09, the echo as the boundary's response, stays. In the table of stones, the two stones appear as of v382: they were written and audited in v382, which stayed only in the canonical folder; they are public from this version on.'''),
]
edit("artigo_pt_v383.pysnip", PT, py=False)
edit("artigo_en_v383.pysnip", EN, py=False)

# ---------------- CONFERIDOR / INSTALAR / RITO
edit("conferir_rito_v383.py", [("Contra o selo v381 (controle): REPROVA 'deve mudar', APROVA 'nao pode mudar'.", "Contra o selo da v382 que esta no Nos (controle): REPROVA 'deve mudar', APROVA 'nao pode mudar'.")])
edit("instalar_v383.py", [("# v383 (aferidor B1/C2)", "# v382 (aferidor B1/C2)")])
edit("rito_v383.sh", [("aferidor v383 C1/C2", "aferidor v382 C1/C2")], py=False)
print("M-1 e BAIXOS aplicados")
