/- SONDA de instalação (rodada 2; NÃO é pedra): importar JUNTOS a pedra e um vizinho que também realizou
   `TGLExt.rhoOut.eq_1`. Se o ambiente recusar a constante duplicada, a instalação na v392 precisa trocar a prova de
   `rhoOut_zero` (que hoje gera a equação); se aceitar, não há colisão por esta via. -/
import ColA
import TheUnitIsTheRank

#check @TGLExt.rhoOut.eq_1
#print axioms TGLExt.TheUnitIsTheRank.rhoOut_zero
#print axioms SondaColA.rhoOut_zero_via_unfold
