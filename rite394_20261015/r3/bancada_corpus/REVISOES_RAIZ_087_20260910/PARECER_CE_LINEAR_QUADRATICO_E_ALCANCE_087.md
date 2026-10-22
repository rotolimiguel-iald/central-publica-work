# Revisão da raiz087 — setores CE e alcance da composição clássica

10/09/2026. /root. [DERIVED — revisão escrita]. [REAL — integridade documental, separada da matemática].

Li integralmente as demonstrações dos setores linear e quadrático na preparação desta entrega e, após sua emissão, os dois pareceres independentes específicos. Não identifiquei erro material no contrato comum: espaço-forma Lorentziana orientada de dimensão quatro, K>0 fixo, setor métrico com sigma constante projetado, coeficientes reais herdados inertes e finitos jatos em cada elemento. A conclusão não é uma compilação Lean nem um cálculo executado.

## 1. Setor linear

[Demonstração linear de Herschel.](<C:/IALD/Central de Patentes/Chatgpt/CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910/ACICLICIDADE_CE_LINEAR_E_PRIMEIRO_DIFERENCIAL.md>)

O ponto decisivo é a ausência de tipos de formas exteriores no módulo graduado de Weyl: os pesos (r+4,r) e (r,r+4) têm diferença quatro, enquanto ΛᵖV* exige diferença zero ou dois. A injeção estrita no símbolo plano transporta essa ausência ao quociente curvo, pois um elemento não nulo de ordem finita tem símbolo principal não nulo. Logo Bᵖ(N₁)=0 para p=0,…,4.

Esse resultado horizontal sozinho não seria uma prova de aciclicidade do CE inteiro. A nota paga a etapa adicional: cada corte finito sob a isotropia semissimples tem coeficientes sem componente trivial; a cohomologia vertical é zero em todos os graus. Cissões equivariantes finitas conservam primitivas invariantes. Elimina-se o menor grau horizontal subtraindo dR com o diferencial completo, incluindo curvatura. Há no máximo cinco valores horizontais. Em grau vertical zero, o ciclo já é zero; não se inventa uma primitiva de grau negativo.

Tensorizar os argumentos reais com Rher conserva exatidão, inclusive com nilpotentes. O resultado é HᵠCE(g,N₁)ʰ=0. Na filtração por valência isso é a aciclicidade de d₁ na diagonal m=E−ghost=1, e não a nulidade do espaço H(s₀) dessa diagonal. O [parecer de Turing](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CE_LINEAR_087_20260910_072356_6364824/PARECER_ACICLICIDADE_LINEAR_E_D1_087.md>) conferiu também a hipótese finita da importação Chevalley–Eilenberg. Minha leitura do parecer não é apresentada como nova leitura direta da primária histórica.

## 2. Setor quadrático

[Demonstração quadrática de Turing.](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md>)

A prova constrói I_r=½⟨∇̄_(r)W,∇̄_(r)W⟩ e J_r=½⟨∇̄_(r)W,*∇̄_(r)W⟩ como elementos CURVOS efetivos, com simetrização normalizada. Os dois símbolos independentes fornecem geração e independência por redução finita da maior ordem. A filtração usa a SOMA das ordens dos fatores; K tem grau zero. Assim B⁰ tem base algébrica I_r,J_r, e B¹ tem base dI_r,dJ_r.

Para B², os tipos permitidos aparecem com sinal de troca negativo no produto de dois Weyl de mesma ordem. São excluídos da potência simétrica bosônica. Os tipos cruzados não atingem o alvo. Portanto B²=0. Essa etapa não foi inferida da classificação de vetores.

A igualdade □I_r=2I_(r+1)+L_r, e sua versão dual, tem restos de ordem no máximo 2r+4. Os comutadores curvos atuam em TODOS os índices, e ∇̄R₀=0 é usado explicitamente. A diagonal dois vem do termo de Leibniz e da simetrização normalizada. Permite redução finita a I₀,J₀ no quociente por □; a ordem principal impede uma relação residual não nula. Não se inverte □ e não se estende a jatos infinitos por coeficiente.

Segue Hᵖrel(N₂)=0 salvo p=4, onde há duas classes livres. No CE inteiro, a filtração horizontal tem cinco níveis e a segunda página só tem coluna p=4. Nenhum diferencial posterior entra ou sai. Os dois geradores verticais de grau três dão os postos 2,4,2 em graus totais 4,7,10, respectivamente. A coluna única em cada grau elimina extensões entre peças; não há limite inverso nesse cálculo.

O [parecer de Singer](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_RELATIVO_QUADRATICO_087_20260910/PARECER_GERACAO_CURVA_RELATIVO_E_CE_087.md>) verifica separadamente esses passos e conserva a distinção entre a cohomologia CE após d₁ e o BRST clássico completo. I₀ usa a normalização da086: I082=2I₀; J₀ mantém a convenção. Não se mistura J₀, pseudoescalar, com o operador J=Luz.

## 3. Composição da classe par: autoria e revisão separadas

A [nota da classe par](<C:/IALD/Central de Patentes/Chatgpt/CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md>) é de minha autoria. Não a apresento como aprovada independentemente por mim. Seu [parecer independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CLASSE_PAR_BRST_087_20260910/PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md>) é de Herschel; o [adendo subsequente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CLASSE_PAR_BRST_087_20260910/ADENDO_CONSUMO_REVISAO_N2_087.md>) registra a leitura efetiva do parecer quadrático de Singer, fechando a dependência documental da composição sem misturar as autorias.

A conclusão revista é uma linha livre Rher[A_I] em H⁴(C_N,s) para N≥6 e no complexo formal, detectada pela projeção a C₆. s é o BV–BRST CLÁSSICO completo por valência. A impossibilidade de uma primitiva considera o complexo com antifields; não há hipótese de ausência de antifields para possíveis fronteiras. O ciclo completo de Pontryagin, por sua vez, tem a primitiva de transgressão e é s-exato. A diferença não é uma contradição: sua primitiva começa em valência inferior e liga diagonais distintas do CE.

Não se conclui que H⁴ inteiro seja uma linha, que todas as outras classes desapareçam, que um limite inverso comute com cohomologia, ou que s já seja um operador quântico renormalizado.

## 4. Efeito sobre o caminho crítico

A [auditoria do critério074 por Singer](<C:/IALD/Central de Patentes/Chatgpt/CONTRATO_CRITERIO_ANOMALIAS_087_20260910/CRITERIO_074_GRUPOS_EXATOS_E_MAPA_085_086.md>) foi lida integralmente. Suas remissões tornam explícito que o critério074 exige grupos de FORMAS com coeficientes em H(s) completo: em particular H¹(Ē;H⁴(s)), além dos outros canais de grau total cinco. Não exige simplesmente H⁴(s)=0. Portanto a linha par não refuta esse critério nem é, por si, uma anomalia física de ghost um.

A revisão matemática acima é dos setores CE. A auditoria074 terá exame independente próprio de suas condições; não conto minha leitura de seu texto como nova prova de todas as importações e normalizações causais ali catalogadas. Continua possível trabalhar diretamente com uma primitiva admissível da anomalia concreta, em vez de provar nulidade de cada grupo suficiente.

Ainda faltam o transporte ao setor físico sigma não constante, admissibilidade e compatibilidade dos contratermos, fechamento interagente/QME, a rota UV e a realização gravitacional dos MESMOS dados selecionados. A fase/ramo e H3 interno já pagos na linhagem não são reabertos pela homonímia com graus de cohomologia.

## 5. Custódia

Este emissor mediu os oito arquivos efetivamente referidos antes/depois e verificou os destinos dos links. Fonte lida e parecer lido são atividades distintas de execução matemática. Nenhum um.py, CAS, Lean ou rito foi executado; nenhum original, Atlas, índice ou memória canônica foi escrito. Somente esta nota nova, seu recibo e o helper novo vivem em Chatgpt.
