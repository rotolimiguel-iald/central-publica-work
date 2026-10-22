# -*- coding: utf-8 -*-
"""comparar_v394_v395.py -- NADA DA v394 PERDIDO: compara, no=a=no (AST), a v394 SELADA (base_v394\\um.py) com o candidato v395: todo no nomeado da v394 existe no candidato, ou foi mudado por um PATCH declarado
(EXPLICACOES abaixo, uma por no). Todo no mudado SEM explicacao aqui, e todo no removido, reprovam (rc 1). Escreve COMPARACAO_V394_v395.json. uso: python -I -B -X utf8 comparar_v394_v395.py"""
import ast, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v395 as DL  # noqa: E402
A = ast.parse(open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8")); B = ast.parse(open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8"))
h = lambda n: hashlib.sha256(ast.dump(n).encode()).hexdigest()[:12]
EXPLICACOES = {
    "UM_VERSION": "W01: a constante unica de versao v394 -> v395",
    "_EMBEDDED_KERNEL_FILES": "K00/K01: +1 modulo (TGLExt/Psibit.lean) e a raiz TGLExt.lean e o TGL/Audit.lean com o import da pedra",
    "_LEAN_THEOREM_FLAGS": "V01: +bandeiras so' de declaracao nomeada da pedra Psibit (FLAGS_v395.json)",
    "prove_external_ladder": "V02: a lista ext_flags ganha as mesmas bandeiras (a escada sobe)",
    "_ESQUELETO_STONES": "V03: o ledger de pedras ganha a Psibit",
    "_V394_FORMAL_CONTRACT": "C12: so' o numero expected_ladder (a escada desta versao); o consumidor exige a igualdade exata com a escada do rito",
    "_V394_QUADRATIC_CONTRACT": "C12: so' o numero expected_ladder",
    "_V394_NETWORK_CONTRACT": "C12: so' o numero expected_ladder",
    "_V394_SPECS": "C13: kh_n1_cobertura_v394 passa a piso em h2, h3, h6 e a tamanho minimo em h8 (+ errata assinada); os outros dois specs nao mudam",
    "main": "N00/N01/N02: a chamada de psibit_v395 na fractalizacao do Um, a chamada dos registros por spec da v395 e o selo (psibit_v395, registros_v395)",
    "build_pt": "W04: a secao v395 do artigo PT, antes da v394",
    "build_en": "W05: a secao v395 do artigo EN, antes da v394",
    "emit_canonical_md": "W07: a linha da v395 no .md canonico",
}
def nm(n):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
        return n.name
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        return n.targets[0].id
    return None


def todos(tree, nome):
    return [n for n in tree.body if nm(n) == nome]


da = {nm(n): n for n in A.body if nm(n)}; db = {nm(n): n for n in B.body if nm(n)}
# nomes definidos mais de uma vez (ex.: main): compara a LISTA de definicoes
mud = []
for k in da:
    if k not in db:
        continue
    la, lb = todos(A, k), todos(B, k)
    if [h(x) for x in la] != [h(x) for x in lb]:
        mud.append(k)
ig = [k for k in da if k in db and k not in mud]
rem = [k for k in da if k not in db]; nov = [k for k in db if k not in da]
anon_a = sorted(h(n) for n in A.body if not nm(n)); anon_b = sorted(h(n) for n in B.body if not nm(n))
sa = {}
for x in anon_a:
    sa[x] = sa.get(x, 0) + 1
sb = {}
for x in anon_b:
    sb[x] = sb.get(x, 0) + 1
anon_perdidos = [k for k, v in sa.items() if sb.get(k, 0) < v]
sem_explicacao = [k for k in mud if k not in EXPLICACOES]
explicados_sem_mudar = [k for k in EXPLICACOES if k not in mud]
res = {"nos_nomeados_v394": len(da), "iguais": len(ig), "mudados": {k: EXPLICACOES.get(k, "SEM EXPLICACAO") for k in mud}, "removidos": rem, "novos": sorted(nov), "n_novos": len(nov), "anonimos_da_v394_ausentes": len(anon_perdidos),
       "mudados_sem_explicacao": sem_explicacao, "explicacao_sem_mudanca": explicados_sem_mudar}
res["ok"] = not sem_explicacao and not rem and not anon_perdidos
json.dump(res, open(os.path.join(HERE, "COMPARACAO_V394_v395.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if not isinstance(v, (dict, list)) else (len(v) if k != "mudados_sem_explicacao" else v)) for k, v in res.items()}, ensure_ascii=False)); print("mudados:", sorted(mud)); print("novos:", sorted(nov))
sys.exit(0 if res["ok"] else 1)
