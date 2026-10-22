# Parecer independente do cálculo de caracteres080

10/09/2026. Revisor /root/selected_geometry_design. Revisão estática, sem reexecutar cálculo, finalizador, Lean ou um.py. Frente080 separada da entrega079.

**Parecer: favorável no problema finito de representações; nenhum erro material identificado no algoritmo ou na interpretação delimitada.** Li integralmente os dois scripts, o recibo de aritmética, o manifesto e a nota final. O rascunho preservado foi comparado em bytes com a transformação documental explicitada.

O resultado aceito é a identidade de caracteres de Λ³[(1,1)⊕(2,0)⊕(0,2)], usando maiores pesos inteiros 2j, e sua sobreposição com os tipos propostos de Weyl. O cálculo não demonstra Calabi, naturalidade do complexo de jatos, cohomologia BRST ou qualquer conclusão de δ(K).

## 1. Fonte e recibo medidos

[compute_lorentz_characters080.py](<C:/IALD/Central de Patentes/Chatgpt/CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/compute_lorentz_characters080.py>): 8146 bytes, SHA-256 87a408520afc38f69107e44cd1d9df4160c24b6a8de50ad4303eb446eb1cb55b.

[CARACTER_EXATO_LAMBDA3_WG_080.json](<C:/IALD/Central de Patentes/Chatgpt/CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/CARACTER_EXATO_LAMBDA3_WG_080.json>): 8932 bytes, SHA-256 308044df30a582fd4940a41df828b8bc9a44a69d742b4f01e2686ca179356ef7.

[DECOMPOSICAO_EXATA_LAMBDA3_E_TORRES_WEYL.md](<C:/IALD/Central de Patentes/Chatgpt/CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/DECOMPOSICAO_EXATA_LAMBDA3_E_TORRES_WEYL.md>): 7594 bytes, SHA-256 e4eb9f3aca95e4c3d988c7f55254fe61645fe39fe74b0d80422009d779d85bde.

Os seis arquivos presentes foram medidos antes/depois. Conferi os pins do manifesto e do próprio recibo, os nomes das chamadas estáticas de controles e as linhas efetivamente registradas no JSON. Há **15 controles aritméticos históricos**, todos marcados PASS no recibo. Minha auditoria não é uma segunda execução deles; suas verificações documentais têm contagem própria no registro anexo.

## 2. Entrada e enumeração exterior

irrep_character(a,b) forma o produto dos pesos a,a−2,…,−a com b,b−2,…,−b, multiplicidade um. Para as três entradas, a base tem dez vetores. Os dois vetores de peso(0,0) são mantidos como duas posições distintas na lista. A etapa combinations(range(len(basis_weights)),3) escolhe índices, não valores de peso: portanto não apaga multiplicidades e não inclui duas vezes o mesmo vetor. As somas de pesos são acumuladas somente após a escolha exterior.

Isso é precisamente a base de Λ³ de um espaço de dez vetores próprios de peso. O número de escolhas é binom(10,3)=120. Não há necessidade de sinal de permutação no caráter: a escolha crescente de índices já fixa uma base exterior, e cada vetor dessa base contribui positivamente com seu peso.

A proposta manual só é lida como um Counter de comparação DEPOIS da enumeração e da decomposição. Ela não é usada para preencher, truncar ou corrigir o resultado obtido.

## 3. Newton e aritmética exata

A identidade usada é
6χ_Λ³ = χ³ − 3χ ψ₂χ + 2ψ₃χ.
Conferi sua contagem por índices: os três índices distintos aparecem seis vezes; a configuração com exatamente dois iguais tem três ocorrências em χ³ e uma em χψ₂χ, cancelada pelo fator três; a configuração com todos iguais tem coeficiente1−3+2=0.

convolve multiplica os inteiros de multiplicidade e soma seus pesos. ψ₂ e ψ₃ multiplicam ambos os pesos por dois ou três; essas aplicações são injetivas no reticulado, de modo que a construção por dicionário não funde chaves diferentes. O suporte usado é a união dos três termos, incluindo pesos cujo resultado se anula. A divisão por seis só ocorre após testar divisibilidade em cada coeficiente. Todos os números são inteiros Python, sem arredondamento ou overflow de inteiros fixos.

A comparação com a enumeração confronta o caráter inteiro como Counter, não somente sua dimensão. As implementações compartilham a mesma entrada e são dois cálculos algébricos distintos; não se deve descrevê-las como observações estatísticas independentes.

## 4. Extração lexicográfica e reconstrução

O peso lexicograficamente máximo de um caráter de representação finita é anulado pelos dois operadores de levantamento de sl2×sl2: subir em qualquer uma das coordenadas produziria um peso lexicograficamente maior. Em uma representação completamente redutível, esse espaço fornece as cópias da representação do maior peso correspondente.

A implementação exige dominância e multiplicidade positiva, subtrai o caráter retangular completo, rejeita restos negativos e remove entradas zero. A dimensão restante cai em cada etapa não vazia. Isso fundamenta a terminação e evita obter uma decomposição virtual disfarçada de positiva.

A reconstrução soma os caracteres irredutíveis obtidos e compara todos os pesos com o caráter exterior inicial. Os maiores pesos tornam esses caracteres linearmente independentes. A soma das contribuições dimensionais do recibo é120; as reflexões dos dois fatores e a troca quiral são controles adicionais, não substitutos da reconstrução.

O recibo lista dez tipos, na convenção de maiores pesos:
(4,0),(0,4),(2,0),(0,2),4(0,0),4(2,2),(3,3),2(3,1),2(1,3),4(1,1).
Essa lista concorda com a expansão exterior manual conferida na revisão matemática da fonte de geração080. Aqui ela permanece uma identidade representacional.

## 5. Por que o controle cobre todo r

O maior peso em cada coordenada do caráter exterior é4. Qualquer ocorrência de um irredutível exige que seu maior peso esteja no caráter, com multiplicidade positiva. Para r≥1, (4+r,r) tem primeira coordenada pelo menos5; (r,4+r) tem segunda coordenada pelo menos5. Logo nenhum deles pode aparecer.

O laço do script percorre apenas o intervalo não excluído pela cota; neste caso, r=0. A conclusão para todos os demais r é a desigualdade acima, escrita no recibo e na nota, e não uma alegação baseada em testar algumas ordens. Em r=0, o recibo fornece multiplicidade um para cada tipo quiral complexo.

Isso pode ser interpretado como a dimensão do espaço de emparelhamentos invariantes desses tipos com Λ³Wg, pois as representações finitas de sl2 são autoduais. A identificação de uma torre de jatos físicos com tais tipos não é demonstrada pelo script. A estrutura real Lorentziana também não é substituída por dois campos reais independentes apenas porque a complexificação possui dois tipos.

## 6. Escrita, histórico e escopo

O script aritmético importa apenas biblioteca padrão. Não lê/importa um.py ou fontes físicas, e restringe o diretório de saída à pasta filha de Chatgpt esperada. Sua escrita usa arquivo novo exclusivo, verifica os bytes e renomeia; rejeita saída ou temporário já existentes. O pin do script é medido antes/depois e é reencontrado no recibo.

O finalizador documental não recalcula os caracteres. Ele confere o recibo e seus pins, substitui um trecho do rascunho por dez fatores completos do produto exterior e escreve arquivos novos. Comparei estaticamente essa substituição: a nota final é exatamente a transformação documentada. O .pending continua presente, com seu pin original, identificado como rascunho histórico; não há resolução por nome aproximado ou substituição silenciosa de documento.

Limites preservados:
- os15 controles são os da execução histórica registrada; nenhuma nova execução foi feita nesta revisão;
- a aritmética inteira não é compilação Lean ou prova de cohomologia;
- Calabi, eliminação de Ricci, todos os jatos, naturalidade e coeficientes herdados dependem da demonstração separada080;
- δ(K), E5, QME, admissibilidade causal e UV não são resultados do cálculo finito.

**Conclusão:** o algoritmo calcula o caráter que declara calcular e seu recibo está coerente com a fonte lida. Não identifiquei erro material ou necessidade de errata no alcance representacional.
