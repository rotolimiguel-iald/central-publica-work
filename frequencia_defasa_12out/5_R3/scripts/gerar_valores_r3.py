# -*- coding: utf-8 -*-
r"""RODADA 3 — variante de TiposTheUnitIsTheRank.lean que le o VALOR (prova/definicao) pelo construtor de ConstantInfo
(thmInfo/defnInfo), porque `ConstantInfo.value?` devolveu 0 para teoremas na primeira passagem. Gera
5_R3\sandbox\ValoresTheUnitIsTheRank.lean e 5_R3\sandbox_r2\ValoresTheUnitIsTheRank.lean a partir dos Tipos*.lean."""
import os
R3 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANT = '      let hv : UInt64 := match ci.value? with | some v => v.hash | none => 0'
NOV = ('      let hv : UInt64 := match ci with\n'
       '        | .thmInfo t => t.value.hash\n'
       '        | .defnInfo d => d.value.hash\n'
       '        | _ => 0')
for sb in ("sandbox", "sandbox_r2"):
    src = os.path.join(R3, sb, "TiposTheUnitIsTheRank.lean")
    dst = os.path.join(R3, sb, "ValoresTheUnitIsTheRank.lean")
    s = open(src, encoding="utf-8").read()
    if s.count(ANT) != 1:
        raise SystemExit("FALHA VISIVEL: ancora nao unica em " + src)
    s = s.replace(ANT, NOV).replace("TIPOS E VALORES", "VALORES (variante thmInfo/defnInfo)")
    with open(dst, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(s)
    print(dst)
