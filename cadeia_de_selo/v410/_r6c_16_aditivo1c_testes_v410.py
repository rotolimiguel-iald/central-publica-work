# -*- coding: utf-8 -*-
"""_r6c_16_aditivo1c_testes_v410.py -- ADITIVO 1 a ordem do conserto unico, parte C (gerencia c1, 10/11/2026; com o ADITIVO 2), FORA do candidato:
«O harness do fechar e o dos textos cobrem os dois blocos e o passo novo, com controle negativo (um passo anterior falso: o gatilho nao e' escrito).»
 1. pos_rito\\teste_textos_custodia_sem_candidato_v410.py: os DOIS blocos do README (README_FRENTE e README_O_QUE_SAI) passam, cada um SOZINHO, pelas MESMAS guardas (junto dos sete textos e da secao README, nas duas variantes da revisao);
    secao nova: o orcamento, as formas por constante, os tres teoremas ratificados, os marcadores do molde, montar_blocos (os NOVE corpos pelas regex do leitor do G1; os dois blocos em marcador proprio, depois do README_EVIDENTE) e dez controles negativos;
 2. pos_rito\\harness_textos_ensaio_v410.py: etapa nova (blocos_do_readme_e_gatilho_da_custodia), depois da etapa custodia_g1_le_os_textos: roda o teste dos textos e o teste do gatilho (teste_gatilho_custodia_sem_candidato_v410.py) em SANDBOX,
    com o Nos EMULADO do harness e o handoff RENDERIZADO por ele;
 3. pos_rito\\harness_fechar_sandbox_v410.py: etapa nova (a mesma), depois da 2e e ANTES da 2d (o fechar com stubs regrava o handoff do Nos do sandbox): o Nos do sandbox e o HANDOFF que o fechar (positivo) gravou nele.
O gatilho de verdade (ORDEM_HANDOFF_CUSTODIA_v410.md na raiz do pacote) nunca e' escrito por teste nenhum: o destino do teste e' sempre dentro da pasta de saida do harness, e o teste confere isso no fim.
Idempotente; backup de BYTES ao lado (.bak_<TS>_aditivo1c); temporario + os.replace; ast.parse. (Escrito pelo Write: o heredoc do Bash colapsa as barras.)"""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); POS = os.path.join(HERE, "pos_rito"); TS = time.strftime("%Y%m%d_%H%M%S")
RES = {}


def aplica(nome, f_):
    p = os.path.join(POS, nome); b0 = open(p, "rb").read(); assert b"\r\n" not in b0, (nome, "CRLF inesperado")
    t1 = f_(b0.decode("utf-8")); ast.parse(t1); b1 = t1.encode("utf-8")
    if b1 != b0:
        bak = p + ".bak_" + TS + "_aditivo1c"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
        tmp = p + ".tmp_r6c"; open(tmp, "wb").write(b1); assert os.path.getsize(tmp) == len(b1) > len(b0); os.replace(tmp, p); assert open(p, "rb").read() == b1
    RES[nome] = "MUDOU (%d -> %d B)" % (len(b0), len(b1)) if b1 != b0 else "igual (ja' feito)"


def um(t, a, b):
    assert t.count(a) == 1, ("contagem", t.count(a), a[:120]); return t.replace(a, b)


# ---------------------------------------------------------------- 1. o teste dos textos da custodia, sem candidato
BLOCO_T = r'''# (ADITIVO 1, parte C, e ADITIVO 2 a ordem do conserto unico; 10/11/2026: a custodia da v410 e' AUTOMATICA) os DOIS blocos do README para a custodia (README_FRENTE e README_O_QUE_SAI): cada um passa SOZINHO pelas MESMAS guardas (a guarda das frases da v410,
# o portao do G1 e a forma); o README_FRENTE cabe no orcamento; as formas ratificadas vem por constante do delta; os tres teoremas da escala sao nomes ratificados pelo operador; os marcadores do molde do README ficam literais; montar_blocos poe os dois, cada um
# no seu marcador (SEM o prefixo PARAGRAFO_), DEPOIS do paragrafo README_EVIDENTE, e as regex do leitor do G1 leem os NOVE corpos, iguais as constantes, sem marcador sem par; os controles negativos TEM de reprovar.
from custodia_g1 import nos as NOSG1  # noqa: E402
G = {"REV": None, "N": N, "DL": DL, "GF": GF, "TX": TX, "re": re}
exec(compile(src[i0:i1], "textos_custodia_handoff_v410.py[textos]", "exec"), G)
BL = G["BLOCOS_README"]; RF, RS = dict(BL)["README_FRENTE"], dict(BL)["README_O_QUE_SAI"]; PA = G["README_PONTEIRO_ABSTRACT"]; nb_ = lambda s_: len(s_.encode("utf-8"))
gb_, fb_ = G["guardas_dos_textos"](BL, {N["pin"]})
for x_ in fb_:
    print("  REPROVADO:", x_)
cb1_ = bool([i_ for i_, _ in BL] == ["README_FRENTE", "README_O_QUE_SAI"] and not fb_ and all(gb_[i_]["guarda_frases_v410"] == [] and gb_[i_]["portao_g1"] == [] and gb_[i_]["forma"] == [] for i_, _ in BL))
print("blocos do README (ADITIVOS 1 e 2): README_FRENTE (%d bytes em UTF-8; teto %d) e README_O_QUE_SAI (%d bytes; a linha de ponteiro, %d bytes), cada um SOZINHO pela guarda das frases da v410, pelo portao do G1 e pela forma: %s" % (nb_(RF), G["README_FRENTE_TETO_B"], nb_(RS), nb_(PA), cb1_)); ok = ok and cb1_
cb2_ = bool(nb_(RF) <= G["README_FRENTE_TETO_B"] and all(G[k_] in RF for k_ in ("D81_EN", "D81_PT", "CLAY_EN", "CLAY_PT", "UMH_EN", "UMH_PT", "OBR_EN", "OBR_PT", "_H0_EN", "_H0_PT"))
            and (G["D81_EN"], G["D81_PT"], G["CLAY_EN"], G["CLAY_PT"], G["OBR_EN"], G["OBR_PT"]) == (DL.FRASE_D81_EN, DL.FRASE_D81_PT, DL.FRASE_CLAY_CANONICA_EN, DL.FRASE_CLAY_CANONICA_PT, DL.FRASE_H0DN_OBRIGATORIA_EN, DL.FRASE_H0DN_OBRIGATORIA_PT)
            and all(RF.count("`" + n_ + "`") == 2 and n_ in DL.NOMES_RATIFICADOS_R6_AESCALA for n_ in G["_RF_NOMES"]) and "it was not opened" in RF and "não foi aberto" in RF and "accreditation" in RF
            and RF.count("{{url:estado}}") == 1 and RS.endswith(PA) and PA.startswith("## Abstract\n\n") and PA.count("{{url:abstract}}") == 1 and "PARAGRAFO_" not in RF + RS and "%" not in RF + RS and "\r" not in RF + RS)
print("blocos do README: o README_FRENTE cabe no orcamento e traz, por constante, a forma da D81, a forma canonica do Clay, a frase do habitante unico e a frase obrigatoria do H0DN (PT e EN), o teste dito NAO aberto, os tres teoremas da escala ratificados (uma vez em cada lingua) e o marcador {{url:estado}}; "
      "o README_O_QUE_SAI termina na linha de ponteiro, com {{url:abstract}}: %s" % cb2_); ok = ok and cb2_
HS_ = "# HANDOFF (sintetico)\n" + G["montar_blocos"](G["TEXTOS"], G["README_EVIDENTE"], BL, "v410")
corp_ = {m_.group("id"): m_.group("corpo") for m_ in NOSG1.RE_MARCADOR.finditer(HS_)}; semp_ = sorted(set(NOSG1.RE_ABRE.findall(HS_)) ^ set(NOSG1.RE_FECHA.findall(HS_)))
pos_ = [HS_.find(s_) for s_ in ("<!-- FIM_COMMIT_v410 -->", "**README: o que fica evidente**", "<!-- INICIO_README_FRENTE_v410 -->", "<!-- FIM_README_FRENTE_v410 -->", "<!-- INICIO_README_O_QUE_SAI_v410 -->", "<!-- FIM_README_O_QUE_SAI_v410 -->")]
cb3_ = bool(not semp_ and len(corp_) == len(G["TEXTOS"]) + len(BL) == 9 == len(NOSG1.RE_ABRE.findall(HS_)) and all(corp_.get("%s_v410" % i_, "").strip("\n") == t_ for i_, t_ in G["TEXTOS"] + BL) and all(p_ >= 0 for p_ in pos_) and pos_ == sorted(pos_)
            and "PARAGRAFO_README_FRENTE" not in HS_ and "PARAGRAFO_README_O_QUE_SAI" not in HS_)
print("blocos do README no handoff (montar_blocos): os NOVE corpos lidos pelas regex do leitor do G1, iguais as constantes, nenhum marcador sem par; os dois blocos em marcador proprio (sem o prefixo PARAGRAFO_), DEPOIS do paragrafo README_EVIDENTE, nesta ordem: %s" % cb3_); ok = ok and cb3_
negb = [("FRENTE_SEM_QUALIFICADOR", "README_FRENTE", "## P = nP and the Clay question, in the kernel\n\n**The theorem:** P = nP."),
        ("FRENTE_SEM_D81_E_SEM_HABITANTE", "README_FRENTE", RF.replace(G["D81_EN"], "P = nP").replace(G["D81_PT"], "P = nP").replace(G["UMH_EN"], "").replace(G["UMH_PT"], "")),
        ("FRENTE_COM_A_PALAVRA_RECUSADA", "README_FRENTE", RF + "\n\nThe scale is " + "CONF" + "IRMED in nature."),
        ("FRENTE_PROVED_SEM_ESTATUTO", "README_FRENTE", RF + "\n\nThe constant of the scale is proved."),
        ("FRENTE_H0DN_SEM_OBRIGACAO", "README_FRENTE", RF.replace(G["OBR_EN"], "it is registered").replace(G["OBR_PT"], "está registrado")),
        ("FRENTE_CLAY_RESOLVIDO_A_SECO", "README_FRENTE", RF + "\n\nThe Clay problem is resolved."),
        ("FRENTE_5_SIGMA_ATINGIDO", "README_FRENTE", RF + "\n\nThe H0DN result: 5σ reached."),
        ("O_QUE_SAI_TITULO_SEM_QUALIFICADOR", "README_O_QUE_SAI", RS + " O bloco de hoje tem o título “P = nP and the Clay question”."),
        ("O_QUE_SAI_DEMERITO_DA_RETRODICAO", "README_O_QUE_SAI", RS + " O teste é pós-" + "dição."),
        ("O_QUE_SAI_D59", "README_O_QUE_SAI", RS + " A entrega do " + "Ki" + "mi fica fora.")]
for nome_, id_, t_ in negb:
    _, f_ = G["guardas_dos_textos"]([(id_, t_)], {N["pin"]})
    print("controle negativo (blocos do README) %-34s reprovou: %s" % (nome_, bool(f_))); ok = ok and bool(f_)
hq_ = HS_.replace("<!-- FIM_README_FRENTE_v410 -->", "")
cq_ = bool(sorted(set(NOSG1.RE_ABRE.findall(hq_)) ^ set(NOSG1.RE_FECHA.findall(hq_))) == ["README_FRENTE_v410"])
print("controle negativo (blocos do README) o marcador do README_FRENTE sem par e' visto pelas regex do leitor do G1: %s" % cq_); ok = ok and cq_
'''


def f_teste(t):
    if "os DOIS blocos do README para a custodia (README_FRENTE e README_O_QUE_SAI)" in t:
        return t
    t = um(t, '    g_, f_ = G["guardas_dos_textos"](G["TEXTOS"] + [("README_EVIDENTE", G["README_EVIDENTE"])], {N["pin"]})\n    print("REV=%s: %d textos; reprovados: %d" % ("aprovada" if REV else "ausente", len(G["TEXTOS"]), len(f_)))\n',
           '    g_, f_ = G["guardas_dos_textos"](G["TEXTOS"] + [("README_EVIDENTE", G["README_EVIDENTE"])] + G["BLOCOS_README"], {N["pin"]})   # (ADITIVOS 1 e 2) os dois blocos do README passam, cada um sozinho, pelas MESMAS guardas\n'
           '    print("REV=%s: %d textos, a secao README e os %d blocos do README; reprovados: %d" % ("aprovada" if REV else "ausente", len(G["TEXTOS"]), len(G["BLOCOS_README"]), len(f_)))\n')
    t = um(t, '# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B] N sintetico com as chaves da escala (D86/D87)',
           "# [ADAPTADO v410, 10/11/2026, claude-construtor-v410; ADITIVOS 1 e 2 a ordem do conserto unico] os DOIS blocos do README para a custodia automatica (README_FRENTE e README_O_QUE_SAI) passam, cada um SOZINHO, pelas MESMAS guardas; a secao nova (no fim) confere o orcamento, as formas por constante, os marcadores e dez controles negativos.\n"
           '# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B] N sintetico com as chaves da escala (D86/D87)')
    return um(t, 'print("RESULTADO:", "PASSOU" if ok else "REPROVOU")\n', BLOCO_T + 'print("RESULTADO:", "PASSOU" if ok else "REPROVOU")\n')


# ---------------------------------------------------------------- 2 e 3. os dois harness: a etapa nova (a mesma; so' mudam o Nos emulado, o ESPERADOS, o handoff de base e a pasta de saida)
BLOCO_H = r'''# ---- @@ROTULO@@ (ADITIVOS 1 e 2 a ordem do conserto unico, gerencia c1, 10/11/2026: a custodia da v410 e' AUTOMATICA) os DOIS blocos do README (README_FRENTE e README_O_QUE_SAI) e o passo FINAL do orquestrador (S9_gatilho_custodia):
# (a) teste_textos_custodia_sem_candidato_v410.py: os sete textos, a secao README e os dois blocos do README, cada um SOZINHO pelas MESMAS guardas (a guarda das frases da v410 e o portao do G1), com os controles negativos;
# (b) teste_gatilho_custodia_sem_candidato_v410.py, em SANDBOX: @@O_QUE_EMULA@@, com os textos da custodia acrescentados pela mesma funcao do gerador (montar_blocos);
#     o orquestrador REAL (s9_gatilho_custodia) escreve o gatilho SO' no sandbox e, com um passo anterior falso (e os demais controles negativos), NAO escreve.
# O gatilho de verdade (ORDEM_HANDOFF_CUSTODIA_v410.md na raiz do pacote) nunca e' escrito por este harness: o destino e' sempre dentro da pasta de saida, e o teste confere isso no fim.
def _etapa_gatilho_custodia():
    _GC = {"ok": False}
    try:
        _gd = os.path.join(OUT, "@@PASTA@@"); shutil.rmtree(_gd, ignore_errors=True); os.makedirs(_gd)
        _env = dict(os.environ, PYTHONIOENCODING="utf-8"); _arg = ["--nos-emulado", @@NOS@@, "--esperados", @@ESPERADOS@@]@@HANDOFF_BASE@@
        _r1 = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "teste_textos_custodia_sem_candidato_v410.py")], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env, timeout=1800)
        open(os.path.join(_gd, "teste_textos_custodia_out.txt"), "w", encoding="utf-8").write((_r1.stdout or "") + "\n--- stderr ---\n" + (_r1.stderr or ""))
        _r2 = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "teste_gatilho_custodia_sem_candidato_v410.py"), _gd] + _arg, cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env, timeout=1800)
        open(os.path.join(_gd, "teste_gatilho_custodia_out.txt"), "w", encoding="utf-8").write((_r2.stdout or "") + "\n--- stderr ---\n" + (_r2.stderr or ""))
        _pj = os.path.join(_gd, "TESTE_GATILHO_CUSTODIA_v410.json"); _rj = json.load(open(_pj, encoding="utf-8")) if os.path.exists(_pj) else {}
        _cs = _rj.get("casos") or {}; _l1 = [l_ for l_ in (_r1.stdout or "").splitlines() if l_.startswith(("blocos do README", "controle negativo (blocos do README)"))]
        _GC.update(textos_rc=_r1.returncode, textos_resultado=((_r1.stdout or "").strip().splitlines() or [""])[-1][:120], blocos_do_readme=[l_[:300] for l_ in _l1], gatilho_rc=_r2.returncode, gatilho_modo=_rj.get("modo"), gatilho_handoff_de_base=_rj.get("handoff_de_base"),
                   gatilho_casos=_rj.get("n_casos"), gatilho_negativos=_rj.get("n_negativos"), gatilho_positivo=_cs.get("positivo"), gatilho_passo_anterior_falso=_cs.get("negativo: um passo anterior FALSO (S5_cadeia_0_10)"),
                   gatilho_reprovados=sorted(k_ for k_, v_ in _cs.items() if not (v_ or {}).get("ok")), seguranca=_rj.get("seguranca"), readme_frente_bytes_utf8=_rj.get("readme_frente_bytes_utf8"),
                   gatilho_de_verdade_existe=os.path.exists(os.path.join(PKG, "ORDEM_HANDOFF_CUSTODIA_v410.md")), saida=_gd)
        _GC["ok"] = bool(_r1.returncode == 0 and _GC["textos_resultado"].startswith("RESULTADO: PASSOU") and len(_l1) >= 14 and all(l_.rstrip().endswith("True") for l_ in _l1)
                         and _r2.returncode == 0 and _rj.get("tudo_passou") is True and _rj.get("modo") == "emulado" and (_GC["gatilho_positivo"] or {}).get("ok") is True and (_GC["gatilho_passo_anterior_falso"] or {}).get("ok") is True
                         and not _GC["gatilho_reprovados"] and (_rj.get("n_negativos") or 0) >= 15 and _rj.get("seguranca") is True)
        if not _GC["ok"]:
            falha("os dois blocos do README ou o gatilho da custodia (S9_gatilho_custodia, em sandbox): textos rc %s (%s); gatilho rc %s, modo %s, reprovados %s; saidas em %s | %s" % (_r1.returncode, _GC["textos_resultado"], _r2.returncode, _rj.get("modo"), _GC["gatilho_reprovados"][:4], _gd,
                                                                                                                                                                         ((_r2.stdout or "") + (_r2.stderr or ""))[-500:].replace(chr(10), " | ")))
    except Exception as ex:  # noqa: BLE001
        _GC["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:300]); falha("os dois blocos do README e o gatilho da custodia: %s" % _GC["erro"])
    R["etapas"]["blocos_do_readme_e_gatilho_da_custodia"] = _GC
    print("  os dois blocos do README (cada um sozinho nas guardas) e o gatilho da custodia em sandbox (o orquestrador real; %s casos, %s negativos; um passo anterior falso: o gatilho NAO e' escrito): %s" % (_GC.get("gatilho_casos"), _GC.get("gatilho_negativos"), "ok" if _GC["ok"] else "FALHOU"))


_etapa_gatilho_custodia()
'''


def bloco_h(rotulo, o_que_emula, pasta, nos, esperados, handoff_base):
    b = BLOCO_H
    for a_, v_ in (("@@ROTULO@@", rotulo), ("@@O_QUE_EMULA@@", o_que_emula), ("@@PASTA@@", pasta), ("@@NOS@@", nos), ("@@ESPERADOS@@", esperados), ("@@HANDOFF_BASE@@", handoff_base)):
        assert b.count(a_) == 1, a_; b = b.replace(a_, v_)
    assert "@@" not in b; return b


def f_textos(t):
    if "def _etapa_gatilho_custodia():" in t:
        return t
    anc = 'if not _g1.get("ok"):\n    falha("a custodia G1 nao le o bloco da linhagem ou o handoff da v410: %s" % _g1)\n'
    b = bloco_h("3b.", "o Nos EMULADO deste harness (um.py, selo, core e stdout do rito, por COPIA) e o handoff RENDERIZADO aqui (RENDER[\"handoff\"], gravado na pasta de saida)", "gatilho_custodia", "NOSE", 'os.path.join(PKG, "ESPERADOS_v410.json")',
                ' + ["--handoff-base", _hb]')
    b = um(b, '        _env = dict(os.environ, PYTHONIOENCODING="utf-8"); _arg = ', '        _hb = os.path.join(_gd, "HANDOFF_BASE_renderizado_pelo_harness.md"); open(_hb, "w", encoding="utf-8", newline="\\n").write(RENDER.get("handoff", ""))\n        _env = dict(os.environ, PYTHONIOENCODING="utf-8"); _arg = ')
    t = um(t, anc, anc + b)
    return um(t, '  marcas         nenhuma linha de comentario com a marca de texto pendente em pos_rito\\\\*.py; ast.parse de todo .py e sh -n do chain.\n',
              '  marcas         nenhuma linha de comentario com a marca de texto pendente em pos_rito\\\\*.py; ast.parse de todo .py e sh -n do chain.\n'
              "  gatilho        (ADITIVOS 1 e 2 a ordem do conserto unico, 10/11/2026) os dois blocos do README (README_FRENTE e README_O_QUE_SAI), cada um sozinho nas guardas (teste_textos_custodia_sem_candidato_v410.py), e o passo final do orquestrador\n"
              "                 (S9_gatilho_custodia) em SANDBOX, com o Nos emulado e o handoff renderizado aqui (teste_gatilho_custodia_sem_candidato_v410.py): escreve so' no sandbox; com um passo anterior falso NAO escreve; o gatilho de verdade nunca e' escrito.\n")


def f_fechar(t):
    if "def _etapa_gatilho_custodia():" in t:
        return t
    anc = '    falha("_etapa_2e levantou %r: %s" % (_e__etapa_2e, traceback.format_exc()[-300:].replace(chr(10), \' | \')))\n'
    b = bloco_h("2f.", "o Nos do SANDBOX (um.py, selo, core e stdout do rito, por COPIA) e o HANDOFF que o fechar (positivo) gravou nele (antes da 2d, em que o fechar com stubs o regrava)", "gatilho_custodia_fechar", "NOSS", 'os.path.join(PKS, "ESPERADOS_v410.json")', "")
    return um(t, anc, anc + b)


aplica("teste_textos_custodia_sem_candidato_v410.py", f_teste)
aplica("harness_textos_ensaio_v410.py", f_textos)
aplica("harness_fechar_sandbox_v410.py", f_fechar)
for k_, v_ in RES.items():
    print("pos_rito/%s: %s" % (k_, v_))
