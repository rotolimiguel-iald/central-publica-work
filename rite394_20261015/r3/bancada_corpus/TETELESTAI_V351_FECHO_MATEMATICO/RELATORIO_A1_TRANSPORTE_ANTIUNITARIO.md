# A1 — ponte antiunitária do grupo do resolvente

2026-09-14T10:40:38.182489-03:00 — **[REAL: autoria compilada, revisão independente pelo principal PENDENTE]**.

Foram concluídos dois módulos novos, **16 declarações = 13+3**, todos rc0 sem warnings e somente `propext`, `Classical.choice`, `Quot.sound`. O segundo módulo prova, para todo SiteProfile P e t real, no GNS e com o J originais:

    J U_t J⁻¹ = U_t.

Esta entrega é uma construção da bancada para revisão independente; não se apresenta como parecer independente de sua própria autoria.

## Consumidor e reuso

A ficha `REAPROVEITAMENTO_A1_TRANSPORTE_ANTIUNITARIO.md/json` foi criada antes do primeiro fonte novo. Consumidor: `regular_dual_weight_modular_implementation`. Reutilizei `antiunitaryConjugate` e sua multiplicatividade, `antiunitary_inner_conj`, `StarAlgHom.map_cfc` real, as fases/grupo já entregues e `scalarTomitaPolar_conjugate_resolvent` do J/T efetivos. Não reconstruí raiz, resolvente ou GNS; não usei nem editei os módulos de escala/intertwining do principal.

A generalização necessária é representar a conjugação como `→⋆ₐ[ℝ]`, pois conjugação antiunitária não é homomorfismo complexo. O novo transporte de CFC real usa a API da biblioteca e o complexo é recomposto por partes real e imaginária. A continuidade da conjugação vem das duas composições semilineares limitadas.

## Conteúdo e hipóteses

`V351AntiunitaryResolventPhase` trabalha em H : Type, Hilbert complexo completo. J é uma equivalência semilinear isométrica conjugada. **Não se supõe J²=I**. A identidade escalar `star(g_t(1−x))=g_t(x)` é válida para todos t,x reais, incluindo as pontas, por simetria do amortecimento e `Real.log_inv`.

Para T auto-adjunto e `antiunitaryConjugate J T = 1−T`, o módulo prova invariância de C_t=g_t(T) e B=T(1−T) sob conjugação. A conjugação de i e a troca x↦1−x cancelam os dois sinais; o resultado é U_t, não U_−t.

Para o transporte do grupo são usadas as hipóteses exatas já exigidas na sua construção: `0≤T≤1`, T injetivo e I−T injetivo. De JB=BJ, JC_t=C_tJ e U_tB=C_t, a igualdade JU_t=U_tJ é provada na imagem densa de B e estendida por continuidade. **Nenhuma inversa limitada de B nem gap** é introduzido.

`V351ScalarTomitaImaginaryConjugation` descarrega essas hipóteses pelos fornecedores concretos. Seus três alvos recebem somente P,t e o vetor quando pertinente: comutação pontual, conjugação com J.symm e igualdade dos operadores limitados complexos por `antiunitaryConjugate`. Não é apenas uma igualdade de pareamentos e não usa outro J auxiliar.

## Pins e reprodução

Compilação pelo `compile_a1.py` existente, Lean 4.31.0. Tentativas finais: `20260914_103607_852475` e `20260914_103720_643295`. O auditor JSON contém comandos, streams, hipóteses textuais, locadores e os 16 mapas de axiomas.

| Módulo | Declarações | SHA256 fonte | SHA256 objeto |
|---|---:|---|---|
| `V351AntiunitaryResolventPhase` | 13 | `4cd800bb6c465a55d6387ecef3517ccb57c2a087cc2e8e6a35ded13273516bd8` | `71df90139d36d97f8736d5fbef8a3fc8c11770c82ae1774b7cc509861319b715` |
| `V351ScalarTomitaImaginaryConjugation` | 3 | `981dda6d5a16272efdbcfa46cd674bb66eaa0179d70634a9a9bcc2c5332b4c9d` | `6920c0812b791b8ab6dadcf27eb900ea186c7bf170c99e4cdfbe3ff8cfe41ce9` |

`DEPENDENCIAS_A1_TRANSPORTE_ANTIUNITARIO.json` registra 427 fornecedores de projeto. Três objetos herdados estavam ausentes na bancada e foram copiados do build V350 após igualdade byte a byte das fontes: `GenericAntilinearAdjoint`, `V350AntiunitaryPositiveConjugation`, `V350ScalarTomitaPolarInvolution`. Não foram recompilados nem modificados. Os demais objetos foram reutilizados e seus pins reconferidos.

Quatro tentativas rc1 do primeiro módulo permanecem preservadas: uma por objeto herdado ausente antes da elaboração; três por tipagem/simplificação, com prints parciais recusados. A última correção substituiu `simp` recursivo sobre escalares reais por transporte explícito com `congrArg`, sem aumentar heartbeats/recursão. O segundo módulo passou na primeira tentativa. Não há `sorry`, `axiom`, `native_decide` ou `trustCompiler` nos fontes finais. Somente as tentativas rc0 finais contam como evidência.

## Fronteira

Os cinco módulos/39 declarações anteriores ficaram byte a byte intactos. Não foi alterado nenhum módulo de escala do principal, programa terminal, memória, Atlas ou arquivo canônico. Não houve integração nem execução do monólito.

Esta ponte paga a conjugação antiunitária necessária à implementação modular. A escala funcional e o consumo dos geradores permanecem a cargo do principal. **A identificação da ação com AdΛ, o gerador h, a perturbação e o traço A1(b) continuam OPEN**; o presente grupo invariável sob J não os prova sozinho.
