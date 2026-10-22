# Revisão própria do termo de uma volta não absorvido

09/09/2026. [DERIVED — revisão matemática escrita]. Objeto: `CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/TERMO_QUARTICO_NAO_ABSORVIDO.md`. Não encontrei erro material na álgebra FRW nem na conclusão de não absorção **na classe declarada**. Este parecer registra minha análise; não atribui aprovação ao operador ou a outro agente.

## 1. Entrada e alcance da revisão

[INPUT] Aceitei o coeficiente acoplado C₄=(7440x²+1616x−211)/96 como entrada da frente completa, conforme a ordem de revisão. Li seu recibo: ele registra 23 verificações e identifica o escopo como contrações exatas de jatos e fórmula universal de calor. Não repeti o cálculo matricial 13×13, não executei seu script e não transformo esse recibo numa prova independente de medida, determinante global ou integral funcional.

[REAL] O manifesto ao lado mede bytes e hashes dos arquivos consultados. Também compara o hash efetivamente lido do script completo com o registrado no recibo, sem executar esse script. A prova algébrica que segue é escrita; não foi chamada de compilação Lean ou de nova rodada CAS.

## 2. Conferência independente das identidades FRW

Do fundo a=2cos(r/2), H²=x−1/4, Ḣ=−x e x=a⁻²:

\[
 \dot x=-2Hx,\qquad
 \ddot x=-2\dot Hx-2H\dot x=2x^2+4H^2x=6x^2-x,
\]
\[
 \Box x=\ddot x+3H\dot x=6x^2-x-6(x-1/4)x=x/2.
\]

As equações on-shell dão Ric_ab=(3/4)g_ab+4W_ab. O endomorfismo Ric^a_b tem um autovalor 3/4 na direção temporal e três autovalores 3/4−4x nas direções espaciais. Logo

\[
 R=3-12x,\quad
 \mathrm{Ric}^2=(3/4)^2+3(3/4-4x)^2
 =48x^2-18x+9/4.
\]

FRW é conformemente plano; portanto Riem²=2Ric²−R²/3=48x²−12x+3/2. Isso dá

\[
 \mathrm{Euler}_4=\mathrm{Riem}^2-4\mathrm{Ric}^2+R^2=3/2-12x.
\]

W tem norma quadrática 3x² e traço Q=−3x. Assim □R=−6x e □Q=−3x/2. Pontryagin é zero no fundo conformemente plano. Os sinais e fatores da nota são consistentes. Em qualquer intervalo aberto não trivial de r num ramo com H≠0, x percorre um intervalo aberto; não se está testando apenas um ponto do fundo.

Finalmente,

\[
 \mathcal C_4=\frac{155}{2}x^2+\frac{101}{6}x-\frac{211}{96},
 \qquad \frac{d^2\mathcal C_4}{dx^2}=155\ne0.
\]

Isso é incompatível com A+Bx para A,B constantes num intervalo aberto. O fator comum de volume μ_g é não nulo no domínio e não altera o teste funcional.

## 3. Auditoria da enumeração de correntes

A conclusão requer precisamente o espaço de correntes naturais covariantes de peso de derivadas ≤3, invariantes por O(4) do alvo, polinomiais em jatos e sem inversos de gradientes/curvatura. Contam-se u como peso 1, Du e Riem como peso 2. Coeficientes podem depender de κ,c,Λ, mas isso não muda o peso de derivadas.

A transitividade de O(4) em S³ torna constantes os coeficientes escalares invariantes sem derivadas. A isotropia O(3) no espaço tangente do alvo não possui vetor invariante nem tensor invariante de ordem ímpar. Seus tensores de ordem dois são múltiplos da métrica. A curvatura constante do alvo só reproduz contrações dessas métricas nessa contagem.

Consequentemente:

- Correntes puramente métricas de peso 3 são contrações de ∇Riem. Bianchi reduz as contrações polares a ∇R; contrações axiais com epsilon não dão um novo vetor independente.
- Um termo misto Riem·u precisaria de uma 1-forma invariante do alvo; ela não existe. Um termo linear D²u também não pode contrair seu único índice de alvo.
- Os termos de matéria u·Du deixam apenas ∇_μQ/2=<u^ν,D_μu_ν> e <u_μ,τ>. A simetria D_μu_ν=D_νu_μ elimina distinções aparentes entre as outras contrações. Uma contração com epsilon do espaço-tempo anula o Hessiano simétrico.
- Uma corrente cúbica u³ precisaria de um tensor de ordem três do alvo. O(4) o exclui. Se a simetria for reduzida a SO(4), o volume do alvo o fornece; a contração polar com g se anula pela antissimetria e a contração axial restante é a dual do pullback desse volume. Sua divergência é identicamente zero, porque d(y*vol_S³)=y*(d vol_S³)=0.

Essa análise inclui os possíveis termos de paridade ímpar pertinentes. Não exige que o pullback do volume seja globalmente exato: seu fechamento basta para a divergência nula.

No fundo, τ=0 como campo em todo o domínio, logo <u,τ> e sua divergência são zero. Também E=0 e todos os seus prolongamentos se anulam. Redefinições de campos, integradas por partes dentro da truncagem de quatro derivadas, deixam termos de equações e correntes dessa mesma ordem. Euler e Pontryagin foram permitidos separadamente; não se confundem com divergências de correntes tensorais globalmente definidas. Assim nenhum termo admitido nessa equivalência gera a parcela x² necessária.

## 4. Conclusão e limites efetivos

[DERIVED] Sob o coeficiente C₄ de entrada e a prescrição declarada, a divergência não se absorve apenas em κ,c,Λ, mesmo permitindo termos de equações, as divergências totais pertinentes e as duas classes características. É necessário algum operador independente de quatro derivadas. A nota não afirma que todos os operadores de quatro derivadas sejam independentes; o teste num fundo não permitiria essa conclusão mais forte.

Não há contradição com adicionar um contratermo arbitrário de quatro derivadas: isso é precisamente ampliar a ação EFT. Por exemplo, Q²=9x² pode contribuir à parcela identificada; seu coeficiente é informação adicional, não um ajuste dos três parâmetros originais. Coeficientes finitos continuam não determinados pelo teste. Uma mudança de medida que acrescente tal densidade também deve ser declarada como entrada adicional; a conclusão não exclui todas as medidas possíveis.

A prova não se estende automaticamente a correntes de ordem superior, coeficientes singulares em dy ou curvatura, novos campos de relógio, termos não locais ou a uma teoria UV completa. Não calcula uma anomalia BRST de ghost number um. Esses limites já estão corretamente expostos no texto revisado. Nenhum original ou artefato congelado foi alterado.
