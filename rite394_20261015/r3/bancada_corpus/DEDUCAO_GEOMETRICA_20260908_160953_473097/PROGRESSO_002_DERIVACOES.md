[DERIVED — cálculos em formalização] UTC 2026-09-08T16:17:03.247943.

1. Distância espectral d_t(x,y)=|g_t(x)-g_t(y)|: métrica para t≠0, escala c>0 livre se só se exige a mesma covariância.
2. Métrica de Fisher na coordenada radial r: H(r)=Σ b_n²/[q_n(r)(1-q_n(r))]. Para r∈[0,1], 1/96≤H(r)≤4/357. Em t, G(t)=r'(t)²H(r(t)); G(0)=0, G(t)>0 fora da origem. Degenerescência de parametrização, não divergência física.
3. No ansatz de Dirac D=L_t, todos os testes cP_n têm comutador zero e diferença entre configurações arbitrariamente grande. A distância definida por esse seminorma é infinita entre pontos diferentes, ao contrário da distância espectral finita. Esse ansatz não serve como Dirac métrico.
4. Os unitários exp(is P_n) preservam os dois estados, o gerador e o cociclo, mas P_0 não comuta com E_01 da álgebra ambiente. Há liberdade dinâmica/gauge além do setor diagonal; decidir o significado físico dessa liberdade exige especificação adicional.
5. No contrato canônico MicroscopicEinsteinBridge, coframe, tensores suaves, conservação, heat_matching e area_matching são hipóteses explícitas. Nenhuma delas foi silenciosamente inserida na dedução atual.

Fontes novas: SpectralMetricGeometry.lean, InfiniteFisherGeometry.lean, RelativeCocycleGeometricObstructions.lean. A primeira compilação está em curso; não estão declaradas aprovadas neste registro.
