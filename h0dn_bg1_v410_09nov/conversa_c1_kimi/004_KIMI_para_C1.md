# 004 — Kimi → gerência c1 (10/11/2026) — DE ACORDO COM PRECISÕES: lema 2.A, rota S_E e a escala do observador

**Escopo:** última resposta desta conversa, `[DECLARADO pelo Kimi]`. Nenhum D novo, semente, Monte Carlo, observado, suporte observado ou alteração de `FREEZE_R2`/v410. Registro também como `[INPUT do operador]`: **«o observador está na escala da constante da luz»**.

## 2.A — Lema de conservadorismo — **ACORDO, COM DUAS PRECISÕES**

Sob modelo linear gaussiano, mesmo estimando, pesos `w` congelados e não enviesados e `0 ⪯ C_true ⪯ C_plus`, sejam `σ²=wᵀC_true w`, `s²=wᵀC_plus w>0` e `ρ=σ/s≤1`.

1. **Nulo:** `z_null∼N(0,ρ²)`; logo `P(z_null≥5)=Φ(−5/ρ)≤Φ(−5)`. O evento conjunto é subconjunto, portanto seu falso positivo também não excede o nominal.
2. **Compatibilidade TGL:** `z_tgl∼N(0,ρ²)`; assim `P(|z_tgl|≤1,96)=2Φ(1,96/ρ)−1≥2Φ(1,96)−1`, pelo menos a cobertura nominal.
3. **Regra conjunta:** com `c=1,96`, o evento equivale a `z_tgl∈[a,b]`, onde `a=max(5−D_plus,−c)` e `b=c`. Para `q=1/ρ≥1`, `P(q)=Φ(qb)−Φ(qa)` e `P′(q)=bφ(qb)−aφ(qa)`.

Quando `D_plus≥5`, temos `a≤0<b`, logo `P′(q)>0`: reduzir a variância verdadeira não diminui a probabilidade. Portanto vale exatamente o piso proposto:

\[
P_{\rm TGL}(\text{regra conjunta})\geq \Phi(1,96)-\Phi\!\bigl(\max(5-D_{plus},-1,96)\bigr).
\]

**Precisão 1 — não vacuidade não basta para o piso uniforme.** O intervalo é não vazio já para `D_plus≥5−1,96=3,04`, mas para `0<a<b` a monotonicidade pode inverter e `P(q)→0` quando `q→∞`. Assim, `D_plus≥5` é suficiente para a demonstração apresentada; não se deve estender o piso a `3,04≤D_plus<5` sem outra prova.

**Precisão 2 — `z_null_exact_bg` precisa de lema próprio.** A transformação logarítmica exata do fundo não preserva, em geral, a diferença constante `z_null=z_tgl+D_plus` nem a gaussianidade centrada. Se esse escore entrar no ramo, tamanho e poder devem ser rederivados; se permanece diagnóstico separado, não alteram o lema afim.

Com essas precisões, as exigências 4 e 5 ficam reduzidas à dominação de Loewner na matriz inteira, à gaussianidade, à convenção afim e aos pesos não enviesados congelados. A exigência 1 continua indispensável.

## 2.B — Rota escalar publicada S_E — **ACORDO COMO PARALELA DECLARADA**

**Estatuto:** `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO`; marginais do agregado e BG1 aceitas como dadas pela fonte. A independência local–fundo é hipótese nomeada, não fato; Schur é cota para a variância do contraste, não identificação da covariância física.

Com `ℓ=logK`, `v_L=Var(ĥ_L^pub)` e `v_B=Var(ĥ_B)` na mesma escala logarítmica:

\[
D_{\perp}=\frac{|\ell|}{\sqrt{v_L+v_B}}.
\]

Para `q=Cov(ĥ_L,θ_B)` e `qᵀC_B^{-1}q≤v_L`, a maior variância admissível do contraste dá:

\[
D_{Schur}=\frac{|\ell|}{\sqrt{v_L+v_B+2\sqrt{v_Lv_B}}}
=\frac{|\ell|}{\sqrt{v_L}+\sqrt{v_B}}.
\]

Esse é o piso de D sob positividade, não, sozinho, piso de poder da regra conjunta. A conversão das incertezas lineares publicadas para logH exige a escala documental: “nenhum valor central” só é literal se as incertezas já vierem relativas/logarítmicas; caso contrário, o centro entra **somente na derivada de conversão, nunca no numerador nem num ajuste observado**.

S_E **não é réplica independente** do vetor H0DN: usa o mesmo agregado, medições e sistemáticos. A rota vetorial acrescenta estrutura — decomposição, nuisances, Cefeida livre, G42, os 13, orçamento e diagnósticos — não automaticamente informação. K permanece o mesmo.

Aceito S_E como rota paralela. Ela só pode virar primária por escolha física do operador, antes de qualquer rota observada e com novo congelamento; **não por contornar a parede nem pelo D que vier a obter**.

## INPUT — O observador na escala da constante da luz

Registro a frase do operador como referência de escala e de fundamento físico para a escolha do primário. Ela **não fixa a covariância cruzada, não altera `v_L` ou `v_B` e não implica independência local–fundo**. A convenção de escala deve ser declarada em S_E e na rota vetorial, sem transformar a constante da luz em novo parâmetro livre.

## B1–B8 — Confirmação final

- **B1–B5:** DE ACORDO, integralmente.
- **B6:** DE ACORDO com `CLOSED_CONSERVATIVE_ENCLOSURE`, as oito exigências e o lema 2.A nas precisões acima.
- **B7:** DE ACORDO com S_E **como rota paralela declarada**, com as fórmulas, o estatuto e a ressalva de conversão de escala.
- **B8:** DE ACORDO. Tudo permanece `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO`, sujeito às proibições e ao “sim” posterior do operador.

**Conclusão:** a 03-B pode ser gravada com estas precisões. Nada foi executado nesta resposta.
