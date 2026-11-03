# -*- coding: utf-8 -*-
"""guarda_ordem_de_chamada_v406.py -- A ORDEM DE CHAMADA (licao 1 da v405: a 1a tentativa do rito de 28/10/2026). AUTORAL na v406: a da v405 olhava so' o corpo da funcao chamada no main; os registros de pedra da v405 sao de uma linha (chamam _v405_registro, que chama _v405_formal e a mecanica), e la' a leitura nao aparece: copiar a guarda daria vacuo (nenhuma leitura vista, tudo «ok»).
ADAPTADA a v406 (02/11/2026): a funcao NOVA e' UMA, `fechamento_v406` (registro com funcao; le do core `kernel_formalization`, `external_ladder`, `qg_closure`, `witness_rigidity`, `beta` e as quatro chaves de testemunha: `rede_fock_v394`, `psibit_v395`, `testemunha_estatica_v396`, `witness_layers`); ela e' chamada no main LOGO DEPOIS do bloco `_v405_rodar_specs` e as chaves que ela le ja' tem de estar gravadas. A leitura dela passa pelo miolo comum da v406 (`_v406_formal`, `_v406_chaves`, `_v398_beta`) e pela mecanica `v406_fechamento_mechanics`. As OITO funcoes e o `_v405_rodar_specs` da v405 seguem conferidos (o codigo delas nao muda na v406: «nada da v405 perdido»).
Toda chave do core que uma funcao de registro NOVA LE, em qualquer funcao que ela alcanca (core.get("K"), core_.get("K"), core["K"], core_["K"]), tem de estar pronta ANTES da instrucao do main que a chama. Pronta quer dizer: (a) vem de run_um (a primeira instrucao do main e' `core = run_um(...)`; as chaves literais dos dicts de run_um);
ou (b) core["K"] = ... numa instrucao ANTERIOR do main; ou (c) a chamada `K(core)` numa instrucao ANTERIOR do main (a convencao dos registros: a funcao grava core["K"]). O que nao se acha em nenhum dos tres e' FALHA VISIVEL (`lidas_sem_origem`), nunca «ok» por omissao.
Esta guarda e' ESTATICA (AST), nao executa nada. Controle negativo em controle_negativo(): a mesma fonte com o registro da Ponte da Massa chamado ANTES da projecao_transversal_v404 tem de reprovar, e uma leitura de chave inexistente tambem.
uso: python -I -B -X utf8 guarda_ordem_de_chamada_v406.py <um.py> [funcao ...]   (rc 0 = toda leitura depois da origem; rc 1 = ha leitura antes ou sem origem)
Como modulo: ordem_de_chamada(src_text, funcoes) -> dict com "ok"; controle_negativo(src_text) -> dict com "ok"."""
import ast, json, re, sys

FUNCOES_PEDRAS = ("ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405")   # (as oito da v405: herdadas, intactas)
FUNCOES_HERDADAS_V405 = FUNCOES_PEDRAS + ("_v405_rodar_specs",)   # (o ultimo: as medidas do Grande Atrator rodam dentro dos specs da v405)
FUNCOES_NOVAS_V406 = ("fechamento_v406",)                         # a v406 e' um BUNDLE de modulos de kernel: o UNICO registro com funcao novo e' o fechamento
FUNCOES_V406 = FUNCOES_NOVAS_V406 + FUNCOES_HERDADAS_V405         # o que o ensaio confere: a nova e as herdadas
MECANICA_DE = dict(zip(FUNCOES_HERDADAS_V405, ("v405_ponte_mechanics", "v405_tensao_mechanics", "v405_identidade_mechanics", "v405_observador_mechanics", "v405_diminuto_mechanics", "v405_tonica_mechanics", "v405_disco_mechanics", "v405_psion_mechanics", "v405_ga_mechanics")))
MECANICA_DE["fechamento_v406"] = "v406_fechamento_mechanics"
COMUNS = ("_v405_registro", "_v405_formal", "_v398_beta")     # o miolo comum das herdadas: tudo o que o registro le passa por aqui
COMUNS_DE = {"fechamento_v406": ("_v406_formal", "_v406_chaves", "_v398_beta")}   # o miolo comum do fechamento (a leitura das quatro chaves esta em _v406_chaves)
INSUMOS_EXIGIDOS = {"fechamento_v406": ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "_v405_rodar_specs"), "ponte_da_massa_v405": ("neutrino_mass", "projecao_transversal_v404"), "massa_tensao_pura_v405": ("neutrino_mass",), "lei_do_diminuto_v405": ("neutrino_mass",), "tonica_do_hamiltoniano_v405": ("neutrino_mass",), "ponto_zero_do_psion_v405": ("neutrino_mass", "projecao_transversal_v404"), "observador_terminal_v405": ("omega_I",), "_v405_rodar_specs": ("joint_coincidence_result_v3", "ga_mass_audit", "mode_A", "mode_B")}
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


def ordem_de_chamada(src, funcoes=FUNCOES_V406):
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
    out = {"funcoes": {}, "ok": True, "comuns_lidos_de": list(COMUNS), "comuns_lidos_de_por_funcao": {k: list(v) for k, v in COMUNS_DE.items()}}
    for fn in funcoes:
        comuns = COMUNS_DE.get(fn, COMUNS)
        faltando = [x for x in (fn, MECANICA_DE.get(fn)) + comuns if x and len(defs.get(x) or []) != 1]
        if faltando:
            out["funcoes"][fn] = {"erro": "funcao ausente ou duplicada: %r" % (faltando,)}; out["ok"] = False; continue
        lidas = set()
        for x in (fn, MECANICA_DE[fn]) + comuns:
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
        # (v406) o insumo exigido vale pela ATRIBUICAO/CHAMADA no main, lido de `atrib`, e nao so' quando a funcao o le como chave do core: o `_v405_rodar_specs` e' uma CHAMADA que tem de vir antes do fechamento_v406, nao uma chave que ele leia
        faltam = [k for k in exig if not ((k in atrib and atrib[k] < ic) or k in de_run)]
        exigidos_antes = {k: {"indice": atrib[k], "linha": main.body[atrib[k]].lineno} for k in exig if k in atrib and atrib[k] < ic}
        ok_fn = bool(lidas) and not antes and not sem_origem and not faltam
        out["funcoes"][fn] = {"chamada": {"indice": ic, "linha": main.body[ic].lineno}, "n_chaves_lidas": len(lidas), "insumos_produzidos_no_main": no_main, "insumos_de_run_um": fora, "lidas_sem_origem": sem_origem, "insumos_exigidos_ausentes": faltam, "insumos_exigidos_atribuidos_antes_no_main": exigidos_antes, "lidos_antes_da_atribuicao": antes, "ok": ok_fn}
        out["ok"] = out["ok"] and ok_fn
    return out


def controle_negativo(src):
    """(1) a Ponte da Massa chamada ANTES da projecao_transversal_v404 reprova; (2) uma leitura de chave sem origem reprova; (3) a fonte intacta passa; (4) [v406] o fechamento_v406 chamado ANTES do bloco `_v405_rodar_specs` (e, portanto, antes de o main fechar as quatro chaves que ele le) reprova; (5) [v406] o fechamento_v406 sem a chamada no main reprova (nunca «ok» por omissao). Rodado sobre o texto: nada executa."""
    r0 = ordem_de_chamada(src)
    ch_proj = "projecao_transversal_v404(core)"; ch_ponte = "ponte_da_massa_v405(core)"
    linhas = src.split("\n")
    ip = [i for i, l in enumerate(linhas) if re.fullmatch(r"\s+_\w+ = projecao_transversal_v404\(core\)\s*", l)]; ip2 = [i for i, l in enumerate(linhas) if re.fullmatch(r"\s+_\w+ = ponte_da_massa_v405\(core\)\s*", l)]
    assert len(ip) == 1 and len(ip2) == 1, ("as linhas das chamadas nao foram achadas uma vez", ip, ip2)
    # troca so' os nomes das funcoes nas duas instrucoes (a ponte passa a vir antes da projecao)
    a_ = linhas[ip[0]].replace(ch_proj, ch_ponte); b_ = linhas[ip2[0]].replace(ch_ponte, ch_proj)
    m_ = list(linhas); m_[ip[0]] = a_; m_[ip2[0]] = b_
    r1 = ordem_de_chamada("\n".join(m_))
    src2 = src.replace('    m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")', '    m_core_ = (core_.get("chave_que_nao_existe_v406") or {}).get("m_nu_meV")', 1)
    assert src2 != src
    r2 = ordem_de_chamada(src2)
    # (4) o fechamento_v406 e o bloco dos specs da v405 trocam de lugar no main: troca de BLOCOS de linhas (lineno..end_lineno das duas instrucoes), por AST, sem reescrever o texto
    main_ = [x for x in ast.parse(src).body if isinstance(x, ast.FunctionDef) and x.name == "main"][-1]
    pos_ = {fn_: [i for i, st in enumerate(main_.body) if re.search(r"\b" + fn_ + r"\(core\)", ast.unparse(st))] for fn_ in ("_v405_rodar_specs", "fechamento_v406")}
    assert all(len(v) == 1 for v in pos_.values()) and pos_["fechamento_v406"][0] == pos_["_v405_rodar_specs"][0] + 1, ("as duas instrucoes nao sao vizinhas/unicas no main", pos_)
    sa_, sb_ = main_.body[pos_["_v405_rodar_specs"][0]], main_.body[pos_["fechamento_v406"][0]]
    lin_ = src.split("\n"); bloco_a, bloco_b = lin_[sa_.lineno - 1:sa_.end_lineno], lin_[sb_.lineno - 1:sb_.end_lineno]
    assert sb_.lineno == sa_.end_lineno + 1, "as duas instrucoes nao sao contiguas no texto"
    r3 = ordem_de_chamada("\n".join(lin_[:sa_.lineno - 1] + bloco_b + bloco_a + lin_[sb_.end_lineno:]))
    f3_ = r3["funcoes"].get("fechamento_v406") or {}
    # (5) a chamada do fechamento_v406 sai do main (a atribuicao vira um dict vazio)
    ln_ = [i for i, l in enumerate(lin_) if re.fullmatch(r"\s+_r406 = fechamento_v406\(core\)\s*", l)]
    assert len(ln_) == 1, ("a linha da chamada do fechamento nao foi achada uma vez", ln_)
    m5_ = list(lin_); m5_[ln_[0]] = re.sub(r"_r406 = fechamento_v406\(core\)", "_r406 = {}", m5_[ln_[0]])
    r4 = ordem_de_chamada("\n".join(m5_), ("fechamento_v406",))
    return {"intacta_passa": bool(r0["ok"]), "ponte_antes_da_projecao_reprova": bool(not r1["ok"] and "projecao_transversal_v404" in ((r1["funcoes"].get("ponte_da_massa_v405") or {}).get("lidos_antes_da_atribuicao") or []) + ((r1["funcoes"].get("ponte_da_massa_v405") or {}).get("insumos_exigidos_ausentes") or [])),
            "chave_sem_origem_reprova": bool(not r2["ok"]),
            "fechamento_antes_dos_specs_da_v405_reprova": bool(not r3["ok"] and "_v405_rodar_specs" in (f3_.get("insumos_exigidos_ausentes") or [])), "fechamento_sem_chamada_no_main_reprova": bool(not r4["ok"] and "erro" in (r4["funcoes"].get("fechamento_v406") or {})),
            "ok": bool(r0["ok"] and not r1["ok"] and not r2["ok"] and not r3["ok"] and "_v405_rodar_specs" in (f3_.get("insumos_exigidos_ausentes") or []) and not r4["ok"] and "erro" in (r4["funcoes"].get("fechamento_v406") or {}))}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    p = sys.argv[1]; fns = tuple(sys.argv[2:]) or FUNCOES_V406
    src_ = open(p, encoding="utf-8").read()
    r = ordem_de_chamada(src_, fns)
    print(json.dumps({"arquivo": p, "ok": r["ok"], "funcoes": {k: {"ok": v.get("ok"), "chamada": v.get("chamada"), "n_chaves_lidas": v.get("n_chaves_lidas"), "lidos_antes_da_atribuicao": v.get("lidos_antes_da_atribuicao"), "lidas_sem_origem": v.get("lidas_sem_origem"), "insumos_exigidos_ausentes": v.get("insumos_exigidos_ausentes"), "insumos_exigidos_atribuidos_antes_no_main": v.get("insumos_exigidos_atribuidos_antes_no_main"), "erro": v.get("erro")} for k, v in r["funcoes"].items()}}, ensure_ascii=False, indent=1))
    sys.exit(0 if r["ok"] else 1)
