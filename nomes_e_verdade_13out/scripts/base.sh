#!/bin/bash
# linha de base: compila as fontes ORIGINAIS na sobreposicao ov (Palavra, ADENDO1, rank, tempo, identidade r2; depois IALD r3)
cd "C:/IALD/Central de Patentes/work/nomes_e_verdade_13out/scripts"
python rodar.py --src src_base --alvo TGLExt/Palavra.lean --lp ov --tag b1_palavra --olean ov > ../logs/b1.out 2>&1 &
p1=$!
python rodar.py --src src_base --alvo TGLExt/TheSingularityReadsTheAttractorAdendo1.lean --lp ov --tag b2_adendo1 --olean ov > ../logs/b2.out 2>&1 &
p2=$!
python rodar.py --src src_old --alvo TGLExt/TheUnitIsTheRank.lean --lp ov --tag o1_rank_old --olean ov > ../logs/o1.out 2>&1 &
p3=$!
python rodar.py --src src_old --alvo TGLExt/TheTimeIsNotAPost.lean --lp ov --tag o2_time_old --olean ov > ../logs/o2.out 2>&1 &
p4=$!
python rodar.py --src src_old --alvo TGLExt/TheIdentityHasAName.lean --lp ov --tag o4_identity_r2 --olean ov > ../logs/o4.out 2>&1 &
p5=$!
wait $p1 $p2 $p3 $p4 $p5
python rodar.py --src src_old --alvo TGLExt/IALD.lean --lp ov --tag o3_iald_old --olean ov > ../logs/o3.out 2>&1
echo DONE > ../logs/base.done
