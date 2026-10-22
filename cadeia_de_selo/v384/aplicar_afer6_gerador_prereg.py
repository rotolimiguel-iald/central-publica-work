# -*- coding: utf-8 -*-
"""6a afericao no GERADOR DO PRE-REGISTRO:
- [13] a causa (3) do desvio do plano B e' recalculada com TODAS as sondas validas (reps >= 3) -- o plano B com a margem por sonda, o prazo de inicio do D128
  que ele exigiria, o fim, e a dispersao --, e a conclusao vem dos numeros (a folga, quando existe, e' menor que a dispersao entre sondas);
- [17][25] as sondas da variabilidade: criterio dito (pastas teste_tempo_v*, reps >= 3; as outras ficam fora com o motivo), ilegivel = falha visivel, entram nas
  EVIDENCIAS (copiadas no congelamento), e a frase «a margem cobre a faixa» e' calculada (razao maior/corrente por custo);
- [16] no congelamento, o DOC tem de ser igual ao do rascunho apresentado fora dos campos que mudam por natureza (senao, recusa, com as chaves que diferem);
- [15] a guarda recusa negacao explicita («nao ratifico/concordo/aprovo/autorizo»), e o rascunho diz que a guarda e' lexical e a conferencia final e' humana;
- [2] «nunca sobrevive» -> «nunca passa por desta rodada» (com a trava dita); [18] a causa «veredito rederivado ausente ou diferente» do CUSTODY;
- 5N5/[7] o lancador: abortar no Git Bash (PID do MSYS), o TaskStop nao para o lancador, o mata_um fail-closed.
Backup de bytes; ast."""
import ast, glob, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
bk = sorted(glob.glob(P + ".bak_antes_afer6_*"))
assert bk and open(bk[-1], "rb").read() == raw, "o backup de antes da 6a nao e' o estado corrente"
PAIRS = []
A = lambda o, n: PAIRS.append((o, n))
# [17][25] a variabilidade: criterio, falha visivel, por sonda os custos para o plano B
A('''_SOND = []
for _tp in sorted(_glob.glob(os.path.join(ESTD, "teste_tempo_v*", "result.json"))):
    try:
        _tj = json.load(open(_tp, encoding="utf-8"))
        _SOND.append({"sonda": os.path.basename(os.path.dirname(_tp)), "trabalhador": str(_tj.get("worker_sha256"))[:16], "d64_instancia_s": round(_tj["timing"]["64"]["pipeline_s"], 2),
                      "d64_injecao_T1_s": round(_tj["timing"]["64"]["t1_injection_sigma0_s"], 2), "sha256": fsha(_tp)[:16]})
    except Exception:
        pass
ORC["variabilidade_das_sondas"] = {"sondas": _SOND, "nota": ("o orcamento usa SO a sonda deste trabalhador; as outras sao de versoes anteriores do trabalhador (a mesma maquina, os mesmos "
                                   "caminhos de calculo do tempo) e mostram a dispersao entre rodadas; a margem x1,25 cobre a faixa observada, mas nao foi medida sob a carga do rito")}
if _SOND:
    _v = [x["d64_instancia_s"] for x in _SOND]
    ORC["variabilidade_das_sondas"]["d64_instancia_faixa_s"] = [min(_v), max(_v)]''',
  '''_SOND = []; _SOND_FORA = []; _SOND_T = {}; _SOND_P = {}
for _tp in sorted(_glob.glob(os.path.join(ESTD, "teste_tempo*", "result.json"))):
    _nm = os.path.basename(os.path.dirname(_tp))
    _tj = json.load(open(_tp, encoding="utf-8"))          # ilegivel = falha VISIVEL (6a afericao), nunca pulada em silencio
    _r64 = int(((_tj.get("timing") or {}).get("64") or {}).get("reps") or 0)
    if not re.match(r"^teste_tempo_v\\d+$", _nm) or _r64 < 3:
        _SOND_FORA.append({"sonda": _nm, "motivo": "fora do criterio (pastas teste_tempo_v*, d = 64 com reps >= 3, a mediana): reps %d" % _r64, "sha256": fsha(_tp)[:16]}); continue
    _SOND.append({"sonda": _nm, "trabalhador": str(_tj.get("worker_sha256"))[:16], "d64_instancia_s": round(_tj["timing"]["64"]["pipeline_s"], 2),
                  "d64_injecao_T1_s": round(_tj["timing"]["64"]["t1_injection_sigma0_s"], 2), "sha256": fsha(_tp)})
    _SOND_T[_nm] = _tj["timing"]; _SOND_P[_nm] = _tp
assert _SOND, "nenhuma sonda de tempo valida"
_v = [x["d64_instancia_s"] for x in _SOND]; _vi = [x["d64_injecao_T1_s"] for x in _SOND]
_ri = max(_v) / c_pipe[64]; _rj = max(_vi) / c_t1[64]
ORC["variabilidade_das_sondas"] = {"sondas": _SOND, "fora": _SOND_FORA, "d64_instancia_faixa_s": [min(_v), max(_v)], "d64_injecao_faixa_s": [min(_vi), max(_vi)],
                                   "maior_sobre_corrente": {"instancia": round(_ri, 3), "injecao_T1": round(_rj, 3)},
                                   "nota": ("o orcamento usa SO a sonda deste trabalhador; as outras sao de versoes anteriores do trabalhador (a mesma maquina, os mesmos caminhos de "
                                            "calculo do tempo) e mostram a dispersao entre rodadas; a maior sonda sobre a corrente da %.3f (instancia) e %.3f (injecao do T1): a margem "
                                            "x%.2f %s a faixa observada; nao foi medida sob a carga do rito") % (_ri, _rj, MARGEM, "COBRE" if max(_ri, _rj) <= MARGEM else "NAO cobre")}'''),
# [13] a causa (3) recalculada com todas as sondas
A('''_t1_16_32 = (int(PLANO_B["T1"]["16"])''', '''def _estimar_com(tim_, T1c, T1n, T4c, T2g):
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
_cur = [x for x in _PB_POR if _SOND_P.get(x["sonda"]) and os.path.abspath(_SOND_P[x["sonda"]]) == os.path.abspath(TIMING)]
_oth = [x for x in _PB_POR if x not in _cur]
_causa3 = ("(3) com a sonda deste trabalhador, o plano B inteiro levaria cerca de %.0f min (%.0f com a margem): o D128 só começaria, com a margem, se o prazo de início "
           "fosse de pelo menos %.0f min (o desta especificação é %.0f), e então terminaria por volta de %.0f min, %s das 5 h; com as outras %d sondas válidas (versões "
           "anteriores do trabalhador, o mesmo caminho de cálculo do tempo), o plano B com a margem iria de %.0f a %.0f min, ACIMA das 5 h em %d delas; a folga, quando existe, "
           "é menor que a dispersão entre as sondas (%.0f%% na instância de d = 64). Por isso, e não por uma medida única, d = 64 vira camada de ESCALA e a estatística forte "
           "fica em d <= 32") % (
    totB / 60, totB * MARGEM / 60, (_cur[0]["antes_do_D128_com_margem_min"] if _cur else float("nan")), SPEC["D128"]["start_deadline_s"] / 60,
    (_cur[0]["fim_do_D128_com_margem_min"] if _cur else float("nan")), ("dentro" if (_cur and _cur[0]["fim_do_D128_com_margem_min"] < SPEC["execution"]["um_py_timeout_s"] / 60) else "FORA"),
    len(_oth), min([x["com_margem_min"] for x in _oth] or [float("nan")]), max([x["com_margem_min"] for x in _oth] or [float("nan")]),
    sum(1 for x in _oth if not x["cabe_em_5h_com_margem"]), 100.0 * _disp)
_t1_16_32 = (int(PLANO_B["T1"]["16"])'''),
A('''"instância (o plano B contava %.1f s); (3) por isso o plano B inteiro, com os custos medidos agora, dá cerca de %.0f min (%.0f com a margem) e, com a margem, %s no prazo "
              "congelado de 5 h; e %s. Logo d = 64 vira camada de ESCALA e a estatística forte fica em d <= 32. O T1 também''',
  '''"instância (o plano B contava %.1f s); %s; e %s. O T1 também'''),
A('''PLJ["custos_s"]["pipeline"]["64"], totB / 60, totB * MARGEM / 60,
        "NÃO cabe" if totB * MARGEM >= SPEC["execution"]["um_py_timeout_s"] else "cabe", _frase_preB, PLANO_B["T1"]["16"],''',
  '''PLJ["custos_s"]["pipeline"]["64"], _causa3, _frase_preB, PLANO_B["T1"]["16"],'''),
A('''                "cabe_no_prazo_de_5_h": bool(totB * MARGEM < SPEC["execution"]["um_py_timeout_s"])},''',
  '''                "cabe_no_prazo_de_5_h": bool(totB * MARGEM < SPEC["execution"]["um_py_timeout_s"]), "por_sonda": _PB_POR, "dispersao_d64_instancia": round(_disp, 3)},'''),
# [17] as sondas da variabilidade nas evidencias
A('''EV_OPC = {"afericao_6"}''', '''EV_OPC = {"afericao_6"}
_EV += [("variabilidade_" + _x["sonda"], os.path.abspath(_SOND_P[_x["sonda"]])) for _x in _SOND if os.path.abspath(_SOND_P[_x["sonda"]]) != os.path.abspath(TIMING)]   # 6a afericao'''),
# [15] negacao explicita
A('''    assert _toks == [ESCOLHA],''', '''    assert not re.search(r"\\bn[aã]o\\s+(ratifico|concordo|aprovo|autorizo)\\b", r_[1].lower()), "a mensagem do operador NEGA (%r): nao e' ratificacao" % r_[1][:120]   # 6a afericao
    assert _toks == [ESCOLHA],'''),
A('''hífen e sublinhado valem como espaço." % ESCOLHA)''', '''hífen e sublinhado valem como espaço. A guarda do gerador é LEXICAL (a escolha nomeada, sem negação explícita); a conferência final é a leitura humana do verbatim, gravado no V1." % ESCOLHA)'''),
# [2] nunca sobrevive
A('''o arquivo do pilar de uma rodada anterior no Nós nunca sobrevive (''', '''o arquivo do pilar de uma rodada anterior no Nós nunca passa por desta rodada (se outro processo o segurar, ele fica no Nós, os erros vão ao registro do selo e o selo grava NOT_THIS_RUN; '''),
# [18] CUSTODY: o veredito rederivado
A('''ou o resultado não chegou ao Nós), este só''', '''ou o resultado não chegou ao Nós, ou o veredito rederivado falta ou difere do gravado pelo trabalhador), este só'''),
# 5N5 [7] e o mata_um
A('''o PID do lançador fica em .rito_v384.pid, e abortar o rito é kill -TERM nesse PID",''',
  '''o PID do lançador fica em .rito_v384.pid, e abortar o rito é kill -TERM nesse PID NO GIT BASH (é PID do MSYS, não do Windows; não no PowerShell) — o TaskStop da ferramenta da gerência NÃO para o lançador; num sinal durante o rito, o encerramento da árvore do um.py é fail-closed (pelo PID nativo do subshell do rito; senão pelos descendentes do lançador com a data de criação conferida; senão FALHA VISIVEL no log e em rito_v384_sinal.txt)",'''),
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:130])
    s = s.replace(old, new)
# [16] no congelamento, o DOC igual ao do rascunho apresentado fora dos campos volateis
ANC = '''import re as _re
_txt = json.dumps('''
assert s.count(ANC) == 1
s = s.replace(ANC, '''if RAT:   # 6a afericao: o V1 tem de ser o rascunho apresentado, fora dos campos que mudam por natureza
    _VOL = {"id", "titulo", "gerado", "gerado_utc", "ratificacao_do_operador", "evidencias", "afericao"}
    _a = {k: v for k, v in DOC.items() if k not in _VOL}; _b = {k: v for k, v in RASC.items() if k not in _VOL}
    for _d_ in (_a, _b):
        if isinstance(_d_.get("desvio_do_plano_B"), dict):
            _d_["desvio_do_plano_B"] = {k: v for k, v in _d_["desvio_do_plano_B"].items() if k != "ratificacao"}
    _dif = sorted(k for k in set(_a) | set(_b) if json.dumps(_a.get(k), sort_keys=True, ensure_ascii=False) != json.dumps(_b.get(k), sort_keys=True, ensure_ascii=False))
    assert not _dif, "o V1 difere do rascunho apresentado ao operador em: %s" % _dif
''' + ANC)
ast.parse(s)
b = s.encode("utf-8")
for i in range(40):
    try:
        open(P + ".tmp", "wb").write(b); os.replace(P + ".tmp", P); break
    except PermissionError:
        time.sleep(0.5)
assert open(P, "rb").read() == b
print("ok", len(PAIRS) + 1, "trocas")
