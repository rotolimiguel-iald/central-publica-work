# -*- coding: utf-8 -*-
"""9a afericao no GERADOR DO PRE-REGISTRO (script salvo; count == 1; backup de BYTES feito e conferido AQUI):
- 6N25/9N11: a nota antiga diz o seu ESCOPO (d = 64); a frase entre parenteses da nota por d e custo passa a ser GERADA dos numeros (se a corrente e' a mais
  lenta nos pontos fora da margem: «o orcamento (a corrente x1,25) cobre uma rodada ate 25% mais lenta que ela, nao mais»; senao, os pontos em que nao e');
  o cabecalho do paragrafo no MD diz que a lista e' de d = 64 e a nota cobre d = 8 a 64;
- 9N3/9N12: o MD mostra o transcrito lido (caminho, de_teste, linhas e sha256, tamanho);
- 9N0/9N13: TODAS as guardas antes de qualquer movimento na pasta; o MD e a pasta de evidencias de uma tentativa INTERROMPIDA (sem o JSON) vao para o lado
  (.incompleto_<data>), nunca apagados; com o JSON (o V1 ja congelado e igual), os dois tem de conferir;
- 9N1: o temporario que nao puder ser removido vira AVISO, e a excecao ORIGINAL e' a relancada;
- 9N7/9N15: o texto do lancador: o aviso do TaskStop volta para junto do aborto; o .fase0 dito como e'; o PID ate o fim da restauracao; o codigo 17; a espera
  de 60 s com a mesma consulta; a contagem ilegivel;
- 9N16: o gerador RECUSA rodar com -O/PYTHONOPTIMIZE (as guardas sao assert)."""
import ast, hashlib, os, time
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert hashlib.sha256(raw).hexdigest().startswith("26aba67a2b7ceb74"), "o gerador nao e' o auditado na 9a (26aba67a)"
bak = P + ".bak_antes_afer9_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
PAIRS = [
    # 9N16
    ('''sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TRANS = ''', '''sys.stdout.reconfigure(encoding="utf-8")
if sys.flags.optimize:   # as guardas deste gerador sao assert: com -O elas sumiriam sem aviso (9a afericao)
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")
HERE = os.path.dirname(os.path.abspath(__file__))
TRANS = '''),
    # 6N25/9N11: o escopo da nota antiga
    ('''"%.3f (instancia) -- a margem x%.2f %s a maior sobre a corrente e %s a dispersao maior/menor; nao foi medida sob a carga do rito") % (''',
     '''"%.3f (instancia) -- em d = 64, a margem x%.2f %s a maior sobre a corrente (instancia e injecao do T1) e %s a dispersao maior/menor da INSTANCIA (os "
                                            "outros pontos e custos: a nota por d e por custo); nao foi medida sob a carga do rito") % ('''),
    # 6N25/9N11: a frase gerada dos numeros
    ('''    "%s; a sonda corrente e' a mais lenta de todas em %s; a maior sobre a menor passa da margem em %s -- nesses pontos a margem NAO cobre a dispersao entre "
    "rodadas (a corrente sendo a mais lenta ali, o orcamento ja usa o pior caso medido; uma rodada mais lenta que todas as sondas nao esta coberta)") % (
    len(_SOND), _pdc_mc["_mc"], _pdc_mc["d"], _pdc_mc["custo"], MARGEM,
    ("cobre a maior sobre a corrente em todo d e custo" if not _pdc_fora_mc else "NAO cobre a maior sobre a corrente em " + _fmt_pdc(_pdc_fora_mc, "_mc")),
    ("d = " + ", ".join(str(x) for x in _pdc_lenta) if _pdc_lenta else "nenhum d"),
    (_fmt_pdc(_pdc_fora_mm, "_mm") if _pdc_fora_mm else "nenhum ponto"))''',
     '''    "%s; a sonda corrente e' a mais lenta de todas em %s; a maior sobre a menor passa da margem em %s") % (
    len(_SOND), _pdc_mc["_mc"], _pdc_mc["d"], _pdc_mc["custo"], MARGEM,
    ("cobre a maior sobre a corrente em todo d e custo" if not _pdc_fora_mc else "NAO cobre a maior sobre a corrente em " + _fmt_pdc(_pdc_fora_mc, "_mc")),
    ("d = " + ", ".join(str(x) for x in _pdc_lenta) if _pdc_lenta else "nenhum d"),
    _frase_mm_)'''),
    ('''_fmt_pdc = lambda xs, k: ", ".join("d = %d %s (%.3f)" % (x["d"], x["custo"], x[k]) for x in xs)
''', '''_fmt_pdc = lambda xs, k: ", ".join("d = %d %s (%.3f)" % (x["d"], x["custo"], x[k]) for x in xs)
_pdc_mm_nao_lenta = [x for x in _pdc_fora_mm if x["_mc"] > 1.0 + 1e-12]   # 9a afericao: a frase sai dos numeros, nunca fixa
_frase_mm_ = ("nenhum ponto" if not _pdc_fora_mm else _fmt_pdc(_pdc_fora_mm, "_mm") + " -- nesses pontos a margem NAO cobre a dispersao entre rodadas" + (
    ("; neles a sonda corrente e' a mais lenta medida, e o orcamento (a corrente x%.2f) cobre uma rodada ate %.0f%% mais lenta que ela, nao mais" % (MARGEM, 100.0 * (MARGEM - 1.0)))
    if not _pdc_mm_nao_lenta else ("; a sonda corrente NAO e' a mais lenta em " + _fmt_pdc(_pdc_mm_nao_lenta, "_mc") + " (maior sobre a corrente)")))
'''),
    # o cabecalho do paragrafo no MD
    ('''"Variabilidade das sondas de tempo (d = 64; s por instância / por injeção do T1): "''',
     '''"Variabilidade das sondas de tempo (a lista: d = 64, s por instância / por injeção do T1; a nota por d e por custo cobre d = 8 a 64): "'''),
    # 9N3/9N12: o transcrito no MD
    ('''      RAT["rascunho_apresentado"]["gerado_utc"], RASCUNHO_SPEC, "a mesma" if RAT["a_especificacao_ratificada_e_a_do_rascunho"] else "OUTRA"))
''', '''      RAT["rascunho_apresentado"]["gerado_utc"], RASCUNHO_SPEC, "a mesma" if RAT["a_especificacao_ratificada_e_a_do_rascunho"] else "OUTRA"))
    _tr_ = RAT.get("transcrito") or {}
    A("- transcrito lido: `%s` (de_teste = %s; %d linha(s) da mensagem, sha256 %s — a linha sem o fim de linha; tamanho na leitura: %s bytes)" % (
      _tr_.get("caminho"), _tr_.get("de_teste"), _tr_.get("linhas_da_mensagem") or 0, ", ".join("`%s`" % x for x in (_tr_.get("sha256_das_linhas_da_mensagem") or [])),
      _tr_.get("tamanho_do_transcrito_na_leitura_bytes")))   # 9a afericao
'''),
    # 9N7/9N15: o texto do lancador
    ('''o PID do lançador fica em .rito_v384.pid, gravado logo depois da guarda (com outro lançador vivo, RECUSA — código 16), e abortar o rito é kill -TERM nesse PID NO GIT BASH, conferindo antes que /proc/<pid>/cmdline contém rito_v384 (é PID do MSYS, não do Windows; não no PowerShell); o log da tentativa e o registro dos sinais só giram (para .anterior) depois da última recusa — o TaskStop da ferramenta da gerência NÃO para o lançador''',
     '''o PID do lançador fica em .rito_v384.pid, gravado logo depois da guarda e só removido no FIM da restauração (com outro lançador vivo, RECUSA — código 16), e abortar o rito é kill -TERM nesse PID NO GIT BASH, conferindo antes que /proc/<pid>/cmdline contém rito_v384 (é PID do MSYS, não do Windows; não no PowerShell) — o TaskStop da ferramenta da gerência NÃO para o lançador; a tentativa escreve num log próprio (.fase0; o de uma tentativa anterior vai para .fase0.anterior) e só depois da última recusa o log real da rodada anterior e o registro dos sinais vão para .anterior e o da tentativa toma o lugar do real (se um desses giros falhar, FALHA VISÍVEL e RECUSA — código 17); o log de uma tentativa recusada fica no .fase0'''),
    ('''e espera até 60 s que nenhuma parada esteja em curso antes de religar (com AVISO no log se expirar; depois de um AVISO, o marcador só sai se a porta ainda escutar 30 s depois e nenhuma parada — Stop-ScheduledTask ou stop_iald_llama.ps1 — estiver em curso)''',
     '''e espera até 60 s que nenhuma parada (Stop-ScheduledTask da tarefa ou stop_iald_llama.ps1) esteja em curso antes de religar (com AVISO no log se expirar; depois de um AVISO, o marcador só sai se a porta ainda escutar 30 s depois e nenhuma dessas paradas estiver em curso — com a contagem ilegível, o marcador fica)'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:160])
    s = s.replace(old, new)
# 9N0/9N13/9N1: o bloco das guardas e da gravacao, trocado inteiro (entre os dois marcos, conferidos)
i0 = s.index('PMD = BASE + ".md"\n'); i1 = s.index('print("versao", VER, "escolha", ESCOLHA)')
velho = s[i0:i1]
for marco in ('_orf = PMD + ".incompleto_"', '# SO AGORA, com todas as guardas passadas', '_tmpd = _dd + ".tmp_"', 'for _pth, _b in ((PMD, md), (PJSON, raw)):', 'os.remove(_pth + ".tmp")'):
    assert velho.count(marco) == 1, marco
NOVO = '''PMD = BASE + ".md"
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
'''
s = s[:i0] + NOVO + s[i1:]
ast.parse(s)
b = s.encode("utf-8")
for i in range(40):
    try:
        open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P); break
    except PermissionError:
        time.sleep(0.5)
assert open(P, "rb").read() == b
print("ok", len(PAIRS) + 1, hashlib.sha256(b).hexdigest()[:16], "| backup", os.path.basename(bak))
