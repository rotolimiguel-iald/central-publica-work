# -*- coding: utf-8 -*-
"""As correcoes da 2a passada NO GERADOR DO CANDIDATO (gerar_candidato_v384.py), por trocas com contagem conferida."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "gerar_candidato_v384.py")
s = open(P, encoding="utf-8").read()
open(P + ".bak_antes_afer2", "w", encoding="utf-8", newline="").write(s)
TAB = chr(9); BS = chr(92)


def rep(old, new, n=1):
    global s
    c = s.count(old)
    assert c == n, (c, old[:120])
    s = s.replace(old, new)


# (1) a ratificacao do operador: obrigatoria para o candidato instalavel; sem ela, so um candidato de ENSAIO (outro nome, nao instalavel)
rep('''PJ = json.load(open(PRJ, encoding="utf-8"))
SPEC = PJ["spec"]''', '''PJ = json.load(open(PRJ, encoding="utf-8"))
SPEC = PJ["spec"]
RAT = PJ.get("ratificacao_do_operador") or {}
ENSAIO = os.environ.get("TGL_CANDIDATO_ENSAIO") == "1"
if not ENSAIO:
    assert RAT.get("verbatim") and RAT.get("quando"), "o pre-registro NAO tem a ratificacao do operador gravada: so candidato de ensaio (TGL_CANDIDATO_ENSAIO=1)"''')
rep('''assert WSHA == PJ["motor"]["worker_sha256"], "o trabalhador NAO e' o congelado no pre-registro (gere um V1.x do pre-registro)"''',
    '''assert WSHA == PJ["motor"]["worker_sha256"] == SPEC["worker_sha256"], "o trabalhador NAO e' o congelado no pre-registro (gere um V1.x do pre-registro)"''')
# (2) W07: as chaves novas no registro do selo; a leitura so diz RATIFIED quando ha ratificacao
rep('''+ 'L_ANTI_IS_SQRT_BETA_SQRT_K_THE_ROOT_LAW__GAMMA_DISS_FREE_NEVER_CALIBRATED__PREREGISTRATION_V1_FROZEN_BY_HASH_' + SPEC_SHA[:16].upper() + '__FOLD_HIERARCHY_IS_MATHEMATICS_NOT_A_TEST__\'''',
    '''+ 'L_ANTI_IS_SQRT_BETA_SQRT_K_THE_ROOT_LAW__GAMMA_DISS_FREE_NEVER_CALIBRATED__PREREGISTRATION_V1_FROZEN_BY_HASH_' + SPEC_SHA[:16].upper() + ('_RATIFIED_BY_THE_OPERATOR' if RAT else '_DRY_RUN_CANDIDATE_NOT_RATIFIED') + '__FOLD_HIERARCHY_IS_MATHEMATICS_NOT_A_TEST__\'''')
rep('''+ 'T1_SEPARATION_STRUCTURAL_IN_EXACT_ARITHMETIC__REUSE_TOOL_KEYED_BY_CONTENT_FINAL_VERSION_ALWAYS_FULL__COMPUTED_NOT_MEASURED__NOT_A_CONFIRMATION__GATE_UNTOUCHED",' + CRLF''',
    '''+ 'T1_IS_THE_INSTRUMENT_SEPARATION_STRUCTURAL_IN_EXACT_ARITHMETIC__NONHERMITIAN_EIGENVALUES_BY_MAGMA_CUSOLVER_CRASHES_DETERMINISTICALLY__REUSE_TOOL_KEYED_BY_CONTENT_FINAL_VERSION_ALWAYS_FULL__COMPUTED_NOT_MEASURED__NOT_A_CONFIRMATION__GATE_UNTOUCHED",' + CRLF''')
rep('''("verdict", "verdict_rederived", "key", "mode", "reuse", "result_sha256", "details_sha256", "worker_sha256", "spec_sha256_in_result", "custody_chain_ok", "partial", "all_verified", "status", "does_not_gate_core")''',
    '''("verdict", "verdict_rederived", "key", "mode", "reuse", "result_sha256", "details_sha256", "worker_sha256", "spec_sha256_in_result", "custody_chain_ok", "partial", "timed_out", "worker_rc", "run_id", "beta_matches_core", "all_verified", "status", "does_not_gate_core")''')
# (3) W08..W11: o terceiro balde; o resultado do pilar no hash do selo; o conversor TXT; o \\texttt virado TAB (v376, errata ao lado)
rep('''for p in patches:
    if p["grupo"] == "G_ARTIGO":
        continue''', '''A08 = "    _formais = [k for k in _not_sealed if k not in _recusas]" + CRLF
add("W08_terceiro_balde", "G_SELO", A08, A08
    + "    # v384 AO LADO (afericao 2, achado 36): o pilar quantico nao concluido (ambiente ou instrumento de calculo) nao e' divida formal da teoria nem recusa de dado" + CRLF
    + "    _computacao = [k for k in _formais if str((core.get(k) or {}).get(\\"verdict\\") or \\"\\").startswith(\\"TGL_QUANTUM_PILLAR_V1__\\")]" + CRLF
    + "    _formais = [k for k in _formais if k not in _computacao]" + CRLF, "selo: o terceiro balde da custodia de sentido (computacao nao concluida).")
A08b = '    seal["not_sealed_this_run"] = {"formais": _formais, "recusas_de_dado": _recusas}' + CRLF
add("W08b_terceiro_balde_selo", "G_SELO", A08b, '    seal["not_sealed_this_run"] = {"formais": _formais, "recusas_de_dado": _recusas, "computacao_nao_concluida": _computacao}   # v384: o terceiro balde' + CRLF,
    "selo: not_sealed_this_run ganha computacao_nao_concluida.")
A09 = '                  "tgl_kernel_proof_manifest.json"]:' + CRLF
add("W09_selo_hash_do_pilar", "G_SELO", A09, '                  "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json"]:   # v384: o resultado do pilar no hash do selo (afericao 2, achado 40)' + CRLF,
    "selo: o resultado do pilar quantico entra na lista hasheada.")
A10 = '    t = t.replace("' + BS + BS + 'bTGL", "β_TGL").replace("' + BS + BS + 'Msun", "M_sol")' + CRLF
add("W10_txt_milhar_e_porcento", "G_ARTIGO", A10, A10 + '    t = t.replace("' + BS + BS + ',", "' + BS + 'u2009").replace("' + BS + BS + '%", "%")   # v384 AO LADO (afericao 2, achado 47): o espaco fino e o por cento no TXT' + CRLF,
    "TXT: \\\\, vira espaco fino e \\\\% vira %.")
_tabs = T.count(TAB + "exttt{evidence")
assert _tabs == 2, ("o TAB da v376 nao esta onde a afericao disse", _tabs)
for _ln in [l for l in T.split(CRLF) if (TAB + "exttt{evidence") in l]:
    assert _ln.lstrip().startswith(("r\\"", "s.append(r\\"", "(r\\"")) or ' r"' in _ln or '(r"' in _ln, "o TAB nao esta numa string crua: " + _ln[:120]
T = T.replace(TAB + "exttt{evidence", BS + "texttt{evidence")
patches.append({"id": "W11_tab_da_v376", "grupo": "G_ARTIGO", "old": TAB + "exttt{evidence", "new": BS + "texttt{evidence",
                "o_que_muda": "ERRATA AO LADO (gerencia, em nome proprio): na errata E7 da v376, um TAB no lugar de \\\\t fazia o PDF mostrar 'exttt'; agora \\\\texttt (PT e EN)."})
for p in patches:
    if p["grupo"] == "G_ARTIGO":
        continue''')
# (4) a volta byte a byte conferida no texto FINAL (achado 38) e o nome do candidato de ensaio
rep('''ast.parse(T)
out = os.path.join(HERE, "um_v384_candidato.py")''', '''ast.parse(T)
_vals = {}
for _l in T.split(CRLF):
    for _nm in ("_QP_WORKER_SRC = ", "_QP_SPEC_JSON = "):
        if _l.startswith(_nm):
            _vals[_nm] = ast.literal_eval(_l[len(_nm):])
assert _vals.get("_QP_WORKER_SRC = ", "").encode("utf-8") == WSRC_B and _vals.get("_QP_SPEC_JSON = ") == SPEC_CANON, "o texto embutido NAO volta exato do candidato final"
out = os.path.join(HERE, "um_v384_candidato_ENSAIO.py" if ENSAIO else "um_v384_candidato.py")''')
rep('''man = {"candidato": out, "sha16": h16, "bytes": len(b), "base_v383_sha16": SHA0, "spec_sha256": SPEC_SHA, "worker_sha256": WSHA, "prereg_sha256": PR_SHA,''',
    '''man = {"candidato": out, "ensaio": ENSAIO, "ratificacao_do_operador": RAT, "sha16": h16, "bytes": len(b), "base_v383_sha16": SHA0, "spec_sha256": SPEC_SHA, "worker_sha256": WSHA, "prereg_sha256": PR_SHA,''')
rep('''json.dump(man, open(os.path.join(HERE, "CANDIDATO_v384.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)''',
    '''_mp = os.path.join(HERE, "CANDIDATO_v384_ENSAIO.json" if ENSAIO else "CANDIDATO_v384.json")
open(_mp + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(_mp + ".tmp", _mp)''')
ast.parse(s)
open(P + ".tmp", "w", encoding="utf-8", newline=chr(10)).write(s); os.replace(P + ".tmp", P); print("ok")
