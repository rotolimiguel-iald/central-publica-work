# Registro angular: fase, peso e rótulo

[REAL — bancada compilada em 09/09/2026] O registro agora retém o conteúdo necessário para reconstruir uma forma angular admissível e distinguir o ramo referido. Nenhum arquivo canônico foi alterado ou executado.

## Resultado demonstrado

`AngularOccurrence = AngularForm × Fin 2`, com `AngularForm = {A // ∃ θ, A = angFamily θ}`. A fase periódica identifica a forma; não se exige um representante real único de θ.

`WeightedPhaseRecord` contém `weight : ℝ`, `phase : ℂ` e `outcome : Fin 2`. A codificação lê a fase da face selecionada, o peso de reflexão da forma e o rótulo fornecido. O decodificador recupera `(angularDecoder phase, outcome)`.

O teorema `decode_encode_occurrence` prova a identidade exata:
`decodeRecord (encodeOccurrence x) = (x.1.val, x.2)`.

Foram demonstradas também a injetividade de `encodeOccurrence`, a admissibilidade da forma decodificada e a identidade de retorno do registro na imagem admissível. Campos arbitrários de um registro não são promovidos automaticamente a um registro admissível.

## Ligação canônica e controle justo

Para `0 ≤ p ≤ 1`, `selectionRecord p outcome` coincide com o registro efetivamente lido de `Smat (selectionAngle p)`, preserva o peso de reflexão e reconstrói essa matriz com seu rótulo.

Os dois ramos justos da `plusDensity` têm peso 1/2, mesma fase angular e ângulo π/4, mas `fairRecord 0 ≠ fairRecord 1`; seus `recordReadout` são distintos. Os teoremas ligam o peso registrado a `branchWeight plusDensity outcome` e reconstroem tanto `unnormalizedBranch` quanto o readout normalizado.

A ponte geral `recordMatchesBranch A r` exige explicitamente `branchWeight A r.outcome = (r.weight : ℂ)`. Dela seguem reconstrução do ramo não normalizado, normalização para peso não nulo e ramo zero para peso zero. Não há normalização silenciosa de um ramo impossível.

## Alcance e integração

[DERIVED no domínio formal] O lastro suficiente aqui é o registro admissível completo. Sua fase e seu rótulo estão retidos no registro; não foram extraídos de uma saída que já os descartou. A matriz angular e a matriz-densidade de entrada são objetos diferentes.

`angular_record_exactness_does_not_invert_reduction` reúne a injetividade da codificação admissível com o teorema canônico de que `qubitReduction` não admite inversa à esquerda. A reconstrução da forma e do ramo é compatível com a irreversibilidade da redução.

[OPEN] Esta extensão não amostra uma ocorrência na natureza, não fornece proveniência experimental do registro, não prova pagamento físico de custo e não constrói a geometria gravitacional geral. Essas conclusões exigem suas respectivas ligações, não a mudança de nome do registro.

A integração numa COPIA do um.py está especificada em `INTEGRACAO_REGISTRO.json`: dois módulos, transposição de um import local, declarações completas e auditoria. A base SelectionAngleReconstruction foi copiada byte a byte da entrega anterior; sete teoremas já existentes foram recompilados junto da extensão.

## Verificação e custódia da bancada

Resultado: `PASS_COMPILED_SCOPE`. Extensão nova: 24 teoremas; base anterior: 7. Total compilado: 31 teoremas, 13 outras declarações, 44 relatórios de axiomas; todos contidos em propext, Classical.choice e Quot.sound. Três compilações retornaram zero, inclusive o agregador, sem mensagens extras. As dependências diretas fontes/binários foram comparadas por hash antes/depois e permaneceram iguais. Dependências transitivas não foram reconstruídas nem integralmente auditadas nesta bancada.

A primeira compilação teve um erro de inferência de tipo de produto. Foi preservada no BUILD_20260909_110319_912008; a fonte anterior foi copiada em backup binário antes da correção. A rodada válida é BUILD_20260909_110512_454553. O relatório não confunde a rodada falha com a válida.
