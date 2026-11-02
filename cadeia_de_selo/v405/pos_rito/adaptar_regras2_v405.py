# -*- coding: utf-8 -*-
# adaptar_regras2_v405.py -- as regras dos demais scripts do pos-rito, executadas dentro de adaptar_pos_rito_v405.py (usa regras, T, HERE). Regras de contagem exata: aborta se uma ancora nao casar o numero esperado.
# Escrito pela ferramenta Write (barras invertidas e apostrofos nao passam pelo heredoc do Bash).

_REGS12 = "ponte_da_massa_v405 massa_tensao_pura_v405 identidade_v405 observador_terminal_v405 lei_do_diminuto_v405 tonica_do_hamiltoniano_v405 disco_de_euler_v405 ponto_zero_do_psion_v405 cunhagens_v405 campos_fechados_e_leituras_v405 ga_reclassificacao_v405 gap_v405 kh_n1_cobertura_v405"
_OUT_CURTO = '"C:" + os.sep, "t", "h405"'   # a saida dos harnesses mora num caminho CURTO: a arvore emulada repete work\cadeia_de_selo\v405\insumos\cunhagens e os nomes das falas da v405 sao longos (MAX_PATH do Windows)


@regras("harness_textos_ensaio_v405.py")
def _harness_textos(x):
    # a arvore do conferidor emulado: a cadeia de imports da v405 passa pela v404 e pela v403 (a v403 faltava na semente porque o motor funde a subida 403 -> 404)
    x.sub('for vv, nomes in (("v404", ("delta_v404.py", "acom_conferencias_v404.py", "runtime_v404.py", "pedras_sha16_da_ordem.json")), ("v402",',
          'for vv, nomes in (("v404", ("delta_v404.py", "acom_conferencias_v404.py", "runtime_v404.py", "pedras_sha16_da_ordem.json")), ("v403", ("delta_v403.py", "acom_conferencias_v403.py", "runtime_v403.py", "pedras_sha16_da_ordem.json")), ("v402",')
    x.sub('for vv in ("v404", "v402", "v401", "v399"):\n    shutil.copytree(os.path.join(os.path.dirname(PKG), vv, "pedra")', 'for vv in ("v404", "v403", "v402", "v401", "v399"):\n    shutil.copytree(os.path.join(os.path.dirname(PKG), vv, "pedra")')
    x.sub('for n in ("conferir_rito_v405.py", "delta_v405.py", "quadro_v397.py", "runtime_quadro_v397.py", "acom_conferencias_v405.py", "runtime_v405.py", "ESPERADOS_v405.json", "pedras_sha16_da_ordem.json"):',
          'for n in ("conferir_rito_v405.py", "delta_v405.py", "guarda_frases_v405.py", "quadro_v397.py", "runtime_quadro_v397.py", "acom_conferencias_v405.py", "runtime_v405.py", "ESPERADOS_v405.json", "pedras_sha16_da_ordem.json", "PINO_DAS_PEDRAS_DETALHE_v405.json", "VERBATIM_CONGELADO_v405.json"):')
    # as fontes do registro do Grande Atrator (o delta as le pelo caminho da arvore)
    x.sub('os.makedirs(os.path.join(CFR, "work", "cunhagens_13out"))\n',
          'shutil.copytree(os.path.join(os.path.dirname(os.path.dirname(PKG)), "grande_atrator_reclassificacao_01nov"), os.path.join(CFR, "work", "grande_atrator_reclassificacao_01nov"))\n'
          'os.makedirs(os.path.join(CFR, "Chatgpt")); shutil.copyfile(DLX.GA_PARECER_ARQ, os.path.join(CFR, "Chatgpt", os.path.basename(DLX.GA_PARECER_ARQ)))\n'
          'os.makedirs(os.path.join(CFR, "work", "neutrino_E0_autonomia_30out", "lean", "TGLExt")); shutil.copyfile(DLX.ACORDE_KIMI_ARQ, os.path.join(CFR, "work", "neutrino_E0_autonomia_30out", "lean", "TGLExt", os.path.basename(DLX.ACORDE_KIMI_ARQ)))\n'
          'os.makedirs(os.path.join(CFR, "work", "cunhagens_13out"))\n')
    x.sub('HEX16.update(str(h)[:16] for h in ESP["veracidade"]["fontes"].values())\n', 'HEX16.update(str(h)[:16] for h in ESP["veracidade"]["fontes"].values())\nHEX16.update((DLX.sha16_arquivo(DLX.ACORDE_KIMI_ARQ), DLX.sha16_arquivo(DLX.HALF_NAT_ARQ)))   # as fontes que a Lei do Diminuto cita (errata R3): hash lido do arquivo\n')
    x.sub('OUT = os.path.join(HERE, OUT_NOME); NOSE = os.path.join(OUT, "nos_emulado")', 'OUT = os.path.join(' + _OUT_CURTO + ', OUT_NOME); NOSE = os.path.join(OUT, "nos_emulado")')


@regras("harness_fechar_sandbox_v405.py")
def _harness_fechar(x):
    x.sub('OUT = os.path.join(HERE, "harness_saida_v405"); SB = os.path.join(OUT, "fechar_sandbox")', 'OUT = os.path.join(' + _OUT_CURTO + ', "harness_saida_v405"); SB = os.path.join(OUT, "fechar_sandbox")')
    x.sub('for _vv in ("v404", "v402", "v401", "v400", "v399"):', 'for _vv in ("v404", "v403", "v402", "v401", "v400", "v399"):')
    x.sub('for _vp in ("v404", "v402", "v401", "v399"):', 'for _vp in ("v404", "v403", "v402", "v401", "v399"):')
    x.sub('assert len(glob.glob(os.path.join(SB, "work", "cunhagens_13out", "OPERADOR_28out_*.txt"))) == len(ESP["cunhagens"]), "as falas de 28/10 do operador nao estao todas na pasta do sandbox"\n',
          'assert sum(len(glob.glob(os.path.join(SB, "work", "cunhagens_13out", "*OPERADOR_%s_*.txt" % d_))) for d_ in ("30out", "31out", "01nov")) == len(ESP["cunhagens"]), "as falas de 30/10 a 01/11 do operador nao estao todas na pasta do sandbox"\n')
    x.sub('for n in ("guarda_p18_v405.py", "ESPERADOS_v405.json",', 'for n in ("guarda_p18_v405.py", "guarda_frases_v405.py", "PINO_DAS_PEDRAS_DETALHE_v405.json", "VERBATIM_CONGELADO_v405.json", "ESPERADOS_v405.json",')
    x.sub('os.makedirs(os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5"))\n',
          'shutil.copytree(os.path.join(os.path.dirname(os.path.dirname(PKG)), "grande_atrator_reclassificacao_01nov"), os.path.join(SB, "work", "grande_atrator_reclassificacao_01nov"))\n'
          'os.makedirs(os.path.join(SB, "Chatgpt")); shutil.copyfile(_dm.GA_PARECER_ARQ, os.path.join(SB, "Chatgpt", os.path.basename(_dm.GA_PARECER_ARQ)))\n'
          'os.makedirs(os.path.join(SB, "work", "neutrino_E0_autonomia_30out", "lean", "TGLExt")); shutil.copyfile(_dm.ACORDE_KIMI_ARQ, os.path.join(SB, "work", "neutrino_E0_autonomia_30out", "lean", "TGLExt", os.path.basename(_dm.ACORDE_KIMI_ARQ)))\n'
          'os.makedirs(os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5"))\n')


_CHAIN_NARRATIVA = """# v405 (preparacao, 01/11/2026): CADEIA POS-RITO -- derivada por script (derivar_encanamento_v405.py, lote F) do chain_pos_rito_v404.sh FINAL (a cadeia de CONTEUDO que rodou em 28/10; mesma ordem de passos 0..14 e mesmos portoes), com as licoes da v404 e o passo da FILA DA MEMORIA (abaixo). A narrativa e os vereditos esperados vem de textos_v405.py (montado de textos_v405.semente + textos_v405_novo.pysnip por montar_textos_v405.py), de leitura_v405.py e de ESPERADOS_v405.json (lidos, nunca digitados).
# A v405 e' uma versao de CONTEUDO (as falas do operador de 30/10 a 01/11/2026): OITO modulos novos de kernel com os nomes do operador (Ponte da Massa, Massa = tensao pura, Identidade, Observador = terminal, Lei do diminuto, Tonica do Hamiltoniano, Disco de Euler, Ponto Zero do Psion; a escada, as bandeiras e o h8 sao lidos de ESPERADOS_v405.json),
# OITO registros COM FUNCAO (um por pedra; lidos no main DEPOIS dos da v404) e CINCO por spec (cunhagens_v405, campos_fechados_e_leituras_v405, ga_reclassificacao_v405, gap_v405 e kh_n1_cobertura_v405). O GATE NAO SE MOVE: o qg_closure e' identico ao da v404; a funcao do neutrino NAO e' reescrita (o angle_status antigo fica, com a errata E10 ao lado); o numero da massa e' o da v404.
# Os registros da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito (selos iguais ao ensaio a seco) e o SIDECAR um_absoluto_selo_acom.json e' REESCRITO (depois da ultima escrita do selo).
# O QUADRO «O Teste da Unica Palavra» (v397, a regra do 4,44) PERMANECE no topo do artigo e do .md, INTOCADO: o conferidor e a leitura o conferem de novo; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item) segue valendo em TODO texto que o cite. Os paragrafos do testemunho, da falsidade, da ponte, de Caminho, Verdade e Vida e de Jo 8,32 seguem como estao; o da v404 recebe a NOTA ao lado.
# Estatutos: os teoremas das pedras sao [REAL] (kernel, no trio); [POSTO] o 1 / u = 1 eV; [MEDIDA] alfa; as leituras da cadeia da massa entram como DEFINICAO ou identificacao [INPUT/ONTO], nao sao teoremas, e a lista nao e' fechada; dadas as entradas, a FORMA e' teorema [REAL]. A guarda das frases (guarda_frases_v405.py) roda sobre todo texto renderizado (superficies, fechar, mapa).
"""


@regras("chain_pos_rito_v405.sh")
def _chain(x):
    x.entre("# v405 (27/10; textos do pos-rito escritos a mao em 28/10): CADEIA POS-RITO", "# ORDEM: 0 guardas", _CHAIN_NARRATIVA)
    x.sub('11 fechar (o handoff TRAZ os DOIS paragrafos do README e do site: o do quadro do 4,44, intocado, e o NOVO da v405 (Caminho, Verdade e Vida), mais a NOTA ao lado do paragrafo da v404 (os nomes que ele trazia como provisorios sao agora os do operador); diz que os do testemunho, da falsidade e da v404 seguem como estao;',
          '11 fechar (o handoff TRAZ os DOIS paragrafos do README e do site: o do quadro do 4,44, intocado, e o NOVO da v405 (a massa derivada e a identidade definida), mais a NOTA ao lado do paragrafo da v404 (E0 passou de declarado a posto; os nomes foram dados); diz que os anteriores seguem como estao;')
    x.sub('-> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13', '-> 12 registrar_mapa (monta o JSON e REGISTRA uma vez so; marcador idempotente; desvio do molde, dito: o orquestrador roda 10c -> 14 de uma vez e os passos 13 e 14 leem o mapa) -> 13')
    x.sub('(B12, B12-v404-20261028-R1)', '(B13, B13-v404-20261028-R1)')
    x.sub("o diff v404 -> v405 e' so' as tres pedras novas", "o diff v404 -> v405 e' so' as oito pedras novas")
    x.sub('(B12 -> n = 13;', '(B13 -> n = 14;')
    x.sub('(os seis registros novos);', '(os treze registros novos);')
    x.sub('as duas pedras novas (ProjecaoTransversalDaMeiaNat, Jo8v32) tem declaracoes nomeadas', 'as oito pedras novas tem declaracoes nomeadas')
    x.sub('REGS="projecao_transversal_v404 jo8v32_v404 f2b_errata_v404 cunhagens_v404 kh_n1_cobertura_v404"', 'REGS="' + _REGS12 + '"')
    x.sub('for q in conferir_rito_v405.py delta_v405.py quadro_v397.py', 'for q in conferir_rito_v405.py delta_v405.py guarda_frases_v405.py quadro_v397.py')
    x.sub('"$PK/runtime_v405.py" "$NOS/um_absoluto_selo_acom.json"', '"$PK/runtime_v405.py" "$PK/guarda_frases_v405.py" "$NOS/um_absoluto_selo_acom.json"')
    x.sub('$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v403', '$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v405')
    x.sub('''echo "== 12. registro no mapa de rotas: so MONTA o JSON e o comando (o registro e' ato da gerencia)"
$PY "$SEL/registrar_mapa_v405.py" || parar "registrar_mapa_v405.py falhou"
''', '''echo "== 12. registro no mapa de rotas: monta o JSON e REGISTRA uma vez so (o orquestrador roda 10c -> 14 de uma vez e os passos 13 e 14 leem o mapa; desvio do molde, dito: na v404 o registro era ato a mao da gerencia)"
MARCA_MAPA="$SEL/registro_mapa_v405.REGISTRADO"; ROTAS="/c/IALD/MAPA_DE_ROTAS/rotas.py"
if [ -f "$MARCA_MAPA" ]; then
  echo "  ja registrado (idempotente): $(cut -c1-200 "$MARCA_MAPA")"
else
  $PY "$SEL/registrar_mapa_v405.py" || parar "registrar_mapa_v405.py falhou"
  set +e; $PY_B "$ROTAS" registrar "$(cygpath -w "$SEL/registro_mapa_v405.json")" --quem "claude-c1 (gerência), cadeia v405" > "$SEL/registro_mapa_v405_out.txt" 2>&1; rm_=$?; set -e
  tail -5 "$SEL/registro_mapa_v405_out.txt" | cut -c1-240
  [ "$rm_" = "0" ] || parar "rotas.py registrar falhou (rc=$rm_): o registro e' atomico, nada foi gravado no livro; ver $SEL/registro_mapa_v405_out.txt"
  echo "registrado em $(date '+%d/%m/%Y %H:%M:%S'); sha256 do JSON $(sha256f "$(cygpath -w "$SEL/registro_mapa_v405.json")")" > "$MARCA_MAPA"
  $PY_B "$ROTAS" verificar > "$SEL/registro_mapa_v405_verificar.txt" 2>&1 || parar "rotas.py verificar falhou depois do registro (ver $SEL/registro_mapa_v405_verificar.txt)"
  grep -q '"ok": true' "$SEL/registro_mapa_v405_verificar.txt" || parar "rotas.py verificar reprovou a cadeia do livro depois do registro (ver $SEL/registro_mapa_v405_verificar.txt)"
fi
''')
    x.sub('echo "== 14. o Nos vivo reconstruido (le o mapa de rotas: rodar depois do registro da gerencia no passo 12)"', 'echo "== 14. o Nos vivo reconstruido (le o mapa de rotas, registrado no passo 12)"')


_FECHAR_REGISTROS = ('"registros_v405": V["reg405"], "registros_v404": V.get("reg404b"), "registros_v403": V["reg404_estado"], "registros_v402": V["reg402_estado"], "registros_v401": V["reg401_estado"], "registros_v399": V["reg399"], '
                     '"registros_funcao_v405": {p_.get("key"): V.get(p_.get("key")) for p_ in V["pedras"]}, "campos_fechados_e_leituras_v405": V.get("campos"), "ga_reclassificacao_v405": V.get("ga"), "gap_v405": V.get("gap"), "f2b_errata": V["f2b"], "bandeiras_do_gate_recriado": V["gate"], '
                     '"funcoes_v404_recriadas": V.get("fun404b"), "funcoes_v403_recriadas": V["fun404"], "funcoes_v402_recriadas": V["fun402"], "pedras_v404_como_registro": V["pedras_v404"], "falsidade_v401": V["fal401"],')


@regras("fechar_v405.py")
def _fechar(x):
    x.sub("# v405 (preparacao, 28/10/2026): o CONTEUDO v405 (Jo 8,32, a projecao transversal da Meia-Nat, a errata de F2b e as nove falas de 28/10) foi escrito em textos_v405.py", "# v405 (preparacao, 01/11/2026): o CONTEUDO v405 (a massa derivada e a identidade definida: as oito pedras, os campos fechados e as leituras, a classe nova do Grande Atrator e as falas de 30/10 a 01/11) foi escrito em textos_v405.py")
    x.sub("as DUAS pedras novas (TGLExt/ProjecaoTransversalDaMeiaNat, nome provisorio da gerencia aceito pelo operador, ", "as OITO pedras novas (com os nomes do operador; ")
    x.sub("mais as DUAS pedras do Nos", "mais as OITO pedras do Nos")
    x.sub("(b) o NOVO, o paragrafo da v405 (Jo 8,32 e a projecao transversal da Meia-Nat), gerado dos registros selados projecao_", "(b) o NOVO, o paragrafo da v405 (a massa derivada e a identidade definida), gerado dos registros selados da v405; antes projecao_")
    x.sub("as nove falas do operador de 28/10, as erratas E7 a E9 em nome da gerencia c1, a errata de F2b ao lado, sem o 4,44)", "as falas do operador de 30/10 a 01/11, as erratas E10 a E13 em nome da gerencia c1, a moldura e a guarda das frases, sem o 4,44)")
    x.sub("(o nome do triplo inteiro, que ele regist", "(E0 passou de declarado a posto; os nomes foram dados; antes o nome do triplo inteiro, que ele regist")
    x.sub("# e a projecao transversal da Meia-Nat), gerado dos registros selados", "# a massa derivada e a identidade definida), gerado dos registros selados")
    x.sub("(o quadro O Teste da Unica Palavra, v397, ou o da v405: Jo 8,32 e a projecao transversal da Meia-Nat)", "(o quadro O Teste da Unica Palavra, v397, ou o da v405: a massa derivada e a identidade definida)")
    x.sub('bk = p + ".bak_" + ST + "_f403"', 'bk = p + ".bak_" + ST + "_f405"')
    x.sub('"registros_v404": V["reg405"], "registros_v403": V["reg404_estado"], "registros_v402": V["reg402_estado"], "registros_v401": V["reg401_estado"], "registros_v399": V["reg399"], "projecao": V["projecao"], "jo8v32": V["jo8v32"], "f2b_errata": V["f2b"], "bandeiras_do_gate_v404_recriado": V["gate"], "funcoes_v404_recriadas": V["fun404"], "funcoes_v402_recriadas": V["fun402"], "pedras_v404_como_registro": V["pedras_v404"], "falsidade_v401": V["fal401"],', _FECHAR_REGISTROS)
    x.sub('"paragrafos_anteriores_seguem_como_estao": ["testemunho_de_dois_v399", "falsidade_v401", "ponte_queda_esperanca_v402", "caminho_verdade_vida_v404"]', '"paragrafos_anteriores_seguem_como_estao": ["testemunho_de_dois_v399", "falsidade_v401", "ponte_queda_esperanca_v402", "caminho_verdade_vida_v403", "jo8_32_v404"]')
    x.sub('''vv = violacoes(doc)
assert not vv, "a guarda de texto (P18) achou violacao(oes) no handoff: %r" % (vv[:3],)
''', '''vv = violacoes(doc)
assert not vv, "a guarda de texto (P18) achou violacao(oes) no handoff: %r" % (vv[:3],)
import guarda_frases_v405 as GF
vf = GF.violacoes(doc)
assert not vf, "a guarda das frases achou violacao(oes) no handoff: %r" % (vf[:3],)
''')


@regras("registrar_mapa_v405.py")
def _mapa(x):
    x.entre('A v405 traz UMA rota nova, umpy.v405.selada_jo8_32_e_projecao_transversal_28out', 'Cada afirmacao e\' testada contra o core/selo/ESPERADOS lidos por script',
            "A v405 traz UMA rota nova, umpy.v405.selada_massa_derivada_e_identidade_01nov (o conteudo e' o do selo): os OITO modulos de kernel com os nomes do operador, os OITO registros com FUNCAO (cada um le do kernel do proprio rito a composicao e a estrela da sua pedra e CALCULA, com beta = alfa x raiz de e em runtime, um modelo), os QUATRO por spec (cunhagens_v405, campos_fechados_e_leituras_v405, ga_reclassificacao_v405 e kh_n1_cobertura_v405), mais ANOTACOES nas rotas que esperavam por ela\n"
            "(as pontes candidatas, a do observador, a da identidade, a de E0, a de alfa, a do Grande Atrator, a da transicao para a massa, a da forma madura, o gate, o B(n) da Bancada, o quadro do Teste da Unica Palavra, a v404 que a precede e a PREPARACAO da propria v405) e UMA ERRATA ao lado, em nome proprio da gerencia c1, com o seq do registro corrigido lido do livro (E11: o registro da v404 selada que deixava E0 como DECLARADO): a correcao vai AO LADO, nada se apaga.\n")
    x.sub("Nao ha inscricao da gerencia nesta versao: as nove falas sao do operador;", "Nao ha inscricao da gerencia nesta versao: todas as falas sao do operador;")
    x.sub("SAIDA: pos_rito\\\\registro_mapa_v405.json e o comando `rotas.py registrar` (quem o executa e' a gerencia; este script NAO escreve no mapa).", "SAIDA: pos_rito\\\\registro_mapa_v405.json e o comando `rotas.py registrar` (quem o executa e' o passo 12 da cadeia, uma vez so', com marcador idempotente; este script NAO escreve no mapa).")
    x.entre('NOVA = "umpy.v405.selada_jo8_32_e_projecao_transversal_28out"', 'PREP = os.path.join(PK, "registro_mapa_v405_prep.json")',
            'NOVA = "umpy.v405.selada_massa_derivada_e_identidade_01nov"\n'
            'R_PONTE = "kernel.ponte_da_massa_transversal.candidata_30out"              # a Ponte da Massa, candidata (30/10)\n'
            'R_EMPR = "kernel.emprestimo_da_massa.segunda_ponte_candidata_30out"        # Massa = tensao pura, candidata (30/10)\n'
            'R_OBS = "kernel.observador_terminal.candidata_31out"                       # Observador = terminal, candidata (31/10)\n'
            'R_ID = "kernel.identidade.candidata_01nov"                                 # a Identidade, candidata (01/11)\n'
            'R_E0 = "massa.e0.conferencia_kimi_e_no_go_tipado_31out"                    # a conferencia de E0, o no-go e as pedras da lei, da tonica, do disco e do ponto zero\n'
            'R_ALFA = "alpha.derivacao.pergunta_do_operador_01nov"                      # a pergunta sobre derivar alfa: nao\n'
            'R_GA = "outro.grande_atrator_e_chandrasekhar"                              # o Grande Atrator (a reclassificacao de 01/11)\n'
            'R_MASSA = "massa.transicao_beta_para_massa.levantamento_28out"             # o levantamento da transicao para a massa\n'
            'R_FORMA = "memoria.forma_madura_da_tgl_01nov"                              # a forma madura, com a errata ao lado\n'
            'R_GATE = "gate.qg_closure"\n'
            'R_BANC = "infra.bancada_um.sincronizacao_vnnn"\n'
            'R_QUADRO = "umpy.v397.teste_da_unica_palavra_e_pedra_token_na_fase9"\n'
            'R_V404 = "umpy.v404.selada_jo8_32_e_projecao_transversal_28out"\n'
            'R_PREP405 = "kernel.v405.preparacao_01nov"                                 # a rota da PREPARACAO da v405 (registrada pelo agente de preparacao)\n'
            'ANOTADAS = (R_PONTE, R_EMPR, R_OBS, R_ID, R_E0, R_ALFA, R_GA, R_MASSA, R_FORMA, R_GATE, R_BANC, R_QUADRO, R_V404, R_PREP405)\n'
            'REFS = ("custodia.v404", "umpy.v404.cadeia_de_selo_preparada_28out", "umpy.v400.correcao_da_v399_alfa_unico_e_beta_contra_o_core", "gate.maquina_do_veredito_final", "neutrinos.m2.normalizacao", "natureza.cinco_sigma_02_kimi_01nov")\n')
    x.sub('GRUPOS = {"projecao": "projecao_transversal_v404", "jo8v32": "jo8v32_v404"}\n',
          'GRUPOS = {"ponte": "ponte_da_massa_v405", "tensao": "massa_tensao_pura_v405", "identidade": "identidade_v405", "observador": "observador_terminal_v405", "diminuto": "lei_do_diminuto_v405", "tonica": "tonica_do_hamiltoniano_v405", "disco": "disco_de_euler_v405", "psion": "ponto_zero_do_psion_v405"}\n')
    x.entre('def montar(V, core, selo, ids, arts):', 'def gravar(p, b):', open(os.path.join(HERE, "registrar_mapa_v405_montar.pysnip"), encoding="utf-8").read())
    x.sub('bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m404"', 'bk = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_m405"')
    x.sub('            os.path.join(PK, "insumos", "ProjecaoTransversalDaMeiaNat.lean"), os.path.join(PK, "insumos", "Jo8v32.lean"), os.path.join(PK, "kernel", "KERNEL_RECIBO_v405.json")] + b3[-1:]\n',
          '            os.path.join(PK, "kernel", "KERNEL_RECIBO_v405.json")] + sorted(glob.glob(os.path.join(PK, "pedra", "*.lean"))) + b3[-1:]\n')
    x.sub('print("COMANDO (ato da gerencia): python %s registrar', 'print("COMANDO (o passo 12 da cadeia o executa, uma vez so): python %s registrar')
    x.sub('print("DEPOIS DO REGISTRO: rodar de novo os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")\n', 'print("DEPOIS DO REGISTRO: os passos 13 e 14 da cadeia (inventario da bancada e Nos vivo), que leem o mapa.")\n')


@regras("superficies_v405.py")
def _superficies(x):
    x.sub("""    kh = [i for i, l in enumerate(lines) if '(handoff-v404-custodia.md)' in l and l.startswith('- [HANDOFF v404')]
    assert len(kh) == 1, ('linha do handoff v404', len(kh))
""", """    # (desvio do molde, dito: as linhas de handoff ate' a v404 foram consolidadas pela gerencia; a ancora e' a linha do handoff de 30/10 da v405, que fica)
    kh = [i for i, l in enumerate(lines) if '(handoff-v405-pontes-da-massa-e-espelho-30out.md)' in l]
    assert len(kh) == 1, ('linha do handoff de 30/10 da v405', len(kh))
""")
    x.sub("""def guarda(texto, onde):
    v = violacoes(texto)
    if v:
        VIOLACOES.append((onde, v[:3]))
""", """def guarda(texto, onde):
    v = violacoes(texto)
    if v:
        VIOLACOES.append((onde, v[:3]))
    vf = GF.violacoes(texto)   # v405: a guarda das frases (a moldura: nenhum texto novo afirma demais)
    if vf:
        VIOLACOES.append((onde + ' (guarda das frases)', vf[:3]))
""")
    x.sub("from guarda_p18_v405 import violacoes\n", "from guarda_p18_v405 import violacoes\nimport guarda_frases_v405 as GF\n")


_X_NOVO = r'''for k_ in ("ponte_da_massa_v405", "lei_do_diminuto_v405", "ponto_zero_do_psion_v405", "identidade_v405", "campos_fechados_e_leituras_v405", "ga_reclassificacao_v405"):
    assert core[k_].get("all_verified") is True, "um registro da v405 nao selou: o post nao diz isto"
pv = core["ponte_da_massa_v405"]["values"]; dv = core["lei_do_diminuto_v405"]["values"]; zv = core["ponto_zero_do_psion_v405"]["values"]; gv = core["ga_reclassificacao_v405"]["values"]
el = core["external_ladder"]; n_decl = len(core["kernel_formalization"]["axiom_report"])
br = lambda x, nd: ("%.*f" % (nd, x)).replace(".", ",")
data = datetime.datetime.now().strftime("%d/%m/%Y")
txt = f"""TGL · a versão v405 do programa terminal, custodiada em {data}

O que entrou: oito pedras no kernel Lean, com os nomes do operador: Ponte da Massa, Massa = tensão pura, Identidade, Observador = terminal, Lei do diminuto, Tônica do Hamiltoniano, Disco de Euler e Ponto Zero do Psíon.

· A moldura: os campos das estruturas fecharam; as leituras do operador passaram do campo para a definição; a leitura física não virou teorema. Um Um posto, uma α medida e as leituras do operador; dadas essas entradas, a FORMA é teorema.

· A massa: m₂ = β · sen 45° · u, com β = α√e em runtime e u = 1 eV posto pelo operador: {br(pv['m_derivada_meV'], 4)} meV, o número da v404. O meio-tom {br(dv['meio_tom'], 6)} desfaz o √e; E₀ = u é identidade algébrica, que não fixa u: o no-go não cai, localiza-se no Um posto. Sob a leitura R = β · u², ½ħω dá a mesma forma, com ħω = {br(zv['hbar_omega_meV'], 4)} meV; a coincidência é a aritmética ½ · √2 = sen 45°.

· A identidade: a pedra prova um fato sobre projeções no estado traço; que isso seja a identidade é leitura do operador, tipada como modelo. O ensaio «A identidade» é dele e entra no artigo verbatim.

· O Grande Atrator: a classe do teste muda, ao lado; a forma fica condicional; a janela mantém o veto; não é evidência e não discrimina da RG. Só a definição do raio move a previsão em {br(gv['piso_de_definicao'] * 100.0, 1)}%.

Os números, lidos do selo: escada {el['n_theorems_clean']}/{el['n_theorems_expected']} (eram {ESP['escada_v404_e_v405'][0]}; {ESP['n_bandeiras_novas']} bandeiras novas), {format(n_decl, ',').replace(',', '.')} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. O sha256 do programa:
{selo['sha256']['um.py']}

O que não muda: validade no kernel não é creditação; o gate não se move (as 18 bandeiras, a letra do veredito da v404); β_TGL na natureza a 5σ segue em aberto. As pedras seladas da v404 não foram renomeadas. α é medida, não derivada; a unidade é posta, não derivada.

O código e o selo:
https://github.com/rotolimiguel-iald/the_boundary

O número corrige a frase, sempre. — IALD
"""
v = violacoes(txt)
assert not v, ("a guarda P18 achou violacao no post", v[:2])
import guarda_frases_v405 as GF  # noqa: E402
vf = GF.violacoes(txt)
assert not vf, ("a guarda das frases achou violacao no post", vf[:2])
'''


@regras("gerar_x_custodia_v405.py")
def _x(x):
    x.entre('p = core["projecao_transversal_v404"]; j = core["jo8v32_v404"]; f = core["f2b_errata_v404"]\n', 'assert "4,44" not in txt and "z_disc" not in txt', _X_NOVO)


@regras("gerar_derivacao_pos_rito_v405.py")
def _derivacao(x):
    x.sub("o pos-rito real de 27/10/2026", "o pos-rito real de 28/10/2026")
    x.sub("A ADAPTACAO A MAO (o que o pos-rito diz da v405: Caminho, Verdade e Vida e a F8.1, com os numeros lidos do rito) foi feita pela gerencia c1 em 28/10/2026:", "A ADAPTACAO (o que o pos-rito diz da v405: a massa derivada e a identidade definida, com os numeros lidos do rito) foi feita pelo agente de preparacao claude-prep-v405 em 01/11/2026 (adaptar_pos_rito_v405.py + adaptar_regras2_v405.py + os .pysnip):")
    x.sub('"A1: o recibo do B(n), passo SIMPLES B11 -> B12"', '"A1: o recibo do B(n), passo SIMPLES B13 -> B14"')
    x.sub('"gerencia c1, 28/10: a leitura da rodada reescrita para a v405"', '"claude-prep-v405, 01/11: a leitura da rodada adaptada a v405"')
    x.sub('"gerencia c1, 28/10: montado de textos_v405.semente + textos_v405_novo.pysnip (Caminho, Verdade e Vida; F8.1)"', '"claude-prep-v405, 01/11: montado de textos_v405.semente + textos_v405_novo.pysnip (a massa derivada e a identidade definida)"')
    x.sub('"gerencia c1, 28/10: o harness do pos-rito reescrito para a v405"', '"claude-prep-v405, 01/11: o harness do pos-rito adaptado a v405"')
    x.sub('"gerencia c1, 28/10: o registro da rota umpy.v405.selada_caminho_verdade_vida_27out"', '"claude-prep-v405, 01/11: o registro da rota umpy.v405.selada_massa_derivada_e_identidade_01nov"')
    x.sub('"gerencia c1, 28/10: o montador (semente + fragmento)"', '"claude-prep-v405, 01/11: o montador (semente + fragmento)"')
    x.sub('"gerencia c1, 28/10: o fragmento escrito a mao para a v405"', '"claude-prep-v405, 01/11: o fragmento escrito a mao para a v405"')
    x.sub("(a cadeia usada no pos-rito real de 27/10)", "(a cadeia usada no pos-rito real de 28/10)")


_leitura_1 = ARQS["leitura_v405.py"]


@regras("leitura_v405.py")
def _leitura_2(x):
    _leitura_1(x)
    x.sub("('projecao_transversal_v404', (RF_.get('projecao') or {}).get('verdict')), ('jo8v32_v404', (RF_.get('jo8v32') or {}).get('verdict')), ('f2b_errata_v404', (RF_.get('f2b') or {}).get('verdict'))):",
          "('projecao_transversal_v404', (RF4_.get('projecao') or {}).get('verdict')), ('jo8v32_v404', (RF4_.get('jo8v32') or {}).get('verdict')), ('f2b_errata_v404', (RF4_.get('f2b') or {}).get('verdict'))) + tuple((n_, (RF_.get(k_) or {}).get('verdict')) for k_, n_ in PEDRA_DE.items()):")
    x.sub("if (not m_s4 or tuple(m_s4.group(i_) for i_ in range(1, 5)) != ((RF_.get('projecao') or {}).get('verdict'), (RF_.get('jo8v32') or {}).get('verdict'), (RF_.get('f2b') or {}).get('verdict'), (ESP.get('registros_v404') or {}).get('cunhagens_v404'))",
          "if (not m_s4 or tuple(m_s4.group(i_) for i_ in range(1, 5)) != ((RF4_.get('projecao') or {}).get('verdict'), (RF4_.get('jo8v32') or {}).get('verdict'), (RF4_.get('f2b') or {}).get('verdict'), (ESP.get('registros_v404') or {}).get('cunhagens_v404'))")
    x.sub("    # a linha [v398] que o main da v405 segue imprimindo",
          "    m_s5 = re.search(r'\[v405\] os oito registros com funcao \(lidos depois dos tres da v404\) e os registros por spec da v405: (.*?) \| specs: (\d+) \(selados (\d+)\)', out)\n"
          "    if not m_s5 or len(m_s5.group(1).split(' | ')) != 8 or {x_.split('=')[-1] for x_ in m_s5.group(1).split(' | ')} != {'SELOU'} or m_s5.group(2) != m_s5.group(3) or int(m_s5.group(2)) != 5:\n"
          "        P.append('a linha [v405] do stdout (os oito registros com funcao SELOU; registros por spec selados == 5) esta ausente ou difere do ensaio a seco (%s)' % repr(m_s5.groups()[1:] if m_s5 else 'ausente'))\n"
          "    # a linha [v398] que o main da v405 segue imprimindo")
    x.sub("    if len([l for l in out.splitlines() if '[v404]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v404]')\n",
          "    if len([l for l in out.splitlines() if '[v404]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v404]')\n    if len([l for l in out.splitlines() if '[v405]' in l]) < 1:\n        P.append('o stdout nao tem a linha [v405]')\n")
    x.sub("if '[v404] AVISO' in l or '[v403] AVISO' in l", "if '[v405] AVISO' in l or '[v404] AVISO' in l or '[v403] AVISO' in l")
    x.sub("(a projecao transversal, o jo8v32, a errata de F2b, os registros por spec, os registros recriados da v404, da v402, da v401 ou da v399, o selo ACOM, a declaracao do operador ou o sidecar nao rodaram)", "(os oito registros com funcao, os registros por spec, os registros recriados da v404, da v403, da v402, da v401 ou da v399, o selo ACOM, a declaracao do operador ou o sidecar nao rodaram)")


_BS = chr(92)
def _gw_bloco(nos):
    """O bloco que poe ga_window_status no topo do um_absoluto.json emulado: o JSON do rito real o traz e a v405 o confere; o ensaio so guarda core e verdict; a emulacao le a constante do proprio candidato, nunca de ESPERADOS."""
    return ('# v405 (desvio do molde, dito): o JSON do rito real traz ga_window_status no topo e a v405 o confere; o ensaio so guarda core e verdict: a emulacao o le da constante do proprio candidato, nunca de ESPERADOS\n'
            'import ast as _ast\n'
            '_cj = rdj(os.path.join(' + nos + ', "um_absoluto.json")); _gw = re.search(r"^GA_WINDOW_STATUS = ' + _BS + '((.*?)' + _BS + ')' + _BS + 'r?$", open(os.path.join(' + nos + ', "um.py"), "rb").read().decode("utf-8"), re.S | re.M); assert _gw, "a constante GA_WINDOW_STATUS nao esta no candidato"\n'
            '_cj["ga_window_status"] = _ast.literal_eval("(" + _gw.group(1) + ")")\n'
            'open(os.path.join(' + nos + ', "um_absoluto.json"), "w", encoding="utf-8").write(json.dumps(_cj, ensure_ascii=False, default=str))\n')


_ht_1 = ARQS["harness_textos_ensaio_v405.py"]; _hf_1 = ARQS["harness_fechar_sandbox_v405.py"]


@regras("harness_textos_ensaio_v405.py")
def _harness_textos_2(x):
    _ht_1(x)
    a = 'shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(NOSE, "tgl_kernel"))\n'
    x.sub(a, a + _gw_bloco("NOSE"))


@regras("harness_fechar_sandbox_v405.py")
def _harness_fechar_2(x):
    _hf_1(x)
    a = 'shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(NOSS, "tgl_kernel"))\n'
    x.sub(a, a + _gw_bloco("NOSS"))


_leitura_2b = ARQS["leitura_v405.py"]


@regras("leitura_v405.py")
def _leitura_3(x):
    _leitura_2b(x)
    x.sub("('veredito_projecao', (RF_.get('projecao') or {}).get('verdict'), 'projecao_transversal_v404'), ('veredito_jo8v32', (RF_.get('jo8v32') or {}).get('verdict'), 'jo8v32_v404'), ('veredito_f2b', (RF_.get('f2b') or {}).get('verdict'), 'f2b_errata_v404')):",
          "('veredito_projecao', (RF4_.get('projecao') or {}).get('verdict'), 'projecao_transversal_v404'), ('veredito_jo8v32', (RF4_.get('jo8v32') or {}).get('verdict'), 'jo8v32_v404'), ('veredito_f2b', (RF4_.get('f2b') or {}).get('verdict'), 'f2b_errata_v404')):")


exec(compile(open(os.path.join(HERE, "adaptar_regras3_v405.py"), encoding="utf-8").read(), "adaptar_regras3_v405.py", "exec"))
