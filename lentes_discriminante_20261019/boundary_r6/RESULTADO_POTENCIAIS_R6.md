# R6 — resposta métrica e ponto de fechamento ainda ausente

19/10/2026, codex-gerente-tgl; F8.LENTES_5SIGMA_20261019, reivindicação1009. [DERIVED condicional / OPEN no problema físico completo].

## 1. Fonte e ramo explicitamente delimitado

O Custo vigente escreve R/(2 kappa²)+xi R|Psi|², xi=1/6. Na convenção F R/2, isso corresponde a F=1/kappa²+2xi|Psi|². O cálculo abaixo trata Psi como escalar e F como escalar independente da métrica na variação. **Não identifica automaticamente esse escalar com a 1-forma Psi_mu de outro termo do artigo.** Se |Psi|² for uma contração métrica de uma 1-forma, sua variação acrescenta termos que este cálculo não contém.

Hipóteses adicionais do ramo: fundo escalar constante, F0>0; perturbação f=deltaF; regime local estático e de campo fraco; V(background)=Vprime(background)=0; stress cinético escalar de segunda ordem; matéria não relativística com pressão desprezível; ausência de fonte modular/anisotrópica adicional na ordem estudada. Condições de contorno isoladas eliminam as liberdades homogêneas. São condições de cálculo, não afirmações de que todas se realizam numa lente TGL.

SOURCE_BOUNDARY_R6.json localiza as hipóteses P1–P4 da Face C na Ponte1530–1544 e o alcance linear1550–1558; T1 vigente exige M_phi=C1. Isso não fornece uma solução radial. O Custo10422–10455 apresenta a equação de Psi e K_boundary tendendo a zero longe da fronteira, mas a passagem geral operador–fonte permanece conjectural na fonte. Os enunciados Lean de Clausius recebem métrica, stress e H3; não constroem um perfil estático de lente.

## 2. Derivação conjunta dos dois potenciais

Em c=1 e assinatura (-+++), use

    ds²=-(1+2U)dt²+(1-2V)dx²,
    F=F0+f,
    F0 G_ab^(1)=T_ab+partial_a partial_b f-eta_ab box f.

Com T00=rho e Tij=0, o cálculo direto do tensor linearizado dá

    G00=2 lap V,
    Gij=partial_i partial_j(V-U)+delta_ij lap(U-V).

Se W resolve o problema de Poisson lap W=rho/(2F0), então

    U=W-f/(2F0),
    V=W+f/(2F0),
    U+V=2W.

O script constrói Ricci e Einstein a partir da perturbação h, substitui esses campos e verifica exatamente as dez componentes independentes. **É solução do subsistema métrico para f fornecido. Não é solução da equação escalar que determina f.**

## 3. Atraso por trajetória e leitura estelar

U e V são adimensionais. Restaurando c, a condição nula dá

    dt=[1-U-V] dl/c + O(potencial²).

Para uma lente localizada e estática, a parte gravitacional da diferença de tempo observada é

    Delta t_grav,ij = -2(1+z_l)/c [integral_i W dl-integral_j W dl].

O termo geométrico, os caminhos estacionários e os fatores de distância também integram o atraso total. O cancelamento de f na soma implica que, **a matéria e F0 fixos, neste ramo e nesta ordem**, não há excesso direto de atraso ou deflexão por f. Isso não cancela mudanças na distribuição de matéria, em F0, no fundo cosmológico, fontes modulares, stress não linear ou condições de contorno.

Estrelas não relativísticas leem outro objeto:

    aceleração = -c² grad U = -c² grad W + c² grad f/(2F0).

Portanto a massa inferida da cinemática não pode ser usada como se f fosse conhecido ou nulo. A relação cinemática/lente pode restringir f quando seu perfil e o modelo estelar estiverem especificados. Também não se pode igualar 1/(8 pi F0) a G medido sem analisar a calibração local.

## 4. O que falta é uma equação operacional por lente, não um novo critério lógico

O acervo recuperado ainda não fornece, neste recorte, o mapa que toma fonte de matéria e condições físicas e devolve Psi(x), F(x) e o stress modular da lente com normalização fixa. Saber que a leitura deve preservar a identidade é um critério de satisfação; o cálculo precisa mostrar qual solução satisfaz as equações e esse critério no espaço-tempo da lente.

O contrato concreto restante é:

1. Especificar qual campo entra em cada termo e como sua norma varia com a métrica, reaproveitando a construção já escrita se existir.
2. Instanciar V e K_boundary no problema espacial da lente, com fonte e condições de contorno; K_boundary→0 sozinho não fixa amplitude, perfil e solução.
3. Obter os dois potenciais e a relação entre os observáveis estelares/fotônicos, incluindo os termos que o ramo acima excluiu.
4. Aplicar o perfilamento massa/distância já verificado e a covariância real. Não reexecutar os forecasts R1–R4 sem esse insumo.

O cálculo atual fecha uma resposta métrica condicional e elimina a atribuição automática de atraso ao fator conforme. **Não fecha a previsão TGL completa por lente nem produz 5 sigma.** A auditoria de conclusão em COMPLETION_AUDIT_R6.json registra os requisitos sem redefinir a meta.

Primeira tentativa teve erro de sintaxe e foi preservada em linear_metric_response.py / RUN_R6.json. A versão nova linear_metric_response_r6_1.py compilou/executou com exit0 e dez resíduos simbólicos nulos; plano e resultado têm nomes próprios. Não houve dado observado ou mudança no cânone.
