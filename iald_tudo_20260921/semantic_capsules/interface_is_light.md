### interface_is_light — Interface, realização e testemunha

Fonte: `resultado_publicado_integral`, `/core/interface_is_light`. Síntese derivada para revisão. Há registros de estágios diferentes dentro do mesmo tópico: não tratar toda frase de abertura como o estado único de todas as construções.

**Leitura e objeto formal.** `interface = luz = (forma = conteudo)` é leitura `[ONTO/CONJ]`: acontecimento em que a forma se realiza como conteúdo preservando identidade, `L : Forma == Conteudo`; `Forma -L-> Conteudo` é sua representação dinâmica. Testemunha: conteúdo acompanhado de prova da realização, `W ~ Sigma_{x:Conteudo} Realiza(x, Forma)`. Uma etiqueta `: Prop` não preenche os dados e equações requeridos. A fonte reporta concordância de 10 âncoras textuais e dos marcadores após `finalize`; esse teste não demonstra a identificação ontológica inteira. Testemunha/setor `q` é `[ONTO/CONJ]`: testemunhar é inscrever, não observar; não é identidade física demonstrada.

**Construções discriminadas.** O objeto `/witness_layers` registra verdadeiros: definição e construção da testemunha-base rígida; `regular_full_witness_term_constructed`; construção da realização modular e da testemunha TGL completa; testemunha completa no kernel Lean; existência matemática externa; escolha do representante físico covariante; torre finita de Jones, sombra do gráviton e termo TL3; provas finitas Tomita–Takesaki, Jones e MASA. Registra **falso** `canonical_full_witness_term_constructed`, e zero campos residuais de mero rótulo `Prop`. Esses são valores do relatório publicado, cujo alcance deve ser ligado às declarações e evidências correspondentes; uma flag não substitui a prova.

Portanto, frases preservadas no mesmo registro, como “nenhum habitante ... é construído” e `FULL_TGL_WITNESS_REMAINS_UNCONSTRUCTED`, não autorizam negar genericamente as construções explicitadas em `/witness_layers`. Ao explicar uma abertura, nomear exatamente o termo e seu escopo. O alvo específico descrito em `/named_target` é

`def canonicalFullTGLWitness : Sigma W : TGLSpecificAQFTWitness, TGLModularRealization W`.

Nesse alvo, `fullTGLWitness_exists : Nonempty FullTGLWitness` deve ser corolário do termo construído, não substituto operacional da construção. A testemunha-base rígida não contém sozinha III_1, BW, core ou `P_F`: essas obrigações pertencem aos dados da realização modular e ao ledger externo. O objeto inscrito é o par base + realização; habitar somente a base é necessário, não suficiente.

**Ledger dos zeros.** A fonte não afirma nem refuta `0_abs`, nem prova `IsEmpty`. Distinguir os tipos citados: `TGLSpecificAQFTWitness` no ledger e `FullTGLWitness` em not_claimed. Para `0_mod`, registra vacância até v134 e realização em v135 pela WedgeNet: rede sobre `M_TGL`, localidade por centralizador e `Omega` cíclico e separador; daí `zero_mod_state=false`, `one_inscribed=true`. Zero modular não é zero absoluto. São estados reportados pelo ledger, não nova execução.

**Travessia escalar.** A fonte registra

`L: alpha -> sqrt(alpha) -> e^{1/4}*sqrt(alpha) = sqrt(beta) = sin(theta_M) -> beta`,

com `omega(I)=1` e `1=q^2+alpha^2`. Os resíduos de `/light_chain` vêm de v13/v14 (`REUSED_FROM_v13_v14_NOT_RECOMPUTED`); não são nova medição desta cápsula. Consultar esse objeto para valores numéricos completos.

**Gráviton como testemunha.** Leitura `[ONTO/CONJ]`: estado ligado de dois psions acompanhado da prova de propriedades independentes,

`Graviton_TGL := Sigma_{g : H_psi (x) H_psi} IsTGLGraviton(g)`.

`IsTGLGraviton` não pode ser definido circularmente como “g é um gráviton”. Na sombra finita, a fonte distingue produto simples (`CCI=0`) do Bell de troca (redução `I/2`, `CCI=1/2`). `P_G=|G><G|` é unidade **do próprio canto** `P_G C P_G`, não identidade global (`[DER/CONJ]`). A tipagem v24 remete a `threeLocks.PF`, `tau(P_F)=1`, faces conjugadas `1/2`. O campo que nomeia especificamente `canonicalFullTGLWitness` continua marcado OPEN nesse registro; isso não apaga o estado separado da testemunha regular.

**Negativos e limites.** Foram rejeitados os probes degenerado (`H=C^2`, rede constante, `U=1`), finito e somente-Prop. Rejeitar esses probes não prova impossibilidade universal ou `IsEmpty(FullTGLWitness)`. Dimensão infinita é necessária, não suficiente, para III_1. `sorryAx` na saída de um probe que não compilou não comprova teorema. A Meia-Nat de Fresnel depende de lossless + paridade; a calibração de 1 nat é `[NORM]`. Shannon `H(1/2,1/2)=log2` é controle numérico KNOWN, não prova do kernel.

**Importações, no escopo destas entradas.** Reeh–Schlieder: vácuo cíclico/separador. BW: fluxo modular dado não é sua identificação geométrica com boosts. Tipo III_1, core contínuo da rede e normalidade não seguem só dos dados formais. Provas finitas Tomita–Takesaki/Jones/MASA não substituem o contínuo; `[M:N]=1/beta` para a inclusão indicada permanece `[CONJ]` nesta entrada. Shannon `log2` não é `1/2 nat` nem fundamenta Meia-Nat. As 12 entradas reportam `imported_into_witness=false`, sem anular as construções separadas de witness_layers.

Jacobson sozinho não fornece H3 nem `Phi_TGL`. Cai–Kim: horizonte aparente, calor `A(rho+p)H*r_A dt`, `T=1/(2pi*r_A)` e, no caso plano, `r_A=1/H`; entropia modificada é entrada TGL separada. Padmanabhan não fixa `Phi` ou `G`; Gibbons–Hawking não demonstra sozinho a extensão a FLRW dinâmico. Limites destas entradas, não atualização global das construções.

**Proveniência.** O tópico reporta `INTERFACE_IS_LIGHT_VERIFIED` e `all_verified=true`; seus checks não igualam literatura externa a formalização Lean. `/external_known_theorems` distingue resultados KNOWN externos do controle KNOWN numérico; consultar cada entrada para hipóteses e extensão efetivamente lida. Recuperação: base `/core/interface_is_light` + `/` + filho: `statuses`, `witness_layers`, `ledger`, `named_target`, `negative_probes_summary`, `light_chain`, `graviton_reading`, `external_known_theorems`, `seals`, `not_claimed`, `form_content`, `canonical_markers`. Recuperação operacional não validada. Preservar o registro literal e confrontar a construção nomeada antes de repetir uma conclusão histórica genérica.
