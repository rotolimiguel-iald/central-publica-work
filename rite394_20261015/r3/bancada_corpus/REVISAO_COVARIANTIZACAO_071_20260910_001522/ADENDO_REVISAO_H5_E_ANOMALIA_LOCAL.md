# Inspeção adicional do corolário H⁵ e da anomalia local

10/09/2026, arco 071. [DERIVED — análise matemática própria]. Este adendo examina `COROLARIO_H5_E_ANOMALIA_LOCAL.md`, na mesma pasta da fonte revisada pelo parecer principal. Os pins medidos constam do manifesto desta revisão. Nenhuma nota congelada foi modificada, nem foi executado CAS, Lean ou um.py.

**Resultado:** não identifiquei erro material nos três passos examinados. O resultado de anomalia é na álgebra completa suave em vielbein, com as primitivas permitidas por essa álgebra. O texto não o promove ao espaço Q2 ou à construção da QME.

## 1. Grau cinco no fator covariante

Após KT positiva, o primeiro estágio deixa apenas representantes de antifield zero. A cohomologia de Lorentz nos módulos tensoriais finitos tem graus 0, 3 e 6. Como há quatro ξ, ghost total cinco admite somente o par (grau ξ, grau CE)=(2,3). Os outros dois pares candidatos, (5,0) e (−1,6), estão ausentes. O diferencial seguinte exige a classe horizontal fraca covariante de grau dois do coeficiente b₂; a nota principal elimina exatamente essa classe.

Portanto o termo E₂ de grau total cinco é zero. A filtração por ξ tem cinco níveis, de 0 a 4, e não há questão de convergência infinita. Uma primitiva de ghost quatro tem teto antigh seis no fator B, pelo mesmo argumento de dez ghosts do parecer principal. A afirmação do corolário de que um elemento de ghost cinco tem teto cinco também é correta: são graus de elementos diferentes.

A classe global de volume de S³ tem grau três. Ela não fornece outro par de grau cinco, porque CE² é zero. Esse teste não substitui a entrada H²_char,cov, que continua sendo consumida explicitamente.

## 2. Dependência suave conjunta e fator dos vielbeins

A decomposição polar fornece uma retração de GL⁺(4,R) em SO(4); a cobertura finita S³×S³→SO(4) fornece, sobre os reais, os graus de de Rham 0, 3 e 6. O mecanismo correspondente para os pares U,V e a topologia dos vielbeins é tratado em [BBH1995, §§4–5](https://arxiv.org/pdf/hep-th/9505173v2). Aqui a extensão aos coeficientes suaves conjuntos é um argumento paramétrico, não uma identificação injustificada de produtos tensoriais algébricos de espaços C∞.

Mais precisamente, a homotopia da retração polar, seguida da homotopia de de Rham em SO(4), dá operadores P e h no fator U,V com d_U h+h d_U=1−P. Eles não atuam em y ou nos geradores de B. Com os sinais graduados do produto, h anticomuta com o diferencial do outro fator; P comuta com ele. Logo essa identidade continua valendo para o diferencial total. A imagem de P é finita nos graus de de Rham citados, com coeficientes suaves em y. Os operadores atuam nos coeficientes de cada um dos finitos monômios de jatos e não introduzem derivadas adicionais de espaço-tempo. Isso justifica o uso paramétrico sem completar os valores do alvo ou os jatos.

No grau total cinco sobrevivem apenas H⁵(B), H²(B) e H⁻¹(B), multiplicados respectivamente pelos graus 0, 3 e 6 do fator GL⁺. As três parcelas são zero pelos resultados indicados. O grau seis não deve ser descartado por exceder a dimensão do espaço-tempo: neste ponto são zeroformas BRST. O corolário corretamente o conserva e usa H⁻¹(B)=0.

## 3. Comparação de formas e limitação de classe

Conferi diretamente a equação (6.15) e a explicação que a acompanha em [BBH1995, §6](https://arxiv.org/pdf/hep-th/9505173v2): a comparação do grau de forma máximo usa a presença do gauge de difeomorfismos. No caso ghost um e forma quatro, ela toma o grau BRST cinco, sem parcela constante nesse grau. A carta contrátil de espaço-tempo e o tratamento dos coeficientes externos na descida permanecem hipóteses; isso não é uma cohomologia global em um espaço-tempo arbitrário.

A distinção racional/suave tem controle concreto correto. A restrição de d(det e)/det e à curva diag(t,1,1,1), t>0, é dt/t. Uma derivada racional tem resíduo simples zero, enquanto dt/t tem resíduo um; a primitiva log t existe suavemente nessa componente e não no anel racional. Portanto o cálculo suave do fator GL⁺ não pode ser importado automaticamente ao anel racional localizado. Esta restrição não desfaz o resultado do fator covariante B, onde a primitiva natural foi obtida por outro argumento.

O texto deixa em aberto a comparação com os contratermos admissíveis, sobretudo na presença de fundos externos e de requisitos adicionais de covariância, suporte ou analiticidade. Também separa a exatidão cohomológica de uma anomalia candidata da construção renormalizada que produziria tal anomalia e da remoção indutiva compatível com a QME. São limites efetivos, não apenas uma ressalva terminológica.

**Conclusão delimitada:** a eliminação escrita de H⁵(B), H⁵(A_sm) e H¹,⁴(s|d_H;A_sm) é consistente com as entradas e classes declaradas. Esta revisão não demonstra a compatibilidade Q2, a teoria interagente física, a ausência de anomalias globais ou a completude UV.
