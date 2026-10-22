# Reexame de suficiência — entrega 068

09/09/2026, horário de Brasília. [REAL — leitura de fontes e recibos] [DERIVED — demonstrações escritas] [KNOWN — contratos de literatura explicitados nas notas]. Todos os arquivos novos ficam em Chatgpt; os originais permanecem somente para leitura.

O avanço desta etapa retira duas pendências concretas do caminho do modelo estudado: a representação probabilística agora é global em toda a Cauchy S³, e a construção quântica livre inclui calibre, auxiliares, fantasmas e o inverso de Feynman. A interação renormalizada, as anomalias e a rota UV continuam sendo obrigações distintas. A suficiência deve ser enunciada para um modelo, domínio e conjunto de hipóteses precisos.

## 1. Qual versão foi realmente encontrada

[REAL] A leitura nova de `um.py`, selo, manifesto do kernel e saída registrada v338 encontrou os quatro artefatos iguais, byte a byte, aos da entrega 067. O selo confere com o hash do programa. O retrato e os pins calculados estão em [ESTADO_CANONICO_068.json](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_068_20260909/ESTADO_CANONICO_068.json>). Nenhum `um.py` foi executado ou importado.

A fonte contém 683 arquivos embutidos. Dos 98 módulos usados como referência pela bancada, 77 estão presentes e 21 ausentes. Isso é uma comparação AST da fonte com a lista da bancada; não é uma nova execução do kernel. A evidência de execução v338 é anterior e foi lida, sem repetição. O conteúdo dos novos documentos 068 também não foi incorporado automaticamente ao programa.

O selo ainda declara `GOROFF_SAGNOTTI_WALL_TYPED_OPEN__TWO_ROUTES_NAMED__BREUER_FINITENESS_MAY_NOT_BE_CITED_AS_UV_ANSWER`. O gate interno e o resultado dos testes de natureza permanecem com seus escopos registrados; não foram alterados.

Preservamos os avanços já existentes sobre registro de fase e ramo, H3 interno, critérios explícitos de falsificação e setores lineares anteriores. Eles não voltam à lista de pendências por terem sido omitidos numa leitura antiga. Os 21 nomes pendentes estão no retrato estruturado; a cópia histórica da integração 98 deve fornecer deltas para a versão viva, jamais substituí-la integralmente.

## 2. O que esta etapa acrescenta

### 2.1 Os mesmos dados podem representar globalmente o fundo e sua matéria

[DERIVED + KNOWN] A [prova global](<C:/IALD/Central de Patentes/Chatgpt/GLOBALIZACAO_PROBABILIDADES_S3_20260909_220238_785086/PROVA_GLOBAL_S3_ASSINADA_E_LIVRE.md>) constrói um alfabeto suficiente de **1.289 probabilidades positivas** no fundo

\[
M=(0,\pi)\times S^3,\qquad g=dr^2-a(r)^2\gamma,\qquad
a=2\cos(r/2),\qquad \phi(r,z)=z,
\]

com a ação Einstein–sigma adotada, \(\kappa c=4\), \(\Lambda=3/4\), \(c>0\). A partição fina conserva as condicionais. O relógio é \(q=1-a^2/8\), e oito pesos

\[
B_{a,\pm}=\frac{1\pm\phi_a/2}{8},\qquad
\phi_a=8(B_{a,+}-B_{a,-})
\]

retêm também os sinais dos quatro componentes de \(\phi\). O mapa global conserva o ponto \((r,z)\), além da métrica reconstruída. Não se recupera apenas \(\phi_a^2\).

O bloco de amplitudes livre tem 21 componentes; o bloco residual tem 140. Com oito grupos e o relógio, \(1+8(21+140)=1289\). Há limites positivos explícitos: cada probabilidade fina de grupo satisfaz \(P_{b\ell}\ge a^2/161280>0\) no domínio aberto. O extremo \(a=0\) não pertence ao domínio. A parte residual importa o teorema de imersão isométrica de Nash para uma métrica positiva em S³. Portanto o resultado é uma **prova de existência com blocos explícitos e um componente fornecido por Nash**; não é uma tabela numérica de 1.289 funções já calculada integralmente.

Se \(\Phi:P\mapsto(g,\phi)\), a nota fornece globalmente um inverso à direita da variação conjunta,

\[
A=D\Phi,\qquad AR=\mathrm{Id},
\]

preservando suportes compactos interiores. Isso permite aplicar em toda a Cauchy os resultados variacionais, de Hessiana e de corrente simplética da entrega 067. Sob a ação \(S_P=S_{\mathrm{Einstein\text{-}sigma}}\circ\Phi\), a equação variacional levantada equivale à equação ambiente no domínio descrito. O estado físico linear anterior transporta-se ao mesmo quociente físico probabilístico.

[INPUT] A ação, a partição e a correspondência continuam explicitadas como entradas. Esta construção não prova que todo relógio previamente selecionado, toda topologia ou todo campo de matéria tenha a mesma representação. A limitação do antigo alfabeto de cinco probabilidades continua verdadeira para aquele alfabeto; o novo resultado usa um espaço de dados maior e especificado.

### 2.2 A quantização livre foi completada no sistema Einstein–sigma

[DERIVED + KNOWN] A [extensão BRST](<C:/IALD/Central de Patentes/Chatgpt/EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md>) constrói as covariâncias do sistema completo \((u,b,c,\bar c)\), incluindo os componentes não físicos. A [revisão independente delimitada](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_ADVERSARIAL_BRST_068_20260909_221529_258581/PARECER_BRST_068.md>) conferiu a álgebra de Cauchy, as correções suaves, os blocos de Green e os contratos microlocais, sem encontrar erro material nesse escopo.

O passo efetivo é construir primeiro um defeito de Ward suave, corrigi-lo sem mudar o comutador nem a frente de onda e só então substituir o bloco físico pela covariância positiva 067. Um projetor arbitrário de dados de Cauchy não foi presumido preservador de frequência. A positividade é exigida no quociente físico; as componentes auxiliares têm pseudocovariâncias, como corresponde ao contrato BRST usado.

O [adendo de Feynman](<C:/IALD/Central de Patentes/Chatgpt/EXTENSAO_BRST_COMPLETA_20260909_220941_811364/ADENDO_FEYNMAN_PARIDADE_E_CONTATOS.md>) fixa \(E=G^{\rm ret}-G^{\rm adv}\), \(W^+-W^-=i\hbar E\) e a paridade \(Z=\operatorname{diag}(+,+,-,-)\). O inverso é

\[
G_L^F=G_L^{\rm ret}-\frac{i}{\hbar}Z\Lambda_L^-
     =G_L^{\rm adv}-\frac{i}{\hbar}\Lambda_L^+,
\qquad LG_L^F=G_L^FL=1.
\]

Os contatos e as Ward lineares estão explicitados. Isso fornece as contrações livres para funcionais não lineares e o dado quadrático de ordenação temporal.

[OPEN] Ainda não é a construção dos produtos temporais renormalizados nas diagonais de ordens superiores nem a identidade mestra quântica da interação. O complexo construído é o **Einstein–sigma**. Se as probabilidades redundantes forem quantizadas como campos independentes, também será necessário tratar suas direções verticais e seus próprios fantasmas; o transporte do quociente físico não demonstra automaticamente esse complexo adicional. A prova do extrator de calibre usa \(\phi=\mathrm{id}\) e \(\dot a/a\ne0\); outro fundo requer verificar novamente esses contratos.

### 2.3 Há um cálculo concreto dos primeiros contratermos

[DERIVED + KNOWN] A [nota de renormalização sigma](<C:/IALD/Central de Patentes/Chatgpt/RENORMALIZACAO_SIGMA_EFT_20260909/CONTRATERMOS_SIGMA_E_ORDEM_EFT.md>) calcula o coeficiente local de calor de uma volta do sigma com alvo S³ e **métrica euclidiana externa**. Com \(W_{\mu\nu}=\langle\partial_\mu\phi,\partial_\nu\phi\rangle\) e \(Q=\operatorname{tr}W\), ele é

\[
\mathcal B_4=\frac{Q^2}{3}+\frac{2W_{\mu\nu}W^{\mu\nu}}{3}
+\frac{RQ}{3}+\frac{5R^2-2\operatorname{Ric}^2+2\operatorname{Riem}^2}{120}
+\frac{\Box Q}{3}+\frac{\Box R}{10}.
\]

A convenção do operador, o sinal da divergência e o corte estão declarados na nota, a partir do coeficiente universal da literatura. Um exemplo exato em toro plano, com \(\phi_k=(\cos kx,\sin kx,0,0)\), satisfaz a equação sigma e produz \(\mathcal B_4=k^4\). Isso não pode ser absorvido, para todos os inteiros \(k\), apenas por uma constante e por um termo proporcional a \(Q=k^2\). Portanto esse setor externo requer operadores de quatro derivadas.

O cálculo **não** é o determinante completo do sistema métrica–sigma–fantasmas e não exclui, sozinho, cancelamentos no cálculo acoplado. Ele mostra onde entram operadores novos na ação efetiva e quais coeficientes finitos precisarão de condições de renormalização. A expansão efetiva trata tais termos como inserções perturbativas; não foi feita uma ressoma que redefinisse o propagador por um operador de ordem superior.

### 2.4 A fonte quártica já tem um fundo clássico corrigido

[DERIVED] Para a ação lorentziana explicitada com \(L_4=b_1Q^2+b_2W^2\), a [dedução variacional](<C:/IALD/Central de Patentes/Chatgpt/RENORMALIZACAO_SIGMA_EFT_20260909/FONTE_QUARTICA_E_HABITANTE_CORRIGIDO.md>) e a [revisão independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_FONTE_QUARTICA_20260909_221154/REVISAO_VARIACIONAL_E_FRIEDMANN.md>) dão, para \(B=3b_1+b_2\),

\[
\rho_4=-\frac{3B}{a^4},\qquad p_4=-\frac{B}{a^4},\qquad
\dot a^2=1-\frac{a^2}{4}-\frac{\kappa B}{a^2},
\]
\[
a_B(r)^2=2+2\sqrt{1-\kappa B}\cos(r-r_0),
\]

quando \(1-\kappa B>0\) e \(a_B^2>0\). As duas componentes de Einstein e a equação sigma foram verificadas. O caso estático \(\kappa B=1\), \(a^2=2\), também satisfaz ambas as componentes.

[INPUT/OPEN] Os \(b_i\) são coeficientes lorentzianos finitos escolhidos. O resultado é uma solução clássica de uma ação truncada; não é uma expectativa quântica total do tensor de energia nem uma prova de resolução da singularidade. O estado e a estabilidade do fundo não corrigido não se transferem sem recalcular os operadores no novo fundo.

### 2.5 As obrigações sobre anomalias agora têm hipóteses identificadas

[DERIVED] A [nota BV](<C:/IALD/Central de Patentes/Chatgpt/BV_ANOMALIAS_SIGMA_FORMAL_20260909_215557/BV_LOCAL_SIGMA_E_RENORMALIZACAO_CONDICIONAL.md>) constrói o diferencial clássico e demonstra um lema de levantamento formal: se a cohomologia local pertinente do sistema de referência em número fantasma um se anula, a deformação em série formal \(\varepsilon\) também permite eliminar cociclos ordem a ordem. Sob produtos temporais renormalizados com a identidade anômala local e as demais hipóteses explicitadas, isso fornece a indução formal para remover a anomalia da identidade mestra.

O [adendo de classes características](<C:/IALD/Central de Patentes/Chatgpt/CLASSES_CARACTERISTICAS_C0_20260909_221649/EULER_PONTRYAGIN_ON_SHELL_E_LIMITE_C0.md>) paga uma parte específica do teste C0/(7.33): nenhuma combinação não nula de Euler e Pontryagin é exata modulo o ideal diferencial das equações, na classe natural algébrica definida, com \(\Lambda>0\). A complexificação é demonstrada para um certificado off-shell racional em jatos; a primitiva tensorial é global. As avaliações em S⁴ e CP² produzem a matriz \(\bigl(\begin{smallmatrix}2&0\\3&3\end{smallmatrix}\bigr)\), de determinante 6.

[OPEN] É preciso compatibilizar a igualdade fraca e a resolução Koszul–Tate com esse mesmo ideal e espaço de coeficientes para completar o uso da classificação. Também falta fechar a cohomologia sigma no alcance pretendido, ou demonstrar a especialização da construção formal no parâmetro físico \(\varepsilon=1\). A regularidade da métrica alvo clássica nesse valor não prova a especialização das primitivas formais. A ausência de anomalias locais, se obtida, ainda não resolveria automaticamente grandes difeomorfismos, fases globais ou independência entre fundos.

As menções a “BRST forte aberto” nas notas BV/C0, escritas antes da conclusão da frente livre, ficam delimitadas por este adendo: o dado livre Einstein–sigma do fundo 068 foi fornecido. O regime BV **interagente renormalizado** e o eventual complexo probabilístico redundante permanecem abertos. As notas anteriores não foram reescritas.

## 3. O que ainda falta, em ordem de dependência

| Obrigação | O que já existe | O resultado que ainda precisa ser entregue |
|---|---|---|
| Correspondência e alcance físico | Representação local geral sob residual positivo; representação global do fundo S³; equivalência variacional condicional | Fixar o alcance do enunciado final e justificar a correspondência/ação nesse alcance, ou mantê-las como postulados explícitos. Generalizar fundos, matéria e relógios apenas quando isso fizer parte da alegação. |
| Interação quântica efetiva | Hessiana, estado físico, sistema livre BRST, inverso Feynman e primeiros operadores locais | Construir os produtos temporais renormalizados do sistema acoplado e as identidades de Ward/mestra da interação, com condições de renormalização declaradas. |
| Anomalias | Diferencial clássico, lema formal condicional, teste característico algébrico | Fechar os contratos cohomológicos e sua aplicação ao sigma físico; tratar separadamente o alcance global e a independência entre fundos. |
| Altas energias | Parede UV tipada e organização em ação efetiva | Demonstrar a rota UV escolhida: controle dos contratermos, limites e previsões na extensão reivindicada. Finitude de uma descrição ou ausência atual de falsificação não fornece esse limite. |
| Quantização direta dos dados P, se reivindicada | Equivalência clássica e transporte do quociente linear | Tratar redundância vertical, medida/Jacobiano funcional e positividade operatorial pertinente, ou definir explicitamente os observáveis P por transporte da teoria ambiente, sem alegar equivalência de duas integrais funcionais independentes. |
| Incorporação verificável | Integração 98 histórica compilada; 77 módulos presentes no canônico; notas novas revisadas em escopos delimitados | Portar os 21 deltas pendentes e formalizar os novos enunciados/hipóteses com a evidência correspondente. Uma nota escrita ou um controle CAS não vira automaticamente declaração Lean compilada. |

O trabalho de integração não substitui essas obrigações matemáticas, e uma obrigação matemática demonstrada não deve ser reaberta apenas porque ainda falta incorporá-la ao programa. A tabela distingue os dois tipos de trabalho.

## 4. Evidência desta entrega e leitura permitida

[REAL] Há **68 controles simbólicos exatos** novos nesta etapa: 47 da representação global, 13 do coeficiente sigma e 8 da fonte quártica. Seus recibos registram resíduos zero e escopos próprios. São controles algébricos; não são 68 teoremas analíticos nem 68 provas Lean. Houve **zero nova execução Lean**, zero execução/importação de `um.py` e zero novo teste de natureza nesta entrega.

[DERIVED] O relatório reúne demonstrações escritas, leitura da raiz e revisões cruzadas delimitadas. Os manifestos registram quais fontes cada revisão realmente examinou. Não se atribui aprovação ao operador, a uma comunidade científica ou a um revisor externo.

A formulação atualmente sustentada é: **há um modelo Einstein–sigma condicional com representação probabilística global do fundo especificado, equivalência variacional e uma quantização livre física acompanhada do sistema BRST completo nesse fundo; a construção interagente, suas anomalias no alcance total e a rota UV ainda exigem os resultados da tabela.** Isso expressa suficiência dentro de um enunciado e mantém visíveis suas hipóteses.

O manifesto `MANIFESTO_ENTREGA_068.json`, nesta pasta, mede os artefatos e confere recibos e preservação de fontes. A [entrega no túnel](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_068_ESPONTANEA_global_brst_eft.md>) orienta a sessão que codifica. Nenhum original, Atlas, índice canônico, memória de outra casa ou gate foi alterado.
