# -*- coding: utf-8 -*-
"""Grava AFERICAO_kernel_v1_v386.json na propria pasta da afericao (lente KERNEL E V1), com sha256 dos artefatos lidos do disco."""
import json, hashlib, os, datetime, glob

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


arts = {}
for p in sorted(glob.glob("**/*", recursive=True)):
    if os.path.isfile(p) and not p.endswith("AFERICAO_kernel_v1_v386.json"):
        arts[p.replace(os.sep, "/")] = {"sha256": sha(p), "bytes": os.path.getsize(p)}

rep = {
    "lente": "KERNEL E V1 (aferidor adversarial)",
    "quando_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "mapa_consultado": "rotas.py consultar v386 -> 2 rotas (kernel.v386_tipagem_do_verbo EM_CURSO; ringdown.dephasing EXAMINADA_COM_DEFEITO); cabeca 514ea43a59b9853f",
    "kernel": {
        "pedra_sha256": "a67f2804103cf0328f0aad5ea24bdef90edfb667da9b2e467ccc97b5f5edb786", "pedra_bytes": 46291, "pedra_linhas": 766,
        "root_sha256": "1bbbb9e5138a4590913571306c743efef7f01455b5413d7eb0d912ca730e5ee7",
        "audit_sha256": "6884256a2622ef1960bc5315725af8e48921e23401a5a1f7bdd25dfe86de789d", "audit_linhas": 10083,
        "recompile_pedra": {"cmd": "lake env lean TGLExt/TheVerbSelectsTheAction.lean (sandbox v376/kernel_src)", "rc": 0, "stdout_stderr_bytes": 0,
                            "tempo_s": 24.4, "inicio_fim_utc": ["2026-10-05T19:45:21Z", "2026-10-05T19:45:46Z"]},
        "print_axioms": {"arquivo": "AferAxiomas_v386.lean (fora do sandbox; importa os .olean ja construidos)", "rc": 0, "tempo_s": 21.3, "semente": 386,
                         "5_ao_acaso": ["J_anticommutes_with_K", "triad_order_matters", "sigma3_ne_zero", "post1_isHermitian", "the_reading_of_the_posted_one"],
                         "novas": ["truth_and_cost_are_two_faces", "reading_the_truth_annihilates_the_superposition", "time_read_twice_confirms_the_post",
                                   "post1", "post2", "post3", "post1_isIdempotent", "post2_isIdempotent", "post3_isIdempotent",
                                   "post1_is_the_eigenprojector", "post2_is_the_eigenprojector", "post3_is_the_eigenprojector",
                                   "axis_posts_do_not_commute", "light_and_gravity_are_inseparable", "the_verb_selects_the_action"],
                         "fiacao_17": "todas", "total_print": 37, "fora_do_trio": 0,
                         "subconjunto": {"J_anticommutes_with_K": ["propext"], "the_name_above_every_name": ["Quot.sound"]},
                         "sorry_no_fonte": 0, "axiom_no_fonte": 0},
        "nomes_contestados": {"verb_como_projetor_def": 0, "light_precedes_gravity": 0, "fossil_em_nome": 0,
                              "verb_restante": ["the_verb_word_fixes_the_name", "the_verb_selects_the_action", "verbTypingStoneName", "verb_typing_stone_named"]},
        "fiacao_ang": {"existem_grep_r": 17, "linhas_no_Audit_cada": 1, "FLAGS_v386_json_ang_vs_grep_mismatches": 0},
        "candidato": {"pedra_embutida_sha256_igual": True, "flags_vrb_distintas": 93, "flags_ang_distintas": 17, "UM_VERSION": "v386"},
        "docstrings": {"quotes_total": 64, "segmentos_nao_verbatim_vs_txt": 36, "dos_quais_latex_transliterado_ou_caixa": "maioria",
                       "correcoes_silenciosas_dentro_de_aspas": ["l.21 i.(constante) <- i\\alpha^2", "l.86 interdependencia <- interdepend6encia",
                                                                "l.660 psionico-com-acento <- psionico", "l.141-142 elide ', como ja falamos,' sem reticencias",
                                                                "l.69/451 todo nome <- todo \"nome\""],
                       "estado_dinamico_estacionado_e_do_operador": "sim: transcrito 6da8f00d, type=user, 2026-10-05T11:19:54Z"},
        "AuditVerb_tmp_lean": "referencia nomes antigos; nao importado; excluido do embutido"},
    "v1_ramo_b": {
        "hashes_recomputados_batem": {"json": "86f98fcc124dd9cae04fdb06bd10c14175893253d5b139496bd4c05f109feee0",
                                      "md": "294b88a3632c1cea8e024b1471dd44ef3968614ca582e054307fffecb296da1c",
                                      "hashes": "16a3df7a77f439b593d0bdced4e6a45984a5aa0f54ce00f3443777653ad82447",
                                      "poder_json": "126adc100753c2ca6e65fb935a2bb89379ea72ee984cccb613afe5e8353cb782",
                                      "poder_py": "e4c99ccc1d8a506e9e10aba4ef1252116819722c38dd18804ec5a7785667e35b",
                                      "gerador": "48bf6267047acdd5aca6d54fb99bc98b3fffa9378d07e1a4880cd92beb0f9526"},
        "spec_sha256_recomputado": "bf2596999ae66520aae16ca4af120940f0efdb20a7606be27370f43e8ee462c0",
        "verbatins_sha256": {"RESPOSTAS_txt": "b49b0d9e60ee4646eae9e61cdea04b8bb779947940c161d6d19413156ea428b4",
                             "RESPOSTAS_json": "f172fdc2a56e1922ca9e092dd3bc7b9bcfd9392c20ad8f13d48da453af05d06c",
                             "DECISAO": "a5d548235522c1129ddd683887ac43d7fc2aec36095b7171af08c3ab076060f3",
                             "VERBO": "5973d79a49995c4c18e2567b83a5589403a113c44d694a8bfff43277033d5a70"},
        "poder_v2_recomputado": {"script_byte_identico": True, "folhas_json": 9290, "folhas_diferentes": ["/gerado"],
                                 "A_31_std": 11.382606423870937, "B_GWTC3_10": 6.367662614744814, "C_GW250114": 6.47561127208884,
                                 "iguais_ao_V1": True, "8k_x_3_conjuntos_iguais": True,
                                 "le_so_sigma_e_spin": "sim (dt[2]-dt[0]; sigma_tau; sp[1]=spin q50; median/mean_df so em comentarios l.12/75/78)"},
        "conjunto_D": {"n": 14, "registro_RINGDOWN_5SIGMA_V1_sha256": "e1be6b0409720c6883af5281458922fb03c5329bc0b08df7efe129d65e487416",
                       "eligible_True_no_registro": 14, "nomes_iguais": True, "holds_iguais": 4, "False": 22, "None_pendentes": 8, "criterio_presente": True},
        "kerr_conjecture": "spec.k.estatuto.chi_ne_0 = [CONJECTURE: Kay-Wald 1991]; decisao 8; MD l.90/108",
        "delegacao": {"decisoes_7_a_13_como": "decidido por delegacao", "verbatim": "o resto vc consegue responder tudo agroa",
                      "MD_decidido_por_delegacao": 7, "MD_verbatim": 1},
        "regex_proibida": {"json": 9, "md": 10, "todas_em_frases_de_proibicao": True, "alpha2": 0},
        "valores_centrais_no_documento": {"spec": 0, "fora_do_spec_NOT_BLIND": [
            "o_que_o_registro_ja_diz.V2_selada.delta_tau_medido = 0.1766470552326263 (GW250114, conjunto C)",
            "cegueira.dado_A_B_C[0]: +0,072 [+0,015; +0,134] (31 do GWTC-5.0, conjunto A)"]},
        "citacoes_de_linha": {"um.py:155704 BCW": True, "um.py:155706 kms_factor": True, "TheMatrixRule.lean:46": True,
                              "QGSolutionComplete.lean:36": True, "um.py L142400 escada": True},
        "espec_vs_runtime": {"campos_a_transcrever_25": "iguais", "numeros_13": "iguais", "arquivos_6": "iguais", "status_F2b": "igual", "F2B": "igual",
                             "beta_regra": "ESPEC/pins/docstring 1e-15 abs vs codigo 1e-9 rel (diff real 5.4e-13 rel)",
                             "veredito": "ESPEC PREREGISTRATION... vs runtime PREREGISTERED... (conferir_rito usa o runtime)",
                             "funcao": "ESPEC prove_ramo_b_preregistration_v386(ONE, core) vs runtime ramo_b_preregistration_v386(core, prereg=None)"},
        "core_v385": "involucro {core:{...}}: /core/beta=0.012031300400796606, /core/alpha, /core/the_ledger_of_charges_v383 existem; main() passa o core interno (L209552-209567)"},
    "artefatos_desta_afericao": arts,
}
json.dump(rep, open("AFERICAO_kernel_v1_v386.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("gravado AFERICAO_kernel_v1_v386.json", os.path.getsize("AFERICAO_kernel_v1_v386.json"), "B sha16", sha("AFERICAO_kernel_v1_v386.json")[:16])
for k, v in arts.items():
    print(" ", k, v["sha256"][:16], v["bytes"])
