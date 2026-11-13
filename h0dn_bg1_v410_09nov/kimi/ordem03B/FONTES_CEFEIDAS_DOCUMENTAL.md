# Fontes de Cefeidas — registro documental, não priors prontos

**Estatuto:** `[KNOWN] documental` · `[DECLARADO pelo Kimi]` · `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO`  
**Ordem vigente:** `ORDEM_KIMI_H0DN_03C_11nov.md`  
**SHA-256 da ordem:** `d0df9b4430ca9ff9d4fccb74ffcddc789819a5f29f7b030aa461a09c5a7c6836`  
**Escopo:** somente literatura pública. Os números abaixo são resultados publicados, não leituras de `y_obs` nem insumos para cálculo de D, Z, t, ĥ ou razão.

## 1. O que precisaria ser demonstrado antes de um prior

No desenho H0DN, `cCep` é a direção acrescentada às equações de hospedeiro Cefeida retidas (`+1 mag` nessas linhas e zero nas demais). Uma restrição publicada só poderia definir `σ_b` em `C(σ_b)=C0+σ_b² cCep cCepᵀ` se fossem demonstrados, antes de qualquer rota observada:

1. **identidade formal do estimando:** mesma combinação linear, sinal, unidade, amostra, âncora, slope, transformações de cor e convenção afim de `cCep`;
2. **independência estatística:** nenhuma reutilização não controlada de fotometria, Cefeidas, SNe, âncora, calibrações ou ajustes comuns;
3. **covariância cruzada com o H0DN:** covariância entre a restrição externa e as equações/parâmetros da rede, incluindo os compartilhamentos;
4. **congelamento:** fonte, variante, prior e regra de uso escolhidos por fundamento físico antes de abrir o observado, nunca pelo D resultante.

Sem todos esses pontos, os valores permanecem documentais. Não se pode atribuir diretamente `σ_b=0,03`, `0,032`, `0,029`, `0,028` ou `0,057` mag.

## 2. Riess et al. 2023 — NGC 4258 e NGC 5584

**Resultados publicados.** Diferenças `JWST − HST` dos interceptos das relações P–L Wesenheit:

- **NGC 4258:** `0,00 ± 0,03 mag`;
- **NGC 5584:** `0,02 ± 0,03 mag`.

**O que medem.** Comparam interceptos P–L obtidos com fotometria JWST/NIRCam e HST, no sistema Wesenheit NIR com cor HST e transformações de banda. A comparação testa principalmente diferenças fotométricas/crowding nesses dois sistemas e hospedeiros; não é uma medida direta de um offset instrumental absoluto, pois há transformações de banda, metallicity, fase, slope e cancelamentos entre degraus.

**Por que não são priors independentes prontos.** Os dois interceptos não são, sem uma derivação adicional, o mesmo escalar `cCep` da rede. A comparação reutiliza identificações/cores HST e produtos SH0ES/R22; NGC 4258 também é âncora geométrica da rede. A covariância entre os dois resultados e com o H0DN não é fornecida pelo par de marginais.

**URLs primárias.**

- https://arxiv.org/abs/2307.15806
- https://arxiv.org/html/2307.15806
- DOI: https://doi.org/10.3847/2041-8213/acf769

## 3. Riess et al. 2024a — cinco hospedeiras de oito SNe Ia

**Resultado publicado.** `Δμ = −0,011 ± 0,032 mag` para a diferença média entre distâncias determinadas com HST e JWST, preservando a convenção de diferença da fonte.

**O que mede.** Um contraste de módulos de distância P–L em cinco hospedeiras de oito SNe Ia, com mais de 1000 Cefeidas, mesma banda NIR equivalente, mesmo slope e mesma âncora geométrica NGC 4258. É uma média de diferenças de distância, não um intercepto instrumental isolado nem automaticamente o parâmetro de viés diferencial `cCep`.

**Por que não é prior independente pronto.** A amostra e os dados HST/SH0ES se sobrepõem ao H0DN; NGC 4258 e transformações/calibrações são compartilhados. A média e sua incerteza não informam, sozinhas, a covariância cruzada com as linhas H0DN nem a correspondência formal com a direção `cCep`. A aproximação do resumo `−0,01 ± 0,03 mag` não deve substituir o valor de precisão maior quando a variante exigir este último.

**URLs primárias.**

- https://arxiv.org/abs/2401.04773
- https://arxiv.org/html/2401.04773
- DOI: https://doi.org/10.3847/2041-8213/ad1ddd

## 4. Riess et al. 2025 — 19 hospedeiras e NGC 3447A

### 4.1 Amostra de 19 hospedeiras de 24 SNe Ia

**Resultado publicado.** Diferença média `−0,022 ± 0,029 mag` entre as distâncias HST e JWST, na convenção da figura/texto da fonte, com as medidas ancoradas em NGC 4258.

**O que mede.** O contraste agregado de distâncias Cefeida HST/JWST nos ciclos 1–2, para 19 hospedeiras de 24 SNe Ia. Mistura produtos F150W e F115W com suas respectivas transformações e tratamentos de slope; não é uma única medida instrumental nem um contraste independente da rede.

**Por que não é prior independente pronto.** Esses produtos JWST já são insumos do H0DN considerado neste desenho. Usar a média novamente como prior independente duplicaria informação. Além disso, faltam a decomposição das covariâncias comuns e a identidade formal com `cCep`.

### 4.2 NGC 3447A versus componente espiral

**Resultado publicado.** `0,002 ± 0,028 mag` para a diferença formal entre os dois campos **JWST**.

**O que mede.** Uma comparação puramente diferencial entre Cefeidas da região NGC 3447A, quase livre de fundo estelar antigo, e da componente espiral de NGC 3447. A própria fonte destaca independência da distância a NGC 4258 e da medida de suas Cefeidas para esse contraste interno.

**Por que ainda não é prior independente pronto.** Ser interno JWST e independente da âncora não o transforma em medida HST × JWST nem em estimador de `cCep`. O contraste responde a diferenças entre duas regiões/componentes e seus ambientes; sua ligação com o viés diferencial da rede precisa ser derivada, e a covariância com o restante do H0DN precisa ser demonstrada.

**URLs primárias.**

- https://arxiv.org/abs/2509.01667
- https://arxiv.org/html/2509.01667
- https://iopscience.iop.org/article/10.3847/2041-8213/ae0ad6
- DOI: https://doi.org/10.3847/2041-8213/ae0ad6

## 5. Sharon et al. 2024 — viés de blending por amplitudes

**Resultado publicado.** `γ = 0,013 ± 0,057 mag`, usando a calibração empírica de `A555/A350`.

**O que mede.** Um possível viés sistemático de blending inferido da comparação entre razões de amplitudes de curvas de luz de Cefeidas extragalácticas e da Via Láctea, após correções de crowding e transformações de filtros. O artigo enfatiza que `γ` é o parâmetro de um teste nulo de crowding não reconhecido, não um componente da determinação direta de H0.

**Por que não é prior independente pronto.** O estimando é uma amplitude-derived blending correction, não o contraste de distâncias representado por `cCep`. A análise usa dados/produtos R20/SH0ES e transformações calibradas com amostras que se conectam à rede; independência e covariância cruzada não estão demonstradas. A incerteza de `γ` inclui uma sistemática de transformação de filtros que não pode ser transplantada sem refazer a propagação para o estimando H0DN.

**URLs primárias.**

- https://arxiv.org/abs/2305.14435
- https://arxiv.org/html/2305.14435v3
- https://academic.oup.com/mnras/article/528/4/6861/7608532
- DOI: https://doi.org/10.1093/mnras/stae451

## 6. Conclusão documental congelada

| Fonte | Resultado documental | Estimando imediato | Pronto para `σ_b`? |
|---|---|---|---|
| Riess 2023 N4258 | `0,00 ± 0,03 mag` | JWST−HST, intercepto P–L Wesenheit | **Não** |
| Riess 2023 N5584 | `0,02 ± 0,03 mag` | JWST−HST, intercepto P–L Wesenheit | **Não** |
| Riess 2024a | `Δμ = −0,011 ± 0,032 mag` | diferença média de módulos HST/JWST em cinco hosts | **Não** |
| Riess 2025, 19 hosts | `−0,022 ± 0,029 mag` | diferença média de módulos HST/JWST; já entra no H0DN | **Não** |
| Riess 2025, NGC3447A | `0,002 ± 0,028 mag` | diferença interna entre dois campos JWST | **Não** |
| Sharon et al. 2024 | `γ = 0,013 ± 0,057 mag` | viés de blending por razões de amplitudes | **Não** |

Nenhuma fonte é escolhida ou rejeitada por seu centro, significância ou efeito esperado em D. Uma futura admissão exige produto de covariância cruzada, prova de identidade e pré-registro; até lá, `σ_b` permanece parâmetro de desenho, não prior externo identificado.

## 7. Flags

```json
{
  "observed_vector_read": false,
  "observed_support_tests": 0,
  "literature_values_used_as_priors": 0,
  "D_or_power_computed": false,
  "estimator_evaluate_called": false,
  "solver_on_observed_called": false,
  "new_seed_or_monte_carlo": false,
  "freeze_R2_or_v410_modified": false
}
```
