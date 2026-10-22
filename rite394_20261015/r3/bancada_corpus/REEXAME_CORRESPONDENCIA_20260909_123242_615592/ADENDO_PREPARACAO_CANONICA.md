# Adendo: a obrigação exata da preparação canônica
[REAL — fontes lidas em 09/09/2026; não nova recompilação canônica] Esta precisão acompanha o reexame e preserva seus resultados anteriores.

A preparação existente é coherentStateCurve(a,b,u,v,w,x,d) = unitaryStateCurve(a,b,⟨w(x),d⟩,u,v). Seu tempo é o da resposta local. Não se deve identificá-lo automaticamente com o tempo modular, nem com uma coordenada espacial afim.

Resultados que já existem e não devem ser pedidos novamente:
- CoherentHeatMatching.lean:35 — coherent_heat_matching: o calor construído da fonte covetorial coerente corresponde à resposta da mesma preparação.
- CoherentHeatMatching.lean:97 — coherent_area_matching_iff_ricci: o matching de área equivale a η Ric(d,d)=2π T_w(d,d).
- CoherentEinsteinBridge.lean:98, em especial a hipótese harea a partir de :107 — Einstein segue de suavidade, conservação obtida por fechamento/onda de w e matching de área.
- CoherentMatterControls.lean:159 e :171 — há fonte coerente conservada cujo calor corresponde e cuja área na tela plana não corresponde, para todo η. O canônico já controla que calor e conservação não implicam a condição de área.

Portanto, a obrigação restante não é reprovar a equivalência. É construir os objetos da mesma origem selecionada para os quais a condição verdadeira de área vale, juntamente com sua regularidade, conservação e interpretação entre cartas. Nas famílias curvas já construídas há testemunhas com alcance específico; preservá-las.

[REAL — inspeção de usos] As extensões Gibbs e somável consultadas conservam um único w. A fonte nula é da forma c·⟨w,d⟩². A soma de amplitudes modifica c; não equivale a uma família independente de covetores w_j. Não foi localizado nesse arco um construtor de todas as fontes de energia nula não negativa.

[OPEN] Uma extensão por Σ_j c_j w_j⊗w_j pode ser investigada, mas precisaria de preparação microscópica conjunta, suavidade, conservação, matching de área e domínio preciso de fontes representáveis. Uma decomposição algébrica pontual não paga essas condições.

[DERIVED — controle aritmético] No exemplo de recodificação de Minkowski por t=exp(s), o valor em s=0 foi também conferido com aritmética racional exata: (1/16)·2²/(1+1²)²=1/16. A dedução completa permanece no relatório como cálculo analítico revisto, não como novo teorema Lean.

Referências canônicas são lidas sob C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt. Nenhuma foi alterada. A nova cópia de bancada guarda tanto os avanços quanto o controle da amostragem afim.
