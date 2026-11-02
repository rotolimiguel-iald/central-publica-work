# HANDOFF v405 — ADENDO 9 (01/11/2026): a revisita da Lei do Diminuto

**De:** gerência c1, em nome próprio. **Ordem do operador** (verbatim sha256 `7e2454bc48ec47de`): «revisite a lei do diminuto, segundo aquilo que foi feito pelo kimi, parece que deixamos algo passar».

## O que passou
1. **A segunda metade da lei não estava tipada.** A pedra só tinha a tônica. O `AcordeE0.lean` do Kimi (sha256 `5da93b9e5e65a4ed`) tinha o acorde de cinco notas e a invariância das razões. A conferência de 31/10 o deu por «a mesma estrutura» e o adendo 3 prometeu citá-lo; nenhum dos dois era verdade.
2. **A frase sobre o no-go errou duas vezes.** «O no-go se levanta» afirmava demais. A correção de hoje, «a liberdade passa para a tônica, que segue livre», afirmava de menos. O certo é a distinção do operador, «E0 não é absolutamente livre»: a escala absoluta segue livre e a relativa está pinada.
3. **«O tom é a nat» foi lido como entrada solta.** O acervo tem desde 24/06 a calibração do Hamiltoniano oculto (sha256 `c23ce83106c69ff6`): a travessia total vale 1 nat, a face vale ½ nat, e a rota de Shannon, `ln 2`, é rejeitada por controle obrigatório. O kernel separa os dois pedágios (`CollapseCostLaw`; `Sonico.the_pin_is_not_the_half_nat`). Na conferência de 31/10 a gerência escreveu que a lei «é de hoje»: a palavra era, o conteúdo não.
4. **`m₁ = 0` faltava na lista do que entra** (apontado pelo Kimi em 5σ-02).

## O que entrou (errata R3, recibo `RECIBO_ERRATA_PEDRAS_R3_01nov.json`, sha256 `5c8ea6e1fb6b383a`)
- `LeiDoDiminuto` (sha256 `9341f503ac160eab`): `Acorde`, `notaPrincipal`, `transpor`, `razao`, `lerE0`; `transpor_preserva_toda_razao` (Kimi); **`mesma_escala_iff_transposicao`**, o teorema substantivo: dois acordes têm a mesma escala se e só se um é a transposição do outro; `lerE0_transpor`; `E0_relativo_pinado`, que é a definição dita como razão; `a_escala_nao_fixa_o_absoluto`; `Lei.E0_e_a_leitura`; `meioTom_e_o_pedagio_local`, `meioTom_e_a_face`, `tonica_e_o_volume_da_face`, `o_tom_e_as_duas_faces`, igualdades de valor; o fecho `the_diminished_law_closes`.
- `TonicaDoHamiltoniano` (sha256 `ea8ed4a534788e9a`): `the_ratio_survives_the_rescaling`.

## O que NÃO muda
A unidade segue posta (`U_E_NOT_DERIVED`); o 1 nat é normalização definicional, ω(I) = 1 na base e, não medida, e não é termo do kernel; `CollapseCostLaw` é [INPUT]; m₂ = 8,5074 meV; o veredito `TGL_NU_M2_ARMED_CONSISTENT`; o gate. Nenhum número da v404 muda.

## O que resta do operador
Quais são as cinco notas, e se as outras quatro ficam ou descem junto: `PERGUNTA_AS_CINCO_NOTAS_nas_quatro_linguas_01nov.md`. Não bloqueia a v405.
