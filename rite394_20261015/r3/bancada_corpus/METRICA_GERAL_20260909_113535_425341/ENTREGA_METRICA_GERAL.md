# Resultado — Einstein a partir da própria métrica

[REAL — compilado em 2026-09-09T14:39:57.078861+00:00] 15 teoremas e 2 definições; 17 relatórios de axiomas, restritos a propext, Classical.choice e Quot.sound. As duas execuções Lean retornaram zero, sem avisos. O recibo completo está em [BUILD_RESULT.json](C:/IALD/Central de Patentes/Chatgpt/METRICA_GERAL_20260909_113535_425341/BUILD_20260909_113901_352028/BUILD_RESULT.json).

**Mudança demonstrada:** o teorema de Einstein em carta pode receber diretamente uma métrica suave lorentziana. Não precisa receber E, D, uma escolha suave de tetrada, gInv ou sua regularidade como dados independentes.

A cadeia deduz:
1. A rigidez do cone nulo dá A=c(x)g.
2. O fator é c(x)=Tr(gInv A)/4; sendo soma finita de produtos, é diferenciável.
3. Conservação e compatibilidade de Levi-Civita tornam c constante no aberto pré-conexo.
4. Bianchi dá a conservação de G(g); a conservação de T permite aplicar o passo anterior a A=G(g)-kT.
5. A própria inversa é construída por g⁻¹=(det g)⁻¹ adj(g), com determinante não nulo derivado da congruência lorentziana e regularidade derivada das entradas de g.
6. O balanço nulo de Ricci implica G(g)+Lambda g=kT, com Lambda constante.

[Teorema com única entrada geométrica g](C:/IALD/Central de Patentes/Chatgpt/METRICA_GERAL_20260909_113535_425341/GeneralMetricEinstein.lean:217) · [Suavidade da inversa construída](C:/IALD/Central de Patentes/Chatgpt/METRICA_GERAL_20260909_113535_425341/GeneralMetricEinstein.lean:196) · [Recuperação do escalar por traço](C:/IALD/Central de Patentes/Chatgpt/METRICA_GERAL_20260909_113535_425341/GeneralMetricEinstein.lean:27).

[INPUT] U aberto pré-conexo; g suave e de assinatura (1,3); T diferenciável, simétrico e conservado para a mesma conexão; k constante; balanço nulo de Ricci para todas as direções nulas. Não se pressupõe a equação de Einstein como hipótese.

[OPEN] Origem de g e T nos mesmos dados selecionados da TGL; realização e regularidade do registro causal/volumétrico; correspondência dinâmica de área/calor e matéria. A compatibilidade entre cartas e a extensão a espaços-tempos globais não foram provadas aqui. O teorema usa Levi-Civita, portanto o setor métrico sem torção; não reivindica fechamento novo do setor de Cartan com torção e spin.

[REAL — revisão independente] A tarefa selected_geometry_design leu os enunciados e o delta da inversa. Confirmou que a congruência é usada apenas pontualmente, sem hipótese oculta de tetrada suave, que não há exigência de invertibilidade fora de U e que o sinal Lambda=-c está correto. Esta é revisão semântica; a compilação foi feita pela bancada autora.

A primeira tentativa falhou por resolução do namespace LorentzByCongruence e sintaxe de continuação de campo. O fracasso está preservado na pasta BUILD_20260909_113548_034702; não é contado como prova. A versão final do presente recibo é a de 12068 bytes, com SHA-256 calculado 2010b6edae79bb2f66f5ace4b764e6179d624e288892d777ca87c618a48eab1f.

Originais intactos; nenhum um.py executado ou importado; gate preservado. As dependências canônicas foram lidas, não reconstruídas integralmente. O status vale para estes enunciados e suas hipóteses.
