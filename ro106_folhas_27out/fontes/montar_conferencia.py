# Monta CONFERENCIA_<6>.json de cada PCT a partir das medidas (conferir.py), das provas de identidade e do cotejo de palavras,
# e calcula por script o sha256 de toda entrada e saida. Nada e digitado a mao alem dos textos de explicacao.
import json, hashlib, pathlib, re, datetime
import fitz
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
E = pathlib.Path(r'C:\IALD\Central de Patentes\EPCT')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def ent(p, papel):
    p = pathlib.Path(p)
    return {'arquivo': str(p), 'papel': papel, 'bytes': p.stat().st_size, 'sha256': sha(p), 'sha16': sha(p)[:16]}


def imghash_pages(pdf, pages=None):
    d = fitz.open(str(pdf))
    out = []
    for i, p in enumerate(d):
        if pages and (i + 1) not in pages:
            continue
        out.append({'pagina': i + 1, 'sha256_das_imagens': [hashlib.sha256(d.extract_image(x[0])['image']).hexdigest() for x in p.get_images(full=True)]})
    return out


def nonbw_asfiled(pdf):
    d = fitz.open(str(pdf))
    fitz.TOOLS.set_aa_level(0)
    import numpy as np
    tot = 0
    n_gray = 0
    per = []
    for p in d:
        pix = p.get_pixmap(dpi=300, colorspace=fitz.csGRAY, alpha=False)
        a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width]
        nw = int((a < 250).sum())
        g = int(((a > 20) & (a < 235)).sum())
        per.append({'pixels_de_tinta': nw, 'pixels_cinza_entre_20_e_235': g, 'fracao_cinza_na_tinta': round(g / max(nw, 1), 3)})
    fitz.TOOLS.set_aa_level(8)
    return per


CAIXAS = {
    'RO106_pagina_1': {'item_1_solicita_corrigir_pedido_tal_como_depositado': True, 'Anexo_A': False, 'Anexo_B1_texto': False,
                       'Anexo_C1_desenhos': True, 'item_2_traducao': False, 'Anexo_B2': False, 'Anexo_C2': False,
                       'copia_a_ISA': False, 'observacoes_adicionais': 'ver form IB/313',
                       'prazo': 'DOIS MESES a partir da data de expedição (expedição 09 de Outubro de 2026)'},
    'RO106_pagina_2_Anexo_C1': {'item_1_publicacao_internacional_razoavelmente_uniforme': True,
                                'Folhas_contendo_desenhos_a_a_p': 'nenhuma marcada',
                                'Desenhos_Regra_11_13': {'d_tinta_preta_duravel_tracos_uniformes_bem_definidos': True,
                                                         'k_numeros_e_letras_de_altura_inferior_a_0_32_cm': True,
                                                         'demais_a_u_exceto_d_e_k': 'nenhuma marcada'},
                                'item_2_reproducao_satisfatoria': False}}
IB313 = {
    '050579': {'form_pagina': {'item_1_defeitos_no_pedido_tal_como_depositado': True, 'Anexo_C1': True, 'Anexo_A': False, 'Anexo_B1': False, 'item_2': False},
               'Anexo_C1': {'item_1_reasonably_uniform_international_publication': True, 'Sheets_containing_drawings_a_p': 'nenhuma marcada',
                            'Drawings_Rule_11_13': {'a': False, 'd': True, 'f': True, 'h': True, 'k': True, 'demais': 'nenhuma marcada'}, 'item_2': False}},
    '050576': {'form_pagina': {'item_1_defeitos_no_pedido_tal_como_depositado': True, 'Anexo_C1': True, 'Anexo_A': False, 'Anexo_B1': False, 'item_2': False},
               'Anexo_C1': {'item_1_reasonably_uniform_international_publication': True, 'Sheets_containing_drawings_a_p': 'nenhuma marcada',
                            'Drawings_Rule_11_13': {'a': True, 'd': True, 'f': True, 'h': True, 'k': True, 'demais': 'nenhuma marcada'}, 'item_2': False}}}
SIGLAS = {'a': 'não admitem reprodução direta', 'd': 'tinta preta durável; traços de espessura uniforme e bem definidos', 'f': 'distinguíveis na reprodução reduzida',
          'h': 'números, letras e linhas de referência com clareza e simplicidade', 'k': 'números e letras com altura mínima de 0,32 cm'}

CFG = {
    '050576': {
        'nome': 'Aprendizado Contínuo', 'pct': 'PCT/BR2026/050576', 'br': 'BR 10 2026 005477-1', 'ref': 'BR102026005477',
        'dir': E / 'BR102026005477-1_APRENDIZADO_CONTINUO',
        'ro106': 'RECIBOS/PCTBR2026050576-ro106-1-pt-20261009.pdf',
        'ib313': 'RECIBOS/SIGNED-PCTBR2026050576-ib313-000015-en-20261007_CUSTODIA_20261019_e21913077659.pdf',
        'appb': 'RECIBOS/DOCUMENTOS_OFICIAIS_WIPO_20261004/PCTBR2026050576-appb-000003-pt-20261004.pdf',
        'filed_local': W / 'entrada/aprendizado/04_DESENHOS_como_depositado.pdf', 'filed_pages_in_appb': [19, 20, 21, 22, 23],
        'novo': W / 'FOLHAS_SUBSTITUTIVAS_050576.pdf', 'medidas': 'medidas_050576.json', 'palavras': 'palavras_apr.json',
        'ident': 'apr_identidade_fonte.json',
        'plano_novo': {'1': [1], '2': [2, 3], '3': [4, 5], '4': [6, 7], '5': [8], '6': [9]},
        'plano_depositado': {'1': [1, 2], '2': [3, 4], '3': [5, 6], '4': [7, 8], '5': [9]},
        'paisagem': [1, 6],
        'fontes': [(W / 'entrada/aprendizado/Psion_Engine_PI_INPI.tex', 'fonte TikZ/LaTeX das 9 figuras (acom\\Psion_Engine_PI_INPI.tex, 09/03/2026)'),
                   (W / 'fontes/aprendizado_folhas.tex', 'fonte das folhas substitutivas (xelatex, Arial Narrow 15 pt)')],
        'figuras': {
            1: 'folha em paisagem (topo à esquerda, R.11.13(j)); corpo 15 pt; fundos coloridos dos domínios PALAVRA/NOME/VERBO trocados por contorno pontilhado; setas tracejadas reencaminhadas para não cruzar rótulos; o rótulo da caixa [1] aparece inteiro («VACUUM/GRAV/PHOT»; no depositado a caixa [3] encobria o final)',
            2: 'corpo 15 pt; círculos e equação central redimensionados; «Comprimir» e «Filtrar» afastados das setas; fundos coloridos retirados',
            3: 'gráfico em preto; mesma função, mesma curva e mesmas fronteiras; grade pontilhada preta; rótulos de região («VACUUM 6 bits», «GRAVITON 10 bits», «PHOTON 16b») reposicionados sem corte e sem cruzar linhas (no depositado: «UUM6 bits» e «PHOTON 16b» cortados); legenda reposicionada',
            4: 'corpo 15 pt; quatro estados e eixos mantidos; w>0, w<0, ∂w>0, ∂w<0 fora das caixas (no depositado cruzavam as caixas); fundos coloridos retirados',
            5: 'caixas ampliadas para conter o texto; setas e «Próxima geração» sem cruzar texto; cores retiradas',
            6: 'colunas com hachuras distintas (GRACE oblíqua, FRONTIER oblíqua inversa, VACUUM horizontal) no lugar de tons de cinza; limiares tracejados; legendas com a hachura correspondente',
            7: 'séries distintas por marcador e tipo de traço (círculo, quadrado, triângulo; tracejado, pontilhado) no lugar de cor; legenda à direita; grade pontilhada preta',
            8: 'colunas com hachura no lugar do cinza; «Vácuo angular» mantido, dentro do quadro sobre os buckets 13-14 vazios',
            9: 'folha em paisagem; caixas e setas pretas; nenhuma sobreposição; «ª» e siglas em maiúsculas de corpo pleno (no depositado: versaletes)'}},
    '050579': {
        'nome': 'MQC', 'pct': 'PCT/BR2026/050579', 'br': 'BR 10 2026 003460-6', 'ref': 'BR102026003460',
        'dir': E / 'BR102026003460-6_MQC',
        'ro106': 'RECIBOS/PCTBR2026050579-ro106-1-pt-20261009.pdf',
        'ib313': 'RECIBOS/SIGNED-PCTBR2026050579-ib313-000015-en-20261007_CUSTODIA_20261019_8ac2767b4e4f.pdf',
        'appb': 'RECIBOS/DOCUMENTOS_OFICIAIS_WIPO_20261004/PCTBR2026050579-appb-000003-pt-20261004.pdf',
        'filed_local': W / 'entrada/mqc/04_DESENHOS_CINZA_como_depositado.pdf', 'filed_pages_in_appb': [20, 21, 22],
        'novo': W / 'FOLHAS_SUBSTITUTIVAS_050579.pdf', 'medidas': 'medidas_050579.json', 'palavras': 'palavras_mqc.json',
        'ident': 'mqc_identidade_fonte.json',
        'plano_novo': {str(i): [i] for i in range(1, 9)},
        'plano_depositado': {'1': [1, 2, 3], '2': [4, 5, 6], '3': [7, 8]},
        'paisagem': [1, 4, 8],
        'fontes': [(W / 'entrada/mqc/mqc_simulacao_celula_elementar.py', 'script de origem das 8 figuras (patents\\...MQC\\prototype_src; idêntico por sha256 ao acom\\mqc_simulacao_celula_elementar.py de 11/02/2026)'),
                   (W / 'fontes/mqc_folhas.py', 'gerador das folhas substitutivas (matplotlib; usa as funções de simulação do script de origem sem alteração)')],
        'figuras': {
            1: 'folha em paisagem; painéis lado a lado como no depositado; categorias distintas por forma de marcador (círculo cheio, quadrado vazado, losango vazado, estrela cheia) no lugar de cor; planos cinza do 3D e círculos sombreados retirados (círculos brancos com contorno); legenda e título reposicionados; o rótulo do eixo Z não aparece no depositado (cortado) e não foi acrescentado',
            2: 'dois painéis empilhados em coluna única; séries distintas por tipo de traço (contínuo, tracejado, ponto-traço, pontilhado) no lugar de cor; área translúcida substituída por hachura; legendas e caixa de texto fora das linhas de dados',
            3: 'três painéis empilhados; mesmas séries com tipos de traço distintos; áreas translúcidas viram hachura; grade pontilhada preta',
            4: 'folha em paisagem, painéis 2x2; barras com quatro hachuras distintas; séries (a)/(b) por tipo de traço; caixa de métricas e legenda dentro do painel (d), sem cobrir texto (a caixa tem quebra de linha após «Correlação:»)',
            5: 'três painéis empilhados; conforme a variante do PCT (convencional tracejada com círculos vazados; IALD contínua com quadrados cheios); 𝒜_C como no PCT',
            6: 'três painéis empilhados; séries por tipo de traço; rótulos dos eixos com sub e sobrescritos em corpo pleno',
            7: 'dois painéis empilhados; conforme a variante do PCT (LOCAL círculo cheio, REGIONAL quadrado vazado, GLOBAL triângulo cheio; sem caixa de anotação na 7a)',
            8: 'folha em paisagem; tabela com o mesmo texto das 40 células; fundos coloridos e cabeçalho azul trocados por fundo branco com cabeçalho em negrito; grifos 𝓐 e 𝓔 desenhados (o depositado os exibia como glifo ausente)'}},
}


NUMERACAO = {
    'achado': ('PCT AI Section 207 nao tem esquema de sufixo para folhas acrescentadas; as folhas de desenhos sao numeradas n/N com o NOVO total. '
               'O kit (1/6 a 6/6 e 1/8 a 8/8) segue o texto. [DECLARADO pela coordenacao: texto lido de wipo.int, s207 e s325, em 27/10/2026; o preparador nao tem rede e nao releu a fonte]'),
    'AI_325': 'o RO marca cada folha de substituicao no canto superior direito (numero do pedido, data de recebimento) e com «SUBSTITUTE SHEET (RULE 26)» na margem inferior [DECLARADO pela coordenacao]: o kit deixa essas areas livres (teste de marcacao do RO)',
    'se_substituir_todo_o_conjunto': '[LEGAL] decisao do operador/agente de PI: o kit pede a substituicao INTEGRAL das folhas de desenhos (nao mantem folhas depositadas)'}


def alt_resumo():
    pj = W / 'conferencia' / 'medidas_ALT_PHOT.json'
    if not pj.exists():
        return 'medidas_ALT_PHOT.json ausente'
    m = json.load(open(pj, encoding='utf-8'))
    f = m['folhas'][0]
    return {'pdf': 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'sha256': m['sha256'], 'resumo': m['resumo'], 'margens_cm': {kk: float(v) for kk, v in f['margens_medidas_cm'].items()},
            'altura_minima_caractere_cm': f['altura_por_linha_texto_vivo']['h_min_cap_alg_asc_cm'], 'oclusoes': len(f['oclusao_fundo_branco_sobre_traco_ou_marca']),
            'marcacao_RO_livre': f['marcacao_do_RO_areas_livres']['livres'], 'palavras_cruzadas': len(f['texto_cruzado_por_traco']),
            'paisagem': f['folha_em_paisagem_topo_a_esquerda']}


def rodada3(k):
    if k != '050576':
        return 'MQC 050579 ACEITA na segunda rodada e CONGELADA: nada foi alterado nesta rodada (hashes conferidos antes/depois)'
    ct = json.load(open(W / 'conferencia' / 'contato_texto_grafico_r3.json', encoding='utf-8'))
    var = json.load(open(W / 'conferencia' / 'medidas_VARIANTE_PHOT.json', encoding='utf-8'))
    a = ct['rodada2_050576 (a266d4a46594b3b2, antes do reparo R2-1)']
    return {
        'R2-1 (unico bloqueio da 2a revisao)': {
            'defeito': 'Fig. 3 (folha 2/6): a linha horizontal da grade em theta = 20 tocava o pe do «V» de «VACUUM 6 bits» (28 px a 600 dpi segundo a revisao)',
            'reparo': 'lacuna da grade ampliada: linha horizontal theta = 20 interrompida entre x = 0,036 e 0,104 e a vertical x = 0,1 interrompida entre theta = 15 e 75 (o rotulo ocupa theta 18,7-71,6 e x 0,044-0,087 em unidades do eixo)',
            'teste_novo': 'TESTE DE CONTATO texto x grafico (pixel a pixel, 600 dpi, texto e grafico renderizados em separado; exclui a regua do radical): pega o caso',
            'antes (PDF da rodada 2)': {'total_de_contatos': a['total_de_contatos'], 'pixels': a['pixels_em_contato'], 'onde': [(f['folha'], c['caixa_cm'], c['px'], c['palavra']) for f in a['folhas'] for c in f['contatos']]},
            'depois': {'principal': ct['rodada3_050576_principal']['total_de_contatos'], 'variante_PHOT_completa': ct['rodada3_050576_variante_PHOT']['total_de_contatos'],
                       'folha_alternativa': ct['rodada3_folha_alternativa_PHOT']['total_de_contatos'], 'MQC_congelado (so leitura)': ct['MQC_050579_congelado (so leitura)']['total_de_contatos']},
            'nota': 'o teste vetorial de «palavras cruzadas por traco» NAO via o caso: reduzia a caixa da palavra em 4% ao longo do texto e o pe do «V» esta na ponta de «VACUUM»; agora a reducao ao longo do texto e 0% e ele marca a folha 2 da rodada 2 («VACUUM») e passa nas folhas reparadas; o teste de contato por pixels tambem pega e passa'},
        'sugestao_1': {'arquivo': 'FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf', 'sha256': var['sha256'], 'folhas': var['paginas'],
                       'conferido': 'folhas 2/6 a 6/6 iguais as principais (texto e pixels a 100 dpi); so a 1/6 difere (PHOT); passa em todos os testes (resumo abaixo)', 'resumo': var['resumo']},
        'sugestao_2': 'item 3(c) das duas cartas do Aprendizado: «algarismos, maiúsculas e letras com haste com altura mínima de 0,32 cm (inclusive nos sinais de referência)»; a carta do MQC (congelado) nao foi tocada',
        'sugestao_3 (da revisao)': 'linha da Fig. 3 das cartas: «VACUUM 6 bits» passou da horizontal para a vertical (mesmo texto)',
        'cartas': 'a carta da variante PHOT agora cita FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf como anexo'}


def reparos(k, med):
    rr = json.load(open(W / 'conferencia' / 'reparos_rodada2.json', encoding='utf-8'))[k]
    base = {'antes_vs_depois_por_folha': rr['folhas']}
    if k == '050576':
        base['R1_setas_Fig1'] = {
            'decisao': 'a descricao e SILENCIOSA sobre o sentido de fluxo entre [1]-[3] e SO sugestiva (nao clara) entre [4]-[5]; regra da coordenacao: reproduzir o sentido VISIVEL na folha depositada: [3] para [1] e [5] para [4]',
            'evidencia_no_depositado': 'recorte da Fig. 1 depositada: as unicas pontas de seta visiveis entre essas caixas apontam para a esquerda (para [1] e para [4]), porque as caixas sobrepostas invertem o comprimento da seta; a fonte TikZ manda quant->cache e hash->chain',
            'evidencia_descricao (paragrafos do appb, 18 paginas de texto lidas)': {
                '[002]': '«sistema integrado de sete componentes ... opera como pipeline unificado de compressao (Palavra), filtragem (Nome) e poda de relacoes (Verbo)» -- enumera (1)-(7); nao diz que a saida de (1) alimenta (3)',
                '[031]-[033]': 'quantizador opera sobre os pesos do modelo (Palavra); nada sobre o cache como destino do quantizador',
                '[041]': 'o cache KV opera sobre as ativacoes de atencao (memoria da Palavra processada); nada sobre receber a saida do quantizador',
                '[045]': 'o hash opera sobre dados arbitrarios (pesos, tensores, certificados): «certificados» e a producao da cadeia [5], logo [5]->[4] tambem e possivel',
                '[046]': 'a cadeia de certificacao registra uma sequencia encadeada de hashes (peso original, peso quantizado, logits, token): sugere [4]->[5], mas nao e afirmacao de fluxo e coexiste com [045]',
                'Fig. 1 (breve descricao, p.5)': '«sete componentes organizados pela ontologia trinaria ... Psion como motor ... retroalimentacao do insight»: sem sentido de fluxo para os pares'},
            'conclusao': 'silencio/ambiguidade -> reproduzido o sentido visivel no depositado; a fonte (sentido [1]->[3], [4]->[5]) fica comentada no .tex (uma linha cada) caso o agente de PI prefira; mudanca listada na linha da Fig. 1 da carta [LEGAL]',
            'medido_no_vetor (cabecas de seta ligadas as hastes)': rr['setas_fig1']}
        base['PHOT'] = {'principal': 'caixa [1] = «VACUUM/GRAV/PHO» (caracteres visiveis no depositado; a caixa [3] cobre o T)',
                        'alternativa': 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf = so a folha 1/6, com «PHOT» inteiro; as demais folhas sao as mesmas (conferido: texto e pixels das folhas 2-6 identicos)',
                        'cartas': 'CARTA_REGRA_26_4_050576 (folha principal) e CARTA_REGRA_26_4_050576_PHOT (folha alternativa), cada uma com a frase da caixa [1] coerente com a sua folha',
                        'palavras': 'PHOT nao esta escrito na descricao (so PHOTON, [033]); VACUUM esta ([033] e legenda da Fig. 3) e foi restaurado na Fig. 3 (as 3 primeiras letras estavam cortadas)',
                        'estatuto': '[LEGAL] decisao do agente de PI',
                        'medidas_da_folha_alternativa': alt_resumo()}
        base['R2_Fig5_Proxima_geracao'] = {'antes': 'fundo branco do rotulo interrompia ~6 mm da borda inferior da caixa CARGA (29 pontos de traco cobertos) e tocava a ponta da seta',
                                           'depois': 'rotulo em duas linhas SEM fundo, abaixo do trecho horizontal da seta; borda da caixa continua; oclusoes da folha 3: 0',
                                           'folga_texto_traco_cm': {'Proxima': [rr['folga_texto_traco_cm']['antes']['Próxima'], rr['folga_texto_traco_cm']['depois']['Próxima']], 'geracao': [rr['folga_texto_traco_cm']['antes']['geração'], rr['folga_texto_traco_cm']['depois']['geração']], 'formato': '[antes, depois]; caixa da fonte, maior que a tinta'}}
        base['R3_Fig8_Vacuo_angular'] = {'antes': 'fundo branco apagava ~1 cm da moldura direita, uma marca de eixo e a grade (193 pontos de traco cobertos)',
                                         'depois': 'rotulo FORA do quadro, sem fundo, com seta oblíqua para os buckets 13 e 14 vazios, como no depositado; oclusoes da folha 5: 0',
                                         'folga_texto_traco_cm': {'Vacuo': [rr['folga_texto_traco_cm']['antes']['Vácuo'], rr['folga_texto_traco_cm']['depois']['Vácuo']], 'angular': [rr['folga_texto_traco_cm']['antes']['angular'], rr['folga_texto_traco_cm']['depois']['angular']], 'formato': '[antes, depois]'}}
        base['R3b_Fig3_grade_e_legenda'] = {'antes': '3 fundos brancos (VACUUM 6 bits, GRAVITON 10 bits, legenda) cobriam 162+36+96 pontos de grade/linha tracejada',
                                            'depois': 'grade desenhada a mao com lacunas ao redor dos rotulos; legenda acima do quadro; oclusoes da folha 2: 0; palavras cruzadas por traco: 0'}
        base['Fig6_limiares'] = {'antes': '7 colunas com fundo branco cobriam o traco tracejado dos limiares (216 pontos)', 'depois': 'limiares desenhados so entre as colunas; oclusoes da folha 4: 0'}
        base['Fig2_rotulos'] = {'antes': '«Comprimir» e «Filtrar» com fundo branco sobre a seta (36 pontos)', 'depois': 'sem fundo, afastados da seta; oclusoes: 0'}
        base['R4_cartas'] = 'carta corrigida: 3(d) agora descreve o que foi feito (sem fundo sobre traco; grade interrompida; setas no sentido visivel); linhas das Figs. 1, 3, 5, 6 e 8 reescritas; decisao das setas e do PHOT declaradas'
    else:
        lg = json.load(open(W / 'conferencia' / 'mqc_legendas_do_depositado.json', encoding='utf-8'))
        base['R1_legendas'] = {'antes': 'legendas de fundo branco cobriam dado: 3(a) 12 de 82 pontos (revisao); 4(a) pico em 2,2-3,0; 4(b) topo das curvas em 2,0-4,7; 4(d) caixa de texto e legenda encostadas; + legendas sobre a grade em todas as folhas',
                               'depois': 'legendas dentro do quadro so em regiao SEM dado (varredura de 121x121 posicoes contra linhas, pontos, colunas e hachuras, com folga de 6 px) ou ACIMA do quadro (3(a), 3(c), 4(a), 4(b), 4(d)); grade interrompida onde ha legenda/caixa; oclusoes: 0 em todas as 8 folhas',
                               'dados_escondidos_no_depositado_e_agora_visiveis': 'SO UM: Fig. 4(d), a caixa de metricas do depositado cobria o trecho da curva alfa^2 de 0,00167 a 0,00225, eta de 0,99675 a 0,99760 (2 vertices); nas demais legendas/caixas do depositado, 0 pontos de dado cobertos (mqc_legendas_do_depositado.json). Figs. 5 e 7 (variante do PCT): legendas em cantos vazios na imagem depositada. Listado na carta.',
                               'medida_do_depositado': lg}
        base['R2_carta_Fig8'] = 'a linha da Fig. 8 da carta cita a troca da caixa de glifo ausente por A_C e E_Psi (Tabela 1 e [0056]/eq. (22) da descricao); 3(d) corrigido'
        base['R3_forma_do_glifo_Fig8'] = {'estatuto': '[LEGAL] decisao do agente de PI',
                                          'nota': ('Desenhados: A em script regular (U+1D49C, igual ao A_C da Fig. 5 DEPOSITADA, que ja mostra A em script) e E em script regular (U+2130). '
                                                   'A descricao ([0056], eq. (22), e Tabela 1) escreve A_C e E_Psi em letra ROMANA; nenhum desenho depositado traz E em script. '
                                                   'Alternativa conservadora: A_C e E_Psi em romano, como na descricao: uma linha em fontes\\mqc_folhas.py (SPECIAL). O preparador nao decide.')}
        base['R4_conferencia'] = 'teste de oclusao por vetor (fundo branco/opaco sobre traco ou marca) e teste da marcacao do RO incluidos; ambos passam em todas as folhas'
    base['marcacao_do_RO'] = {'antes': [(r['folha'], r['antes']['RO_livre']) for r in rr['folhas'] if 'antes' in r], 'depois': [(r['folha'], r['depois']['RO_livre']) for r in rr['folhas'] if 'depois' in r]}
    return base


def montar(k):
    c = CFG[k]
    d = c['dir']
    med = json.load(open(W / 'conferencia' / c['medidas'], encoding='utf-8'))
    pal = json.load(open(W / 'conferencia' / c['palavras'], encoding='utf-8'))
    ident = json.load(open(W / 'conferencia' / c['ident'], encoding='utf-8'))
    appb = d / c['appb']
    filed = c['filed_local']
    ph_appb = imghash_pages(appb, c['filed_pages_in_appb'])
    ph_loc = imghash_pages(filed)
    igual = [a['sha256_das_imagens'] == b['sha256_das_imagens'] for a, b in zip(ph_appb, ph_loc)]
    novo = c['novo']
    entradas = [ent(d / c['ro106'], 'RO/106 (Anexo C1) de 09/10/2026'), ent(d / c['ib313'], 'IB/313 [15] de 07/10/2026 (via assinada, custódia 19/10)'),
                ent(appb, 'pedido internacional como depositado, servido pelo ePCT (RO/BR, documentos 04/10/2026)'),
                ent(filed, 'PDF de desenhos como depositado (conteúdo idêntico por hash de imagem às páginas %s do appb)' % c['filed_pages_in_appb'])]
    for p, papel in c['fontes']:
        entradas.append(ent(p, papel))
    if k == '050579':
        for f in sorted((W / 'entrada/mqc/png_originais_11fev').glob('*.png')):
            entradas.append(ent(f, 'PNG original de 11/02/2026 (BR)'))
    saidas = [ent(novo, 'FOLHAS SUBSTITUTIVAS (PDF vetorial, A4)')]
    nome_carta = 'CARTA_REGRA_26_4_' + k
    for ext, papel in (('.md', 'carta da Regra 26.4 (minuta)'), ('.pdf', 'carta da Regra 26.4 (PDF)')):
        saidas.append(ent(W / (nome_carta + ext), papel))
    if k == '050576':
        saidas.append(ent(W / 'FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf', 'VARIANTE PHOT completa: 6 folhas (folha 1/6 alternativa + 2/6 a 6/6 iguais as principais), para enviar sozinha'))
        saidas.append(ent(W / 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'folha 1/6 ALTERNATIVA com «PHOT» inteiro (para o agente de PI escolher)'))
        for ext, papel in (('.md', 'carta da Regra 26.4, variante PHOT (minuta)'), ('.pdf', 'carta da Regra 26.4, variante PHOT (PDF)')):
            saidas.append(ent(W / (nome_carta + '_PHOT' + ext), papel))
    # resumo das medidas por folha (compacto)
    folhas = []
    for f in med['folhas']:
        al = f['altura_por_linha_texto_vivo']
        folhas.append({'folha': f['folha'], 'tamanho_cm': f['tamanho_cm'], 'paisagem_topo_a_esquerda': f['folha_em_paisagem_topo_a_esquerda'],
                       'margens_medidas_cm': {kk: float(v) for kk, v in f['margens_medidas_cm'].items()}, 'margens_ok': f['margens_ok'],
                       'tinta_bbox_cm': [float(x) for x in f['tinta_bbox_cm']],
                       'numero_da_folha': f['numero_da_folha'], 'legendas_figura': f['legendas_figura'],
                       'imagens_raster': f['imagens_raster'],
                       'pixels_nem_preto_nem_branco_600dpi_sem_AA': f['pixels_nem_preto_nem_branco_600dpi_sem_AA'],
                       'pixels_coloridos': f['pixels_coloridos_R_G_B_diferentes'],
                       'cores_vetoriais': f['cores_vetoriais'], 'cores_texto': f['cores_texto_rgb_int'],
                       'altura_minima_caractere_cm_texto_vivo': al['h_min_cap_alg_asc_cm'],
                       'linhas_cap_alg_asc_medidas': al['n_linhas_cap_alg_asc'], 'linhas_abaixo_0_32': len(al['linhas_abaixo_032_cap_alg_asc']),
                       'so_altura_x_abaixo_0_32 (letras sem haste; fora do critério)': al['so_altura_x_abaixo_032'],
                       'larguras_de_traco_vetorial_pt': f['larguras_de_traco_pt'],
                       'largura_de_traco_p10_mm_raster': (f['tracos_area_util'] or {}).get('largura_mm_p10'),
                       'uniformidade_do_traco_cv': (f['tracos_area_util'] or {}).get('cv_largura'),
                       'reducao_a_2_3': f['reducao_2_3'], 'moldura_detectada': f['moldura_detectada'],
                       'palavras_cruzadas_por_traco': f['texto_cruzado_por_traco'], 'palavras_sobrepostas': f['texto_sobre_texto'],
                       'TESTE_DE_CONTATO texto x grafico (pixel a pixel, 600 dpi; rodada 3)': f['TESTE_DE_CONTATO_texto_x_grafico (pixel a pixel, 600 dpi)'],
                       'TESTE_DE_OCLUSAO (fundo branco/opaco sobre traco ou marca de dado)': {'ocorrencias': f['oclusao_fundo_branco_sobre_traco_ou_marca'], 'passa': len(f['oclusao_fundo_branco_sobre_traco_ou_marca']) == 0},
                       'TESTE_DA_MARCACAO_DO_RO (canto superior direito e margem inferior livres; AI 325)': f['marcacao_do_RO_areas_livres'],
                       'texto_inclinado_a_verificar_visualmente': f['texto_inclinado_verificar_visualmente'],
                       'metodo_A5_informativo (agrupa fragmentos de curva como glifo; não é o critério)': {kk: (f['texto_area_util'] or {}).get(kk) for kk in ('n_linhas', 'h_cap_min_cm', 'h_cap_p05_cm', 'n_linhas_abaixo_032')}})
    ref = med['como_depositado_mesma_metrica']
    asf_gray = nonbw_asfiled(filed)
    before = []
    for r, g in zip(ref['folhas'], asf_gray):
        t = r['texto'] or {}
        before.append({'folha_depositada': r['folha'], 'h_cap_min_cm': t.get('h_cap_min_cm'), 'h_cap_mediana_cm': t.get('h_cap_mediana_cm'), 'h_cap_max_cm': t.get('h_cap_max_cm'),
                       'linhas': t.get('n_linhas'), 'linhas_abaixo_0_32': t.get('n_linhas_abaixo_032'), 'linhas_texto_cinza_claro': t.get('n_linhas_texto_cinza_claro'),
                       'largura_de_traco_p10_mm': (r['tracos'] or {}).get('largura_mm_p10'), 'preenchimento_cinza_cm2': (r['tons'] or {}).get('preenchimento_cinza_cm2'),
                       **g})
    def sinais(textos):
        s = {'colchetes': sorted(set(re.findall(r'\[\d+\]', ' '.join(textos)))), 'paineis': sorted(set(re.findall(r'\([a-d]\)', ' '.join(textos)))),
             'legendas_figura': sorted(set(re.findall(r'Figura\s*\d+', ' '.join(textos))))}
        return s
    src_lines = [l for x in pal for l in x.get('linhas_texto_fonte_como_depositado', x.get('linhas_texto_origem', []))]
    new_lines = [l for x in pal for l in x['linhas_texto_folha_nova']]
    nm = {
        'criterio': 'mesmas figuras, mesmos elementos, mesmos sinais de referência, mesmas palavras e mesmos dados do pedido internacional como depositado; só a apresentação muda',
        'figuras_como_depositado': c['plano_depositado'], 'figuras_nas_folhas_novas': c['plano_novo'],
        'n_figuras': len(c['figuras']),
        'palavras_por_folha (letras; sem números)': [{kk: x[kk] for kk in x if kk not in ('linhas_texto_fonte_como_depositado', 'linhas_texto_origem', 'linhas_texto_folha_nova')} for x in pal],
        'sinais_de_referencia_e_painéis_origem': sinais(src_lines), 'sinais_de_referencia_e_painéis_folhas_novas': sinais(new_lines),
        'linhas_de_texto_origem': {str(x['folha']): x.get('linhas_texto_fonte_como_depositado', x.get('linhas_texto_origem')) for x in pal},
        'linhas_de_texto_folhas_novas': {str(x['folha']): x['linhas_texto_folha_nova'] for x in pal},
        'alteracoes_por_figura (apresentação)': c['figuras']}
    if k == '050579':
        nm['dados_identicos'] = json.load(open(W / 'conferencia' / 'mqc_dados_identicos.json', encoding='utf-8'))
        nm['nota_artefatos_do_cotejo'] = ('«mathdefault» é texto interno do formatador de eixos do matplotlib (não é palavra do desenho); «ac» e «a»/«c» e «holográficâ» são '
                                          'artefatos de extração de texto (𝒜_C em matemática; acento combinante de T̂ vizinho) - ver linhas de texto acima.')
        nm['nota_figs_5_e_7'] = ('No PCT como depositado as Figs. 5 e 7 são a regeneração da Central de agosto (00_DOSSIE.json, epct_corrections_2026_08_03: marcadores; sem a caixa de '
                                 'anotação da 7a; 𝒜_C em mathtext), com as MESMAS funções de simulação e sementes; as folhas novas seguem essa variante. As demais (1-4, 6, 8) são o código de '
                                 'plotagem do script, sem o suptítulo que o PCT cortou.')
    else:
        nm['dados_identicos'] = 'as figuras são a compilação do .tex de origem; a compilação sem alteração reproduz o PCT depositado (correlação de forma 0,998 a 1,000 em 8 das 9 figuras; Fig. 4 = mesmo desenho, corte do PNG 25 px menor no PCT) - apr_identidade_fonte.json'
        nm['nota_fig_3'] = ('A curva «θ = arcsin(g/g_max)» foi mantida COMO NO DEPOSITADO: a fonte usa deg(asin(x)) e o pgfplots já devolve graus em asin, de modo que o traço sobe quase '
                            'na vertical e sai do quadro (ymax=95) - é o que o PCT mostra. Corrigir a expressão seria mudar o desenho (decisão [LEGAL], Regra 91).')
    doc = {
        'estatuto': '[REAL] o que foi medido/lido aqui, por script; [LEGAL] a suficiência frente ao RO/106 e ao IB/313 é do operador / agente de PI; nada foi enviado',
        'preparado_em': datetime.datetime.now().astimezone().isoformat(timespec='seconds'), 'preparador': 'sonnet-ro106-preparador',
        'pct': c['pct'], 'pedido_br': c['br'], 'ref_do_processo_no_RO106': c['ref'], 'nome': c['nome'],
        'prazo': {'expedicao_RO106': '2026-10-09', 'prazo': 'DOIS MESES a partir da expedição -> 2026-12-09 [DERIVED, Regras 26.2 e 80.2]', 'consequencia': 'considerado retirado (Regra 26.5)', 'meta_interna_Central': '2026-11-19'},
        'caixas_marcadas_lidas_nas_imagens': {
            'metodo': 'PDFs renderizados em PNG (130 dpi) e olhados; as caixas lidas pela marca (✓ no RO/106, ☒ no IB/313). Conferência numérica: a diferença de pixels entre as páginas do MQC e do Aprendizado cai só nas áreas do número do PCT/referência (RO/106 p.1 linhas 417-481 px, p.2 linhas 113-125 px; IB/313 p.2 e p.3 em 50-60, 470-480, 1450-1460 e 70-80, 720-730, 1440-1460 px) e, no IB/313 p.3, na caixa «a» de Desenhos (só o Aprendizado).',
            'RO106': CAIXAS, 'IB313_15': IB313[k], 'legenda_das_letras': SIGLAS,
            'leitura_da_Central_em_12_10': 'RO/106 d, k; IB/313: MQC d, f, h, k; Aprendizado a, d, f, h, k -> CONFIRMADA (o «a» do Aprendizado está em Desenhos (Regra 11.13), não em Folhas)'},
        'como_depositado': {'pdf_de_desenhos': c['filed_local'].name, 'sha256': sha(filed), 'folhas': len(ph_loc), 'figuras': len(c['figuras']),
                            'appb_do_ePCT': str(appb), 'appb_sha256': sha(appb), 'paginas_de_desenho_no_appb': c['filed_pages_in_appb'],
                            'hash_de_imagens_por_folha_local': ph_loc, 'hash_de_imagens_por_folha_no_appb': ph_appb, 'identicas_folha_a_folha': igual,
                            'medida_antes (método A5, 300 dpi)': before},
        'folhas_substitutivas': {'pdf': str(novo), 'sha256': sha(novo), 'folhas': med['paginas'], 'plano': c['plano_novo'], 'folhas_em_paisagem': c['paisagem'],
                                 'folhas_como_depositado': len(ph_loc), 'folhas_a_substituir': 'TODAS as %d folhas de desenhos (1/%d a %d/%d)' % (len(ph_loc), len(ph_loc), len(ph_loc), len(ph_loc)),
                                 'paginas_do_pedido_apos_a_troca': 'appb tem %d páginas; com a troca fica %d' % (fitz.open(str(appb)).page_count, fitz.open(str(appb)).page_count - len(ph_loc) + med['paginas']),
                                 'por_que_mais_folhas': 'letras >= 0,32 cm (corpo 14-15 pt) não cabem nas mesmas folhas: os painéis das figuras multipainel e os blocos de texto não reduzem sem violar a altura mínima; folha em paisagem onde a largura exige (Regra 11.13(j))'},
        'fonte_usada': {'tipo': 'script/fonte vetorial original (não houve limiarização de raster)', 'arquivos': [e for e in entradas[4:]],
                        'prova_de_identidade_com_o_depositado': ident},
        'medidas_das_folhas_novas': {'resumo': {(kk if kk != 'altura_minima_de_linha_cm_metodo_A5' else 'altura_minima_de_linha_cm_metodo_A5_INFORMATIVO_ruido_de_curvas_de_dados_nao_e_o_criterio'): v for kk, v in med['resumo'].items()}, 'criterios': med['criterios'], 'ferramentas': med['ferramentas'], 'folhas': folhas,
                                     'fontes_embutidas': [list(x[:5]) for p in fitz.open(str(novo)) for x in p.get_fonts()][:40]},
        'sem_materia_nova': nm,
        'reparos_rodada_2': reparos(k, med),
        'rodada_3': rodada3(k),
        'numeracao_das_folhas': NUMERACAO,
        'entradas_sha256': entradas, 'saidas_sha256': saidas,
    }
    return doc


if __name__ == '__main__':
    import sys
    for k in [x for x in ('050576', '050579') if x in sys.argv[1:]]:
        doc = montar(k)
        p = W / f'CONFERENCIA_{k}.json'
        tmp = p.with_suffix('.json.tmp')
        tmp.write_text(json.dumps(doc, indent=1, ensure_ascii=False, default=str), encoding='utf-8')
        tmp.replace(p)
        print(k, p.stat().st_size, doc['medidas_das_folhas_novas']['resumo'])
