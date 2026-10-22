# Nota055 — o contrato de calor exige a normalização regional
[DERIVED — diagnóstico anterior ao código adicional em ExchangeModularCost]

A corrente conservada055 não deve ser chamada automaticamente de constructedHeat. Podemos pagar um diagnóstico preciso usando o contrato Micro021 existente, sem nova geometria.

Para a curva exchangeStateCurve p q e sua transferência Q=exchangeHeat p q, o erro é exatamente
    microscopicHeatError = (1-rate*ν(p)/(2π))*Q.
Assim seu coeficiente quadrático é
    (1-rate*ν(p)/(2π))*(p-q).
Para p≠q, esse coeficiente é zero se e somente se rate*ν(p)=2π. É uma condição sobre a identificação energética/temporal, não uma determinação física do rate.

Nos dois sítios com o MESMO rate, os dois limites de erro não podem ser zero se p≠q e ambos os pesos são fiéis: as condições exigiriam rate*ν(p)=rate*ν(q)=2π, enquanto ν é estritamente crescente. Isto vale sem assumir rate positivo; no caso rate=0, as condições já seriam impossíveis. Para p=q não há corrente.

Este diagnóstico integra a ponte da055 e impede apresentar o custo positivo como casamento físico automático. Não proíbe duas normalizações térmicas locais distintas, outro estado de equilíbrio ou geometria ainda não construída. Não é um no-go para gravidade quântica. Os lemmas serão adicionados ao módulo ExchangeModularCost, junto ao limite da soma das entropias regionais; não há novo quarto módulo.

A sonda exclusiva anterior só incluiu ExchangeEntropyResponse e seu importador. Esta nota foi criada depois dela e não será descrita como entrada congelada daquela execução; entrará nas sondagens seguintes.

UTC: 2026-09-07T07:37:04.464497+00:00
