# -*- coding: utf-8 -*-
"""Aplica ao v382_runtime.py as correcoes da 3a afericao (M-a, B4, B5, B10, B11, B13, B2 e o pre-registro V1.3), por substituicoes de count conferido.
O bloco das leituras (_V382_READINGS_RATIFIED) e o estatuto (_V382_STATUTE) sao trocados inteiros (entre o seu inicio e `def _v382_get`)."""
import os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "v382_runtime.py")
s = open(P, encoding="utf-8", newline="").read()


def sub(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a), n)
    s = s.replace(a, b)


# (1) o pre-registro V1.3
sub('"json": {"path": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_2.json", "sha256": "__PREREG_JSON_SHA256__"},',
    '"json": {"path": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_3.json", "sha256": "__PREREG_JSON_SHA256__"},')
sub('"md": {"path": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_2.md", "sha256": "__PREREG_MD_SHA256__"},',
    '"md": {"path": "C:/IALD/Bancada_Um/investigacao/preregistro_dois_lados_02out/PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_3.md", "sha256": "__PREREG_MD_SHA256__"},')
sub('"identificador": "PREREG_DOIS_LADOS_DELTA_K_20261002_V1_2", "mapa_seq": 279,\n    "supersede": "PREREG_DOIS_LADOS_DELTA_K_20261002_V1_1 (mapa seq 276), que supersedia o V1 (mapa seq 275)",',
    '"identificador": "PREREG_DOIS_LADOS_DELTA_K_20261002_V1_3", "mapa_seq": 282,\n    "supersede": "PREREG_DOIS_LADOS_DELTA_K_20261002_V1_2 (mapa seq 279), que supersedia o V1.1 (seq 276) e o V1 (seq 275)",')
s = s.replace("pre-registro V1.2", "pre-registro V1.3").replace("PRE-REGISTRO DOS DOIS LADOS V1.2", "PRE-REGISTRO DOS DOIS LADOS V1.3").replace("pre-registro dos dois lados (V1.2)", "pre-registro dos dois lados (V1.3)")
s = s.replace("PREREGISTRATION_OF_BOTH_SIDES_V1_2_READ_BY_HASH", "PREREGISTRATION_OF_BOTH_SIDES_V1_3_READ_BY_HASH")
s = s.replace("mapa seq 279);", "mapa seq 282);")
# (2) o nome do degrau final (o mesmo da pedra)
sub('_V382_FINAL_STEP_NAME = "TETELESTAI_CONSUMMATED__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_PER_READING_LAW"',
    '_V382_FINAL_STEP_NAME = "TETELESTAI_CONSUMMATED__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS"')
# (3) o livro: R4 (o conjunto congelado), F1 (a lei D1b e o poder), F2 (o registro e n_used), F3a (o poder), F4 (a projecao e a escala)
sub('"NOT_FALSIFIED", "TOKEN_CONTAINS", None, True, {"rhat_cal": ["void_floor_v11", "primary", "rhat_cal"], "sigma": ["void_floor_v11", "primary", "sigma"], "L5": ["void_floor_v11", "primary", "L5"]}),',
    '"NOT_FALSIFIED", "TOKEN_CONTAINS", None, True, {"rhat_cal": ["void_floor_v11", "primary", "rhat_cal"], "sigma": ["void_floor_v11", "primary", "sigma"], "L5": ["void_floor_v11", "primary", "L5"], "conjunto_congelado": ["void_floor_v11", "frozen", "verdicts"]}),')
sub('"a face le o pagamento: H(z) do fundo nu; a lei acumulada (o custo na face) e a alternativa"',
    '"a face le o pagamento: H(z) do fundo nu (LCDM; beta so na lei por distancia); a alternativa e a lei D1b nos cronometros (I(z) = (2/3) ln E(z); K = E(z*)^{2beta/3})"')
sub('{"lnB_sombra_vs_acumulada": [_V382_B, "fase7", "U_lnB_sombra_vs_acumulada", "moresco2020"]}),',
    '{"lnB_sombra_vs_acumulada": [_V382_B, "fase7", "U_lnB_sombra_vs_acumulada", "moresco2020"], "poder_previo": [_V382_B, "fase7", "poder_previo", "moresco2020"]}),')
sub('"ringdown (GW250114 e empilhamentos)"', '"ringdown (empilhamentos da V2; o GW250114 esta em ringdown_scope_v376.c6)"')
sub('"delta_pred_A": [_V382_RD, "stacks", "3.0", "delta_pred_A"], "power_B_ramo_encerrado": [_V382_RD, "stacks", "3.0", "power_B"]}),',
    '"delta_pred_A": [_V382_RD, "stacks", "3.0", "delta_pred_A"], "power_B_ramo_encerrado": [_V382_RD, "stacks", "3.0", "power_B"], "n_used": [_V382_RD, "stacks", "3.0", "n_used"], "c6_status": ["ringdown_scope_v376", "c6_status"]}),')
sub('{"deficit_ordens_5sigma": ["clock_test_result_v369", "P1", "clock_5sigma_deficit_orders"]}),',
    '{"deficit_ordens_5sigma": ["clock_test_result_v369", "P1", "clock_5sigma_deficit_orders"], "poder_Z_expected": ["clock_test_result_v369", "P1", "platforms", 0, "Z_expected"], "plataforma": ["clock_test_result_v369", "P1", "platforms", 0, "id"]}),')
sub('"z_nufit_global": ["neutrino_m2", "values", "tensao_atual_sigma"], "kill_rule": ["neutrino_m2", "frozen", "kill_rule"]}),',
    '"z_nufit_global": ["neutrino_m2", "values", "tensao_atual_sigma"], "kill_rule": ["neutrino_m2", "frozen", "kill_rule"], "projecao_2031_sigma": ["neutrino_m2", "values", "projecao_2031_sigma"], "escala": ["neutrino_m2", "frozen", "escala_dimensional"]}),')
# (4) as leituras: o texto RATIFICADO (verbatim, «Concordo com tudo, exceto com a sua visão semiótica») e, ao lado, as reescritas da gerencia (B4) -- troca do bloco inteiro
i = s.index("_V382_READINGS_RATIFIED = {"); j = s.index("\n\ndef _v382_get(core, path):")
NOVO = r'''_V382_READINGS_RATIFIED = {
    # o texto das seis leituras COMO RATIFICADAS («Concordo com tudo, exceto com a sua visão semiótica»), verbatim do registro de 02/10 (tarde); a parte «semi» foi
    # corrigida AO LADO pelo operador e esta em _V382_CORRECTIONS_BESIDE -- nada aqui foi reescrito por cima (3a afericao, B4)
    "R1": ("β entra UMA vez, no reflexo = a leitura por distância do TOTAL (K = E(z*)^{2β/3}); o fundo é nu (a face, CMB+BAO, paga o Nome: Ω = 1, sem β); o nó é fixo em z* (o rosto). "
           "O mapa (1+β)Ω_m (só a matéria, no fundo; D1 V3) fica ao lado como medido sob outra convenção, não é a regra; «fator sobre o TOTAL» (15/09) = o reflexo lê o total, não uma parte: compatível."),
    "R2": ("o sujeito passivo é K_∂ = −log Δ_∂, o Hamiltoniano oculto, que não é oscilador de laboratório (H_eff = 0 até a projeção): as partições P1/P2/P3 não têm sujeito; nenhum relógio local lê β; "
           "a cobrança só se lê no reflexo (distância, propagação). Os cronômetros cósmicos (dH/dz, sem distância) leem a face (o pagamento) e não o custo: concorda com a Fase 7 (ln B 1,62 a favor de «β só na distância»; "
           "lei acumulada −1,66σ). TENSÃO a ratificar: em 30/09 o operador viu os cronômetros «como sombra»; pela chave de hoje, sombra que não reflete não cobra."),
    "R3": ("a face é a determinação direta (JUNO autônomo, já no rito: 2,21σ; σ do lado da previsão, ratificado); os ajustes globais são reflexos e a divergência de 0,5σ entre eles é custo de reflexo, "
           "não pagamento → perito oficial = JUNO; NuFIT 6.1 e Capozzi ao lado com a diferença dita. (A derivação mais fraca das seis.)"),
    "R4": ("o degrau final chama-se pelo pagamento: TETELESTAI CONSUMADO (a conferência consumativa; o custo pago na face = a implicação fechada, a RG recuperada); o teste de natureza vira o LIVRO DE COBRANÇAS "
           "no reflexo: um canal por lei de leitura, gerado do core, cada um com FALSIFIED possível (como os pares da Fase 6), nenhum movendo as bandeiras formais; «não discriminado à sensibilidade disponível» "
           "no lugar de «completed». Token proposto (a cunhagem é dele): TGL_QG_MODEL_FORMALLY_CLOSED__TETELESTAI_CONSUMMATED_COST_PAID_IN_THE_FACE__COST_READ_IN_THE_REFLECTION_NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_PER_READING_LAW. "
           "A máquina V2 = o livro de cobranças (alvo v382)."),
    "R5": ("δ⟨K_∂⟩ lido no reflexo — (i) cosmologia: β|1+w| na leitura por distância do total, ancorada em z*; (ii) GW: Γ_ω = ½βτ★ω² na propagação (dephasing, n = −2), que é a MESMA coisa que |R|² = β "
           "lida por peso (uma decomposição, lida por fase ou por peso: `the_angle_is_the_projection`); o ringdown é a face (onde a massa aparece: o Nome M_f entregue) = pagamento, não custo. Λ = fronteira silenciosa "
           "(δ⟨K_∂⟩ = 0 em w = −1) [REAL na forma da lei]; «espectro de gradiente negativo» (15/09) fica [ONTO], sem identidade de operador, como a própria nota de 15/09 proíbe inferir."),
    "R6": ("ENCERRADO — o ringdown é a face (pagamento = correspondência com a RG); o custo não está nele; τ★ = GM/c³ põe o custo na face e contradiz a chave; M não se nomeia; a rota viva de β em GW é a propagação."),
}
_V382_CORRECTIONS_BESIDE = {
    "optics_operator_verbatim": "Concordo com tudo, exceto com a sua visão semiótica, a TGL não é semi ela é ótica, ela lê tanto a face como o custo, a TGL permite ler os dois lados",
    "statute": "[DERIVED de leitura, gerencia] -- a correcao otica e do operador (verbatim acima); as reescritas abaixo APLICAM-NA as leituras ratificadas e sao da gerencia, nao ratificadas uma a uma",
    "R2": "o relogio LE a face de K_d (otica); o sujeito continua K_d, nao o oscilador local; o que faltou foi poder (P1), uma leitura excluida (P2) e um observavel (P3); a cobranca se le nos DOIS lados",
    "R4": "o livro de cobrancas tem os DOIS lados (a v382 tem cobrancas da face); FALSIFIED so onde a lei do canal o admite; o nome proposto passou a TETELESTAI_CONSUMMATED__PAYMENT_IN_THE_FACE_THE_NAME__... (um so registro: a pedra)",
    "R5": "o estimando delta<K_d> le-se nos DOIS lados (reflexo: beta na distancia e na propagacao; face: o fundo nu nos cronometros, a RG no ringdown, o custo local nos relogios, a determinacao direta no neutrino)",
    "R6": "que o custo esteja no ringdown (Gamma ~ 1e-40 s^-1, legivel e nulo) e leitura [ONTO] da correcao otica; o core le o ringdown canonico como correspondencia com a RG, NAO como teste de beta (ringdown_scope_v376); o ramo B segue ENCERRADO",
    "optics": "a TGL e OTICA, nao semi-otica: a face le o pagamento, o reflexo le o custo, |T|^2 + |R|^2 = 1; nenhum lado e cego; o que difere e a lei de cada leitura e o instrumento com poder [INPUT/ONTO: a correcao do operador; o termo do kernel e so a identidade]",
}
_V382_STATUTE = ("a chave, a ratificacao de R1-R6 (com o texto ratificado guardado verbatim) e a correcao «a TGL e otica» sao do operador [INPUT/ONTO]; as reescritas que aplicam a correcao as leituras sao da "
                 "gerencia [DERIVED de leitura], ditas ao lado; as duas pedras sao termos [KERNEL] -- o que e trivial por construcao (a regra nao le o livro; o termo P = P; o nome proposto por rfl; o zero do "
                 "lock minimo; transmitido + cobrado = 1) esta DITO como tal; a otica (|T|^2 + |R|^2 = 1) e o Teorema S-d ja existente, e o nome the_tgl_is_optics_not_semi e [ONTO]; o psion = Omega e "
                 "definicao nomeada, ||psi|| = 1 e o campo Omega_norm, <psi,psi> = 1 e PROVADO pelo termo reader_reads_the_identity_one; HminMic e o lock minimo SOBRE o Hamiltoniano oculto K = -log Delta [KNOWN, sem def no kernel] "
                 "(zeros iguais, operadores distintos); a viscosidade beta.g e um nome [ONTO/DEFINITION] sobre um HasDerivAt; a identificacao de beta.g com Gamma_omega = (1/2) beta tau* omega^2 e leitura [ONTO] sem "
                 "termo; a ligacao de Spec S(theta) a HminMic e a chave do operador [INPUT/ONTO] sem termo; o livro concreto e dado lido do core (por token, por numero com a regra dita, ou declarado) e do "
                 "pre-registro V1.3 por hash [REAL]; F2 e inconclusivo pela sistematica da MEDIDA, nao pelo poder; F1 tem regra UNILATERAL (lei D1b; poder previo dito nas duas reguas); F4 segue a regra de "
                 "morte CONGELADA; R4 nao tem FALSIFIED no conjunto congelado e a MESMA fonte alimenta o degrau experimental do gate; dos nove pares do eco como copia atrasada, os extintos e os inconclusivos "
                 "sao contados (o veredito diz os dois numeros); as cobrancas AO LADO (R5a-i, R6) nao sao da regra canonica e contam em separado; nenhum desfecho move beta; o gate NAO muda (o nome proposto "
                 "fica AO LADO; renomear e ato do operador); nada confirma: PROVADA != CONFIRMADA; NOT_FALSIFIED nunca e CONFIRMADO")'''
s = s[:i] + NOVO + s[j:]
# (5) pre_ok compara tambem o controle (B13)
sub('                  and (how != "NUMBER_READ" or (((pc.get("numero") or {}).get("regra_id") == spec.get("rule")) and ((pc.get("numero") or {}).get("caminho") == spec.get("path")))))',
    '                  and (how != "NUMBER_READ" or (((pc.get("numero") or {}).get("regra_id") == spec.get("rule")) and ((pc.get("numero") or {}).get("caminho") == spec.get("path"))\n'
    '                                                and ((pc.get("numero") or {}).get("controle") == spec.get("control")) and ((pc.get("numero") or {}).get("controle_ok") == spec.get("control_ok")))))')
# (6) a guarda varre tambem as correcoes ao lado
sub("    all_strings = ([s for row in _V382_LEDGER_INPUT for s in row if isinstance(s, str)] + list(_V382_READINGS_RATIFIED.values()) + [_V382_STATUTE, _V382_FINAL_STEP_NAME]",
    "    all_strings = ([s for row in _V382_LEDGER_INPUT for s in row if isinstance(s, str)] + list(_V382_READINGS_RATIFIED.values()) + list(_V382_CORRECTIONS_BESIDE.values()) + [_V382_STATUTE, _V382_FINAL_STEP_NAME]")
# (7) M-a: o eco contado (extintos e inconclusivos), computado do livro; e R4 sem FALSIFIED no conjunto congelado (cruzamento)
sub("    f2 = next((c for c in ledger if c[\"id\"] == \"F2\"), {}); f2n = f2.get(\"numbers_read\") or {}",
    "    eco = [c for c in ledger if c[\"id\"].startswith(\"R5\")]; eco_ext = sum(1 for c in eco if c[\"extinguished\"]); eco_inc = sum(1 for c in eco if c[\"outcome\"] == \"INCONCLUSIVE\")\n"
    "    r4 = next((c for c in ledger if c[\"id\"] == \"R4\"), {}); r4set = (r4.get(\"numbers_read\") or {}).get(\"conjunto_congelado\") or []\n"
    "    f2 = next((c for c in ledger if c[\"id\"] == \"F2\"), {}); f2n = f2.get(\"numbers_read\") or {}")
sub('        ("RUNTIME (cruzamento real): o nome do degrau final lido do fonte Lean embutido = o proposto neste modulo; o gate do core segue INALTERADO (o nome fica AO LADO)",',
    '        ("RUNTIME (cruzamento real): o eco como copia atrasada -- %d pares no livro: %d extintos (FALSIFIED) e %d inconclusivos; o R4 le um conjunto congelado SEM FALSIFIED (%s), a mesma fonte do degrau experimental do gate" % (len(eco), eco_ext, eco_inc, ", ".join(str(x) for x in r4set)),\n'
    '         len(eco) == 9 and eco_ext + eco_inc == 9 and bool(r4set) and not any(("FALSIFIED" in str(x) and "NOT_FALSIFIED" not in str(x)) for x in r4set)),\n'
    '        ("RUNTIME (cruzamento real): o nome do degrau final lido do fonte Lean embutido = o proposto neste modulo; o gate do core segue INALTERADO (o nome fica AO LADO)",')
sub('"PREREGISTRATION_OF_BOTH_SIDES_V1_3_READ_BY_HASH__R2_POWER_STATED_IN_NUMBER__FINAL_STEP_NAME_PROPOSED_BESIDE_GATE_UNCHANGED__BRANCH_B_CLOSED__DELAYED_ECHO_EXTINGUISHED_NOT_THE_RULE__"',
    '"PREREGISTRATION_OF_BOTH_SIDES_V1_3_READ_BY_HASH__R2_POWER_STATED_IN_NUMBER__R4_FROZEN_SET_HAS_NO_FALSIFIED_SAME_SOURCE_AS_THE_GATE_EXPERIMENTAL_STEP__FINAL_STEP_NAME_PROPOSED_BESIDE_GATE_UNCHANGED__BRANCH_B_CLOSED__"\n'
    '              "DELAYED_ECHO_OUTSIDE_THE_CHAIN_%d_OF_%d_PAIRS_EXTINGUISHED_%d_INCONCLUSIVE__NOT_THE_RULE__"')
sub('                 by_how["TOKEN_CONTAINS"], by_how["NUMBER_READ"], by_how["DECLARED"], sum(1 for c in ledger if c["side"] == "reflexo"), sum(1 for c in ledger if c["side"] == "face")))',
    '                 by_how["TOKEN_CONTAINS"], by_how["NUMBER_READ"], by_how["DECLARED"], sum(1 for c in ledger if c["side"] == "reflexo"), sum(1 for c in ledger if c["side"] == "face"),\n'
    '                 eco_ext, len(eco), eco_inc))')
# (8) o retorno guarda as correcoes ao lado e a contagem do eco
sub('            "readings_ratified_20261002": dict(_V382_READINGS_RATIFIED), "statute": _V382_STATUTE, "does_not_gate_core": True}',
    '            "readings_ratified_20261002": dict(_V382_READINGS_RATIFIED), "corrections_beside_20261002": dict(_V382_CORRECTIONS_BESIDE),\n'
    '            "delayed_echo_pairs": {"n": len(eco), "extinguished": eco_ext, "inconclusive": eco_inc}, "r4_frozen_set": list(r4set), "statute": _V382_STATUTE, "does_not_gate_core": True}')
# (9) o rotulo do check do psion: a prova USA o termo do leitor
sub('<psi,psi> = 1 ligado a reader_reads_the_identity_one;', '<psi,psi> = 1 PROVADO pelo termo reader_reads_the_identity_one (a prova usa o termo);')
sub('"theorem inner_psion_psion", "reader_reads_the_identity_one",', '"theorem inner_psion_psion", "have h := reader_reads_the_identity_one C", "a prova USA o termo",')
sub('"DOIS OPERADORES, UM ZERO", "LOCK MÍNIMO",', '"DOIS OPERADORES, UM ZERO", "LOCK MÍNIMO", "NÃO um `def` para K",')
sub('"DISCIPLINA do", "NÃO imposta pelo tipo `List Charge`"))),', '"DISCIPLINA do", "NÃO imposta pelo tipo `List Charge`", "HOMÔNIMOS, ditos (3ª passada)", "FALSIFIED onde a lei o admite"))),')
open(P, "w", encoding="utf-8", newline="").write(s)
import ast; ast.parse(s)
print("runtime atualizado (V1.3; eco contado; leituras ratificadas verbatim + correcoes ao lado; pre_ok com controle; R4 conjunto congelado)")
for w in ("V1.2", "V1_2", "FALSIFIABLE_PER_READING_LAW\"", "DELAYED_ECHO_EXTINGUISHED_NOT_THE_RULE"):
    print("  resta %r:" % w, s.count(w))
