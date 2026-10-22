# Revisão independente da redução topológica e de graus

09/09/2026, continuidade070. [DERIVED — revisão escrita da raiz]. Foi lida integralmente a nota `TOPOLOGIA_BRST_SIGMA_070_20260909_233042_647697/TOPOLOGIA_ALVO_E_REDUCAO_H1.md`. Não encontrei erro material nos resultados delimitados abaixo. Os pins serão medidos no manifesto da entrega. Não houve execução CAS ou Lean.

## Corrente, alvo e primitiva mista

A normalização do volume corresponde a dividir a forma de volume unitária de S³ por 2π². O fator 1/3! compensa as permutações dos três diferenciais. A integral é 1 com a orientação indicada. Pullback comuta com a derivada exterior, portanto a corrente é fechada sem equações de movimento. O diferencial total d+s aplicado ao pullback total reproduz a descida de graus (0,3),(1,2),(2,1),(3,0), sem componente (1,4).

No alvo redondo compacto, para uma 2-forma fechada Omega2, d delta G Omega2=Omega2 porque a parte harmônica é zero e dG Omega2=Gd Omega2=0. A mesma conta vale para a 3-forma após subtrair sua média. O Green de Hodge age numa função/tensor prescrito do alvo, não em configurações sobre o espaço-tempo. Isso preserva localidade em jatos de phi para h fixo, mas não prova uma regra universal local para toda métrica de alvo variável. Esse limite foi mantido.

Com Dq3=P4 e Dalpha1=Omega2, D(alpha1 q3)=Omega2q3−alpha1P4. O segundo termo tem cinco direções horizontais generalizadas em dimensão quatro e se anula. O argumento requer que a curvatura generalizada seja a horizontal usada na álgebra BRST, e não uma matriz de ghost-curvatura arbitrária com componentes verticais independentes. A nota assume e explicita essa apresentação. A componente de forma4/ghost1 é a variação de um contratermo de forma4/ghost0 modulo d. Seu termo Chern–Simons não foi promovido a uma primitiva estritamente invariante na classe de C0.

## Redução finita do setor de ghost5

A contagem CE é consistente: so(1,3)_C=sl2⊕sl2, e os graus disponíveis são0,3,6. O grau3 tem dois representantes independentes. Em ghost5 com no máximo quatro ghosts de translação, somente o nível2 pode sobreviver à redução de s0. Sua equação seguinte fornece fechamento fraco das duas 2-formas coeficientes. É precisamente aí que entra H²_char,cov=0.

Se B2≈DA1, a diferença B2−DA1 é δ-exata pelo contrato KT. A primitiva usada para remover o nível2 tem uma parte A1 theta3 de nível1 e ghost4, mais uma parte de antifield de nível2 e ghost4. A primeira é s0-fechada; sua variação s1 cancela o termo desejado. As contribuições de s2, inclusive as provenientes da variação de theta3, têm nível superior. Assim a subtração não introduz um nível inferior não controlado. Nos níveis3 e4, CE² e CE¹ são zero. A indução termina porque não há quinto ghost de translação independente.

O argumento em ghost2 também confere: apenas nível2×CE0 poderia sobreviver, e seu coeficiente é removido pelo mesmo contrato característico. Não há dependência escondida da independência das classes características de grau4. C0 continua um resultado útil, mas não é a hipótese que falta a esse argumento específico de ghost5.

## Coeficientes suaves, colagem e limites

Na etapa de Lie, cada expressão envolve finitos tipos tensoriais; funções dos valores do alvo são coeficientes Lorentz-escalares. A operação em um módulo tensorial finito pode ser aplicada deixando esses coeficientes intactos. Isso justifica essa etapa algébrica para C∞(U), sem um argumento inválido para toda representação infinita.

A partição de unidade comuta com s0, mas não com s1 ou d. A fórmula exibida para s rho_i e d rho_i mostra por que a colagem KT não paga automaticamente a colagem de primitivas relativas. A média sobre SO(4) ou O(4) também exige primitivas globais já existentes. Essas condições foram conservadas na nota.

A cohomologia de de Rham do produto dos espaços de valores não tem grau5; a nota não identifica por isso todo o complexo BRST com esse produto. A corrente do alvo de grau3 e as classes de vielbein de grau3 precisariam de um fator de grau2 para essa contribuição. A ausência desse fator no setor dinâmico ainda passa pelo contrato H²_char,cov. O exemplo discreto em categoria spin foi citado apenas para limitar uma inferência global, sem lhe atribuir presença no modelo bosônico em análise.

**Conclusão da revisão:** a nota fornece uma redução condicional finita e resultados explícitos sobre o alvo. Não prova ainda o contrato relativo de grau2, a descida/globalização completa na classe de Q2 ou a QME interagente. A distinção entre esses resultados e uma prova irrestrita de ausência de anomalias permanece correta.
