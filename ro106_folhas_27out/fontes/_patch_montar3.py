import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\montar_conferencia.py')
s = p.read_text(encoding='utf-8')
a = "                        'estatuto': '[LEGAL] decisao do agente de PI'}\n        base['R2_Fig5_Proxima_geracao']"
assert s.count(a) == 1
s = s.replace(a, """                        'estatuto': '[LEGAL] decisao do agente de PI',
                        'medidas_da_folha_alternativa': alt_resumo()}
        base['R2_Fig5_Proxima_geracao']""")
b = "def reparos(k, med):"
assert s.count(b) == 1
s = s.replace(b, '''def alt_resumo():
    pj = W / 'conferencia' / 'medidas_ALT_PHOT.json'
    if not pj.exists():
        return 'medidas_ALT_PHOT.json ausente'
    m = json.load(open(pj, encoding='utf-8'))
    f = m['folhas'][0]
    return {'pdf': 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf', 'sha256': m['sha256'], 'resumo': m['resumo'], 'margens_cm': {kk: float(v) for kk, v in f['margens_medidas_cm'].items()},
            'altura_minima_caractere_cm': f['altura_por_linha_texto_vivo']['h_min_cap_alg_asc_cm'], 'oclusoes': len(f['oclusao_fundo_branco_sobre_traco_ou_marca']),
            'marcacao_RO_livre': f['marcacao_do_RO_areas_livres']['livres'], 'palavras_cruzadas': len(f['texto_cruzado_por_traco']),
            'paisagem': f['folha_em_paisagem_topo_a_esquerda']}


def reparos(k, med):''')
p.write_text(s, encoding='utf-8')
print('ok')
