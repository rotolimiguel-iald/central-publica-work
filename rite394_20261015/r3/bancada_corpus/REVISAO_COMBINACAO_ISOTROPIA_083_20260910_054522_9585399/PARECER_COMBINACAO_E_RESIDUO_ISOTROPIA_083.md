# Revisão independente: combinação TT e resíduo de isotropia083

10/09/2026. Autoria: finish_gibbs_realization. [DERIVED — revisão escrita independente]. [REAL — medições documentais no recibo]. Investigação083, excluída da entrega082. Nenhuma reexecução matemática, CAS, Lean ou execução/importação de um.py.

**Conclusão delimitada.** Li integralmente a [nota da combinação](<C:/IALD/Central de Patentes/Chatgpt/COMBINACAO_TT_E_FALHA_ISOTROPIA_083_20260910/COMBINACAO_NO_DETECTOR_E_CONTRAEXEMPLO_ISOTROPIA.md>) e seu manifesto. Refiz à mão o diferencial de β, as multiplicações e levantamentos das matrizes, a combinação de perfis e a avaliação alternativa. Não identifiquei erro material: a combinação prescrita passa no detector TT para todo k, mas seu defeito tem componente não nula na outra avaliação de Killing, inclusive modulo fronteiras s0.

Essa conclusão exclui apenas a classe da combinação indicada e os representantes que diferem dela por s0. Não exclui outras classes de candidatos. Este parecer não atribui sua conclusão à aprovação da raiz, do autor da nota ou do operador.

## 1. Objetos e domínio fixados

O domínio é o da referência espaço-forma de curvatura K>0 real fixada, assinatura \(+---\), \(\phi_0\) constante, setor métrico mínimo e escalares herdados inertes. No ponto \(p_0=(0,0,0,z_0)\), \(z_0=\ell\), \(g_0(p_0)=\eta\) e \(K=z_0^{-2}\).

Conservo as definições
\[
J=\operatorname{tr}(W_1\wedge W_1)/\operatorname{vol}_{g_0},
\quad
\nu(p)=\varepsilon_{abcd}p^ap^bp^cp^d/4!,
\quad a=J\nu(p),
\]
\[
\beta_o=-\tfrac12\varepsilon_{abcd}p^ap^bM^{cd},
\quad
q_{\rm grad}=\varepsilon_{abcd}(\bar\nabla^aJ)p^bp^cp^d/3!.
\]
M é a parte antissimétrica de \(\bar\nabla C\); em Killing \(M^a{}_b=\bar\nabla_bC^a\). Portanto \(M_{ab}=-m_{ab}\), para \(m_{ab}=\bar\nabla_{[a}C_{b]}\). Essa troca de sinal em relação à matriz m elevada da nota finita082 foi explicitada corretamente.

O candidato é
\[
Q=-J\beta_o/(12K)-q_{\rm grad}/(28K).
\tag{R1}
\]
Ele tem duas pernas métricas e três ghosts, E5 e ghost3. O fechamento s0 decorre do fechamento de W1, de seus jatos e dos ghosts lineares. O coeficiente 1/K é uma constante real no domínio fixado e não depende do k da perturbação. Isso não fornece uma fórmula polinomial regular num anel universal com K variável ou em K=0.

## 2. Conferência do perfil TT inteiro

As entradas da combinação são as identidades previamente demonstradas:
\[
R(k)=L_k(s_1(J\beta_o))=24k^3/z_0-96k/z_0^3,
\]
\[
L_k(s_1q_{\rm grad})=(\bar\Box J)(p_0)
=112k/z_0^3-56k^3/z_0.
\]
O segundo perfil usa \(dq_{\rm grad}=(\bar\Box J)\nu(p)\) e \(\nu(p_0)=\theta^{0123}\) na avaliação original. Seus termos s0 são conservados na realização BRST e anulados pela avaliação sobre a solução linear com Killing.

Refiz a combinação antes de substituir K:
\[
-R/(12K)-(\bar\Box J)(p_0)/(28K)
=\frac{-2k^3/z_0+8k/z_0^3+2k^3/z_0-4k/z_0^3}{K}
=\frac{4k}{Kz_0^3}.
\]
Usando \(K=z_0^{-2}\), isso é \(+4k/z_0\) para todo k. Os coeficientes não foram ajustados a um único modo. Como o alvo A6 tem resposta \(-4k/z_0\), o detector TT original anula o defeito inteiro dessa combinação.

Essa igualdade é entre perfis de um funcional. Ainda não é igualdade entre cocadeias ou classes; os §§3–6 da fonte verificam justamente a distinção.

## 3. Derivação direta de dβ, com sinais graduados

No CE adotado,
\[
dp=-Mp,\qquad dM=-M^2+Kpp^\flat.
\]
Todos os componentes p e M são ímpares; \(Mp\), \(M^2\) e dp são pares. Para conferir a forma covariante utilizada pelo autor, expandi diretamente o produto de β.

Escreva
\[
T=\varepsilon_{abcd}p^ap^b(M^2)^{cd},
\quad
U=\varepsilon_{abcd}(Mp)^a p^bM^{cd}.
\]
As duas parcelas em que d atua nos p somam U: a segunda adquire um sinal ao trocar a,b, e \(Mp\) é par. A parcela dM dá \(T/2-12K\nu\). Assim
\[
d\beta_o=U+T/2-12K\nu.
\]
A invariância infinitesimal de ε, com M aplicado aos quatro índices e os fatores reordenados pela paridade, dá \(2U+2T=0\). As duas parcelas dos índices dos p são iguais a U; as duas parcelas dos índices de M são iguais a T. Portanto
\[
\boxed{d\beta_o=-T/2-12K\nu(p).}
\tag{R2}
\]
O termo de curvatura usa \((pp^\flat)^{cd}=p^cp^d\) e \(\varepsilon pppp=24\nu\). O sinal − e o fator 12 conferem.

Isso também explica o fator 2 em \([M,M]_{\rm gr}=2M^2\) da organização covariante apresentada na fonte. Tratar esse colchete como um comutador de matrizes pares apagaria uma parcela necessária.

Como J é par e escalar para a isotropia orientada,
\[
d(J\beta_o)=(p\cdot\bar\nabla J)\beta_o
-JT/2-12KJ\nu.
\]
Logo
\[
dQ+a=
-\frac{(p\cdot\bar\nabla J)\beta_o}{12K}
+\frac{J}{24K}T+
\left(2J-\frac{\bar\Box J}{28K}\right)\nu.
\tag{R3}
\]
Conferi em particular o fator 2J: uma parcela Jν vem da curvatura em \(d(J\beta_o)\), e a outra é o alvo acrescentado. A fórmula (14) da fonte está correta.

## 4. As matrizes realmente utilizadas na avaliação

A fonte define, por entradas, \(J_{ab}[a,b]=\eta_{aa}\) e \(J_{ab}[b,a]=-\eta_{bb}\). Portanto
\[
J_{02}[0,2]=J_{02}[2,0]=1,\quad
J_{03}[0,3]=J_{03}[3,0]=1,
\]
\[
J_{23}[2,3]=-1,\quad J_{23}[3,2]=1.
\]
Não identifiquei essas matrizes pelo nome com \(e_ae_b^\flat-e_be_a^\flat\) de outra passagem: para as duplas de assinatura mista, essa expressão tem o sinal oposto. As entradas presentes fixam inequivocamente o dicionário.

Com
\[
p=\theta^0e_0+\theta^1e_1,\qquad
M=\theta^2J_{02}+\theta^3J_{03},
\]
a multiplicação dá
\[
[J_{02},J_{03}]=-J_{23},\qquad M^2=-\theta^{23}J_{23}.
\]
As entradas mistas são \((M^2)^2{}_3=+\theta^{23}\) e \((M^2)^3{}_2=-\theta^{23}\). Levantar o segundo índice espacial muda o sinal:
\[
(M^2)^{23}=-\theta^{23},\qquad
(M^2)^{32}=+\theta^{23}.
\]
Consequentemente
\[
T=-4\theta^{0123},\qquad \nu(p)=0.
\]
As quatro contribuições iguais vêm das duas ordens de p0,p1 e das duas ordens dos índices 2,3. Por (R2),
\[
\boxed{\operatorname{ev}_{\rm iso}d\beta_o=+2\theta^{0123}.}
\tag{R4}
\]

Conferi também a decomposição direta: \(dp^2=+\theta^{02}\) e \(dp^3=+\theta^{03}\). As parcelas de d(pp) somam \(+4\theta^{0123}\); a parcela de dM vale \(T/2=-2\theta^{0123}\). Sua soma é +2. Em termos de m elevado, \(dm^{23}=-\theta^{23}\), conforme a fonte.

## 5. Realização por Killing e ordem correta das operações

Os quatro dados usados são: dois valores e0,e1 com derivada zero, e dois valores zero com derivadas J02,J03. Todos pertencem ao espaço dos dados admissíveis de Killing no ponto. A planura da conexão de transporte na curvatura constante realiza cada par por um Killing local com seus prolongamentos compatíveis. A afirmação usada é a de [Khavkine, arXiv:1805.03751v2, §3, (22–25) e parágrafo seguinte](https://arxiv.org/pdf/1805.03751v2), conferida nesta sessão. Ela justifica a realização local, não o cálculo algébrico do resíduo.

Esses quatro Killing não precisam gerar uma subálgebra de dimensão quatro: o comutador dos dois de isotropia produz a direção J23 ausente na lista. A fonte aplica dCE no complexo completo antes de substituir os dados. Isso é essencial.

Embora \(\beta_o\) se anule na restrição porque não há componente M23 inicial, \(d\beta_o\) não se anula. A restrição não foi apresentada como morfismo CE para um alvo com diferencial nulo. Não há contradição entre \(\operatorname{ev}\beta_o=0\) e (R4).

Os valores p ocupam somente duas direções, de modo que todo produto de três ou quatro p se anula. Isso não elimina \(\theta^{0123}\): os dois ghosts restantes vêm de M e sobrevivem no produto \(p^2M^2\).

## 6. Resíduo e não exatidão modulo s0

Na mesma solução TT, \(J(p_0)=-4k/z_0\). Os termos de (R3) com três ou quatro p são zero na nova avaliação. Não é preciso conhecer um gradiente de J para esse teste. Resta
\[
\operatorname{ev}_{\rm iso}(dQ+a)
=\frac{J}{24K}(-4\theta^{0123})
=-\frac{J}{6K}\theta^{0123}
=\frac{2k}{3Kz_0}\theta^{0123}.
\]
Em \(k=2/z_0\), \(K=z_0^{-2}\), obtém-se
\[
\boxed{\operatorname{ev}_{\rm iso}(dQ+a)=\tfrac43\theta^{0123}\ne0.}
\tag{R5}
\]
Conferi o sinal positivo e a ausência de um fator dois extra.

A não exatidão alegada é justificada pelas condições da avaliação: R0C e seus prolongamentos são zero porque os campos são Killing locais; H0h e seus prolongamentos são zero pela solução linear078 em uma vizinhança; antifields e seus jatos são postos em zero após aplicar s0. Assim essa avaliação anula s0 de qualquer expressão de jatos finitos.

As identidades CE082 e da corrente horizontal têm correções s0 explícitas no complexo original. Elas se anulam nessa avaliação. Se \(s_1Q+A_6=s_0F\), sua avaliação seria zero, contradizendo (R5). Uma troca \(Q\mapsto Q+s_0\chi\) acrescenta \(-s_0s_1\chi\) ao defeito e também não muda (R5).

Portanto essa classe de Q falha como cancelamento, mesmo passando no detector TT anterior para todos os modos. Isso não demonstra inexistência de outras classes Q, nem decide o grupo CE inteiro.

## 7. Alcance e custódia

[DERIVED] A engenharia de Q é zero porque \([J\beta_o]=[q_{\rm grad}]=2\) e [K]=2. No domínio com K real fixado, 1/K é uma constante permitida na extensão escalar real; não foi acrescentado um parâmetro dependente de k. Essa observação não resolve as condições de admissibilidade causal Q2 nem a regularidade num anel com K variável.

[OPEN] Outra combinação natural pode ter componentes adicionais de isotropia ou derivadas. A imagem CE completa, a pertinência de −[A6], os graus posteriores, outros fundos, QME e UV permanecem fora da conclusão.

[REAL — documental] Os pins da fonte, do manifesto, do helper de origem e dos antecedentes foram medidos antes/depois. O helper próprio desta revisão apenas compara bytes, hashes e destinos de links; não executa a matemática da origem. O recibo contabiliza somente verificações documentais. Os artefatos finais são publicados por temporário verificado e renomeação, e nenhum pin final aponta para um temporário renomeado. Todas as fontes congeladas permanecem intactas.
