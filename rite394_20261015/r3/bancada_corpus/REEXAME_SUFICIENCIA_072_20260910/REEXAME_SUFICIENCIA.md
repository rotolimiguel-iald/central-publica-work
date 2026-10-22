# Continuidade da suficiência — entrega 072

10/09/2026. [DERIVED — provas escritas] [KNOWN — importações com hipóteses] [REAL — leitura dos artefatos]. Arquivos novos somente em Chatgpt; originais, Atlas e memórias canônicas preservados.

**Avanço:** a comparação com a teoria causal ganhou construções explícitas. Uma família de anomalias admite uma primitiva que respeita a covariância de fundo e a regularidade exigida. O complexo clássico de fundos possui uma retração natural para os campos completos. A comparação dos produtos ganhou um transporte de primeira ordem e uma realização de Ward com anomalia em referência fixa. Para o setor físico, a passagem de vetores livres a vetores interagentes positivos agora tem uma recorrência operacional, sob os contratos representacionais declarados.

O alcance dos resultados é delimitado nas fontes. A anomalia geral de Q2, sua remoção em todas as ordens, a representação auxiliar compatível e o controle UV continuam abertos. Nenhuma dessas obrigações foi substituída por uma contagem de verificações.

## 1. Estado do programa vivo

A [captura 072](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_072_20260910/ESTADO_CANONICO_072.json>) leu os quatro artefatos canônicos e encontrou os mesmos bytes da entrega 071. O programa v338 conserva 683 arquivos embutidos; 77 dos 98 módulos comparados estão presentes e 21 continuam pendentes de integração. O selo confere com o programa.

Esta entrega não executou/importou um.py, não compilou Lean e não realizou CAS, cálculos de diagramas ou testes de natureza. As novas demonstrações são escritas e receberam as revisões internas indicadas. Os falsificadores, H3 interno e o registro de fase e ramo existentes continuam reconhecidos.

## 2. Uma primitiva admissível foi construída explicitamente

Na [prova de logvolume](<C:/IALD/Central de Patentes/Chatgpt/PRIMITIVA_COVARIANTE_LOGVOLUME_072_20260910_003839_535005/PRIMITIVA_LOGVOLUME_E_CONTRATO_Q2.md>), defina

\[
b=\log\frac{\mu_g}{\mu_{\bar g}}.
\]

Para uma densidade real L natural dos campos completos, com sL=Lie_C L, temos a identidade off-shell

\[
(\bar\nabla_\mu C^\mu)L
=s(bL)-d_H\iota_C(bL).
\]

O ponto decisivo é sb−C·db=div_barg C: a referência é transportada na covariância da família, mas permanece inerte sob o BRST quântico. A razão dos volumes é um escalar real e local; sua expansão perto de g=bar g tem coeficientes analíticos e finitos por ordem. O fator b tem ordem diferencial zero e escala geométrica zero.

A mesma construção vale para f(b)(div_barg C)L com primitiva F(b)L, F'=f. Inclui densidades cosmológica, de curvatura, sigma e EFT que satisfaçam a hipótese de transformação. Não afirma que toda quebra de Q2 pertença a essa família. A integração na hierarquia completa de mudanças dos produtos T_n, com fontes e contatos, continua sujeita às identidades de renormalização.

A [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_072_20260910_004104_732492/PARECER_PRIMITIVA_LOGVOLUME.md>) conferiu sinais, domínio e classe. A [precisão aditiva](<C:/IALD/Central de Patentes/Chatgpt/PRIMITIVA_COVARIANTE_LOGVOLUME_072_20260910_003839_535005/PRECISAO_REMISSAO_E_ALCANCE.md>) corrige uma remissão e mantém o alcance.

## 3. A retração dos fundos possui uma fórmula de transporte

A [construção clássica](<C:/IALD/Central de Patentes/Chatgpt/RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md>) acrescenta fundos B e parceiros Omega, com D=s+d_B. Os pares relativos são u=B−fields e v=Omega−s(fields). Na matéria, a diferença é substituída por Log_phi(B_phi), com seu diferencial completo. A mudança de base do vetor inclui o termo (sJ)u; ele não é descartado.

A seção correta envia B para os campos completos e Omega para seus valores BRST. A homotopia K satisfaz

\[
DK+KD=1-ip.
\]

Se Da+d_Hb=0 e a projeção pa=sB+d_HC possui uma primitiva na classe desejada, a fórmula

\[
a=D(iB+Ka)+d_H(iC+Kb)
\]

constrói a primitiva estendida. A retração é natural na vizinhança da diagonal de S³ e finita coeficiente a coeficiente. Não avalia a métrica em zero, não exige uma carta global do alvo e não transforma uma primitiva apenas suave em analítica.

A [precisão sobre fontes conjugadas](<C:/IALD/Central de Patentes/Chatgpt/RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/PRECISAO_FONTES_CONJUGADAS_E_REFERENCIA.md>) restringe a conjugação de gauge à subálgebra sem antifields externos B*,Omega*. A [revisão independente interna](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_RETRACAO_FUNDOS_072_20260910_004627_020318/PARECER_RETRACAO_FUNDOS.md>) conferiu a composição.

## 4. Variação dos propagadores e Ward em referência fixa

O [contrato Q2](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md>) torna explícitos campos, fundos, regularidade, escala e contatos. T1–T11 não incluem automaticamente a identidade de variação da cisão entre fundo e perturbação.

A [prova de transporte](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md>) calcula o defeito de Leibniz da derivada do fundo: ela diferencia o kernel no produto. Já nos campos lineares, a parte antissimétrica muda com o propagador causal E. Uma contração simétrica isolada não corrige essa variação.

Para uma família autoadjunta e hiperbólica, a identidade resolvente dá

\[
\dot E=-E^{ret}\dot P E^{ret}+E^{adv}\dot P E^{adv}
      =-E^{ret}\dot P E-E\dot P E^{adv}.
\]

O transporte r=1−epsilon Eret dotP reproduz essa variação de E até primeira ordem. Esse é um passo efetivo para comparar as álgebras; não é ainda a identidade renormalizada de acordo perturbativo.

A nota também realiza a Ward estendida **com anomalia** num esquema que conserva os propagadores da referência B0 e trata os desvios e parceiros como fontes centrais formais. As mudanças da cinética, os termos lineares e os termos Omega da ação completa entram como inserções. A organização formal precisa manter esses termos; não se diferencia a expansão sem tadpole através de fundos arbitrários.

Essa construção produz o levantamento no esquema de referência. Ainda é necessário tratar B0, que pode permanecer nos coeficientes após a retração, e comparar o esquema com os produtos da família variável. Não se introduz um segundo fundo inerte para depois chamá-lo de ausente. A admissibilidade da primitiva e a remoção geral da anomalia continuam obrigações.

## 5. A positividade interagente ganhou uma recorrência

A [nota do estado formal](<C:/IALD/Central de Patentes/Chatgpt/POSITIVIDADE_BRST_FORMAL_072_20260910/ESTADO_INTERAGENTE_FORMAL_E_CONTRATOS.md>) distingue positividade física livre, representação auxiliar e cohomologia da carga. Um certificado algébrico de quartetos satisfaz {Q0,h}=N_aux e fornece uma inversa R0 na imagem de Q0.

Sob uma representação compatível com os campos Hadamard/Wick, domínio comum e carga renormalizada simétrica e nilpotente Q(z)=Q0+sum z^n Qn, todo vetor livre fechado admite o levantamento

\[
\psi_n=-R_0\sum_{j=1}^n Q_j\psi_{n-j}.
\]

A obstrução de cada passo é fechada e tem norma nula; a completude livre a torna exata. A mesma construção prova positividade formal e identifica o radical com a imagem da carga. Normalizar o levantamento do vetor físico produz um estado positivo nos observáveis interagentes admitidos.

O certificado de quartetos ainda precisa ser realizado na representação Hadamard/Wick apropriada ao modelo. A corrente, sua implementação e a QME também permanecem contratos efetivos. Não se infere o levantamento local de todo observável a partir do levantamento dos vetores, nem um estado global independente de cutoff.

A [revisão da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_072_20260910_004104_732492/PARECER_POSITIVIDADE_FORMAL.md>) conferiu a recorrência e o alcance. A [correção de orientação graduada](<C:/IALD/Central de Patentes/Chatgpt/POSITIVIDADE_BRST_FORMAL_072_20260910/PRECISAO_COMUTADOR_GRADUADO_E_R0.md>) mantém [A,Q]_gr=−(−1)^|A|[Q,A]_gr ao traduzir convenções; as provas de estado não são alteradas.

## 6. Caminho crítico atualizado

No setor de anomalias, agora existem uma primitiva concreta admissível para uma família, uma retração clássica de fundos, um transporte simplético de primeira ordem e uma realização de Ward com anomalia em referência fixa. Permanecem a classificação da quebra geral no espaço correto, o tratamento do fundo de referência, as identidades de acordo perturbativo e a remoção compatível com todos os produtos/inserções.

No setor físico, a recorrência de estados já está demonstrada sob contratos precisos. O trabalho efetivo passa a incluir a representação auxiliar compatível com Hadamard/Wick, a carga renormalizada no domínio comum e a compatibilidade das mudanças de cutoff/fundo.

A reconstrução gravitacional geral conserva sua obrigação de correspondência física e de alcance a partir dos mesmos dados selecionados. Os resultados condicionados à ação ambiente não demonstram automaticamente uma medida independente ou um BRST vertical das probabilidades P, se esse alcance for alegado. Condições finitas de renormalização, globalidade e UV permanecem distintas.

Os 21 módulos anteriores e as novas demonstrações ainda precisam de integração e, para estas últimas, formalização. A fase e o ramo já integrados não são reabertos. O objetivo geral permanece ativo.

Os pareceres e precisões devem acompanhar as notas na integração. O adendo de revisões, a memória, o desenho, o resultado estruturado e o manifesto são novos arquivos da bancada; a entrega no túnel aponta para eles. Verificações de integridade documental não são teoremas matemáticos, execução de diagramas ou confirmação física.
