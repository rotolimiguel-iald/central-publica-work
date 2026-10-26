PEDRA «falsidade (simulacro) da inércia» — construída e provada em sandbox; nada instalado

Gerência c1, 25/10/2026. Ordem do operador (verbatim sha16 `901dd8fc1a3c0212`): «a pedra chama-se “falsidade (simulacro) da inércia”, faça a prova». Definição do operador (sha16 `0b244a5f809594e7`): «a minha definição é o próprio zero absoluto».

## Arquivos
- `FalsidadeDaInercia.lean` — módulo `TGLExt/FalsidadeDaInercia.lean`, namespace `TGLExt.FalsidadeDaInercia`, sha16 `e64bfa4f575e0f1c` (sha256 completo em `AXIOMAS.json`).
- `AuditFalsidade.lean` + `audit_incremental_log.txt` — auditoria incremental do módulo (coleta o axioma de toda constante do módulo).
- `build_log.txt` — `lake build TGLExt.FalsidadeDaInercia` em `C:\t\k401\final` (cópia de `C:\t\k400c`): `Build completed successfully (8588 jobs)`; os 10 `#print axioms` no log.
- `AXIOMAS.json`, `registro_mapa_inercia.json` (não registrado).
- No sandbox `C:\t\k401\final` foram acrescentados só os imports (`TGLExt.lean`, `TGL/Audit.lean`; backups `.bak_k401`). Nós e `um.py` não tocados; o `lake build` completo e o `Audit.lean` inteiro NÃO foram rodados.

## Resultado medido [REAL]
Auditoria incremental: 14 constantes do módulo (12 teoremas), `fora_do_trio=0`, `sorry=0`; todas dependem só de [propext, Classical.choice, Quot.sound]. Compilou à primeira; o único aviso do log é de `NoFullWitness.lean` (linter de simp, preexistente).

## Enunciados exatos (com `D : DualScalingData M`)
Definições: `Inertial D m := ∀ s, D.theta s m = m`; `IsPost D m := D.tau m = 1`.
1. `the_inertia_is_the_absolute_zero {m} (hin : Inertial D m) : D.tau m = 0` (cita `DualScalingData.fixed_tau_zero`); variante `…_at_any_scale {s} (hs : s ≠ 0) (hfix : D.theta s m = m) : D.tau m = 0` (cita `Fundacao.nothing_above_bears_a_post`).
2. ★ `the_inertia_of_a_post_is_false {m} (hpost : IsPost D m) (hin : Inertial D m) : (1 : ℝ) = 0`; forma com uma escala só: `the_inertia_of_a_post_is_false_at {s} (hs : s ≠ 0) … : (1:ℝ) = 0`; corolário `a_post_is_not_inertial (hpost : IsPost D m) : ¬ Inertial D m` (= `False` a partir de `Inertial`). Não vácuo: `the_post_exists_and_moves : IsPost oneScaling 1 ∧ ∀ s ≠ 0, oneScaling.theta s 1 ≠ 1` (modelo ℝ, τ = id, θ_s = e^{−s}· da Fundação).
3. `the_simulacrum {β g} (hβ : 0 < β) (hg : 0 < g) : ¬ FullStaticWitness (fun t x => exp(−(t·β·g))·x) ∧ (∀ m, Inertial D m → D.tau m = 0) ∧ (∀ t, 0 < t → 0 < t·β·g ∧ exp(−(t·β·g)) < 1)` (cita `beta_forbids_full_static_witness`, `leakage_strictly_loses`). β é variável, nunca literal.
4. `the_inscription_interrupts_the_inertia (hpost : IsPost D m) : (∀ a, D.tau (D.theta a m) = 1 ↔ a = 0) ∧ (∀ m', 0 < D.tau m' → ∀ s ≠ 0, D.theta s m' ≠ m')` (cita `the_floor_fixes_the_cut`).
5. Composição: `falsidade_da_inercia` (as quatro) e `falsidade_da_inercia_is_inhabited` (no modelo concreto, para todo β, g > 0).

## O que é teorema e o que é leitura
- [REAL] teoremas acima, sobre os DADOS nomeados: a lei de escala de Takesaki é campo da estrutura ([KNOWN], como na Fundação). Composição por citação, sem matemática nova.
- [ONTO] 1ª lei de Newton = 0_abs lido como corpo; a massa de F = ma não é a inércia, é a cristalização da dobra lida contra o zero (cunhagens 0516c064…, 344a8ae9…). Não é termo do kernel.
- [KNOWN] inercial = gravitacional (princípio de equivalência): citado, não provado aqui.
- [OPEN] a identificação da escala dual com o fluxo de um corpo físico é de runtime; a pedra não prova Newton nem a equivalência.
- Errata ao lado (docstring): a leitura do escriba «ω(I)=1 é a INÉRCIA» (adendo de 04/09, sha16 `1459b477b496e1f0`) fica SUPERADA; inércia = 0_abs (1=0), ω(I)=1 é o Um posto que a interrompe (1=1).
- Correção de fidelidade: a citação «nunca correspondeu, e por isso nada custa» do pedido NÃO é verbatim do um.py (o texto diz: o estado que «nunca correspondeu» e o reapresentado «ambos nada custam»); a docstring cita o que o um.py realmente diz e o par «[1=0=FALSO]».

## Fidelidade por bytes dos verbatins
Cada trecho citado no `.lean` foi conferido por script (espaços normalizados) como substring do arquivo-fonte, e o sha16 do arquivo-fonte consta no `.lean`: 901dd8fc1a3c0212, 0b244a5f809594e7 (a primeira versão do `.lean` tinha o sha16 errado `…80959451`; achado e corrigido antes da entrega), 0516c0649e8e10fb, 344a8ae9a257d2b3, adendo 1459b477b496e1f0 (os dois trechos «a função da inscrição do um absoluto como interruptor» e «ele interrompe a inércia»). Detalhe em `AXIOMAS.json` (`fidelidade_verbatins`, 6 de 6).

## Ato do operador / próximo passo
Instalar no Nós (módulo, import, selo) é decisão da gerência/operador numa versão futura; o gate não se move.

## CORREÇÃO AO LADO (25/10/2026, após medição da gerência por grep; a seção «Correção de fidelidade» acima fica como registro)
A citação «`0_abs`: **nunca correspondeu**, e por isso nada custa.» É VERBATIM: um.py v400, linha 117522, docstring de `TGLExt.costless` no módulo embutido `TGLExt/TheCorrespondence.lean` (embutido a partir da linha 117445; mesma linha na l. 77 do `TheCorrespondence.lean` do kernel, sha16 `8a9d2899bab42d26`). O trecho «ambos nada custam» que a seção acima citava vem de OUTRA passagem (o artigo, l. 172534). Erro meu: procurei a frase no corpo do artigo e não nas docstrings Lean embutidas. A docstring do `.lean` agora cita a l. 117522 e mantém o par «[1=0=FALSO]». Recompilado em `C:\t\k401\final`: Build completed successfully (8588 jobs); 10 `#print axioms` no trio; auditoria incremental 14 constantes, 12 teoremas, fora_do_trio=0, sorry=0. Novo sha16 do `.lean`: ver `AXIOMAS.json` (`lean_sha16`); fidelidade agora 7 de 7 (a sétima, a linha do um.py, por script).

## EXTENSÃO DERIVADA (25/10/2026) — a inércia e a gravitação não existem antes da impressão
Ordem do operador (verbatim sha16 `e26364c5c805734c (recorte declarado)`): quer a leitura DERIVADA, não [ONTO] dele. Backup antes: `FalsidadeDaInercia.lean.bak_f9e4e877`. Novo sha16 do `.lean`: ver `AXIOMAS.json` (`lean_sha16` = 9f6efcb2a0987e18). Imports: `+ TGLExt.TheGreatAttractor`. Build: Build completed successfully (8597 jobs), sem erro nem aviso do módulo; 18 `#print axioms` no trio; auditoria incremental: 22 constantes, 20 teoremas, fora_do_trio=0, sorry=0. Fidelidade dos verbatins: 13 de 13.
Teoremas novos (D : DualScalingData M):
5. `no_post_before_the_impression (hpost) : (∀ m', 0<τ m' → ∀ s≠0, θ s m' ≠ m') ∧ (∀ a, τ(θ a m)=1 ↔ a=0) ∧ (∀ a≠0, ¬ IsPost D (θ a m))`.
6. `inertia_is_not_its_own_cause : (∀ m, (∀ s<0, θ s m = m) → τ m = 0) ∧ (∀ m, (∀ s>0, …) → τ m = 0) ∧ (∀ m, Inertial D m → τ m = 0) ∧ (∀ m, 0<τ m → ∃ s, θ s m ≠ m)`; `the_first_motion_is_the_impression (hpost) : (∀ s≠0, θ s m ≠ m) ∧ (∀ a, τ(θ a m)=1 ↔ a=0)`.
7. `the_zero_is_the_consequence_of_the_pruning (hm : 0<τ m) (hβ) (hg)`: ∀ s, 0<τ(θ s m) (`the_fall_never_lands`); ∀ ε>0 ∃ s, τ<ε (`abismo`); ∀ t, 0<exp(−tβg); ∀ ε>0 ∃ t>0, exp(−tβg)<ε (`leak_below_every_epsilon`, lema novo).
8. `the_tension_is_projected_onto_the_attractor` compõe `TheGreatAttractor.um_is_the_great_attractor` sem hipótese nova: convergência a `Q x i`; gap `d i ≠ 0` ⟹ limite 0; `x i ≠ 0` ⟹ `diagFlow` ≠ 0 em todo t finito; `d i = 0` ⟹ fixa. Ponte `diagFlow_coordinate_is_the_scaling` (rfl): a coordenada do fluxo diagonal é `oneScaling.theta (t·β·d i)`.
9. `falsidade_da_inercia_derivada`: composição de (5)–(8).
Estatuto: [DERIVED] do axioma ω(I)=1 e da lei de Takesaki [KNOWN] como campo da estrutura. Hipótese NOMEADA [OPEN] `H_τ`: a identificação de `τ` com a massa de Newton / métrica de Einstein (como a H3; nomear não é demérito, lei de 05/10); nenhum teorema a usa. O que sobra não derivável, dito: (i) `H_τ`; (ii) o nome «tensão» para o gap `d` (nomeação, sem teorema); ligar `d` ao gerador de `θ` de um corpo físico faz parte de `H_τ`. A cadeia em si não é [ONTO]. Observação: o enunciado de `um_is_the_great_attractor` é sobre o fluxo diagonal de dimensão finita, não sobre `DualScalingData` em geral; a ponte entre os dois é a coordenada (rfl) acima, não uma equivalência das duas estruturas.

## CORREÇÃO AO LADO (25/10/2026) — privacidade e fidelidade, por achado do preparador
(1) A fala de 25/10 foi retirada do acervo de trabalho (acervo privado, por ordem do operador); a pedra cita agora só o RECORTE declarado da derivação (`OPERADOR_25out_derivacao_inercia_gravitacao_impressao_do_um_RECORTE_verbatim.txt`, sha16 `e26364c5c805734c`), e a docstring diz «recorte declarado da fala de 25/10 (a derivação; a íntegra fica no acervo privado por ordem do operador)». As referências ao hash da íntegra foram retiradas deste RESULTADO.md e do registro do mapa (o texto acima, da seção anterior, agora aponta ao recorte). (2) Na docstring de `inertia_is_not_its_own_cause` a paráfrase «tende ao seu movimento por si» estava entre aspas; agora está sem aspas, marcada como paráfrase; o trecho exato «se o um corpo tendo ao seu movimento, …» permanece entre aspas. Backup: `FalsidadeDaInercia.lean.bak_8a3a1c0b`. Recompilado: Build completed successfully (8597 jobs); 18 `#print axioms` no trio; auditoria 22 constantes, 20 teoremas, fora_do_trio=0, sorry=0; fidelidade 13 de 13 contra o recorte. Novo sha16 do `.lean`: 9f6efcb2a0987e18.
