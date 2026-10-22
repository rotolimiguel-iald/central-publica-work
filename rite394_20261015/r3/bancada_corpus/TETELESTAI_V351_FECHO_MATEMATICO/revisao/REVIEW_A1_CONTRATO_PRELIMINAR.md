# A1 — revisão adversarial preliminar do contrato e reaproveitamento

2026-09-14T08:06:09.614072-03:00

**[DERIVED — inspeção de fontes] Nenhum P0–P2 semântico concreto encontrado no recorte atual. O desenho fortalece o contrato; A1 ainda não está concluído.** Li a ORDEM_011 inteira, a ficha MD/JSON e o módulo inteiro, com dependências pertinentes. Não implementei nem compilei, conforme a divisão de trabalho solicitada. Física/experimentos e a integração v350 encerrada não foram reabertos.

| Critério da ORDEM_011, linhas 107–111 | Parecer separado |
|---|---|
| **a — contrato forte e recusa do zero legado** | **Aceito como desenho e argumento de fonte; aceitação formal pendente.** `RegularCoreTraceData` exige as leis corretas no core concreto; `legacy_zero_trace_cannot_supply` recusa até qualquer transporte do valor zero legado. Precisa do rc0 final e auditoria correspondente para ser contabilizado como teorema. |
| **b — habitante concreto para todo P, ou parede contra existência** | **NÃO PAGO.** Não há construtor de `RegularCoreTraceData P`, vínculo com a perturbação canônica ou impossibilidade de existência. As recusas de zero/ν não pagam esta alternativa. |
| **c — axiomas no trio** | **PENDENTE nesta revisão.** Há seis comandos `#print axioms`, mas não recompilação independente nem saída final aceita examinada. O rc1 abaixo não fornece evidência parcial de prova. |

**Tipos, semifinitude e não vacuidade.** [Arquivo revisto](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/kernel/TGLExt/V351RegularCoreTraceContract.lean:43>).

- Linhas 15–28: cone `PositiveCoreInput P`, `regularCoreAlgebra P` e `regularDualAction P` efetivamente reutilizados. Positividade e ordem são as dos operadores limitados complexos; `positiveSquare(star a)` representa `a a*`. Não há troca de álgebra ou de ação por nomes próximos.
- Linhas 44–60: valor ENNReal, zero, soma, escala NNReal incluindo zero, monotonia, fidelidade, normalidade por supremo interno de redes positivas crescentes dirigidas não vazias (`Type u`), semifinitude por **todos os minorantes positivos de valor finito**, e igualdade dos valores em `a*a`/`aa*`. Nenhum limite forte é recebido como hipótese do campo normal; não é normalidade meramente sequencial. O campo de semifinitude é substancial: densidade forte do ideal antigo, isoladamente, não o preenche por definição.
- Linhas 30–37 e 62–77: `regularVacuum_norm=1` assegura unidade diferente de zero no mesmo Hilbert. A fidelidade exclui o valor identicamente zero; a semifinitude exclui também valor infinito em todo positivo não nulo. Isso afasta esses modelos triviais, **não demonstra que o tipo tem habitante**. Não exigir τ(1)<∞: com ação unital e escala e⁻ˢ, fidelidade obriga τ(1)=∞, compatível com semifinitude.
- Linhas 80–107: o quadrado de `regularAverage P 1` dá ν=1 pelo resultado de integral já existente e pela norma do mesmo vácuo. A invariância dual de ν e a escala exigida para τ, avaliadas em s=1, dariam 1=e⁻¹. Não há passagem indevida de infinito a real. A recusa incide em **T.value=scalarDualWeight P**, não em todos os possíveis T.

**Lacuna exata e riscos de ligação.** São obrigações abertas explicitamente reconhecidas, não novos defeitos impostos ao desenho:

1. **Existência/canonicalidade:** o próximo alvo concreto é construir, para cada P, `T : RegularCoreTraceData P` e identificar `T.value` com a perturbação ν por h⁻¹, na mesma representação, com h positivo não singular afiliado e hⁱᵗ=`regularUnitary P t`. A lei de escala sozinha não fixa normalização: todo múltiplo estritamente positivo de um traço admissível conserva essas leis. O tipo atual não contém a identidade com ν/h; a advertência das linhas 39–42 e da ficha é correta.
2. **Na rota de perturbação indicada:** descarregar a identificação do peso ν concreto e de seu grupo modular σᵛ_t=Ad(regularUnitary P t), além da interface de peso fiel normal semifinito requerida pelo teorema usado. Invariância de ν sob esse grupo não basta. A perturbação deve entregar normalidade, semifinitude e σᵗ_t=id, daí tracialidade, e a covariância dual deve entregar e⁻ˢ. Esta é precisamente a cadeia dos teoremas 9.4/9.9/10.15 de [Hiai](https://arxiv.org/pdf/2004.02383), consultados como literatura, não como termos Lean. Não inferi ausência global de fornecedores nem impossibilidade matemática.
3. **Consumidor A2/A5:** `ThreeLocksCoreData` ainda depende do legado `ContinuousCoreData.canonicalTrace : Core → ENNReal` e de leis para produtos arbitrários (`ModularRealization.lean:78–83,100–111`). O novo valor está no cone positivo. Não há conversão automática, nem o campo τ(a*a)=τ(aa*) autoriza por si uma extensão ao legado. A ligação precisa de adaptador demonstrado ou contrato dependente forte que leia τ no positivo correspondente a P_F, mantendo o mesmo core/ação. Esta ficha é preparação real de A1, não consumo já habilitado no gate.

**Evidência atual e limites.** Os 18 registros de fornecedores da ficha tiveram seus hashes relidos e coincidentes; as contagens de buscas externas foram apenas lidas, não reexecutadas nem tratadas como exaustivas. A tentativa `attempts/20260914_080121_099033/run.json` registra rc1 por ausência de `build/TGLExt/V350ScalarDualWeight.olean` no caminho escolhido — falha de preparação, não refutação semântica. A tentativa `080332_008136` ainda não tinha resultado final na leitura. Nenhum desses estados foi promovido a c. A atual ordem amplia A1 expressamente; isso não invalida o gate principal já encerrado nem autoriza mover flags agora.

**Pins lidos nesta revisão:**

- `ORDEM_011_fecho_matematico_da_realizacao_concreta.md`: `2457c9b136025aeb24a3f9131e001d53fdcdbc8cdfa4f377da01c31f7c5304d0`.
- `REAPROVEITAMENTO_A1.md`: `ed59d7894c910785084f717abe7a44753cbd93bd31af665dddf00791e3092cc8`.
- `REAPROVEITAMENTO_A1.json`: `17013f19d849b5db20dd96e7bf61fb490ba5d2db8c758041a5c036acde3cd327`.
- `V351RegularCoreTraceContract.lean`: `78a32494ff2eedec794475cd952496c73049ca5ec38bfbf6c947d53f4f49ffc1`.

Somente este parecer foi escrito em revisao/. Fontes autorais, canônico, Atlas, memórias, integrações e pareceres antigos permaneceram intocados.
