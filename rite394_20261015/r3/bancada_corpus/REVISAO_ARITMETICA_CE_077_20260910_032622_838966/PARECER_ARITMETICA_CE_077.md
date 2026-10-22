# Revisão independente do controle exterior CE — 077

[REAL — leitura e custódia] Foi lido integralmente o script compute_finite_ce077_run2.py e foi analisado por JSON o recibo completo da execução 02, incluindo suas três bases invariantes e os 420 registros. O script anterior foi comparado byte a byte após a única substituição indicada abaixo. Nenhum deles foi importado ou executado; não houve nova execução SymPy, CAS, Lean ou um.py.

[DERIVED — parecer matemático delimitado] **Não identifiquei erro material no modelo finito, no diferencial exterior, na obtenção dos invariantes ou na interpretação dos ranks registrados.** Esta é uma revisão independente da implementação e de seu recibo. Os ranks são resultados da execução anterior, não uma segunda determinação numérica realizada por este parecer.

## 1. Objetos efetivamente calculados

As dez matrizes são uma base de so(ε), com ε igual a (+++++), (−++++) e (−+++−). O script verifica Xᵀε+εX=0 e a reconstrução exata dos 100 comutadores de pares ordenados. A independência da base segue das dez entradas superiores distintas; a identidade de Jacobi segue do comutador matricial. A isotropia consiste nos seis pares dentro dos índices 0,…,3: so(4) no controle compacto e so(1,3) nos dois controles indefinidos.

O diferencial em [linhas 71–81](<C:/IALD/Central de Patentes/Chatgpt/compute_finite_ce077_run2.py:71>) é dθᵏ=−Σᵢ<ⱼ fᵏᵢⱼ θⁱ∧θʲ. A soma sobre i<j já incorpora a alternativa usual −½Σᵢⱼ; não falta fator ½. O sinal (−1)^posição é o da derivação de grau 1. O produto exterior elimina índices repetidos e ordena pela paridade das inversões. O controle d² nas dez geradoras, junto à implementação como derivação, controla d² na álgebra gerada por elas.

A ação em [linhas 82–90](<C:/IALD/Central de Patentes/Chatgpt/compute_finite_ce077_run2.py:82>) é a coadjunta Lₐθᵏ=−fᵏₐᵢθⁱ. Sua extensão tem grau zero, portanto não usa o sinal (−1)^posição do diferencial. Não há confusão entre essas duas regras.

## 2. Casimir assinado e Lorentz

[DERIVED] O operador que encontra candidatos é C=Σₐ<ᵦ εₐεᵦ Lₐᵦ², proporcional ao Casimir da forma de traço na isotropia. Em assinatura Lorentz não se pode identificar seu núcleo ao núcleo conjunto por positividade.

O script não faz essa inferência: depois de calcular uma base de ker C, testa cada vetor contra os seis Lₐᵦ ([linhas 99–104](<C:/IALD/Central de Patentes/Chatgpt/compute_finite_ce077_run2.py:99>)). Todo invariante pertence automaticamente a ker C; o teste inverso em uma base estabelece a igualdade com o núcleo conjunto. Isso evita aceitar um eventual autovalor Casimir zero em representação não trivial. Não se presume positividade do Casimir indefinido.

A comparação entre assinaturas também tem justificação estrutural: sobre ℂ, uma matriz diagonal de entradas 1 ou i transforma ε na identidade. Sua conjugação preserva a subálgebra dos quatro primeiros índices e induz isomorfismos dos complexos exteriores e ações de isotropia. Ranks e dimensões dos núcleos de matrizes reais finitas não mudam por extensão de escala a ℂ. Os três pares complexificados são (so(5,ℂ),so(4,ℂ)). Isso não é uma média sobre o grupo Lorentz não compacto, nem identifica as formas reais como álgebras reais.

A leitura em termos do grupo refere-se à isotropia conectada. Não foi imposta invariância sob reflexões adicionais de O(1,3); as contrações orientadas da nota principal 077 permanecem permitidas.

## 3. Resultados e normalização

[REAL — recibo existente, sem rerun] Nas três assinaturas:

| Espaço ou mapa finito | Valor |
|---|---:|
| dim (Λ²k*)^h | 0 |
| dim (Λ³k*)^h | 4 |
| dim (Λ⁴k*)^h | 3 |
| rank d: (Λ³k*)^h → Λ⁴k* | 3 |
| dimensão do núcleo desse mapa | 1 |
| rank d: Λ²k* → Λ³k* | 35 |
| rank d: Λ³k* → Λ⁴k* | 84 |

O script constrói separadamente a cúbica de Cartan do bracket, verifica que é não nula, fechada e invariante, e verifica que gera a linha do núcleo restrito.

Precisão de nomenclatura: a variável 'killing' em [linha 114](<C:/IALD/Central de Patentes/Chatgpt/compute_finite_ce077_run2.py:114>) contém **Tr₅(XY)** na representação fundamental. A forma de Killing de so(5) é 3Tr₅(XY). Esse fator não nulo não altera fechamento, invariância, ranks ou a linha cúbica. A cúbica serializada não deve receber a normalização da forma de Killing sem esse fator.

Os ranks integrais são compatíveis com dim H³_CE(k)=120−84−35=1. Já 85=120−35 e 126=210−84 são dimensões de quocientes pelos respectivos espaços de bordos antes de impor todos os próximos ciclos; não são dimensões de H³ e H⁴ completos. A aplicação aos truncamentos BRST exige a redução da nota principal 077, acompanhada de seu adendo de sinais.

## 4. Exatidão e conteúdo do recibo

As matrizes iniciais têm entradas inteiras; a extração das constantes divide somente por εₐ=±1. As operações seguintes usam matrizes e inteiros exatos SymPy. Não há literal de ponto flutuante nem tolerância de rank. A revisão conferiu que as bases serializadas contêm coeficientes racionais exatos e índices exteriores válidos, mediante análise do JSON pela biblioteca padrão, sem reconstruir o cálculo CE.

O recibo declara SymPy 1.14.0 e um pin do próprio script, agora revalidado. Os ranks gravados como constantes no resumo são precedidos por controles explícitos das mesmas igualdades; os flags correspondentes estão todos verdadeiros.

São 140 controles por assinatura: 10 de antissimetria métrica, 100 de brackets, 10 de d² nas geradoras, 7 de invariância conjunta, 3 de dimensões invariantes, 3 do mapa restrito/sobrevivente, 4 da cúbica de Cartan e 3 dos ranks integrais/composição nula. Os 420 nomes são distintos e aparecem na ordem gerada pelo script. São controles do mesmo cálculo, não 420 demonstrações independentes ou testes físicos.

O JSON não exporta todas as matrizes nem certificados de escalonamento de cada rank. Esta auditoria estática não substitui a execução exata original nem é certificado Lean. Verifica a implementação, a consistência do recibo e a custódia das fontes.

## 5. Proveniência e preservação

[REAL] A diferença entre compute_finite_ce077_new.py e compute_finite_ce077_run2.py é exclusivamente a pasta de saída: acrescentou-se '_EXECUCAO_02'. Nenhuma regra algébrica ou verificação foi alterada. O script escreve o novo recibo em pasta nova e lê seus próprios bytes para o pin.

[DECLARADO pela tarefa principal] As tentativas anteriores falharam por dependências/permissões; a execução 02 usou dependências em nova pasta Chatgpt. Não se reconstituiu aqui o histórico de processos nem se auditou o conteúdo dos pacotes. Uma busca de nomes encontrou bloqueios de leitura em subpastas de dependências; elas não são necessárias para este parecer. A versão de biblioteca acima é a reportada na execução, não uma importação nova.

[REAL — esta revisão] Os cinco arquivos pinados no recibo foram relidos e permaneceram idênticos. Nenhum original, fonte congelada, instalação, Atlas ou memória existente foi alterado. Somente este parecer e seu novo recibo foram gravados.

## 6. Limites

O cálculo controla álgebra exterior de dimensão dez e invariantes de isotropia. Não calcula jatos universais, cohomologia de todos os truncamentos, lim¹, admissibilidade causal de contratermos, QME, anomalias do modelo completo ou dados físicos.

Uma transição inicial não sobrejetiva não determina lim¹≠0. A linha de Cartan sobrevivente à primeira transição não é, só por este cálculo, uma classe sobrevivente em toda a completação. O levantamento posterior Pontryagin/C5 não foi lido nem incluído.

**Conclusão: PASS no alcance da revisão estática matemática e documental do controle CE finito, sem nova execução aritmética.**

## Pins medidos

- [compute_finite_ce077_run2.py](<C:/IALD/Central de Patentes/Chatgpt/compute_finite_ce077_run2.py>) — 7177 bytes; SHA-256 639490bdb393ee0703ef886169ef2581d1563e7b5b7b7d6efddf6326681a72cd.
- [compute_finite_ce077_new.py](<C:/IALD/Central de Patentes/Chatgpt/compute_finite_ce077_new.py>) — 7165 bytes; SHA-256 a85e7b61fb0cb0c59239046d0fecce81ad5b0dea42dc01641e7454a5399fc4aa.
- [prepare_finite_ce077_run2.py](<C:/IALD/Central de Patentes/Chatgpt/prepare_finite_ce077_run2.py>) — 810 bytes; SHA-256 25a452e17a1dd2f5db425519e45b875571795357657c259c6ac37ae34df87c4f.
- [RESULTADO_CE_EXATO_077.json](<C:/IALD/Central de Patentes/Chatgpt/ALGEBRA_EXTERIOR_CE_077_20260910_EXECUCAO_02/RESULTADO_CE_EXATO_077.json>) — 66872 bytes; SHA-256 f0d15ce09e893194fa42293323234d4006b63e4cbb1f3fb02c74e78ae73b3555.

A revisão principal dos truncamentos, consumida apenas para delimitar a aplicação ao BRST, está pinada no recibo.
