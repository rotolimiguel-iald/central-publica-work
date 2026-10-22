# Adendo077 — correção do sinal Koszul–Tate do quadrático mínimo

10/09/2026. [DERIVED — correção e conferência algébrica escrita]. Este arquivo corrige a equação(3) e sua atribuição de convenção na [nota077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/S0_KILLING_E_PRIMEIRA_TRANSICAO.md>). A fonte e seu manifesto permanecem intactos. Não modifica a entrega076. Nenhum um.py, Lean ou CAS executado/importado.

**Correção:** para a ação quadrática ali escrita, com fonte à esquerda e a convenção de derivadas direitas efetivamente usada em069/076, o sinal é
\[
 \boxed{s_0u^*=+H_0u,}
\]
e não −H0u. O sinal de s0c*=+R0†u* permanece positivo. A frase da nota que atribuía o triplo anterior à mesma convenção deve ser lida com esta correção.

## 1. Conferência na ação escrita

O [levantamento das correntes076, seção2](<C:/IALD/Central de Patentes/Chatgpt/MODULOS_BRST_EBAR_076_20260910/LEVANTAMENTO_BRST_CORRENTES_KILLING_076.md>) explicita as derivadas direitas e a ordem da fonte do [dicionário069](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md>). Também conferi diretamente a [equação140 de Fröb](https://arxiv.org/pdf/1803.10235v3), que usa
\[
 s_0\Phi=-\frac{\delta_R S_2}{\delta\Phi^*},
 \qquad
 s_0\Phi^*=+\frac{\delta_R S_2}{\delta\Phi}.
 \tag{A1}
\]
Aqui Φ inclui campos e ghosts, com a graduação e as derivadas indicadas.

Na ação
\[
 S_2=\tfrac12\langle u,H_0u\rangle+\langle u^*,R_0c\rangle,
 \tag{A2}
\]
u é par, u* e R0c são ímpares, c é ímpar e c* é par. Os coeficientes H0,R0 dependem apenas do fundo. Usamos a definição de derivada direita com a variação posta à direita. Portanto
\[
 \delta_{u^*}(u^*R_0c)
       =(\delta u^*)R_0c=-(R_0c)\delta u^*,
 \qquad \frac{\delta_RS_2}{\delta u^*}=-R_0c.
\]
A primeira equação(A1) dá s0u=R0c. Variar u par no quadrático dá δ_RS2/δu=H0u; isso fixa o sinal positivo corrigido.

Ao variar c, integrar por partes em
\[
 \langle u^*,R_0\delta c\rangle
   =\langle R_0^\dagger u^*,\delta c\rangle
\]
já deixa a variação à direita. Não se atravessa novamente o coeficiente ímpar. Assim δ_RS2/δc=R0†u*. Não há c* no quadrático. O conjunto correto é
\[
 \boxed{
 s_0u=R_0c,\qquad s_0c=0,\qquad
 s_0u^*=H_0u,\qquad s_0c^*=R_0^\dagger u^*.
 }
 \tag{A3}
\]
O adjunto da nota, R0†u*=−2∇bar·π+p_a dφ0^a, permanece inalterado.

A nilpotência usa exatamente as mesmas identidades de Noether:
\[
 s_0^2u^*=H_0R_0c=0,\qquad
 s_0^2c^*=R_0^\dagger H_0u=0.
 \tag{A4}
\]
Nenhum sinal de H0 ou da ação física foi redefinido para evitar a correção.

## 2. Complexo isomorfo não significa mesma convenção Hamiltoniana

Denote d_− o complexo linear com o triplo incorreto (−H0,+R0†) e d_+ o corrigido (+H0,+R0†). A aplicação nos geradores
\[
 F(u)=u,\quad F(c)=c,\quad
 F(u^*_{\rm antigo})=-u^*_{\rm corrigido},\quad
 F(c^*_{\rm antigo})=-c^*_{\rm corrigido}
 \tag{A5}
\]
satisfaz d_+F=Fd_−. Nos dois geradores que mudam,
\[
 d_+F(u^*_{\rm antigo})=-H_0u=F d_-(u^*_{\rm antigo}),
\]
\[
 d_+F(c^*_{\rm antigo})=-R_0^\dagger u^*_{\rm corrigido}
            =F d_-(c^*_{\rm antigo}).
\]
O mapa prolonga-se aos jatos e à álgebra graduada, preservando ghost, valência e naturalidade.

(A5) é um isomorfismo de COMPLEXOS LINEARES. Não estou chamando-o de transformação canônica que conserve o mesmo antibracket e a mesma ação(A2), nem transportando sem cálculo todo o BRST não linear. A nota deve usar(A3) na convenção citada. A existência de(A5) não torna correta a atribuição anterior de sinal.

## 3. Efeito delimitado nos primeiros cálculos077

A correção não altera R0c, sc, o ideal linear dos jatos de Killing ou o CE induzido por sc quadrático. Portanto não altera as contagens iniciais por valência usadas na nota:

- Em ghost3/valência≤3, há somente três ghosts. As fronteiras relevantes são s(c²) e s0(u c²); nenhuma contém antifield.
- Para levantar essas classes de C3 a C4, a correção possível é u c³. Sua variação relevante é s0u=R0c, cujo sinal não mudou.
- Em ghost4/valência≤4, há somente quatro ghosts. As fronteiras relevantes são s(c³) e s0(u c³), novamente sem antifields.
- Antifields podem participar de outros componentes de C4 e de valências posteriores. A afirmação aqui é apenas que os mapas e quocientes efetivamente empregados nas contagens iniciais não usam o sinal corrigido.

Assim, esta correção de convenção não modifica os resultados calculados na referência de curvatura constante: dim H³(C3)=4, imagem de H³(C4)→H³(C3) de dimensão1 e H⁴(C4)=0, com os mesmos limites de categoria da nota. A revisão matemática dos demais passos permanece independente; este adendo não declara aceita toda a nota por causa da correção.

A inferência que impede presumir sobrejetividade universal usa os quatro ciclos regulares em ghosts e sua restrição. Também não depende do segmento de antifields corrigido. Permanece proibido concluir daí lim¹ não nulo ou que o sobrevivente CE se levante à cohomologia completa.

## 4. Custódia

Quatro fontes foram medidas antes e depois; a nota077 e seu manifesto histórico estão entre elas. Os novos arquivos são somente este adendo, seu registro de pins e o script/manifesto da correção. Nenhuma aprovação de outra pessoa ou sessão é atribuída por este documento. A correção e as contas(A1)–(A5) são registradas sob autoria desta tarefa.

