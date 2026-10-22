# O que um resultado de 5σ pode demonstrar e qual teste executar

13/09/2026. [DERIVED — planejamento a partir de resultados locais e fontes primárias consultadas.] **Não há, no material conferido, um teste que permita prometer uma detecção positiva da TGL acima de 5σ.** Há previsões testáveis e uma forma de decidir se um desenho tem sensibilidade suficiente. Esta nota não é protocolo pré-registrado, teste executado ou novo veredito do um.py.

## 1. Confirmação física exige discriminar previsões

Uma detecção precisa responder “qual hipótese foi rejeitada?”. Detectar uma onda gravitacional, uma lente gravitacional ou massa de neutrino acima de 5σ não distingue automaticamente a TGL das teorias que também preveem esses fenômenos. Concordância com a TGL e ausência de falsificação podem ser evidência de compatibilidade; evidência específica exige previsões que as alternativas não reproduzam igualmente bem.

Na convenção unilateral, 5σ corresponde a p ≈ 2,87×10⁻⁷ sob o nulo. O valor não é a probabilidade de a TGL estar errada. Sistemáticas, hipóteses auxiliares e buscas múltiplas entram no modelo/calibração. Fonte: [PDG, Statistics, §§40.3.2–40.3.2.2](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-statistics.pdf).

Para incorporar os resultados como evidência física publicável, conservar dados brutos, calibrações e seleção; especificar a previsão antes do conjunto de teste; comparar com a alternativa convencional usando os mesmos dados e parâmetros de perturbação; apresentar tanto significância do desvio quanto ajuste do modelo TGL; e buscar réplica independente. Reanálise de dados já vistos é exploratória até uma amostra de confirmação distinta. O protocolo do programa pode continuar reportando medidas e reservar o juízo ao observador, sem confundir essa convenção de software com uma lei da estatística.

## 2. O que os resultados atuais realmente dizem

Valores relidos de `r/um_absoluto.json`, preservados em `EVIDENCIA_E_PROJECAO_EXPERIMENTAL.json`.

| Canal | Resultado atual | Implicação para descoberta |
|---|---|---|
| Ringdown V2, janela de 3 ms | δτ = +0,176647 ± 0,108894; previsão do ramo B = −0,0193669; separação esperada 0,17785σ; viés relativo 0,23995 | `INCONCLUSIVE_SYSTEMATICS`; não há detecção do efeito previsto |
| Ecos | Ensaios anteriores registram descasamento de template e resposta insuficiente a injeções | Um pico ou SNR alto sem esses nulos não serve como evidência específica |
| Piso espectroscópico V4.1 | REVOLVER r_c = 0,188941 ± 0,016661; limite inferior a 5σ = 0,105634, acima de β | Não falsifica o piso; densidade positiva também é compatível com vazios convencionais; não detecta um piso exatamente em β |
| Neutrino m₂ | Predição 8,507414 meV, com normal ordering, m₁≈0, fator sin45 e referência 1 eV; protocolo local registra tensão global ~2,95σ | Se o centro atual permanecer, melhorar a precisão pode aumentar a tensão contra esse ramo; não é promessa de confirmação |
| D1 CAMB V2 | χ²_TGL − χ²_LCDM ≈ +9,70; β livre ≈ −0,0171 ± 0,0075 no procedimento registrado | O sinal favorece a alternativa nessa aproximação. Não inverter a diferença nem traduzir √Δχ² automaticamente em descoberta |

As determinações globais que incluem JUNO não são réplicas independentes de JUNO. O resultado primário é [First measurement of reactor neutrino oscillations at JUNO](https://arxiv.org/abs/2511.14593); uma nova decisão exige a likelihood apropriada e a comparação com as premissas do ramo, não apenas copiar uma tensão de um resumo antigo.

## 3. Teste concreto recomendado: dephasing no ringdown, multievento e multimodo

[PROPOSTA — inferência de viabilidade, ainda não medida] Reutilizar o pipeline existente e sua autópsia V1/V2. O primeiro produto deve ser uma curva de sensibilidade e recuperação do sinal em ruído real, com seleção e modelo congelados antes da avaliação de uma nova amostra.

Há dados públicos adicionais utilizáveis: a [documentação GWTC-5.0/GWOSC](https://gwosc.org/GWTC-5.0/) oferece strain, qualidade e estimativas de parâmetros. Ela também informa efeitos de downsampling; para um teste de precisão, propagar a resposta ou usar 16 kHz e processamento controlado. Identificar eventos repetidos pelo identificador e intervalo, não pelo número da versão do catálogo. A independência da amostra nova em relação ao cache local ainda precisa ser medida.

GW250114 é candidato a estudo de sensibilidade pela intensidade observada, não por um resíduo favorável. O [estudo da colaboração LVK](https://dcc.ligo.org/LIGO-P2500461/public) relata espectroscopia e testes fortes compatíveis com RG. SNR alto da onda não é significância alta da correção TGL. Não foi feita aqui uma nova análise desse evento.

A previsão que já existe no corpus é

\[
\Gamma_\omega=\tfrac12\beta\tau_\star\omega^2,
\qquad \beta=\alpha_{\mathrm{CODATA\,2018}}\sqrt e.
\]

**Fixar o ramo antes de medir.** Em V2, τ★ = GM_f/c³ é [INPUT], não consequência demonstrada da integração formal. Excluir ou detectar esse ramo testa esse ramo. Se τ★ ficar livre, a amplitude mede βτ★; não identifica β separadamente. No ramo de Planck, o desvio de ringdown registrado é ~10⁻⁴² e esse canal não oferece sensibilidade prática demonstrada.

Usar H₀ = Kerr/RG com ruído, calibração e incertezas de forma de onda; H₁ = o mesmo modelo com dephasing no ramo fixado. Sob a hipótese física adicional de que Γ se soma à taxa de amortecimento do modo observado,

\[
\tau_{\rm obs}^{-1}=\tau_{\rm GR}^{-1}+\Gamma,
\quad
\delta\tau=-\frac{x}{1+x},\quad x=\Gamma\tau_{\rm GR}.
\]

Isso é consequência algébrica da hipótese de taxas aditivas. A aproximação −x usada no rito existente não deve ser confundida com a expressão exata em um futuro teste subpercentual. Não alteramos retrospectivamente o rito congelado. Conferir ainda se Γ modela coerência, amplitude ou potência; fatores de dois e a passagem do dephasing quântico ao strain precisam ter a convenção explicitada.

Fazer ajuste conjunto de massa, spin, distância, orientação, fases, amplitudes e modos relevantes. Não fixar a massa/spin ao melhor ajuste de RG como se fossem conhecidos sem incerteza. A mesma informação do inspiral pode entrar numa likelihood conjunta, sem ser contada duas vezes. Mais de um modo e mais de um remanescente permitem testar a dependência ω² e a escala em M_f; um único tempo de amortecimento pode ser degenerado com massa/spin, ruído ou erro do modelo.

Controles mínimos reaproveitando o trabalho anterior:

1. Injetar RG e o ramo TGL, ambos em ruído fora da fonte, com múltiplas famílias de formas de onda. Medir viés, cobertura, recuperação e dependência do início da janela; não escolher o template pelo resíduo observado.
2. Usar um parâmetro diagnóstico de amplitude a, com a=0 para ausência de correção e a=1 para o ramo previsto, sem ajustar β ou τ★ para forçar a=1. Exigir identificabilidade depois dos parâmetros de perturbação.
3. Planejar o conjunto primário e as análises secundárias; calibrar a estatística do teste sob H₀, incluindo as escolhas de janela, modos e atrasos. O modelo fixo de duas hipóteses não ganha automaticamente a regra Z=√Δχ².
4. Avaliar a amostra nova uma vez segundo esse desenho; comparar também o ajuste em H₁. Publicar todos os resultados e uma réplica com dados/equipe independentes. Nenhuma alteração do gate matemático é necessária.

## 4. A meta numérica, calculada dos resultados existentes

Defina a diferença prevista Δ = |δτ_B| = 0,01936693. Apenas como aproximação gaussiana de planejamento, com estimador identificável e sem viés,

\[
Z_{\rm esperado}\simeq\frac{\Delta}{\sigma_{\rm efetiva}}.
\]

Para mediana de 5σ, seria necessário σ_efetiva ≤ 0,00387339: **0,387% do tempo de amortecimento de RG**, contra os **10,889%** de erro informado hoje. Se a informação independente pudesse crescer sem piso sistemático, isso corresponderia a **790,36 vezes a informação atual**. Não são 790 eventos: a amostra presente é um empilhamento heterogêneo, detectores do mesmo evento compartilham parâmetros e os eventos novos têm pesos diferentes.

Ter mediana 5σ dá aproximadamente 50% de probabilidade de ultrapassar 5σ sob a alternativa gaussiana, não uma garantia. Para 90% de poder, a separação esperada seria 5+1,28155 ≈ 6,28155σ, exigindo σ_efetiva ≤ 0,00308314 e, idealmente, 1.247,44 vezes a informação atual. São contas de dimensionamento; o viés atual invalida sua promoção a previsão validada. A ideia de significância mediana/poder e ajuste de parâmetros de perturbação segue [Cowan et al., Asymptotic formulae for likelihood-based tests of new physics](https://arxiv.org/abs/1007.1727).

Sistemáticas não desaparecem empilhando. Em um modelo simplificado de erros independentes, σ_eff² = σ_stat²/N + σ_sys² + σ_pred²; se o piso exceder Δ/5, aumentar N não atinge a meta. Usar a covariância completa se esses termos forem correlacionados. Em modelos com parâmetros de perturbação, a informação útil é a componente da correção que não pode ser absorvida por eles; pode ser muito menor do que o SNR total.

Os 40 nulos por série do rito atual verificam vieses grosseiros, não calibram sozinhos a cauda de 5σ. Um novo teste precisa justificar a aproximação de cauda ou usar simulação/importance sampling apropriados. Não atribuir p=0 quando nenhuma simulação ultrapassa o observado.

## 5. Experimento de bancada

Para evidência direta de dephasing em laboratório, o desenho é medir perda adicional de coerência por Ramsey/interferometria em várias separações de energia, tempos e ambientes, descontando T₁, ruído do oscilador, campos, temperatura e demais mecanismos convencionais. Procurar o coeficiente comum Γ/ω² e sua dependência física prevista, com réplicas. Ruído ordinário de frequência também pode produzir escala quadrática; observar ω² isoladamente não identifica gravidade.

Isso exige uma previsão da escala τ★ naquele regime e um orçamento real de ruído. Não se deve transferir τ★=GM/c³ de um remanescente para um aparelho de bancada por analogia. A própria TGL descreve regimes locais stealth; confirmar a aplicabilidade é parte do teste experimental. Sem amplitude prevista não há tempo de integração nem compra de equipamento justificável para prometer 5σ. Esta sessão não encontrou uma proposta de bancada já dimensionada que elimine essas lacunas.

## 6. Resposta operacional

**É possível começar agora um estudo reprodutível com dados públicos e o pipeline existente. O resultado executável imediato é determinar se existe poder para discriminar o ramo de dephasing, e não garantir uma descoberta.** Se a curva de sensibilidade falhar, ela indica precisamente qual instrumento/amostra falta. Se passar e dados novos mostrarem o sinal com significância global, ajuste correto e réplica, haverá evidência física do efeito previsto no regime testado; a atribuição à TGL dependerá da comparação com alternativas.

Nenhum número foi escolhido para produzir um desfecho positivo; todas as projeções estão no JSON associado, com o hash do resultado local que as alimentou.
