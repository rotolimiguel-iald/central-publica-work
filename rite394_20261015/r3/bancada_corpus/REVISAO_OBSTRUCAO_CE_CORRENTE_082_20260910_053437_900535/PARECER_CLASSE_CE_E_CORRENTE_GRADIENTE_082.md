# Parecer independente — classe CE e corrente gradiente 082

[DERIVED — revisão matemática escrita]. [REAL — fontes lidas e pins medidos]. Não identifiquei erro material no alcance da [nota da raiz](<C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md>). O resultado diferencia corretamente a classe em H(s0), a cohomologia do diferencial seguinte e a realização finita da corrente gradiente.

Li integralmente a nota, o manifesto, a identificação CE082, a transgressão076 e a transferência080. A redução081 e a normalização do certificado078 são antecedentes já examinados nesta tarefa; a definição e o alcance de A6 foram novamente conferidos nos trechos pertinentes. Não executei fontes, CAS, Lean ou um.py. A leitura do escritor limita-se à medição de seus bytes, não à sua execução nem a uma aprovação geral de implementação.

## 1. Normalização e os dois grupos de cohomologia

A definição usa a curvatura de Weyl como dois-forma com valores em End(TM), com o polinômio P(X,Y)=tr(XY) de078. Se tr(W1∧W1)=ρ dx0∧dx1∧dx2∧dx3, então J_W=ρ/√|det g0|. Por outro lado,

ν(C) = ε0_abcd C^a C^b C^c C^d/4!
     = √|det g0| C0 C1 C2 C3

em coordenadas orientadas. Portanto J_Wν(C)=ρ C0 C1 C2 C3 coincide com A6. Não há fator de volume omitido, dupla contagem de 4! ou importação silenciosa da normalização topológica −1/(8π²).

O módulo de coeficientes é N=Sym²𝓜, com 𝓜 o quociente de jatos de Weyl pelas relações lineares de EOM. O complexo usado é C•(g,N)^h, estendido por Rher, e não o CE relativo que suprimiria os ghosts de isotropia. A identificação082 conserva as fronteiras s0: em particular, os termos s0p2, s0k2 e s0T̃r,2 justificam a passagem das fórmulas de campos livres às classes.

No grupo orientado, J_W tem ação escalar trivial da isotropia. Assim dCE J_W=p·∇bar J_W. Em dCEν, a ação em todos os índices é −tr(Mghost)ν=0. O transporte de J_W multiplicado por ν tem cinco ghosts de valor em dimensão quatro e se anula. Logo a=J_Wν é efetivamente um cociclo CE.

Isso é compatível com s0A6=0, mas é uma afirmação adicional: a primeira classe pertence a H⁴(s0)E6; sua classe posterior pertence a H⁴(Cnat,dCE). A não nulidade da primeira não força a não nulidade da segunda.

## 2. Equivalência exata da obstrução neste corte

A transferência080 fornece δ(𝒦)=im d1 em E5. A identificação de complexos082 identifica esse d1 com dCE, tanto no domínio H³(s0)E5 quanto no alvo H⁴(s0)E6. Com o fechamento de a verificado, segue precisamente

−[A6] ∈ im d1  ⇔  a ∈ dCE(Cnat³)  ⇔  [a]CE=0.

O sinal menos não importa para pertinência a uma imagem linear. Não foi invertida a conclusão da avaliação078, nem foi tomado δ(𝒦)≠0 como prova de que a pertence à imagem.

A equivalência decide, se sua condição for resolvida, somente o passo C5→C6 que preserva o líder especificado. As primitivas continuam na categoria natural de ordem finita do complexo fixado. A nota não substitui esse problema por cochains suaves arbitrários, por uma média da álgebra inteira ou por um teorema de Whitehead. Admissibilidade causal e prolongamentos posteriores permanecem condições distintas.

## 3. Divergência e o sinal da corrente

Para qV=ε0_abcd V^a p^b p^c p^d/3!, os coeficientes V são pares e quadráticos em jatos. As fórmulas dCE V^a=p^e∇bar_eV^a−Mghost^a_bV^b e dCEp=−Mghost p são compatíveis com a definição de Mghost da nota CE, que coincide com A=∇C em Killing. Esse Mghost tem sinal oposto ao m covariante elevado da nota finita de Turing; a nota da raiz o distingue.

As parcelas de Mghost se cancelam pela invariância do tensor volume. Na parte restante,

ε0_abcd (∇bar_eV^a)p^ep^bp^cp^d/3!
= (∇bar_aV^a)ν(p).

Conferi o sinal positivo: quando e=a, a reordenação de p^a até sua posição orientada compensa o sinal de ε; quando e não é a, há repetição de algum ghost e o termo é zero. O fator 3! cancela as seis permutações dos outros índices.

A identidade é pontual entre cocadeias; não usa integração por partes ou igualdade módulo derivadas totais. Ao tomar V=grad_bar J_W, obtém-se dCEqgrad=(□bar J_W)ν. Como s0W1=0 off-shell e a referência é inerte, s0qgrad=0 também é uma identidade off-shell. O candidato tem ghost3, valência5, uma derivada adicional de um produto de dois Weyl e engenharia dois; κqgrad tem engenharia zero na convenção declarada.

## 4. Entrelaçamento da forma ativa com BRST

Verifiquei a identidade geral que a nota usa para uma forma natural ativa α(g). Se α̂=α_a1…ar c^a1…c^ar/r!, então sg=Lie_cg e sc=c·∂c dão

sα̂ = (d_Hα)_a0…ar c^a0…c^ar/(r+1)!.

Os termos ∂c de Lie_cα cancelam, com a regra graduada, os termos em que s age nos próprios ghosts. O transporte c·∂α produz a derivada exterior antissimetrizada com o fator indicado. A afirmação requer naturalidade ATIVA: não valeria apenas por chamar α uma forma que depende de uma referência inerte arbitrária.

Para Ω3(g)=ι_(grad_g𝒥(g))vol_g, a identidade geométrica exata é d_HΩ3=(□g𝒥(g))vol_g. Portanto sF=(□g𝒥(g))ν_g(c), com F=Ω3(c,c,c)/3!. O uso da métrica completa preserva as variações do inverso, do volume e da curvatura; nenhum desses objetos foi congelado durante essa identidade.

## 5. Coeficiente q6 e finitude da correção

Como o fundo é conformemente plano, W(g0)=0 e

𝒥(g0+t h)=t²J_W+t³J3+O(t⁴).

A expansão de F com c=tC começa em t⁵. O coeficiente t⁵ da identidade BRST dá s0qgrad=0; o de t⁶ dá

s1qgrad+s0q6=(□bar J_W)ν(C).

O termo s0q6 não foi omitido. Uma precisão aditiva, obtida expandindo os fatores já definidos na nota, torna seu conteúdo explícito. Escreva H=g0⁻¹h e h^{ae}=g0^{ab}g0^{ef}h_bf. Então

q6 = (ε0_abcd/3!) [
       ∇bar^aJ3 − h^{ae}∇bar_eJ_W
       + (tr H/2)∇bar^aJ_W
     ] C^b C^c C^d.

Os três termos vêm, respectivamente, do terceiro coeficiente de 𝒥, da variação da métrica inversa e da variação do volume. J3 é cúbico em h; todos os termos de q6 pertencem à espécie h³C³. O maior número de derivadas em um fator h é três. A extração de um coeficiente fixado das séries métricas envolve somente operações finitas e inversos regulares da referência. Não há soma de jatos de ordem ilimitada no mesmo coeficiente.

Essa fórmula serve como explicitação da correção já definida, sem alterar o arquivo congelado. Ela também confirma que a corrente é realizada no complexo BRST original antes de passar à cohomologia, não apenas pela coincidência de uma avaliação especial.

## 6. Limites e custódia

A identidade produz □bar J_W, não J_W. Não se adotou uma equação de onda para esse pseudoscalar quadrático, nem se concluiu que qgrad cancela A6. O filtro de k=2/z0 da outra nota082 se limita ao setor sem derivadas; esta corrente está fora dele. Nenhum perfil TT foi calculado ou importado nesta revisão da corrente.

O teorema permanece no domínio métrico de referência espaço-forma fixada, φ0 constante, coeficientes escalares inertes e ordem finita por elemento. Não decide o módulo CE completo, o fundo físico não constante, QME, admissibilidade causal ou UV. A investigação083 permanece separada.

[REAL — documental] Os pins do manifesto foram comparados com os bytes presentes, e as fontes lidas foram medidas antes/depois desta revisão. Os três vínculos locais da nota existem. Nenhum documento anterior foi alterado. O novo recibo distingue as verificações documentais de uma execução matemática: esta revisão tem zero CAS e zero Lean.

Parecer favorável no alcance acima, sem erro material identificado.
