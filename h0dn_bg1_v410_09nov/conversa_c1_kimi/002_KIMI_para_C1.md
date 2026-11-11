# 002 — Kimi → gerência c1 (10/11/2026) — Resposta aos cinco complementos da 03-A

**Escopo:** resposta item por item, `[DECLARADO pelo Kimi]`. Nenhum D novo, semente, Monte Carlo, vetor observado, suporte observado ou alteração de `FREEZE_R2`/v410. A v410 segue sem o teste.

## 2.1 — Três saídas e o significado de S2–S5 — **ACORDO COM CLÁUSULAS**

Aceito (α) `CERTIFICÁVEL POR COTA`, (β) `VALE FECHAR` e (γ) `FALTA INFORMAÇÃO`, desde que (α) exija poder conservador sob a regra conjunta, não apenas D acima do portão.

- **S2/CAP13:** `13D−C13 ⪰ 0` é cota superior demonstrável **somente dentro do bloco 13**, com as mesmas marginais, unidades e estimando. Não domina a matriz completa sem controlar os blocos cruzados 13–42, 13–HF e 13–host; para contraste geral é preciso provar Loewner na matriz inteira ou a condição de Schur correspondente. Sem isso, S2 é apenas robustez.
- **S3/PV integral:** ser pública, integral e PSD prova positividade, não dominação sobre `C_true`. Só vira cota superior se houver decomposição que demonstre `C_plus−C_true ⪰ 0`, inclusive suporte, pesos não negativos e residual. Antes disso, S3 é adversarial.
- **S4/elipsoide:** se a classe física estiver contida no elipsoide PSD, `min D` é **piso de D** para essa classe, embora possa ser frouxo. Para virar piso de poder, ainda é preciso demonstrar controle do tamanho e monotonicidade da regra conjunta. Não é cota superior de variância.
- **S5:** herda certificado apenas no domínio comum em que todas as hipóteses anteriores valem simultaneamente. Se essa prova existir, aceito a leitura assimétrica: `S5 ≥ limiar → (α)`; `S5 < limiar → não decide`. Sem ela, S5 é somente estresse e não decide.

Assim, (β) significa pedir produtos na ordem do orçamento; (γ) significa mostrar que informação eleva D, nunca abandonar apenas porque um envelope adversário ficou abaixo do limiar.

## 2.2 — Modelo de referência — **ACORDO**

(i) `free_cepheid_host_differential_bias` é **robustez nossa**, acrescentada por `cCep` sem prior, não o modelo principal publicado pelo H0DN. O principal da fonte é o baseline público, com seus parâmetros e covariância; o plano nosso separa explicitamente os dois modelos. [analysis_plan](kimi-cite://text?path=C%3A%2FIALD%2FCentral%20de%20Patentes%2Fwork%2Fastra_bell_fock_tt_05nov%2Fh0dn_bg1_06nov%2Fanalysis_plan.json&text=Second%20model%20appends%20cCep%20with%20no%20prior. "citation")

(ii) Aceito os dois lado a lado. O operador pode escolher o primário depois de ler a partitura condicional, mas **antes de qualquer rota observada**, por fundamento físico e não por “qual dá mais D”; o outro permanece robustez declarada. S0 e S1 podem subir ou descer relativamente à âncora: A1 preserva informação, mas `EXTRA13_OUT`, a substituição G42 e a reponderação mudam o desenho, e isso deve ser medido, não presumido.

## 2.3 — Família contínua entre os modelos — **ACORDO COM CONTRAPROPOSTA**

Proponho `C(σ_b)=C0+σ_b² cCep cCepᵀ`, recomputando pesos, variâncias e D para cada `σ_b`, em S0 e S1. `σ_b=0` deve reproduzir o publicado; `σ_b→∞` deve reproduzir o modelo livre no limite bem definido. Os dois endpoints são testes obrigatórios: se falharem, a família para.

Para D=5,842, 6,282 e 6,645, resolve-se `σ_b` analítica/numericamente; se o alvo estiver fora do intervalo da família, registrar `NOT_REACHABLE_WITHIN_FAMILY`, sem inventar raiz. Nenhum prior será escolhido pelo resultado.

Candidatas apenas documentais, **não priors independentes prontos**:

- Riess et al. 2023: JWST−HST `0,00±0,03` em N4258 e `0,02±0,03` em N5584, interceptos P–L Wesenheit; não são offsets instrumentais nem restrições independentes da rede, que compartilha dados/âncora. [Riess 2023](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fabs%2F2307.15806 "citation")
- Riess et al. 2024a: `Δμ=−0,011±0,032` em cinco hospedeiras; mede diferença de módulos P–L, não diretamente `cCep`, e compartilha dados HST/H0DN. [Riess 2024a](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2401.04773 "citation")
- Riess et al. 2025: `−0,022±0,029` em 19 hospedeiras, já insumo H0DN; NGC3447A `0,002±0,028` é interno JWST, independente da âncora, mas não mede HST×JWST nem automaticamente `cCep`. [Riess 2025](kimi-cite://web?url=https%3A%2F%2Fiopscience.iop.org%2Farticle%2F10.3847%2F2041-8213%2Fae0ad6 "citation")
- Sharon et al.: `γ=0,013±0,057`, viés de blending por amplitudes, estimando diferente e sem independência demonstrada da rede. [Sharon](kimi-cite://web?url=https%3A%2F%2Farxiv.org%2Fhtml%2F2305.14435v3 "citation")

Antes de qualquer prior, exigir identidade formal do estimando com `cCep`, independência estatística e covariância cruzada com H0DN. Até lá, esses números ficam `[KNOWN]` documental, não restrição independente admitida.

## 2.4 — Parede da montagem — **ACORDO COM REFORÇO**

`y=Aθ` deve fechar as 72 identidades por construção, mas sozinho é quase tautológico: prova a álgebra da transformação, não a montagem das células brutas. Acrescento **fixtures sintéticos de tabela**, com valores fictícios e offsets MAS conhecidos, processados pela rotina inteira; só assim testamos também o mapa fonte→equação→centros.

Aceito o protocolo futuro, escrito agora e não executado: uma única conferência por variante admitida, tolerância pré-fixada pela precisão da fonte, resultado binário, sem projeção, sem nova tentativa após falha e com a rota contada. O operador autoriza quando chegar a hora; falha implica `ASSEMBLY_CONSTRAINT_VIOLATION`, não reparo.

## 2.5 — Cota superior pode contar como “fechada”? — **CONTRAPROPOSTA DE ESTATUTO**

Pode contar como **`CLOSED_CONSERVATIVE_ENCLOSURE`**, nunca como `PHYSICAL_COVARIANCE_IDENTIFIED`. Para admiti-la num `FREEZE_R3`, exijo:

1. `C_plus−C_true ⪰ 0` demonstrado na **matriz completa**, inclusive cruzamentos e todas as alternativas cobertas;
2. mesma parametrização, estimando, linhas e mapa de suporte; nenhum jitter usado para esconder violação de montagem;
3. pesos, contraste, hipóteses, limiar, seleção e regra de parada congelados antes da amostra confirmatória;
4. prova de controle uniforme do tamanho sob o nulo e da cobertura de compatibilidade TGL sob a alternativa;
5. prova de piso de poder para a **regra conjunta**, com monotonicidade demonstrada ou ínfimo explícito sobre toda `0 ⪯ C_true ⪯ C_plus`;
6. para S4, contenção da classe física no elipsoide e cálculo do ínfimo global, não de um ponto adversarial;
7. fonte e construção da cota independentes do resultado, nenhuma escolha após olhar D ou dados;
8. revisão independente e qualquer alteração posterior tratada como nova versão exploratória.

Se qualquer componente ficar sem prova, o estado permanece `ENCLOSURE_OPEN`. Mesmo com todos os pontos, a abertura continua dependendo do operador, do portão de poder e da revisão da gerência.

**Conclusão:** estou de acordo com a 03-B se incorporar estas cláusulas. Nada foi executado nesta resposta.
