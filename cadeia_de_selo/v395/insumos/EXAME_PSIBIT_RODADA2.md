# 2ª e ÚLTIMA rodada — Psibit v2, sha16 `50c199eb01976151` (gerência c1, modelo forte, 21/10/2026)

O sha16 `50c199eb01976151` é o mesmo em `work\psibit_v395` e em `C:\t\k395\final\TGLExt`. O `.bak_` da v1 foi ignorado.

## VEREDITO: PEDRA_APROVADA

1. **A composição é incondicional e não é vácua.** `psibit_is_the_mode_of_the_reader` não tem binder de topo nem `FockCertificate`. As hipóteses que restam ficam dentro das conjunções e são satisfazíveis: `cos²θ = sin²θ` e `sin 2θ ≠ 0` valem em θ = π/4. A BAIXA do ponto fixo também foi atendida: (6) agora vale nos pesos iguais π/4 + kπ/2, por `balanced_collapse_is_half` e `collapseEntropy_at_balanced_weights`.
2. **A face do psion ficou condicional e diz por quê.** `the_psion_face_of_the_psibit` está sob `∀ {L} (C : FockCertificate L)`. A docstring diz que o kernel não habita o certificado, e as duas fontes que cita estão certas: `TheImportedSecondQuantization` l.66–67, «NÃO-VACUIDADE … nenhum habitante … é exibido»; e `F1Fecho394/CanonicalFockAssemblyR1.lean`, «not a claim that the remaining imported fields are inhabited». A minha varredura do ambiente confirma: os únicos produtores de `FockCertificate` são o construtor e `rescale`.
3. **A bijeção é real nos dois sentidos.** `IsCode` é intrínseco: 0 ≤ w ≤ 1, Palavra = 0 ↔ w = 0, Verbo = 0 ↔ w = 1. `Set.BijOn` está provada de verdade nos dois sentidos (leva no conjunto, é injetiva pelo inverso e é sobrejetiva com preimagem explícita). Também estão provadas `Set.range v = UnitVec` (via `Complex.arg`) e `Set.range codeAmp = {c | IsCode c}`.
4. **Recompilação e axiomas [REAL].**
   - `lake env lean TGLExt/Psibit.lean`: rc 0, 32 s, sem erro nem aviso; os 25 `#print axioms` saem no trio (`recompilacao_psibit_v2.log`).
   - `lake build TGLExt.Psibit`: rc 0; o `.olean` da v2 já estava atualizado (`lake_build_psibit_v2.log`).
   - Auditoria própria (`auditoria_psibit_v2.log`): **133 declarações**, 101 teoremas, 0 fora do trio, **0 `sorryAx`**. Axiomas: 130 com o trio inteiro, 2 só com `propext`, 1 com `propext` e `Quot.sound`.

A divergência da patente (ACOM Mirror) não muda e segue com o operador [LEGAL]; ver `EXAME_PSIBIT.md`, item (5).
