import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\montar_conferencia.py')
s = p.read_text(encoding='utf-8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a))
    s = s.replace(a, b)


# saidas: alternativa, cartas
rep("    saidas = [ent(novo, 'FOLHAS SUBSTITUTIVAS (PDF vetorial, A4)')]",
    """    saidas = [ent(novo, 'FOLHAS SUBSTITUTIVAS (PDF vetorial, A4)')]
    nome_carta = 'CARTA_REGRA_26_4_' + k
    for ext, papel in (('.md', 'carta da Regra 26.4 (minuta)'), ('.pdf', 'carta da Regra 26.4 (PDF)')):
        saidas.append(ent(W / (nome_carta + ext), papel))
    if k == '050576':
        saidas.append(ent(W / 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'folha 1/6 ALTERNATIVA com «PHOT» inteiro (para o agente de PI escolher)'))
        for ext, papel in (('.md', 'carta da Regra 26.4, variante PHOT (minuta)'), ('.pdf', 'carta da Regra 26.4, variante PHOT (PDF)')):
            saidas.append(ent(W / (nome_carta + '_PHOT' + ext), papel))""")
# folhas: novos testes
rep("                       'palavras_cruzadas_por_traco': f['texto_cruzado_por_traco'], 'palavras_sobrepostas': f['texto_sobre_texto'],",
    """                       'palavras_cruzadas_por_traco': f['texto_cruzado_por_traco'], 'palavras_sobrepostas': f['texto_sobre_texto'],
                       'TESTE_DE_OCLUSAO (fundo branco/opaco sobre traco ou marca de dado)': {'ocorrencias': f['oclusao_fundo_branco_sobre_traco_ou_marca'], 'passa': len(f['oclusao_fundo_branco_sobre_traco_ou_marca']) == 0},
                       'TESTE_DA_MARCACAO_DO_RO (canto superior direito e margem inferior livres; AI 325)': f['marcacao_do_RO_areas_livres'],""")
# secoes novas antes de entradas/saidas
rep("        'sem_materia_nova': nm,\n        'entradas_sha256': entradas, 'saidas_sha256': saidas,",
    """        'sem_materia_nova': nm,
        'reparos_rodada_2': reparos(k, med),
        'numeracao_das_folhas': NUMERACAO,
        'entradas_sha256': entradas, 'saidas_sha256': saidas,""")
rep("def montar(k):",
    '''NUMERACAO = {
    'achado': ('PCT AI Section 207 nao tem esquema de sufixo para folhas acrescentadas; as folhas de desenhos sao numeradas n/N com o NOVO total. '
               'O kit (1/6 a 6/6 e 1/8 a 8/8) segue o texto. [DECLARADO pela coordenacao: texto lido de wipo.int, s207 e s325, em 27/10/2026; o preparador nao tem rede e nao releu a fonte]'),
    'AI_325': 'o RO marca cada folha de substituicao no canto superior direito (numero do pedido, data de recebimento) e com «SUBSTITUTE SHEET (RULE 26)» na margem inferior [DECLARADO pela coordenacao]: o kit deixa essas areas livres (teste de marcacao do RO)',
    'se_substituir_todo_o_conjunto': '[LEGAL] decisao do operador/agente de PI: o kit pede a substituicao INTEGRAL das folhas de desenhos (nao mantem folhas depositadas)'}


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
                        'estatuto': '[LEGAL] decisao do agente de PI'}
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
                                                   'Alternativa conservadora: A_C e E_Psi em romano, como na descricao: uma linha em fontes\\\\mqc_folhas.py (SPECIAL). O preparador nao decide.')}
        base['R4_conferencia'] = 'teste de oclusao por vetor (fundo branco/opaco sobre traco ou marca) e teste da marcacao do RO incluidos; ambos passam em todas as folhas'
    base['marcacao_do_RO'] = {'antes': [(r['folha'], r['antes']['RO_livre']) for r in rr['folhas'] if 'antes' in r], 'depois': [(r['folha'], r['depois']['RO_livre']) for r in rr['folhas'] if 'depois' in r]}
    return base


def montar(k):''')
p.write_text(s, encoding='utf-8')
print('ok')
