# -*- coding: utf-8 -*-
"""comparar_v401_v402.py -- NADA DA v401 PERDIDO: compara, no=a=no (AST), a v401 SELADA (base_v401\\um.py) com o candidato v402: todo no nomeado da v401 existe no candidato IGUAL, ou foi mudado por um PATCH declarado (EXPLICACOES abaixo, uma por no), ou foi REMOVIDO de proposito
(nenhum: a v402 nao remove nome algum). Todo no mudado SEM explicacao, todo no removido, todo no anonimo perdido ou novo reprovam (rc 1). Os nos NOVOS esperados sao so' os da v402 (os tres registros com funcao e as tres mecanicas, o miolo comum, os contratos, os textos, as fontes, as inscricoes, os specs e o rodar_specs).
Escreve COMPARACAO_V401_v402.json. Escrito a mao para a v402 (os numeros das explicacoes sao LIDOS de CANDIDATO_v402.json, nunca digitados).
uso: python -I -B -X utf8 comparar_v401_v402.py"""
import ast, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v402 as DL  # noqa: E402
A = ast.parse(open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")); B = ast.parse(open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8"))
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v402.json"), encoding="utf-8"))
E_ANT, E_NOVA = CM["escada"]; NB = CM["n_bandeiras"]
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
EXPL_CONTRATO = "C12: expected_ladder %d -> %d" % (E_ANT, E_NOVA)
EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao v401 -> v402",
    "_EMBEDDED_KERNEL_FILES": "K00/K01: a raiz TGLExt.lean e o TGL/Audit.lean regenerados (+ os tres imports das pedras) e +3 modulos Lean (TGLExt/PonteDaEscalaDual.lean, TGLExt/QuedaSemGeometria.lean, TGLExt/EsperancaCondicional.lean)",
    "_LEAN_THEOREM_FLAGS": "V01: +%d bandeiras das tres pedras (so' declaracao nomeada)" % NB,
    "prove_external_ladder": "V02: a lista ext_flags ganha as %d bandeiras (a escada %d -> %d)" % (NB, E_ANT, E_NOVA),
    "_ESQUELETO_STONES": "V03: o ledger de pedras ganha as tres pedras da v402",
    "_V401_SPECS": "C13: kh_n1_cobertura_v401 h2/h3/h6 viram pisos e h8 o tamanho minimo (+ errata ao lado); o veredito do registro nao muda",
    "_V394_FORMAL_CONTRACT": EXPL_CONTRATO, "_V394_QUADRATIC_CONTRACT": EXPL_CONTRATO, "_V394_NETWORK_CONTRACT": EXPL_CONTRATO, "_V395_PSIBIT_CONTRACT": EXPL_CONTRATO,
    "_V396_TESTEMUNHA_CONTRACT": EXPL_CONTRATO, "_V398_SONICO_CONTRACT": EXPL_CONTRATO, "_V398_AFINACAO_CONTRACT": EXPL_CONTRATO, "_V401_FALSIDADE_CONTRACT": EXPL_CONTRATO,
    "main": "N00/N01/N02: as chamadas dos tres registros com funcao (ponte, queda, esperanca) e dos specs v402 e as chaves novas do selo (try/AVISO; nada do que existia muda)",
    "build_pt": "W04: a secao «A ponte da escala dual, a queda sem geometria e a esperanca condicional» do artigo PT, antes da secao v401 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",
    "build_en": "W05: the section «The dual-scale bridge, the fall without geometry and the conditional expectation» of the EN article, before the v401 section (the box at the top does NOT change)",
    "emit_canonical_md": "W09: a linha «A ponte da escala dual, a queda sem geometria e a esperanca condicional (v402)» no .md canonico, antes da linha da v401 (o quadro do topo NAO muda)",
}
NOVOS_ESPERADOS = {"ponte_da_escala_dual_v402", "queda_sem_geometria_v402", "esperanca_condicional_v402", "v402_ponte_mechanics", "v402_queda_mechanics", "v402_esperanca_mechanics", "_v402_close", "_v402_formal", "_v402_registro", "_V402_RECUSA",
                   "_V402_CONTRACTS", "_V402_TEXTS", "_V402_FONTES", "_V402_VERBATINS2", "_V402_SPECS", "_V402_NOMES_REGISTROS", "_v402_rodar_specs"}


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
# os nos anonimos novos esperados: o `import math as _m402` do bloco da v402 e os dois `update` que entregam as fontes e as inscricoes ao motor de registros (v392)
anon_novos_ok = len(anon_novos_txt) == 3 and sum("_m402" in x for x in anon_novos_txt) == 1 and sum("_V392_FONTES.update(_V402_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V402_VERBATINS2)" in x for x in anon_novos_txt) == 1
sem_explicacao = [k for k in mud if k not in EXPLICACOES]
explicados_sem_mudar = [k for k in EXPLICACOES if k not in mud]
res = {"nos_nomeados_v401": len(da), "iguais": len(ig), "mudados": {k: EXPLICACOES.get(k, "SEM EXPLICACAO") for k in mud}, "removidos": rem, "novos": nov, "n_novos": len(nov), "novos_esperados": sorted(NOVOS_ESPERADOS),
       "anonimos_perdidos": [ast.unparse(n)[:160] for n in anon_perdidos], "anonimos_novos": anon_novos_txt, "os_tres_anonimos_novos_sao_o_import_de_math_e_os_dois_update": anon_novos_ok,
       "mudados_sem_explicacao": sem_explicacao, "explicacao_sem_mudanca": explicados_sem_mudar}
res["ok"] = bool(not sem_explicacao and not rem and set(nov) == NOVOS_ESPERADOS and not anon_perdidos and anon_novos_ok and not explicados_sem_mudar)
json.dump(res, open(os.path.join(HERE, "COMPARACAO_V401_v402.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, (dict, list)) else (len(v) if k not in ("mudados_sem_explicacao", "removidos", "anonimos_perdidos", "novos", "explicacao_sem_mudanca") else v)) for k, v in res.items()}, ensure_ascii=False)); print("mudados:", sorted(mud))
sys.exit(0 if res["ok"] else 1)
