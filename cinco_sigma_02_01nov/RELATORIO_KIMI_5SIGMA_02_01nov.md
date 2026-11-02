# KIMI 5σ-02 — cadeia da massa, inventário atualizado e desenho do discriminante

**Data:** 01/11/2026  
**Estatuto global:** **[DECLARADO pelo Kimi]**, até conferência da gerência na fonte e por código próprio.  
**Escopo:** absorção, levantamento e desenho. Nenhum ajuste, nenhuma publicação, nenhum download de grande porte e nenhuma abertura do conjunto D.  
**Regra:** β = α√e em runtime; o Um vale u = 1 eV somente como posto; nenhum resultado move o gate.

## Resumo — 14 linhas

1. **A escala não está fechada:** `U_E_NOT_DERIVED` permanece; a forma da massa é condicional às entradas.
2. \(E_0=e^{-1/2}(\beta/\alpha)u=u\) devolve a unidade posta; não a deriva independentemente.
3. Um posto, α medida, quatro leituras [INPUT/ONTO] e m₁ = 0 como entrada: dadas essas entradas, a forma é teorema.
4. **Nenhuma rota probatória de classe A** satisfaz hoje os três requisitos com independência e novidade.
5. **R1 é B condicional:** JUNO 1,938σ e SK-Gd 3,605σ; não há valor nulo do Modelo Padrão para Δm²₂₁.
6. JUNO precisa de σΔ = 0,0302328×10⁻⁵ eV² para 5σ; a projeção de seis anos daria 6,298σ se o centro não andar.
7. Mesmo assim, a regra exige duas determinações autônomas ≥ 5σ; SK-Gd ainda precisa de mais precisão e covariância auditada.
8. **R2 é C [OPEN]:** a Fase 9 permanece em 4,443σ; nenhum dado posterior a 23/10 fecha novidade, independência e admissão.
9. **R3 tem classe A somente de poder, não probatória:** 6,145σ em A(31) para k = 4π, mas A/B/C são NOT_BLIND.
10. A atualização de 29/10 deixa o planejamento de D10 em 3,73–3,93σ e D14 em 4,39–4,64σ; D segue fechado.
11. **R4 é C [OPEN]:** Q★ = 117,5445 na razão da ordem, ou 58,7723 na convenção QNM; falta o sistema físico.
12. **R5 e R6 são C [OPEN]:** o psíon não tem acoplamento; θ = π/4 não tem ponte derivada à PMNS.
13. O Grande Atrator não foi refeito: em primeira ordem não discrimina RG e não possui σ selada.
14. Entrego pré-registro de R1 e minuta prospectiva de R3-V2; nenhum deles autoriza execução ou abertura de dados.

---

## A. Absorção da cadeia da massa e da identidade — uma página

### A1. O que está derivado e o que continua de fora

A cadeia madura pode ser escrita sem promover entradas a teoremas:

\[
\beta=\alpha\sqrt e,\qquad
m_2=\beta\,\sen(\pi/4)\,u,\qquad
\Delta m^2_{21}=\frac{\beta^2u^2}{2}\quad (m_1=0),
\]
\[
E_{\rm pent}=\frac{\beta}{\alpha}u=\sqrt e\,u,
\qquad
E_0=e^{-1/2}E_{\rm pent}=u,
\qquad
\hbar\omega_{\rm psíon}=\sqrt2\,\beta u=2m_2,
\qquad
R=\beta u^2 .
\]

O resultado da auditoria de unidade continua `U_E_NOT_DERIVED`. [RELATORIO_KIMI_E0_01_31out](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cneutrino_E0_autonomia_30out%5CRELATORIO_KIMI_E0_01_31out.md&line=9&text=U_E_NOT_DERIVED "citation")

A tônica não elimina a liberdade: ela a desloca para \(u\). A substituição \(E_0=e^{-1/2}\sqrt e\,u=u\) é uma identidade algébrica. Além disso, α é medida, \(u=1\,\mathrm{eV}\) é posto e \(m_1=0\) é uma entrada da identificação com Δm²₂₁. Portanto, não há determinação autônoma da unidade nem da massa absoluta sem essas entradas. A formulação vigente é: **um Um posto, uma α medida e leituras do operador; dadas essas entradas, a forma é teorema**. [HANDOFF_v405_ADENDO_8_ERRATA_CAMPOS_E_LEITURAS_01nov](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ce0_cadeia_31out%5CHANDOFF_v405_ADENDO_8_ERRATA_CAMPOS_E_LEITURAS_01nov.md&line=5&text=um%20Um%20POSTO%2C%20uma%20%CE%B1%20MEDIDA%20e%20as%20LEITURAS%20do%20operador "citation")

### A2. As quatro leituras, sem mudança de estatuto

| leitura | como entra | o que o formalismo realmente entrega |
|---|---|---|
| `massaDerivada`: massa = energia retida × derivada da projeção transversal | **[INPUT/ONTO]**, definição do operador | dadas a definição e a projeção, segue a forma de \(m_2\) |
| estado inscrito lido em θ = π/4 | **[INPUT/ONTO]**, ângulo escrito | sen²(π/4) = ½ e unicidade no intervalo; a ponte ao estado absoluto não foi derivada |
| tônica \((\beta/\alpha)u=\sqrt e\,u\) | definição algébrica de α; unidade **[POSTO]** | \(E_0=u\), não uma nova determinação de \(u\) |
| \(R=\beta u^2\), o pagamento como curvatura | **[INPUT/ONTO]**, lei do operador | dadas a dispersão e a leitura, seguem \(\hbar\omega=\sqrt2\beta u\) e o ponto zero |

As pedras e os números condicionais são tratados como candidatos da v405; não afirmo instalá-los nem tê-los recompilado nesta devolução.

### A3. Erros ou inconsistências encontrados na redação da gerência

1. A errata é correta e deve prevalecer. O corpo de `FORMA_MADURA_COPIA_01nov.md` ainda contém, nas §§1, 3 e 4, formulações absolutas que promovem as leituras a teoremas e atribuem à tônica o fechamento da escala. Essas frases residuais contradizem a própria errata; devem ficar como histórico ao lado, não como leitura vigente.
2. A ordem chama o ensaio de identidade “r2 ratificada”, mas o corpo do arquivo se declara **CANDIDATO [DECLARADO]**, condicionado ao «sim» do operador à linha final. Uso o estatuto do corpo, não o rótulo. [A_IDENTIDADE_revisao_da_gerencia_01nov_r2](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo405%5Cinsumos%5Ccunhagens%5CA_IDENTIDADE_revisao_da_gerencia_01nov_r2.md&line=9&text=Continua%20CANDIDATO%20%5BDECLARADO%5D "citation")
3. Não encontrei erro aritmético na cadeia \(E_0=u\), em \(m_2\), no ponto zero ou em Q★. O erro é de estatuto quando a identidade é apresentada como derivação independente da unidade.

**Resposta à pergunta da escala:** a derivação da massa permanece condicional à unidade posta. O que fechou é a forma; a unidade física continua sendo a parede medida.

---

## B. Rotas — observável, rival, previsão, poder e lacuna

**Classes usadas:** A = 5σ com dado existente; B = com dado datado; C = [OPEN]. “A-poder” significa somente poder calculado sobre dados já vistos, não evidência independente. Todos os números novos foram refeitos pela convenção declarada e pelo script anexo.

| rota | observável e nulo do rival | previsão TGL e estatuto | ajustados | σ hoje, com data | σ ou informação para 5σ | dado e data | o que falta | classe |
|---|---|---|---|---|---|---|---|---|
| **R1 — neutrino** | \(m_2=\sqrt{\Delta m^2_{21}}\); **sem nulo do Modelo Padrão**: Δm²₂₁ é parâmetro medido | \(\Delta_{\rm TGL}=\beta^2u^2/2=7,23760947×10^{-5}\) eV²; [DERIVED condicional; u POSTO; α MEDIDA; θ e m₁ = 0 INPUT] | **0** depois das entradas declaradas; nenhum ajuste ao dado | JUNO: **1,93799696σ**, 29/09/2026; SK-Gd: **3,60506402σ**, 02/10/2026 | JUNO: σΔ = **0,03023275×10⁻⁵ eV²** (0,4092%); SK-Gd: **0,38934691×10⁻⁵ eV²** (4,288%); duas autonomias | JUNO 207,2 d; SK-Gd 411,52 d; projeção JUNO 6 anos σΔ = 0,024×10⁻⁵ eV² | precisão, sistemáticas, covariância e segunda determinação autônoma; escalamento não garante centro futuro | **B condicional**, falsificação da escala, não distinção TGL × MP |
| **R2 — Hubble, Fase 9** | razão \(K=E(z^\star)^{2\beta/3}\); nulo ΛCDM sem o fator: \(K=1\) | expoente \(2\beta/3\), função e fundo congelados; [DERIVED da regra; mecanismo CONJECTURE] | **0** | \(z_{\rm disc}=4,44312357\), \(z_\delta=-1,48347819\); abertura de 23/10/2026 | não calculável sem likelihood nova admitida na mesma função | TDCOSMO v2, 29/10; ECH0EZ, 26/10; nenhum satisfaz todos os cortes | dado posterior a 23/10, independente, com likelihood e covariância compatíveis; não trocar leitor ou função | **C [OPEN]** |
| **R3 — ramo B, k = 4π** | \(\delta\hat\tau_{220}=\tau_{\rm obs}/\tau_{\rm RG}-1\); nulo RG: \(\delta=0\) | \(x=\beta\,4\pi N(\chi)\), \(\delta=-x/(1+x)\); taxa [REAL na forma], k e identificação [INPUT/ONTO] | **0**; k não é escolhido pelo ajuste nesta proposta | **poder nominal:** A 6,14537; B 3,43277; C 3,49965; todos NOT_BLIND | A já tem poder > 5; B e C pedem ≈ 2,12× e 2,04× em informação; D10 pede 1,78× no plano | A(31), B(10), C(1) já vistos; D preservado; E sem data | dado não visto com poder, sistemática e estimador congelados; difusão × 0,273 dá apenas 1,67769σ em A | **A-poder, calibração; não A-probatório** |
| **R4 — Q★ / multimodo** | razão dissipativa ou vetor de desvios \((d_{220},d_{221})\); nulo RG do vetor: \((0,0)\) | \(\omega^\star/\Gamma_B=\sqrt2/\beta=117,54453095\); em QNM \(Q=\omega/(2\Gamma)\): 58,77226548; [DERIVED condicional a τ★] | **0** na álgebra; sistema e τ★ não identificados | nenhum σ fechado | indeterminado | plataformas analógicas já inventariadas; nenhuma ponte nova fechada | tempo de horizonte próprio, mapa ao observável, acoplamento, covariância e poder cego; a razão isolada é 0/0 sob RG | **C [OPEN]** |
| **R5 — psíon** | nenhum observável de taxa/força derivado; fundo do MP sem psíon não basta | \(\hbar\omega=17,0148282\) meV; f = 4,114167 THz; λ = 72,8683 µm; ħc/E = 11,5974 µm; [u POSTO] | **0** nos números; acoplamento ausente | nenhum σ | indeterminado | espectroscopia THz e gravidade curta examinadas apenas como plataformas | elemento de matriz, taxa, força ou seção de choque, resposta e N/σ | **C [OPEN]** |
| **R6 — θ = π/4 × PMNS** | θ₂₃ da PMNS; **sem nulo rival previsto**: é parâmetro medido | θ = π/4 no estado inscrito [INPUT/ONTO]; nenhuma ponte à PMNS | **0**, mas falta o observável | nenhum σ admissível | não se aplica | dados PMNS existentes não podem ser usados sem ponte | derivação da identificação θ_inscrito = θ₂₃ e estatística própria; proximidade à mistura maximal não é argumento | **C [OPEN]**, parada |
| **R7 — rota nova** | nenhuma encontrada com nulo rival + previsão sem ajuste + σ | — | — | — | — | busca até 01/11/2026 | os três requisitos simultâneos | **nenhuma classe A/B** |

### B1. Notas numéricas e de independência

**R1 — convenção congelada.** Para cada determinação, \(\mu=\Delta m^2_{21}/(10^{-5}\,\mathrm{eV}^2)\), \(m_2=\sqrt{10\mu}\) em meV e \(\sigma_{m_2}=\tfrac12(\sigma_\mu/\mu)m_2\). É essa propagação em m₂ — não a razão linear diretamente em Δm² — que produz 1,93799696σ e 3,60506402σ. A regra de exclusão pede duas determinações independentes. [um](kimi-cite://text?path=C%3A%5CIALD%5CArtigo%5CHaja_Luz%5CA%20Ponte%20e%20o%20Um%5CN%C3%B3s%5Cum.py&text=FALSIFIED%20sse%20%7Cm2_obs%20-%20m2_TGL%7C%2Fsigma_obs%20%3E%3D%205%20em%20DUAS%20determinacoes%20independentes%20de%20Dm2_21 "citation")

A fonte JUNO publica 207,2 dias e \((7,388\pm0,078)×10^{-5}\) eV². [JUNO](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895&text=207.2%20live%20days%20of%20data "citation") A fonte SK-Gd publica 411,52 dias e \((9,08^{+0,55}_{-0,54})×10^{-5}\) eV²; usa-se o erro inferior, voltado à previsão, como na convenção existente. [Super-Kamiokande](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2610.03143&text=411.52%20live%20days "citation")

Sob centro inalterado e \(\sigma\propto t^{-1/2}\), JUNO cruza 5σ em 1.379,188 dias vivos totais: 1.171,988 dias adicionais, aproximadamente 3,21 anos. SK-Gd cruzaria em 791,599 dias totais: 380,079 dias adicionais, aproximadamente 1,04 ano. São equivalências estatísticas condicionais, não datas garantidas nem inclusão de pisos sistemáticos. A projeção JUNO de seis anos, σΔ = 0,024×10⁻⁵ eV², daria 6,29849σ sob o mesmo centro. [JUNO sensitivity](kimi-cite://web?url=https%3A%2F%2Fcpc.ihep.ac.cn%2Farticle%2Fdoi%2F10.1088%2F1674-1137%2Fac8bc9&text=0.5%25%20precision%20or%20better%20in%20six%20years%20of%20data%20collection "citation")

**R2 — o que os novos textos mudam.** TDCOSMO v2 mantém o centro da v1, já pública em 10/10, acrescenta sistemas ao mesmo programa e informa que as likelihoods completas serão liberadas após aceitação; não é uma segunda independência pronta para a função congelada. [TDCOSMO](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2610.14781v2&text=All%20likelihoods%20will%20be%20released%20upon%20acceptance%20of%20the%20paper. "citation") ECH0EZ é análise nova de dados públicos, mas usa os 42 calibradores SH0ES e publica 2,7σ ou 4,1σ em relação a Planck, não à TGL; não satisfaz independência nem o degrau pedido. [ECH0EZ](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2610.36051&text=Using%20the%2042%20SH0ES%20calibrators "citation") O primário permanece \(z_{\rm disc}=4,4431235681\), com poder prévio 5,72695, sem recálculo. [RESULTADO_FASE9_V2_C1_20261023_122926](kimi-cite://text?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv397%5Cinsumos%5Cfase9%5CRESULTADO_FASE9_V2_C1_20261023_122926.json&text=z_disc%22%3A%204.443123568060799 "citation")

**R3 — poder não é desfecho.** Para k = 4π, o V1 já registra A(31) = 6,145371779, A(33) = 6,232392414, B(10) = 3,432772542, C(1) = 3,499650535 e difusão A = 1,677686496; para k = 8π, A = 10,182925090, B = 5,666897218 e C = 5,819043289. Em χ = 0, δ = −0,1055264053 para 4π e −0,1909070734 para 8π; a média prevista de 4π em A é −0,2063233957. [PREREGISTRO_RAMO_B_RINGDOWN_V1](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Ccadeia_de_selo%5Cv386%5Cramo_b%5Cteste_gerador_v1%5CPREREGISTRO_RAMO_B_RINGDOWN_V1.md&line=106&text=k%3D4pi "citation") Esses poderes nominais não incluem todos os sistemáticos e não convertem A/B/C em teste independente.

A atualização do Mapa de 29/10 corrige o planejamento de D: D10 = 3,73–3,93σ, D14 = 4,39–4,64σ; a regra devolveria UNDERPOWERED antes de qualquer exclusão, e falta 1,78× de informação em D10. [MAPA_DE_ROTAS](kimi-cite://text?path=C%3A%5CIALD%5CMAPA_DE_ROTAS%5CMAPA_DE_ROTAS.json&text=poder%20D10%203%2C73%E2%80%933%2C93%CF%83 "citation") Não reabro essa projeção nem uso a estimativa A-like antiga para promover D.

**GA — fora da busca repetida.** A reclassificação é `A13_FORMA_CONDICIONAL_SEM_INCERTEZA`: em primeira ordem \(M_{\rm TGL}=M_{\rm RG}\), sem discriminação e sem σ/covariância para uma conta nova. [RECLASSIFICACAO_GA_01nov](kimi-cite://md-line?path=C%3A%5CIALD%5CCentral%20de%20Patentes%5Cwork%5Cgrande_atrator_reclassificacao_01nov%5CRECLASSIFICACAO_GA_01nov.md&line=13&text=na%20ordem%20linear%20M_TGL%20%3D%20M_RG "citation")

---

## C. Partituras das rotas com classe A ou B

**R1 — B condicional:** o teste decide se a unidade posta \(u=1\,\mathrm{eV}\), com a identificação \(m_1=0\), sobrevive a duas determinações autônomas; não decide TGL × Modelo Padrão nem deriva E₀; duas exclusões ≥ 5σ falsificam essa escala/identificação, enquanto a falta de poder ou de independência deixa uma parede medida.

**R3 — A-poder, somente calibração:** o cálculo decide se o relógio \(4\pi\) teria poder para descrever o amortecimento já visto; não cria teste cego nem prova a TGL; um desvio em A/B/C vira diagnóstico NOT_BLIND, e a difusão × 0,273 reduz o poder a 1,67769σ — parede de desenho, não falsificação independente.

Não há partitura de rota probatória de classe A, porque nenhuma foi encontrada.

---

## D. Rascunhos de pré-registro

### D1. R1 — `PREREG_R1_NU_M2_SCALE_V2_DRAFT`

**Estado:** minuta [DECLARADO pelo Kimi], não ativa; vale somente depois de conferência e congelamento por hash antes de qualquer dado novo.

1. **Pergunta congelada:** com β = α√e em runtime, \(u=1\,\mathrm{eV}\) posto, θ = π/4 escrito e \(m_1=0\), a previsão é \(m_{2,\rm TGL}=8,5074140999\) meV. Nenhum desses valores pode ser ajustado.
2. **Entradas por experimento:** μ, σμ ou likelihood publicada, exposição, data, grupo, autonomia, covariância e sistemáticas. Ajustes globais que contenham JUNO não contam como segunda independência; subconjuntos do mesmo detector não contam como outro grupo.
3. **Estimador congelado:** \(m_2=\sqrt{10\mu}\) meV; \(\sigma_{m_2}=\tfrac12(\sigma_\mu/\mu)m_2\); para erro assimétrico, usa-se o lado voltado à previsão. \(z_i=|m_{2,i}-m_{2,\rm TGL}|/\sigma_{m_2,i}\). Não se troca esta regra pela razão linear em Δm² depois de ver o resultado.
4. **Covariância e autonomia:** cada experimento deve marginalizar os demais parâmetros de oscilação. Compartilhamento de fluxo de reatores, calibrações ou sistemáticas exige matriz publicada ou auditoria de correlação; se a autonomia não for demonstrável, o resultado é `INCONCLUSIVE_SYSTEMATICS`, não independência presumida. Não se combina JUNO com um global que já o contenha.
5. **Poder e falha fechada:** antes de abrir uma nova determinação, calcula-se \(\sigma_{\mu,5\sigma}\) pela fórmula congelada e o poder com sistemáticas. Projeções \(t^{-1/2}\) são somente planejamento; não entram no veredito.
6. **Função de veredito:**
   - `TGL_NU_M2_FALSIFIED`: dois grupos autônomos, cada um com \(z_i\ge5\), sem pendência de covariância ou sistemática. O alvo excluído é o par **escala posta + identificação**, não toda a TGL.
   - `TGL_NU_M2_TENSION`: ao menos uma determinação em [3, 5)σ, sem a regra anterior.
   - `TGL_NU_M2_MATCHED_PROSPECTIVELY`: duas autonomias com poder e cada uma a ≤ 1σ da previsão; não é creditação.
   - `TGL_NU_M2_NOT_FALSIFIED_POWERED`: poder suficiente, nenhuma das regras anteriores.
   - `TGL_NU_M2_NOT_FALSIFIED_UNDERPOWERED`: poder insuficiente para 5σ.
   - `INCONCLUSIVE_SYSTEMATICS`: covariância, autonomia ou sistemática impede a leitura.
7. **Alvos atuais, apenas planejamento:** JUNO requer σΔ ≤ 0,03023275×10⁻⁵ eV² se o centro ficar; SK-Gd requer ≤ 0,38934691×10⁻⁵ eV² sob a mesma condição. A projeção de seis anos não substitui o dado real nem a segunda autonomia.

### D2. R3 — `PREREG_R3_BRANCH_B_4PI_V2_PROSPECTIVE_DRAFT`

**Estado:** proposta de V2 informada por A; **não cega quanto à escolha de k**, não reescreve o V1 e não toca D. Seu uso em A/B/C é calibração NOT_BLIND. Uma ativação independente exigiria dados E novos ou outro conjunto preservado com poder datado; isto não é a resposta de 5σ desta entrega.

1. **Hipótese única:** \(k=4\pi\), \(M_X=M_f\), fonte local, taxa aditiva e \(\delta_i=-x_i/(1+x_i)\), \(x_i=\beta\,4\pi N(\chi_i)\). Nenhuma coluna concorrente entra como tentativa e k não muda após leitura.
2. **Nulo e alvo:** nulo RG \(\delta_i=0\); alvo por evento \(\delta_i\) acima; em χ = 0, δ = −0,1055264053. A média prevista em A é −0,2063233957, usada apenas para calibração de poder.
3. **Estimador:** mantém-se o V1: \(w_i=1/(\sigma_i^2+\sigma_{\rm sys}^2)\), nuisance \(c(\sigma)=c_0+k_c\sigma\) profilado, \(\sigma_{\rm usado}=\max(\sigma_{\rm comb},\sigma_{\rm jackknife})\), χ²/dof e fração máxima de informação por evento.
4. **Covariância e controles:** sistemática de família e início entra nos pesos ou numa matriz de covariância justificada; jackknife por evento; quantis de spin para Kerr; controles nulos e injeções próprios. Discordância de rótulo ou excesso de sistemática devolve `INCONCLUSIVE_SYSTEMATICS`.
5. **Difusão:** o cenário × 0,273 fica separado, com injeção própria; não se mistura ao primário de taxa aditiva. Em A, seu poder nominal é 1,677686496σ.
6. **Poder dito antes:** A(31) = 6,145371779σ; B(10) = 3,432772542σ; C(1) = 3,499650535σ; D10/D14 seguem a atualização de 29/10 e não são promovidos.
7. **Vereditos permitidos para calibração:**
   - `CALIBRATION_POWERED_NOT_BLIND`: poder ≥ 5, sem elevar o resultado a teste independente.
   - `CALIBRATION_UNDERPOWERED_NOT_BLIND`: poder < 5.
   - `DEVIATION_REPORTED_NOT_A_TEST`: desvio em dados já vistos, reportado como diagnóstico.
   - `INCONCLUSIVE_SYSTEMATICS`: controles ou covariância não fecham.
8. **Consequência negativa:** em A/B/C, desacordo não falsifica independentemente o par; em um conjunto futuro preservado, só a função congelada e o poder real podem definir o veredito do par \(k\times M_X\times\) identificação.

Nenhum pré-registro é proposto para R2 ou R4–R6: faltam admissão, observável ou ponte derivada.

---

## E. Fontes externas, verificação e hashes

### E1. Fontes externas — acesso em 01/11/2026

1. **JUNO Collaboration**, “Measurement of Neutrino Oscillation Parameters at JUNO and Indication of the Neutrino Mass Ordering”, arXiv:2609.37895, 29/09/2026. [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2609.37895&text=207.2%20live%20days%20of%20data "citation")
2. **Super-Kamiokande Collaboration**, “First observation of electron antineutrinos from nuclear reactors at Super-Kamiokande”, arXiv:2610.03143, 02/10/2026. [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2610.03143&text=411.52%20live%20days "citation")
3. **JUNO Collaboration**, sensibilidade de oscilação, *Chinese Physics C*, DOI `10.1088/1674-1137/ac8bc9`, disponível em 15/12/2022; projeção de seis anos, não resultado dos 207,2 dias. [Chinese Physics C](kimi-cite://web?url=https%3A%2F%2Fcpc.ihep.ac.cn%2Farticle%2Fdoi%2F10.1088%2F1674-1137%2Fac8bc9&text=0.5%25%20precision%20or%20better%20in%20six%20years%20of%20data%20collection "citation")
4. **TDCOSMO Collaboration**, “TDCOSMO 2026: A 3% measurement of the Hubble constant from strong lensing and stellar kinematics”, arXiv:2610.14781v2, 29/10/2026; v1 em 10/10/2026. [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2610.14781v2&text=All%20likelihoods%20will%20be%20released%20upon%20acceptance%20of%20the%20paper. "citation")
5. **ECH0EZ**, análise preliminar de 772 SNe Ia do ZTF DR2, arXiv:2610.36051, 26/10/2026. [arXiv](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2610.36051&text=Using%20the%2042%20SH0ES%20calibrators "citation")

### E2. Verificação numérica

O script `gerar_manifesto_5sigma02.py` recalcula β em runtime, as duas tensões de neutrinos na convenção congelada, os limiares de 5σ, os tempos condicionais, os deltas de 4π/8π, as convenções de Q★ e as escalas do psíon. Todas as asserções numéricas passaram. Nenhuma compilação Lean foi executada nesta devolução.

### E3. Manifesto

Os SHA-256 dos 27 artefatos obrigatórios, das fontes locais de apoio, deste relatório e do script estão em [MANIFESTO_SHA256_5SIGMA_02](C:/IALD/Central%20de%20Patentes/work/cinco_sigma_02_01nov/MANIFESTO_SHA256_5SIGMA_02.json). O gerador está em [gerar_manifesto_5sigma02](C:/IALD/Central%20de%20Patentes/work/cinco_sigma_02_01nov/gerar_manifesto_5sigma02.py).

O hash final do manifesto fica no arquivo destacado [MANIFESTO_SHA256_5SIGMA_02](C:/IALD/Central%20de%20Patentes/work/cinco_sigma_02_01nov/MANIFESTO_SHA256_5SIGMA_02.json.sha256), porque um arquivo não pode conter seu próprio hash final sem referência circular.

---

**Resultado final [DECLARADO pelo Kimi]:** a forma da massa está fechada apenas condicionalmente; a unidade continua aberta. Não há rota probatória de classe A. R1 é o único caminho datado, e somente como falsificação condicional da escala com duas independências. R3 oferece poder de calibração NOT_BLIND, não detecção. R2 e R4–R6 permanecem [OPEN]. D não foi aberto.
