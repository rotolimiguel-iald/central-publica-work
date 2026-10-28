# Registra (somente leitura dos PDFs) o teste de contato texto x grafico: antes (rodada 2) e depois (rodada 3), e o MQC congelado.
import sys, json, pathlib
sys.path.insert(0, r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
import conferir as C
import fitz
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
alvos = {
    'rodada2_050576 (a266d4a46594b3b2, antes do reparo R2-1)': W / '_tmp/base/apr_rodada2.pdf',
    'rodada3_050576_principal': W / 'FOLHAS_SUBSTITUTIVAS_050576.pdf',
    'rodada3_050576_variante_PHOT': W / 'FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf',
    'rodada3_folha_alternativa_PHOT': W / 'ALTERNATIVA_FOLHA_1_050576_PHOT.pdf',
    'MQC_050579_congelado (so leitura)': W / 'FOLHAS_SUBSTITUTIVAS_050579.pdf',
}
out = {'metodo': 'texto e grafico renderizados em separado (600 dpi, sem antialias) por redacao em copia na memoria; contato = pixel de tinta comum; componentes >= 3 px; exclui a regua do radical (palavra com a raiz quadrada)'}
for nome, pdf in alvos.items():
    n = fitz.open(str(pdf)).page_count
    folhas = []
    for i in range(n):
        ct, info = C.contato_texto_grafico(str(pdf), i)
        folhas.append({'folha': i + 1, 'contatos': ct, **info})
    out[nome] = {'pdf': pdf.name, 'folhas': folhas, 'total_de_contatos': sum(len(f['contatos']) for f in folhas), 'pixels_em_contato': sum(c['px'] for f in folhas for c in f['contatos'])}
    print(nome, out[nome]['total_de_contatos'], out[nome]['pixels_em_contato'])
(W / 'conferencia' / 'contato_texto_grafico_r3.json').write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding='utf-8')
