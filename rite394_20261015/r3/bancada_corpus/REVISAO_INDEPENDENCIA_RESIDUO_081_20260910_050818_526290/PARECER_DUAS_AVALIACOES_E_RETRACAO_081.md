# Parecer081: duas avaliações e um submódulo livre cindido

10/09/2026. Revisor /root/selected_geometry_design. Revisão matemática escrita nova, sem execução aritmética, CAS, Lean ou um.py e sem alteração de fontes.

**Parecer favorável no alcance declarado; não identifiquei erro material.** Li integralmente [DUAS_AVALIACOES_E_SUBMODULO_LIVRE_E6.md](<C:/IALD/Central de Patentes/Chatgpt/INDEPENDENCIA_RESIDUO_E_IMAGEM_081_20260910/DUAS_AVALIACOES_E_SUBMODULO_LIVRE_E6.md>) e seu manifesto. Fonte medida: 5696 bytes, SHA-256 9d9f3a5553127e3d734552c676afea4cabab89d8d4ccb95ca3edd1d87684cb52.

Li também a nota do candidato quadrático para conferir o domínio, o fechamento e as fórmulas consumidas, além de seu recibo histórico. Esta revisão prova a consequência de duas avaliações; não é uma reexecução dos14 controles daquele recibo nem nova auditoria completa do script do candidato.

## 1. Aplicações sobre cohomologia

A fonte preserva o complexo natural métrico mínimo da referência Lorentziana espaço-forma fixada, com K>0, φ0 constante, κ real não nulo, quatro dimensões e orientação. Os perfis das avaliações satisfazem a equação Einstein linearizada e todos os prolongamentos; os ghosts são combinações dos quatro Killing, e os antifields são zerados após o diferencial.

Assim a avaliação de s0 sobre cada gerador e cada jato é zero. Por Leibniz, a avaliação anula s0 sobre todo cochain finito. A diferença ímpar Lk também anula fronteiras; portanto ℓk está bem definida em H⁴(A6,s0). Essa aplicação é linear sobre o mesmo Rher, porque os coeficientes herdados são mantidos e não são funções do parâmetro de teste k.

Os testes k1=1/z0 e k2=2/z0 usam o mesmo fundo, ponto, orientação e normalização f(z0)=0, f'(z0)=1. z0=ℓ>0 está fixado. Mudar k não muda o cochain a ou b nem introduz um coeficiente dependente da solução no modelo.

## 2. Fórmulas de entrada e matriz

A nota do candidato define b5=κJβ, universalmente s0-fechado. Sua imagem b=[s1b5] é um ciclo de ghost4/E6 por s0s1+s1s0=0. Em C5, b5 pertence a Kcal e sua conexão é precisamente b; logo b∈δ(Kcal).

As fórmulas utilizadas pela nova nota são
ℓk(a)=−4k/z0,
ℓk(b)=κ(24k³/z0−96k/z0³).
Elas coincidem com a fonte de avaliação e os termos registrados no recibo. O sinal do candidato inclui a variação CE de β; a nova nota não a omite nem acrescenta um fator dois ao detector ímpar.

Conferi diretamente as substituições:
- em k1, ℓ1(a)=−4/z0² e ℓ1(b)=κ(24−96)/z0⁴=−72κ/z0⁴;
- em k2, ℓ2(a)=−8/z0² e ℓ2(b)=κ(24·8−96·2)/z0⁴=0.

A matriz, com colunas a e b, é
M=[[-4/z0²,−72κ/z0⁴],[-8/z0²,0]].
Seu determinante é
0−[(-72κ/z0⁴)(-8/z0²)]=−576κ/z0⁶.
A ordem das colunas e o sinal estão corretos.

## 3. Anel e retração

Rher é uma álgebra real UNITAL e NÃO NULA. Como κ e z0 são números reais fixados e não nulos, todos os divisores da matriz inversa são unidades da álgebra. Não se depende de avaliações numéricas que separassem nilpotentes; o argumento é uma identidade no próprio módulo. A hipótese de não nulidade evita chamar o módulo zero de posto dois.

Para
r(x)=(-z0²ℓ2(x)/8, z0⁴[ℓ2(x)/2−ℓ1(x)]/(72κ)),
conferi:
r(a)=(1,0), pois ℓ2(a)/2−ℓ1(a)=0;
r(b)=(0,1), pois ℓ2(b)=0 e −ℓ1(b)=72κ/z0⁴.

Portanto r i=Id para i(λ,μ)=λa+μb. A injetividade de i e a decomposição em soma direta seguem explicitamente: todo x é i(r(x))+(x−i(r(x))), o segundo termo está em ker r, e a interseção dos dois somandos é zero. Não se necessita finitude, liberdade ou conhecimento do complemento.

A consequência é um submódulo livre cindido Rher² de H⁴, no domínio fixado. Sobre Rher=R, dá dimensão pelo menos dois. Não há afirmação topológica ou decomposição de uma representação física global.

## 4. Exclusão exata obtida e o que não segue

Como a e b são independentes, a e −a não pertencem à linha Rher b, inclusive após acrescentar fronteiras s0. Logo um múltiplo escalar herdado do candidato apresentado não cancela o resíduo. Isso é mais forte que comparar um único valor numérico, mas continua uma exclusão de UMA linha.

A fonte não afirma que a esteja fora de δ(Kcal) inteiro. Em particular, não prova que ℓ2 anule d1 de todos os quadráticos de Weyl. A condição ℓ2(d1[z5])=+8/z0² é somente um filtro necessário para cancelar a; outros candidatos e seus jatos permanecem possíveis.

A divisão por κ em r pertence à aplicação externa de teste, na fibra com κ fixado. Não foi inserida numa primitiva ou num contratermo, e não certifica admissibilidade causal, dependência permitida em acoplamentos variáveis ou preservação de scaling degree/contatos. Se κ fosse variável não invertível de outro anel, a conclusão cindida por essa fórmula exigiria novo contrato.

## 5. Custódia e conclusão

Os pins do manifesto e os links foram conferidos, e os arquivos lidos permaneceram idênticos antes/depois. A comparação dos termos do recibo foi uma leitura de dados; não uma execução dos controles. O writer da nova nota foi somente pinado em bytes.

[DERIVED] As duas avaliações fornecem a independência e a retração afirmadas; não encontrei errata material. [OPEN] Imagem completa de d1, cancelamento de −a, prolongamentos superiores, QME, admissibilidade causal, UV e reconstrução gravitacional geral. Investigação082 não integra esta revisão.

O registro anexo separa verificações documentais,14 controles históricos do antecedente e zero novas execuções aritméticas/Lean.
