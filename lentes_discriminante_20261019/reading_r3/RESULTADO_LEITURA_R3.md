# Leitura D1b nas lentes — previsão existente, parte identificável e precisão necessária

19/10/2026. Em nome de codex-gerente-tgl; F8.LENTES_5SIGMA_20261019, reivindicação1009. [DERIVED condicional / OPEN na ponte de observáveis]. Nenhum dado observado foi composto.

## 1. A previsão escalar existe: não deve ser apagada

A v393 e o pré-registro da Fase9 incluem TDCOSMO na hipótese H0_lens=K·H0_bg. O K tem uma identidade formal própria na lei do contraste. A auditoria posterior e a projeção F3.1 de08/10 preservam, ao mesmo tempo, “TGL likelihood map OPEN” paraL5. D1B_OPTICAL_CONTRACT_R3.md e seus excertos/pinos recuperam ambas as afirmações, com fontes e linhas. O que falta é a tradução do estimador/likelihood de lentes, não a existência de uma previsão escalar ou do trabalho anterior.

A regra R-G vigente é

\[
H_{\rm fit}/H_{\rm bg}=f_\phi/(f_tF_D),\qquad
F_D=f_lf_s/f_{ls},\quad f_\phi=\Delta\phi_{\rm fit}/\Delta\phi_{\rm true}.
\]

A hipótese escalar equivale a exigir f_t F_D/f_phi=1/K. Esse é um **critério de correspondência a satisfazer pela construção**. Fixar o produto não especifica os três fatores, a resposta das imagens ou a covariância da massa inferida. A previsão pode ser testada como hipótese de uma compressão, com esse alcance explícito; uma dedução por trajetória exige o consumidor óptico completo ou prova de invariância dessa compressão.

## 2. O termo entre lente e fonte foi derivado para a extensão óptica explícita

Se — hipótese adicional, não promovida ao cânone — a integral acumulada da leitura SN for a distância radial de uma geometria FLRW óptica plana, defina

\[
\nu=2\beta/3,\quad J(z)=\int_0^z E(u)^{\nu-1}du,\quad
\chi_A(z)=\frac{c}{H_0K_*}J(z).
\]

Então D_ls=[χ_A(z_s)−χ_A(z_l)]/(1+z_s), e

\[
D_{\Delta t,A}=\frac{c}{H_0K_*}\frac{J_lJ_s}{J_s-J_l},\qquad
\frac{D_{\Delta t,A}}{D_{\Delta t,bg}}=\frac{Q_lQ_s}{K_*Q_{ls}}.
\]

Q_ls é a média integrada no intervalo entre lente e fonte, não k(z_s). A fonte do motor implementa a leitura em SN/cronômetros; não encontramos nela a promoção geral à geometria de lente. O cálculo aqui testa essa extensão explicitamente, sem misturá-la com o fundo local H²(1+β|1+w|) daR2 ou aplicarβ duas vezes no mesmo consumidor.

### Nova degenerescência geométrica

Em geometria plana, 1/D_Δt=1/χ_l−1/χ_s. Portanto χ̃=χ/(a+bχ) dá D̃_Δt=D_Δt/a: o parâmetro b cancela em todos os pares. Isso é uma identidade de distâncias; não demonstra invariância de arcos/kinemática nem equivale à transformação de folha de massa. A primeira correção quadrática de J em função da distância de fundo segue essa direção invisível a atrasos na ordem correspondente. Não foi alegado que o J completo seja uma transformação de Möbius.

### Cálculo sintético da forma restante

Plano anterior à execução: cinco pares de redshift iguais aos controlesR2, Ωm=0,3, Ωr=0 e escala H0K*=70. São escolhas de planejamento em baixos redshifts. O fator K* comum fica exatamente absorvido na escala livre. Após ajustar escala eΩm do comparador, o maior residual é **3,77968×10⁻⁵**, ou0,00378%; a norma com cinco erros independentes de1% é **0,00615**. Para norma5 nesse desenho ideal, os erros individuais teriam de ser aproximadamente **1,23×10⁻⁵ em fração**, ou0,00123%.

O perfil apenas da escala deixa residual máximo4,99123×10⁻⁴. Isso mostra quanto a liberdade adicional de matéria absorve. A quadratura128/256 foi conferida, diferença máxima1,33×10⁻¹⁵. O ajuste foi procurado numa grade de401 valores e refinado no melhor intervalo, incluindo extremos; não é prova formal de mínimo global. Um ajuste melhor reduziria a separação. Nenhum perfil de massa ou convergência externa foi fixado por dado: acrescentá-los pode reduzir informação ainda mais.

Esses números não são a previsão única da TGL nem uma significância observada: respondem à pergunta condicional sobre a forma da extensão óptica testada.

## 3. A referência externa muda o teste: o K comum não deve ser descartado

Permitir H0 inteiramente livre apaga K. Isso **não representa** o teste escalar da casa, que tem uma referência externa de fundo. Por isso calculamos separadamente o cenário do contrato existente, sem usar o centro observado das lentes.

O draft pinado fornece BG1=68,531 eσ_bg=0,301km/s/Mpc; Ωm,Ωr,z_* permitem recalcular K, comβ=ALPHA_FINE_CODATA_2018·√e em runtime. Resultado:

\[
K=1,0838071748529643,\qquad
\Delta H=(K-1)H_{\rm bg}=5,7433894998484964\ {m km/s/Mpc}.
\]

Para duas medições gaussianas independentes — uma de fundo e outra do leitor de lentes — a distância Asimov ao modelo de Hubble comum é

\[
Z_A=\frac{\Delta H}{\sqrt{\sigma_{\rm lente}^2+\sigma_{\rm bg}^2}}.
\]

É uma fórmula de separação prevista sob a hipótese escalar. Não é um teste sobre o centro TDCOSMO. Mantemos K fixo e não acrescentamos incerteza/correlação deΩm,z_* ou erro de mapeamento: o cenário é otimista, não a likelihood final.

| Erro de lente usado como cenário gaussiano | Separação prevista com BG1 | Limite ideal com fundo exato |
|---|---:|---:|
| 2,3km/s/Mpc | 2,476 | 2,497 |
| 2,4km/s/Mpc | 2,374 | 2,393 |
| 3,9km/s/Mpc | 1,468 | 1,473 |

As barras2,3/2,4 vêm da assimetria publicada emTDCOSMO2026 e são dois cenários simétricos de planejamento, sem recuperar sua likelihood;3,9 é a barra superior2025. Não somamos2025 e2026, que compartilham lentes, nem juntamos isso ao compostoFase9. Fontes públicas já custodiadas naR1.

O requisito ideal para mediana5 é **σ_lente≤1,10854km/s/Mpc**, mantendoσ_bg=0,301 e todas as hipóteses acima. Isso corresponde aproximadamente a1,5% da previsão local, não aos0,24% do cenário genéricoδ=β daR1. São amplitudes/modelos distintos; a R1 já estava explicitamente condicionada a uma amplitude ilustrativa. Mediana5 não é90% de probabilidade de descoberta. A independência do fundo e dos priors usados pela análise de lentes requer verificação na likelihood real.

## 4. Estado da meta e próximo ato técnico

**Avanço:** previsão escalar preservada e localizada; integral entre dois redshifts derivada para extensão nomeada; parte de forma após ajustes calculada; distinção entre escala livre e fundo externo quantificada. **Pendente:** construir o mapa físico do estimador por trajetória ou demonstrar a invariância da compressão, com massa/anisotropia/ambiente e calibração compartilhadas. O contrato da casa já marca essa pendência, que não pode ser fechada apenas substituindo H0 no resultado publicado.

O acervo público oferece uma likelihood hierárquica TDCOSMO2025 com massa/anisotropia e computação explícita de D_d,D_s,D_ds. A documentação oficial identifica essas entradas (https://cosmosis.readthedocs.io/en/latest/reference/standard_library/tdcosmo.html, já custodiada naR1). Ela é um consumidor possível depois da ponte; não instalamos nem executamos esse software. O pacote2026 consultado anuncia disponibilização dos dados/likelihood após aceitação; disponibilidade futura não é presumida.

O próximo trabalho útil é recuperar/construir a lei de leitura de relógio, feixe e potencial que realize o produto f_t F_D/f_phi=1/K, e testar sua compatibilidade conjunta com cinemática e fonte. Não pedir novamente uma definição abstrata de identidade; não escolher fatores para ajustar o número. Se a ponte não existir nas fontes nem for derivável das hipóteses tipadas, a lacuna deverá ficar explícita como informação física adicional necessária.

Não houve5σ observado nesta etapa. Meta empírica segue aberta, sem alterar kernel, programa, dados observados, Bancada ou gate. Fontes/plano/scripts/resultados são novos e pinados; revisão independente em REVIEW_R3.json, quando emitida, delimita o alcance sem promoção automática ao cânone.
