# Defeito do CCR, transporte e Ward estendida em referência fixa

10/09/2026, arco072. [DERIVED — demonstrações escritas; KNOWN/INPUT — entradas explícitas]. Somente novos arquivos Chatgpt; zero CAS/Lean e nenhuma execução/importação de um.py.

## 1. Resultado e entradas

Demonstramos a falha da derivação ingênua de kernels variáveis, seu controle no CCR, um reparo simplético de primeira ordem e uma Ward anômala estendida em referência fixa. A última construção mantém B0 nos coeficientes e não prova exatidão/QME.

O contrato está em [Admissibilidade Q2](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md>). A ação clássica estendida é entrada da [Retração relativa072, §6](<C:/IALD/Central de Patentes/Chatgpt/RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md>). Dicionário e Q2_069 fornecem o diferencial livre nilpotente, os Green, contatos e a Ward anômala original. Nada abaixo modifica essas fontes.

## 2. Convenções

Basta o bloco bosônico para demonstrar a obstrução. Tome P_ε formalmente autoadjunto e Green-hiperbólico, com P₀=P e δP compacto nos coeficientes. Identifique antes os fibrados/densidades em um par dual de referência fixo. Para mapas próximos, pode-se usar transporte paralelo alvo entre pullbacks; os fatores de volume e forma de fibra da Hessiana são também transportados. Não se varia a métrica mantendo uma adjunção incompatível. Multiplicar a Hessiana por uma forma de fibra para normalizar a onda não permite descartá-la nos Green.

Escreva Gʳ,Gᵃ para Green retardado/avançado, (Gʳ)*=Gᵃ e E=Gʳ−Gᵃ. Para funcionais regulares e H−Hᵀ=iE, use

\[
F\star_B G=\mu\exp(\hbar\Gamma_{H_B})(F\otimes G).
\tag{1}
\]

Γ_H contrai uma derivada funcional de cada fator e μ os multiplica. Esta convenção põe i na parte antissimétrica de H. O argumento não depende de chamá-lo iG⁺ ou função de dois pontos.

## 3. Defeito de Leibniz e controle linear

Os operadores Γ com kernels independentes dos campos comutam. Derivar a série (1), mantendo coordenadas funcionais fixas, dá exatamente

\[
\boxed{\delta(F\star_B G)-(\delta F)\star_B G-F\star_B(\delta G)
=\hbar\mu\exp(\hbar\Gamma_{H_B})\Gamma_{\delta H_B}(F\otimes G).}
\tag{2}
\]

Os termos em que δ atua nos próprios funcionais já foram subtraídos. Para F_f(ϕ)=〈f,ϕ〉 e F_g lineares com testes fixos,

\[
[F_f,F_g]_{\star_B}=i\hbar E_B(f,g)\,1.
\tag{3}
\]

Uma derivação que anule F_f,F_g anularia o lado esquerdo. A derivada real do direito é iħδE_B(f,g). Logo, sempre que δE_B≠0, a derivada ingênua não é uma derivação dessa família identificada. Direções de simetria podem ter δE=0; não se afirma o contrário.

Uma troca de ordenação α_w=exp((ħ/2)Γ_w^diag), w=wᵀ, fixa os funcionais lineares e muda só a contração simétrica. Não altera (3), portanto não corrige δE≠0. Isso independe de positividade/cohomologia. O defeito (2) pode conectar pontos separados: antes de reparar a derivação, não é automaticamente uma quebra local diagonal da classe Q2.

### Controle concreto

Considere só como controle hiperbólico P=∂_t²−Δ_S³+m² em ℝ×S³, m>0, δP=χ(t), χ≥0 suave, compacta e não nula. No modo espacial constante,

\[
G^r(t,s)=\theta(t-s)\frac{\sin(m(t-s))}{m}.
\]

Para t>s e suppχ⊂(s,t),

\[
\delta E(t,s)=-\int_s^t
\frac{\sin(m(t-u))}{m}\chi(u)\frac{\sin(m(u-s))}{m}\,du.
\tag{4}
\]

Se 0<t−s<π/m, o resultado é estritamente negativo. Testes suaves próximos desses tempos conservam um pareamento não nulo. É um exemplo quadridimensional de variação do CCR, não um cálculo de anomalia física do Einstein–sigma.

## 4. Reparo por transporte retardado

Diferenciar P_εG_ε^{r/a}=1 e usar a condição de suporte do Green dá

\[
\delta G^{r/a}=-G^{r/a}\delta P G^{r/a}.
\tag{5}
\]

Consequentemente,

\[
\boxed{\delta E=-G^r\delta P G^r+G^a\delta P G^a
                  =-G^r\delta P E-E\delta P G^a.}
\tag{6}
\]

Na segunda igualdade os termos mistos cancelam. Perturbação compacta e suportes causais dão sentido aos produtos sobre testes. A (4) é a restrição da (6) ao modo constante.

Defina

\[
r_\varepsilon=1-\varepsilon G^r\delta P+O(\varepsilon^2).
\tag{7}
\]

Então (P+εδP)r_εu=Pu+O(ε²); soluções antigas vão a soluções novas e coincidem no passado da perturbação. Pela adjunção fixa,

\[
\boxed{r_\varepsilon E r_\varepsilon^*
=E-\varepsilon(G^r\delta P E+E\delta P G^a)+O(\varepsilon^2)
=E_\varepsilon+O(\varepsilon^2).}
\tag{8}
\]

O pullback do novo observável linear é F_f↦F_{r_ε*f}; (8) verifica seu novo CCR. É um certificado simplético infinitesimal, sem afirmar convergência ou transporte físico em todas as ordens.

Coloque A=−GʳδP. Após esse transporte, o defeito do kernel fica

\[
w=\delta H-AH-HA^*
 =\delta H+G^r\delta P H+H\delta P G^a.
\tag{9}
\]

As equações H−Hᵀ=iE e (6) dão w−wᵀ=0. Se os kernels Hadamard forem escolhidos compatíveis com o transporte, a diferença no mesmo operador é suave, e w é uma troca suave e simétrica de Wick. A simetria foi provada algebricamente; a suavidade exige essa comparação Hadamard, não decorre da simetria.

r*f=f−εδP Gᵃf pode ganhar suporte em suppδP∩J⁻(suppf), fora do suporte original. Logo o transporte não é uma derivação local que preserve estritamente o suporte de cada inserção. Não o inserimos diretamente nessa hipótese de um teorema de Ward. Tampouco (8) fixa a extensão de T_n às diagonais.

## 5. O que ainda exige acordo perturbativo

[KNOWN] A equação76 de Taslimi Tehrani–Zahn relaciona a derivada transportada de produtos, a variação das inserções e uma inserção retardada de δS₀, incluindo contatos. Sua conexão física usa também a condição de gauge da equação95; a seção4 deixa uma obrigação específica para gravidade. [Fonte primária, 1804.07640v3](https://arxiv.org/pdf/1804.07640).

[OPEN] Para o multiplet atual, precisam ser normalizados conjuntamente os termos quadráticos, ghosts/não mínimo, antifields, sigma e as inserções marcadas, nas cotas de Q2. Só então se compara a teoria com P_B livre àquela que trata P_B−P_B0 como interação. (8) não prova nem refuta essa normalização: evita saltá-la.

## 6. Construção em uma álgebra de referência fixa

Fixe B0=(ḡ0,φ̄0) on-shell, A0,B0, T0 da Q2_069 e seu diferencial ŝ₀ nilpotente, derivação graduada. Os kernels livres são os de B0.

Adicione fontes externas θ de ghost zero e ω de ghost um/paridade ímpar, com seus jatos. Use B_g=ḡ0+θ_g e B_φ=Exp_φ̄0(θ_φ), θ_φ∈Γ(φ̄0*TS³), formalmente perto da seção zero. Defina

\[
d_\theta\theta=\omega,\quad d_\theta\omega=0,\qquad
D_0=\widehat s_0+d_\theta.
\tag{10}
\]

No mapa original Ω_φ=d_θExp_φ̄0(θ_φ): o diferencial de Exp não é omitido. A apresentação é global no fibrado da referência e formal nas diferenças; o prolongamento aos jatos é evolutivo. θ,ω são centrais no sentido graduado, sem propagadores, e ŝ₀ os anula.

Se R é a álgebra formal dos jatos dessas fontes, A0,B0⊗R possui

\[
D_0^2=0,\qquad
D_0(F\star_0G)=D_0F\star_0G+(-1)^{|F|}F\star_0D_0G.
\tag{11}
\]

H_B0 não depende de θ, portanto não aparece (2). D₀ preserva suporte local das inserções. Trata-se de uma construção em esquema fixo, sem identificar d_θ com a derivada dos kernels de T_B.

### Produtos e identidade exata dos espectadores

Expanda cada inserção em coeficientes a_i(θ,ω,jatos) multiplicando operadores locais originais. Defina distribucionalmente

\[
T_n^{\rm ref}(a_1(x_1)O_1(x_1),\ldots,a_n(x_n)O_n(x_n))
=a_1(x_1)\cdots a_n(x_n)T_{0,n}(O_1(x_1),\ldots,O_n(x_n)),
\tag{12}
\]

com sinais de Koszul. Coeficientes suaves multiplicam distribuições renormalizadas. Quando se muda a representação por ação por partes, as derivadas dos a_i entram por Leibniz; não são tratados como constantes. A definição é compatível porque T0 satisfaz a mesma identidade.

A regra, aplicada a todas as inserções, preserva fatorização, graduação, realidade, suporte/regularidade e cotas quando se contabilizam os pesos externos. Não acrescenta linhas internas ou extensões singulares. A derivação das fontes obedece exatamente

\[
d_\theta T_n^{\rm ref}(F_1,\ldots,F_n)
=\sum_i(-1)^{|F_1|+\cdots+|F_{i-1}|}
T_n^{\rm ref}(F_1,\ldots,d_\theta F_i,\ldots,F_n).
\tag{13}
\]

Logo d_θ sozinho não tem anomalia. Isso não anula a anomalia das interações com inserções Ω.

## 7. Domínio BV, ação e filtração

As inserções contêm campos originais e seus antifields, mais θ,ω, mas são independentes dos conjugados θ*,ω*. ( , )_dyn é o antibracket dos campos originais/antifields, com coeficientes externos espectadores.

Essa restrição é essencial: fontes centrais sem Green não produzem automaticamente, por contrações, o antibracket de inserções arbitrárias com θ*. O mecanismo dinâmico usa EOM e contatos. Inserções dos conjugados de fundo exigiriam um dicionário quântico adicional, fora deste enunciado.

A ação da retração072 tem a forma ⟨θ*,ω⟩+Σ, com Σ independente desses conjugados. A férmion Ψ(fields,B), sem antifields, desloca θ* e acrescenta a Σ o termo de fonte proporcional a ωδ_θΨ. Não muda seu coeficiente ω nem gera dependência não linear em θ*,ω*. Separando novamente ⟨θ*,ω⟩, a CME implica

\[
d_\theta\Sigma+\tfrac12(\Sigma,\Sigma)_{\rm dyn}=0.
\tag{14}
\]

Os sinais são os da conjugação da nota072/dicionário069; o termo de fonte de gauge é conservado.

Escreva os campos completos em coordenadas de flutuação de B0 e separe Σ=Σ0,B0+V_ext. Todas as diferenças de gauge/cinética/fontes ficam em V_ext. A parte livre continua a mesma ação on-shell; termos constantes, lineares e quadráticos que surjam na reorganização não são apagados nem exigem uma CME quadrática off-shell.

Precisão de finitude: sob a organização t⁻², podem existir tadpoles t⁻¹θ (ou termos de grau externo maior). A grau externo total k fixo, contando θ,ω, no máximo k vértices assim podem entrar. Alterações quadráticas têm também grau externo positivo, logo seu número é limitado por k. Os vértices originais não quadráticos têm peso t^(n−2)≥1. Fixar o grau final em t, o grau externo, laços e truncagem limita os vértices positivos depois de contabilizar os negativos.

Assim, após fatorar os termos puramente centrais das matrizes relativas normalizadas, usa-se uma série Laurent em t com parte negativa finita a cada k (os tadpoles contribuem no mínimo −k), ou filtração combinada equivalente. Não se afirmou série só de potências não negativas em t. Termos de zero pernas t⁻², se presentes na reorganização, são centrais; mesmo antes de fatorá-los sua contribuição é finita a grau externo fixo, podendo exigir a cota −2k em vez de −k. A normalização relativa não apaga tadpoles que dependem dos campos.

Como d_θΣ0,B0=0, a equação (14) torna-se

\[
\mathcal M(V_{\rm ext})
:=s_0V_{\rm ext}+d_\theta V_{\rm ext}
 +\tfrac12(V_{\rm ext},V_{\rm ext})_{\rm dyn}=0.
\tag{15}
\]

s₀ é o operador clássico nas inserções, distinto da derivação ŝ₀ na álgebra. A igualdade local testada vale onde os cutoffs são constantes; a identidade completa conserva os termos df.

## 8. Ward anômala estendida e consistência

[KNOWN/INPUT] Usamos a Ward Q2_069, decorrente dos Teoremas3,6,7/equação154 de Fröb, com seu antibracket dinâmico e contatos. Suas hipóteses de derivação/localidade foram preservadas por (11). [Fonte primária, 1803.10235v3](https://arxiv.org/pdf/1803.10235).

A demonstração da extensão é direta: aplique a Ward original coeficiente a coeficiente aos funcionais de (12) e some (13). Para F par, ghost zero, compacto,

\[
\boxed{
D_0T^{\rm ref}(e_\otimes^{iF/\hbar})
=\frac{i}{\hbar}T^{\rm ref}
\left([\mathcal M(F)+\mathcal A^{\rm ref}(e_\otimes^F)]
       \otimes e_\otimes^{iF/\hbar}\right).}
\tag{16}
\]

A_ref é a extensão dos mapas locais originais aos coeficientes externos, incluindo suas derivadas quando aparecem nesses mapas. Não é declarada zero. d_θF vem de (13), sem pressupor Ward dos kernels variáveis. Diferenciar (16) em parâmetros de inserções dá as identidades polarizadas, com sinais graduados; não se provou apenas um vértice isolado.

A_ref começa em ħ, tem ghost um e jatos finitos por coeficiente na categoria de referência. Sua localidade também resulta da recorrência: D₀ é derivação, portanto o defeito na aridade nova cancela nos abertos de fatorização causal depois de subtrair as ordens inferiores; resta diagonal total. É precisamente a etapa que (2) impediria no procedimento ingênuo.

Com F=V_ext e cutoffs constantes, M=0. Está assim construído

\[
a_{\rm ext}^{\rm ref}=\mathcal A^{\rm ref}(e_\otimes^{V_{\rm ext}}).
\tag{17}
\]

Ele pode conter fontes Ω pelas inserções de V_ext, embora d_θ sozinho não tenha anomalia. A construção não pressupõe sua primitiva.

Defina nas inserções o diferencial clássico completo

\[
s_{\rm ext}^{\rm cl}=s_0+d_\theta+(V_{\rm ext},\cdot)_{\rm dyn}.
\tag{18}
\]

Leibniz graduada do antibracket e Jacobi dão (s_ext^cl)²=(M(V_ext),·)_dyn=0 na região de (15). Aplicar D₀ novamente a (16) dá a identidade de consistência original com d_θ sobre os coeficientes: (13) prolonga por Leibniz cada operação de inserção, os termos clássicos se juntam em M, e os demais são inserções de anomalia em anomalia.

Se as ordens inferiores foram removidas nesse esquema e a primeira quebra é ħ^N a_N^ref, os termos com duas anomalias começam em ordem superior. Portanto

\[
\boxed{s_{\rm ext}^{\rm cl}a_N^{\rm ref}+d_H b_N^{\rm ref}=0.}
\tag{19}
\]

Não se infere exatidão de (19), nem se transfere a conclusão à derivada ingênua de kernels variáveis.

Na avaliação θ=ω=0, incluindo jatos, T_ref reduz a T0 e a ação à da referência; d_θ tem fator ω e some. A (16) recupera a Ward original em B0. Esse é o levantamento efetivamente demonstrado: fontes formais na mesma álgebra. Não se identificaram todos os T_B de outra família independente.

## 9. B0 continua presente após a retração

A retração072 põe B=campos completos e Ω=s(campos completos), depois de desfazer o gauge por conjugação, e fornece a fórmula de transporte de primitivas quando elas existem na classe correta. Ela age nos doublets adicionados.

Ela não age na referência B0 dos kernels/normalização T0. Coeficientes locais de a_ext^ref podem conservar curvaturas de ḡ0, jatos de φ̄0 e os tensores permitidos nessa referência. A projeção gera, portanto, um cociclo no complexo com esses espectadores; H¹,⁴ de uma classe apenas dos campos completos não se aplica por identificação nominal.

[OPEN] É necessária uma primitiva admissível na categoria com B0 ou uma prova de levantamento natural/independência que remova a referência. Para comparar diretamente diferentes T_B, também continua necessário o acordo perturbativo com contatos e compatibilidade de gauge. O(4) diagonal transporta B0; não elimina sua dependência.

## 10. Estatuto

[DERIVED] As equações (2), (6), (8)–(13) e (16)–(19) dão o defeito, o reparo do CCR e a Ward anômala em referência fixa. A (14) consome a CME clássica072 no domínio explicitado. Entradas analíticas Q2 permanecem importações delimitadas.

[OPEN] Não foram demonstrados acordo perturbativo completo do multiplet, remoção admissível da anomalia, QME causal, independência física completa de fundo, estado interagente positivo ou fechamento UV. A falha da derivação ingênua é um controle de uma tentativa específica, não prova de anomalia não removível.
