# Parecer independente084: eliminação finita da isotropia e canal de Euler

10/09/2026. [DERIVED — revisão matemática escrita independente da nova redução084]. [REAL — custódia documental]. Nenhuma execução matemática, CAS, Lean ou um.py. Todas as fontes anteriores preservadas.

**Parecer favorável no alcance declarado. Não identifiquei erro material** na [redução084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>). A forma normal finita e o critério
\[
J_W\nu\in dC_{\rm nat}^3
\quad\Longleftrightarrow\quad
J_W=\operatorname{div}_0V+K^2f_E,\qquad
f_E\in\mathscr N^{\mathfrak g},
\quad V\in(\mathscr N\otimes V_0)^{\mathfrak h}
\]
estão justificados no mesmo complexo fixado, sem presumir que \(\mathscr N^{\mathfrak g}=0\) ou que exista o par(V,f_E).

Li integralmente a fonte e seu manifesto. Também li as notas necessárias da corrente horizontal082, da transferência080, da redução081 e da transgressão076, e os pareceres independentes das duas entradas082.

**Proveniência.** A identificação CE082 e a redução081 são de minha autoria antecedente. Este parecer não é uma nova aprovação independente dessas provas. A identificação082 foi objeto do [parecer externo de Turing](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CE_QUADRATICO_082_20260910_053047_6990258/PARECER_IDENTIFICACAO_CE_082.md>), aqui lido. A presente revisão avalia a nova eliminação vertical084 e sua composição com essas entradas. Meu controle breve por mensagem antes da escrita também não é contado como revisão integral prévia.

## 1. Módulo, decomposição e sinais de grau

O complexo é \(C^\bullet(\mathfrak g,\mathscr N)^{\mathfrak h}\), com
\(\mathscr N=R_{\rm her}\otimes\operatorname{Sym}^2\mathcal M\),
\(\mathfrak g=\mathfrak h\oplus V_0\), \(\mathfrak h=\mathfrak{so}(1,3)\) e \(\dim V_0=4\).
\(\mathcal M\) conserva suas relações de jatos/EOM. Não foi trocado por uma torre livre, nem o CE invariante pelo relativo.

A separação pelos números de ghosts p e θ tem
\[
d_0:(r,q)\mapsto(r,q+1),\quad
d_1:(r,q)\mapsto(r+1,q),\quad
d_2:(r,q)\mapsto(r+2,q-1).
\]
Os valores nos geradores preservam o sinal082:
\(dp=-\theta p\), \(d\theta=-\theta^2+Kpp^\flat\).
O ghost θ é a parte antissimétrica de ∇C, não o m covariante elevado de sinal oposto.

O diferencial vertical inclui a ação de isotropia nos coeficientes E_r=\(\mathscr N\otimes\Lambda^rV_0^*\), inclusive nos ghosts p. Com o shuffle graduado declarado, é o CE de h nesses coeficientes. Um sinal global dependente de r sob outra ordem de escrita é absorvido nesse shuffle; não altera o cálculo de cohomologia e não autoriza retirar os sinais nas subtrações dR.

As identidades de bigrau extraídas de d²=0 estão completas. Em particular, \(d_1^2\) não é tomado como zero no complexo inteiro: ele é compensado por \(\{d_0,d_2\}\). A nulidade de \(d_{\rm rel}^2\) na linha horizontal invariante usa especificamente d0=0 e d2=0 nessa linha.

## 2. O uso da cohomologia finita de h é legítimo

Um elemento de E_r usa finitíssimos jatos de Weyl e coeficientes escalares. Seu fecho por h está contido num espaço tensorial finito de mesma ordem de jatos. A passagem ao quociente das EOM não aumenta a dimensão desse corte. A extensão por escalares inertes conserva essa afirmação elemento a elemento.

d0 preserva tal corte. Não é necessário que ele seja preservado por transvecções, e a nota não faz essa suposição. Após aplicar d1 numa das subtrações, basta tomar um corte maior, ainda finito. Existem somente três etapas de eliminação vertical.

Conferi diretamente a fonte primária indicada: [Chevalley–Eilenberg1948, teoremas19.1 e24.1](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/chev-eilen.pdf). O primeiro identifica a cohomologia trivial com cochains invariantes; o segundo elimina a cohomologia em irreps FINITAS não triviais de uma álgebra semissimples. A decomposição finita em irreps separa o coeficiente trivial. Essa importação é aplicada à h, não a um suposto módulo finito da álgebra g inteira.

Para uma primitiva vertical de um ciclo invariante, há também controle de naturalidade: escolha o corte finito que contém a primitiva e seu ciclo, e projete a primitiva para a parte h-invariante. O diferencial comuta com essa projeção, logo sua imagem continua sendo o ciclo dado. É uma cisão equivarante finita, não integração sobre o grupo Lorentz não compacto.

Como \(\Lambda^q\mathfrak h\) é finita, cochains CE comutam com a união filtrante desses cortes. A cohomologia também comuta com esse limite DIRETO de espaços vetoriais. Assim a igualdade vertical
\[
H^q(C^{r,\bullet},d_0)
=(\mathscr N\otimes\Lambda^rV_0^*)^{\mathfrak h}
 \otimes H^q(\mathfrak h,\mathbb R)
\]
é justificada. Não envolve um limite inverso ou a completação em infinitas derivadas dentro de um coeficiente.

A complexificação de h em dois fatores sl2 fornece duas classes reais de Cartan em grau3, e uma em grau6, além da unidade de grau0. H¹ e H² são zero. Esse passo usa o compacto dual dos dois fatores, ou equivalentemente seus módulos exteriores; não substitui h pelo seu subgrupo compacto máximo so(3), cuja única classe3 daria uma contagem incorreta.

## 3. As cúbicas e o termo de curvatura

Os bilineares \(B_{\rm tr}=\operatorname{tr}(XY)\) e
\(B_E=\varepsilon_{abcd}X^{ab}Y^{cd}/24\)
são invariantes e independentes sobre h. Seus cociclos \(-B(\theta,\theta^2)/3\) dão as duas Cartan verticais. A normalização de B_E está explícita, não é herdada de uma ocorrência homônima de Euler em outra nota.

Revi a identidade
\[
\operatorname{CS}_B=B(\theta,F)-\tfrac13B(\theta,\theta^2),
\quad F=Kpp^\flat,\qquad
d\operatorname{CS}_B=B(F,F).
\]
É a Chern–Simons graduada com \(d\theta=F-\theta^2\). A relação \(dF=F\theta-\theta F\) segue de dp e do abaixamento métrico, e a invariância de B cancela os termos de conexão. Trata-se de um polinômio finito em ghosts; não é uma troca da curvatura de fundo pela curvatura dinâmica.

Para o traço, \(p_bp^b=0\) dá \(\operatorname{tr}(F^2)=0\). Para B_E, \(F^{ab}=Kp^ap^b\) e \(\varepsilon pppp=24\nu\) dão
\[
d\operatorname{CS}_{\rm tr}=0,\qquad
d\operatorname{CS}_E=K^2\nu.
\]
Os sinais e o fatorK² estão corretos. Um coeficiente f somente h-invariante produziria adicionalmente df∧CS; essa parcela é eliminada apenas DEPOIS da condição f∈\(\mathscr N^{\mathfrak g}\) demonstrada no passo seguinte.

## 4. A eliminação vertical não salta a condição sobre os coeficientes

Decompõe-se Q em Q03+Q12+Q21+Q30 e supõe-se que dQ tenha somente bigrau(4,0).

A equação(0,4) permite escrever
\[
Q_{0,3}=f_{\rm tr}\tau_{\rm tr}+f_E\tau_E+d_0R_{0,2},
\qquad f_i\in\mathscr N^{\mathfrak h}.
\]
Subtrair dR02 conserva dQ e remove a peça vertical exata. Os termos de d1R02 e d2R02 permanecem nas outras componentes; não foram apagados.

A equação seguinte, de bigrau(1,3), diz que
\[
\sum_i(d_{\rm rel}f_i)\otimes[\tau_i]=0
\]
na cohomologia vertical. Os \(d_{\rm rel}f_i\) já pertencem ao setor invariante dos coeficientes \(\mathscr N\otimes V_0^*\); não são classes de grau vertical positivo que ainda possam ser anuladas por uma fronteira nesse coeficiente. A independência das duas Cartan força cada um a zero. Isso é precisamente \(\rho_{P_a}f_i=0\) para todos os a. Junto à invariância por h, conclui-se f_i∈\(\mathscr N^{\mathfrak g}\).

Esse é o ponto decisivo: os coeficientes são invariantes sob g por uma equação, não por uma aplicação indevida de Whitehead ou por serem escalares de Lorentz.

Pode-se então subtrair \(\sum_i f_i\operatorname{CS}_i\): dfi=0, e a mudança em dQ é inteiramente horizontal. Q03 fica zero.

A equação(1,3) remanescente torna Q12 verticalmente fechada. Hh²=0 permite Q12=d0R11 com R11 invariante e finita. Subtrair dR11 remove Q12, conservando seus efeitos em Q21/Q30. A equação(2,2) torna Q21 verticalmente fechada; Hh¹=0 fornece R20, e a última subtração deixa Q30. Nenhuma subtração recria uma componente de menor número de p, pois d1 e d2 só aumentam esse número.

Somar os três R dá a forma normal
\[
Q=q_V+f_{\rm tr}\operatorname{CS}_{\rm tr}
      +f_E\operatorname{CS}_E+dR.
\]
O termo fechado de traço é conservado, sem reivindicar unicidade da decomposição ou exaustão de H³ para dQ arbitrário não horizontal.

## 5. Necessidade e suficiência no mesmo módulo

A orientação identifica Q30 com um vetor quadrático natural V:
\(q_V=\varepsilon_{abcd}V^ap^bp^cp^d/3!\).
A [identidade da corrente082](<C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md>) dá \(dq_V=(\operatorname{div}_0V)\nu\), sem passar a um quociente por divergências.

Aplicar d à forma normal prova a necessidade:
\(J_W=\operatorname{div}_0V+K^2f_E\).
A identificação com o coeficiente de ν é injetiva, pois \(\Lambda^4V_0^*\) tem a base não nula ν e estamos no mesmo módulo de coeficientes. A recíproca é a construção explícita \(Q=q_V+f_E\operatorname{CS}_E\). A direção “se” não presume uma primitiva natural maior que a classe usada na direção “somente se”.

A nota conserva \(\mathscr N\) como módulo QUADRÁTICO. A unidade do anel escalar não é automaticamente um elemento desse módulo, e J_W ser um escalar de h não implica que seja invariante por transvecções. Portanto o critério não foi tornado tautológico acrescentando livremente um f de grau zero.

K² permanece visível. Com K real fixo não nulo, multiplicar por K² é uma unidade; num anel restrito em K variável essa substituição exige outra tipagem. Igualmente, restrições suplementares de engenharia ou admissibilidade causal não são dispensadas por uma solução no módulo maior.

## 6. A organização por páginas concorda com a prova finita

A filtração por grau horizontal tem somente r=0,…,4. A página vertical possui linhas q=0,3,6, e d1 induz o complexo horizontal relativo B. Os diferenciais das páginas2 e3 têm alvos em linhas vazias, portanto são nulos.

O único canal que atinge(4,0) é
\[
d_4:E_4^{0,3}=\mathscr N^{\mathfrak g}\otimes\mathbb R^2
\longrightarrow E_4^{4,0}=H^4(B).
\]
Sua realização pela Chern–Simons é zero para traço e \([K^2f\nu]\) para Euler. A nota mantém ainda a possibilidade do canal(0,6)→(4,3); não declara todas as Cartan permanentes. Não há novo diferencial de página superior a4 por falta de posições horizontais.

Essa descrição não usa uma hipótese Mittag–Leffler. A forma normal já provou diretamente a afirmação sobre a imagem em grau4; a sequência espectral finita é uma organização adicional, não uma inferência que esconda uma extensão de cohomologias.

## 7. Limites e conclusão da revisão

Não identifiquei erro material. A redução fornece um critério necessário e suficiente dentro do CE natural fixado e diminui o tipo de ghosts que precisa ser examinado. A obtenção das primitivas verticais é finita e h-invariante, e os coeficientes das Cartan são obrigados a pertencer a \(\mathscr N^{\mathfrak g}\).

Não foi calculado esse último módulo, nem demonstrada sua nulidade. Não foi encontrado V que produza J_W modulo o canal de Euler. Não há classificação total de derivadas, extensão ao fundo físico φ=id, afirmação de regularidade universal em K, admissibilidade Q2, QME ou UV.

Os cálculos083 não são usados nesta prova084 nem incorporados retroativamente na entrega anterior. Este parecer é novo; os controles documentais do recibo não são teoremas Lean, CAS ou execução de um.py.
