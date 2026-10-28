import json, hashlib, pathlib
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')


def sh(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


for lab, f in (('050576', 'FOLHAS_SUBSTITUTIVAS_050576.pdf'), ('VARIANTE_PHOT', 'FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf'), ('ALT_PHOT', 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf')):
    m = json.load(open(W / 'conferencia' / ('medidas_%s.json' % lab), encoding='utf-8'))
    r = m['resumo']
    print(lab, 'sha ok:', m['sha256'] == sh(W / f), '| contatos', r['contatos_texto_grafico_total'], '| oclusoes', r['oclusoes_total'], '| cruzadas', r['palavras_cruzadas_por_traco_total'], '| RO livre', r['folhas_com_marcacao_do_RO_livre'], '| h_min', r['altura_minima_cap_alg_asc_cm_todas_as_folhas_texto_vivo'], '| nonBW', r['pixels_nem_preto_nem_branco_total'])
c = json.load(open(W / 'CONFERENCIA_050576.json', encoding='utf-8'))
print('conferencia sha ok:', c['folhas_substitutivas']['sha256'] == sh(W / 'FOLHAS_SUBSTITUTIVAS_050576.pdf'))
r = c['rodada_3']['R2-1 (unico bloqueio da 2a revisao)']
print(r['antes (PDF da rodada 2)'])
print(r['depois'])
print([x['arquivo'].split('\\')[-1] + ' ' + x['sha16'] for x in c['saidas_sha256']])
