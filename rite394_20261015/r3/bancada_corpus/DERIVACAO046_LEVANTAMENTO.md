# Derivação046 — levantamento do limite em Ω

[DERIVED — anterior à escrita Lean; a formalização será validada separadamente.]

Sejam P um SiteProfile, H=TowerHilbert P, M=theFactorObject P e Ω=hOmega P. Dada uma sequência C_n:H→L[ℂ]H, suponha C_n∈M, ‖C_n‖≤K, K≥0 e C_nΩ→z. O alvo é construir B∈M com ‖B‖≤K, BΩ=z e C_nv→Bv para TODO v∈H. A existência de B e a convergência forte não são hipóteses.

1. Para cada matriz local a no corte N, a API existente rTowerPi_omega identifica r(a)Ω com a imagem GNS de a. A API factor_comm_rTowerPi dá C_n r(a)=r(a) C_n. Logo C_n(r(a)Ω)=r(a)(C_nΩ)→r(a)z, pela continuidade de r(a).

2. Esses vetores são densos: exists_tof representa todo vetor de TowerPre por uma matriz local e towerPre_denseRange dá densidade de TowerPre em H. Além disso, ‖C_n(v−w)‖≤K‖v−w‖ uniformemente em n. A aproximação por um vetor local e a desigualdade triangular em três termos mostram que (C_nv)_n é de Cauchy para cada v. A completude de H produz o limite f(v); este passo será provado, não pressuposto.

3. A sequência C_n é limitada na norma de operadores. A API mathlib ContinuousLinearMap.ofTendstoOfBoundedRange empacota a função limite f como operador contínuo linear complexo B, a partir da convergência pontual provada e da limitação da sequência. A desigualdade ‖Bv‖≤K‖v‖ passa ao limite; assim ‖B‖≤K. A unicidade do limite em Ω dá BΩ=z.

4. O fator é definido como duplo centralizador. Para y no primeiro centralizador, as igualdades yC_n=C_ny e y*C_n=C_ny* passam ao limite pontual, usando continuidade de y e y*. Portanto yB=By e y*B=By*, o que verifica diretamente a pertença B∈M. Não se usa a falsa inferência de que convergência em Ω, sozinha, implica convergência forte: a limitação uniforme e a órbita direita densa são essenciais.

5. Opcionalmente, a separância já existente factor_omega_separating prova unicidade do operador B em M a partir de BΩ=z. Esta unicidade não substitui a construção anterior.

Escopo: o módulo será independente de Cesàro e de qualquer período modular. Não constrói ainda o limite das médias em Ω para vetores gerais, nem um ExpectationInput, nem normalidade ou positividade completa. Ele fornece o levantamento limitado que faltava entre um limite vetorial demonstrado e um operador pertencente ao fator. Nenhuma hipótese física ou postulado de esperança é acrescentado.

Fontes locais de APIs: TGLExt.RightMult (rTowerPi_omega, factor_comm_rTowerPi e separância), TGLExt.TowerHilbert (towerPre_denseRange), Mathlib.Analysis.Normed.Operator.Completeness (ofTendstoOfBoundedRange). Os arquivos canônicos são somente leitura; não se compila nesta subtarefa.
