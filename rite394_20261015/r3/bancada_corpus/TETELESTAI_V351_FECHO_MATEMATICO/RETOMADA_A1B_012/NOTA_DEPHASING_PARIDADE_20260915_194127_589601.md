# Dephasing, dedução constante e paridade — discussão conceitual

[INPUT] Formulação do operador: “dephasing=dedução constante=paridade oposto do acoplamento mínimo”. A formulação recebida propõe C_min=+β_TGL P_+, D_deph=−β_TGL P_− e P_+P_−=0; descreve preservação das populações com perda exponencial de coerência.

[REAL — leitura, sem nova compilação] Consultadas as fontes da cópia RETOMADA_A1B_012/k/TGLExt: Ergodicity.lean define dephase(g,t,x)_ij=exp(−t g_ij)x_ij (linha 184), preserva a diagonal e demonstra convergência com taxas estritamente positivas fora dela. TheSingularExpectation.lean:76 contém dephase_fixed_iff_diagonal, com g_ii=0 e g_ij>0 para i≠j. O teorema caracteriza pontos fixos nessa família; taxas positivas arbitrárias, sozinhas, não demonstram positividade completa de todo multiplicador de Schur. Não houve execução do um.py, compilação Lean ou mudança de gate nesta discussão.

[DERIVED — consequências da lei exponencial] Para uma coerência inicialmente não nula, taxa Γ constante e dephasing puro na representação de interação, c(t)=exp(−Γt)c(0) implica −d_t ln|c(t)|=Γ. A dedução constante é relativa/logarítmica: −d_t|c|=Γ|c|, não subtração constante do módulo. A equação apenas para o módulo admite rotação adicional da fase; com Hamiltoniano diagonal pode aparecer exp(−iω_ij t). Γ depende do modo. β é adimensional, e não é por si só uma taxa dimensional. O Atlas registra Γ_ω=(β τ★/2)ω²; sua constância temporal requer os fatores relevantes constantes.

[DERIVED — realização de paridade, sob hipóteses explícitas] Se P_± são projeções ortogonais complementares, defina Z=P_+−P_−. Z é uma involução linear autoadjunta; não se identifica aqui com a conjugação antiunitária J de Tomita. No espaço dos operadores, R(X)=ZXZ satisfaz R²=id. Seus superprojetores são E_±=(id±R)/2, distintos dos projetores P_± do espaço de Hilbert.

E_+(ρ)=P_+ρP_++P_−ρP_− é o bloco preservado; E_−(ρ)=P_+ρP_−+P_−ρP_+ é a coerência entre blocos, ímpar sob R. Esta componente ímpar não é isoladamente uma matriz de densidade positiva. Para Γ≥0:

L_deph(ρ)=(Γ/2)(ZρZ−ρ)=−Γ E_−(ρ),
T_t(ρ)=E_+(ρ)+exp(−Γt)E_−(ρ), t≥0.

A forma de Lindblad usa operador de salto sqrt(Γ/2) Z. Equivalentemente T_t=[(1+exp(−Γt))/2]id+[(1−exp(−Γt))/2]R: mistura convexa de dois canais unitários, logo completamente positiva e preservadora do traço. O setor par tem autovalor 0 no gerador, o ímpar −Γ. Se os blocos têm dimensão maior que 1, coerências dentro de cada bloco também sobrevivem; somente para blocos unidimensionais o setor fixo é exatamente a diagonal completa. O mapa de pinching existente é E_+.

[DERIVED — distinção decisiva] A componente amortecida é ímpar; o gerador comuta com R (é covariante sob essa paridade). Para dephasing de energia L_K(X)=−c[K,[K,X]], c≥0, em dimensão finita ou domínio comum apropriado, L_{−K}=L_K. A inversão K→−K não inverte o dissipador: o sinal aparece duas vezes. O mesmo vale para a fórmula com |k_i−k_j| usada em uma leitura modular da cópia Ergodicity. Não se identifica parâmetro modular adimensional com tempo físico sem a escala correspondente.

[OPEN — identificação específica proposta] As fontes lidas não estabelecem que o acoplamento mínimo seja +β P_+ nem que sua conjugação gere dephasing de mesmo módulo. Um operador −β P_− isolado não especifica uma dinâmica dissipativa preservadora do traço. A realização acima sustenta o sentido de “deduzir a coerência do setor ímpar”; não prova que dissipação e acoplamento mínimo sejam operações de paridades opostas. A coincidência de β como coeficiente, se presente na construção, precisa ser distinguida da igualdade das operações e de suas unidades.

Fonte externa consultada para a forma GKSL: https://qutip.readthedocs.io/en/latest/guide/dynamics/dynamics-master.html (equação de Lindblad e operadores de salto). A especialização em Z e as identidades acima são derivadas nesta nota.

[ESCOPO] Discussão e memória próprias. Nenhuma nova camada Python/Lean, nenhuma reabertura de A2 entregue, nenhum dado experimental calculado. Atlas e originais preservados; esta nota registra a formulação e suas condições para posterior incorporação autorizada pela gerência.
