# Revisão independente — álgebra fechada da ação direita e CFC

2026-09-14T21:06:46.209115-03:00

**A1_RIGHT_ACTION_ALGEBRA_REVIEW_ACCEPTED__RESOLVENT_RIGHT_ACTION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 12 declarações (10 teoremas, 2 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] Delta de 12 declarações: dez teoremas e duas definições, ScalarPolarRight e scalarPolarRightAlgebra. Fonte e ficha MD/JSON lidas integralmente. O domínio é TODO scalarWeightLeftIdeal P, o peso e a inscrição GNS anteriores, com scalarTomitaPolarFactor P original. Não há novo GNS, novo operador J ou hipótese de traço.

[REAL] scalarPolarRight_iff_cuts é uma equivalência efetiva. No sentido direto usa a identidade já obtida de Λ(Ab) e scalarGNSCutMap_weight_embedding; no reverso os cortes naturais identificam o vetor previamente fixado Jπ(b*)J⁻¹Λ(A) por scalarWeightGNSEmbedding_of_cut_actions. Portanto a pertença Ab∈nν é concluída, não assumida como consequência de uma igualdade entre expressões indefinidas.

[REAL] As leis zero/um/soma/escala/produto têm a orientação correta. Na escala complexa as conjugações de b* e de J se cancelam. No produto, a aplicação de b a A antecede a de c a Ab: ρ(bc)=ρ(c)ρ(b), com ρ(b)=Jπ(b*)J⁻¹. A prova não comuta b e c. Provas de pertença ao ideal são transportadas por Subtype.ext, sem mudar o elemento subjacente.

[REAL] scalarPolarRightAlgebra exige EXPLICITAMENTE as duas propriedades, de b e de b*. A condição estrelada do produto usa c*b* nessa ordem. Assim star_mem é descarregada por involução da estrela; não se infere fechamento pela estrela de uma hipótese de ação direita unilateral. A unidade pertence à álgebra; scalarPolarRightAlgebra_regular_mem põe cada elemento regular λ_t na mesma álgebra usando o lema já reproduzido para t e −t. O empacotamento não é vazio ou meramente nominal.

[REAL] scalarPolarRight_isClosed demonstra continuidade na NORMA: π é 1-Lipschitz pela cota do operador ambiente e sua restrição; dualOrbitRepresentation é limitada por ||b||. As equações dos cortes são igualdades de mapas contínuos; sua interseção topológica sobre todo A e todo n é fechada. Isso não é uma interseção a.e. não enumerável, nem continuidade forte geral de star. A álgebra é a interseção dessa propriedade fechada com sua pré-imagem pela estrela contínua.

[REAL] scalarRightAction_cfc faz CFC no B(H_regular) AMBIENTE. O core é fechado por sua igualdade com o duplo centralizador e Set.isClosed_centralizer. Sua inclusão é um mapa fechado de subtipo; isso torna fechada a imagem da álgebra direita. O IsClosed local necessário a cfc_mem é provado, não postulado. Nenhuma instância CompleteSpace ou CFC do subtipo N é presumida. O elemento da imagem é transportado de volta pela igualdade de valores e injetividade de Subtype.val.

[REAL] O último enunciado recebe f:ℂ→ℂ sem hipótese de continuidade ou normalidade de b porque afirma pertença do cfc totalizado da Mathlib, que também vale no ramo padrão zero. Ele NÃO identifica por si a ação pontual de uma função arbitrária ou um cálculo espectral fora de suas hipóteses. Para os consumidores R_n e sqrt(Bε), continuidade no espectro, normalidade/auto-adjunção e igualdade com os operadores existentes continuam obrigações concretas. Esse alcance é compatível com a ficha.

[REAL] A ficha precede o código, aponta nove fornecedores e liga o empacotamento ao uso de cfc_mem para a ação dos cortes na perturbação do peso. Os pins desses fornecedores e da busca são confrontados aos bytes no finalizador. Quatro tentativas autorais rc1 foram preservadas e excluídas (20:46:24, 20:49:26, 20:52:33, 20:59:15); incluem falhas de elaboração/coerção, constante inexistente, timeout e prints com sorryAx. Somente 20260914_210039_263478 rc0 sem avisos é aceito. O histórico completo está em history_read.json; não se supõe que os pins dos fontes antigos correspondam ao fonte final.

[REAL] Auditoria autoral relida e pinada, sem reexecução: BadRightActionProductOrder troca star(b*c) por star(c*b), mantendo o produto Abc na esquerda, e falha por Type mismatch com imports válidos. Este resultado certifica a rejeição da adulteração testada, não uma alegação de contraexemplo numérico a toda comutatividade possível.

[REAL] Execução própria rc0 em 86.69 s. 661 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351ScalarRightActionAlgebra | `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af` | `6df95ceec07c0c09d5626abad15921883c2beeddfc64c2671787226d5840491e` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Nenhum aproximante R_n ou limite forte-* concreto é construído neste delta; não se conclui R∈scalarPolarRightAlgebra. A identificação racional do corte existente Bε e sua raiz, a ação desses cortes, a perturbação e a tracialidade permanecem abertas. Sem nova condição para gate, sem cobrança de minorantes para ν, sem atualização de memórias ou programas. Consultas CFC/seno e DCT são propostas separadas e não contam como teoremas compilados.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_algebra_direita\independent_20260914_210431_947693\run.json>) — SHA256 `509a9b8b9f052c82ce231518c7230fe9a42b0dde6e474c74e89932d0498de1db`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_algebra_direita\compilation.json>) — SHA256 `ed8a1ce06af9070d34119e4b6041873729c1aca07e3c17544dd0456a48320285`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_algebra_direita\independent_20260914_210431_947693\type_axiom_audit.json>) — SHA256 `35877c9a8cb9eecbc10dc09b3c48fae218c4d81c77d8f8d47c39db3ec295cb99`.
