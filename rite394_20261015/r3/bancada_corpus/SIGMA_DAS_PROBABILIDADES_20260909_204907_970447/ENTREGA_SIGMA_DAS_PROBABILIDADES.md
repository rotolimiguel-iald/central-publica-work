# Sigma das mesmas probabilidades — entrega local

[REAL — Lean] SelectedProbabilitySigma passou na primeira compilação: 19 teoremas, 5 definições e 24 auditorias de axiomas. Fonte e importador terminaram com exit 0, sem warnings; os termos auditados usam somente propext, Classical.choice e Quot.sound. Namespace: ChatgptAudit.SelectedSigma.

[Fonte congelada](<C:/IALD/Central de Patentes/Chatgpt/SIGMA_DAS_PROBABILIDADES_20260909_204907_970447/SelectedProbabilitySigma.lean>): 12.479 bytes, SHA-256 eaa0121a02a3f0d32b1f6da09ae2ef133c6689d227e12cdb97a5969d1cac711e.
[Recibo PASS](<C:/IALD/Central de Patentes/Chatgpt/SIGMA_DAS_PROBABILIDADES_20260909_204907_970447/BUILD_20260909_205211_077766/BUILD_RESULT.json>): compilação isolada sobre a biblioteca transposta 93 aprovada, com fronteira medida antes/depois e preservada. O recibo não declara reconstrução ou hashing integral das dependências transitivas canônicas/Mathlib.

## Construção e resultado

[REAL — Lean] A entrada é SelectedProbabilityData (Option J) U, com J finito e não vazio. Ela contém as probabilidades P, seus certificados de normalização, positividade e suavidade, o diferencial injetivo na carta de dimensão quatro e um relógio selecionado não nulo. A hipótese hsel fixa P.selected=none.

O complemento é definido por 1−P(x,P.selected), lendo o rótulo efetivamente selecionado. Sob hsel, selected_complement_sum (linha 35) o identifica com Σ_j P(x,some j); selected_complement_positive (linha 46) prova sua positividade em U. Portanto

Q_j(x) = P(x,some j)/(1−P(x,none)),
φ_j(x) = √Q_j(x)

são positivos em U. conditional_probability_none (linha 30) estabelece explicitamente o denominador acima, e conditional_probability_normalized (linha 57) prova ΣQ_j=1. As raízes são suaves no aberto porque seus argumentos são estritamente positivos. sigma_potential_normalized (linha 81) prova Σφ_j²=1; sigma_tangent_constraint (linha 103) prova Σφ_j dφ_j=0.

[REAL — Lean] Os covetores sigmaCovectors P são dφ_j. Sua suavidade e fechamento são derivados nas linhas 93 e 98. A fonte não recebe covetores independentes.

[REAL — Lean] selectedSigmaRecord (linha 110) usa selectedLorentzRecord P e esses potenciais na preparação Gibbs. selected_sigma_metric (linha 115) prova que sua métrica é exatamente selectedMetric P, já construída a partir do Fisher e do relógio do mesmo P. O codec é aplicado somente como adaptador posterior à construção dessa métrica.

Para k>0, selected_sigma_source (linha 120) identifica a fonte do registro com a soma

T = Σ_j c [dφ_j⊗dφ_j − (1/2) g g⁻¹(dφ_j,dφ_j)],
c = k/(π cosh² k).

Métrica, covetores e T não são entradas independentes dessa definição. As linhas 129 e 138 identificam os coeficientes quadráticos entrópico e modular Gibbs na direção nula v com −πT(v,v).

[REAL — Lean, condicional] Se os campos construídos satisfazem Box_g φ_j=λ(x)φ_j para um λ comum, selected_sigma_conserved (linha 148) deriva a conservação total. Isso usa o cancelamento sigma, sem pedir ondas individuais nulas e sem receber a conservação como segunda hipótese.

[REAL — Lean, condicional] selected_sigma_einstein_from_area (linha 169) conclui G+Λg=(2π/η)T, com Λ constante no aberto preconexo U. A conclusão usa g=selectedMetric P e a fonte do mesmo selectedSigmaRecord.

## Hipóteses que permanecem

[INPUT] Positividade e normalização de P, suavidade, posto completo do diferencial em dimensão quatro, rótulo temporal fixo e relógio não nulo. A leitura assinada g=(2/a)c⊗c−F continua a construção geométrica escolhida; esta folha não deduz sua universalidade física.

[INPUT — equação dinâmica em P] Box_g φ_j=λ(x)φ_j não decorre automaticamente de Σφ_j²=1. Não formalizamos aqui a identificação de λ com −Σ_j g⁻¹(dφ_j,dφ_j); a versão comum solicitada basta à conservação.

[POSTULATE — correspondência física na aplicação] A condição de área Gibbs ΔS−ηΔA=o(t²) continua escrita explicitamente em harea, em cada ponto e direção nula não zero, com telas de equilíbrio, k>0 e η≠0. A definição dos campos e a conservação não removem essa condição. O teorema não contém um axioma Lean novo: harea é uma hipótese parametrizada cuja interpretação física é marcada como postulada.

[OPEN nesta folha] A parametrização por raízes escolhe a região positiva da esfera: φ_j>0. Não representa automaticamente setores com sinais arbitrários ou cruzamentos de probabilidade zero. Todas as garantias de positividade e regularidade são em U; as funções totais fora dele não recebem essas garantias.

[OPEN nesta folha] Quantização do modelo sigma, identificação com campos CCR livres, variação de uma ação em P quando g[P] também varia, construção de um habitante global compatível e confirmação física. O protocolo Gibbs quadrático usa covetores derivados de P, mas não é identificado com a amostragem afim P(x+tv). A geometria continua sendo Levi-Civita sem torção. Nenhuma alegação de que toda métrica lorentziana seja coberta decorre daqui.

## Preservação e proveniência

[REAL — operação local] Fonte e documentos nasceram em pasta nova Chatgpt. A fonte passou sem correções e não foi editada após o PASS. O builder e a configuração foram copiados byte a byte da pasta GIBBS_RELOGIO_ASSINADO_20260909. Nenhum um.py foi executado ou importado; nenhum original, memória canônica ou módulo anterior foi alterado.

Este documento registra análise do próprio autor da folha e evidências de compilação medidas. Não atribui aprovação independente a terceiros. A derivação prévia foi escrita antes da fonte e permanece ao lado desta entrega.
