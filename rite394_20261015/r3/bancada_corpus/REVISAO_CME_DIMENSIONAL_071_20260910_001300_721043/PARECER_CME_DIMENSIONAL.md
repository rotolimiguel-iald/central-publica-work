# Parecer independente: CME dimensional e alcance da importação

10/09/2026. [DERIVED — revisão matemática escrita] [REAL — leitura e pins de arquivos].

**Resultado: não identifiquei erro material na nota examinada, dentro do escopo que ela declara.** A extensão dimensional fornece a identidade BV clássica exata para o sistema bosônico. A renormalização importada pertence ao esquema dimensional indicado; a identidade quântica na Q2 curva continua dependendo do contrato de comparação, que a nota não dá como realizado.

## 1. Objeto e evidência

Li integralmente [CME_DIMENSIONAL_E_CONTRATO_DE_TRANSFERENCIA.md](<C:/IALD/Central de Patentes/Chatgpt/CME_DIMENSIONAL_EINSTEIN_SIGMA_071_20260910/CME_DIMENSIONAL_E_CONTRATO_DE_TRANSFERENCIA.md>). O manifesto deste parecer mede o arquivo antes e depois e vincula esta revisão àquele conteúdo. Não fiz execução de um.py, CAS, Lean, diagramas ou do esquema de subtração; tampouco revisei o estado canônico nesta subtarefa.

Consultei a fonte primária [Anselmi, *Renormalization of gauge theories without cohomology*](https://arxiv.org/pdf/1301.7577). Embora a abertura da URL com sufixo v2 tenha falhado no serviço web, o PDF retornado pela URL acima mostra na primeira página **1301.7577v2, 31 Jul 2013**. Foram examinados a identidade (1.6), a precisão sobre o regulador em §2, o algoritmo e a extensão de parâmetros de §3, e as condições de truncatura e infravermelho de §4. Não atribuo hash ao PDF remoto: a versão foi identificada pelo próprio documento, e não por igualdade de bytes com um download.

## 2. Verificação da identidade clássica

[DERIVED] Com s ímpar à esquerda, o sinal sC=C·∂C é compatível com sy=C·∂y. Explicitamente,

\[
 s^2y^A=(C^\sigma\partial_\sigma C^\rho)\partial_\rho y^A
 -C^\rho(\partial_\rho C^\sigma)\partial_\sigma y^A
 -C^\rho C^\sigma\partial_\rho\partial_\sigma y^A=0.
\]

Os dois primeiros termos se cancelam por renomeação; o último contrai um par antissimétrico com derivadas simétricas. Para um tensor, a composição graduada das derivadas de Lie fornece a mesma identidade. Assim s²g=0; s²C=0 segue da regra graduada sobre C·∂C. O par s barC=−b, sb=0 é compatível e não requer uma equação de movimento.

Os coeficientes h_AB(y) obedecem sh_AB=C·∂h_AB. A contração Q entre g inversa e os dois diferenciais dy cancela os termos com derivadas do ghost, deixando sQ=C·∂Q. A variação da densidade métrica e a escalaridade de R então dão sL_D=∂_μ(C^μL_D). Esses cancelamentos não contêm uma identidade especial de quatro dimensões. Eles valem como identidades da álgebra tensorial continuada, com os índices do alvo mantidos tridimensionais.

É possível tornar o pareamento da nota inteiramente concreto tomando os antifields como fontes de densidade dual, com a simetria apropriada para g* e a posição graduada escolhida para que sΦ=(Φ,Σ_D). Assim não se introduz inadvertidamente uma medida dependente de g no anticolchete canônico. Como as transformações sΦ não dependem dos antifields, o colchete de Σ_D consigo mesma tem apenas os setores de grau zero e um em antifield: o primeiro é 2sS_D, e o segundo codifica s²Φ. Ambos se anulam módulo divergências. A falta de um termo b*sb, que seria zero, não elimina a fonte conjugada a b do espaço BV.

A expressão “mínima estendida” em (4) é apenas uma nomenclatura informal: o conjunto apresentado já contém o par não minimal. Isso não altera o cálculo ou a conclusão.

Não interpreto a prova como existência de uma variedade de dimensão fracionária. A nota faz corretamente a distinção entre o objeto físico e a álgebra de regularização.

## 3. Gauge, normalização e mudança de coordenadas

[DERIVED] Mantendo os dados de fundo fixos sob s, a férmion escrita produz

\[
 s\Psi_D=\int dV_{\bar g}\left[b^\mu F_\mu-
 \frac{b^\mu b_\mu}{2\ell_D}+\bar C^\mu sF_\mu\right].
\]

O sinal positivo do último termo e o sinal negativo do quadrático em b seguem juntos de s barC=−b e da regra de Leibniz ímpar. Não há troca silenciosa da convenção não minimal. A transformação canônica dos antifields preserva a CME, qualquer que seja o parâmetro D admitido na álgebra. O coeficiente 1/2 no traço do gauge de Donder não afirma uma projeção sem traço.

A mudança de coordenadas no alvo admite levantamento cotangente; em particular, Exp_ybar ξ é uma mudança formal invertível no feixe tangente ao mapa de fundo, numa vizinhança formal da seção zero. Isso preserva a identidade clássica sem converter uma única carta do alvo em descrição global de todas as configurações.

As dimensões de massa registradas conferem para y adimensional: [κ_D]=2−D, [c_D]=D−2, [Λ_D]=2. Também confere a normalização material do §3: com c=4/κ e y=Exp_y0(√κ ξ/2), o termo quadrático é cκ/8 vezes h_y0(dξ,dξ), portanto seu coeficiente é 1/2. Essa observação serve para a parametrização local EFT; não substitui o fundo físico não constante por um vácuo constante.

## 4. Importação: hipótese exata e conclusão limitada

[KNOWN] A fonte usa regularização dimensional, subtração mínima e a identidade (Γ,Γ)=⟨(S,S)⟩. §3 parte da CME exata no regulador; a ação inicial não recebe termos finitos explicitamente multiplicados por potências positivas de ε. A subtração local avança a identidade em ordem de loops, e a extensão de parâmetros organiza os termos gerados. Para teorias não renormalizáveis por contagem de potências, §4 requer truncaturas compatíveis, cinéticas apropriadas e controle infravermelho. O resultado não garante equivalência automática entre as simetrias de gauge antes e depois da extensão. [Anselmi, (1.6), §§2–4 e introdução](https://arxiv.org/pdf/1301.7577).

[DERIVED — aplicação revista] A nota realmente exibe a entrada algébrica: S_D, suas fontes e o gauge usam contrações métricas e difeomorfismos, sem γ5, tensor epsilon de espaço-tempo ou projeções quirais. Não se limita a testar a CME em D=4. Os parâmetros bare independentes permitem evitar uma expansão prematura dos fatores de escala; a introdução posterior de parâmetros renormalizados deve conservar o tratamento de evanescentes e polos. A cautela sobre não eliminar Euler por uma identidade de quatro dimensões antes da subtração é adequada.

A invariância da medida formal e o teorema de localidade das subtrações pertencem ao esquema importado; não são consequências apenas da conta clássica acima. A frase de aplicação da nota os mantém no domínio perturbativo declarado. Também não vejo uma afirmação de que o setor κc=4 seja automaticamente preservado pelo fluxo RG: a própria nota deixa os parâmetros independentes e admite extensão EFT e condições finitas adicionais. Fixar essa relação como condição renormalizada em todas as escalas exigiria outra demonstração.

Não há neste parecer uma verificação concreta das prescrições infravermelhas ou da cadeia truncada para o habitante I×S³. Tampouco a nota as entrega. Por isso o resultado aceitável continua sendo **CME dimensional exata e rota importada de renormalização no esquema especificado**, preservando as condições analíticas e de truncatura, em vez de uma execução completa dessa rota no fundo físico.

## 5. O contrato causal continua aberto

[DERIVED] O lema do §6 é correto como lema condicional de transporte: uma equivalência admissível que leva ação, inserções BV, contatos e operações juntos transporta uma identidade entre eles. Aplicar um mapa só à ação não justificaria a conclusão, e a nota exclui precisamente esse atalho.

Os seguintes passos permanecem distintos: construir produtos dimensionais para a família curva considerada; verificar axiomas causais, realidade e dependência local/covariante; construir a comparação de fontes e contatos; controlar as mudanças de cartas do alvo e de fundo. A concordância do nome dos campos ou da expressão da ação não fornece esses mapas. A redação dos §§4, 6 e 7 preserva essa diferença.

Assim, não se promove a identidade de ghost zero do calor a uma anomalia de ghost um, a CME clássica à QME causal, ou a remoção das quebras produzidas pelo regulador a uma classificação nula de todo H¹(s|d). A positividade de estados, os parâmetros finitos e a extensão ultravioleta permanecem obrigações próprias. Não há erro material a corrigir na fonte congelada no escopo desta revisão.
