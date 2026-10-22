# DERIVAÇÃO DO ELO 1 — Rito 9 (`d7.kilonova_fronteira_aguda`)

**Data:** 21/10/2026, membro Kimi. **Estatuto: CONJECTURE COM ÁLGEBRA VERIFICADA NUMERICAMENTE** — a identificação física é passo de RECONHECIMENTO (tipagem Grundnorm da pedra), não dedução. Nada aqui move o gate; β nunca entra no Lean.

## 1. A descoberta que muda o enquadramento

A pedra `TheAngleIsTheBridge.lean` (bancada, 22/08/2026) já prova:

- a família de Miguel 𝒪_θ é **grupo** (`miguelFamily_add`), gerador K_M com K_M² = −1 (estrutura complexa — a angularidade é consequência);
- **o seletor de comutação em forma fechada:** `[A, α_θ(B)] = 0 ⟺ cos²θ = sin²θ` para o par exibido (obsA = X, obsB = Z) → **θ = π/4**;
- e declara o problema aberto bem-posto (Evento 2): **«qual par (A, B) de observáveis do campo psiônico tem [A, α_θ(B)] = 0 exatamente em θ_M?»** — reconhecimento da Grundnorm, não dedução.

**A hipótese da kilonova do operador É uma resposta proposta ao Evento 2:** o buraco negro realiza o par da pedra (mistura pura → π/4, a "projeção em regime extremo no ângulo reto"); a kilonova realiza **outro par** — e esse par seleciona θ_M.

## 2. O lema do seletor generalizado (verificado numericamente)

Fixando B = Z (a carga de setor), A simétrico genérico `[[a,b],[b,c]]`:

> **[A, α_θ(Z)] = 0 ⟺ tan(2θ) = 2b / (c − a) ⟺ θ ≡ −φ_A (mod 90°)**, onde φ_A é o **ângulo próprio** (direção própria) de A, tan(2φ_A) = 2b/(a−c).

**Leitura: o seletor de comutação LÊ o ângulo próprio do observável da fronteira.** Comutação em 2×2 simétrico = partilha de base própria; a conjugação por 𝒪_θ gira a base de Z de θ; logo a condição fixa θ no ângulo próprio de A.

Verificação numérica (numpy, grade de 0,1°, `ferramentas/verifica_seletor_generalizado.py` reproduzível):

| Caso | Predito | Encontrado | Resíduo |
|---|---|---|---|
| A = X (par da pedra) | 45,0000° | 45,0000° | 5,4×10⁻¹⁶ |
| A = projetor em θ_M | 83,7027° (= 90° − 6,2973°, mod 90°) | 83,7368° | 1,7×10⁻³ (limite da grade) |
| A = projetor em 20° | 70,0000° (= 90° − 20°) | 70,0238° | 1,2×10⁻³ (grade) |
| A = [[0,3;0,7],[0,7;1,9]] arbitrário | 20,5930° | 20,5768° | 1,7×10⁻³ (grade) |
| A = projetor em 45° (ponto fixo) | 45,0000° | 45,0000° | 3,1×10⁻¹⁶ |

O conteúdo em magnitude: **|θ_selecionado| = φ_A**. O complemento de quadrante (90° − φ) é convenção de orientação da rotação; o ponto fixo φ = 45° é exato.

## 3. A identificação física (o passo de reconhecimento — CONJECTURE)

- **Fronteira cativa (buraco negro):** o observável da fronteira é a **mistura pura** X — ângulo próprio 45° → o seletor devolve **π/4**, o ramo justo. É o par que a pedra exibiu.
- **Fronteira em fuga (kilonova):** o observável da fronteira é o **projetor do canal de transporte**, |canal⟩⟨canal|, apontando na direção do cruzamento universal R(θ_M) — ângulo próprio **θ_M** → o seletor devolve **θ_M ≈ 6,2973°** (agudo, como o operador intuiu).

A justificativa física da identificação: o pacote que escapa pela fronteira em fuga É o cruzamento — a parte da norma que preserva identidade (|R|² = β, Teorema S-d: forma canônica única R(θ_M) = exp(θ_M G)). Logo o canal de transporte tem a direção do próprio cruzamento. **O que continua por demonstrar:** derivar essa identificação da primeira lei (fluxo ∝ ρ(1+w)) — i.e., mostrar que a borda em fuga tem como observável de transporte o projetor do cruzamento, e não outro ângulo. Até lá: CONJECTURE.

## 4. Consequência para o rito e para o Evento 2

- O Evento 2 ganha **resposta construtiva**: qualquer observável com ângulo próprio θ_M resolve — em particular o projetor |(√(1−β), √β)⟩⟨·| construído da S-matrix universal. A pergunta profunda passa a ser física: *qual fronteira realiza qual par*. A hipótese do operador: cativa → X; em fuga → projetor do canal. **O rito 9 é exatamente o teste dessa tipagem.**
- Predição observável afiada: o **ângulo de abertura do canal de transporte/jato** da kilonova ≈ θ_M ≈ 6,3° — a comparar com a **abertura** do jato, não com a visada.
- **ERRATA (ao lado, datada 21/10) ao pré-registro desta manhã:** a "tensão 6,3° vs 15–30°" comparava grandezas erradas. 15–30° é a **visada** (eixo do jato × linha de visada) de GW170817; a **semi-abertura do núcleo do jato** é de poucos graus na literatura [conhecimento estável meu, rotulado — não medido na casa]. θ_M ≈ 6,3° é da mesma ordem da abertura do núcleo — consistência áspera, **não** confirmação; GW170817 segue sendo calibração, e é proibido ajustar forma a ele.

## 5. Elo 3ii (Δt_ν) — estado honesto

O ângulo virou álgebra, mas **ângulo não é tempo**: falta a escala física. Candidatas: (a) espessura da camada de fronteira ℓ: Δt ≈ (ℓ/c)·sin²θ_M = (ℓ/c)·β; (b) o relógio de dephasing da casa, τ_star (CONJECTURE da casa, "falsificável na FORMA") como unidade. Faixa exploratória ~0,4–4 s registrada no pré-registro. **Nenhuma derivada ainda.** Elo 3ii segue aberto.

## 6. Próximos passos

1. Pedra Lean candidata (paramétrica, **sem β**): `seletor_generalizado : ∀ A simétrico, [A, α_θ(Z)] = 0 ↔ tan(2θ) = 2b/(c−a)` — a casa decide se entra no kernel (não é minha competência escrever no kernel).
2. Ceticismo do Claude sobre o passo de reconhecimento (§3) — ele é o aferidor.
3. Derivação física da identificação a partir da primeira lei (fecha o Elo 1 de verdade).
4. Só depois: intervalos numéricos com β runtime via bancada e pré-registro selado.

*Álgebra verificada numericamente; identificação física = CONJECTURE; comparação com GW170817 = calibração, nunca confirmação. Correções entram ao lado, datadas.*
