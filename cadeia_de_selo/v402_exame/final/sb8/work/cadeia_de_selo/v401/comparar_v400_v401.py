# -*- coding: utf-8 -*-
"""comparar_v400_v401.py -- NADA DA v400 PERDIDO: compara, no=a=no (AST), a v400 SELADA (base_v400\\um.py) com o candidato v401: todo no nomeado da v400 existe no candidato IGUAL, ou foi mudado por um PATCH declarado (EXPLICACOES abaixo, uma por no), ou foi REMOVIDO de proposito
(nenhum: a v401 nao remove nome algum). Todo no mudado SEM explicacao, todo no removido, todo no anonimo perdido ou novo reprovam (rc 1). Os nos NOVOS esperados sao so' os da v401 (o registro com funcao, o contrato, o texto, as fontes, as inscricoes, os specs e o rodar_specs). Escreve COMPARACAO_V400_v401.json.
uso: python -I -B -X utf8 comparar_v400_v401.py"""
import ast, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v401 as DL  # noqa: E402
A = ast.parse(open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")); B = ast.parse(open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8"))
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao v400 -> v401",
    "_EMBEDDED_KERNEL_FILES": "K00/K01: a raiz TGLExt.lean e o TGL/Audit.lean regenerados (+ o import da pedra) e +1 modulo Lean (TGLExt/FalsidadeDaInercia.lean)",
    "_LEAN_THEOREM_FLAGS": "V01: +12 bandeiras da pedra FalsidadeDaInercia (so' declaracao nomeada)",
    "prove_external_ladder": "V02: a lista ext_flags ganha as 12 bandeiras (a escada 9541 -> 9553)",
    "_ESQUELETO_STONES": "V03: o ledger de pedras ganha a v401",
    "_V399_SPECS": "C13: kh_n1_cobertura_v399 h2/h3/h6 viram pisos e h8 o tamanho minimo (+ errata ao lado); o veredito do registro nao muda",
    "_V394_FORMAL_CONTRACT": "C12: expected_ladder 9541 -> 9553", "_V394_QUADRATIC_CONTRACT": "C12: expected_ladder 9541 -> 9553", "_V394_NETWORK_CONTRACT": "C12: expected_ladder 9541 -> 9553", "_V395_PSIBIT_CONTRACT": "C12: expected_ladder 9541 -> 9553",
    "_V396_TESTEMUNHA_CONTRACT": "C12: expected_ladder 9541 -> 9553", "_V398_SONICO_CONTRACT": "C12: expected_ladder 9541 -> 9553", "_V398_AFINACAO_CONTRACT": "C12: expected_ladder 9541 -> 9553",
    "main": "N00/N01/N02: as chamadas do registro da falsidade e dos specs v401 e as duas chaves novas do selo (try/AVISO; nada do que existia muda)",
    "build_pt": "W04: a secao «A falsidade (simulacro) da inercia» do artigo PT, antes da secao v399 (o quadro «O Teste da Unica Palavra» do topo NAO muda)",
    "build_en": "W05: the section «The falsity (simulacrum) of inertia» of the EN article, before the v399 section (the box at the top does NOT change)",
    "emit_canonical_md": "W09: a linha «A falsidade (simulacro) da inercia (v401)» no .md canonico, antes da linha da v399 (o quadro do topo NAO muda)",
}
NOVOS_ESPERADOS = {"v401_falsidade_mechanics", "_v401_formal", "_V401_RECUSA", "falsidade_da_inercia_v401", "_V401_FALSIDADE_CONTRACT", "_V401_FALSIDADE_TEXT", "_V401_FONTES", "_V401_VERBATINS2", "_V401_SPECS", "_V401_NOMES_REGISTROS", "_v401_rodar_specs"}


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
# os nos anonimos novos esperados: o `import math as _m401` do bloco da v401 e os dois `update` que entregam as fontes e as inscricoes ao motor de registros (v392)
anon_novos_ok = len(anon_novos_txt) == 3 and sum("_m401" in x for x in anon_novos_txt) == 1 and sum("_V392_FONTES.update(_V401_FONTES)" in x for x in anon_novos_txt) == 1 and sum("_V392_VERBATINS2.update(_V401_VERBATINS2)" in x for x in anon_novos_txt) == 1
sem_explicacao = [k for k in mud if k not in EXPLICACOES]
explicados_sem_mudar = [k for k in EXPLICACOES if k not in mud]
res = {"nos_nomeados_v400": len(da), "iguais": len(ig), "mudados": {k: EXPLICACOES.get(k, "SEM EXPLICACAO") for k in mud}, "removidos": rem, "novos": nov, "n_novos": len(nov), "novos_esperados": sorted(NOVOS_ESPERADOS),
       "anonimos_perdidos": [ast.unparse(n)[:160] for n in anon_perdidos], "anonimos_novos": anon_novos_txt, "os_tres_anonimos_novos_sao_o_import_de_math_e_os_dois_update": anon_novos_ok,
       "mudados_sem_explicacao": sem_explicacao, "explicacao_sem_mudanca": explicados_sem_mudar}
res["ok"] = bool(not sem_explicacao and not rem and set(nov) == NOVOS_ESPERADOS and not anon_perdidos and anon_novos_ok and not explicados_sem_mudar)
json.dump(res, open(os.path.join(HERE, "COMPARACAO_V400_v401.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, (dict, list)) else (len(v) if k not in ("mudados_sem_explicacao", "removidos", "anonimos_perdidos", "novos", "explicacao_sem_mudanca") else v)) for k, v in res.items()}, ensure_ascii=False)); print("mudados:", sorted(mud))
sys.exit(0 if res["ok"] else 1)
