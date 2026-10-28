# Roda SO o teste de contato texto x grafico (pixel a pixel) num PDF. Uso: python contato_rapido.py <pdf>   (somente leitura)
import sys
sys.path.insert(0, r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
import conferir as C
import fitz
pdf = sys.argv[1]
n = fitz.open(pdf).page_count
tot = 0
for i in range(n):
    ct, info = C.contato_texto_grafico(pdf, i)
    tot += len(ct)
    print(i + 1, 'contatos:', len(ct), ct[:6], '| texto px', info['pixels_de_texto'], 'grafico px', info['pixels_de_grafico'])
print('TOTAL', tot)
