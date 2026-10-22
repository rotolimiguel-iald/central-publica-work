# Derivação prévia — codec angular de campos tensoriais gerais

[INPUT] A tarefa é construir uma representação de campos reais por probabilidades interiores, com recuperação pela função selectionAngle já existente. A construção é informacional: NÃO demonstra uma lei física que produza essas probabilidades a partir de observações.

[DERIVED — a verificar em Lean] Para x real, θ(x)=(arctan x+π/2)/2 está em (0,π/2). Defina p(x)=sin²θ(x), em (0,1), e d(p)=tan(2 selectionAngle(p)−π/2). O ramo principal do arco-seno recupera θ(x), logo d(p(x))=x. Reciprocamente, p(d(q))=q para 0<q<1.

A extensão às matrizes é componente a componente, sem escolher uma família geométrica: cada entrada real pode ser codificada. Para um campo tensorial em uma carta de quatro coordenadas, a mesma operação é aplicada em cada ponto e par de índices. Suavidade da codificação é global; suavidade da decodificação requer probabilidades estritamente interiores em cada ponto. Não é exigida separação uniforme dos extremos para suavidade local, mas não se afirma estabilidade numérica uniforme.

O registro armazena somente um campo de probabilidades, sua interioridade e sua suavidade. A assinatura lorentziana é um certificado explícito sobre o campo decodificado, não uma métrica guardada como segundo campo. Simetria e assinatura não são derivadas de probabilidades arbitrárias. A construção de um registro a partir de uma métrica já conhecida prova capacidade da linguagem e a ida e volta; não prova que a natureza entrega esse registro.

[OPEN] Origem física do registro completo; ligação das probabilidades do codec a observáveis selecionados reais; consistência entre cartas e reconstrução global; lei dinâmica, matéria e conservação. Este módulo não altera o estatuto desses pontos, nem o gate.

Plano de verificação: compilação nova apenas deste módulo e de um importador, auditoria de todas as declarações, hashes da fonte e da fronteira direta de dependências antes/depois. Dependências canônicas permanecem somente leitura e não serão recompiladas.
