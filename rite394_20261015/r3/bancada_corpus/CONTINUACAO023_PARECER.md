[REAL / INPUT / OPEN] Continuação 023: um covetor comum, resposta tensorial e conservação

06/09/2026. Trabalho da bancada em C:\IALD\Central de Patentes\Chatgpt, continuando a entrega 022. A derivação foi registrada antes dos novos módulos em CONTINUACAO023_DERIVACAO_PREVIA.md. A ordem 006 já foi aprovada pela sessão irmã, conforme a ordem 007; esta é uma continuação espontânea do objetivo amplo, sem nova ordem gerencial 023.

O avanço desta etapa consiste em relacionar uma família unitária comum a um tensor candidato em todas as direções de cada ponto e calcular sua conservação. Os antecedentes que ainda selecionam essa família permanecem explícitos. As compilações limpas foram verificadas; a entrega fixa os bytes no manifesto. A auditoria independente cabe à gerência.

O modelo usa um eixo hermitiano M=[[a,b],[b,−a]], a²+b²=1, e amplitudes positivas u,v, u²+v²=1, fixos em todo o domínio. Um campo de covetores w fornece a frequência em cada direção d:

    ell_x(d) = Σ_i w_i(x) d^i
    H_x(d) = ell_x(d) M
    U_x(d,t) = cos(ell_x(d)t) I − i sin(ell_x(d)t) M

A composição na direção e a unitariedade são demonstradas em DirectionalUnitaryFamily.lean:

    H_x(d+e)=H_x(d)+H_x(e)
    U_x(d+e,t)=U_x(d,t)U_x(e,t)
    U_x(d,t)† U_x(d,t)=I

Esta composição compara direções no MESMO ponto x. Não transporta estados entre pontos e não representa, por si, o grupo de translações do espaço-tempo. O núcleo de w produz frequência zero e fluxo trivial. A família depende de um único funcional linear, e a matriz quadrática correspondente tem a forma de um produto externo: não é uma parametrização de toda matéria.

A evolução bipartida, o traço parcial e os limites da marginal são reutilizados da entrega 022, sem alterar seus arquivos. Para a marginal efetiva:

    L_x(d) = lim ΔS/t² = lim ΔK/t² = L0 ell_x(d)²
    L0 = unitaryResponse(a,b,1,u,v)
    lim D/t² = 0

Os limites são pela esquerda em t=0, como nas telas geométricas anteriores. A fórmula em 023 é ligada à função unitaryResponse já calculada para a trajetória unitária de 022, não a uma nova curva de probabilidades arbitrária.

A matriz da resposta é L0 w⊗w. A mudança de base é verificada por:

    ell_(Eᵀw)(d)=ell_w(Ed)
    (Eᵀw)⊗(Eᵀw)=Eᵀ(w⊗w)E

A segunda identidade vale até para E não invertível; ao interpretar uma mudança de base, E é invertível. Não se infere daí uma lei de transporte entre regiões.

Escolher κ=−L0/π e construir, com a métrica e sua inversa,

    q = gInv^{ij} w_i w_j
    T_ij = κ [w_i w_j − (q/2) g_ij].

CoherentScalarStress.lean prova simetria, suavidade, o caso zero e a contração quadrática. Para d nulo:

    T(d,d)=κ ell(d)²
    L(d)=−π T(d,d).

Se κ≥0, a contração nula do candidato é não negativa. O controle de resposta negativa da entrega 022 dá κ>0. Esta normalização foi ESCOLHIDA para realizar a correspondência calor–modular: o código não a apresenta como uma previsão independente da intensidade ou das unidades da matéria.

[KNOWN] Para w=dφ, a expressão é a forma do tensor de um campo escalar sem massa, multiplicada por uma constante. A relação entre conservação e equações de movimento consta nas notas de Carroll, capítulo 1, equações (1.112)–(1.113); o capítulo 4 discute a versão covariante. A contribuição desta etapa é verificar as identidades nas definições de derivada, conexão, inversa e divergência da bancada e associá-las à resposta unitária selecionada. Não se reivindica a descoberta dessa lei clássica.

Fontes primárias consultadas:
- [Carroll, capítulo 1](https://ned.ipac.caltech.edu/level5/March01/Carroll3/Carroll1.html).
- [Carroll, capítulo 4](https://ned.ipac.caltech.edu/level5/March01/Carroll3/Carroll4.html).

A divergência foi calculada antes de receber qualquer hipótese de conservação. Definir:

    W_ij = ∂_i w_j − Γ_i^k_j w_k
    div(w) = gInv^{ik} W_ik.

Sob compatibilidade métrica, inversa efetiva e diferenciabilidade, CovectorStressCalculus.lean e ScalarStressConservation.lean demonstram:

    ∇_i (w⊗w) = (∇_i w)⊗w + w⊗(∇_i w)
    ∂_i q = 2 gInv^{jk} w_k W_ij
    ∇^i T_ij = κ [div(w) w_j + gInv^{ik} w_k (W_ij−W_ji)].

A última identidade é geral: a parcela antissimétrica permanece quando o covetor não é fechado. Se ∂_i w_j=∂_j w_i e a conexão não tem torção, W é simétrico e obtemos:

    ∇^i T_ij = κ div(w) w_j.

Logo div(w)=0 basta para a conservação. Para κ≠0 e w(x)≠0, a conservação em todas as componentes no ponto também implica div(w)=0. Os casos degenerados estão excluídos apenas da NECESSIDADE; não da suficiência.

Para um potencial φ suave, potential_covector_smooth e potential_covector_closed provam que w=dφ é suave e fechado, usando a comutação das derivadas parciais. A condição div(w)=0 torna-se a equação de onda covariante. A evolução unitária finita construída não fornece essa equação; growing_time_not_conserved verifica um caso em que ela falha.

A correspondência com o calor usa os objetos efetivos, sem trocar o integral de 020 por um polinômio imposto. Para a tela de equilíbrio P, o calor construído e a curva de estados de 022 têm:

    Q(t)/t² → −rate T(d,d)/2
    ΔK(t)/t² → L(d)
    E_heat(t) = Q(t) − rate ΔK(t)/(2π).

Com o tensor normalizado acima, coherent_heat_matching prova E_heat(t)/t²→0. A prova não precisa da equação de onda; precisa da contração nula e da regularidade necessárias ao calor efetivo. coherent_heat_matching_determines_null prova também a necessidade da mesma contração para qualquer outro T que realize a correspondência, quando rate≠0.

A área continua sendo a área induzida da tela anterior, com A(0)=1 e coeficiente −Ric(d,d)/2. O erro de identificação é:

    E_area(t) = ΔS(t) − η (A(t)−A(0))
    E_area(t)/t² → L(d)+η Ric(d,d)/2.

coherent_area_matching_iff_ricci demonstra a equivalência EXATA:

    E_area(t)/t²→0  ↔  η Ric(d,d)=2π T(d,d).

Esse resultado não prova a origem microscópica da relação entropia–área. Ele mostra que, neste modelo, exigir esse erro pequeno já exige o balanço nulo de Einstein. A equivalência é registrada para impedir que a hipótese seja ocultada por uma troca de nome.

CoherentEinsteinBridge.lean fornece dois resultados sob antecedentes explícitos:

- frame_covector_source_unique: em domínio aberto preconexo, qualquer tensor simétrico, diferenciável e conservado com as mesmas contrações nulas difere do candidato por uma constante vezes g, desde que o candidato seja conservado pelas condições de fechamento e onda.
- einstein_from_coherent_area_matching: para uma solda A suave com inversa B suave, w suave e fechado, equação de onda, parâmetros unitários fixos e correspondência de área em toda direção nula não zero, existe Λ constante tal que G+Λg=(2π/η)T. rate e η são não nulos. A conservação de T e a correspondência de calor são provadas dentro da aplicação.

O teorema é geral para os campos suaves admitidos em um domínio de R⁴ com uma solda global nesse domínio. Não fornece a colagem entre cartas nem a origem modular dos quatro componentes e da assinatura lorentziana.

Os controles foram escolhidos antes do código:

| Controle | Resposta verificada |
|---|---|
| w=0 | Tensor zero e fluxo trivial nas direções de frequência zero. |
| Plano, w=e0 constante, κ>0 | T=(κ/2)diag(1,1,1,1), simétrico, não nulo e conservado. O erro de calor/t² vai a zero. O erro de área/t² não vai a zero, para nenhuma η. |
| Plano, w=x0 e0=d(x0²/2) | Covetor suave e fechado, div(w)=1 e ∇T=κ x0 e0. A divergência não é zero em x=e0. A unitariedade direcional continua disponível pelo teorema geral. |

O primeiro controle preserva a degeneração. O segundo prova que conservação e correspondência do calor não bastam para a área. O terceiro prova que unitariedade e coerência direcional não bastam para conservar esse tensor.

[INPUT / OPEN] Permanecem a seleção de w e do eixo/referência, a equação de onda a partir da dinâmica do acervo, a normalização e identificação física de T, a relação entre o parâmetro unitário e o afim, a lei microscópica de área, o horizonte imerso e área integrada espacialmente, as unidades de temperatura/entropia e o coeficiente de Newton. Permanecem também a coerência entre regiões/andares, limites não comutantes ou tipo III, a origem modular da solda/dimensão/assinatura e a globalização.

O modelo finito periódico não substitui o regime hiperbólico da face, nem contorna as obstruções anteriores para a torre-produto. Ele é um candidato adicional de bancada, não uma identificação com a dinâmica canônica do um.py.

Reprodução da custódia, depois da entrega:

    & 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation023.py'

O auditor só lê no modo padrão. Confere bytes, tamanho, identidade do fonte compilado, exit code, estabilidade do fonte, lista de axiomas e correspondência da entrega com o manifesto. A recompilação independente é tarefa da gerência, em cópia, seguindo a ordem de módulos registrada. Fontes locais e oleans copiados são fixados; Lean/mathlib externos continuam dependências do ambiente. O pacote não é integralmente portátil.

Todas as alterações estão em artefatos novos desta continuação sob Chatgpt. As revisões desses artefatos guardam backups imediatos dos bytes. Tentativas rejeitadas são preservadas com seus logs e metadados, sem contar como prova. A entrega anterior foi reconferida em leitura. Originais, entregas já seladas, um.py, kernel canônico, Atlas, memórias, diários, selos e gate não foram editados. Não houve execução ou importação do um.py, coleta observacional, publicação externa ou acesso a confidenciais.

A atualização das superfícies canônicas e a incorporação cabem à gerência pelo protocolo do túnel. O objetivo amplo permanece ativo e não alcançado. A confirmação física não é produzida por estas implicações formais.

[REAL — medição final por script] 7 módulos; 63 teoremas; 1 definição com axiomas impressos separadamente; 9 tentativas rejeitadas preservadas.

| Módulo | Teoremas | Definições impressas |
|---|---:|---:|
| DirectionalUnitaryFamily | 14 | 0 |
| CoherentScalarStress | 9 | 0 |
| CovectorStressCalculus | 6 | 0 |
| ScalarStressConservation | 7 | 0 |
| CoherentHeatMatching | 4 | 1 |
| CoherentEinsteinBridge | 5 | 0 |
| CoherentMatterControls | 18 | 0 |

Todos os fontes finais correspondem aos hashes dos metadados de compilação. Exit 0, fonte estável e nenhum erro, aviso ou sorryAx nos logs finais; todas as declarações impressas dependem apenas de propext, Classical.choice e Quot.sound. A contagem inclui controles e lemas auxiliares, não apenas resultados principais.

O manifesto enumera os artefatos, tamanhos e hashes. O protocolo do túnel e os manifestos anteriores necessários são fixados; os enunciados e as hipóteses viajam com a prova. A gerência ainda deverá recompilar e auditar de forma independente.
