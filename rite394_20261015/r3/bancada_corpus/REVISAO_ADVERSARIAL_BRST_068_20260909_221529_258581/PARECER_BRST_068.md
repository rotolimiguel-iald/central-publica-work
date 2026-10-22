# Revisão adversarial da extensão BRST linear — entrega 068

[DERIVED — parecer matemático escrito, revisão independente de escopo delimitado] Li integralmente a [nota BRST 068](<C:/IALD/Central de Patentes/Chatgpt/EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md>), comparei sua composição com o contrato de Jacobi/Green 066 e com o estado físico 067 e conferi os dois contratos primários indicados abaixo. **Não encontrei erro material na cadeia examinada.** Este parecer não é aprovação externa humana nem compilação Lean. Não executei os scripts da nota.

A revisão trata a redução S/V/TT já registrada em 067 como resultado anterior de referência; não refaz aqui sua derivação ADM, completude harmônica ou todos os coeficientes. O foco independente foi a passagem desse resultado físico para o sistema de gauge/auxiliar/ghost completo.

## 1. Álgebra de Cauchy e fator de fixação

A distinção entre `C` e `K*` foi mantida corretamente. Com `D=H+ℓ C*C`, `Q=CK`, a relação `C E_D=ℓ⁻¹ E_Q K*` e sua adjunta dão

\[
\Omega_D(kz,u)=\ell\Omega_Q(z,cu),\qquad k^\dagger=\ell c.
\]

O extrator `\mathcal E` recupera os parâmetros de gauge porque a matéria identidade lê a parte espacial e o traço espacial da métrica lê `6\mathfrak h v^r+2 div v_sp`. Como `\mathfrak h≠0`, segue `\mathcal E K=Id`. No nível de soluções, a nota usa apenas os **dados de Cauchy** de `\mathcal E u`; não presume `Q(\mathcal E u)=0` fora de um gauge puro. Assim `ek=Id` é legítimo.

Conferi a correção isotrópica da inversa esquerda. Escrevendo `F=ee†`,

\[
q=e-\tfrac12Fk^\dagger,\qquad
qq^\dagger=F-\tfrac12F-\tfrac12F
+\tfrac14F(k^\dagger k)F=0.
\]

Aqui se usaram `ek=Id`, `k†e†=Id` e `k†k=ℓck=0`. Consequentemente `qk=Id`, `r=ℓq†` satisfaz `cr=Id`, `qr=0`, e `p=Id−kq−rc` é autoadjunto simplético, idempotente, com `cp=qp=0`. São identidades efetivas; a sobrejetividade de c não foi deduzida só de ausência de núcleo de K. Os adjuntos de mapas de dados são de ordem espacial finita, pois os pareamentos cinéticos são locais e não degenerados.

## 2. Defeito Ward e correção suave

A conversão entre formas B sobre soluções e kernels W sobre testes conserva o fator ℓ. Por exemplo, `E_D C*f=ℓ⁻¹ K E_Qf`; portanto

\[
\ell W_D(C^*f,g)=B(k\rho_QE_Qf,\rho_DE_Dg).
\]

O lado correspondente `W_Q(f,K*g)` produz `ℓ B_Q(z,cu)`. Isso confirma a equivalência entre (5.5) e (5.6) na nota.

Para `d(z,u)=B₀(kz,u)−ℓ B_Q(z,cu)`, `ck=0` implica que `d(z,kz')=B₀(kz,kz')` é hermitiano. Assim, em

\[
h_d(u,v)=-d(qu,v)-\overline{d(qv,u)}+d(qu,kqv),
\]

os dois últimos termos se cancelam quando `u=kz`; resta `h_d(kz,v)=−d(z,v)`. A correção é hermitiana e comum aos sinais ±. Ela preserva CCR e impõe as Ward, mas não prova sozinha positividade; a nota não comete essa inferência.

O argumento microlocal é adequado: `\mathcal D^+−\mathcal D^-=0` pela identidade exata dos propagadores. Como os dois sinais têm orientações disjuntas, a distribuição comum é suave. Só então os mapas de dados q/k são aplicados. Não se atribui preservação de frequência a um projetor arbitrário de Cauchy.

## 3. O uso de S e a substituição física

No grau espacial ≥2, o parâmetro longitudinal/transversal de `Kv` é precisamente o E/F da decomposição do tensor espacial; `ξ=v_sp`. Logo `ξ−(∇E+F)=0` e a componente TT é zero. A retirada dos núcleos baixos corresponde ao gauge já identificado em 067. Isso justifica `SK=0` sobre campos arbitrários, sem usar a equação D.

Portanto `S*j` é um teste invariante. A Ward corrigida implica `C W_{D,1}S*j=0`; juntamente com `D W_{D,1}=0`, resulta `H W_{D,1}S*j=0`. A redução 067 então se aplica a essa imagem. Seu comutador é o comutador reduzido pela equivalência simplética, e a composição **espacial, local no tempo** por S conserva a orientação da frente de onda característica, conforme o argumento FIO explicitado em 067.

Essa ordem dos passos é decisiva: primeiro se obtém uma covariância reduzida com o mesmo comutador e as orientações corretas; daí `Δ⁺=Δ⁻` é suave. Somente essa diferença suave é levantada por `h_phys(u,v)=δ(spu,spv)`. Não é uma tentativa de projetar um kernel Hadamard singular com p e presumir que continue Hadamard. Como `pk=0`, a nova correção não altera as Ward; como `spu=su` em `ker c`, substitui exatamente o bloco físico pelo estado positivo 067.

## 4. Matriz completa e sentido do contrato forte

Conferi os blocos bosônicos de Green. A inversão de Schur dá `G_L,uu=G_D`, `G_L,ub=KG_Q`, `G_L,bu=G_QK*`, `G_L,bb=0`. O zero b–b é correto: `ℓ² C G_D C*−ℓ=0`. Não falta ali um termo local.

Nas pseudocovariâncias (7.1), as duas Ward anulam respectivamente os blocos `u–u` e `b–u` de `LΛ`; os demais usam `HK=0` e `QW_Q=0`. A diferença bosônica e a soma graduada ghost reproduzem os blocos do propagador completo. Para o sinal mais, a multiplicação dá `γΛ⁺=Λ⁺γ*`. Para o sinal menos, os blocos não nulos satisfazem a correspondente anticomutação; os sinais ghost escritos na nota são necessários para isso.

Em grau zero, os testes físicos têm `K*F=0`; os termos cruzados com b se anulam, deixando a positividade já construída. O uso de `Qb=0` e suporte compacto para eliminar uma contribuição compacta adicional é válido pela unicidade de Cauchy.

Assim o sentido **forte que faltava em 067** — equações e CCR/CAR no sistema livre inteiro, e não apenas no quociente — foi tratado explicitamente. A nota fala corretamente em pseudocovariâncias nas componentes não físicas. O dado permite o produto estrela livre graduado de funcionais microcausais sob o contrato indicado. Isso não deve ser renomeado como uma construção completa da teoria BV interagente: identidades mestras da interação, anomalias e renormalização de produtos temporais são outros passos, não examinados por mim nesta revisão.

## 5. Contratos primários conferidos e limites

[KNOWN] Conferi as hipóteses H1/H2 de §5.2.3 e a Proposição 5.4/Observação 5.5 de [Gérard–Murro–Wrochna](https://link.springer.com/article/10.1007/s00023-025-01539-1). Elas fornecem pseudocovariâncias Hadamard para o operador de onda em fibrado com forma hermitiana não degenerada; a observação separa expressamente essa construção da positividade. No fundo da nota, trivialização temporal e normalização da densidade deixam esse contrato aplicável perto da Cauchy compacta; a propagação estende os dados a I. Não é necessário invocar o teorema de vácuo Einstein do mesmo artigo.

[KNOWN] Conferi também a [Hipótese 2.15 e §3.2 de Wrochna–Zahn](https://arxiv.org/html/1407.8079v2). As identidades matriciais, a homologia em grau −1 e os Green exibidos atendem ao contrato geral usado; a Proposição 3.4, que exige `T=K`, não foi importada indevidamente. A diferença graduada das duas pseudocovariâncias acompanha o padrão daquela seção.

[INPUT] A ação, o fundo `φ=id` e `\mathfrak h≠0`, a Cauchy S³ e a construção física anterior permanecem explícitos. A prova não se generaliza automaticamente a outro fundo em que o extrator falhe ou a condições de fronteira diferentes. Nenhuma preservação automática de frequência por e/q/p foi usada. Não há afirmação de positividade da álgebra auxiliar inteira, de probabilidades operatoriais não lineares ou de controle dos extremos temporais.

[REAL — custódia desta revisão] As três fontes lidas foram medidas antes e depois da escrita deste novo parecer; os pins estão no manifesto acompanhante. Não alterei notas congeladas, não executei `um.py`, integradores, compiladores Lean ou scripts CAS nesta revisão.
