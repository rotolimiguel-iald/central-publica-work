# Parecer independente sobre os módulos H³/H⁴ e o setor calculado — 076

10/09/2026. [DERIVED — revisão matemática escrita delimitada]. Resultado: **não identifiquei erro material nos enunciados e provas explicitamente delimitados da nota076**. O parecer não classifica os módulos completos, não prova os dois grupos residuais e não fecha QME. Não houve Lean, CAS, execução/importação de um.py, edição de fonte existente ou nova captura do canônico.

Objeto lido integralmente: [MODULOS_H3_H4_E_SETOR_CALCULADO.md](<C:/IALD/Central de Patentes/Chatgpt/MODULOS_BRST_EBAR_076_20260910/MODULOS_H3_H4_E_SETOR_CALCULADO.md>). Pin medido antes da gravação deste parecer: **18039 bytes; SHA-256 5084cfc22a77ee6b4ed62c25130c738a0da41b1964501a67b9aef714594cc643**. O recibo ao lado mede novamente os arquivos após a escrita e confere o manifesto do autor. É revisão de uma demonstração escrita, não um certificado de execução formal.

## 1. A propriedade dos antifields foi conferida, incluindo o antifield do ghost

A propriedade(4), nas linhas75–83 da nota, é válida no setor MÉTRICO mínimo declarado. Para evitar confusão com conjugação complexa, escrevo c^† para o antifield BV do ghost c. Ele é par, tem ghost −2 e é um covetor densidade de peso1.

Fixe a convenção sc^μ=c^ν∂_νc^μ e as derivadas funcionais à direita. O termo da ação BV que contém c^† é

\[
 S_{\rm gh}=-\int c^\nu c^\dagger_\mu\partial_\nu c^\mu\,d^4x,
 \qquad sc^\mu=-\frac{\delta^R S}{\delta c^\dagger_\mu},
 \quad sc^\dagger_\mu=\frac{\delta^R S}{\delta c^\mu}.
\]

A variação em c, ordenada à direita e integrada por partes, fornece

\[
 \gamma c^\dagger_\mu
 =c^\nu\partial_\nu c^\dagger_\mu
   +(\partial_\mu c^\nu)c^\dagger_\nu
   +(\partial_\nu c^\nu)c^\dagger_\mu
 =(\mathcal L_c c^\dagger)_\mu.
\]

A contribuição restante é a parte de Noether/KT, obtida pela variação em c dos termos de antifields de g e φ. Ela contém esses antifields, campos ativos e seus jatos, mas nenhum c. Seu sinal convencional não altera b_Nδc^†=0. Isso confere o caso que não poderia ser justificado apenas citando o transporte de g e φ.

A separação entre transporte tensorial e KT, inclusive seu prolongamento covariante, também está explicitada em [BBH1995, equações2.6–2.9, 3.6–3.7, 3.13 e 3.16](https://arxiv.org/pdf/hep-th/9505173v2). Usei essas fórmulas para conferir a convenção, sem importar a classificação cohomológica desse artigo. A convenção ativa é compatível com o [dicionário BV069, seção4](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md>).

Há ainda uma razão explícita para a estabilidade dos prolongamentos: δg=δφ=0. Logo δ aniquila a conexão de Levi-Civita ativa, a conexão do alvo composta com φ e os fatores métricos usados para converter densidades. As derivadas covariantes ATIVAS de um antifield conservam a decomposição sT=L_cT+δT, com a segunda parcela sem ghosts. Essa afirmação não substitui a conexão ativa por uma conexão de fundo fixa, nem inclui derivados de ghosts no setor.

## 2. E_N=C_N=0 no setor K tem o domínio correto

As identidades(5)–(7) usam b_Nc=dx, b_N∂c=−Γ̄dx e o fato de b_N aniquilar os demais geradores de K. A substituição na derivada de Lie produz a derivada covariante de fundo do tipo tensorial correspondente. Para c não derivado,

\[
 b_N(c^\mu\partial_\mu c^\nu)
 =dx^\mu\partial_\mu c^\nu
   -c^\mu\bar\Gamma^\nu_{\mu\rho}dx^\rho
 =dx^\mu(\partial_\mu c^\nu+
              \bar\Gamma^\nu_{\mu\rho}c^\rho).
\]

O último sinal vem da troca de c com dx. As conexões cancelam nas contrações escalares completas, incluindo os pesos de densidade. Como C_N=[d_H,b_N] também aniquila esses geradores, as duas identidades são exatas em K, sem exigir que α já seja ciclo.

O domínio não inclui ∇̄c nem um ghost Lorentz covariantizado por analogia. Permanece a [precisão de frame074](<C:/IALD/Central de Patentes/Chatgpt/HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/PRECISAO_FRAME_LOCAL_074.md>). O resultado também não afirma D_N²=0 por ausência de curvatura de Γ̄: a ação de D_N fora de K é diferente e a curvatura em C_N∇̄c continua presente.

A família A_L=ρ_L c⁰c¹c²c³ confere em quatro dimensões. Com η_c=c⁰c¹c²c³, sη_c=−η_c∂_μc^μ. A parcela de transporte de ρ_L produz cinco ghosts não derivados e se anula; as duas divergências cancelam. Assim sA_L=E_NA_L=C_NA_L=0. Isto prova ciclos, não sua não trivialidade, independência ou exaustividade.

## 3. A homotopia formal de S³ funciona para φ₀ variável

Conferi diretamente as equações(14)–(18). Para F_u=Exp_(φ₀)(utξ), W_u=∂_uF_u e V_u=sF_u, as identidades s²F_u=0, sW_u=∂_uV_u e d_targetΩ=0 dão

\[
 \partial_u\bigl(\Omega(V_u,V_u,V_u)/6\bigr)
       =s\bigl(\Omega(W_u,V_u,V_u)/2\bigr).
\]

Integrando em u, o termo na extremidade zero é zero porque F₀=φ₀ e sφ₀=0. O resultado é precisamente τ₃=sK₂. A prova não usa d_Hφ₀=0 nem a equação de movimento de φ.

A contagem inicial também confere. Em variáveis normalizadas c=tC,

\[
 W_u=t\xi+O(t^2),\qquad V_u=ut\,s_t\xi+O(t^2),
 \qquad \frac12\int_0^1u^2du=\frac16.
\]

Daí K₂=t³Ω(φ₀)ξ(s_tξ)²/6+O(t⁴). Em ξ=0, s_tξ=C·∂φ₀. Portanto o derivado BRST da primitiva pode ser não nulo nessa seção, embora a primitiva se anule nela. A avaliação ξ=0 não é um mapa de complexos para o BRST ativo. Essa distinção resolve o aparente paradoxo do fundo não constante.

Cada coeficiente formal depende de um número finito de jatos e é polinomial em u; a integração é coeficiente a coeficiente. A exponencial redonda dá uma construção intrínseca no fibrado formal φ₀*TS³, sem escolher uma única carta de valores para a imagem de φ₀. O peso t^E/número de campos é preservado na comparação entre K₂ e τ₃; o prefator de laço os coloca na mesma organização da [completação Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>). Isso não prova que tal ciclo ocorra como anomalia nem impõe por si todos os contatos causais.

A orientação do alvo foi tratada corretamente: Ω, τ₃ e K₂ mudam de sinal juntos sob uma inversão de orientação. Não se declarou um invariante O(4) escalar em um setor onde só existe esse comportamento de sinal.

Precisão aditiva de alcance: a identidade sφ₀=0 não torna d_Hφ₀ zero. Assim a exatidão BRST acima não elimina, por exemplo, a possível classe horizontal de φ₀*Ω. Tampouco fornece uma primitiva de de Rham global de Ω em S³. Ela usa o fundo inerte e a vizinhança formal da diagonal, como a nota afirma.

## 4. Coeficientes de fundo, correntes e classes globais foram separados

Para β somente de B₀ e α∈K, E_N(βα)=(d_Hβ)α. Para sα=0, a identidade geral E_Nα=d_Hα+s(b_Nα) está com o sinal correto. O mapa μ da equação(13) é bem definido em classes: multiplicar uma igualdade s-exata por β, com sβ=0, preserva a exatidão com o sinal graduado apropriado.

Nada disso torna μ injetivo, sobrejetivo ou um isomorfismo de módulos livres. A nota mantém expressamente em aberto as relações introduzidas por coeficientes de fundo e pela completação. Esse limite é necessário antes de substituir os grupos residuais por cohomologia de de Rham do fundo com coeficientes constantes.

A divergência dos seis j_AB da equação(10) confere sob □Y_A=λY_A. A nota não afirma ter construído todos os levantamentos KT nem demonstrado que essas seis correntes constituam toda H³. Seu uso de K para um levantamento já escrito com os geradores permitidos é uma implicação condicional correta.

A separação dos geradores CE³, das classes de de Rham de GL⁺₄ e do volume S³ está correta. O termo de curvatura s₂θ³ impede identificar um polinômio CE com um ciclo completo de s. Conferi também a remissão de transgressão e a hipótese7.33 de [BBH1995, equações7.2–7.3 e teorema7.2](https://arxiv.org/pdf/hep-th/9505173v2). A nota não toma esse teorema como aplicável sem conferir a classe material e os espectadores.

A fórmula(3) consome a decomposição e os graus baixos já declarados em071; não os auditei novamente como classificação integral nesta revisão. Na vizinhança formal do valor invertível U₀, a contração radial dos pares livres (U,V=sU) é válida nesse fator. A nota não estende esse fato ao complexo natural inteiro nem troca o ghost Lorentz pelo difeomórfico.

## 5. Veredito e limite da revisão

[DERIVED] Parecer favorável às provas explícitas de (4)–(18), à delimitação dos candidatos e à distinção entre a classe global071 e a completação formal com fundo. **Nenhuma correção material da fonte é solicitada por esta revisão.**

[OPEN] Permanecem a geração e as relações dos módulos H³/H⁴ na classe natural/Rees, o cálculo dos dois grupos de Ē_N do critério074, a primitiva admissível de uma anomalia efetiva, os contratos causais completos e QME. O parecer não valida uma classificação integral de correntes, não incorpora076 ao manifesto075 e não atualiza o estado canônico.

[REAL — custódia documental] O recibo registra os pins relidos, a comparação com o manifesto do autor e a preservação byte a byte dos dez arquivos locais de entrada durante a gravação. Esses checks são de custódia; a análise matemática acima foi feita por leitura e cálculo escrito, sem CAS/Lean. Nenhuma aprovação é atribuída ao autor da nota ou a terceiro.
