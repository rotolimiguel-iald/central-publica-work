# -*- coding: utf-8 -*-
"""comparar_v403_v404.py -- NADA DA v403 PERDIDO: compara, no=a=no (AST), a v403 SELADA (base_v403\\um.py) com o candidato v404: todo no nomeado da v403 existe no candidato IGUAL, ou foi mudado por um PATCH declarado (EXPLICACOES abaixo, uma por no), ou foi REMOVIDO de proposito
(nenhum: a v404 nao remove nome algum). Todo no mudado SEM explicacao, todo no removido, todo no anonimo perdido ou novo reprovam (rc 1). Os nos NOVOS esperados sao so' os da v404 (os tres registros com funcao e as duas mecanicas, o leitor da deformacao, o miolo comum, os contratos, os textos, as fontes, as falas, os specs e o rodar_specs).
O GATE NAO SE MOVE: as funcoes evaluate_quantum_gravity_closure e prove_qg_closure_gate, e tambem prove_neutrino_mass_gravitational (a errata do angulo e' AO LADO), ramo_b_preregistration_v386 e ledger_errata_v386 (o V1 e o livro nao sao reescritos), sao conferidas IGUAIS (nao estao em EXPLICACOES).
Escreve COMPARACAO_V403_v404.json. Escrito a mao para a v404 (os numeros das explicacoes sao LIDOS de CANDIDATO_v404.json, nunca digitados). Molde: comparar_v402_v403.py.
uso: python -I -B -X utf8 comparar_v403_v404.py"""
import ast, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v404 as DL  # noqa: E402
A = ast.parse(open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")); B = ast.parse(open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8"))
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v404.json"), encoding="utf-8"))
E_ANT, E_NOVA = CM["escada"]; NB = CM["n_bandeiras"]
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
EXPL_CONTRATO = "C12: expected_ladder %d -> %d" % (E_ANT, E_NOVA)
EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao v403 -> v404",
    "_EMBEDDED_KERNEL_FILES": "K00/K01: a raiz TGLExt.lean regenerada (+ os dois imports das pedras; o Audit nao muda) e +2 modulos Lean (TGLExt/ProjecaoTransversalDaMeiaNat.lean, TGLExt/Jo8v32.lean)",
    "_LEAN_THEOREM_FLAGS": "V01: +%d bandeiras das duas pedras (so' declaracao nomeada)" % NB,
    "prove_external_ladder": "V02: a lista ext_flags ganha as %d bandeiras (a escada %d -> %d)" % (NB, E_ANT, E_NOVA),
    "_ESQUELETO_STONES": "V03: o ledger de pedras ganha as duas pedras da v404",
    "_V403_SPECS": "C13: kh_n1_cobertura_v403 h2/h3/h6 viram pisos e h8 o tamanho minimo (+ errata ao lado); o veredito do registro nao muda",
    "_V394_FORMAL_CONTRACT": EXPL_CONTRATO, "_V394_QUADRATIC_CONTRACT": EXPL_CONTRATO, "_V394_NETWORK_CONTRACT": EXPL_CONTRATO, "_V395_PSIBIT_CONTRACT": EXPL_CONTRATO,
    "_V396_TESTEMUNHA_CONTRACT": EXPL_CONTRATO, "_V398_SONICO_CONTRACT": EXPL_CONTRATO, "_V398_AFINACAO_CONTRACT": EXPL_CONTRATO, "_V401_FALSIDADE_CONTRACT": EXPL_CONTRATO,
    "_V402_CONTRACTS": EXPL_CONTRATO + " nos tres contratos da v402 (ponte, queda, esperanca)", "_V403_CONTRACTS": EXPL_CONTRATO + " nos tres contratos de pedra da v403 (caminho, vida, adendo da verdade; o do gate fica None)",
    "main": "N00/N00b/N01/N02: as chamadas dos tres registros com funcao (projecao transversal e jo8v32 depois das bandeiras do gate; a errata de F2b depois da errata ao lado de R6 da v386) e dos specs v404 e as chaves novas do selo (try/AVISO; nada do que existia muda)",
    "build_pt": "W04 e F2B: a secao «Jo 8,32 e a projecao transversal da Meia-Nat» do artigo PT, antes da secao v403; a linha do ramo B da tabela e a frase das contagens leem o estado do canal F2b do registro novo (o quadro «O Teste da Unica Palavra» do topo NAO muda)",
    "build_en": "W05 e F2B: the section «John 8:32 and the transverse projection of the Half-Nat» of the EN article, before the v403 section; the branch B row of the table and the counts sentence read the F2b channel state from the new record (the box at the top does NOT change)",
    "emit_canonical_md": "W09: a linha «Jo 8,32 e a projecao transversal da Meia-Nat (v404)» no .md canonico, antes da linha da v403 (o quadro do topo NAO muda)",
}
NOVOS_ESPERADOS = {"projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404", "v404_projecao_mechanics", "v404_jo8_mechanics", "v404_parse_deformacao", "_v404_close", "_v404_formal", "_v404_registro", "_V404_RECUSA",
                   "_V404_CONTRACTS", "_V404_TEXTS", "_V404_FONTES", "_V404_VERBATINS2", "_V404_SPECS", "_V404_NOMES_REGISTROS", "_v404_rodar_specs"}
FUNCOES_QUE_NAO_PODEM_MUDAR = ("evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386")


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
# os nos anonimos novos esperados: o `import math as _m404` do bloco da v404 e os dois `update` que entregam as fontes e as falas ao motor de registros (v392)
anon_novos_ok = len(anon_novos_txt) == 3 and sum("_m404" in x for x in anon_novos_txt) == 1 and sum("_V392_FONTES.update(_V404_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V404_VERBATINS2)" in x for x in anon_novos_txt) == 1
sem_explicacao = [k for k in mud if k not in EXPLICACOES]
explicados_sem_mudar = [k for k in EXPLICACOES if k not in mud]
intactas = {f: bool(todos(A, f) and [h(x) for x in todos(A, f)] == [h(x) for x in todos(B, f)]) for f in FUNCOES_QUE_NAO_PODEM_MUDAR}
res = {"nos_nomeados_v403": len(da), "iguais": len(ig), "mudados": {k: EXPLICACOES.get(k, "SEM EXPLICACAO") for k in mud}, "removidos": rem, "novos": nov, "n_novos": len(nov), "novos_esperados": sorted(NOVOS_ESPERADOS),
       "anonimos_perdidos": [ast.unparse(n)[:160] for n in anon_perdidos], "anonimos_novos": anon_novos_txt, "os_tres_anonimos_novos_sao_o_import_de_math_e_os_dois_update": anon_novos_ok,
       "mudados_sem_explicacao": sem_explicacao, "explicacao_sem_mudanca": explicados_sem_mudar, "funcoes_intactas": intactas, "o_gate_nao_se_move_e_a_v386_nao_e_reescrita": all(intactas.values())}
res["ok"] = bool(not sem_explicacao and not rem and set(nov) == NOVOS_ESPERADOS and not anon_perdidos and anon_novos_ok and not explicados_sem_mudar and all(intactas.values()))
json.dump(res, open(os.path.join(HERE, "COMPARACAO_V403_v404.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, (dict, list)) else (len(v) if k not in ("mudados_sem_explicacao", "removidos", "anonimos_perdidos", "novos", "explicacao_sem_mudanca", "funcoes_intactas") else v)) for k, v in res.items()}, ensure_ascii=False)); print("mudados:", sorted(mud))
sys.exit(0 if res["ok"] else 1)
