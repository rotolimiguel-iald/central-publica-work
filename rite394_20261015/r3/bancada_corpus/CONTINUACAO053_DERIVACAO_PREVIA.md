# Continuação053 — polarizador real, todos os horizontes e liberdade de área
[DERIVED — derivação prévia; nenhum teorema053 compilado]

## Estado e objetivo
A052 foi revalidada em modo somente leitura: PASS selado,94T/17D/111prints,7607arquivos. A ordem vigente continua010; alvoC pede decidir se covariância por horizontes seleciona forma/protocolo. A053 enfrentará TODOS os habitantes TowerHorizon, no espaço de direções efetivas do estado, superando a restrição ao plano052. H3 e a reconstrução geral permanecem OPEN.

## Objetos a construir
Fixar SiteProfile P, H=TowerHilbert P, M=theFactorObject P e ω=omegaState P. Seja R o fecho do subespaço real gerado por AΩ com A autoadjunto em M. Construir o implementador GNS canônico W_h para todo h:TowerHorizon:
W_h(AΩ)=adT(h)(A)Ω.
Não identificar W_h com h.U: este último não precisa fixar Ω. A construção deve pagar extensão, linearidade complexa, isometria, inversa e a igualdade em A global. W_h preserva R.

No Hilbert real R, g0(x,y)=Re〈x,y〉 e Ωq(x,y)=Im〈x,y〉. Definir o polarizador D=-P_R i restrito a R, por projeção ortogonal real. Sua caracterização é g0(x,Dy)=Ωq(x,y). Assim D é linear real, limitado por1 e antiautoadjunto. Uma versão total no Hilbert real ambiente pode ser P_R(-i)P_R, que coincide com D em R. Não chamar D de gerador modular K ou de conjugação J.

Como W_h é isometria complexa e leva R sobre R, comuta com P_R e com i, portanto entrelaça D. Esse argumento deve ser literal para o W_h construído; não assumir uma comutação modular adicional.

## Família que desce às direções do estado
Para ε≥0:
hε(A,B)=g0(D(AΩ),D(BΩ))+ε g0(D²(AΩ),D²(BΩ)).
São formas reais simétricas positivas semidefinidas em geradores autoadjuntos. O alvo global é:
hε(A,A)=0 ↔ D(AΩ)=0 ↔ A∈M^ω.
A segunda equivalência usa a caracterização de Riesz, a densidade real, a conjugação do estado e a decomposição de um B geral em partes autoadjuntas. Não basta provar apenas centralizador→radical.
Isso permite invariância por adição de direções centralizantes e uma forma positiva definida no quociente algébrico. Não se presume uma variedade global de estados nem equivalência uniforme com a norma GNS. As respostas infinitesimais da curva unitária têm o mesmo núcleo centralizante.

Provar hε(adT(h)A,adT(h)B)=hε(A,B) para TODO TowerHorizon. É a família global que sustenta o negativo, não apenas duas matrizes sem vínculo com a torre.

## Cálculo local e controle racional
No prefixo fiel diagonal, o polarizador em autoadjuntos deve satisfazer:
(D_N a)ij=i*(wi-wj)/(wi+wj)*aij.
Essa fórmula calcula o objeto global projetivo; não introduz um segundo D sem ponte. Pode ser paga testando contra todos os autoadjuntos globais via expectativa no prefixo e densidade.

Usar P=thirdThermalReference, p=1/3. O primeiro par é o X,Y do sítio0 da052; g0 tem GramI e D X=(1/3)Y, D Y=-(1/3)X.
O segundo par, no prefixoN=1 com índices00 e11, é:
A2=E00,11+E11,00, B2=-iE00,11+iE11,00.
Seus pesos são1/9 e4/9, g0 tem Gram(5/9)I, Ωq(A2,B2)=-1/3, D A2=(3/5)B2 e D B2=-(3/5)A2.
Ambos os pares são autoadjuntos, horizontais para a expectativa046 efetiva e produzem duas respostas infinitesimais independentes do estado. Não usar a direção verticalZ da proposta051.

Normalizar a mesma família pelo primeiro par:
Hε=hε/[2*(1/9+ε/81)].
No primeiro par, Hε tem Gram(1/2)I e traço1. No segundo par NÃO normalizado GNS:
área(H0;A2,B2)=9/10;
área(H1;A2,B2)=1377/1250;
diferença=126/625>0.
Os valores na base normalizada GNS seriam81/50 e12393/6250; não misturar esses pares. A área é sqrt(detGram), não detGram.

O mesmo estado, a mesma álgebra, os mesmos geradores, o mesmo mapa de resposta e a mesma normalização ficam fixos. As duas formas preservam todos os horizontes, mas divergem no segundo par. Isso decide negativamente a seleção por covariância+essa calibração. Não afirma ausência de outros critérios seletivos, nem que a área GNS já definida na034 tenha deixado de ser única por sua própria definição.

## Alcance e próximo dado
[OPEN] Seleção física de regiões/subálgebras, compatibilidade de inclusões, escala dimensional, dinâmica e H3.
A polarização orientada sign(logΔ) e a calibração pela raiz |D| são caminhos adicionais, ainda distintos desta família hε. Uma análise paralela encontrou possível falha de compatibilidade da calibraçãoΩ sob inclusões não modulares; qualquer uso disso requer prova própria. Não misturar com os teoremas053.
M ser fator não implica R factorial no sentido de subespaço padrão: Ω já está no radical. Positividade de formas imaginárias não é afirmada no Hilbert complexo inteiro.

## Construção, revisão e custódia
Módulos previstos: HorizonGNSImplementation, SymplecticPolarizer, TowerStatePolarizer, LocalPolarizerWitness, CovariantAreaCounterexample. Namespace ChatgptAudit.Covariant053.
Derivação antes de cada fonte; backups exatos antes de revisão; diretórios limpos exclusivos; todas as declarações/instâncias nomeadas com prints; zeroavisos/erros e somente o trio permitido. Revisão cruzada por autoria.
Somente arquivos novos/cópias em Chatgpt. Originais, memórias, Atlas, índice, um.py, kernel e selos≤052 são somente leitura. Nenhuma alteração do gate.

Emissão UTC: 2026-09-07T04:59:15.363400+00:00
