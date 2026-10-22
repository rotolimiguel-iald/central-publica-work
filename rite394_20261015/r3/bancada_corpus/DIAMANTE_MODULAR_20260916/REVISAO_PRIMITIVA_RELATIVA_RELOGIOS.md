# Revisão independente — primitiva relativa nos relógios físicos

16/09/2026. [DERIVED — parecer matemático escrito, não Lean]. Revisor Singer, agente `01a0ac43-294f-7d21-9237-38c5de79dbb7`, separado do autor. Dois pareceres recebidos por ferramenta; não editou arquivos nem executou scripts.

## Leituras e resultado

O revisor declarou leitura integral de `write_bv_clock088_new.py`, da extensão BRST068 e do dicionário BV069. Consultou pontualmente Atlas/índice e BBH §2.7. Na segunda rodada leu integralmente `PRIMITIVA_RELATIVA_RELOGIOS.md`.

Primeiro veredito:

> “Aprovo a homotopia e a extensão formal no domínio localizado declarado. Aprovo também o argumento relativo sem descida completa.”

Conferiu a manutenção dos antifields antigos não fixados como coordenadas independentes; a mudança precisa ser invertível na álgebra diferencial de jatos, sem recolocar um antibracket canônico fictício. A restrição τ(H)=0 dá nove componentes. A identidade Hscr K=0 torna as transformações residuais independentes de ζ,C e permite a contração também na presença de antifields.

Conferiu a filtração, exigindo contar campos, ghosts, auxiliares e antifields com valência um; derivadas conservam a valência. Fundo on-shell, s₀/d_H/h₀ preservadores da valência e s_+ estritamente crescente sustentam a indução. Não autorizou substituir {s₀,h₀} pela mesma identidade com s completo.

Conferiu os sinais: para R=a−sB−d_HC e b_R=b−sC, vale sR+d_Hb_R=0. Se R_{<E}=0, então R_E=s₀h₀R_E+d_Hh₀(b_R)_E. Ambos os incrementos têm sinal positivo. Não se exige (b_R)_{<E}=0. A primitiva formal existe coeficiente a coeficiente, sem convergência numérica nem ordem diferencial uniforme demonstradas.

## Leitura final

Segundo veredito:

> “[DERIVED — APROVADO] Li integralmente o documento. A redação incorpora corretamente as ressalvas do parecer e mantém seu escopo.”

Confirmou a extensão da fórmula a todo g>0 e 0≤p≤4; recomendou explicitar que para p=0 as formas de grau negativo são zero, b=C=0. Essa precisão editorial foi incorporada antes da emissão.

## Limites da aprovação

O parecer usa o fundo on-shell e as identidades diferenciais fornecidas pela068; não é nova auditoria da ação066 nem dos selos. Exige a mesma completação localizada, coeficientes estáveis sob derivação horizontal, ausência de fontes residuais de ghost positivo e relógios não degenerados.

Não aprova extensão à categoria universal, família admissível de contratermos, QME, carga quântica, estado interagente/UV ou identificação modular-geométrica. Não certifica as referências históricas, manifestos ou compilações mencionados na nota: estes recebem conferência documental separada no manifesto desta rodada.
