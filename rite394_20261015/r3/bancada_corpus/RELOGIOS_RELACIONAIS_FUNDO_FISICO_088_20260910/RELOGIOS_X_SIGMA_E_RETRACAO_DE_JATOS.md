# Relógios naturais do fundo físico e retração local dos jatos field/ghost

10/09/2026. Investigação088, separada da entrega087. Autor: /root/finish_gibbs_realization. [DERIVED — demonstração escrita; revisão independente ainda não consumida nesta emissão]. [REAL — leitura e pins no manifesto].

**Resultado.** No fundo físico069, o escalar composto X=g⁻¹(dφ,dφ)_γ, junto da aplicação sigma, fornece um mapa de relógios de posto quatro em TODO o interior (0,π)×S³. Sua inversa é tensorial, sem carta global de S³. O extrator F(h,ξ)=E⁻¹(ξ,δX) coincide com o extrator diferencial já escrito068. Além da identidade FK=Id, construímos uma mudança diferencial invertível de campos e de seus jatos: (h,ξ) corresponde a (H,ζ), com H um tensor de traço espacial zero e ζ=F(h,ξ). No subcomplexo livre field/ghost, s₀H=0, s₀ζ=C e s₀C=0. A homotopia dos pares é explícita e finita por coeficiente.

O resultado é cinemático e off-shell nos campos perturbados. Não demonstra a cohomologia BV completa, um operador BRST quântico, a QME ou admissibilidade causal de contratermos. Os coeficientes usados pertencem a uma localização dos dados de fundo onde E é invertível; não cobrem fundos sigma constantes.

## 1. Dados da fonte, notação e o que não é uma entrada independente

A [construção causal069](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md>), §§1–2, fixa

    M=(0,π)×S³,   ḡ=dr²−a(r)²γ,   a(r)=2cos(r/2),
    φ̄(r,z)=z,    g_t=ḡ+t h,        φ_t=Exp_φ̄(tξ),
    ξ∈Γ(φ̄*TS³).

γ é a métrica redonda do alvo. O mapa φ̄ é a projeção à esfera, não uma carta real global. t é o parâmetro de variação, distinto de r. As fórmulas são globais como fórmulas de fibrados sobre o interior; testes da construção causal têm suporte compacto interior.

O [dicionário069](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/DICIONARIO_GRASSMANN_E_ACAO_BV.md>), §3, fixa

    s₀(h,ξ)=K C,   K v=(Lie_v ḡ, dφ̄(v)),   s₀C=0.       (1)

C é o ghost difeomórfico ímpar, seção de TM. Os coeficientes de fundo são s₀-inertes. O K de (1) é um operador de gauge, não curvatura seccional ou uma cópia de outro gerador canônico. O [Jacobi066](<C:/IALD/Central de Patentes/Chatgpt/QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md>), §§1,2,5, fornece os mesmos fibrados e convenções. A evolução histórica dos estados/propagadores não é reexaminada aqui.

Defina, para quaisquer campos da ação ambiente,

    A=dφ̄ : TM→E_φ,   E_φ=φ̄*TS³,
    S=φ̄*γ,          S_{μν}=γ(A_μ,A_ν),
    X(g,φ)=g^{μν}γ_ij(φ)∂_μφ^i∂_νφ^j,
    X̄=X(ḡ,φ̄),    β=dX̄.                                (2)

X e δX são COMPOSTOS de g,φ e de h,ξ, respectivamente. Não acrescentamos uma quarta matéria independente, um novo momento canônico ou um campo escalar propagante. A ação ambiente já assumida na069 permite as perturbações (h,ξ); não se infere dessa hipótese que elas venham todas dos mesmos cinco pesos categóricos. A dependência conjunta será conservada em todas as inversões abaixo.

## 2. Derivada de X e identidade de gauge

Se D é a conexão do alvo puxada por φ̄, a compatibilidade métrica e a ausência de torção dão

    δS_{μν}=γ(D_μξ,A_ν)+γ(A_μ,D_νξ).

Com h^{μν}=ḡ^{μα}ḡ^{νβ}h_{αβ} e δg^{μν}=−h^{μν}, segue a identidade intrínseca

    δX[h,ξ]=−h^{μν}S_{μν}
              +2ḡ^{μν}γ(D_μξ,A_ν).                    (3)

Prova em carta apenas para conferir o primeiro passo: diferenciar γ_ij(φ_t)∂μφ_t^i∂νφ_t^j produz o termo ∂_kγ_ij ξ^k, além das duas derivadas de ξ. Pela identidade ∂_kγ_ij=γ_ℓj Γ^ℓ_ki+γ_iℓ Γ^ℓ_kj, os três termos se agrupam exatamente nas duas derivadas covariantes. Como o resultado é tensorial, as cartas colam; não se escolhe uma carta contendo S³ inteira. A exponencial só fixa a derivada inicial ξ, não introduz um termo adicional em primeira ordem.

No fundo (1), A_r=0 e A_i é a identificação do espaço tangente da esfera. Portanto

    X̄=−3/a²,
    δX=−a⁻⁴γ^{ij}h_{ij}−2a⁻² div_γξ.                 (4)

h_{rr} e h_{ri} não aparecem em (4). D_rξ existe, mas seu coeficiente em (3) é zero porque A_r=0 e ḡ^{ri}=0. A divergência é a da seção tangente à S³ em cada r, não a divergência espaço-temporal de quatro componentes independentes.

A naturalidade do escalar completo X fornece, SEM EOM,

    δX[Kv]=Lie_v X̄=β(v),
    s₀δX=β(C)=C^μ∂_μX̄.                               (5)

Para controlar explicitamente todos os termos de derivada de ghost, no bloco espacial

    (Lie_v ḡ)_{ij}=−2aa'v^rγ_{ij}−a²(Lie_{v_sp}γ)_{ij},
    γ^{ij}(Lie_v ḡ)_{ij}=−6aa'v^r−2a²div_γv_sp.

Inserir isso em (4), junto de ξ=A v=v_sp, cancela os dois termos de divergência e dá 6a'/a³ v^r. A mesma identidade linear vale para o ghost ímpar C. O passo usa apenas covariância e diferenciação de (2); não usa Einstein, a equação sigma, equações de ghosts ou gauge fixado.

## 3. O mapa E é invertível em todo o interior

Escreva Hubble=𝔥=a'/a. Como

    a'=−sin(r/2),  a>0,  a'<0       para 0<r<π,
    β=β_r dr,     β_r=X̄'=6a'/a³=6𝔥/a²<0,              (6)

β não se anula em nenhum ponto interior. A=dφ̄ é sobrejetivo de posto3, ker A=R∂_r é uma linha timelike e β é não nulo nessa linha. Logo o mapa de fibrados

    E: TM→E_φ⊕R,          E(v)=(A v,β(v))               (7)

é um isomorfismo real de posto4 ponto a ponto: E(v)=0 implica v∈ker A e β(v)=0, logo v=0; domínio e alvo têm o mesmo posto. Seus coeficientes e sua inversa são suaves no interior.

Há até uma descrição global sem reduzir S³ a três coordenadas reais: χ̄=(φ̄,X̄) é difeomorfismo de (0,π)×S³ para S³×(−∞,−3/4). A inversa temporal é r=2arccos√(−3/(4X̄)). Essa expressão controla o posto global; não é necessária para a construção tensorial. O mapa (7) é a derivada de χ̄, com a ordem dos fatores da aplicação escrita.

Os extremos temporais não pertencem ao domínio. Em r=0, β_r=0 e a inversa deixa de existir; em r=π a métrica deixa de ser não degenerada. Não se afirma limite uniforme nesses extremos. Em qualquer compacto interior os coeficientes da inversa e suas derivadas de ordem fixada são limitados. Isso conserva suporte de operadores diferenciais locais, mas não decide as cotas causais de renormalização.

## 4. Inversa tensorial, sem frame ou carta global

Defina o adjunto algébrico A†:E_φ→TM pelas métricas de fundo:

    ḡ(A†y,v)=γ(y,A v).

No presente fundo A A†=−a⁻² Id_{E_φ}. Mais geralmente, num aberto de fundos onde A é sobrejetivo e ker A é timelike, A A† é invertível. Ponha

    B=A†(A A†)⁻¹,     P=Id−B A,
    w=P(β#),         d=β(w),     n=w/d,                 (8)

onde β#=ḡ⁻¹β. B é uma inversa direita de A; BA é a projeção ḡ-ortogonal sobre (ker A)^⊥ e P sobre ker A. P é autoadjunto. Assim d=ḡ(w,w)>0 se β|ker A é não nulo. Temos A n=0 e β(n)=1.

A inversa de (7) é

    E⁻¹(y,f)=B y+n[f−β(B y)].                          (9)

De fato A do lado direito é y; aplicar β dá f. Para v qualquer, v−BAv está em ker A e é reconstruído por sua avaliação por β, provando também E⁻¹E=Id. Todas as operações são contrações, adjuntos algébricos, projeções e inversões em fibras. Não há inversa de operador diferencial, solução elíptica, Green ou escolha de base global.

No fundo físico, β anula (ker A)^⊥, β# pertence a ker A e

    B=−a²A†,   βB=0,   n=β#/ḡ⁻¹(β,β)=(β_r)⁻¹∂_r.

Logo (9) reduz a B y+n f. Essa simplificação não deve ser usada num fundo genérico se βB não for zero. A fórmula geral(9) continua natural sob embeddings que transportam ḡ,φ̄,γ e sob mudanças de cartas do alvo.

**Classe de coeficientes.** (8–9) são suaves, de ordem finita nos jatos de fundo, no aberto onde A A† e d são invertíveis. Em descrição por jatos são expressões racionais nas inversões indicadas, com os coeficientes suaves da métrica alvo. A operação localiza a categoria nesse aberto. Ela não constitui uma função suave universal nos jatos de TODOS os fundos. Em particular, φ̄ constante tem A=0 e está excluída, assim como β|ker A=0. Não se transporta esta inversa para o teste espaço-forma/sigma constante087.

## 5. O par BRST e sua relação exata com a068

Defina o operador diferencial local, de ordem um,

    F(h,ξ)=E⁻¹(ξ,δX[h,ξ]),      ζ=F(h,ξ).              (10)

δX não foi convertido numa variável independente: sua fórmula(3) é parte de (10). As identidades(1),(5),(9) dão

    F K=Id,           s₀ζ=C,           s₀C=0.          (11)

Em componentes do fundo,

    ζ^i=ξ^i,
    ζ^r=δX/β_r
        =[−a⁻²γ^{ij}h_{ij}−2div_γξ]/(6𝔥).            (12)

Esta é EXATAMENTE a fórmula(3.1) da [extensãoBRST068, §3](<C:/IALD/Central de Patentes/Chatgpt/EXTENSAO_BRST_COMPLETA_20260909_220941_811364/EXTENSAO_BRST_E_CORRECOES_SUAVES.md>), onde o extrator se chama 𝓔 e já se demonstrava 𝓔K=1 off-shell. Portanto088 não reivindica descobrir um extrator ausente. Os acréscimos são sua realização como relógios compostos naturais, a inversa global de fibrados(9) e o controle explícito dos jatos e de suas variáveis remanescentes abaixo. O E algébrico(7), o F diferencial(10) e o propagador causal homônimo de outras fontes são objetos distintos.

## 6. Mudança diferencial invertível, com as relações eliminadas

Encontrar s₀ζ=C não bastaria se ζ fosse uma coordenada dependente com relações não tratadas. Aqui se pode construir a inversa completa. Defina

    T^{μν}=ḡ^{μα}ḡ^{νβ}S_{αβ},   τ(q)=T^{μν}q_{μν},
    W₉=ker[τ:S²T*M→R],
    H=h−Lie_ζ ḡ.                                    (13)

T não é o tensor de energia-momento: é apenas o contravariante definido nesta equação. W₉ é um fibrado de posto9, pois τ é não nulo; no fundo τ(S)=3/a⁴>0. Sua restrição τ(H)=0 é precisamente γ^{ij}H_{ij}=0.

Ponha u=(h,ξ) e U=u−KF u. De (11), FU=0. Como a primeira componente de E F u é ξ, a componente sigma de U é ξ−Aζ=0. Assim U=(H,0) e

    0=δX[H,0]=−τ(H).                                 (14)

Concluímos que H é seção de W₉. Além disso s₀H=Lie_C ḡ−Lie_(s₀ζ)ḡ=0. A inversa para seções ARBITRÁRIAS H∈Γ(W₉) e ζ∈Γ(TM) é

    h=H+Lie_ζḡ,                ξ=Aζ.                  (15)

De (3), F(H,0)=0; de (11), F(Kζ)=ζ. Logo aplicar (10),(13) a (15) devolve exatamente H,ζ. A composição no outro sentido é a definição de H e a primeira componente de E F. Portanto

    Γ(S²T*M⊕E_φ)  ↔  Γ(W₉⊕TM)                        (16)

é uma mudança LINEAR diferencial local com inversa diferencial local. Ela depende somente dos dados de fundo. Na direção antiga→nova, ζ usa uma derivada de ξ e H até duas derivadas de ξ/uma de h; na inversa, h usa até uma derivada de ζ e ξ nenhuma. Os13 campos ambientes foram reescritos como9+4 variáveis; isso é uma contagem cinemática, não9 graus de liberdade físicos após EOM/constraints.

Equivalentemente, P_field=Id−KF é um projetor diferencial de ordem no máximo2, com P_field²=P_field, FP_field=0 e P_field K=0. Sua imagem é exatamente {(H,0):H∈Γ(W₉)}. Essas identidades seguem de FK=Id e não exigem EOM. O projetor não é um propagador ou uma projeção ortogonal em espaço de estados.

## 7. Prolongamento: o que é local e triangular nos jatos

Prolongar(10),(13),(15) por derivadas totais fornece substituições mutuamente inversas na álgebra de jatos infinitos, entendida como LIMITE DIRETO das funções que dependem de finitos jatos. As composições já são identidades diferenciais para seções arbitrárias; portanto suas prolongações são identidades de jatos, e não identidades testadas somente em soluções escolhidas.

Não se afirma um isomorfismo de J^k com o mesmo J^k: uma função de k jatos novos pode envolver até k+2 jatos antigos; na direção inversa, até k+1. Isso é um aumento FINITO de ordem. Em cada coeficiente polinomial/valência fixada entram finitíssimos jatos; a transformação preserva essa classe. Não há integração de derivadas, série infinita de ordem diferencial ou escolha de dados de Cauchy.

As coordenadas independentes dos novos jatos podem ser construídas em cartas por eliminação algébrica de uma componente de H pelo τ(H)=0 e por prolongação desse constraint. Intrinsecamente, use uma conexão em W₉. Uma escolha natural é

    Π_W q=q−S τ(q)/τ(S),      ∇^W=Π_W∘∇̄|W₉.          (17)

τ(S) é não nulo no domínio. As derivadas covariantes simetrizadas de ∇^W são coordenadas de jatos livres do fibrado W₉: a ordem mais alta coincide com a derivada parcial simetrizada, e os termos adicionais têm ordem inferior. A mesma conexão de Levi-Civita ∇̄ é usada nos dois fibrados TM de ζ e C. Não tratar derivadas covariantes não simetrizadas como geradores livres: seus comutadores são as relações de curvatura do fundo.

Como s₀ fixa todas as conexões e projeções de fundo, nas coordenadas de jatos obtemos

    s₀H_I=0,        s₀ζ_I=C_I,       s₀C_I=0           (18)

para cada multiíndice simetrizado I. As relações de curvatura são as mesmas para ζ e C e são preservadas por(18). A escolha por cartas ou por(17) cola em mudanças naturais de trivialização; não requer paralelizar S³ por uma base escolhida.

Esta é a triangulação local efetiva: primeiro se substituem ξ e o traço espacial de h pelos quatro componentes de ζ usando(12); depois os nove componentes restantes são corrigidos por Lie_ζḡ. Na inversa(15) recuperam-se ξ e h sem resolver PDE. A descrição de projetores evita atribuir independência a δX além dos próprios h,ξ.

## 8. Retração algébrica APENAS do subcomplexo field/ghost

Considere a álgebra de polinômios nos finitos jatos de H,ζ,C, com coeficientes suaves naturais dos fundos localizados do §4. ζ e H são pares de ghost zero; C é ímpar de ghost um. Neste parágrafo não entram antifields, fontes centrais, antighosts ou equações de movimento.

Defina a derivação ímpar ρ de ghost−1 por

    ρ(C_I)=ζ_I,    ρ(ζ_I)=0,    ρ(H_I)=0,
    ρ(coeficientes de fundo)=0.                         (19)

Ela é bem definida globalmente: substitui jatos do MESMO fibrado com a MESMA conexão e se prolonga como derivação graduada. Os sinais são os da derivada à esquerda nos geradores ímpares. Conferindo em cada gerador e usando que o anticomutador de derivações ímpares é derivação, segue

    s₀ρ+ρs₀=N_pair,                                   (20)

onde N_pair conta fatores ζ_I e C_I. Não conta os fatores H. Seja π a avaliação ζ_I=C_I=0 para TODOS os jatos, com inclusão ι na álgebra original. Para a parcela de grau pair n>0, defina h_pair=ρ/n; em grau zero, h_pair=0. Então

    s₀h_pair+h_pair s₀=Id−ιπ.                          (21)

A demonstração é finita para cada polinômio e não divide por campos ou por número de ghost. Um cociclo f satisfaz f−ιπf=s₀h_pair f. Se seu ghost é positivo nesse SUBCOMPLEXO, πf=0, logo ele é s₀-exato ali. A álgebra de jatos de H permanece em ghost zero; não foi apagada. A transformação e a homotopia preservam a valência total em flutuações. Podem ser aplicadas coeficiente a coeficiente em uma série por valência que tenha finitos jatos em cada coeficiente, sem postular uma cota uniforme para a série inteira.

[KNOWN — mecanismo delimitado] A identidade de contagem e a homotopia dos pares, incluindo seus jatos, são o mecanismo do Apêndice2.B, equações(2.48)–(2.51), de [Barnich–Brandt–Henneaux, hep-th/0002245v3](https://arxiv.org/pdf/hep-th/0002245). Aqui a mudança de variáveis, o domínio e as relações foram demonstrados antes de aplicar esse mecanismo. Não se importou uma classificação de anomalias ou um teorema BV completo por essa citação.

A prova(21) tem alcance field/ghost. Para incluir antifields é necessário escrever sua transformação e mostrar compatibilidade com essa retração; para o s não linear é necessário controlar a perturbação por valência e os demais geradores. Nenhum desses passos é presumido pelo simples doublet. A análise de formas, operadores quânticos, estados e contratermos exige ainda sua própria classe e seus contatos. A presente nota não declara H(s) inteiro zero nem QME.

## 9. Consequência e fronteira de admissibilidade

[DERIVED] A hipótese de um relógio não estacionário foi paga para o FUNDO FÍSICO069 inteiro: X̄'=6a'/a³<0, E é isomorfismo e F recupera o extrator068 de modo natural. A retração de jatos field/ghost(16–21) acrescenta um contrato efetivo, incluindo independência, relações de curvatura e finitude por coeficiente. O resultado vale sem impor EOM aos campos perturbados; o fundo foi escolhido da069, mas a construção se estende ao aberto de fundos caracterizado em(8).

[OPEN — não deduzido aqui] A localização por inversos de gradientes/Gram de fundo pode não preservar a classe UNIVERSAL de contratermos e seus requisitos de escala/regularidade. Preservar valência e ser suave no aberto regular não prova admissibilidade causal no domínio inteiro. A dependência de ḡ,φ̄ e seus jatos deve permanecer na categoria efetivamente autorizada; não se decreta que todo coeficiente natural localizado pertença a Q2. A presente investigação não estende o teorema ao sigma constante ou a referências onde β estaciona.

[OPEN — fora desta nota] Transporte à cohomologia BV completa e ao diferencial não linear, normalizações, remoção da anomalia/QME, carga e positividade interagentes, observáveis globais, UV e reconstrução pelos mesmos dados probabilísticos. A existência de relógios não demonstra por si que as variáveis ambientes sejam uma quantização dos cinco pesos. Fase/ramo e H3 interno anteriormente pagos não são reabertos; nenhum gate é alterado.

## 10. Leitura e custódia

Foram relidas a construção causal069, o dicionário069 e as seções pertinentes da068 e066 para os dados de fundo, o extrator e a convenção BRST. O manifesto distingue leitura integral das duas fontes069 de leitura das seções indicadas das fontes066/068. A referência primária BBH foi consultada na web; não se inventa um hash local de PDF.

A busca inicial por nomes encontrou diretórios de dependências com acesso negado, alheios ao alvo; a leitura seguinte foi limitada às quatro fontes identificadas. Não se declara uma varredura exaustiva do computador. Os arquivos-fonte não foram executados e seus pins foram medidos antes/depois. Somente arquivos NOVOS desta pasta, escritos por temporário exclusivo, conferência e rename sem sobrescrita. Zero execução matemática, CAS, Lean, natureza, um.py ou recaptura canônica. Uma eventual revisão independente será um artefato separado; não é antecipada nesta nota.
