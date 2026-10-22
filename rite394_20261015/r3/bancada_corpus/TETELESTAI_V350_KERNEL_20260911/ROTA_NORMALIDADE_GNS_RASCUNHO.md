# Normalidade GNS e a próxima obrigação de fechabilidade

[REAL — DEV compilado, ainda não integrado nem revisado independentemente]

Dois módulos novos, ScalarGNSStrongContinuity e ScalarGNSNormality,
contêm sete declarações auditadas. Para a mesma N e o mesmo H_I, a
representação π_I transfere limites fortes de redes com uma cota uniforme
de norma. A prova é a restrição ao subespaço fechado da transferência
ambiente previamente demonstrada; a topologia usada é a norma de H_I.

π_I é positiva e monótona. Para toda rede positiva crescente T_i em N
com supremo B interno a N, a prova constrói o limite forte em N,
identifica-o com B pela unicidade do supremo e transfere a convergência.
Obtém-se que π_I(B) é o supremo de π_I(T_i) em B(H_I), contra todos os
majorantes ambientes. O último teorema reformula o resultado para
qualquer conjunto não vazio dirigido de elementos positivos de N.
Não se pressupõe convergência forte no enunciado de normalidade.

As tentativas falhadas estão nos logs. Incluem aplicação de `map_le_map`
inexistente, inferência inadequada com `map_rel` e uma tentativa de usar
o cálculo funcional contínuo sem conseguir inferir a instância exigida.
A fonte final usa `OrderHomClass.monotone` na representação ambiente,
seguida de restrição por produto interno a H_I. Não houve aumento dos
limites de inferência nem introdução de axioma de positividade.

[OPEN] Isso não prova que o gráfico G={(Λ(A),Λ(A*)): A∈I∩I*}
seja fechável. Ainda falta demonstrar que (0,y)∈fecho(G) força y=0.
A fidelidade do peso, a normalidade da representação e a densidade do
domínio são resultados distintos dessa obrigação. Não se afirmou que
η seja separante para N: o lema local existente sobre η é para a
subálgebra fixa F. O domínio máximo de ν também permanece distinto de I.

[KNOWN — orientação bibliográfica, não importada como axioma Lean]
Masuda, Teorema 3.12 e seu esboço, trata a passagem de pesos normais fiéis
semifinitos a álgebras de Hilbert e destaca a fechabilidade da involução
como etapa própria. Seu argumento remete à aproximação do peso por
funcionais normais positivos dominados. A remissão ao livro citada pelo
autor não foi lida nesta rodada nem convertida em prova do kernel.
[Artigo primário de Masuda, p. 45](https://www.math.okayama-u.ac.jp/mjou/mjou60/_02_Masuda.pdf).

[OPEN — roteiro a testar] Já existem cortes duais limitados e sua exaustão
monótona. Uma via é usá-los para construir aproximações normais limitadas
do peso e os mapas GNS correspondentes, demonstrando a separação de
vetores verticais do gráfico. Outra via exigiria provar explicitamente
um conjunto denso de vetores que testem a adjunta. Nenhuma dessas vias
está encerrada por este documento. Não se presume que uma citação ou
um gráfico inicial injetivo forneça o operador fechado.

Tomita/KMS, gerador e traço canônico com escala dual, as interfaces gerais,
Three Locks/H1–H3, o setor quântico interagente, o certificado consumido
pelo gate e o runtime integral continuam abertos. As fontes originais
permanecem somente leitura. Estes sete alvos não entram no pacote
integrado do domínio inicial de Tomita nem no alcance de seu parecer.
