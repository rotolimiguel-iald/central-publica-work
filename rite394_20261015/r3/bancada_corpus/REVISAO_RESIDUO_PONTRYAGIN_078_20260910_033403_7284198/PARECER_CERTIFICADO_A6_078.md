# Revisão independente do certificado A₆ e de seu alcance

10/09/2026, etapa078, fora da entrega077. Autor: /root/finish_gibbs_realization. [DERIVED — revisão matemática escrita] [REAL — fontes medidas]. Não executei Lean, CAS, um.py ou os scripts das fontes. Nenhum arquivo congelado ou original foi alterado.

**Conclusão da revisão.** Não identifiquei erro material no [certificado de não exatidão A₆](<C:/IALD/Central de Patentes/Chatgpt/RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md>). A solução explicitada satisfaz o operador linearizado físico acoplado; os ghosts escolhidos são Killing em uma vizinhança; a avaliação de todos os jatos anula fronteiras de s₀ e conserva A₆ não nulo. A consequência vale para a classe específica [T≤5] de077. Não exclui outras classes em H³(C₅) com o mesmo líder em C₃.

Este parecer é análise de minha autoria. Não é aprovação em nome do operador ou de outro agente, nem equivale a compilação Lean. O [controle Weyl pontual da raiz](<C:/IALD/Central de Patentes/Chatgpt/CONTROLE_WEYL_PONTUAL_078_20260910/RESULTADO_WEYL_PONTUAL_078.json>) foi lido como evidência algébrica complementar; não foi reexecutado nem usado como prova das EOM ou do mapa de avaliação.

## 1. Convenções: correção explícita de minha leitura preliminar

A ordenação é x⁰=τ, x¹=x, x²=y, x³=z, com η=diag(+1,−1,−1,−1). O fator a=ℓ/z depende da coordenada **espacial** z. A fonte usa R^a_bcd=∂cΓ^a_bd−∂dΓ^a_bc+Γ^a_ecΓ^e_bd−Γ^a_edΓ^e_bc e Ric_bd=R^a_bad.

Em uma mensagem preliminar, interpretei z como coordenada temporal de índice zero e levantei uma ressalva de sinal. Essa interpretação não correspondia à fonte. Foi retirada antes deste parecer. Não é necessário inverter Ricci ou Λ na construção examinada.

Confiro diretamente Γ⁰_03=−1/z, Γ³_00=−1/z, Γ³_33=−1/z. Com w=ln(ℓ/z), temos w_z=−1/z, w_zz=1/z², □ηw=−1/z² e |dw|²η=−1/z². Na transformação

\[
 \operatorname{Ric}(a^2\widetilde g)
 =\operatorname{Ric}(\widetilde g)
 -2(\widetilde\nabla dw-dw\otimes dw)
 -\widetilde g(\widetilde\Box w+2|dw|^2),
\]

o tensor ∇dw−dw⊗dw é zero em η, e o último escalar é −3/z². Portanto Ric(g0)=3η/z²=(3/ℓ²)g0. Como W(g0)=0, a curvatura é a do espaço forma de K=1/ℓ². Isso confere com Λ>0 e a contração primeira–terceira declaradas.

[KNOWN] Conferi a referência [Wheeler, Weyl geometry, §2](https://arxiv.org/pdf/1801.03178). Ela desenvolve a transformação conforme e a invariância do Weyl. Sua apresentação de assinatura não dispensa a conta acima; não a usei para atribuir automaticamente um sinal à carta da fonte.

## 2. A solução da EDO e a Hessiana acoplada

As duas soluções propostas são

\[
 F(z)=\cos(kz)+kz\sin(kz),\quad
 G(z)=\sin(kz)-kz\cos(kz).
\]

F'=k²z cos(kz), G'=k²z sin(kz). Substituir mostra que ambas satisfazem f''−2f'/z+k²f=0; seu Wronskiano FG'−F'G=k³z² não se anula para k≠0,z>0. Assim existe uma combinação real única com f(z0)=0 e f'(z0)=1. Em particular f''(z0)=2/z0. A solução é analítica na vizinhança escolhida; nenhum teorema de extensão de jatos arbitrários a uma solução de PDE é necessário.

Na perturbação γ do bloco xy, o traço plano é γ11+γ22=0 e a divergência é zero, porque não há dependência em x,y nem componentes γ0μ ou γ3μ. Consequentemente δRic(η)_ij=−½□ηγ_ij; os demais componentes são zero. A alteração de conexão que entra no termo conforme é δΓ³_ij=½∂zγ_ij, logo δ(∇_i∂_jw)=γ'_ij/(2z). A variação do escalar □w+2|dw|² é zero: γ33=0 e o traço espacial xy e sua derivada são zero.

O resultado é

\[
 \delta\operatorname{Ric}(g_0+t h)_{ij}-\Lambda h_{ij}
 =-\tfrac12\Box_\eta\gamma_{ij}-\gamma'_{ij}/z,
 \quad h=a^2\gamma.
\]

Como □ηγ=−(k²f+f'')Q(τ), a EDO anula esse tensor identicamente na vizinhança. As componentes fora do bloco xy permanecem zero. Não foi verificado apenas o valor em p.

δRic=Λh implica δR=0, pela variação da métrica inversa na contração com Ric0=Λg0. Portanto δ(G+Λg)=0. Com φ0 constante, dφ0=0; a primeira variação do tensor de matéria é zero, e não há mistura linear de h com ξ na Hessiana física. A escolha ξ=0 satisfaz a parte sigma. Logo H₀(h,0)=0 para o operador **físico mínimo sem gauge fixing**, que é justamente o operador exigido pelo teste.

A prova não exige h numa solução não linear g0+t h, não exige condições de contorno numa carta inteira e não importa os modos físicos da referência φ0=id. Uma vizinhança globalmente hiperbólica suficientemente pequena pode ser escolhida com z afastado de zero. Se for necessário permanecer em qualquer vizinhança pequena dos jatos dinâmicos nulos, substitua h por εh com ε real pequeno e não nulo; a equação linear continua válida e a densidade quadrática adquire apenas ε².

## 3. Verificação dos quatro produtos de Weyl

No ponto p=(0,0,0,z0), os únicos segundos jatos relevantes são γ11,zz=u, γ22,zz=−u e γ12,τz=v, com u=2/z0 e v=k. γ11,ττ e γ22,ττ são zero porque f(z0)=0. A Ricci calculada em η+tγ não é a Ricci do fundo conforme completo: seus termos são compensados pelos termos conformes na seção anterior.

A invariância conforme de W como tensor (1,3) permite usar essa perturbação plana para a 2-forma matricial W[1]. Não aparece volume a⁴ adicional em tr(W[1]∧W[1]). Pondo A=1/(2z0), B=k/2, a subtração do Schouten dá as quatro formas abaixadas da fonte:

\[
 W_{01}=-Ae^{01}+Be^{23},\quad W_{02}=Ae^{02}+Be^{13},
\]
\[
 W_{13}=Be^{02}-Ae^{13},\quad W_{23}=Be^{01}+Ae^{23}.
\]

Os outros pares independentes são zero. Para V=dτ∧dx∧dy∧dz, os quadrados são, respectivamente, −2ABV, −2ABV, +2ABV, +2ABV, usando e02∧e13=−V. No traço matricial, os pares 01/02 recebem fator +2 e os pares 13/23 recebem fator −2, pois

\[
 \operatorname{tr}(W\wedge W)
 =-2\sum_{a<b}\eta_{aa}\eta_{bb}W_{ab}\wedge W_{ab}.
\]

Cada par contribui −4ABV. Assim ρ[2](p)=−16AB=−4k/z0≠0. Essa verificação escrita confirma o coeficiente do recibo pontual da raiz. O recibo, por seu próprio limite, não verifica as EOM, Killing, todos os jatos ou a não-exatidão; esses passos foram examinados separadamente.

## 4. O mapa de avaliação realmente anula todos os jatos de s₀

As translações ∂τ,∂x,∂y são Killing exatos, pois os coeficientes de g0 não dependem dessas coordenadas. Para D=τ∂τ+x∂x+y∂y+z∂z, temos L_Dη=2η e D(a²)=−2a². Portanto L_Dg0=0. D/z0 é Killing e tem valor ∂z em p. Os quatro campos preservam φ0 constante.

Escreva C=θ⁰∂τ+θ¹∂x+θ²∂y+θ³D/z0, onde θ são geradores de uma álgebra exterior e têm diferencial zero. Com u=(h,0), u*=C*=0, as fórmulas corrigidas

\[
 s_0u=R_0C,\quad s_0C=0,\quad
 s_0u^*=+H_0u,\quad s_0C^*=R_0^\dagger u^*
\]

avaliam em zero como funções numa vizinhança. Logo todos os seus prolongamentos também avaliam em zero. A afirmação inclui antifields: não é suficiente anular seus valores, e a fonte corretamente verifica também suas variações H₀u e todos os derivados. A variação sigma do campo é C·dφ0=0.

Ao avaliar depois no ponto, C^μ(p)=θ^μ, e obtemos

\[
 \operatorname{ev}_p(A_6)
 =-4k\,\theta^0\theta^1\theta^2\theta^3/z_0\ne0.
\]

Pela regra graduada de Leibniz, ev_p(s₀F)=0 para todo polinômio de jatos de ordem finita no domínio. Coeficientes espectadores regulares são avaliados no mesmo B0. O teste não precisa que os quatro vetores formem uma subálgebra; s₀C=0. Tampouco é um mapa para o BRST **completo**: sc e os termos não lineares em h teriam de ser tratados, e não são anulados por esse argumento.

Se uma série formal em valência fosse primitiva de A₆ para s₀, seu coeficiente homogêneo de valência seis já seria uma primitiva. Esse coeficiente é local finito na classe Rees. Portanto não é necessário avaliar uma série infinita inteira em amplitude numérica. O teste é legítimo tanto para primitivas naturais quanto para primitivas coordenadas regulares nesse domínio.

## 5. Obstrução para a classe de C₅ e limites da conclusão

A [transgressão077](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md>), com seu [dicionário](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/DICIONARIO_CARTAN_DO_RECIBO_077.md>), fornece T=T≤5+t⁶α6+… e sT=A_P. Como s não diminui valência nesse fundo mínimo on-shell,

\[
 (sT_{\le5})_{[6]}=A_6-s_0\alpha_6.
\]

A₆ é s₀-fechado porque W0=0 dá W[1][L_Cg0]=L_CW0=0, enquanto s₀C=0. A avaliação não nula mostra [A₆]≠0 em H⁴(s₀), portanto nenhuma correção de valência seis remove o resíduo do representante T≤5.

Isso também impede levantar a **mesma classe** [T≤5] de H³(C₅): se um ciclo de C₆ restringisse a T≤5+sB, estender B como cocadeia finita a C₆ e subtrair sua fronteira produziria um ciclo que restringisse exatamente a T≤5. Seria contraditório com o resíduo acima. O argumento usa a sobrejetividade de cocadeias da truncagem, não presume sobrejetividade cohomológica.

Não encontrei extrapolação indevida na fonte. Ela conserva os limites necessários:

- Outras classes em H³(C₅) podem ter o mesmo líder cúbico e correções diferentes nas valências quatro/cinco; sua obstrução pode mudar.
- A não-exatidão em s₀ não afirma uma anomalia causal efetiva nem resolve a classificação do BRST completo.
- O teste usa a referência permitida φ0 constante; não calcula o grupo de toda referência, em especial φ0=id.
- Uma falha de levantamento específica não prova lim¹ não nulo, falha de Mittag–Leffler ou ausência de todos os levantamentos da linha CE.
- A pertença à classe Rees não demonstra o consumo pela hierarquia de normalização Q2, nem QME, carga interagente ou UV.

[DERIVED] O certificado matemático e a consequência específica C₅→C₆ são sustentados pelas contas acima. [REAL] O manifesto registra as fontes e os arquivos novos, sem executar os scripts lidos. Fontes congeladas e entrega077 permanecem intactas.
