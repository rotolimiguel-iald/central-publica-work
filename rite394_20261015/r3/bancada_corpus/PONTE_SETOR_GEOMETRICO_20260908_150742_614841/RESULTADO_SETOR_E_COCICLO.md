# Setor geométrico: construção finita, obstrução e cociclo relativo

**Ainda não foi obtida uma prova de gravidade quântica.** Este trabalho resolve uma questão matemática delimitada que surgiu na auditoria: como obter uma saída comutativa do colapso sem confundir a álgebra de blocos com a álgebra gerada pelo estado.

[REAL — escopo compilado] 19 teoremas e 10 definições/abreviações no módulo novo, 29 declarações conferidas por impressão de axiomas. Compilação do módulo e de um importador: PASS_COMPILED_SCOPE. [REAL — cálculo racional] 63 verificações exatas adicionais passaram.

A conclusão útil tem duas partes. Existe uma esperança comutativa canônica em cada corte finito. Porém, para a passagem usual de um sítio a dois, ela não retém todo observável do sítio anterior. Um segundo estado, e portanto um cociclo relativo com informação adicional, permite uma construção diferente que distingue os elementos do bloco. Isso é uma possibilidade matemática verificada neste caso; a escolha física do segundo estado permanece aberta.

## 1. A construção positiva no corte finito

[DERIVED — demonstração matemática escrita; a generalidade desta seção não foi compilada em Lean]

Seja ρ uma matriz densidade fiel em dimensão finita, com decomposição espectral

\[
\rho=\sum_{\lambda}\lambda P_\lambda,\qquad
m_\lambda=\operatorname{rank}P_\lambda,\qquad \lambda>0.
\]

A álgebra Aρ=W*(ρ) consiste nas matrizes escalares em cada bloco espectral. Defina

\[
F_\rho(X)=\sum_\lambda
 \frac{\operatorname{Tr}(P_\lambda X P_\lambda)}{m_\lambda}\,P_\lambda.
\]

Esta aplicação tem imagem Aρ e as propriedades necessárias de uma esperança condicional:

1. **Unidade e idempotência.** Fρ(I)=I. Em cada bloco, a média de cλPλ é cλ; portanto Fρ fixa Aρ e Fρ²=Fρ.
2. **Bimodularidade.** Para B,C em Aρ, seus valores em cada bloco são escalares. A fórmula dá Fρ(BXC)=B Fρ(X) C.
3. **Preservação do estado.** Tr(ρFρ(X))=Σλ λ Tr(PλXPλ)=Tr(ρX).
4. **Completa positividade.** Escolha uma base ortonormal apenas para escrever a prova em cada bloco, e ponha Vλ,ij=mλ⁻¹ᐟ²|λ,i⟩⟨λ,j|. Então Fρ(X)=Σλ,i,j Vλ,ij X Vλ,ij*. Essa soma preserva positividade em todas as amplificações, pois cada termo é uma congruência por I⊗Vλ,ij.
5. **Covariância.** Para ρ′=UρU*, as projeções espectrais são P′λ=UPλU* e os postos não mudam. A invariância do traço implica Fρ′(UXU*)=UFρ(X)U*. Não foi escolhida uma base para definir Fρ.
6. **Unicidade no contrato.** Se G é outra esperança condicional ρ-preservante sobre Aρ, escreva G(PλXPλ)=cλPλ usando a bimodularidade. Preservar o estado dá λmλcλ=λTr(PλXPλ). Como λ>0, cλ é o coeficiente da fórmula acima. A bimodularidade anula os blocos cruzados, completando G=Fρ.

A normalidade aqui é automática pela dimensão finita. A caracterização de completa positividade por representações de Kraus e por matriz de Choi é exposta no [teorema2.22 de Watrous](https://cs.uwaterloo.ca/~watrous/TQI/TQI.double.2.pdf), pp.82–84. A aplicação específica e as igualdades acima estão demonstradas nesta nota.

**Distinção essencial:** a esperança por blocos Eρ(X)=ΣλPλXPλ fixa a álgebra {ρ}′. Já Fρ faz também a média interna de cada bloco. Em geral Fρ≠Eρ; de fato Fρ∘Eρ=Fρ. A segunda operação é um passo matemático adicional ao colapso gaussiano que apenas elimina frequências diferentes.

## 2. O que acontece ao acrescentar um sítio

[REAL — cálculo e caso compilado]

Use ρ₀=diag(1/3,2/3) no primeiro sítio e ρ₁=ρ₀⊗ρ₀ nos dois sítios:

\[
\rho_1=\operatorname{diag}(1/9,2/9,2/9,4/9).
\]

A inclusão usual leva P₀=diag(1,0) ao observável

\[
P=P_0\otimes I=\operatorname{diag}(1,1,0,0).
\]

No primeiro sítio, Fρ₀(P₀)=P₀. Nos dois sítios,

\[
F_{\rho_1}(P)=\operatorname{diag}(1,1/2,1/2,0)\ne P.
\]

Logo Fρ₁∘ι ≠ ι∘Fρ₀. Além disso, W*(ρ₀) incluída dessa maneira não está contida em W*(ρ₁): P não é escalar no bloco degenerado 01/10.

O módulo prova que, entre os observáveis locais diag(a,a,b,b), a aplicação retém exatamente aqueles com a=b. As informações locais não constantes são perdidas por essa média.

A aplicação compilada spectralCenterAverage é a fórmula da partição 1+2+1 desse exemplo. Ela não é apresentada como a projeção sobre W*(ρ) em todos os perfis: por exemplo, em p=1/2 há uma degenerescência maior e a verdadeira média espectral seria diferente.

## 3. Teorema de incompatibilidade com hipóteses explícitas

[REAL — compilado; não é uma impossibilidade de toda reconstrução geométrica]

Considere qualquer conjunto S de matrizes 4×4 que satisfaça:

- P=diag(1,1,0,0) pertence a S;
- quaisquer dois elementos de S comutam;
- S é preservado por conjugação por todo unitário que preserva ρ₁.

Essas três condições são incompatíveis. Basta o unitário V que atua como identidade fora do bloco 01/10 e nesse bloco vale

\[
V_{\rm bloco}=\begin{pmatrix}3/5&-4/5\\4/5&3/5\end{pmatrix}.
\]

Ele preserva ρ₁. Por covariância, VPV* pertenceria a S. Mas

\[
(PVPV^*-VPV^*P)_{01,10}=12/25\ne0.
\]

Assim P e VPV* não comutam, contradizendo a segunda condição. Nenhum fechamento algébrico extra é necessário para a contradição.

O teorema Lean [no_state_covariant_commutative_sector_containing_local_seed](<C:/IALD/Central de Patentes/Chatgpt/PONTE_SETOR_GEOMETRICO_20260908_150742_614841/GeometricSectorObstruction.lean:93>) formaliza essa incompatibilidade para a matriz produto parametrizada por p. O corolário [no_state_covariant_commutative_extension](<C:/IALD/Central de Patentes/Chatgpt/PONTE_SETOR_GEOMETRICO_20260908_150742_614841/GeometricSectorObstruction.lean:103>) diz que não existe tal setor que contenha todos os observáveis locais diag(a,a,b,b).

**Alcance:** trata-se de uma seleção que precisa ser invariante sob todos os unitários preservadores do estado considerado. Não se provou impossibilidade de usar dados adicionais, restringir o grupo físico admissível, transportar também um contexto de observação, ou trabalhar com geometria não comutativa. O cociclo relativo merece precisamente essa distinção.

## 4. Um segundo estado resolve a degenerescência neste exemplo

[INPUT — testemunha escolhida, sem alegação de seleção física]

Escolha um segundo estado produto, com pesos 1/4 e 1/5 nos dois sítios:

\[
\sigma=\operatorname{diag}(1/20,1/5,3/20,3/5).
\]

[REAL — aritmética racional] σ é fiel, normalizado e comuta com ρ₁. A densidade relativa é

\[
R=\sigma\rho_1^{-1}
=\operatorname{diag}(9/20,9/10,27/40,27/20).
\]

Seus quatro valores são positivos e distintos. O unitário V anterior não preserva σ: a entrada 01,10 de VσV* vale 3/125, enquanto a de σ é zero. Portanto V deixa de pertencer ao estabilizador do par (ρ₁,σ). A obstrução da seção3 não pode ser aplicada ao par simplesmente ignorando esse novo dado.

[DERIVED — prova finita] Defina a família relativa

\[
u_t=\sigma^{it}\rho_1^{-it}=R^{it}.
\]

A igualdade usa a comutatividade das duas densidades. A família é unitária e satisfaz a identidade de cociclo relativa ao fluxo de ρ₁; neste caso ela é também um grupo, pois seus elementos comutam com ρ₁.

Como os valores de R são distintos, seus logaritmos também o são. Para t positivo suficientemente pequeno, os quatro valores exp(it log rj) são distintos. Logo as projeções sobre cada estado da base podem ser recuperadas por interpolação polinomial em u_t. Consequentemente,

\[
W^*(u_t:t\in\mathbb R)=W^*(R)=\text{álgebra diagonal completa}.
\]

Isso dá uma seleção comutativa capaz de distinguir 01 de 10. Ela retém P e, no exemplo, admite os observáveis diagonais do sítio anterior. A esperança correspondente é a projeção sobre as quatro diagonais.

Sob transporte simultâneo (ρ,σ)↦(UρU*,UσU*), R e suas projeções transportam-se por U; a esperança do setor escolhido transporta-se junto. Assim, a construção é covariante **como função do par**. Não se exige que o mesmo setor fique invariável quando σ é mudado sem ser registrado.

Essa é uma realização finita da ideia de que a informação relativa pode selecionar o setor. Ela não prova:

- que o segundo estado seja determinado pelos postulados iniciais;
- que todos os cortes de uma torre infinita produzam uma escolha compatível, normal e física;
- que o espectro selecionado seja um círculo ou uma variedade 3+1;
- que sua métrica, área e calor satisfaçam as hipóteses da reconstrução de Einstein.

No exemplo finito, o espectro da álgebra diagonal tem quatro pontos. A presença de fases não o transforma automaticamente em S¹.

## 5. Ligação com o acervo existente

A construção não parte da alegação de que “só o estado existe” na TGL. A [densidade de verossimilhança](<C:/IALD/Central de Patentes/Chatgpt/DensityStateUniqueness.lean>) e a [órbita de fase centralizante](<C:/IALD/Central de Patentes/Chatgpt/CentralizerPhaseOrbit.lean>) já são objetos do trabalho anterior.

Esses arquivos foram consultados como fontes existentes. O estado preparado aparece com dados como SummableAmplitude; a fase recebe um gerador. A tarefa subsequente é verificar se os objetos efetivamente escolhidos no modelo fornecem separação espectral e compatibilidade entre cortes, e qual princípio determina a preparação. A testemunha racional desta nota não foi identificada com uma lei física ou com uma rodada canônica desses arquivos.

[OPEN] Mesmo fechando esse setor, continuam necessárias a relação entre distância espectral e angular, a construção geométrica geral, a identificação de área/calor e as hipóteses físicas da reconstrução. O teorema de Einstein já localizado continua sendo uma implicação disponível, não uma conclusão deste lote.

## 6. Evidências, falhas e limites

- [Fonte Lean nova](<C:/IALD/Central de Patentes/Chatgpt/PONTE_SETOR_GEOMETRICO_20260908_150742_614841/GeometricSectorObstruction.lean>).
- [Resultado da compilação](<C:/IALD/Central de Patentes/Chatgpt/PONTE_SETOR_GEOMETRICO_20260908_150742_614841/BUILD_20260908_152430_518457/BUILD_RESULT.json>) e [log integral](<C:/IALD/Central de Patentes/Chatgpt/PONTE_SETOR_GEOMETRICO_20260908_150742_614841/BUILD_20260908_152430_518457/GeometricSectorObstruction.log>).
- [63 verificações racionais e testemunha relativa](<C:/IALD/Central de Patentes/Chatgpt/PONTE_SETOR_GEOMETRICO_20260908_150742_614841/TESTEMUNHA_EXATA.json>).
- [Auditor de compilação](<C:/IALD/Central de Patentes/Chatgpt/PONTE_SETOR_GEOMETRICO_20260908_150742_614841/build_geometric_sector.py>) e [cálculo exato](<C:/IALD/Central de Patentes/Chatgpt/PONTE_SETOR_GEOMETRICO_20260908_150742_614841/exact_relative_selector.py>).
- [Inventário final](<C:/IALD/Central de Patentes/Chatgpt/PONTE_SETOR_GEOMETRICO_20260908_150742_614841/VERIFICACAO_FINAL.json>).

As tentativas anteriores permanecem na pasta: houve um timeout inicial, um import inexistente e metas de simplificação não resolvidas antes do build identificado acima. Logs com erros ou dependência de sorryAx pertencem às tentativas falhas e não sustentam este resultado. Somente o build PASS e seu hash corrente sustentam a indicação “compilado”.

A completa positividade geral da seção1 e a reconstrução pela família relativa da seção4 são provas matemáticas escritas. O Lean deste lote cobre os enunciados do módulo, incluindo a obstrução universal sob suas hipóteses e as propriedades algébricas indicadas da média 4×4; não se atribui ao compilador uma formalização mais ampla.

O compilador e os imports diretos de Mathlib foram usados por leitura e identificados por hashes. As dependências transitivas da biblioteca não foram todas recompiladas nem todas hasheadas. A inspeção de axiomas está limitada às declarações novas. Não houve revisão científica independente deste lote; ele não é uma custódia canônica nem altera o gate.

Todas as escritas ficaram na nova pasta sob Chatgpt. As revisões dos arquivos novos preservaram backups imediatos de bytes; nenhum original do acervo, Atlas, índice ou memória canônica foi modificado.

**Estatuto final:** avanço matemático delimitado, com uma saída relativa finita e uma obstrução precisa à escolha baseada apenas no estado. Gravidade quântica e reconstrução gravitacional geral permanecem [OPEN].
