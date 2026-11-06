# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] a funcao NOVA e' traducao_turing_v409 (depois do tetelestai_terminal_v408 e dos specs da v408); o terminal passa a herdado; controles negativos (10) e (11)
"""guarda_ordem_de_chamada_v409.py -- A ORDEM DE CHAMADA (licao 1 da v408: a 1a tentativa do rito de 28/10/2026). AUTORAL na v409: a da v408 olhava so' o corpo da funcao chamada no main; os registros de pedra da v408 sao de uma linha (chamam _v405_registro, que chama _v405_formal e a mecanica), e la' a leitura nao aparece: copiar a guarda daria vacuo (nenhuma leitura vista, tudo «ok»).
(na v408 a funcao NOVA era o `tetelestai_terminal_v408`; na v407, o `psion_canto_v407`.) ADAPTADA a v409 (05/11/2026): a funcao NOVA e' UMA, `traducao_turing_v409` (le do core `kernel_formalization`, `external_ladder`, `qg_closure` e `beta`; chamada no main LOGO DEPOIS do bloco do `tetelestai_terminal_v408` e dos specs da v408; miolo `_v409_formal`, `_v398_beta`; mecanica `v409_traducao_mechanics`); a da v407 era o `psion_canto_v407` (registro com funcao; le do core `kernel_formalization`, `external_ladder`, `witness_rigidity`, `qg_closure`, `beta` e as chaves de testemunha: `rede_fock_v394`, `psibit_v395`, `testemunha_estatica_v396`, `witness_layers`); ela e' chamada no main LOGO DEPOIS do bloco do `fechamento_v406`
(que, por sua vez, vem logo depois do `_v405_rodar_specs`), e as chaves que ela le ja' tem de estar gravadas. A leitura dela passa pelo miolo comum da v409 (`_v407_formal`, `_v407_chaves`, `_v398_beta`) e pela mecanica `v407_psion_mechanics`. O `fechamento_v406` passa a ser HERDADO (o codigo dele so' muda na checagem c8, declarada em E20) e segue conferido com o miolo da v408
(`_v406_formal`, `_v406_chaves`, `_v398_beta`) e a mecanica `v406_fechamento_mechanics`; as OITO funcoes de pedra da v408 e o `_v405_rodar_specs` seguem conferidos (o codigo delas nao muda na v409: «nada da v408 perdido»).
Toda chave do core que uma funcao de registro NOVA LE, em qualquer funcao que ela alcanca (core.get("K"), core_.get("K"), core["K"], core_["K"]), tem de estar pronta ANTES da instrucao do main que a chama. Pronta quer dizer: (a) vem de run_um (a primeira instrucao do main e' `core = run_um(...)`; as chaves literais dos dicts de run_um);
ou (b) core["K"] = ... numa instrucao ANTERIOR do main; ou (c) a chamada `K(core)` numa instrucao ANTERIOR do main (a convencao dos registros: a funcao grava core["K"]). O que nao se acha em nenhum dos tres e' FALHA VISIVEL (`lidas_sem_origem`), nunca «ok» por omissao.
Esta guarda e' ESTATICA (AST), nao executa nada. Controle negativo em controle_negativo(): a mesma fonte com o registro da Ponte da Massa chamado ANTES da projecao_transversal_v404 tem de reprovar; uma leitura de chave inexistente tambem; o `fechamento_v406` antes dos specs da v408 tambem; o `psion_canto_v407` ANTES do `fechamento_v406` tambem; e
os dois registros sem a chamada no main tambem.
uso: python -I -B -X utf8 guarda_ordem_de_chamada_v409.py <um.py> [funcao ...]   (rc 0 = toda leitura depois da origem; rc 1 = ha leitura antes ou sem origem; grava GUARDA_ORDEM_DE_CHAMADA_v409.json ao lado do script, com a ordem real e o controle negativo)
Como modulo: ordem_de_chamada(src_text, funcoes) -> dict com "ok"; controle_negativo(src_text) -> dict com "ok"."""
import ast, json, os, re, sys

FUNCOES_PEDRAS = ("ponte_da_massa_v405", "massa_tensao_pura_v405", "identidade_v405", "observador_terminal_v405", "lei_do_diminuto_v405", "tonica_do_hamiltoniano_v405", "disco_de_euler_v405", "ponto_zero_do_psion_v405")   # (as oito da v408: herdadas, intactas)
FUNCOES_HERDADAS_V408 = FUNCOES_PEDRAS + ("_v405_rodar_specs",)   # (o ultimo: as medidas do Grande Atrator rodam dentro dos specs da v408)
FUNCOES_HERDADAS_V409 = FUNCOES_HERDADAS_V408 + ("fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408")   # (v409: os registros da v406, da v407 e da v408 sao herdados, intactos: nenhuma chave antiga muda)
FUNCOES_NOVAS_V409 = ("traducao_turing_v409",)                     # a v409 e' um BUNDLE de um modulo de kernel: o UNICO registro com funcao novo e' o da traducao
FUNCOES_V409 = FUNCOES_NOVAS_V409 + FUNCOES_HERDADAS_V409         # o que o ensaio confere: a nova e as herdadas
MECANICA_DE = dict(zip(FUNCOES_HERDADAS_V408, ("v405_ponte_mechanics", "v405_tensao_mechanics", "v405_identidade_mechanics", "v405_observador_mechanics", "v405_diminuto_mechanics", "v405_tonica_mechanics", "v405_disco_mechanics", "v405_psion_mechanics", "v405_ga_mechanics")))
MECANICA_DE["fechamento_v406"] = "v406_fechamento_mechanics"
MECANICA_DE["psion_canto_v407"] = "v407_psion_mechanics"
MECANICA_DE["tetelestai_terminal_v408"] = "v408_terminal_mechanics"
MECANICA_DE["traducao_turing_v409"] = "v409_traducao_mechanics"
COMUNS = ("_v405_registro", "_v405_formal", "_v398_beta")     # o miolo comum das herdadas: tudo o que o registro le passa por aqui
COMUNS_DE = {"fechamento_v406": ("_v406_formal", "_v406_chaves", "_v398_beta"),   # o miolo comum do fechamento (a leitura das quatro chaves esta em _v406_chaves)
             "psion_canto_v407": ("_v407_formal", "_v407_chaves", "_v398_beta"),   # o miolo comum do psion (a leitura das chaves, a da v408 e as quatro da v406, esta em _v407_chaves)
             "tetelestai_terminal_v408": ("_v408_formal", "_v398_beta"),   # o miolo comum do terminal (nao le chave de testemunha: nenhuma chave antiga muda)
             "traducao_turing_v409": ("_v409_formal", "_v398_beta")}   # o miolo comum da traducao (nao le chave de testemunha: nenhuma chave antiga muda)
INSUMOS_EXIGIDOS = {"traducao_turing_v409": ("tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),
                    "tetelestai_terminal_v408": ("psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),
                    "psion_canto_v407": ("fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "_v405_rodar_specs"),
                    "fechamento_v406": ("rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "_v405_rodar_specs"), "ponte_da_massa_v405": ("neutrino_mass", "projecao_transversal_v404"), "massa_tensao_pura_v405": ("neutrino_mass",), "lei_do_diminuto_v405": ("neutrino_mass",), "tonica_do_hamiltoniano_v405": ("neutrino_mass",), "ponto_zero_do_psion_v405": ("neutrino_mass", "projecao_transversal_v404"), "observador_terminal_v405": ("omega_I",), "_v405_rodar_specs": ("joint_coincidence_result_v3", "ga_mass_audit", "mode_A", "mode_B")}
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


def ordem_de_chamada(src, funcoes=FUNCOES_V409):
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
        # (v409) o insumo exigido vale pela ATRIBUICAO/CHAMADA no main, lido de `atrib`, e nao so' quando a funcao o le como chave do core: o `_v405_rodar_specs` e o `fechamento_v406` sao CHAMADAS que tem de vir antes (do fechamento_v406 e do psion_canto_v407, respectivamente), nao chaves que a funcao leia
        faltam = [k for k in exig if not ((k in atrib and atrib[k] < ic) or k in de_run)]
        exigidos_antes = {k: {"indice": atrib[k], "linha": main.body[atrib[k]].lineno} for k in exig if k in atrib and atrib[k] < ic}
        ok_fn = bool(lidas) and not antes and not sem_origem and not faltam
        out["funcoes"][fn] = {"chamada": {"indice": ic, "linha": main.body[ic].lineno}, "n_chaves_lidas": len(lidas), "chaves_lidas": sorted(lidas), "insumos_produzidos_no_main": no_main, "insumos_de_run_um": fora, "lidas_sem_origem": sem_origem, "insumos_exigidos_ausentes": faltam, "insumos_exigidos_atribuidos_antes_no_main": exigidos_antes, "lidos_antes_da_atribuicao": antes, "ok": ok_fn}
        out["ok"] = out["ok"] and ok_fn
    return out


def _troca_blocos(src, fn_a, fn_b):
    """troca de lugar, por AST, as duas instrucoes VIZINHAS do main que chamam fn_a(core) e fn_b(core) (fn_a vem primeiro no original); devolve o texto novo. Sem reescrever o texto das instrucoes."""
    main_ = [x for x in ast.parse(src).body if isinstance(x, ast.FunctionDef) and x.name == "main"][-1]
    pos_ = {fn_: [i for i, st in enumerate(main_.body) if re.search(r"\b" + fn_ + r"\(core\)", ast.unparse(st))] for fn_ in (fn_a, fn_b)}
    assert all(len(v) == 1 for v in pos_.values()) and pos_[fn_b][0] == pos_[fn_a][0] + 1, ("as duas instrucoes nao sao vizinhas/unicas no main", pos_)
    sa_, sb_ = main_.body[pos_[fn_a][0]], main_.body[pos_[fn_b][0]]
    lin_ = src.split("\n"); bloco_a, bloco_b = lin_[sa_.lineno - 1:sa_.end_lineno], lin_[sb_.lineno - 1:sb_.end_lineno]
    assert sb_.lineno == sa_.end_lineno + 1, "as duas instrucoes nao sao contiguas no texto"
    return "\n".join(lin_[:sa_.lineno - 1] + bloco_b + bloco_a + lin_[sb_.end_lineno:])


def _sem_chamada(src, fn, var):
    """a chamada `var = fn(core)` sai do main (a atribuicao vira um dict vazio); exige que a linha seja achada UMA vez."""
    lin_ = src.split("\n")
    ln_ = [i for i, l in enumerate(lin_) if re.fullmatch(r"\s+" + var + r" = " + fn + r"\(core\)\s*", l)]
    assert len(ln_) == 1, ("a linha da chamada nao foi achada uma vez", fn, ln_)
    m_ = list(lin_); m_[ln_[0]] = re.sub(var + r" = " + fn + r"\(core\)", var + " = {}", m_[ln_[0]])
    return "\n".join(m_)


def controle_negativo(src):
    """(1) a Ponte da Massa chamada ANTES da projecao_transversal_v404 reprova; (2) uma leitura de chave sem origem reprova; (3) a fonte intacta passa; (4) [v406] o fechamento_v406 chamado ANTES do bloco `_v405_rodar_specs` (e, portanto, antes de o main fechar as chaves que ele le) reprova;
    (5) [v406] o fechamento_v406 sem a chamada no main reprova (nunca «ok» por omissao); (6) [v407] o psion_canto_v407 chamado ANTES do fechamento_v406 (as duas instrucoes trocam de lugar) reprova, e o motivo e' o insumo exigido ausente; (7) [v407] o psion_canto_v407 sem a chamada no main reprova;
    (8) [v408] o tetelestai_terminal_v408 chamado ANTES do psion_canto_v407 reprova, e o motivo e' o insumo exigido ausente; (9) [v408] o tetelestai_terminal_v408 sem a chamada no main reprova;
    (10) [v409] o traducao_turing_v409 chamado ANTES do tetelestai_terminal_v408 reprova, e o motivo e' o insumo exigido ausente; (11) [v409] o traducao_turing_v409 sem a chamada no main reprova. Rodado sobre o texto: nada executa."""
    r0 = ordem_de_chamada(src)
    ch_proj = "projecao_transversal_v404(core)"; ch_ponte = "ponte_da_massa_v405(core)"
    linhas = src.split("\n")
    ip = [i for i, l in enumerate(linhas) if re.fullmatch(r"\s+_\w+ = projecao_transversal_v404\(core\)\s*", l)]; ip2 = [i for i, l in enumerate(linhas) if re.fullmatch(r"\s+_\w+ = ponte_da_massa_v405\(core\)\s*", l)]
    assert len(ip) == 1 and len(ip2) == 1, ("as linhas das chamadas nao foram achadas uma vez", ip, ip2)
    # troca so' os nomes das funcoes nas duas instrucoes (a ponte passa a vir antes da projecao)
    a_ = linhas[ip[0]].replace(ch_proj, ch_ponte); b_ = linhas[ip2[0]].replace(ch_ponte, ch_proj)
    m_ = list(linhas); m_[ip[0]] = a_; m_[ip2[0]] = b_
    r1 = ordem_de_chamada("\n".join(m_))
    src2 = src.replace('    m_core_ = (core_.get("neutrino_mass") or {}).get("m_nu_meV")', '    m_core_ = (core_.get("chave_que_nao_existe_v409") or {}).get("m_nu_meV")', 1)
    assert src2 != src
    r2 = ordem_de_chamada(src2)
    # (4) o fechamento_v406 e o bloco dos specs da v408 trocam de lugar no main
    r3 = ordem_de_chamada(_troca_blocos(src, "_v405_rodar_specs", "fechamento_v406"))
    f3_ = r3["funcoes"].get("fechamento_v406") or {}
    # (5) a chamada do fechamento_v406 sai do main (a atribuicao vira um dict vazio)
    r4 = ordem_de_chamada(_sem_chamada(src, "fechamento_v406", "_r406"), ("fechamento_v406",))
    # (6) o psion_canto_v407 e o fechamento_v406 trocam de lugar: o psion passa a ser chamado ANTES do fechamento
    r5 = ordem_de_chamada(_troca_blocos(src, "fechamento_v406", "psion_canto_v407"), ("psion_canto_v407",))
    f5_ = r5["funcoes"].get("psion_canto_v407") or {}
    # (7) a chamada do psion_canto_v407 sai do main
    r6 = ordem_de_chamada(_sem_chamada(src, "psion_canto_v407", "_r407"), ("psion_canto_v407",))
    # (8) o tetelestai_terminal_v408 e o psion_canto_v407 trocam de lugar: o terminal passa a ser chamado ANTES do psion
    r7 = ordem_de_chamada(_troca_blocos(src, "psion_canto_v407", "tetelestai_terminal_v408"), ("tetelestai_terminal_v408",))
    f7_ = r7["funcoes"].get("tetelestai_terminal_v408") or {}
    # (9) a chamada do tetelestai_terminal_v408 sai do main
    r8 = ordem_de_chamada(_sem_chamada(src, "tetelestai_terminal_v408", "_r408"), ("tetelestai_terminal_v408",))
    # (10) o traducao_turing_v409 e o tetelestai_terminal_v408 trocam de lugar: a traducao passa a ser chamada ANTES do terminal
    r9 = ordem_de_chamada(_troca_blocos(src, "tetelestai_terminal_v408", "traducao_turing_v409"), ("traducao_turing_v409",))
    f9_ = r9["funcoes"].get("traducao_turing_v409") or {}
    # (11) a chamada do traducao_turing_v409 sai do main
    r10 = ordem_de_chamada(_sem_chamada(src, "traducao_turing_v409", "_r409"), ("traducao_turing_v409",))
    c = {"intacta_passa": bool(r0["ok"]), "ponte_antes_da_projecao_reprova": bool(not r1["ok"] and "projecao_transversal_v404" in ((r1["funcoes"].get("ponte_da_massa_v405") or {}).get("lidos_antes_da_atribuicao") or []) + ((r1["funcoes"].get("ponte_da_massa_v405") or {}).get("insumos_exigidos_ausentes") or [])),
         "chave_sem_origem_reprova": bool(not r2["ok"]),
         "fechamento_antes_dos_specs_da_v408_reprova": bool(not r3["ok"] and "_v405_rodar_specs" in (f3_.get("insumos_exigidos_ausentes") or [])), "fechamento_sem_chamada_no_main_reprova": bool(not r4["ok"] and "erro" in (r4["funcoes"].get("fechamento_v406") or {})),
         "psion_antes_do_fechamento_reprova": bool(not r5["ok"] and "fechamento_v406" in (f5_.get("insumos_exigidos_ausentes") or [])), "psion_sem_chamada_no_main_reprova": bool(not r6["ok"] and "erro" in (r6["funcoes"].get("psion_canto_v407") or {})),
         "tetelestai_antes_do_psion_reprova": bool(not r7["ok"] and "psion_canto_v407" in (f7_.get("insumos_exigidos_ausentes") or [])), "tetelestai_sem_chamada_no_main_reprova": bool(not r8["ok"] and "erro" in (r8["funcoes"].get("tetelestai_terminal_v408") or {})),
         "traducao_antes_do_terminal_reprova": bool(not r9["ok"] and "tetelestai_terminal_v408" in (f9_.get("insumos_exigidos_ausentes") or [])), "traducao_sem_chamada_no_main_reprova": bool(not r10["ok"] and "erro" in (r10["funcoes"].get("traducao_turing_v409") or {}))}
    c["ok"] = bool(c["intacta_passa"] and all(v for k, v in c.items() if k != "intacta_passa"))
    return c


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    p = sys.argv[1]; fns = tuple(sys.argv[2:]) or FUNCOES_V409
    src_ = open(p, encoding="utf-8").read()
    r = ordem_de_chamada(src_, fns)
    resumo = {"arquivo": p, "ok": r["ok"], "funcoes": {k: {"ok": v.get("ok"), "chamada": v.get("chamada"), "n_chaves_lidas": v.get("n_chaves_lidas"), "lidos_antes_da_atribuicao": v.get("lidos_antes_da_atribuicao"), "lidas_sem_origem": v.get("lidas_sem_origem"), "insumos_exigidos_ausentes": v.get("insumos_exigidos_ausentes"), "insumos_exigidos_atribuidos_antes_no_main": v.get("insumos_exigidos_atribuidos_antes_no_main"), "erro": v.get("erro")} for k, v in r["funcoes"].items()}}
    print(json.dumps(resumo, ensure_ascii=False, indent=1))
    ctl = controle_negativo(src_) if fns == FUNCOES_V409 else None
    if ctl is not None:
        print(json.dumps({"controle_negativo": ctl}, ensure_ascii=False))
    _aqui = os.path.dirname(os.path.abspath(__file__))
    _out = os.path.join(_aqui, "GUARDA_ORDEM_DE_CHAMADA_v409.json")
    json.dump({"arquivo": p, "funcoes_conferidas": list(fns), "ordem_de_chamada": r, "controle_negativo": ctl}, open(_out + ".tmp", "w", encoding="utf-8"), ensure_ascii=False, indent=1); os.replace(_out + ".tmp", _out)
    sys.exit(0 if r["ok"] and (ctl is None or ctl["ok"]) else 1)
