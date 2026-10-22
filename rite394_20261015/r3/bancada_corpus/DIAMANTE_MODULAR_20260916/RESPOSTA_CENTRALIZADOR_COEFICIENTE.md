# Centralizador, resto modular e primeiro coeficiente

16/09/2026. Continuação da investigação, após a entrega V2. Esta nota não altera o programa canônico, o gate, nem o alcance da realização PRODUCT_TOWER.

## Resposta exata

[DERIVED] As hipóteses do enunciado não fornecem centralidade de R nem um primeiro coeficiente universal. Para N = M_ω, sob as condições de domínio necessárias:

    A ∈ N  ⇒  [K_ω,A] = 0  ⇒  [R,A] = −[K_ξ,A].

Logo, R age trivialmente sobre N se e somente se K_ξ age trivialmente sobre N. Esta é uma condição verificável; não se obtém sua satisfação só da existência da esperança preservante de ω.

[KNOWN] O centralizador é a álgebra fixa do fluxo modular (Hiai, Proposition 2.16). A esperança normal preservante do estado sobre essa álgebra existe por Takesaki, Theorem 6.6, para estado normal fiel. Fonte: https://arxiv.org/pdf/2004.02383 . Não confundir uma subálgebra meramente globalmente invariante pelo fluxo com esta álgebra fixa ponto a ponto.

A versão mais segura no contínuo é δ_R = δ_ω − δ_ξ em domínio comum; sobre N, δ_R = −δ_ξ. A diferença formal de dois geradores ilimitados não é automaticamente autoadjunta. Se K_ξ não implementa automorfismos da álgebra regional, nem sequer há um segundo fluxo regional completo para comparar. Comutadores em um domínio insuficiente não substituem comutação forte.

Comutar com N é pertencer ao comutante N′ (ou, para operador ilimitado, ter as projeções espectrais em N′). Pertencer a Z(N) exige também pertencer/ser afiliado a N. Se N = C I, a ação é trivial para qualquer resto: isso não demonstra geometricidade em observáveis não triviais.

## O teste completo na regularização matricial

Se ρ = Σ_a p_a P_a é fiel e p_a são valores distintos, então

    N = ⊕_a B(P_a H),
    N′ ∩ B(H) = Z(N) = {Σ_a q_a P_a}.

Assim, para K_ω = −log ρ,

    [R,N]=0 ⇔ [K_ξ,N]=0 ⇔ K_ξ = Σ_a q_a P_a.

Prova: comutar com cada projeção de base força K_ξ a ser diagonal; comutar com cada unidade matricial dentro de um bloco força os valores diagonais desse bloco a serem iguais. A volta segue por multiplicação. Essa caracterização, incluindo degenerescências, está em `commutes_with_preserved_algebra_iff`.

Não basta [K_ξ,ρ]=0. Isso só torna K_ξ bloco diagonal, podendo atuar dentro de um bloco degenerado. Controle exato: ρ=I/2, K_ξ=diag(1,0), A=σ_x. Todos pertencem ao centralizador M₂, mas [K_ξ,A]≠0. Se o espectro de ρ é simples, a condição reduz-se à diagonalidade. Esse caso especial não deve ser extrapolado a fatores de tipo III.

A parede E_ω(R)=0 não implica [R,N]=0 já foi provada na entrega V2 e NÃO é novamente implementada. Há uma razão adicional para não usar só leitura instantânea: com R=σ_x e A=σ_z,

    E([R,A])=0,
    E([R,[R,A]])=4 A,
    E(e^(−itR) A e^(itR))=cos(2t) A.

O primeiro sinal na leitura pode aparecer na segunda ordem embora a ação não central já exista na primeira. Tempo modular t e parâmetro de deformação ε são variáveis distintas.

## O coeficiente calculável: primeira e segunda variações

[DERIVED — prova escrita; controles numéricos, não formalização integral em Lean] Fixe UMA família regularizada fiel, com identificação dos espaços:

    ρ_ε = ρ₀ + ε B + ε² C + O(ε³),
    K_{ξ,ε} = Q₀ + ε Q₁ + ε² Q₂ + O(ε³).

Em dimensão finita, positividade estrita numa vizinhança permite diferenciar o logaritmo. Para G_u=(ρ₀+uI)⁻¹:

    R₁ = −∫₀∞ G_u B G_u du − Q₁,
    R₂ =  ∫₀∞ G_u B G_u B G_u du − ∫₀∞ G_u C G_u du − Q₂.

R₂ é o coeficiente de ε², não a segunda derivada (que vale 2R₂). Prova: usar a representação resolvente do logaritmo e expandir (ρ_ε+uI)⁻¹. Se o menor autovalor de ρ₀ é a>0, ||G_u||≤1/(a+u). Para |ε| ||B|| suficientemente pequeno, a série de Neumann converge e cada termo acima é dominado por uma potência integrável de (a+u)⁻¹. Isso justifica a integração termo a termo para a família matricial. Não transfere automaticamente a justificativa ao limite de tipo III.

Na base de ρ₀, o coeficiente universal do CÁLCULO do logaritmo é

    L(p_m,p_n) = (log p_m − log p_n)/(p_m − p_n), se p_m ≠ p_n;
    L(p,p) = 1/p.
    (R₁)_{mn} = −L(p_m,p_n) B_{mn} − (Q₁)_{mn}.

Prova escalar: integrar 1/((u+p_m)(u+p_n)) por frações parciais; no caso coincidente, integrar (u+p)⁻². O núcleo L é universal como regra matemática, mas os p_m, B e Q₁ são dados do problema físico. Ele não fornece um número universal, nem fixa β_TGL.

[KNOWN — comparação de alcance] Balakrishnan–Parrikar, https://arxiv.org/html/2002.00018 , Eq. (21) e §2: variações modulares de estados preparados por integrais de caminho contêm operadores transportados em tempo modular. A aplicação ali é a meias-regiões e, por simetria conforme, bolas de CFT. Não é uma expressão calculada para toda teoria interagente num espaço-tempo arbitrário.

## O centralizador também se move: o termo que não pode faltar

Para N_ε=M_{ω_ε}, não basta testar [R₁,A₀] e deixar N parado. Suponha que uma identificação diferenciável forneça A_ε∈N_ε:

    A_ε=A₀+ε A₁+ε² A₂+… .

A primeira obstrução à ação trivial é

    B₁(A₀) = [R₁,A₀] + [R₀,A₁].

Como [K_{ω,ε},A_ε]=0,

    B₁(A₀) = −[Q₁,A₀] − [Q₀,A₁].

A segunda é [R₂,A₀]+[R₁,A₁]+[R₀,A₂]. Se R₀=cI, o termo [R₀,A₁] desaparece. Se R₀ é central apenas em N₀, não se pode eliminá-lo. O balanço algébrico de primeira ordem e o transporte exato por conjugação estão em Lean; a existência de uma identificação diferenciável de centralizadores não é presumida.

Controle: U_ε=e^(−iεσ_x), ρ_ε=U_ερ₀U_ε†, R_ε=U_εR₀U_ε† e A_ε=U_εA₀U_ε†, com ρ₀ e R₀ diagonais. R_ε continua central em N_ε para todo ε. Entretanto, [R₁,A₀] pode ser diferente de zero: ele é cancelado por [R₀,A₁]. Um teste que não transporta a álgebra acusa falsamente perda de centralidade.

Se há quebra de degenerescência, o problema é ainda anterior: ρ₀=I/2 tem centralizador M₂; ρ_ε=diag(1/2+ε,1/2−ε), ε≠0, tem centralizador diagonal. A dimensão cai de quatro para dois sobre C. Não existe isomorfismo dessas álgebras que permita a comparação presumida. É preciso especificar um setor persistente ou outra regra, não escolher um coeficiente silenciosamente.

O modelo finito R_ε=c ε^m σ_x admite qualquer m≥1 e amplitude c, com [R_ε,σ_z]_{01}=−2c ε^m. É um contraexemplo à determinação da ordem/coefficientes APENAS pelas premissas algébricas; NÃO é um contraexemplo relativístico interagente construído. Esse limite de alcance fica explícito.

## Dependência em raio, curvatura e acoplamentos

[DERIVED — organização dimensional condicional] Numa expansão controlada em torno de um ponto fixo conforme UV em dimensão d, com deformação g_i O_i de dimensão Δ_i, aparecem combinações adimensionais g_i ℓ^(d−Δ_i), acoplamentos marginais correntes, ℓ² Riemann(x₀), ℓ³∇Riemann(x₀), além de termos mistos e logaritmos. Esses são parâmetros possíveis, não coeficientes calculados.

Os operadores/coefficientes exigem o estado regional, as dimensões dos campos, os correladores e coeficientes de OPE, a prescrição renormalizada do tensor de energia, a forma/região e o transporte escolhido. A curvatura no centro e o raio não determinam, em geral, o estado de uma região finita inteira. Uma ambiguidade puramente escalar não afeta comutadores; melhorias operatoriais do tensor podem afetar a carga e precisam ser fixadas.

[KNOWN] No vácuo conforme de uma bola de Minkowski, sob as hipóteses apropriadas, R é escalar e não há primeiro termo não central: Casini–Huerta–Myers, https://arxiv.org/html/1102.0440v2 . Interações não excluem esse caso. Fora dele, a universalidade não segue da completude UV.

[KNOWN — exemplo livre, não substitui o caso interagente] Cadamuro–Fröb–Minz, https://link.springer.com/article/10.1007/s00023-024-01508-0 , Eq. (4.15): a correção modular de pequena massa num intervalo bidimensional depende de mℓ, logaritmos e núcleos não locais. Não é um coeficiente universal nem cálculo do primeiro comutador no centralizador de uma QFT interagente.

Dois dados do enunciado são adicionais: hiperbolicidade global não fornece um Killing conforme exato para todo diamante; e não escolhe um vácuo canônico em todo espaço-tempo. Ver Jacobson–Visser, https://arxiv.org/html/1812.01596v3 , para diamantes maximamente simétricos, e Fewster–Verch, https://arxiv.org/abs/1106.4785 , para limites de uma escolha natural universal de estados, sob suas hipóteses. Se ξ é aproximado, sua ordem de aproximação participa de R.

## Relação com a TGL e escopo da investigação

O Atlas atualizado registra a incorporação V2 na v358. Isso é [DECLARADO na memória consultada]: a tentativa desta rodada de leitura direta do manifesto/kernel canônico encontrou caminho não disponível/acesso negado; não houve reexecução canônica. A bancada reutiliza as fontes e evidências próprias anteriores, sem duplicar a torre, o canal ou o cociclo. O critério `stationary_generator_balance` e a stationariedade global já estavam provados.

A leitura parcial positiva de PRODUCT_TOWER da V2 permanece válida no seu enunciado. Não se deve substituí-la pelo centralizador completo. A identificação física com Q_{ξ,D} continua uma obrigação distinta. O nome ontológico “inércia” pode designar a correção de transporte [ONTO]; os resultados aqui não identificam R com massa inercial, dissipação ou um valor universal de β.

[OPEN] Não há nesta entrega uma solução verificada da gravidade quântica, nem cálculo de R para a teoria física interagente completa no UV. A pergunta matemática foi reduzida a critérios e coeficientes explícitos; realizar esses coeficientes fisicamente exige uma família definida de álgebras/estados/cargas e um controle de seu limite. A meta ampla permanece ativa, sem mudar sua definição para coincidir com os testes finitos.
