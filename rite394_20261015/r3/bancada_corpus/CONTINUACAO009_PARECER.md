[REAL / INPUT / KNOWN / OPEN] Curvatura geral em uma carta, Bianchi e reconstrução com o tensor de Einstein geométrico — continuação espontânea após 008, 05/09/2026.

## O avanço em relação à entrega 008

A entrega 008 concluía G+Λg=κT para dois campos G e T cuja conservação era dada. Esta continuação constrói a conexão de Levi-Civita da métrica, sua curvatura, Ricci, o escalar e o campo G=Ric−½Rg. Prova simetria e conservação desse G e o coloca efetivamente no teorema de reconstrução. Portanto a construção do G geométrico e a obrigação div G=0 foram pagas nesta carta. Não foram simplesmente renomeadas como campos de uma estrutura.

O teorema final é `geometric_einstein_equation_from_ricci_null_balance`. Seus dados são:

- U⊆ℝ⁴ aberto e preconexo; o caso vazio é permitido e trivial. Em um domínio não vazio, vale a conexão usual.
- Referencial E(x) e inversa D(x) com componentes C∞ e ED=DE=I em U.
- g=EᵀηE e g⁻¹=DηDᵀ, com η=diag(1,−1,−1,−1).
- Matéria T simétrica, com componentes diferenciáveis e div T=0 para a conexão construída.
- Acoplamento real constante κ e a condição, para cada x e cada vetor v, g(v,v)=0 ⇒ (Ric−κT)(v,v)=0.

A conclusão é a existência de uma constante real Λ tal que

    G_geom[g]+Λg=κT em U.

`frameEinsteinTensor E D` é o G efetivo dessa fórmula. `frameLeviCivita E D` é a conexão efetiva. Sua regularidade, simetria e conservação são obtidas por provas anteriores, não por argumentos adicionais no teorema final. A condição de Ricci passa para G porque o termo proporcional a g se anula em vetores nulos. A constância de Λ reutiliza a prova da entrega 008.

## Objetos e convenções

Os índices vão de 0 a 3; Γᵢ é a matriz com entrada Γᵃᵢᵦ. A convenção de curvatura é

    Fᵢⱼ = ∂ᵢΓⱼ−∂ⱼΓᵢ+ΓᵢΓⱼ−ΓⱼΓᵢ,
    Rᵃᵦᵢⱼ = (Fᵢⱼ)ᵃᵦ,
    Rₐᵦᵢⱼ = gₐc Rᶜᵦᵢⱼ,
    Ricᵦⱼ = Σₐ Rᵃᵦₐⱼ,
    R = Σᵢⱼ g^{ij} Ricᵢⱼ,
    G = Ric−½Rg.

As derivadas são `fderiv ℝ` aplicado aos vetores coordenados, tal como na entrega 008. A conexão não foi linearizada, e o termo ΓᵢΓⱼ−ΓⱼΓᵢ está presente. Não se restringiu a métrica geral a uma ansatz diagonal ou homogênea. O resultado trata de componentes em uma carta: transformações entre cartas e colagem global ainda não foram formalizadas aqui.

`SmoothMatrixOn` usa `ContDiffOn ℝ ∞`. Na mathlib desta máquina, `⊤ : ℕ∞ω` significa ω, isto é, analiticidade, enquanto ∞ é o elemento intermediário de regularidade suave. A versão inicial com ⊤ foi preservada; os fontes finais foram corrigidos e recompilados para C∞. A hipótese final não exige analiticidade.

## Cadeia de provas

1. `SmoothMatrixCalculus.lean`: regras de produto, soma, transposta e derivadas coordenadas; simetria das segundas derivadas reais; regularidade dos campos matriciais e de seus primeiros jatos.

2. `CurvatureJetAlgebra.lean`: cancelamentos algébricos de curvatura. A distinção é explícita: nesse módulo dΓ e ddΓ são jatos. Primeira Bianchi usa torção zero e sua derivada; a identidade diferencial exterior usa comutação das segundas derivadas. Compatibilidade métrica e sua derivada dão antissimetria da curvatura com índice abaixado. A troca de pares é deduzida das antissimetrias e da primeira Bianchi.

3. `CoordinateCurvature.lean`: os jatos são instanciados com derivadas reais de Γ. A regra do produto produz a derivada da curvatura; a comutação necessária vem da regularidade C∞. A identidade exterior e a primeira Bianchi são assim obtidas para campos em U.

4. `MetricCurvatureSymmetries.lean`: diferencia a identidade de compatibilidade em U, produz as simetrias da curvatura abaixada, define Ricci, R e G e prova a simetria de Ricci e G. A contração que usa g⁻¹ é identificada com a contração do índice superior da curvatura.

5. `CovariantCurvatureBianchi.lean`: acrescenta as correções dos índices de direção ao comutador matricial, definindo a derivada covariante completa de F. Por torção zero, essas correções cancelam na soma cíclica. O abaixamento de índices é ligado à derivada covariante do tensor correspondente por compatibilidade métrica. As antissimetrias da derivada abaixada também são provadas.

6. `ContractedBianchi.lean`: contrai explicitamente os índices da segunda Bianchi. Os termos de conexão que aparecem ao diferenciar o traço de curvatura são cancelados por permutação das somas finitas, identificando a expressão com ∇Ric. Não se declara a divergência como um campo presumido de Ricci.

7. `GeometricEinsteinReconstruction.lean`: deriva

       ∂ₖg⁻¹=−Γₖg⁻¹−g⁻¹Γₖᵀ,
       ∂ₖR=tr(g⁻¹∇ₖRic),
       2 div Ric=dR,
       div(Ric−½Rg)=0.

   As identidades de traço são ligadas a derivadas genuínas em U. A regularidade da conexão de Levi-Civita é provada a partir de g e g⁻¹. O teorema final usa essa conexão e esse tensor G na reconstrução de 008.

8. `CurvatureControls.lean`: controle exato com g=exp(2x⁰)η. A conexão é calculada pela fórmula de Levi-Civita, e não apenas proposta como um símbolo Γ independente. A componente (F₁₂)¹₂ é 1 e G=diag(3,−1,−1,−1). Esse G não é múltiplo de g em nenhum ponto. O controle verifica sinais e mostra por que a condição de balanço nulo da matéria não pode ser omitida. O manifesto de compilação é a evidência de quais desses enunciados passaram.

## O que continua como entrada ou dívida

| Objeto ou ligação | Estatuto |
|---|---|
| Curvatura, Ricci, R e G a partir de Γ de Levi-Civita | [REAL] construídos na carta. |
| Primeira e segunda Bianchi; conservação de G | [REAL] provadas a partir das definições e regularidade indicadas. |
| Reconstrução G_geom+Λg=κT com Λ constante | [REAL] implicação com hipóteses explícitas. |
| Dimensão quatro e assinatura de η | [INPUT]. Não foram extraídas da dinâmica modular. |
| Referencial E e sua inversa suave | [INPUT]. A origem dinâmica ainda não foi demonstrada. |
| Conservação de T e balanço de Ricci em todos os vetores nulos | [INPUT]. Não foram derivados de uma teoria quântica ou de dados de horizonte. |
| H3 físico, Clausius/Raychaudhuri e ponte modular-geometria | [OPEN]. A construção geométrica não fornece essas hipóteses. |
| Compatibilidade entre cartas e variedade global | [OPEN] nesta formalização. |
| Objetivo amplo de gravitação quântica | [OPEN]. Não foi substituído por esta implicação clássica nem declarado completo. |

[KNOWN] A identidade contraída de Bianchi e a conservação do tensor de Einstein são resultados clássicos. Foi consultada como referência primária de convenções a exposição do autor [David Tong, seção 3 de General Relativity](https://www.damtp.cam.ac.uk/user/tong/gr/grhtml/S3.html). Nesta entrega, os enunciados têm provas Lean próprias; a referência não entrou como axioma ou como substituta de uma ligação ausente. A assinatura e a convenção de índices desta bancada estão escritas acima para evitar transportar sinais por mera semelhança de nomes.

## Custódia e tentativas

A derivação geral e o cálculo prévio do controle foram registrados antes de seus respectivos fontes. Falhas de inferência, reescrita, normalização de somas e orientação de traço foram preservadas com seus logs e backups de bytes. Uma tentativa de revisão via stdin encontrou um erro de codificação Unicode antes de escrever qualquer arquivo; o transporte das revisões seguintes foi feito por JSON ASCII com escapes Unicode. A validação anterior à escrita evitou truncamento.

O manifesto desta continuação lista fontes, logs finais, metadados, backups e dependências locais por SHA256 dos bytes. A compilação de construção e a conferência de hashes não substituem a auditoria independente da gerência.

Somente a bancada Chatgpt recebeu escritas. As entregas anteriores são imutáveis. `um.py`, kernel canônico, Atlas, memórias, selos e gate não foram alterados; nenhum `um.py` foi executado ou importado. Não foram buscados dados observacionais. A incorporação e a atualização das superfícies da casa cabem à gerência após sua auditoria.
