# Resposta microscópica antes da fonte e fronteira gravitacional

9 de setembro de 2026. Esta nota registra a análise da tarefa principal sobre as fontes lidas e os resultados compilados nesta bancada. Originais e entregas anteriores permanecem somente leitura.

## O avanço efetivo

[REAL — Lean, alcance das folhas] Há uma construção explícita de probabilidades normalizadas e estritamente positivas, com resposta entrópica e modular coincidentes na ordem quadrática. Seus coeficientes determinam um registro gravitacional e seu tensor de matéria, sem receber esse tensor como argumento. A conservação é demonstrada quando os covetores do protocolo são fechados e satisfazem a equação de onda na métrica fornecida. A correspondência entre entropia e área continua uma hipótese física identificável.

O protocolo e a métrica são entradas da construção. O argumento não deriva a escolha do protocolo de um axioma de identidade, não identifica o parâmetro de preparação com o tempo modular ou afim por definição e não demonstra que um resultado experimental específico ocorreu.

## 1. Protocolo misto e energia do próprio estado

[DERIVED — realização matricial escrita] Num sítio não tracial, escolha a base de modo que

\[
\rho_0=\frac{e^{kZ}}{2\cosh k},\qquad k>0,\quad
W=X+Z,\qquad
\rho_s=\frac{e^{\log\rho_0+sW}}{\operatorname{Tr}e^{\log\rho_0+sW}}.
\]

As matrizes de Pauli satisfazem \(X^2=Z^2=I\) e \(XZ+ZX=0\). Portanto, para \(H_s=(k+s)Z+sX\), vale \(H_s^2=r(s)^2I\), onde \(r(s)=\sqrt{(k+s)^2+s^2}>0\). Separar as potências pares e ímpares da exponencial fornece

\[
\rho_s=\frac12\left(I+\frac{\tanh r(s)}{r(s)}H_s\right).
\]

Medir os projetores fixos \((I\pm Z)/2\) dá

\[
q_+(s)=\frac12\left[1+\frac{k+s}{r(s)}\tanh r(s)\right],\quad
q_-(s)=1-q_+(s),\quad q'_+(0)=\frac{1}{2\cosh^2k}.
\]

Essas fórmulas são as probabilidades reais formalizadas em `MixedQuadraticGibbsResponse`. A identidade com a exponencial matricial acima é uma derivação escrita; o recibo dessa folha não afirma que ela foi formalizada em Lean.

[INPUT — protocolo] Escolha a preparação quadrática \(s=v^2t^2\). [REAL — Lean] Os limites calculados são

\[
\lim_{t\to0^-}\frac{S(q(v^2t^2))-S(q(0))}{t^2}
=\lim_{t\to0^-}\frac{\Delta K(q(v^2t^2))}{t^2}
=-\frac{k}{\cosh^2k}\,v^2.
\]

Aqui \(\Delta K=\sum_i(q_i-p_i)(-\log p_i)\), com \(p=q(0)\). Como os projetores medidos diagonalizam \(\rho_0\), esse incremento é exatamente \(\operatorname{Tr}[(\rho_s-\rho_0)(-\log\rho_0)]\). O operador de energia de referência permanece o mesmo; não foi substituído pelo de uma medição inclinada.

A tangente temporal da distribuição em zero é nula. Sua informação de Fisher temporal também é nula, e \(D(q(t)\Vert p)/t^2\to0\). A igualdade \(\Delta S=\Delta K-D\) explica a coincidência dos dois limites. Ela não exige que \(\rho_s\) comute com \(\rho_0\); para \(k>0\), \([W,\log\rho_0]\ne0\).

No primeiro protocolo, com perturbação transversal \(sX\), medição X e preparação linear \(s=vt\), o resultado era diferente: a distribuição de referência era uniforme, \(\Delta K\equiv0\), e \(\Delta S/t^2\to-\chi(k)^2v^2/2\), com \(\chi(k)=\tanh|k|/|k|\) e extensão \(\chi(0)=1\). Essa resposta informacional permanece válida em `TransverseGibbsResponse`, mas não paga o calor modular intrínseco exigido pela ponte. O novo protocolo resolve essa diferença no alcance declarado.

## 2. Famílias finitas, fonte e conservação

Fixe finitos sítios independentes, parâmetros constantes \(k_j>0\) e covetores suaves \(w_j\). Em \((x,d)\), tome \(v_j=w_j(x)(d)\). A soma das respostas é

\[
Q_x(d)=-\sum_j\frac{k_j}{\cosh^2k_j}\,[w_j(x)(d)]^2.
\]

[REAL — Lean] A folha `MixedGibbsGravitationalBridge` prova o limite da soma das entropias e da soma dos incrementos modulares. [DERIVED — produto independente] Essa soma de entropias pode ser realizada como entropia de uma distribuição produto com \(2^{|J|}\) resultados: \(p(\mathbf i)=\prod_jp_j(i_j)\), \(q_t(\mathbf i)=\prod_jq_{j,t}(i_j)\). Normalização e \(\log\prod_jp_j=\sum_j\log p_j\) dão \(S(q_t)=\sum_jS(q_{j,t})\) e \(\Delta K_{\otimes p_j}=\sum_j\Delta K_{p_j}\). Uma mistura de ramos rotulados teria pesos adicionais; não é a construção usada aqui. O produto global e sua realização no fator não são contabilizados como teoremas novos de Lean neste lote.

A normalização por \(-\pi\), dez sondagens direcionais e a reversão de traço constroem

\[
c_j=\frac{k_j}{\pi\cosh^2k_j}>0,\qquad
T_{ab}=\sum_jc_j\left(w_{j,a}w_{j,b}
-\frac12g_{ab}g^{cd}w_{j,c}w_{j,d}\right).
\]

O tensor \(T\) é saída. A métrica lorentziana \(g\) é decodificada do registro métrico fornecido. Para \(d\) nulo,

\[
Q_x(d)=-\pi T_x(d,d),\qquad T_x(d,d)\ge0.
\]

[REAL — Lean] Se \(dw_j=0\) e \(\nabla^aw_{j,a}=0\) para cada setor, então \(\nabla^aT_{ab}=0\). As identidades de inversa, compatibilidade métrica e ausência de torção são pagas pela construção de Levi-Civita; não entram novamente como axiomas independentes. Os \(k_j\) são constantes no espaço-tempo: se forem campos variáveis, aparecem derivadas adicionais, que não estão cobertas por esse enunciado.

Esta classe de fontes satisfaz positividade nula. Não equivale à cobertura de todos os tensores assinados permitidos pelo decodificador geral. Também depende da disponibilidade dos sítios não traciais escolhidos; um perfil arbitrário não fornece automaticamente qualquer quantidade desses sítios. Reorientar a base trata um sítio com peso menor que metade, mas constitui uma escolha explícita de observável. O sítio tracial tem resposta quadrática nula nesse protocolo.

## 3. Onde a hipótese de área entra

Para toda direção nula não nula, a hipótese é

\[
\frac{\sum_j\Delta S_j(t)-\eta[A(t)-A(0)]}{t^2}\longrightarrow0,
\]

com \(A\) a área induzida da tela/congruência da métrica reconstruída. [REAL — Lean] A igualdade dos coeficientes permite transportar essa condição ao registro formal já existente, sem identificar o estado Gibbs com o estado calibrado ou com a preparação unificada. Sob abertura e preconexão do domínio, \(\eta\ne0\), as telas especificadas e as equações dos covetores, segue

\[
G_{ab}+\Lambda g_{ab}=\frac{2\pi}{\eta}T_{ab}.
\]

O seletor canônico conserva a leitura do registro. Para parâmetro de caracterização não nulo e domínio não vazio, sua reconstrução recupera os campos e transporta essa equação. Isso é suficiência matemática condicional, com fonte calculada antes de \(T\). A codificação por um real exato e sua reconstrução não fornecem, por si, precisão finita, estabilidade experimental ou escolha dinâmica do registro admissível.

## 4. Controle que impede apagar a condição de área

[DERIVED — controle escrito] Tome Minkowski \(g=\operatorname{diag}(1,-1,-1,-1)\), um parâmetro \(k>0\) constante e \(w=dx^0\). O covetor é fechado e satisfaz a equação de onda; a fonte é constante e conservada:

\[
T=\frac c2I,\qquad c=\frac{k}{\pi\cosh^2k}>0.
\]

Para \(d=(1,1,0,0)\), \(g(d,d)=0\), \(T(d,d)=c\) e a resposta entrópica é \(-\pi c\ne0\). Uma tela paralela tem área constante; consequentemente, o erro de área dividido por \(t^2\) tende a \(-\pi c\), e não a zero. O protocolo, a codificação e a conservação permanecem bem definidos, mas esse par \((g,T)\) não satisfaz a hipótese de área.

Não é uma refutação da lei de correspondência quando ela é postulada como condição de admissibilidade. É uma demonstração de sua independência em relação aos ingredientes já construídos. O kernel canônico já contém um controle análogo, com outra preparação, em `CoherentMatterControls.coherent_flat_area_not_matching`; esta nota aplica o mesmo argumento ao novo coeficiente Gibbs e distingue os dois estatutos.

## 5. Dinâmica extensiva e alcance quântico

[REAL — Lean] `FiniteCommutatorEvolution` identifica a série de comutadores com a evolução finita real \(e^{itH_N}Ae^{-itH_N}\). `SmallTimeLocalDynamics` demonstra que esses operadores convergem em norma para observáveis locais quando \(2J|t|<1\), usando estabilização das parcelas e um majorante somável. Não assume o limite como hipótese e não exige \(\sum_j\|V_j\|<\infty\). A convergência Lean deste lote é pontual no tempo.

[DERIVED + KNOWN — prova escrita revisada nesta tarefa] A demonstração em `DINAMICA_EXTENSIVA_DEMONSTRACAO_20260909_1813` estende o resultado à álgebra C* quase local, a todo tempo, uniformemente em compactos, incluindo o fundo modular sem norma uniforme dos geradores de sítio. A passagem ao quadro de interação mantém suporte e norma; a globalização usa isometria e compactos de entradas. A construção de estados KMS usa Gibbs finitos e regularização gaussiana, com convenção de sinal explícita. A aplicação do resultado de Nachtergaele–Sims foi conferida com \(F(r)=(1+r)^{-2}\) e norma de interação no máximo \(4J\). [Artigo primário](https://arxiv.org/abs/1410.8174).

A análise direta da tarefa principal verificou o fator combinatório, a ordem dos comutadores no argumento de Volterra, a globalização com entradas móveis, a passagem KMS e a obstrução de normalidade. Trata-se de análise de uma prova escrita, não de sua transformação em recibo Lean.

[DERIVED — obstrução] Para um perfil produto não tracial constante, médias macroscópicas de Z convergem fortemente a \(mI\), \(m\ne0\). A dinâmica admissível de rotações X troca Z por −Z em um tempo fixo. Uma extensão normal ao fator original preservaria o limite escalar, mas a dinâmica o troca por \(-mI\). Portanto, extensão normal universal nesse fator é falsa sob o contrato atual. O estado KMS pode fornecer sua própria representação normal; identificar essa representação com a original exige uma condição adicional.

Uma cadeia quântica extensiva bem definida não constitui ainda uma teoria quântica interagente do espaço-tempo reconstruído. A origem da rede física, o limite contínuo/UV, o tratamento geral das perturbações, as anomalias e as identificações geométricas não decorrem das estimativas de localidade.

## 6. Obrigações que restam

1. [INPUT/OPEN] Fixar ou derivar uma lei física que determine a métrica, os covetores, a escolha de preparação/relógio e a correspondência de área a partir dos dados TGL admissíveis. Se postulada, a suficiência deve citar precisamente esse postulado.
2. [OPEN] Relacionar o registro selecionado às informações efetivamente disponíveis e à reconstrução com precisão controlada. A reconstrução exata e a distinção por fase já demonstradas permanecem válidas em seus domínios; não se reabre sua prova algébrica.
3. [OPEN] Estender a classe quântica interagente ao alcance físico desejado: setores de matéria necessários, perturbações gerais, representação pertinente, anomalias e rota contínua/UV. A parte de existência da dinâmica extensiva no fecho C* tem agora prova escrita, e seu limite local tem nova formalização.

Os critérios falsificadores existentes no `um.py` são relevantes e devem ser preservados. A ausência de uma refutação nos testes executados não preenche automaticamente as hipóteses matemáticas acima, nem autoriza dizer que todos os dados possíveis ou existentes foram confrontados. O reexame distingue suficiência dentro do modelo, execução dos testes e confirmação física.
