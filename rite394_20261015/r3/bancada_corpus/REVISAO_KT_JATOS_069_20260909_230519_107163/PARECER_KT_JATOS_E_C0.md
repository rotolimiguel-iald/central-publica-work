# Parecer independente sobre o certificado Einstein–sigma em jatos

09/09/2026, arco 069. [DERIVED — revisão matemática escrita]. Revisão de leitura, sem execução de `um.py`, Lean ou CAS. A nota examinada e os originais permanecem intactos. Os pins medidos constam do manifesto novo ao lado.

**Parecer:** não encontrei erro material nas seções 3–7. A demonstração sustenta a identificação entre anulação na superfície estacionária formal e pertencimento ao ideal diferencial das equações, na classe natural polinomial especificada. A resolução KT ordinária decorre do mesmo sistema triangular. O resultado não é uma classificação de toda a cohomologia BRST relativa a d. A consequência C0 usa também a demonstração Euler/Pontryagin anterior e mantém seus contratos.

O objeto principal desta revisão é [CERTIFICADO_POLINOMIAL_EINSTEIN_SIGMA.md](../REGULARIDADE_KT_JATOS_20260909_224852/CERTIFICADO_POLINOMIAL_EINSTEIN_SIGMA.md), especialmente as linhas 70–255. Abaixo registro os controles que sustentam o parecer e duas precisões de importação que tornam explícitos passos curtos da fonte.

## 1. Imagem de Einstein linearizado e constraints

[DERIVED] Com assinatura (+---), a construção em gauge de Donder está consistente. Para h de grau N, a inversão espacial de Laplace leva uma fonte homogênea de grau N−2 a um polinômio de grau N. Na identidade usada em (5), o coeficiente do termo sem a Laplaciana adicional é

    2(j+1)(2d−2j+3).

É positivo para 0≤j≤floor(d/2). A recorrência dos a_j cancela todos os termos remanescentes. Não há divisão por uma variável ou campo.

Os dados A de (6) têm grau N; os dados B de (7) têm grau N−1, pois V tem grau N e recebe uma derivada. Com v_b=∂^a hbar_ab=∂t hbar_0b−∂i hbar_ib, A e B dão v|t=0=0. As duas derivadas iniciais são

    ∂t v_0|0 = ΔA_00−2E_00|0−∂iB_i0 = 0,
    ∂t v_i|0 = ΔA_0i−2E_0i|0−∂jB_ji = 0.

A divergência livre de E implica □v=0. A recorrência de Taylor com dados nulos elimina v em todos os coeficientes, sem hipótese analítica de convergência. O término da recorrência é automático: os últimos coeficientes espaciais são lineares ou constantes e suas Laplacianas se anulam. Assim G^(1)(h)=−□hbar/2=E, com os sinais usados na fonte.

O controle separado de D_N também confere: se □V_b=f_b, então E_ab=∂aV_b+∂bV_a−η_ab∂^cV_c satisfaz ∂^aE_ab=f_b. Para f de grau N−3, V tem grau N−1 e E tem o grau N−2 correto. Isso prova a sobrejetividade necessária a partir de N=3; em N=2 a divergência é zero por grau.

A escolha inicial de t é somente um método de provar sobrejetividade entre espaços finitos. Ela não é uma inversa física de Einstein e não precisa sobreviver na cisão covariante final.

## 2. Gauge radial, cisão e classe de operações permitidas

[DERIVED] A fórmula (10) passa pelo teste de Euler. Com f_a=h_ab x^b, F=h_ab x^a x^b e ξ homogêneo de grau N+1, resulta

    ξ·x = F/[2(N+1)],
    (∂aξ_b+∂bξ_a)x^b = ∂a(ξ·x)+Nξ_a = f_a.

Logo h−L_ξ η é normal e tem a mesma imagem por G^(1). O divisor N é legítimo porque N≥2. Não é necessário escolher outra coordenada de tempo para esse passo.

A completa redutibilidade é aplicada a representações tensorais de dimensão finita, não a espaços de soluções de uma EDP. Como a matriz dos geradores, os mapas e as equações de cisão são racionais, a existência complexa implica solução racional por eliminação linear. A eventual média sobre representantes de componentes desconexas é finita. Não há média sobre o grupo de Lorentz não compacto.

**Precisão útil na passagem “equivariante ⇒ operações por métrica/volume”.** Uma cisão entre submódulos tensoriais estende-se a um operador entre potências tensoriais por complementos equivariantes. Identificando duais mediante η, seu tensor de coeficientes é invariante ortogonal. O teorema fundamental de invariantes expressa esses tensores por permutações, contrações métricas e, no grupo especial ortogonal, pelo tensor de volume. Uma referência primária que explicita ambas as partes e os espaços de intertwiners é [Lehrer–Zhang, Teoremas 2.1 e 3.1, Observação 2.2 e Corolário 4.2](https://arxiv.org/pdf/1612.03998). Esse passo justifica a classe restrita de denominadores; uma matriz constante arbitrária, sem equivariância, não justificaria tal conclusão.

[DERIVED] A descida real/racional também é finita: a expressão em contrações resolve outro sistema linear racional com soluções complexas, logo possui uma solução racional. Ao trocar η por g, os inversos provêm exclusivamente das contrações com g⁻¹ e, na apresentação por vielbein, de det(e). A cisão pode ser escolhida uma vez em cada ordem N e usada coerentemente na indução; não se exige cota uniforme nem limite analítico dessas matrizes.

**Precisão de localização em Jentsch.** O Teorema 3(a) é enunciado para um espaço euclidiano; não convém citá-lo isoladamente como enunciado Lorentz. O primeiro parágrafo inclui métricas não degeneradas de assinatura arbitrária, e o Teorema 1 fornece os polinômios universais da expansão normal nesse contexto; a conversão em coordenadas normais e curvatura aparece também em 3(b). São essas identidades universais que a presente demonstração usa. [Jentsch, v2, introdução, Teorema 1 e Teorema 3(b)](https://arxiv.org/pdf/1509.08269v2).

[DERIVED] Não se necessita de positividade para essa conversão: a fórmula direta da curvatura, o operador de Young e a identidade dos coeficientes normais são polinomiais e usam uma forma não degenerada. A realização analítica de todo jato por uma métrica global não é parte da conclusão. Portanto essa precisão de referência não constitui uma falha material da prova examinada.

## 3. Triangularidade da matéria e Noether em todas as ordens

[DERIVED] A contagem de derivadas paga a passagem principal da nota. Em ordem N, o termo de maior derivada métrica em ∇^(N−2)E é G_NH_N. As derivadas de T, que é quadrático em dy, alcançam somente a ordem N−1 no mapa. Em D^(N−2)τ, a derivada métrica mais alta tem ordem N−1, enquanto o bloco de ordem N no mapa é □Y_N. A substituição de jatos parciais do mapa pelos jatos simetrizados covariantes altera apenas graus inferiores, inclusive os jatos métricos até N−1. Não aparece acoplamento oculto entre H_N e Y_N no bloco diagonal.

A condição de coordenadas métricas normais é linear em cada coeficiente homogêneo H_N. Os coeficientes livres de graus inferiores não impõem uma condição algébrica adicional sobre H_N além de pertencer ao módulo normal. As simetrias de curvatura entram na conversão desses coeficientes, não como uma nova constraint omitida.

A identidade completa é

    ∇^aE_ab + κc h_AB τ^A u_b^B = 0.

Em grau N, sua prolongação relevante usa N−3 derivadas sobre a divergência. Por isso a matéria envolvida é τ de nível N−1 ou menor, já paga na indução anterior. A diferença entre divergência da derivada simetrizada e derivada da divergência contém comutadores de curvatura multiplicando equações inferiores. Assim D_NE_N está no ideal dos níveis anteriores, também off-shell; sua anulação não é uma hipótese adicional sobre o novo jato livre.

Com Π=1−SD, z_N=ΠE_N e ζ_N=τ_N, as duas inversões de (14) são triangulares e polinomiais. As componentes restantes de E_N são SD_NE_N e pertencem ao ideal anterior. Isso estabelece (15) por indução, em vez de simplesmente apagar as constraints. A base N=2 contém todas as componentes de Einstein e do traço do Hessiano do mapa como equações independentes.

Pôr os novos z_N e ζ_N iguais a zero, escolhendo os parâmetros livres arbitrariamente, prolonga qualquer jato estacionário finito. A passagem ao limite projetivo é então formal e recursiva. Não exige a convergência da série de Taylor de uma solução.

## 4. Certificado polinomial e KT

[DERIVED] O prolongamento sobrejetivo é exatamente o que permite deduzir F(q,0)=0 para todos os parâmetros livres q a partir da anulação em todos os jatos estacionários formais. Sem esse passo, o argumento de homotopia seria insuficiente.

A integral em (17) é finita, termo a termo em um polinômio nas coordenadas das equações. Ela divide monômios apenas por inteiros positivos. A coordenada y permanece fixa, portanto C∞(U) continua sendo o anel dos coeficientes, sem expansão analítica em y. A presença de divisores de zero em C∞(U) não afeta o argumento: as novas coordenadas z são variáveis polinomiais livres sobre esse anel e a identidade é explícita. Reescrever pela inversa triangular preserva a ordem de jato finita e a mesma classe de denominadores.

O homotopy é equivariante porque as cisões e a escala simultânea dos módulos z o são. A construção tensorial da seção 2 permite que os coeficientes do certificado se colem entre referenciais. A localidade na carta do alvo permanece: isso não resolve cohomologia da topologia global do alvo.

O bloco principal das identidades independentes tem dimensão dim(V*⊗P_(N−3)), porque D_N é sobrejetiva. A mudança dos antifields dependentes para a combinação de Noether é triangular, com diagonal invertível constante; os termos r_Au_b^A envolvem níveis inferiores. Com δ anulando os campos, ele comuta com as conexões e prolongamentos empregados, e δ²C*=0 segue da identidade completa acima. Após a mudança, os pares (p,z) e (C*,p_tilde) admitem a contração polinomial pelo número de variáveis. Não sobra uma identidade principal nova que exija antifield adicional.

A relação com o critério padrão é precisa: o split e a homotopia são os ingredientes de regularidade que [BBH 2000, §5.1.3, Lema 5.1 e Teorema 5.1](https://arxiv.org/pdf/hep-th/0002245v3) usam para a resolução KT. Aqui o split específico Einstein–sigma foi demonstrado, não importado somente por analogia. O argumento é para δ; passar a δ módulo d, a s módulo d ou a uma normalização quântica requer outros passos.

## 5. Consequência que pode ser registrada

[DERIVED] A combinação com a nota C0 anterior é legítima no alcance indicado. Se A Euler₄+B Pontryagin₄−dβ é natural, polinomial nos jatos diferenciados e formalmente nulo, o certificado da seção 6 o põe no ideal diferencial exato. A prova anterior exclui essa identidade para constantes A,B salvo A=B=0, sob seus contratos de Λ>0 e classe regular que admite mapa constante. A presença de dβ apenas aumenta uma ordem de jato finita.

O parecer favorável diz respeito a esse certificado e à consequência característica C0. Não equivale a provar que toda expressão nula apenas sobre soluções globais efetivamente realizadas tem o mesmo certificado; não substitui a superfície estacionária formal por um ansatz ou pelo fundo φ=id. Também não calcula H¹(s|d) integral do sigma, não especializa automaticamente uma série ε-ádica em ε=1 e não resolve a QME interagente.

[REAL] Não identifiquei correção material necessária na nota examinada. As duas precisões bibliográficas/tensoriais acima são registradas neste arquivo novo, sem alteração da fonte congelada. A conclusão é uma revisão matemática escrita com escopo declarado; não é compilação formal nem confirmação física.
