# -*- coding: utf-8 -*-
"""7a afericao no GERADOR DO PRE-REGISTRO:
- ALTO: a comparacao do V1 com o rascunho apresentado e' feita sobre as formas CANONICAS dos dois lados (ida e volta pelo JSON) -- antes, chaves inteiras em
  memoria contra chaves texto do JSON faziam todo congelamento ser recusado;
- MEDIO: as evidencias so sao copiadas DEPOIS de todas as guardas (palavras proibidas, comparacao, V1/MD ja existentes), por uma pasta TEMPORARIA renomeada; se a
  pasta permanente ja existir, tem de conferir arquivo a arquivo; so entao o V1 e o MD sao gravados;
- a sonda corrente identificada por sha256 (assert de exatamente uma);
- B_AMPLIADO_D64: a conclusao do desvio condicionada a escolha; a folga contra a dispersao CALCULADA;
- o texto da guarda de negacao diz exatamente o que ela recusa; o criterio das sondas, as fora e a dispersao maior/menor no texto;
- o item 7 da arvore com a ressalva da falha da propria gravacao do parcial;
- um transcrito de TESTE por variavel de ambiente (TGL_PREREG_TRANSCRITO_TESTE), recusado na pasta permanente.
Backup de bytes; ast."""
import ast, glob, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
bk = sorted(glob.glob(P + ".bak_antes_afer7_*"))
assert bk and open(bk[-1], "rb").read() == raw, "o backup de antes da 7a nao e' o estado corrente"
PAIRS = []
A = lambda o, n: PAIRS.append((o, n))
A('''TRANS = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")''',
  '''TRANS = os.environ.get("TGL_PREREG_TRANSCRITO_TESTE") or os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
if os.environ.get("TGL_PREREG_TRANSCRITO_TESTE"):   # so para testar o congelamento numa pasta de TESTE (7a afericao); nunca na permanente
    assert os.path.normcase(HERE) != os.path.normcase(os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out")), "transcrito de TESTE na pasta permanente"''')
A('''_cur = [x for x in _PB_POR if _SOND_P.get(x["sonda"]) and os.path.abspath(_SOND_P[x["sonda"]]) == os.path.abspath(TIMING)]''',
  '''_TSHA = fsha(TIMING)
_cur = [x for x in _PB_POR if fsha(_SOND_P[x["sonda"]]) == _TSHA]   # por sha256, nao por caminho (7a afericao)
assert len(_cur) == 1, "a sonda corrente nao esta exatamente uma vez entre as sondas validas (%d)" % len(_cur)'''),
A('''"anteriores do trabalhador, o mesmo caminho de cálculo do tempo), o plano B com a margem iria de %.0f a %.0f min, ACIMA das 5 h em %d delas; a folga, quando existe, "
           "é menor que a dispersão entre as sondas (%.0f%% na instância de d = 64). Por isso, e não por uma medida única, d = 64 vira camada de ESCALA e a estatística forte "
           "fica em d <= 32") % (''', '''"anteriores do trabalhador, o mesmo caminho de cálculo do tempo), o plano B com a margem iria de %.0f a %.0f min, ACIMA das 5 h em %d delas; %s "
           "(a dispersão entre as sondas é de %.0f%% na instância de d = 64). Por isso, e não por uma medida única, %s") % ('''),
A('''    sum(1 for x in _oth if not x["cabe_em_5h_com_margem"]), 100.0 * _disp)''',
  '''    sum(1 for x in _oth if not x["cabe_em_5h_com_margem"]),
    (("a maior folga entre as sondas que cabem é de %.0f%% das 5 h, %s que a dispersão" % (100.0 * _folga_max, "MENOR" if _folga_max < _disp else "maior")) if _folga_max is not None
     else "nenhuma sonda deixa folga nas 5 h"), 100.0 * _disp,
    ("d = 64 vira camada de ESCALA e a estatística forte fica em d <= 32" if ESCOLHA == "B_REDUZIDO" else
     "o T1 de d = 64 fica reduzido (%d injeções contra %s do plano B), e a estatística forte do T1 fica em d <= 32" % (SPEC["T1"]["d_counts"]["64"], PLANO_B["T1"]["64"])))'''),
A('''_disp = (max(_v) - min(_v)) / min(_v)''', '''_disp = (max(_v) - min(_v)) / min(_v)
_fol = [(SPEC["execution"]["um_py_timeout_s"] / 60 - x["com_margem_min"]) / (SPEC["execution"]["um_py_timeout_s"] / 60) for x in _PB_POR if x["cabe_em_5h_com_margem"]]
_folga_max = max(_fol) if _fol else None   # a folga CALCULADA, contra a dispersao (7a afericao)'''),
# o texto da variabilidade: criterio, fora, dispersao maior/menor
A('''                                   "nota": ("o orcamento usa SO a sonda deste trabalhador; as outras sao de versoes anteriores do trabalhador (a mesma maquina, os mesmos caminhos de "
                                            "calculo do tempo) e mostram a dispersao entre rodadas; a maior sonda sobre a corrente da %.3f (instancia) e %.3f (injecao do T1): a margem "
                                            "x%.2f %s a faixa observada; nao foi medida sob a carga do rito") % (_ri, _rj, MARGEM, "COBRE" if max(_ri, _rj) <= MARGEM else "NAO cobre")}''',
  '''                                   "nota": ("criterio: as pastas teste_tempo_v* do pacote com d = 64 medido em reps >= 3 (a mediana); fora do criterio: %s; o orcamento usa SO a "
                                            "sonda deste trabalhador; as outras sao de versoes anteriores do trabalhador (a mesma maquina, os mesmos caminhos de calculo do tempo) e "
                                            "mostram a dispersao entre rodadas: a maior sonda sobre a corrente da %.3f (instancia) e %.3f (injecao do T1), e a maior sobre a menor da "
                                            "%.3f (instancia) -- a margem x%.2f %s a maior sobre a corrente e %s a dispersao maior/menor; nao foi medida sob a carga do rito") % (
                                       ", ".join("%s (%s)" % (x["sonda"], x["motivo"]) for x in _SOND_FORA) or "nenhuma", _ri, _rj, max(_v) / min(_v), MARGEM,
                                       "cobre" if max(_ri, _rj) <= MARGEM else "NAO cobre", "cobre" if max(_v) / min(_v) <= MARGEM else "NAO cobre")}'''),
# a guarda de negacao, no texto
A('''A guarda do gerador é LEXICAL (a escolha nomeada, sem negação explícita); a conferência final é a leitura humana do verbatim, gravado no V1." % ESCOLHA)''',
  '''A guarda do gerador é LEXICAL: exige a escolha nomeada e recusa a mensagem com «não»/«nao» imediatamente antes de «ratifico», «concordo», «aprovo» ou «autorizo»; a conferência final é a leitura humana do verbatim, gravado no V1." % ESCOLHA)'''),
# o item 7 da arvore
A('''o parcial é gravado logo depois do espectro, com n0 e zero_mode_ok, e sobrevive a uma morte do processo) ->''',
  '''o parcial é gravado logo depois do espectro, com n0 e zero_mode_ok, e sobrevive a uma morte do processo — salvo falha da própria gravação do parcial, registrada em partial_write_error no result.json só se o D128 retornar) ->'''),
# as evidencias: planejadas no laco, copiadas so depois das guardas
A('''EVID = []
for _pp_, _p_ in _EV:''', '''EVID = []; _COPIAR = []
for _pp_, _p_ in _EV:'''),
A('''    if RAT:
        _dd = os.path.join(HERE, "evidencias_PREREGISTRO_V1"); os.makedirs(_dd, exist_ok=True)
        _dst = os.path.join(_dd, _pp_ + "__" + os.path.basename(_p_))
        if not os.path.exists(_dst):
            shutil.copyfile(_p_, _dst)
        assert fsha(_dst) == _e["sha256"], "a copia permanente da evidencia nao confere: %s" % _dst
        _e["copia_permanente"] = _dst''', '''    if RAT:   # so PLANEJADA aqui; a copia acontece depois de TODAS as guardas (7a afericao)
        _dst = os.path.join(HERE, "evidencias_PREREGISTRO_V1", _pp_ + "__" + os.path.basename(_p_))
        _e["copia_permanente"] = _dst; _COPIAR.append((_p_, _dst, _e["sha256"]))'''),
A('''_EV += [("variabilidade_" + _x["sonda"], os.path.abspath(_SOND_P[_x["sonda"]])) for _x in _SOND if os.path.abspath(_SOND_P[_x["sonda"]]) != os.path.abspath(TIMING)]   # 6a afericao''',
  '''_EV += [("variabilidade_" + _x["sonda"], os.path.abspath(_SOND_P[_x["sonda"]])) for _x in _SOND if fsha(_SOND_P[_x["sonda"]]) != _TSHA]   # 6a e 7a afericoes'''),
# ALTO: a comparacao canonica
A('''    _a = {k: v for k, v in DOC.items() if k not in _VOL}; _b = {k: v for k, v in RASC.items() if k not in _VOL}''',
  '''    _DOCJ = json.loads(json.dumps(DOC, ensure_ascii=False))   # a forma CANONICA (ida e volta pelo JSON): chaves inteiras viram texto, como no rascunho (7a afericao)
    _a = {k: v for k, v in _DOCJ.items() if k not in _VOL}; _b = {k: v for k, v in RASC.items() if k not in _VOL}'''),
# a gravacao: so depois de tudo
A('''raw = json.dumps(DOC, ensure_ascii=False, indent=1).encode("utf-8")
p = BASE + ".json"
if os.path.exists(p):
    if open(p, "rb").read() != raw:
        raise SystemExit("RECUSO: %s ja existe com outro conteudo (o congelado nao se sobrescreve; gere um V1.x)" % p)
else:
    open(p + ".tmp", "wb").write(raw); assert os.path.getsize(p + ".tmp") == len(raw); os.replace(p + ".tmp", p)
''', '''raw = json.dumps(DOC, ensure_ascii=False, indent=1).encode("utf-8")
PJSON = BASE + ".json"
if os.path.exists(PJSON) and open(PJSON, "rb").read() != raw:
    raise SystemExit("RECUSO: %s ja existe com outro conteudo (o congelado nao se sobrescreve; gere um V1.x)" % PJSON)
'''),
A('''md = ("\\n".join(L) + "\\n").encode("utf-8")
p = BASE + ".md"
if os.path.exists(p) and open(p, "rb").read() != md:
    raise SystemExit("RECUSO: %s ja existe com outro conteudo" % p)
if not os.path.exists(p):
    open(p + ".tmp", "wb").write(md); assert os.path.getsize(p + ".tmp") == len(md); os.replace(p + ".tmp", p)''',
  '''md = ("\\n".join(L) + "\\n").encode("utf-8")
PMD = BASE + ".md"
if os.path.exists(PMD) and open(PMD, "rb").read() != md:
    raise SystemExit("RECUSO: %s ja existe com outro conteudo" % PMD)
# SO AGORA, com todas as guardas passadas: as evidencias (pasta TEMPORARIA renomeada; a permanente que ja existir tem de conferir) e depois o V1 e o MD (7a afericao)
if RAT and _COPIAR:
    _dd = os.path.join(HERE, "evidencias_PREREGISTRO_V1")
    if os.path.isdir(_dd):
        for _src, _dst, _sh in _COPIAR:
            assert os.path.exists(_dst) and fsha(_dst) == _sh, "a pasta de evidencias ja existe e nao confere com esta: %s" % _dst
    else:
        _tmpd = _dd + ".tmp_" + time.strftime("%Y%m%d_%H%M%S"); os.makedirs(_tmpd)
        for _src, _dst, _sh in _COPIAR:
            _t = os.path.join(_tmpd, os.path.basename(_dst)); shutil.copyfile(_src, _t)
            assert fsha(_t) == _sh, "a copia da evidencia nao confere: %s" % _t
        os.replace(_tmpd, _dd)
for _pth, _b in ((PJSON, raw), (PMD, md)):
    if not os.path.exists(_pth):
        open(_pth + ".tmp", "wb").write(_b); assert os.path.getsize(_pth + ".tmp") == len(_b); os.replace(_pth + ".tmp", _pth)'''),
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:130])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8")
for i in range(40):
    try:
        open(P + ".tmp", "wb").write(b); os.replace(P + ".tmp", P); break
    except PermissionError:
        time.sleep(0.5)
assert open(P, "rb").read() == b
print("ok", len(PAIRS), "trocas")
