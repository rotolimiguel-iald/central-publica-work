# Seleção, ângulo de Miguel e reconstrução — correção de leitura

09/09/2026. Bancada Chatgpt; originais somente leitura. Base canônica conferida: v334, SHA do um.py em EVIDENCIAS_DA_LEITURA.json.

## 1. Correção que o operador exigiu

[INPUT] O operador lembrou que os critérios de falsificação já estão no um.py e que a seleção deve ser acompanhada até a fase angular, de onde se reconstrói a informação.

[REAL — fontes] A objeção procede quanto à existência dos critérios: _MAPA_PILARES, um.py:157814, contém 14 pilares; _mapa_falsificadores_md, :157833, gera “Como matar esta teoria”. Exemplos operacionais:
- NEUTRINO_M2_V2: desvio de pelo menos 5 sigma em DUAS determinações independentes; regra em :4486, implementação em :4526.
- VOID_FLOOR: limite SUPERIOR corrigido por família abaixo de beta e p global < 2,87e-7, após aprovação dos controles de sistemáticos; evaluate_void_floor_test, :127092–127111.
- Outros critérios e classes estão preservados no inventário estruturado desta leitura. O protocolo privado de colapso não foi copiado.

A indicação anterior de que seria necessário escrever os resultados incompatíveis com a teoria foi imprecisa: eles já estavam escritos. Não confundir existência dos critérios, sua execução e aprovação pelos testes. Diagnóstico documental secundário: o texto curto de _MAPA_PILARES diz “limite inferior” no piso, enquanto o avaliador usa limite SUPERIOR; o critério operativo foi citado acima. Nenhum original alterado.

## 2. A cadeia que faltou à resposta anterior

[REAL — teoremas canônicos lidos e hashes conferidos]
TheAngleIsTheProjection.lean demonstra:
O(theta) = exp(i theta) P_plus + exp(-i theta) P_minus,
com os projetores conhecidos e partindo a identidade.

TheObserverReadsTheAngle.lean demonstra:
P_plus O(theta) = exp(i theta) P_plus.

Logo a face selecionada carrega o valor complexo da fase. A seleção não precisa perder informação sobre a forma inteira QUANDO o objeto pertence à família angular prescrita: a outra fase já está vinculada à primeira pela lei da família.

A referência anterior somente a TheIALDSelector.lean, sem seguir essa cadeia, não bastava para avaliar a afirmação do operador sobre reconstrução.

## 3. Composição agora verificada em Lean

No módulo novo SelectionAngleReconstruction.lean:

phaseReading(A) := 2 * (P_plus * A)[0,0]
angularDecoder(z) := z P_plus + z^(-1) P_minus.

A entrada [0,0] de P_plus vale 1/2; portanto
phaseReading(O(theta)) = exp(i theta).

Como exp(i theta) nunca é zero e sua inversa é exp(-i theta):
angularDecoder(phaseReading(O(theta))) = O(theta).

[REAL — compilação desta bancada] Há sete teoremas e duas definições, nove declarações auditadas. Resultado PASS_COMPILED_SCOPE; todas dentro de propext/Classical.choice/Quot.sound, e o lema geral de injetividade sem axiomas. A compilação de importação também retornou 0. Não há avisos no resultado aceito.

Teoremas:
1. phase_reading_is_the_angular_phase — extração da fase;
2. angular_family_reconstructed_from_one_selected_face — reconstrução integral da matriz da família por uma face;
3. one_selected_face_separates_angular_forms — duas formas da família com mesma seleção são iguais;
4. angular_form_is_the_boundary_s_matrix — ligação explícita angFamily = Smat; as duas definições complexas reduzem à mesma matriz, fechada por rfl;
5. miguel_boundary_reconstructed_from_its_selected_face — especialização em thetaMiguel(beta);
6. ambient_selection_has_distinct_inputs — controle de domínio: P_plus e I são distintos mas têm a mesma projeção à esquerda;
7. reconstruction_on_all_inputs_forces_injectivity — qualquer decodificador exato para todas as entradas exige injetividade nesse domínio.

O primeiro build compilou as proposições, mas a guarda da bancada recusou dois avisos de estilo. O segundo retirou um argumento simp não usado e um combinador de táticas desnecessário, sem alterar enunciados, e passou. Primeiro build e backup de bytes foram preservados.

## 4. O que significa “informação completa”

[REAL — alcance] Reconstrói-se a MATRIZ COMPLETA pertencente à família angular prescrita, usando a fase complexa selecionada e os projetores já conhecidos. Não é mera recuperação do componente projetado.

Não é preciso escolher um ramo de theta para recuperar O(theta), que é periódico. Para recuperar theta como número real, é preciso especificar o ramo; thetaMiguel(beta)=arcsin(sqrt(beta)) já escolhe um. A identidade de reconstrução compilada vale para qualquer beta real como parâmetro dessa definição; a interpretação probabilística de beta conserva 0<=beta<=1.

[DERIVED — compatibilidade com irreversibilidade] A seleção pode ser muitos-para-um no espaço ambiente e injetiva num conjunto admissível mais restrito. Isso permite reconstrução do conteúdo codificado sem produzir uma inversa universal de toda redução irreversível.

[OPEN — não coberto pelo novo módulo]
- A leitura matricial P_plus O(theta), o ialdSelector em ellTwo, a expectativa de colapso no fator e o índice Python têm tipos distintos. O módulo novo liga angFamily a Smat; não constrói um transporte de todas essas estruturas entre si.
- A prova usa o valor COMPLEXO completo da fase. Ela não afirma que uma etiqueta de seleção, uma intensidade isolada ou uma medição de precisão finita carrega automaticamente esse valor.
- A identidade recompõe a forma angular. Não é, por si, reconstrução de um estado arbitrário de ellTwo, de todo o fator, de todos os graus físicos ou de uma métrica 3+1.
- A especialização thetaMiguel(beta) não deriva o valor de beta sem entrada; o runtime canônico usa alpha CODATA vezes sqrt(e). O ângulo canônico comum não é, isoladamente, um código de todas as configurações distintas.
- Há outra reconstrução canônica mais ampla, geometric_log_reading_injective e the_word_fixes_the_place: uma leitura real exata distingue configurações booleanas no perfil construído, para t!=0. Ela merece ser preservada, mas não foi identificada por este módulo com o ângulo constante de Miguel.
- A ocorrência física particular de um colapso e a correspondência região–álgebra/área–entropia são enunciados adicionais. A definição tipada do colapso e seus estatutos físicos não foram modificados.

É correto chamar a igualdade obtida de resultado do modelo com interpretação física proposta. A frase “seleção não pode reconstruir” é ampla demais e foi corrigida. A frase “esta igualdade já atesta todo o colapso físico e toda a reconstrução gravitacional” excede os enunciados verificados.

## 5. Evidências e entrega à sessão que codifica

Arquivo formal: SelectionAngleReconstruction.lean.
Compilação aceita: BUILD_20260909_083701_077373/BUILD_RESULT.json e logs no mesmo diretório.
Fontes canônicas e falsificadores: EVIDENCIAS_DA_LEITURA.json.
Manifesto desta bancada: MANIFESTO_DA_BANCADA.json.

[REAL] As dependências diretas, fontes e binários importados foram hasheados antes/depois e permaneceram iguais. Usaram-se bibliotecas compiladas já existentes; não foram recompiladas todas as dependências transitivas. Nenhum original um.py foi executado/importado, nenhum fonte canônico foi editado, nenhum gate foi movido.

[OPEN — revisão] Esta é a compilação da bancada que construiu o módulo; revisão científica independente e integração na v334/versão seguinte não foram realizadas aqui. Não somar seus sete teoremas à contagem canônica antes de integração e nova rodada. O Atlas canônico permanece fonte única, sem cópia ou bifurcação. Este adendo fornece à gerência os resultados e o alcance para atualizar as superfícies da casa conforme o processo vigente.
