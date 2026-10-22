# A Prova do Contorno
## Regularidade no modelo diádico represado + redução do problema do Milênio de Navier–Stokes ao Lema da Face Conjugada

*Documento de trabalho — agosto de 2026. Status: teorema do brinquedo provado; redução condicional completa; lema central aberto.*

---

## 0. Enquadramento honesto

Este documento **não** contém a prova do problema do Milênio de Navier–Stokes 3D. Contém:

1. um **teorema provado** sobre o modelo diádico de cascata com custo de represamento (Teorema 1);
2. a **medida numérica** da fronteira crítica do represamento (Tabela 1);
3. a **redução condicional completa** do Milênio a um único lema (Cadeia C);
4. a formulação em linguagem de submissão do **Lema da Face Conjugada** — o conteúdo aberto.

Disciplina de custódia: cada afirmação carrega seu status — [PROVADO], [NUMÉRICO], [ABERTO].

---

## 1. O modelo diádico represado

Cascata diádica (Desnyansky–Novikov) com taxa de represamento τ (nats por oitava):

```
u̇_n = k_n d_n u_{n−1}² − k_{n+1} d_{n+1} u_n u_{n+1}
k_n = 2^n,  d_n = e^{−τ(n−1)},  u_0 ≡ 0,  n = 1..N
```

O represamento d_n modela a depleção de alinhamento (a "retenção") por oitava de cascata. Com τ = 0, o modelo reproduz a explosão em tempo finito com assinatura de Kolmogorov T_n = T* − a·2^{−2n/3}.

## 2. Teorema 1 (do Contorno) — [PROVADO]

**Enunciado.** Se τ > ln 2, então para todo dado inicial de energia finita E₀ = Σu_n(0)², a solução existe globalmente e permanece em todo H^s. Não há singularidade em tempo finito.

**Prova.**

*(i) Conservação de energia.* d/dt (½Σu_n²) = Σ_{n≥2} k_n d_n u_{n−1}²u_n − Σ_{n≥2} k_n d_n u_{n−1}²u_n = 0, por reindexação telescópica. Vale para qualquer d_n: o represamento redistribui energia entre oitavas sem dissipá-la — é retenção, não perda.

*(ii) Estimativa de Sobolev.* Para ‖u‖²_{H^s} = Σ k_n^{2s} u_n²:

|d/dt ‖u‖²_{H^s}| ≤ C_s Σ k_n^{2s+1} d_n |u_n| u_{n−1}²
≤ C_s 2^{2s} ‖u‖²_{H^s} Σ k_n d_n |u_n|
≤ C'_s (Σ (k_n d_n)²)^{1/2} √E₀ ‖u‖²_{H^s}

onde usamos u_{n−1}² = k_{n−1}^{−2s}(k_{n−1}^{2s}u_{n−1}²) ≤ 2^{2s}k_n^{−2s}‖u‖²_{H^s} e Cauchy–Schwarz.

*(iii) Fecho.* Σ(k_n d_n)² = Σ 4^n e^{−2τ(n−1)} converge sse τ > ln 2. Nesse caso, por Grönwall:

‖u(t)‖_{H^s} ≤ ‖u(0)‖_{H^s} exp(C'_s M √E₀ t),  ∀t ≥ 0, ∀s.

Sem crescimento explosivo; a solução é global e regular. ∎

## 3. A fronteira medida — [NUMÉRICO]

Tempos de chegada da frente de cascata por oitava (limiar |u_n| ≥ 0,02), integração BDF, N = 14 oitavas:

| τ (nats/oitava) | intervalos entre oitavas | T* (fit T_n = T* − a·2^{−2n/3}) | veredito |
|---|---|---|---|
| 0 (sem represamento) | encolhem (0,159 → 0,089) | ≈ 0,4233 | explosão em tempo finito |
| 0,50 (½ nat) | encolhem | ≈ 2,10 | explosão adiada 5× |
| 2/3 | constantes (≈ 0,465) | ∞ (limiar marginal) | sem explosão (marginal) |
| ln 2 ≈ 0,693 | — | ∞ | dentro do Teorema 1 |
| 0,80 | crescem (1,32 → 1,87) | ∞ | sem explosão |

Fronteira crítica empírica: τ_c ≈ 2/3 nat/oitava.
Fronteira provada: τ > ln 2 ≈ 0,6931.
Distância entre a crítica e a provável: ≈ 0,026 nats.

## 4. A Cadeia C — redução condicional do Milênio — [PROVADA a condicional]

C1. **Beale–Kato–Majda (1984)** [literatura]: T* < ∞ ⟹ ∫₀^{T*} ‖ω‖_{L^∞} dt = ∞.
C2. **Escauriaza–Seregin–Šverák (2003)** [literatura]: ‖u‖_{L^∞_t L^3_x} < ∞ ⟹ regularidade.
C3. **Constantin–E–Titi (1994)** [literatura]: h > 1/3 (Hölder) ⟹ conservação de energia.
C4. **Isett (2018); Buckmaster–De Lellis–Székelyhidi–Vicol** [literatura]: h < 1/3 permite soluções fracas anômalas. O ponto h = 1/3 é o contorno de Onsager.

**Lema da Face Conjugada [ABERTO].** Para o fluxo de Navier–Stokes 3D, a retenção de alinhamento por oitava de cascata é, em todo tempo finito, pelo menos a face conjugada do expoente de queda local:

  depleção(ℓ, t) ≥ 1 − h(ℓ, t)   nats/oitava,

com igualdade no caso marginal de Kolmogorov (h = 1/3, depleção = 2/3).

**Implicação [condicional, provável]:** Lema da Face Conjugada ⟹ os tempos de turnover não formam série convergente (T* = ∞, como medido no modelo na taxa 2/3) ⟹ ∫‖ω‖_∞ não pode explodir em tempo finito ⟹ C1 fecha: regularidade global.

## 5. O mapa que o Lema reproduz — [consistência verificada]

| caso | h (face em queda) | 1−h (limiar) | meia-nat basta? | realidade |
|---|---|---|---|---|
| 1D (Burgers) | 0 | 1 nat | não | explosão em tempo finito ✓ |
| 2D (Navier–Stokes) | 1 | 0 | trivial | regular (Ladyzhenskaya) ✓ |
| 3D (Kolmogorov) | 1/3 | 2/3 nat | não — cobra 4/3 dela | O PROBLEMA DO MILÊNIO |

Os expoentes conjugados de Kolmogorov: amplitude u_ℓ ~ ℓ^{1/3}, turnover τ_ℓ ~ ℓ^{2/3}, soma 1/3 + 2/3 = 1; espectro E(k) ~ k^{−5/3} = k^{−(1+2/3)}.

## 6. O que falta — a declaração exata

Provar o Lema da Face Conjugada a partir das equações de Navier–Stokes, sem postulado: mostrar que a dinâmica do campo de direção de vorticidade ξ = ω/|ω| impõe retenção ≥ 1−h por oitava. Caminhos candidatos: o critério geométrico de Constantin–Fefferman (1993) + uma taxa de depleção de alinhamento; ou uma estimativa crítica direta em L³ (C2).

Enquanto o Lema estiver aberto, este documento é uma redução — a mais afiada que conseguimos — e não uma solução. O número corrige a frase.
