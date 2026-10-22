# Suficiência — primeira transição BRST e levantamento até C5

10/09/2026, entrega077. [DERIVED — matemática escrita revisada] [REAL — álgebra racional finita e integridade documental].

**Esta etapa calculou a primeira perda de classes entre truncagens e construiu o prolongamento da linha sobrevivente até valência cinco.** O trabalho não supõe que passar num corte finito resolva a completação: a sexta ordem e as imagens em todos os cortes continuam sendo obrigações explícitas.

## 1. Estado canônico e procedência

A [captura077](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_077_20260910/ESTADO_CANONICO_077.json>) relê os quatro artefatos canônicos. Seus bytes permanecem iguais aos da076: v338, 683 arquivos embutidos, 77 presentes e 21 ausentes no conjunto acompanhado de 98 módulos. O selo corresponde ao um.py lido. É leitura e análise AST, não execução ou nova compilação Lean.

A076 foi progresso: forneceu ciclos, primitivas e a sequência de comparação por limites. A077 usa esses resultados para calcular mapas concretos. A investigação078 posterior fica fora desta entrega.

## 2. Convenção corrigida e referência usada

O quadrático mínimo S2=½⟨u,H0u⟩+⟨u*,R0c⟩, na convenção efetiva de derivadas direitas, dá

s0u=R0c, s0c=0, s0u*=+H0u, s0c*=+R0†u*.

A nota autoral tinha −H0u; a revisão independente detectou a incompatibilidade e um adendo a corrigiu ao lado. Não se trocou a ação para preservar uma frase incorreta. Os primeiros mapas calculados usam setores sem antifields, por isso suas dimensões não dependem do sinal corrigido. Nas ordens posteriores, o dicionário correto é obrigatório.

O teste é o complexo BV mínimo local sobre g0 de curvatura constante não nula e φ0 constante. B0 é inerte e on-shell; campos dinâmicos continuam off-shell. Não se incluem as fontes externas θ/ω sem a sua filtração própria. Também não se constrói, por esse teste, uma representação Hadamard física na referência simétrica.

[Nota077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/S0_KILLING_E_PRIMEIRA_TRANSICAO.md>) · [Correção KT](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>) · [Revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_PRIMEIROS_TRUNCAMENTOS_077_20260910_031524_472175/PARECER_TRUNCAMENTOS_E_SINAL_077.md>).

## 3. O que os primeiros cortes demonstram

C_N conserva valência E≤N: cada campo, ghost, antifield ou seu jato conta uma perna. Isso NÃO é um corte na ordem de derivadas.

Quocientar os jatos ghosts pelas imagens de s0 dos campos deixa os dez dados de Killing W=V⊕Λ²V, com V Lorentziano de dimensão quatro. Em outra referência, o estabilizador pode ser diferente; ausência de reducibilidade universal não significa ausência de Killing em cada fundo.

No teste com isotropia G=SO⁺(1,3), orientação e coeficientes da referência fixados, temos:

| Objeto | Resultado |
|---|---:|
| dim(Λ²W)^G | 0 |
| dim(Λ³W)^G | 4 |
| dim(Λ⁴W)^G | 3 |
| dim H³(C3) | 4 |
| dim im[H³(C4)→H³(C3)] | 1 |
| H⁴(C4) | 0 |

A condição para levantar uma cúbica até C4 é seu fechamento no diferencial CE da álgebra de Killing. Sua parte no ideal R0c é cancelada por uma correção finita u c³. O núcleo CE natural tem dimensão um.

Os quatro controles cúbicos foram escritos como expressões naturais antes da especialização do fundo. Assim, numa classe universal regular que admite esse teste, não podem todos levantar a C4. A inferência não identifica a cohomologia universal com a fibra e não atribui uma anomalia à teoria.

## 4. Controle exato independente da contagem escrita

Foi construído um cálculo racional das álgebras so(5), so(1,4) e so(2,3), com seus dez geradores matriciais e a isotropia nos quatro primeiros índices. As três assinaturas deram os mesmos números 0/4/3, posto três e núcleo unidimensional no mapa invariante de grau três para quatro. A linha é a da cúbica de Cartan.

O cálculo mede os núcleos e postos por aritmética exata. O Casimir assinado é apenas auxiliar: todos os vetores de seu núcleo são conferidos contra cada gerador da isotropia. Não se presume positividade no caso não compacto.

Os 420 controles incluem representação, comutadores, d², invariantes e ranks; não contam 420 teoremas sobre o BRST completo. Houve uma execução matemática completa. Tentativas anteriores falharam visivelmente por biblioteca ausente ou acesso restrito, sem produzir um resultado de aprovação.

[Resultado exato](<C:/IALD/Central de Patentes/Chatgpt/ALGEBRA_EXTERIOR_CE_077_20260910_EXECUCAO_02/RESULTADO_CE_EXATO_077.json>) · [Escopo e ambiente](<C:/IALD/Central de Patentes/Chatgpt/ALGEBRA_EXTERIOR_CE_077_20260910_EXECUCAO_02/LEITURA_DO_CONTROLE_CE_077.md>).

## 5. A linha que chega até C5

A transgressão076 fornece T=tr(kΩ)−tr(k³)/3 e sT=A_P. Seu transporte métrico mantém o termo sS. A identidade pontual tr(R∧R)=tr(Weyl∧Weyl), demonstrada por Schouten/Bianchi, mostra que a densidade de Pontryagin começa quadraticamente nas perturbações quando Weyl(g0)=0. Somando quatro ghosts, A_P começa em valência pelo menos seis.

A nota constrói explicitamente T≤5=t³α3+t⁴α4+t⁵α5. Como s não diminui valência e sT∈F6, T≤5 é um ciclo em C5. Seu líder é

α3=tr(M Kpp♭)−tr(M³)/3.

Ele é não nulo no primeiro corte. O dicionário de blocos com as matrizes do cálculo exato dá α3=−Cartan, fixando o sinal e a identificação dos objetos. A escala por √|K| é usada apenas nesse controle finito; a fórmula natural original é regular e não divide por K.

Portanto dim im[H³(C5)→H³(C3)]=1 no teste. Não se afirmou dim H³(C5)=1.

[Construção e correções](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/PONTRYAGIN_CE3_E_LEVANTAMENTO_C5.md>) · [Dicionário de Cartan](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/DICIONARIO_CARTAN_DO_RECIBO_077.md>) · [Parecer da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_077_20260910/PARECER_PONTRYAGIN_E_C5_077.md>).

## 6. Sexta ordem, completação e objetivo completo

O primeiro coeficiente possível do resíduo da transgressão inteira é A6=ρ_[2](Weyl_[1]∧Weyl_[1]) C0C1C2C3. Ele é s0-fechado. O resíduo do TRUNCAMENTO é (sT≤5)6=A6−s0α6; não se deve confundir os dois nem declarar obstrução apenas porque um polinômio aparece.

Restam a exatidão admissível desse resíduo, a liberdade de corrigir termos anteriores e o levantamento nas ordens seguintes. As imagens para todos os cortes ainda precisam ser controladas. A falha C4→C3 não implica lim¹≠0. Neste alvo C3 fixo, a dimensão finita garante estabilização eventual das imagens; isso não estabelece a condição para todos os N.

Permanecem os módulos completos e os demais canais do critério074, a primitiva de anomalia e a família de contratermos causais, corrente/carga interagentes e QME. Também continuam a compatibilidade entre referências, estados e cutoffs, a reconstrução gravitacional geral pelos MESMOS dados selecionados e a justificação da rota UV. Fase, ramo, H3 interno e os falsificadores existentes não foram reabertos.

A valência cinco deste levantamento não é o grau total cinco da anomalia. A conta atual é de ghost3 e forma zero; não autoriza a bandeira “anomalia removida”.

## 7. Entrega e preservação

Notas, correções e pareceres devem ser integrados conjuntamente. As dependências matemáticas foram copiadas somente para uma pasta nova em Chatgpt; nenhuma instalação original foi alterada. Todas as escritas desta etapa são novas na bancada. Não houve execução/importação de um.py, compilação Lean, teste de natureza ou mudança de selo/gate. Atlas, índice e memórias canônicas permanecem somente leitura; a memória e o desenho desta etapa são arquivos novos.

Os pareceres documentais e o manifesto final registram a integridade da entrega. Controles documentais, controles racionais finitos e demonstrações escritas têm alcances diferentes. O objetivo completo permanece aberto.
