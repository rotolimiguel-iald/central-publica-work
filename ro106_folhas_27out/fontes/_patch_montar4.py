import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\montar_conferencia.py')
s = p.read_text(encoding='utf-8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:90], s.count(a))
    s = s.replace(a, b)


rep("                       'TESTE_DE_OCLUSAO (fundo branco/opaco sobre traco ou marca de dado)':",
    "                       'TESTE_DE_CONTATO texto x grafico (pixel a pixel, 600 dpi; rodada 3)': f['TESTE_DE_CONTATO_texto_x_grafico (pixel a pixel, 600 dpi)'],\n                       'TESTE_DE_OCLUSAO (fundo branco/opaco sobre traco ou marca de dado)':")
rep("        saidas.append(ent(W / 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf',",
    "        saidas.append(ent(W / 'FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf', 'VARIANTE PHOT completa: 6 folhas (folha 1/6 alternativa + 2/6 a 6/6 iguais as principais), para enviar sozinha'))\n        saidas.append(ent(W / 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf',")
rep("        'reparos_rodada_2': reparos(k, med),", "        'reparos_rodada_2': reparos(k, med),\n        'rodada_3': rodada3(k),")
rep("def reparos(k, med):", '''def rodada3(k):
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


def reparos(k, med):''')
p.write_text(s, encoding='utf-8')
print('ok')
