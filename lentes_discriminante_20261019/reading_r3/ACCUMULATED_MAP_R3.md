# Leitura acumulada D1b e distâncias de lente — R3

19/10/2026 · F8.LENTES_5SIGMA_20261019, claim1009 · referência própria SESSION_REFERENCE.json, revisão3 confirmada. [DERIVED condicional]. Autor: subagente codex da coordenação. Sem novo cálculo numérico, composto, forecast ou execução dos motores. A identidade abaixo não promove a calibração de luminosidade à geometria por decreto.

## 1. Reaproveitamento: o que já existe e o que este arquivo acrescenta

**Já existe:** NOTA_DERIVACOES_F2.md:18–29 deriva ν=2β/3, k(z)=E(z)^ν, K*=k(z*), a leitura A(z)=K*/k(z) e a distância acumulada ∫du/[E A]. A linha39 delimita que o motor consultado aplicava a leitura ao canal de luminosidade, mantendo BAO no fundo nu. A mesma nota:70–84 deixa aberta a extensão de dois redshifts, e `f2_analysis.py`:57–60 calcula somente proxies de endpoint para lentes; não calcula D_Δt acumulado. A errata R-G fixa a direção de f_phi (ver §5 abaixo).

`poder_forma/forecast_shape.py` e `NOTA_PODER_FORMA.md` já projetam amplitude e tangente Ωm em **SN+BAO**. Seus resultados não são poder de lentes; não são reexecutados. Na cobertura focal destes arquivos não foi encontrado ajuste exato de D_Δt acumulado após H0/Ωm. Isso não é alegação de ausência universal no acervo. A contribuição nova desta nota é o mapa condicional entre dois redshifts e seu espaço de nuisances.

## 2. Hipótese adicional indispensável

[INPUT — extensão candidata, não derivada da D1b escalar] Admitir que χ_A abaixo seja a coordenada radial de uma geometria **FLRW óptica plana**, com composição aditiva das distâncias comóveis, os mesmos redshifts e a relação angular D_A(z1,z2)=[χ_A(z2)−χ_A(z1)]/(1+z2). Admitir também a fórmula de atraso de lente fina nessa geometria, com o potencial e o relógio explicitados em §5. A leitura de luminosidade isolada não demonstra essas hipóteses, dualidade de distâncias, lei da lente nem propagação polarizada.

Para E(z)>0, E(0)=1, β constante, ν=2β/3, 0<z_l<z_s, defina

I(z)=∫₀ᶻ E(u)⁻¹du; J(z)=∫₀ᶻ E(u)^(ν−1)du;
I_ls=I(z_s)−I(z_l)=∫zl^zs du/E(u);
J_ls=J(z_s)−J(z_l)=∫zl^zs E(u)^(ν−1)du.

χ_bg(z)=(c/H0)I(z), χ_A(z)=cJ(z)/(H0 K*), K*=E(z*)^ν>0.

**Não usar J(z_s)−J(z_l) como endpoint k(z_s)I_ls:** o peso varia dentro do intervalo. A primitiva deve compartilhar a mesma normalização/zero; diferenciar primitivas com contratos distintos também é inválido.

## 3. Distâncias e fator exato de atraso

Na hipótese do §2,

D_l,A=c J_l/[H0 K*(1+z_l)],
D_s,A=c J_s/[H0 K*(1+z_s)],
D_ls,A=c J_ls/[H0 K*(1+z_s)],

**D_Δt,A=(1+z_l)D_l,A D_s,A/D_ls,A = c J_l J_s/[H0 K* J_ls].**

O fundo correspondente é D_Δt,bg=c I_l I_s/(H0 I_ls). Defina médias ponderadas Q_l=J_l/I_l, Q_s=J_s/I_s e, essencialmente, Q_ls=J_ls/I_ls. Então

f_l=Q_l/K*, f_s=Q_s/K*, f_ls=Q_ls/K*,
**F_D ≡ D_Δt,A/D_Δt,bg = (1/K*)·Q_l Q_s/Q_ls.**

A comparação com a **sombra geométrica** χ_sh=χ_bg/K* dá D_Δt,A/D_Δt,sh=Q_l Q_s/Q_ls. A sombra aqui também é hipótese geométrica; não confundir esse denominador com o fundo nu. No limite β=0, K*=Q_l=Q_s=Q_ls=1. Os fatores (1+z_l),(1+z_s) cancelam como indicado; não introduzir um fator (1+z_s) extra no atraso.

## 4. Sinal: o que pode e o que não pode ser afirmado

Para E não decrescente e ν≥0, k=E^ν também é não decrescente. As médias satisfazem

1≤Q_l≤Q_ls,  Q_s=(I_l Q_l+I_ls Q_ls)/(I_l+I_ls),  Q_l≤Q_s≤Q_ls.

Assim F_D≤Q_l/K*. Se z*≥z_l, K*≥k(z_l)≥Q_l, portanto **0<F_D≤1**, mantendo H0 e E nus fixos. Em particular z*≥z_s basta. A desigualdade é estrita nas situações não constantes pertinentes. Com f_t=f_phi=1, o ajuste GR de forma cosmológica fixa devolveria H0_fit/H0_bg=1/F_D≥1. Esse sinal é condicional ao relógio, potencial e fixação de parâmetros; não é um veredito.

Depois de remover a escala K*, o fator G=Q_l Q_s/Q_ls não tem sinal universal em torno de1 decorrente apenas de E crescente. Por exemplo, um E quase1 até a lente e bem maior entre lente e fonte dá Q_l≈1<Q_ls e G<1; um E que sobe rapidamente perto da origem e fica quase constante no restante pode dar G>1. Suavizações preservam essas desigualdades estritas. São exemplos funcionais analíticos, não modelos TGL selecionados nem cálculos numéricos. Para uma família concreta E(z;Ωm,Ωr), é necessário calcular G, não transferir um desses sinais.

## 5. f_phi e relógio: conservar a errata R-G

Reaproveitar **ERRATA_R_G_FPHI.md:5–17**:

f_phi=Δφ_fit/Δφ_true; f_t=Δt_obs/Δt_phys;
Δt_phys=D_Δt,A Δφ_true/c;
D_Δt,fit/D_Δt,bg=f_t F_D/f_phi;
H0_fit/H0_bg=f_phi/(f_t F_D), **somente mantendo os demais parâmetros da geometria de referência fixos**.

Se Ωm ou outro parâmetro de forma mudar no ajuste, escreva S_bg(η)=I_l(η)I_s(η)/I_ls(η). Para η_true e η_fit,

H0_fit/H0_true = [S_bg(η_fit)/S_bg(η_true)]·f_phi/(f_t F_D(η_true)).

Essa expressão resulta de igualar os atrasos, não de atribuir massa independente à lente. f_phi é razão entre potenciais reconstruído e verdadeiro do mesmo par orientado; não é automaticamente1 nem independente do ajuste da massa, fonte, convergência externa e distâncias. Todos esses objetos devem ser recalculados pela mesma lei de lente. A hipótese FLRW óptica sozinha não determina f_t ou f_phi. Os resultados de R2 sobre folha de massa e degenerescência permanecem aplicáveis.

## 6. Escala versus forma após ajustar H0 e Ωm

Se K* é uma constante comum à amostra, a mudança **H0_tilde=H0 K*** remove K* de todas as distâncias χ_A. Como χ_A'(z)=c/[H0 K* E(z)^(1−ν)], a geometria óptica candidata tem H_opt(z)=H0_tilde E(z)^(1−ν), com H_opt(0)=H0_tilde. Isso é a expansão definida por essa geometria candidata, não identificação demonstrada com H físico da cosmologia TGL.

A escala comum K* não oferece discriminação de distâncias quando H0 está livre. Mesmo que K* dependa de Ωm por E(z*), a transformação coordenada H0↔H0_tilde é válida para cada Ωm; um prior de H0 deve ser transformado e interpretado, não ignorado. Se o procedimento de calibração atribuir K* distinto a cada fonte, este argumento de uma única escala não se aplica sem novo contrato.

Resta a forma J_l J_s/J_ls. Ela não é a reparametrização de coeficientes da lei H_TGL²=H_LCDM²[1+β|1+w|] estudada na R2: **são mapas diferentes**. Aqui, para E²=Ωm(1+z)³+Ωr(1+z)⁴+ΩΛ, H_opt²/H0_tilde²=(E²)^(1−ν); não se pode simplesmente reutilizar os coeficientes lineares da R2. A forma pode ser parcialmente absorvida por Ωm, e a possibilidade remanescente precisa ser perfilada, não declarada identificável por nome.

Uma fórmula útil, sem nova execução: defina μ_ab=[∫za^zb (lnE)/E du]/I_ab. Para β pequeno e E fixo,

ln F_D = −ln K* + ν(μ_0l+μ_0s−μ_ls)+O(ν²).

Como μ_0s=[I_l μ_0l+I_ls μ_ls]/I_s, o coeficiente de forma é μ_0l−(I_l/I_s)(μ_ls−μ_0l). A contribuição −lnK*=−νlnE(z*) é comum a todas as lentes e é removida pela amplitude H0 livre. Isso explica por que um fator endpoint isolado superestima a informação nova.

Para pares de redshifts pré-especificados, monte o vetor de resposta s_i=∂β lnD_Δt,A,i e as tangentes de nuisance N=(-1,∂Ωm lnD_Δt,bg,...), acrescentando os parâmetros que afetam a reconstrução de Δφ e o relógio. Com a covariância conjunta Σ, use a projeção W=Σ⁻¹ e I_perfil=sᵀWs−sᵀWN(NᵀWN)^+NᵀWs, como em R2. No limite linear em β, a coluna de forma é (2/3)(μ_0l+μ_0s−μ_ls), após remover a constante K*. Um cálculo completo deve usar as previsões integrais e ajustar os parâmetros consistentemente; a tangente apenas mede identificabilidade local.

**Não foi calculado novo poder.** A etapa numérica só acrescentaria conhecimento com plano prévio, pares (zl,zs), E/fecho, covariância e nuisance fixados, mantendo q/f_phi/f_t no estatuto correto. Os antigos forecasts SN/BAO não são transferíveis a este vetor de distâncias de lente.

## Conclusão delimitada

A extensão óptica candidata fecha algebricamente D_l,D_s,D_ls,D_Δt e sua convenção de potencial, reaproveitando a integral e a errata existentes. Ela evidencia: (i) o intervalo lente–fonte tem integral própria; (ii) K* comum é escala absorvível por H0; (iii) a forma restante exige ajuste conjunto e pode ser fraca ou degenerada; (iv) promover luminosidade acumulada a geometria/tempo continua uma hipótese de mapa, não uma extensão TGL já demonstrada. Nenhum dado ou artefato anterior foi alterado.
