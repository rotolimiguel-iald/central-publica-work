# Continuação053 — polarizador real e não unicidade da área covariante

[REAL — alcance das declarações compiladas e auditadas] Emissão UTC: 2026-09-07T05:59:33.323944+00:00

O lote constrói formas reais bilineares para o mesmo estado da torre e prova sua covariância por todos os TowerHorizon admitidos. No setor dos operadores autoadjuntos limitados do fator, o radical dessas formas coincide exatamente com o centralizador e com o núcleo de todas as respostas infinitesimais do estado. Duas formas recebem a mesma calibração de traço no primeiro par de Pauli e dão densidades de área diferentes sobre um mesmo segundo par efetivo. Portanto, covariância por esses horizontes mais essa calibração não selecionam uma única forma. H3 e reconstrução gravitacional geral permanecem [OPEN].

## Implementação GNS da ação de cada horizonte

Fixar um SiteProfile P, H=TowerHilbert P, M=theFactorObject P, o vetor Ω=hOmega P e o estado ω=omegaState P. Cada h:TowerHorizon P já possui uma ação adT(h) sobre M que preserva ω. A053 constrói um implementador complexo-linear, isométrico e bijetivo W_h em H, com:

    W_h(AΩ) = adT(h)(A)Ω, para todo A∈M;
    W_h Ω = Ω;
    W_h⁻¹ = W_(h.inv).

A construção começa no pré-Hilbert local, verifica a compatibilidade dos representantes e estende por completamento. A fórmula para um A geral do fator é demonstrada pelo limite das esperanças de prefixo e pela preservação da distância GNS. Não se presume que o implementador original h.U fixe Ω, nem se identifica h.U com W_h.

Definir R como o fecho do span REAL dos vetores AΩ com A∈M autoadjunto. Este é o mesmo realStateSubspace em todos os módulos053. W_h leva R sobre R. A inversa e a invariância desse espaço são provadas, não hipóteses adicionais dos exemplos locais.

## Polarizador efetivo e família de formas

Considerar H como espaço de Hilbert real com produto g₀(x,y)=Re〈x,y〉. A projeção ortogonal real P_R define o operador limitado:

    D = P_R ∘ (−i) ∘ P_R.

Sobre R, sua caracterização é:

    Re〈x,Dy〉 = Im〈x,y〉, para x,y∈R.

D tem norma no máximo um e é antissimétrico para o produto real. Sua definição não é a de um gerador modular nem a de uma conjugação antilinear J. A projeção e o polarizador entrelaçam o W_h efetivamente construído, porque W_h é complexo-unitário e preserva R.

Para ε≥0, definir:

    hε(A,B) = Re〈D(AΩ),D(BΩ)〉
              + ε Re〈D²(AΩ),D²(BΩ)〉.

stateCovariantBilinear é uma aplicação REAL bilinear no ambiente dos operadores limitados B(H); não é bilinear sobre ℂ. A simetria e a positividade semidefinida são provadas a partir da expressão:

    hε(A,A) = ‖D(AΩ)‖² + ε‖D²(AΩ)‖² ≥ 0.

A classificação do radical abaixo tem quantificadores mais estreitos: refere-se a A autoadjunto e pertencente a M. Não se transporta essa classificação para todos os operadores ou todos os vetores do Hilbert.

## Radical, respostas e descida às direções efetivas

Para ε≥0 e A∈M autoadjunto, os teoremas demonstram:

    hε(A,A)=0  ↔  D(AΩ)=0  ↔  A∈M^ω,
    hε(A,A)>0 ↔ A∉M^ω.

Aqui M^ω é o centralizador definido pela condição ω(AB)=ω(BA) para todo B∈M. A direção inversa, de nulidade do polarizador para centralização, usa todos os testes autoadjuntos, a densidade real e a decomposição de um B geral em suas partes autoadjuntas.

A resposta usada é a derivada da leitura do mesmo estado pela curva unitária já definida na bancada. Para A,B autoadjuntos:

    resposta(A;B) = d/dt Re ω(U_A(t)* B U_A(t)) em t=0
                 = −2 Im ω(BA),  U_A(t)=exp(i t A).

O núcleo de todas essas respostas, com B variando nos autoadjuntos de M, é exatamente M^ω. Logo o radical das formas coincide com as direções que não alteram infinitesimalmente nenhuma dessas leituras.

Os lemas de descida provam literalmente invariância por adição centralizante em cada entrada:

    hε(A+C,B)=hε(A,B),   hε(A,B+C)=hε(A,B),

quando C é autoadjunto no centralizador. O mesmo vale para a família normalizada. [DERIVED] Essas identidades e a classificação do radical permitem a leitura como forma positiva definida no quociente algébrico dos geradores autoadjuntos pelas direções centralizantes. O lote não constrói uma variedade global de estados, nem uma métrica de espaço-tempo ou uma norma tangente uniformemente equivalente à GNS.

## Covariância por todos os horizontes admitidos

O entrelaçamento do polarizador com W_h implica:

    hε(adT(h)A, adT(h)B)=hε(A,B),

para todo h:TowerHorizon P e A,B∈M. A construção geral vale para qualquer SiteProfile P; os testemunhos racionais de não unicidade abaixo usam a referência thirdThermalReference.

Não é uma invariância limitada a um quarto de volta ou a um subconjunto de horizontes. Tampouco se exige uma nova comutação com Δ como hipótese: usa-se a ação GNS canônica e a projeção real. Isso não escolhe quais dos TowerHorizon devem representar horizontes físicos ou regiões de espaço-tempo.

## Cálculo local ligado ao polarizador global

Para um prefixo fiel diagonal de pesos w_i, a fórmula matricial em autoadjuntos é:

    (D_N a)_ij = i (w_i−w_j)/(w_i+w_j) · a_ij.

Os denominadores são positivos. A identidade state_polarizer_local liga essa matriz ao D global aplicado a towerPi(a)Ω. O vínculo é provado por pareamentos e pela esperança no prefixo; não se introduz uma matriz conveniente sem relação com o operador global.

Fixar agora thirdThermalReference, com peso de cada sítio p=1/3. O primeiro par é X₁=sitePauliX P 0, Y₁=sitePauliY P 0, já identificado com direções efetivas do estado. Seu Gram real GNS é I₂ e:

    D(X₁Ω)=(1/3)Y₁Ω,   D(Y₁Ω)=−(1/3)X₁Ω.

O segundo par pertence ao prefixo N=1, que contém dois sítios. Nos índices 00 e 11, de pesos 1/9 e 4/9, definir:

    A₂=E_(00,11)+E_(11,00),
    B₂=−i E_(00,11)+i E_(11,00).

Na torre, esses são doubleFlipX e doubleFlipY. O Gram real GNS do par é (5/9)I₂, Im ω(A₂B₂)=−1/3, e:

    D(A₂Ω)=(3/5)B₂Ω,   D(B₂Ω)=−(3/5)A₂Ω.

Os dois elementos são autoadjuntos em M e são zerados pela expectativa centralizante efetiva da046. Para a combinação u₀A₂+u₁B₂, as leituras em A₂,B₂ têm resposta (2u₁/3,−2u₀/3), uma aplicação injetiva. Portanto a diferença de áreas compara direções efetivas, sem usar uma direção vertical centralizante para fabricar a liberdade.

## Mesma calibração, áreas distintas no mesmo par

A família global é normalizada pelo primeiro par:

    Hε = hε / [2(1/9+ε/81)],  ε≥0.

O fator é estritamente positivo. O Gram no primeiro par é (1/2)I₂ para todo ε≥0: traço um e a mesma calibração. Antes dessa normalização, os Grams são:

    Gram(hε;X₁,Y₁) = (1/9+ε/81) I₂,
    Gram(hε;A₂,B₂) = (1/5+9ε/125) I₂.

O segundo par A₂,B₂ permanece fixo e NÃO é reescalado para norma GNS um. A área é a raiz quadrada do determinante do Gram, e não o determinante:

| Forma | Gram no primeiro par | Gram no segundo par bruto | Área no segundo par bruto |
|---|---|---|---:|
| H₀ | (1/2)I₂ | (9/10)I₂ | 9/10 |
| H₁ | (1/2)I₂ | (1377/1250)I₂ | 1377/1250 |

A diferença de áreas é 126/625>0. O lema normalized_forms_not_global_rescaling exclui que H₁ seja qualquer múltiplo escalar global de H₀. A igualdade da calibração no primeiro par impede atribuir a diferença a uma simples escolha comum de unidade.

O teorema two_global_covariant_calibrated_forms reúne duas formas reais bilineares distintas, simétricas e positivas semidefinidas, invariantes por todo TowerHorizon da referência, com o mesmo radical centralizante no setor autoadjunto, a mesma primeira calibração e as duas áreas sobre o mesmo segundo par, cuja resposta é injetiva.

[INPUT] O traço um no primeiro par é o critério de calibração testado. O resultado é a sua insuficiência em conjunto com a covariância. Não afirma que todo critério adicional falha nem que uma área literalmente definida como GNS em outro lote deixe de ser determinada por essa definição.

## O que o resultado muda — e o que continua aberto

A liberdade demonstrada sobrevive à exigência de todos os horizontes admitidos e à remoção das direções sem resposta. Isso é mais forte que escolher dois pesos em uma decomposição abstrata ou permanecer dentro de um único plano com uma escala livre.

As formas Hε são construídas de D e D². Elas são distintas de uma calibração por |D| ou por uma fase polar orientada; tais critérios não são selecionados por este teorema. Não se identifica D com uma transformação da álgebra inteira em si. A parte imaginária do estado atua no setor real apropriado, sem positividade afirmada para uma forma complexa bilinear.

[OPEN] Selecionar fisicamente estado, álgebra, regiões e observadores; justificar um critério adicional de forma e sua compatibilidade com inclusões; fixar escala dimensional de área; vincular área, matéria, relógio e Ricci em H3; reconstruir geometria lorentziana e dinâmica geral. O resultado053 é um controle de não unicidade sob hipóteses explícitas, não uma prova de impossibilidade de qualquer reconstrução física.

## Compilação, revisão e custódia

| Módulo053 | Teoremas | Definições | Instâncias | Prints | Alcance |
|---|---:|---:|---:|---:|---|
| [HorizonGNSImplementation.lean](<C:/IALD/Central de Patentes/Chatgpt/HorizonGNSImplementation.lean>) | 28 | 8 | 1 | 37 | Implementador GNS de todo horizonte e preservação do setor real fechado. |
| [SymplecticPolarizer.lean](<C:/IALD/Central de Patentes/Chatgpt/SymplecticPolarizer.lean>) | 19 | 3 | 0 | 22 | Projeção real, polarizador, formas reais bilineares e covariância. |
| [TowerStatePolarizer.lean](<C:/IALD/Central de Patentes/Chatgpt/TowerStatePolarizer.lean>) | 20 | 4 | 0 | 24 | Vínculo à torre; radical centralizante, respostas e descida por adições. |
| [LocalPolarizerWitness.lean](<C:/IALD/Central de Patentes/Chatgpt/LocalPolarizerWitness.lean>) | 33 | 8 | 0 | 41 | Fórmula local do polarizador global e dois pares efetivos no mesmo estado. |
| [CovariantAreaCounterexample.lean](<C:/IALD/Central de Patentes/Chatgpt/CovariantAreaCounterexample.lean>) | 23 | 2 | 0 | 25 | Calibração comum e duas densidades distintas sem reescala global. |

Total053: 123 teoremas, 25 definições, 1 instâncias nomeadas, 149 prints. Lote final: 6/6 etapas, incluindo Imports053All. O auditor verificou zero avisos/erros, ausência de sorryAx, cobertura exata das declarações e somente propext, Classical.choice e Quot.sound nos prints.

Diretório final: C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_CLEAN_20260907_054322_083933

Build SHA256: 22c939a03d19293f2f7f1a5e49690590bc57a9ef576c42c25e7c500ed3219d3c

A revisão independente final está ligada a esse hash e diretório. A revisão de infraestrutura [CONTINUACAO053_REVISAO_INFRA_NEWTON.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_REVISAO_INFRA_NEWTON.md>) registra leitura dos scripts, replay de evidências052 e controles negativos em memória; ela tem o alcance e os hashes da data de sua emissão. Alterações posteriores, se registradas na revisão final, não são retroativamente atribuídas àquela nota.

Os cinco fontes053 foram copiados por bytes e compilados em diretório exclusivo. As dependências históricas foram pinadas e copiadas, não recompiladas nesta rodada. O auditor reconstitui os vínculos upstream045 e os registros históricos, inclusive052. Imports externos que cruzam a fronteira local e seus companheiros binários são medidos; não se afirma reconstrução exaustiva do fecho externo. Fontes lidas apenas para descobrir imports não recebem por isso uma proveniência fonte→binário.

Sondas falhas, logs e backups são preservados como história, sem valor de prova. O gerador e o auditor não transformam revisão documental em validação física. Somente Chatgpt recebe as escritas deste lote; canonical_gate_changed=false descreve esse escopo. Atlas, índice, um.py, kernel e memórias canônicas não são incorporados ou alterados por esta emissão.

Revisão final: [CONTINUACAO053_REVISAO_INDEPENDENTE.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO053_REVISAO_INDEPENDENTE.md>). Entrega: [ENTREGA_053_polarizador_e_area_covariantes.md](<C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ENTREGA_053_polarizador_e_area_covariantes.md>). A selagem ocorre separadamente após os documentos; o manifesto não é hash autorreferente. QG não é declarada confirmada, resolvida ou provada.
