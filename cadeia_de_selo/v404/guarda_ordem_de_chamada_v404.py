# -*- coding: utf-8 -*-
"""guarda_ordem_de_chamada_v404.py -- A ORDEM DE CHAMADA (licao da 1a tentativa do rito v404, 28/10/2026, gerencia c1).
Toda chave do core que uma funcao de registro NOVA LE (core.get("K") ou core["K"]) e que o main do um.py ATRIBUI (core["K"] = ...)
tem de ser atribuida ANTES da instrucao do main que chama a funcao. O ensaio a seco nao pegava isto porque exercita as funcoes
sobre a copia do core da versao SELADA (que ja' traz as chaves); o rito real pegou: f2b_errata_v404, chamada logo depois do Jo8v32,
leu um core ainda sem ramo_b_preregistration_v386, ledger_errata_v386 e the_ledger_of_charges_v383 (atribuidos ~400 linhas abaixo)
e RECUSOU as 7 checagens (fail-closed correto; a cadeia nao tinha a guarda). Esta guarda e' ESTATICA (AST), nao executa nada.
uso: python -I -B -X utf8 guarda_ordem_de_chamada_v404.py <um.py> [funcao ...]   (rc 0 = toda leitura depois da atribuicao; rc 1 = ha leitura antes)
Como modulo: ordem_de_chamada(src_text, funcoes) -> dict com "ok"."""
import ast, json, sys

FUNCOES_V404 = ("projecao_transversal_v404", "jo8v32_v404", "f2b_errata_v404")
INSUMOS_EXIGIDOS = {"f2b_errata_v404": ("ramo_b_preregistration_v386", "ledger_errata_v386", "the_ledger_of_charges_v383")}


def _chave_core(node):
    """core["K"] -> "K" (so' chave literal), senao None."""
    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id == "core" and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
        return node.slice.value
    return None


def ordem_de_chamada(src, funcoes=FUNCOES_V404):
    tree = ast.parse(src)
    mains = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main"]
    assert mains, "sem def main"
    main = mains[-1]
    atrib = {}   # chave -> indice da PRIMEIRA instrucao do main que a atribui (core["K"] = ...)
    for i, st in enumerate(main.body):
        for n in ast.walk(st):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    k = _chave_core(t)
                    if k is not None:
                        atrib.setdefault(k, i)
    unp = [ast.unparse(st) for st in main.body]
    out = {"funcoes": {}, "ok": True}
    for fn in funcoes:
        fds = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == fn]
        if len(fds) != 1:
            out["funcoes"][fn] = {"erro": "funcao ausente ou duplicada (%d)" % len(fds)}; out["ok"] = False; continue
        lidas = set()
        for n in ast.walk(fds[0]):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get" and isinstance(n.func.value, ast.Name) and n.func.value.id == "core" and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
                lidas.add(n.args[0].value)
            k = _chave_core(n)
            if k is not None and not isinstance(n.ctx, ast.Store):
                lidas.add(k)
        lidas.discard(fn)
        ch = [i for i, s in enumerate(unp) if fn + "(core)" in s]
        if len(ch) != 1:
            out["funcoes"][fn] = {"erro": "chamada no main ausente ou nao unica", "indices": ch}; out["ok"] = False; continue
        ic = ch[0]
        dep = {k: {"indice": atrib[k], "linha": main.body[atrib[k]].lineno, "antes_da_chamada": atrib[k] < ic} for k in sorted(lidas) if k in atrib}
        exig = INSUMOS_EXIGIDOS.get(fn, ())
        faltam = [k for k in exig if k not in dep]
        ok_fn = all(d["antes_da_chamada"] for d in dep.values()) and not faltam
        out["funcoes"][fn] = {"chamada": {"indice": ic, "linha": main.body[ic].lineno}, "insumos_atribuidos_no_main": dep, "insumos_fora_do_main": sorted(k for k in lidas if k not in atrib),
                              "insumos_exigidos_ausentes": faltam, "lidos_antes_da_atribuicao": sorted(k for k, d in dep.items() if not d["antes_da_chamada"]), "ok": ok_fn}
        out["ok"] = out["ok"] and ok_fn
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    p = sys.argv[1]; fns = tuple(sys.argv[2:]) or FUNCOES_V404
    r = ordem_de_chamada(open(p, encoding="utf-8").read(), fns)
    print(json.dumps({"arquivo": p, "ok": r["ok"], "funcoes": {k: {"ok": v.get("ok"), "chamada": v.get("chamada"), "lidos_antes_da_atribuicao": v.get("lidos_antes_da_atribuicao"), "insumos_exigidos_ausentes": v.get("insumos_exigidos_ausentes"), "erro": v.get("erro")} for k, v in r["funcoes"].items()}}, ensure_ascii=False, indent=1))
    sys.exit(0 if r["ok"] else 1)
