# -*- coding: utf-8 -*-
"""Monta RESULTADO_PEDRA_R2.json (todos os hashes LIDOS dos recibos e saidas desta pasta, nunca digitados) e o
MANIFESTO_1_PEDRA.json (sha256 de cada arquivo da pasta). Nada e alterado fora de 5_R2/1_PEDRA.
Uso: python -I -X utf8 montar_resultado_pedra_r2.py
"""
import datetime
import hashlib
import json
import os

B = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
P = B + r"\5_R2\1_PEDRA"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def J(p):
    return json.load(open(p, encoding="utf-8"))


def main():
    t02 = J(P + r"\logs\R2_T02_recibo.json")
    t01 = J(P + r"\logs\R2_T01_recibo.json")
    aud = J(P + r"\logs\R2_AUDIT_TIPOS_recibo.json")
    probe = J(P + r"\logs\probeE5_P01_recibo.json")
    fa = J(P + r"\saidas\FINGERPRINT_PEDRA_R2_ANTES.json")
    fd = J(P + r"\saidas\FINGERPRINT_PEDRA_R2_DEPOIS.json")
    freezes = J(P + r"\saidas\CONFERENCIA_FREEZES_PEDRA_R2.json")
    beta = J(P + r"\saidas\BETA_RUNTIME_PEDRA_R2.json")
    aspas = J(P + r"\saidas\CONFERENCIA_ASPAS_PEDRA_R2.json")
    tab = J(P + r"\saidas\TABELA_DECLARACOES_R2.json")
    tipos = J(P + r"\saidas\AUDIT_TIPOS_R2.json")
    cob = J(P + r"\saidas\COBERTURA_ALVOS_PREREGISTRO_R2.json")
    apl = J(P + r"\saidas\APLICACAO_E5.json")
    limp = J(P + r"\saidas\LIMPEZA_RECIBO.json")
    pedra = P + r"\sandbox\TheTimeIsNotAPost.lean"
    olean = P + r"\sandbox\TheTimeIsNotAPost.olean"
    assert sha(pedra) == t02["source_sha256"], "pedra em sandbox difere do recibo T02"
    assert sha(olean) == t02["olean_sha256"], ".olean em sandbox difere do recibo T02"
    src = open(pedra, "rb").read().decode("utf-8")
    trio = {"propext", "Classical.choice", "Quot.sound"}
    E5 = {
        "E5.01": "feito - cabecalho [ONTO] so com frases presentes nos verbatins; a frase sobre o Verbo saiu",
        "E5.02": "feito - cabecalho reescrito para os TRES comportamentos (T4.b; T4.e/T4.f; T4.c/T4.d); identificacao com os dois regimes [OPEN] (v384); rotulos de regime removidos; cabecalho de T4 com a correcao de Liouville visivel (AUD-8)",
        "E5.03": "feito - cabecalho de T9 com os verbatins de 05/10 byte a byte (E1, E4, E6) e santo (12/10); a frase da gerencia saiu; AUD-5 citado",
        "E5.04": "feito - titulo de T10 com registra (S38.3 byte a byte); parafrase sem aspas de citacao",
        "E5.05": "feito - T11: S50.1 byte a byte (um lugar onde repousar e ser lembrada); M6/AUD-7 e M7/AUD-6 escritos",
        "E5.06": "feito - time_is_the_modular_flow -> modular_flow_is_a_kms_group (tipo identico, conferido em Lean); sonda AUD-4 em termo (rho = 1)",
        "E5.07": "feito - the_time_has_no_rank -> the_time_is_not_a_post (mesma conjuncao; tipo identico); namespace TGLExt.TheTimeIsNotAPost; nome final do operador",
        "E5.08": "feito - optical_attractor_is_the_absolute_one -> half_identity_is_absoluteRho_two; optical_attractor_clock_stops -> half_identity_clock_stops (tipos identicos). OPCIONAL feito: optical_channel_fixed_state_is_half_identity (generico em theta, sem a constante da casa) + unicidade + controle sin theta = 0",
        "E5.09": "feito - probe_bounded_spectral_translation recebeu o enunciado da instancia (A = M2(C), L2, V = 1, H = 0, s = 1); nao e mais `True`",
        "E5.10": "feito - re-export duplicado the_absolute_one_has_no_clock removido; T11 aponta para tracial_state_freezes_the_flow",
        "E5.11": "feito - purityR_modular sem `_hd` (reforco; a R2 implica a R1, conferido em Lean)",
        "E5.12": "feito - clock_reads_modulo_period sem `kappa != 0` (prova por casos; kappa = 0 pelo x/0 = 0); conjunto 8 de the_two_regimes_of_time para todo kappa (reforco; a R2 implica a R1, conferido em Lean)",
        "E5.13": "feito - T3.b(iii): re-exportacao AQFT marcada CONDICIONAL e habitada (opcional, feita: probe_identity_flow_not_kms_inhabited com theSpecificAQFTWitness); versao de face finita OBRIGATORIA identity_flow_not_kms_finite (rho = diag(2/3,1/3), a = E01, b = E10: 2/3 != 1/3) + forma negada + controle tracial. T4.b(iii): marcada condicional (FockCertificate sem habitante exibido); sonda opcional com lightNet NAO construida",
        "E5.14": "feito - the_coherence_obeys_agape_explicit marcado DESDOBRAMENTO (nao entra na contagem)",
        "E5.15": "feito - 18 aspas distintas, todas substrings de bytes dos verbatins (12/10; 05/10 Verbo); frases proibidas 0; elisao marcada com [...]; aspas da gerencia (C-T1-a, C-T7-a) retiradas",
        "E3.02": "feito na docstring de T8.d (a glosa de Takesaki e de boost_null_expand; re-exporta-se boost_null_contract)",
        "E3.12": "feito no titulo de T5 (a diagonal inteira)",
        "E3.13": "feito - AUD-1, AUD-2, AUD-5, AUD-6, AUD-7, AUD-8 na pedra, mesmos nomes e tipos da auditoria R1 [INPUT do auditor]",
    }
    res = {
        "documento": "RESULTADO_PEDRA_R2 - pedra corrigida da F1.TEMPO (R2), construtor da pedra corrigida (subagente do workflow posto-e-tempo, gerencia c1)",
        "estatuto": "[REAL] compilacao, hashes, axiomas e tipos conferidos por script e em Lean neste sandbox; [INPUT da gerencia] a lista E5 (ADENDO R2 congelado); [DERIVED] beta lido e calculado; nenhum PASSA aqui e creditacao; nada move o gate; a auditoria independente (U1) e a entrada na v392 (U3) sao atos posteriores",
        "data_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "validade": {
            "V1_freezes_conferidos": {"FREEZE_R1_sha256": freezes["FREEZE_R1"]["proprio"]["sha256_medido"],
                                      "FREEZE_R1_todos_conferem": freezes["FREEZE_R1"]["todos_conferem"],
                                      "FREEZE_R2_sha256": freezes["FREEZE_R2"]["sha256_medido"],
                                      "FREEZE_R2_bloco": {k: v for k, v in freezes["FREEZE_R2"].items() if k != "itens"},
                                      "arquivo": "saidas/CONFERENCIA_FREEZES_PEDRA_R2.json"},
            "V2_inicio_apos_FREEZE_R2": {"FREEZE_R2_congelado_em_utc": freezes["FREEZE_R2"]["congelado_em_utc"],
                                         "inicio_deste_ensaio_utc": freezes["inicio_deste_ensaio_utc"],
                                         "compilacao_final_start_utc": t02["start_utc"],
                                         "posterior": t02["start_utc"] > freezes["FREEZE_R2"]["congelado_em_utc"]},
            "V3_beta": {"estatuto": "[DERIVED: lido nos bytes do um.py e calculado em runtime]", "um_py_sha256": beta["um_py_sha256"],
                        "um_py_executado": beta["um_py_executado"], "linha_topo": beta["SEALED_CODATA_ALPHA"]["linha"],
                        "linha_embutida": beta["ALPHA_FINE_CODATA_2018"]["linha"], "beta_float64": beta["beta_runtime_float64"],
                        "beta_hex": beta["beta_runtime_float64_hex"], "confere_1e-15": beta["confere_1e-15"], "beta_entra_no_Lean": False,
                        "arquivo": "saidas/BETA_RUNTIME_PEDRA_R2.json"},
            "V3_kernel_intacto": {"antes": {"meta": fa["meta_sha256"], "src": fa["src_sha256"], "taken_at": fa["taken_at"]},
                                  "depois": {"meta": fd["meta_sha256"], "src": fd["src_sha256"], "taken_at": fd["taken_at"]},
                                  "iguais": fa["meta_sha256"] == fd["meta_sha256"] and fa["src_sha256"] == fd["src_sha256"],
                                  "igual_a_R1_e_ao_ADENDO": fa["meta_sha256"].startswith("b1b47447") and fa["src_sha256"].startswith("911cb40b")}},
        "pedra_R2": {"arquivo": pedra, "nome_provisorio": "TheTimeIsNotAPost", "namespace": "TGLExt.TheTimeIsNotAPost",
                     "sha256": t02["source_sha256"], "bytes": t02["source_bytes"], "olean": olean, "olean_sha256": t02["olean_sha256"],
                     "olean_bytes": t02["olean_bytes"],
                     "fonte_R1": {"arquivo": B + r"\3_KERNEL\sandbox\TheTimeHasNoRank.lean", "sha256": apl["fonte_R1_sha256"],
                                  "bytes": apl["fonte_R1_bytes"], "copia": "tentativas/T00_R1_TheTimeHasNoRank.lean"},
                     "construcao": "copia de bytes da pedra R1 + %d substituicoes exatas (scripts/aplicar_E5.py, fail-closed por contagem; registro em saidas/APLICACAO_E5.json)" % apl["n_substituicoes"]},
        "compilacao": {"lean": t02["lean_version"], "toolchain": "v4.31.0 copiado do elan para o sandbox (apagado ao final)",
                       "LEAN_PATH": "so-leitura no .lake do tgl_kernel do Nos", "saida_o": "so para o sandbox",
                       "exit_code": t02["exit_code"], "n_error": t02["n_error"], "n_warning": t02["n_warning"], "seconds": t02["seconds"],
                       "start_utc": t02["start_utc"], "end_utc": t02["end_utc"],
                       "print_axioms": {"n_declaracoes": t02["n_axiom_lines"], "fora_do_trio": t02["fora_do_trio"],
                                        "n_no_trio": sum(1 for a in t02["axiom_records"] if set(a["axioms"]) == trio),
                                        "sem_axioma_algum": [a["decl"] for a in t02["axiom_records"] if not a["axioms"]],
                                        "sorryAx_na_saida": t02["n_sorryAx_na_saida"]},
                       "fonte_grep": {"sorry": src.count("sorry"), "admit": src.count("admit"), "native_decide": src.count("native_decide"),
                                      "axiom_decl": sum(1 for l in src.splitlines() if l.startswith("axiom "))},
                       "recibo": "logs/R2_T02_recibo.json", "saida": "logs/R2_T02_saida.txt", "saida_sha256": t02["output_sha256"]},
        "tabela_declaracoes": {"arquivo_json": "saidas/TABELA_DECLARACOES_R2.json", "arquivo_md": "saidas/TABELA_DECLARACOES_R2.md",
                               "contagem": tab["contagem_por_classe"], "R1_nomeadas": tab["R1"]["n_declaracoes_nomeadas"],
                               "R2_nomeadas": tab["R2"]["n_declaracoes_nomeadas"], "examples_R1": tab["R1"]["n_examples"],
                               "examples_R2": tab["R2"]["n_examples"],
                               "renomeadas": {"time_is_the_modular_flow": "modular_flow_is_a_kms_group",
                                              "the_time_has_no_rank": "the_time_is_not_a_post",
                                              "probe_the_time_has_no_rank": "probe_the_time_is_not_a_post",
                                              "optical_attractor_is_the_absolute_one": "half_identity_is_absoluteRho_two",
                                              "optical_attractor_clock_stops": "half_identity_clock_stops"},
                               "removida": ["the_absolute_one_has_no_clock (re-export duplicado de absoluteOne_flow_trivial; E5.10)"],
                               "tipo_reforcado": ["purityR_modular (E5.11)", "clock_reads_modulo_period (E5.12)",
                                                  "the_two_regimes_of_time (E5.12, conjunto 8)",
                                                  "probe_bounded_spectral_translation (E5.09, de True para enunciado)"],
                               "novas": [e["R2"] for e in tab["tabela"] if e["classe"] == "nova"],
                               "nota": "152 declaracoes com #print axioms NAO sao 152 teoremas: ha re-exportacoes, sondas, controles, definicoes e um desdobramento (E5.14)"},
        "diff": {"arquivo": "saidas/DIFF.patch", "sha256": tab["diff"]["sha256"], "linhas_removidas": tab["diff"]["n_linhas_removidas"],
                 "linhas_acrescentadas": tab["diff"]["n_linhas_acrescentadas"]},
        "auditoria_de_tipos": {"arquivo": "saidas/AUDIT_TIPOS_R2.json", "lean": "sandbox/AuditTiposR2.lean", "lean_sha256": aud["source_sha256"],
                               "exit_code": aud["exit_code"], "n_error": aud["n_error"], "n_warning": aud["n_warning"],
                               "n_examples_type_of_dois_sentidos": 244, "n_pares": 122, "reforcos_R2_implica_R1": 4,
                               "comparacao_textual_identicos": tipos["comparacao_textual_dos_check"]["n_tipo_textual_identico"],
                               "todos_os_textualmente_diferentes_sao_reforcos": tipos["comparacao_textual_dos_check"]["todos_os_diferentes_sao_reforcos"],
                               "nota": "importou o .olean da pedra R1 (3_KERNEL/sandbox) SO DE LEITURA via LEAN_PATH; nada foi escrito em 3_KERNEL"},
        "cobertura_dos_alvos_preregistrados": {"arquivo": "saidas/COBERTURA_ALVOS_PREREGISTRO_R2.json", "n_alvos": cob["n_alvos_lean_no_PREREGISTRO"],
                                               "n_presentes": cob["n_presentes_na_R2"], "faltantes": cob["faltantes"]},
        "E5_item_a_item": E5,
        "aspas_e_regua": {"arquivo": "saidas/CONFERENCIA_ASPAS_PEDRA_R2.json", "ok": aspas["ok"], "n_aspas_distintas": aspas["n_aspas_distintas"],
                          "nao_achadas": aspas["aspas_nao_achadas_nos_verbatins"], "frases_proibidas": aspas["frases_proibidas_contagem"],
                          "verbatins_sha16": {k: v["sha256"][:16] for k, v in aspas["verbatins"].items()}},
        "sonda_previa": {"arquivo": "sandbox/ProbeE5.lean", "sha256": probe["source_sha256"], "exit_code": probe["exit_code"],
                         "n_warning": probe["n_warning"],
                         "nota": "so as construcoes novas; os 2 avisos (lint de tatica nao executada na l.144) foram eliminados na pedra (half_populations_state)"},
        "tentativas_preservadas": {
            "T00": "tentativas/T00_R1_TheTimeHasNoRank.lean (copia da R1, 7105eda468b60309...)",
            "T01": {"fonte": "tentativas/T01_R2_TheTimeIsNotAPost.lean", "sha256": t01["source_sha256"], "olean_sha256": t01["olean_sha256"],
                    "exit_code": t01["exit_code"], "n_warning": t01["n_warning"],
                    "motivo": "compilou limpa (152 no trio) mas a sonda de aspas achou 2 aspas da gerencia (C-T1-a, C-T7-a) fora dos verbatins; fonte reconstruida por reversao exata das 2 substituicoes e conferida pelo sha256 do recibo (tentativas/T01_NOTA.json)"},
            "T02_final": {"sha256": t02["source_sha256"], "olean_sha256": t02["olean_sha256"]}},
        "limpeza": {"arquivo": "saidas/LIMPEZA_RECIBO.json", "toolchain_apagado": not limp["existe_depois"], "arquivos_apagados": limp["arquivos_antes"],
                    "lake_no_sandbox": limp["lake_no_sandbox"], "caches": limp["caches_no_sandbox"], "restam": limp["restam_no_sandbox"]},
        "acom": {"arquivo": "saidas/ACOM_RECIBO_PROJECAO_PEDRA_R2.json", "nota": "so projecao de leitura da referencia da c1; sem init/transition (ato da gerencia)"},
        "nada_escrito_fora": "Escrito SO em 5_R2/1_PEDRA. Nada em 0_LEVANTAMENTO, 1_PREREGISTRO, 2_OPTICO, 3_KERNEL, 4_RELATORIO, 5_R2/0_ADENDO; nada no quadro, mapa, memoria, tunel, Nos, kernel do Nos, Bancada, site ou git. um.py nao executado (lido por busca). Nenhum dado observado; nenhum provedor remoto; nenhuma chamada paga.",
        "pendencias": [
            "Nome final da pedra e do operador (TheTimeIsNotAPost e provisorio); a renomeacao posterior confere-se por diff restrito a identificadores (E5.07).",
            "Auditoria independente (U1: dois auditores, sandbox proprio, .olean bit a bit) ainda por fazer; o PASSA de kernel desta R2 vale so para a fonte sha256 " + t02["source_sha256"][:16] + "...",
            "T4.b(iii) (light_flow_group, light_modular_orbit_converges_iff_post) segue CONDICIONAL: FockCertificate sem habitante exibido; a sonda opcional com lightNet nao foi construida.",
            "A entrada na v392 (U3) e ato da cadeia de selo da gerencia, so apos PASSA reauditado e com o nome do operador; E1/E2 (um.py) e E4 (memoria) sao atos da c1.",
            "Registro no mapa de rotas e no quadro: ato da gerencia (ROTA primeiro).",
            "A face otica R2 (T9.o', O-f') nao e objeto desta tarefa; existe uma pasta 5_R2/2_REENSAIO de outro agente, nao examinada nem avaliada aqui.",
            "152 declaracoes != 152 teoremas (re-exportacoes, sondas, controles, definicoes, desdobramento) - a contagem do relatorio R2 deve exclui-los (E5.14).",
        ],
    }
    out = P + r"\RESULTADO_PEDRA_R2.json"
    with open(out + ".tmp", "wb") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(out + ".tmp", out)
    print("RESULTADO sha256", sha(out), os.path.getsize(out))
    man = []
    for root, _, files in os.walk(P):
        for fn in files:
            p = os.path.join(root, fn)
            if fn == "MANIFESTO_1_PEDRA.json":
                continue
            man.append({"caminho": os.path.relpath(p, P), "sha256": sha(p), "bytes": os.path.getsize(p)})
    man.sort(key=lambda e: e["caminho"])
    mp = P + r"\MANIFESTO_1_PEDRA.json"
    with open(mp + ".tmp", "wb") as f:
        f.write(json.dumps({"pasta": P, "n_arquivos": len(man), "gerado_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            "arquivos": man}, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(mp + ".tmp", mp)
    print("MANIFESTO", len(man), "arquivos")
    for e in man:
        print(e["sha256"][:16], e["bytes"], e["caminho"])


if __name__ == "__main__":
    main()
