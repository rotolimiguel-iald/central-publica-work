# Revisão independente da polarização BRST adaptada

10/09/2026, arco 073. [DERIVED — análise matemática própria, somente leitura das fontes]. Não é aprovação em nome do operador ou de outro agente; não houve Lean, CAS, execução de um.py ou edição da fonte examinada.

**Conclusão delimitada:** não identifiquei erro material na construção da nota `POLARIZACAO_BRST_HADAMARD_073_20260910/POLARIZACAO_ADAPTADA_E_MAJORANTE.md`, lida integralmente, incluindo a precisão de adjuntos de sua seção 2. O novo split conserva frequências módulo operadores suaves e o projetor final conserva-as no sentido Hadamard, além de entrelaçar exatamente o complexo. Isso paga o requisito que meu adendo de reparo havia mantido aberto para a covariância global, dentro das entradas geométricas e analíticas declaradas. A composição com campos Wick e com a carga interagente ainda exige seu próprio domínio e identidades.

## 1. Entradas efetivamente utilizadas

Li a fonte de polarização integral e confrontei suas identidades com `EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md`, particularmente §§3–6. A positividade e completude física são entradas escritas de 067, que a nota explicitamente preserva. Não refiz a redução ADM ou sua completude nesta revisão.

Consultei diretamente a fonte primária [Gérard–Murro–Wrochna, §5.2.10, Proposição 5.4 e Observação 5.5](https://link.springer.com/article/10.1007/s00023-025-01539-1). Ela fornece projeções exatas de soma um, autoadjuntas para a forma de Cauchy, com a orientação microlocal pertinente, e não pressupõe positividade nos fibrados indefinidos. Sua fórmula de grafos confirma que idempotência não está sendo importada de uma parametrix apenas assintótica. Os passos de adaptação BRST da nota são deduções próprias a partir desse dado.

O adjunto da fonte revisada é sesquilinear: H(u,v)=iΩ(jmath u,v). Nesse sentido Π±†=Π±. A transposição relativa à extensão bilinear de Ω troca os dois ramos. Para os mapas reais k,c,e as duas convenções coincidem; para os projetores complexos é necessário distingui-las. A precisão agora explícita remove a ambiguidade que haveria em escrever simplesmente H=iΩ.

## 2. Realidade, modos baixos e exatidão da inversa

A simetrização por transposição bilinear do fator de Riccati é admissível porque a equação i∂b−b²+A conserva essa transposição e o símbolo principal positivo. A unicidade módulo operadores suaves implica que b−bᵀ é suave; a média altera apenas esse resto. Uma correção real simétrica de baixas frequências preserva essa propriedade. A acretividade Hilbert de b implica a de τb*τ quando τ é uma involução unitária, de modo que a soma correspondente conserva o controle necessário à fórmula de grafos. Esse argumento fixa os dados iniciais e não altera o operador de onda.

Na seção 4, o defeito Ward é suave nas duas orientações e a matriz simplética local é invertível. Assim cΠ_D−Π_Qc é suave; tomar o adjunto e usar k†=ℓc fornece Π_Dk−kΠ_Q suave. Não se substitui essa prova pela igualdade de símbolos principais.

Para e_d=Σσ Π_Q^σ eΠ_D^σ, o entrelaçamento é exato antes da correção e e_dk−1 é suave. Portanto

\[
e_1=e_d+(1-e_dk)e,\qquad e_1k=e_dk+1-e_dk=1.
\]

O termo adicional é suave porque e tem ordem finita. Esse acerto não requer inverter um operador de Fredholm, remover modos baixos ou supor que a inversa original e preserve frequências. Os dois sinais são trocados simultaneamente pela conjugação, mantendo e₁ real.

## 3. Darboux e reconstrução física

O transporte das identidades de 068 para e₁ é puramente algébrico. Com k†k=0 e e₁k=1, a soma dos quatro termos de qq† é e₁e₁†−e₁e₁†/2−e₁e₁†/2+0. Dela seguem cr=1, qr=0 e o projetor simplético p. Como tomar adjuntos e multiplicar operadores de ordem finita preserva o ideal suave, os extratores q,r e p conservam os ramos módulo esse ideal.

O mapa s₀=sp só recebe soluções físicas: os dados de C U_Dpu são cp u=0, portanto essa solução Q é zero por unicidade. A redução 067 fornece o isomorfismo simplético pE→Z. Consequentemente s₀†s₀=p, e a sobrejetividade já fornecida pela reconstrução implica s₀s₀†=1. A definição R=s₀† é, assim, uma inversa demonstrada e preserva a classe pseudodiferencial de ordem finita. Não se está convertendo mera injetividade em sobrejetividade.

Esse trecho consome a completude de 067 em S³ no intervalo com Hubble não nulo. Ele não estabelece um novo resultado para fundos sem o extrator EK=1, nem uma carta probabilística global dos cinco pesos.

## 4. O elo Hadamard que o split arbitrário não pagava

O operador p de 068 podia misturar frequências. No novo split, [p,Π_D] é suave. Logo U_DpΠ_D=U_DΠ_Dp módulo uma evolução suave. Essa identidade justifica que a saída física continua no ramo escolhido antes de aplicar o extrator espacial S. Como os campos em questão satisfazem exatamente C=0 e a equação física, S os leva às equações reduzidas, preservando a orientação conforme o controle espacial de 067/068.

As covariâncias correspondentes a A_Z=s₀Π_DR têm a mesma CCR reduzida de 067. Os dois sinais de sua diferença são iguais, enquanto suas orientações são opostas. Portanto Π_Z−A_Z é suave, depois de usar a matriz simplética local invertível. Essa comparação não inverte uma covariância degenerada e não pressupõe que A_Z seja um projetor exato.

No projetor final

\[
\widehat\Pi_D=k\Pi_Qq+r\Pi_Qc+R\Pi_Zs_0,
\]

os produtos cruzados desaparecem pelo split. A autoadjunção troca os dois primeiros termos, com os fatores ℓ cancelados entre k†=ℓc e q†=r/ℓ. O terceiro termo é autoadjunto. A soma dos dois sinais é um, e cada sinal é idempotente.

Por outro lado, decompor 1=p+kq+rc antes de Π_D e usar os entrelaçamentos módulo suave dá

\[
\Pi_D\sim p\Pi_Dp+k\Pi_Qq+r\Pi_Qc.
\]

A comparação física anterior substitui o primeiro termo por RΠ_Zs₀ módulo suave. Portanto Πhat_D−Π_D é suave. **É esta identidade, e não somente a forma diagonal do bloco, que demonstra Hadamard do resultado final.** O raciocínio paga exatamente o contrato microlocal explicitado no meu adendo `REPARO_DO_BLOCO_E_LIMITE_HADAMARD.md`.

## 5. Radical e cohomologia depois do quociente

Pelas identidades do split, a covariância final tem blocos C=0 e D_c=0 na notação de minha nota de radical. Assim

\[
N_E=N_A\oplus kN_G\oplus rN_G,
\qquad cN_E=N_G,
\qquad p(N_E\cap\ker c)=N_A.
\]

Logo satisfaz S1 e S2 antes mesmo de usar uma identificação abstrata de Fock. Alternativamente, por ser obtida de um projetor autoadjunto para uma forma não degenerada, seu radical é exatamente o ramo complementar. A comutação exata da polarização com k e c faz desse radical um subcomplexo direto; quocientá-lo não cria as classes extras do contraexemplo finito.

Na imagem da polarização, a cohomologia é Z⁺: k envia F⁺ ao bloco gauge e c envia o bloco rF⁺ a F⁺. Os blocos auxiliares têm forma cruzada não degenerada; a restrição física é positiva. Esse argumento é compatível com a sequência exata da nota de radical e efetivamente escolhe uma extensão P₀ adequada em uma partícula. Não transforma toda extensão suave possível de 068 em uma escolha adequada.

## 6. Majorante e seus limites

Na energia H^{1/2}⊕H^{−1/2}, os projetores de ordens (0,−1;1,0) são limitados. Sua autoadjunção para a forma forte total torna a decomposição em imagem e kernel ortogonal para essa forma. A forma restrita à imagem é forte: estenda um funcional pela projeção, represente-o pela inversa total e projete o representante. Isso fornece existência e controle do representante restrito.

Conferi a fórmula P=Π(Π+Π*−1)⁻¹ para a projeção Hilbert ortogonal. Escrevendo A=Π+Π*−1, tem-se A²=1−(Π−Π*)²≥1 e AΠ*=ΠA; seguem autoadjunção, imagem correta e idempotência de P. Após reescalonamento da energia, os operadores são de ordem zero. O símbolo de G=PJ₀P+(1−P) é invertível em cada ramo, e G é um operador Hilbert autoadjunto invertível. Assim o cálculo funcional para sign(G) e |G|^{±1/2} é feito num espaço positivo com gap espectral demonstrado, não em uma pseudocovariância Krein arbitrária. A regularidade elíptica preserva C∞.

A norma do setor E é puxada pelo isomorfismo T(z,x,y)=Rz+kx+ry. A fonte não presume que todos esses mapas de ordem positiva sejam limitados no mesmo Sobolev D inicial; isso evita uma promoção indevida de continuidade. No núcleo suave, as operações de split e reconstrução têm perdas finitas e continuam definidas.

**Limites mantidos:** ainda é necessário mostrar a estabilidade do domínio Fock escolhido pelos operadores Wick e pelos coeficientes interagentes, e a implementação/simetria/nilpotência da carga pertinente. A topologia de uma partícula, por si, não representa funcionais microcausais não polinomiais arbitrários nem uma soma perturbativa convergente. Não se deduz QME, independência global de cutoff/fundo, positividade não perturbativa ou completude UV deste parecer.

## 7. Custódia e natureza da revisão

O manifesto acompanhante mede os arquivos lidos e este parecer mediante duas leituras estáveis. Não executei seus construtores, não alterei covariâncias em disco e não refiz testes Lean/CAS. O resultado é análise independente da prova escrita na classe e no fundo indicados; os contratos analíticos primários usados estão identificados acima.
