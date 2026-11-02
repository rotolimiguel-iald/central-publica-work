# -*- coding: utf-8 -*-
"""gerar_pino_das_pedras_v405.py -- escreve pedras_sha16_da_ordem.json (o pino de cada uma das OITO pedras da v405) LENDO o sha256 do arquivo de cada pedra (as fontes em work\\experimento_espelho_30out, work\\cadeia_de_selo405,
work\\observador_terminal_31out e work\\e0_cadeia_31out) e CONFERINDO contra a FONTE VIGENTE dos sha256: o RECIBO DE ERRATA da gerencia (work\\e0_cadeia_31out\\RECIBO_ERRATA_PEDRAS_01nov.json, 13:28 de 01/11: sete arquivos, sha256_antes -> sha256_depois; nenhuma prova mudou; tres teoremas rebatizados;
ObservadorTerminal intocado). O ARQUIVO MANDA e tem de bater com `sha256_depois` (fail-closed). Os recibos antigos (RECIBO_NOMEACAO_E_DERIVACAO_01nov.json, RECIBO_PEDRA_IDENTIDADE_01nov.json) ficam como REGISTRO e sao a cadeia de custodia: cada `sha256_antes` da errata tem de ser o sha256 que eles pinaram, e os teoremas e axiomas deles,
com a renomeacao da errata aplicada, tem de ser os `#print axioms` da fonte de agora. O observador (intocado) segue conferido pelo RECIBO_PEDRA_OBSERVADOR_TERMINAL_31out_R2.json.
Confere tambem: sorry 0; todos os teoremas do recibo no trio {propext, Classical.choice, Quot.sound}; o numero de `#print axioms` na fonte == o numero de teoremas do recibo (a errata nao muda a contagem por pedra: 21, 15, 15, 26, 19, 13, 12, 6, MEDIDA aqui).
AO LADO (errata R2 da gerencia, 16:45 de 01/11, depois da revisao de terceiro): a FONTE VIGENTE agora e' RECIBO_ERRATA_PEDRAS_R2_01nov.json (OITO arquivos). O arquivo tem de bater com `sha256_depois` do R2; o `sha256_antes` do R2 tem de ser o `sha256_depois` do R1 (sete) ou o sha256 do recibo R2 do observador (a oitava): a cadeia de custodia inteira. Duas mudancas de codigo: Disco.the_flow_is_the_canonical_law (teorema novo, sem axiomas no recibo antigo: o kernel mede em pos_build) e the_terminal_reads_one -> the_omega_pole_reads_one (quarto rebatismo). A contagem por pedra e' MEDIDA (o disco sobe de 12 para 13).
AO LADO (errata R3 da gerencia, 17:21 de 01/11, a revisita da Lei do Diminuto ordenada pelo operador): a FONTE VIGENTE agora e' RECIBO_ERRATA_PEDRAS_R3_01nov.json (oito pedras; seis mudaram; Identidade e ObservadorTerminal inalteradas). O arquivo tem de bater com `sha256_depois` do R3; o `sha256_antes` do R3 tem de ser o `sha256_depois` do R2, e as duas inalteradas tem de ser iguais no R2 e no R3. Codigo novo: 11 teoremas na LeiDoDiminuto e 1 na TonicaDoHamiltoniano; a contagem por pedra e' MEDIDA da fonte.
AO LADO (errata R4 da gerencia, 18:41 de 01/11, a resposta do operador: o diminuto modula a tonica; o gap): a FONTE VIGENTE agora e' RECIBO_ERRATA_PEDRAS_R4_01nov.json (oito pedras; tres mudaram). Mesma cadeia de custodia: R4.sha256_antes == R3.sha256_depois, e as inalteradas iguais no R3 e no R4. Codigo novo: 8 teoremas na LeiDoDiminuto e 14 na PontoZeroDoPsion; a contagem e' MEDIDA da fonte.
AO LADO (errata R5 da gerencia, 18:56 de 01/11: a escala e' o que fica parado): a FONTE VIGENTE agora e' RECIBO_ERRATA_PEDRAS_R5_01nov.json (oito pedras; quatro mudaram). Mesma cadeia: R5.sha256_antes == R4.sha256_depois, e as inalteradas iguais no R4 e no R5. Um teorema novo na LeiDoDiminuto e dois rebatizados (os nomes da lista da R3 ja sao os novos).
AO LADO (errata R6 da gerencia, 19:02 de 01/11: uma docstring da Tonica, reprovada pela guarda F12): a FONTE VIGENTE agora e' RECIBO_ERRATA_PEDRAS_R6_01nov.json. Esse recibo repete as entradas do R5 (com o `sha256_antes` do R5) e so' a Tonica tem depois novo; logo a pedra mudada na R6 e' a de depois diferente do R5, e nao a que tem `sha256_antes`. Cadeia: R6.sha256_antes == R5.sha256_depois na mudada; R6.depois == R5.depois nas demais. Nenhum teorema novo.
AO LADO (errata R7 da gerencia, 20:57 de 01/11, a segunda revisao de terceiro): a FONTE VIGENTE agora e' RECIBO_ERRATA_PEDRAS_R7_01nov.json (oito pedras; tres mudaram: PontoZeroDoPsion com codigo, LeiDoDiminuto e TonicaDoHamiltoniano so' docstring). Mesma leitura da R6: a pedra mudada e' a de depois diferente da anterior. Na PontoZeroDoPsion seis teoremas foram rebatizados (RENOMES_R7), tres sao novos (NOVOS_R7) e os lemas do lock mudaram de assinatura, com o nome; a contagem e' MEDIDA da fonte.
Reexecutavel: se o JSON ja existe e e' igual, fica; se difere, aborta. uso: python -I -B -X utf8 gerar_pino_das_pedras_v405.py   (molde: gerar_pino_das_pedras_v404.py)"""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
WK = os.path.dirname(os.path.dirname(HERE))                      # ...\Central de Patentes\work
ESP = os.path.join(WK, "experimento_espelho_30out"); C405 = os.path.join(WK, "cadeia_de_selo405"); OBS = os.path.join(WK, "observador_terminal_31out"); E0 = os.path.join(WK, "e0_cadeia_31out")
TRIO = {"propext", "Classical.choice", "Quot.sound"}
R_NOM = json.load(open(os.path.join(E0, "RECIBO_NOMEACAO_E_DERIVACAO_01nov.json"), encoding="utf-8"))
R_OBS = json.load(open(os.path.join(OBS, "RECIBO_PEDRA_OBSERVADOR_TERMINAL_31out_R2.json"), encoding="utf-8"))
R_IDT = json.load(open(os.path.join(C405, "RECIBO_PEDRA_IDENTIDADE_01nov.json"), encoding="utf-8"))
POR_MODULO = {p["modulo"]: p for p in R_NOM["pedras"]}
R_ERR_P = os.path.join(E0, "RECIBO_ERRATA_PEDRAS_01nov.json")
R_ERR = json.load(open(R_ERR_P, encoding="utf-8"))
assert R_ERR["nenhuma_prova_mudou"] is True and R_ERR["nomes_de_modulo_intocados"] is True and R_ERR["ObservadorTerminal"] == "intocado", "o recibo de errata nao diz o que a gerencia ordenou"
ERRATA = {a_["modulo"]: a_ for a_ in R_ERR["arquivos"]}
assert len(ERRATA) == len(R_ERR["arquivos"]) == 7 and "ObservadorTerminal" not in ERRATA, ("a errata tem de cobrir SETE arquivos, sem o observador", sorted(ERRATA))
RENOMES = {"TGLExt." + a_: "TGLExt." + b_ for a_, b_ in R_ERR["teoremas_renomeados"].items()}
assert len(RENOMES) == 3, RENOMES
renome_ = lambda n_: RENOMES.get(n_, n_)
# ---- a errata R2 (16:45 de 01/11/2026, gerencia c1, depois da revisao de terceiro): a FONTE VIGENTE. O R1 fica como elo da cadeia de custodia.
R2_P = os.path.join(E0, "RECIBO_ERRATA_PEDRAS_R2_01nov.json")
R2 = json.load(open(R2_P, encoding="utf-8"))
assert len(R2["pedras"]) == 8, sorted(R2["pedras"])
R2_DEP = {"DiscoDeEuler": "the_flow_is_the_canonical_law", "ObservadorTerminal": "the_omega_pole_reads_one"}
assert len(R2["codigo_mudado"]) == 2 and all(any(m_.startswith(k_ + ":") and v_ in m_ for m_ in R2["codigo_mudado"]) for k_, v_ in R2_DEP.items()), ("o recibo R2 nao diz as duas mudancas de codigo que a ordem deu", R2["codigo_mudado"])
RENOMES_R2 = {"the_terminal_reads_one": "the_omega_pole_reads_one"}        # nomes CURTOS: e' como o recibo R2 do observador os traz
NOVOS_R2 = {"DiscoDeEuler": ["TGLExt.DiscoDeEuler.Disco.the_flow_is_the_canonical_law"]}     # teorema novo: os axiomas sao medidos pelo kernel (pos_build_kernel_v405), nao por um recibo anterior
# ---- a errata R3 (17:21 de 01/11/2026, gerencia c1, a revisita da Lei do Diminuto): a FONTE VIGENTE. O R2 fica como elo da cadeia de custodia.
R3_P = os.path.join(E0, "RECIBO_ERRATA_PEDRAS_R3_01nov.json")
R3 = json.load(open(R3_P, encoding="utf-8"))
assert len(R3["pedras"]) == 8 and sorted(R3["pedras"]) == sorted(R2["pedras"]), sorted(R3["pedras"])
INALTERADAS_R3 = sorted(k_ for k_, v_ in R3["pedras"].items() if "sha256_antes" not in v_)
assert INALTERADAS_R3 == ["Identidade", "ObservadorTerminal"], INALTERADAS_R3
assert len(R3["codigo_mudado"]) == 2 and any(m_.startswith("LeiDoDiminuto:") and "the_diminished_law_closes" in m_ for m_ in R3["codigo_mudado"]) and any(m_.startswith("TonicaDoHamiltoniano:") and "the_ratio_survives_the_rescaling" in m_ for m_ in R3["codigo_mudado"]), ("o recibo R3 nao diz as duas mudancas de codigo que a ordem deu", R3["codigo_mudado"])
_LDD3 = ["transpor_preserva_toda_razao", "mesmas_razoes_iff_transposicao", "lerE0_transpor", "E0_relativo_pinado", "as_razoes_nao_fixam_o_absoluto", "Lei.E0_e_a_leitura", "meioTom_e_o_pedagio_local", "meioTom_e_a_face", "tonica_e_o_volume_da_face", "o_tom_e_as_duas_faces", "the_diminished_law_closes"]
NOVOS_R3 = {"LeiDoDiminuto": ["TGLExt.LeiDoDiminuto." + n_ for n_ in _LDD3], "TonicaDoHamiltoniano": ["TGLExt.TonicaDoHamiltoniano.the_ratio_survives_the_rescaling"]}     # os axiomas sao medidos pelo kernel, nao por um recibo anterior
# ---- a errata R4 (18:41 de 01/11/2026, gerencia c1, a resposta do operador): a FONTE VIGENTE. O R3 fica como elo da cadeia de custodia.
R4_P = os.path.join(E0, "RECIBO_ERRATA_PEDRAS_R4_01nov.json")
R4 = json.load(open(R4_P, encoding="utf-8"))
assert len(R4["pedras"]) == 8 and sorted(R4["pedras"]) == sorted(R3["pedras"]), sorted(R4["pedras"])
INALTERADAS_R4 = sorted(k_ for k_, v_ in R4["pedras"].items() if "sha256_antes" not in v_)
assert INALTERADAS_R4 == ["Identidade", "MassaTensaoPura", "ObservadorTerminal", "PonteDaMassa", "TonicaDoHamiltoniano"], INALTERADAS_R4
assert len(R4["codigo_mudado"]) == 2 and any(m_.startswith("LeiDoDiminuto:") and "the_diminished_law_closes" in m_ for m_ in R4["codigo_mudado"]) and any(m_.startswith("PontoZeroDoPsion:") and "the_gap_closes" in m_ for m_ in R4["codigo_mudado"]), ("o recibo R4 nao diz as duas mudancas de codigo que a ordem deu", R4["codigo_mudado"])
_LDD4 = ["modular_tonica", "modular_sustenta", "lerE0_e_a_tonica_modulada", "modular_comuta_com_transpor", "modular_nao_e_transposicao", "razao_abre_meio_tom", "um_tom_vira_terca_menor", "resolver_modular"]
_PZP4 = ["o_lock_tem_gap_um", "lock_no_angulo", "lock_no_angulo_de_miguel", "o_gap_e_lido_do_angulo_de_miguel", "a_tonica_e_o_gap_sobre_alpha", "a_massa_e_a_projecao_do_gap", "o_psion_e_raiz_de_dois_gaps", "a_frequencia_do_sistema_e_a_do_psion_iff", "a_taxa_de_fronteira_no_psion", "o_ponto_zero_autoconsistente_e_o_gap", "o_psion_e_a_projecao_do_modo", "a_qualidade_nao_depende_da_unidade", "o_relogio_do_gap", "the_gap_closes"]
NOVOS_R4 = {"LeiDoDiminuto": ["TGLExt.LeiDoDiminuto." + n_ for n_ in _LDD4], "PontoZeroDoPsion": ["TGLExt.PontoZeroDoPsion." + n_ for n_ in _PZP4]}
# ---- a errata R5 (18:56 de 01/11/2026, gerencia c1: a escala e' o que fica parado): a FONTE VIGENTE. O R4 fica como elo da cadeia de custodia.
R5_P = os.path.join(E0, "RECIBO_ERRATA_PEDRAS_R5_01nov.json")
R5 = json.load(open(R5_P, encoding="utf-8"))
assert len(R5["pedras"]) == 8 and sorted(R5["pedras"]) == sorted(R4["pedras"]), sorted(R5["pedras"])
INALTERADAS_R5 = sorted(k_ for k_, v_ in R5["pedras"].items() if "sha256_antes" not in v_)
assert INALTERADAS_R5 == ["Identidade", "MassaTensaoPura", "PonteDaMassa", "TonicaDoHamiltoniano"], INALTERADAS_R5
assert len(R5["codigo_mudado"]) == 1 and all(n_ in R5["codigo_mudado"][0] for n_ in ("modular_mantem_a_escala", "mesmas_razoes_iff_transposicao", "as_razoes_nao_fixam_o_absoluto")), ("o recibo R5 nao diz a mudanca de codigo que a ordem deu", R5["codigo_mudado"])
NOVOS_R5 = {"LeiDoDiminuto": ["TGLExt.LeiDoDiminuto.modular_mantem_a_escala"]}
# ---- a errata R6 (19:02 de 01/11/2026, gerencia c1: uma docstring da Tonica): a FONTE VIGENTE. O R5 fica como elo da cadeia de custodia.
R6_P = os.path.join(E0, "RECIBO_ERRATA_PEDRAS_R6_01nov.json")
R6 = json.load(open(R6_P, encoding="utf-8"))
assert len(R6["pedras"]) == 8 and sorted(R6["pedras"]) == sorted(R5["pedras"]), sorted(R6["pedras"])
MUDOU_R6 = sorted(k_ for k_, v_ in R6["pedras"].items() if v_["sha256_depois"] != R5["pedras"][k_]["sha256_depois"])
assert MUDOU_R6 == ["TonicaDoHamiltoniano"], MUDOU_R6
assert R6["codigo_mudado"] == [], ("a ordem diz que a R6 nao mudou codigo; o recibo diz outra coisa", R6["codigo_mudado"])
# ---- a errata R7 (20:57 de 01/11/2026, gerencia c1, a segunda revisao de terceiro): a FONTE VIGENTE. O R6 fica como elo da cadeia de custodia.
R7_P = os.path.join(E0, "RECIBO_ERRATA_PEDRAS_R7_01nov.json")
R7 = json.load(open(R7_P, encoding="utf-8"))
assert len(R7["pedras"]) == 8 and sorted(R7["pedras"]) == sorted(R6["pedras"]), sorted(R7["pedras"])
MUDOU_R7 = sorted(k_ for k_, v_ in R7["pedras"].items() if v_["sha256_depois"] != R6["pedras"][k_]["sha256_depois"])
assert MUDOU_R7 == ["LeiDoDiminuto", "PontoZeroDoPsion", "TonicaDoHamiltoniano"], MUDOU_R7
assert len(R7["codigo_mudado"]) == 1 and R7["codigo_mudado"][0].startswith("PontoZeroDoPsion:") and all(n_ in R7["codigo_mudado"][0] for n_ in ("retidoNoAngulo", "tempoDoRetido", "lockDe", "o_gap_com_unidade", "o_retido_e_o_valor_esperado_do_lock", "HminMic_e_o_lock", "the_gap_closes")), ("o recibo R7 nao diz a mudanca de codigo que a ordem deu", R7["codigo_mudado"])
_PZP = "TGLExt.PontoZeroDoPsion."
RENOMES_R7 = {_PZP + a_: _PZP + b_ for a_, b_ in {"o_gap_e_lido_do_angulo_de_miguel": "o_retido_e_lido_do_angulo_de_miguel", "a_tonica_e_o_gap_sobre_alpha": "a_tonica_e_o_retido_sobre_alpha", "a_massa_e_a_projecao_do_gap": "a_massa_e_a_projecao_do_retido", "o_psion_e_raiz_de_dois_gaps": "o_psion_e_raiz_de_dois_retidos", "o_ponto_zero_autoconsistente_e_o_gap": "o_ponto_zero_autoconsistente_e_o_retido", "o_relogio_do_gap": "o_relogio_do_retido"}.items()}
NOVOS_R7 = {"PontoZeroDoPsion": [_PZP + n_ for n_ in ("o_gap_com_unidade", "o_retido_e_o_valor_esperado_do_lock", "HminMic_e_o_lock")]}
# (chave, nome do modulo, arquivo da pedra, de onde vem o pino)
PEDRAS = [("ponte", "PonteDaMassa", os.path.join(ESP, "PonteDaMassa.lean"), "nomeacao"),
          ("tensao", "MassaTensaoPura", os.path.join(ESP, "MassaTensaoPura.lean"), "nomeacao"),
          ("identidade", "Identidade", os.path.join(C405, "Identidade.lean"), "identidade"),
          ("observador", "ObservadorTerminal", os.path.join(OBS, "ObservadorTerminal.lean"), "observador_r2"),
          ("diminuto", "LeiDoDiminuto", os.path.join(E0, "LeiDoDiminuto.lean"), "nomeacao"),
          ("tonica", "TonicaDoHamiltoniano", os.path.join(E0, "TonicaDoHamiltoniano.lean"), "nomeacao"),
          ("disco", "DiscoDeEuler", os.path.join(E0, "DiscoDeEuler.lean"), "nomeacao"),
          ("psion", "PontoZeroDoPsion", os.path.join(E0, "PontoZeroDoPsion.lean"), "nomeacao")]
pino = {}; detalhe = {}
for k, nome, arq, fonte in PEDRAS:
    b = open(arq, "rb").read(); h = hashlib.sha256(b).hexdigest()
    impressos = re.findall(r"(?m)^#print axioms (\S+)\s*$", b.decode("utf-8"))
    e7_ = R7["pedras"][nome]; e6_ = R6["pedras"][nome]; e5_ = R5["pedras"][nome]; e4_ = R4["pedras"][nome]; e3_ = R3["pedras"][nome]; e2_ = R2["pedras"][nome]     # a FONTE VIGENTE (R7): o arquivo manda e tem de bater com sha256_depois
    assert os.path.normcase(os.path.normpath(e7_["arquivo"])) == os.path.normcase(os.path.normpath(arq)), ("a errata R7 aponta outro arquivo", nome, e7_["arquivo"], arq)
    assert e7_["sha256_depois"] == h and e7_["sha16_depois"] == h[:16], ("o arquivo da pedra DIVERGE do recibo R7 (sha256_depois)", nome, h[:16], e7_["sha256_depois"][:16])
    if nome in MUDOU_R7:
        assert e7_["sha256_antes"] == e6_["sha256_depois"] and e7_["bytes_depois"] == len(b), ("a cadeia de custodia rompeu: R7.sha256_antes != R6.sha256_depois", nome)
    else:
        assert e6_["sha256_depois"] == h, ("a pedra inalterada na R7 difere do recibo R6", nome)
    if nome in MUDOU_R6:
        assert e6_["sha256_antes"] == e5_["sha256_depois"], ("a cadeia de custodia rompeu: R6.sha256_antes != R5.sha256_depois", nome)
    else:
        assert e5_["sha256_depois"] == e6_["sha256_depois"], ("a pedra inalterada na R6 difere do recibo R5", nome)
    if nome in INALTERADAS_R5:
        assert e4_["sha256_depois"] == e5_["sha256_depois"], ("a pedra dita inalterada na R5 difere do recibo R4", nome)
    else:
        assert e5_["sha256_antes"] == e4_["sha256_depois"], ("a cadeia de custodia rompeu: R5.sha256_antes != R4.sha256_depois", nome)
    assert os.path.normcase(os.path.normpath(e3_["arquivo"])) == os.path.normcase(os.path.normpath(arq)), ("a errata R3 aponta outro arquivo", nome, e3_["arquivo"], arq)
    if nome in INALTERADAS_R4:
        assert e3_["sha256_depois"] == e4_["sha256_depois"], ("a pedra dita inalterada na R4 difere do recibo R3", nome)
    else:
        assert e4_["sha256_antes"] == e3_["sha256_depois"], ("a cadeia de custodia rompeu: R4.sha256_antes != R3.sha256_depois", nome)
    assert os.path.normcase(os.path.normpath(e2_["arquivo"])) == os.path.normcase(os.path.normpath(arq)), ("a errata R2 aponta outro arquivo", nome, e2_["arquivo"], arq)
    if nome in INALTERADAS_R3:     # a cadeia de custodia: inalterada no R3 == R2.sha256_depois; alterada: R3.sha256_antes == R2.sha256_depois
        assert e2_["sha256_depois"] == e3_["sha256_depois"], ("a pedra dita inalterada na R3 difere do recibo R2", nome)
    else:
        assert e3_["sha256_antes"] == e2_["sha256_depois"] and e3_["bytes_antes"] == e2_["bytes_depois"], ("a cadeia de custodia rompeu: R3.sha256_antes != R2.sha256_depois", nome)
    if nome in ERRATA:      # a cadeia de custodia: R2.sha256_antes == R1.sha256_depois; e o R1 ligado ao recibo antigo, abaixo
        e_ = ERRATA[nome]
        assert os.path.normcase(os.path.normpath(e_["path"])) == os.path.normcase(os.path.normpath(arq)), ("a errata aponta outro arquivo", nome, e_["path"], arq)
        assert e2_["sha256_antes"] == e_["sha256_depois"] and e2_["bytes_antes"] == e_["bytes_depois"], ("a cadeia de custodia rompeu: R2.sha256_antes != R1.sha256_depois", nome)
    if fonte == "nomeacao":
        r = POR_MODULO["TGLExt." + nome]
        if nome in ERRATA:
            assert r["sha256"] == ERRATA[nome]["sha256_antes"] and r["bytes"] == ERRATA[nome]["bytes_antes"], ("a cadeia de custodia rompeu: o sha256_antes da errata != o do recibo da nomeacao", nome)
        else:
            assert r["sha256"] == h and r["bytes"] == len(b), ("o arquivo da pedra DIVERGE do recibo da nomeacao", nome, h[:16], r["sha256"][:16], len(b), r["bytes"])
        assert r["sorry"] == 0 and r["fora_do_trio"] == 0 and r["no_trio"] == r["teoremas"], ("o recibo nao diz sorry 0 / trio", nome)
        th = {renome_(n_): v_ for n_, v_ in r["axiomas"].items() if not n_.startswith("(")}
        if nome == "ObservadorTerminal":   # a nomeacao confirmou o nome e nao recompilou a r2: os axiomas vem do recibo R2 (abaixo)
            th = {}
        n_teor = r["teoremas"]; recibo_nome = "RECIBO_NOMEACAO_E_DERIVACAO_01nov.json"; recibo_p = os.path.join(E0, recibo_nome)
    if nome == "ObservadorTerminal":
        assert R_OBS["lean"]["sha256"] == e2_["sha256_antes"] and R_OBS["lean"]["bytes"] == e2_["bytes_antes"], ("a cadeia de custodia rompeu: R2.sha256_antes != o do recibo R2 do observador", nome, h[:16])
        assert R_OBS["sorry"] == 0 and R_OBS["fora_do_trio"] == [] and R_OBS["n_teoremas"] == 26
        th = {RENOMES_R2.get(n_, n_): v_ for n_, v_ in R_OBS["teoremas_no_trio"].items()}; assert "the_terminal_reads_one" not in th and "the_omega_pole_reads_one" in th
        n_teor = R_OBS["n_teoremas"]; recibo_nome = "RECIBO_PEDRA_OBSERVADOR_TERMINAL_31out_R2.json"; recibo_p = os.path.join(OBS, recibo_nome)
    if fonte == "identidade":
        assert R_IDT["lean"]["sha256"] == ERRATA[nome]["sha256_antes"] and R_IDT["lean"]["bytes"] == ERRATA[nome]["bytes_antes"], ("a cadeia de custodia rompeu: o sha256_antes da errata != o do recibo da Identidade", nome)
        assert R_IDT["sorry"] == 0 and R_IDT["fora_do_trio"] == [] and R_IDT["n_teoremas"] == 15
        th = dict(R_IDT["teoremas_no_trio"]); n_teor = R_IDT["n_teoremas"]; recibo_nome = "RECIBO_PEDRA_IDENTIDADE_01nov.json"; recibo_p = os.path.join(C405, recibo_nome)
    for n_ in NOVOS_R2.get(nome, []) + NOVOS_R3.get(nome, []) + NOVOS_R4.get(nome, []) + NOVOS_R5.get(nome, []) + NOVOS_R7.get(nome, []):   # os teoremas novos da R2 em diante entram com axiomas por medir: quem mede e' o Audit do kernel (a contagem sobe por MEDIDA, nao por presuncao); os nomes da R4 rebatizados na R7 entram com o nome vigente
        th[RENOMES_R7.get(n_, n_)] = []; n_teor += 1
    # «no trio» = a lista de axiomas de cada teorema e' SUBCONJUNTO de {propext, Classical.choice, Quot.sound} (o recibo R2 do observador lista os axiomas efetivos, p.ex. so' propext; os outros recibos listam os tres)
    assert len(th) == n_teor and all(set(v_) <= TRIO for v_ in th.values()), ("os teoremas do recibo nao estao todos no trio ou a contagem difere", nome, len(th), n_teor)
    curto = lambda n_: n_.split(".")[-1]
    th_nomes = set(th)
    if all("." not in n_ for n_ in th_nomes):   # o recibo R2 do observador traz os nomes curtos (sem o namespace)
        assert sorted(curto(n_) for n_ in impressos) == sorted(th_nomes), ("os #print axioms da fonte != os teoremas (curtos) do recibo", nome, sorted(set(curto(n_) for n_ in impressos) ^ th_nomes)[:4])
    else:
        assert set(impressos) == th_nomes, ("os #print axioms da fonte != os teoremas do recibo", nome, len(impressos), n_teor, sorted(set(impressos) ^ th_nomes)[:4])
    assert len(impressos) == n_teor and len(set(impressos)) == n_teor
    pino[k] = h[:16]
    detalhe[k] = {"modulo": "TGLExt." + nome, "arquivo": arq, "sha256": h, "bytes": len(b), "recibo": recibo_nome, "recibo_sha256": hashlib.sha256(open(recibo_p, "rb").read()).hexdigest(),
                  "errata": ({"recibo": os.path.basename(R_ERR_P), "recibo_sha256": hashlib.sha256(open(R_ERR_P, "rb").read()).hexdigest(), "sha256_antes": ERRATA[nome]["sha256_antes"], "sha256_depois": ERRATA[nome]["sha256_depois"]} if nome in ERRATA else None),
                  "errata_r2": {"recibo": os.path.basename(R2_P), "recibo_sha256": hashlib.sha256(open(R2_P, "rb").read()).hexdigest(), "sha256_antes": R2["pedras"][nome]["sha256_antes"], "sha256_depois": R2["pedras"][nome]["sha256_depois"]},
                  "errata_r7": {"recibo": os.path.basename(R7_P), "recibo_sha256": hashlib.sha256(open(R7_P, "rb").read()).hexdigest(), "mudou_na_r7": nome in MUDOU_R7, "sha256_depois": R7["pedras"][nome]["sha256_depois"]},
                  "errata_r6": {"recibo": os.path.basename(R6_P), "recibo_sha256": hashlib.sha256(open(R6_P, "rb").read()).hexdigest(), "mudou_na_r6": nome in MUDOU_R6, "sha256_depois": R6["pedras"][nome]["sha256_depois"]},
                  "errata_r5": {"recibo": os.path.basename(R5_P), "recibo_sha256": hashlib.sha256(open(R5_P, "rb").read()).hexdigest(), "sha256_antes": R5["pedras"][nome].get("sha256_antes"), "sha256_depois": R5["pedras"][nome]["sha256_depois"], "nota": R5["pedras"][nome].get("nota")},
                  "errata_r4": {"recibo": os.path.basename(R4_P), "recibo_sha256": hashlib.sha256(open(R4_P, "rb").read()).hexdigest(), "sha256_antes": R4["pedras"][nome].get("sha256_antes"), "sha256_depois": R4["pedras"][nome]["sha256_depois"], "nota": R4["pedras"][nome].get("nota")},
                  "errata_r3": {"recibo": os.path.basename(R3_P), "recibo_sha256": hashlib.sha256(open(R3_P, "rb").read()).hexdigest(), "sha256_antes": R3["pedras"][nome].get("sha256_antes"), "sha256_depois": R3["pedras"][nome]["sha256_depois"], "nota": R3["pedras"][nome].get("nota")},
                  "n_teoremas_no_trio": len(th), "teoremas": impressos, "sorry": 0, "crlf": b.count(b"\r\n")}
out = os.path.join(HERE, "pedras_sha16_da_ordem.json")
novo = json.dumps(pino, ensure_ascii=False)
if os.path.exists(out):
    assert open(out, encoding="utf-8").read().strip() == novo, "pedras_sha16_da_ordem.json ja existe e DIFERE: nao sobrescrevo"
else:
    open(out + ".tmp", "w", encoding="utf-8", newline="\n").write(novo + "\n"); assert os.path.getsize(out + ".tmp") > 0; os.replace(out + ".tmp", out)
json.dump(detalhe, open(os.path.join(HERE, "PINO_DAS_PEDRAS_DETALHE_v405.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(novo); print("teoremas:", {k: v["n_teoremas_no_trio"] for k, v in detalhe.items()}, "total", sum(v["n_teoremas_no_trio"] for v in detalhe.values()))
