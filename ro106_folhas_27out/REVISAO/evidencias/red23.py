import fitz, numpy as np
from PIL import Image
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
d=fitz.open(W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf")
# 2/3 reduction scanned at 300 dpi == render at 200 dpi (linear)
pg=d[1]
pm=pg.get_pixmap(dpi=200,colorspace=fitz.csGRAY)
a=np.frombuffer(pm.samples,dtype=np.uint8).reshape(pm.h,pm.w)
b=(a<128).astype(np.uint8)*255
Image.fromarray(255-b).crop((int(250*200/125/1.0*0.0),int(900*200/125),pm.w,int(1400*200/125))).save("red23_apr2_fig3.png")
Image.fromarray(a).crop((0,int(900*200/125),pm.w,int(1400*200/125))).save("red23_apr2_fig3_gray.png")
# count residual dotted grid dark px along a vertical grid line? report ink fractions
print(pm.w,pm.h)
