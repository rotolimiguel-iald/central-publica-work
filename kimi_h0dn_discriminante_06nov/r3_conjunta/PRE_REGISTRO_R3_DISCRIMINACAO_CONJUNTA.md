# PRÉ-REGISTRO CANDIDATO R3 — DISCRIMINAÇÃO CONJUNTA H0DN × BG1

**Data:** 06/11/2026  
**Estado:** `CANDIDATE_BLOCKED_NOT_FROZEN`  
**Autor:** Kimi, em nome próprio, por ordem do operador  
**Plano machine-readable:** `analysis_plan_r3.json`  
**Regra de abertura:** **PROIBIDA até que todos os gates G1–G9 estejam cumpridos e revistos independentemente.** G10 é obrigatório antes de qualquer alegação além de uma única determinação.

> Este documento prepara um futuro teste confirmatório. Não congela a covariância física, não autoriza abrir dados observados, não altera R2, não constitui veredito de natureza e não move o gate.

## 1. Pergunta científica

Na rede H0DN × BG1, com a lei TGL \(K\) já congelada, a razão local/fundo de Hubble permite:

1. rejeitar o nulo de diferença logarítmica zero a **5σ unilateral**;
2. permanecer simultaneamente **compatível com a previsão TGL a 95% bilateral**?

A pergunta não é apenas quantas vezes um simulado cruza 5σ. O evento confirmatório exige as duas condições no mesmo resultado observado.

## 2. Modelos e proibição de seleção

### Primário confirmatório

`free_cepheid_host_differential_bias`.

Esse modelo perfila todos os parâmetros originais e acrescenta o termo diferencial Cepheid livre. Ele foi escolhido como primário para não substituir a incerteza física pelo modelo mais otimista.

### Secundário, somente diagnóstico

`published_baseline`.

O resultado secundário não pode substituir, melhorar ou reverter o primário. Não haverá escolha do modelo mais favorável após a abertura.

## 3. Regra confirmatória

Para cada modelo \(m\), calcula-se o estimador de \(h=\log_{10}H_0\) pela geometria congelada da rede e pelo fundo BG1.

O escore nulo usa o logaritmo exato do fundo físico:

\[
Z_{0,m}^{\rm exato}
=
\frac{\hat h_m-\left[\log_{10}(H_0+\delta H_0)-\log_{10}H_0\right]}
{\sigma_{0,m}}.
\]

O escore de compatibilidade conserva o gradiente separado da previsão:

\[
Z_{{\rm TGL},m}
=
\frac{t_m-\log_{10}K-b_{K,m}}{\sigma_{{\rm TGL},m}}.
\]

A regra conjunta primária é

\[
\boxed{
Z_{0,\rm primário}^{\rm exato}\geq q_{\rm primário}
\quad\text{e}\quad
|Z_{\rm TGL,primário}|\leq1,959963984540054.
}
\]

A regra secundária tem a mesma forma, com seu próprio corte, e é somente diagnóstica.

### Corte exato

O corte \(q_m\) será recalculado depois do fechamento da covariância, resolvendo por quadratura a cauda do fundo gaussiano físico em \(H_0\), sem clipping, redraw ou ajuste:

\[
\Pr\!\left(Z_{0,m}^{\rm exato}\geq q_m\mid H_0^{\rm nulo}\right)
=\Phi(-5)=2,866515718791933\times10^{-7}.
\]

Referências apenas diagnósticas da R2, **proibidas como cortes R3 se a covariância mudar**:

- basal: \(q/\sigma_0=5,00360498452007\);
- Cepheid livre: \(q/\sigma_0=5,001955991015191\).

### Compatibilidade TGL

A janela bilateral é de 95%, com meia-largura

\[
\Phi^{-1}(0,975)=1,959963984540054.
\]

Compatibilidade isolada não é detecção. Rejeição do nulo isolada não é creditação. A falsa junção sob o nulo será estimada diretamente, embora o evento conjunto seja subconjunto do evento marginal de 5σ.

## 4. Vereditos permitidos

| Token | Condição |
|---|---|
| `DISCRIMINATED_NULL_AND_COMPATIBLE_TGL_AT_5SIGMA` | A regra primária passa, todos os gates físicos e de custódia passam e a seleção de rotas é válida. **Uma determinação apenas.** |
| `NULL_REJECTED_BUT_NOT_DISCRIMINATED` | O nulo primário é rejeitado, mas o resíduo TGL excede a janela de 95%. |
| `TGL_COMPATIBLE_NULL_NOT_REJECTED` | O resíduo é compatível, mas o nulo não é rejeitado; reportar o poder, sem detecção. |
| `NOT_DISCRIMINATED` | O nulo não é rejeitado e o resíduo TGL excede a janela. |
| `INCONCLUSIVE_SYSTEMATICS` | Um gate físico/custodial falha ou uma sensibilidade fisicamente admitida e pré-especificada reverte o veredito. |
| `EXPLORATORY_ONLY` | A seleção de rotas ou a multiplicidade entre rotas não tem controle confirmatório adequado. |

Nenhum token significa confirmação final da TGL. Uma segunda determinação autônoma continua obrigatória para creditação.

## 5. Poder necessário antes da abertura confirmatória

A abertura confirmatória exige, no modelo primário e em todos os modelos de robustez fisicamente admitidos:

\[
\boxed{
\Pr\!\left(Z_0^{\rm exato}\geq q
\ \text{e}\ |Z_{\rm TGL}|\leq1,96\mid{\rm TGL}\right)\geq0,90.
}
\]

O poder será calculado analiticamente e por Monte Carlo, com intervalo de Wilson e sem escolher a melhor realização.

### Referências atuais, não promessas

Nos escores R2, usando os cortes exatos de referência:

- basal: rejeição exata 96,585%; evento conjunto **94,110%**;
- Cepheid livre: rejeição exata 62,440%; evento conjunto **59,984%**.

Logo o modelo primário atual **não satisfaz o gate de 90%**.

Na aproximação linear de planejamento, 90% conjunto exige:

- \(D=6,439531\);
- redução de 19,2294% no desvio da rede;
- ou uma restrição Cepheid externa independente de aproximadamente 0,0142396 mag.

Esses números serão recalculados com o corte exato e a covariância final. Nenhuma restrição externa desse tipo é afirmada como já medida.

Se o poder ficar abaixo de 90%, não haverá abertura confirmatória. Uma abertura diagnóstica exigiria decisão explícita do operador e jamais poderia emitir o token de discriminação a 5σ.

## 6. Gates obrigatórios

### G1 — Operador de agregação

Recuperar e validar independentemente a aplicação das curvas às 55 equações H0DN, incluindo os 26 calibradores com múltiplas curvas, com fonte, código, hashes e fixtures numéricos.

### G2 — Identificadores

Resolver os oito IDs ausentes e validar ou rejeitar os dois aliases por fonte primária:

- ausentes: `2008fv`, `2021rhu`, `1998bu`, `1989B`, `1994D`, `ASASSN-14lp`, `2021J`, `2020nvb`;
- aliases candidatos: `2008fv_comb`, `1994DRichmond`.

Semelhança nominal não é prova de identidade.

### G3 — Decomposição física

Separar SN-only, Cepheid/host e velocidades peculiares. Demonstrar que nenhuma informação Cepheid, SN ou PV foi duplicada. `STAT+SYS` não pode ser transplantado indiscriminadamente.

### G4 — Geometria da covariância

Congelar a covariância conjunta completa e verificar:

- simetria e finitude;
- ausência de autovalores negativos substantivos;
- posto e separação espectral não ambíguos;
- desenho e coluna Cepheid no suporte;
- identidade da influência e desvios positivos;
- nenhuma diagonalização, ridge ou reparo oculto.

### G5 — Seleção de rotas

Congelar a contabilidade da seleção entre rotas e da multiplicidade, ou uma amostra/reserva confirmatória independente. O histórico de escolha de H0DN após estimativas de poder deve ser declarado; a melhor rota retrospectiva não pode ser apresentada como confirmação.

### G6 — Corte e cauda

Recalcular o corte exato e verificar a cauda marginal e a falsa junção:

- solução analítica/quadratura;
- importance sampling com erro padrão relativo \(\leq1\%\);
- zero excedências ordinárias não é prova da cauda;
- nenhum novo ajuste depois dos escores.

### G7 — Poder

Satisfazer o gate de 90% de poder conjunto no primário e nos modelos fisicamente admitidos. Se o gate não for alcançado, a abertura confirmatória permanece recusada.

### G8 — Revisão independente

Covariância, agregação, estimador, seleção de rotas, poder e guardas de recusa serão revistos por agente que não os construiu. Quem constrói não aprova sozinho.

### G9 — Custódia cega R3

Depois do fechamento da covariância:

1. congelar código, plano, fontes e thresholds por SHA-256;
2. gerar novas sementes R3 sob custódia; os escores R2 não serão reutilizados para veredito;
3. executar 100.000 injeções ordinárias por hipótese e 100.000 de importância por modelo;
4. pinar escores antes dos rótulos;
5. obter reconhecimento independente antes da abertura das classes;
6. permitir uma única abertura observada.

### G10 — Segunda determinação

Antes de qualquer alegação além de “uma determinação”, identificar e pré-registrar uma segunda rota autônoma, com sistemáticas independentes. Não somar sigmas nem tratar conjuntos sobrepostos como réplicas.

## 7. Sensibilidades pré-especificadas

Mantêm-se como coordenadas de estresse, não como priors medidos:

- viés Cepheid fixo: \(-0,05\) e \(+0,05\) mag;
- ruído adicional: 0,01, 0,03, 0,05 e 0,10 mag;
- covariâncias cruzadas físicas: estimadas ou limitadas por evidência primária antes das injeções R3.

Sinais adversariais calculados a partir dos pesos de influência são somente sensibilidade matemática. Não são medição de correlação, veto à TGL ou licença para escolher outro modelo.

Se uma sensibilidade fisicamente admitida e pré-especificada reverter o veredito, o resultado é `INCONCLUSIVE_SYSTEMATICS`.

## 8. Alterações proibidas após a abertura

Não se pode alterar:

- corte ou janela de compatibilidade;
- modelo ou rota primária;
- pesos de agregação, IDs ou aliases;
- covariância, influência ou estimador;
- prior Cepheid externo ou meta de poder;
- tratamento de perdas, exclusões ou regra de ajuste;
- seleção do melhor modelo, cenário ou sensibilidade.

Qualquer reparo será escrito ao lado, com nova versão e sem reescrever R2/R3 ou seus recibos.

## 9. Estado atual do preflight

Todos os gates G1–G9 estão `OPEN`. Portanto:

\[
\boxed{\text{OPENING\_ALLOWED\_NOW}=\mathrm{FALSE}.}
\]

Não existe `OBSERVED_RESULTS_R3.json` permitido nesta fase. O arquivo `PREFLIGHT_R3.json`, gerado pelo validador, registra a recusa e os hashes efetivos dos artefatos.

## 10. Artefatos de referência

- `analysis_plan_r3.json`: regra machine-readable;
- `avaliar_r3_escores_r2.py`: diagnóstico exato nos escores já abertos;
- `R3_DIAGNOSTICO_ESCORES_R2.json`: resultados exatos de referência;
- `validar_r3.py`: guarda de recusa e preflight;
- `PREFLIGHT_R3.json`: estado corrente dos gates;
- `FREEZE_R3_PENDING.json`: manifesto pendente, **não é freeze**;
- `../DISCRIMINANTE_CONJUNTO.json`: evento conjunto linear exploratório;
- `../MARGENS_DISCRIMINANTE_CONJUNTA.json`: margens lineares de planejamento;
- `../COVARIANCA_COMPONENTES.json` e `../covariancia_componentes.npz`: componentes públicos preparados.

## 11. Condição para passar a FREEZE

Somente quando G1–G9 tiverem evidência preenchida e revisão independente, uma nova versão poderá:

1. marcar cada gate como `CLOSED` com artefatos e hashes;
2. congelar os thresholds exatos e o estimador final;
3. gerar a custódia cega R3;
4. autorizar formalmente a única abertura observada.

Até lá, **R3 é preparação, não licença de abertura**. Nenhum resultado da natureza é afirmado e o gate permanece imóvel.
