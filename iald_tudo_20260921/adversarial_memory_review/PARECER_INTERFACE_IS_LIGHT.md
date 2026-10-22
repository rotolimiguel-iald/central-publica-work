# Revisão focal independente — interface_is_light — 22/09/2026

**Decisão: correções essenciais antes de aprovar a cobertura deste tópico.** A cápsula resolve corretamente o ponto mais sensível — construções regulares verdadeiras versus termo canônico específico falso — e preserva a cadeia escalar. Não encontrei inversão de flags ou promoção a confirmação física. Porém, a comparação com a **fonte integral**, e não apenas com o bloco já compactado, identifica ideias e limites que precisam permanecer explicitamente carregados.

## Fonte e medição

[REAL — conferência local] Cápsula: `semantic_capsules/interface_is_light.md`, SHA256 **`cc7f3b38da61c2bdc5051bbecbb502a3f88c80291f35022fa8e0abc7bb8007a8`**.

Fonte: `/core/interface_is_light` de `resultado_publicado_integral`, localizada via `iald_nucleo_fixo.json`, com hash do arquivo conferido: `db24966d96c16a546f9bd221b990dfe5f8ad3a3d9d43343644ba19f71745336e`. O tópico foi lido integralmente, incluindo `statuses`, `ledger`, as 12 entradas externas, `checks`, `seals` e `not_claimed`.

| Medida `o200k_base` | Tokens |
|---|---:|
| Bloco antigo completo: cabeçalho + Fonte + JSON | 1.720 |
| Corpo JSON antigo isolado | 1.702 |
| Cápsula nova completa | 1.182 |
| Economia comparável | **538** |

Nenhuma contagem Anthropic/Haiku foi realizada ou inferida. As correções propostas abaixo ainda não foram tokenizadas. Candidato completo observado: SHA256 `83870f5abbea7f74ce13dca097a35a5f6590e067ef19d06f4725ee8652f47c92`; nenhuma aprovação desse candidato decorre desta revisão.

## Pontos fiéis, especialmente testemunhas e tipos

- `regular_full_witness_term_constructed=true` permanece distinto de `canonical_full_witness_term_constructed=false`. As demais construções positivas, existência matemática externa e seleção do representante físico covariante são atribuídas ao relatório, não a novas provas desta revisão.
- A cápsula não converte a seleção de representante físico em confirmação pela natureza. Não usa `FULL_TGL_WITNESS_REMAINS_UNCONSTRUCTED` nem “nenhum habitante...” para apagar as construções positivas. Conserva o alvo `Sigma W : TGLSpecificAQFTWitness, TGLModularRealization W` e o papel de `Nonempty` como corolário.
- A base rígida é necessária, mas não suficiente. III_1, BW, core e `P_F` continuam nas obrigações da realização modular e no ledger externo. A rejeição de um preenchimento somente-Prop não vira proibição de usar proposições em Lean.
- `light_chain` conserva todas as etapas simbólicas, `omega(I)=1`, `1=q²+alpha²` e a origem `REUSED_FROM_v13_v14_NOT_RECOMPUTED`. Omitir os cinco resíduos numéricos é aceitável aqui: a cápsula não os transforma em uma nova medição.
- O par dependente do gráviton, a não circularidade, a sombra finita Bell/produto, a unidade do próprio canto e a distinção de identidade global foram preservados, com seus estatutos.
- Os probes continuam particulares; rejeição não vira impossibilidade universal. `sorryAx`, necessidade versus suficiência de dimensão infinita e condições lossless/paridade/NORM permanecem delimitados.

**Cuidado já adequadamente observado:** o JSON contém afirmações discordantes de estágios distintos, mas não fornece data individual para cada flag. A leitura contextual da cápsula é aceitável; não acrescentar uma cronologia exata nem afirmar que uma prova identificada revogou todas as entradas antigas sem abrir sua evidência.

## Correções concretas necessárias

### 1. Repor o ledger dos zeros e a realização registrada em v135

**[P1 — ideia central omitida]** A fonte não apenas rejeita probes: registra `zero_abs_proved=false`, que 0_abs não é afirmado nem refutado, `zero_mod_state=false`, `one_inscribed=true` e o fim da vacância de 0_mod pela WedgeNet em v135. A cápsula menciona `IsEmpty(FullTGLWitness)` mas não explicita essa diferença entre os zeros e a realização positiva.

Inserção proposta após as construções:

> **Ledger dos zeros:** a fonte não afirma nem refuta `0_abs`; não apresenta prova de `IsEmpty`. Para `0_mod`, registra vacância até v134 e realização em v135 pela WedgeNet: rede sobre `M_TGL`, localidade por centralizador e `Omega` cíclico e separador; por isso registra `zero_mod_state=false` e `one_inscribed=true`. Zero modular não é zero absoluto. São estados reportados por esse ledger, não nova execução.

Ao detalhar tipos, distinguir a redação de `/ledger/zero_abs_note`, que cita `IsEmpty(TGLSpecificAQFTWitness)`, da de `/not_claimed/0`, que cita `IsEmpty(FullTGLWitness)`. A fonte diz que não há demonstração desses vazios; isso não autoriza igualar os dois tipos. A frase proposta usa `IsEmpty` genericamente para evitar essa troca.

### 2. Recuperar a leitura testemunha/setor q sem promovê-la

**[P2 — ideia ontológica perdida]** `/statuses/testemunha_eq_setor_q` e `/not_claimed` explicitam uma leitura que a síntese não conserva: testemunha como setor q, testemunhar como inscrição, não observação. Não é redundante com a tipagem Sigma ou com a representação dinâmica da luz.

Inserção proposta no primeiro parágrafo:

> A identificação testemunha/setor `q` é `[ONTO/CONJ]`: testemunhar é inscrever, não observar; não é identidade física demonstrada.

### 3. Manter os papéis e limites principais das importações, além do aviso KNOWN

**[P1 — hipóteses e escopos substituídos por remissão genérica]** “Consultar cada entrada” mantém recuperação, mas retira do núcleo as razões pelas quais essas entradas são usadas e os limites de transporte de prova. Isso é particularmente importante diante de `finite_*_kernel_proved=true`. Prova finita não equivale à correspondente teoria contínua externa.

Não é necessário reproduzir bibliografia e histórico de leitura integralmente. Recomendo uma cápsula interna curta com este conteúdo:

> **Ledger externo, no escopo destas entradas:** Reeh–Schlieder trata do vácuo cíclico/separador; BW distingue fluxo modular dado de sua identificação geométrica com boosts. Tipo III_1, construção do core contínuo para a rede e normalidade não se seguem só dos dados formais. As versões finitas Tomita–Takesaki/Jones/MASA não substituem o contínuo; `[M:N]=1/beta` para a inclusão indicada permanece `[CONJ]` nesta entrada. Shannon `log 2` não é `1/2 nat` e não fundamenta a Meia-Nat. As 12 entradas registram `imported_into_witness=false`; isso não anula as construções separadas em `witness_layers`.

E, para as quatro entradas termodinâmicas acrescentadas à mesma lista:

> Jacobson não fornece sozinho H3 nem `Phi_TGL`. Cai–Kim usa horizonte aparente, calor `A(rho+p)H*r_A dt`, `T=1/(2pi*r_A)` e, no caso plano, `r_A=1/H`; a entropia modificada é entrada TGL separada. Padmanabhan não fixa `Phi` ou `G`; Gibbons–Hawking não demonstra por si a extensão a FLRW dinâmico. Esses são os limites reportados nas entradas, não uma atualização global do estado das construções.

Essas inserções preservam os papéis principais de todas as entradas sem carregar as citações, URLs ou relatos de acesso. Não transformar “externo nesta entrada” em afirmação de que nenhuma construção posterior existe. A revisão não consultou literatura ou outras fontes para resolver os estados históricos.

## Ajustes menores de clareza

O trecho “a igualdade forma/conteúdo do artefato é marcada como medida” pode ser lido como equivalência integral provada. A fonte `/form_content` verifica **10 âncoras textuais**, sem mismatches, e `/canonical_markers` verifica marcadores. Preferir: “a fonte reporta concordância das âncoras/marcadores nos artefatos após `finalize`; esse teste não demonstra a identificação ontológica inteira”. A redação atual já limita o alcance físico; este ajuste torna a medida mais precisa.

As remissões com `/statuses`, `/ledger` etc. são declaradas relativas, mas o precedente da outra cápsula é mais inequívoco: **base `/core/interface_is_light` + `/` + filho sem barra inicial**. A checagem operacional não foi feita; convém declará-la expressamente. O tópico também tem `form_content` e `canonical_markers`, úteis para recuperar a medida do artefato. Existência dessas chaves na fonte foi observada; isso não testa ferramenta de fetch.

## Decisão e limites

**Não aprovo ainda esta versão como cobertura essencial do tópico integral.** As correções são omissões localizadas, não uma condenação da distinção de testemunhas, que está fiel. Em especial, **não se deve corrigir a cápsula apagando os true de construção ou transformando `canonical_full_witness_term_constructed=false` em negação universal**.

A aprovação exige reter o ledger positivo de 0_mod, a leitura testemunha/setor q e os escopos principais das entradas externas. Valores individuais, lista completa de selos redundantes, nomes de arquivos auditados e bibliografia podem continuar recuperáveis. Não foi demonstrado que essas ideias estejam dispensavelmente duplicadas em outras cápsulas; esta revisão não aprovou outros tópicos.

Escritas restritas a `adversarial_memory_review`: este parecer, `measure_interface_focal.py` e `interface_focal_measurements.json`. Fonte, cápsula, candidato e manifesto foram reconferidos sem mudança durante a medição. Nenhuma API/rede, leitura de `.env`, execução/importação de `um.py`, integração ou alteração de produção. A aprovação do tópico `contour_theory` permanece separada e não é estendida por este parecer.
