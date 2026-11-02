# -*- coding: utf-8 -*-
"""guarda_ordem_de_chamada_v405.py -- A ORDEM DE CHAMADA (licao 1 da v404: a 1a tentativa do rito de 28/10/2026). AUTORAL na v405: a da v404 olhava so' o corpo da funcao chamada no main; os registros de pedra da v405 sao de uma linha (chamam _v405_registro, que chama _v405_formal e a mecanica), e la' a leitura nao aparece: copiar a guarda daria vacuo (nenhuma leitura vista, tudo «ok»).
Toda chave do core que uma funcao de registro NOVA LE, em qualquer funcao que ela alcanca (core.get("K"), core_.get("K"), core["K"], core_["K"]), tem de estar pronta ANTES da instrucao do main que a chama. Pronta quer dizer: (a) vem de run_um (a primeira instrucao do main e' `core = run_um(...)`; as chaves literais dos dicts de run_um);
ou (b) core["K"] = ... numa instrucao ANTERIOR do main; ou (c) a chamada `K(core)` numa instrucao ANTERIOR do main (a convencao dos registros: a funcao grava core["K"]). O que nao se acha em nenhum dos tres e' FALHA VISIVEL (`lidas_sem_origem`), nunca «ok» por omissao.
Esta guarda e' ESTATICA (AST), nao executa nada. Controle negativo em controle_negativo(): a mesma fonte com o registro da Ponte da Massa chamado ANTES da projecao_transversal_v404 tem de reprovar, e uma leitura de chave inexistente tambem.
uso: python -I -B -X utf8 guarda_ordem_de_chamada_v405.py <um.py> [funcao ...]   (rc 0 = toda leitura depois da origem; rc 1 = ha leitura antes ou sem origem)
Como modulo: ordem_de_chamada(src_text, funcoes) -> dict com "ok"; controle_negativo(src_text) -> dict com "ok"."""
import ast, json, re, sys

FUNCOES_PEDRAS = ("ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405")
FUNCOES_V405 = FUNCOES_PEDRAS + ("_v405_rodar_specs",)   # (o ultimo: as medidas do Grande Atrator rodam dentro dos specs da v405)
MECANICA_DE = dict(zip(FUNCOES_V405, ("v405_ponte_mechanics", "v405_tensao_mechanics", "v405_identidade_mechanics", "v405_observador_mechanics", "v405_diminuto_mechanics", "v405_tonica_mechanics", "v405_disco_mechanics", "v405_psion_mechanics", "v405_ga_mechanics")))
COMUNS = ("_v405_registro", "_v405_formal", "_v398_beta")     # o miolo comum: tudo o que o registro le passa por aqui
INSUMOS_EXIGIDOS = {"ponte_da_massa_v405": ("neutrino_mass", "projecao_transversal_v404"), "massa_tensao_pura_v405": ("neutrino_mass",), "lei_do_diminuto_v405": ("neutrino_mass",), "tonica_do_hamiltoniano_v405": ("neutrino_mass",), "ponto_zero_do_psion_v405": ("neutrino_mass", "projecao_transversal_v404"), "observador_terminal_v405": ("omega_I",), "_v405_rodar_specs": ("joint_coincidence_result_v3", "ga_mass_audit", "mode_A", "mode_B")}
NOMES_DO_CORE = ("core", "core_")


def _chave_core(node):
    """core["K"] / core_["K"] -> "K" (so' chave literal), senao None."""
    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name) and node.value.id in NOMES_DO_CORE and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
        return node.slice.value
    return None


def lidas_em(fd):
    """as chaves literais do core que o corpo da funcao fd le."""
    lidas = set()
    for n in ast.walk(fd):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "get" and isinstance(n.func.value, ast.Name) and n.func.value.id in NOMES_DO_CORE and n.args and isinstance(n.args[0], ast.Constant) and isinstance(n.args[0].value, str):
            lidas.add(n.args[0].value)
        k = _chave_core(n)
        if k is not None and not isinstance(n.ctx, ast.Store):
            lidas.add(k)
    return lidas


def _chaves_de_run_um(fd):
    """as chaves literais dos dicts escritos em run_um (o core nasce ali). E' um superconjunto: dicts aninhados entram; a guarda nao usa isto para provar que uma chave FALTA, so' para achar a origem."""
    ks = set()
    for n in ast.walk(fd):
        if isinstance(n, ast.Dict):
            ks |= {k.value for k in n.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)}
    return ks


def ordem_de_chamada(src, funcoes=FUNCOES_V405):
    tree = ast.parse(src)
    defs = {}
    for n in tree.body:
        if isinstance(n, ast.FunctionDef):
            defs.setdefault(n.name, []).append(n)
    assert defs.get("main"), "sem def main"
    assert len(defs.get("run_um") or []) == 1, "run_um ausente ou duplicada"
    main = defs["main"][-1]
    de_run = _chaves_de_run_um(defs["run_um"][0])
    atrib = {}   # chave -> indice da PRIMEIRA instrucao do main que a produz: core["K"] = ... ou K(core)
    unp = [ast.unparse(st) for st in main.body]
    for i, st in enumerate(main.body):
        for n in ast.walk(st):
            if isinstance(n, ast.Assign):
                for t in n.targets:
                    k = _chave_core(t)
                    if k is not None:
                        atrib.setdefault(k, i)
        for nome in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\(core\)", unp[i]):
            atrib.setdefault(nome, i)
    out = {"funcoes": {}, "ok": True, "comuns_lidos_de": list(COMUNS)}
    for fn in funcoes:
        faltando = [x for x in (fn, MECANICA_DE.get(fn)) + COMUNS if x and len(defs.get(x) or []) != 1]
        if faltando:
            out["funcoes"][fn] = {"erro": "funcao ausente ou duplicada: %r" % (faltando,)}; out["ok"] = False; continue
        lidas = set()
        for x in (fn, MECANICA_DE[fn]) + COMUNS:
            lidas |= lidas_em(defs[x][0])
        lidas.discard(fn)
        ch = [i for i, s in enumerate(unp) if fn + "(core)" in s]
        if len(ch) != 1:
            out["funcoes"][fn] = {"erro": "chamada no main ausente ou nao unica", "indices": ch}; out["ok"] = False; continue
        ic = ch[0]
        no_main = {k: {"indice": atrib[k], "linha": main.body[atrib[k]].lineno, "antes_da_chamada": atrib[k] < ic} for k in sorted(lidas) if k in atrib}
        fora = sorted(k for k in lidas if k not in atrib and k in de_run)
        sem_origem = sorted(k for k in lidas if k not in atrib and k not in de_run)
        # o que vem de run_um e TAMBEM e' reatribuido no main conta pela origem de run_um (ja' esta la' quando a chamada acontece)
        antes = sorted(k for k, d in no_main.items() if not d["antes_da_chamada"] and k not in de_run)
        exig = INSUMOS_EXIGIDOS.get(fn, ())
        faltam = [k for k in exig if not ((k in no_main and no_main[k]["antes_da_chamada"]) or k in de_run)]
        ok_fn = bool(lidas) and not antes and not sem_origem and not faltam
        out["funcoes"][fn] = {"chamada": {"indice": ic, "linha": main.body[ic].lineno}, "n_chaves_lidas": len(lidas), "insumos_produzidos_no_main": no_main, "insumos_de_run_um": fora, "lidas_sem_origem": sem_origem, "insumos_exigidos_ausentes": faltam, "lidos_antes_da_atribuicao": antes, "ok": ok_fn}
        out["ok"] = out["ok"] and ok_fn
    return out


def controle_negativo(src):
    """(1) a Ponte da Massa chamada ANTES da projecao_transversal_v404 reprova; (2) uma leitura de chave sem origem reprova; (3) a fonte intacta passa. Rodado sobre o texto: nada executa."""
    r0 = ordem_de_chamada(src)
    ch_proj = "projecao_transversal_v404(core)"; ch_ponte = "ponte_da_massa_v405(core)"
    linhas = src.split("\n")
    ip = [i for i, l in enumerate(linhas) if re.fullmatch(r"\s+_\w+ = projecao_transversal_v404\(core\)\s*", l)]; ip2 = [i for i, l in enumerate(linhas) if re.fullmatch(r"\s+_\w+ = ponte_da_massa_v405\(core\)\s*", l)]
    assert len(ip) == 1 and len(ip2) == 1, ("as linhas das chamadas nao foram achadas uma vez", ip, ip2)
    # troca so' os nomes das funcoes nas duas instrucoes (a ponte passa a vir antes da projecao)
    a_ = linhas[ip[0]].replace(ch_proj, ch_ponte); b_ = linhas[ip2[0]].replace(ch_ponte, ch_proj)
    m_ = list(linhas); m_[ip[0]] = a_; m_[ip2[0]] = b_
    r1 = ordem_de_chamada("\n".join(m_))
    src2 = src.replace('    m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")', '    m_core_ = (core_.get("chave_que_nao_existe_v405") or {}).get("m_nu_meV")', 1)
    assert src2 != src
    r2 = ordem_de_chamada(src2)
    return {"intacta_passa": bool(r0["ok"]), "ponte_antes_da_projecao_reprova": bool(not r1["ok"] and "projecao_transversal_v404" in ((r1["funcoes"].get("ponte_da_massa_v405") or {}).get("lidos_antes_da_atribuicao") or []) + ((r1["funcoes"].get("ponte_da_massa_v405") or {}).get("insumos_exigidos_ausentes") or [])),
            "chave_sem_origem_reprova": bool(not r2["ok"]), "ok": bool(r0["ok"] and not r1["ok"] and not r2["ok"])}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    p = sys.argv[1]; fns = tuple(sys.argv[2:]) or FUNCOES_V405
    src_ = open(p, encoding="utf-8").read()
    r = ordem_de_chamada(src_, fns)
    print(json.dumps({"arquivo": p, "ok": r["ok"], "funcoes": {k: {"ok": v.get("ok"), "chamada": v.get("chamada"), "n_chaves_lidas": v.get("n_chaves_lidas"), "lidos_antes_da_atribuicao": v.get("lidos_antes_da_atribuicao"), "lidas_sem_origem": v.get("lidas_sem_origem"), "insumos_exigidos_ausentes": v.get("insumos_exigidos_ausentes"), "erro": v.get("erro")} for k, v in r["funcoes"].items()}}, ensure_ascii=False, indent=1))
    sys.exit(0 if r["ok"] else 1)
