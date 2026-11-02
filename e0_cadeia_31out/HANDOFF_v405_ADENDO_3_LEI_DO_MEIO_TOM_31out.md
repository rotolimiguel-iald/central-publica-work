# HANDOFF v405 — ADENDO 3 (31/10/2026): a lei do meio-tom pinado, com o tom fixado («o tom é a nat»)

**De:** gerência c1, em nome próprio. **A lei do operador** (quatro verbatims, sha256: `8300a509ca9549e3057d5d1122aecc81b28fc64177a5e0ba80d77141c3e008a6`, `0798c7839ad5ebe0eab93eb02edae1612dff2ddde7311fa80c5d9616306f4b63`, `79c7999956e6d8e0e195f0999631244c86fe3de7546661ddbecfbcf6ccceb8ac`, `270fd74d5d79bf4d22a569b50b69f41ad034504e1ad897e94e2eac8b95d2fe4a`): E₀ não desce a oitava; mantém-se a escala da pêntada (definida pelo hamiltoniano oculto) e desce-se só o meio-tom pinado da nota principal; o tom é a nat.

## O que entra na v405 (6ª pedra, depois de `E0LiberdadeDeEscala`, que ela levanta)
- `TGLExt/LeiDoMeioTom.lean` (nome PROVISÓRIO; sha256 `770b881936572cb1ffb46fbe123ba23199751d08322ad563c8d0d240ff874928`; 11 teoremas e 3 definições, trio, 0 sorry; importa a ponte 1): `meioTom = e^(−1/2)`; `Lei` (tônica `E_pent`); `E0_determined_by_the_tonic`; `massa_le_alpha` (m₂ = α·sen45°·E_pent); `tonic_sqrt_e_gives_one`/`one_needs_tonic_sqrt_e` (E₀ = 1 ⟺ E_pent = √e); `octave_is_not_a_whole_number_of_half_tones`; `the_law_closes`.
- Registro `lei_do_meio_tom_v405` [INPUT (a lei e o tom) + REAL (termos) + OPEN (a tônica em eV)]: a tônica √e eV reproduz a previsão corrente (8,507 meV); a tônica segue a derivar do hamiltoniano oculto; nenhuma tônica escolhida pelo dado. O `AcordeE0.lean` do Kimi fica citado (mesma estrutura, r genérico).
- O registro `e0_scale_open_v405` passa a dizer: o no-go vale no formalismo SEM a lei; COM a lei (r pinado) a escala fica reduzida à tônica.

## O que NÃO entra
- Nenhum valor de E_pent escolhido pelo dado (nem 5/3 eV, nem 1,666 eV); o veredito do rito não se move.

## Pendências do operador
- O NOME desta pedra (e das anteriores); a tônica da pêntada — ou a instrução de como derivá-la do hamiltoniano oculto (Ĥ_Ψ do Tratado §3, ξ = β): que regulador, que unidade.

## AO LADO (31/10/2026, 17:40) — r2: a fórmula da massa; o Um posto é o 1 de 1 eV; α é a magnitude (cauda) da inscrição no bulk
**Cunhagem do operador (sha256 `9445171a763afcfc`):** «acabamos de descobrir a fórmula da massa. Então o meu um absoluto é o um de 1 eV e a constante da estrutura fina é a magnitude (cauda) dessa INSCRIÇÃO no bulk». **r2 de `LeiDoMeioTom`** (sha256 `765ac8e2d94ea69fcdd7908adce649e2d8f2686fa91f60e77ced8ce069a3b60c`; 14 teoremas, 3 definições, trio, 0 sorry; `saida_lean_lei_r2.txt` `53a20bd0781c703b`): `beta_eq_alpha_mul_sqrt_e` (β = α·e^(1/2)); **`the_mass_formula`**: m₂ = U·α·e^(1/2)·sen45° — o Um posto U, a magnitude α, o volume √e, a projeção transversal; `the_mass_formula_at_the_posted_one`: em U = 1, m₂ = β·sen45° (a forma da v404, agora derivada). Em runtime (α CODATA 2018; U = 1 eV posto): 8.5074 meV — o MESMO número; o teste é o mesmo; o veredito não se move. A unidade é POSTA pelo operador (rota (a) do adendo 2); «α é a cauda» é leitura [ONTO] sobre `Verdade.alpha_is_measured_from_within`. Registro proposto na v405: `formula_da_massa_v405` [POSTO (o Um = 1 eV) + INPUT (α CODATA) + REAL (termos) + ONTO (os nomes)], com a frase do artigo a ratificar: «a TGL tem dois dados de fora, α medido e o Um posto em 1 eV; o resto da massa do neutrino é teorema». O recibo R1 fica; o R2 é `RECIBO_PEDRA_LEI_DO_MEIO_TOM_31out_R2.json`. <!-- formula_da_massa_um_posto_1eV_31out -->
