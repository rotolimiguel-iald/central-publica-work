# Adendo — proposta do operador de significância conjunta multissonda

13/09/2026. [INPUT] O operador propõe que a composição preditiva de Planck, BAO/RSD, shear, supernovas, neutrinos, ecos e ondas gravitacionais possa produzir mais de 5σ para β_TGL fixo. [DERIVED] A estratégia é estatisticamente possível em princípio. O conjunto examinado ainda não contém uma significância global validada dessa composição. Ela não deve ser substituída por soma de sigmas, de vereditos ou de contagens Lean.

Este adendo complementa o handoff de incorporação. Não muda o kernel, não inicia MCMC, não declara novo rito pré-registrado e não acrescenta condição ao gate principal.

## 1. Pontuações que existem, com o significado correto

Valores extraídos do JSON final da rodada, com fonte/hash no `EVIDENCIA_MULTISSONDA.json`. “Z observado” abaixo significa o diagnóstico numérico emitido por cada pipeline, sem promover os pipelines recusados a significância global válida.

| Análise | Z observado contra ausência do efeito | Separação/poder esperado informado | Resultado |
|---|---:|---:|---|
| GW angular, nulos com mesmo espectro | +0,801 | não é teste identificável de β | WITHIN; ruído explica a métrica |
| Eco acoplado MAY | −2,041 | 2,534σ | INCONCLUSIVE_SYSTEMATICS |
| Eco acoplado KMS | +1,144 | 2,994σ | INCONCLUSIVE_SYSTEMATICS |
| Eco ancorado V2 MAY | +2,052 | 3,211σ | INCONCLUSIVE_SYSTEMATICS |
| Eco ancorado V2 KMS | +0,219 | 4,396σ | INCONCLUSIVE_SYSTEMATICS |
| Eco PE V2 MAY | −0,312 | 1,167σ | INCONCLUSIVE_SYSTEMATICS |
| Eco PE V2 KMS | +1,211 | 1,112σ | INCONCLUSIVE_SYSTEMATICS |
| Ringdown dephasing V2 | +1,622 vs RG, em direção oposta ao ramo B | 0,178σ | INCONCLUSIVE_SYSTEMATICS |

O “4,4σ” do eco ancorado KMS é sensibilidade estimada a um sinal injetado, **não detecção de 4,4σ**: o Z observado é 0,219. O 4,81 desse mesmo ensaio é afastamento em relação a a=1, não evidência a favor do eco; os controles de sistemática também o recusam. No ringdown, δτ_B é negativo e o valor observado positivo.

MAY e KMS são alternativas de atraso sobre parte dos mesmos eventos. V1/V2 e diferentes templates são revisões/controles sobre dados reaproveitados. Ringdown e eco do mesmo evento compartilham strain e parâmetros. O antigo eco de maio −2,369σ permanece registro histórico com outra normalização; não é réplica adicional. O antigo “100σ” e H2=α² foram retirados como artefatos do próprio estimador/gerador.

**Resultado conjunto atual: não determinado.** Ausência de likelihood conjunta, covariâncias e calibração de nulos nesta entrega não equivale a Z=0. Não é correto escolher um número entre 1, 2, 3, 4 ou 5 a partir dessa tabela.

## 2. O que corrigir na proposta enviada

1. **β fixo e β livre são análises diferentes.** Primária: β=α√e fixo e apenas parâmetros cosmológicos/experimentais apropriados ajustáveis. Diagnóstico separado: liberar β, examinar seu intervalo e compatibilidade com o valor previsto. Não escrever simultaneamente “sem ajuste de β” e “prior uniforme β∈[0,0,03]”. A fronteira β=0 desse prior exige cuidado na calibração de um teste de descoberta; uma região de credibilidade que não contém zero não equivale automaticamente a p global de 5σ.
2. **Percentual:** 0,002/β = 16,6233%, não 1,7%. Uma incerteza de 1,7% seria cerca de 0,000204532. Em aproximação gaussiana, se o centro medido fosse β, σβ=0,002 daria β/σβ≈6,016; a meta nominal de mediana 5σ é σβ≤β/5≈0,00240626. Isso pressupõe parâmetro identificável, modelo válido e ausência de viés.
3. **χ²/dof não tem unidade “sigma”.** Calcular a distribuição da estatística com os graus de liberdade efetivos ou por calibração. Uma tensão H₀ entre dois métodos não é uma detecção TGL: o modelo precisa melhorar a descrição conjunta sem deteriorar as demais observações.
4. **Δχ²>25 não basta em qualquer comparação.** Definir o sinal da diferença. Para duas teorias fixas perfiladas em parâmetros compartilhados, calibrar a razão de verossimilhanças sob H₀; não presumir um novo parâmetro regular com Wilks. A regra Z≈√q vale apenas sob suas hipóteses. Uma análise Bayesiana pode reportar evidência/Bayes factor, mas não deve chamá-los de sigma sem uma calibração estatística declarada. Fontes metodológicas: [Cowan et al.](https://arxiv.org/abs/1007.1727) e [PDG, Statistics](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-statistics.pdf).
5. **Fixar β não fixa funções μ(a,k), Σ(a,k), escalas e transferência.** Usar as funções que a TGL efetivamente prevê e que o código já implementa; inventariar seus fornecedores antes de qualquer implementação. Se μ e Σ forem livres, o resultado testa uma família fenomenológica de gravidade modificada, não demonstra o valor fixo de β. Igualmente, a fórmula de m_psion deve ter seu regime e a implementação que altera observáveis; KATRIN mede massa efetiva de decaimento β, cosmologia restringe soma de massas, e oscilação mede diferenças quadráticas. Esses objetos não se substituem sem as relações de mistura/ordenamento.
6. **As likelihoods não são independentes por terem nomes de experimentos diferentes.** Conferir regiões sobrepostas, catálogos reutilizados, calibrações comuns e covariâncias. Não duplicar DESI DR1 dentro de uma liberação posterior, BOSS/eBOSS onde o conjunto combinado já os inclui, ou calibração SH0ES compartilhada com supernovas. Usar uma análise conjunta de shear/clustering já validada quando disponível. Exemplo primário de tratamento de covariâncias e parâmetros compartilhados: [DES Y3, artigos da colaboração](https://www.darkenergysurvey.org/des-year-3-cosmology-results-papers/).
7. **Separar dados medidos e previsão de instrumento.** Forecast Euclid/Rubin/LSST não é mais uma likelihood observada. Conferir produto/liberação real e escopo antes de inseri-lo. CMB-S4 não deve figurar como observação atual nem data futura garantida: o projeto informa encerramento ordenado após a retirada do apoio DOE/NSF em julho de 2025. Fonte: [comunicado oficial CMB-S4](https://cmb-s4.org/).
8. **“Máximo atual 3–4σ” e “5σ exige próxima geração” não foram calculados para este modelo nesta entrega.** Não transportar como limite demonstrado. O ganho real exige projeção de poder com o mapa TGL→observáveis e as covariâncias. Complementaridade pode melhorar a identificação, mas não garante ganho se a direção TGL estiver degenerada ou se as sondas discordarem dela.

## 3. Protocolo corrigido, reutilizando o acervo

**Etapa A — recuperar o que já existe.** Ler `core.d1_camb_result_v2`, os ritos vivos de neutrino, vazios e dephasing, o relatório do Nível 2 e seus fornecedores. Mapear cada previsão a um observável e à implementação física que a produz. Uma equação ou um nome igual não substitui o cálculo de transferência. Separar resultados desenvolvidos com os dados em questão de testes ainda não examinados.

**Etapa B — definir um único modelo primário.** H₀=ΛCDM/RG convencional; H₁=TGL no ramo e domínio explicitados, β fixo por α√e. Compartilhar os mesmos parâmetros cosmológicos e de perturbação apropriados e usar as mesmas informações auxiliares. Evitar superparametrizar Ω_m, H₀, A_s/σ₈ e somas de massas como se fossem todos independentes em qualquer parametrização. Relacionar as amplitudes de eco/dephasing somente onde essa relação é fisicamente prevista; β comum não fornece sozinho atraso nem τ★.

**Etapa C — compor dados, não vereditos.** Construir a likelihood conjunta, com covariância cruzada e parâmetros comuns. Se a independência condicional for demonstrada, fatorar por blocos; caso contrário, usar o bloco conjunto ou um subconjunto sem duplicação. Para ecos e ringdown no mesmo strain, ajustar o sinal completo conjuntamente ou calibrar a distribuição conjunta das estatísticas em simulações correspondentes.

**Etapa D — medir a comparação.** Usar T = 2[ln L₁,max − ln L₀,max], com direção positiva favorecendo H₁, e calibrar P₀(T≥T_obs) sob o nulo completo. Fixar escolhas, ramos e estatística primária antes da amostra de teste. Reportar também a qualidade absoluta do ajuste e resíduos por sonda. MCMC marginaliza/incorpora incertezas; por si só não cria uma distribuição nula ou uma significância de descoberta. Se optar por evidência Bayesiana, declarar priors e sensibilidade da evidência a eles separadamente.

**Etapa E — diagnosticar robustez.** Uma análise com β livre é um diagnóstico secundário útil: se ele preferir valor diferente, não empurrar o posterior para o valor desejado por um prior estreito. Fazer remoção de uma sonda por vez, revisões de calibração e réplica de implementação. Pré-especificar como tratar inconsistência e alternativas concorrentes, sem selecionar apenas os canais favoráveis.

**Etapa F — previsão de poder e novos dados.** Antes de declarar capacidade de 5σ, injetar tanto H₀ quanto H₁ no desenho real e medir sensibilidade e viés. Dados já abertos podem fundamentar metodologia exploratória; a confirmação preditiva subsequente pede amostra reservada/independente.

## 4. Por que o multimodal pode ultrapassar 5σ sem truque

Exemplo apenas didático, sem dados TGL: três estatísticas normais com média nula e variância um sob H₀, independentes e com direção/ponderação definidas de antemão. Se cada uma observar Z_i=3, o Stouffer de pesos iguais é (3+3+3)/√3=5,196. Se a correlação entre cada par for ρ=0,5, a mesma soma padronizada vale 9/√6=3,674. Nenhum desses números descreve a nossa plataforma.

De modo geral, para esses Z_i com matriz de correlação R e pesos fixos w, Z_comb = (wᵀZ)/√(wᵀRw). A regra só se aplica quando os Z_i e sua distribuição conjunta estão justificados para a mesma hipótese/direção; ela não permite misturar poder esperado, tensão contra a previsão, teste de ruído e Bayes factor. A likelihood física conjunta é preferível aos resumos quando os parâmetros são compartilhados.

## 5. O resultado desfavorável que deve permanecer visível

O procedimento D1 CAMB V2 existente registra χ²_LCDM≈37,399 e χ²_TGL≈47,098; portanto, nessa aproximação, T≈−9,70, favorecendo ΛCDM. O posterior livre ali prefere β negativo. Isso não é a combinação completa proposta nem uma refutação global automática da TGL; é evidência local adversa que a combinação deve carregar com o sinal correto. Somá-la como “3,86σ a favor” inverteria o resultado.

**Decisão deste adendo:** a proposta multissonda é apropriada como próximo desenho empírico, corrigida como acima. Não há evidência calculada nesta sessão de que o Z conjunto já seja maior que 5. Os resultados experimentais não bloqueiam a incorporação da cadeia formal verificada e não devem ser promovidos pelo estado do gate.
