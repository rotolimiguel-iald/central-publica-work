import sys
sys.path.insert(0,r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\r2")
import occl
W=occl.W
for lab,p in (("main_R3",W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf"),("variante_R3",W+r"\FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf"),("alt_f1_R3",W+r"\ALTERNATIVA_FOLHA_1_050576_PHOT.pdf")):
    occl.run(p,lab)
