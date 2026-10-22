# Definição conjunta da bancada e retorno ao diamante modular

[DERIVED — composição documental das construções existentes; não novo teorema Lean]

Responde ao [recibo do operador de16/09](../TUNEL/PARA_CHATGPT/RESPOSTA_OPERADOR_16SET_DEFINICAO_CONJUNTA_NO_ESTUDO_INTEIRO.md). A definição está distribuída no estudo. Não se pede novamente um arquivo único, uma ação genérica ou um estado que já tenha sido construído. Os relatórios `AUDITORIA_CONJUNTA_CORE`, `AUDITORIA_CONJUNTA_GEOMETRIA` e `AUDITORIA_CONJUNTA_FISICA` discriminam as leituras; o manifesto desta entrega deve ser consultado para a cobertura efetivamente concluída.

## 1. Objeto composto, sem trocar seus domínios

O pacote existente é uma família com dados declarados:

\[
\mathfrak P=(S_0^{\rm BV},\{\mathcal T_n\}_{\mathfrak r},
\{b_i(\mu)\},\bar g,\bar\phi,\omega_{067},
\mathscr D,Q_0,R_0,\chi,\text{condições de bordo}).
\]

`mathfrak r` é a prescrição finita de renormalização, `chi` o cutoff da construção causal; `mathcal T_n` são produtos temporais, diferentes do transporte de testes `T_t` no problema modular. `R0` nesta lista é a homotopia livre de072/073, diferente do resto modular `R`. A ação, os produtos, o estado e o domínio têm fornecedores concretos. A existência de todos esses fornecedores não autoriza apagar suas hipóteses de composição.

**Antecedentes que esta composição preserva [KERNEL documentado, sem recompilação nesta rodada]:** a auditoria geométrica identifica estados globais no mesmo Hilbert sob afinidade positiva026–027, resposta entrópica finita na classe somável028, tensor conservado e casamento área–entropia numa família curva029, cociclo/densidade relativos030–033 e esperança centralizante normal completamente positiva046–047. Também identifica o balanço óptico finito corrigido051, a reconstrução exata de g/T pelo registro enriquecido058 e um potencial XX local somável059. Assim, nem “só existe um corte finito” nem “a área é sempre apenas assumida” descrevem o estudo. As pendências de estado/cociclo que059 registrava são consumidas por060–061 na classe somável; não são dívidas atuais dessa classe. Ver [auditoria geométrica, §§1–7](AUDITORIA_CONJUNTA_GEOMETRIA.md).

**Core e fechamento já pagos [KERNEL documentado]:** a [auditoria A1/A2 e Friedmann](AUDITORIA_CONJUNTA_CORE.md) identifica o fornecedor `scalarInverseLimitTraceData P` do mesmo traço normal, fiel, semifinito e escalado, sem premissa tracial residual. A2 fornece suporte de traço1, faces de traço1/2, extensão cíclica compatível com o cone e a montagem `regularFullWitness : FullTGLWitness`. Seu Hamiltoniano mínimo é `1-P_F`, com gap relativo; a cunha mínima ali usa `U(t)=1`. A realização está paga no seu tipo, sem que esse Hamiltoniano seja automaticamente a carga microscópica regional. O peso dual de unidade infinita, o traço escalado e um estado normalizado no canto são objetos diferentes.

**Cosmologia já construída [KERNEL sob INPUT declarado]:** B2/B3 fornece `flrwStress` e conservação/Friedmann nas hipóteses indicadas, com constante cosmológica comum; B4 prova a diferença entre as rotas setorial e total e conserva o termo da derivada do fator variável. A escolha do operador pelo fator total já está respondida e é preservada. B1′ fornece uma interface de quarta face cujo enunciado recebe `hEOM`: não se deve tratá-la como uma derivação variacional adicional. O stress efetivo real de FLRW não é identificado por esse tipo, sozinho, com a inserção operatorial renormalizada069 ou sua expectativa. A composição registra ambos e exige somente sua identificação quando ela for usada fisicamente.

### Ação renormalizada

**[INPUT/POSTULATE, com consequências DERIVED]** A ação ambiente física é

\[
S_0[g,\phi]=-{1\over2\kappa}\int(R_g-2\Lambda)d\mu_g
 +{c\over2}\int g^{\mu\nu}
 \langle\partial_\mu\phi,\partial_\nu\phi\rangle\,d\mu_g.
\]

067 §§2–3 fornece o representante probabilístico livre e o transporte da Hessiana e corrente; §4 fixa a convenção de sinal e o fundo. O alvo sigma é `S3`. A adoção dessa ação não é inferida apenas de `omega(I)=1`.

**[DERIVED+KNOWN]** 068–069 fornece a extensão BRST e, na mesma expansão física `g=bar g+z h`, `phi=Exp_barphi(z xi)`, os produtos temporais renormalizados locais/covariantes e a álgebra interagente auxiliar. Isto já é uma construção perturbativa de interação. Não é correto registrá-la como ausente. A fonte exata é [Produtos temporais069](../CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md), §§1–7, com o dicionário BV da mesma pasta.

**[DERIVED, família EFT]** Os termos locais incluem o representante

\[
S_4=\int(b_1Q^2+b_2W_{\mu\nu}W^{\mu\nu})d\mu_g,
\quad W_{\mu\nu}=\langle\partial_\mu\phi,\partial_\nu\phi\rangle,
\quad Q=g^{\mu\nu}W_{\mu\nu}.
\]

069–070 calcula o coeficiente acoplado de uma volta, suas reduções por EOM/divergências e o fluxo logarítmico. [Redução070](../REDUCAO_ON_SHELL_RG_070_20260909_232623_681687/REDUCAO_EFT_E_FLUXO_LOGARITMICO.md), §§1–7:

\[
A_1=-\frac{13s^2}{16}+\frac{7s}{6}+\frac16,
\quad A_2=\frac{27s^2}{8}-s+\frac13,
\quad s=\kappa c.
\]

Os valores finitos `b_i(mu0)` não são fixados por esses logaritmos. A composição é uma família renormalizada com parâmetros e prescrição, não a inexistência de renormalização. A classificação integral de operadores em todas as ordens, a QME satisfeita e um limite UV não estão contidos na tabela de uma volta. `beta_RG` não é `beta_TGL`.

### Estado/vácuo

**[DERIVED+KNOWN]** 067 fornece `omega067`, estado quase livre positivo Hadamard do sistema físico linear, com setores S/V/TT completos no quociente admitido. O fundo é `g=dr²-4cos²(r/2)gamma`, `phi=id`, `c>0`, `kappa c=4`, `Lambda=3/4`, em compactos interiores de `(0,pi) × S3`. Não se identifica por nome esse estado com um vácuo preferido de qualquer espaço-tempo.

**[DERIVED]** 073 fornece uma polarização BRST adaptada à mesma covariância067, a Fock–Krein auxiliar, o domínio nuclear suave `mathscr D`, a carga livre e a homotopia. [Fock073](../FOCK_HADAMARD_QUARTETOS_073_20260910/FOCK_DOMINIO_WICK_E_P0.md), §§1–7:

\[
Q_0R_0+R_0Q_0=1-P_{\rm phys}.
\]

Isto paga P0 e a realização Wick compacta de P1 que072 requeria. A frase histórica de072 dizendo que P0 ainda precisava ser realizado foi superada por073; não deve reaparecer como falta atual.

**[DERIVED+KNOWN, condicional]** [Estado072](../POSITIVIDADE_BRST_FORMAL_072_20260910/ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md), §§2,4–7, já dá a recorrência

\[
\psi_n=-R_0\sum_{j=1}^{n}Q_j\psi_{n-j},\quad
\Omega(z)=\|I(z)\Omega_{067}\|^{-1}_{\rm formal}I(z)\Omega_{067},
\quad \omega_z([A])=[\Omega(z),A(z)\Omega(z)].
\]

Ela produz estado físico positivo **formal** quando a carga interagente renormalizada implementa o diferencial nilpotente com os contatos e a involução corretos. 073 torna essa recorrência representacionalmente utilizável; não produz automaticamente a carga que ela recebe. Convergência a acoplamento finito, um estado de von Neumann e compatibilidade adiabática/global não seguem de positividade formal coeficiente a coeficiente.

**Estado da torre é outro fornecedor existente:** 061 constrói o estado fiel normal de Araki para potencial local globalmente somável; 063 amplia a dinâmica à classe extensiva quase local, com ressalva explícita sobre extensão normal. A prova modular/KMS dessa torre permanece válida no seu domínio. Não há nesta composição um mapa identificado que converta automaticamente sua família de estados na rede relativística física067/069.

### Tensão e fronteira

**[DERIVED]** [Fonte quartica068](../RENORMALIZACAO_SIGMA_EFT_20260909/FONTE_QUARTICA_E_HABITANTE_CORRIGIDO.md), §§1–4, varia a ação e fornece, com `T=2/sqrt|g| delta S_m/delta g^{-1}`,

\[
T^{(2)}_{\mu\nu}=c(W_{\mu\nu}-g_{\mu\nu}Q/2),
\]
\[
T^{(4)}_{\mu\nu}=4b_1QW_{\mu\nu}
 +4b_2W_{\mu\rho}W_\nu{}^\rho-g_{\mu\nu}(b_1Q^2+b_2W^2).
\]

A conservação da fonte clássica total acompanha a EOM sigma corrigida. A construção069 permite inserções locais renormalizadas com a liberdade causal indicada; a carga física requer ainda o levantamento compatível com as identidades BRST. A derivada de um funcional efetivo, a inserção operatorial e a expectativa dessa inserção devem manter papéis separados. O cálculo de uma parcela local não equivale à expectativa quântica total.

**[DERIVED]** [Transporte simplético067](../ADENDO_LINEARIZADO_COARSE_LIVRE_20260909_214421_410751/ADENDO_LINEARIZADO_E_SIMPLÉTICO.md), §§6–7, fornece o potencial composto com termo
`J^mu=E_alpha b^{alpha mu}_i p^i`. Nas soluções linearizadas os potenciais casados produzem correntes iguais. A mudança `theta -> theta+dY` deixa um termo em `partial Sigma`; condições de bordo ou o seu tratamento explícito permanecem necessários. A redução070 também distingue densidades iguais módulo divergências de densidades pontualmente iguais. Não apagar essas correntes na região finita.

O critério para um Hamiltoniano que gere uma transformação no espaço reduzido é uma igualdade de variação com a forma simplética, incluindo sua contribuição de bordo. Não se obtém esse Hamiltoniano tomando a variação de toda a ação gravitacional como um tensor de matéria e impondo depois suas EOM: essa operação confundiria vínculos com a carga que se pretende comparar.

## 2. As costuras remanescentes são específicas

| Costura | O que está disponível | O que precisa coincidir no mesmo objeto |
|---|---|---|
| Q2 → QME/P2 | Produtos renormalizados e quebra local consistente; cohomologia suave e análises naturais071–087 | Primitiva da quebra concreta no espaço admissível, renormalização finita implementada e corrente/carga com suas identidades |
| P0/Wick → estado interagente | Domínio073 e recorrência072 | Coeficientes da carga anterior; compatibilidade das construções locais para o alcance global reivindicado |
| Fonte local → carga regional | T2, T4, correntes variacionais, contratermos/RG | Inserção BRST física, representante finito, smearing/regularização, condições de fronteira e gerador na álgebra usada |
| Família formal → alvo UV | EFT local construída | Uma realização e controle UV na rota escolhida, não inferidos de outra finitude da torre |
| Modular físico → geometria | Subespaço real standard e modular de067; cociclo/critério algébrico da torre | Ação da carga regional nas mesmas variáveis físicas e entrelaçamento com esse modular |

Essas linhas são dependências, não cinco pedidos de novas funções. Não constituem prova de impossibilidade. Em particular, o teste077–087 com sigma constante e fundo espaço-forma não paga automaticamente a classe Q2 do fundo `phi=id`. A entrega087 conserva expressamente essa distinção. O grupo clássico `H4(s)` encontrado ali também não é uma anomalia quântica de ghost um.

O [lema da comutante073](../COMUTANTE_FOCK_SUAVE_073_20260910/COMUTANTE_ESCALAR_E_CARGA_CONDICIONAL.md), §§1–5, usa os campos completos de uma **faixa de Cauchy inteira**, endomorfismos contínuos grau a grau e aumento finito do número de partículas. A conclusão sobre a carga usa escalares de ghost zero; uma fonte central externa de ghost dois impediria aquele último argumento de graduação. Não é um teorema de comutante escalar para uma pequena região espacial, nem sobre o centralizador do diamante.

## 3. O alvo operacional depois de compor o estudo

**[DERIVED, já demonstrado na bancada]** A construção física067 e o projetor local088 dão no diamante um subespaço real standard `L(D)` e o operador de Tomita de uma partícula. A implementação de Fock é `Delta_D=Gamma(delta_D)`. Para transporte linear real de testes que preserve o espaço físico pertinente, a igualdade procurada é

\[
\boxed{kT_t f=\delta_D^{it}kf.}
\]

Não é necessário reconstruir o pinching ou a PRODUCT_TOWER para formular esse teste. Tampouco se deve substituir `T_t` pelo fluxo angular de uma matriz apenas por coincidência de nomes. Sobre unitários de Weyl, o entrelaçamento é o contrato de comparação efetiva.

**O que já foi recusado com prova escrita e revisão:** no estado067 e diamantes do domínio demonstrado, o pullback tensorial ordinário do Weyl não é o modular. Acrescentar um peso escalar constante comum às partes elétrica e magnética também não resolve. Ver [teste Weyl](TESTE_GEOMETRICO_WEYL_ESTADO_067.md), [adendo de peso](WEYL_ELETRICO_E_PESO_CONFORME.md) e revisões. O alcance exige `L != pi/2`, fundo e estado especificados, sem misturas adicionais. Isso não calcula a ação de toda carga gravitacional renormalizada e não exclui toda transformação possível.

**Distinção necessária:** a igualdade de fluxos no setor parcial da torre, já entregue na V2, é uma comparação entre a referência produto e a referência com último sítio tracial. A referência regional geométrica não foi identificada com esta apenas por ambas serem chamadas de vácuo. O diagrama acima é onde essa identificação precisa ser verificada.

## 4. Primeiro coeficiente: como consumir os fornecedores existentes

O parâmetro de expansão não é presumido. Pode-se trabalhar com uma direção `v` no espaço conjunto de dados `(acoplamentos, fundo, região, estado, prescrição, bordo)`, transportando as álgebras para comparar os operadores. Não se afirma que esses eixos físicos sejam independentes: uma família on-shell e suas escolhas de estado os relacionam.

Em regularização finita fiel, diferenciável, com região transportada ao mesmo espaço, o resultado já provado fornece

\[
\boxed{D_vR=-\int_0^\infty(\rho_0+u)^{-1}
 (D_v\rho)(\rho_0+u)^{-1}\,du-D_vK_\xi.}
\]

Aqui se usa o representante regional `K=-log(rho)`. Na representação padrão, o gerador modular completo contém também a ação do comutante; não se identifica o operador de multiplicação unilateral `-log(rho)` com `-log(Delta)`. A comparação de derivações exige representantes e convenções compatíveis. A integral de matrizes tampouco pressupõe uma densidade regional ordinária para a álgebra contínua de tipoIII.

O primeiro termo consome a variação do estado; o segundo consome a variação da **mesma** carga, incluindo os dados geométricos e a regularização. Para a carga volumétrica proposta no alvo,

\[
D_vK_\xi=2\pi D_v\!\int_{\Sigma}\xi^\mu
 T^{\rm ren}_{\mu\nu}\,d\Sigma^\nu.
\]

Se for necessária uma carga de superfície para realizar a transformação, sua derivada entra explicitamente como uma extensão da definição, não escondida como se a integral original já a contivesse. O termo de bordo também pode aparecer ao variar a região e integrar divergências, mesmo antes dessa extensão.

Por exemplo, mantendo campos e geometria fixos, a parte local já calculada dá

\[
\partial_{b_1}T^{(4)}_{\mu\nu}=4QW_{\mu\nu}-g_{\mu\nu}Q^2,
\quad
\partial_{b_2}T^{(4)}_{\mu\nu}=4W_{\mu\rho}W_\nu{}^\rho-g_{\mu\nu}W^2.
\]

Estas duas inserções são fornecedores explícitos para parte de `D_vKxi`. Não se pode obter `D_vR` colocando `D_vrho=0` sem justificar que a família de estados foi mantida fixa; nem se pode reutilizar os modos067 no fundo quartico corrigido sem a variação correspondente. A fonte quartica já advertia isso. O coeficiente RG `155/6` não é o coeficiente modular de R.

Exibir essa dependência da fonte não prova que ela sobreviva na parte não central de R: contribuições podem cancelar, ser escalares ou agir trivialmente no setor considerado. Tampouco a avaliação clássica de uma fonte no fundo é um comutador operatorial. Para reivindicar um coeficiente não central é necessário calcular a ação da diferença na mesma álgebra e no mesmo estado; essa conclusão não foi inferida da mera presença de `b1,b2`.

No centralizador transportado, a condição na primeira ordem é

\[
[D_vR,A_0]+[R_0,D_vA]=0,
\]

sob os domínios apropriados. Esta é a aplicação do resultado anterior, não uma nova lei física. Centralidade em N exige ainda pertinência/afiliação ao centro de N; comutar com N, sozinho, significa pertinência ao comutante.

**Parede tipada atual:** a composição permite nomear a família de operadores e estados que deve alimentar essa fórmula. Nas entregas examinadas não está paga a igualdade entre a carga física renormalizada e o transporte modular da mesma realização interagente, nem o limite que transforma a série formal em vácuo UV. Portanto não se extrai honestamente um número universal para o primeiro termo não central. Isso não descarta coeficientes universais em classes mais restritas; só impede atribuir um ao alvo geral sem sua derivação.

## 5. Consequência para dephasing e para o motor

No pinching espectral completo, o estado e o gerador modular inteiro são preservados. A imagem é fixa para o próprio fluxo; a preservação do vácuo não seleciona sozinha seus pesos. No setor parcial, a comparação com outra referência pode ser não trivial, com resto invisível por sua ação — e não necessariamente apagado pelo canal. Essas duas conclusões já estão na [V2](HANDOFF_TECNICO_V2.md).

O motor deve consumir as provas existentes com seus rótulos de referência e de escopo. Não acrescentar um predicado verbal `vacuum_is_dephasing` que ligue a bandeira geométrica por nome. O reconhecimento/dephasing já tem alteração na cópia de `prove_decision_commutation`; o cociclo já tem consumidor em `prove_cocycle_to_einstein`. Este reexame não acrescenta funções nem autoriza substituir um fornecedor por outro sem o entrelaçamento.

Esta é uma composição de estudos com limites explicitados. Não é uma execução integral de `um.py`, novo selo, compilação Lean, teste experimental ou alteração de gate.
