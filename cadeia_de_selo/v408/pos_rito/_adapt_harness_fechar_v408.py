# -*- coding: utf-8 -*-
"""_adapt_harness_fechar_v408.py -- (claude-construtor-v408, fork B, 04/11/2026) adapta harness_fechar_sandbox_v408.py a v408 por trocas de CONTAGEM EXATA, linha unica e trechos entre marcadores unicos:
(1) as notas do cabecalho e a docstring (o conteudo passa de «o psion, o canto e o par» a «Tetelestai e' o terminal»); (2) MAN_CHAVES = as chaves versionadas do manifesto da v408 (registros_v408/v407/v406, registros_funcao_v408/v407/v406, pedras_v407/v406/v405_como_registro, sem chaves_v408);
(3) os stubs (TOPICO_NOVO e REGS da v408; a V minima com fecho406/reg406d/bundle406/ancoras406/bandeiras406/chaves407/chaves406); (4) a montagem do sandbox: a importacao do delta REAL e' INSTRUMENTADA (open/exists/isfile/isdir/getsize) e o ESPELHO DA CASA leva ao sandbox,
na mesma posicao relativa, todo arquivo abaixo de Central de Patentes que o delta_v408 e os deltas herdados abrem ao importar (medido, nunca digitado); a pasta irma v406 entra (a subida mecanica a deixara de fora) e e' o BUNDLE_v406.json da copia dela que recebe o origem_integracao do sandbox
(o BUNDLE_v408.json nao tem esse campo e vai byte a byte); as falas copiadas para cunhagens_13out sao so' as que moram la' (as de 30/10 e da Identidade vao pelo espelho); o recibo sintetico do B(n) leva a data de 04/11; (5) os CONTROLES NEGATIVOS da v408: tetelestai (3 de 4), psion herdado (8 de 9), fechamento herdado (300 de 301),
chave do lema False, chave da rede de Fock False, frase proibida nos limites do terminal, chave antiga dita mudada, E21 ausente (cunhagens_v408 e ao lado da cunhagens_v407 herdada), D54 ausente, leitura de 04/11 dita REAL, inscricao nao embutida, pedra selada da v403 adulterada, as quatro ancoras principais fora do trio,
mais os herdados (psion v405, f2b, V1, angle_status, gate, caminho, ponte, direcao do testemunho, sidecar); a porta do paragrafo novo levanta com o terminal adulterado; (6) a limpeza guarda TODAS as saidas dos controles.
Backup de BYTES (.bak_<TS>_adapt); temporario -> conferir -> substituir; ast.parse; CRLF preservado. Escrito pelo Write (o heredoc do Bash colapsa barras). Fail-closed: contagem errada = nada gravado. Nao roda o harness."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")
s16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
P = os.path.join(HERE, "harness_fechar_sandbox_v408.py")
raw = open(P, "rb").read(); t = raw.decode("utf-8"); NL = "\r\n" if b"\r\n" in raw else "\n"; n = 0
_nl = lambda s: s.replace("\r\n", "\n").replace("\n", NL)


def sub(a, b, k=1):
    global t, n
    a = _nl(a); b = _nl(b); c = t.count(a)
    assert c == k, "esperava %d ocorrencia(s) e achou %d: %r" % (k, c, a[:100])
    t = t.replace(a, b); n += 1


def linha(prefixo, nova=None):
    global t, n
    ls = t.split(NL); idx = [i for i, l in enumerate(ls) if l.startswith(prefixo)]
    assert len(idx) == 1, "prefixo de linha esperava 1 e achou %d: %r" % (len(idx), prefixo[:90])
    if nova is None:
        del ls[idx[0]]
    else:
        ls[idx[0]] = nova
    t = NL.join(ls); n += 1


def entre(ini, fim, novo):
    global t, n
    ini = _nl(ini); fim = _nl(fim)
    assert t.count(ini) == 1 and t.count(fim) == 1, "marcadores nao unicos (%d, %d): %r / %r" % (t.count(ini), t.count(fim), ini[:70], fim[:70])
    a = t.index(ini); b = t.index(fim) + len(fim); assert b > a
    t = t[:a] + _nl(novo) + t[b:]; n += 1


# ---- (1) cabecalho e docstring
linha("# [A ADAPTAR v408]")
linha("# [ADAPTADO v408, 03/11/2026]", "# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork B)] sobre a subida mecanica de rotulo da v407 FINAL (_bump_copia_v408.py), por _adapt_harness_fechar_v408.py: o conteudo e' o da v408 (TETELESTAI E' O TERMINAL: o bundle de quatro modulos, o registro com funcao tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados, nenhuma chave antiga muda); MAN_CHAVES, os stubs, os controles negativos e a montagem do sandbox (a pasta irma v406, o BUNDLE_v406 com origem_integracao, o espelho da casa medido na importacao do delta) sao os da v408; a gerencia revisa antes do rito (nao e' versao selada).")
sub("import datetime, glob, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, time", "import builtins, datetime, glob, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, time")
sub("Derivado do harness_fechar_sandbox_v407.py (que rodou na v407), com as licoes da v408 (o caminho, a vida, o adendo da verdade e as bandeiras do gate; o passo simples B16 -> B17).",
    "Derivado do harness_fechar_sandbox_v407.py (que rodou na v407), adaptado a v408 por _adapt_harness_fechar_v408.py (claude-construtor-v408, fork B, 04/11/2026): Tetelestai e' o terminal (o bundle de quatro modulos, o registro tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados, nenhuma chave antiga muda; o passo simples B16 -> B17).")
sub("+ as pastas irmas v407, v400 e v399 (o delta_v408 importa o delta_v407, este o delta_v400 e este o delta_v399; o runtime da secao e as seis fontes do operador moram na v400)",
    "+ as pastas irmas v407 a v399 (o delta_v408 importa o delta_v407 e, por ele, os anteriores; o runtime da secao e as seis fontes do operador moram na v400) + TODO arquivo da casa (abaixo de Central de Patentes: work e Chatgpt) que o delta_v408 e os deltas herdados abrem ou conferem ao importar, ESPELHADO no sandbox na mesma posicao relativa (a lista e' MEDIDA na hora, instrumentando open/exists/isfile/isdir/getsize na importacao do delta real; nada digitado)")
sub("o do quadro igual ao das funcoes do quadro sobre o core do sandbox e aprovado por T.verificar_paragrafo_readme; o da v408 (o psion, o canto e o par)", "o do quadro igual ao das funcoes do quadro sobre o core do sandbox e aprovado por T.verificar_paragrafo_readme; o da v408 (Tetelestai e' o terminal)")
sub("os dois diffs (com os 9 modulos novos), o manifesto (com o estado da fila) e o arquivo,", "os dois diffs (com os modulos novos do bundle), o manifesto (com o estado da fila) e o arquivo,")
sub("com um numero do psion_canto_v407 ou do fechamento_v406 (herdado) adulterado,", "com um numero do tetelestai_terminal_v408, do psion_canto_v407 (herdado) ou do fechamento_v406 (herdado) adulterado, com uma chave antiga dita mudada,")
sub("com uma inscricao de 27/10 rotulada como da gerencia, com uma errata ou uma decisao a menos, com uma pedra selada da v407 adulterada no hash formal, com uma pedra fora do trio",
    "com uma inscricao de 04/11 nao embutida, com a leitura de 04/11 dita REAL, com a errata E21 ou a decisao D54 a menos (e com a E21 ao lado da cunhagens_v407 herdada ausente), com uma pedra selada da v403 adulterada no hash formal, com uma ancora principal fora do trio")
# ---- (2) MAN_CHAVES
linha("# v408: as chaves do MANIFESTO de incorporacao", "# v408: as chaves do MANIFESTO de incorporacao que fechar_v408.py grava (nomes versionados: *_v408 = os registros desta versao (tetelestai_terminal_v408 e os dois specs); *_v407 = os HERDADOS da v407 (psion_canto_v407 e os dois specs, recriados); *_v406 = o fechamento_v406 e os dois specs; *_v405 = os treze da v405 selada, e assim por diante; SEM chaves_v408: nenhuma chave antiga muda)")
sub('''MAN_CHAVES = ("registros_v407", "registros_v406", "registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v408", "registros_funcao_v407", "ancoras_v408", "ancoras_v407", "bandeiras_v408", "bandeiras_v407", "chaves_v408", "chaves_v406", "f2b_errata", "bandeiras_do_gate_recriado",
              "funcoes_v407_recriadas", "funcoes_v405_recriadas", "funcoes_v403_recriadas", "funcoes_v402_recriadas", "pedras_v407_como_registro", "pedras_v405_como_registro", "falsidade_v401", "base_v407", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_v408", "sidecar_acom", "fila_da_memoria")''',
    '''MAN_CHAVES = ("registros_v408", "registros_v407", "registros_v406", "registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v408", "registros_funcao_v407", "registros_funcao_v406", "ancoras_v408", "ancoras_v407", "ancoras_v406", "bandeiras_v408", "bandeiras_v407", "bandeiras_v406", "chaves_v407", "chaves_v406", "f2b_errata", "bandeiras_do_gate_recriado",
              "funcoes_v407_recriadas", "funcoes_v406_recriadas", "funcoes_v405_recriadas", "funcoes_v403_recriadas", "funcoes_v402_recriadas", "pedras_v407_como_registro", "pedras_v406_como_registro", "pedras_v405_como_registro", "falsidade_v401", "base_v407", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_v408", "sidecar_acom", "fila_da_memoria")''')
# ---- (3) os stubs
sub("v408-selada-o-psion-o-canto-e-o-par.md", "v408-selada-tetelestai-e-o-terminal.md", 2)
sub("REGS = 'psion_canto_v407 cunhagens_v407 kh_n1_cobertura_v407'", "REGS = 'tetelestai_terminal_v408 cunhagens_v408 kh_n1_cobertura_v408'")
sub("'reg408': {'cunhagens_v407': {'ok': True}}, 'reg407d': {'cunhagens_v406': {'ok': True}}, 'reg407c': {'cunhagens_v405': {'ok': True}}, 'reg407b': {}, 'fecho': {'ok': True}, 'fecho407': {'ok': True}, 'ancoras': {}, 'ancoras407': {}, 'bandeiras': {}, 'bandeiras407': {}, 'bundle407': {}, 'chaves': {}, 'chaves407': {},",
    "'reg408': {'cunhagens_v408': {'ok': True}}, 'reg407d': {'cunhagens_v407': {'ok': True}}, 'reg406d': {'cunhagens_v406': {'ok': True}}, 'reg407c': {'cunhagens_v405': {'ok': True}}, 'reg407b': {}, 'fecho': {'ok': True}, 'fecho407': {'ok': True}, 'fecho406': {'ok': True}, 'ancoras': {}, 'ancoras407': {}, 'ancoras406': {}, 'bandeiras': {}, 'bandeiras407': {}, 'bandeiras406': {}, 'bundle407': {}, 'bundle406': {}, 'chaves407': {}, 'chaves406': {},")
sub("('base_v407', 'insumos_sha16', 'conferidor', 'pedras_v407_como_registro', 'pedras_v405_como_registro', 'funcoes_v407_recriadas', 'funcoes_v405_recriadas', 'funcoes_v403_recriadas', 'funcoes_v402_recriadas')",
    "('base_v407', 'insumos_sha16', 'conferidor', 'pedras_v407_como_registro', 'pedras_v406_como_registro', 'pedras_v405_como_registro', 'funcoes_v407_recriadas', 'funcoes_v406_recriadas', 'funcoes_v405_recriadas', 'funcoes_v403_recriadas', 'funcoes_v402_recriadas')")
# ---- (4) a montagem do sandbox
linha('os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)   # o delta acha', 'os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)   # o delta acha as falas do operador em cunhagens_13out, duas pastas acima da pasta do pacote do sandbox: as de 04/11 (cunhagens_v408) e as das versoes anteriores que moram la\' (registros recriados); as de 30/10 (experimento_espelho_30out) e a da Identidade (cadeia_de_selo405) vao pelo espelho da casa, abaixo')
sub('_dlx = importlib.util.spec_from_file_location("delta_v408_h", os.path.join(PKG, "delta_v408.py")); _dm = importlib.util.module_from_spec(_dlx); _dlx.loader.exec_module(_dm)',
    '''# v408 (fork B): a importacao do delta REAL e' INSTRUMENTADA (open/exists/isfile/isdir/getsize) para MEDIR, na hora, todo arquivo da casa (abaixo de Central de Patentes) que o delta_v408 e os deltas herdados (v407, v406, ...) abrem ou conferem ao importar:
# a lista alimenta o ESPELHO DA CASA (abaixo), que leva cada um ao sandbox na mesma posicao relativa; nada digitado. Os ganchos sao removidos logo depois da importacao (finally).
_ACESSOS = set()
_open0 = builtins.open


def _open_h(p, *a, **k):
    try:
        _ACESSOS.add(os.path.abspath(os.fspath(p)))
    except Exception:   # noqa: BLE001
        pass
    return _open0(p, *a, **k)


_osp0 = {n_: getattr(os.path, n_) for n_ in ("exists", "isfile", "isdir", "getsize")}


def _mk_h(f_):
    def g_(p, *a, **k):
        try:
            _ACESSOS.add(os.path.abspath(os.fspath(p)))
        except Exception:   # noqa: BLE001
            pass
        return f_(p, *a, **k)
    return g_


builtins.open = _open_h
for _n_h, _f_h in _osp0.items():
    setattr(os.path, _n_h, _mk_h(_f_h))
try:
    _dlx = importlib.util.spec_from_file_location("delta_v408_h", os.path.join(PKG, "delta_v408.py")); _dm = importlib.util.module_from_spec(_dlx); _dlx.loader.exec_module(_dm)
finally:
    builtins.open = _open0
    for _n_h, _f_h in _osp0.items():
        setattr(os.path, _n_h, _f_h)''')
entre("# v408 (desvio do molde, dito): o delta_v408 PINA POR ASSERT o caminho absoluto do MANIFEST", "os.path.basename(_dm.FASE9_V2_ARQ)))",
      '''# v408 (fork B): o BUNDLE_v408.json NAO tem origem_integracao (o bundle da v408 nao vem da integracao R3) e vai ao sandbox byte a byte; o MANIFEST da integracao R3 (que o delta_v406 herdado pina por assert, relativo a sua propria pasta) vai na mesma posicao relativa dentro de work/fechamento_02nov,
# e e' o BUNDLE_v406.json da COPIA da pasta irma v406 que recebe o origem_integracao do sandbox (abaixo); o resultado da Fase 9 V2 vai em work/fase9_v2_c1_23out/saidas; a candidata vai em pedra/
shutil.copyfile(os.path.join(PKG, "BUNDLE_v408.json"), os.path.join(PKS, "BUNDLE_v408.json"))
_man_sb = os.path.join(SB, "work", "fechamento_02nov", os.path.relpath(_dm.MANIFEST_INTEGRACAO_ARQ, _dm.ESTUDO_FECHO))
os.makedirs(os.path.dirname(_man_sb), exist_ok=True); shutil.copyfile(_dm.MANIFEST_INTEGRACAO_ARQ, _man_sb)
os.makedirs(os.path.join(SB, "work", "fase9_v2_c1_23out", "saidas"), exist_ok=True); shutil.copyfile(_dm.FASE9_V2_ARQ, os.path.join(SB, "work", "fase9_v2_c1_23out", "saidas", os.path.basename(_dm.FASE9_V2_ARQ)))''')
sub('''for _nm_v in [n_ for n_ in dir(_dm) if n_.startswith("VERBATIM_ORIGEM") and isinstance(getattr(_dm, n_), list)]:
    for _o in getattr(_dm, _nm_v):
        shutil.copyfile(_o, os.path.join(SB, "work", "cunhagens_13out", os.path.basename(_o)))
''', "")
entre("for _o in list(_dm.VERBATIM_ORIGEM) + list(_dm.VERBATIM_ORIGEM_V406) + list(_dm.VERBATIM_ORIGEM_V408):", '"as falas de 03/11 do operador nao estao todas na pasta do sandbox"   # v408: as falas desta versao sao as de 03/11 (as de 02/11 e as anteriores vao junto, para o delta herdado)',
      '''for _nm_v in [n_ for n_ in dir(_dm) if n_.startswith("VERBATIM_ORIGEM") and isinstance(getattr(_dm, n_), (list, tuple))]:   # v408: as falas desta versao sao as de 04/11 (VERBATIM_ORIGEM_V408); as das versoes anteriores que moram em cunhagens_13out vao junto, para os deltas herdados; as de outras pastas vao pelo espelho da casa
    for _o in getattr(_dm, _nm_v):
        if os.path.isfile(_o) and os.path.basename(os.path.dirname(_o)) == "cunhagens_13out":
            shutil.copyfile(_o, os.path.join(SB, "work", "cunhagens_13out", os.path.basename(_o)))
assert all(os.path.isfile(os.path.join(SB, "work", "cunhagens_13out", os.path.basename(_o))) for _o in _dm.VERBATIM_ORIGEM_V408) and len(_dm.VERBATIM_ORIGEM_V408) == len(ESP["cunhagens"]), "as falas de 04/11 do operador nao estao todas na pasta do sandbox (ou ESPERADOS[cunhagens] != delta.VERBATIM_ORIGEM_V408)"''')
linha("# v408 (desvio do molde, dito): o delta_v408 PINA POR ASSERT o manifesto da parametrizacao do teste (d)", "# v408: o delta_v407 herdado PINA POR ASSERT o manifesto da parametrizacao do teste (d) (D_TESTE_MANIFESTO, sha16 da ordem): o sandbox o leva (copia de bytes) na mesma posicao relativa; leva tambem as fontes dos quatro modulos (pedra/)")
sub('for _vv in ("v407", "v405", "v404", "v403", "v402", "v401", "v400", "v399"):', 'for _vv in ("v407", "v406", "v405", "v404", "v403", "v402", "v401", "v400", "v399"):   # v408 (fork B): a v406 entra (o delta_v407 importa o delta_v406; a subida mecanica a tinha deixado de fora)')
sub('''for _vp in ("v407", "v405", "v404", "v403", "v402", "v401", "v399"):
    shutil.copytree(os.path.join(os.path.dirname(PKG), _vp, "pedra"), os.path.join(SB, "work", "cadeia_de_selo", _vp, "pedra"))''',
    '''for _vp in ("v407", "v406", "v405", "v404", "v403", "v402", "v401", "v399"):
    if os.path.isdir(os.path.join(os.path.dirname(PKG), _vp, "pedra")):
        shutil.copytree(os.path.join(os.path.dirname(PKG), _vp, "pedra"), os.path.join(SB, "work", "cadeia_de_selo", _vp, "pedra"))''')
sub('''# v408 (desvio do molde, dito): o BUNDLE_v407.json da COPIA da pasta v407 no sandbox tem de apontar para o MANIFEST da integracao DENTRO do sandbox (o delta_v407 da copia confere por assert que origem_integracao == o MANIFEST relativo a sua propria pasta); so' esse campo e' reescrito
_b6p = os.path.join(SB, "work", "cadeia_de_selo", "v407", "BUNDLE_v407.json"); _b6 = rdj(_b6p); _b6["origem_integracao"] = _man_sb.replace(os.sep, "/")''',
    '''# v408 (fork B; a subida mecanica apontava para o BUNDLE_v407.json, que NAO tem origem_integracao): o BUNDLE_v406.json da COPIA da pasta v406 no sandbox tem de apontar para o MANIFEST da integracao DENTRO do sandbox (o delta_v406 da copia confere por assert que origem_integracao == o MANIFEST relativo a sua propria pasta); so' esse campo e' reescrito
_b6p = os.path.join(SB, "work", "cadeia_de_selo", "v406", "BUNDLE_v406.json"); _b6 = rdj(_b6p); assert "origem_integracao" in _b6, "o BUNDLE_v406.json da copia nao tem origem_integracao"; _b6["origem_integracao"] = _man_sb.replace(os.sep, "/")''')
_R35 = 'shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"))'
sub(_R35, _R35 + '''
# ---- v408 (fork B): o ESPELHO DA CASA -- todo arquivo abaixo de Central de Patentes que a importacao do delta REAL abriu ou conferiu (medido acima, _ACESSOS) vai ao sandbox na MESMA posicao relativa (copia de bytes), se ainda nao estiver la': os deltas herdados (v407 a v399) derivam WK da propria pasta e abrem, ao importar,
# as candidatas de 02/11 (beta_calor_02nov, k_guarda_travessia_02nov, rota_RE_dualidade_02nov, fechamento_02nov), as de 03/11 e 04/11 (pedras_candidatas_03nov, pedras_candidatas_04nov), as falas de 30/10 (experimento_espelho_30out), a da Identidade (cadeia_de_selo405), a decisao das fontes nao publicadas (custodia_G1), o manifesto do teste (d),
# o resultado da Fase 9 V2, o acorde do Kimi... Arquivos fora da casa (o Nos real, a Bancada_Um) sao lidos no lugar, so' leitura; os do proprio pacote (PKG) que faltarem na copia (p. ex. DESENHO_v408.md) vao para PKS. Nenhum arquivo ja' presente no sandbox e' sobrescrito por este espelho.
_CEN_REAL = os.path.dirname(os.path.dirname(PKG))
_ESP_N = 0; _ESP_B = 0; _ESP_LISTA = []
for _p_a in sorted(_ACESSOS):
    if not (_p_a.startswith(_CEN_REAL + os.sep) and os.path.isfile(_p_a)):
        continue
    _dst_a = os.path.join(PKS, os.path.relpath(_p_a, PKG)) if _p_a.startswith(PKG + os.sep) else os.path.join(SB, os.path.relpath(_p_a, _CEN_REAL))
    if os.path.exists(_dst_a):
        continue
    os.makedirs(os.path.dirname(_dst_a), exist_ok=True); shutil.copyfile(_p_a, _dst_a); _ESP_N += 1; _ESP_B += os.path.getsize(_dst_a); _ESP_LISTA.append(os.path.relpath(_p_a, _CEN_REAL))
R["etapas"]["espelho_da_casa"] = {"n_arquivos_copiados": _ESP_N, "bytes": _ESP_B, "n_acessos_medidos": len(_ACESSOS), "arquivos": _ESP_LISTA[:400], "nota": "medido instrumentando open/exists/isfile/isdir/getsize na importacao do delta_v408 real; copia de bytes na mesma posicao relativa; nada digitado; nada sobrescrito"}
print("  espelho da casa (o que o delta e os deltas herdados abrem ao importar): %d arquivos copiados (%d B) de %d acessos medidos" % (_ESP_N, _ESP_B, len(_ACESSOS)))''')
sub('r["manifesto_anterior"] = json.loads(json.dumps(pre["manifesto_anterior"])); r["manifesto_novo"]["deployment_id"] = "B%d-v408-20261103-R1" % n', 'r["manifesto_anterior"] = json.loads(json.dumps(pre["manifesto_anterior"])); r["manifesto_novo"]["deployment_id"] = "B%d-v408-20261104-R1" % n')
# ---- (5) os controles negativos do fechar
entre('_recusa_com_core("fechar_psion_valor_adulterado"', 'lambda c, _ia=_ia: c["kernel_formalization"]["axiom_report"].__setitem__(list(_dm.ANCORAS)[_ia], ["propext", "sorryAx"]))',
      '''_recusa_com_core("fechar_tetelestai_valor_adulterado", "o numero de modulos ok do tetelestai_terminal_v408 adulterado no core (3 de 4)", lambda c: c["tetelestai_terminal_v408"]["values"].__setitem__("n_modulos_ok", 3))
_recusa_com_core("fechar_psion_valor_adulterado", "o numero de modulos ok do psion_canto_v407 (herdado) adulterado no core (8 de 9)", lambda c: c["psion_canto_v407"]["values"].__setitem__("n_modulos_ok", 8))
_recusa_com_core("fechar_fecho406_valor_adulterado", "o numero de modulos ok do fechamento_v406 (herdado) adulterado no core (300 de 301)", lambda c: c["fechamento_v406"]["values"].__setitem__("n_modulos_ok", 300))
_recusa_com_core("fechar_chave_do_lema_false", "a chave do lema (linked_to_the_corner_by_a_lemma) de volta a literal False no core", lambda c: c["testemunha_estatica_v396"]["fock_face"].__setitem__("linked_to_the_corner_by_a_lemma", False))
_recusa_com_core("fechar_fecho_chave_false", "a chave rede_fock_v394.whole_certificate_inhabited de volta a False no core (o literal)", lambda c: c["rede_fock_v394"].__setitem__("whole_certificate_inhabited", False))
_recusa_com_core("fechar_tetelestai_frase_proibida", "uma frase proibida nos limites do tetelestai_terminal_v408", lambda c: c["tetelestai_terminal_v408"]["limites"].append("a TGL nao tem terminal"))
_recusa_com_core("fechar_tetelestai_chave_antiga_mudada", "o registro do terminal diz que uma chave antiga mudou (chaves_antigas_que_mudam nao vazia; controle extra do fork B)", lambda c: c["tetelestai_terminal_v408"]["chaves_antigas_que_mudam"].append("rede_fock_v394.whole_certificate_inhabited"))
_recusa_com_core("fechar_psion_adulterado", "numero do Ponto Zero do Psion (recriado) adulterado no core (hbar omega)", lambda c: c["ponto_zero_do_psion_v405"]["values"].__setitem__("hbar_omega_meV", 17.5))
_recusa_com_core("fechar_f2b_adulterado", "numero da errata de F2b adulterado no core (a previsao do par)", lambda c: c["f2b_errata_v404"]["values"].__setitem__("previsao_do_par", 0.1))
_recusa_com_core("fechar_f2b_canal_ainda_awaiting", "o canal F2b ainda AWAITING no core (a retirada nao aconteceu)", lambda c: c["f2b_errata_v404"].__setitem__("F2b_status_now", "AWAITING"))
_recusa_com_core("fechar_v1_reescrito", "o V1 do ramo B reescrito no core (F2b_status do registro da v386)", lambda c: c["ramo_b_preregistration_v386"].__setitem__("F2b_status", "WITHDRAWN"))
_recusa_com_core("fechar_angle_status_reescrito", "o texto antigo de neutrino_mass.angle_status reescrito no core (a errata e' ao lado)", lambda c: c["neutrino_mass"].__setitem__("angle_status", "sin(45deg) agora e DERIVADO"))
_recusa_com_core("fechar_gate_adulterado", "numero do gate (recriado) adulterado no core (17 calculadas)", lambda c: c["bandeiras_do_gate_v403"]["values"].__setitem__("n_calculated", 17))
_recusa_com_core("fechar_bandeira_do_gate_false", "uma bandeira calculada do gate (linearized_spin2_finite_face) False no core", lambda c: c["qg_closure"]["physics_flags"].__setitem__("linearized_spin2_finite_face", False))
_recusa_com_core("fechar_caminho_v407_adulterado", "numero do caminho da v403 (recriado) adulterado no core (energia minima do nucleo)", lambda c: c["caminho_v403"]["values"].__setitem__("min_core_energy", 0.31))
_recusa_com_core("fechar_ponte_v402_adulterada", "numero da ponte da v402 (recriada) adulterado no core", lambda c: c["ponte_da_escala_dual_v402"]["values"].__setitem__("min_null_energy_shift", 0.31))
# a PORTA do paragrafo novo isolada: T.paragrafo_v408() da copia do sandbox tem de LEVANTAR com o numero de modulos do terminal adulterado no core (a verificacao compara com os numeros de ESPERADOS e de delta_v408)
cj = json.loads(raw_core.decode("utf-8")); cj["core"]["tetelestai_terminal_v408"]["values"]["n_modulos_ok"] = 3
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
import importlib.util as _iu1
_sp1 = _iu1.spec_from_file_location("textos_sb1", os.path.join(POS, "textos_v408.py")); _t1 = _iu1.module_from_spec(_sp1); _sp1.loader.exec_module(_t1)
try:
    _t1.paragrafo_v408(); _levanta1 = False
except Exception as _ex1:   # noqa: BLE001
    _levanta1 = isinstance(_ex1, AssertionError)
NEG.append({"controle": "a porta do paragrafo novo (paragrafo_v408, chamada pelo fechar) levanta com o numero de modulos do tetelestai_terminal_v408 adulterado", "rc": 2 if _levanta1 else 0, "recusou": _levanta1, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v408-custodia.md"))})
open(core_p, "wb").write(raw_core)
_recusa_com_core("fechar_direcao_invertida", "a direcao do testemunho invertida no core (a IALD como quem testifica do operador; declaracao da v399 recriada)", lambda c: c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"].__setitem__("a_IALD", "testifica do operador"))
_recusa_com_core("fechar_inscricao_nao_embutida", "uma inscricao de 04/11 deixou de estar embutida no core (cunhagens_v408)", lambda c: list(c["cunhagens_v408"]["verbatim"].values())[0].__setitem__("embedded_ok", False))
_recusa_com_core("fechar_sem_errata_e21", "a errata E21 ausente do registro cunhagens_v408 (restam E22 e E23)", lambda c: c["cunhagens_v408"]["erratas"].pop(0))
_recusa_com_core("fechar_sem_decisao_d54", "a decisao D54 da gerencia ausente do registro cunhagens_v408", lambda c: c["cunhagens_v408"]["extras"]["decisoes"].pop("D54"))
_recusa_com_core("fechar_leitura_sem_onto", "a leitura de 04/11 dita [REAL] no core (e' ONTO)", lambda c: c["cunhagens_v408"]["extras"]["leituras"].__setitem__("estatuto", "[REAL]"))
_recusa_com_core("fechar_cunhagens_v407_sem_e21_ao_lado", "a errata E21 ao lado de cunhagens_v407 (herdada, recriada) ausente do core", lambda c: c["cunhagens_v407"]["erratas"].pop())
_recusa_com_core("fechar_pedra_v403_adulterada", "a pedra selada da v403 (Caminho) adulterada no hash formal do core", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/Caminho.lean", "0" * 64))
for _nm_a in list(_dm.ANCORAS_PRINCIPAIS):
    _recusa_com_core("fechar_ancora_%s_fora_do_trio" % _nm_a.split(".")[-1], "a ancora principal %s fora do trio no core" % _nm_a, lambda c, _n=_nm_a: c["kernel_formalization"]["axiom_report"].__setitem__(_n, ["propext", "sorryAx"]))''')
sub('print("  paragrafo novo (o psion, o canto e o par) e nota ao lado dos anteriores no handoff:', 'print("  paragrafo novo (Tetelestai e\' o terminal) e nota ao lado dos anteriores no handoff:')
# ---- (6) a limpeza guarda TODAS as saidas dos controles
entre('    for nome in ("fechar_out.txt", "fechar_sem_religamento_out.txt",', '"fechar_stub_out.txt", "registrar_mapa_out.txt"):',
      '    for nome in sorted(f_ for f_ in os.listdir(SB) if f_.endswith("_out.txt") or (f_.startswith("b3_") and f_.endswith((".txt", ".json")))):   # v408 (fork B): TODAS as saidas dos controles e do b3 (a lista fixa do molde deixava de fora os controles novos)')
# ---- o veredito
sub("o da v408 (o psion, o canto e o par) pela verificacao propria; a nota ao lado do paragrafo da v407;", "o da v408 (Tetelestai e' o terminal) pela verificacao propria; a nota ao lado do paragrafo da v407 (E21);")
sub("os diffs (os 9 modulos novos), o manifesto ", "os diffs (os modulos novos do bundle), o manifesto ")
sub("com um numero do psion_canto_v407, do fechamento_v406 herdado, do Ponto Zero do Psion,", "com um numero do tetelestai_terminal_v408, do psion_canto_v407 herdado, do fechamento_v406 herdado, do Ponto Zero do Psion,")
sub("com a direcao do testemunho invertida, com uma inscricao rotulada como da gerencia, ", "com a direcao do testemunho invertida, com uma inscricao de 04/11 nao embutida, com uma chave antiga dita mudada, ")
sub("com uma errata ou decisao a menos, com a leitura de 03/11 dita REAL, com a chave do lema de volta a False, com uma pedra selada da v407 adulterada, com uma pedra fora do trio e com o sidecar adulterado ou ausente;",
    "com a errata E21 ou a decisao D54 a menos (e com a E21 ao lado da cunhagens_v407 herdada ausente), com a leitura de 04/11 dita REAL, com a chave do lema de volta a False, com uma pedra selada da v403 adulterada, com uma ancora principal fora do trio e com o sidecar adulterado ou ausente;")
assert "# [A ADAPTAR v408]" not in t and "[ADAPTADO v408, 03/11/2026" not in t and "psion_canto_v407\"][\"values\"][\"n_modulos_ok\"] = 8" not in t and "_dm.ANCORA_LEMA" not in t and "VERBATIM_ORIGEM_V406) + list" not in t
novo = t.encode("utf-8"); assert novo != raw
ast.parse(t)
bak = P + ".bak_" + TS + "_adapt"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
tmp = P + ".tmp_adapt"; open(tmp, "wb").write(novo); assert os.path.getsize(tmp) == len(novo); os.replace(tmp, P); assert open(P, "rb").read() == novo
print("harness_fechar_sandbox_v408.py %d troca(s): %d B -> %d B sha16 %s -> %s (%s; ast ok; backup %s)" % (n, len(raw), len(novo), s16(raw), s16(novo), "CRLF" if NL == "\r\n" else "LF", os.path.basename(bak)))
