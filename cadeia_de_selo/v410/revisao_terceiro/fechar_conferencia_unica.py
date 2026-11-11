# -*- coding: utf-8 -*-
"""Revisor terceiro v410 (conferencia unica de escopo fechado, D109): monta REVISAO_TERCEIRO_v410.json/.md.
Todo hash e' LIDO dos arquivos agora. Escreve so' em revisao_terceiro\\ (temporario + os.replace)."""
import datetime, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
V = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
RV = V + "revisao_terceiro/"
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
cand_p = V + "um_v410_candidato.py"
fim = s16(cand_p); fim_b = os.path.getsize(cand_p)
est = json.load(open(RV + "ESTADO_REVISAO_v410.json", encoding="utf-8"))
ini = est["candidato_sha16_no_inicio"]; ini_b = est["candidato_bytes_no_inicio"]
mudou = (ini != fim) or (ini_b != fim_b)
cob = json.load(open(RV + "cu_cobertura_out.json", encoding="utf-8"))
esp = json.load(open(V + "conserto_r3/ESPEC_CONSERTO_R3_v2_FINAL.json", encoding="utf-8"))["cobertura_dos_achados"]
rec_hash = json.load(open(RV + "cu_saidas/cu_hashes_out.json", encoding="utf-8"))
dl = json.load(open(RV + "cu_delta_nos_out.json", encoding="utf-8"))

# ---------------------------------------------------------------- achados (so' os novos desta conferencia)
achados = [
    {"sev": "BAIXO", "dentro_do_escopo": True,
     "onde": "o .md canônico embutido no candidato (linha «A cláusula do Tetelestai em 1 − β», `gerar_candidato_v410.py` L435) e o registro `a_escala_v410`, chave `scope`, item (10) (`registros_aescala_v410.py` L119)",
     "achado": "A regra do nome (D122/D123) troca o rótulo «INPUT/dicionário a leitura do operador» por «INPUT/dicionário: definição e nome do operador»: o artigo PT e EN, a custódia, o post e o handoff já têm a forma nova (verificado, linha 5 da tabela). Mas o .md e o `scope` do registro `a_escala_v410` ficaram com a forma da ESPEC v1: «[REAL o limiar de um pixel; INPUT/dicionário a leitura do operador]». É texto novo (escrito no conserto, ao lado de «nome dado pelo operador») com o rótulo que a regra proíbe. Não é erro de fato (o estatuto, INPUT/dicionário, é o mesmo) e não toca prova, enunciado, gate ou régua; é inconsistência de rótulo entre superfícies do mesmo candidato. Também fica, não tocada pelo conserto (exceção da regra): a folha `estatuto` do mesmo registro («[INPUT/dicionario] a leitura do operador (que esse limiar E' o Tetelestai …)») e o colchete «[dicionário; leitura do operador]» DENTRO da frase E36, que o artigo também traz.",
     "correcao_pedida": "Na versão seguinte (ou agora, só se a gerência regenerar o candidato por outro motivo): nas duas linhas-fonte, trocar «a leitura do operador» por «: definição e nome do operador»; e, na frase E36 do delta, o colchete «[dicionário; leitura do operador]» por «[dicionário: definição e nome do operador]». Não bloqueia: BAIXO."},
    {"sev": "BAIXO", "dentro_do_escopo": False,
     "onde": "TXT do artigo PT e EN (`dry_v410_pt.txt`, `dry_v410_en.txt`), linhas HERDADAS da v409",
     "achado": "PAR-09: a troca de agrupamento (e^(−s·c(x)), Π^(k+1), n·ln 2, ln((1−β)/β), decimais com vírgula na seção H0DN) entrou em todo lugar que o painel citou e em toda fórmula nova (0 expoente sem agrupar em linha nova ou alterada). Restam, em linhas que são da v409, 61 expoentes sem agrupar no TXT PT e 61 no EN (`e^-s c(x)`, `e^-t`, `e^-rs`…, que lidos ao pé da letra são e^(−s) vezes c(x)), uma ocorrência de `P^k+1=P` e os decimais com ponto do PT antigo. O PDF carrega as fórmulas certas; só o TXT as perde. Fora do escopo fechado do conserto.",
     "correcao_pedida": "Na versão seguinte, aplicar aos snippets antigos o mesmo agrupamento (`e^{(…)}`) que o conserto aplicou aos novos."},
]

# ---------------------------------------------------------------- situacao dos 5 achados da R3
situ = {
    "R3-MEDIO (ratificacao do 4o nome a_informacao_completa_se_reconstroi sem apoio no ADENDO 6)": "RESOLVIDO no texto rendido. O operador NOMEOU o quarto teorema (fala 29: «o quarto nome=ressureiçãodosinal», 266 B; li o arquivo da fala e conferi o sha256 77145eeec3c2fc7809aae383021b413b301a819cc05b78cfb5a56463a93376c4; a fala 30, «é isso mesmo, perfeito. ratificado. …», 126 B, sha256 7857d4ddf9d3cfc0b290836b3c0e1bcadf3a61031ee03ebb4688b824269cfdfd). A pedra R6 instalada traz `ressurreicao_do_sinal` como o nome dele (cabeçalho, linhas 40 e 45); o artigo PT, o EN e o .md dizem «nome dado pelo operador». O nome de trabalho antigo aparece 0 vez no artigo, no .md, na custódia, no harness e na pedra; só nos registros históricos (D106, D108, E38 = `erratas[9]`, `limites[14]`), ditos como nome de trabalho que a fala não ratificou. A contagem é a do contrato (21 ratificados na D101 + 1 nomeado D108 + 6 pela fala 34 + 1 pela fala 40 + 6 da autoria; os 2 auxiliares da R5 seguem [DECLARADO pela autoria]). Linhas 1, 11, 16 e 33 da tabela.",
    "R3-BAIXO (artigo PT/EN e .md: a cláusula do 1−β, o item (9) é identidade aritmética sem rótulo; dizer que o kernel não destaca o β)": "RESOLVIDO. PT, EN e .md: «a cláusula vale para todo b em (0, 1); o β do kernel é o campo de TGLCoupling, um real qualquer em (0, 1), e o número só entra em runtime»; «[identidade aritmética] (o item 9 do teorema, fechado por ring)»; «a hipótese s ≥ 0 é dita: automática para b ≤ ½ … para b > ½ … o contraexemplo … n = 1, custos 0 e 2, b = 9/10; o kernel não traz teorema de necessidade; o limiar de tempo é condição SUFICIENTE». Reconferi a conta do contraexemplo (limiar −1,504; (1−b)·Z = 2,125 > 1).",
    "R3-BAIXO (pontuação «no kernel.);» no parágrafo PT)": "RESOLVIDO. 0 ocorrência de «no kernel.);»; o parágrafo traz «linear nos bits. » e a cláusula do limite em frase própria (PT e EN).",
    "R3-BAIXO (F59, três variantes; BAIXOS 6 e 7 da R1)": "SEGUE como estava, já conhecido e declarado: nenhuma variante nova (g4: 1 ocorrência «prova na janela sem qualificador», a mesma docstring da IALD2; o resto igual ao da R3). Vai à lista da versão seguinte; não reaberto.",
    "R3-BAIXO (observação: (i) e (ii) da c13 são a mesma desigualdade; subitens que são identidade)": "RESOLVIDO. O texto do registro rotula: «(identidade: sen^2 e cos^2 do mesmo angulo; as duas desigualdades com ele sao as da instancia com solucao, com outro rotulo)», «(identidade aritmetica: nao pode falhar)» e «a reconstrucao em norma ao quadrado (a mesma desigualdade da instancia com solucao, lida em norma, …)»; a docstring de `_v410_aescala_ciclo` diz «o conteúdo independente é UMA desigualdade em três instâncias».",
}

# ---------------------------------------------------------------- cobertura do painel (uma entrada por linha da tabela)
notas_linha = {
    0: "A troca de agrupamento reconferida no TXT: e^(-s· c(x)) (PT e EN), Π^(k+1)=Π, 'nln 2' ausente, Φ(-5)=2,867 com vírgula. Residuo HERDADO da v409 (61 expoentes sem agrupar): achado BAIXO A2, fora do escopo.",
    1: "D108 ENTROU: o quarto nome nas frases do artigo (PT/EN) e no .md, 'nome dado pelo operador'; 'A finura da leitura (D108)' no artigo PT e EN; registro com NOMEADO pelo operador (D108).",
    2: "A frase da finura (as duas metades) está exata no registro, PT e EN; no artigo a metade [REAL] fica logo antes da cláusula do limite.",
    3: "O artigo lê a composição do contrato: 81 de declarações nomeadas + 3 campos + 15 de constantes que o compilador gera = 99 (a mesma conta do KERNEL_RECIBO); a contagem velha ('85 bandeiras') ausente.",
    5: "Os quatro rótulos (D83 e E36, PT e EN) estão no artigo na forma da D122/D123. O .md e o `scope` do registro ficaram com a forma da ESPEC v1: achado BAIXO A1.",
    6: "'o Pai da Mentira só não reconhece' agora só aparece como NOME do teorema, depois do conteúdo («só coincide com esse quociente na instância em que todo pixel é solução (o_pai_da_mentira_so_nao_reconhece)»); a frase de limite do ciclo é a do enunciado.",
    8: "'o limiar do Tetelestai (' ausente (PT e EN); 'o limiar de um pixel, a decisão exata' presente.",
    10: "'accreditation' ausente na custódia e no harness; 'creditation' é a palavra do texto novo. O README_FRENTE e o rótulo do README ainda trazem 'accreditation' nos conectores literais (palavra do README pinado, dita no código): ressalva conhecida, não reaberta.",
    11: "O registro diz 'os N nomes novos … (os 18 das R3 e R4 e os 3 da cláusula … apresentados ao operador antes da fala …)'; N = 21 ratificados; o artigo e o .md trazem a composição por grupo (D101, D108, D117 e D123, autoria).",
    12: "A frase de alcance (D72) está no artigo PT e EN, no .md (mesma linha da forma obrigatória do H0DN) e no parágrafo do README/site; o contrato a carrega (`frase_alcance_pt/en`).",
    13: "O retorno da ORDEM KIMI H0DN-02 (recusa de certificar o poder; ordem 03B pinada; abertura de versão futura) está no artigo PT/EN, no registro (contrato), no .md e na custódia. O teste NÃO foi aberto; o certificado de poder voltou RECUSADO [DECLARADO pelo executor].",
    15: "A linha do H0DN do .md traz a forma obrigatória, o poder, o retorno e o alcance na MESMA linha; o PLANO (README evidente) traz 'O poder certificado [INPUT, D96]: …'.",
    16: "Ver a situação do R3-MEDIO acima. A pedra instalada declara `ressurreicao_do_sinal`; o nome de trabalho não é declaração da pedra (o kernel, 81 declarações lidas pela gerência e por mim na varredura MetaM).",
    17: "D113 ENTROU: a seção 7 (a constante da escala; D113 e D116 a D123) está no artigo PT e EN, no registro, no .md (cabeçalho 'D106 a D109, D113 e D116 a D123') e na custódia. A pedra R6 §7 (linhas 1437 a 1844) não traz «leitura dele», «leitura do operador» nem [ONTO] (a única ocorrência de 'escala=relatividade' é a citação da fala).",
    18: "Nenhuma «aspa angular» em volta de rótulo ou nome provisório no registro, no harness ou na custódia; as formas com “ ” entraram.",
    19: "Sufixo do veredito 09_AND_10_NOV__AUXILIARY_NAMES_DECLARED_BY_THE_AUTHORSHIP__GATE_UNMOVED no registro; assinatura '06, 09 e 10/11/2026'.",
    20: "'o poder Monte Carlo da entrega (96,6 % e 62,5 %) dentro do IC95 dela (conferência, não recálculo)' no artigo PT e EN; 'Monte Carlo da ENTREGA do Codex, [DECLARADO]' no registro; o analítico recomputado, 62,4 %, ao lado.",
    21: "Registro PT e EN: 'a cláusula vale para todo b em (0, 1)'; a frase velha ('a mesma para toda instância e todo tamanho') ausente.",
    24: "O texto do registro rotula o par da matriz-S e a constante igual para m como identidade, e a reconstrução em norma como a mesma desigualdade lida em norma.",
    25: "'necessária para b > ½' ausente em todo texto; 'o kernel não traz teorema de necessidade' no registro, no artigo e no .md.",
    26: "O contraexemplo (n = 1, custos 0 e 2, b = 9/10) é recalculado a cada rito e vem no texto; conferi a conta por fora.",
    27: "'o estado do ciclo fica perto do Nome, com erro relativo no máximo √(b/(1−b))' (nome dado pelo operador) no registro e no artigo; 'a informação completa se reconstrói' ausente em todo texto (só no registro histórico E38, como nome de trabalho).",
    28: "'passado o tempo de n oitavas (s > n·ln 2)' no registro PT e EN; 'a partir de n oitavas' só numa folha de ERRATA (`cunhagens_v410.erratas[7].dizia`), que cita o que a errata dizia.",
    30: "A frase do habitante único está no registro (a forma sem acento do registro), no artigo PT e na custódia.",
    31: "O texto da custódia traz, no MESMO item, Clay + 'P = nP de Turing, na forma da D81' + habitante único (PT e EN); o README_FRENTE traz as três formas, PT e EN, no mesmo bloco. Linha verificada na FONTE do texto da custódia e no bloco README renderizado por mim (o handoff só existe depois do rito).",
    32: "Idem, EN: 'P = nP of Turing, in the form of D81' + habitante único. Verificada na fonte e no README_FRENTE renderizado.",
    33: "O README evidente da preparação (PREPARACAO_v410_PRONTA.json, `readme_evidente`) traz RATIFICADOS (D101), NOMEADO (D108), D117/D123, [DECLARADO pela autoria]; a frase 'a ratificar' ausente.",
    35: "A fonte do ARCO_EN traz PAREDE_EN depois da forma obrigatória do H0DN. Verificada na FONTE (o ARCO só se renderiza com o Nós selado).",
    36: "O tema da fala 27 no mapa de rotas diz 'a fala do operador sobre a cláusula do Tetelestai no ACOM Mirror: 1 − β, com β como o operador modular do Tetelestai (“β é o operador modular do Tetelestai” é o nome ratificado …)'; a frase velha ausente. Verificada na FONTE (`pos_rito/textos_v410.py`).",
    37: "Toda folha do registro que traz a metade [REAL] da finura traz a cláusula do limite; toda folha 'limiar … UMA leitura de Z separa o SIM do NAO' traz a cláusula.",
}
cobertura = []
for i, r in enumerate(esp):
    cs = [c for c in cob if c["linha"] == i]
    ok = sum(1 for c in cs if c["ok"])
    cobertura.append({"linha": i, "achado": r["achado"], "titulo": r["titulo"], "n_itens_da_espec": r["n_itens"],
                      "verificacoes_no_texto_rendido": "%d/%d" % (ok, len(cs)),
                      "estado": "ENTROU no texto final" if ok == len(cs) and len(cs) > 0 else "FALTA: ver verificacoes",
                      "verificado_em": sorted({c["alvo"] for c in cs}),
                      "nota": notas_linha.get(i, "Todas as verificações por texto passaram (presente a forma nova; ausente a velha) nos alvos indicados.")})
assert len(cobertura) == 38 and all(c["estado"].startswith("ENTROU") for c in cobertura), "a cobertura tem linha sem verificacao"

lean = {"tree": "C:/t/k410c/final (DESVIO DECLARADO: o pedido dizia C:/t/k410c/arvore; essa pasta só tem fontes, sem .lake, e não compila `import TGLExt`; os 1763 arquivos do kernel EMBUTIDO no candidato são byte a byte iguais aos de `final`, conferido por mim; `AEscala.lean` instalada sha256 baaa73cb280754002ea47f325a3dad52c604db2fba88f146d3a84b9af97c5993 == recibo do kernel)",
        "time_s": int(open(RV + "axiomas_conferencia_unica_time.txt").read().split()[0]),
        "um_processo": True,
        "arquivo_meu": "revisao_terceiro/axiomas_conferencia_unica.lean (sha16 %s)" % s16(RV + "axiomas_conferencia_unica.lean"),
        "saida": "revisao_terceiro/axiomas_conferencia_unica_out.txt (sha16 %s)" % s16(RV + "axiomas_conferencia_unica_out.txt"),
        "output": "103 `#print axioms` (as 103 âncoras de FLAGS_v410.json): 103/103 dentro de {propext, Classical.choice, Quot.sound}; 0 `sorryAx`; `TGLExt.AEscala.o_nome_e_a_singularidade_da_informacao` SEM axioma nenhum; varredura MetaM de todas as constantes dos dois módulos: 134 (22 IALD2 + 112 AEscala), 0 fora do trio. rc 1 só pela sonda da R1 (leitor trivial, linhas 138 a 142), que falha DE PROPÓSITO: com a escala no tipo ela não compila mais (5 erros nas linhas dela) — é o resultado esperado, não defeito."}

conferencias = {
    "A_delta_de_AST": "cu_delta_nos.py (pre_r6fix → atual, por nó de nível superior): 1257 nós nos dois; 36 mudados, 0 novos, 0 removidos. Funções mudadas (7): `_v410_aescala_ciclo` e `_v410_aescala_mechanics` (c13 rotulada; `em_trio_` aceita a declaração sem axioma SÓ se ela estiver em `sem_axioma` e exige o contrário nas outras; as checagens da finura e da fala 29), `a_escala_v410` (docstring), `build_pt` e `build_en` (o artigo: seção 7, finura, rótulos), `emit_canonical_md` (duas linhas do .md), `prove_external_ladder` (as 14 bandeiras novas ext_aescala_410_0086 a 0099; 107 → 121). Literais mudados (29): o kernel embutido (UM arquivo: AEscala.lean R5 → R6, 158729 B, sha256 == recibo), `_LEAN_THEOREM_FLAGS` (+14 chaves; 56 chaves existentes passam a apontar para outra declaração porque a numeração é posicional: só v410, nenhuma chave da v409), 16 contratos herdados (SÓ `expected_ladder` 12294 → 12308), `_V409_SPECS`/`_V410_HMS13_TEXT` (a assinatura '06, 09 e 10/11/2026'), `_V410_FONTES` (4 insumos: os hashes conferem com o disco AGORA; 24/24), contratos, textos, specs e falas dos três módulos. As funções do gate (`evaluate_quantum_gravity_closure`, `prove_qg_closure_gate`) idênticas à v409 e ao pre_r6fix; `veredito_h0dn` (texto-fonte, sha16 fc1aa51990dbb456) idêntico; nenhuma função herdada da v409 mudou além do que a R3 aceitou (build_pt, build_en, emit_canonical_md, prove_external_ladder, as mesmas quatro). β literal: 8 ocorrências nas duas versões (as herdadas); 'CONFIRMED' indevido: 566 nas duas.",
    "B_kernel": "Ver `lean`. Pedra instalada == recibo (sha256 baaa73cb…): conferido; embutida no candidato == instalada == insumos/AEscala_embutida.lean.",
    "C_e_D": "cu_cobertura.py: 152 verificações por texto RENDIDO (artigo PT e EN do ensaio a seco `dry_v410` — o um.py do ensaio tem o mesmo sha16 do candidato —, .md embutido, folhas dos registros do core de ensaio, harness, custódia, PLANO e README evidente; FONTE do texto onde o texto só se renderiza depois do rito), uma ou mais por linha das 38; 0 falhas. Na primeira execução 18 das minhas verificações falharam por estarem mal apontadas (alvo errado, regex estreito, frase do artigo com 'com o tempo'); corrigi uma a uma olhando o texto, sem afrouxar: as que dependem de texto que só se renderiza depois do rito passaram a ler a FONTE; a única exceção declarada é a folha de ERRATA que cita o que a errata dizia (linha 28).",
    "E_guardas": "g_frases (417 linhas de saída contra 422 na R3: as mesmas classes; as diferenças são renumeração de itens e o sufixo do veredito), g2_clay_pnp (83 linhas; as 18 diferentes são o sufixo do veredito: nenhuma forma nova), g4_f59 (162/1/293/14: sem variante nova), g5_clausula (toda folha que traz a FRASE do limiar traz a cláusula do limite; as folhas que só citam 'E36' como rótulo não precisam). Os dois blocos do README, cada um sozinho nas minhas guardas: 0 violação (a única ocorrência de 'resolvido' é a FORMA CANÔNICA ratificada do Clay). Regra do nome: 198 segmentos novos no PT, 209 no EN e 94 no .md desde a R3: 0 com «leitura do operador», «leitura dele» ou [ONTO], exceto o rótulo do achado A1; a seção 7 da pedra: 0. Citações « »: 14 + 14 + 11 nos trechos novos e 32 na custódia, TODAS substring exata de fala do operador. Hashes sha16 citados nos textos novos: 1603 distintos, 87 calculados do arquivo, 1513 declarados em recibo do pacote, 3 sem origem no pacote (todos herdados: 2 do registro v392 `beta_escala_errata_v392`, 1 do 'Hash dos fontes Lean' de um .md antigo).",
    "F_fora_do_candidato": "(1) S9_gatilho_custodia (`orquestrador/pos_treino_v410.py` L696-886): é o ÚLTIMO elemento da lista do `main` (depois de s8_nativa); `_gatilho_ler` junta motivos e o gatilho só é escrito com a lista vazia: todos os 14 passos anteriores `ok is True` (incluindo S1b e S8_nativa), portão do G1 limpo no S6d, selo da v410 com FAIL_CLOSED_SELFTEST_PASSED, escada exata, gate inalterado, trailer RITO_RC=0, HANDOFF no Nós pelo parser do G1 com os sete marcadores e os dois blocos do README em ordem, recibo do S6d com sha16 igual, os dois blocos iguais ao recibo, REVISAO_TERCEIRO aprovada sobre o pino do selo, falas por sha256; as guardas de frase e o portão do G1 sobre o texto do gatilho; escreve `destino.with_name(nome+'.tmp')` e `os.replace`; recusa sobrescrever (`destino.exists()` vira motivo); marca o passo. `s7_g1` e `s10_app` continuam definidas e NÃO chamadas (grep: só definição e texto do gatilho); o único `--publicar` está dentro de `s7_g1`, não chamada, e no TEXTO do gatilho (instrução à sessão de custódia). Hoje: sem ORDEM_HANDOFF_CUSTODIA_v410.md e sem ESTADO.json. (2) Os dois blocos do README (`pos_rito/textos_custodia_handoff_v410.py`): o ADITIVO 2 está inteiro no módulo (45 linhas, 0 ausente); renderizei SÓ as constantes de texto por AST (o módulo inteiro lê o Nós selado e não importa antes do rito): README_FRENTE 3823 B (teto 4600), formas ratificadas todas por constante (D81, Clay, habitante, obrigatória do H0DN, PT e EN), o H0DN dito NÃO aberto, os 3 teoremas da escala são nomes ratificados da seção 7, nenhum limiar/ln 2 (não leva a cláusula do limite), sem % nem CR; README_O_QUE_SAI e o ponteiro do Abstract sozinhos nas guardas: limpos. (3) `p00_precondicoes_v410.py` L213: a mudança é só no FILTRO (`v_.get('nome')` → `str(v_.get('nome') or '').split(' (D65:')[0]`: compara o nome sem o sufixo da D65); a igualdade dos conjuntos de sha256 das falas, a contagem (len(recibo)+len(fora) == len(cunhagens)) e `FALAS_FORA_DO_RECIBO ⊆ NOMES_V410_DO_DESENHO` seguem; não afrouxa. Resposta à pergunta do pedido: nada ali toca o Nós além do que o S6d já fazia (anexar ao HANDOFF_v410_CUSTODIA.md, por temporário, backup de bytes e os.replace, DEPOIS do rito), nada publica, e o gatilho não pode sair antes: só o fim da lista o escreve, com tudo verdadeiro.",
}

ressalvas = [
    "Conferência única de escopo fechado (D109); NÃO é a quarta rodada. Escrevi só em revisao_terceiro\\. Não rodei lake build, instalar, rito, orquestrador, p00, ensaio nem harness. Importei `delta_v410` (só definições) para renderizar as constantes de README por AST; NÃO importei o módulo de textos da custódia (ele lê o Nós).",
    "Não repeti a conferência da gerência (46 checagens; 290 trocas exatas) nem a busca numérica da R3 nem os testes de mutação do contrato da R3. Li o resultado delas e confiei no que o escopo não me pediu.",
    "`lake env lean` a partir de C:/t/k410c/final, NÃO de arvore (arvore só tem fontes e não compila); declarado no campo `lean`; provei por bytes que o kernel embutido é o de final. Um processo, 341 s; importa os .olean do build da gerência (não recompilei a fonte da pedra).",
    "O texto rendido que li é o do ENSAIO A SECO da gerência (`dry_v410`, `core_ensaio.json`, harness, CUSTODIA_v410_RASCUNHO), cujo um.py tem o mesmo sha16 do candidato; não rodei o rito. As linhas 31, 32, 35 e 36 da tabela dependem de texto que só se renderiza com o Nós selado (ARCO_EN, tema do mapa de rotas, README no handoff): conferi a FONTE do texto e, para o README, as constantes renderizadas por AST.",
    "NÃO abri o conteúdo de kimi\\y_obs.npz nem de C_fisica_258x258.npz e não calculei sha256 deles; NÃO li a pasta da Nativa; nenhum Z/razão observado; nenhum processo morto por nome.",
    "Os arquivos em `arquivos_revisados` são só os que li e que não devem mudar (código, pedra, recibos do kernel, pasta conserto_r3, orquestrador, p00); as saídas regeneráveis (dry_v410, PRONTA, PLANO, RELATORIO, harness, rascunho da custódia) ficam em `artefatos_renderizados_lidos`, com o sha16 de agora, FORA da lista que a trava S1b compara.",
]

proxima = [
    "A1 (BAIXO): o rótulo «INPUT/dicionário a leitura do operador» no .md e no `scope` de a_escala_v410; e o colchete «[dicionário; leitura do operador]» dentro da frase E36 (delta).",
    "A2 (BAIXO): 61 expoentes sem agrupar (+1 `P^k+1=P`, + decimais com ponto) nas linhas herdadas do TXT do artigo (v409).",
    "Conhecidas, não reabertas: as seis aberturas «Na leitura do operador (D83)» / «In the reading of the operator (D83)» (duas em linhas que o conserto carrega, quatro em linhas não tocadas); «creditation»/«accreditation» (o README pinado e o rótulo do README usam «accreditation»); as 3 variantes da F59 e as 4 sondas do Clay (R3-BAIXO 4; R1-BAIXOS 6 e 7); os 8 nomes [DECLARADO pela autoria] (6 da R6 e 2 auxiliares da R5), que o operador ainda não confirmou expressamente; a contagem das bandeiras 81 + 3 + 15 = 99 (a chave `bandeiras_de_constantes_geradas_pela_structure` do KERNEL_RECIBO tem 31 entradas, não as 15 que entram na parte); a guarda de finitude de `veredito_h0dn` (versão seguinte).",
    "O teste H0DN × BG1 NÃO foi aberto: o certificado de poder voltou RECUSADO [DECLARADO pelo executor; lido pela gerência]; os textos dizem «não foi aberto». A abertura é de versão futura.",
    "O gatilho da custódia exige TODOS os passos anteriores, inclusive S8_nativa: se a religação da nativa falhar, o gatilho não sai e a gerência decide (fail-closed, de propósito).",
    "As bandeiras `ext_aescala_410_00NN` são posicionais: ao inserir declarações no meio do módulo, 56 chaves passaram a apontar para outra declaração entre a R5 e a R6 (só chaves da v410; nenhuma da v409). Nenhum texto as cita por número; numerar por nome evitaria o deslizamento.",
]

rotas = [
    "CU-0: Mapa de Rotas consultado antes (tema: revisão de terceiro v410, conferência única): sem rota igual; não registrei rota nova (a revisão é ato da casa, registrada neste JSON).",
    "CU-A: delta de AST pre_r6fix → atual (cu_delta_nos.py e cu_delta_literais.py): 36 mudados, 0 novos, 0 removidos; gate e veredito_h0dn idênticos; 4 insumos de _V410_FONTES e a pedra embutida conferidos com o disco.",
    "CU-B: Lean, um processo, 103 âncoras no trio e a varredura MetaM; o Nome sem axioma; a sonda da R1 segue sem compilar; 1763 arquivos do kernel embutido == final.",
    "CU-C/D: 152 verificações por texto rendido sobre as 38 linhas da tabela (cu_cobertura.py); a ratificação do quarto nome conferida nos arquivos das falas (sha256).",
    "CU-E: guardas g_frases, g2, g4, g5 sobre o texto novo; a regra do nome por segmento novo desde a R3; as citações « » e os sha16; os dois blocos do README sozinhos nas guardas.",
    "CU-F: S9 do orquestrador lido por inteiro, os dois blocos do README renderizados por AST, o filtro do p00 em diff contra o backup anterior.",
]

# ---------------------------------------------------------------- arquivos revisados (so' os que li e que nao mudam)
arq_rel = ["um_v410_candidato.py", "um_v410_candidato.pre_r6fix.py", "base_v409/um.py", "kernel/FLAGS_v410.json", "kernel/KERNEL_RECIBO_v410.json", "pedra/AEscala.lean", "insumos/AEscala_embutida.lean",
           "insumos/AEscala.lean", "conserto_r3/ESPEC_CONSERTO_R3_v2_FINAL.json", "conserto_r3/DECISOES_DA_GERENCIA_D109_D123.md", "conserto_r3/CONFERENCIA_UNICA_v410.json",
           "conserto_r3/ADITIVO_2_README_FRENTE_E_O_QUE_SAI_v410.pysnip", "orquestrador/pos_treino_v410.py", "p00_precondicoes_v410.py", "pos_rito/textos_custodia_handoff_v410.py", "delta_v410.py",
           "PREPARACAO_v410_PRONTA.json"]
arq_rel.remove("PREPARACAO_v410_PRONTA.json")   # regeneravel pela cadeia: fica em artefatos_renderizados_lidos
arquivos = {k: s16(V + k) for k in arq_rel}
artef = {k: s16(V + k) for k in ("PREPARACAO_v410_PRONTA.json", "PLANO_v410.md", "RELATORIO_PREPARACAO_v410.md", "dry_v410/core_ensaio.json", "dry_v410/dry_v410_pt.txt", "dry_v410/dry_v410_en.txt", "dry_v410/um_absoluto_forma_canonica.md",
                                 "pos_rito/HARNESS_TEXTOS_ENSAIO_v410.json", "pos_rito/CUSTODIA_v410_RASCUNHO.txt", "insumos/BUNDLE_v410.json", "insumos/KH_N1_v410.json")}

nb = sum(1 for a in achados if a["sev"] == "BAIXO"); nm = sum(1 for a in achados if a["sev"] == "MEDIO"); na = sum(1 for a in achados if a["sev"] == "ALTO")
aprovada = (na == 0 and nm == 0 and not mudou)
doc = {
    "aprovada": aprovada,
    "rodada": "conferência única do conserto (D109), depois da R3",
    "quando": now,
    "candidato_sha16": fim, "candidato_bytes": fim_b,
    "candidato_sha16_no_inicio": ini, "candidato_mudou_durante_a_revisao": mudou,
    "revisor": "Claude Sonnet (agente revisor de terceiro; conferência única de escopo fechado, D109; não construí a v410; a mesma instância de trabalho da R1, R2 e R3)",
    "n_alto": na, "n_medio": nm, "n_baixo": nb,
    "achados": achados,
    "situacao_dos_achados_da_R3": situ,
    "cobertura_do_painel": cobertura,
    "lean": lean,
    "conferencias": conferencias,
    "ressalvas": ressalvas,
    "ressalvas_para_a_versao_seguinte": proxima,
    "rotas_examinadas": rotas,
    "arquivos_revisados": arquivos,
    "artefatos_renderizados_lidos": artef,
    "criterio_D109": "aprovada = 0 ALTO e 0 MEDIO dentro do escopo A–F (calculado: %d ALTO, %d MEDIO); achado fora do escopo é ressalva para a versão seguinte, não bloqueia, salvo ALTO para o rito (nenhum: nenhum β literal novo, nenhum CONFIRMED indevido, nenhuma fala/hash/citação fabricada, nenhuma leitura de arquivo vedado no rito, nenhum teorema fora do trio ou com sorry, nada que mova o gate ou faça o rito/cadeia falhar)." % (na, nm),
    "nota": ("aprovada=%s: %d ALTO, %d MEDIO, %d BAIXO. O conserto da R3 e do painel ENTROU no texto rendido nas 38 linhas da tabela (152 verificações, 0 falhas); o kernel confere (103/103 no trio, o Nome sem axioma); o MEDIO da R3 (o quarto nome) está resolvido pela fala 29 do operador, que li no arquivo; os aditivos fora do candidato (S9, README, p00) não tocam o Nós antes do rito, não publicam e não escrevem o gatilho antes do fim com tudo verdadeiro. Os dois BAIXOS são rótulo/legibilidade e não bloqueiam. A tabela é do conserto; o julgamento de estatuto continua do operador. NOT_FALSIFIED nunca é CONFIRMED." % (aprovada, na, nm, nb)),
}
assert mudou is False, "o candidato mudou durante a revisao: %s -> %s" % (ini, fim)


def grava(path, txt):
    tmp = path + ".tmp"
    open(tmp, "w", encoding="utf-8", newline="\n").write(txt)
    assert os.path.getsize(tmp) > 1000
    os.replace(tmp, path)


js = json.dumps(doc, ensure_ascii=False, indent=1)
# o .md
L = ["# REVISÃO DE TERCEIRO — v410 — conferência única do conserto (D109), depois da R3", "",
     "Candidato revisado: `%s` (%d B); no início: `%s`; mudou durante a revisão: **%s**. Revisor: %s. Quando: %s." % (fim, fim_b, ini, "sim" if mudou else "não", doc["revisor"], now), "",
     "## Veredito", "", "**aprovada = %s** — %d ALTO, %d MEDIO, %d BAIXO (calculado)." % (str(aprovada).lower(), na, nm, nb), "", doc["nota"], "",
     "## Os cinco achados da R3", ""]
for k, v in situ.items(): L += ["- **%s**: %s" % (k, v), ""]
L += ["## Achados novos (todos BAIXO)", ""]
for a in achados: L += ["- **%s** (dentro do escopo: %s) — onde: %s. %s. **Correção pedida:** %s" % (a["sev"], "sim" if a["dentro_do_escopo"] else "não", a["onde"], a["achado"], a["correcao_pedida"]), ""]
L += ["## Kernel (Lean)", "", "- Tree: " + lean["tree"], "- Tempo: %d s; um processo." % lean["time_s"], "- " + lean["output"], ""]
L += ["## Conferências", ""]
for k, v in conferencias.items(): L += ["- **%s**: %s" % (k, v), ""]
L += ["## Cobertura da tabela do painel (38 linhas)", "", "| # | achado | verificações | estado |", "|---|---|---|---|"]
for c in cobertura: L.append("| %d | %s | %s | %s |" % (c["linha"], c["achado"], c["verificacoes_no_texto_rendido"], c["estado"]))
L += [""] + ["- **%s (%s)**: %s" % (c["achado"], c["titulo"][:60], c["nota"]) for c in cobertura if not c["nota"].startswith("Todas as verificações")] + [""]
L += ["## O que NÃO fiz (ressalvas)", ""] + ["- " + x for x in ressalvas] + [""]
L += ["## Para a versão seguinte", ""] + ["- " + x for x in proxima] + [""]
L += ["## Rotas examinadas", ""] + ["- " + x for x in rotas] + [""]
L += ["## Arquivos revisados (sha16 lidos agora)", ""] + ["- `%s` `%s`" % (k, v) for k, v in arquivos.items()] + [""]
L += ["## Artefatos renderizados lidos (sha16 de agora; fora da trava S1b)", ""] + ["- `%s` `%s`" % (k, v) for k, v in artef.items()] + [""]
grava(RV + "REVISAO_TERCEIRO_v410.json", js)
grava(RV + "REVISAO_TERCEIRO_v410.md", "\n".join(L))
grava(RV + "REVISAO_TERCEIRO_v410.CU.json", js)
grava(RV + "REVISAO_TERCEIRO_v410.CU.md", "\n".join(L))
print("gravado: REVISAO_TERCEIRO_v410.json sha16", s16(RV + "REVISAO_TERCEIRO_v410.json"), "bytes", os.path.getsize(RV + "REVISAO_TERCEIRO_v410.json"))
print("aprovada:", aprovada, "| ALTO/MEDIO/BAIXO:", na, nm, nb, "| candidato:", fim, fim_b, "| mudou:", mudou)
