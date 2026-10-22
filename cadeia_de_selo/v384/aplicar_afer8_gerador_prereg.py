# -*- coding: utf-8 -*-
"""8a afericao no GERADOR DO PRE-REGISTRO (script salvo, count == 1; backup de BYTES ja feito: .bak_antes_afer8_20261004_080849, conferido aqui):
- 6N25: a dispersao das sondas POR d E POR CUSTO (instancia, injecao do T1, nivel extra de ruido do T1), CALCULADA, com o texto gerado dos numeros: onde a
  maior sonda sobre a corrente passa da margem e onde a maior sobre a menor passa (a margem x1,25 NAO cobre d = 32 instancia nem a injecao do T1 em d = 64);
- a guarda do transcrito de TESTE tambem por os.path.samefile (atalhos 8.3, juncoes);
- a ratificacao registra QUAL transcrito foi lido: caminho, de_teste, e o sha256 da LINHA bruta da mensagem do operador (a linha nao muda; o arquivo cresce);
- as afericoes 7 e 8 OBRIGATORIAS nas evidencias; a 9 opcional;
- a pasta de evidencias que ja existir tem de ter EXATAMENTE os mesmos arquivos (listdir igual), nao so os que conferem;
- a gravacao: o MD primeiro e o JSON por ultimo (o JSON e' a autoridade: se ele existe, o MD existe), cada um temporario -> tamanho -> substituir, com novas
  tentativas em PermissionError (40 x 0,25 s) e o temporario apagado se falhar;
- o texto do lancador: o codigo 16, o PID gravado logo depois da guarda, a conferencia do /proc/<pid>/cmdline antes de abortar, o giro do log e dos sinais so
  depois da ultima recusa, e o marcador que fica com parada em curso."""
import ast, glob, os, time
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
_bk = glob.glob(P + ".bak_antes_afer8_*"); assert len(_bk) == 1 and open(_bk[0], "rb").read() == raw, _bk
PAIRS = [
    # a guarda do transcrito de teste (samefile)
    ('''if os.environ.get("TGL_PREREG_TRANSCRITO_TESTE"):   # so para testar o congelamento numa pasta de TESTE (7a afericao); nunca na permanente
    assert os.path.normcase(HERE) != os.path.normcase(os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out")), "transcrito de TESTE na pasta permanente"''',
     '''TRANS_DE_TESTE = bool(os.environ.get("TGL_PREREG_TRANSCRITO_TESTE"))
if TRANS_DE_TESTE:   # so para testar o congelamento numa pasta de TESTE (7a afericao); nunca na permanente -- tambem por samefile (8a afericao)
    _PERM_ = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out")
    assert os.path.normcase(HERE) != os.path.normcase(_PERM_) and not (os.path.isdir(_PERM_) and os.path.samefile(HERE, _PERM_)), "transcrito de TESTE na pasta permanente"'''),
    # as linhas do transcrito: a extracao fatorada (para achar a LINHA bruta da ratificacao)
    ('''def _texts():
    with open(TRANS, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
            except Exception:
                continue
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
''', '''def _textos_de(d):
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
                out_.append(line.rstrip(b"\\r\\n"))
    return out_
'''),
    # a ratificacao registra o transcrito
    ('''           "a_especificacao_ratificada_e_a_do_rascunho": RASCUNHO_SPEC == SPEC_SHA}''',
     '''           "a_especificacao_ratificada_e_a_do_rascunho": RASCUNHO_SPEC == SPEC_SHA}
    _lb = _linhas_brutas(r_[0], r_[1])
    assert len(_lb) >= 1, "a linha bruta da ratificacao nao foi achada no transcrito"
    RAT["transcrito"] = {"caminho": os.path.abspath(TRANS), "de_teste": TRANS_DE_TESTE, "linhas_da_mensagem": len(_lb),
                         "sha256_das_linhas_da_mensagem": [sha(x) for x in _lb], "tamanho_do_transcrito_na_leitura_bytes": os.path.getsize(TRANS)}   # 8a afericao'''),
    # 6N25: por d e por custo
    ('''assert ORC["o_D128_comeca_no_prazo_mesmo_com_a_margem"] and ORC["o_D128_termina_antes_do_prazo_do_um_py_mesmo_com_a_margem"], ORC''',
     '''_PDC = []   # 8a afericao (6N25): a dispersao POR d E POR CUSTO, calculada
for _d in sorted(c_pipe):
    for _ck, _nmk in (("pipeline_s", "instancia"), ("t1_injection_sigma0_s", "injecao do T1"), ("t1_extra_noise_level_s", "nivel extra de ruido do T1")):
        _vals = [float(_SOND_T[x["sonda"]][str(_d)][_ck]) for x in _SOND if str(_d) in _SOND_T[x["sonda"]] and _ck in _SOND_T[x["sonda"]][str(_d)]]
        _cv = float(tim[str(_d)][_ck])
        _PDC.append({"d": _d, "custo": _nmk, "corrente_s": round(_cv, 4), "n_sondas": len(_vals), "_mc": max(_vals) / _cv, "_mm": max(_vals) / min(_vals),
                     "maior_sobre_corrente": round(max(_vals) / _cv, 3), "maior_sobre_menor": round(max(_vals) / min(_vals), 3)})
_pdc_mc = max(_PDC, key=lambda x: x["_mc"]); _pdc_fora_mc = [x for x in _PDC if x["_mc"] > MARGEM]; _pdc_fora_mm = [x for x in _PDC if x["_mm"] > MARGEM]
_pdc_lenta = sorted(set(x["d"] for x in _PDC) - set(x["d"] for x in _PDC if x["_mc"] > 1.0 + 1e-12))
_fmt_pdc = lambda xs, k: ", ".join("d = %d %s (%.3f)" % (x["d"], x["custo"], x[k]) for x in xs)
ORC["variabilidade_das_sondas"]["por_d_e_custo"] = [{k: v for k, v in x.items() if not k.startswith("_")} for x in _PDC]
ORC["variabilidade_das_sondas"]["nota_por_d_e_custo"] = (
    "Por d e por custo (instancia, injecao do T1, nivel extra de ruido do T1; %d sondas): a maior sonda sobre a corrente vai ate %.3f (d = %d, %s) -- a margem x%.2f "
    "%s; a sonda corrente e' a mais lenta de todas em %s; a maior sobre a menor passa da margem em %s -- nesses pontos a margem NAO cobre a dispersao entre "
    "rodadas (a corrente sendo a mais lenta ali, o orcamento ja usa o pior caso medido; uma rodada mais lenta que todas as sondas nao esta coberta)") % (
    len(_SOND), _pdc_mc["_mc"], _pdc_mc["d"], _pdc_mc["custo"], MARGEM,
    ("cobre a maior sobre a corrente em todo d e custo" if not _pdc_fora_mc else "NAO cobre a maior sobre a corrente em " + _fmt_pdc(_pdc_fora_mc, "_mc")),
    ("d = " + ", ".join(str(x) for x in _pdc_lenta) if _pdc_lenta else "nenhum d"),
    (_fmt_pdc(_pdc_fora_mm, "_mm") if _pdc_fora_mm else "nenhum ponto"))
assert ORC["o_D128_comeca_no_prazo_mesmo_com_a_margem"] and ORC["o_D128_termina_antes_do_prazo_do_um_py_mesmo_com_a_margem"], ORC'''),
    # as afericoes 7 e 8 obrigatorias; a 9 opcional
    ('''       ("afericao_6", os.path.join(ESTD, "afericao6_resultado.json")), ("aferidor_verbatim", os.path.join(ESTD, "AFERIDOR_v384.txt"))] + [("estresse_" + k, p_) for k, p_ in EST.items()]
EV_OPC = {"afericao_6"}''',
     '''       ("afericao_6", os.path.join(ESTD, "afericao6_resultado.json")), ("afericao_7", os.path.join(ESTD, "afericao7_resultado.json")),
       ("afericao_8", os.path.join(ESTD, "afericao8_resultado.json")), ("afericao_9", os.path.join(ESTD, "afericao9_resultado.json")),
       ("aferidor_verbatim", os.path.join(ESTD, "AFERIDOR_v384.txt"))] + [("estresse_" + k, p_) for k, p_ in EST.items()]
EV_OPC = {"afericao_9"}   # 8a afericao: a 6, a 7 e a 8 obrigatorias'''),
    # o MD mostra a nota por d e custo
    ('''_VS.get("d64_instancia_faixa_s", ["?", "?"])[1], _VS["nota"])); A("")''',
     '''_VS.get("d64_instancia_faixa_s", ["?", "?"])[1], _VS["nota"] + ((". " + _VS["nota_por_d_e_custo"]) if _VS.get("nota_por_d_e_custo") else ""))); A("")'''),
    # a pasta de evidencias que ja existe: os MESMOS arquivos
    ('''    if os.path.isdir(_dd):
        for _src, _dst, _sh in _COPIAR:''',
     '''    if os.path.isdir(_dd):
        assert sorted(os.listdir(_dd)) == sorted(os.path.basename(_d_) for _s_, _d_, _h_ in _COPIAR), "a pasta de evidencias ja existe com OUTROS arquivos: %s" % _dd   # 8a
        for _src, _dst, _sh in _COPIAR:'''),
    # a gravacao: MD primeiro, JSON por ultimo, com novas tentativas
    ('''for _pth, _b in ((PJSON, raw), (PMD, md)):
    if not os.path.exists(_pth):
        open(_pth + ".tmp", "wb").write(_b); assert os.path.getsize(_pth + ".tmp") == len(_b); os.replace(_pth + ".tmp", _pth)''',
     '''for _pth, _b in ((PMD, md), (PJSON, raw)):   # o MD primeiro, o JSON (a autoridade) por ultimo; temporario -> tamanho -> substituir, com novas tentativas (8a)
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
                os.remove(_pth + ".tmp")
            raise'''),
    # o texto do lancador
    ('''o PID do lançador fica em .rito_v384.pid, e abortar o rito é kill -TERM nesse PID NO GIT BASH (é PID do MSYS, não do Windows; não no PowerShell)''',
     '''o PID do lançador fica em .rito_v384.pid, gravado logo depois da guarda (com outro lançador vivo, RECUSA — código 16), e abortar o rito é kill -TERM nesse PID NO GIT BASH, conferindo antes que /proc/<pid>/cmdline contém rito_v384 (é PID do MSYS, não do Windows; não no PowerShell); o log da tentativa e o registro dos sinais só giram (para .anterior) depois da última recusa'''),
    ('''e espera até 60 s que nenhuma parada esteja em curso antes de religar (com AVISO no log se expirar)''',
     '''e espera até 60 s que nenhuma parada esteja em curso antes de religar (com AVISO no log se expirar; depois de um AVISO, o marcador só sai se a porta ainda escutar 30 s depois e nenhuma parada — Stop-ScheduledTask ou stop_iald_llama.ps1 — estiver em curso)'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:140])
    s = s.replace(old, new)
assert "def sha(" in s or "sha = " in s or "sha=" in s, "a funcao sha do gerador nao foi achada"
ast.parse(s)
b = s.encode("utf-8")
for i in range(40):
    try:
        open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P); break
    except PermissionError:
        time.sleep(0.5)
assert open(P, "rb").read() == b
import hashlib
print("ok", len(PAIRS), hashlib.sha256(b).hexdigest()[:16])
