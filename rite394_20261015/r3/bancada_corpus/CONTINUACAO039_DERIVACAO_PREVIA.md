# Continuação039 — derivação anterior ao código
[DERIVED/INPUT/OPEN] 06/09/2026. A etapa038 foi progresso: excluiu uma identificação universal da norma angular com o déficit óptico. A árvore canônica foi relida (v325); assinatura, origem dos dados geométricos, H3 e globalização continuam OPEN. Nenhuma ordem009 foi encontrada.

Alvo: construir a ponte do cone positivo do bloco M2 já presente na torre para uma forma quadrática de assinatura(1,3), ligando as coordenadas ao filtro já construído. A ordem007C literal não é redefinida: congruência por filtro não é automorfismo modular, nem entrelaçamento unitário finito com boost.

1. Coordenadas: X(t,x,y,z)=[[t+z,x-iy],[x+iy,t-z]]. Provar hermiticidade, inversa coordenada, detX=t²-x²-y²-z², e positividade/determinante nulo dos produtos externos vv*. Isso representa TODO o espaço hermitiano local, não apenas matrizes diagonais.

2. Seleção pelo cone: para uma forma quadrática REAL q de dez coeficientes, exigir q(coords(vv*))=0 para todo v complexo2. Nove avaliações bastam: v=(1,±1),(1,±i),(1,0),(0,1),(1+2i,1-2i),(2,1),(2,i). As seis primeiras anulam mistos temporais e fixam os três sinais espaciais; as últimas anulam os mistos espaciais. Conclusão q(X)=q(I)detX. Se q(I)>0, a assinatura é(1,3); a escala é livre. Isso exige forma quadrática, não mera homogeneidade. O critério pode ser enunciado para matrizes positivas singulares, incluindo zero. Não exige nem demonstra posto um como operador na torre infinita.

3. Filtro: para os logaritmos locais ell0,ell1 EXISTENTES, chi=(ell0-ell1)/2. R=exp(Llocal/2) é relativeFilter. Rhat=exp(-(ell0+ell1)/4)R=diag(exp(chi/2),exp(-chi/2)). Provar detRhat=1, preservação do determinante por X↦Rhat X Rhat*, e ação hiperbólica no plano(t,z). Sua fase U=exp(i theta Llocal) age como rotação no plano(x,y). Rhat I Rhat*=Rhat², portanto a congruência não é unital salvo chi=0. A normalização por determinante não conserva em geral a normalização de estado omega(R²)=1.

4. Ponte local/global: investigar e provar a redução do filtro global para o bloco0 por esperança do estado-produto: E0(RXR)=R0 X R0 para X local0, usando normalização da cauda. Uma igualdade somente de expectativas escalares será identificada como tal, nunca como igualdade de operadores.

Controle de fidelidade: siteOperator_injective já existe e deve ser reutilizado. A propriedade de raio extremo é DO CONE LOCAL. A projeção local e0 decompõe-se globalmente como e0e1+e0(I-e1); o cone global não seleciona esse bloco ou esses raios. A estrutura matricial2x2 fornece dimensão real4; não deriva quatro dimensões físicas de omega(I)=1.

A formalização planejada usa HermitianLocalCoordinates, HermitianConeRigidity, LocalFilterLorentzAction e GlobalFilterLocalReduction. Cada declaração nova terá #print axioms, sem axiomas extras, sem sorry/native_decide e sem instância anônima. Builds seriais em pastas novas, mais importação conjunta do lote. Dependências históricas serão escolhidas por bytes dos manifestos e dos builds limpos, incluindo overrides035 para evitar o olean de raiz stale.

Revisão analítica independente: McClintock verificou rigidez por nove avaliações e localizou GeneralNullCone/TensorNullCone; Beauvoir verificou hipóteses, fidelidade do sítio e limite local/global; Newton investiga APIs de redução. Fonte primária do modelo hermitiano: John Baez, seção Connection to special relativity, https://math.ucr.edu/home/baez/diary/may_2024.html . A identidade de determinante é conhecida; a contribuição desta bancada é sua ligação tipada aos objetos e hipóteses deste projeto.

Nada nesta etapa autoriza declarar área gravitacional, seleção do bloco físico, solda, conexão, H3 ou QG resolvida. Originais, um.py, kernel, Atlas, memórias e gates permanecem read-only. Escrita somente em Chatgpt.
