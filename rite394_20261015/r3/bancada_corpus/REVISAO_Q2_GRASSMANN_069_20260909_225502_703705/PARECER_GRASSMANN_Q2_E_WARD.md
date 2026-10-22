# Parecer independente sobre ação Grassmann e Q2 — arco 069

09/09/2026. [DERIVED — revisão matemática escrita] [REAL — leitura de arquivos e pins] [KNOWN — fontes primárias consultadas].

**Parecer:** não identifiquei erro material nas duas notas examinadas. A apresentação graduada e os dados livres satisfazem os contratos necessários para aplicar a construção causal e a identidade de Ward anômala ao multiplet métrica–sigma–fantasmas descrito. O resultado de Q2 é existência formal dos produtos e da álgebra interagente auxiliar, com anomalia local consistente. Não equivale à remoção da anomalia, à construção do quociente físico interagente ou a independência entre fundos.

## 1. Escopo e fontes

Foram lidos integralmente:

- [DICIONARIO_GRASSMANN_E_ACAO_BV.md](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md>);
- [PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md>).

A revisão aproveita a leitura anterior das demonstrações de Jacobi, BRST completo e Feynman 068; não repete a redução ADM ou todos os modos. Foram reabertas as fontes primárias de Hollands e Fröb nos trechos indicados abaixo. Outro agente desta tarefa leu também o dicionário e conferiu suas matrizes, realificação e férmion de gauge; a presente revisão das importações Q2 foi realizada aqui. Não se atribui aprovação externa ou do operador.

## 2. Hessiana graduada, Green e reciprocidade

Para J=diag(1,1,1,−1), a identidade P_gr=LJ converte os dois blocos ghost simétricos de L em (0,−Q;Q,0). Com campos ímpares e Q transposto por integração por partes,

\[
\frac12(-cQ\bar c+\bar cQc)=\bar cQc.
\]

Assim a ação (2) realmente produz a Hessiana bilinear graduada indicada. Não é necessário, e seria inadequado, interpretar LJ como uma congruência ordinária de uma forma bilinear. A nota distingue expressamente essa operação.

Os inversos JG_L fecham à esquerda e à direita:

\[
(LJ)(JG_L)=LG_L=1,\qquad
(JG_L)(LJ)=J(G_LL)J=1.
\]

A entrada c–barc do Green é G_Q e a entrada barc–c é −G_Q, com a reciprocidade graduada requerida. O mesmo cálculo vale para Feynman e preserva os contatos mistos, inclusive o cancelamento do complemento de Schur em b–b.

Na realificação, usando E real,

\[
\widehat W^+-\widehat W^-
=\tfrac12[(W^+-W^-)-\overline{(W^+-W^-)}]
=i\hbar E.
\]

A conjugação troca a orientação microlocal; portanto cada média conserva a orientação apropriada. Hermiticidade mais \(\widehat W^-=\overline{\widehat W^+}\) dá \(\widehat W^-=(\widehat W^+)^{\rm t}\). Nas matrizes completas, transpor JΛ⁺ troca os slots ghost e gera exatamente os sinais de JΛ⁻. Assim o anticomutador ghost é iħE_gr no bloco correspondente; o setor bosônico mantém o comutador usual. A restrição física 067 já obedece à relação real e não é alterada pela média.

A involução c*=c, barc*=−barc torna barcQc real por reversão da ordem dos fatores e integração por partes. Para o diferencial ímpar, a compatibilidade com essa involução deve ser entendida graduadamente: em geradores homogêneos, s(X*)=(−1)^{p(X)}(sX)*. Ela é satisfeita pelas transformações apresentadas; exigir uma igualdade não graduada no antighost introduziria um falso conflito de sinais.

## 3. BRST livre e gauge fixado não linear

JγJ produz s₀barc=−b, s₀u=Kc, s₀c=s₀b=0. A variação bosônica é bCKc; a variação ghost é −bQc. Elas se cancelam porque CK=Q e HK=0. O diferencial é nilpotente fora das equações.

As entradas mistas das contrações também conferem: s₀(u barc) tem contração K W_Q⁺−W_{ub}⁺=0; s₀(barc u) tem −W_{bu}⁺−W_{barc c}⁺K*=0. Os sinais de Grassmann e as Ward livres são ambos necessários. A introdução de anticampos externos sem contrações é coerente com o formalismo livre: os termos u‡Kc−barc‡b geram esse diferencial e a parte Koszul–Tate por uma única ação BV quadrática. Invariância e nilpotência estabelecem sua equação mestra clássica.

A férmion Ψ=−barc(Ch−b/(2ℓ)) fornece bCh−b²/(2ℓ)+barc C(sh), inclusive o sinal do termo ghost. Sua parte quadrática coincide com os dados livres; o termo barc C L_c h é uma interação de valência superior. O sigma já participa da Hessiana acoplada e dos termos de anticampos, sem exigir uma nova escolha artificial de C.

O auxiliar b permanece no contrato por seus kernels mistos e contatos. Como não aparece nos vértices internos de interação sem anticampos deste gauge, não se pretende aplicar o teorema de ondas a um novo propagador ultralocal independente. Os anticampos, por sua vez, são fontes externas. Isso é suficiente para o setor de interações usado; não se afirma um resultado automático para qualquer gauge não linear diferente.

## 4. A importação de produtos não se limita a escalares

[KNOWN — conferido na fonte] [Hollands, §3.5](https://arxiv.org/pdf/0705.3340) inclui explicitamente multipletos escalares ou tensoriais que satisfazem sistemas de ondas com coeficientes locais covariantes e a extensão Grassmann. O Teorema 2, ao final do §3.6, afirma existência dos produtos T1–T11 e caracteriza sua liberdade local. T11 é a identidade da ação por partes, não uma proibição de contatos das equações de campo. O §3.5 também distingue ghost e antighost independentes; suas convenções com fator i são compatíveis com o dicionário explícito da nota.

A aplicação ao modelo está efetivamente justificada pelos seguintes fatos particulares:

- O bloco D é normalizado por uma forma de fibra invertível a um sistema de ondas de símbolo escalar no fibrado de posto 13; o bloco Q é um sistema de ondas de posto 4. As normalizações permanecem nos kernels. Uma forma de fibra indefinida nos setores não físicos não impede a extensão distribucional.
- A expansão Exp_{φ̄}(tξ) vive no fibrado φ̄*TS³. Em cada grau t seus coeficientes são tensores locais finitos. A conexão de pullback, o endomorfismo de Jacobi e o acoplamento de primeira ordem com h entram nos coeficientes de transporte de Hadamard, sem criar um símbolo principal de outro tipo.
- A extensão Lorentz covariante dos kernels universais é compatível com os índices finitos de fibra. O transporte paralelo permite comparar as fibras nas cartas; as mudanças de carta alvo são mudanças de apresentação desses mesmos tensores. Não se exige uma única carta contendo φ̄(M).
- A classe completa de contra-termos EFT foi admitida. A cada grau fixado de flutuações e ordem perturbativa, a valência e a ordem de jato são finitas. Não se impõe um fechamento falso apenas nos parâmetros originais.

A categoria de naturalidade deve transportar todos os dados de fundo, conforme a nota exige: ḡ, φ̄, conexões, pareamentos e operadores. Isso é uma construção covariante nos dados, e não um teorema de independência quântica da escolha de fundo. O caráter on-shell do fundo físico é usado no sistema livre BV; a expansão não é levada a um fundo plano escalar diferente.

Não encontrei aqui um contrato escondido que restringisse a importação a um único campo escalar ou a uma ação renormalizável por contagem de potência. As restrições reais são as que a nota mantém: sistema de ondas e dados locais, suporte compacto interior, expansão formal e classe EFT suficiente.

## 5. Recorrência causal e anomalia local

A fatorização fora da diagonal total utiliza produtos de ordens inferiores; as diagonais parciais já estão resolvidas nessa etapa. As ambiguidades de extensão têm o limite de derivadas de δ indicado pela codimensão 4(n−1). Para obter covariância, a nota importa a expansão de escala local e a extensão tensorial, em vez de atribuí-la a um corte arbitrário em coordenadas. Curvaturas e dados de pullback entram nos coeficientes locais. A simetria graduada, realidade e identidade da ação por partes são parte do contrato importado.

[KNOWN — conferido na fonte] [Fröb, §2](https://arxiv.org/pdf/1803.10235) trabalha com campos de paridade geral em somas de fibrados, ação quadrática graduada com Green exatos e contrações Hadamard. O Teorema 3 exige uma derivação local covariante que preserve suportes e fornece a quebra A=O(ħ), com suporte na diagonal e graduação. O Teorema 6 identifica o termo clássico de ordem dois com o antibracket; as identidades livres de Green e de dois pontos são necessárias e aparecem explicitamente antes dele. O Teorema 7, incluindo sua extensão ao diferencial livre completo, fornece a consistência; a equação (154) é a forma usada na nota.

Essas exigências são satisfeitas pelo S₀ BV e pelas Ward conferidas acima. O diferencial em qualquer representação de Wick acompanha a mudança suave de ordenação; a covariância abstrata não é definida pela escolha global dos modos do estado. Portanto a dependência global do representante Hadamard não transforma o operador local de BRST em uma operação não local sobre a teoria abstrata.

O objeto obtido é A(e^V), e não uma afirmação de A(e^V)=0. Se A(e^V) começa em ħ^N depois de removidas as ordens anteriores, a inserção A(A(e^V)⊗e^V) começa em ħ^(N+1), porque o mapa externo A começa em ħ. Com a equação mestra clássica válida na região de cutoff constante, a consistência dá sa_N=0 modulo d. Os termos onde o cutoff varia não são apagados globalmente; estão fora da região local de observação escolhida.

O passo a_N=sB_N+dD_N ainda exige a cohomologia e primitivas admissíveis. Nem Hollands §3.5 nem os teoremas gerais de Fröb fornecem essa conclusão específica para o sigma. As notas examinadas não fazem essa promoção.

## 6. Contagem perturbativa e alcance de Q2

A identidade I−V+1=L dá δ=2+2L+Σ(d_v−2) quando os propagadores internos relevantes têm comportamento de onda; vértices e inserções com derivadas distribuem essa ordem entre pernas e coeficientes de fundo. Ela é uma cota para a extensão, não um cálculo de coeficientes não nulos. A nota permite termos de zero, uma ou duas pernas nos contra-termos de laço e mantém a ordem em ħ. Isso evita usar indevidamente a valência mínima da ação inicial para proibir tais termos.

O fator ħ/i na definição do mapa relativo fornece R₀(F)=T₁(F). Fatorização causal e suportes compactos justificam a álgebra local auxiliar pelo limite adiabático algébrico. Não se extrai um limite de estados, espalhamento global ou convergência a partir dessa construção.

**Resultado admitido da revisão:** Q2 — existência formal dos produtos temporais locais/covariantes, campos interagentes auxiliares, quebra local e consistência — está sustentado no modelo e na classe EFT especificados, por composição de demonstrações e importações com os requisitos acima. Nenhum erro material foi identificado nesse alcance. A escolha de renormalizações finitas continua uma liberdade declarada, não uma lacuna na existência.

**Permanecem distintos e abertos:** remoção cohomológica da quebra, QME interagente satisfeita, quociente físico interagente, estado interagente positivo, independência entre fundos, anomalias globais e rota UV. A revisão não audita uma quantização independente dos dados probabilísticos redundantes.

## 7. Custódia

Foram criados apenas este parecer e seu manifesto em pasta nova Chatgpt. Nenhum arquivo existente foi alterado, nenhum um.py importado/executado, e nenhum Lean ou CAS foi executado. Os pins das duas notas foram medidos antes e depois da escrita dos novos artefatos; sua igualdade é registrada no manifesto.

- `C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md` — 7610 bytes; SHA-256 `5cefd0a1be321e426627d9ad14a5cf1c788b98a4456d2190d1ba5932a7698124`.

- `C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md` — 16140 bytes; SHA-256 `7884a4da5030c5befdad567cff75f4011add1a571a1bb36dee7e9da5a39b6676`.
