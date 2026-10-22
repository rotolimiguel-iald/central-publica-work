# Revisão independente de J1 e do detector covariante083

10/09/2026. Autoria desta revisão: finish_gibbs_realization. [DERIVED — revisão matemática escrita]. [REAL — leitura e medição documental no recibo]. Investigação083, excluída da entrega082. Zero reexecução matemática, CAS, Lean ou execução/importação de um.py nesta revisão.

**Conclusão.** Li integralmente a [nota083](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md>), o código e os dois registros JSON pertinentes. Não identifiquei erro material na identidade de onda, na normalização, na simetria helicoidal, no algoritmo covariante ou no detector, dentro da referência espaço-forma e da solução TT linear078 utilizadas. Em particular, o candidato \(\kappa^2J_1\beta\) tem resposta \(-7488\kappa^2/z_0^6\) em \(k=2/z_0\).

Esse valor impede estender a anulação do setor sem derivadas082 a todo o setor com jatos. Não prova que esse candidato, ou uma combinação ainda desconhecida, cancele −[A6]. O conteúdo abaixo é de minha análise; não atribuo a conclusão à aprovação de outra pessoa ou de outro agente.

## 1. Convenção e normalização efetivamente revisadas

A assinatura é \(+---\), z é espacial, \(a=\ell/z\), \(K=\ell^{-2}>0\), orientação \(d\tau\wedge dx\wedge dy\wedge dz\). A curvatura tem a convenção
\[
R^u{}_{bfa}=K(\delta^u_f g_{ba}-\delta^u_a g_{bf}).
\]
Assim \([\nabla_f,\nabla_a]\) atua com −R em cada índice covariante. Não se inferiu o sinal de \(\Box\) do nome usual dado ao espaço-forma.

O objeto W é a duas-forma de Weyl linear com valores em endomorfismos. A fonte define
\[
J=\operatorname{tr}(W\wedge W)/\operatorname{vol}_{g_0},\quad
J_1=g_0^{ef}\operatorname{tr}(\bar\nabla_eW\wedge\bar\nabla_fW)/
\operatorname{vol}_{g_0}.
\]
A derivada em J1 atua em todos os índices do tensor, inclusive os da duas-forma; não é apenas a derivada exterior interna.

Conferi o fator de Hodge. Escrever \(W^a{}_b=\frac12W^a{}_{bcd}dx^c\wedge dx^d\) dá um fator 1/4 no traço do produto exterior. A antissimetria dos índices internos introduz um sinal menos ao converter \(W^a{}_bW^b{}_a\) em uma contração com ambos os índices internos na mesma ordem. Em assinatura Lorentz, \(\varepsilon^{0123}=-1/\sqrt{|g_0|}\) introduz o sinal oposto na conversão para Hodge. O resultado é o da fonte:
\[
J=\tfrac12W_{abcd}(*W)^{abcd}.
\]
O mesmo fator vale para J1. A soma sobre seis duplas exteriores independentes no código já incorpora os fatores da forma diferencial; não se acrescenta outro 1/4 àquela soma. O controle 16EB é consistente com essas convenções.

## 2. Derivação independente de \(\Box W=6KW\)

Uso a dupla inicial do Weyl para conferir a fórmula da fonte, que usa a dupla final. Na solução Einstein linear sobre W0=0, as identidades de Bianchi e de divergência homogêneas dão
\[
\bar\nabla_eW_{abcd}+\bar\nabla_aW_{becd}
+\bar\nabla_bW_{eacd}=0,\qquad
\bar\nabla^eW_{eacd}=0.
\]
Aplicar \(\bar\nabla^e\), comutar as derivadas nos dois termos seguintes e zerar as divergências resulta em
\[
\bar\Box W_{abcd}
+[\bar\nabla^e,\bar\nabla_a]W_{becd}
+[\bar\nabla^e,\bar\nabla_b]W_{eacd}=0.
\tag{R1}
\]
Refiz a primeira contração em dimensão n. Os índices b,e produzem respectivamente \(+KW_{abcd}\) e \(-(n-1)KW_{abcd}\). Os índices c,d produzem
\[
K(W_{bcad}+W_{bdca})=-KW_{abcd}
\]
pela Bianchi algébrica; os traços de Weyl são zero. Portanto
\[
[\bar\nabla^e,\bar\nabla_a]W_{becd}
=-(n-1)KW_{abcd}.
\tag{R2}
\]
A segunda contração de (R1) tem o mesmo valor, trocando a,b e usando antissimetria. Em n=4, (R1) dá
\[
\boxed{\bar\Box W=6KW.}
\tag{R3}
\]
Essa conta concorda com as duas parcelas −3KW da equação (11) da fonte. A inferência da Bianchi homogênea está corretamente limitada ao shell linear: o Schouten do campo Einstein até primeira ordem é \(Kg/2\); sua Cotton é zero até essa ordem; W0=0 elimina os termos de variação da conexão multiplicando o Weyl de fundo.

Como g0, sua estrela e o volume são paralelos, Leibniz no traço exterior fornece
\[
\bar\Box J=2\operatorname{tr}((\bar\Box W)\wedge W)/
\operatorname{vol}_{g_0}+2J_1=12KJ+2J_1.
\]
Consequentemente \(J_1=\bar\Box J/2-6KJ\). Isso é uma identidade on-shell linear. O fechamento s0 de J1 e do candidato, por contraste, usa apenas W0=0, referência inerte e naturalidade, sendo off-shell. A nota mantém essa separação.

## 3. A simetria helicoidal vale na vizinhança inteira

O bloco TT é
\[
Q(\tau)=
\begin{pmatrix}\cos(k\tau)&\sin(k\tau)\\
\sin(k\tau)&-\cos(k\tau)\end{pmatrix}
=R(k\tau/2)Q(0)R(k\tau/2)^T.
\]
Para \(\alpha=k\epsilon/2\), a transformação
\((\tau,X,z)\mapsto(\tau+\epsilon,R(\alpha)X,z)\)
tem pullback no bloco espacial
\[
R(\alpha)^TQ(\tau+\epsilon)R(\alpha)=Q(\tau).
\]
Ela preserva g0, h e a orientação. Portanto qualquer pseudoscalar natural desses campos e de seus jatos, incluindo J e J1, é invariante pelo seu gerador helicoidal.

Os campos e seus jatos coordenados são independentes de x,y. Logo a parte rotacional do gerador anula J, e a invariância implica \(\partial_\tau J=0\) em toda a vizinhança. Segue também \(\partial_\tau^2J=0\); não se concluiu isso apenas do valor em \(\tau=0\). A solução radial é a mesma para k e −k porque sua EDO e os dados iniciais dependem de k².

Para F(z), a fórmula escalar é
\[
\bar\Box F=a^{-4}\partial_z(-a^2F')
=(z/\ell)^2(-F''+2F'/z).
\]
O termo de primeira derivada é exigido pelo volume conforme. Essa justificação paga o uso de \(\bar\Box J\) a partir da expressão radial de081 sem eliminar indevidamente uma derivada temporal.

## 4. Leitura estática do cálculo covariante direto

Li integralmente [compute_covariant_j1_new.py](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/compute_covariant_j1_new.py>). Não o executei nem importei. O corpo de cálculo usa polinômios de Laurent racionais em k,z,ℓ,f,p, com p=f′. A função de derivada total implementa
\[
D_z=\partial_z+p\partial_f+(2p/z-k^2f)\partial_p.
\]
ℓ e k ficam constantes em D_z. A substituição pontual da função data é aplicada somente depois das derivadas, zerando f, tomando p=1 e ℓ=z0. A função de avaliação em razão usa k=ratio/z0 depois disso. Não há derivada do valor já especializado.

O algoritmo constrói os componentes W de (18), incluindo a antissimetria das duas duplas. Os predicados de pares, Bianchi e traços verificam o tensor fornecido; não substituem a derivação escrita de que ele é o Weyl da TT. Essa é uma entrada proveniente de078/081, declarada na fonte.

A função gamma coincide com a conexão de \(a^2\eta\):
\[
\bar\Gamma^u{}_{be}
=-\frac{\delta^u_b\delta_{e3}+\delta^u_e\delta_{b3}
+\eta_{be}\delta^u_3}{z}.
\]
Em cada componente \(N_{e;abcd}=a^{-2}\bar\nabla_eW_{abcd}\), o laço:

- calcula a derivada radial ou temporal apropriada;
- acrescenta \(-2\widetilde W/z\) quando e=3, devido a \(W_{abcd}=a^2\widetilde W_{abcd}\);
- subtrai a conexão em cada um dos quatro índices a,b,c,d;
- conserva essas conexões também em e=1,2, embora as derivadas ordinárias x,y sejam zero.

A derivada temporal usa o gerador \(A_{\rm rot}=(k/2)\left(\begin{smallmatrix}0&-1\\1&0\end{smallmatrix}\right)\) em cada índice covariante, coerente com a rotação ativa dos valores de Q. O fato de J ser independente de τ não autoriza zerar \(\partial_\tau W\); o código não o zera.

O traço exterior levanta o primeiro índice interno de cada N por η, soma a troca dos índices internos e as duplas exteriores com o símbolo de orientação. O resultado é contraído por \(\eta^{ee}\) e multiplicado por \((z/\ell)^6\). Esse fator é correto: \(a^{-2}\) da contração das duas derivadas e \(a^{-4}\) do volume, após o cancelamento do peso \(a^2\) de W com seu levantamento interno.

A rota direta não usa a equação de onda no cálculo dos N. A rota de comparação usa \(J_1=\bar\Box J/2-6KJ\). Ambas compartilham o tensor W fornecido e a EDO radial; portanto o controle é independente entre essas duas contrações, não uma reconstrução independente de toda a solução Einstein. O recibo marca expressamente essa limitação.

## 5. Derivadas, perfil e valor exigido pelo teste

A expressão resultante é
\[
J_1=\ell^{-6}\left[
80kz^3p^2-100k^3z^4fp-28k^3z^5p^2
+20k^5z^5f^2+8k^5z^6fp\right].
\]
Conferi sua derivada no ponto usando f=0, p=1, p′=2/z0 somente depois de derivar. Os cinco termos contribuem respectivamente
\[
560k/z_0^4,\quad-100k^3/z_0^2,\quad
-252k^3/z_0^2,\quad0,\quad8k^5.
\]
Logo
\[
J_1(z_0)=80k/z_0^3-28k^3/z_0,\qquad
J_1'(z_0)=560k/z_0^4-352k^3/z_0^2+8k^5.
\]
Esses valores coincidem com a leitura do recibo.

O pseudoscalar completo \(\mathcal J_1(g)\) começa em ordem h² porque W0 e ∇W0 são zero. A naturalidade dá a identidade off-shell
\[
s_1J_1+s_0J_{1,3}=C^\mu\partial_\mu J_1.
\]
O coeficiente \(J_{1,3}\) tem ordem finita. Na avaliação078, os ghosts são Killing em uma vizinhança, anulando R0C e todos os seus jatos. Isso paga a retirada do termo s0; ele não foi omitido na identidade universal.

Com \(\beta=-6\theta^{012}/z_0\) e \(s_1\beta=-18\theta^{0123}/z_0^2\), a passagem de θ3 por três ghosts introduz o sinal menos. Assim
\[
\operatorname{ev}s_1(J_1\beta)
=\left(6J_1'/z_0-18J_1/z_0^2\right)\theta^{0123}.
\]
Refiz a combinação:
\[
\boxed{R_1(k)=48k^5/z_0-1608k^3/z_0^3+1920k/z_0^5.}
\]
Ela é ímpar em k; a metade da diferença das avaliações ±k conserva R1, sem fator dois adicional. Em k=2/z0,
\[
R_1(2/z_0)=(1536-12864+3840)/z_0^6
=-7488/z_0^6.
\]
O fator herdado κ² dá o valor declarado. Com κ real fixado não nulo e z0>0, ele é não zero.

## 6. Cohomologia, engenharia e limites

J1 possui duas pernas h e β três ghosts. O candidato tem E5, ghost3 e é s0-fechado off-shell. Na engenharia adotada, [J1]=6, [β]=−2 e [κ²]=−4, resultando em peso zero. Esse ajuste usa κ herdado, sem coeficiente dependente de k nem inverso de K.

O detector anula s0 em qualquer expressão finita pelos contratos078/079, inclusive primitivas antifield. Portanto a resposta não nula certifica a não trivialidade de \([s_1(\kappa^2J_1\beta)]\) no alvo utilizado. Isso consome a validade das EOM e dos Killing em toda a vizinhança, que não foi reexecutada aqui.

O setor sem derivadas082 tinha resposta \(A R(k)\), com \(R(k)=24k^3/z_0-96k/z_0^3\). Como R(2/z0)=0 e R1(2/z0)≠0, a nova resposta não pertence àquela linha. Já uma combinação \(A R+B R_1\), com coeficientes herdados independentes de k, não reproduz \(4k/z_0\) para todo k: o termo k5 força B=0, o termo k3 força A=0.

Essa última comparação só abrange os dois perfis indicados. Não classifica todos os candidatos com uma derivada, não exclui outros jatos e não estabelece igualdade de classes a partir de igualdade de detectores. Permanecem abertos −[A6] na imagem, a imagem CE completa e as restrições de admissibilidade causal. Não se conclui QME, teoria UV ou suficiência geral da gravidade quântica.

## 7. Controles e custódia

[REAL — leitura] O recibo da origem contém dez predicados algébricos com valor TRUE, além dos pins antes/depois das três fontes do cálculo e do próprio script. Não contei os controles de preservação como teoremas algébricos adicionais. Minha leitura estática e as contas escritas acima não são uma segunda execução desses dez predicados.

O novo helper desta pasta realiza apenas medições de bytes/SHA-256, comparações dos registros e verificação de links; publica este parecer e seu recibo por temporário verificado e renomeação. Os pins finais não apontam para temporários renomeados. A nota, o código e os manifestos da origem permanecem congelados. Todos os controles próprios contabilizados no recibo são documentais; não há CAS, Lean ou execução/importação de um.py.

Uma tentativa anterior de emitir este texto pela orquestração falhou por sintaxe JavaScript antes da execução das ferramentas. Nenhuma escrita ou execução matemática ocorreu nessa tentativa. A chamada corrigida criou o texto novo, sem alterar qualquer fonte anterior.
