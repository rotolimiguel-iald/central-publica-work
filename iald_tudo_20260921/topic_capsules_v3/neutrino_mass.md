### neutrino_mass

Fonte: `resultado_publicado_integral`, `/core/neutrino_mass`. [DERIVED — proposta semântica não integrada, NÃO APROVADA.] Estatutos/resultados são reportados na fonte, não reexecutados aqui; OPEN histórico não apaga construção posterior de outro tipo.

**rule**

Regra congelada V1: `m_nu=beta*sin(45deg)*1eV`, `beta=alpha*sqrt(e)`; identifica m_2 com ordenamento normal, m_1≈0; massa absoluta só coincide com `sqrt(Dm²_21)` nesse limite. 1 eV é escala DECLARADA fixa, não ajustada; sin45 é POSTULATE (ordem 20/08/2026), não derivação. A forma sem sin45 (~12.03 meV) coexiste na origem. PDG 2023: `Dm²_21=(7.53±0.18)e-5 eV²`. POWERED iff erro relativo<0.03; FALSIFIED iff |desvio|>5sigma. Vereditos permitidos: NOT_FALSIFIED_POWERED/UNDERPOWERED, INCONCLUSIVE, FALSIFIED; CONFIRMED proibido. Resultado antigo reportado powered, desvio 1.6404744598524612sigma; números exatos no painel.

**history**

Errata de custódia: fórmula/número em 22/01/2026, git público 17/02; módulo v141 em 25/07. Alegação de prioridade pelo Zenodo 17526619/2025 foi retirada: depósito não contém fórmula/número/derivação; traz outra lei `m_nu(Dt)=m0+a log(Dt/tau0)` com dois parâmetros. Sem anterioridade ao splitting PDG. Postdição não ajustada, não previsão ex ante: dado já citado na frase original; escala 1.0200 eV que zeraria tensão foi RECUSADA. Refinamento pós-JUNO ex ante desfavorável: tensão 1.64→2.21→2.95sigma, projeção 7.83sigma contra limiar 5. V1 não muda frozen/hash; teste vivo é `neutrino_m2`/NEUTRINO_M2_V2. Soma absoluta prospectiva NEUTRINO_SUM_V1/v147 armada, não medida nesse registro; cosmologia futura não é dado atual aqui. Não move gate.

**Dados e controles reportados** — números/flags copiados da fonte, não parâmetros novos. Chaves e posições de listas seguem a fonte; null no painel indica texto descrito acima, não dado ausente.

```json
{"m_nu_meV":8.507414099900329,"m_nu_kg":1.516584316741259e-38,"sqrt_dm2_21_meV":8.677557259966655,"sqrt_dm2_21_err_meV":0.10371582382430264,"deviation_meV":0.1701431600663259,"deviation_pct":1.9607264460387983,"deviation_sigma":1.6404744598524612,"powered":true,"does_not_gate_core":true}
```

Veredito literal reportado: `TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED`. Detalhes e custódia: fonte-base acima + chave original; recuperação operacional não validada.
