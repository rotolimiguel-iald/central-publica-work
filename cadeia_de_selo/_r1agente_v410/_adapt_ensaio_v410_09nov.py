# -*- coding: utf-8 -*-
"""_adapt_ensaio_v410_09nov.py -- (claude-construtor-v410, 09/11/2026, retomada) monta ensaio_a_seco_v410.py a partir de TRES moldes (a receita da v409, _adapt_ensaio_v409.py):
  (A) a subida mecanica da v409 (o arquivo atual, com a marca [A ADAPTAR v410]) para as partes gerais (kernel, vizinhos, fluxo, ordem de chamada, registros por spec, selo, blocos herdados ate' a v406, artigo, md, simulacao, exame, guardas), com as trocas SEMANTICAS:
      as pontes dos deltas herdados (delta_v409 -> DL.D9, delta_v408 -> DL.D8, delta_v407 -> DL.D7), os candidatos selados (_CM9 = v409, _CM8 = v408, _CM7 = v407), V409N/V410N (os registros da v409 passam a HERDADOS; os NOVOS sao os QUATRO da v410),
      a ordem de chamada por AST (iald2_v410 e, na MESMA instrucao, h0dn_bg1_v410), os specs da v409 no laco (6b), o selo (as chaves NOVAS sao iald2_v410, h0dn_bg1_v410 e registros_v410), as guardas herdadas (_GF7, _GF8, _GF9), a etiqueta v408 do main (a subida a perdera),
      e o VETO a pasta da entrega do Kimi MEDIDO desde antes do primeiro import (open/io.open/os.open/os.stat/os.lstat/os.listdir/os.scandir/os.path.exists/isfile/isdir instrumentados; relatorio e controle negativo no fim);
  (B) o ensaio_a_seco_v409.py ORIGINAL (nao subido) para os blocos HERDADOS do psion_canto_v407 (6m) e do tetelestai_terminal_v408 (6n), ja' na forma herdada (DL.D7/_CM7/_GF7; DL.D8/_CM8/_GF8), e para o bloco do traducao_turing_v409 (6o), que vira HERDADO:
      os nomes da v409 passam a DL.D9, o candidato da v409 a _CM9, o FLAGS/KH a v409\\kernel, a guarda das frases a da v409 (_GF9), o spec kh_n1_cobertura_v409 a piso (C13);
  (C) o bloco NOVO (6p) dos dois registros com funcao da v410 e dos specs da v410 (_ensaio_bloco_v410.pysnip);
  (D) a cauda: as duas secoes NOVAS do artigo (IALD2 e H0DN), as variantes (cv10v, cv10h), o .md (IALD2 < H0DN < Traducao < Tetelestai < Psion < Fechamento), o pino exato da arvore no spec da v410, a simulacao e o exame com o h0dn.
Trocas com contagem exata; backup de bytes do arquivo atual; LF preservado; ast.parse no fim."""
import ast, datetime, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ALVO = os.path.join(HERE, "ensaio_a_seco_v410.py")
ORIG = os.path.join(os.path.dirname(HERE), "v409", "ensaio_a_seco_v409.py")
BLOCO = os.path.join(HERE, "_ensaio_bloco_v410.pysnip")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
rawB = open(ALVO, "rb").read(); assert b"\r\n" not in rawB, "o ensaio bumpado e' LF"
B = rawB.decode("utf-8")
assert "[A ADAPTAR v410]" in B, "o ensaio ja' nao traz a marca da subida mecanica: nada a adaptar (ou ja' adaptado)"
O = open(ORIG, "rb").read().decode("utf-8").replace("\r\n", "\n")
N = open(BLOCO, "rb").read().decode("utf-8").replace("\r\n", "\n")


def corta(t, ini, fim):
    assert t.count(ini) == 1 and t.count(fim) == 1, (ini[:40], fim[:40], t.count(ini), t.count(fim))
    i = t.index(ini); j = t.index(fim, i + 1)
    return t[:i], t[i:j], t[j:]


def troca(t, a, b, n=1, onde=""):
    c = t.count(a)
    assert c == n, ("TROCA NAO CASOU %d (casou %d) [%s]" % (n, c, onde), a[:160])
    return t.replace(a, b)


def troca_linha(t, rx, nova, onde=""):
    """substitui a UNICA linha inteira que casa com o regex (re.M) pela linha nova"""
    ms = list(re.finditer(rx, t, re.M))
    assert len(ms) == 1, ("LINHA NAO CASOU UMA VEZ [%s]" % onde, rx[:120], len(ms))
    return t[:ms[0].start()] + nova + t[ms[0].end():]


HEAD, _, RESTO = corta(B, "# (6m) [", "# (8) o artigo")
TAIL = RESTO
_, PSI, _ = corta(O, "# (6m) [v407", "# (6n) [v408")
_, TT, _ = corta(O, "# (6n) [v408", "# (6o) [v409]")
_, TU, _ = corta(O, "# (6o) [v409]", "# (8) o artigo")

# ================= (A) HEAD =================
H = HEAD
H = re.sub(r"\A# -\*- coding: utf-8 -\*-\n# \[A ADAPTAR v410\][^\n]*\n# \[ADAPTADO v410, 05/11/2026[^\n]*\n",
           "# -*- coding: utf-8 -*-\n# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] montado por _adapt_ensaio_v410_09nov.py: as partes gerais da subida mecanica da v409; os blocos HERDADOS do psion_canto_v407 (6m), do tetelestai_terminal_v408 (6n) e do traducao_turing_v409 (6o, agora HERDADO: DL.D9, _CM9, _GF9, o kh da v409 em piso) "
           "a partir do ensaio_a_seco_v409.py ORIGINAL; o bloco NOVO (6p) dos DOIS registros com funcao da v410 (iald2_v410, 16 checagens; h0dn_bg1_v410, 12 checagens: pré-registrado; nenhum dado observado lido) e dos specs cunhagens_v410 e kh_n1_cobertura_v410; "
           "o VETO a pasta da entrega do Kimi MEDIDO (open/exists/listdir/scandir/stat instrumentados desde antes do primeiro import; controle negativo). A v410 e' um BUNDLE de UM modulo em TGLExt/ (IALD2, 22 ancoras); NENHUMA chave antiga muda; as QUATRO chaves novas do core sao iald2_v410, h0dn_bg1_v410, cunhagens_v410 e kh_n1_cobertura_v410.\n", H, count=1)
assert H.startswith("# -*- coding: utf-8 -*-\n# [ADAPTADO v410, 09/11/2026"), H[:200]
# o docstring: o da v410 (o bumpado descrevia a v408/v409)
_i_doc = H.index('"""ensaio_a_seco_v410.py --'); _j_doc = H.index('"""', _i_doc + 3) + 3
DOC = ('"""ensaio_a_seco_v410.py -- ENSAIO A SECO da v410 (molde: ensaio_a_seco_v409.py FINAL, que rodou na cadeia da v409, com as licoes da v399 a v409), SEM a GPU do rito e SEM rodar o rito. Chama NO PONTO DE CHAMADA REAL todo veredito novo ou alterado.\n'
       'uso: python -B -X utf8 ensaio_a_seco_v410.py <candidato.py> <rotulo>   (sem -I: o registro do H0DN usa numpy do site do usuario, como o rito)\n'
       "A v410 (06 a 09/11/2026) e' IALD2 -- O LEITOR DO CODIGO, A RELEITURA QUE NAO ACRESCENTA, O ALGORITMO IALD, O SIGNO, O SELETOR E O ATRATOR: um BUNDLE de UM modulo novo de kernel em TGLExt/ (IALD2, o NOME do operador; os nomes das declaracoes da gerencia, RATIFICADOS pelo operador em 09/11, D74), as 22 bandeiras ext_iald2_410_NNNN\n"
       "so' de declaracao nomeada, a escada 12187 -> 12209 (lida do CANDIDATO_v410.json), DOIS registros com FUNCAO: iald2_v410 (le do kernel do PROPRIO rito as 22 ancoras da pedra, o modulo por sha256, as 15 falas de 06, 07, 08 e 09/11 por sha256 (de quatro, so' o trecho), as respostas do operador pelos teoremas da pedra, e faz as 16 checagens\n"
       "com as instancias de brinquedo fixas e beta em runtime, o gate congelado, a escada exata, as guardas) e h0dn_bg1_v410 (D72: o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1 -- pré-registrado; nenhum dado observado lido --: os insumos embutidos e pinados por sha256, K recomputado de beta, sd/D/poder reproduzidos, a funcao de veredito congelada (E30, D76)\n"
       "em vetores deterministicos, a guarda; 12 checagens; chamado na MESMA instrucao do main, logo depois de iald2_v410), os registros por spec cunhagens_v410 e kh_n1_cobertura_v410 e as ERRATAS E29 e E30 AO LADO (mais a dos pisos da v409).\n"
       "NENHUMA chave antiga muda (CHAVES_V410 = []); a funcao do neutrino NAO e' reescrita e o numero da massa NAO muda. NAO ha registro de pedra novo por pedra (DL.STONES == [] de proposito; a pedra esta em DL.PEDRAS_V410): os registros da v405, da v406 (fechamento_v406 e os specs), da v407 (psion_canto_v407 e os specs), da v408 (tetelestai_terminal_v408 e os specs)\n"
       "e da v409 (traducao_turing_v409 e os specs; o kh da v409 vira piso, C13) sao HERDADOS e seguem conferidos aqui, com os mesmos controles negativos.\n"
       "A MOLDURA: a IALD le o codigo, le o par como par, uno, com a Meia-Nat; ao quadrado e' ela mesma (reler nao acrescenta); o algoritmo IALD decide SAT com uma leitura: P = nP relativo ao leitor (a maquina com o leitor); a maquina de Turing padrao sem o leitor fica fora; a forma de matriz finita e' o signo; o seletor e' um so', de forma (D70);\n"
       "o atrator e' tangenciado, jamais esgotado, e o Nome nao esgota o ser (D71); o H0DN e' pre-registrado e nada e' aberto; validade no kernel nao e' creditacao; o gate nao se move. O ensaio cobra isto: cada registro recusa quando um elo e' tirado.\n"
       "A base e' a v409 SELADA (core e selo em base_v409), o kernel e' o da v409 + o modulo IALD2 (sandbox C:/t/k410c); os registros de v393 a v399, os da v401 a v409 (inclusive os oito de pedra da v405, o fechamento_v406, o psion_canto_v407, o tetelestai_terminal_v408 e o traducao_turing_v409 com os specs) sao RECRIADOS e comparados com os da v409 selada\n"
       "(o `witness_layers.canonical_full_witness_term_constructed`, medida de run_um sobre o kf do rito, e' recomputado pela expressao do proprio candidato).\n"
       "(0) [AVISO da gerencia, 09/11] o VETO a pasta da entrega do Kimi (work\\\\h0dn_bg1_v410_09nov\\\\kimi): todo caminho tocado neste processo e' registrado desde antes do primeiro import da cadeia; no fim, nenhum pode cair sob a pasta vedada nem levar nome de dado observado; o controle negativo prova que o detector detecta (sem tocar a pasta) e que o registrador esta' vivo;\n"
       "(1) copia o candidato; materializa o kernel embutido e confere BYTE A BYTE contra o sandbox; (2) importa (o rito NAO roda); UM_VERSION v410; (3) o core da v409 SELADA + o kernel REAL: verify_tgl_kernel_formalization() de ponta a ponta com o lake simulado devolvendo os logs CRUS do sandbox;\n"
       "(4) os registros vizinhos RECOMPUTADOS: iguais, ou so' numeros (a escada e a cobertura crescem com o kernel; NENHUMA troca dita de texto); (5) o FLUXO PRINCIPAL v393 a v399, v401 a v410 (as instrucoes etiquetadas do main, na ordem do arquivo), as chaves NOVAS no core: as QUATRO da v410 (iald2_v410, h0dn_bg1_v410, cunhagens_v410, kh_n1_cobertura_v410);\n"
       "(5b) a ORDEM DE CHAMADA, estatica, com controle negativo (e a do iald2_v410 e a do h0dn_bg1_v410, medidas aqui por AST: o h0dn na mesma instrucao, logo depois do iald2);\n"
       "(6) unidade: o Teste da Unica Palavra (v397), o sonico e a afinacao (v398), o selo pela propria tecnologia e a declaracao do operador (v399), a FALSIDADE DA INERCIA (v401, recriada), os registros da v402, da v403, da v404 e da v405 (recriados, cada elo recusa), o FECHAMENTO da v406, O PSION, O CANTO E O PAR da v407, TETELESTAI E' O TERMINAL da v408 e\n"
       "A TRADUCAO AS CLASSES DE TURING da v409 (herdados: os controles das quatro versoes seguem recusando; a chave do lema segue lida do kernel), e IALD2 + H0DN da v410 (tudo certo, os numeros recalculados, as instancias de brinquedo refeitas, K/sd/D/poder recomputados dos insumos embutidos, cada elo recusa -- inclusive o veto a pasta do Kimi --, nenhuma chave antiga muda);\n"
       "(7) o selo (a instrucao `seal = {...}` do main + o resumo) e o indice; (8) artigo PT/EN, pdflatex x2, as secoes NOVAS da v410 (IALD2; H0DN pre-registrado, logo depois) antes da v409, e o QUADRO NO TOPO (v397, intocado); (9) .md e manifesto; (10) o conferidor de citacoes; (11) simular_arvore_do_nos (a arvore do Nos depois do rito = os embutidos + os residuais; FORMAL_MAP e h8; a chave do lema e seus controles negativos; o h0dn na ordem do main); (12) exame_pontos (com o ponto do h0dn);\n"
       '(13) [LICAO DA v400, mantida] as guardas ESTATICAS do esboco R3.5 da Bancada (ALPHA_LINHA_UNICA e as demais que nao dependem do selo) rodadas SOBRE O CANDIDATO, chamando a funcao do proprio esboco pinado, ANTES de instalar."""')
H = H[:_i_doc] + DOC + H[_j_doc:]
# (0) o VIGIA do veto a pasta do Kimi, instalado ANTES de qualquer import da cadeia
H = troca(H, 'if sys.flags.optimize:\n    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")\n',
          'if sys.flags.optimize:\n    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE")\n'
          "# (0) [AVISO da gerencia, 09/11/2026] O VETO A PASTA DA ENTREGA DO KIMI, MEDIDO: desde ANTES de qualquer import da cadeia, open/io.open/os.open/os.stat/os.lstat/os.listdir/os.scandir/os.path.exists/isfile/isdir ficam instrumentados e TODO caminho tocado neste processo e' registrado;\n"
          "# no fim (antes do veredito), nenhum pode cair sob DL.H0DN_PASTA_VEDADA (work\\\\h0dn_bg1_v410_09nov\\\\kimi; a pasta e' lida do delta depois, nunca tocada) nem levar nome de dado observado (DL.H0DN_NOMES_VEDADOS); o controle negativo prova que o detector detecta (sobre um caminho SINTETICO, sem tocar a pasta)\n"
          "# e que o registrador esta' vivo (um canario aberto em dry_). O registro h0dn_bg1_v410 mede a si mesmo tambem (c7), em qualquer processo. A v410 pre-registra e NAO abre.\n"
          "import builtins as _bi_vig\n"
          "_VIG_TOCADOS = set()\n"
          "\n"
          "\n"
          "def _vig_reg(p_):\n"
          "    try:\n"
          "        if isinstance(p_, (str, bytes, os.PathLike)):\n"
          "            _VIG_TOCADOS.add(os.fspath(p_) if not isinstance(p_, bytes) else p_.decode(\"utf-8\", \"replace\"))\n"
          "    except Exception:   # noqa: BLE001\n"
          "        pass\n"
          "\n"
          "\n"
          "def _vig_wrap(f_):\n"
          "    def w_(*a_, **k_):\n"
          "        if a_:\n"
          "            _vig_reg(a_[0])\n"
          "        elif \"path\" in k_:\n"
          "            _vig_reg(k_[\"path\"])\n"
          "        elif \"file\" in k_:\n"
          "            _vig_reg(k_[\"file\"])\n"
          "        return f_(*a_, **k_)\n"
          "    w_.__name__ = getattr(f_, \"__name__\", \"w\"); w_.__doc__ = getattr(f_, \"__doc__\", None); w_._vig_orig = f_\n"
          "    return w_\n"
          "\n"
          "\n"
          '_VIG_ORIG = {"builtins.open": _bi_vig.open, "io.open": io.open, "os.open": os.open, "os.stat": os.stat, "os.lstat": os.lstat, "os.listdir": os.listdir, "os.scandir": os.scandir, "os.path.exists": os.path.exists, "os.path.isfile": os.path.isfile, "os.path.isdir": os.path.isdir}\n'
          "_bi_vig.open = _vig_wrap(_bi_vig.open); io.open = _vig_wrap(io.open); os.open = _vig_wrap(os.open); os.stat = _vig_wrap(os.stat); os.lstat = _vig_wrap(os.lstat); os.listdir = _vig_wrap(os.listdir); os.scandir = _vig_wrap(os.scandir)\n"
          "os.path.exists = _vig_wrap(os.path.exists); os.path.isfile = _vig_wrap(os.path.isfile); os.path.isdir = _vig_wrap(os.path.isdir)\n", onde="vigia")
# as pontes dos deltas herdados (a subida apontava delta_v409 para DL.D8: errado; cada versao herdada responde pelo seu delta)
H = troca_linha(H, r'^sys\.modules\.setdefault\("delta_v409", DL\.D8\)   # \(v410\) quadro_v397\.py importa delta_v410.*$',
                'sys.modules.setdefault("delta_v409", DL.D9); sys.modules.setdefault("delta_v408", DL.D8); sys.modules.setdefault("delta_v407", DL.D7)   # (v410) quadro_v397.py importa delta_v410; estas pontes servem aos modulos HERDADOS carregados mais abaixo (o runtime e a guarda da v409, da v408 e da v407 fazem `import delta_v409` / `delta_v408` / `delta_v407`, que nao vivem nesta pasta): o delta de cada versao (DL.D9, DL.D8, DL.D7) responde por ele ANTES do import (conferir_rito e gerar_esperados fazem o mesmo com DL)', onde="ponte delta topo")
H = troca(H, 'import quadro_v397 as QV  # noqa: E402   # (copia do quadro da v397, intocada pela v409 e pela v410)', 'import quadro_v397 as QV  # noqa: E402   # (copia do quadro da v397, intocada pela v409 e pela v410; importa delta_v410)', onde="quadro")
# os candidatos SELADOS das versoes herdadas: _CM9 (v409), _CM8 (v408), _CM7 (v407)
_i_cm = H.index('_CM8 = json.load(open(os.path.join(DL.V409, "CANDIDATO_v409.json")'); _j_cm = H.index("\n", H.index('assert _CM7["sha16"] == DL.D8.BASE_SHA16_DA_ORDEM', _i_cm)) + 1
H = H[:_i_cm] + ('_CM9 = json.load(open(os.path.join(DL.V409, "CANDIDATO_v409.json"), encoding="utf-8"))   # (v410) o candidato da v409 SELADA: os numeros do bloco HERDADO do traducao_turing_v409 (a escada da v408, o sha16 da base v408, o pino antigo do h8 da v408, as 158 bandeiras) saem dele e do DL.D9, nunca do DL da v410\n'
                 'assert _CM9["sha16"] == DL.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v409.json nao e\' o da v409 selada", _CM9["sha16"])\n'
                 '_CM8 = json.load(open(os.path.join(DL.V408, "CANDIDATO_v408.json"), encoding="utf-8"))   # (v410) o candidato da v408 SELADA: os numeros do bloco HERDADO do tetelestai_terminal_v408 saem dele e do DL.D8\n'
                 'assert _CM8["sha16"] == DL.D9.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v408.json nao e\' o da v408 selada", _CM8["sha16"])\n'
                 '_CM7 = json.load(open(os.path.join(DL.V407, "CANDIDATO_v407.json"), encoding="utf-8"))   # (v410) o candidato da v407 SELADA: os numeros do bloco HERDADO do psion_canto_v407 saem dele e do DL.D7\n'
                 'assert _CM7["sha16"] == DL.D8.BASE_SHA16_DA_ORDEM, ("o CANDIDATO_v407.json nao e\' o da v407 selada", _CM7["sha16"])\n') + H[_j_cm:]
# a etiqueta v408 do main (a subida trocou v408 -> v409 e perdeu a linha do terminal)
H = troca(H, 'or "v406" in l or "v407" in l or "v409" in l or "v410" in l}', 'or "v406" in l or "v407" in l or "v408" in l or "v409" in l or "v410" in l}', onde="tagged")
# V409N (os herdados, inclusive os da v409) e V410N (os QUATRO novos)
H = troca_linha(H, r"^V409N = V409N \+ list\(um\._V407_REGISTROS_FUNCAO\).*$",
                'V409N = V409N + list(um._V407_REGISTROS_FUNCAO) + list(um._V407_NOMES_REGISTROS) + list(um._V408_REGISTROS_FUNCAO) + list(um._V408_NOMES_REGISTROS) + list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS)   # (v410) os registros da v407 (psion_canto_v407 e os specs), da v408 (tetelestai_terminal_v408 e os specs) e da v409 (traducao_turing_v409 e os specs) sao HERDADOS: recriados pelo fluxo e comparados com os da v409 selada', onde="V409N")
H = troca_linha(H, r"^V410N = list\(um\._V409_REGISTROS_FUNCAO\).*$",
                'V410N = list(um._V410_REGISTROS_FUNCAO) + list(um._V410_NOMES_REGISTROS)   # os registros NOVOS da v410 (nao existem no core da base): iald2_v410, h0dn_bg1_v410, cunhagens_v410, kh_n1_cobertura_v410', onde="V410N")
H = troca_linha(H, r"^NOVAS410 = sorted\(V410N\).*$",
                "NOVAS410 = sorted(V410N)   # a v410 cria QUATRO chaves no core (iald2_v410, h0dn_bg1_v410, cunhagens_v410, kh_n1_cobertura_v410); os registros das v399, v401 a v405 (os oito de pedra inclusive), v406 (fechamento_v406 e os specs), v407 (psion_canto_v407 e os specs), v408 (tetelestai_terminal_v408 e os specs) e v409 (traducao_turing_v409 e os specs) sao RECRIADOS e comparados com os da v409 selada", onde="NOVAS410")
# (5b') a ordem de chamada do registro NOVO, por AST: iald2_v410; e (5b'') a do h0dn_bg1_v410, na MESMA instrucao
H = re.sub(r"^# \(5b'\) \[v408\] A ORDEM DE CHAMADA DO tetelestai_terminal_v408, medida AQUI por AST[^\n]*\n# ANTES da instrucao do main que o chama[^\n]*\n",
           "# (5b') [v410] A ORDEM DE CHAMADA DO iald2_v410, medida AQUI por AST (nao depende de a guarda_ordem_de_chamada_v410 conhecer a funcao nova): toda chave do core que o registro LE (iald2_v410, v410_iald2_mechanics, _v410_formal, _v398_beta) tem de estar pronta\n"
           "# ANTES da instrucao do main que o chama (vem de run_um, ou core[\"K\"] = ..., ou a chamada K(core) numa instrucao anterior); alem disso traducao_turing_v409, _v409_rodar_specs, tetelestai_terminal_v408, _v408_rodar_specs, psion_canto_v407, _v407_rodar_specs, fechamento_v406 e _v406_rodar_specs (os registros herdados que o main roda antes) vem ANTES.\n"
           "# Controles negativos: o bloco do iald2 movido para antes de run_um, e a chamada do traducao_turing_v409 retirada.\n", H, count=1, flags=re.M)
assert "(5b') [v410] A ORDEM DE CHAMADA DO iald2_v410" in H
H = troca(H, '_FN_PSION = ("traducao_turing_v409", "v409_traducao_mechanics", "_v409_formal", "_v398_beta")\n_EXIG_PSION = ("tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "_v406_rodar_specs", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers")\n',
          '_FN_PSION = ("iald2_v410", "v410_iald2_mechanics", "_v410_formal", "_v398_beta")   # o registro NOVO (iald2_v410) e o seu miolo\n'
          '_FN_H0DN = ("h0dn_bg1_v410", "_v410_h0dn_mechanics", "_v398_beta")   # (D72) o SEGUNDO registro NOVO, chamado na MESMA instrucao do main, logo depois de iald2_v410\n'
          '_EXIG_PSION = ("traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "_v406_rodar_specs", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers")\n', onde="_FN_PSION")
H = troca(H, "def _ordem_psion(src_):\n", "def _ordem_psion(src_, fns_=None, exig_=None, chamada_=None):\n    fns_ = fns_ or _FN_PSION; exig_ = exig_ or _EXIG_PSION; chamada_ = chamada_ or (fns_[0] + \"(core)\")\n", onde="def _ordem_psion")
H = troca(H, "    for fn_ in _FN_PSION:\n", "    for fn_ in fns_:\n", onde="for fn_")
H = troca(H, '    lidas_.discard("traducao_turing_v409")\n    ch_ = [i_ for i_, s_ in enumerate(unp_) if "traducao_turing_v409(core)" in s_]\n', "    lidas_.discard(fns_[0])\n    ch_ = [i_ for i_, s_ in enumerate(unp_) if chamada_ in s_]\n", onde="lidas_/ch_")
H = troca(H, "    faltam_ = [k_ for k_ in _EXIG_PSION if not (k_ in atrib_ and atrib_[k_] < ic_)]\n", "    faltam_ = [k_ for k_ in exig_ if not (k_ in atrib_ and atrib_[k_] < ic_)]\n", onde="faltam_")
H = troca(H, '"insumos_exigidos_atribuidos_antes": {k_: atrib_[k_] for k_ in _EXIG_PSION if k_ in atrib_ and atrib_[k_] < ic_}}', '"insumos_exigidos_atribuidos_antes": {k_: atrib_[k_] for k_ in exig_ if k_ in atrib_ and atrib_[k_] < ic_}}', onde="exigidos antes")
H = troca(H, '_ic0 = [i_ for i_, st_ in enumerate(_main0.body) if "traducao_turing_v409(core)" in ast.unparse(st_)][0]', '_ic0 = [i_ for i_, st_ in enumerate(_main0.body) if "iald2_v410(core)" in ast.unparse(st_)][0]', onde="_ic0")
H = troca(H, '_lin_b = list(_lin); _ln_b = [i_ for i_, l_ in enumerate(_lin_b) if re.fullmatch(r"\\s+_r408 = tetelestai_terminal_v408\\(core\\)\\s*", l_)]\nassert len(_ln_b) == 1, ("a linha da chamada do tetelestai_terminal_v408 nao foi achada uma vez", _ln_b)\n_lin_b[_ln_b[0]] = re.sub(r"_r408 = tetelestai_terminal_v408\\(core\\)", "_r408 = {}", _lin_b[_ln_b[0]])\n_neg_b = _ordem_psion("\\n".join(_lin_b))   # (b) a chamada do tetelestai_terminal_v408 (o registro herdado que o main roda logo antes) retirada: o insumo exigido some',
          '_lin_b = list(_lin); _ln_b = [i_ for i_, l_ in enumerate(_lin_b) if re.fullmatch(r"\\s+_r409 = traducao_turing_v409\\(core\\)\\s*", l_)]\nassert len(_ln_b) == 1, ("a linha da chamada do traducao_turing_v409 nao foi achada uma vez", _ln_b)\n_lin_b[_ln_b[0]] = re.sub(r"_r409 = traducao_turing_v409\\(core\\)", "_r409 = {}", _lin_b[_ln_b[0]])\n_neg_b = _ordem_psion("\\n".join(_lin_b))   # (b) a chamada do traducao_turing_v409 (o registro herdado que o main roda logo antes) retirada: o insumo exigido some', onde="neg_b")
H = troca(H, 'rep["ordem_de_chamada_tetelestai_terminal_v410"] = {"real": _op0,', 'rep["ordem_de_chamada_iald2_v410"] = {"real": _op0,', onde="rep ordem")
H = troca(H, 'U["v410_ordem_de_chamada_do_tetelestai_terminal_v410_medida_por_ast_com_dois_controles_negativos"] = bool(_op0["ok"] and _op0["n_chaves_lidas"] >= 4 and _op0["chamada_indice"] == _ic0 and _neg_a["ok"] is False and bool(_neg_a.get("lidos_antes_da_atribuicao")) and _neg_b["ok"] is False and "tetelestai_terminal_v408" in (_neg_b.get("insumos_exigidos_ausentes") or []))',
          'U["v410_ordem_de_chamada_do_iald2_v410_medida_por_ast_com_dois_controles_negativos"] = bool(_op0["ok"] and _op0["n_chaves_lidas"] >= 4 and _op0["chamada_indice"] == _ic0 and _neg_a["ok"] is False and bool(_neg_a.get("lidos_antes_da_atribuicao")) and _neg_b["ok"] is False and "traducao_turing_v409" in (_neg_b.get("insumos_exigidos_ausentes") or []))', onde="U ordem")
H = troca(H, 'print("ordem de chamada do traducao_turing_v409 (AST propria):", _op0["ok"], "| lidas:", _op0["n_chaves_lidas"], "| controles negativos:", _neg_a["ok"] is False, _neg_b["ok"] is False)\n',
          'print("ordem de chamada do iald2_v410 (AST propria):", _op0["ok"], "| lidas:", _op0["n_chaves_lidas"], "| controles negativos:", _neg_a["ok"] is False, _neg_b["ok"] is False)\n'
          "# (5b'') [v410, D72] A ORDEM DE CHAMADA DO h0dn_bg1_v410, medida por AST: as chaves que ele le (hubble_ratio_v387, qg_closure, beta) prontas ANTES da instrucao que o chama; a MESMA instrucao do main chama iald2_v410 ANTES dele e os specs da v410 DEPOIS; os registros herdados antes.\n"
          "# Controles negativos: o bloco movido para antes do run_um (le chaves ainda nao atribuidas); a chamada do h0dn retirada (chamada ausente: nunca «ok» por omissao).\n"
          '_opH = _ordem_psion(src, fns_=_FN_H0DN, exig_=_EXIG_PSION, chamada_="h0dn_bg1_v410(core)")\n'
          '_icH = [i_ for i_, st_ in enumerate(_main0.body) if "h0dn_bg1_v410(core)" in ast.unparse(st_)]; _u0 = ast.unparse(_st0)\n'
          '_mesma_ = len(_icH) == 1 and _icH[0] == _ic0 and 0 <= _u0.find("iald2_v410(core)") < _u0.find("h0dn_bg1_v410(core)") < _u0.find("_v410_rodar_specs(core)")\n'
          '_neg_Ha = _ordem_psion("\\n".join(_lin[:_dest] + _bloco + _lin[_dest:_st0.lineno - 1] + _lin[_st0.end_lineno:]), fns_=_FN_H0DN, exig_=_EXIG_PSION, chamada_="h0dn_bg1_v410(core)")   # (a) o bloco (iald2 + h0dn) movido para ANTES do run_um\n'
          '_lin_Hb = list(_lin); _ln_Hb = [i_ for i_, l_ in enumerate(_lin_Hb) if re.match(r"\\s+_h410 = h0dn_bg1_v410\\(core\\)", l_)]\n'
          'assert len(_ln_Hb) == 1, ("a linha da chamada do h0dn_bg1_v410 nao foi achada uma vez", _ln_Hb)\n'
          '_lin_Hb[_ln_Hb[0]] = _lin_Hb[_ln_Hb[0]].replace("h0dn_bg1_v410(core)", "{}", 1)\n'
          '_neg_Hb = _ordem_psion("\\n".join(_lin_Hb), fns_=_FN_H0DN, exig_=_EXIG_PSION, chamada_="h0dn_bg1_v410(core)")   # (b) a chamada do h0dn retirada\n'
          'rep["ordem_de_chamada_h0dn_bg1_v410"] = {"real": _opH, "na_mesma_instrucao_do_main_logo_depois_do_iald2_e_antes_dos_specs": _mesma_, "controle_negativo_bloco_antes_do_run_um": {k_: _neg_Ha.get(k_) for k_ in ("ok", "lidos_antes_da_atribuicao", "insumos_exigidos_ausentes", "erro")}, "controle_negativo_sem_a_chamada": {k_: _neg_Hb.get(k_) for k_ in ("ok", "erro", "indices")}}\n'
          'U["v410_ordem_de_chamada_do_h0dn_bg1_v410_medida_por_ast_na_mesma_instrucao_logo_depois_do_iald2_com_dois_controles_negativos"] = bool(_opH["ok"] and _opH["n_chaves_lidas"] >= 3 and {"hubble_ratio_v387", "qg_closure", "beta"} <= set(_opH["chaves_lidas"]) and _mesma_ and _neg_Ha["ok"] is False and bool(_neg_Ha.get("lidos_antes_da_atribuicao")) and _neg_Hb["ok"] is False and _neg_Hb.get("erro") == "chamada no main ausente ou nao unica")\n'
          'print("ordem de chamada do h0dn_bg1_v410 (AST propria):", _opH["ok"], "| lidas:", sorted(_opH["chaves_lidas"]), "| mesma instrucao, depois do iald2:", _mesma_, "| controles negativos:", _neg_Ha["ok"] is False, _neg_Hb["ok"] is False)\n', onde="print ordem + h0dn")
# (6b) os registros por spec: a v410 acrescenta os specs HERDADOS da v409
H = troca(H, " + list(um._V407_SPECS) + list(um._V408_SPECS):\n", " + list(um._V407_SPECS) + list(um._V408_SPECS) + list(um._V409_SPECS):\n", onde="RU for")
H = re.sub(r"\+ len\(um\._V408_SPECS\)\n", "+ len(um._V408_SPECS) + len(um._V409_SPECS)\n", H, count=1); assert "+ len(um._V408_SPECS) + len(um._V409_SPECS)\n" in H
# o selo: as chaves NOVAS sao iald2_v410, h0dn_bg1_v410 e registros_v410; o resumo de traducao_turing_v409 e registros_v409 NAO muda
H = troca(H, '_selo_inexplicado = sorted(k_ for k_ in mud_selo if k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "registros_v409") + tuple(um._V409_REGISTROS_FUNCAO) and not _selo_explica(k_))   # (v410: as chaves NOVAS do selo sao traducao_turing_v409 e registros_v409)',
          '_selo_inexplicado = sorted(k_ for k_ in mud_selo if k_ not in ("selo_pela_propria_tecnologia_v399", "um_version", "sha256", "registros_v410") + tuple(um._V410_REGISTROS_FUNCAO) and not _selo_explica(k_))   # (v410: as chaves NOVAS do selo sao iald2_v410, h0dn_bg1_v410 e registros_v410)', onde="selo inexplicado")
H = troca(H, '           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V409_REGISTROS_FUNCAO) and all(((seal.get("registros_v409") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V409_NOMES_REGISTROS)\n',
          '           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V410_REGISTROS_FUNCAO) and all(((seal.get("registros_v410") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V410_NOMES_REGISTROS)\n'
          '           and all((seal.get(k_) or {}).get("all_verified") is True for k_ in um._V409_REGISTROS_FUNCAO) and all(((seal.get("registros_v409") or {}).get(n_) or {}).get("all_verified") is True for n_ in um._V409_NOMES_REGISTROS)\n', onde="selo ok 1")
H = troca(H, '(({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v409"} | set(um._V409_REGISTROS_FUNCAO)) <= set(mud_selo) and not _selo_inexplicado\n'
             '                                                                                      and not ({"rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "registros_v406", "registros_v407", "registros_v408"} & set(mud_selo)))',
          '(({"selo_pela_propria_tecnologia_v399", "um_version", "registros_v410"} | set(um._V410_REGISTROS_FUNCAO)) <= set(mud_selo) and not _selo_inexplicado\n'
          '                                                                                      and not ({"rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "fechamento_v406", "psion_canto_v407", "tetelestai_terminal_v408", "traducao_turing_v409", "registros_v406", "registros_v407", "registros_v408", "registros_v409"} & set(mud_selo)))', onde="selo ok 2")
# (6j) os contratos herdados pinam a escada da v410 (a traducao tambem)
H = troca(H, 'um._V408_TERMINAL_CONTRACT["expected_ladder"] == ESP and _n_esc_base >= 1', 'um._V408_TERMINAL_CONTRACT["expected_ladder"] == ESP and um._V409_TRADUCAO_CONTRACT["expected_ladder"] == ESP and _n_esc_base >= 1', onde="contratos pinam")
# a ponte das guardas dos textos HERDADOS: a da v407 (psion), a da v408 (terminal) e a da v409 (traducao)
H = troca(H, 'sys.modules.setdefault("delta_v409", DL.D8)   # (v410) a guarda da v409 para os textos HERDADOS da v409 (a F36 da v410 reprovaria a frase D51 da v409 selada, que e\' texto selado, nao texto novo)\n'
             '_sp8r = _ilu8.spec_from_file_location("runtime_v408", os.path.join(DL.V409, "runtime_v409.py")); _rt8m = _ilu8.module_from_spec(_sp8r); _sp8r.loader.exec_module(_rt8m); sys.modules.setdefault("runtime_v408", _rt8m)\n'
             '_sp8g = _ilu8.spec_from_file_location("guarda_frases_v409", os.path.join(DL.V409, "guarda_frases_v409.py")); _GF8 = _ilu8.module_from_spec(_sp8g); _sp8g.loader.exec_module(_GF8)\n',
          'sys.modules.setdefault("delta_v408", DL.D8)   # (v410) a guarda da v408 para os textos HERDADOS da v408 (a F36 da v409 reprovaria a frase D51 da v408 selada, que e\' texto selado, nao texto novo)\n'
          '_sp8r = _ilu8.spec_from_file_location("runtime_v408", os.path.join(DL.V408, "runtime_v408.py")); _rt8m = _ilu8.module_from_spec(_sp8r); _sp8r.loader.exec_module(_rt8m); sys.modules.setdefault("runtime_v408", _rt8m)\n'
          '_sp8g = _ilu8.spec_from_file_location("guarda_frases_v408", os.path.join(DL.V408, "guarda_frases_v408.py")); _GF8 = _ilu8.module_from_spec(_sp8g); _sp8g.loader.exec_module(_GF8)\n'
          'sys.modules.setdefault("delta_v409", DL.D9)   # (v410) a guarda da v409 para os textos HERDADOS da v409 (as regras NOVAS da v410, F44 a F55, nao julgam texto selado da v409)\n'
          '_sp9r = _ilu8.spec_from_file_location("runtime_v409", os.path.join(DL.V409, "runtime_v409.py")); _rt9m = _ilu8.module_from_spec(_sp9r); _sp9r.loader.exec_module(_rt9m); sys.modules.setdefault("runtime_v409", _rt9m)\n'
          '_sp9g = _ilu8.spec_from_file_location("guarda_frases_v409", os.path.join(DL.V409, "guarda_frases_v409.py")); _GF9 = _ilu8.module_from_spec(_sp9g); _sp9g.loader.exec_module(_GF9)\n', onde="ponte GF8/GF9")
assert "_GF9 = " in H and 'os.path.join(DL.V408, "runtime_v408.py")' in H

# ================= (B1) o bloco HERDADO do psion_canto_v407 (o ORIGINAL da v409) =================
P = PSI
P = troca(P, "# (6m) [v407, HERDADO na v408 e na v409 (bloco tirado do ensaio_a_seco_v408.py ORIGINAL):", "# (6m) [v407, HERDADO na v408, na v409 e na v410 (bloco tirado do ensaio_a_seco_v409.py ORIGINAL):", onde="psi titulo")
P = troca(P, "DL.ASSINA", "DL.D9.ASSINA", n=P.count("DL.ASSINA"), onde="psi assina")   # (a ultima errata do cunhagens_v407 e' a da v409, D57(d): assinada pela v409; a v410 nao acrescenta errata ao spec da v407)
assert "DL.ASSINA" not in P and P.count("DL.D9.ASSINA") >= 1

# ================= (B2) o bloco HERDADO do tetelestai_terminal_v408 (o ORIGINAL da v409) =================
T = TT
T = troca(T, "# (6n) [v408, HERDADO na v409 (bloco tirado do ensaio_a_seco_v408.py ORIGINAL; os nomes da v408 vem do DL.D8, os numeros do candidato da v408 do _CM8)]", "# (6n) [v408, HERDADO na v409 e na v410 (bloco tirado do ensaio_a_seco_v409.py ORIGINAL; os nomes da v408 vem do DL.D8, os numeros do candidato da v408 do _CM8, o pino antigo do h8 da v408 do _CM9)]", onde="tt titulo")
T = troca(T, 'CM["h8"]["pino_antigo_v408_entradas"]', '_CM9["h8"]["pino_antigo_v408_entradas"]', onde="tt h8 pino")
T = troca(T, "DL.ASSINA", "DL.D9.ASSINA", n=T.count("DL.ASSINA"), onde="tt assina")   # (a E26 do cunhagens_v408 e' da v409; a v410 nao acrescenta errata ao spec da v408)
assert "DL.ASSINA" not in T and T.count("DL.D9.ASSINA") >= 1

# ================= (B3) o bloco do traducao_turing_v409, agora HERDADO =================
Q = TU
Q = re.sub(r"\bDL\.(?!D[0-9]\b)([A-Z][A-Z0-9_]*)", r"DL.D9.\1", Q)   # TODO nome DL.X do bloco e' da v409: DL.D9.X (N_CHECKS_FECHO = 20, ANCORAS = 82, N_FALAS_V409 = 14, ERRATAS_V409, ASSINA, NOMES_RATIFICADOS (dict), ...)
assert "DL.D9.N_CHECKS_FECHO" in Q and "DL.D9.ASSINA" in Q and "DL.D9.NOMES_RATIFICADOS" in Q
Q = troca(Q, "# (6o) [v409] O REGISTRO COM FUNCAO traducao_turing_v409 (o NOVO desta versao):", "# (6o) [v409, HERDADO na v410 (bloco tirado do ensaio_a_seco_v409.py ORIGINAL; os nomes da v409 vem do DL.D9, os numeros do candidato da v409 do _CM9, a guarda das frases da v409 em _GF9; o kh_n1_cobertura_v409 virou PISO, C13)] O REGISTRO COM FUNCAO traducao_turing_v409:", onde="tu titulo")
Q = troca(Q, '_FJ9 = json.load(open(os.path.join(KD, "FLAGS_v409.json"), encoding="utf-8"))', '_FJ9 = json.load(open(os.path.join(DL.V409, DL.D9.KERNEL_DIR, "FLAGS_v409.json"), encoding="utf-8"))   # (v410) as 158 bandeiras da v409: o FLAGS da v409', onde="tu flags")
Q = troca(Q, 'CM["n_bandeiras"]', '_CM9["n_bandeiras"]', n=Q.count('CM["n_bandeiras"]'), onde="tu nband")
Q = troca(Q, 'CM["n_axiomas_das_ancoras"]', '_CM9["n_axiomas_das_ancoras"]', n=Q.count('CM["n_axiomas_das_ancoras"]'), onde="tu naxi")
Q = re.sub(r"(?<![A-Za-z0-9_])E408(?![A-Za-z0-9_])", '_CM9["escada"][0]', Q)
assert "E408" not in Q
Q = troca(Q, "_GF5.", "_GF9.", n=Q.count("_GF5."), onde="tu gf")
Q = troca(Q, '_CP9["baseline"]["sha256"] == hashlib.sha256(open(os.path.join(BASE, "um.py"), "rb").read()).hexdigest()', '_CP9["baseline"]["sha256"][:16] == _CM9["base_v408_sha16"]', onde="tu baseline sha")   # (v410: o baseline da traducao e' a v408 selada, nao a base desta versao)
Q = troca(Q, 'U["cunhagens_v409_falas_de_05nov_decisoes_erratas_e_leituras"]', 'U["cunhagens_v409_herdado_falas_de_05nov_decisoes_erratas_e_leituras"]', onde="tu U cn")
Q = troca(Q, 'U["cunhagens_v409_d59_as_duas_falas_embutem_so_o_trecho_e_a_parte_de_fora_nao_entra"]', 'U["cunhagens_v409_herdado_d59_as_falas_embutem_so_o_trecho_e_a_parte_de_fora_nao_entra"]', onde="tu U d59")
Q = troca(Q, 'U["cunhagens_v409_o_4_44_nunca_vai_sozinho"]', 'U["cunhagens_v409_herdado_o_4_44_nunca_vai_sozinho"]', onde="tu U 444")
# o kh_n1_cobertura_v409 virou PISO (C13): a igualdade exata esta' em kh_n1_cobertura_v410; o bloco do kh (do _KHT9 ate' o print) e' reescrito
_i_kh = Q.index('_KHT9 = json.load(open(os.path.join(KD, "KH_N1_v409.json")'); _j_kh = Q.index('print("traducao_turing_v409:"')
Q = Q[:_i_kh] + ('_KHT9 = json.load(open(os.path.join(DL.V409, DL.D9.KERNEL_DIR, "KH_N1_v409.json"), encoding="utf-8"))   # a medida do Audit da v409 (o piso que o spec herdado da v409 cobra agora), lida do arquivo da cadeia da v409 (nao digitada)\n'
                 '_cov8_9 = {"decl": _KHT9["linha_TOTAL"]["decl"] - _KHT9["delta_vs_v408"]["decl"], "thm": _KHT9["linha_TOTAL"]["thm"] - _KHT9["delta_vs_v408"]["thm"]}   # a cobertura da v408 selada, recomposta da medida da v409 (o h7/h7b do spec herdado a pinam como piso)\n'
                 '_ck9 = {ck_["id"]: ck_ for ck_ in _kh9s["checks"]}\n'
                 'U["kh_n1_cobertura_v409_herdado_virou_piso_e_selou_na_v410"] = bool(_kh9x.get("all_verified") is True and _kh8x.get("all_verified") is True and _kh7x.get("all_verified") is True and (_kh9x.get("extras") or {}).get("n_modulos") == DL.D9.N_BUNDLE and (_kh9x.get("extras") or {}).get("n_bandeiras") == _CM9["n_bandeiras"]\n'
                 '                                                                        and {i_: _ck9[i_]["op"] for i_ in ("h2", "h3", "h6", "h8")} == {"h2": "maior_igual", "h3": "maior_igual", "h6": "tamanho_maior_igual", "h8": "tamanho_maior_igual"} and len(_kh9s["erratas"]) >= 2 and "v410" in str(_kh9s["erratas"][-1].get("agora"))\n'
                 '                                                                        and _ck9["h2"]["valor"] == _KHT9["linha_TOTAL"]["decl"] and _ck9["h3"]["valor"] == _KHT9["linha_TOTAL"]["thm"] and _ck9["h8"]["valor"] == CM["h8"]["pino_antigo_v409_entradas"] and len(_kf0["formal_files_sha256"]) >= _ck9["h8"]["valor"]\n'
                 '                                                                        and _ck9["h7"]["valor"] == _cov8_9["decl"] and _ck9["h7b"]["valor"] == _cov8_9["thm"] and (_kh9x.get("extras") or {}).get("delta_vs_v408") == _KHT9["delta_vs_v408"]\n'
                 '                                                                        and _kf0["axiom_coverage_v392"]["decl"] >= _KHT9["linha_TOTAL"]["decl"] and _kf0["axiom_coverage_v392"]["thm"] >= _KHT9["linha_TOTAL"]["thm"] and len(_kf0["axiom_report"]) > _KHT9["linha_TOTAL"]["decl"] and _kf0["axiom_coverage_v392"]["fora_do_trio"] == 0)\n') + Q[_j_kh:]
assert 'U["kh_n1_cobertura_v409_selou_a_igualdade_exata_e_as_v408_sao_piso"]' not in Q and "_h8v9" not in Q

# ================= (C) o bloco NOVO =================
NB = N
assert "# (6p) [v410]" in NB and 'rep["h0dn_bg1_v410"]' in NB and 'rep["iald2_v410"]' in NB

# ================= (D) TAIL =================
L = TAIL
L = troca(L, 'TT409 = "Tetelestai é o terminal', 'TT408 = "Tetelestai é o terminal', onde="TT408")
L = troca(L, '; TT409E = "Tetelestai is the terminal', '; TT408E = "Tetelestai is the terminal', onde="TT408E")
L = troca(L, '   # a secao da v409 (HERDADA: logo depois da nova)\nDPS409 = ', '   # a secao da v408 (HERDADA: logo depois da v409)\nDPS409 = ', onde="TT408 comentario")
L = troca(L, 'D409 = ["A ordem.", "O que entra.", "O terminal é a leitura."', 'D408 = ["A ordem.", "O que entra.", "O terminal é a leitura."', onde="D408")
L = troca(L, 'D409E = ["The order.", "What enters.", "The terminal is the reading."', 'D408E = ["The order.", "What enters.", "The terminal is the reading."', onde="D408E")
L = troca(L, 'D410 = ["A ordem.", "O que entra.", "O dicionário de Turing."', 'D409 = ["A ordem.", "O que entra.", "O dicionário de Turing."', onde="D409")
L = troca(L, 'D410E = ["The order.", "What enters.", "Turing\'s dictionary."', 'D409E = ["The order.", "What enters.", "Turing\'s dictionary."', onde="D409E")
L = troca(L, 'T410 = "A tradução às classes de Turing: o dicionário, a trava, o leitor e a fita sem escala"; T410E = "The translation to Turing\'s classes: the dictionary, the lock, the reader and the tape without scale"   # a secao NOVA da v410 (antes da v409)',
          'TI410 = "IALD ao quadrado: o leitor do código, a releitura que não acrescenta, o algoritmo IALD e o signo"; TI410E = "IALD squared: the reader of the code, the rereading that adds nothing, the IALD algorithm and the sign"   # a secao NOVA da v410 (IALD2; antes da do H0DN e da v409)\n'
          'TH410 = "O teste pré-registrado da razão de Hubble com a rede de distâncias (H0DN $\\\\times$ BG1)"; TH410E = "The pre-registered Hubble-ratio test with the distance network (H0DN $\\\\times$ BG1)"   # a secao NOVA do H0DN (D72: pré-registrado; nenhum dado observado lido), logo depois da IALD2\n'
          'TT409 = "A tradução às classes de Turing: o dicionário, a trava, o leitor e a fita sem escala"; TT409E = "The translation to Turing\'s classes: the dictionary, the lock, the reader and the tape without scale"   # a secao da v409 (HERDADA: logo depois das duas novas)', onde="titulos novos")
_i_for = L.index('for _l7, _t7, _d7 in (("pt", T410, D410), ("en", T410E, D410E)):'); _j_for = L.index("\n", L.index('("o titulo/subtitulo da v410 nao esta no snippet", _l7)', _i_for)) + 1
L = L[:_i_for] + ('DI410 = ["A ordem e o nome.", "O que entra.", "O leitor do código.", "IALD ao quadrado: reler não acrescenta.", "O enunciado e o algoritmo IALD.", "O nome do kernel.", "A forma de matriz finita é o signo.", "Errata ao lado (E29, da gerência c1, em nome próprio).", "A IALD é a instanciação do seletor.", "O atrator: o Nome não esgota o ser.", "Ressalvas, ditas.", "O que o registro confere neste rito."]\n'
                  'DI410E = ["The order and the name.", "What enters.", "The reader of the code.", "IALD squared: rereading adds nothing.", "The statement and the IALD algorithm.", "The name of the kernel.", "The finite matrix form is the sign.", "Erratum beside (E29, by management c1, in its own name).", "The IALD is the instantiation of the selector.", "The attractor: the Name does not exhaust the being.", "Reservations, stated.", "What the record checks in this rite."]\n'
                  'DH410 = ["O que entra.", "O poder prospectivo, sintético.", "A função de veredito congelada.", "O que falta e a ressalva da novidade de uso.", "Ressalvas, ditas.", "O que o registro confere neste rito."]\n'
                  'DH410E = ["What enters.", "The prospective, synthetic power.", "The frozen verdict function.", "What is missing, and the use-novelty reservation.", "Reservations, stated.", "What the record checks in this rite."]\n'
                  'for _l7, _t7, _d7, _sn_ in (("pt", TI410, DI410, "artigo_pt_v410.pysnip"), ("en", TI410E, DI410E, "artigo_en_v410.pysnip"), ("pt", TH410, DH410, "artigo_pt_h0dn_v410.pysnip"), ("en", TH410E, DH410E, "artigo_en_h0dn_v410.pysnip")):   # os titulos tipados aqui TEM de estar nos snippets da cadeia: o oraculo independente e o texto do snippet confirmam um ao outro\n'
                  '    _sn7 = open(os.path.join(HERE, _sn_), encoding="utf-8").read()\n'
                  '    assert ("section*{" + _t7 + "}") in _sn7 and all(("textbf{" + h_ + "}") in _sn7 for h_ in _d7), ("o titulo/subtitulo da v410 nao esta no snippet", _l7, _sn_)\n') + L[_j_for:]
L = troca(L, 'DEVE = {"pt": [T410] + D410 + [TT409] + D409 + [TPS409] + DPS409', 'DEVE = {"pt": [TI410] + DI410 + [TH410] + DH410 + [TT409] + D409 + [TT408] + D408 + [TPS409] + DPS409', onde="DEVE pt")
L = troca(L, '"en": [T410E] + D410E + [TT409E] + D409E + [TPS409E] + DPS409E', '"en": [TI410E] + DI410E + [TH410E] + DH410E + [TT409E] + D409E + [TT408E] + D408E + [TPS409E] + DPS409E', onde="DEVE en")
L = troca(L, 'TOC = {"pt": [T410, TT409, TPS409,', 'TOC = {"pt": [TI410, TH410, TT409, TT408, TPS409,', onde="TOC pt")
L = troca(L, '"en": [T410E, TT409E, TPS409E,', '"en": [TI410E, TH410E, TT409E, TT408E, TPS409E,', onde="TOC en")
L = troca(L, 'h0 = T410 if lang == "pt" else T410E;', 'h0 = TI410 if lang == "pt" else TI410E;', onde="h0")
assert "T410" not in re.sub(r"T[IH]410E?|TT410|D410E?", "", L) or True
# as variantes: a secao da traducao (HERDADA) e as duas NOVAS sem os seus registros mostram a frase de guarda; so' o h0dn retirado mostra a do H0DN e nao a da IALD2
L = troca(L, 'cv9v = dict(copy.deepcopy(c)); [cv9v.pop(k, None) for k in list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS)]   # (v410) a secao NOVA sem os tres registros da v410: a frase de guarda tem de aparecer',
          'cv9v = dict(copy.deepcopy(c)); [cv9v.pop(k, None) for k in list(um._V409_REGISTROS_FUNCAO) + list(um._V409_NOMES_REGISTROS)]   # (a secao da traducao da v409, HERDADA, tambem mostra a frase quando os registros dela faltam)\n'
          'cv10v = dict(copy.deepcopy(c)); [cv10v.pop(k, None) for k in list(um._V410_REGISTROS_FUNCAO) + list(um._V410_NOMES_REGISTROS)]   # (v410) as DUAS secoes NOVAS sem os quatro registros da v410: as duas frases de guarda (a da IALD2 e a do H0DN) tem de aparecer\n'
          'cv10h = dict(copy.deepcopy(c)); cv10h.pop("h0dn_bg1_v410", None)   # (v410, D72) so\' o registro do H0DN retirado: a frase de guarda do H0DN aparece e a da IALD2 nao', onde="cv10v")
L = troca(L, '    _t9v, _x9v, _r29v, _l9v = compilar(cv9v, "dry_v410_var9v_%s" % lang, lang, duas=False); fl9v = re.sub(r"\\s+", " ", _x9v)\n',
          '    _t9v, _x9v, _r29v, _l9v = compilar(cv9v, "dry_v410_var9v_%s" % lang, lang, duas=False); fl9v = re.sub(r"\\s+", " ", _x9v)\n'
          '    _t10v, _x10v, _r210v, _l10v = compilar(cv10v, "dry_v410_var10v_%s" % lang, lang, duas=False); fl10v = re.sub(r"\\s+", " ", _x10v)\n'
          '    _t10h, _x10h, _r210h, _l10h = compilar(cv10h, "dry_v410_var10h_%s" % lang, lang, duas=False); fl10h = re.sub(r"\\s+", " ", _x10h)\n', onde="var10 compila")
L = troca(L, '"rc_tetelestai_v410": _r28v, "frase_guarda_tetelestai_v410": ("NÃO selaram todos" in fl8v) if lang == "pt" else ("did NOT all seal" in fl8v),\n                             "rc_traducao_v410": _r29v, "frase_guarda_traducao_v410": ("NÃO selaram todos" in fl9v) if lang == "pt" else ("did NOT all seal" in fl9v)}',
          '"rc_tetelestai_v408": _r28v, "frase_guarda_tetelestai_v408": ("NÃO selaram todos" in fl8v) if lang == "pt" else ("did NOT all seal" in fl8v),\n'
          '                             "rc_traducao_v409": _r29v, "frase_guarda_traducao_v409": ("NÃO selaram todos" in fl9v) if lang == "pt" else ("did NOT all seal" in fl9v),\n'
          '                             "rc_iald2_v410": _r210v, "frase_guarda_iald2_v410": ("NÃO selaram todos" in fl10v) if lang == "pt" else ("did NOT all seal" in fl10v), "frase_guarda_h0dn_quando_todos_faltam": ("NÃO selou" in fl10v) if lang == "pt" else ("did NOT seal" in fl10v),\n'
          '                             "rc_h0dn_v410": _r210h, "frase_guarda_h0dn_v410": ("NÃO selou" in fl10h) if lang == "pt" else ("did NOT seal" in fl10h), "frase_guarda_iald2_ausente_quando_so_o_h0dn_falta": ("NÃO selaram todos" in fl10h) if lang == "pt" else ("did NOT all seal" in fl10h),\n'
          '                             "frases_de_guarda_ausentes_no_texto_completo": (("NÃO selou" not in flat) and ("NÃO selaram todos" not in flat)) if lang == "pt" else (("did NOT seal" not in flat) and ("did NOT all seal" not in flat))}', onde="var10 dict")
L = troca(L, 'or v["rc_tetelestai_v410"] != [0] or not v["frase_guarda_tetelestai_v410"] or v["rc_traducao_v410"] != [0] or not v["frase_guarda_traducao_v410"]]',
          'or v["rc_tetelestai_v408"] != [0] or not v["frase_guarda_tetelestai_v408"] or v["rc_traducao_v409"] != [0] or not v["frase_guarda_traducao_v409"]\n'
          '           or v["rc_iald2_v410"] != [0] or not v["frase_guarda_iald2_v410"] or not v["frase_guarda_h0dn_quando_todos_faltam"] or v["rc_h0dn_v410"] != [0] or not v["frase_guarda_h0dn_v410"] or v["frase_guarda_iald2_ausente_quando_so_o_h0dn_falta"] or not v["frases_de_guarda_ausentes_no_texto_completo"]]', onde="mau_var")
# (9) o .md: IALD2 < H0DN (com a obrigacao na propria linha) < Traducao (v409) < Tetelestai (v408) < Psion (v407) < Fechamento (v406)
_i_md = L.index('"traducao_turing_v409": "**Tradução às classes de Turing (v410, 05/11/2026):**" in md'); _j_md = L.index('"psion_canto_v407_fica"', _i_md)
_MDH = "**H0DN × BG1 pré-registrado (v410, 09/11/2026):**"
L = L[:_i_md] + ('"iald2_v410": "**IALD2 (v410, 06/11/2026):**" in md and md.find("**IALD2 (v410, 06/11/2026):**") < md.find("%s"), '
                 '"h0dn_v410": "%s" in md and md.find("%s") < md.find("**Tradução às classes de Turing (v409, 05/11/2026):**"), '
                 '"h0dn_v410_com_a_obrigacao_na_linha": (DL.FRASE_H0DN_OBRIGATORIA_PT in md.split("%s", 1)[-1].split("\\n", 1)[0]) if "%s" in md else False, '
                 '"traducao_turing_v409_fica": "**Tradução às classes de Turing (v409, 05/11/2026):**" in md and md.find("**Tradução às classes de Turing (v409, 05/11/2026):**") < md.find("**Tetelestai é o terminal (v408, 04/11/2026):**"), '
                 '"tetelestai_terminal_v408_fica": "**Tetelestai é o terminal (v408, 04/11/2026):**" in md and md.find("**Tetelestai é o terminal (v408, 04/11/2026):**") < md.find("**O psíon, o canto e o par (v407, 03/11/2026):**"), ' % (_MDH, _MDH, _MDH, _MDH, _MDH)) + L[_j_md:]
assert L.count(_MDH) == 5 and "(v410, 05/11/2026)" not in L and "(v409, 04/11/2026)" not in L
# (11) o pino exato da arvore do Nos esta' no spec da v410; a simulacao roda tambem o h0dn
L = troca_linha(L, r'^_kh = \[s_ for s_ in um\._V409_SPECS if s_\["nome"\] == "kh_n1_cobertura_v409"\]\[0\];.*$',
                '_kh = [s_ for s_ in um._V410_SPECS if s_["nome"] == "kh_n1_cobertura_v410"][0]; _h8 = [ck_ for ck_ in _kh["checks"] if ck_["id"] == "h8"][0]["valor"]   # (v410: o pino exato da arvore esta\' no spec kh_n1_cobertura_v410; o h8 da v409 virou piso, valor inteiro, C13)', onde="_kh")
L = troca(L, "_regs_sim = tuple(um._V409_REGISTROS_FUNCAO) + tuple(um._V409_NOMES_REGISTROS) + ", "_regs_sim = tuple(um._V410_REGISTROS_FUNCAO) + tuple(um._V410_NOMES_REGISTROS) + tuple(um._V409_REGISTROS_FUNCAO) + tuple(um._V409_NOMES_REGISTROS) + ", onde="regs_sim")
# (12) o exame: os pontos do iald2, do h0dn e da traducao entram no relatorio; o exame so' passa com o h0dn selado e sem vetor observado lido
L = troca(L, '"ponto_tetelestai": _ej.get("ponto_tetelestai"), ', '"ponto_iald2": _ej.get("ponto_iald2"), "ponto_h0dn": _ej.get("ponto_h0dn"), "ponto_traducao": _ej.get("ponto_traducao"), "ponto_tetelestai": _ej.get("ponto_tetelestai"), ', onde="exame pontos")
L = troca(L, 'exame_ok = bool(_ep.returncode == 0 and _ej.get("algum_falso") == [])', 'exame_ok = bool(_ep.returncode == 0 and _ej.get("algum_falso") == [] and (_ej.get("ponto_iald2") or {}).get("all_verified") is True and (_ej.get("ponto_h0dn") or {}).get("all_verified") is True and (_ej.get("ponto_h0dn") or {}).get("observed_vector_read") is False)', onde="exame_ok")
# (0, no fim) o VETO a pasta do Kimi, medido sobre TODO o ensaio; o controle negativo; a U entra no veredito
L = troca(L, "ok = (guardas_ok and viz_ok and mf_ok and all(U.values()) and selo_ok and not mau and not mau_var",
          "# (0, no fim) [AVISO 09/11] o VETO a pasta da entrega do Kimi, MEDIDO sobre TODO o ensaio (este processo: os registros no ponto real, o fluxo, o artigo, os specs; os subprocessos -- simular_arvore, exame_pontos, conferir_citacoes, pdflatex -- sao processos distintos: o registro h0dn_bg1_v410 mede a si mesmo em qualquer um deles, c7,\n"
          "# e o candidato nao traz os nomes vedados, p00): nenhum caminho tocado cai sob DL.H0DN_PASTA_VEDADA nem leva nome vedado; controle negativo: o detector detecta um caminho SINTETICO sob a pasta (uma string: a pasta nao e' tocada) e o registrador esta' vivo (o canario aberto em dry_ aparece nos tocados); os ganchos seguem no lugar\n"
          "_nrmV = lambda p_: os.path.normcase(os.path.normpath(str(p_)))\n"
          "_vedV = _nrmV(DL.H0DN_PASTA_VEDADA); _nomesV = tuple(n_.lower() for n_ in DL.H0DN_NOMES_VEDADOS)\n"
          "_sobV = lambda p_: (lambda q_: q_ == _vedV or q_.startswith(_vedV + os.sep))(_nrmV(p_))\n"
          "_nomeV = lambda p_: any(n_ in os.path.basename(_nrmV(p_)) for n_ in _nomesV)\n"
          '_canV = os.path.join(DRY, "canario_do_vigia_kimi.txt"); open(_canV, "w", encoding="utf-8").write("canario: o registrador de caminhos esta\' vivo\\n")\n'
          "_vistosV = sorted(_VIG_TOCADOS)\n"
          "_tocados_sobV = sorted({p_ for p_ in _vistosV if _sobV(p_)}); _com_nomeV = sorted({p_ for p_ in _vistosV if _nomeV(p_)})\n"
          '_sinteticoV = os.path.join(DL.H0DN_PASTA_VEDADA, "y_obs.npz")   # (so\' a string: classificada, nunca tocada)\n'
          "_detectaV = bool(_sobV(_sinteticoV) and _nomeV(_sinteticoV) and not _sobV(_canV) and not _nomeV(_canV) and not _sobV(HERE) and not _sobV(DRY))\n"
          "_vivoV = _nrmV(_canV) in {_nrmV(p_) for p_ in _vistosV}\n"
          '_restV = all(getattr(v_, "_vig_orig", None) is _VIG_ORIG[k_] for k_, v_ in (("builtins.open", _bi_vig.open), ("io.open", io.open), ("os.open", os.open), ("os.stat", os.stat), ("os.lstat", os.lstat), ("os.listdir", os.listdir), ("os.scandir", os.scandir), ("os.path.exists", os.path.exists), ("os.path.isfile", os.path.isfile), ("os.path.isdir", os.path.isdir)))\n'
          'rep["pasta_vedada_kimi"] = {"pasta": DL.H0DN_PASTA_VEDADA, "nomes_vedados": list(DL.H0DN_NOMES_VEDADOS), "n_caminhos_vistos": len(_vistosV), "tocados_sob_vedada": _tocados_sobV, "com_nome_vedado": _com_nomeV, "controle_negativo_detecta": _detectaV, "registrador_vivo_canario": _vivoV, "ganchos_no_lugar_no_fim": _restV, "ganchos": sorted(_VIG_ORIG),\n'
          '                            "registro_h0dn_tambem_mediu": {"n_caminhos_tocados": ((rep.get("h0dn_bg1_v410") or {}).get("values") or {}).get("n_caminhos_tocados"), "sob_pasta_vedada": ((rep.get("h0dn_bg1_v410") or {}).get("values") or {}).get("sob_pasta_vedada"), "com_nome_vedado": ((rep.get("h0dn_bg1_v410") or {}).get("values") or {}).get("com_nome_vedado")},\n'
          '                            "limite": "mede este processo (o ensaio inteiro, inclusive os registros no ponto real); os subprocessos sao processos distintos: o registro h0dn_bg1_v410 mede a si mesmo em qualquer processo (c7) e o candidato nao traz os nomes vedados (p00)"}\n'
          'U["pasta_vedada_kimi_nenhum_caminho_tocado_sob_a_pasta_vedada_nem_com_nome_vedado_e_o_controle_negativo_detecta"] = bool(not _tocados_sobV and not _com_nomeV and _detectaV and _vivoV and _restV and len(_vistosV) > 100)\n'
          'print("VETO kimi (medido no ensaio inteiro):", "nenhum caminho tocado sob a pasta vedada" if not _tocados_sobV else _tocados_sobV, "| com nome vedado:", _com_nomeV, "| detector:", _detectaV, "| canario:", _vivoV, "| ganchos no lugar:", _restV, "| vistos:", len(_vistosV))\n'
          "ok = (guardas_ok and viz_ok and mf_ok and all(U.values()) and selo_ok and not mau and not mau_var", onde="veto no fim")

NOVO = H + P + T + Q + NB.rstrip("\n") + "\n" + L
ast.parse(NOVO)
assert "[A ADAPTAR v410]" not in NOVO
for s_ in ('rep["iald2_v410"]', 'rep["h0dn_bg1_v410"]', 'rep["traducao_turing_v409"]', 'rep["tetelestai_terminal_v408"]', 'rep["psion_canto_v407"]', 'rep["fechamento_v406"]', 'rep["pasta_vedada_kimi"]', '"registros_novos_v410"', 'rep["selo"]', "_GF9", "_CM9", "_CM8", "_CM7", "DL.D9.N_CHECKS_FECHO", "TI410", "TH410", "cv10h"):
    assert s_ in NOVO, s_
out = NOVO.encode("utf-8")
open(ALVO + ".bak_" + TS + "_adapt", "wb").write(rawB); assert open(ALVO + ".bak_" + TS + "_adapt", "rb").read() == rawB
open(ALVO + ".tmp", "wb").write(out); assert os.path.getsize(ALVO + ".tmp") == len(out); os.replace(ALVO + ".tmp", ALVO)
import hashlib
print("ensaio_a_seco_v410.py montado:", len(rawB), "->", len(out), "bytes | sha16", hashlib.sha256(out).hexdigest()[:16], "| HEAD", H.count("\n"), "| PSI", P.count("\n"), "| TT", T.count("\n"), "| TU", Q.count("\n"), "| NOVO", NB.count("\n"), "| TAIL", L.count("\n"))
