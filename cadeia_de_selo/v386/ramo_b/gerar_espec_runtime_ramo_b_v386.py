# -*- coding: utf-8 -*-
"""gerar_espec_runtime_ramo_b_v386.py -- A ESPECIFICACAO do que o um.py v386 deve LER POR HASH e registrar sobre o ramo B (05/10/2026).
Le o V1 congelado na Bancada (PREREGISTRO_RAMO_B_RINGDOWN_V1.json/.md, V1_RAMO_B_HASHES.json, as copias do PODER v2), calcula os sha256 do disco
(nunca digitados), transcreve as chaves que o runtime deve copiar e grava ESPEC_RUNTIME_RAMO_B_v386.json ao lado deste script. O texto da errata de R6
para o livro leva o verbatim do operador de 17:11:36 UTC LIDO de DECISAO_OPERADOR_RAMO_B_05out.json. Nada se calcula de fisica aqui; nenhum valor central.
Uso: python gerar_espec_runtime_ramo_b_v386.py"""
import datetime
import hashlib
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
BANCADA = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_ramo_b_05out")
P_V1_JSON = os.path.join(BANCADA, "PREREGISTRO_RAMO_B_RINGDOWN_V1.json")
P_V1_MD = os.path.join(BANCADA, "PREREGISTRO_RAMO_B_RINGDOWN_V1.md")
P_HASHES = os.path.join(BANCADA, "V1_RAMO_B_HASHES.json")
P_PODER = os.path.join(BANCADA, "PODER_CEGO_RAMO_B_v2.json")
P_PODER_PY = os.path.join(BANCADA, "poder_cego_ramo_b_v2.py")
P_GERADOR = os.path.join(BANCADA, "gerar_preregistro_ramo_b_05out.py")
P_DECISAO = os.path.join(HERE, "DECISAO_OPERADOR_RAMO_B_05out.json")
P_RESP = os.path.join(HERE, "..", "RESPOSTAS_operador_05out.json")
OUT = os.path.join(HERE, "ESPEC_RUNTIME_RAMO_B_v386.json")


def fsha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 24), b""):
            h.update(chunk)
    return h.hexdigest()


def jload(p):
    return json.loads(open(p, "rb").read().decode("utf-8"))


V1 = jload(P_V1_JSON)
HS = jload(P_HASHES)
DEC = jload(P_DECISAO)
RESP = jload(os.path.abspath(P_RESP))
SPEC = V1["spec"]
# conferencias fail-closed: o hash gravado no V1_RAMO_B_HASHES bate o disco; o spec_sha256 bate o recomputado do spec
canon = lambda o: json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
assert hashlib.sha256(canon(SPEC).encode("utf-8")).hexdigest() == V1["spec_sha256"] == HS["spec_sha256"], "spec_sha256 nao confere"
for f, v in HS["arquivos"].items():
    assert fsha(v["caminho"]) == v["sha256"] and os.path.getsize(v["caminho"]) == v["bytes"], "V1_RAMO_B_HASHES nao confere com o disco: %s" % f
VERB_REABRE = DEC["verbatim"]
VERB_DELEG = RESP["trechos"]["delegacao"]
ARQ = {k: {"path": p.replace("\\", "/"), "sha256": fsha(p), "bytes": os.path.getsize(p)} for k, p in (("json", P_V1_JSON), ("md", P_V1_MD), ("hashes", P_HASHES), ("poder_json", P_PODER), ("poder_py", P_PODER_PY), ("gerador", P_GERADOR))}
HIP = SPEC["poder_cego"]["hipotese"]

ESPEC = {
    "id": "ESPEC_RUNTIME_RAMO_B_v386", "gerado_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "gerador": {"arquivo": os.path.basename(__file__), "sha256": fsha(os.path.abspath(__file__))},
    "para": "o candidato um.py v386 (nasce no scratchpad; o Nós e so leitura); molde: _V383_PREREG + _v383_read_prereg (dois lados) e _QP_PREREG (pilar) -- caminho e sha256 EMBUTIDOS, lidos do disco a cada rodada, conferidos byte a byte; nunca 'ok' falso",
    "regua": "nenhum valor central entra; nenhuma bandeira do gate depende do que entra (does_not_gate_core = True; the_gate_ignores_the_ledger); nenhum calculo novo de fisica -- o runtime TRANSCREVE o V1 e confere hashes; beta nunca literal (o runtime confere spec.beta.valor_runtime contra o seu proprio beta a 1e-15); NOT_FALSIFIED nunca e CONFIRMED; a RG e o limite classico",
    "preregistro_V1": {"identificador": V1["id"], "spec_sha256": V1["spec_sha256"], "spec_sha256_formula": V1["spec_sha256_formula"], "pasta": BANCADA.replace("\\", "/"), "arquivos": ARQ,
                       "ler_por_hash": ["json", "md", "hashes"], "conferir_tambem": ["poder_json", "poder_py"], "o_que_conferir": ["sha256 do JSON, do MD e do V1_RAMO_B_HASHES.json contra os embutidos", "spec_sha256 recomputado do objeto spec do JSON == o embutido", "cada entrada de V1_RAMO_B_HASHES.arquivos contra o disco (sha256 + bytes)", "spec.beta.valor_runtime == beta do rito (|diff| < 1e-15)"]},
    "registro_no_core": {
        "chave_proposta": "ramo_b_preregistration_v386", "funcao_proposta": "prove_ramo_b_preregistration_v386(ONE, core)", "molde_dos_campos": "the_axiom_v385 / quantum_pillar_reproducibility_v385: verdict, all_verified, checks, status, does_not_gate_core = True; mais read_ok, sha256_expected, sha256_read, error (como the_ledger_of_charges_v383.preregistration)",
        "campos_a_transcrever_do_V1_json": {
            "k": ["spec", "k"], "M_X": ["spec", "M_X"], "identificacao": ["spec", "identificacao"], "lugar": ["spec", "tau_star", "lugar"], "identidade_exata": ["spec", "identidade_exata"],
            "decisoes_por_delegacao": ["decisoes_por_delegacao"], "ratificacao": ["ratificacao", "frase_de_registro"], "ratificacao_quando_utc": ["ratificacao", "quando_utc"], "ratificacao_sha256_txt": ["ratificacao", "verbatim_inteiro_sha256_txt"],
            "conjunto_D": ["spec", "conjuntos", "D"], "conjuntos_NOT_BLIND": ["spec", "conjuntos", "A"], "poder_por_k": ["spec", "poder_cego", "por_k"], "poder_hipotese": ["spec", "poder_cego", "hipotese"], "sigma_comb_A31": ["spec", "poder_cego", "sigma_comb_A31"],
            "sigma_beta_lido": ["spec", "beta_lido"], "vereditos_permitidos_na_ordem": ["spec", "vereditos_permitidos_na_ordem"], "vereditos_proibidos": ["spec", "vereditos_proibidos"], "tokens": ["spec", "tokens"], "status": ["spec", "status"], "nao_decide": ["spec", "nao_decide"], "sistematica": ["spec", "sistematica"],
            "o_que_a_gerencia_errou_e_corrigiu": ["o_que_a_gerencia_errou_e_corrigiu"], "a_ponte_do_tempo_verbatim": ["a_ponte_do_tempo", "verbatim_operador_18_29_37"], "acervo_fase_de_retorno": ["a_ponte_do_tempo", "acervo"]},
        "numeros_que_o_runtime_transcreve_sem_recalcular": {"hipotese_k": HIP["k"], "poder_exato_A31": HIP["poder_exato"]["A_31_std"], "poder_exato_B10": HIP["poder_exato"]["B_GWTC3_10"], "poder_exato_C": HIP["poder_exato"]["C_GW250114"], "poder_x0p273": HIP["poder_exato"]["A_31_x0p273_difusao_de_fase"],
                                                           "delta_pred_A31_exato": HIP["delta_pred_ponderado"]["exato"], "sigma_comb_A31": SPEC["poder_cego"]["sigma_comb_A31"], "sigma_beta_lido_A31": SPEC["beta_lido"]["sigma_dita_antes_conjunto_A31_hipotese"], "sigma_beta_lido_sobre_beta_A31": SPEC["beta_lido"]["sigma_sobre_beta_A31_hipotese"],
                                                           "conjunto_D_n": SPEC["conjuntos"]["D"]["n_elegiveis"], "conjunto_D_sem_hold": SPEC["conjuntos"]["D"]["n_sem_pendencia_de_qualidade"], "k_em_chi_0": SPEC["k"]["em_chi_0"], "beta_runtime_do_V1": SPEC["beta"]["valor_runtime"]},
        "status": {"token_do_canal_no_livro": "AWAITING_PREREGISTRATION", "com_V1_lido_por_hash": "AWAITING (qualificador PRE_REGISTERED_V1_READ_BY_HASH__AWAITING_DATA)", "hash_divergente_ou_ausente": "AWAITING_PREREGISTRATION__V1_NOT_READ (fail-closed; erro dito)", "veredito_do_V1": SPEC["status"]["veredito_deste_V1"]},
        "veredito_proposto_do_registro": "TGL_RAMO_B_PREREGISTRATION_V386__V1_READ_BY_HASH_<sha16>__OTHER_LAW_OWN_CHANNEL_F2B__K_2PI_OVER_KAPPA_HAT_KMS__M_F_DET__ENVELOPE_ADDITIVE_RATE__SOURCE_LOCAL__SET_D_O4_14_BLIND_ONLY_TEST__A_B_C_NOT_BLIND_CALIBRATION__BETA_READ_DECLARED_SIGMA_STATED__AWAITING_DATA__DECIDED_BY_DELEGATION_2026_10_05__NOT_A_CONFIRMATION__GATE_UNTOUCHED",
        "veredito_se_falhar": "TGL_RAMO_B_PREREGISTRATION_V386__V1_NOT_READ__<motivo>__AWAITING_PREREGISTRATION__GATE_UNTOUCHED",
    },
    "livro_de_cobrancas": {
        "cobranca_nova_F2b": {"id": "F2b", "lado": "face", "criterio_de_lado": "o remanescente (o Nome M_f entregue) lendo o seu proprio custo como complemento (otica: |T|^2 + |R|^2 = 1) [ONTO -- gerencia, ratificado por delegacao]", "registro": "ringdown: conjunto D (14 de O4, cego; PE so-220 na casa, v387); A/B/C calibracao NOT_BLIND",
                              "lei": "OUTRA LEI: Gamma_omega = (1/2) beta tau* omega^2 com tau* = k G M_f/c^3, k = 2pi/kappa_hat(chi_f) (periodo KMS/modular do horizonte), fonte, envoltoria -- pre-registro V1 por hash", "chave_core": "ramo_b_preregistration_v386", "token": "AWAITING_DATA", "desfecho": "AWAITING", "como": "DECLARED",
                              "na_regra": False, "na_regra_motivo": "tau* = k GM/c^3 e hipotese [INPUT] fora do contorno (ringdown_scope_v376: 'hipotese [INPUT] fora do contorno'); fica AO LADO como R6 -- decisao da gerencia, confirmavel pelo operador",
                              "canal_futuro_com_falsified": True, "futuro": "v387: FALSIFIED_AT_5SIGMA do PAR (k, M, identificacao) / NOT_FALSIFIED_POWERED [__GR_TENSION_REPORTED] / NOT_FALSIFIED_UNDERPOWERED / INCONCLUSIVE_SYSTEMATICS pela MESMA funcao de veredito, lida por hash",
                              "regra_do_livro": "ONE_CHANNEL_PER_READING_LAW_IN_THE_RUNTIME -- F2b e canal de OUTRA lei; F2 (correspondencia com a RG, tau* = t_Planck) fica intocado; o numero de cobrancas passa de 11 a 12 (o conferidor do V1.4 dos dois lados continua a conferir 11 == len(_V383_LEDGER_INPUT): a F2b entra num registro proprio, ao lado, ou a gerencia estende o conferidor -- decisao da gerencia)"},
        "errata_ao_lado_de_R6": {"onde": "the_ledger_of_charges (v386): corrections_beside_20261005.R6 e corrections_beside_20261005.F2 -- AO LADO; readings_ratified_20261002.R6 e corrections_beside_20261002.R6 NAO se reescrevem",
                                 "verbatim_do_operador_17_11_36_utc": VERB_REABRE, "quando_utc": DEC["quando"], "arquivo": P_DECISAO.replace("\\", "/"), "sha256": fsha(P_DECISAO),
                                 "texto_R6": V1["a_chave_e_a_otica"]["errata_ao_lado_de_R6_para_o_core_v386"]["corrections_beside_20261005.R6"], "texto_F2": V1["a_chave_e_a_otica"]["errata_ao_lado_de_R6_para_o_core_v386"]["corrections_beside_20261005.F2"],
                                 "delegacao_verbatim_18_29_37_utc": VERB_DELEG, "delegacao_quando_utc": RESP["quando"], "delegacao_sha256_txt": RESP["sha256_txt"]},
        "F2_intocado": True, "R2_intocado": True,
    },
    "o_que_NAO_entra_na_v386": ["nenhum valor central de dtau220 (nem de A/B/C, que estao em disco)", "nenhuma PE; nenhum estimador rodado", "nenhum termo Lean de ringdown fingido: o V1 diz que o termo nao existe; o termo de IDENTIDADE tau* = k G m_X/c^3 (algebrico) e pedido a parte, ao lado, e nunca substitui a leitura por hash",
                                "nenhuma bandeira do gate; o degrau experimental continua lendo o V11 do piso", "nenhuma reescrita de R6/F2 ratificados: so correcao AO LADO"],
    "v387": {"o_que": "estagio cego do conjunto D (sigma_i, a_i, N, kappa_hat, delta_pred, poder, C1, C5 -> PODER_RAMO_B_ANTES_DE_ABRIR.json com hash) -> injecoes C2(b) -> abertura de D -> RESULTADO_RAMO_B_V1.json pela MESMA funcao de veredito -> o um.py le por hash e aplica a matriz do V1 sem recalcular; A/B/C abrem-se como calibracao NOT_BLIND",
             "custo_DECLARADO_CPU_h": SPEC["conjuntos"]["D"]["custo_DECLARADO_CPU_h"], "congelamento_do_conjunto_por_evento": "na v387, no estagio cego, antes de qualquer PE abrir (holds/pendentes podem mudar a lista; o criterio ja esta congelado)"},
    "ordem_de_conferencia_para_o_conferidor_da_versao_final": ["os arquivos em disco na pasta da Bancada existem e batem os sha256 embutidos", "o core v386 traz ramo_b_preregistration_v386 com read_ok = True", "o livro traz corrections_beside_20261005.R6/F2 e a F2b", "o selo lista os sha256 do V1 (json, md, hashes)", "nenhum CONFIRMED/PROVED_BY no veredito; gate intocado (18 bandeiras iguais a v385)"],
}
b = json.dumps(ESPEC, ensure_ascii=False, indent=1).encode("utf-8")
open(OUT + ".tmp", "wb").write(b); assert os.path.getsize(OUT + ".tmp") == len(b); os.replace(OUT + ".tmp", OUT)
print("ESPEC:", OUT, hashlib.sha256(b).hexdigest(), len(b))
for k, v in ARQ.items():
    print("  %-10s %s %d %s" % (k, v["sha256"], v["bytes"], v["path"]))
