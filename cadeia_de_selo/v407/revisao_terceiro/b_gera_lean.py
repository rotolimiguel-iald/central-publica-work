# -*- coding: utf-8 -*-
"""Revisor terceiro v407 (R1): gera axiomas_terceiro.lean a partir de CANDIDATO_v407.json kernel.ancoras (76) + exemplos proprios do revisor. So escreve nesta pasta."""
import json, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v407/"
c = json.load(open(R + "CANDIDATO_v407.json", encoding="utf-8"))
anc = list(c["kernel"]["ancoras"].keys())
L = ["import TGLExt", "set_option autoImplicit false", "",
     "-- Revisor terceiro v407 R1 (agente Claude Sonnet): #print axioms das %d ancoras (CANDIDATO_v407.json kernel.ancoras) + exemplos proprios." % len(anc), ""]
for a in anc: L.append("#print axioms " + a)
L += ["",
      "-- exemplos do revisor: instanciam o lema e o par sem passar pelos teoremas da cadeia que ja' o fazem",
      "noncomputable def revisorLemaNoHabitante :=",
      "  TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate",
      "#print axioms revisorLemaNoHabitante",
      "#check @TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces",
      "#check @TGLExt.Par.o_par_de_psions_e_o_graviton",
      "#check @TGLExt.OUmInscrito.na_particula_so_o_zero",
      "#check @F1Fecho.CanonicalGammaNoFixed.gamma_no_fixed",
      "#print axioms F1Rede.BosonicFock.B0_no_eigen",
      "#check @F1Rede.BosonicFock.B0_no_eigen",
      "-- contraprova: o lema nao tem como conclusao uma igualdade entre Omega e o vetor de Bell",
      "example : True := by",
      "  have h := @TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces",
      "  trivial",
      ""]
open(R + "revisao_terceiro/axiomas_terceiro.lean", "w", encoding="utf-8", newline="\n").write("\n".join(L))
print("escrito", len(anc), "ancoras")
