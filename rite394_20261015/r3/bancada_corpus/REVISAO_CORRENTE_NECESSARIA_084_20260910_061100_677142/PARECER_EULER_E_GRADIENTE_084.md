# Revisão independente: canal Euler isolado e múltiplo do gradiente

10/09/2026. Autoria: selected_geometry_design. [DERIVED — revisão matemática escrita]. [REAL — leitura, pins e preservação medidos no recibo]. Investigação084, separada de085. Zero nova execução matemática, CAS ou Lean; nenhum um.py executado ou importado.

**Conclusão.** Li integralmente a [nota da raiz084](<C:/IALD/Central de Patentes/Chatgpt/CORRENTE_NECESSARIA_E_LIMITE_GRADIENTE_084_20260910/EULER_SOZINHO_E_GRADIENTE_ESCALAR_NAO_BASTAM.md>) e seu manifesto. Conferi as fórmulas necessárias nas fontes081–083 e li integralmente a nota083 e sua revisão independente. Não identifiquei erro material nas duas exclusões, no domínio fixado e com coeficientes herdados inertes. A conclusão é:

1. Nenhum múltiplo herdado não nulo de J_W é invariante sob toda a álgebra de Killing. O canal Euler sozinho não produz o alvo.
2. Não existem c∈Rher e f∈N^g com J_W=c□bar J_W+K²f. Isso exclui V=c grad J_W, mesmo admitindo qualquer f invariante no módulo quadrático.

O critério por isotropia é antecedente de minha autoria, posteriormente submetido a revisão independente própria. Este parecer verifica a NOVA aplicação da raiz; não é uma aprovação independente retroativa de minha demonstração do critério.

## 1. Categoria, sinal e passagem às avaliações

O domínio continua sendo a referência espaço-forma orientada em quatro dimensões, K>0 real fixo, κ real fixo não nulo, projeção métrica com φ0 constante e N=Rher⊗Sym²Mcal. Mcal é o quociente dos jatos lineares Weyl/EOM, e não uma torre livre. Rher é uma álgebra real unital não nula, cujos elementos são inertes sob as ações usadas. Os candidatos têm jatos finitos por elemento.

A [redução084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>), §5, fornece o critério J_W=div V+K²f, com f∈N^g. O sinal positivo da divergência coincide com a [corrente082](<C:/IALD/Central de Patentes/Chatgpt/OBSTRUCAO_CE_E_CORRENTE_HORIZONTAL_082_20260910/CLASSE_CE_DO_RESIDUO_E_CORRENTE_GRADIENTE.md>), equações(3–4). Negar toda a primitiva troca simultaneamente o sinal do alvo; não há assimetria relevante entre provar exatidão de a e de −a.

A invariância sob todas as transvecções implica ∇bar_a f=0 no próprio quociente, pela identificação082. Ser apenas um escalar de Lorentz seria insuficiente. A derivada preserva o ideal de EOM e seus prolongamentos. A família TT usada resolve essas equações numa vizinhança inteira; portanto avaliar uma relação e suas derivadas nessa família é legítimo. O uso do módulo efetivo, com suas relações, não foi substituído por avaliações em variáveis Weyl livres.

Para um pseudoscalar no domínio orientado fixado, a derivada covariante de primeira ordem é a derivada ordinária de sua componente escalar. No ponto, a componente z corresponde a uma direção de transvecção. Não se precisa estender essa identificação da transvecção particular por toda a carta para obter a condição pontual necessária.

## 2. Canal Euler isolado: separação por uma unidade

A [fonte081](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md>), equação(17), fornece

J_W(p0)=−4k/z0,    ∂zJ_W(p0)=4k³−28k/z0².

A segunda fórmula foi obtida mantendo ℓ e k constantes ANTES de avaliar f(z0)=0, f′(z0)=1 e ℓ=z0. Ela não é a derivada do primeiro valor já especializado.

Em k=1/z0, ∂zJ_W=−24/z0³. Se λJ_W∈N^g, com λ herdado, a derivada da igualdade de invariância fornece λ∂zJ_W=0. A avaliação estendida por identidade em Rher dá (−24/z0³)λ=0.

Todo real não nulo é uma unidade numa álgebra real unital não nula. Portanto λ=0, inclusive se Rher tiver nilpotentes ou divisores de zero. Não houve avaliação de λ em pontos numéricos, nem hipótese de que tais pontos detectem seus nilpotentes. Em particular, a linha Rher J_W encontra N^g apenas em zero.

Logo J_W=K²f com f∈N^g é impossível. Isso também exclui qualquer V com divergência zero no critério. Não determina N^g inteiro e não autoriza trocar um f arbitrário por J_W/K² sem verificar a invariância que acaba de falhar.

## 3. Prolongamento de □J_W e ordem correta das substituições

Li a [nota083](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATO_DERIVADA_WEYL_083_20260910/CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md>), em particular(12–13),(17),(20–21), e a [revisão independente083](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md>), §§2–5. Os contratos utilizados são

□bar J_W=2J1+12KJ_W,
J1′(p0)=8k⁵−352k³/z0²+560k/z0⁴.

A primeira identidade vale on-shell linear numa vizinhança e inclui o sinal Lorentziano de □bar. Não foi importada de outra assinatura. K=ℓ⁻² é constante espacial; sua identificação com z0⁻² só é feita após derivar e avaliar.

Refiz a combinação escrita:

∂z□bar J_W = 2J1′+12KJ_W′
=16k⁵+(-704+48)k³/z0²+(1120−336)k/z0⁴
=16k⁵−656k³/z0²+784k/z0⁴.

Em k=1/z0 e k=2/z0, respectivamente, os coeficientes são
16−656+784=144 e 16·32−656·8+784·2=−3168.
As duas avaliações de ∂zJ_W são −24/z0³. Assim a tabela da raiz está correta.

Não foi preciso reexecutar os dez controles083. O antecedente083 fornece a igualdade de J1 covariante em toda a vizinhança; as contas acima são derivações escritas e não novos resultados CAS. Não se derivou K=z⁻² nem se ignorou uma dependência temporal sem o contrato helicoidal083.

## 4. A exclusão conjunta não restringe artificialmente f

Se J_W=c□bar J_W+K²f, com c herdado inerte e f∈N^g, derivar elimina f por sua invariância, independentemente de como f seja representado. As duas avaliações dão

−24/z0³−144c/z0⁵=0,
−24/z0³+3168c/z0⁵=0.

A segunda menos a primeira é (3312/z0⁵)c=0. O coeficiente é novamente uma unidade real; c=0. A primeira equação seria então um real não nulo vezes a unidade igual a zero, impossível numa álgebra real unital não nula.

Os dois testes usam o MESMO K, z0, anel e coeficiente c. Só a frequência da solução TT varia. Isso é essencial: a proposição exclui coeficientes herdados fixados, e não coeficientes escolhidos depois como funções do k de teste. Não se introduziram inversos de elementos de Rher nem se fez uma separação de nilpotentes.

A prova permite qualquer f∈N^g, inclusive um elemento ainda desconhecido que não seja múltiplo de J_W. Ela não usa N^g=0. Pela igualdade div(c grad J_W)=c□bar J_W, cobre também a soma desse vetor com qualquer corrente de divergência nula no quociente.

## 5. Finitude, fronteira e custódia

Os elementos continuam finitos em jatos, e os prolongamentos necessários permanecem finitos. Para cada candidato, a avaliação de todos os jatos exigidos é definida pela solução local. Não se invoca um limite de truncamentos, uma homotopia infinita, Mittag–Leffler ou regularização da série.

O resultado não classifica vetores naturais com outras contrações, gradientes de outros escalares, misturas com jatos superiores ou a imagem geral de div modulo K²N^g. Não demonstra uma anomalia efetiva, QME, suficiência UV, transporte ao fundo sigma físico ou admissibilidade causal integral. Também não reabre a entrega083 nem incorpora085.

[REAL — documental] O recibo mede antes/depois os oito arquivos efetivamente consultados ou pinados, compara os pins do manifesto e verifica os quatro links locais da nota revisada. O emissor da origem foi somente medido, não executado nem apresentado como código matemático auditado. O helper desta revisão faz apenas leitura, hashes, comparações documentais e gravação nova por temporário verificado. Nenhum arquivo anterior foi modificado.
