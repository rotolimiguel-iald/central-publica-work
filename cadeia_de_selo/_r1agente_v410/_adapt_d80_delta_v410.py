# -*- coding: utf-8 -*-
"""_adapt_d80_delta_v410.py -- D80 (09/11/2026, ordem do operador ratificada por sha256; AO LADO do DESENHO_v410): o recibo documental HMS/13 do Kimi ENTRA na v410 como o TERCEIRO registro com FUNCAO, h0dn_fontes_hms13_v410,
ADITIVO e POSTERIOR ao FREEZE_R2. Este script leva ao delta_v410.py: (1) as constantes do registro (nome, pasta de origem -- o BUILD le, o RITO nao --, os QUATRO artefatos embutidos, os dez campos obrigatorios da ORDEM §3.7, a guarda numerica,
o veredito, a ratificacao por sha256 LIDA do DESENHO, o trecho citavel); (2) REGISTROS_FUNCAO com os tres; (3) as decisoes D78, D79 (com a D79b) e D80 em DECISOES e DECISOES_V410; (4) a leitura da ratificacao em LEITURA_V410; (5) o trecho entre as
excecoes da guarda das frases. Os textos das decisoes NAO trazem os nomes vedados de dado observado (o gerador os recusa no candidato). Backup de bytes; trocas exatas; ast.parse; LF preservado."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
P = os.path.join(HERE, "delta_v410.py"); b0 = open(P, "rb").read(); assert b0.count(b"\r\n") == 0
bk = P + ".bak_" + TS + "_d80"; open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")
assert "HMS13_REGISTRO" not in t, "o delta ja' traz a D80"


def troca(a, b, n=1):
    global t
    c = t.count(a); assert c == n, (c, n, a[:120]); t = t.replace(a, b)


# (1) + (2): as constantes do registro e os TRES registros com funcao
troca('REGISTROS_FUNCAO = [FECHO_REGISTRO, H0DN_REGISTRO]              # os DOIS registros com FUNCAO da v410 (D72): iald2_v410 e, logo depois, h0dn_bg1_v410\n',
      '# ---------------------------------------------------------------- D80 (09/11/2026, ordem do operador, ratificada por sha256; AO LADO do DESENHO): O RECIBO DOCUMENTAL HMS/13 DO KIMI ENTRA NA v410 -- o TERCEIRO registro com FUNCAO, ADITIVO e POSTERIOR ao FREEZE_R2 (os 9 pinos do congelamento e os 11 do H0DN nao mudam);\n'
      '# os limites da ORDEM do Kimi (ORDEM_CLAUDE_UMPY_HMS_13.md, [DECLARADO pelo Kimi; hashes lidos]) valem como contrato. O BUILD (gerar_candidato) le estes artefatos documentais por bytes e sha256; o RITO (este registro e qualquer outro) NAO abre nada de kimi\\.\n'
      'HMS13_REGISTRO = "h0dn_fontes_hms13_v410"\n'
      'TAG_HMS13 = "H0DN_FONTES_HMS13"\n'
      'HMS13_DIR = os.path.join(H0DN_PASTA_VEDADA, "revisao_independente")   # a pasta do pacote de revisao do Kimi: so\' o BUILD a le (D80 refina a D78); o rito nao\n'
      'HMS13_HANDOFF_ARQ = os.path.join(HMS13_DIR, "HANDOFF_CLAUDE_UMPY_HMS_13.json")\n'
      'HMS13_ORDEM_ARQ = os.path.join(HMS13_DIR, "ORDEM_CLAUDE_UMPY_HMS_13.md")\n'
      'HMS13_ORDEM_SHA16_DO_DESENHO = re.search(r"`revisao_independente\\\\ORDEM_CLAUDE_UMPY_HMS_13\\.md` \\(sha16 `([0-9a-f]{16})`", _DESENHO_TXT).group(1)   # LIDO do DESENHO (D79); conferido contra o arquivo no build\n'
      'HMS13_RATIFICACAO_ARQ = os.path.join(WK, "cunhagens_13out", "OPERADOR_09nov_vibrato_insignia_nome_inalcancavel_e_ratificacao_hms13_verbatim.txt")   # a fala do operador (09/11); so\' a frase final e\' a ratificacao a citar (D80)\n'
      'HMS13_RATIFICACAO_SHA256_DO_DESENHO = re.search(r"ratificacao_hms13_verbatim\\.txt`, sha256 `([0-9a-f]{64})`", _DESENHO_TXT).group(1)   # LIDO do DESENHO (D80); conferido contra o arquivo no build\n'
      'HMS13_TRECHO_RATIFICACAO = "o kimi fezz o trabalho e já te entregou"   # D80: a frase final da fala, com a grafia dele; a cunhagem que a antecede NAO entra na v410 (fica registrada para a v411); o arquivo inteiro entra so\' por sha256\n'
      'HMS13_EMBUTIDOS = [("MAPA_FONTES_E_COVARIANCIA_13.json", "MAPA_FONTES_E_COVARIANCIA_13.json"), ("MANIFEST_FONTES_PRIMARIAS.json", "fontes_primarias/MANIFEST_FONTES_PRIMARIAS.json"), ("VALIDACAO_FONTES_13.json", "VALIDACAO_FONTES_13.json"), ("LEVANTAMENTO_FONTES_PRIMARIAS_13.md", "LEVANTAMENTO_FONTES_PRIMARIAS_13.md")]   # SOMENTE estes quatro (D80; ORDEM §3.2-3.5): nem PDFs, nem textos dos artigos, nem o vetor observado, nem a covariancia, nem o validador\n'
      'HMS13_CAMPOS = {"estatuto": "REAL_DOCUMENTAL__PHYSICS_OPEN", "fontes_primarias": 18, "calibradores": 13, "partial_components_only": True, "full_13x13_covariance_available": False, "within_SN_full_decomposition_available": False, "physical_covariance_closed": False, "independent_physical_review_complete": False, "full_HMS_admitted": False, "opening_allowed": False}   # os dez campos obrigatorios da ORDEM §3.7, exatamente\n'
      'HMS13_NUMEROS_PERMITIDOS = ("bytes", "line", "text_characters", "count", "sigma", "error")   # D80 (guarda fail-closed no build e no rito): nos artefatos embutidos, numero so\' em chave que traga um destes radicais (bytes, contagens, numeros de linha, caracteres de texto, componentes de erro: sigma, error, mu_error)\n'
      'HMS13_COMPRIMENTOS_PROIBIDOS = (255, 64)                           # toda lista numerica e\' proibida nos artefatos; as de 255 ou 64 (o vetor observado; os valores publicados) sao ditas a parte\n'
      'N_CHECKS_HMS13 = 12\n'
      'VEREDITO_HMS13_OK = "TGL_H0DN_FONTES_HMS13_V410__DOCUMENTARY_COVERAGE_18_PRIMARY_SOURCES_FOR_13_CALIBRATORS__PARTIAL_ERROR_COMPONENTS_ONLY__PHYSICAL_COVARIANCE_OPEN__FULL_HMS_NOT_ADMITTED__OPENING_NOT_ALLOWED__ADDITIVE_AFTER_FREEZE_R2__NO_OBSERVED_VECTOR_READ__GATE_UNMOVED"\n'
      'VEREDITO_HMS13_RECUSA = "TGL_H0DN_FONTES_HMS13_V410__REFUSED_%s__GATE_UNMOVED"\n'
      'FRASE_HMS13_OBRIGATORIA_PT = "cobertura documental de fontes, não covariância física fechada; nada aberto"   # D80: OBRIGATORIO em todo texto do registro HMS/13\n'
      'FRASE_HMS13_OBRIGATORIA_EN = "documentary source coverage, not a closed physical covariance; nothing opened"\n'
      'REGISTROS_FUNCAO = [FECHO_REGISTRO, H0DN_REGISTRO, HMS13_REGISTRO]   # os TRES registros com FUNCAO da v410 (D72, D80): iald2_v410; logo depois, na mesma instrucao do main, h0dn_bg1_v410; logo depois, h0dn_fontes_hms13_v410 (aditivo e posterior ao FREEZE_R2)\n')
# (3) as decisoes D78, D79 (com a D79b) e D80 -- sem os nomes vedados de dado observado
troca('DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77")\n',
      'DECISOES.update({\n'
      '    "D78": ("registro, nao decisao (09/11/2026, AO LADO do DESENHO): a entrega do Kimi K3 Pro a ORDEM_KIMI_H0DN_01 comecou PARCIAL: o vetor observado montado linha a linha (255 linhas; A, C, nomes das linhas e dos parametros identicos ao FREEZE_R2) e a construcao dele sem solver, sem evaluate, sem Z nem razao [DECLARADO pelo Kimi; lido do arquivo]; "\n'
      '            "o teste de suporte na covariancia publicada REPROVOU [REAL, lido pela gerencia; o numero nao entra aqui]: as 72 direcoes de variancia zero de C nao comportam o vetor montado como valor reportado; leitura [DERIVED]: parede de montagem do dado, nao falsificacao da lei K nem leitura de beta_TGL; se a abertura fosse hoje, "\n'
      '            "a funcao de veredito devolveria o ramo (1) inconclusivo por sistematica; a covariancia fisica (G3/G4) nao foi entregue; para a v410 nada muda: pré-registrado; nenhum dado observado lido"),\n'
      '    "D79": ("registro e decisao (09/11/2026, ~15:40, AO LADO do DESENHO): a entrega do Kimi fechou em BLOQUEADA (G1 candidato forte derivado; G2 identidade e proveniencia fechadas; G3/G4 obstrucao exata, covariancia fisica aberta; a forma HMS completa passa no suporte mas NAO e\' admitida, porque a diagonal HMS ja\' esta em mu_error e duplicaria variancia: diagnostico, nao admissao; "\n'
      '            "abertura nao permitida; nenhum Z, solver ou evaluate) [DECLARADO pelo Kimi; 23/23 hashes conferidos por script]; e o Kimi enderecou a gerencia a ORDEM de incorporar ao um.py so\' o recibo documental das 18 fontes primarias dos 13 calibradores, aditivo e posterior ao FREEZE_R2, sem ler o pacote no rito. "\n'
      '            "Decisao da gerencia na hora: (1) a v410 nao muda (a D78 vale tambem para revisao_independente); (2) a incorporacao fica PENDENTE de ratificacao do operador (ordem de IA a IA nao substitui a palavra dele); (3) recomendacao: candidata ao lado (v411 ou posterior). "\n'
      '            "D79b, correcao em nome proprio da gerencia: os quatro depositos do Kimi na fila ficaram NAO_REGISTRADO (o campo quem nao e\' o dono do diretorio), intactos; a substancia esta registrada pela gerencia, com hashes lidos, no topico h0dn-bg1-teste-5sigma-06nov.md e na propria D79; nada da entrega se perdeu"),\n'
      '    "D80": ("ordem do operador (09/11/2026, ~15:45; fala verbatim inteira em work\\\\cunhagens_13out\\\\OPERADOR_09nov_vibrato_insignia_nome_inalcancavel_e_ratificacao_hms13_verbatim.txt, por sha256; a frase final e\' a ratificacao: «" + HMS13_TRECHO_RATIFICACAO + "» + o caminho do HANDOFF do Kimi): a incorporacao documental HMS/13 ENTRA na v410, "\n'
      '            "como um registro NOVO, ADITIVO e POSTERIOR ao FREEZE_R2 (h0dn_fontes_hms13_v410; os 9 pinos do congelamento e os 11 do H0DN nao mudam), com estatuto REAL_DOCUMENTAL__PHYSICS_OPEN e os dez campos obrigatorios da ORDEM do Kimi (fontes_primarias 18, calibradores 13, partial_components_only, e as seis bandeiras falsas: "\n'
      '            "full_13x13_covariance_available, within_SN_full_decomposition_available, physical_covariance_closed, independent_physical_review_complete, full_HMS_admitted, opening_allowed); embutidos em BUILD, por bytes e sha256, so\' o mapa de fontes e covariancia, o manifesto das fontes primarias, a validacao e o levantamento legivel (para o artigo); "\n'
      '            "NAO os PDFs, NAO os textos dos artigos, NAO o vetor observado, NAO a covariancia, NAO centros observados, NAO o validador. A D78 fica refinada: o BUILD pode ler esses artefatos da pasta do Kimi; o RITO continua NAO abrindo nada de kimi\\\\ (o controle negativo do p00 mede «nenhuma leitura em rito»; o espelho da casa continua excluindo a pasta). "\n'
      '            "Guarda fail-closed no build: se um artefato embutido trouxer valor do vetor observado, modulo de distancia de calibrador ou centro fotometrico, o build PARA e avisa a gerencia (a cobertura documental e\' de fontes, hashes, IDs e componentes de erro). veredito_h0dn, FREEZE_R2, outcomes e chaves antigas preservados; gate identico ao baseline; nenhuma semente nova; nenhum Z. "\n'
      '            "Custo aceito: a cadeia reabre do candidato (o anterior guardado ao lado como .pre_hms13). A cunhagem que antecede a ratificacao na mesma fala fica registrada na memoria para a v411 e NAO entra na v410 (provar ou podar: a palavra no um.py pede o espelho no kernel); o nome e\' dele"),\n'
      '})\n'
      'DECISOES_V410 = ("D63", "D64", "D65", "D66", "D67", "D68", "D69", "D70", "D71", "D72", "D73", "D74", "D75", "D76", "D77", "D78", "D79", "D80")\n')
# (4) a leitura da ratificacao
troca('LEITURA_V410 = {\n',
      'LEITURA_V410 = {\n'
      '    "a_ratificacao_hms13": "«" + HMS13_TRECHO_RATIFICACAO + "» [INPUT]: a ratificacao do operador (09/11/2026) da incorporacao documental HMS/13 (D80): ele aponta o HANDOFF do Kimi e manda incorporar; o resto da fala (uma cunhagem do operador) NAO entra na v410 -- fica registrada para a v411 -- e o arquivo inteiro entra so\' por sha256; "\n'
      '                           "o que entra e\' cobertura documental de fontes (18 fontes primarias dos 13 calibradores), nao covariancia fisica fechada; nada aberto",\n')
# (5) o trecho entre as excecoes da guarda das frases (e\' fala do operador: fica fora das regras novas quando citado)
troca('FRASES_VERBATIM_V410 = sorted({fr_ for _, fr_ in FRASES_V410} | {FRASE_NOME_DO_ALGORITMO, FRASE_RELER, FRASE_POR_IDENTIFICACAO, FRASE_SELETOR_CURTA, FRASE_RECONHECIMENTO, FRASE_REPRESENTACAO_DE_BETA, FRASE_SENTIDOS}, key=len, reverse=True)',
      'FRASES_VERBATIM_V410 = sorted({fr_ for _, fr_ in FRASES_V410} | {FRASE_NOME_DO_ALGORITMO, FRASE_RELER, FRASE_POR_IDENTIFICACAO, FRASE_SELETOR_CURTA, FRASE_RECONHECIMENTO, FRASE_REPRESENTACAO_DE_BETA, FRASE_SENTIDOS, "o kimi fezz o trabalho e já te entregou"}, key=len, reverse=True)   # (D80: a frase final da ratificacao, so\' ela, e\' fala do operador citavel)')
nb = t.encode("utf-8"); ast.parse(nb)
tmp = P + ".tmp_" + TS; open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb); os.replace(tmp, P)
print("delta_v410.py", len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16])
# conferencia: o delta importa e os novos nomes existem
sys.path.insert(0, HERE)
import importlib
DL = importlib.import_module("delta_v410")
assert DL.REGISTROS_FUNCAO == ["iald2_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410"] and DL.DECISOES_V410[-1] == "D80" and len(DL.DECISOES_V410) == 18 and DL.N_CHECKS_HMS13 == 12
assert len(DL.HMS13_ORDEM_SHA16_DO_DESENHO) == 16 and len(DL.HMS13_RATIFICACAO_SHA256_DO_DESENHO) == 64
print("ORDEM sha16 (DESENHO):", DL.HMS13_ORDEM_SHA16_DO_DESENHO, "| ratificacao sha256 (DESENHO):", DL.HMS13_RATIFICACAO_SHA256_DO_DESENHO[:16], "| N_FALAS", DL.N_FALAS_V410, "| N_CHECKS_FECHO", DL.N_CHECKS_FECHO)
for _n in ("y_obs", "CONSTRUCAO_Y_OBS", "C_fisica", "ENTREGA_H0DN_Y_OBS"):
    assert _n not in DL.DECISOES["D78"] + DL.DECISOES["D79"] + DL.DECISOES["D80"] + DL.LEITURA_V410["a_ratificacao_hms13"], _n
print("ok")
