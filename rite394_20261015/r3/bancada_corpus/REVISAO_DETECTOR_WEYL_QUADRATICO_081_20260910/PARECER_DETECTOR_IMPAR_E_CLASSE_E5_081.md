# Parecer independente081: candidato quadrático Weyl e detector ímpar

10/09/2026. Revisor: /root/prepare_integration_83. [DERIVED — revisão matemática escrita]. [REAL — leitura e custódia medidas]. Nenhum código matemático do autor, finalizador, Lean ou um.py foi executado/importado nesta revisão.

**Parecer favorável no alcance delimitado. Não identifiquei erro matemático material.** Li integralmente a [nota FINAL](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md>), o script de cálculo, o recibo e o manifesto. O arquivo .pending foi tratado somente como antecedente histórico de custódia, sem substituir a nota final.

O candidato b5=κJβ é natural, de ghost3/E5, universalmente s0-fechado na referência fixada. A conta fornece

\[
L_k(s_1b_5)=\kappa(24k^3/z_0-96k/z_0^3).
\tag{R1}
\]

A imagem não nula demonstra δ(K)≠0 nessa categoria. Não demonstra que −[A6] pertença a essa imagem. A nota preserva corretamente essa distinção.

**Precisões documentais.** O [recibo](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTROLES_DETECTOR_WEYL_QUADRATICO_081.json>) tem 14 condições TRUE: 13 são algébricas e a última, all_sources_unchanged, é documental. Além disso, o próprio script tem um pin somente no FIM da execução matemática, sem script_before. Não se pode declarar sua identidade antes/depois dessa execução. Os cinco inputs possuem ambas as medições; o finalizador e esta revisão têm janelas posteriores próprias. Essas precisões não mudam a matemática nem os arquivos congelados.

## 1. Tipo, paridades e fechamento

W[1] é a variação de Weyl, como duas-forma End(TM), no espaço-forma com W(g0)=0. A identidade W[1][Lie_Cg0]=0 vale para ghosts arbitrários. Logo s0W[1]=0 e todos os seus jatos de fundo também são fechados. Como s0C=s0m=0, segue s0(κJβ)=0 antes de usar EOM.

J é definido por tr(W[1]∧W[1])=J vol_g0; é real e quadrático em h. β=ε_abcd C^aC^b m^cd/2 usa a mesma orientação. Em Grassmann, J é par, β é ímpar de ghost3 e b5 é ímpar. Ao inverter a orientação espaço-temporal, J e β trocam de sinal e Jβ conserva o sinal. Isso não se confunde com a comparação dinâmica k↦−k do detector.

A valência é 2+3=5. Na convenção [C]=−1, [∇]=1, [h]=0, [κ]=−2, temos [J]=4, [β]=−2 e [κJβ]=0. κ é herdado e fixado, não uma função de k escolhida para ajustar o teste. Essa conta não paga automaticamente scaling degree ou contatos de todas as normalizações Q2.

## 2. Killing, m e o sinal CE de β

Os campos ∂τ,∂x,∂y,D/z0 são Killing genuínos de g0=(ℓ/z)²η em uma vizinhança; z é espacial. Em p0=(0,0,0,z0), com ℓ=z0, a base coordenada é ortonormal e C(p0)=θ. A conexão conforme e a derivada da dilatação dão

\[
A^a{}_b=\bar\nabla_bC^a
=-(\delta_{b3}\theta^a+\delta^a_3\theta_b)/z_0.
\]

Conferi A_ab=−m_ab; levantar os dois índices dá m^i3=−θi/z0 e m^3i=+θi/z0 para i=0,1,2. A contração epsilon fornece β=−6θ012/z0: o 1/2 cancela as duas posições de i3, preservando as seis permutações dos outros índices.

Os Killing fecham a subálgebra com [v_i,v_3]=v_i/z0. Com sc=C·∂C, a substituição é compatível com

\[
d_\theta\theta^i=\theta^i\theta^3/z_0,\qquad
d_\theta\theta^3=0.
\]

Ela vale para a mesma combinação de campos e TODOS os seus jatos. Cada um dos três termos de dθ(θ012) tem sinal positivo, logo

\[
\operatorname{ev}(s_1\beta)=-18\theta^{0123}/z_0^2.
\tag{R2}
\]

Não se deriva em z o coeficiente −6/z0 nessa conta: é um coeficiente da referência/avaliação fixa, inerte sob s1. A variação dos jatos de C já é reproduzida pela subálgebra de Killing. Não é necessário impor dCEβ=0 para ter um ciclo de C5.

## 3. Curvatura e derivada do pseudoscalar

Conferi à mão a fórmula ao longo de τ=x=y=0 na família TT078:
γ11=f cos(kτ), γ22=−γ11, γ12=f sin(kτ),
f''−2f'/z+k²f=0.

As componentes planas R[1]0i0j=k²f Qij/2 e R[1]3i3j=−f''Qij/2, com Ric[1]ij=f'Qij/z, deixam o setor elétrico E=(k²f−f'/z)/2. As componentes mistas dão B=kf'/2 nas formas da equação15 da fonte. A contração de traço em assinatura(+---) tem fator −2ηaaηbb e resulta em 16EB dτ dx dy dz.

O Weyl de tipo(1,3) é conformemente invariante; a forma volume que define J continua sendo vol_g0=(ℓ/z)^4 dτ dx dy dz. Portanto

\[
J(z)=4k\ell^{-4}\left[k^2z^4 f f'-z^3(f')^2\right].
\tag{R3}
\]

Recalculei por diferenciação escrita, a ℓ e k FIXOS:

\[
J'(z)=4k\ell^{-4}
\left[k^2(4z^3ff'+z^4((f')^2+ff''))
-3z^2(f')^2-2z^3f'f''\right].
\]

Só depois usei f(z0)=0, f'(z0)=1, f''(z0)=2/z0 e ℓ=z0. Assim

\[
J(z_0)=-4k/z_0,\qquad J'(z_0)=4k^3-28k/z_0^2.
\tag{R4}
\]

O fator conforme contribui à derivada embora valha um no ponto. Derivar somente −4k/z0 não daria a derivada da função geométrica com dados iniciais fixados. O script RECEBE as fórmulas E,B e W_ab; não calcula Christoffel/Riemann/Ricci a partir da métrica. Essa parte é prova escrita, conferida separadamente, não 14 verificações completas da geometria.

## 4. A ponte BRST/Lie conserva o resto s0

A equação18a resolve a obrigação de passagem à derivada de Lie. Para o pseudoscalar da métrica ativa,

\[
\mathcal J(g_0+th)=t^2J+t^3J_3+\cdots,\qquad
s\mathcal J=tC\cdot\partial\mathcal J,
\]

porque W(g0)=0 e a definição completa usa vol_g. Comparar a terceira ordem dá

\[
s_1J-C\cdot\partial J=-s_0J_3.
\tag{R5}
\]

J3 é natural, cúbico e finito em jatos, obtido junto a uma métrica não degenerada. Não exige convergência em t numérico. Seu s0 contém R0C e seus prolongamentos; na avaliação por Killing genuínos todos são zero.

Como s0β=0, multiplicar(R5) por β preserva a igualdade modulo uma fronteira s0. A fonte não elimina esse resto na álgebra off-shell. Também não precisa supor que J seja independente de τ: após multiplicar por β(p0)∝θ012, os termos μ=0,1,2 de C^μ∂μJ se anulam por repetição de ghosts.

## 5. Detector e conclusão cohomológica

O sinal decisivo é θ3θ012=−θ0123. Como β tem coeficiente negativo, o primeiro termo de s1(Jβ) contribui +6J'/z0; o segundo, −18J/z0². Substituir(R4) fornece

\[
\frac6{z_0}(4k^3-28k/z_0^2)
-\frac{18}{z_0^2}(-4k/z_0)
=24k^3/z_0-96k/z_0^3.
\]

O coeficiente é ímpar em k. A metade da diferença entre k e −k o preserva sem fator adicional. Em k=1/z0, o valor é −72κ/z0⁴, não nulo para κ≠0.

A avaliação anula s0 de toda expressão finita: a família resolve H0h=0 em uma vizinhança, os ghosts são Killing em uma vizinhança e os antifields são postos em zero APÓS aplicar o diferencial. Isso anula todos os prolongamentos de H0h, R0C e R0†h*, não apenas uma lista finita de valores testados por CAS. Lk é um funcional linear sobre H⁴(s0), sem ser tomado por homomorfismo de álgebras.

Como b5 é s0-fechado, s1b5 é um ciclo de E6. O valor não nulo implica [s1b5]≠0. Em C5, b5 é ciclo e sua restrição a C3 é zero. A conexão da sequência C6→C5 leva [b5] a [s1b5]. Portanto δ(K)≠0 é legítimo; não se deduz apenas da não nulidade de um polinômio.

Isso NÃO identifica a classe com −[A6]. O detector de A6 é linear em k, enquanto(R1) contém k³. Um único múltiplo escalar herdado do candidato não iguala o valor requerido para todos os k: o coeficiente cúbico o forçaria a zero. Coincidência num k isolado tampouco seria igualdade cohomológica. Outros candidatos e compensações permanecem abertos.

## 6. Script, recibo e custódia: limites efetivamente verificados

Li integralmente o [script](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/compute_odd_weyl081.py>), sem o executar.

Ele usa Fraction em polinômios de Laurent nas variáveis(k,z,ell,f,p,q), com p=f', q=f''. A derivada total é ∂z+p∂f+q∂p, suficiente para J porque ele não depende de q antes de derivar. A especialização f=0,p=1,q=2/z,ell=z ocorre depois. Nas entradas usadas, não há expoentes negativos de f/p/q que invalidem essa operação.

A multiplicação exterior por máscaras elimina geradores repetidos e conta inversões. dghost tem os sinais de uma derivação ímpar; z permanece inerte nesse diferencial. Os controles não reexecutam a demonstração das EOM078.

A decomposição de Sym²W enumera pesos com repetição, dimensão55. Conferi também à mão, em pesos inteiros:
(8,0)+(0,8)+(4,0)+(0,4)+2(0,0)+(4,4).
O emparelhamento com o recibo080 de Λ³G dá oito escalares e dois termos Weyl, total10. É uma contagem de contrações SEM derivadas de Weyl; a nota não a promove a dimensão de H³(s0)E5.

Há 14 condições TRUE e o comprimento da lista confere: 13 algébricas e uma de preservação das cinco fontes. O campo script contém SOMENTE uma medição final do próprio código. Nesta revisão, o código atual confere com esse pin; não se reconstrói daí um pin inicial que o recibo não possui. O finalizador mede script/recibo/rascunho antes/depois de SUA execução posterior; essa janela não é a da execução matemática.

Li também o finalizador. Ele cria a nota final nova a partir do rascunho preservado, inserindo explicitamente(R5), e confere pins. O manifesto distingue a nota .md do .pending histórico. Esta revisão confere os pins atualmente referidos e preserva os arquivos durante sua própria janela, sem executar nenhum dos dois scripts do autor.

## 7. Alcance aprovado

Aceito a prova na categoria métrica mínima natural da referência espaço-forma FIXADA, φ0 constante, κ não nulo, escalares herdados e ordem finita por cochain. Aceito fechamento, paridades, detector(R1), imagem cohomológica não nula e δ(K)≠0 nesse domínio.

Não se deduz cancelamento de A6, classificação completa de E5, admissibilidade de todos os contatos Q2, transporte a φ=id, um anel universal em K variável, QME, lim¹ ou UV. As precisões13+1 e do pin final do script devem acompanhar o inventário documental.

O registro desta revisão mede as fontes antes/depois. Nenhum original ou arquivo079/080/081 existente foi alterado; nenhuma compilação Lean ou execução própria de CAS é atribuída a esta revisão.
