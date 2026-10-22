# A obstrução seguinte é uma classe CE; uma corrente horizontal explícita

10/09/2026. [DERIVED — demonstração escrita da raiz, pendente de revisão independente]. Esta nota082 usa o domínio fixado080/081: referência Einstein espaço-forma orientada em quatro dimensões, K>0 e κ real não nulo fixos, projeção métrica com φ0 constante e extensão por escalares herdados inertes Rher. Nenhum arquivo anterior foi alterado. Zero execução matemática ou Lean nesta nota.

**Resultado.** A classe a=[A6], não nula na cohomologia de s0, é um cociclo para o diferencial seguinte. A questão do cancelamento completo passa a ser a nulidade de sua classe na cohomologia de Chevalley–Eilenberg com coeficientes quadráticos de Weyl, no subcomplexo invariante pela isotropia. Essas são DUAS cohomologias diferentes. Uma corrente com gradiente do pseudoscalar quadrático fornece uma imagem explícita, envolvendo □bar J_W; isso não a identifica com A6.

## 1. Do alvo em H(s0) à classe seguinte

Use o [isomorfismo de complexos082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>), com N=Sym²M e M o módulo de jatos lineares de Weyl modulo EOM. M não é livre nem foi provado localmente finito para toda a álgebra g de Killing. Ponha

Cnat^q = Rher ⊗ C^q(g,N)^h,
h = so(1,3),
ν(p) = ε_abcd p^a p^b p^c p^d / 4!,
J_W = tr(W1∧W1) / vol_g0.

Aqui ε é o tensor volume de g0, p=C é o ghost de valor e a matriz Mghost=antisym(∇bar C) da nota CE não deve ser confundida com o módulo M. A letra J_W tem esta definição local; não designa a involução canônica J=Luz.

O alvo de078 corresponde precisamente a

a = J_W ν(p) ∈ Cnat^4.

Em coordenadas orientadas, ν(p)=sqrt(|det g0|) C0 C1 C2 C3; logo J_Wν(p) tem o mesmo coeficiente ρ de A6. Não se suprimiu o fator volume.

Como J_W é pseudoscalar para o grupo orientado, a ação de isotropia nele é zero. As fórmulas082 dão

dCE J_W = p^e ∇bar_e J_W,
dCE p = −Mghost p.

No produto dos quatro p, a ação da matriz é −tr(Mghost)ν(p)=0. O termo de transporte tem cinco p em dimensão quatro e também é zero. Portanto

                         dCE a = 0.                         (1)

Isso não usa EOM além das relações que definem N. Equivalentemente, a forma natural ativa tr(W(g)∧W(g)), avaliada nos quatro ghosts, é BRST-fechada; sua primeira equação após s0A6=0 dá a mesma nulidade de d1[A6].

Pela [transferência080](<C:/IALD/Central de Patentes/Chatgpt/TRANSFERENCIA_DELTA_PARA_E5_080_20260910/IMAGEM_DELTA_E_PRIMEIRO_DIFERENCIAL_E5.md>), δ(Kcal)=im d1E5. Assim

−[A6] ∈ im d1E5
       ⇔ a ∈ dCE(Cnat^3)
       ⇔ [a]_CE = 0 em H⁴(Cnat,dCE).                        (2)

O sinal menos não altera a condição de pertinência a uma imagem linear. O primeiro [A6] vive em H⁴(s0)E6; o segundo [a]_CE vive na cohomologia do diferencial seguinte, já nesse primeiro grupo. A não nulidade demonstrada078 de [A6] não decide a não nulidade de [a]_CE. A imagem não nula encontrada081 também não decide (2).

A equivalência é no complexo natural fixado. Uma solução ali ainda precisa satisfazer restrições adicionais de admissibilidade causal, se forem impostas pelo problema completo. O grau seguinte da torre e as demais anomalias tampouco são pagos por (2).

## 2. Uma corrente horizontal produz a divergência como imagem

Se V é um vetor quadrático dos jatos, invariante por contração natural e com a ação tensorial de082, defina a cocadeia horizontal

q_V = ε_abcd V^a p^b p^c p^d / 3!.

Horizontal significa que ela usa p e não Mghost. Isso descreve esta família específica; não retira os ghosts de isotropia do complexo Cnat geral. Pela regra graduada,

dCE V^a = p^e ∇bar_e V^a − Mghost^a_b V^b.

As parcelas de Mghost se cancelam na contração com o tensor volume: somar as ações nos quatro índices é sua ação total, que vale zero. A parcela restante é

ε_abcd (∇bar_e V^a) p^e p^b p^c p^d / 3!
       = (∇bar_a V^a) ν(p).

O sinal é positivo; por exemplo, a=e=0 dá +∇bar_0 V^0 p0p1p2p3, e os sinais das outras três posições são compensados pela reordenação dos ghosts. Logo

                  dCE q_V = (div_bar V) ν(p).               (3)

Não há integração por partes nem quociente por derivadas totais nesta igualdade. Ela é uma igualdade entre cocadeias pontuais. Também não é uma aplicação do lema de Poincaré a uma categoria de primitivas maior.

Escolhendo V=∇bar J_W, obtemos um candidato concreto de E5 e ghost3:

q_grad = ε_abcd (∇bar^a J_W) p^b p^c p^d / 3!,
                 dCE q_grad = (□bar J_W) ν(p).              (4)

J_W é quadrático em Weyl, portanto q_grad tem um total de uma derivada covariante adicional nos dois fatores. Ele está fora do setor sem derivadas excluído082. O fechamento s0q_grad=0 é off-shell, pois s0W1=0 e a conexão de referência é inerte. Sua engenharia é dois; se for exigida engenharia zero, tomar κq_grad, com κ herdado inerte e dimensão −2. A identidade (4) recebe o mesmo fator κ dos dois lados.

## 3. A identidade tem uma realização BRST finita antes da cohomologia

Defina no campo métrico completo

𝒥(g) = tr(W(g)∧W(g)) / vol_g,
Ω3(g) = ι_(grad_g 𝒥(g)) vol_g,
F(g,c) = Ω3(g)_abc c^a c^b c^c / 3!.

Ω3 é uma três-forma natural. Para qualquer forma natural α(g), com sg=Lie_c g e sc=c·∂c, vale

s (α(g)(c,...,c)/r!) = (d_H α(g))(c,...,c)/(r+1)!.          (5)

A verificação de (5) expande Lie_c α: os termos ∂c em cada índice cancelam os termos em que s atua nos ghosts; o termo c·∂α antis simetriza a derivada exterior. Os sinais usam ghosts à esquerda com a convenção já fixada076. Não se confunde d_H com s; (5) é o entrelaçamento por avaliação em ghosts de uma forma NATURAL ATIVA.

Como d_H Ω3=(□_g 𝒥(g))vol_g, segue

s F(g,c) = (□_g 𝒥(g)) vol_g(c,c,c,c)/4!.                  (6)

Na expansão g=g0+t h, c=tC, temos 𝒥=t²J_W+O(t³), e

F = t⁵q_grad + t⁶q6 + ...,
s_t = s0 + t s1 + ... .

O coeficiente de t⁶ em (6) dá a identidade finita

           s1 q_grad + s0 q6 = (□bar J_W) ν(C).              (7)

Aqui q6 é definido explicitamente como [t⁶]F(g0+t h,tC). É um polinômio natural de ordem finita de jatos: grad da curvatura usa no máximo três derivadas de h, e a expansão de inversas e do volume em um coeficiente fixado é finita. Não se usa uma soma infinita de jatos no mesmo coeficiente. O termo q6 pertence à espécie h³C³, ghost3/valência6, exatamente a espécie necessária à fronteira s0 de ghost4/valência6.

Assim (4) não se baseia apenas em uma avaliação TT. Ela segue de uma identidade no complexo original com sua correção s0 conservada. Não se declara que q_grad cancela o resíduo: seu resultado é □bar J_W, e o alvo é −J_W. Igualá-los exige outra demonstração.

## 4. Alcance do filtro sem derivadas e próxima decisão

A [exclusão finita082](<C:/IALD/Central de Patentes/Chatgpt/SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779/IMAGEM_DO_DETECTOR_NO_SETOR_FINITO.md>) mostra que o detector em k=2/z0 anula dCE de todo o setor de dez contrações sem derivadas. Ele não anula a priori a imagem de q_grad nem de outros candidatos com derivadas. A direção (4) é uma família concreta a examinar, sem fingir uma classificação completa.

[OPEN] Decidir (2), ou construir uma combinação admissível e uma primitiva finita que paguem r6+s1Q=s0a6. Esta nota não calcula □bar J_W na família TT, não adota uma equação de onda para Weyl por memória, não conclui que o candidato passa no detector e não decide a classe CE. A investigação083 fica separada.

[REAL — documental] Os pins do manifesto são lidos das cinco fontes antes/depois. Esta nota é matemática escrita; nenhum cálculo CAS, controle algébrico executado ou Lean é atribuído a ela. Originais, Atlas, índice, memórias canônicas e gate permanecem intactos.
