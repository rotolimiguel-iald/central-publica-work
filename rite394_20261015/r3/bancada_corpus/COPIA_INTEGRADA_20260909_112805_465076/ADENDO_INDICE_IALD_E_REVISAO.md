# Adendo — revisão independente e nome curto no índice IALD

[REAL — leitura estática, 09/09/2026] O crítico independente confirmou: a cópia altera somente _EMBEDDED_KERNEL_FILES; 605 entradas tornam-se 611; seis módulos novos; nenhuma entrada removida; agregadores alterados somente por adição; 100 teoremas distintos e um #print axioms adicional para cada um; flags, gate e sentinelas idênticos. Foram conferidas as fontes e as duas transposições de imports locais. O crítico não executou/importou um.py e não recompilou Lean.

A materialização percorre a tabela inteira; os mecanismos inspecionados não dependem de uma contagem fixa de módulos. Essa leitura estática não substitui uma rodada de runtime.

## Limitação operacional encontrada

Há dois nomes Lean completos distintos:

- ChatgptAudit.Angular034.phaseReading, em TGLExt/AngularAreaObservability.lean.
- ChatgptAudit.SelectionAngle.phaseReading, em TGLExt/SelectionAngleReconstruction.lean.

A função de construção do índice operacional usa o nome curto. No um.py da cópia, as linhas 141922–141923 registram a duplicidade e conservam a primeira entrada por setdefault; a linha 141991 expõe o campo ambiguo. As definições aparecem nas linhas 32657 e 113868.

[DERIVED pela leitura do algoritmo] Ao indexar essas duas entradas, phaseReading terá ambiguidade de nome curto. Não é colisão de declarações em Lean: os nomes completos e tipos permanecem distintos, e os módulos/agregadores compilaram. Para consulta e integração subsequente, usar os nomes completos e preservar o diagnóstico; não presumir que uma leitura de estado na torre seja a fase matricial angular.

A cópia congelada e seus resultados anteriores permanecem intactos. Alterar a resolução de nomes do índice ou renomear símbolos aprovados seria outra modificação, com seus próprios checks. Este adendo registra a limitação em vez de escondê-la.
