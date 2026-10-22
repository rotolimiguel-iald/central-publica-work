# Da contorção à fonte e à carga regional

17/09/2026. [DERIVED — cálculo tensorial escrito; não Lean]. Esta nota paga a passagem geométrica **dada uma contorção**, não deriva o campo K_β a partir de β, de ψ ou do dissipador.

## Fornecedores recuperados

Leitura canônica, sem execução: `A Ponte Einstein Cartan Miguel.tex`, linhas530–548, escreve Γ=Γ_LC+K_β em uma reconstrução condicional; linhas2223–2234 incluem a derivação explícita de K_β no contínuo entre os problemas abertos daquele estrato. No `Nós/um.py` lido, `prove_cocycle_to_einstein` já declara T^TGL=T^matter+T^{partial,beta}+T^{torsion/diss} e mantém G(g) de Levi–Civita. Há consumidores identificados como v361 e fontes marcadas v362 no arquivo consultado; não se inferiu uma rodada ou selo corrente dessas ocorrências.

Portanto, a conexão de Levi–Civita do fornecedor Einstein–sigma não prova ausência de Cartan na teoria inteira. A questão pertinente é a fonte efetiva e suas equações. Não substituir a torção modular de matrizes por torsão espaço-temporal: os tipos e as derivações são diferentes.

## Identidade exata e convenção

Escreva C^ρ_{μσ}=K_β^ρ_{μσ} para evitar confusão com o Hamiltoniano modular. Usamos ∇_μV^ρ=∂_μV^ρ+Γ^ρ_{μσ}V^σ e

R^ρ_{σμν}=∂_μΓ^ρ_{νσ}−∂_νΓ^ρ_{μσ}+Γ^ρ_{μλ}Γ^λ_{νσ}−Γ^ρ_{νλ}Γ^λ_{μσ}.

Se Γ=Γ_LC+C, expansão direta fornece

ΔR^ρ_{σμν}=∇_μC^ρ_{νσ}−∇_νC^ρ_{μσ}+C^ρ_{μλ}C^λ_{νσ}−C^ρ_{νλ}C^λ_{μσ},

onde ∇ é Levi–Civita. Na expansão, os termos mistos Γ_LC C formam as três parcelas de conexão da derivada covariante do tensor C; a simetria de Γ_LC nos índices inferiores cancela a parcela adicional ao antissimetrizar μ,ν. Contrair ρ com μ dá

\[
D_{\sigma\nu}=\nabla_\rho C^\rho{}_{\nu\sigma}
-\nabla_\nu C^\rho{}_{\rho\sigma}
+C^\rho{}_{\rho\lambda}C^\lambda{}_{\nu\sigma}
-C^\rho{}_{\nu\lambda}C^\lambda{}_{\rho\sigma}.
\]

Defina B_{μν}=D_{(μν)}−½g_{μν}g^{ab}D_{ab}. Então, exatamente,

\[
G_{(\mu\nu)}(\Gamma)=G_{\mu\nu}(g)+B_{\mu\nu}[C].
\]

Para chamar C de contorção métrica, impomos ainda C_{ρμσ}=−C_{σμρ}; a identidade de diferença de curvaturas é mais geral. A torsão é T^ρ_{μν}=C^ρ_{μν}−C^ρ_{νμ}.

## Fonte efetiva: equivalência, não equação de movimento nova

Se a equação simétrica de entrada for G_(μν)(Γ)+Λg_{μν}=κΘ_(μν), ela equivale a

\[
G_{\mu\nu}(g)+\Lambda g_{\mu\nu}
=\kappa T^{\rm eff}_{\mu\nu},\qquad
T^{\rm eff}_{\mu\nu}=\Theta_{(\mu\nu)}-\kappa^{-1}B_{\mu\nu}[C].
\]

As equações da conexão e o setor antissimétrico não desapareceram: a reescrita não os resolve. Θ deve ser a fonte correspondente à ação escolhida, podendo conter dependência em C; não substituí-la silenciosamente por um tensor de matéria sem torsão. Termos adicionais de ação, como Holst, exigem transportar também sua contribuição. B não é automaticamente um novo tensor conservado isoladamente.

O teorema de [De Lorenzo–De Paoli–Speziale, proposição1](https://arxiv.org/pdf/1807.02041) sustenta a conservação da fonte efetiva de Einstein–Cartan a partir das identidades de Noether, usando as equações de matéria e torsão. Essa hipótese importa quando se pretende derivar a equação métrica por termodinâmica: inferir conservação da própria equação métrica a ser derivada seria circular.

## Como entra no primeiro coeficiente do resto modular

Fixe nesta variação g,ξ,Σ,κ e a prescrição de bordo. Introduza uma amplitude formal ε, que **não** é uma variação livre de β_TGL, e C_ε=εC₁+O(ε²). Então

B₁=SymTraceReverse(∇_ρC₁^ρ_{νσ}−∇_νC₁^ρ_{ρσ}).

O termo quadrático em C começa na ordem ε². Se C_ε=εC₁+ε²C₂+…, B₂ contém tanto a derivada de C₂ quanto os produtos de C₁. Não há uma regra universal de que a primeira correção seja sempre linear: um C₁ constante em Minkowski tem B₁=0, podendo ter B₂≠0.

A expansão é em torno de C₀=0. Para uma contorção inicial não nula, a primeira variação recebe também os produtos cruzados C₀·dotC e dotC·C₀; não se pode usar apenas a parcela de derivadas acima.

Para Q_ξ=2π∫_Σ ξ^μT^eff_{μν}dΣ^ν, a parcela geométrica na sua primeira variação é

\[
\dot Q_\xi=2\pi\int_\Sigma\xi^\mu
(\dot\Theta_{(\mu\nu)}-B_{1\mu\nu}/\kappa)d\Sigma^\nu.
\]

Numa regularização fiel, consumindo a derivada do logaritmo já demonstrada,

\[
R_1=-D\log_{\rho_0}[\dot\rho_0]
-2\pi\int_\Sigma\xi^\mu\dot\Theta_{(\mu\nu)}d\Sigma^\nu
+\frac{2\pi}{\kappa}\int_\Sigma\xi^\mu B_{1\mu\nu}d\Sigma^\nu.
\]

É uma fórmula de composição condicional: os termos de carga devem ser inserções renormalizadas na mesma representação de ρ. Um B construído apenas de campos clássicos de fundo, inserido como número vezes I, é central e não prova uma contribuição não central. Uma realização operatorial de C e dos produtos em B exige seu fornecedor e renormalização. Se métrica, superfície, ξ,κ ou bordo variarem, acrescentam-se suas variações; não estão contidas na fórmula de direção fixa acima.

A primeira contribuição não central é detectada por [R₁,A₀]+[R₀,A₁] para observáveis transportados do centralizador. A derivação não calcula dotρ₀ nem prova essa expressão diferente de zero no diamante físico. Seu avanço é explicitar o consumidor tensorial e o sinal da parcela de contorção, sem transformar K_β em uma constante escalar.

## Evidência e obrigações

`verify_contorsion_source.py` confere a identidade por aritmética racional exata: conexão de referência simétrica genérica, diferença e jatos genéricos, amplitudes positivas/negativas, fonte simétrica e exemplo vetorial metricamente compatível com termo quadrático não nulo. Não é solução on-shell da TGL, simulação de vácuo, coeficiente físico medido ou prova de UV. A demonstração universal é a expansão escrita; os controles detectam erros de índices e sinais.

Conferência adicional do exemplo, sem alterar a escolha física da teoria: em Minkowski, V_μ=(1,2,0,−1) constante e C^ρ_{μσ}=δ^ρ_μV_σ−g_{μσ}V^ρ dão B₁=0 e B₂ com linhas (−2,4,0,−2), (4,12,0,−4), (0,0,4,0), (−2,−4,0,6), por aritmética racional. Assim o termo de fonte, e não apenas a diferença de Ricci, tem contribuição quadrática não nula nesse controle. O exemplo não afirma que a primeira variação do resto modular inteiro seja zero: a resposta do estado e de Θ ainda entra.

[OPEN] Consumir K_β e a equação da conexão da mesma ação, formar a fonte renormalizada e sua resposta de estado, e comparar o fluxo regional ao modular. Nenhum novo consumidor do motor, alteração de gate ou modificação canônica foi feito.

[DERIVED — revisão independente Hypatia] Índices, sinais, fonte efetiva e composição condicional aprovados. Ressalvas incorporadas: os 40 controles de fonte reutilizam a aplicação de simetrização/traço e testam sua linearidade, não independentemente o coeficiente −1/2; esse coeficiente foi conferido na revisão escrita. Os jatos sorteados dbase não satisfazem todas as simetrias de uma conexão geométrica, mas cancelam na diferença; são controles da identidade algébrica, não fundos físicos sorteados. O negativo só recusa a escala linear para uma parcela quadrática não nula. Parecer e escopo em REVISAO_CONTORCAO_FONTE.md. Não é nova formalização Lean.
