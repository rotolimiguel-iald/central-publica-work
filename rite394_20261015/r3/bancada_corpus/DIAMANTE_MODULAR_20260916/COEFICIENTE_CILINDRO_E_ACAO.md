# Primeiro resto modular: uma fórmula calculável e seus dados físicos

16/09/2026. [DERIVED] Derivação analítica nesta bancada, em regularização fiel e com preparação euclidiana especificada. [REAL] Verificação independente da fórmula por evolução matricial ordenada, descrita abaixo. Não é nova prova Lean, cálculo numérico de uma QFT ou solução de gravidade quântica. Reutiliza a derivada do logaritmo já entregue.

## 1. O que acrescenta à resposta anterior

A fórmula R₁=−Dlog(ρ₀)[ρ₁]−Q₁ deixava ρ₁ como entrada. Aqui calculamos ρ₁ a partir de uma preparação euclidiana H₀+εV(τ). Obtemos um filtro explícito para cada harmônico de V. Isso especifica como o tempo modular participa do coeficiente; ainda exige identificar a preparação e a carga Q com os objetos físicos da TGL.

A expansão de Hamiltonianos modulares para estados preparados por fontes euclidianas e o papel especial das fontes independentes do tempo angular são tratados em Balakrishnan–Parrikar, seções 2.1–2.2. Usamos a convenção de sinal **+εV** no Hamiltoniano euclidiano; não copiamos o sinal da fonte de outra convenção. [Fonte primária](https://arxiv.org/html/2002.00018).

## 2. Preparação e primeira variação

Fixe período angular b=2π, uma regularização finita e

    Uε = T exp[−∫₀ᵇ (H₀+εV(τ))dτ],
    ρε = Uε / Tr Uε,       Kε = −log ρε.

Suponha V hermitiano e V(b−τ)=V(τ). A simetria de reflexão permite escrever a preparação como B†B, garantindo positividade. Para a derivação a primeira ordem, as integrais e derivadas são ordinárias de matrizes; sua extensão ao contínuo não é pressuposta.

Derivar a evolução ordenada fornece

    U₁ = −∫₀ᵇ e^{−(b−τ)H₀} V(τ) e^{−τH₀} dτ.

Na base H₀|a⟩=Eₐ|a⟩, ponha ω_ab=Eₐ−E_b. A derivada do logaritmo já demonstrada dá, módulo um escalar de normalização,

    (K₁)ab = [bω_ab/(exp(bω_ab)−1)] ∫₀ᵇ exp(τω_ab) Vab(τ)dτ.

Para ω_ab=0, a expressão contínua é ∫₀ᵇ Vab(τ)dτ. Não dividir numericamente por zero em blocos degenerados. A constante de normalização é

    c₁ = −∫₀ᵇ Tr(ρ₀V(τ))dτ,

que multiplica I. É irrelevante para comutadores, mas foi mantida no teste da matriz K inteira.

## 3. O filtro dos harmônicos — coeficiente explícito

Use a expansão real, compatível com a reflexão,

    V(τ) = V₀ + Σₙ≥₁ Vₙ cos(nτ).

Na regularização considerada, tome uma soma finita; passar a uma série requer convergência suficiente. Uma primitiva direta é

    ∫ exp(ωτ) cos(nτ)dτ
      = exp(ωτ)[ω cos(nτ)+n sin(nτ)]/(ω²+n²).

Avaliada entre 0 e 2π e inserida na expressão anterior, resulta em

    (K₁)ab = 2π(V₀)ab
            + 2π Σₙ≥₁ [ω_ab²/(ω_ab²+n²)] (Vₙ)ab + c₁ δab.

O fator é real e par em ω_ab, como exige a hermiticidade. A preparação constante dá exatamente K₁=2πV₀+c₁I. Em ω_ab=0, todos os harmônicos não constantes desaparecem de K₁; isso não os faz desaparecer de qualquer carga candidata escolhida separadamente.

Para o resto solicitado pelo operador, a fórmula geral permanece

    R₁ = K₁ − Q₁.

**Somente sob a hipótese adicional Q₁=2πV(0)** — carga instantânea nesta representação, sem termos extras de superfície, melhoria ou contato — segue

    (R₁)ab = −2π Σₙ≥₁ [n²/(ω_ab²+n²)](Vₙ)ab + c₁δab.       (★)

Esse é o novo coeficiente calculável. Não é um número único: é um operador cujos elementos dependem dos intervalos espectrais e dos Vₙ. Se Q₁ tem uma contribuição adicional B₁, acrescentar −B₁ ao lado direito; não omiti-la para obter fechamento.

Equivalente, no espaço de operadores matriciais, a contribuição do harmônico n é −2π n²(ad(H₀)²+n²)⁻¹Vₙ. Esse inverso existe para n≥1. A apresentação é cálculo funcional do operador já dado, não definição de outro motor de dephasing. Um multiplicador negativo no **coeficiente de um Hamiltoniano** também não é uma taxa dissipativa de Lindblad.

## 4. Onde entram raio, campo, interação e curvatura

Para uma bola no vácuo de uma CFT em Minkowski, a correspondência com um estado térmico no cilindro hiperbólico fornece a referência H₀. Essa correspondência não exige que a CFT seja livre. A geometria e a carga exata de referência estão em Casini–Huerta–Myers, seção 2, equações 22 e 27–28. [Fonte primária](https://arxiv.org/html/1102.0440v2).

Em coordenadas euclidianas adimensionais no cilindro,

    t_E = ℓ sinτ/(cosh u+cosτ),
    r   = ℓ sinh u/(cosh u+cosτ),
    ds_flat² = Ω² ds_cyl²,       Ω=ℓ/(cosh u+cosτ).

Uma deformação escalar primária g_i∫O_i, de dimensão Δ_i em d dimensões, transforma a medida e o operador com pesos d e −Δ_i. Logo sua fonte no cilindro é

    λ_i(τ,u) = g_i ℓ^{d−Δ_i}(cosh u+cosτ)^{Δ_i−d}.

Se a deformação admite expansão controlada e a preparação euclidiana descrita, seus harmônicos determinam os Vₙ de (★). A dependência em ℓ surge já em g_iℓ^{d−Δ_i}; os elementos de matriz de O_i e o espectro de H₀ contêm os dados da CFT, inclusive suas interações.

Isso NÃO elimina condições de renormalização e de infravermelho: cosh u+cosτ se anula em u=0, τ=π, ponto correspondente ao infinito do espaço plano. Uma deformação relevante constante pode exigir regulação de IR e pode produzir comportamento não analítico. A existência de um ponto fixo UV, sozinha, não autoriza intercambiar expansão, remoção de regulador e integral.

Uma deformação exatamente marginal que permanece conforme pode continuar com resto escalar. Uma perturbação de geometria introduz fontes tensoriais e termos locais de renormalização; o mapa plano acima não fornece, sozinho, o coeficiente em um espaço-tempo curvo arbitrário. O coeficiente universal da operação de logaritmo não torna universais os dados físicos aos quais ela é aplicada.

## 5. Centralizador: como testar este coeficiente

Se Nε é o centralizador de ρε e Aε é uma família diferenciável de seus elementos, continua valendo

    [Rε,Aε] = −[Qε,Aε].

A primeira obstrução é [R₁,A₀]+[R₀,A₁]. Quando a referência conforme tem R₀=cI, o segundo termo desaparece. Nesse caso, (★), depois de incluir B₁ quando houver, pode ser testada diretamente por [R₁,A₀]. Se o centralizador perde dimensões sob a deformação, nem todo A₀ admite a família Aε requerida. Não ignorar essa restrição.

Se Nε=ℂI, a ação é trivial em qualquer ordem e o teste não determina Rε. Se Nε é maior, os Vₙ e Q₁ precisam satisfazer as condições de comutação correspondentes. A fórmula não presume de antemão a resposta.

## 6. Diagnóstico físico do traço — reutilização da prova existente

`DiamondConformalCurrent.lean` já prova a contração da identidade de corrente conforme. Não criamos outra prova com o mesmo conteúdo. Para T simétrico, conservado e ξ conforme de Killing, com ∇_(μξ_ν)=χgμν,

    ∇μ(2πTμνξν) = 2πχ Tμ_mu.

No diamante plano com ξ⁰=(ℓ²−t²−r²)/(2ℓ), ξⁱ=−txⁱ/ℓ, χ=−t/ℓ. Assim o teste local da divergência se anula em t=0 mesmo quando o traço não é zero; uma leitura somente nessa fatia não prova conservação em todo o diamante.

Em QFT renormalizada, a identidade de traço pode conter operadores multiplicados por funções de acoplamentos, divergências de correntes e anomalias geométricas. Jack–Osborn explicitam a distinção entre β^I de RG e os coeficientes B^I após contribuições de correntes, já no espaço plano (eqs. 1.5–1.7). São dados da teoria, não o invariante β_TGL. [Fonte primária](https://arxiv.org/pdf/1312.0428).

Uma anomalia puramente geométrica 𝒜[g]I, sobre **fundo clássico fixo**, é escalar e comuta com os observáveis. Não a contar como obstrução não central apenas por depender da curvatura. Termos com operadores de campos, melhorias, massas e fontes podem ter ação não trivial. Se a métrica for quantizada, esse argumento de escalaridade não é automaticamente aplicável.

A identidade de corrente diagnostica uma condição para a carga; não identifica o resto modular inteiro com a integral do traço. O estado regional e a preparação continuam necessários.

## 7. O que foi lido na ação da TGL

[REAL — leitura da fonte] `C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py`, função `_latex_part_I_lagrangian_en`, linhas 10090–10217, apresenta:

- os termos usuais da matéria;
- Φμν=∂μΨν−∂νΨμ e −Φ²/4, enquanto o texto chama Ψ de campo escalar de fronteira;
- R/(2κ²)+ξR|Ψ|², com ξ=1/6;
- L_modular=L_ΛCDM β_TGL |1+w_eff(z)|;
- a equação (□−m²−ξR)Ψ=β_TGL K∂Ψ como resultado declarado da variação.

Nesse trecho não está explicitada a relação entre Ψμ e Ψ, nem a dependência funcional de L_modular em Ψ que produziria K∂Ψ. Não suprimos essas relações por conta própria. Se Ψμ fosse simplesmente ∂μΨ, Φμν seria zero para um escalar suave com derivadas que comutam; se for um campo independente, essa opção tem outra variação. O texto consultado não fixa qual dessas tipagens, ou outra construção, deve ser usada no cálculo quântico.

Também é necessário indicar como w_eff, que aparece como quantidade cosmológica, varia fora da solução de fundo. Tratar esse fator como externo durante uma variação e como dependente dos campos durante outra produz ações diferentes. Isso é uma pendência de especificação no trecho consultado, não uma afirmação de inexistência em todo o acervo. A quarta face formal já preserva honestamente a EOM como hipótese.

## 8. Verificação realizada e encaminhamento

`verify_cylinder_response.py` compara a fórmula analítica com −log de produtos euclidianos ordenados e normalizados, usando fontes que se refletem em τ→2π−τ. Em resoluções 128, 256, 512 e 1024, o erro caiu aproximadamente por quatro a cada duplicação. No caso com dois harmônicos e degenerescência, o erro final foi 8,55×10⁻⁷; no caso sem degenerescência, 1,73×10⁻⁶. O controle constante ficou na ordem de 10⁻⁹. Os números completos e o hash do script estão em `CYLINDER_RESPONSE_CHECKS.json`.

Um controle adicional mantém ρ exatamente constante, dentro do erro de 6,45×10⁻¹⁵, com V(τ)=cosτ W e [W,H₀]=0. A carga instantânea ainda difere e pode agir num bloco degenerado. É um controle matricial da distinção preparação/carga; não é um contraexemplo de QFT interagente.

Para o um.py: não acrescentar outra camada de funções. Guardar a expressão (★) como resultado DERIVED e usar os consumidores de cociclo/logaritmo existentes quando a preparação física V e Q₁ forem identificadas. Não converter o filtro em β_TGL, taxa Γ ou certificado físico por igualdade de nomes. A pergunta pelo arquivo da ação quântica, vácuo e Tμν foi encaminhada ao operador; o trabalho acima não depende de uma resposta presumida.

[OPEN] A realização física regional, a preparação quântica da TGL, seu primeiro coeficiente físico e a solução de gravidade quântica permanecem não demonstrados. Esta entrega especifica uma rota perturbativa calculável e seus dados de entrada, sem substituir o objetivo completo por sua verificação regularizada.


### Nota de proveniência

O restante da mesma função, linhas 10219–10278, já distingue a consequência cosmológica da identificação operatorial para horizontes gerais, que o artigo marca como conjectural. Esse registro histórico não reabre a dualidade da torre provada depois. Os dois arquivos do artigo localizados têm hashes distintos; seus trechos integrais da função foram preservados com localização em TGL_ACTION_SOURCE_EXCERPTS.json. Não se pressupõe que o artigo antigo seja o estado inteiro do kernel v358.
