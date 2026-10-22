# Funcional ímpar em k: o resíduo conserva sinal, o setor antifield desaparece

10/09/2026, investigação079. [DERIVED — demonstração escrita; revisão independente pendente]. Somente arquivos novos em Chatgpt. Este resultado usa o certificado078 e o sistema079, sem modificar suas fontes.

**Resultado.** Uma diferença de duas avaliações lineares elimina a contribuição direta de TODAS as espécies u*C⁴ à obstrução em valência seis, inclusive seus jatos, enquanto conserva A6. Não se impõe fechamento separado a essa espécie nem se presume fatoração das identidades de Noether. Isso reduz uma condição necessária de cancelamento ao termo quadrático Q[h,h;C³]. Os antifields continuam podendo ser necessários às demais identidades de fechamento.

## 1. A família e os dois sinais

Use exatamente a referência do certificado078: coordenadas (τ,x,y,z), g0=(ℓ/z)²diag(+---), z>0 espacial, Λ=3/ℓ², mapa sigma φ0 constante. Fixe k≠0 e z0>0. Seja f_k a solução local única de

f_k''−2f_k'/z+k²f_k=0,   f_k(z0)=0,   f_k'(z0)=1.

A EDO e os dados dependem de k apenas por k². Pela unicidade (ou pelas soluções elementares com Wronskiano não nulo do certificado), f_−k=f_k na vizinhança comum. Esta igualdade vale para todos os jatos em z.

Defina h_k=(ℓ/z)²γ_k, onde o bloco transversal é

γ_k|xy = f_k(z) [[cos(kτ),sin(kτ)],[sin(kτ),−cos(kτ)]],

e as outras componentes são zero. Ambas as perturbações h_k e h_−k satisfazem as equações lineares no mesmo fundo. Não se exige que g0+εh_k resolva a equação não linear exatamente. Podemos restringir ε e a vizinhança para manter a assinatura ao tomar derivadas em ε=0.

## 2. Por que o Einstein quadrático é par em k

Para tornar explícito qual objeto se usa, ponha

F(g)=Ric(g)−½g R(g)+Λg,   F(g0+εh)=εF1[h]+ε²F2[h,h]+...

O símbolo F2 é o COEFICIENTE de ε², sem um fator ½ adicional. É um tensor covariante simétrico, quadrático em h e seus jatos, construído somente da métrica, sua inversa e derivadas. Seus coeficientes para essa família dependem apenas de τ,z; x,y são coordenadas de translação.

Considere a rotação constante T de π/2 no plano xy, mantendo τ,z. Ela preserva g0 e transforma o bloco γ em −γ. A naturalidade tensorial de F dá

T*F2[h_k,h_k]=F2[T*h_k,T*h_k]=F2[−h_k,−h_k]=F2[h_k,h_k].

Como os coeficientes não dependem de x,y, esta é invariância matricial no MESMO (τ,z). Um tensor simétrico real invariante pela rotação de π/2 tem forma

F2 =
[[a,0,0,b],
 [0,c,0,0],
 [0,0,c,0],
 [b,0,0,d]],

na ordem (τ,x,y,z). Com efeito, os vetores mistos com uma única perna xy não têm vetor fixo dessa rotação; o bloco simétrico xy que comuta com ela é escalar. Nenhuma isotropia de todo o campo h foi presumida: h troca de sinal e F2 é quadrático.

Agora tome Y=diag(1,1,−1,1), a reflexão y→−y. Temos Y*g0=g0 e Y*h_k=h_−k. Toda matriz da forma acima é invariante sob Y. A mesma fórmula tensorial de Einstein fornece então

F2[h_−k,h_−k]=Y*F2[h_k,h_k]=F2[h_k,h_k].                 (1)

Não estamos exigindo que Y seja um morfismo admissível da categoria ORIENTADA de Q2 ou que uma cocadeia com epsilon seja invariante por Y. (1) é uma identidade da expressão métrica de Einstein, que não contém epsilon, comparando duas perturbações na MESMA orientação fixada. Alternativamente, ela pode ser conferida diretamente nos símbolos de Christoffel. Assim não se troca o sinal de orientação do funcional de avaliação.

A identidade é entre funções suaves de todas as coordenadas na vizinhança. Portanto todas as derivadas parciais e todos os jatos covariantes de fundo de F2 também são iguais para k e −k. Não é apenas uma coincidência num ponto.

## 3. Relação com a equação que aparece no antifield

A equação métrica da ação Einstein–sigma é, no setor φ0 constante, um múltiplo constante em k do tensor de Einstein com índices elevados, densitizado por √|det g|. Trabalhamos com os coeficientes relativos à orientação coordenada fixada. Esse fator usa o valor absoluto do determinante e não introduz um sinal sob a comparação algébrica anterior.

Como F0=0 no fundo e F1[h_±k]=0 em toda a vizinhança, o coeficiente quadrático da equação métrica normalizada é

E_g,2[h_±k,h_±k] = cκ √|det g0| g0⁻¹ F2[h_±k,h_±k] g0⁻¹,           (2)

com cκ o prefator fixado pela ação/convenção. Não se escolhe aqui seu sinal para compensar qualquer resultado: somente sua independência de k é necessária. Os termos que variam a densidade ou a elevação multiplicariam F0 ou F1 e, nesta família on-shell linear, são zero como funções, junto de seus jatos.

Logo E_g,2 e TODOS os seus jatos são pares em k. O setor sigma satisfaz E_sigma,2[h,0]=0 para qualquer h, como na projeção sigma079. Os acoplamentos, φ0 e os coeficientes herdados são os mesmos nas duas avaliações; não variam com k.

## 4. O funcional antissimetrizado

Sejam ev_k e ev_−k as avaliações do certificado078. Mantemos em ambas p=(0,0,0,z0), os quatro ghosts de Killing ∂τ,∂x,∂y,D/z0, os geradores Grassmann θ0,...,θ3, a orientação e todos os coeficientes de fundo. Variam somente h_k e seus jatos; ξ, antifields e seus jatos são zero.

Cada avaliação anula s0 de todos os geradores e seus prolongamentos. Para uma zeroforma A de ghost4, defina o funcional linear real

L_k(A) = coeff_(θ0θ1θ2θ3) ((ev_k A−ev_−k A)/2).

Consequentemente L_k(s0B)=0 para todo B admissível de ghost3. O funcional desce à classe de H⁴(s0) no grau de valência considerado. Ele é diferença de avaliações; não se afirma que seja homomorfismo de álgebras.

O certificado078 dá ev_±k(A6)=∓4k/z0 θ0θ1θ2θ3. Assim

L_k(A6)=−4k/z0 ≠ 0.                                      (3)

Em particular, L_k(r6)=L_k(A6), porque r6=A6−s0α6.

## 5. Eliminação de toda a contribuição direta de antifields

Uma expressão geral na espécie u*C⁴ pode ser escrita pontualmente como soma finita

B_R = Σ_(A,I) (∇bar_I u*_A) R^(A,I)(jC;B0),

com contrações herdadas e coeficientes independentes do campo h. Jatos de ghost arbitrários são permitidos. A valência cinco e ghost3 impedem qualquer fator adicional de h nessa espécie.

Primeiro aplicamos s1, depois avaliamos. Os termos em que s1 age em R continuam multiplicados por um antifield e desaparecem na avaliação. A parte Lie_Cu* também desaparece. Sobra

ev_±k(s1 B_R)
 = Σ_(A,I) ev_±k(∇bar_I E2,A) ev(R^(A,I)).

A contribuição sigma é zero; todos os jatos métricos são pares em k por (1–2). Os ghosts e os coeficientes R são idênticos nos dois lados, mesmo quando R contém epsilon. Portanto

L_k(s1 B_R)=0                                             (4)

para QUALQUER expressão finita dessa espécie. Não foi usada a hipótese s0B_R=0. A demonstração inclui jatos de antifields e não faz integração por partes.

## 6. O que isto impõe ao sistema completo079

Escreva, como na nota079,

b4=P[u;C³],  b5=½Q[u,u;C³]+B_R.

O fechamento prévio ainda exige s0b4=0 e s0b5+s1b4=0. Na valência seis, s2b4=0 para o mapa sigma constante; a condição é

s0b6+s1b5=−r6.

Aplicando L_k, usando (3–4) e colocando ξ=0, resulta a condição necessária explícita

L_k(s1(½Q[h,h;C³])) = +4k/z0.                             (5)

Assim, nenhuma solução com Q=0 pode cancelar A6, mesmo que P e R sejam permitidos e satisfaçam suas condições anteriores. Mais geralmente, qualquer candidato Q cujo s1 tenha avaliação par na família é excluído como único termo quadrático responsável.

Isso NÃO torna os antifields dispensáveis no sistema: eles ainda podem pagar o fechamento anterior e a parte linear em antifields da valência seis. A conclusão é sobre sua contribuição DIRETA a este funcional detector, não sobre a equivalência de complexos com ou sem antifields.

A corrente −I_CJ2 da nota079 possui o valor exigido em (5), mas falha o fechamento prévio se tomada isoladamente. Portanto (5) é um filtro necessário que já tem candidatos não nulos; não foi transformado numa falsa impossibilidade universal. A existência de P,Q,R,D,E,F que satisfaçam todo o sistema continua aberta.

## 7. Controle separado e limites

Um cálculo simbólico separado da raiz pode conferir F2 por Γ2, Ric2 e contrações, para f(z) arbitrária e k simbólico, e depois a especialização aos dados do ponto. O recibo desse cálculo, quando produzido, será evidência adicional finita; a demonstração de todos os jatos decorre da identidade de funções (1), não de enumerar infinitos jatos em um CAS.

As demonstrações acima são novas e aguardam revisão independente. Não se calcula δ(K) inteiro, nem H³/H⁴ completo, lim¹, anomalia quântica, QME ou UV. A fase/ramo do registro físico não é alterada: k→−k é um controle de polarização da família geométrica auxiliar, não o seletor canônico.

Fontes locais: certificado078, correção KT077 e sistema/projeção079 com seu adendo de ideal fechado e coeficientes herdados. Pins no manifesto desta nota. Nenhum original, documento078, Atlas ou memória canônica alterado; zero um.py e zero Lean.
