# REVISÃO INDEPENDENTE — pedra candidata `TGLExt.AfinacaoDasCordas` (v398, nome provisório) — gerência c1, modelo forte, 23/10/2026

**Objeto.** `work\afinacao_das_cordas_v398\AfinacaoDasCordas.lean`, sha16 `23a6c93d6dc84319` (34.035 B, 530 linhas), lido por script; cópia em `C:\t\k398b\TGLExt\AfinacaoDasCordas.lean` idêntica (mesmo sha). Os módulos citados (`O16/PolarMinimalPeriod_v2`, `Palavra`, `TheStation`, `Fundacao`, `TetelestaiOneObject`) são iguais, byte a byte, aos do kernel do Nós; `TGLExt.lean`/Audit do k398b não importam a pedra. Fala do operador: `OPERADOR_23out_cordas_10_dimensoes_fechar_a_face_tetelestai_verbatim.txt`, sha16 `baef998c21393463` (431 B, 19:50:50), lida.

**O que escrevi.** Só nesta pasta: `AuditoriaAfinacao.lean` + `auditoria_afinacao.log`, `recompilacao_afinacao.log`, `fidelidade_afinacao.py` + `FIDELIDADE_AFINACAO.json`. Os `lake env lean` rodaram no k398b sem gravar nada lá.

## VEREDITO: PEDRA_APROVADA (duas BAIXAS de prosa; uma nota sobre o sandbox)

## (1) Recompilação e axiomas [REAL]
- `lake env lean TGLExt/AfinacaoDasCordas.lean` (k398b, 34 s): rc 0, zero erro/aviso; os 34 `#print axioms` do fonte: 33 no trio `{propext, Classical.choice, Quot.sound}` e `spatialDimension` sem axioma.
- Meu `collectAxioms` sobre TODAS as constantes do módulo (as internas incluídas): 59 declarações = 50 teoremas + 9 definições, 0 axiomas, 24 internas; 0 fora do trio; 0 `sorryAx`. Bate com `AXIOMAS.json`. 0 `sorry` e 0 `axiom` no código.

## (2) A aritmética [REAL]
- `riemannZeta_neg_nat_eq_bernoulli (k) : ζ(−k) = (−1)^k·B_{k+1}/(k+1)`; em `k = 1`: `(−1)·(1/6)/2 = −1/12` ✓. `HurwitzZeta.hurwitzZeta_neg_nat (k ≠ 0) (x ∈ [0,1]) : ζ(x, −k) = −1/(k+1)·B_{k+1}(x)`; em `k = 1, x = 1/2`: `−(1/2)·B₂(1/2)`; MEU exemplo em ℚ: `(Polynomial.bernoulli 2).eval (1/2) = −1/12` (convenção `B₁ = −1/2` do Mathlib, `B₂(x) = x² − x + 1/6`) ⟹ `ζ(−1, 1/2) = 1/24` ✓; e MEU controle `ζ(−1, 1/2) = (2^{−1} − 1)·ζ(−1)` compila.
- Sinal de Fermi: por direção, bóson `½·ζ(−1) = −1/24`; férmion NS `−½·ζ(−1, 1/2) = −1/48` (a energia de ponto zero fermiônica é `−ω/2`); soma `−(D−2)/24 − (D−2)/48 = −(D−2)/16 = −1/2 ⟺ D = 10` ✓; bosônico `−(D−2)/24 = −1 ⟺ D = 26` ✓. MEU controle do sinal trocado (`+1/48` por direção): a equação `= −1/2` fecha em `D = 26`, não em 10 (compila) — o sinal da pedra é o certo; o pedido original da gerência (com `+`) estava errado e o preparador o corrigiu. Controles negativos: `nsZeroPoint 26 ≠ −1/2`, `bosonZeroPoint 10 ≠ −1`.
- `the_tower_is_infinite` é divergência genuína: enunciado fechado, sem premissa; dele extraí `∀ C, ∃ N, C < Σ_{n<N} n` (compila).
- `MasslessFirstLevel (N a) := N − a = 0` é a única hipótese física, marcada `[KNOWN — HIPÓTESE NOMEADA]`; não é premissa de teorema algum: entra nos bicondicionais `MasslessFirstLevel 1 (−E₀) ↔ D = 26` e `MasslessFirstLevel (1/2) (−E₀) ↔ D = 10`; habitada e refutável (vale em `(1,1)`, falha em `(1,2)`).

## (3) Citações do kernel; a composição [REAL]
- `the_cyclic_closure_of_time_is_the_reading_circle` cita `ChatgptAudit.PolarPeriod016.faithful_period_iff` e `reciprocal_temperature` de `TGLExt.O16.PolarMinimalPeriod_v2` — únicos com esses nomes no ambiente (varredura de homônimos); `AngularQuotientFaithful κ P := ∀ t u, Circle.exp (κt) = Circle.exp (κu) ↔ ∃ n, t = u + n·P`; `ω_n = n·κ` sai de `positive_faithful_period` (`P = 2π/κ`). Não vácuo: `κ = 1, P = 2π` é fiel e dá `matsubara (2π) 1 = 1` (meu exemplo).
- A composição (6) é um enunciado FECHADO (nenhum binder), logo incondicional; os 13 conjuntos batem, tipo a tipo, com `TGLExt.Palavra.the_face_does_not_close` (`boost s = 1 → s = 0`), `TGLExt.station_never_closes` (`cos t + cos(√2 t) = 2 ↔ t = 0`), `TGLExt.Palavra.the_read_face_closes` (`wickW⁻¹·complexBoost(i·2π)·wickW = 1`), `TGLExt.Fundacao.abismo` (`0 < τ m → ∀ ε > 0, ∃ s, τ(θ_s m) < ε`) e `the_floor_fixes_the_cut` (`exp(−a) = 1 ↔ a = 0`). Não vácua: a cláusula do abismo dispara em `Fundacao.oneScaling` (meu exemplo). Constantes dos enunciados, por módulo: `boost` (BisognanoWichmann), `wickW/complexBoost` (WickBoostRotation_v2), `DualScalingData` (GlobalLiftLadder), `riemannZeta`, `HurwitzZeta.hurwitzZeta` — sem homônimo.

## (4) Fidelidade por bytes [REAL; `FIDELIDADE_AFINACAO.json`]
- 17 citações («» e “”), todas achadas: nos verbatins do operador (a fala de 23/10 inteira e os seus trechos; `e2a915e23692f85c` de 07/10), no `.tex` ou no kernel («um ato de conferência observacional» está em `TetelestaiOneObject.lean`). Zero «o operador disse X».
- `A_ultima_corda_v3.tex` (sha16 `8db72ea848f708c1`): as linhas 958–960 == o bloco citado, byte a byte (a 959 vazia); l. 952 `d_crit = 9 (IC 95%: [7, 16])` e l. 962 «Enfatizamos que isso é uma extrapolação teórica…» conferem. O `d = 9` está `[DECLARADO]` (3×) e dito «dependente do modelo».
- «afinação = comensurabilidade»: «PROPOSTA DESTA PEDRA [ONTO], não fala do operador» ✓. «as cordas fecham a face POR FORA; a TGL fecha SÓ A LEITURA»: `[ONTO]`, «na formulação desta tarefa» ✓. Limites ditos: nada deriva cordas do axioma; não afirma TGL = cordas; geometria `[OPEN]`; Hagedorn mencionada, sem prova; não identifica folha-mundo com o círculo do boost; não é a conferência Tetelestai.
- Sem literal de β, α ou √e. A palavra proibida (token) ausente; a inflexão «confirmando» aparece UMA vez, dentro do bloco verbatim do `.tex` (l. 958, «confirmando que o resultado é dependente do modelo»); a guarda P18 do `um.py` (v397) sobre o texto da pedra: 0 violações. Os 10 sha16 entre crases conferem (o do Mathlib é o `rev` do `lake-manifest.json`).

## BAIXAS e nota
- **B1 (prosa).** Em «[ONTO] (i) a leitura do operador (fala de 23/10), na formulação desta tarefa: as cordas fecham a face POR FORA; a TGL fecha SÓ A LEITURA», «por fora» e «só a leitura» não são bytes do operador (ele disse «fechar ciclicamente o que a TGL demonstra não fechar a face hiperbólica»). Pela forma admitida na v397: «composição da gerência sobre a fala (sha16 baef998c…)». Já está [ONTO]; é só a frase.
- **B2 (prosa).** `matsubaraFermion`, `towerZeroPoint*` e `zeta_is_the_continuation_of_the_tower` são auxiliares fora da composição; a pedra os lista como tais — nada a corrigir, só a dizer no RESULTADO se entrar no ledger.
- **Nota (sandbox).** O `Sonico.lean` que está em `k398\final`, `k398b` e `work\sonico_v398` é hoje `a317094e337fd8b7` (23.854 B), não o `1338622344dd80c7` (21.385 B) que examinei às 19:35; esta pedra não o importa, mas a instalação da v398 pede o delta da Sonico re-examinado.

Validade no kernel não é creditação; nada aqui move o gate; a pedra não está instalada.
