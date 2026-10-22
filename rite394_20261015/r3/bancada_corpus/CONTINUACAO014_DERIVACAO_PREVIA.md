[DERIVED / INPUT / OPEN] Continuação 014 — transporte de telas e integração dos módulos

Derivação anterior ao novo código, 05/09/2026. A entrega 013 foi reconferida: 408 hashes, cinco módulos, 26 teoremas e sete construções impressas. O turno anterior é classificado como progresso; o objetivo amplo continua ativo e não foi alcançado. O túnel permanece com a ordem gerencial 007 como a mais recente.

Correção de integração identificada por leitura: GeometricScreenControls.lean (012) e NullFrameConstruction.lean (013) declaram flatNullFrame no mesmo namespace ChatgptAudit, com tipos distintos. A verificação por módulo de 013 não cobriu a importação conjunta com esse controle de 012. Os artefatos entregues não serão alterados. Três cópias do trecho construtivo de 013 receberão o namespace ChatgptAudit.Screen013 e nomes de módulo próprios; um módulo de integração importará o controle anterior e essas cópias simultaneamente. Essa correção não será contada como novos teoremas matemáticos.

Alvo geométrico: construir um habitante de GeometricScreenAlong sob uma métrica suave com conexão compatível e um campo nulo suave, não zero no ponto e geodésico na vizinhança. Essas hipóteses de campo, métrica e geodesicidade continuam INPUT. A construção deverá produzir curva e tela transportada, preservando a área variável. Não receberá a família de telas pronta.

1. Ponha B=∇V, L=Σ VⁱΓᵢ e K=B−L. Considere o campo autônomo sobre (x,F)∈R⁴×Mat₄(R):
   x′=V(x), F′=K(x)F.
   Com V e Γ suaves, esse campo é C¹. Picard–Lindelöf fornece uma solução num intervalo aberto em torno de 0, com x(0)=x₀ e F(0) igual ao referencial de 013. O teorema de existência é o da mathlib local, não um axioma novo.

2. Escolha W=coluna 1 de F e S=colunas 2 e 3. A primeira coluna usada na base final será V(x(t)), de modo que não é necessário supor ou provar sua coincidência com a coluna 0 da solução matricial. A identidade diferencial ordinária dá V′=(B−L)V.

3. Para qualquer coluna Z que satisfaça Z′=(B−L)Z, compatibilidade métrica dá
   d[g(V,Z)]/dt = g(BV,Z)+g(V,BZ).
   Geodesicidade elimina BV e a identidade de nulidade de 013 elimina g(V,BZ). A derivada é zero. A partir dos dados iniciais seguem g(V,W)=−1 e g(V,S_i)=0 no intervalo. V continua nulo pela hipótese de campo nulo.

4. O Gram h=SᵀgS é contínuo e vale −I₂ no ponto inicial. Portanto h₀₀<0 e det h>0 num intervalo menor. Não se impõe h=−I₂ fora do ponto inicial.

5. Complete a tela sem modificá-la. Na base bruta (V,W,S₁,S₂), denote a=g(W,W) e b_i=g(S_i,W). Tome q=h⁻¹b, d=a−bᵀq e
   N=W−S q+(d/2)V.
   Então g(V,N)=−1, g(N,N)=0 e g(N,S_i)=0. A nova base (V,N,S₁,S₂) tem Gram nullScreenGram(h). O determinante desse Gram é −det h≠0; isso implica invertibilidade da base. As identidades deverão ser provadas por operações matriciais efetivas.

6. A primeira coluna V permite usar o teorema null_field_preserves_frame_pairing de 013 para produzir a condição restante do contrato NullScreenAt. Assim, em cada ponto do intervalo menor, a tela transportada S admite um certificado do contrato anterior. A continuidade, a tangência da curva e S′=(B−L)S fornecem GeometricScreenAlong.

7. Aplicar a lei de área geométrica de 012 à tela construída. A=√det(SᵀgS) pode variar; A′=tr(∇V)A decorre das condições preservadas, não de uma renormalização.

Controles previstos antes do código: a importação conjunta deve passar; um caso plano constante deve recuperar uma tela constante; uma família com expansão não nula não deverá ser forçada a h=−I₂. Caso um desses controles exija dados que o resultado ainda não construiu, a limitação será nomeada, sem substituir a construção geral por um único exemplo.

[OPEN] Mesmo pagando esse transporte, ainda faltam a construção geral do campo nulo geodésico e do horizonte imerso, as condições iniciais de equilíbrio, o vínculo microscópico entre álgebra/estado/entropia e geometria, calor, Clausius/H3, escala física, assinatura/dimensão e globalização. Esses itens não são resultados da existência de uma solução de ODE.

Somente arquivos novos e cópias próprias não seladas sob Chatgpt podem ser escritos. Backup dos bytes antes de revisões. Nenhuma execução/importação de um.py ou alteração do acervo, memórias, selos, kernel canônico ou gate. As contagens e os hashes serão obtidos dos artefatos. Tentativas falhas e avisos ficam preservados. A gerência audita independentemente antes de incorporar.


Adendo de 06/09/2026, anterior ao código do controle curvo: usar o modelo já verificado em CurvatureControls.lean, g=e^(2x⁰)η e sua conexão de Levi-Civita explícita. Definir q=e^(−2x⁰), k=(1,1,0,0) e V=qk. Então V é nulo e suave em todo R⁴. A derivada ordinária é ∂ᵢV=−2qδᵢ₀k. Somando a conexão, B=∇V=qM, onde as colunas de M são −k, k, e₂, e₃. Logo BV=0 e tr B=2q. No ponto x=0, g=η, V=k, a tela inicial é normalizada e θ=2. A construção geral de transporte deverá fornecer A(0)=1 e A′(0)=2. Assim há um habitante com curvatura não nula e área que não é localmente constante. O controle será uma existência formal construída via Picard–Lindelöf, não uma avaliação numérica nem um dado observacional.

Para esse teste, extrair também a lei de área no parâmetro inicial t=0 a partir do transporte efetivo da solução. Os dados de positividade do Gram valem no ponto inicial por normalização. A lei no ponto não depende de calor ou Clausius.
