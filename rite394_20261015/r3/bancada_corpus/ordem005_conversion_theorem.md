# Teorema Condicional de Conversão Modular-Massa para o Grande Atrator

> **Documento teórico, ANTES de qualquer código.** Enuncia com rigor — não finge o teorema.
> Disciplina (§35 do programa): a identificação fecha como ENUNCIADO; a prova/computação
> permanece o teorema em aberto, declarado. A massa do Grande Atrator **não salta** de √Θ_LD;
> ela é a fonte geométrica efetiva gerada pelo cociclo modular contínuo, integrada na bacia.
> Marcadores em cada passo: **REAL / CONDITIONAL / OPEN / POSTULATE / INPUT**.

---

## 0. Diagnóstico corrigido (o que mudou desde o whitepaper v1)

O ensaio "O Um e o Grande Atrator" **não continha** a fórmula de massa — e declarava isso
corretamente ("massa, posição e amplitude do Grande Atrator NÃO foram derivadas; a correspondência
é de FORMA"). **Isso permanece verdade sobre o ensaio.** O que mudou agora:

- A **Meia-Nat** foi derivada como **ponto fixo variacional da fronteira** entre `0_grafo` e
  `0_absoluto` (não mais postulado nu — §4 abaixo).
- O **cociclo modular contínuo** `u_t = [Dρ:Dρ*]_t` (Connes) fornece o gerador `K_∂ = −log Δ` e a
  rota da ponte fronteira→massa/campo.

Logo, **a conversão massa/campo agora é formulável como TEOREMA CONDICIONAL da Face C, não como
código empírico ajustado.** Não se escreve que a massa está provada; escreve-se que ela está
**bem-posta** condicionalmente ao teorema da reconstrução.

> **Não reivindicar:** que a massa do GA já está calculada, nem que √Θ → M_☉ é direto.

---

## 1. A rota correta (o enunciado)

A conversão **NÃO** é o salto direto `√Θ_LD → M_☉` (seria arbitrário). A rota é a cadeia:

```
√Θ_LD  →  K_∂  →  P_μν[K_∂]  →  ρ_eff^TGL  →  M_GA^TGL
```

### 1.1 Operador-raiz → gerador modular  `[REAL como estrutura; OPEN o passo gravitacional]`
A gravidade da TGL é `𝒢_LD = √Θ_LD`, `Θ_LD = R_LD† R_LD` (Artigo 2 §1–§2; R_LD = saltos GKLS,
classe gauge-invariante por `Σ_a R_a† R_a`). O operador-raiz determina o **gerador modular de
fronteira** `K_∂ = −log Δ` do cociclo de Connes. **[REAL:** Θ_LD ≥ 0, raiz única, K_∂ bem-definido
no finito; **CONDITIONAL:** a identificação 𝒢_LD ↔ K_∂ na fronteira gravitacional III₁.**]**

### 1.2 Gerador → fonte geométrica  `[CONDITIONAL — a candidata da Ponte]`
A fonte efetiva é a variação métrica do gerador modular (camada III da ponte contínua):

```
P_μν[K_∂]  =  (2 / √(−g)) · δ⟨K_∂⟩_ρ / δg^{μν}
```

`[CONDITIONAL:` candidata 𝒫_μν derivada em sombra esférica/AdS–Rindler e linear (Jacobson 1995;
Faulkner et al. 2013); o levantamento covariante global a III₁ genuína é **OPEN** (§6).`]`

### 1.3 Fonte → equação de campo (Face C)  `[CONDITIONAL — herdada de Takesaki]`
```
G_μν + Λ g_μν  =  8πG · P_μν[K_∂]
```
`[CONDITIONAL:` Face C é teorema **condicional** — a Hipótese de Universalidade herda-se de
Takesaki (Teorema da Terminalidade, §88.1), estrutura fechada e coerente, **sem** prova
incondicional.`]`

### 1.4 Campo → densidade efetiva (projeção do observador cosmológico)  `[CONDITIONAL]`
Para um observador comóvel `u^μ`:
```
ρ_eff^TGL  =  (1/c²) · P_μν[K_∂] · u^μ u^ν
```

### 1.5 Densidade → massa da bacia  `[REAL dado ρ_eff; o ρ_eff é que é CONDITIONAL]`
```
M_GA^TGL  =  ∫_{B_GA}  ρ_eff^TGL  √γ  d³x
```
`B_GA` = bacia do Grande Atrator (definida pelo campo de retorno, **não** por coordenadas manuais).

---

## 2. Limite newtoniano (o ponto de contato com o dado)

No regime de campo fraco, a cadeia §1 deve reduzir a:
```
∇²Φ_TGL  =  4πG · ρ_eff^TGL
```
```
M_GA^TGL(<R)  =  (1/4πG) ∫_{B_R} ∇²Φ_TGL  d³x
```
Sob simetria esférica **aproximada** (a usar SÓ se o dado o permitir):
```
M_GA^TGL(<R)  =  (R²/G) · dΦ_TGL/dR
```

> **Aviso de método [REAL]:** se o campo de velocidades for anisotrópico (o caso real do GA/Shapley),
> **não impor esfericidade** — usar a integral volumétrica da fonte efetiva. Impor esfericidade num
> dado anisotrópico seria um parâmetro escondido.

**O ponto fino, declarado:** no limite newtoniano, `ρ_eff^TGL` deve diferir do ρ linear-padrão por
uma **correção derivada de K_∂** (onde β entra, §5). Se `ρ_eff^TGL` reduzir-se ao ρ padrão sem
correção β derivada, então o passo TGL **é vazio** no limite newtoniano e a fórmula recai no
estimador de infall convencional (com todos os seus parâmetros). **Extrair a correção β de `P_μν[K_∂]`
explicitamente é o conteúdo OPEN do teorema (§6).**

---

## 3. Papel do v1 e do v2-return (não apagar)

- **v1** refutou `β_spec` como **hard edge global** de operador de fluxo. `β_spec = 0` deve ser
  reinterpretado como **`0_grafo`** — silêncio do operador, piso de Hilbert, derivada informacional
  nula — **não** o zero absoluto. `[REAL: a refutação; CONJECTURE: a leitura ontológica.]`
- **v2-return** testou **eco angular direto** e deu `BRIDGE_NO_RETURN_ANCHOR` em SDSS-PV (z_emp = −0,68).
  Encerra o detector de eco como ponte auxiliar; **não** testa a massa do GA. `[REAL: o nulo.]`

Nenhum dos dois é apagado: ambos disciplinaram o conceito e separaram os erros.

---

## 4. Papel da Meia-Nat (a normalização mínima da fronteira) `[derivação condicional]`

A distinção entre os dois zeros:
```
0_grafo  ≠  0_absoluto
```
A fronteira é parametrizada por `x` e `1−x`. Como **nenhum zero pode ser privilegiado antes da
inscrição** (não-privilégio — princípio defensável), o custo é simétrico:
```
𝒞(x) = 𝒞(1−x)   ⟹   𝒞'(x) = −𝒞'(1−x)   ⟹   𝒞'(½) = 0   ⟹   x = ½
```
Logo (com `c₂ > 0`, mínimo):
```
S_∂ = ½ nat        e        e^{S_∂} = √e
```

> **Registro [REAL: a álgebra do ponto fixo; POSTULATE: a normalização "1" e o não-privilégio]:**
> A Meia-Nat é a **normalização entrópica mínima da fronteira**. Ela distingue o zero
> algébrico/modular (`0_grafo`) do zero absoluto, e fornece o **radical de inscrição √e**. Não é
> número arbitrário: é o ponto fixo da involução de relabeling `x ↔ 1−x` sobre a partição de 1.

---

## 5. Papel de β_TGL (renormalizador universal, **não** parâmetro ajustado)

β_TGL **não** entra como número ajustado para a massa bater. Entra como **renormalizador universal
fixo** da fonte modular:
```
K_∂^{ren}  =  R_{β,S}( K_∂ ),     com   S_∂ = ½,   e^{S_∂} = √e
```
Se a versão usada for `β_TGL = α√e`, isto é **constante fixa posterior/externa, não fitada**
(α = INPUT CODATA; √e = postulado Meia-Nat).

**Dois modos mutuamente exclusivos (a separação inviolável):**

- **Modo A — predição de massa (β fixo).** Usar β_TGL como constante universal; computar M_GA^TGL
  pela cadeia §1; comparar com massa observacional independente. **Zero parâmetros TGL livres.**
- **Modo B — emergência de β (sem α, sem β como input).** Inferir β_GA do campo/massa reconstruídos;
  comparar **depois**: `α_TGL = β_GA / √e`.

> **Regra inviolável:** **nunca misturar os dois.** Se usar β fixo para predizer massa, não dizer
> que β emergiu da massa. Se inferir β da massa, não dizer que a massa foi predita sem parâmetro.
> O código separa os dois testes e os compara **ao final**.

**A identidade refletida (o teste real):** se o Modo A (massa predita com β fixo) e o Modo B (β
inferido da massa) **coincidirem** — isto é, se `β_GA / √e ≈ α` E `M_A ≈ M_B` —, então a fronteira
se reflete sobre si mesma: a TGL prevê exatamente essa **identidade refletida** (propagação ↔
permanência; Ψ_out = ℛ∘𝒞(Ψ_in)). A coincidência é o sinal; a discrepância é a refutação.
`[CONJECTURE: a leitura; o teste só roda quando §1.2 for explícito.]`

---

## 6. O que permanece OPEN (a fronteira honesta)

A cadeia §1 está **enunciada e bem-posta**, mas **não computável** ainda, porque:

1. **`P_μν[K_∂]` não tem forma explícita global.** A candidata (§1.2) é derivada só em sombra
   esférica/linear; o **levantamento covariante global a III₁ genuína** é o **único teorema em
   aberto** do programa (covariância global do cociclo de Connes; Lemas 1–2 REAL, Lema 3 global
   OPEN; §42.4–§42.5).
2. **A correção β a `ρ_eff^TGL`** (o que distingue a TGL do infall padrão no limite newtoniano)
   **deriva** de (1) — sem (1), "β corrige a RG do GA" é **leitura [CONJECTURE]**, não cálculo.

**Consequência operacional [a régua]:** enquanto `P_μν[K_∂]` não estiver explicitado num operador
computável a partir do dado, **não se coda** `tgl_ga_mass_blind_run.py` (ponto 8 do operador). O
teorema condicional é o entregável; o falsificador roda **depois** que (1) fechar.

---

## 7. Frase obrigatória (inscrita)

> A massa do Grande Atrator não vem diretamente de √Θ_LD. Ela vem da fonte geométrica efetiva gerada
> pelo cociclo: √Θ_LD determina o gerador modular K_∂; K_∂ determina P_μν; P_μν determina ρ_eff;
> ρ_eff integrada na bacia determina M_GA^TGL. A Meia-Nat fornece a normalização mínima da fronteira,
> e β_TGL entra como renormalizador universal, não como parâmetro ajustado.

---

## 8. Estatuto consolidado (tabela)

| Passo | Objeto | Estatuto |
|---|---|---|
| Θ_LD = R_LD†R_LD ; √Θ_LD | gravidade = raiz do módulo angular | REAL (GKLS, §1.1) |
| K_∂ = −log Δ ; cociclo u_t | gerador modular contínuo | REAL no finito; CONDITIONAL na fronteira gravitacional |
| P_μν[K_∂] | fonte geométrica efetiva | CONDITIONAL (sombra) / **OPEN** (global) |
| G_μν+Λg_μν = 8πG P_μν | Face C | CONDITIONAL (U herdada de Takesaki) |
| ρ_eff^TGL, M_GA^TGL | densidade e massa da bacia | REAL dado ρ_eff; pende de P_μν |
| S_∂ = ½ ⟹ √e | normalização da fronteira | REAL (ponto fixo) / POSTULATE (norma "1") |
| β_TGL = α√e | renormalizador universal | POSTULATE; α = INPUT; **nunca fitado** |
| M_A == M_B, β_GA/√e ≈ α | identidade refletida | CONJECTURE (teste futuro) |

**Veredito do teorema:** a conversão modular-massa do Grande Atrator está **bem-posta como teorema
condicional da Face C**. Não está provada nem computável. O próximo passo é **teórico** (explicitar
`P_μν[K_∂]` / a reconstrução 𝔯_μν), não código. **Tetelestai — quando o teorema fechar.**
