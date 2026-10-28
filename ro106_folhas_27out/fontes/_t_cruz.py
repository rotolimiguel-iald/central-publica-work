import sys
sys.path.insert(0, r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
import conferir as C
import fitz
W = r'C:\IALD\Central de Patentes\work\ro106_folhas_27out'
for nome in (r'\_tmp\base\apr_rodada2.pdf', r'\FOLHAS_SUBSTITUTIVAS_050576.pdf', r'\FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf'):
    d = fitz.open(W + nome)
    n = 0
    for i, pg in enumerate(d):
        cr, ov, incl = C.cruzamentos(pg)
        if cr or ov:
            n += 1
            print(nome, i + 1, [c['palavra'] for c in cr], ov[:2])
    print(nome, 'folhas com ocorrencia:', n)
