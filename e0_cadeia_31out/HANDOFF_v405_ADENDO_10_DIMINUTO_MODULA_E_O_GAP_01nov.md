# HANDOFF v405 — ADENDO 10 (01/11/2026): o diminuto modula a tônica; o gap do ângulo de Miguel

**De:** gerência c1, em nome próprio. **Resposta do operador** (verbatim sha256 `7c2caaa87b0cdb01`). O adendo 9 fica como registro; esta é a leitura vigente onde os dois divergem.

## O que a fala decide
- **O diminuto é modulação.** Só a tônica desce o meio-tom pinado; as demais notas ficam sustentadas, e por isso desce pinado; a escala e o tom ficam. A transposição do `AcordeE0` é só a liberdade do no-go. O adendo 9 ligou «mantendo a escala» à transposição: errado.
- **A conferência de 31/10 §10 tinha razão, e a §20 de hoje errou ao corrigi-la.** O meio-tom pinado quebra a simetria do acorde: separa a tônica das notas sustentadas (`modular_nao_e_transposicao`). Não quebra a liberdade global (`modular_comuta_com_transpor`).
- **«Operando em terças»:** na afinação tom = nat, a nota que estava um tom acima fica três meios-tons acima da tônica modulada, e^(3/2) (`um_tom_vira_terca_menor`).

## A conexão que faltava [REAL, salvo onde marcado]
- **O lock.** O lock mínimo do Hamiltoniano oculto, H_min = 1 − P, tem gap 1: vale 0 no vácuo e 1 no ortogonal (`o_lock_tem_gap_um`). No estado a um ângulo θ do vácuo, ⟨H_min⟩ = sen²θ (`lock_no_angulo`). No ângulo de Miguel, β (`lock_no_angulo_de_miguel`).
- **O gap na unidade posta:** Δ = β·u = sen²θ_M·u, a energia retida.
- **Tudo é Δ:** tônica = Δ/α; massa = Δ·sen 45°; ħω_psíon = √2·Δ; ½·ħ(2/τ) = Δ; ω_psíon = (2/τ)·sen 45°.
- **A ligação de duas pedras:** a frequência do sistema da `TonicaDoHamiltoniano`, √2/τ, e a do psíon da `PontoZeroDoPsion`, √2·β·u, são iguais se e só se τ = ħ/Δ (`a_frequencia_do_sistema_e_a_do_psion_iff`).

## O que é leitura, e o limite
- **[ONTO, a ratificar]** ler τ = ħ/Δ como o τ★ do sistema. É tempo próprio, não t_P.
- **[REGRA do operador, 24/08]** κ é testemunha; `κ = F(α, β, θ_M)` é proibido como objetivo de busca. Na pedra κ só entra como hipótese.
- **`U_E_NOT_DERIVED` fica.** Δ carrega u. O que se reduz é a lista do Kimi: gap, κ, τ★, carga e fluxo são um só número, não seis. A unidade segue posta, e a fala do operador sobre a origem da medida é [ONTO] sobre o estatuto de POSTO.
- **Negativo medido:** sob esta leitura, E_fluxo = c⁵τ/(4πG) ≈ 10⁵⁷ eV, logo a ponte E_fluxo = E₀ do Kimi não vale.
- **Disco:** K = Ω²·E não depende da inclinação; o ângulo não fixa K. [OPEN]
- **Forma no kernel do «fundo»:** `zero_mode_weight_is_one` (∫¼sech²(κ/2) dκ = 1, faces ½) e `alpha_transport` (gradiente negativo). Forma, não derivação da unidade.

## Recibo
`RECIBO_ERRATA_PEDRAS_R4_01nov.json` (sha256 `dee017f551d21854`): `LeiDoDiminuto` `49e9d8e708eb03d0`, `PontoZeroDoPsion` `b6a692ee71134e26`.

## AO LADO (01/11/2026, 18:5x, gerência c1): a errata R5, a escala é o que fica parado

Achado do preparador: as pedras chamavam de escala a razão à tônica, que o diminuto altera; a fala diz «mantendo a escala». Vigente: a escala é o que fica parado, as notas sustentadas e as razões entre elas (`modular_mantem_a_escala`); a razão à tônica muda. A escala de energia do no-go chama-se valor absoluto, e a outra, valor relativo à tônica. Rebatizados: `mesmas_razoes_iff_transposicao`, `as_razoes_nao_fixam_o_absoluto`. Onde os textos desta data dizem «mesma escala» para dois acordes transpostos, leia-se «mesmas razões». Recibo sha256 `f4654673043c8525`; `LeiDoDiminuto` `aa0e8411dd15eb9f`.

## ERRATA AO LADO (01/11/2026, 20:5x, gerência c1, em nome próprio; achado da segunda revisão de terceiro): o gap é u, não Δ

O texto acima chamou Δ = β·u de gap: errado. O gap espectral do lock é 1, na unidade posta `u`, o E₀ da Lei do Diminuto, e a tônica fica meio-tom acima dele. Δ é o valor esperado do lock no ângulo de Miguel, a energia retida, 1/β vezes menor que o gap. A tabela lê-se assim: gap, u = 1 eV; tônica, √e·u; retido, β·u = 12,03 meV. Que o ângulo de Miguel seja o sistema do gap é leitura do operador [ONTO]. Os lemas do lock valem em qualquer espaço de Hilbert; `HminMic` é instância condicional a um `FockCertificate`, que o kernel não habita. Rebatizados: `retidoNoAngulo`, `tempoDoRetido`. A leitura do «fundo» por `zero_mode_weight_is_one` e `alpha_transport` é da gerência [ONTO], com homônimo: `alphaKappa` não é a α de estrutura fina. Que o tom fique é fala do operador [INPUT]: o kernel não tem termo para o tom. Recibo R7 sha256 `2740f7e50df1b7a7`; `PontoZeroDoPsion` `c64079a9c5b3e0e1`.
