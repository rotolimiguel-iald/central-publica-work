# -*- coding: utf-8 -*-
"""comparar_v399_v400.py -- NADA DA v399 PERDIDO: compara, no=a=no (AST), a v399 SELADA (base_v399\\um.py) com o candidato v400: todo no nomeado da v399 existe no candidato IGUAL, ou foi mudado por um PATCH declarado
(EXPLICACOES abaixo, uma por no), ou foi REMOVIDO de proposito (REMOVIDOS_DECLARADOS: so' o nome ALPHA_FINE_CODATA_2018 da secao do selo ACOM, a redeclaracao que a Bancada recusou). Todo no mudado SEM explicacao, todo removido
sem declaracao e todo no anonimo perdido que nao seja o `if "SEALED_CODATA_ALPHA" in globals():` da redeclaracao reprovam (rc 1). Nenhum no novo e' esperado (a v400 nao acrescenta nome algum). Escreve COMPARACAO_V399_v400.json.
uso: python -I -B -X utf8 comparar_v399_v400.py"""
import ast, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
A = ast.parse(open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")); B = ast.parse(open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8"))
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao v399 -> v400",
    "_beta_runtime": "W02/A2: le o alfa do programa (SEALED_CODATA_ALPHA) em vez da redeclaracao",
    "registro_core_v399": "W02/A3: recebe beta_core e a checagem do beta confronta com core[\"beta\"] a 1e-9 (deixa de ser tautologica); valores beta_core e rel_beta_vs_core",
    "selo_acom_v399": "W02/A4: o ponto de chamada passa core.get(\"beta\") ao registro",
    "build_pt": "W04: a errata ao lado da secao v399 do artigo PT (o quadro «O Teste da Unica Palavra» do topo NAO muda)",
    "build_en": "W05: o erratum beside the v399 section of the EN article (the box at the top does NOT change)",
    "emit_canonical_md": "W09: a linha da errata (v400) no .md canonico (o quadro do topo NAO muda)",
}
REMOVIDOS_DECLARADOS = {"ALPHA_FINE_CODATA_2018": "W02/A1: a redeclaracao de alfa da secao do selo ACOM (coluna 0) sai; o programa le SEALED_CODATA_ALPHA. No um.py v399 esse nome so' existia por ela (a linha 5584 e' texto de um script embutido)"}


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
rem = [k for k in da if k not in db]; nov = [k for k in db if k not in da]
anon_a = [n for n in A.body if not nm(n)]; anon_b = [n for n in B.body if not nm(n)]
sa, sb = {}, {}
for n in anon_a:
    sa.setdefault(h(n), []).append(n)
for n in anon_b:
    sb.setdefault(h(n), []).append(n)
anon_perdidos = [n for k, v in sa.items() for n in v[len(sb.get(k, [])):] if len(sb.get(k, [])) < len(v)]
anon_novos = [n for k, v in sb.items() for n in v[len(sa.get(k, [])):] if len(sa.get(k, [])) < len(v)]
perdidos_txt = [ast.unparse(n)[:160] for n in anon_perdidos]
so_o_if_do_alfa = len(anon_perdidos) == 1 and isinstance(anon_perdidos[0], ast.If) and "SEALED_CODATA_ALPHA" in perdidos_txt[0] and "ALPHA_FINE_CODATA_2018" in ast.unparse(anon_perdidos[0])
sem_explicacao = [k for k in mud if k not in EXPLICACOES]
removidos_sem_declaracao = [k for k in rem if k not in REMOVIDOS_DECLARADOS]
explicados_sem_mudar = [k for k in EXPLICACOES if k not in mud]
res = {"nos_nomeados_v399": len(da), "iguais": len(ig), "mudados": {k: EXPLICACOES.get(k, "SEM EXPLICACAO") for k in mud}, "removidos": {k: REMOVIDOS_DECLARADOS.get(k, "SEM DECLARACAO") for k in rem}, "novos": sorted(nov), "n_novos": len(nov),
       "anonimos_perdidos": perdidos_txt, "anonimos_novos": [ast.unparse(n)[:160] for n in anon_novos], "o_unico_anonimo_perdido_e_o_if_da_redeclaracao": so_o_if_do_alfa,
       "mudados_sem_explicacao": sem_explicacao, "removidos_sem_declaracao": removidos_sem_declaracao, "explicacao_sem_mudanca": explicados_sem_mudar}
res["ok"] = not sem_explicacao and not removidos_sem_declaracao and not nov and not anon_novos and so_o_if_do_alfa and not explicados_sem_mudar and set(rem) == set(REMOVIDOS_DECLARADOS)
json.dump(res, open(os.path.join(HERE, "COMPARACAO_V399_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, (dict, list)) else (len(v) if k not in ("mudados_sem_explicacao", "removidos_sem_declaracao", "anonimos_perdidos", "novos") else v)) for k, v in res.items()}, ensure_ascii=False)); print("mudados:", sorted(mud))
sys.exit(0 if res["ok"] else 1)
