# -*- coding: utf-8 -*-
"""comparar_v405_v406.py -- NADA DA v405 PERDIDO: compara, no=a=no (AST), a v405 SELADA (base_v405\\um.py) com o candidato v406: todo no nomeado da v405 existe no candidato IGUAL, ou foi mudado por um PATCH declarado (EXPLICACOES abaixo, uma por no), ou foi REMOVIDO de proposito
(nenhum: a v406 nao remove nome algum). Todo no mudado SEM explicacao, todo no removido, todo no anonimo perdido ou novo reprovam (rc 1). Os nos NOVOS esperados sao so' os da v406 (o registro com funcao `fechamento_v406` e a mecanica dele, os auxiliares da leitura do certificado habitado, a guarda das frases, o contrato, os textos, as fontes, as falas, os
registros por spec `cunhagens_v406` e `kh_n1_cobertura_v406` e o `_v406_rodar_specs`). A v406 e' um BUNDLE de modulos de kernel (301 em TGLExt/F1Fecho394), nao um conjunto de pedras: nao ha funcao de pedra nova.
ADAPTADO a v406 (02/11/2026, a partir do comparar_v404_v405.py): os 32 patches do `CANDIDATO_v406.json` (campo `patches`) sao mapeados aos nos que eles mudam (PATCH_PARA_NOS): o conjunto de ids tem de ser IGUAL ao do candidato e a uniao dos nos tem de ser IGUAL ao conjunto dos nos mudados, nem um a mais nem um a menos.
O que tem de ficar IGUAL (conferido): o gate (evaluate_quantum_gravity_closure e prove_qg_closure_gate), prove_neutrino_mass_gravitational (a errata do angulo e' AO LADO), ramo_b_preregistration_v386 e ledger_errata_v386 (o V1 e o livro nao sao reescritos), prove_ga_mass_audit, prove_joint_coincidence_result_v3, GA_WINDOW_STATUS, o run_um (onde o
witness_layers e' medido sobre o kf do rito), a funcao do kernel (verify_tgl_kernel_formalization) e TODO registro da v405 (as oito funcoes de pedra, `_v405_rodar_specs`, o miolo `_v405_*`); so' os CONTRATOS e SPECS que carregam a escada ou o estado das chaves mudam, pelos patches C12 a C16 declarados.
Escreve COMPARACAO_V405_v406.json. Os numeros das explicacoes sao LIDOS de CANDIDATO_v406.json, nunca digitados.
uso: python -I -B -X utf8 comparar_v405_v406.py"""
import ast, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v406 as DL  # noqa: E402
A = ast.parse(open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")); B = ast.parse(open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8"))
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v406.json"), encoding="utf-8"))
E_ANT, E_NOVA = CM["escada"]; NB = CM["n_bandeiras"]; NM = CM["kernel"]["modulos_novos"]
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
EXPL_CONTRATO = "C12: expected_ladder %d -> %d" % (E_ANT, E_NOVA)
EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao v405 -> v406",
    "_EMBEDDED_KERNEL_FILES": "K00/K01: a raiz TGLExt.lean regenerada (+ os dois imports do fecho; o Audit nao muda) e +%d modulos Lean em TGLExt/F1Fecho394 (os 300 da bancada do ChatGPT e a candidata CanonicalFullTGLWitnessR1)" % NM,
    "_LEAN_THEOREM_FLAGS": "V01: +%d bandeiras ext_fch406_NNNN (so' declaracao nomeada)" % NB,
    "prove_external_ladder": "V02: a lista ext_flags ganha as %d bandeiras (a escada %d -> %d)" % (NB, E_ANT, E_NOVA),
    "_ESQUELETO_STONES": "V03: o ledger de pedras ganha os %d modulos do bundle" % NM,
    "_V394_FORMAL_CONTRACT": EXPL_CONTRATO, "_V394_QUADRATIC_CONTRACT": EXPL_CONTRATO, "_V394_NETWORK_CONTRACT": EXPL_CONTRATO, "_V395_PSIBIT_CONTRACT": EXPL_CONTRATO,
    "_V396_TESTEMUNHA_CONTRACT": EXPL_CONTRATO, "_V398_SONICO_CONTRACT": EXPL_CONTRATO, "_V398_AFINACAO_CONTRACT": EXPL_CONTRATO, "_V401_FALSIDADE_CONTRACT": EXPL_CONTRATO,
    "_V402_CONTRACTS": EXPL_CONTRATO + " nos tres contratos da v402 (ponte, queda, esperanca)", "_V403_CONTRACTS": EXPL_CONTRATO + " nos tres contratos de pedra da v403 (caminho, vida, adendo da verdade; o do gate fica None)",
    "_V404_CONTRACTS": EXPL_CONTRATO + " nos dois contratos de pedra da v404 (projecao, jo8v32; o da errata de F2b fica None)", "_V405_CONTRACTS": EXPL_CONTRATO + " nos oito contratos de pedra da v405",
    "_V394_SPECS": "C14: cunhagens_v394 u4 (whole_certificate_inhabited) falso -> verdadeiro (+ errata E17 ao lado); o veredito do registro nao muda de prefixo",
    "_V395_SPECS": "C15: cunhagens_v395 u3 (status) -> INHABITED_BY_physicalFockCertificate_V406 e u4 falso -> verdadeiro (+ errata E17 ao lado)",
    "_V396_SPECS": "C16: cunhagens_v396 u3 (status) -> INHABITED_BY_physicalFockCertificate_V406 e u5 falso -> verdadeiro (+ errata E17 ao lado)",
    "_V405_SPECS": "C13: kh_n1_cobertura_v405 h2/h3/h6 viram pisos e h8 o tamanho minimo; gap_v405 x_i falso -> verdadeiro (+ errata E17 ao lado); os vereditos nao mudam",
    "rede_fock_v394": "C17/C17b: whole_certificate_inhabited deixa de ser o literal False e passa a LEITURA do kernel (_v406_certificado_habitado; +inhabited_by_v406, joint_contract_v406, errata_v406) e o veredito ganha a variante JOINT_CERTIFICATE_INHABITED_V406 (a TROCA DITA)",
    "psibit_v395": "C18: conditional_psion_face.inhabitant_exhibited e status deixam de ser literais e passam a leitura do kernel (reading_v395 guarda o texto antigo; +inhabited_by_v406, errata_v406); o veredito NAO muda",
    "testemunha_estatica_v396": "C19: fock_face.inhabitant_exhibited e status deixam de ser literais e passam a leitura do kernel (reading_v396 guarda o texto antigo; linked_to_the_corner_by_a_lemma SEGUE False; +errata_v406); o veredito NAO muda",
    "main": "N00/N02: as chamadas do `fechamento_v406` e dos registros por spec da v406 (depois do bloco `_v405_rodar_specs`, antes de emit_figures; try/AVISO) e as chaves novas do selo (fechamento_v406, registros_v406); nada do que existia muda",
    "build_pt": "W04: a secao «O fechamento: a passagem para o continuo e o certificado habitado» do artigo PT, antes da secao v405 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",
    "build_en": "W05: the section «The closure: the passage to the continuum and the inhabited certificate» of the EN article, before the v405 section (the box at the top does NOT change)",
    "emit_canonical_md": "W09: a linha «O fechamento (v406, 02/11/2026)» no .md canonico, antes da linha da v405 (o quadro do topo NAO muda)",
}
# cada patch do CANDIDATO_v406.json -> os nos nomeados da base que ele muda (W02 so' ACRESCENTA nos novos: nenhum no da base)
PATCH_PARA_NOS = {"W01_versao": ["UM_VERSION"], "K00_TGLExt.lean": ["_EMBEDDED_KERNEL_FILES"], "K01_modulos_novos": ["_EMBEDDED_KERNEL_FILES"], "V01_bandeiras": ["_LEAN_THEOREM_FLAGS"], "V02_escada": ["prove_external_ladder"], "V03_ledger": ["_ESQUELETO_STONES"],
                  "W09_md": ["emit_canonical_md"], "W04_artigo_PT": ["build_pt"], "W05_artigo_EN": ["build_en"], "W02_runtime_v406": [],
                  "C13_specs_v405_pisos_e_gap": ["_V405_SPECS"], "C14_specs_v394_u4": ["_V394_SPECS"], "C15_specs_v395_u3_u4": ["_V395_SPECS"], "C16_specs_v396_u3_u5": ["_V396_SPECS"],
                  "C17_rede_fock_literal_vira_leitura": ["rede_fock_v394"], "C17b_rede_fock_veredito": ["rede_fock_v394"], "C18_psibit_literal_vira_leitura": ["psibit_v395"], "C19_testemunha_literal_vira_leitura": ["testemunha_estatica_v396"],
                  "N00_main_fechamento": ["main"], "N02_selo": ["main"]}
PATCH_PARA_NOS.update({"C12_" + x: [x] for x in ("_V405_CONTRACTS", "_V404_CONTRACTS", "_V403_CONTRACTS", "_V402_CONTRACTS", "_V401_FALSIDADE_CONTRACT", "_V398_SONICO_CONTRACT", "_V398_AFINACAO_CONTRACT", "_V396_TESTEMUNHA_CONTRACT", "_V395_PSIBIT_CONTRACT", "_V394_FORMAL_CONTRACT", "_V394_QUADRATIC_CONTRACT", "_V394_NETWORK_CONTRACT")})
NOVOS_ESPERADOS = set(DL.REGISTROS_FUNCAO) | {"v406_fechamento_mechanics", "_v406_certificado_habitado", "_v406_chaves", "_v406_formal", "_v406_guarda_frases", "_V406_FECHO_CONTRACT", "_V406_FECHO_TEXT", "_V406_FONTES", "_V406_VERBATINS2", "_V406_RECUSA",
                                              "_V406_NOMES_REGISTROS", "_V406_REGISTROS_FUNCAO", "_V406_SPECS", "_v406_rodar_specs"}
FUNCOES_QUE_NAO_PODEM_MUDAR = tuple(CM["gate_nao_se_move"]["funcoes_identicas_a_base"])   # lidas do candidato (o gerador conferiu); abaixo, a lista minima que a v405 ja' exigia
FUNCOES_MINIMAS = ("evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "prove_ga_mass_audit", "prove_joint_coincidence_result_v3", "GA_WINDOW_STATUS")
MAIS_QUE_NAO_PODEM_MUDAR = ("run_um", "verify_tgl_kernel_formalization")


def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        return n.targets[0].id
    return None


def todos(tree, nome):
    return [n for n in tree.body if nm(n) == nome]


da = {nm(n): n for n in A.body if nm(n)}; db = {nm(n): n for n in B.body if nm(n)}
mud = []
for k in da:
    if k not in db:
        continue
    la, lb = todos(A, k), todos(B, k)
    if [h(x) for x in la] != [h(x) for x in lb]:
        mud.append(k)
ig = [k for k in da if k in db and k not in mud]
rem = [k for k in da if k not in db]; nov = sorted(k for k in db if k not in da)
anon_a = [n for n in A.body if not nm(n)]; anon_b = [n for n in B.body if not nm(n)]
sa, sb = {}, {}
for n in anon_a:
    sa.setdefault(h(n), []).append(n)
for n in anon_b:
    sb.setdefault(h(n), []).append(n)
anon_perdidos = [n for k, v in sa.items() for n in v[len(sb.get(k, [])):] if len(sb.get(k, [])) < len(v)]
anon_novos = [n for k, v in sb.items() for n in v[len(sa.get(k, [])):] if len(sa.get(k, [])) < len(v)]
anon_novos_txt = [ast.unparse(n)[:160] for n in anon_novos]
# os nos anonimos novos esperados: so' os dois `update` que entregam as fontes e as falas da v406 ao motor de registros (v392)
anon_novos_ok = len(anon_novos_txt) == 2 and sum("_V392_FONTES.update(_V406_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V406_VERBATINS2)" in x for x in anon_novos_txt) == 1
sem_explicacao = [k for k in mud if k not in EXPLICACOES]
explicados_sem_mudar = [k for k in EXPLICACOES if k not in mud]
intactas = {f: bool(todos(A, f) and [h(x) for x in todos(A, f)] == [h(x) for x in todos(B, f)]) for f in sorted(set(FUNCOES_QUE_NAO_PODEM_MUDAR) | set(FUNCOES_MINIMAS) | set(MAIS_QUE_NAO_PODEM_MUDAR))}
# TODO no da v405 que nasceu nela (registros com funcao, miolo `_v405_*`, constantes `_V405_*` que nao sao contrato/spec escada) segue IGUAL
herdados_v405 = sorted(k for k in da if (k.startswith("_v405") or k.startswith("v405_") or k.endswith("_v405") or k.startswith("_V405_")) and k not in ("_V405_CONTRACTS", "_V405_SPECS"))
v405_mexidos = [k for k in herdados_v405 if k in mud]
# os patches do candidato == os patches mapeados; a uniao dos nos == os nos mudados
ids_cand = sorted(p["id"] for p in CM["patches"]); ids_map = sorted(PATCH_PARA_NOS)
nos_dos_patches = sorted({n_ for v in PATCH_PARA_NOS.values() for n_ in v})
patches_ok = bool(ids_cand == ids_map and len(ids_cand) == CM["n_patches"] and nos_dos_patches == sorted(mud))
res = {"nos_nomeados_v405": len(da), "iguais": len(ig), "mudados": {k: EXPLICACOES.get(k, "SEM EXPLICACAO") for k in mud}, "n_mudados": len(mud), "removidos": rem, "novos": nov, "n_novos": len(nov), "novos_esperados": sorted(NOVOS_ESPERADOS),
       "anonimos_perdidos": [ast.unparse(n)[:160] for n in anon_perdidos], "anonimos_novos": anon_novos_txt, "os_dois_anonimos_novos_sao_os_update_das_fontes_e_das_falas_v406": anon_novos_ok,
       "mudados_sem_explicacao": sem_explicacao, "explicacao_sem_mudanca": explicados_sem_mudar, "funcoes_intactas": intactas, "o_gate_nao_se_move_e_a_v386_nao_e_reescrita": all(intactas.values()),
       "herdados_da_v405_conferidos": len(herdados_v405), "herdados_da_v405_mexidos": v405_mexidos,
       "patches": {"n_no_candidato": CM["n_patches"], "n_mapeados": len(ids_map), "ids_so_no_candidato": sorted(set(ids_cand) - set(ids_map)), "ids_so_no_mapa": sorted(set(ids_map) - set(ids_cand)), "nos_mudados_sem_patch": sorted(set(mud) - set(nos_dos_patches)), "nos_de_patch_nao_mudados": sorted(set(nos_dos_patches) - set(mud)), "ok": patches_ok},
       "candidato_sha16": CM["sha16"]}
res["ok"] = bool(not sem_explicacao and not rem and set(nov) == NOVOS_ESPERADOS and not anon_perdidos and anon_novos_ok and not explicados_sem_mudar and all(intactas.values()) and not v405_mexidos and patches_ok
                 and set(FUNCOES_MINIMAS) <= set(FUNCOES_QUE_NAO_PODEM_MUDAR) and hashlib.sha256(open(os.path.join(HERE, DL.CANDIDATO), "rb").read()).hexdigest()[:16] == CM["sha16"])
json.dump(res, open(os.path.join(HERE, "COMPARACAO_V405_v406.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, (dict, list)) else (len(v) if k not in ("mudados_sem_explicacao", "removidos", "anonimos_perdidos", "novos", "explicacao_sem_mudanca", "funcoes_intactas", "herdados_da_v405_mexidos", "patches") else v)) for k, v in res.items()}, ensure_ascii=False)); print("mudados:", sorted(mud))
sys.exit(0 if res["ok"] else 1)
