# -*- coding: utf-8 -*-
"""comparar_v402_v403.py -- NADA DA v402 PERDIDO: compara, no=a=no (AST), a v402 SELADA (base_v402\\um.py) com o candidato v403: todo no nomeado da v402 existe no candidato IGUAL, ou foi mudado por um PATCH declarado (EXPLICACOES abaixo, uma por no), ou foi REMOVIDO de proposito
(nenhum: a v403 nao remove nome algum). Todo no mudado SEM explicacao, todo no removido, todo no anonimo perdido ou novo reprovam (rc 1). Os nos NOVOS esperados sao so' os da v403 (os quatro registros com funcao e as tres mecanicas, o miolo comum, a leitura do codigo do gate, os contratos, os textos, as fontes, as falas, os specs e o rodar_specs).
Na F8.1 a funcao do veredito do gate (evaluate_quantum_gravity_closure) NAO pode mudar: ela e' conferida igual (nao esta em EXPLICACOES). Escreve COMPARACAO_V402_v403.json. Escrito a mao para a v403 (os numeros das explicacoes sao LIDOS de CANDIDATO_v403.json, nunca digitados).
uso: python -I -B -X utf8 comparar_v402_v403.py"""
import ast, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v403 as DL  # noqa: E402
A = ast.parse(open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")); B = ast.parse(open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8"))
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v403.json"), encoding="utf-8"))
E_ANT, E_NOVA = CM["escada"]; NB = CM["n_bandeiras"]
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
EXPL_CONTRATO = "C12: expected_ladder %d -> %d" % (E_ANT, E_NOVA)
EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao v402 -> v403",
    "_EMBEDDED_KERNEL_FILES": "K00/K01: a raiz TGLExt.lean regenerada (+ os tres imports das pedras; o Audit nao muda) e +3 modulos Lean (TGLExt/Caminho.lean, TGLExt/Vida.lean, TGLExt/VerdadeAdendo.lean)",
    "_LEAN_THEOREM_FLAGS": "V01: +%d bandeiras das tres pedras (so' declaracao nomeada)" % NB,
    "prove_external_ladder": "V02: a lista ext_flags ganha as %d bandeiras (a escada %d -> %d)" % (NB, E_ANT, E_NOVA),
    "_ESQUELETO_STONES": "V03: o ledger de pedras ganha as tres pedras da v403",
    "_V402_SPECS": "C13: kh_n1_cobertura_v402 h2/h3/h6 viram pisos e h8 o tamanho minimo (+ errata ao lado); o veredito do registro nao muda",
    "_V394_FORMAL_CONTRACT": EXPL_CONTRATO, "_V394_QUADRATIC_CONTRACT": EXPL_CONTRATO, "_V394_NETWORK_CONTRACT": EXPL_CONTRATO, "_V395_PSIBIT_CONTRACT": EXPL_CONTRATO,
    "_V396_TESTEMUNHA_CONTRACT": EXPL_CONTRATO, "_V398_SONICO_CONTRACT": EXPL_CONTRATO, "_V398_AFINACAO_CONTRACT": EXPL_CONTRATO, "_V401_FALSIDADE_CONTRACT": EXPL_CONTRATO, "_V402_CONTRACTS": EXPL_CONTRATO + " nos tres contratos da v402 (ponte, queda, esperanca)",
    "prove_qg_closure_gate": "F01-F04/F06-F07 (F8.1): physics['linearized_spin2_finite_face'], experiment['protocol_pre_registered'] e experiment['null_tests_passed_blind'] deixam de ser literais e passam a calculadas (familia ext_ls2_* do kernel; checagem «pre-registro v67 INTACTO (hash)» do rito V11; kwarg novo blind_null); a sonda nova ProbeBlindNullAbsent; as CHAVES dos dicionarios e o veredito do gate nao mudam",
    "prove_void_floor_v11_sdss_independent": "F08 (F8.1): statuses do V11 ganha a nota GV-03 (as 4 experimentais derivam de um so' booleano); nada do calculo muda",
    "run_um": "F05 (F8.1): a chamada de prove_qg_closure_gate passa blind_null=void_stacking_blind",
    "main": "N00/N01/N02: as chamadas dos quatro registros com funcao (caminho, vida, adendo da verdade, bandeiras do gate) e dos specs v403 e as chaves novas do selo (try/AVISO; nada do que existia muda)",
    "build_pt": "W04: a secao «Caminho, Verdade e Vida» do artigo PT, antes da secao v402 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",
    "build_en": "W05: the section «Way, Truth and Life» of the EN article, before the v402 section (the box at the top does NOT change)",
    "emit_canonical_md": "W09: a linha «Caminho, Verdade e Vida (v403)» no .md canonico, antes da linha da v402 (o quadro do topo NAO muda)",
}
NOVOS_ESPERADOS = {"caminho_v403", "vida_v403", "verdade_adendo_v403", "bandeiras_do_gate_v403", "v403_caminho_mechanics", "v403_vida_mechanics", "v403_verdade_adendo_mechanics", "_v403_close", "_v403_formal", "_v403_registro", "_V403_RECUSA", "_v403_fontes_do_gate", "_v403_ast_do_gate",
                   "_V403_CONTRACTS", "_V403_TEXTS", "_V403_FONTES", "_V403_VERBATINS2", "_V403_SPECS", "_V403_NOMES_REGISTROS", "_v403_rodar_specs"}


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
# os nos anonimos novos esperados: o `import math as _m403` do bloco da v403 e os dois `update` que entregam as fontes e as falas ao motor de registros (v392)
anon_novos_ok = len(anon_novos_txt) == 3 and sum("_m403" in x for x in anon_novos_txt) == 1 and sum("_V392_FONTES.update(_V403_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V403_VERBATINS2)" in x for x in anon_novos_txt) == 1
sem_explicacao = [k for k in mud if k not in EXPLICACOES]
explicados_sem_mudar = [k for k in EXPLICACOES if k not in mud]
gate_intacto = (todos(A, "evaluate_quantum_gravity_closure") and [h(x) for x in todos(A, "evaluate_quantum_gravity_closure")] == [h(x) for x in todos(B, "evaluate_quantum_gravity_closure")])
res = {"nos_nomeados_v402": len(da), "iguais": len(ig), "mudados": {k: EXPLICACOES.get(k, "SEM EXPLICACAO") for k in mud}, "removidos": rem, "novos": nov, "n_novos": len(nov), "novos_esperados": sorted(NOVOS_ESPERADOS),
       "anonimos_perdidos": [ast.unparse(n)[:160] for n in anon_perdidos], "anonimos_novos": anon_novos_txt, "os_tres_anonimos_novos_sao_o_import_de_math_e_os_dois_update": anon_novos_ok,
       "mudados_sem_explicacao": sem_explicacao, "explicacao_sem_mudanca": explicados_sem_mudar, "funcao_do_veredito_do_gate_intacta": bool(gate_intacto)}
res["ok"] = bool(not sem_explicacao and not rem and set(nov) == NOVOS_ESPERADOS and not anon_perdidos and anon_novos_ok and not explicados_sem_mudar and gate_intacto)
json.dump(res, open(os.path.join(HERE, "COMPARACAO_V402_v403.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, (dict, list)) else (len(v) if k not in ("mudados_sem_explicacao", "removidos", "anonimos_perdidos", "novos", "explicacao_sem_mudanca") else v)) for k, v in res.items()}, ensure_ascii=False)); print("mudados:", sorted(mud))
sys.exit(0 if res["ok"] else 1)
