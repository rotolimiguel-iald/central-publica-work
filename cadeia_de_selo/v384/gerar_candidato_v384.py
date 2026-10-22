# -*- coding: utf-8 -*-
"""gerar_candidato_v384.py -- gera o um.py CANDIDATO v384 a partir da v383 SELADA no Nos (NUNCA escreve o canonico). Molde: gerar_candidato_v383.py.
AS ORDENS DO OPERADOR (02-03/10/2026): o mundo quantico da TGL na GPU, em paralelo com o kernel e os testes cosmologicos; os CINCO saltos de Lindblad;
o servidor parado durante o rito (no lancador, nao aqui); o rito robusto; a FERRAMENTA de reaproveitamento; a introducao e a nota no artigo.
(1) KERNEL EMBUTIDO: o MESMO da v383 (nenhuma pedra nova).
(2) PATCHES (count(old) == 1): UM_VERSION v384; o runtime v384 (o trabalhador da GPU EMBUTIDO byte a byte, a especificacao congelada, o hash e os sha256 do
    pre-registro LIDOS dos arquivos); o lancamento logo antes do kernel (depois da inscricao); a espera e o registro no core depois da v383; a introducao e a
    nota no artigo PT/EN (antes da Regua/Ruler); o selo (uma leitura e o registro proprio AO LADO do gate).
uso: python gerar_candidato_v384.py <PREREGISTRO_..._V1.json> <worker.py>"""
import ast, hashlib, json, os, re, sys
if sys.flags.optimize:   # as guardas sao assert: com -O elas sumiriam sem aviso (9a afericao)
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
CRLF = "\r\n"
BS = chr(92); TAB = chr(9)
PRJ, WK = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
PRM = PRJ[:-5] + ".md"
V3 = os.path.join(os.path.dirname(HERE), "v383")
AP3 = json.load(open(os.path.join(V3, "APLICADO_AO_CANONICO_20261002_200400.json"), encoding="utf-8"))
SHA0 = AP3["um_py_novo"]["sha16"]
raw = open(os.path.join(NOS, "um.py"), "rb").read()
assert hashlib.sha256(raw).hexdigest()[:16] == SHA0, "o canonico no Nos nao e a v383 selada"
T = raw.decode("utf-8")
RT = open(os.path.join(HERE, "v384_runtime.py"), encoding="utf-8").read()
RT0_FIRST = open(os.path.join(V3, "v383_runtime.py"), encoding="utf-8").read().splitlines()[0]
# o pre-registro e o trabalhador, LIDOS (nunca digitados)
PJ = json.load(open(PRJ, encoding="utf-8"))
SPEC = PJ["spec"]
RAT = PJ.get("ratificacao_do_operador") or {}
ENSAIO = os.environ.get("TGL_CANDIDATO_ENSAIO") == "1"
PERM = "C:/IALD/Bancada_Um/investigacao/preregistro_pilar_quantico_03out/"
if not ENSAIO:
    assert RAT.get("verbatim") and RAT.get("quando"), "o pre-registro NAO tem a ratificacao do operador gravada: so candidato de ensaio (TGL_CANDIDATO_ENSAIO=1)"
    assert (RAT.get("transcrito") or {}).get("de_teste") is False, "a ratificacao nao diz qual transcrito leu, ou veio de transcrito de TESTE"   # 8a afericao
    _TRC = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
    assert os.path.normcase(os.path.abspath((RAT.get("transcrito") or {}).get("caminho") or "")) == os.path.normcase(_TRC), "a ratificacao nao foi lida do transcrito canonico"   # 8a
    _pp = PRJ.replace(BS, "/")
    assert _pp.startswith(PERM) and "RASCUNHO" not in _pp.upper() and "/TEMP/" not in _pp.upper() and "SCRATCHPAD" not in _pp.upper(), \
        "o pre-registro do candidato instalavel tem de morar no lugar permanente (%s), nunca rascunho/TEMP: %s" % (PERM, _pp)   # 3a afericao
SPEC_CANON = json.dumps(SPEC, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
SPEC_SHA = hashlib.sha256(SPEC_CANON.encode("utf-8")).hexdigest()
assert SPEC_SHA == PJ["spec_sha256"], "o hash da especificacao nao bate com o gravado no pre-registro"
if not ENSAIO:
    assert RAT.get("spec_sha256_ratificada") == SPEC_SHA == RAT.get("spec_sha256_do_rascunho_apresentado") and RAT.get("a_especificacao_ratificada_e_a_do_rascunho") is True, \
        "a ratificacao nao e' da especificacao apresentada ao operador"   # 3a afericao
WSRC_B = open(WK, "rb").read(); WSRC = WSRC_B.decode("utf-8")
assert "\r" not in WSRC, "o trabalhador tem de estar em LF (o texto embutido e' materializado byte a byte)"
WSHA = hashlib.sha256(WSRC_B).hexdigest()
assert WSHA == PJ["motor"]["worker_sha256"] == SPEC["worker_sha256"], "o trabalhador NAO e' o congelado no pre-registro (gere um V1.x do pre-registro)"
PR_SHA = {"json": hashlib.sha256(open(PRJ, "rb").read()).hexdigest(), "md": hashlib.sha256(open(PRM, "rb").read()).hexdigest()}
for ph, val in (("__QP_WORKER_SRC__", repr(WSRC)), ("__QP_SPEC_JSON__", repr(SPEC_CANON)), ("__QP_SPEC_SHA256__", SPEC_SHA),
                ("__QP_PREREG_JSON_PATH__", PRJ.replace("\\", "/")), ("__QP_PREREG_JSON_SHA256__", PR_SHA["json"]),
                ("__QP_PREREG_MD_PATH__", PRM.replace("\\", "/")), ("__QP_PREREG_MD_SHA256__", PR_SHA["md"])):
    assert RT.count(ph) == 1, ph
    RT = RT.replace(ph, val)
ast.parse(RT)
# o texto embutido volta EXATO
_ns = {}
exec(compile("\n".join(l for l in RT.splitlines() if l.startswith(("_QP_WORKER_SRC = ", "_QP_SPEC_JSON = "))), "<qp>", "exec"), _ns)
assert _ns["_QP_WORKER_SRC"].encode("utf-8") == WSRC_B and _ns["_QP_SPEC_JSON"] == SPEC_CANON

patches = []


def add(pid, grupo, old, new_, selo):
    global T
    assert T.count(old) == 1, (pid, T.count(old))
    T = T.replace(old, new_)
    patches.append({"id": pid, "grupo": grupo, "old": old, "new": new_, "o_que_muda": selo})


def crlf(s):
    return s.replace("\r\n", "\n").replace("\n", CRLF)


def linha_unica(prefixo_regex):
    m = re.search(prefixo_regex + r"[^\r\n]*\r\n", T, re.M)
    assert m and T.count(m.group(0)) == 1, prefixo_regex
    return m.group(0)


m = re.search(r'^UM_VERSION = "v383"[^\r\n]*' + CRLF, T, re.M)
assert m and T.count('UM_VERSION = "v383"') == 1
add("W01_versao", "G_MEMORIA", m.group(0), 'UM_VERSION = "v384"   # v384 (03/10/2026): a CONSTANTE UNICA de versao -- o pilar quantico na GPU (cinco saltos de Lindblad) em paralelo com o rito; v383 em 02/10' + CRLF,
    "UM_VERSION = 'v384'.")
assert T.count(RT0_FIRST) == 1
add("W02_runtime", "G_RUNTIME", RT0_FIRST, crlf(RT.rstrip("\n") + "\n\n\n") + RT0_FIRST,
    "runtime v384: o trabalhador da GPU embutido (sha256 %s), a especificacao congelada (sha256 %s), o lancamento, a espera, a rederivacao, o cache." % (WSHA[:16], SPEC_SHA[:16]))
A03 = "    materialize_embedded_kernel()   # v31: o kernel nasce DESTE arquivo" + CRLF
add("W03_lancamento", "G_RUNTIME", A03, "    _QP_ST_V384 = quantum_pillar_start_v384()   # v384: o pilar quantico (o sistema aberto da TGL na GPU) e' lancado AGORA, em paralelo com o kernel e os ritos cosmologicos" + CRLF + A03,
    "main: o trabalhador da GPU e' lancado logo depois da inscricao, antes do kernel.")
A04 = linha_unica(r'^    print\("   \[v383\] o livro de cobrancas')
reg = ['    core["quantum_pillar_v384"] = quantum_pillar_finish_v384(_QP_ST_V384, core)   # v384: espera o trabalhador (prazo e progresso), le, confere o sha256, REDERIVA o veredito, grava o cache (rodada completa)',
       '    print("   [v384] o pilar quantico (o sistema aberto da TGL na GPU: H_LD e os cinco saltos de Lindblad; [COMPUTED]): %s" % core["quantum_pillar_v384"]["verdict"])']
add("W04_registro", "G_RUNTIME", A04, A04 + CRLF.join(reg) + CRLF, "core: +1 chave v384 (depois da v383, antes do artigo).")
pt = open(os.path.join(HERE, "artigo_pt_v384.pysnip"), encoding="utf-8").read()
A05 = '    s.append(r"\\section*{R\u00e9gua: o que cada coisa \u00e9}")' + CRLF
add("W05_artigo_PT", "G_ARTIGO", A05, crlf(pt.rstrip("\n") + "\n") + A05, "artigo PT: a introducao (o que o codigo faz agora) e a nota (o que se calcula na GPU e como), antes da Regua.")
en = open(os.path.join(HERE, "artigo_en_v384.pysnip"), encoding="utf-8").read()
A06 = '    s.append(r"\\section*{Ruler: what each thing is}")' + CRLF
add("W06_artigo_EN", "G_ARTIGO", A06, crlf(en.rstrip("\n") + "\n") + A06, "artigo EN: the introduction and the GPU note, before the Ruler.")
A07 = linha_unica(r'^ {12}"the_ledger_of_charges_reading_v383": ')
add("W07_selo", "G_SELO", A07, A07 + "            # v384 (03/10/2026) -- o PILAR QUANTICO: registro proprio AO LADO do gate; nenhum valor do gate muda; [COMPUTED], nunca medicao" + CRLF
    + '            "the_quantum_pillar_reading_v384": "OPERATOR_ORDERS_2026_10_02_AND_03__THE_QUANTUM_WORLD_OF_THE_TGL_ON_THE_GPU_IN_PARALLEL_WITH_THE_KERNEL_AND_THE_COSMOLOGICAL_RITES__FIVE_LINDBLAD_JUMPS_RATIFIED__'
    + 'L_ANTI_IS_SQRT_BETA_SQRT_K_THE_ROOT_LAW__GAMMA_DISS_FREE_NEVER_CALIBRATED__' + (('PREREGISTRATION_V1_FROZEN_BY_HASH_' + SPEC_SHA[:16].upper() + '_RATIFIED_BY_THE_OPERATOR') if (RAT and not ENSAIO) else ('PREREGISTRATION_V1_DRAFT_SPEC_HASH_' + SPEC_SHA[:16].upper() + '_DRY_RUN_CANDIDATE_NOT_RATIFIED')) + '__FOLD_HIERARCHY_IS_MATHEMATICS_NOT_A_TEST__'
    + 'T1_IS_THE_INSTRUMENT_SEPARATION_STRUCTURAL_IN_EXACT_ARITHMETIC__NONHERMITIAN_EIGENVALUES_BY_MAGMA_CUSOLVER_CRASHES_DETERMINISTICALLY__REUSE_TOOL_KEYED_BY_CONTENT_FINAL_VERSION_ALWAYS_FULL__COMPUTED_NOT_MEASURED__NOT_A_CONFIRMATION__GATE_UNTOUCHED",' + CRLF
    + '            "quantum_pillar_v384": {k_: (core.get("quantum_pillar_v384") or {}).get(k_) for k_ in ("verdict", "verdict_rederived", "key", "mode", "reuse", "result_sha256", "details_sha256", "cpuref_sha256", "run_dir", "copied_to_out", "copy_to_out_error", "out_marker_error", "out_file_removed", "out_file_remove_error", "out_file_sha256", "worker_sha256", "spec_sha256_in_result", "custody_chain_ok", "partial", "timed_out", "worker_rc", "run_id", "beta_matches_core", "all_verified", "status", "does_not_gate_core")},' + CRLF,
    "selo: +1 leitura (string) e +1 registro proprio do pilar quantico, ao lado do gate.")
A08 = "    _formais = [k for k in _not_sealed if k not in _recusas]" + CRLF
add("W08_terceiro_balde", "G_SELO", A08, A08
    + "    # v384 AO LADO (afericao 2, achado 32): o pilar quantico nao concluido (ambiente ou instrumento de calculo) nao e' divida formal da teoria nem recusa de dado" + CRLF
    + "    _computacao = [k for k in _formais if str((core.get(k) or {}).get(\"verdict\") or \"\").startswith(\"TGL_QUANTUM_PILLAR_V1__\")]" + CRLF
    + "    _formais = [k for k in _formais if k not in _computacao]" + CRLF, "selo: o terceiro balde da custodia de sentido (computacao nao concluida).")
A08b = '    seal["not_sealed_this_run"] = {"formais": _formais, "recusas_de_dado": _recusas}' + CRLF
add("W08b_terceiro_balde_selo", "G_SELO", A08b, '    seal["not_sealed_this_run"] = {"formais": _formais, "recusas_de_dado": _recusas, "computacao_nao_concluida": _computacao}   # o terceiro balde (ver o comentario acima)' + CRLF,
    "selo: not_sealed_this_run ganha computacao_nao_concluida.")
A08c = ('    print("[selo] custodia de sentido: %d modulo(s) all_verified=False -- formais (divida): %s | recusas de dado (ativos): %s"' + CRLF
        + '          % (len(_not_sealed), ", ".join(_formais) or "nenhum", ", ".join(_recusas) or "nenhuma"))' + CRLF)
add("W08c_terceiro_balde_stdout", "G_SELO", A08c,
    '    print("[selo] custodia de sentido: %d modulo(s) all_verified=False -- formais (divida): %s | recusas de dado (ativos): %s | computacao nao concluida: %s"   # v384: o terceiro balde nomeado (regra v303)' + CRLF
    + '          % (len(_not_sealed), ", ".join(_formais) or "nenhum", ", ".join(_recusas) or "nenhuma", ", ".join(_computacao) or "nenhuma"))' + CRLF,
    "stdout: o terceiro balde nomeado na linha da custodia de sentido (regra v303).")
A09 = '                  "tgl_kernel_proof_manifest.json"]:' + CRLF
add("W09_selo_hash_do_pilar", "G_SELO", A09, '                  "tgl_kernel_proof_manifest.json", "um_absoluto_pilar_quantico.json"]:   # v384: o resultado do pilar no hash do selo (afericao 2, achado 36)' + CRLF,
    "selo: o resultado do pilar quantico entra na lista hasheada.")
A09b = '        json.dump(seal, open(os.path.join(OUT, "um_absoluto_selo.json"), "w", encoding="utf-8"), indent=2)' + CRLF
add("W09b_selo_so_o_pilar_desta_rodada", "G_SELO", A09b,
    '        # v384 (5a afericao): o arquivo do pilar so e' + "'" + ' hasheado se for o que o runtime escreveu NESTA rodada (out_file_sha256); senao, NOT_THIS_RUN' + CRLF
    + '        _pq_ = core.get("quantum_pillar_v384") or {}' + CRLF
    + '        if "quantum_pillar_v384" in core and seal["sha256"].get("um_absoluto_pilar_quantico.json") not in ("MISSING_THIS_RUN", _pq_.get("out_file_sha256")):' + CRLF
    + '            seal["sha256"]["um_absoluto_pilar_quantico.json"] = "NOT_THIS_RUN"' + CRLF + A09b,
    "selo: o arquivo do pilar so vale se for o desta rodada (NOT_THIS_RUN).")
A10 = '    t = t.replace("' + BS + BS + 'bTGL", "β_TGL").replace("' + BS + BS + 'Msun", "M_sol")' + CRLF
add("W10_txt_milhar_e_porcento", "G_ARTIGO", A10, A10 + '    t = t.replace("' + BS + BS + ',", "' + BS + 'u2009").replace("' + BS + BS + '%", "%")   # v384 AO LADO (afericao 2, achado 47): o espaco fino e o por cento no TXT' + CRLF,
    "TXT: \\, vira espaco fino e \\% vira %.")
_tabs = T.count(TAB + "exttt{evidence")
assert _tabs == 2, ("o TAB da v376 nao esta onde a afericao disse", _tabs)
for _ln in [l for l in T.split(CRLF) if (TAB + "exttt{evidence") in l]:
    assert _ln.lstrip().startswith(("r\"", "s.append(r\"", "(r\"")) or ' r"' in _ln or '(r"' in _ln, "o TAB nao esta numa string crua: " + _ln[:120]
T = T.replace(TAB + "exttt{evidence", BS + "texttt{evidence")
patches.append({"id": "W11_tab_da_v376", "grupo": "G_ARTIGO", "old": TAB + "exttt{evidence", "new": BS + "texttt{evidence",
                "o_que_muda": "ERRATA AO LADO (gerencia, em nome proprio): na errata E7 da v376, um TAB no lugar de \\t fazia o PDF mostrar 'exttt'; agora \\texttt (PT e EN)."})
for p in patches:
    if p["grupo"] == "G_ARTIGO":
        continue
    nw = p["new"]
    assert not re.search(r"(?<!NOT_)(?<!UN)CONFIRMED", nw.replace("NOT_FALSIFIED", "").replace("NOT_A_CONFIRMATION", "")), (p["id"], "CONFIRMED")
    assert not re.search(r"(?<!AP)PROVED_BY|TGL_PROVED", nw), (p["id"], "PROVED_BY")
ast.parse(T)
_vals = {}
for _l in T.split(CRLF):
    for _nm in ("_QP_WORKER_SRC = ", "_QP_SPEC_JSON = "):
        if _l.startswith(_nm):
            _vals[_nm] = ast.literal_eval(_l[len(_nm):])
assert _vals.get("_QP_WORKER_SRC = ", "").encode("utf-8") == WSRC_B and _vals.get("_QP_SPEC_JSON = ") == SPEC_CANON, "o texto embutido NAO volta exato do candidato final"
out = os.path.join(HERE, "um_v384_candidato_ENSAIO.py" if ENSAIO else "um_v384_candidato.py")
b = T.encode("utf-8")
open(out + ".tmp", "wb").write(b); assert os.path.getsize(out + ".tmp") == len(b); os.replace(out + ".tmp", out)
h16 = hashlib.sha256(b).hexdigest()[:16]
man = {"candidato": out, "ensaio": ENSAIO, "ratificacao_do_operador": RAT, "sha16": h16, "bytes": len(b), "base_v383_sha16": SHA0, "spec_sha256": SPEC_SHA, "worker_sha256": WSHA, "prereg_sha256": PR_SHA,
       "patches": [{k: p[k] for k in ("id", "grupo", "o_que_muda")} for p in patches], "kernel": "o MESMO da v383 (nenhuma pedra nova)"}
_mp = os.path.join(HERE, "CANDIDATO_v384_ENSAIO.json" if ENSAIO else "CANDIDATO_v384.json")
open(_mp + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(_mp + ".tmp", _mp)
print(json.dumps(man, ensure_ascii=False, indent=1))
