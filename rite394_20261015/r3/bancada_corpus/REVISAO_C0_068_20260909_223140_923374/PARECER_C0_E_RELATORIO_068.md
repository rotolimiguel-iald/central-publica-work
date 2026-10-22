# Parecer independente delimitado sobre C0 — entrega 068

09/09/2026. [DERIVED — revisão matemática escrita] [REAL — arquivos e hashes lidos]. Revisão interna independente da construção, sem atribuição de aprovação ao operador ou a revisor externo.

**Parecer:** não identifiquei erro material na demonstração de não trivialidade de Euler/Pontryagin modulo o ideal diferencial natural algébrico definido na nota. O relatório 068 conserva esse alcance e a obrigação residual de regularidade/igualdade fraca. Não se conclui a cohomologia completa, ausência geral de anomalias ou QME renormalizada.

## 1. Fontes e escopo

Foram lidos integralmente o [adendo C0](<C:/IALD/Central de Patentes/Chatgpt/CLASSES_CARACTERISTICAS_C0_20260909_221649/EULER_PONTRYAGIN_ON_SHELL_E_LIMITE_C0.md>) e o [relatório 068](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_068_20260909/REEXAME_SUFICIENCIA.md>). Os pins medidos aparecem ao final e no manifesto acompanhante. A revisão do relatório é de consistência com o resultado C0 e com as demonstrações global/BRST que este revisor já examinou; não é uma nova auditoria de todos os recibos canônicos ou dos cálculos EFT.

## 2. Complexificação off-shell

A ordem lógica da prova é válida. Supõe-se um certificado universal finito na classe admissível e fixa-se primeiro y=y₀, com todos os jatos derivados de y nulos. Isso converte os coeficientes suaves do alvo em constantes e preserva uma identidade off-shell nos jatos métricos livres. Não é necessário que soluções lorentzianas sejam densas entre soluções complexas.

Em g=eᵀηe, as derivadas de e são variáveis livres de uma ordem finita; qualquer jato assim escolhido com det e>0 é realizado localmente por um coframe suave invertível. Conexão, curvatura e suas derivadas são racionais, e a hipótese sobre denominadores permite eliminar todos eles por uma potência finita de det e. Um polinômio que se anula no aberto real dos jatos livres é identicamente nulo, inclusive após extensão complexa.

Com T=diag(1,i,i,i), TᵀηT=I e det T=−i. A substituição e_L=T e_R produz exatamente a métrica riemanniana g_R e prolonga-se aos jatos. O volume continuado pode ter uma fase constante; isso não altera a anulação das equações nem a independência das classes. A conjugação preserva o traço quadrático e transforma o Pfaffiano por um fator não nulo, de modo que a passagem (A,B)→(A′,B′) é invertível.

**Precisão de leitura:** a extensão racional aqui demonstrada é nos jatos métricos depois de congelar o escalar real y₀. A primeira frase do lema da nota deve ser lida com a prova que vem em seguida. Não há uma extensão holomorfa alegada para funções suaves arbitrárias do alvo ou para todos os jatos escalares complexos. Essa precisão não afeta a conclusão, que usa exclusivamente mapas constantes.

## 3. A primitiva global e os testes compactos

A naturalidade tensorial exclui coordenadas ou frames preferidos e a primitiva de Chern–Simons não covariante. Por isso β não depende da escolha de coframe local. Após complexificação, a identidade de transformação estende-se ao grupo ortogonal complexo conectado; as transições riemannianas passam a T R T⁻¹. As expressões calculadas nas cartas coincidem e definem uma 3-forma complexa global suave. Não é preciso um coframe global, uma estrutura spin ou uma métrica lorentziana global nas variedades de teste.

A restrição dos denominadores assegura que não aparece uma singularidade nova ao fixar y constante nem nos jatos de curvatura dos exemplos. Expressões localizadas em gradientes não nulos estariam fora desse argumento.

Para mapas constantes, todas as equações de matéria se anulam e T=0. Em dimensão quatro, G+Λg=0 equivale a Ric=Λg. A esfera redonda de raio √(3/Λ) satisfaz isso; a reescala (λ_FS/Λ)g_FS também, pois a conexão e o tensor Ric com índices inferiores não mudam sob reescala constante.

Com as normalizações topológicas adotadas, os números são (χ,p₁)[S⁴]=(2,0) e (χ,p₁)[CP²]=(3,3). As fórmulas de Euler e assinatura foram conferidas em [Gursky–LeBrun, equações (6)–(7)](https://arxiv.org/pdf/math/9807055); os valores de CP² também constam em [Bouwknegt–Evslin–Mathai, após o Lema 2.4](https://arxiv.org/pdf/1409.1296). Stokes elimina dβ, mesmo com valores complexos, e os jatos das EOM desaparecem. A matriz de avaliação tem determinante 6, logo força A′=B′=0 e então A=B=0. Esse passo não deixa uma combinação característica residual.

## 4. Ideal diferencial e igualdade fraca

A prova exclui uma identidade off-shell finita da forma E_char=dβ+ΣU_I∇^I E_g+ΣV_J∇^J E_y, com coeficientes na classe fixada. Ela não prova que toda expressão que se anula na superfície estacionária admite esse certificado nessa mesma classe. Tal identificação demanda uma resolução/regularidade apropriada; um resultado com coeficientes suaves arbitrários não fornece por si um certificado racional.

Conferi na fonte primária [Barnich–Brandt–Henneaux 1995](https://arxiv.org/pdf/hep-th/9505173) que A₂ é polinomial, conforme (3.19)–(3.20); que (7.33) é a hipótese sobre classes de grau máximo na cohomologia equivariante fraca; e que (8.4)–(8.8) traduzem os invariantes em formas tensoriais com D=d. Assim a passagem adicional identificada pela nota é real e não deve desaparecer do enunciado final. O uso de coeficientes suaves no alvo é uma extensão especificada pelo adendo, cuja validade para o teste decorre de congelá-los antes da continuação; isso não importa toda a classificação de A₂ para um sigma global.

No sigma, constantes admissíveis com tensão nula permitem o mesmo teste para certificados universais regulares. Um domínio restrito ao mapa identidade e a gradientes de posto máximo excluiria esse teste; não se pode trocar o complexo de contra-termos por tal domínio sem nova análise.

## 5. Consistência do relatório 068

O §2.5, linhas 101–103 do retrato lido, descreve exatamente a não trivialidade modulo o ideal, menciona a classe algébrica e Λ>0, e deixa em aberto a compatibilidade com igualdade fraca/KT. Também preserva as obrigações de cohomologia sigma, especialização formal e alcance global. A tabela subsequente e a formulação final não promovem o argumento a H¹ total ou ausência irrestrita de anomalias.

A linha 105 delimita as menções históricas a “matriz BV forte” aberta: a frente livre Einstein–sigma foi fornecida em outra nota, enquanto interação renormalizada e complexo probabilístico redundante continuam abertos. Isso é coerente com a revisão BRST delimitada já registrada, sem editar a nota C0 anterior.

**Resultado de revisão:** nenhum erro material encontrado nesse escopo; nenhuma correção obrigatória indicada. A formulação a preservar é “independência de Euler e Pontryagin modulo dΩ³ natural e o ideal diferencial EOM especificado”, com os contratos e limites acima.

## 6. Custódia

Nenhum arquivo existente foi alterado. Nenhum um.py foi executado ou importado; nenhum Lean ou CAS foi executado. Foram criados apenas este parecer e seu manifesto, em pasta nova dentro de Chatgpt. Os dois arquivos revisados foram medidos antes e depois da escrita e devem permanecer idênticos.

Pins medidos:

- `C:/IALD/Central de Patentes/Chatgpt/CLASSES_CARACTERISTICAS_C0_20260909_221649/EULER_PONTRYAGIN_ON_SHELL_E_LIMITE_C0.md` — 14254 bytes; SHA-256 `cc67cb0326dc6e21ce6ea84e32700ef07de3058991c865841ffefdf37ee3af3c`.

- `C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_068_20260909/REEXAME_SUFICIENCIA.md` — 15618 bytes; SHA-256 `eb965812e39dd7b9cfcecb179d27d1df1a9f96c3f98a7aa5e400077067fb8159`.
