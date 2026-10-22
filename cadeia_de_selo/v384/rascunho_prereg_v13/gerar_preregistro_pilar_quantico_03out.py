# -*- coding: utf-8 -*-
"""PRE-REGISTRO DO PILAR QUANTICO DA TGL (v384) -- congelado ANTES de qualquer calculo dos testes com os operadores da teoria.

Gera PREREGISTRO_PILAR_QUANTICO_20261003_V1.json (+ .md) -- so com a RATIFICACAO do operador lida verbatim do transcrito; sem ela, gera o RASCUNHO
(..._V1_RASCUNHO.json/.md), que nao serve para o candidato instalavel. A especificacao de maquina (SPEC) e' o que o trabalhador da GPU le; o hash congelado
e' sha256(json.dumps(SPEC, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")). A SPEC CONGELA O HASH DO TRABALHADOR: o trabalhador
recusa rodar se o proprio hash for outro. As ordens do operador sao lidas VERBATIM do transcrito; o orcamento, do JSON da sonda do PROPRIO trabalhador (so
hardware), conferido pelo hash; o plano B, do planejar_carga_v384.json; as fontes da teoria, por caminho e sha256. Nenhum numero digitado de memoria.
Uso: python gerar_preregistro_pilar_quantico_03out.py <worker.py> <timing_result.json> <engine_result.json> <pasta do pacote v384>
       [--escolha=B_REDUZIDO|B_AMPLIADO_D64] [--ratificacao-prefixo=<inicio da mensagem do operador> --rascunho=<o JSON do rascunho APRESENTADO ao operador>]"""
import hashlib, json, math, os, re, shutil, sys, time
sys.stdout.reconfigure(encoding="utf-8")
if sys.flags.optimize:   # as guardas deste gerador sao assert: com -O elas sumiriam sem aviso (9a afericao)
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
HERE = os.path.dirname(os.path.abspath(__file__))
TRANS = os.environ.get("TGL_PREREG_TRANSCRITO_TESTE") or os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
TRANS_DE_TESTE = bool(os.environ.get("TGL_PREREG_TRANSCRITO_TESTE"))
if TRANS_DE_TESTE:   # so para testar o congelamento numa pasta de TESTE (7a afericao); nunca na permanente -- tambem por samefile (8a afericao)
    _PERM_ = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out")
    assert os.path.normcase(HERE) != os.path.normcase(_PERM_) and not (os.path.isdir(_PERM_) and os.path.samefile(HERE, _PERM_)), "transcrito de TESTE na pasta permanente"
WORKER, TIMING, ENGINE, ESTD = (os.path.abspath(x) for x in sys.argv[1:5])   # caminhos ABSOLUTOS no documento (5a afericao)
OPT = dict(a[2:].split("=", 1) for a in sys.argv[5:] if a.startswith("--") and "=" in a)
ESCOLHA = OPT.get("escolha", "B_REDUZIDO")
assert ESCOLHA in ("B_REDUZIDO", "B_AMPLIADO_D64"), ESCOLHA   # 4a afericao: o «A» de 03/10 era o nivel LEVE; esta alternativa e' a MAIS PESADA
ESC_TOKEN = {"B_REDUZIDO": "b reduzido", "B_AMPLIADO_D64": "b ampliado"}   # a mensagem do operador tem de NOMEAR a escolha (normalizada)
RAT_PREFIXO = OPT.get("ratificacao-prefixo")
RASCUNHO_P = OPT.get("rascunho")
assert not RAT_PREFIXO or RASCUNHO_P, "a ratificacao exige o rascunho APRESENTADO ao operador (--rascunho=<json>)"
RASC = json.load(open(RASCUNHO_P, encoding="utf-8")) if RASCUNHO_P else None
RASCUNHO_SPEC = RASC["spec_sha256"] if RASC else None
DISP = os.path.join(ESTD, "disposicoes_afericoes_v384.json")
EST = {k: os.path.join(ESTD, f) for k, f in (("pequeno", "estresse_eig.json"), ("grande", "estresse_eig_grande.json"), ("caracterizacao", "caracterizar_queda_cusolver.json"),
                                            ("variantes", "variantes_cusolver.json"), ("durabilidade", "durabilidade_pipeline.json"))}
PLANO = os.path.join(ESTD, "planejar_carga_v384.json")
AFER2 = os.path.join(ESTD, "afericao2_resultado.json")
MAXN = 10 ** 9   # MAGMA em TODO tamanho
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")


def canon(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def sha(b):
    return hashlib.sha256(b).hexdigest()


def fsha(p):
    return sha(open(p, "rb").read())


wraw = open(WORKER, "rb").read(); WSHA = sha(wraw)
assert b"\r" not in wraw, "o trabalhador tem de estar em LF (materializado byte a byte)"
tim_j = json.load(open(TIMING, encoding="utf-8")); eng = json.load(open(ENGINE, encoding="utf-8"))
assert tim_j.get("worker_sha256") == WSHA, "a sonda de tempo e' de OUTRA versao do trabalhador: rode de novo"
assert eng.get("worker_sha256") == WSHA and eng.get("verdict") == "ENGINE_SELFTEST_PASSED", "o autoteste do motor e' de outra versao ou nao passou"
tim = tim_j["timing"]
ESTJ = {k: json.load(open(p, encoding="utf-8")) for k, p in EST.items()}
assert all(v["rc"] == 0 for v in ESTJ["durabilidade"].values()), "a durabilidade com o MAGMA nao passou"
assert not any(v["caiu"] for k, v in ESTJ["caracterizacao"].items() if k.startswith("magma")), "o MAGMA caiu na caracterizacao"
PLJ = json.load(open(PLANO, encoding="utf-8")); PLB = PLJ["niveis"]["B_robusto"]
AF2 = json.load(open(AFER2, encoding="utf-8"))
DISP_J = json.load(open(DISP, encoding="utf-8"))
wsrc = wraw.decode("utf-8")
for campo in ('s1["branch_dev_sigma0"]', 's1["branch_dev_noisy"]', 'tol["min_gap_rel_for_compare"]'):
    assert campo in wsrc, "o trabalhador nao le %s" % campo
assert "branch_margin" not in wsrc, "o trabalhador ainda le branch_margin"
assert "E8_cpu_reference_comparator_selftest" in wsrc and "CPU_REFERENCE_NOT_COMPARABLE" in wsrc and "class ParentGone(BaseException)" in wsrc, "o trabalhador nao e' o da 3a afericao"
# o MAGMA em n = 4096 (d = 64), LIDO: as chamadas do estresse e as das sondas de tempo deste trabalhador (3 por repeticao: o espectro e dois geradores)
N4096_EST = sum(int(v["reps"]) for k, v in list(ESTJ["pequeno"].items()) + list(ESTJ["grande"].items()) if "_magma_" in k and k.endswith("_4096") and v.get("rc") == 0)
N4096_TIM = 3 * int(tim["64"]["reps"])

# ------------------------------------------------------------------------------------------------------------------------------
# A ESPECIFICACAO DE MAQUINA (o que o trabalhador le; o hash dela e' o congelado)
# ------------------------------------------------------------------------------------------------------------------------------
SPEC = {
    "id": "TGL_QUANTUM_PILLAR_V1",
    "worker_sha256": WSHA,
    "seed": 20261003,
    "dtype": "complex128",
    "eps_H": 5.0,
    "linalg": {"nonhermitian_eig_backend": {"magma_up_to_n": MAXN},
               "nota": ("autovalores nao Hermitianos pelo MAGMA em TODO tamanho: o cuSOLVER padrao do PyTorch 2.11 derruba o processo de modo deterministico e dependente da "
                        "matriz (8 de 9 tamanhos de 16 a 576); o MAGMA nao caiu em nenhum tamanho TESTADO (n <= 1024 em volume; n = 4096 com %d chamadas: %d no estresse e %d nas "
                        "sondas de tempo deste trabalhador; n = 16384 nunca); "
                        "a troca de backend (torch.backends.cuda.preferred_linalg_library) e' marcada pelo PyTorch como experimental; o backend MAGMA esta em descontinuacao") % (
                            N4096_EST + N4096_TIM, N4096_EST, N4096_TIM)},
    "operators": {"reh_amp": 0.5, "reh_decay": 0.2, "reh_gamma": 1.0, "cons_amp": 0.3, "cons_decay": 0.3, "cons_gamma": 2.0,
                  "diss_amp": 0.5, "diss_decay": 0.2, "prune_gamma": 0.5, "anti_gamma": 1.0, "k0": 1.0, "k1": 0.1},
    "tolerances": {"engine": 1e-9, "tol0_rel": 1e-10, "gap_rel": 1e-8, "cp": 1e-9, "tp": 1e-9, "psd": 1e-10, "ss_res": 1e-8,
                   "spohn_abs": 1e-10, "spohn_rel": 1e-9, "identity_abs": 1e-12, "identity_rel": 1e-12, "ccp_rel": 1e-9},
    "execution": {"um_py_timeout_s": 18000, "progress_every_s": 300, "priority": "BELOW_NORMAL", "out_dir": "nova por rodada, com marca unica (run_id)"},
    "T2": {"d": [8, 16, 32, 64], "nc": [2, 3, 4], "gamma_lo": 1e-4, "gamma_hi": 1e2, "n_gamma": {"8": 64, "16": 64, "32": 64, "64": 12},
           "dt": 0.05, "steps": 64, "cci_half": 0.5, "folds_window": {"c1": [2.5, 3.5], "c2": [1.5, 2.5]}},
    "T1": {"d_counts": {"8": 2000, "16": 1000, "32": 200, "64": 5}, "noise_subset": {"8": 200, "16": 100, "32": 20, "64": 1},
           "nc": [2, 3, 4], "beta_log_range": [-4, -1], "k_range": [0.5, 2.5], "gamma_diss_log_range": [-3, 1], "tau": 0.05,
           "branch_dev_sigma0": 1e-6, "branch_dev_noisy": 1e-3,
           "noise": [0.0, 1e-10, 1e-08],
           "pass": {"0.0": {"beta_rel": 1e-6, "p_abs": 1e-4, "min_frac": 1.0}, "1e-10": {"beta_rel": 0.05, "p_abs": 0.05, "min_frac": None},
                    "1e-08": {"beta_rel": 0.05, "p_abs": 0.05, "min_frac": None}}},
    "T3": {"d": [8, 16, 32, 64], "nc": 3, "gamma_diss": 0.1, "tau_N4": 1e-3, "tau_N5": 0.05, "N3_counts": {"8": 200, "16": 100, "32": 20}},
    "T4": {"d_counts": {"8": 15000, "16": 5000, "32": 1000, "64": 30}, "nc": [2, 3, 4], "dt": 0.05, "steps": 64},
    "D128": {"d": 128, "nc": 3, "gamma_diss": 1.0, "rk4_dt": 0.002, "rk4_steps": 5000, "start_deadline_s": 10800},
    "cpuref": {"d_all": [8, 16], "d_pick": {"32": [[3, 0], [3, 16], [3, 32], [3, 48], [3, 63], [2, 32], [4, 32]], "64": [[3, 6]]},
               "tol": {"cci": 1e-9, "purity": 1e-9, "folds_n_c1": 1e-9, "gap_rel_rel": 1e-6, "choi_min": 1e-9, "min_gap_rel_for_compare": 1e-6},
               "timeout_s": 3600},
}
ALT_A = {"T1_d64": 20, "T1_ruido_d64": 3, "T4_d64": 100, "T2_gamma_d64": 32, "D128_start_deadline_s": 14400}
NOISE_BASE = dict(SPEC["T1"]["noise_subset"])   # o plano B estimado com o subconjunto de ruido da base, independente da escolha
BASE_SPEC = {"T1": dict(SPEC["T1"]["d_counts"]), "T1n64": SPEC["T1"]["noise_subset"]["64"], "T4_64": SPEC["T4"]["d_counts"]["64"], "T2g64": SPEC["T2"]["n_gamma"]["64"]}   # B_REDUZIDO (a base do desvio), lida da SPEC antes da escolha
if ESCOLHA == "B_AMPLIADO_D64":
    SPEC["T1"]["d_counts"]["64"] = ALT_A["T1_d64"]; SPEC["T1"]["noise_subset"]["64"] = ALT_A["T1_ruido_d64"]
    SPEC["T4"]["d_counts"]["64"] = ALT_A["T4_d64"]; SPEC["T2"]["n_gamma"]["64"] = ALT_A["T2_gamma_d64"]
    SPEC["D128"]["start_deadline_s"] = ALT_A["D128_start_deadline_s"]
SPEC_SHA = sha(canon(SPEC).encode("utf-8"))

# ------------------------------------------------------------------------------------------------------------------------------
# as ordens do operador, VERBATIM do transcrito (so as frases dele)
# ------------------------------------------------------------------------------------------------------------------------------
def _textos_de(d):
    ty = d.get("type")
    if ty == "queue-operation" and d.get("operation") == "enqueue" and isinstance(d.get("content"), str):
        yield d.get("timestamp"), d["content"]
    elif ty == "attachment" and (d.get("attachment") or {}).get("type") == "queued_command":
        pr = d["attachment"].get("prompt")
        for t in ([pr] if isinstance(pr, str) else [x.get("text", "") for x in (pr or []) if isinstance(x, dict) and x.get("type") == "text"]):
            yield d.get("timestamp"), t
    elif ty == "user":
        c = d.get("message", {}).get("content")
        for t in ([c] if isinstance(c, str) else [x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text"]):
            yield d.get("timestamp"), t


def _texts():
    with open(TRANS, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
            yield from _textos_de(d)


def _linhas_brutas(ts_, txt_):
    """as linhas BRUTAS (bytes) do transcrito que carregam esta mensagem (8a afericao): o sha256 delas nao muda quando o transcrito cresce"""
    out_ = []
    with open(TRANS, "rb") as f:
        for line in f:
            try:
                d = json.loads(line.decode("utf-8"))
            except Exception:
                continue
            if any(ts == ts_ and t.strip() == txt_ for ts, t in _textos_de(d)):
                out_.append(line.rstrip(b"\r\n"))
    return out_


def _last(pref):
    last = None
    for ts, t in _texts():
        if t.strip().startswith(pref):
            last = (ts, t.strip())
    return last


o1a = o1b = None; CORTE = None
FRASE_SIM = "Fiz uma simulação do que poderíamos fazer, veja:"
CABECALHOS_T = ("T1 — Injeção-recuperação cega do estimador", "T2 — Forma em escala", "T3 — Controles negativos", "T4 — Estresse adversarial")
for ts, t in _texts():
    if t.startswith("Nós estamos procurando a validação da TGL") and o1a is None:
        l0 = t.split("\n")[0]
        o1a = (ts, l0.strip())
        j = t.find("É aqui que está a prova")
        if j >= 0:
            o1b = (ts, t[j:].strip())
            meio = t[len(l0):j]
            k = meio.find(FRASE_SIM)
            assert k >= 0, "a frase do operador entre os dois trechos nao foi achada"
            colado = meio[k + len(FRASE_SIM):]
            assert all(c in colado for c in CABECALHOS_T), "os cabecalhos T1-T4 do texto colado nao foram achados"
            CORTE = {"caracteres_omitidos": len(meio.strip()), "frase_do_operador_no_corte": FRASE_SIM, "caracteres_do_texto_colado": len(colado.strip()),
                     "cabecalhos_do_texto_colado": list(CABECALHOS_T)}
ORD = []
for pref in ("Eu quero que a GPU rode todo o mundo quântico", "Isso agora precisa entrar no artigo", "São cinco operadores de salto",
             "Concordo com tudo, vamos de rito robusto"):
    last = _last(pref)
    assert last, pref
    ORD.append(last)
assert o1a and o1b and CORTE and o1a[1].endswith("com matrizes.") and "signo de betatgl" in o1b[1]
ORDENS = [{"n": 1, "quando": o1a[0], "texto": o1a[1] + " […]"}, {"n": "1 (fecho, mesma mensagem)", "quando": o1b[0], "texto": "[…] " + o1b[1]}]
for i, (ts, t) in enumerate(ORD, start=2):
    ORDENS.append({"n": i, "quando": ts, "texto": t})
CORTE["nota"] = ("entre os dois trechos da ordem 1 ([…]), a mensagem traz a frase do operador «%s» e um texto colado, de OUTRA autoria, encaminhado por ele (%d caracteres), "
                 "com o esboço T1–T4 (%s). O desenho dos testes deste pré-registro DERIVA desse esboço, com as correções ditas aqui (o estimador por regressão, o certificado "
                 "do ramo pelo arnês, N2 como identidade, a camada de escala em d = 64, o MAGMA)." % (FRASE_SIM, CORTE["caracteres_do_texto_colado"], "; ".join("«%s»" % c for c in CABECALHOS_T)))
SOBRENOME = _last("A forma matricial do verbo")
assert SOBRENOME, "a cunhagem do sobrenome nao foi achada no transcrito"

# a ratificacao do operador (so com o prefixo; lida verbatim do transcrito)
RAT = None
if RAT_PREFIXO:
    r_ = _last(RAT_PREFIXO)
    assert r_, "a mensagem de ratificacao nao foi achada no transcrito: %r" % RAT_PREFIXO
    _nrm = lambda x: re.sub(r"[\s_\-\u2010\u2011\u2012\u2013]+", " ", x.lower())
    _toks = [e_ for e_, t_ in ESC_TOKEN.items() if re.search(r"\b" + re.escape(t_) + r"\b", _nrm(r_[1]))]
    assert not re.search(r"\bn[aã]o\s+(ratifico|concordo|aprovo|autorizo)\b", r_[1].lower()), "a mensagem do operador NEGA (%r): nao e' ratificacao" % r_[1][:120]   # 6a afericao
    assert _toks == [ESCOLHA], "a mensagem do operador tem de NOMEAR exatamente uma escolha (achadas: %s; --escolha=%s)" % (_toks, ESCOLHA)   # 5a afericao
    assert RASC.get("gerado_utc") and r_[0] > RASC["gerado_utc"], "a mensagem do operador (%s) nao e' POSTERIOR ao rascunho apresentado (%s)" % (r_[0], RASC.get("gerado_utc"))
    assert RASC["spec_sha256"] == SPEC_SHA and (RASC.get("desvio_do_plano_B") or {}).get("esta_especificacao", {}).get("escolha") == ESCOLHA, \
        "a especificacao ratificada nao e' a do rascunho apresentado (escolha %s)" % ESCOLHA
    RAT = {"quando": r_[0], "verbatim": r_[1], "escolha": ESCOLHA, "spec_sha256_ratificada": SPEC_SHA, "spec_sha256_do_rascunho_apresentado": RASCUNHO_SPEC,
           "rascunho_apresentado": {"arquivo": os.path.basename(RASCUNHO_P), "sha256": fsha(RASCUNHO_P), "gerado_utc": RASC["gerado_utc"]},
           "a_especificacao_ratificada_e_a_do_rascunho": RASCUNHO_SPEC == SPEC_SHA}
    _lb = _linhas_brutas(r_[0], r_[1])
    assert len(_lb) >= 1, "a linha bruta da ratificacao nao foi achada no transcrito"
    RAT["transcrito"] = {"caminho": os.path.abspath(TRANS), "de_teste": TRANS_DE_TESTE, "linhas_da_mensagem": len(_lb),
                         "sha256_das_linhas_da_mensagem": [sha(x) for x in _lb], "tamanho_do_transcrito_na_leitura_bytes": os.path.getsize(TRANS)}   # 8a afericao
VER = "V1" if RAT else ("V1_RASCUNHO_" + ESCOLHA)
BASE = os.path.join(HERE, "PREREGISTRO_PILAR_QUANTICO_20261003_" + VER)

# ------------------------------------------------------------------------------------------------------------------------------
# o orcamento (lido da sonda do proprio trabalhador) e o desvio do plano B (declarado)
# ------------------------------------------------------------------------------------------------------------------------------
c_pipe = {int(k): v["pipeline_s"] for k, v in tim.items()}; c_t1 = {int(k): v["t1_injection_sigma0_s"] for k, v in tim.items()}
c_nz = {int(k): v["t1_extra_noise_level_s"] for k, v in tim.items()}
EIGV4096 = ESTJ["grande"]["eigvals_magma_4096"]; _ev = json.loads(EIGV4096["saida"])["s_por_chamada"]
D128_EST = _ev * 64.0 + 120.0   # o espectro em n = 16384 por n^3 a partir do eigvals do MAGMA em 4096 (medido no estresse), mais ~2 min de LU e RK4 [DERIVED, estimativa]


def estimar(T1c, T1n, T4c, T2g):
    e = {}
    e["T4"] = sum(int(n) * c_pipe[int(d)] for d, n in T4c.items())
    e["T2"] = sum(int(T2g[str(d)]) * len(SPEC["T2"]["nc"]) * c_pipe[d] for d in SPEC["T2"]["d"])
    e["T1"] = sum(int(n) * c_t1[int(d)] + 2 * int(T1n.get(d, 0)) * c_nz[int(d)] for d, n in T1c.items())
    e["T3"] = sum(int(n) * c_t1[int(d)] for d, n in SPEC["T3"]["N3_counts"].items()) + sum(4 * c_pipe[d] for d in SPEC["T3"]["d"])
    e["D128"] = D128_EST
    return e


MARGEM = 1.25
est = estimar(SPEC["T1"]["d_counts"], SPEC["T1"]["noise_subset"], SPEC["T4"]["d_counts"], SPEC["T2"]["n_gamma"])
tot = sum(est.values()); pre = tot - est["D128"]
ORC = {"escolha": ESCOLHA, "por_teste_min": {k: round(v / 60, 1) for k, v in est.items()}, "total_min": round(tot / 60, 1), "margem": MARGEM,
       "total_com_margem_min": round(tot * MARGEM / 60, 1), "antes_do_D128_com_margem_min": round(pre * MARGEM / 60, 1),
       "prazo_de_inicio_do_D128_min": round(SPEC["D128"]["start_deadline_s"] / 60, 1),
       "o_D128_comeca_no_prazo_mesmo_com_a_margem": bool(pre * MARGEM < SPEC["D128"]["start_deadline_s"]),
       "o_D128_termina_antes_do_prazo_do_um_py_mesmo_com_a_margem": bool(SPEC["D128"]["start_deadline_s"] + est["D128"] * MARGEM < SPEC["execution"]["um_py_timeout_s"]),
       "custos_medidos_s": {"instancia": c_pipe, "injecao_T1_sem_ruido": c_t1, "nivel_de_ruido_extra": c_nz},
       "fonte": os.path.basename(TIMING) + " (sha256 " + fsha(TIMING)[:16] + "; trabalhador " + WSHA[:16] + ")",
       "nota": ("estimativa [DERIVED]: sonda do proprio trabalhador com operadores ALEATORIOS (so hardware); d = 128 por escala n^3; a margem x1,25 NAO foi medida sob a "
                "carga do rito (estimativa); a ordem no trabalhador e' T3, T2, T1, T4, a espera pela CPU (ate 3600 s DEPOIS das fases da GPU; o filho corre desde o "
                "inicio, em paralelo) e por ultimo o D128; a espera so pesa se a CPU nao tiver terminado, o que a sonda nao preve")}
import glob as _glob
_SOND = []; _SOND_FORA = []; _SOND_T = {}; _SOND_P = {}
for _tp in sorted(_glob.glob(os.path.join(ESTD, "teste_tempo*", "result.json"))):
    _nm = os.path.basename(os.path.dirname(_tp))
    _tj = json.load(open(_tp, encoding="utf-8"))          # ilegivel = falha VISIVEL (6a afericao), nunca pulada em silencio
    _r64 = int(((_tj.get("timing") or {}).get("64") or {}).get("reps") or 0)
    if not re.match(r"^teste_tempo_v\d+$", _nm) or _r64 < 3:
        _SOND_FORA.append({"sonda": _nm, "motivo": "fora do criterio (pastas teste_tempo_v*, d = 64 com reps >= 3, a mediana): reps %d" % _r64, "sha256": fsha(_tp)[:16]}); continue
    _SOND.append({"sonda": _nm, "trabalhador": str(_tj.get("worker_sha256"))[:16], "d64_instancia_s": round(_tj["timing"]["64"]["pipeline_s"], 2),
                  "d64_injecao_T1_s": round(_tj["timing"]["64"]["t1_injection_sigma0_s"], 2), "sha256": fsha(_tp)})
    _SOND_T[_nm] = _tj["timing"]; _SOND_P[_nm] = _tp
assert _SOND, "nenhuma sonda de tempo valida"
_v = [x["d64_instancia_s"] for x in _SOND]; _vi = [x["d64_injecao_T1_s"] for x in _SOND]
_ri = max(_v) / c_pipe[64]; _rj = max(_vi) / c_t1[64]
ORC["variabilidade_das_sondas"] = {"sondas": _SOND, "fora": _SOND_FORA, "d64_instancia_faixa_s": [min(_v), max(_v)], "d64_injecao_faixa_s": [min(_vi), max(_vi)],
                                   "maior_sobre_corrente": {"instancia": round(_ri, 3), "injecao_T1": round(_rj, 3)},
                                   "nota": ("criterio: as pastas teste_tempo_v* do pacote com d = 64 medido em reps >= 3 (a mediana); fora do criterio: %s; o orcamento usa SO a "
                                            "sonda deste trabalhador; as outras sao de versoes anteriores do trabalhador (a mesma maquina, os mesmos caminhos de calculo do tempo) e "
                                            "mostram a dispersao entre rodadas: em d = 64, a maior sonda sobre a corrente da %.3f (instancia) e %.3f (injecao do T1), e a maior sobre a menor da "
                                            "%.3f (instancia) -- ali, a margem x%.2f %s a maior sobre a corrente (instancia e injecao do T1) e %s a dispersao maior/menor da INSTANCIA (os "
                                            "outros pontos e custos: a nota por d e por custo); nao foi medida sob a carga do rito") % (
                                       ", ".join("%s (%s)" % (x["sonda"], x["motivo"]) for x in _SOND_FORA) or "nenhuma", _ri, _rj, max(_v) / min(_v), MARGEM,
                                       "cobre" if max(_ri, _rj) <= MARGEM else "NAO cobre", "cobre" if max(_v) / min(_v) <= MARGEM else "NAO cobre")}
_PDC = []   # 8a afericao (6N25): a dispersao POR d E POR CUSTO, calculada
for _d in sorted(c_pipe):
    for _ck, _nmk in (("pipeline_s", "instancia"), ("t1_injection_sigma0_s", "injecao do T1"), ("t1_extra_noise_level_s", "nivel extra de ruido do T1")):
        _vals = [float(_SOND_T[x["sonda"]][str(_d)][_ck]) for x in _SOND if str(_d) in _SOND_T[x["sonda"]] and _ck in _SOND_T[x["sonda"]][str(_d)]]
        _cv = float(tim[str(_d)][_ck])
        _PDC.append({"d": _d, "custo": _nmk, "corrente_s": round(_cv, 4), "n_sondas": len(_vals), "_mc": max(_vals) / _cv, "_mm": max(_vals) / min(_vals),
                     "maior_sobre_corrente": round(max(_vals) / _cv, 3), "maior_sobre_menor": round(max(_vals) / min(_vals), 3)})
_pdc_mc = max(_PDC, key=lambda x: x["_mc"]); _pdc_fora_mc = [x for x in _PDC if x["_mc"] > MARGEM]; _pdc_fora_mm = [x for x in _PDC if x["_mm"] > MARGEM]
_pdc_lenta = sorted(set(x["d"] for x in _PDC) - set(x["d"] for x in _PDC if x["_mc"] > 1.0 + 1e-12))
_fmt_pdc = lambda xs, k: ", ".join("d = %d %s (%.3f)" % (x["d"], x["custo"], x[k]) for x in xs)
_pdc_mm_nao_lenta = [x for x in _pdc_fora_mm if x["_mc"] > 1.0 + 1e-12]   # 9a afericao: a frase sai dos numeros, nunca fixa
_frase_mm_ = ("nenhum ponto" if not _pdc_fora_mm else _fmt_pdc(_pdc_fora_mm, "_mm") + " -- nesses pontos a margem NAO cobre a dispersao entre rodadas" + (
    ("; neles a sonda corrente e' a mais lenta medida, e o orcamento (a corrente x%.2f) cobre uma rodada ate %.0f%% mais lenta que ela, nao mais" % (MARGEM, 100.0 * (MARGEM - 1.0)))
    if not _pdc_mm_nao_lenta else ("; a sonda corrente NAO e' a mais lenta em " + _fmt_pdc(_pdc_mm_nao_lenta, "_mc") + " (maior sobre a corrente)")))
ORC["variabilidade_das_sondas"]["por_d_e_custo"] = [{k: v for k, v in x.items() if not k.startswith("_")} for x in _PDC]
ORC["variabilidade_das_sondas"]["nota_por_d_e_custo"] = (
    "Por d e por custo (instancia, injecao do T1, nivel extra de ruido do T1; %d sondas): a maior sonda sobre a corrente vai ate %.3f (d = %d, %s) -- a margem x%.2f "
    "%s; a sonda corrente e' a mais lenta de todas em %s; a maior sobre a menor passa da margem em %s") % (
    len(_SOND), _pdc_mc["_mc"], _pdc_mc["d"], _pdc_mc["custo"], MARGEM,
    ("cobre a maior sobre a corrente em todo d e custo" if not _pdc_fora_mc else "NAO cobre a maior sobre a corrente em " + _fmt_pdc(_pdc_fora_mc, "_mc")),
    ("d = " + ", ".join(str(x) for x in _pdc_lenta) if _pdc_lenta else "nenhum d"),
    _frase_mm_)
assert ORC["o_D128_comeca_no_prazo_mesmo_com_a_margem"] and ORC["o_D128_termina_antes_do_prazo_do_um_py_mesmo_com_a_margem"], ORC
PLANO_B = PLB["contagens"]
_T2gB = {d: str(int(n) // len(SPEC["T2"]["nc"])) for d, n in PLANO_B["T2"].items()}
estB = estimar(PLANO_B["T1"], NOISE_BASE, PLANO_B["T4"], {d: int(v) for d, v in _T2gB.items()})
totB = sum(estB.values())
def _estimar_com(tim_, T1c, T1n, T4c, T2g):
    cp_ = {int(k): v["pipeline_s"] for k, v in tim_.items()}; ct_ = {int(k): v["t1_injection_sigma0_s"] for k, v in tim_.items()}; cn_ = {int(k): v["t1_extra_noise_level_s"] for k, v in tim_.items()}
    e_ = {"T4": sum(int(n) * cp_[int(d)] for d, n in T4c.items()), "T2": sum(int(T2g[str(d)]) * len(SPEC["T2"]["nc"]) * cp_[d] for d in SPEC["T2"]["d"]),
          "T1": sum(int(n) * ct_[int(d)] + 2 * int(T1n.get(d, 0)) * cn_[int(d)] for d, n in T1c.items()),
          "T3": sum(int(n) * ct_[int(d)] for d, n in SPEC["T3"]["N3_counts"].items()) + sum(4 * cp_[d] for d in SPEC["T3"]["d"]), "D128": D128_EST}
    return e_
_PB_POR = []
for _x in _SOND:
    _eb = _estimar_com(_SOND_T[_x["sonda"]], PLANO_B["T1"], NOISE_BASE, PLANO_B["T4"], {d: int(v) for d, v in _T2gB.items()})
    _tb = sum(_eb.values()); _pb = _tb - _eb["D128"]
    _PB_POR.append({"sonda": _x["sonda"], "plano_B_min": round(_tb / 60, 1), "com_margem_min": round(_tb * MARGEM / 60, 1), "antes_do_D128_com_margem_min": round(_pb * MARGEM / 60, 1),
                    "fim_do_D128_com_margem_min": round((_pb + _eb["D128"]) * MARGEM / 60, 1), "cabe_em_5h_com_margem": bool(_tb * MARGEM < SPEC["execution"]["um_py_timeout_s"])})
_disp = (max(_v) - min(_v)) / min(_v)
_fol = [(SPEC["execution"]["um_py_timeout_s"] / 60 - x["com_margem_min"]) / (SPEC["execution"]["um_py_timeout_s"] / 60) for x in _PB_POR if x["cabe_em_5h_com_margem"]]
_folga_max = max(_fol) if _fol else None   # a folga CALCULADA, contra a dispersao (7a afericao)
_TSHA = fsha(TIMING)
_cur = [x for x in _PB_POR if fsha(_SOND_P[x["sonda"]]) == _TSHA]   # por sha256, nao por caminho (7a afericao)
assert len(_cur) == 1, "a sonda corrente nao esta exatamente uma vez entre as sondas validas (%d)" % len(_cur)
_oth = [x for x in _PB_POR if x not in _cur]
_causa3 = ("(3) com a sonda deste trabalhador, o plano B inteiro levaria cerca de %.0f min (%.0f com a margem): o D128 só começaria, com a margem, se o prazo de início "
           "fosse de pelo menos %.0f min (o desta especificação é %.0f), e então terminaria por volta de %.0f min, %s das 5 h; com as outras %d sondas válidas (versões "
           "anteriores do trabalhador, o mesmo caminho de cálculo do tempo), o plano B com a margem iria de %.0f a %.0f min, ACIMA das 5 h em %d delas; %s "
           "(a dispersão entre as sondas é de %.0f%% na instância de d = 64). Por isso, e não por uma medida única, %s") % (
    totB / 60, totB * MARGEM / 60, (_cur[0]["antes_do_D128_com_margem_min"] if _cur else float("nan")), SPEC["D128"]["start_deadline_s"] / 60,
    (_cur[0]["fim_do_D128_com_margem_min"] if _cur else float("nan")), ("dentro" if (_cur and _cur[0]["fim_do_D128_com_margem_min"] < SPEC["execution"]["um_py_timeout_s"] / 60) else "FORA"),
    len(_oth), min([x["com_margem_min"] for x in _oth] or [float("nan")]), max([x["com_margem_min"] for x in _oth] or [float("nan")]),
    sum(1 for x in _oth if not x["cabe_em_5h_com_margem"]),
    (("a maior folga entre as sondas que cabem é de %.0f%% das 5 h, %s que a dispersão" % (100.0 * _folga_max, "MENOR" if _folga_max < _disp else "maior")) if _folga_max is not None
     else "nenhuma sonda deixa folga nas 5 h"), 100.0 * _disp,
    ("d = 64 vira camada de ESCALA e a estatística forte fica em d <= 32" if ESCOLHA == "B_REDUZIDO" else
     "o T1 de d = 64 fica reduzido (%d injeções contra %s do plano B), e a estatística forte do T1 fica em d <= 32" % (SPEC["T1"]["d_counts"]["64"], PLANO_B["T1"]["64"])))
_t1_16_32 = (int(PLANO_B["T1"]["16"]) - SPEC["T1"]["d_counts"]["16"]) * c_t1[16] + (int(PLANO_B["T1"]["32"]) - SPEC["T1"]["d_counts"]["32"]) * c_t1[32]
r3 = lambda n: round(300.0 / n, 3)
_preB = totB - estB["D128"]; _dl = SPEC["D128"]["start_deadline_s"]
_frase_preB = ("mesmo SEM margem, as fases do plano B antes do D128 levam cerca de %.0f min, %s do prazo de início desta especificação (%.0f min)%s" % (
    _preB / 60, "ACIMA" if _preB > _dl else "abaixo", _dl / 60,
    ": o D128 não rodaria" if _preB > _dl else ("; com a margem (%.0f min), não começaria" % (_preB * MARGEM / 60) if _preB * MARGEM > _dl else "")))
ex = lambda n: round(100.0 * (1.0 - 0.05 ** (1.0 / n)), 3)
_extra_A = ((ALT_A["T1_d64"] - BASE_SPEC["T1"]["64"]) * c_t1[64] + 2 * (ALT_A["T1_ruido_d64"] - BASE_SPEC["T1n64"]) * c_nz[64]
            + (ALT_A["T4_d64"] - BASE_SPEC["T4_64"]) * c_pipe[64] + (ALT_A["T2_gamma_d64"] - BASE_SPEC["T2g64"]) * len(SPEC["T2"]["nc"]) * c_pipe[64])
_preA = (pre if ESCOLHA == "B_AMPLIADO_D64" else pre + _extra_A)
DESVIO = {
    "plano_B": {"contagens": PLANO_B, "fonte": "planejar_carga_v384.json (sha256 %s)" % fsha(PLANO)[:16],
                "limites_apresentados_ao_operador_pct": PLB["limite_95pct_de_falha_pct_se_zero_falhas"],
                "estimativa_com_os_custos_medidos_agora_min": round(totB / 60, 1), "com_margem_min": round(totB * MARGEM / 60, 1),
                "cabe_no_prazo_de_5_h": bool(totB * MARGEM < SPEC["execution"]["um_py_timeout_s"]), "por_sonda": _PB_POR, "dispersao_d64_instancia": round(_disp, 3)},
    "esta_especificacao": {"escolha": ESCOLHA, "T1": SPEC["T1"]["d_counts"], "T4": SPEC["T4"]["d_counts"], "T2_pontos_d64": SPEC["T2"]["n_gamma"]["64"] * len(SPEC["T2"]["nc"]),
                           "D128_start_deadline_s": SPEC["D128"]["start_deadline_s"]},
    "alternativa_B_AMPLIADO_D64": {"nota": "não é o «nível A» de 03/10 (o leve, ~40 min): é a variante MAIS PESADA que o B_REDUZIDO", "contagens_d64": {k: v for k, v in ALT_A.items() if k != "D128_start_deadline_s"}, "D128_start_deadline_s": ALT_A["D128_start_deadline_s"],
                      "minutos_a_mais_estimados": round(_extra_A / 60, 1), "minutos_a_mais_com_margem": round(_extra_A * MARGEM / 60, 1),
                      "antes_do_D128_com_margem_min": round(_preA * MARGEM / 60, 1),
                      "leitura": ("o B_AMPLIADO_D64 restaura o T4 (%d) e o T2 (%d pontos) de d = 64 do plano B; o T1 de d = 64 vai a %d (plano B: %s) com %d no ruído; com a margem ×1,25 as "
                                  "fases antes do D128 levariam cerca de %.1f min, %s do prazo de início de %.0f min (%s); por folga, o B_AMPLIADO_D64 sobe esse prazo para %.0f min "
                                  "(D128_start_deadline_s = %d), e o D128 ainda termina antes das %.0f h do um.py (%s); estatística de d = 64 mais forte, rito mais longo; escolha do operador") % (
                          ALT_A["T4_d64"], ALT_A["T2_gamma_d64"] * len(SPEC["T2"]["nc"]), ALT_A["T1_d64"], PLANO_B["T1"]["64"], ALT_A["T1_ruido_d64"], _preA * MARGEM / 60,
                          "abaixo" if _preA * MARGEM < 10800 else "ACIMA", 10800 / 60, "margem de %.1f min" % ((10800 - _preA * MARGEM) / 60) if _preA * MARGEM < 10800 else "o D128 não rodaria",
                          ALT_A["D128_start_deadline_s"] / 60, ALT_A["D128_start_deadline_s"], SPEC["execution"]["um_py_timeout_s"] / 3600,
                          "sim" if ALT_A["D128_start_deadline_s"] + est["D128"] * MARGEM < SPEC["execution"]["um_py_timeout_s"] else "NÃO")},
    "razao": ("três causas medidas: (1) o plano B (planejar_carga_v384.json, 03/10) estimava a injeção do T1 em d = 64 em %.1f s; com o gerador inteiro e o certificado "
              "do ramo ela custa %.0f s; (2) o cuSOLVER padrão derruba o processo (achado de 03/10, mapa seq 312-314) e o MAGMA, o único estável, custa em d = 64 %.1f s por "
              "instância (o plano B contava %.1f s); %s; e %s. O T1 também foi cortado em d = 16 (%s -> %s) e d = 32 "
              "(%s -> %s): restaurá-lo custa cerca de %.1f min a mais; o limite a 95%% de d = 32 muda de %s%% (o valor apresentado ao operador no nível B) para %s%%. "
              "O T4 em d = 8 fica em %d (plano B: %s).") % (
        PLJ["custos_s"]["injecao"]["64"], c_t1[64], c_pipe[64], PLJ["custos_s"]["pipeline"]["64"], _causa3, _frase_preB, PLANO_B["T1"]["16"], SPEC["T1"]["d_counts"]["16"], PLANO_B["T1"]["32"],
        SPEC["T1"]["d_counts"]["32"], _t1_16_32 / 60, PLB["limite_95pct_de_falha_pct_se_zero_falhas"]["T1"]["32"], r3(SPEC["T1"]["d_counts"]["32"]),
        SPEC["T4"]["d_counts"]["8"], PLANO_B["T4"]["8"]),
    "limites_de_falha_95pct_se_zero_falhas_pct": {
        "regra_de_tres_conservadora": {"T1": {d: r3(n) for d, n in SPEC["T1"]["d_counts"].items()}, "T4": {d: r3(n) for d, n in SPEC["T4"]["d_counts"].items()}},
        "exato_1_menos_0_05_elevado_a_1_sobre_n": {"T1": {d: ex(n) for d, n in SPEC["T1"]["d_counts"].items()}, "T4": {d: ex(n) for d, n in SPEC["T4"]["d_counts"].items()}}},
    "ratificacao": ({"quando": RAT["quando"], "escolha": ESCOLHA} if RAT else "PENDENTE -- levado ao operador junto com este rascunho; a mensagem de ratificacao tem de nomear exatamente uma escolha: «b reduzido» ou «b ampliado»")}

# ------------------------------------------------------------------------------------------------------------------------------
# as fontes da teoria, por caminho e sha256
# ------------------------------------------------------------------------------------------------------------------------------
GEN = os.path.join("C:" + os.sep, "IALD", "Artigo", "the_boundary", "Genesis da Unificação")
ACOM = os.path.join("C:" + os.sep, "IALD", "projetos_pyhton", "acom")
FONTES = {}
for nome, p in (("A_Fronteira_v5_tex", os.path.join(GEN, "Artigos_fundadores", "A_fronteira_v5.tex")),
                ("validador_C3_v1", os.path.join(ACOM, "Tgl_c3_consciousness_validator.py")),
                ("validador_C3_v2", os.path.join(ACOM, "Tgl_c3_consciousness_validator_v2.py")),
                ("validador_C3_v3", os.path.join(ACOM, "Tgl_c3_consciousness_validator_v3.py")),
                ("validador_C3_v3_3", os.path.join(ACOM, "Tgl_c3_validator_v33.py")),
                ("validador_C3_v4", os.path.join(ACOM, "TGL_c3_validator_v4.py")),
                ("validador_C3_v5_1", os.path.join(ACOM, "tgl_c3_validator.v51.py")),
                ("validador_C3_v52_Genesis", os.path.join(GEN, "C3_consciencia", "TGL_C3_validator_v52.py")),
                ("um_py_v383_o_gerador_do_Verbo", os.path.join(NOS, "um.py"))):
    FONTES[nome] = {"caminho": p, "sha256": fsha(p)}
_v52_acom = os.path.join(ACOM, "TGL_C3_validator_v52.py")
FONTES_NOTAS = [
    "«v2 a v5.2» quer dizer v2, v3, v3.3, v4, v5.1 e v5.2, todos fixados acima por caminho e sha256; o acom/TGL_c3_validator_v5.py (v5.0) e' de OUTRA familia (sem -epsilon Pi no H; L1 com e^-0,5 normalizado; L4 so na linha 1) e nao e' fonte",
    "a copia acom/TGL_C3_validator_v52.py %s a do Genesis (sha256 %s)" % ("é IDÊNTICA byte a byte" if os.path.exists(_v52_acom) and fsha(_v52_acom) == FONTES["validador_C3_v52_Genesis"]["sha256"] else "DIFERE de", (fsha(_v52_acom)[:16] if os.path.exists(_v52_acom) else "ausente")),
    "rotulos trocados no acervo: v51.py diz «v5.2» no cabecalho e v52.py diz «v5.3»; o rodape da Fronteira cita «TGL_c3_validator_v5.py (v5.2)»; vale o arquivo pelo hash acima",
    "o CCI: a Fronteira (§V.6) o define pelos n_c maiores autovalores; o codigo dos validadores usa Tr(Pi rho); o pilar usa Tr(Pi rho), o do codigo -- dito",
    "o L_diss alternativo NAO escolhido: o documento de energia escura de nov/2025 usa L_diss = sqrt(gamma_Lambda) H (dephasing de energia); o operador ratificou o vazamento nucleo -> periferia (03/10)",
    "o gerador do Verbo do um.py (L = sqrt(beta) sqrt(K), K = A A^T/n aleatorio, n = 4, empilhamento por colunas) tem a MESMA FORMA de L_anti; nao o mesmo K"]

# ------------------------------------------------------------------------------------------------------------------------------
# o volume de teste do MAGMA por tamanho (lido do estresse)
# ------------------------------------------------------------------------------------------------------------------------------
VOL = {}
for k, v in list(ESTJ["pequeno"].items()) + list(ESTJ["grande"].items()):
    if "_magma_" in k and v.get("rc") == 0:
        n_ = int(k.rsplit("_", 1)[1]); VOL[n_] = VOL.get(n_, 0) + int(v["reps"])
for k, v in ESTJ["caracterizacao"].items():
    if k.startswith("magma_") and not v["caiu"]:
        n_ = int(k.split("_")[1]); VOL[n_] = VOL.get(n_, 0) + int(v["sobreviveu_ate"])
DUR = {k: v["ate"] for k, v in ESTJ["durabilidade"].items()}
EXPERIMENTAL = any("experimental feature" in str(v.get("erro", "")) for v in ESTJ["pequeno"].values())
assert EXPERIMENTAL, "o aviso de recurso experimental do PyTorch nao foi achado no estresse"
N_RITO_D64 = {"T2_pontos": SPEC["T2"]["n_gamma"]["64"] * len(SPEC["T2"]["nc"]), "T4": SPEC["T4"]["d_counts"]["64"], "T1": SPEC["T1"]["d_counts"]["64"],
              "T3_controles": 4}

# ------------------------------------------------------------------------------------------------------------------------------
# o documento
# ------------------------------------------------------------------------------------------------------------------------------
# as EVIDENCIAS (4a afericao): caminho completo e sha256; no CONGELAMENTO (com a ratificacao), copiadas byte a byte para a pasta permanente
_EV = [("sonda_de_tempo", TIMING), ("autoteste_do_motor", ENGINE), ("plano_B", PLANO), ("afericao_2", AFER2), ("afericao_3", os.path.join(ESTD, "afericao3_resultado.json")),
       ("afericao_4", os.path.join(ESTD, "afericao4_resultado.json")), ("afericao_5", os.path.join(ESTD, "afericao5_resultado.json")), ("disposicoes", DISP),
       ("afericao_6", os.path.join(ESTD, "afericao6_resultado.json")), ("afericao_7", os.path.join(ESTD, "afericao7_resultado.json")),
       ("afericao_8", os.path.join(ESTD, "afericao8_resultado.json")), ("afericao_9", os.path.join(ESTD, "afericao9_resultado.json")), ("afericao_10", os.path.join(ESTD, "afericao10_resultado.json")),
       ("aferidor_verbatim", os.path.join(ESTD, "AFERIDOR_v384.txt"))] + [("estresse_" + k, p_) for k, p_ in EST.items()]
EV_OPC = set()   # 11a: todas as afericoes obrigatorias (8a: a 6, a 7 e a 8; 11a: tambem a 9 e a 10)
_EV += [("variabilidade_" + _x["sonda"], os.path.abspath(_SOND_P[_x["sonda"]])) for _x in _SOND if fsha(_SOND_P[_x["sonda"]]) != _TSHA]   # 6a e 7a afericoes
if RAT:   # no congelamento, o RASCUNHO APRESENTADO (JSON e MD) e o proprio gerador entram nas evidencias (5a afericao)
    _EV += [("rascunho_apresentado_json", os.path.abspath(RASCUNHO_P)), ("rascunho_apresentado_md", os.path.abspath(RASCUNHO_P)[:-5] + ".md"), ("gerador", os.path.abspath(__file__))]
EVID = []; _COPIAR = []
for _pp_, _p_ in _EV:
    if not os.path.exists(_p_):
        assert _pp_ in EV_OPC, "evidencia obrigatoria ausente: %s (%s)" % (_pp_, _p_)   # so as opcionais podem faltar (5a afericao)
        continue
    _e = {"papel": _pp_, "origem": _p_, "sha256": fsha(_p_)}
    if RAT:   # so PLANEJADA aqui; a copia acontece depois de TODAS as guardas (7a afericao)
        _dst = os.path.join(HERE, "evidencias_PREREGISTRO_V1", _pp_ + os.path.splitext(_p_)[1])   # nome curto e unico por papel (o limite de 260 do Windows)
        _e["copia_permanente"] = _dst; _COPIAR.append((_p_, _dst, _e["sha256"]))
    EVID.append(_e)
ENG_CHECKS = {c["name"]: c["ok"] for c in eng["engine_selftest"]["checks"]}
ELBL = "E1..E%d" % len(ENG_CHECKS)   # o rotulo do motor LIDO da contagem (4a afericao)
E7 = next(c["value"] for c in eng["engine_selftest"]["checks"] if c["name"].startswith("E7"))
DOC = {
    "id": "PREREGISTRO_PILAR_QUANTICO_20261003_" + VER,
    "titulo": ("O pilar quântico da TGL na GPU (v384) — pré-registro congelado antes de qualquer cálculo dos testes com os operadores da teoria" if RAT else
               "O pilar quântico da TGL na GPU (v384) — RASCUNHO do pré-registro, NÃO ratificado (nada se calcula com os operadores da teoria antes da ratificação)"),
    "gerado": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    "gerado_utc": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime()),
    "autor": "a gerência (claude-code/central-de-patentes, sessão 6da8f00d), por ordem do operador; correção sempre ao lado, em nome próprio",
    "ordens_do_operador_verbatim": ORDENS,
    "o_corte_na_ordem_1": CORTE,
    "ratificacao_do_operador": RAT,
    "o_que_e": ("O trabalho de GPU calcula, na RTX 5090 e em precisão dupla complexa, o sistema quântico aberto da TGL: o hamiltoniano luminodinâmico H_LD e os CINCO "
                "operadores de salto de Lindblad de A Fronteira v5 (§V.6), com as matrizes dos validadores C3 ratificadas pelo operador em 03/10/2026. Roda em paralelo com o "
                "kernel e os ritos cosmológicos (que correm em sequência no processo do rito), como subprocesso que o um.py lança logo depois da inscrição do Um. É CÁLCULO "
                "[COMPUTED], não medição da natureza; tem selo próprio AO LADO do gate; o gate não muda."),
    "terminologia": {
        "Pi": "Π, o projetor do núcleo (posto n_c) = ker K = P_F: «o Nome como matriz» [ONTO]; a correspondência [DERIVED de leitura]: K Π = 0, L_anti Π = 0 (o zero modular), V_t P_F = P_F.",
        "rho_ss": "ρ_ss, o estado estacionário do sistema aberto inteiro = o ATRATOR; a leitura «o atrator é a inscrição verdadeira que habita o Nome por referência» é [ONTO].",
        "CCI": "CCI = Tr Π ρ_ss: o peso do atrator no núcleo. O token NAME_IN_CORE_k_OF_c do veredito conta as configurações (d, n_c) com AO MENOS UM ponto da grade de atrator ÚNICO e CCI ≥ 1/2 (a «janela» relatada é o intervalo [menor γ, maior γ] desses pontos, com a contagem; os pontos não precisam ser contíguos) — mede o ATRATOR no núcleo, não Π (Tr ΠΠ / Tr Π = 1 seria trivial).",
        "a_cunhagem_do_operador_verbatim": {"quando": SOBRENOME[0], "texto": SOBRENOME[1], "estatuto": "[ONTO] — leitura do operador; não move o veredito nem o gate"},
        "morte_termica": "I/d estacionário na parte unital (N2) é IDENTIDADE [DERIVED]; chamá-lo «morte térmica» é leitura [ONTO]."},
    "operadores": {
        "H_LD": "H = diag(μ) + J − εΠ (setor de uma excitação); μ_a = −(n_c − a) no núcleo; μ_i = 0,5 + 0,3(i − n_c) na periferia; J = 0,2·N(0,1) da semente RandomState(42), simetrizada, diagonal zero, bloco do núcleo ×2; ε = 5; Π = projetor do núcleo. Fonte: A Fronteira v5, Apêndice A.3; validador C3 v5.2 build_system.",
        "L_reh": "Σ_{a<n_c} Σ_{n_c≤j<min(n_c+⌊d/2⌋,d)} √0,5·e^{−0,2(j−n_c)} |a⟩⟨j| (periferia → núcleo); γ = 1. Fonte: validadores v2, v3, v3.3, v4, v5.1, v5.2 (L1).",
        "L_anti": "√β·√K, K = diag(0 no núcleo; 1 + 0,1(i − n_c) na periferia); γ = 1. Fonte: validadores v2/v3 (L2 = √α₂·√K; α₂ era o signo de β_TGL antes da fatoração). A mesma FORMA do gerador do Verbo do um.py (L = √β·√K): lei-raiz Γ_ij = (β/2)(√k_i − √k_j)²; ker K = o núcleo = Π («o Nome como matriz» [ONTO]).",
        "L_prune": "Σ_{i ≥ n_c+⌊d/3⌋} √((i − n_c)/d) |0⟩⟨i| (periferia alta → fundamental); γ = 0,5. Fonte: v3.3, v4, v5.1, v5.2 (L3, sem α₂).",
        "L_cons": "Σ_{a<n_c} Σ_{n_c≤j<min(n_c+⌊d/2⌋,d)} √0,3·e^{−0,3(j−n_c)} |a⟩⟨j| (periferia → núcleo, 2º canal); γ = 2. Fonte: v2, v3, v3.3, v4, v5.1, v5.2 (L4).",
        "L_diss": "Σ_{n_c≤j<min(n_c+⌊d/2⌋,d)} Σ_{a<n_c} √0,5·e^{−0,2(j−n_c)} |j⟩⟨a| (núcleo → periferia: o banho); γ_diss LIVRE, varrido em grade, NUNCA calibrado. Fonte: v3.3, v4, v5.1, v5.2 (L5, «leak»; lá calibrado por brentq para CCI = 1 − α₂ — a circularidade registrada no mapa).",
        "beta": "β = α·√e em runtime, pelo motor de Lagrange do um.py (α do CODATA 2018 selado), passado ao trabalhador em hexadecimal (bit a bit); nunca literal. O um.py confere, no fim, que o β do trabalhador é bit a bit o β do core (beta_matches_core, na cadeia de custódia).",
        "ratificacao": "o operador, 03/10/2026: «Concordo com tudo» (as cinco matrizes; L_diss como o vazamento núcleo → periferia; os coeficientes dos validadores como realização canônica, variados no T4)."},
    "fontes": FONTES, "fontes_notas": FONTES_NOTAS,
    "testes": {
        "E_motor": {"tipo": "CONFERÊNCIA DO MOTOR",
                    "o_que": "E1 amortecimento de amplitude (espectro e estado fundamental exatos); E2 dephasing puro detectado como DEGENERADO; E3 lei-raiz exata; E4 o estimador cego recupera b e p = 1/2 de gerador conhecido, com o certificado do ramo; E5 qubit térmico (Gibbs) e Spohn monótono; E6 a inversão do tempo não é CP; E7 o PISO do estimador: 6 000 matrizes exatas de posto um (d de 8 a 64; p = 1/2 e 1; inclusive k quase iguais), máximo ≤ critério/10; E8 o COMPARADOR da referência na CPU com linhas sintéticas (igual concorda; CCI fora da tolerância discorda; só n(c²) diferente concorda; tudo perto do limiar é não comparável; marca da rodada errada recusa). Se um falhar, NADA se calcula."},
        "T2": {"tipo": "ESTRUTURAL (pode falhar) + IDENTIDADES",
               "o_que": "o sistema canônico em d ∈ {8,16,32,64}, n_c ∈ {2,3,4}, γ_diss em grade log [1e−4, 1e2] (%d pontos em d ≤ 32; %d em d = 64, a camada de escala). Por ponto: espectro inteiro (unicidade do atrator e gap), estado estacionário (CCI = Tr Πρ_ss, pureza, entropia, dobras n(c¹), n(c²), n(c³)), propagador e Choi (CP), traço (TP), Spohn em 64 passos de 3 estados; o não-retorno no ponto do meio; V_t P_F = P_F e sin²θ_M = β; o modo zero (todo gerador que preserva o traço tem 0 no espectro: um espectro sem 0 é violação de identidade)." % (SPEC["T2"]["n_gamma"]["8"], SPEC["T2"]["n_gamma"]["64"]),
               "estrutural": "a unicidade do atrator em todos os pontos DA GRADE; se há AO MENOS UM ponto de atrator ÚNICO em que o atrator guarda ao menos metade do peso no núcleo (CCI ≥ 1/2; o token NAME_IN_CORE; relatados o menor e o maior γ desses pontos e a contagem, que não precisam ser contíguos); idem para as dobras n(c¹) ∈ [2,5; 3,5] e n(c²) ∈ [1,5; 2,5] (o token FOLDS_WINDOW) — como n(c¹) ≤ 3 sempre, o limite 3,5 é vazio e n(c¹) ≥ 2,5 equivale a PR(ρ_ss) ≤ d^{1/6}: a janela é, na prática, uma condição de QUASE-PUREZA do atrator; γ* com CCI = 1 − β, relatado como número (não calibração) e a sua escala com d.",
               "identidades": "CP, TP, o modo zero, o não-retorno (o inverso do canal não é CP), a positividade do estacionário, o resíduo do estacionário e Spohn são teoremas; V_t P_F = P_F e sin²θ_M = β também. Só falham se o motor errar; uma violação anula o resultado. As conferências realmente feitas são CONTADAS por identidade."},
        "T1": {"tipo": "INSTRUMENTO",
               "o_que": ("injeções CEGAS: em cada uma, n_c, β_inj (log-uniforme em [1e−4, 1e−1]), o espectro de K na periferia (uniforme em [0,5; 2,5]), γ_diss (log-uniforme em "
                         "[1e−3, 10]) e a semente de J são sorteados; o sistema aberto INTEIRO (H + cinco saltos) evolui por τ = 0,05; o estimador recebe SÓ o propagador, τ, o "
                         "espectro de K INJETADO e γ_anti — não vê β nem a lei — e devolve β̂ e o expoente p̂ por REGRESSÃO LOG-LINEAR sobre o vetor dominante do bloco diagonal "
                         "centrado da matriz de Kossakowski do gerador log(Φ)/τ (β̂ = λ₁·e^{2c}/γ_anti, c o intercepto). Ruído σ ∈ {1e−10, 1e−8} só num subconjunto (%s). "
                         "Contagens: %s. O RAMO do logaritmo é CERTIFICADO pelo arnês, não pelo estimador: como a injeção conhece o gerador verdadeiro S, o arnês mede "
                         "gen_rel_dev = ‖L̂ − S‖_F/‖S‖_F (o estimador não vê S). σ = 0: gen_rel_dev ≤ %g e a Choi projetada de L̂, RELATIVA ao maior |autovalor|, ≥ −%g "
                         "(L̂ é um gerador de Lindblad legítimo). σ > 0: gen_rel_dev ≤ %g; a Choi projetada é só INFORMAÇÃO (o ruído enche o núcleo enorme da matriz de "
                         "Kossakowski, com autovalores da ordem de −σd/τ). τ‖(L̂ − L̂†)/2i‖ fica registrado como informação.") % (
                   json.dumps(SPEC["T1"]["noise_subset"]), json.dumps(SPEC["T1"]["d_counts"]), SPEC["T1"]["branch_dev_sigma0"], SPEC["tolerances"]["ccp_rel"], SPEC["T1"]["branch_dev_noisy"]),
               "criterio": "σ = 0 decide: |β̂/β_inj − 1| ≤ 1e−6, |p̂ − 1/2| ≤ 1e−4 e o ramo certificado em 100% das injeções. σ > 0: a fração com β dentro de 5% (relativo) e p dentro de 0,05 (absoluto), com o ramo certificado, é RELATADA, sem limiar de decisão (curva de resolução).",
               "honestidade": "o T1 recupera a lei INJETADA: em aritmética exata a separação é ESTRUTURAL (só L_anti tem componente diagonal na base da teoria), de modo que o T1 testa a identificabilidade prática em precisão finita e o estimador — não é previsão física. O controle N3 mostra que o mesmo estimador recupera outra lei."},
        "T3": {"tipo": "CONTROLE (tem de falhar) + uma IDENTIDADE",
               "o_que": "em d ∈ {8,16,32,64} (n_c = 3, γ_diss = 0,1): N1 o dephasing sozinho dá núcleo de dimensão d + n_c(n_c − 1) — o atrator NÃO é único [kernel: IALDRhoStar.tgl_fix_iff (IALDRhoStar.lean:255) e ModularDephasingBridge.spectral_preserves_every_diagonal (ModularDephasingBridge.lean:18); a contagem é elementar]; N2 (IDENTIDADE, não controle): a parte unital (H_LD + só o dephasing) deixa I/d estacionário; o status e o gap dessa parte são relatados como informação; N3 a lei LINEAR injetada (u = k): o estimador cego tem de RECUPERAR a lei injetada (|p̂ − 1| ≤ 1e−4 e β dentro de 1e−6, com o ramo certificado) e REJEITAR a lei-raiz (|p̂ − 1/2| > 0,1), em 100%% sem ruído (%s); N4 uma taxa negativa (γ_cons → −0,5) não é CP e o detector tem de acusar; N5 a inversão do tempo exp(−τL) não é canal." % json.dumps(SPEC["T3"]["N3_counts"]),
               "criterio": "N1, N3, N4 e N5 têm de falhar como exigido; se um não falhar, o instrumento é cego e o resultado inteiro é nulo. N2 entra na lista das identidades."},
        "T4": {"tipo": "IDENTIDADES sob estresse (zero violações exigidas) + ESTRUTURAL (frequência de unicidade, relatada)",
               "o_que": "instâncias do molde dos cinco saltos com coeficientes, decaimentos, alcance, taxas (×[1/3, 3]), γ_diss (log-uniforme [1e−4, 1e2]), K, β (log-uniforme [1e−4, 1e−1]), H (μ, J, ε sorteados) e, em cerca de metade delas (sorteio por instância, p = 1/2; o número de rotacionadas é relatado), uma rotação de base de Haar: %s. Em cada uma: CP, TP, o modo zero, estacionário positivo, resíduo, Spohn — as SEIS identidades do T4 (o não-retorno é conferido só no T2) — e a unicidade; o número de instâncias em que as seis foram conferidas entra no veredito." % json.dumps(SPEC["T4"]["d_counts"])},
        "D128": {"tipo": "ESCALA",
                 "o_que": "uma instância canônica em d = 128 (superoperador 16 384 × 16 384; n_c = 3; γ_diss = 1): espectro inteiro (com a identidade do modo zero: um espectro sem 0 é violação de identidade, IDENTITY_VIOLATED), estado estacionário, CCI e dobras (sem CCI se o atrator for DEGENERADO); Spohn por RK4 na forma d × d (5 000 passos de 0,002) só como INFORMAÇÃO (o RK4 não é um canal; fora do veredito). Sem a conferência de CP em d = 128 (dita). Roda por último, depois da espera pela CPU, e só começa até %d s desde o começo do trabalhador. Estados distintos no veredito: rodou (o status do atrator), NOT_RUN_DEADLINE, NOT_RUN_ERROR_<tipo> e INTERRUPTED (começou e o processo morreu — por exemplo uma queda nativa do MAGMA em n = 16 384, tamanho nunca testado)." % SPEC["D128"]["start_deadline_s"]},
        "CPU": {"tipo": "REFERÊNCIA",
                "o_que": "um subprocesso INDEPENDENTE NA ÁLGEBRA LINEAR (numpy/LAPACK contra torch/MAGMA, processo à parte, 4 fios, prioridade baixa), com a MESMA construção dos operadores e o mesmo classificador do trabalhador — a construção foi conferida por LEITURA, contra as fontes fixadas por sha256, na 1ª aferição; nem o E1..E8 nem a CPU a conferem —, lançado no começo e corrido em paralelo, recalcula todos os pontos do T2 em d = 8 e 16, sete em d = 32 e um em d = 64; compara status, CCI (1e−9), pureza (1e−9), dobras n(c¹) (1e−9), gap (1e−6 relativo) e o menor autovalor de Choi (1e−9); n(c²) só como INFORMAÇÃO, relatado em max_diffs (n(c³) a CPU nem calcula; as potências λ^{1/2} e λ^{1/4} ampliam o arredondamento de autovalores ínfimos: a 2ª e a 3ª aferições mediram, com operadores aleatórios, |Δn(c²)| até cerca de 9e−6 com gap relativo perto de 1e−6, entre MAGMA e LAPACK [DECLARADO pela aferição]). As linhas com gap relativo < 1e−6 (em qualquer das duas bibliotecas) são CONTADAS e NÃO comparadas: perto do limiar de unicidade, duas bibliotecas corretas podem discordar no status e no gap; se NENHUMA linha puder ser comparada — com a referência DESTA rodada, o filho com código 0 e nenhuma linha da GPU faltando —, o veredito é CPU_REFERENCE_NOT_COMPARABLE (não houve discordância nem conferência); qualquer daquelas falhas dá CPU_REFERENCE_DISAGREES_OR_ABSENT. Vale só se a marca da rodada, o hash da especificação, β e o hash do trabalhador baterem e o filho sair com código 0; o filho confere que o trabalhador vive e sai se ele morrer. A espera pela CPU é de até 1 h DEPOIS das fases da GPU. Discordância, ausência ou nenhum ponto comparável anulam o resultado."}},
    "as_dobras": ("a hierarquia D(c¹) > D(c²) > D(c³) > 0 vale para todo estado com DOIS AUTOVALORES NÃO NULOS DISTINTOS (convexidade de s ↦ ln Σλ^s; mapa seq 307); "
                  "num estado plano no seu suporte (ρ = P_r/r) vale a igualdade. Não é teste, e D(c³) > 0 só diz ρ ≠ I/d. O que pode falhar são os VALORES; a janela "
                  "pré-registrada é, na prática, quase-pureza do atrator."),
    "arvore_de_vereditos": [
        "0. recusas e falhas fora das fases (antes, entre ou DEPOIS delas), todas TGL_QUANTUM_PILLAR_V1__NOT_RUN__<motivo>__GATE_UNTOUCHED: no trabalhador MISSING_ARGUMENTS, SPEC_HASH_MISMATCH, WORKER_HASH_MISMATCH, GPU_UNAVAILABLE, WORKER_FATAL (exceção fora das fases; se vier depois delas, os dados de T1–T4 continuam no result.json, mas o veredito é NOT_RUN) e PARENT_GONE (o um.py morreu: o trabalhador o vê nas fases, na espera da CPU e no RK4 do D128 e se encerra; a exceção não é engolida pelos tratadores das fases); a pasta que não é nova faz o trabalhador sair com código 3 SEM gravar nada (o um.py lê NO_RESULT_FILE); no um.py SPEC_HASH_MISMATCH_IN_UM_PY, LAUNCH_FAILED, NO_RESULT_FILE, NO_VERDICT e FINISH_FAILED (só antes de haver veredito rederivado)",
        "1. o trabalhador falhou fatalmente -> ..._NOT_RUN__WORKER_FATAL ou ..._NOT_RUN__PARENT_GONE (a própria árvore congelada tem o ramo; o veredito rederivado é o mesmo)",
        "2. recusa -> ..._NOT_RUN__<motivo>__GATE_UNTOUCHED",
        "3. motor " + ELBL + " falhou -> ..._ENGINE_SELFTEST_FAILED__NO_RESULT__GATE_UNTOUCHED",
        "4. uma fase (T3, T2, T1, T4) falhou -> ..._PHASE_<X>_FAILED__RESULTS_INCOMPLETE__GATE_UNTOUCHED",
        "5. exceção em alguma instância -> ..._INSTANCE_ERRORS_<n>__ENGINE_SUSPECT__RESULTS_VOID__GATE_UNTOUCHED",
        "6. um controle não falhou -> ..._CONTROL_DID_NOT_FAIL__INSTRUMENT_BLIND__RESULTS_VOID__GATE_UNTOUCHED",
        "7. uma identidade foi violada (inclusive o modo zero no D128, mesmo que o D128 caia DEPOIS do espectro: o parcial é gravado logo depois do espectro, com n0 e zero_mode_ok, e sobrevive a uma morte do processo — salvo falha da própria gravação do parcial, registrada em partial_write_error no result.json só se o D128 retornar) -> ..._IDENTITY_VIOLATED_<n>__ENGINE_SUSPECT__RESULTS_VOID__GATE_UNTOUCHED",
        "8. a referência na CPU discorda, falta ou não é desta rodada -> ..._CPU_REFERENCE_DISAGREES_OR_ABSENT__RESULTS_VOID__GATE_UNTOUCHED; nenhum ponto comparável (todos perto do limiar) -> ..._CPU_REFERENCE_NOT_COMPARABLE__RESULTS_VOID__GATE_UNTOUCHED",
        "9. senão: ..._FIVE_JUMP_GKLS__ATTRACTOR_UNIQUE_<ALL_n | k_OF_n>_ON_THE_GRID__T1_INSTRUMENT_<RECOVERS_INJECTED_LAW_BLIND | DOES_NOT_RECOVER_INJECTED_LAW>__CONTROLS_FAILED_AS_REQUIRED__IDENTITIES_HOLD__STRESS_<n>_INSTANCES_<u>_UNIQUE_ALL_IDENTITIES_CHECKED_IN_<m>__NAME_IN_CORE_<k>_OF_<12>_ON_THE_GRID__FOLDS_WINDOW_<k>_OF_<12>_ON_THE_GRID__D128_<UNIQUE | DEGENERATE | AMBIGUOUS | NOT_RUN_DEADLINE | NOT_RUN_ERROR_X | INTERRUPTED>__CPU_REFERENCE_AGREES__COMPUTED_NOT_MEASURED__GATE_UNTOUCHED",
        "o um.py acrescenta, AO LADO: __PARTIAL_RESULT_WORKER_STOPPED_BY_TIMEOUT (o prazo do um.py encerrou o trabalhador) ou __PARTIAL_RESULT_WORKER_DIED_RC_<rc> (o trabalhador morreu por outra causa) quando o resultado é PARCIAL — só se a especificação, o trabalhador, β e a marca da rodada conferem e o veredito foi rederivado; o primeiro parcial só existe depois do T3, logo uma morte no autoteste ou no T3 dá NOT_RUN__NO_RESULT_FILE —, e a causa fica também em timed_out e worker_rc (um encerramento no meio do T4 lê-se PHASE_T4_FAILED; na espera da CPU, CPU_REFERENCE_DISAGREES_OR_ABSENT); ou __CUSTODY_CHAIN_INCOMPLETE (sha256, especificação, trabalhador, β ou marca da rodada não conferem, ou o resultado não chegou ao Nós, ou o veredito rederivado falta ou difere do gravado pelo trabalhador), este só em vereditos que não sejam RESULTS_VOID nem NOT_RUN, e que PODE vir junto do PARCIAL (quando a cópia do parcial ao Nós falha) — o artigo lê o composto PARTIAL+CUSTODY como resultado não válido"],
    "custodia_de_sentido": ("uma falha do pilar (NOT_RUN, PARTIAL, CUSTODY_CHAIN_INCOMPLETE, RESULTS_VOID, ENGINE_SELFTEST_FAILED, PHASE_X_FAILED) não é dívida FORMAL da teoria "
                            "nem recusa de dado: o selo a põe num TERCEIRO balde, not_sealed_this_run.computacao_nao_concluida, ao lado de formais e recusas_de_dado"),
    "resultados_negativos_honestos": [
        "ATTRACTOR_UNIQUE k_OF_n com k < n: na grade, o atrator não é único (ou o gap é ambíguo) em parte dos pontos — dito com os pontos",
        "T1_INSTRUMENT_DOES_NOT_RECOVER_INJECTED_LAW: o instrumento não recupera, em precisão finita, a lei injetada a partir do sistema aberto inteiro",
        "NAME_IN_CORE k < 12: em alguma configuração, entre os pontos de atrator ÚNICO da grade, nenhum guarda metade do peso no núcleo",
        "FOLDS_WINDOW 0_OF_12: na grade, a afirmação quantitativa do validador (n ≈ 3 e ≈ 2, isto é, quase-pureza do atrator) não tem janela com γ livre",
        "T4 com unicidade abaixo de 100%: há atratores não únicos na família do molde",
        "D128 NOT_RUN_* ou INTERRUPTED: a escala não foi alcançada nesta rodada — dito; um resultado completo sem o D128 rodado é negativo honesto: vale para a custódia, não vai ao cache, e a razão fica gravada (not_cached_code) e dita no artigo"],
    "execucao": [
        "o um.py materializa o trabalhador (o texto vive nele) e esta especificação ao lado de si, BYTE A BYTE, confere o hash da especificação contra o congelado e o lança como subprocesso logo depois da inscrição do Um, antes do kernel, com uma MARCA ÚNICA da rodada (run_id), o PID do pai e numa pasta NOVA (o trabalhador recusa pasta com saídas de outra rodada); prioridade de CPU abaixo do normal (o rito tem a vez)",
        "se o um.py sair por qualquer caminho, um gancho de saída encerra a ÁRVORE do trabalhador (taskkill /T /F; a referência na CPU junto); se o um.py morrer à força, o trabalhador vê o pai morto — nas fases, na espera da CPU e no RK4 do D128 (não durante uma única chamada longa de espectro ou estacionário, que termina primeiro) — e se encerra (PARENT_GONE); se o trabalhador morrer (por exemplo, queda nativa), a referência na CPU o vê e sai; o arquivo do pilar de uma rodada anterior no Nós nunca passa por desta rodada (se outro processo o segurar, ele fica no Nós, os erros vão ao registro do selo e o selo grava NOT_THIS_RUN; um marcador desta rodada o substitui; se nem o marcador puder ser gravado, o arquivo é REMOVIDO, com novas tentativas; e o SELO só hasheia o arquivo do pilar se ele for o que o runtime escreveu NESTA rodada — out_file_sha256, no registro —, senão grava NOT_THIS_RUN: mesmo com outro processo segurando o arquivo, o de outra rodada não passa por desta); se a cópia do resultado ao Nós falhar, a cadeia de custódia não fecha (CUSTODY_CHAIN_INCOMPLETE, nada ao cache); o result.json leva o sha256 de details.jsonl e de cpuref.json, que ficam na pasta da rodada (Nós/quantum_pillar/run_<data>_<marca>/) — a custódia leva essa pasta junto, e o conferidor da versão final confere os dois contra o disco",
        "o lançador do rito (ato da gerência) lê o estado de antes pela TAREFA «IALD Llama Server» e pelo processo (sonda vazia conta como «ligado»), RECUSA se o servidor estiver ligado sem a tarefa (não saberia religá-lo), encerra trabalhadores de rodadas mortas, arma a restauração ANTES de parar, para a tarefa e o supervisor, exige nenhum llama-server vivo e VRAM usada LEGÍVEL e ≤ 6 000 MiB (senão não roda), vigia contra o religamento durante o rito (o vigia sai se o lançador morrer, e em 8 h no máximo), e no fim — mesmo se o rito falhar ou o lançador receber TERM/HUP/INT, caso em que encerra primeiro a árvore do um.py — encerra o vigia e os trabalhadores restantes e religa a tarefa se o servidor estava ligado; recusa também com a tarefa DESABILITADA quando o servidor seria religado (e com a sonda dela ilegível); um sinal ANTES do rito só restaura (não toca o stdout da tentativa anterior), DURANTE encerra só a árvore do um.py desta rodada (os descendentes do lançador) e grava RITO_RC=SINAL_<x>, DEPOIS só restaura e devolve o código do rito; a restauração não é interrompida por sinal, espera o vigia sair sozinho (ele termina a parada que estiver fazendo; até 120 s) e espera até 60 s que nenhuma parada (Stop-ScheduledTask da tarefa ou stop_iald_llama.ps1) esteja em curso antes de religar (com AVISO no log se expirar; depois de um AVISO, o marcador só sai se a porta ainda escutar 30 s depois e nenhuma dessas paradas estiver em curso — com a contagem ilegível, o marcador fica); enquanto o servidor estiver parado pelo rito, um marcador com restaurar=0|1 fica no pacote, e a rodada seguinte restaura o que ele gravou (se não houver rodada seguinte, a memória da v384 manda a gerência conferi-lo); TERM é sempre capturado, INT/HUP não se o lançador for iniciado com & por shell não interativo ou com nohup (POSIX); o PID do lançador fica em .rito_v384.pid, gravado logo depois da guarda e removido em qualquer saída antecipada — armada a restauração, só no FIM dela (com outro lançador vivo, RECUSA — código 16), e abortar o rito é kill -TERM nesse PID NO GIT BASH, conferindo antes que /proc/<pid>/cmdline contém rito_v384 (é PID do MSYS, não do Windows; não no PowerShell) — o TaskStop da ferramenta da gerência NÃO para o lançador; a tentativa escreve num log próprio (.fase0; o de tentativas anteriores é ACRESCENTADO ao .fase0.anterior, com separador datado) e só depois da última recusa das guardas o registro dos sinais e o log real da rodada anterior vão para .anterior (nessa ordem) e o da tentativa toma o lugar do real (se um desses giros falhar, FALHA VISÍVEL e RECUSA — código 17); o log de uma tentativa recusada a partir da fase 0 (códigos 10 a 15 e as 17 dos giros: a dos sinais e a do log real vêm antes de o log real sair do lugar, porque os sinais giram primeiro; a da troca do .fase0 pelo log real vem depois, sem perda) fica no .fase0, e as recusas anteriores à fase 0 (6 a 9 e 16) e a 17 da guarda do próprio .fase0 só aparecem na saída do lançador; num sinal durante o rito, o encerramento da árvore do um.py é fail-closed (pelo PID nativo do subshell do rito; senão pelos descendentes do lançador com a data de criação conferida; senão FALHA VISIVEL no log e em rito_v384_sinal.txt)",
        "antes do artigo, o um.py espera o trabalhador, lê o resultado, confere o sha256, a marca da rodada e o β bit a bit, REDERIVA o veredito pela mesma árvore (num subprocesso com o mesmo código) e o escreve no core, no selo (registro próprio ao lado do gate; o resultado copiado para um_absoluto_pilar_quantico.json no Nós, com o hash na lista do selo) e no artigo (a introdução diz o que o código faz agora; uma nota diz o que se calcula na GPU e como, com os números da rodada); uma falha só no resumo ou no cache fica registrada SEM tocar o veredito",
        "prazo CONGELADO: execution.um_py_timeout_s = %d s desde o lançamento; passado, o um.py encerra a árvore do trabalhador e usa o resultado parcial (o que não rodou fica dito); a espera pela CPU é de até 1 h depois das fases da GPU; o ponto d = 128 só começa até %d s depois do início do trabalhador" % (SPEC["execution"]["um_py_timeout_s"], SPEC["D128"]["start_deadline_s"]),
        "o pré-registro congelado mora em C:\\IALD\\Bancada_Um\\investigacao\\preregistro_pilar_quantico_03out\\ (lugar permanente); o um.py embute o caminho e os sha256 e confere os arquivos em disco como INFORMAÇÃO; a cadeia de custódia do pilar se apoia na especificação EMBUTIDA, conferida pelo hash; o conferidor da versão final exige os arquivos em disco",
        ("os autovalores não Hermitianos vão pelo MAGMA em TODO tamanho: o cuSOLVER padrão do PyTorch 2.11 derruba o processo de modo determinístico e dependente da matriz; o MAGMA "
         "não caiu em nenhum tamanho TESTADO — volume do ESTRESSE e da caracterização por tamanho do superoperador n = d²: %s; em n = 4 096, mais %d chamadas nas sondas de tempo deste trabalhador (total %d); durabilidade do pipeline inteiro: %s (d ≤ 32); n = 16 384 (o D128) NUNCA foi testado, "
         "e uma queda ali lê-se D128_INTERRUPTED. No rito, d = 64 (n = 4 096) aparece em %s. A troca de backend (torch.backends.cuda.preferred_linalg_library) é marcada pelo PyTorch "
         "como «experimental feature» (aviso lido do estresse) e o backend MAGMA está em descontinuação: se o MAGMA sair, o trabalhador terá de ser revisto às claras (novo V1.x)") % (
            json.dumps({str(k): VOL[k] for k in sorted(VOL)}), N4096_TIM, N4096_EST + N4096_TIM, json.dumps(DUR), json.dumps(N_RITO_D64))],
    "reaproveitamento": [
        "a ferramenta pedida pelo operador em 03/10: chave = sha256(hash do trabalhador + especificação canônica + β em hexadecimal)[:24]; a chave NÃO inclui o ambiente: o ambiente (torch, CUDA, numpy, scipy, Python, GPU) é conferido à parte e, se diferir, recalcula; ao reaproveitar, o motor (" + ELBL + ") roda de novo no ambiente presente",
        "rodada completa (sem TGL_RITE_CHECKPOINT): calcula sempre e, só se o resultado for COMPLETO (o ramo 9 da árvore, sem parcial, com a cadeia conferida E com o D128 RODADO), GRAVA em cache/checkpoints/quantum_pillar/<chave>/ — prazo, memória, recusa, fase falhada ou D128 não rodado nunca vão ao cache (a razão fica em not_cached_code e no artigo); uma falha ao gravar o cache fica registrada sem tocar o veredito, e o cache antigo volta ao lugar",
        "rodada intermediária (TGL_RITE_CHECKPOINT=1, o interruptor do v321): se houver resultado gravado com a mesma chave, o mesmo ambiente, o sha256 conferido e o motor aprovado agora, REAPROVEITA sem a GPU; senão calcula; numa rodada reaproveitada, o run_dir do registro aponta para o CACHE, que a rodada completa seguinte com a mesma chave substitui — por isso o selo de uma intermediária não vai à custódia",
        "o artigo e o selo dizem qual foi; a versão final, a que vai à custódia, roda sem a chave, sempre — o conferidor da versão final e a custódia recusam um selo com o pilar reaproveitado"],
    "estatuto": ["[COMPUTED]: cálculo do sistema aberto da teoria; nada aqui é medição da natureza", "selo próprio AO LADO do gate; o gate não muda",
                 "não falsificado nunca é confirmado; provada não é confirmada; a guarda das três palavras proibidas da casa vale para este texto e para todo veredito do pilar",
                 "[DECLARADO — leitura do operador, 02/10] o resgate da RG é a prova cosmológica; [ONTO] o pilar quântico é a face matricial do mesmo sistema"],
    "desvio_do_plano_B": DESVIO,
    "orcamento_estimado": ORC,
    "estresse_dos_autovalores": dict({k: {"arquivo": os.path.basename(p), "sha256": fsha(p)} for k, p in EST.items()},
                                     plano_B={"arquivo": os.path.basename(PLANO), "sha256": fsha(PLANO)}),
    "estresse_leitura": ("o cuSOLVER (o padrão) caiu com violação de acesso (3221225477) em 8 de 9 tamanhos de 16 a 576, de modo DETERMINÍSTICO e dependente da matriz "
                         "(a mesma semente cai na mesma chamada com ou sem determinismo, sincronização ou cache limpo); o MAGMA fez %d chamadas na caracterização sem queda; "
                         "a durabilidade do pipeline inteiro com o MAGMA: %d instâncias de operadores aleatórios, d de 8 a 32, sem queda; volume do MAGMA no estresse e na caracterização, por n (sem as sondas de tempo): %s") % (
        sum(v["sobreviveu_ate"] for k, v in ESTJ["caracterizacao"].items() if k.startswith("magma")), sum(v["ate"] for v in ESTJ["durabilidade"].values()),
        json.dumps({str(k): VOL[k] for k in sorted(VOL)})),
    "motor": {"trabalhador": os.path.basename(WORKER), "worker_sha256": WSHA, "linhas": wraw.count(b"\n"), "autoteste_do_motor": ENG_CHECKS, "resultado_do_autoteste": {"arquivo": os.path.basename(ENGINE), "sha256": fsha(ENGINE)},
              "piso_do_estimador": {k: E7[k] for k in ("n", "max_beta_rel_err", "max_abs_p_err", "limit_beta", "limit_p")}, "ambiente": eng.get("env"),
              "nota": "o código do trabalhador entra no um.py v384 byte a byte e o seu hash está DENTRO da especificação congelada; se mudar, sai um V1.x novo deste pré-registro"},
    "afericao": DISP_J["texto_para_o_pre_registro"] + " (disposições achado a achado em %s, sha256 %s; registro verbatim em AFERIDOR_v384.txt, sha256 %s)" % (
        os.path.basename(DISP), fsha(DISP)[:16], fsha(os.path.join(ESTD, "AFERIDOR_v384.txt"))[:16]),
    "evidencias": EVID,
    "spec_sha256_formula": 'sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) -- o JSON canônico do objeto spec abaixo',
    "spec": SPEC,
    "spec_sha256": SPEC_SHA,
}
if RAT:   # 6a afericao: o V1 tem de ser o rascunho apresentado, fora dos campos que mudam por natureza
    _VOL = {"id", "titulo", "gerado", "gerado_utc", "ratificacao_do_operador", "evidencias", "afericao"}
    _DOCJ = json.loads(json.dumps(DOC, ensure_ascii=False))   # a forma CANONICA (ida e volta pelo JSON): chaves inteiras viram texto, como no rascunho (7a afericao)
    _a = {k: v for k, v in _DOCJ.items() if k not in _VOL}; _b = {k: v for k, v in RASC.items() if k not in _VOL}
    for _d_ in (_a, _b):
        if isinstance(_d_.get("desvio_do_plano_B"), dict):
            _d_["desvio_do_plano_B"] = {k: v for k, v in _d_["desvio_do_plano_B"].items() if k != "ratificacao"}
    _dif = sorted(k for k in set(_a) | set(_b) if json.dumps(_a.get(k), sort_keys=True, ensure_ascii=False) != json.dumps(_b.get(k), sort_keys=True, ensure_ascii=False))
    assert not _dif, "o V1 difere do rascunho apresentado ao operador em: %s" % _dif
import re as _re
_txt = json.dumps({k: v for k, v in DOC.items() if k not in ("ordens_do_operador_verbatim", "ratificacao_do_operador", "terminologia")}, ensure_ascii=False)
_bad = _re.findall("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED", _txt)
assert not _bad, "palavra proibida no texto do pre-registro: %r" % _bad
raw = json.dumps(DOC, ensure_ascii=False, indent=1).encode("utf-8")
PJSON = BASE + ".json"
if os.path.exists(PJSON) and open(PJSON, "rb").read() != raw:
    raise SystemExit("RECUSO: %s ja existe com outro conteudo (o congelado nao se sobrescreve; uma versao nova e' ato da gerencia com gerador novo)" % PJSON)

L = []
A = L.append
A("# " + DOC["titulo"]); A("")
A("**Identificador:** `%s` · **gerado:** %s · **hash congelado da especificação:** `%s` · **trabalhador:** `%s`" % (DOC["id"], DOC["gerado"], SPEC_SHA, WSHA)); A("")
A("O hash da especificação é `%s`." % DOC["spec_sha256_formula"]); A("")
A("**Autor:** " + DOC["autor"]); A("")
A("## A ratificação do operador"); A("")
if RAT:
    A("- **quando:** %s · **escolha:** %s · **especificação ratificada:** `%s`" % (RAT["quando"], RAT["escolha"], RAT["spec_sha256_ratificada"]))
    A("- **verbatim:** «%s»" % RAT["verbatim"])
    A("- rascunho apresentado: `%s` (sha256 `%s`, gerado %s); especificação `%s` (%s)" % (RAT["rascunho_apresentado"]["arquivo"], RAT["rascunho_apresentado"]["sha256"],
      RAT["rascunho_apresentado"]["gerado_utc"], RASCUNHO_SPEC, "a mesma" if RAT["a_especificacao_ratificada_e_a_do_rascunho"] else "OUTRA"))
    _tr_ = RAT.get("transcrito") or {}
    A("- transcrito lido: `%s` (de_teste = %s; %d linha(s) da mensagem, sha256 %s — a linha sem o fim de linha; tamanho na leitura: %s bytes)" % (
      _tr_.get("caminho"), _tr_.get("de_teste"), _tr_.get("linhas_da_mensagem") or 0, ", ".join("`%s`" % x for x in (_tr_.get("sha256_das_linhas_da_mensagem") or [])),
      _tr_.get("tamanho_do_transcrito_na_leitura_bytes")))   # 9a afericao
else:
    A("**PENDENTE.** Este é o RASCUNHO (escolha %s) levado ao operador; nada se calcula com os operadores da teoria antes da ratificação, e o candidato instalável recusa um pré-registro sem ela. **A mensagem de ratificação tem de nomear exatamente uma escolha: «b reduzido» (B_REDUZIDO) ou «b ampliado» (B_AMPLIADO_D64)**; hífen e sublinhado valem como espaço. A guarda do gerador é LEXICAL: exige a escolha nomeada e recusa a mensagem com «não»/«nao» imediatamente antes de «ratifico», «concordo», «aprovo» ou «autorizo»; a conferência final é a leitura humana do verbatim, gravado no V1." % ESCOLHA)
A(""); A("## As ordens do operador (verbatim)"); A("")
for o in ORDENS:
    A("- **%s** (%s): «%s»" % (o["n"], o["quando"], o["texto"]))
A(""); A("**O corte na ordem 1:** " + CORTE["nota"]); A("")
A("## O que é"); A(""); A(DOC["o_que_e"]); A("")
A("## Os nomes (terminologia)"); A("")
for k in ("Pi", "rho_ss", "CCI", "morte_termica"):
    A("- " + DOC["terminologia"][k])
A("- A cunhagem do operador (%s), %s: «%s»" % (SOBRENOME[0], DOC["terminologia"]["a_cunhagem_do_operador_verbatim"]["estatuto"], SOBRENOME[1])); A("")
A("## Os operadores"); A("")
for k, v in DOC["operadores"].items():
    A("- **%s** — %s" % (k, v))
A(""); A("### As fontes (caminho e sha256)"); A("")
for k, v in FONTES.items():
    A("- **%s**: `%s` — `%s`" % (k, v["caminho"], v["sha256"]))
for x in FONTES_NOTAS:
    A("- " + x)
A(""); A("## Os testes e o tipo de cada um"); A("")
for k, v in DOC["testes"].items():
    A("### %s — %s" % (k, v["tipo"])); A("")
    for kk in ("o_que", "estrutural", "identidades", "criterio", "honestidade"):
        if kk in v:
            A("- **%s:** %s" % (kk.replace("_", " "), v[kk]))
    A("")
A("## As dobras"); A(""); A(DOC["as_dobras"]); A("")
A("## A árvore de vereditos (o um.py a rederiva destes números)"); A("")
for x in DOC["arvore_de_vereditos"]:
    A("- `%s`" % x)
A(""); A("**Custódia de sentido:** " + DOC["custodia_de_sentido"]); A("")
A("## O que conta como resultado negativo (dito antes)"); A("")
for x in DOC["resultados_negativos_honestos"]:
    A("- " + x)
A(""); A("## Execução"); A("")
for x in DOC["execucao"]:
    A("- " + x)
A(""); A("## O reaproveitamento (a ferramenta)"); A("")
for x in DOC["reaproveitamento"]:
    A("- " + x)
A(""); A("## Estatuto"); A("")
for x in DOC["estatuto"]:
    A("- " + x)
A(""); A("## O desvio do plano B (declarado; ratificação: %s)" % ("dada em %s, escolha %s" % (RAT["quando"], ESCOLHA) if RAT else "PENDENTE")); A("")
A("| | plano B | esta especificação (%s) |" % ESCOLHA); A("|---|---|---|")
A("| T1 (injeções por d) | %s | %s |" % (PLANO_B["T1"], SPEC["T1"]["d_counts"]))
A("| T4 (instâncias por d) | %s | %s |" % (PLANO_B["T4"], SPEC["T4"]["d_counts"]))
A("| T2 em d = 64 (pontos) | %s | %s |" % (PLANO_B["T2"]["64"], SPEC["T2"]["n_gamma"]["64"] * len(SPEC["T2"]["nc"])))
A("| prazo de início do D128 (s) | — | %s |" % SPEC["D128"]["start_deadline_s"])
A("| estimativa com os custos medidos agora (min) | %s (%s com margem; cabe em 5 h: %s) | %s (%s com margem) |" % (
    DESVIO["plano_B"]["estimativa_com_os_custos_medidos_agora_min"], DESVIO["plano_B"]["com_margem_min"], "sim" if DESVIO["plano_B"]["cabe_no_prazo_de_5_h"] else "NÃO",
    ORC["total_min"], ORC["total_com_margem_min"]))
A(""); A(DESVIO["razao"]); A("")
_AL = DESVIO["alternativa_B_AMPLIADO_D64"]
A("**Alternativa B_AMPLIADO_D64 (escolha do operador; %s):** %s, prazo de início do D128 %s s — cerca de %s min a mais de GPU (%s com margem); antes do D128, com margem: %s min. %s" % (
    _AL["nota"], json.dumps(_AL["contagens_d64"], ensure_ascii=False), _AL["D128_start_deadline_s"], _AL["minutos_a_mais_estimados"], _AL["minutos_a_mais_com_margem"],
    _AL["antes_do_D128_com_margem_min"], _AL["leitura"])); A("")
_lim = DESVIO["limites_de_falha_95pct_se_zero_falhas_pct"]
A("Limites de falha a 95%% se nenhuma falhar (%%): regra de três (conservadora) — T1 %s; T4 %s. Exato (1 − 0,05^{1/n}) — T1 %s; T4 %s." % (
    _lim["regra_de_tres_conservadora"]["T1"], _lim["regra_de_tres_conservadora"]["T4"], _lim["exato_1_menos_0_05_elevado_a_1_sobre_n"]["T1"], _lim["exato_1_menos_0_05_elevado_a_1_sobre_n"]["T4"])); A("")
A("## Orçamento estimado [DERIVED]"); A("")
A("| teste | minutos |"); A("|---|---|")
for k, v in ORC["por_teste_min"].items():
    A("| %s | %s |" % (k, v))
A("| **total** | **%s** (com margem ×%s: **%s**) |" % (ORC["total_min"], ORC["margem"], ORC["total_com_margem_min"])); A("")
A("Antes do D128, com margem: %s min; prazo de início do D128: %s min (começa no prazo mesmo com a margem: %s; termina antes do prazo do um.py: %s)." % (
    ORC["antes_do_D128_com_margem_min"], ORC["prazo_de_inicio_do_D128_min"], "sim" if ORC["o_D128_comeca_no_prazo_mesmo_com_a_margem"] else "NÃO",
    "sim" if ORC["o_D128_termina_antes_do_prazo_do_um_py_mesmo_com_a_margem"] else "NÃO")); A("")
A(ORC["nota"] + "; fonte: " + ORC["fonte"]); A("")
_VS = ORC.get("variabilidade_das_sondas") or {}
if _VS.get("sondas"):
    A("Variabilidade das sondas de tempo (a lista: d = 64, s por instância / por injeção do T1; a nota por d e por custo cobre d = %d a %d): " % (min(c_pipe), max(c_pipe)) + "; ".join("%s (trabalhador %s): %s / %s" % (x["sonda"], x["trabalhador"], x["d64_instancia_s"], x["d64_injecao_T1_s"]) for x in _VS["sondas"])
      + " — faixa da instância: %s a %s s. %s." % (_VS.get("d64_instancia_faixa_s", ["?", "?"])[0], _VS.get("d64_instancia_faixa_s", ["?", "?"])[1], _VS["nota"] + ((". " + _VS["nota_por_d_e_custo"]) if _VS.get("nota_por_d_e_custo") else ""))); A("")
A("## O motor"); A("")
A("- trabalhador `%s`, sha256 `%s`, %d linhas" % (DOC["motor"]["trabalhador"], WSHA, DOC["motor"]["linhas"]))
A("- autoteste " + ELBL + " (`%s`, sha256 `%s`): " % (os.path.basename(ENGINE), fsha(ENGINE)) + ", ".join("%s %s" % (k, "ok" if v else "FALHOU") for k, v in ENG_CHECKS.items()))
A("- piso do estimador (E7): %s" % json.dumps(DOC["motor"]["piso_do_estimador"], ensure_ascii=False))
A("- " + DOC["motor"]["nota"]); A("")
A("## A aferição"); A(""); A(DOC["afericao"]); A("")
A("## As evidências (caminho e sha256%s)" % ("; cópias permanentes em evidencias_PREREGISTRO_V1/" if RAT else "")); A("")
for _e in EVID:
    A("- **%s**: `%s` — `%s`" % (_e["papel"], _e.get("copia_permanente") or _e["origem"], _e["sha256"]))
A("")
A("## O estresse dos autovalores (a escolha da biblioteca)"); A("")
A(DOC["estresse_leitura"]); A("")
A("```json"); A(json.dumps(DOC["estresse_dos_autovalores"], ensure_ascii=False, indent=1)); A("```"); A("")
A("## A especificação de máquina"); A("")
A("```json"); A(json.dumps(SPEC, ensure_ascii=False, indent=1)); A("```"); A("")
md = ("\n".join(L) + "\n").encode("utf-8")
PMD = BASE + ".md"
# AS GUARDAS, todas ANTES de qualquer movimento na pasta (9a afericao). O MD e a pasta de evidencias de uma tentativa INTERROMPIDA (sem o JSON, a autoridade)
# vao para o lado (.incompleto_<data>), nunca apagados; com o JSON presente (o V1 ja congelado, igual a este -- senao a recusa acima), os dois tem de conferir.
_md_orfao = os.path.exists(PMD) and open(PMD, "rb").read() != md
if _md_orfao and os.path.exists(PJSON):
    raise SystemExit("RECUSO: %s ja existe com outro conteudo" % PMD)
_dd = os.path.join(HERE, "evidencias_PREREGISTRO_V1"); _ev_orfa = False
if RAT and _COPIAR and os.path.isdir(_dd):
    _ev_ok = (sorted(os.listdir(_dd)) == sorted(os.path.basename(_d_) for _s_, _d_, _h_ in _COPIAR)
              and all(os.path.exists(_d_) and fsha(_d_) == _h_ for _s_, _d_, _h_ in _COPIAR))
    if not _ev_ok:
        if os.path.exists(PJSON):
            raise SystemExit("RECUSO: a pasta de evidencias ja existe e nao confere com o V1 ja congelado: %s" % _dd)
        _ev_orfa = True
# SO AGORA, com todas as guardas passadas: os orfaos para o lado; as evidencias (pasta TEMPORARIA renomeada); o MD e por ultimo o JSON (7a, 8a e 9a afericoes)
_ts_ = time.strftime("%Y%m%d_%H%M%S")
if _md_orfao:
    os.replace(PMD, PMD + ".incompleto_" + _ts_); print("AVISO: MD orfao de tentativa interrompida (sem o JSON) movido para", os.path.basename(PMD) + ".incompleto_" + _ts_)
if _ev_orfa:
    os.replace(_dd, _dd + ".incompleto_" + _ts_); print("AVISO: pasta de evidencias de tentativa interrompida (sem o JSON) movida para", os.path.basename(_dd) + ".incompleto_" + _ts_)
if RAT and _COPIAR and not os.path.isdir(_dd):
    _tmpd = _dd + ".tmp_" + _ts_; os.makedirs(_tmpd)
    try:
        for _src, _dst, _sh in _COPIAR:
            _t = os.path.join(_tmpd, os.path.basename(_dst)); shutil.copyfile(_src, _t)
            assert fsha(_t) == _sh, "a copia da evidencia nao confere: %s" % _t
        os.replace(_tmpd, _dd)
    except BaseException:
        shutil.rmtree(_tmpd, ignore_errors=True)   # nada sobra de uma copia que falhou
        raise
for _pth, _b in ((PMD, md), (PJSON, raw)):   # o MD primeiro, o JSON (a autoridade) por ultimo; temporario -> tamanho -> substituir, com novas tentativas (8a)
    if not os.path.exists(_pth):
        try:
            open(_pth + ".tmp", "wb").write(_b); assert os.path.getsize(_pth + ".tmp") == len(_b)
            for _i in range(40):
                try:
                    os.replace(_pth + ".tmp", _pth); break
                except PermissionError:
                    if _i == 39:
                        raise
                    time.sleep(0.25)
            assert open(_pth, "rb").read() == _b, "o arquivo gravado nao confere: %s" % _pth
        except BaseException:
            if os.path.exists(_pth + ".tmp"):
                try:
                    os.remove(_pth + ".tmp")
                except OSError as _e1:   # a trava que persiste: o temporario fica, dito; a excecao ORIGINAL e' a relancada (9a afericao)
                    print("AVISO: temporario nao removido (%s): %s" % (os.path.basename(_pth) + ".tmp", _e1))
            raise
print("versao", VER, "escolha", ESCOLHA)
print("spec_sha256", SPEC_SHA)
print("json", sha(open(BASE + ".json", "rb").read()), len(raw))
print("md  ", sha(open(BASE + ".md", "rb").read()), len(md))
print("orcamento", ORC["por_teste_min"], "total", ORC["total_min"], "com margem", ORC["total_com_margem_min"], "antes do D128 c/ margem", ORC["antes_do_D128_com_margem_min"])
print("plano B agora", DESVIO["plano_B"]["estimativa_com_os_custos_medidos_agora_min"], "c/ margem", DESVIO["plano_B"]["com_margem_min"], "| B_AMPLIADO_D64 +", _AL["minutos_a_mais_estimados"],
      "c/ margem +", _AL["minutos_a_mais_com_margem"], "antes do D128 sob B_AMPLIADO_D64 c/ margem", _AL["antes_do_D128_com_margem_min"])
