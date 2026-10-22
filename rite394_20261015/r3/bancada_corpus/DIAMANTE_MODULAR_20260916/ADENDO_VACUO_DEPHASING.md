# Vácuo, dephasing e a ponte entre fluxos

16/09/2026. Adendo solicitado pelo operador antes de encaminhar o handoff.

[INPUT — trecho literal] “vácuo=dephasing, portanto, a teoria que vc busca unir é por identificação a TGL, é a própria torre”.

[INPUT — hipótese literal a examinar] “O dephasing proposto pela TGL preserva a referência de vácuo e suprime, no setor identificado, precisamente as contribuições que impedem a correspondência geométrica.”

O restante da mensagem distingue estado, canal, conteúdo preservado e pede demonstrar a ação sobre o resto e a igualdade dos fluxos. Este arquivo registra a resposta matemática. A identificação ontológica é preservada como [ONTO]; a identificação de um vácuo físico regional com um estado concreto da torre precisa conservar seu enunciado e alcance.

## Resultado principal

Há uma ponte exata entre dephasing e igualdade de ações modulares. **O critério é a ação do resto sobre a álgebra preservada. Não é o valor do resto após a leitura.** Há duas realizações diferentes, que não devem ser trocadas silenciosamente:

1. O dephasing espectral completo do próprio estado tem imagem estacionária para seu fluxo modular. Isso vale nos andares da torre e para a esperança global já construída.
2. Um dephasing parcial pode preservar movimento não trivial e tornar invisível a ação do resto. Foi construída uma realização em cada andar produto da torre, sem alterar os pesos originais.

Nenhuma dessas afirmações identifica automaticamente a referência remanescente com uma integral local de T contra um campo de vetores do diamante. A entrega prova igualdade entre ações especificadas; o nome “geométrica” ainda exige essa identificação.

## A. O que a definição completa prova

Na regularização, K=-log rho e E_K(X)=sum P_a X P_a. Positividade estrita torna iguais as decomposições espectrais de rho e K, inclusive suas degenerescências. A implementação existente `TGLExt.specExpect` já efetua essa leitura na base diagonal. Não foi criado outro canal.

[REAL — Lean] `spectral_preserves_every_diagonal` demonstra que E_K fixa toda matriz diagonal nessa base. Em particular fixa rho, mas não o seleciona unicamente. `spectral_preserves_modular_generator` demonstra E_K(K)=K, incluindo o gerador inteiro. A igualdade

    K = Q + C I + R

implica, por linearidade,

    K = E_K(Q) + C I + E_K(R).

Não implica E_K(R)=0. A versão formal `spectral_preserves_remainder_balance` absorve C I em Q; `specExpect_one` fornece sua separação.

O kernel anterior já prova `sigma_fixed_specExpect` e `sigma_fixed_iff_specExpect`, com pesos degenerados permitidos. Logo, para N=Ran E_K:

    sigma_t(X)=X para todo X em N e todo t.

[REAL — aplicação nova] `spectral_reading_is_stationary` prova que a igualdade sigma_t|N=alpha_t|N equivale a alpha_t|N=id. Assim, **uma ação geométrica não trivial nesse mesmo conjunto não pode coincidir com o fluxo modular que E_K tornou estacionário**. Isso não nega transformação de observáveis fora de N nem transporte entre regiões; impede confundir esses objetos.

[REAL — torre global, se certificado no manifesto] `existing_tower_dephasing_is_stationary` aplica a conclusão ao operador `aperiodicExpectation P` existente. Usa sua identidade em cada prefixo, a comutação das esperanças dos andares com o fluxo, o fluxo matricial já identificado e o limite GNS. Não pressupõe stationariedade como campo de um contrato. `existing_tower_flow_bridge_iff_stationary` fornece o mesmo critério para qualquer ação de comparação no fator. A preservação do conjunto da tela, registrada anteriormente, não foi confundida com essa fixação ponto a ponto.

## B. Por que apagar R não basta — controle que pode falhar

Considere K=diag(0,2), R=[[0,1],[1,0]], Q=K-R e p=diag(1,0). A normalização de exp(-K) apenas acrescenta um escalar ao gerador, sem mudar os fluxos.

    E_K(R)=0, E_K(p)=p, [K,p]=0, mas [R,p]≠0 e [Q,p]≠0.

[REAL — Lean] `erased_remainder_counterexample` verifica exatamente as duas leituras e a não comutação, sem tolerância numérica. `generator_bridge_iff` liga essa não comutação à diferença dos geradores das ações.

[REAL — cálculo finito] Em t=0,61 o controle mede norma da diferença de fluxos aproximadamente 0,75958; mesmo após a leitura final a diferença é aproximadamente 0,40798. Os números exatos da execução constam de `DEPHASING_NUMERICAL_CHECKS.json`. Portanto, a leitura inicial/final não elimina excursões intermediárias para fora do setor. A evolução com projeções continuamente intercaladas seria outro problema dinâmico; não substitui o fluxo original por decreto.

## C. A ponte positiva construída

Na base comum, tome geradores diagonais Q=diag(q_i), R_0=diag(r_i) e K_0=Q+R_0. Normalize:

    rho_i = exp(-(q_i+r_i))/Z,
    sigma_i = exp(-q_i)/Y.

O resto normalizado é R=diag(r_i)+(log Z-log Y)I. A esperança E_r mantém X_ij precisamente quando r_i=r_j. Ela é, portanto, espectral para o resto e geralmente MAIS AMPLA que E_K.

Para cada entrada preservada,

    log rho_i-log rho_j = -(q_i-q_j)
                        = log sigma_i-log sigma_j.

Multiplicar X_ij pela fase modular fornece, em TODO tempo real:

    sigma_t^rho(E_r X) = sigma_t^sigma(E_r X).

[REAL — Lean] `coarse_dephasing_flow_bridge` prova a igualdade, com Z,Y positivos arbitrários e sem identificá-los. `coarse_preserves_vacuum` prova E_r(rho)=rho; `coarse_remainder_is_invisible` prova [R_0,E_r(X)]=0. O resto sobrevive: E_r(R_0)=R_0. **Ele não interfere na ação preservada porque é central nessa álgebra de blocos.** Pode não ser escalar na álgebra inteira.

O caso q_i diferente de q_j dentro de um mesmo bloco conserva uma fase variável e, portanto, movimento não trivial. Essa possibilidade é verificada numericamente sobre uma base completa de matrizes; não é reivindicada como identificação física espacial.

## D. Aplicação aos mesmos pesos de PRODUCT_TOWER

O objeto existente satisfaz

    towerW(P,N+1)(i,a) = towerW(P,N)(i) * siteW(P.w(N+1))(a).

Defina b_a=siteW(P.w(N+1))(a). Todos os pesos são positivos, e suas somas são um. Leia SOMENTE o último sítio pela esperança existente `specExpect (fun (i,a) => b_a)`. Compare com a referência

    rho_ref(i,a) = towerW(P,N)(i)/2.

Esta referência conserva o andar anterior e usa peso (1/2,1/2) no último sítio. Também é normalizada. O resto é

    R(i,a) = -log(2 b_a),

constante em cada bloco preservado. Segue a igualdade dos fluxos na imagem dessa leitura para **todo perfil admissível P, todo N e todo t**.

[REAL — Lean] `product_dephasing_flow_bridge`, `tower_last_site_flow_bridge` e `tower_last_site_reference_normalized`. A conclusão usa literalmente `towerW`, `siteW`, `rhoD`, `sigma` e `specExpect` já existentes. Nenhuma nova torre foi definida. A leitura parcial é uma aplicação específica do mapa genérico, não uma reinterpretação silenciosa da esperança global centralizante.

[REAL — 30 controles numéricos] Perfis de dois, três e quatro sítios: normalização, preservação do estado, sobrevivência de resto não escalar, comutação em toda a base, igualdade dos fluxos em três tempos e movimento não trivial preservado. Erro máximo de igualdade nos perfis testados < 9e-16. Os testes incluem o contraexemplo B. Essa faixa finita é verificação numérica; a quantificação em N vem do termo Lean.

## E. O alcance físico e o sentido de inércia

[DERIVED] O critério infinitesimal, para K=Q+R, é

    [K,X]=[Q,X]  se e somente se  [R,X]=0.

Está em `generator_bridge_iff`. Para passar de geradores a fluxos gerais é necessário preservar o domínio/álgebra ao longo da órbita. No caso diagonal construído, a prova por fases resolve isso para todo t; não foi usada apenas uma derivada em zero. Para ações gerais, o pacote anterior dá o critério exato pelo cociclo em todo tempo e pela invariância do canto.

[ONTO] A interpretação “inércia” pode nomear a parcela que permanece sem produzir diferença na ação observada. Na ponte C/D isso significa concretamente R no comutante da álgebra preservada. O resto, sua leitura e o gerador dissipativo Gamma(E-id) continuam tendo tipos distintos. Não foi demonstrada identidade com massa inercial ou com um operador físico universal do zero absoluto.

[OPEN — identificação específica, sem reabrir o gate interno] Para chamar o fluxo de referência de C/D de geométrico no diamante físico, é preciso ligá-lo ao Q_{xi,D} feito do tensor de energia, no MESMO modelo/região/estado e representação. O teorema da torre não fornece essa integral por trocar seu rótulo. Se essa identificação já existe no acervo, a gerência deve apontar e aplicar seu termo com hipóteses, sem acrescentar outra camada. Se não há tal termo, deve manter a identificação física aberta. A igualdade entre a álgebra abstrata de tipo III e uma álgebra regional, sozinha, não identifica estados, rede de regiões ou tensor de energia.

O dephasing completo proposto pelo operador fornece um teorema de stationariedade. O parcial fornece uma ponte não trivial entre fluxos especificados. Ambos entram na entrega com seus critérios e controles; nenhum altera automaticamente o gate do um.py.
