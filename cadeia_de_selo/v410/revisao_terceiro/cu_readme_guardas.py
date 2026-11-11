import sys, re, json
sys.stdout.reconfigure(encoding="utf-8")
from cu_corpus import *
RD = json.load(open("cu_saidas/readme_render.json", encoding="utf-8"))
L = json.load(open("literais_v410.json", encoding="utf-8"))
AC = L["_V410_AESCALA_CONTRACT"]; HC = L["_V410_H0DN_CONTRACT"]
PADROES = {
    "clay_resolvido_seco": r"(?i)clay[^.\n]{0,40}(resolvid[oa]|resolved|solved)|resolveu[^.\n]{0,30}clay|clay_solved",
    "tgl_resolve_milenio": r"(?i)(TGL|IALD)[^.\n]{0,30}(resolve|resolves|solves|resolved)[^.\n]{0,40}(milên|milen|millennium)",
    "tautologia": r"(?i)tautolog", "nao_resolve": r"(?i)n[ãa]o resolve|does not resolve|does not solve",
    "nao_afirma_prova_pnp": r"(?i)(n[ãa]o\s+(afirma|prova|decide)|does not (claim|prove|assert|decide))[^.\n]{0,60}P\s*=\s*n?N?P",
    "CONFIRMED": r"CONFIRMED(?!_)(?!\s*\))", "PROVED_BY": r"PROVED_BY",
    "5sigma_atingido": r"(?i)5\s*(σ|sigma)\s*(atingid|observad|reached|observed)|FIVE_SIGMA_OBSERVED|H0DN_CONFIRMS|\bDETECTED\b",
    "abertura_permitida": r"(?i)abertura\s+permitida|opening[_ ]allowed\W{0,4}true",
    "provado_na_natureza": r"(?i)provado na natureza|proved in nature|proven in nature",
    "F59_negacao_seca_dos_passos": r"(?i)(m[áa]quina de Turing|Turing machine)[^.\n]{0,80}(n[ãa]o s[ãa]o|are not|n[ãa]o conta|does not count)[^.\n]{0,60}(passos|steps)",
    "leitor_paga": r"(?i)o leitor paga|the reader pays",
    "mentiroso": r"(?i)Pai da Mentira|Father of Lies|decisor sem escala[^.\n]{0,40}(mente|minta|lies)",
    "rotulo_leitura_do_operador": r"(?i)leitura do operador|leitura dele|\[ONTO\]|operator[’']s reading|his reading",
    "ratificado_aux": r"a_flutuacao_do_fundo_e_cotada|ate_meio_o_tempo_do_tetelestai_nao_e_negativo",
    "limiar_ou_linear": r"(?i)limiar|threshold|ln 2|linear (nos|in the) bits",
    "5sigma_prova": r"(?i)(β|beta)[^.\n]{0,30}prov",
}
for nome in ("README_FRENTE", "README_O_QUE_SAI", "README_PONTEIRO_ABSTRACT"):
    t = ws(RD[nome]); print("=====", nome, len(RD[nome].encode("utf-8")), "B")
    for pn, rx in PADROES.items():
        ms = list(re.finditer(rx, t))
        if ms: print("   %-30s %d | %s" % (pn, len(ms), ctx(t, ms[0], 90)))
t = ws(RD["README_FRENTE"])
print()
print("formas ratificadas todas no bloco FRENTE (D81 PT/EN, Clay PT/EN, habitante PT/EN, H0DN obrigatoria PT/EN):", all(ws(RD[k]) in t for k in ("D81_PT", "D81_EN", "CLAY_PT", "CLAY_EN", "UMH_PT", "UMH_EN", "OBR_PT", "OBR_EN")))
print("o bloco diz que o H0DN NAO foi aberto (PT/EN):", ws(RD["_H0_PT"]) in t, ws(RD["_H0_EN"]) in t)
print("os 3 nomes da secao 7 ratificados:", [n for n in ("sem_escala_nao_ha_fita", "a_constante_da_luz_e_a_escala_do_tempo", "o_nome_e_a_singularidade_da_informacao") if "`%s`" % n in RD["README_FRENTE"]])
print("tamanho FRENTE:", RD["_tamanho_README_FRENTE_B"], "B; teto", RD["README_FRENTE_TETO_B"])
print("sem % e sem CR:", "%" not in RD["README_FRENTE"] + RD["README_O_QUE_SAI"], "\r" not in RD["README_FRENTE"] + RD["README_O_QUE_SAI"])
print()
print(RD["README_FRENTE"])
print("-----")
print(RD["README_O_QUE_SAI"])
