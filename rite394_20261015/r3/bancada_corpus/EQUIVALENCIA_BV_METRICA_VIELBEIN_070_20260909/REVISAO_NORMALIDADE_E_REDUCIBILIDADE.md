# Revisão independente: normalidade, transporte em Lambda e reducibilidade

09/09/2026, continuidade070. [DERIVED — revisão escrita da raiz]. Li integralmente `NORMALIDADE_RELATIVA_070_20260909_233414/NORMALIDADE_FORMAL_E_RESIDUO_SUAVE.md` e conferi os locadores primários dos resultados de normalidade e cohomologia relativa. Não identifiquei erro material no alcance declarado. Este parecer não altera a fonte nem executa CAS ou Lean.

## 1. Filtragem e formalidade

O peso K=N_derivadas+2N_antifields_campos+3N_antifields_ghosts confere para a ação de duas derivadas: δ0 troca um antifield de campo de peso2 por uma equação com duas derivadas; troca C* de peso3 por uma combinação de derivadas de antifields de campos ou de um primeiro jato vezes um antifield. Coeficientes g⁻¹,h(y) têm peso zero. Derivá-los aumenta o peso em um, inclusive quando h é apenas suave. A contribuição cosmológica em δg* tem peso zero e, portanto, δ_-2 realmente reduz K em dois.

No lema relativo, ao escolher N como o maior peso de a, componentes de b com peso superior a N−1 têm d_H b=0 separadamente e podem ser descartadas sem modificar a condição de ciclo. A redução por δΛ c_N+d_H e_(N−1) elimina o peso N e gera apenas o novo resto cosmológico de peso N−2. Os demais pesos presentes continuam limitados. A indução é finita em K; não exige convergência ou especialização de uma série em Lambda.

A afirmação é condicional à existência da primitiva de base na mesma classe. A seção5 a fornece na completação formal indicada, recorrendo ao quadrático Pauli–Fierz/Klein–Gordon e ao critério de normalidade. A seção8 mantém aberta a passagem para coeficientes suaves na carta inteira. Essa distinção é necessária: o controle de derivadas por K não limita o número de potências dos valores não diferenciados.

O resultado para Lambda fixo usa polinômios nos derivados com K limitado. Não se deve alargar essa álgebra a séries irrestritas em todos os jatos em torno de dados fora das equações. Tal ampliação poderia tornar invertível uma equação com termo constante não nulo e trivializar artificialmente seu ideal. O transporte finito da nota não faz essa ampliação: os jatos diferenciados continuam variáveis polinomiais, inclusive ao impor a relação Ric=Lambda g+sW.

[KNOWN — verificado] BBH1994 §10, página31, inclui expressamente Einstein com e sem constante cosmológica; Teorema10.1 admite séries nos valores não diferenciados e polinômios nos derivados. BBH2000 Teorema6.6 e o fim da prova6.7 usam a eliminação de M2 que a nota identifica. A errata sobre Lambda é fundamentada; os artigos não fornecem, por essa frase, convergência suave das primitivas de matéria.

## 2. Prova pelos quatro covetores

Se Lie_v g e v·dy são fracamente nulos como identidades prolongadas, qualquer escalar natural derivado de g,y tem variação fracamente nula. Em particular Lie_v Q=v·dQ. A possível dependência de v em jatos não altera a identidade de naturalidade para o prolongamento evolutivo da transformação; as derivadas de v já aparecem nas variações de g e dy e se cancelam na transformação escalar.

O jato exibido satisfaz as simetrias e a equação sigma: B01^1=B10^1=b é fora da diagonal, portanto seu traço Lorentz é zero. Com u_i^A=delta_i^A e u_0=0,

    ∂0 Q = 2 g11 B01^1 u1^1 = −2b,
    ∂i Q = 0.

Os três diferenciais dy são independentes nas direções espaciais. Juntos com dQ, formam a base indicada. Einstein determina Ricci por esses primeiros jatos, mas não proíbe esse Hessiano sigma sem traço. A sobrejetividade das prolongações estacionárias de069 é a entrada necessária para passar do jato de ordem2 aos jatos de ordem suficiente para v.

Para cada valor do alvo, o determinante não é o polinômio zero nos parâmetros estacionários livres. Seu conjunto não nulo é denso. Uma expressão suave v anulada nesse conjunto se anula em toda a fibra; isso permanece verdadeiro se v envolver jatos de ordem maior, pois o determinante depende só dos inferiores e os demais parâmetros livres permanecem independentes. Na álgebra formal de valores sobre um corpo, os mesmos parâmetros diferenciados são polinomiais e o determinante não nulo não é divisor de zero.

O argumento prova anulação de v; não produz uma primitiva usando o inverso do determinante. A distinção importa: localizar um complexo por esse determinante e provar exatidão apenas na região não degenerada não provaria, por densidade, a existência global de primitivas regulares. A nota limita o uso da densidade corretamente à função v.

## 3. O resíduo M2 permanece real

A representação a2=C* f+M2 e o uso da KT para retirar f≈0 são consistentes com a prova primária. Mesmo depois disso, δM2+d b=0 só fornece um ciclo relativo. A aciclicidade ordinária de δ não autoriza substituir essa equação por δM2=0 nem descartar o termo d b.

A nota paga M2 na completação formal por normalidade e o transporte em K. Na classe suave natural, conserva exatamente a necessidade de uma primitiva relativa regular e sua covariantização. O argumento de quatro covetores não foi promovido a ausência de todas as anomalias. A homotopia radial para formas do alvo remove somente o setor de pullbacks fechado localmente; não resolve por analogia o setor dinâmico dependente das EOM.

**Resultado aceito:** transporte finito em Lambda com hipótese de base explícita; normalidade e H4_2 relativo no espaço formal declarado; ausência de reducibilidade universal na classe suave especificada; delimitação correta do contrato relativo/covariante ainda aberto. A classificação completa de H^(1,4)(s|d), a QME satisfeita e o controle UV continuam distintos.
