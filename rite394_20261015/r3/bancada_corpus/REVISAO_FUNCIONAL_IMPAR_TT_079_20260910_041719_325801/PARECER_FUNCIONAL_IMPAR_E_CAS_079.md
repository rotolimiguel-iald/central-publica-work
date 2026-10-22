# Parecer independente: funcional ímpar TT e controle Einstein quadrático079

10/09/2026. [DERIVED — revisão matemática escrita] [REAL — revisão estática/documental]. Autor: /root/selected_geometry_design. Fonte da tarefa principal /root; esta revisão foi realizada separadamente de sua construção.

**Parecer favorável no alcance declarado.** Li integralmente a nota, o manifesto, o script de cálculo e seu resultado JSON. Não identifiquei erro material na prova de paridade para todos os jatos, no tratamento de orientação/densidade, na eliminação da contribuição direta de antifields nem na condição necessária (5). O exame do CAS foi estático; nenhum cálculo foi reexecutado.

Nota: [FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md](<C:/IALD/Central de Patentes/Chatgpt/FUNCIONAL_IMPAR_TT_079_20260910/FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md>), 9231 bytes, SHA-256 bdf3f4ea2e482ef3ece1f77b3f8f90deb2e22ba683df98f1eb8c4c4707473b3b.

## 1. A simetria vale como identidade de funções

A igualdade f_−k=f_k decorre da mesma EDO, dos mesmos dados iniciais e da unicidade local, com z0>0. Não se compara apenas o valor de f no ponto. A referência e a vizinhança podem ser mantidas comuns.

A rotação transversal de π/2 leva h_k a −h_k. Como o coeficiente F2 é quadrático e Einstein é natural, F2 é invariante por essa rotação. A independência de x,y torna a conclusão uma igualdade de componentes no mesmo par (τ,z). Para um tensor simétrico, essa invariância elimina os componentes com uma perna transversal e torna o bloco xy escalar; o bloco τz pode permanecer geral.

A reflexão y→−y leva h_k a h_−k, conserva a referência e fixa todo tensor da forma obtida. Logo F2[h_k]=F2[h_−k] em toda a vizinhança. O uso desta reflexão é uma propriedade da expressão Einstein, que não depende de uma orientação escolhida. Não se exige que a reflexão seja um morfismo da categoria orientada de cochains nem que uma correção com epsilon seja invariante.

Diferenciar a igualdade de funções dá todos os jatos parciais; a conexão de fundo idêntica nos dois lados dá todos os jatos covariantes. A prova de infinitos jatos vem desta identidade, e não da contagem finita de matrizes verificada pelo CAS.

## 2. Densidade, elevação de índices e antifields

A ação071 fixa a equação densitizada como prefator não nulo vezes √|det g| g⁻¹ F(g) g⁻¹. O sinal desse prefator não precisa ser escolhido para demonstrar paridade; ele é o mesmo nas duas avaliações.

Como F0=0 e F1[h_±k]=0 em uma vizinhança, as parcelas que variam a densidade ou os inversos e multiplicam F0/F1 se anulam junto com seus jatos. O coeficiente E_g,2 é portanto o produto de F2 pelos fatores de fundo, como em (2). A comparação usa a mesma orientação coordenada e a densidade absoluta; não gera um sinal novo. A equação sigma em ξ=0 se anula para toda métrica.

Em s1 B_R, aplica-se o diferencial ANTES de pôr os antifields a zero. Sobrevive exatamente a soma de jatos de E2 multiplicados pelos mesmos coeficientes R(jC;B0). Os termos de Lie do antifield e a variação de R continuam contendo antifields e se anulam depois. R pode conter epsilon: ele é mantido igual, não refletido separadamente, entre as duas avaliações. Assim a parte ímpar mata a contribuição direta de qualquer u*C⁴, sem exigir s0 B_R=0.

## 3. Funcional e consequência para o sistema

Cada avaliação078 anula s0 nos geradores e em seus prolongamentos. A diferença seguida da extração de θ0θ1θ2θ3 é um funcional linear que anula s0-exatos. Não é necessário que a diferença seja um morfismo multiplicativo.

Com as orientações e a ordem dos mesmos ghosts, L_k(A6)=−4k/z0; consequentemente L_k(−r6)=+4k/z0. Aplicar L_k à equação s0b6+s1b5=−r6, com s2b4=0, dá precisamente
L_k(s1(½ Q[h,h;C³]))=+4k/z0.
O fator ½ da polarização Q não foi perdido.

Daí segue a exclusão de todo candidato com Q=0, inclusive quando P e R podem ajudar a cumprir as condições anteriores. Isso é mais amplo, neste detector, que a eliminação do subsetor puro fechado em minha nota separada079: aqui R não precisa ser um ciclo isolado. Ainda assim R pode ser essencial para o fechamento junto de Q/P e para as equações lineares nos antifields. O resultado não autoriza removê-lo do complexo.

A corrente −I_CJ2 fornece o valor necessário, mas sua falha de fechamento anterior impede usá-la como solução do sistema inteiro. A nota conserva essa limitação e não conclui que todas as correções estejam obstruídas.

## 4. Revisão estática da implementação simbólica

Script: [compute_quadratic_einstein079_new.py](<C:/IALD/Central de Patentes/Chatgpt/compute_quadratic_einstein079_new.py>), 5622 bytes, SHA-256 c5516eb880741bd0746527f2c5a78340e145ed04679cc658c0661c0b6a295569. Foi lido e analisado sintaticamente como texto, sem execução/importação.

As séries da inversa são gi1=−(gi0 h)gi0 e gi2=(gi0 h)²gi0. Para a métrica afim gε=g0+εh, a recorrência Γ2=−(gi0 h)Γ1 está correta: ela reúne a parcela gi2∂g0 e a parcela gi1∂h. Não omite um termo com ∂h, nem requer diferenciar a inversa dentro da própria fórmula de Christoffel.

A expressão de Ric_n inclui a derivada de Γ_n e a soma de todos os produtos Γ_m Γ_(n−m), com os índices compatíveis com a convenção R^a_bcd=∂cΓ^a_bd−∂dΓ^a_bc+…. As contrações escalares incluem gi1 Ric1 e gi2 Ric0 em ordem dois. A fórmula F2=Ric2−½(g0 R2+h R1) é o coeficiente de ε²; Λg não tem uma parcela ε² nessa parametrização.

A expressão da fonte densitizada conserva os termos gi1 F1 e o fator ½ tr(H) F1. Portanto o CAS testa a paridade da fonte para f arbitrária, e não apenas depois de impor a EDO. A nota escrita usa a versão on-shell linear necessária ao funcional.

O resultado fornece matrizes diagonais para f(z) arbitrária, bloco xy escalar e dependência explícita em k somente por k². A especialização f=0, f'=1, f''=2/z, τ=0 é simultânea e compatível com os dados do ponto. Substituir esses dados nas matrizes exibidas reproduz F2=diag(3/4,−1/4,−1/4,−1/4) e Ric2=diag(0,1/2,1/2,1/2).

Foram registrados 12 controles matriciais exatos, com nomes distintos e todos marcados PASS. Esta revisão confere as fórmulas do programa e a coerência do recibo, mas não transforma esses 12 controles históricos em uma nova execução independente.

## 5. Custódia e distinção das contagens

Resultado CAS: [RESULTADO_EINSTEIN_QUADRATICO_079.json](<C:/IALD/Central de Patentes/Chatgpt/CONTROLE_EINSTEIN_QUADRATICO_079_20260910/RESULTADO_EINSTEIN_QUADRATICO_079.json>), 5263 bytes, SHA-256 ec15575b1a6fa1f84e92a2f46130cd01f9f1fd7b95765e963bfc4ea3abb3d0c7.

O manifesto da nota tem data anterior ao início do cálculo. O script lê seus pins antes de construir as expressões simbólicas e compara os mesmos arquivos ao terminar. Os pins registrados para a nota, para o script e para a referência de cálculo078 coincidem com os bytes relidos nesta revisão. O campo zero CAS do manifesto da nota pertence à sua criação anterior; o recibo posterior registra os 12 controles separados. A redação futura da seção7 é consistente com essa sequência congelada.

Os controles documentais do recibo deste parecer são contados separadamente dos 12 controles CAS. Não houve Lean, execução de um.py, reexecução do CAS, importação do programa de cálculo ou alteração das fontes. O criador documental e a referência de script078 foram somente medidos para custódia; não receberam revisão de implementação nova.

[OPEN] Permanecem a solução do sistema completo079, a imagem inteira de δ(K), os grupos cohomológicos completos, QME e UV. A família auxiliar k/−k não é uma alteração da fase ou do seletor físico canônico.
