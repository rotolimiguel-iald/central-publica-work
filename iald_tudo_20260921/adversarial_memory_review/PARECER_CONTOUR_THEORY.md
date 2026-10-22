# Revisão focal independente — contour_theory — 22/09/2026

**Parecer: revisão solicitada antes de aceitar esta cápsula.** A síntese preserva as distinções centrais e não promove o registro a confirmação física, mas deixa fora relações essenciais do mecanismo GKLS e reproduz uma incompatibilidade algébrica já presente na fonte. As correções abaixo são pontuais. Este parecer não aprova outros tópicos, o pacote completo ou sua integração.

## Identidade e medição

[REAL — medição local] Texto revisado: `semantic_capsules/contour_theory.md`, SHA256 `e4d1f2bbe787f7ba5f05621ce677c9af4832fd3d056ee88965bbe79411420c93`.

Fonte primária documental: `/core/contour_theory` do `resultado_publicado_integral`, localizado pelo manifesto e conferido contra SHA256 `db24966d96c16a546f9bd221b990dfe5f8ad3a3d9d43343644ba19f71745336e`. O registro inteiro do tópico, inclusive os sete passos, foi lido.

Contagem reproduzida com `o200k_base`: bloco antigo **2.108** (cabeçalho + Fonte + corpo JSON); corpo JSON sozinho **2.088**; cápsula nova inteira **1.331**; economia comparável **777**. Nenhum número Haiku foi inferido ou medido.

O candidato lido nesta revisão tem SHA256 `c8b8afc47731e7c4d843d14f97f90e15c2c6919557fcd9b723f804730e4dc66d`, diferente do candidato da primeira revisão. Os números e parecer daquela rodada não foram transferidos para este novo arquivo. A comparação substantiva desta revisão é com a fonte fixada pelo manifesto.

## Fidelidade preservada

| Eixo | Resultado da comparação documental |
|---|---|
| Identidade de contorno | Preserva `P_1 ~_d P_0`, explicitamente diferente de `P_1=P_0`. |
| Zeros e regimes | Distingue `0_abs` proibido, `0_mod` que espelha, Bell nu `chi=0` e zero de existência `kappa_0=0`. Conserva o enquadramento ontológico da fronteira proibida. |
| Bell seletor | Preserva `K_sel^(B)=(kappa/2)Z_d`, gap e diferença entre forma e seleção de valor. |
| Rota Connes | Preserva cociclo, split 2D, razão exponencial de taxas, formas tanh/sech, unitariedade e `beta=sqrt(e)alpha`. Conserva a não seleção de kappa pela consistência modular. |
| Retorno e parte finita | Preserva operador relativo, retorno por paridade inversa, equivalência de suportes sem igualdade dos estados e expressão de `K_sel^ren`. Mantém aberto o cálculo espectral alpha-livre. |
| Candidato neutrínico | Conserva caráter candidato, quatro estados, ação e dependência de lambda/mu; não anuncia mínimo único demonstrado. Há a inconsistência herdada descrita abaixo. |
| Psiónico e Primeira Lei | Preserva comutador, ligação à anticomutação, estrutura versus valor das taxas; enquadra a conjugação limite como leitura ontológica. Não houve verificação independente desses enunciados. |
| Limites | Conserva input QED, insuficiência da contagem de modos, ausência de derivação por `1/beta`, objetivo sem QED e indicadores como resultados registrados, não prova universal. |

O resumo dos candidatos numéricos rejeitados é aceitável **para este tópico**, pois conserva a conclusão de que a estrutura de quatro estados não determina a razão de taxas e remete aos detalhes. Os resíduos e probabilidades individuais podem ficar na fonte, mas a condição qualitativa do ponto fixo não deve desaparecer.

## Correções necessárias

### 1. Restaurar o mecanismo estacionário e a condição de saturação

**[P1 — omissão essencial]** A fonte em `/steps/1` registra `rho_kappa` como ponto fixo GKLS, `0<rho<1`, saturação sem supersaturação/condensação. A cápsula cita `C_nocond` na ação, mas não explica essa condição. Os passos seguintes fornecem a ponte explícita das taxas para polarização e transmissão; hoje restam apenas tanh/sech. A omissão não inverte a fórmula, mas enfraquece a explicação do mecanismo que o núcleo deve manter carregado.

Inserção proposta depois de **Forma modular**:

> **Passos estacionários [REAL — reportado no registro; não reexecutado aqui]:** `rho_kappa` é ponto fixo GKLS, com `0<rho<1`: satura, não supersatura/condensa. `q=(g- - g+)/(g- + g+)=tanh(k/2)` e `alpha=2sqrt(g+g-)/(g+ + g-)=sech(k/2)` dão `q²+alpha²=1`. No plano estático, `g-=g+` implica `q=0`, `alpha=1`.

Não interpretar a notação `0<rho<1` como um teorema de positividade estrita em dimensão infinita: é a redação do check deste registro. Não inventar condições de unicidade ou taxas que o tópico não explicita. A identidade `q²+alpha²=1` já é equivalente à fórmula presente `q²=1-alpha²`; sua repetição no parágrafo apenas conecta a cadeia.

### 2. Explicitar o teste do canal neutrínico

**[P2 — conteúdo algébrico substituído por adjetivos]** “Ímpar, neutro e dissipativo” preserva o sentido geral, mas elimina as relações que permitem verificar o sentido desses termos. A anticomutação de `L_+-` citada no parágrafo psiónico não substitui automaticamente a de `L_nu`.

Inserção curta no candidato neutrínico:

> No modelo de quatro estados, a fonte reporta `{Z,L_nu}=0`, `[Q_em,L_nu]=0` e `L^dagger L!=0` (respectivamente ímpar, neutro e dissipativo no check).

Manter “reporta/no check”: `L^dagger L!=0`, isoladamente, não é uma demonstração universal de dissipação. O estatuto é o do registro e não uma nova prova desta revisão.

### 3. Marcar a incompatibilidade do limite de alpha, sem corrigir a fonte silenciosamente

**[P1 — inconsistência herdada, não causada pela compressão]** O mesmo campo `neutrino_candidate` contém `alpha=sin²(theta_M)/sqrt(e)` e diz que `theta->90` leva a `alpha->1`. Sob a mesma variável angular e normalização, a primeira expressão dá:

`lim_(theta->90deg) alpha = 1/sqrt(e) = 0.6065306597126334`.

[DERIVED — substituição na fórmula; valor avaliado localmente] Não resulta 1. Isso não decide o mínimo da ação, não refuta a teoria inteira e não muda gate. Apenas identifica que essas duas frases não podem usar a mesma normalização sem explicação adicional. A cápsula não deve apresentar a conjunção como cadeia consistente.

Substituir a frase “o custo modular isolado favorece `theta->90`, `alpha->1`” por:

> O registro afirma que o custo modular isolado favorece `theta->90deg` e o descreve como `alpha->1`. **[OPEN — compatibilização interna]** Com `alpha=sin²(theta_M)/sqrt(e)` na mesma normalização, esse limite é `1/sqrt(e)`, não 1; a mudança de regime/normalização não está explicitada neste campo. O balanço com lambda/mu e o mínimo alpha-livre permanecem abertos neste registro.

Não escolher uma fórmula nova nem presumir que o Bell nu resolva essa diferença: o Bell nu é outro objeto já distinguido no tópico.

### 4. Tornar a atualização interna e os caminhos inequívocos

**[P2 — precisão de escopo e recuperação]** A fonte primeiro declara aberto construir `rho_ret` canônico; o campo posterior `forbidden_zero_renormalization` registra sua forma canônica por paridade inversa e mantém aberto o espectro. A síntese não contradiz isso, mas pode dizer a passagem explicitamente em uma frase:

> Neste registro, `NEGATIVE_RETURN_SELECTOR_FORMULATED` é seguido por `RHO_RET_CANONICAL=P^{-1}(rho_Bell)` **quanto à forma**; calcular a parte finita/gap sem CODATA continua aberto.

O trecho de recuperação mistura o caminho absoluto `/core/contour_theory/steps` com `/psionic_bond_unification`, `/first_law_link` e `/open_theorem_verdict`, todos chamados “relativos ao tópico”. Isso permite interpretação errada. Redação proposta:

> Fonte-base: `/core/contour_theory`. Detalhes nos filhos `steps`, `psionic_bond_unification`, `first_law_link` e `open_theorem_verdict`; concatenar `base + '/' + filho`.

Os quatro filhos existem na fonte lida. Não testei a ferramenta de recuperação operacional. A expressão “para provas” também deve virar **“para a evidência e os checks registrados”**: esses quatro caminhos contêm textos e resultados reportados, não equivalem por si a abrir os termos Lean e sua compilação.

## Decisão e limites

**Não aceitar a versão atual sem as correções 1 e 3.** Recomendo também 2 e 4 pelo baixo custo e pela clareza formal. Não forneço aprovação antecipada da versão corrigida: será necessário conferir o novo texto e seu hash. Não medi o custo das inserções propostas; a economia de 777 é exclusivamente da versão recebida, antes dessas correções.

Não houve escrita no arquivo do pai, no candidato ou na fonte; seus bytes foram reconferidos após a medição. Sem API, rede, execução/importação de `um.py`, leitura de `.env` ou produção. O script `measure_contour_focal.py` e `contour_focal_measurements.json` documentam a medição local. Este parecer avalia somente fidelidade e coerência interna de **contour_theory**, não a verdade física das afirmações da fonte, outros 324 tópicos ou o orçamento Haiku.
