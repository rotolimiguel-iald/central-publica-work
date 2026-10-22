# Continuação 037 — quarta ordem dos estados e calibração do relógio
06/09/2026. [DERIVED / INPUT / OPEN] Derivação anterior à compilação. Continuação da meta ampla e da ordem007; processo008 obrigatório. Nenhum original ou artefato selado será alterado.

## Estado e escolha da obrigação
A036 foi PROGRESSO: 87 teoremas novos, área induzida efetiva ligada à curvatura da família029 e anisotropia de maré independente da base ortonormal. A revalidação somente em leitura da036 retornou PASS (2084 arquivos). O túnel contém001–008, sem009 na leitura inicial. A árvore canônica v325 conserva H3/casamento microscópico e seleção do relógio/área como INPUT.

Esta etapa NÃO cria uma H3 nova para depois declará-la resolvida. Calcula os coeficientes exatos dos estados já construídos e testa se uma extensão quártica do casamento poderia selecionar a liberdade óptica036. O casamento quadrático existente não exige essa extensão. H3 dinâmico e a reconstrução geral continuam OPEN.

Foi examinada uma outra rota: Herm(2), determinante lorentziano e congruência do filtro local exp(L_n/2). É matematicamente viável, mas exige selecionar um bloco local e provar sua ligação ao filtro global, que em geral não preserva M2 por congruência. Além disso, essa representação interna não identifica o espaço-tempo nem seu relógio. Nenhuma prova dessa rota será reclamada neste lote.

## Informação efetiva do estado
Reutilizar as definições028:
h(t)=t²/(1+t²), q_n=1/3-b_n h(t), B=Σb_n, B2=Σb_n².
S(t)=amplitudeEntropyIncrement b t=amplitudeModularIncrement b t-amplitudeRelativeEntropy b t.
D(t)=amplitudeRelativeEntropy b t, já igual à leitura psi_t(L(t)) na030.
Não definir uma entropia substituta a partir da geometria.

[DERIVED, a formalizar] A curva afim binária p+(k,-k)y e o lema quadrático021 dão KL/y²→9k²/4 pelo passado. Compor y=-h(t) leva ao limite perfurado D_n(t)/t⁴→9b_n²/4.
A cota existente D_n≤(9/2)b_n² h² fornece majorante (9/2)b_n² após dividir por t⁴. A somabilidade já provada permite Tannery, sem hipótese nova de decaimento:
D(t)/t⁴→9B2/4.

Para t≠0, há identidade racional exata:
[S(t)+log(2)B t²]/t⁴ = log(2)B/(1+t²)-D(t)/t⁴.
Logo C_S=log(2)B-9B2/4. Também B2≤B/12.

## Área efetiva e limite quártico
A036 fornece derivadas reais até4, mas não resto de Taylor. Aqui se deve aplicar Taylor–Peano à função explícita C4, calcular seu polinômio e transferir por igualdade eventual à inducedArea da tela Jacobi.
Para a,c≥0:
[A(t)-1+(a+c)t²/2]/t⁴→(a²+6ac+c²)/24.
Em a=r/2+s,c=r/2-s, |s|<r/2:
C_A=r²/12-s²/6.

## Teste de extensão, com hipóteses visíveis
[INPUT para este teste] η>0, B>0, mesmo parâmetro nos estados e no feixe, r=2log(2)B/η. O casamento quadrático já está satisfeito. O defeito quártico é
δ4=C_S-η C_A=C_S-(log2)²B²/(3η)+ηs²/6.
Uma igualdade quártica extra só é possível se C_S≤(log2)²B²/(3η); para a subfamília estrita de cossenos, exige também C_S>(log2)²B²/(6η).

Controle adversarial: 0<B≤η implica δ4≥7B/48>0. Usar B2≤B/12, 1/2≤log2≤1, (log2)²≤log2 e B²/η≤B. Uma testemunha não vazia para cada η>0 é b0=min(1/24,η/2), demais termos zero.
Isto recusa SOMENTE esse fortalecimento quártico com relógio fixado. Não é refutação da H3 quadrática nem da gravidade quântica.

## Relógio
Definir phi_lambda(t)=t+lambda t³. Sua derivada na origem é1 e ela preserva o lado do tempo localmente. Se
[f(t)-a t²]/t⁴→C,
então
[f(phi_lambda(t))-a t²]/t⁴→C+2a lambda.
Para S, a=-log2 B: C_S muda para C_S-2lambda log2 B.
Com lambda=δ4/(2log2 B), pode-se anular o defeito alterando SOMENTE a atribuição de tempo aos estados.
Uma reparametrização COMUM aos dois lados preserva δ4, pois o defeito já tem ordem4. Portanto esse ajuste exige um dado de relógio relativo; não determina por si a curvatura ou a física.

## Limite dos cortes
A expansão entrópica finita centralizada pelo B global deixa log2(B-B_N)/t² no quociente de quarta ordem. N→∞ sozinho não basta num limite conjunto. Esta entrega tratará o estado global, sem reclamar uniformidade em cortes. Opções futuras: limite iterado, taxa B-B_N=o(t²), ou geometria adaptada a B_N.

## Custódia
Todas as criações/revisões não seladas ficam em Chatgpt, com temporário verificado e backups de bytes. Instâncias nomeadas e #print axioms para todas as declarações. Compilação serial e importação conjunta em diretório novo; a036 será lida de sua compilação limpa fixada, nunca de oleans ausentes/antigos na raiz. Dependências históricas fixadas permanecem uma fronteira não recompilada. Nenhum gate, Atlas, memória canônica ou um.py será tocado.
