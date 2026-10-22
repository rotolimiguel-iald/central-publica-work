# Revisão da especialização formal e decisão para a construção interagente

09/09/2026. [DERIVED — revisão escrita da raiz]. Foi lida integralmente a [nota de especialização 069](<C:/IALD/Central de Patentes/Chatgpt/ESPECIALIZACAO_EPSILON_SIGMA_069_20260909_224620_755674/ESPECIALIZACAO_FILTRADA_E_OBSTRUCAO_NO_FUNDO.md>), preservada como fonte.

A identidade de grafo \(\sum(v-2)=E+2L-2\) decorre da contagem das extremidades e continua válida com tadpoles. O peso de laço dos vértices de contratermo produz corretamente a versão com \(L_{\rm total}\). A nota distingue essa contagem de uma construção de primitivas de anomalias, que ainda exigem controle próprio de grau.

O teorema filtrado é correto no escopo declarado: na recorrência \(r_n=a_n-\sum_{m=1}^n s_m b_{n-m}\), todos os termos têm grau pelo menos \(2n+w\); a exatidão na mesma filtração permite escolher \(b_n\) com esse limite. Em cada quociente de grau finito há só um número finito de índices n. Isso define a soma diagonal em ε=1 no mesmo centro formal. A hipótese de exatidão filtrada está no enunciado e não é deduzida de H¹=0 sem controle.

Conferi o controle abstrato \(D_\varepsilon=1-\varepsilon x^3\partial_x\). Para o cociclo x, a recorrência dá \(b_n=(2n-1)!!x^{2n+1}\). A translação formal para \(x=b+\eta\), b diferente de zero, exigiria somar no coeficiente constante termos cuja razão absoluta é \((2n+1)b^2\), logo os termos não tendem a zero. Isso refuta a inferência de transporte por mera mudança de centro, sem demonstrar uma anomalia do sigma ou a inexistência de outra primitiva no novo domínio.

No mapa identidade, a expansão em coordenadas escalares de \(h_{11}(\varepsilon,\bar y)\) contém todos os graus ε na parte quadrática de flutuações quando \(\bar y\ne0\). Mesmo em coordenadas normais centradas no valor da matéria, dφ̄ deixa inserções quadráticas de curvatura. A referência plana tampouco é on-shell no mesmo fundo: \(\Box_{\bar g}z^A=3z^A/a^2\). Assim não se recupera a filtração por simplesmente renomear o centro.

A expansão global pela exponencial da esfera tem coeficientes regulares em ξ=0 e tensoriais no fibrado \(\bar\phi^*TS^3\). Ela sustenta a construção direta de vértices em torno do fundo físico feita na outra nota desta pasta. Não fornece por si H¹σ.

**Decisão de trabalho:** preservar o lema ε-ádico/filtrado com suas hipóteses e abandonar a passagem automática ao fundo físico como argumento de suficiência. Q2 é construído diretamente no parâmetro de flutuações; a cohomologia será verificada no complexo físico ou por um transporte que tenha estimativas suficientes. A rota negativa analisada não será contada novamente como uma pendência vaga ou como uma prova concluída.

Nenhuma divergência material foi encontrada nesta revisão. Não houve execução Lean/CAS; os pins da fonte são medidos no manifesto da entrega. Nenhum arquivo anterior foi alterado.
