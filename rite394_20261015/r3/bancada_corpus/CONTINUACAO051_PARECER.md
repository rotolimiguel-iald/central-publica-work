# Continuação051 — balanço óptico finito e curvatura variável

[REAL — escopo das declarações compiladas e auditadas] UTC: 2026-09-07T03:54:04.773513+00:00

A correção finita de Clausius do modelo041/043 recebe uma lei integral exata, construída a partir da expansão e do cisalhamento da tela. A correção é definida diretamente pelos dados ópticos, independentemente do calor e do resíduo. O lote também identifica o termo adicional que impede transportar sem alteração a fórmula de Ricci constante para Ricci variável. H3 e a reconstrução gravitacional geral permanecem OPEN.

## Balanço integral geral

Num intervalo aberto convexo I contendo zero, assumir as derivadas A'=Aθ, θ'=−R−F, Q'=−K t M(t)A(t), com θ(0)=Q(0)=0 e a continuidade indicada nos enunciados. Definir:

    Z_f(t) = ∫₀ᵗ f(u)du,
    E_F(t) = ∫₀ᵗ A(s) Z_F(s)ds.

O teorema optical_volterra_balance demonstra:

    Q(t) − K(A(t)−A(0))
      = K ∫₀ᵗ A(s)[Z_F(s)+Z_R(s)−s M(s)]ds.

São hipóteses de evolução e dados iniciais explícitos. A e Q não são reconstruídos de um estado quântico neste lema. Nenhuma positividade de A é necessária para essa identidade algébrica-integral.

Se R=M ponto a ponto, permanece o drift Z_R(s)−sR(s). Só no caso de R=M=r constante ele desaparece, dando Q−KΔA=K E_F. O controle R(t)=r+vt calcula exatamente drift=−v t²/2, com ambos os sinais conforme v. Esse é um controle escalar da parcela de curvatura; não afirma que toda função R escolhida já vem de uma geometria fisicamente selecionada. O sinal pontual do drift tampouco determina sozinho o sinal da integral orientada.

## Tensor óptico e convenção do cisalhamento

Para B=[[x,z],[z,y]], em uma tela real ortonormal de dimensão dois:

    θ = tr(B) = x+y,
    F = tr(B²) = x²+2z²+y²
      = θ²/2 + 2[((x−y)/2)²+z²].

O nome Lean opticalShearNormSq significa ((x−y)/2)²+z²: METADE da norma quadrática do tensor sem traço. Assim, a norma inteira chamada shearNorm na derivação prévia é 2*opticalShearNormSq. O fator dois não é ajuste posterior da identidade.

O traço do sistema B'=−B²−Rmat produz θ'=−tr(Rmat)−F. A norma, o traço e a parcela de cisalhamento são invariantes sob as rotações explícitas OBOᵀ, com c²+s²=1. O sistema inclui as três componentes independentes da matriz simétrica, e sua conexão ao balanço integral está provada no controle com traço Ricci constante.

[INPUT] Essa formulação trabalha no setor simétrico, sem torção óptica. Não é um teorema para toda congruência arbitrária com vorticidade. A base ortonormal, a tela e as equações ópticas continuam dados.

## Instância geométrica e sinal

Na tela036/043, f_a(t)=cos(√a t), q_a=f_a'/f_a e A(t)=|f_a(t)f_c(t)|. Em um intervalo aberto convexo contendo zero, sem zeros de f_a ou f_c, instanciar:

    θ=q_a+q_c,   F=q_a²+q_c²,
    E(t)=∫₀ᵗ A(s)∫₀ˢ(q_a(u)²+q_c(u)²)du ds.

Sob a,c≥0 e a hipótese explícita eta*(a+c)=2π*mass, o calor041 satisfaz:

    opticalClausiusDefect(t) = (rate/(2π))*eta*E(t).

[INPUT] Q herda o peso afim −rate*t do protocolo041. Identificar esse fluxo finito com calor de um horizonte físico exige justificativa adicional; o lote não demonstra uma escolha canônica exata de campo de Killing ou de temperatura.

A transferência para o calor construído geometricamente na043 está demonstrada somente no germe passado já identificado ali. O enunciado intervalar do calor041 não foi usado para estender artificialmente o calor043 para tempos ou domínios ainda não relacionados.

E≥0 nos dois sentidos de tempo, porque as duas integrais orientadas invertem juntas. No contexto regular da identidade, as funções são contínuas e as integrais finitas. Os lemas de positividade abstrata, isolados e sem hipóteses de integrabilidade, usam a integral totalizada do Lean; eles não autorizam uma leitura física através de cáusticas.

O limite bilateral perfurado, para t→0 com t≠0, é E(t)/t⁴ → (a²+c²)/12. Sua prova usa a identidade geométrica e o limite041 com uma especialização auxiliar de parâmetros que fixa K=1; não introduz uma nova seleção física desses parâmetros. O resultado recupera precisamente o resíduo de ordem quatro conhecido.

Para o segmento orientado t→0, ΔS=eta*(1−A(t)) e Q_segmento=−Q(t). Com T≠0, a identidade corresponde a:

    ΔS = Q_segmento/T + eta*E(t).

O lema de orientação é algébrico e exige T≠0; a temperatura física positiva é uma identificação adicional. Para T=0, o controle devolve apenas Q=0. Chamar eta*E de produção FÍSICA de entropia exige justificar a identificação de área, entropia e temperatura.

[KNOWN — contexto externo] A termodinâmica de horizontes fora do equilíbrio e a discussão de dissipação gravitacional aparecem em [Eling–Guedens–Jacobson2006](https://arxiv.org/pdf/gr-qc/0602001) e [Chirco–Liberati2010](https://arxiv.org/pdf/0909.4194). Esses artigos contextualizam a pergunta; não são usados como prova Lean nem demonstram a interpretação física de E neste modelo.

## Verificação e custódia

| Módulo051 | Teoremas | Definições | Instâncias | Prints | Alcance |
|---|---:|---:|---:|---:|---|
| [OpticalVolterraBalance.lean](<C:/IALD/Central de Patentes/Chatgpt/OpticalVolterraBalance.lean>) | 12 | 3 | 0 | 15 | Identidade integral geral, drift de Ricci e positividade bilateral. |
| [OpticalRiccatiInvariant.lean](<C:/IALD/Central de Patentes/Chatgpt/OpticalRiccatiInvariant.lean>) | 13 | 4 | 0 | 17 | Tensor óptico simétrico, traço de Riccati e invariância por rotação. |
| [OpticalFiniteBalance.lean](<C:/IALD/Central de Patentes/Chatgpt/OpticalFiniteBalance.lean>) | 11 | 3 | 0 | 14 | Instância da tela036/043, calor041 e limite quártico da correção. |
| [OpticalBalanceControls.lean](<C:/IALD/Central de Patentes/Chatgpt/OpticalBalanceControls.lean>) | 9 | 0 | 0 | 9 | Ricci afim, ligação matricial ao balanço e orientação térmica. |

Total051: 45 teoremas, 10 definições, 0 instâncias, 55 prints. Compilação conjunta: 5/5 etapas, incluindo importador. Zero avisos/erros, cobertura exata das declarações e somente propext, Classical.choice e Quot.sound. A revisão independente liga-se ao hash e ao diretório final.

Diretório final: C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO051_CLEAN_20260907_034646_061873

Build SHA256: a05d7d00976b75e9b5c9f998c8e1c9d68fabfb5c5cdbba67cebdea89c03db607

Os quatro fontes051 foram copiados por bytes e compilados em diretório exclusivo. Dependências históricas até043 foram reutilizadas por cópias pinadas; o auditor verifica os contratos e os vínculos históricos registrados, sem rebatizar seus binários como recompilados nesta rodada. A fronteira externa inclui imports diretos e companheiros Mathlib/stdlib; não foi reconstruído ou hashado exaustivamente todo o fecho transitivo externo. Fontes locais sem pin histórico têm hash de leitura para descoberta de imports; isso sozinho não estabelece proveniência fonte–binário.

Sondas falhas, logs e backups permanecem guardados como histórico documental. Não sustentam declarações de prova.

## Caminho ainda aberto

[OPEN] Selecionar a álgebra, o estado, o fluxo físico e a geometria; justificar a área/entropia e o casamento Ricci–matéria; tratar curvatura geral, dados ópticos mais gerais e a reconstrução gravitacional. O balanço finito explica uma correção na geometria já dada, mas não deriva a hipótese de H3 da teoria quântica.

A [nota sobre área covariante](<C:/IALD/Central de Patentes/Chatgpt/NOTA051_AREA_COVARIANTE_PENDENTE.md>) propõe uma família por E e I−E com pesos relativos distintos mesmo após normalização. Ela permanece [DERIVED — análise pendente], com obrigações formais explícitas; não pertence ao censo de teoremas051.

Escritas somente em Chatgpt; nenhuma incorporação em um.py, kernel, Atlas, índice ou memórias canônicas. canonical_gate_changed=false descreve o escopo desta rodada, não uma auditoria de alterações por terceiros. QG não está declarada confirmada, resolvida ou provada.

Revisão: [CONTINUACAO051_REVISAO_INDEPENDENTE.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO051_REVISAO_INDEPENDENTE.md>). Entrega: [ENTREGA_051_balanco_optico_finito.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_051_balanco_optico_finito.md>).
