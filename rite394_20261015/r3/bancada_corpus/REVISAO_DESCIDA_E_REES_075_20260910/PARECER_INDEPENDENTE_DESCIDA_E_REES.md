# Parecer independente: descida natural e preservação de Rees

10/09/2026, frente075. [DERIVED — revisão escrita independente]. Nenhuma fonte foi alterada. Não houve execução de um.py, Lean, CAS ou construtores das notas examinadas. Este parecer registra minha análise, não aprovação em nome do operador ou de outro agente.

**Conclusão delimitada:** não identifiquei erro material na composição das duas notas de Singer abaixo, na categoria que elas explicitam. O primeiro descendente natural segue da exatidão ordinária da topforma s a₄¹ e da identidade variacional covariante. Os passos restantes seguem do lema de símbolos para formas de grau menor que quatro. As escolhas horizontais preservam E,N,L e o peso de Rees por componente quando as conexões dos fibrados perturbativos são fixadas por B₀. Não se demonstra a exatidão do cociclo total ou uma QME com esses resultados.

## 1. Documentos efetivamente lidos e entrada da revisão

Li integralmente:

- `DESCIDA_NATURAL_SIMBOLOS_075_20260910/DESCIDA_NATURAL_POR_OPERADORES.md`;
- `DESCIDA_NATURAL_SIMBOLOS_075_20260910/ADENDO_PRIMEIRO_DESCENDENTE_E_COMPOSICAO_075.md`;
- `COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md`.

Confrontei a composição com minha prova `AUDITORIA_DESCIDA_NATURAL_075_20260910/SIMBOLOS_GRASSMANN_E_PRIMEIRO_DESCENDENTE.md`, especialmente seu complemento de topforma. Esta revisão não reexecuta a entrega074 ou os controles documentais de outras tarefas. Os pins lidos estão no manifesto acompanhante.

O argumento de descida é compatível com o uso do lema horizontal em [BBH2000, Teoremas4.1–4.2 e §9.2](https://arxiv.org/pdf/hep-th/0002245v3), mas a naturalidade aqui é demonstrada pelas operações covariantes específicas das notas, não importada da primitiva coordenada geral.

## 2. Categoria: liberdade de jatos e tensorialidade

A separação Y/Z é suficiente: Y tem ghost zero; Z reúne geradores de ghost não zero que são seções de fibrados vetoriais graduados com leis de transformação lineares e coeficientes de ghost zero. Seus jatos são livres. Não se usa o ghost Lorentz cru com sua transformação afim como se fosse um tensor independente; a fonte restringe-se à apresentação métrica efetiva ou a uma tensorialização já demonstrada.

As conexões usadas na prova horizontal não dependem de Z. Isso permite que a variação prolongada em Z comute com as derivadas covariantes, e preserva o grau Euler N. No alvo, a conexão pullback por um campo de ghost zero serve à prova em campos completos; para controlar valência perturbativa, a fonte exige uma apresentação diretamente nos fibrados de B₀. Essa distinção está corretamente mantida.

A hipótese é uma identidade universal off-shell. Se os jatos de Z satisfizessem equações diferenciais, a linearização só valeria sobre suas variações admissíveis, e a leitura do símbolo principal livre não seria justificada. Da mesma forma, uma igualdade apenas avaliada num fundo não substitui a identidade universal usada no lema.

## 3. Símbolos, Grassmann e terminação

A linearização por parâmetro ε par, com v de mesma paridade e ghost que Z, é a escolha correta. Os jatos v são geradores novos, de modo que uma identidade linear neles permite separar todos os coeficientes, inclusive quando são Grassmann-ímpares. Substituir v=Z antes de obter a identidade de operadores poderia apagar termos e não é feito.

Na convenção dx à esquerda, confirmei

\[
\delta=p_i dx^i\wedge,\qquad h=\partial_{p_i}\iota_i,
\qquad\delta h+h\delta=(r+n-q)I.
\]

O termo r é o grau homogêneo do símbolo; n−q vem da contração exterior. Nenhum deles é um grau de ghost. As operações de símbolo não reordenam os coeficientes Grassmann e o cálculo permanece válido sobre essa álgebra de coeficientes.

O símbolo da primitiva tem ordem r−1. Realizá-lo por derivadas covariantes simetrizadas dá um operador natural; subtrair sua derivada horizontal retira precisamente a ordem r. Derivadas dos coeficientes e curvaturas ficam no resíduo de ordem menor em v e são processadas na indução seguinte. Assim a construção termina, embora a ordem de jatos dos coeficientes possa aumentar finitamente.

Em r=0, o denominador n−q é não nulo para q<n, portanto o residual é zero. Em q=0, h não produz uma forma de grau negativo: a identidade força o próprio operador a zero em cada ordem. A nota principal não extrapola esse argumento para q=n.

A realização covariante, com conexão fixada, também define uma escolha linear na forma fechada: usar um limite superior de ordem maior apenas insere símbolos zero. Isso permite a aplicação por componente sem escolher uma homotopia diferente por uma condição não linear sobre a ordem efetiva da entrada.

## 4. Avaliação v=Z, Euler e topforma

Depois de obtida P=d_HQ, a avaliação v_I→Z_I é um mapa de álgebras diferenciais graduadas. Derivações dos coeficientes de Q e de seus argumentos permanecem presentes nos dois lados. Portanto P[Z]=d_H(Q[Z]) é válido mesmo quando os coeficientes de Q contêm ghosts.

Euler_Z conta cada Z e cada um de seus jatos uma vez. Numa componente homogênea, P[Z]=Nω. Dividir por N>0 fornece a primitiva com o mesmo ghost e o mesmo N. A hipótese sobre coeficientes exclui constantes externas de ghost positivo fora desse conjunto; por isso ghost positivo realmente implica N>0.

O adendo de Singer consome corretamente meu complemento de topforma. F=d_Hβ ordinariamente implica a nulidade dos operadores Euler–Lagrange em Z. Ao decompor em N, cada operador de Euler de F_N tem grau N−1; componentes distintas não se cancelam. Assim cada F_N possui operador de Euler nulo. A primeira variação com integração por partes covariante produz

\[
\delta_vF_N=v^A\mathcal E_A(F_N)+d_H\Theta_{F_N}[v]
=d_H\Theta_{F_N}[v].
\]

A corrente Θ é construída de F, das conexões e de v, sem usar uma primitiva ordinária não natural como dado geométrico. A avaliação v=Z e a divisão por N fornecem a primitiva natural. Não houve promoção de toda topforma fechada a divergência: a exatidão ordinária de F é o antecedente que anula seu termo Euler, e N=0 permanece excluído.

Em particular, a obstrução Euler(g₀) da entrega074 não é apagada: ela tem ghost zero, N=0, e não entra nesse argumento. Curvaturas nas ordens inferiores do operador linear em v também não significam que a avaliação normal de074 passe a comutar com d_H em geral.

## 5. Conferência de E, N e da completação de Rees

A nota074 define

\[
\mathcal R_L^q=\prod_{E\ge0}t^{E+2L-2}\mathcal P_E^q.
\]

Cada campo normalizado, ghost e antifield e cada um de seus jatos conta uma perna E. Coeficientes de B₀ e dx contam zero. N conta apenas as pernas do subconjunto Z. Essas graduações são diferentes de ghost e de peso de engenharia.

Para uma entrada de grau (E,N), a linearização em Z retira uma perna dos coeficientes e introduz uma v de mesmo tipo: o total, contando v, continua E, e o coeficiente em Z passa de N a N−1. As conexões B₀ não acrescentam campos de flutuação. Derivar um coeficiente de B₀ mantém E=0; derivar um jato normalizado apenas troca a ordem do jato, mantendo E=1. Símbolos, contrações e quantização não mudam essas contagens. A avaliação v=Z recompõe a perna retirada e N, e a divisão inteira não altera grau algum.

Esse cálculo vale tanto para a redução por símbolos quanto para a corrente obtida por integração por partes da topforma. Logo cada **operador de primitiva horizontal** conserva E,N e atua no mesmo L:

\[
H(t^{E+2L-2}\omega_E)=t^{E+2L-2}H(\omega_E).
\]

Não aparece t⁻¹ nesse operador; isso é diferente da translação b_N da entrega074. Cada coeficiente de saída depende apenas do coeficiente da mesma valência E de entrada e de suas operações diferenciais finitas. A continuidade na topologia de produto por E está, portanto, justificada sem um limite uniforme da ordem de jatos em todos os graus.

Essa preservação de E,N diz respeito às escolhas horizontais aplicadas a cada entrada. O diferencial s pode misturar E ou N; para a descida composta basta que ele preserve a classe Rees, como a nota074 delimita. Não se afirma que cada termo da descida inteira tenha o mesmo N inicial quando se intercala s.

Na classe analítica e homogênea, as operações finitas preservam a regularidade e o peso declarado quando as conexões os preservam. A nota não deriva analiticidade de uma entrada meramente C∞ nem substitui as restrições de escala de todos os mapas multilineares de renormalização por essa contagem.

## 6. Composição da descida e fronteira exata

O antecedente necessário é

\[
s a_4^1+d_H\beta_3^2=0
\]

como identidade ordinária universal off-shell, com a₄¹ e s naturais, s²=0 e {s,d_H}=0. Aplicar o complemento à topforma s a₄¹ fornece a₃² natural. Aplicar s e usar o lema horizontal nos graus3,2,1 fornece a₂³,a₁⁴,a₀⁵ naturais. O caso q=0 dá s a₀⁵=0. Os sinais do adendo estão coerentes: se s a₄¹=d_Hη₃², escolhe-se a₃²=−η₃².

Assim a soma Ω=a₄¹+a₃²+a₂³+a₁⁴+a₀⁵ satisfaz (s+d_H)Ω=0. O adendo paga o primeiro descendente que a nota principal ainda mantinha condicionado, mas somente quando a consistência ordinária universal é dada. Não afirma que uma quebra observada em uma única referência possua automaticamente tal levantamento universal.

Os limites que permanecem são materiais:

- fontes centrais de ghost positivo sem jatos livres não estão cobertas;
- fecho apenas no quociente on-shell de Z não permite a leitura dos símbolos livres;
- a identidade de consistência precisa estar na mesma apresentação e completação das primitivas;
- a construção de Ω natural fechado não fornece uma primitiva de Ω para s+d_H;
- os grupos E₂, a admissibilidade conjunta na hierarquia causal, a remoção da anomalia e a QME continuam obrigações distintas.

Não encontrei na fonte uma extrapolação desses resultados para independência quântica geral de fundo ou completude UV. Este parecer registra coerência matemática da composição delimitada, e não uma prova dessas conclusões mais fortes.

## 7. Custódia

O manifesto lê os bytes das duas fontes de Singer, da classe Rees074, da auditoria de topforma e deste parecer. As fontes são lidas duas vezes para conferir estabilidade. O parecer e seu script foram escritos como arquivos temporários novos e publicados por rename após verificação de bytes. Nenhuma fonte anterior foi substituída.
