# Revisão independente — energia ponderada e cota de bloco

WEIGHTED_ENERGY_DEV_REVIEW — PARCIAL DEV14, dois módulos congelados. 2026-09-13T08:00:15-03:00

[REAL] Concluídas leitura integral, exame dos tipos/hipóteses e recompilação própria dos dois módulos, com auditor cumulativo separado de 14 declarações. **Nenhum achado matemático P0–P2.** Há uma ressalva explícita de igualdade binária no primeiro módulo, descrita abaixo. Este parecer encerra apenas DEV14; não certifica outros módulos, integração ou consumo pelo gate.

## Evidência própria e proveniência

- `weighted_energy_independent_20260913_075046_729438`: WeightedVariationalEnergy rc0 em 40.183 s; auditor7 rc0 em 28.83 s.
- `weighted_energy14_independent_20260913_075357_051838`: ProjectionGapLowerBound rc0 em 28.88 s; auditor14 rc0 em 24.594 s. Os 14 tipos/universos foram impressos e lidos; cada fecho transitivo de axiomas contém somente propext, Classical.choice e Quot.sound, coincidindo com os alvos autorais aceitos.
- LEAN_PATH próprio com 337 e 340 dependências de projeto respectivamente, reaproveitadas e pinadas da árvore `paired_blocks27_independent_20260913_070702_176639`; a segunda execução inclui o binário produzido pela primeira. O manifesto guarda a origem imediata e hashes das fontes/binários herdados. Isso não significa recompilação de toda a ancestralidade nesta rodada. Oito diretórios de pacotes externos foram usados somente para leitura, com 14 pares externos diretos pinados. Nenhum build autoral de projeto no LEAN_PATH; nenhuma biblioteca reconstruída.
- Mãe documental lida: paired_blocks_custody.json SHA256 `3b2a02fd49d6aeba2f881714349b1b34995b01969421b9eca64980ce745ba21e`. Preservação de dependências e artefatos readonly registrada nos compilation.json; nenhuma memória ou fonte autoral foi escrita.

| Fonte | SHA256 fonte | SHA256 .olean autor | SHA256 .olean próprio |
|---|---|---|---|
| WeightedVariationalEnergy.lean | `faa59d932b70c36495447232daf4fce44c6c68766931a13ca75b7b143bc489d6` | `595c0a5038ad5afe0242805898ea1a0ed03b077e15f598f62a34b92a9a12614d` | `58f612ac171b5cf6e570769cc6dc5a448accd039a420bfdaa6d79a22f8e6a648` |
| ProjectionGapLowerBound.lean | `faeacebcdbd50fffa3d8f3e4eda1fc3369d201331eef96c05b74dbbd939b7c0e` | `0f02a54498ce2cd25e97343e8694a0a95d42e444380cfcd44bf1eeb50f26aa9a` | `0f02a54498ce2cd25e97343e8694a0a95d42e444380cfcd44bf1eeb50f26aa9a` |

Logs autorais aceitos: WeightedVariationalEnergy_20260913_074553_539505.json e ProjectionGapLowerBound_20260913_075000_423719.json. Seus hashes de log/stdout/stderr estão nos manifests próprios. Foram preservadas e excluídas as duas tentativas rc1 anteriores do primeiro módulo e a tentativa rc1 do segundo; prints parciais ou com sorryAx não contam como evidência.

**Ressalva binária:** o .olean próprio de WeightedVariationalEnergy não é literalmente igual ao autoral. Ambos contêm o caminho absoluto de sua fonte associado ao warning de hA não utilizado (linha 70); os stdout coincidem após somente substituir esse caminho. O arquivo binary_comparison.json registra comprimentos, hashes, posição do caminho e região igual. Não foi demonstrada equivalência completa de serialização normalizada. A recompilação integral e a importação no auditor passaram rc0. ProjectionGapLowerBound teve igualdade literal de binários. O campo binary_equal_author=true do segundo compilation.json refere-se apenas a esse módulo novo; não apaga a divergência do primeiro.

## Hipóteses e composição conferidas

**WeightedVariationalEnergy.lean, linhas 12–108.** Operadores limitados no mesmo Hilbert complexo completo. A orientação do produto interno e os conjugados são consistentes: Re z=1 e a identidade complexa fornecida dão a energia real. `variationalPair_energy_bound` recebe Y auto-adjunto, Z=L*L e a identidade variacional; não supõe simetria de uma forma B_z, nem precisa positividade de Y para essa desigualdade. A fatoração com sqrt(e) usa e≥0. O último teorema recebe explicitamente eT=Te, AT=TA e Bx=A(Tη); daí obtém a cota com ||T||². A prova não introduz AB=BA. O hA não utilizado na especialização intermediária é hipótese redundante benigna; hA é usado na etapa final. A identidade variacional e sua instanciação concreta não são construídas neste módulo genérico.

**ProjectionGapLowerBound.lean.** e=(I−cA)⁺ é definido pelo CFC; nas identidades e conclusões de ordem relevantes, A auto-adjunto é hipótese explícita. De eB=0, BB*=A(I−A), eA=Ae e injetividade de A, o cancelamento é ponto a ponto, sem dividir por B nem supor AB=BA. Para c≥1, e²=(1−c)e, positividade e a propriedade C* implicam e=0, inclusive c=1. De e=0 e c>0 resulta c⁻¹I≤A por multiplicação escalar não negativa e cancelamento; a implementação não depende da instância PosSMulReflectLE que falhou na tentativa autoral. A última declaração deriva IsStrictlyPositive A da cota já recebida, incluindo a condição IsUnit. Nenhum CompleteSpace de subtipo VNA, PVM, gap prévio ou domínio total de operador não limitado foi presumido.

**Limite determinante:** eB=0 permanece uma premissa honesta do segundo módulo, não resultado deste DEV14. A energia genérica não fornece sozinha esse anulamento nem a cota uniforme para os blocos concretos. São limites de composição, não defeitos dos enunciados revisados. Os resultados não identificam por si sós Δ^it/KMS, a inclusão inversa com J original ou traço. Tampouco esses objetivos adicionais são automaticamente requisitos do gate v350: essa relação deve ser decidida pelos contratos efetivamente consumidos, objeto da auditoria de reutilização separada solicitada depois.

## Alvos auditados

- `TGLV350.Regular.selfAdjoint_inner_im_zero`
- `TGLV350.Regular.realPhaseEnergyIdentity`
- `TGLV350.Regular.variationalPair_energy_bound`
- `TGLV350.Regular.weightedBlock_Y_selfAdjoint`
- `TGLV350.Regular.weightedBlock_root_sandwich`
- `TGLV350.Regular.weightedBlock_phase_energy_bound`
- `TGLV350.Regular.weightedBlock_multiplier_energy_bound`
- `TGLV350.Regular.projectionGapPart_nonneg`
- `TGLV350.Regular.projectionGapPart_commutes`
- `TGLV350.Regular.projectionGapPart_square`
- `TGLV350.Regular.injectiveBlock_complement_zero`
- `TGLV350.Regular.projectionGapPart_eq_zero_of_block_zero`
- `TGLV350.Regular.projectionBlock_lower_bound_of_gap_zero`
- `TGLV350.Regular.projectionBlock_strictPositive_of_lower_bound`

## Artefatos verificáveis

Os diretórios acima, sob revisao/, contêm manifest.json, compilation.json, fontes congeladas, auditores, stdout/stderr e histórico autoral. Em particular: [compilation7](weighted_energy_independent_20260913_075046_729438/compilation.json), [comparação binária](weighted_energy_independent_20260913_075046_729438/binary_comparison.json), [compilation14](weighted_energy14_independent_20260913_075357_051838/compilation.json), [auditor14](weighted_energy14_independent_20260913_075357_051838/sources/WeightedEnergyAudit14.lean). Não houve execução de um.py, integrador, recorder ou testes autorais. Nenhuma integração aprovada por este parecer parcial.
