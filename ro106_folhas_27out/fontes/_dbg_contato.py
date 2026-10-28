import sys, pathlib
sys.path.insert(0, r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
import conferir as C
import numpy as np
from PIL import Image
pdf = r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\FOLHAS_SUBSTITUTIVAS_050576.pdf'
data = pathlib.Path(pdf).read_bytes()
t = C._render_so(data, 1, 'texto')
g = C._render_so(data, 1, 'grafico')
k = 600 / 2.54
box = (int(4.5 * k), int(18.5 * k), int(9.5 * k), int(26.2 * k))
for nome, a in (('texto', t), ('grafico', g)):
    im = Image.fromarray((~a[box[1]:box[3], box[0]:box[2]]).astype(np.uint8) * 255)
    im = im.resize((im.width // 3, im.height // 3))
    im.save(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\_tmp\dbg_%s.png' % nome)
    print(nome, a.sum())
