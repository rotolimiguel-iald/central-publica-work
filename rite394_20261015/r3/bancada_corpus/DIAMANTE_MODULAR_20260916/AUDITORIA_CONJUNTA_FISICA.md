# Composição física das entregas — ação, estado e carga

[DERIVED — síntese de provas escritas existentes] [REAL — leitura documental nesta rodada; não recompilação]. Autor: bancada principal. Escopo do inventário: os 47 arquivos do grupo `PHYSICAL_QUANTUM_AND_RECENT` em `JOINT_DEFINITION_INVENTORY.json`, lidos integralmente por lotes 0–10, 10–20, 20–32 e 32–47. O registro por arquivo e os pins estão em `AUDITORIA_CONJUNTA_FISICA.json`. Este documento não afirma leitura integral de todas as fontes ligadas recursivamente às entregas.

## 1. A definição conjunta que já existe

A cadeia não começa com uma ação ou um estado ausentes. Ela começa com a ação Einstein–sigma adotada em 065–067, seu representante probabilístico suficiente, o estado físico 067, o sistema auxiliar BRST 068 e a renormalização causal 069. As entregas posteriores acrescentam contratermos/RG, cohomologia, representação e uma recorrência condicional de estados. Não se deve substituir essa cadeia por um pedido ao operador para fornecer um único arquivo.

| Peça | Fonte e seção que a fornece | Estatuto e domínio |
|---|---|---|
| Ação física e estado de fundo | `REEXAME_SUFICIENCIA_067_20260909/REEXAME_SUFICIENCIA.md`, §§2–4; convenção de sinal ligada ali | Adoção da ação: INPUT/POSTULATE. Equivalência variacional local: DERIVED; Nash: KNOWN. Fundo Einstein–sigma em faixa interior de `(0,pi) × S3`, `phi=id`, `kappa*c=4`, `Lambda=3/4` |
| Transporte da dinâmica e do bordo entre probabilidades e campos | `ADENDO_LINEARIZADO_COARSE_LIVRE_20260909_214421_410751/ADENDO_LINEARIZADO_E_SIMPLÉTICO.md`, §§2–7 | DERIVED: `AR=Id`, `B=A*HA`, equivalência simplética nas soluções. Potenciais casados e fluxo pela fronteira são parte do contrato |
| Campo livre físico e estado | 067 §4 e suas fontes S/V/TT/Hadamard | DERIVED+KNOWN: estado quase livre positivo, CCR física e Hadamard no fundo e quociente construídos. Não apenas uma pseudocovariância |
| Produtos renormalizados e interações | `CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md`, §§1–7; dicionário BV da mesma pasta | DERIVED+KNOWN: família de produtos temporais locais/covariantes, álgebra auxiliar interagente e quebra local consistente; série formal EFT com contratermos admitidos |
| Fonte quartica explícita | `RENORMALIZACAO_SIGMA_EFT_20260909/FONTE_QUARTICA_E_HABITANTE_CORRIGIDO.md`, §§1–4 | DERIVED, para os coeficientes lorentzianos finitos `b1,b2` adotados. Não é todo o tensor quântico renormalizado |
| Contratermos e fluxo RG | `REDUCAO_ON_SHELL_RG_070_20260909_232623_681687/REDUCAO_EFT_E_FLUXO_LOGARITMICO.md`, §§1–7; calor completo 069 como entrada | DERIVED: redução on-shell de uma volta, convenção bare/renormalizado e fluxo logarítmico. Mantém termos de divergência e redefinições; não fixa valores finitos nem uma beta de kappa única |
| Estado interagente formal | `POSITIVIDADE_BRST_FORMAL_072_20260910/ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md`, §§2,5–7 | DERIVED+KNOWN condicional a P0–P2: levantamento recursivo e estado positivo formal na álgebra física admitida |
| Realização de P0 e parte de P1 | `FOCK_HADAMARD_QUARTETOS_073_20260910/FOCK_DOMINIO_WICK_E_P0.md`, §§1–7, consumindo sua polarização adaptada | DERIVED: mesma covariância física067; domínio nuclear suave, quartetos e coeficientes Wick compactos. P0 não continua genericamente aberto após073 |
| P2/carga | 072 §4; `COMUTANTE_FOCK_SUAVE_073_20260910/COMUTANTE_ESCALAR_E_CARGA_CONDICIONAL.md` | DERIVED condicional: implementação de derivação nilpotente e comutante escalar na faixa de Cauchy implicam carga nilpotente. O lema não constrói a identidade renormalizada de entrada |
| Cohomologia e admissibilidade | entregas071–087, especialmente `REEXAME_SUFICIENCIA_087_20260910/REEXAME_SUFICIENCIA.md`, §“A obrigação de anomalias ficou mais precisa” | Resultados DERIVED com categorias diferentes. O teste espaço-forma com sigma constante de077–087 não é automaticamente o fundo físico `phi=id` de Q2 |
| Modularidade regional física | `ESTADO_EINSTEIN_SIGMA_E_MODULAR_LOCAL.md`, nesta pasta, usando067 e projetor local088 | DERIVED, revisão independente registrada: subespaço real standard e segunda quantização modular no mesmo modelo linear. Não é a wedgeNet escalar nem um novo estado escolhido por nome |

As contagens de Lean/CAS citadas nas entregas são históricas. Esta rodada verifica o encadeamento documental; não as promove a novas execuções.

## 2. Ação e tensão: o conteúdo preciso

Na convenção física da bancada,

\[
S_0=-\frac1{2\kappa}\int(R-2\Lambda)d\mu_g
 +\frac c2\int Q\,d\mu_g,
\quad Q=g^{\mu\nu}W_{\mu\nu},\quad
W_{\mu\nu}=\langle\partial_\mu\phi,\partial_\nu\phi\rangle_{S^3}.
\]

O representante local quartico de068–070 acrescenta
`int(b1 Q²+b2 W²) dmu`. Os produtos temporais069 constituem uma família de prescrições renormalizadas, com liberdade de termos locais, e não um único funcional numérico determinado só por normalização de probabilidades. A tabela070 fixa os coeficientes dos logaritmos na prescrição indicada. Com `s=kappa*c`,

\[
A_1=-13s^2/16+7s/6+1/6,\quad
A_2=27s^2/8-s+1/3.
\]

Em `s=4`, `3A1+A2=155/6` e, na conversão lorentziana local declarada,
`mu d(3b1+b2)/dmu=-155 hbar/[3(4pi)²]` a uma volta. Os valores em uma escala de referência continuam parâmetros finitos da família construída. A dedução não estabelece escala temporal `mu=a^-1`, convergência dos laços ou rota UV.

A variação efetivamente feita fornece

\[
T^{(2)}_{\mu\nu}=c(W_{\mu\nu}-g_{\mu\nu}Q/2),\qquad
T^{(4)}_{\mu\nu}=4b_1QW_{\mu\nu}
 +4b_2W_{\mu\rho}W_\nu{}^\rho-g_{\mu\nu}(b_1Q^2+b_2W^2).
\]

No fundo isotrópico, a parcela quartica tem `rho4=-3(3b1+b2)/a^4` e `p4=rho4/3`. A presença de uma expressão explícita para essa parcela é reconhecida. Ainda precisam ser distinguidos: inserção operatorial renormalizada, sua expectativa no estado, derivada de ação efetiva, fonte clássica de ação truncada e carga Hamiltoniana regional da teoria com métrica dinâmica. Elas não são sinônimos.

O transporte variacional067 mantém o termo `J^mu=E_alpha b^{alpha mu}_i p^i` do mapa diferencial dos pesos. Mudanças `theta -> theta+dY` alteram a forma integrada por termo em `partial Sigma`. A redução070 também retém uma corrente de divergência. Portanto nem o transporte ao registro nem a redução on-shell permitem apagar o bordo de um diamante finito.

## 3. Os estados existentes não devem ser confundidos

1. **Torre com potencial local somável, 061:** estado fiel normal de Araki, com cociclo normalizado, modularidade e KMS demonstrados por aplicação de resultado analítico. Não é uma falta de existência. Exige soma global de normas finita.
2. **Interação extensiva, 063:** dinâmica quase local e estados/limites KMS nos contratos construídos. A extensão normal ao fator original não é automática; a própria entrega conserva um contraexemplo. Não se conclui identificação com a rede relativística apenas por ambas terem estados KMS.
3. **Modelo físico067:** estado quase livre positivo e localmente Hadamard, usado na construção regional de16/09. Existe no fundo e na teoria linear especificados.
4. **Deformação física072+073:** o estado067 é o termo inicial de uma recorrência formal. P0 e a parte Wick de P1 estão realizados por073; a carga interagente e suas identidades de P2 são entradas restantes. A positividade formal não é um estado numérico já completado em norma, nem um vácuo UV selecionado.

A distinção é de objetos e domínios, não de mera terminologia. Nenhuma dessas construções deve ser repetida sob outro nome.

## 4. Localização exata da costura BRST

A quebra produzida por069 satisfaz `s a_N+d b_N=0`. É preciso uma primitiva `a_N=s B_N+d D_N` **na classe admitida pelos produtos**, com realidade, naturalidade, escala, contatos e dependência dos fundos compatíveis, seguida da implementação da renormalização finita. O resultado071 numa classe suave maior não paga automaticamente esse transporte. As análises074–087 refinam o problema; não demonstram a sua impossibilidade e não são autorização para apagar a anomalia concreta.

073 fornece `R0=N_aux^-1 h` no domínio comum. Assim, quando a carga renormalizada for fornecida, `psi_n=-R0 sum_{j=1}^n Q_j psi_{n-j}` já é uma construção utilizável. Não se pede novamente uma prova abstrata de positividade livre. A pendência é implementar a carga e verificar suas identidades nos mesmos coeficientes renormalizados.

## 5. Retorno ao diamante e a R

No modelo linear existente, a comparação operacional continua sendo

\[
kT_t f=\delta_D^{it}kf.
\]

O lado direito já tem construção regional; não foi diagonalizado por completo. O lado esquerdo precisa ser o transporte implementado pela **carga física escolhida**, na mesma álgebra, e não um pullback introduzido por analogia. As provas anteriores excluem o pullback tensorial ordinário do Weyl e sua correção por peso escalar constante comum, no fundo067 e diamantes indicados (`L != pi/2`, sem misturas). Isso não exclui toda ação derivada da carga completa.

Sobre o centralizador, a identidade já provada `[R,A]=-[Kxi,A]` não recebe um novo coeficiente apenas por juntar entregas. Em regularização finita fiel e família diferenciável casada, o fornecedor existente é `R1=-Dlog(rho0)[rho1]-Q1`, acompanhado do transporte de A se o centralizador muda. Para calcular um coeficiente físico, a família deve fazer coincidir a variação do estado, da inserção renormalizada, do fundo/região e dos termos de bordo. O estudo já fornece partes concretas dessa família; não fornece nas entregas lidas uma identidade que torne essas partes automaticamente a mesma carga modular.

Isto é uma **costura tipada ainda não demonstrada**, não prova de inexistência da ponte. Também não é evidência empírica nem mudança de gate. A principal correção de memória é reconhecer, simultaneamente, a ação, a renormalização causal, os quatro estatutos de estado e os termos de tensão/bordo já construídos.
