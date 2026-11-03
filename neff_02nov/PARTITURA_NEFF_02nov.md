# PARTITURA DE N_eff — nucleossíntese pura e combinação completa

**Data:** 02/11/2026  
**Estatuto:** **[DECLARADO pelo Kimi]**, até decisão do operador e conferência da gerência.  
**Estado:** `D8_PENDING` · `OPEN_X16_NO_SELECTION` · `E3_AWAITING_OPERATOR` · `TGL_LIKELIHOOD_EVALUATED = false`.  
**Escopo:** desenho e aritmética de poder. Nenhum dado admitido, nenhuma execução de natureza, nenhum ajuste, nenhuma alteração do V1, do canal, do gate ou do frozen.

---

## 1. A pergunta e o que o teste decide

**Pergunta:** a inscrição TGL da radiação, lida como um excesso fixo \(\Delta N_{\rm eff}>0\), sobrevive a duas determinações independentes de \(N_{\rm eff}\), sem ajuste ao dado?

| objeto | valor e estatuto |
|---|---|
| Nulo do Modelo Padrão | \(\Delta N_{\rm eff}=0\), equivalente a \(N_{\rm eff}^{\rm SM}=3,044\) |
| Previsão TGL-S | \(\Delta N_{\rm eff}=0,119466075253733\), logo \(N_{\rm eff}^{\rm TGL}=3,163466075253733\) |
| Estatuto da previsão | **[DERIVED condicional ao fechamento \(\rho+p\)]**; β = α√e em runtime; zero ajuste ao novo dado |
| Natureza dimensional | **número puro**; não herda \(u=1\,\mathrm{eV}\) |
| Escopo desta partitura | **TGL-S**; TGL-L não é reavaliado |
| Alvo de eventual exclusão | o par **mapa × observável**, não β isolado nem toda a TGL |

A previsão e a regra já existiam no V1 congelado; não são uma nova escolha feita depois do dado. [PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1](kimi-cite://text?path=C%3A%5CIALD%5CBancada_Um%5Cinvestigacao%5Cpreregistro_fase8_primordial%5CPREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json&text=%22delta_N_eff%22%3A%200.11946607525373273 "citation")

**Partitura em uma linha:** o teste decide se essa identificação da radiação resiste a duas leituras independentes; não deriva E₀, não prova a TGL e não cria creditação. Duas exclusões ≥ 5σ derrubam o par mapa × observável; ausência de poder ou de independência é parede medida.

---

## 2. Os dois canais, sem misturar seus estatutos

### Canal A — nucleossíntese pura, He LBT + D

Entram somente hélio e deutério primordiais e a rede BBN:

- \(Y_P^{\rm LBT26}=0,2458\pm0,0013\);
- \((\mathrm{D/H})_P\times10^5=2,547\pm0,104\);
- resultado: \(N_{\rm eff}=2,976\pm0,093\), média posterior e intervalo bilateral de 68%.

Não entram Planck, ACT, SPT, lensing, BAO ou polarização. [Goldstein & Hill, §III](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2603.13226v2%23S3&text=Using%20only%20primordial%20helium%20and%20deuterium%20abundance%20measurements "citation")

**Estatuto:** `BACKGROUND_ONLY`. Não usa anisotropias nem evolução perturbativa do CMB; portanto, a ressalva perturbativa não se aplica a este cálculo. Permanece a exigência de que a identificação TGL não altere separadamente as taxas nucleares ou outros ingredientes da BBN. Se for necessária a BBN TGL exata, D5b continua sendo uma reserva separada.

### Canal B — combinação completa

Entram He + D + CMB-PAS + DESI DR2 BAO, com lensing conjunto e **sem** Planck low-\(\ell\) EE na configuração basal:

\[
N_{\rm eff}=2,990\pm0,070 .
\]

O valor é a média posterior e intervalo bilateral de 68%. [Goldstein & Hill](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2603.13226v2&text=This%20is%20the%20main%20result%20of%20this%20brief%20paper "citation")

**Estatuto:** `FULL_COMBINATION_REQUIRES_PERTURBATIVE_CLOSURE`. O ajuste publicado é em \(\Lambda\)CDM + \(N_{\rm eff}\), não uma likelihood TGL. Para usá-lo como teste TGL-S são necessárias, pelo menos:

1. radiação free-streaming com \(N_{\rm eff}(\beta)\);
2. a peça de matéria \(\omega_{c,\rm eff}=\omega_c+\beta(\omega_b+\omega_c)\), derivada do mesmo β;
3. resposta perturbativa própria para TT/TE/EE, lensing e BAO;
4. mesmas escolhas de dados, cortes, priors e nuisances, sem dupla contagem.

Fixar apenas \(N_{\rm eff}=3,163466\) dentro do ajuste alheio não implementa TGL-S. Se a equivalência efetiva mudar entre BBN e recombinação, um único \(N_{\rm eff}\) constante também é insuficiente.

---

## 3. Contas de poder e de tensão

Convenção: diagnóstico gaussiano unidimensional, com a previsão TGL tratada como exata. Não são posteriors TGL nem vereditos. A coluna “σ exclusão” usa o centro atual como se ele permanecesse inalterado.

| bloco | \(z_{\rm TGL}\) ao centro | \(z_{\rm SM}\) ao centro | separação TGL–SM | σ para 5σ de separação | σ para excluir TGL a 5σ se o centro persistir | melhoria necessária, separação / exclusão |
|---|---:|---:|---:|---:|---:|---:|
| **A — He+D puro:** 2,976 ± 0,093 | 2,0158 | 0,7312 | 1,2846 | 0,0238932 | 0,0374932 | 3,892× / 2,480× |
| **B — CMB-PAS+DESI sem abundâncias:** 3,010 ± 0,110 | 1,3951 | 0,3091 | 1,0861 | 0,0238932 | 0,0306932 | 4,604× / 3,584× |
| **Completa:** 2,990 ± 0,070 | 2,4781 | 0,7714 | 1,7067 | 0,0238932 | 0,0346932 | 2,930× / 2,018× |

As contas e as asserções estão em [CONTAS_PARTITURA_NEFF](C:/IALD/Central%20de%20Patentes/work/neff_02nov/CONTAS_PARTITURA_NEFF.json), geradas por [calcular_partitura_neff](C:/IALD/Central%20de%20Patentes/work/neff_02nov/calcular_partitura_neff.py).

**Leitura correta:** hoje o centro está mais próximo do Modelo Padrão. Não se inverte esse sinal. A separação TGL–SM mede poder; a tensão ao centro mede outra coisa, e as duas ficam lado a lado conforme D9.

### O limite de 95% não é uma exclusão TGL pronta

Na combinação completa, com prior unilateral \(\Delta N_{\rm eff}>0\), os autores publicam \(\Delta N_{\rm eff}<0,107\) a 95%. A previsão TGL excede esse teto em:

\[
0,1194660753-0,107=0,0124660753,
\]

ou 11,65% do limite. Isso é **desfavor/tensão indicativa** sob o mapeamento efetivo, mas não uma exclusão TGL robusta: o limite usa \(\Lambda\)CDM + \(N_{\rm eff}\), outro conjunto de priors e marginalizações, não fornece significância para o ponto TGL e não contém sua resposta perturbativa própria. [Goldstein & Hill, §III](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2603.13226v2%23S3&text=Combining%20the%20primordial%20abundance%20measurements%20with%20CMB%20%28without%20low-%E2%84%93%20EE%29%20and%20BAO%20observations "citation")

---

## 4. Independência e covariância

### Partição candidata para duas determinações

1. **Bloco A:** He+D puro, \(2,976\pm0,093\);
2. **Bloco B:** CMB-PAS+DESI sem abundâncias, \(3,010\pm0,110\).

Essa é a partição mais limpa porque separa os blocos observacionais. Ela **não dispensa** a auditoria de covariância, nuisances e da ponte perturbativa do bloco B.

### O que não conta como duas independências

- a combinação completa e qualquer subconjunto dela;
- v1 e v2 da mesma fonte;
- `BBN_CONSISTENCY` e `FREE` sobre o mesmo conjunto;
- duas pipelines sobre os mesmos dados;
- DESI DR1 e DR2, que são amostras aninhadas;
- três posteriors de lensing multiplicados como se fossem independentes.

P-ACT usa cortes para reduzir sobreposição Planck–ACT, e a lensing Planck–ACT–SPT deve permanecer uma única likelihood conjunta, com covariâncias cruzadas. [ACT DR6](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2503.14454v2&text=This%20combination%20is%20built%20to%20increase%20constraining%20power%20while%20minimizing%20the%20overlap%20between%20the%20two%20experiments%20and%20allowing%20us%20to%20neglect%20their%20covariance. "citation"), [Qu et al.](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2504.20038v2&text=The%20cross-covariance%20between%20ACT%20and%20Planck "citation")

**Regra fail-closed:** covariância ou classificação de sobreposição ausente ⇒ `INCONCLUSIVE_SYSTEMATICS`, não independência presumida. Não se usa média ponderada nem produto de posteriors marginais como substituto da likelihood conjunta.

---

## 5. D8 — ficha de admissão das fontes

D8 é a **admissão explícita das fontes primárias pelo operador, identificadas por SHA-256**. Ter bytes, extrair corretamente uma tabela ou calcular um hash não cumpre D8 automaticamente. O canal atual continua devolvendo `source_admission = D8_PENDING`. [neff_canal](kimi-cite://text?path=C%3A%5CIALD%5CBancada_Um%5Cbancada%5Cneff_canal.py&text=%22source_admission%22%3A%20%22D8_PENDING%22 "citation")

### Fonte nova candidata, fora do elenco original do V1

| campo | valor |
|---|---|
| fonte | Goldstein & Hill, arXiv:2603.13226v2 |
| data da versão | 20/03/2026, 03:01:33 UTC |
| arquivo local | `work/neff_02nov/fontes/Goldstein_Hill_2603.13226v2.pdf` |
| bytes | 7.064.517 |
| páginas | 14 |
| SHA-256 | `13055d9f51bf2205ac72ced2d5d358a54f4e9e21b02e925dddaf57b8abe17618` |
| estado | **D8_PENDING_OPERATOR_EXPLICIT_DECISION** |

A ficha legível por máquina está em [FICHA_D8_GOLDSTEIN_HILL](C:/IALD/Central%20de%20Patentes/work/neff_02nov/FICHA_D8_GOLDSTEIN_HILL.json).

### Fontes já nomeadas no V1

`1807.06209`, `2503.14454`, `2506.20707`, Cooke+2018, Steigman 2007, Cyburt+2016 e Aver permanecem nas fichas congeladas. Não são admitidas “por arraste” pela nova fonte. Se usadas decisoriamente, sua admissão precisa ser explícita, com versão e hash correspondentes. [PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1](kimi-cite://text?path=C%3A%5CIALD%5CBancada_Um%5Cinvestigacao%5Cpreregistro_fase8_primordial%5CPREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json&text=%22D8%22%3A%20%22fontes%20por%20sha256 "citation")

### Ressalva de auditoria do canal

O canal atualmente instalado não é o candidato R3 auditado e não possui auditoria c1 própria. Esta partitura **não reivindica** para o binário instalado a auditoria do candidato, nem apresenta o canal como o módulo cujo hash consta no V1.

**Decisão D8 a deixar em branco para o operador:** admitir ou recusar Goldstein & Hill `2603.13226v2`, com o hash acima; admitir ou recusar cada fonte antiga efetivamente usada, sem mudar `n_alvos_sem_hash` antes dessa decisão.

---

## 6. X16 — escolha de \(Y_p\), ainda aberta

X16 exige escolher **simultaneamente** a versão da fonte e a hipótese de \(Y_p\). As quatro linhas permanecem não selecionadas; `primary_observation = None` e `veredito = NENHUM`.

| versão | hipótese | CMB-SPA, Tabela 5 | tensão documental TGL, apenas diagnóstico |
|---|---|---:|---:|
| v1 | `BBN_CONSISTENCY` | 2,81 ± 0,12 | 2,9456σ |
| v1 | `FREE` | 2,99 +0,22/−0,26 | 0,7885σ, cauda superior |
| v2 | `BBN_CONSISTENCY` | 2,82 ± 0,12 | 2,8622σ |
| v2 | `FREE` | 2,96 +0,21/−0,24 | 0,9689σ, cauda superior |

A tensão usa \(N_{\rm TGL}=3,1634660753\); no ramo `FREE`, a cauda superior é a voltada à previsão acima do centro. Ela não é critério para escolher a linha.

**Errata obrigatória:** a antiga linha `2,97 ± 0,12` não é CMB-SPA da Tabela 5 e não deve ser usada. A presença de `opcoes_CMB_SPA_Yp` somente com v2 na saída do canal é conveniência de apresentação, **não escolha X16 de v2**.

**Decisões X16 a deixar em branco para o operador:**

- versão: **v1 ou v2**;
- hipótese: **BBN_CONSISTENCY ou FREE**;
- se `FREE`: ratificar previamente a convenção de cauda para \(z\) e para poder;
- se `BBN_CONSISTENCY`: decidir separadamente se D5b/BBN TGL exata será exigido.

Não se escolhe a opção por produzir menor tensão, e nenhuma dessas linhas conta como outra independência.

---

## 7. Função de veredito preservada

A partitura não altera a função congelada `veredito_fase8_v1`. A ordem fail-closed é:

1. **`AWAITING_SOURCE`** — fonte ou parametrização necessária ausente.
2. **`INCONCLUSIVE_SYSTEMATICS`** — alvo sem hash; ou, havendo mais de uma análise independente, \(\chi^2_{\rm int}/(n-1)>2\) ou \(p_{\rm dispersao}<0,01\).
3. **`FALSIFIED_AT_5SIGMA`** — **duas ou mais** análises independentes com \(|z|\ge5\). Uma única análise ≥ 5σ não basta; o alvo é o par mapa × observável.
4. **`TENSION_3_TO_5_SIGMA`** — alguma análise independente com \(|z|\ge3\), sem a regra anterior.
5. **`NOT_FALSIFIED_UNDERPOWERED`** — poder < 5 depois de nenhum ramo anterior casar.
6. **`NOT_FALSIFIED_POWERED`** — nos demais casos.

A função e seus testes sintéticos estão no V1; o sufixo congelado e a imobilidade do gate devem ser preservados pelo runner. [PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1](kimi-cite://text?path=C%3A%5CIALD%5CBancada_Um%5Cinvestigacao%5Cpreregistro_fase8_primordial%5CPREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json&text=%22funcao_de_veredito%22%3A%20%7B "citation")

Não se preenchem `dispersao_por_gl` ou `p_dispersao` com valores sintéticos como se fossem observados. O token antigo `POWER_P1P00_OF_5_SIGMA` é apenas o predeterminado do elenco antigo e não se transporta após X16 ou da inclusão da nova fonte.

---

## 8. O que falta antes de qualquer execução

### Para o canal puro

- [ ] D8 explícito para as fontes usadas;
- [ ] X16 somente se CMB-SPA/Yp entrar no desenho;
- [ ] confirmar se a equivalência BBN é suficiente ou se D5b é necessária;
- [ ] classificação de independência e covariância;
- [ ] runner hasheado e palavra E3 do operador.

### Para a combinação completa

- [ ] todos os itens acima que forem pertinentes;
- [ ] fechamento TGL-S de radiação **e matéria**;
- [ ] likelihood perturbativa própria, com os mesmos dados e nuisances;
- [ ] covariância e dupla contagem aprovadas;
- [ ] convergência e priors declarados;
- [ ] nenhum uso do ajuste \(\Lambda\)CDM + \(N_{\rm eff}\) como se fosse likelihood TGL.

### Classe atual

- **Não é classe A:** não há duas determinações independentes ≥ 5σ.
- **Não é classe B:** nenhum instrumento documentado em disco alcança \(\sigma(N_{\rm eff})=0,0239\).
- **Estado:** `OPEN_D8_X16_PERTURBATIVE_CLOSURE`.

As projeções históricas de CMB-S4 e SO ampliado não são calendário operacional. A frase permitida continua sendo: 5σ de separação pede \(\sigma(N_{\rm eff})\le0,0238932151\); nenhum instrumento documentado chega lá. [PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1](kimi-cite://text?path=C%3A%5CIALD%5CBancada_Um%5Cinvestigacao%5Cpreregistro_fase8_primordial%5CPREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json&text=nenhum%20instrumento%20documentado%20em%20disco%20chega%20la "citation")

---

## 9. Folha de decisão do operador

**D8 — Goldstein & Hill `2603.13226v2`:**  
[  ] admitir com SHA-256 `13055d9f51bf2205ac72ced2d5d358a54f4e9e21b02e925dddaf57b8abe17618`  
[  ] recusar

**X16 — CMB-SPA/Yp:**  
[  ] v1 `BBN_CONSISTENCY`  
[  ] v1 `FREE`, cauda a ratificar: __________  
[  ] v2 `BBN_CONSISTENCY`  
[  ] v2 `FREE`, cauda a ratificar: __________  
[  ] nenhuma linha CMB-SPA nesta etapa

**Escopo físico:**  
[  ] somente nucleossíntese pura nesta etapa  
[  ] combinação completa somente após fechamento perturbativo TGL-S  
[  ] outro: __________

**Partição de independência:**  
[  ] A = He+D; B = CMB-PAS+DESI sem abundâncias  
[  ] outra partição justificada: __________  
[  ] ainda não demonstrada

**E3 — execução:** permanece **FECHADA** até palavra expressa do operador depois de D8, X16, escopo, covariância e runner hasheado.

---

**Resultado [DECLARADO pelo Kimi]:** \(N_{\rm eff}\) tem nulo rival, previsão adimensional e dados públicos úteis. A nucleossíntese pura oferece o canal de fundo mais limpo; a combinação completa oferece mais precisão, mas exige uma likelihood TGL perturbativa própria. Hoje não há 5σ, nem duas independências, nem calendário documentado para 5σ. A partitura deixa D8/X16 prontos para decisão sem executar o teste.
