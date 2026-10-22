# Fecho dos andares e exponenciais — 09/09/2026

[REAL — compilação e revisão] A segunda folha `FiniteLevelExponentials.lean` passou com **5 teoremas e 1 instância local nomeada, 6 declarações auditadas**, duas execuções Lean com código zero, sem avisos e somente propext, Classical.choice e Quot.sound. A fonte está congelada. O agente raiz leu a folha integralmente e registrou parecer semântico favorável.

[finite_level_norm_closed](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteLevelExponentials.lean:15>) identifica o andar efetivo com a imagem de towerPiLinear. A fonte é um espaço matricial finito-dimensional; a imagem linear também é finito-dimensional e, portanto, fechada em norma. Nenhum fechamento do andar foi assumido como campo de estrutura.

[finite_level_exp_mem](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteLevelExponentials.lean:20>) tem prova independente desse passo topológico: A=towerPi(a) e tower_pi_exp dão exp(A)=towerPi(exp(a)). [finite_level_exp_smul_mem](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteLevelExponentials.lean:26>) inclui multiplicação por escalar complexo.

[finite_level_cocycle_mem](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteLevelExponentials.lean:31>) prova que o produto concreto exp(it(H+V))exp(−itH) pertence ao mesmo andar quando H e V pertencem a ele. Este enunciado de suporte não exige auto-adjunção; unitariedade e a lei torcida são propriedades adicionais construídas nas folhas próprias.

[finite_level_mono](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/FiniteLevelExponentials.lean:40>) prova a inclusão de andares N≤M usando tPush e towerPi_compat. O espectador da folha Hamiltoniana pode assim ser aplicado aos elementos locais efetivos.

## Composição e alcance

[REAL] Esta entrega completa o resultado dos dois arquivos desta pasta: **25 teoremas, 5 definições e 3 instâncias locais nomeadas, 33 declarações auditadas**. Cada fonte foi compilada separadamente com seu importador; são quatro processos Lean aprovados ao todo. Não houve aqui build conjunto dos cociclos XX completos.

O relatório anterior, preservado, descrevia esta segunda folha como em verificação. Esse estado histórico está superado pelo PASS deste adendo. A fonte e o manifesto Hamiltonianos foram novamente conferidos byte a byte e permanecem intactos.

[OPEN — não concluído nesta folha] A construção dos cortes XX, a lei torcida canônica desses cortes, a estimativa uniforme e sua passagem ao limite são composições separadas. Esta folha não assume sua conclusão e não afirma que todo operador do fator pertença a algum andar finito.

## Integridade e reprodução

[Recibo PASS](<C:/IALD/Central de Patentes/Chatgpt/HAMILTONIANO_MODULAR_FINITO_20260909_153743_672430/BUILD_20260909_154352_065864/BUILD_RESULT.json>).

Fonte: 2320 bytes; SHA-256 `3cda71e421551569a26d359b81f137e12745ed61d7494a894e271386a2f0c7b1`.

Builder: `build_finite_modular.py FiniteLevelExponentials`. O builder usa pasta nova por execução e mede fontes/binários diretamente importados antes e depois. Dependências canônicas/Mathlib transitivas usam seus binários existentes; não houve reconstrução integral da árvore.

As escritas desta etapa são arquivos novos na pasta Chatgpt. Nenhum um.py foi executado/importado; originais, Atlas, memórias canônicas, selos e gate permaneceram intocados.
