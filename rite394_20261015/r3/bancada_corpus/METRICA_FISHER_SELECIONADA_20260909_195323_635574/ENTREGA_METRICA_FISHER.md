# Entrega: métrica de Fisher com relógio selecionado

[REAL — Lean, escopo compilado] SelectedFisherLorentzMetric.lean passou contra a biblioteca83 congelada: **21 teoremas, 7 outras declarações, 28 auditorias**, fonte e importador com exit 0, sem warning. Fonte congelada com 15368 bytes e SHA256 b7d4bf93ed9e41ab9c5211007cbe2057b2446aaee480dc7cd2fef1a72dd911e1. O recibo está em [BUILD_RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/METRICA_FISHER_SELECIONADA_20260909_195323_635574/BUILD_20260909_200624_640468/BUILD_RESULT.json>).

A entrada SelectedProbabilityData (:220) contém apenas P, normalização, positividade, suavidade, injetividade do diferencial conjunto, um rótulo fixo e não nulidade de dP nesse rótulo. Não contém g, F pronto, tetrada, inversa ou equação de Einstein.

A cadeia nova é P → F=Σ dP_i⊗dP_i/P_i → c=dP_selecionado → a=cᵀF⁻¹c>0 → g=(2/a)c⊗c−F. selected_fisher_positive (:240) deriva a positividade definida de F do posto. reflected_metric_lorentz (:95) deriva uma congruência com diag(+1,−1,−1,−1): uma fatoração F=BᵀB é extraída da positividade e uma reflexão ortogonal explícita adapta sua primeira linha. Nenhuma congruência é recebida como hipótese. O frame auxiliar serve à prova ponto a ponto; não precisa ser escolhido suavemente.

reflected_inverse_right, reflected_inverse_eq e reflected_inverse_left (:150, :172, :182) provam a inversa
g⁻¹=(2/a)(F⁻¹c)⊗(F⁻¹c)−F⁻¹.
A suavidade é obtida pela fórmula racional: inversa de F por adjugata/determinante positivo e divisão por a>0. selected_metric_smooth (:267) e selected_metric_inverse_smooth (:277) fornecem a interface analítica.

selectedLorentzRecord (:283) usa o codec existente somente como adaptador DE SAÍDA. selected_record_decodes_derived_metric (:287) prova que o registro devolve exatamente g(P). Os seus dezesseis parâmetros codificados não são identificados com os pesos P de entrada. selected_probability_curve_fisher (:292) liga F à curva diagonal normalizada efetiva P(x+tv), positiva localmente enquanto permanece em U; não lhe atribui matching de área.

[DERIVED — exemplo escrito] [EXEMPLO_CATEGORICO_CURVO.md](<C:/IALD/Central de Patentes/Chatgpt/METRICA_FISHER_SELECIONADA_20260909_195323_635574/EXEMPLO_CATEGORICO_CURVO.md>) constrói P=(x₀,x₁,x₂,x₃,1−Σx) no interior do simplex. O posto é quatro e o relógio dx₀ não se anula. Em coordenadas angulares, g=dr²−4cos²(r/2)h_S³, com curvatura mista não nula. Esse exemplo não recebeu certificado Lean neste lote; demonstra que a rota proposta não se restringe ao controle plano dos quatro Bernoulli-produto. Não há afirmação de cobertura de todas as métricas lorentzianas.

[INPUT] Quatro parâmetros, a família de observações/preparações, seus certificados de posto, o rótulo temporal fixo e a lei de leitura assinada. Positividade de Fisher sozinha não escolhe essa lei. zero_clock_control (:299) dá g(F,0)=−F, expondo por que o relógio não nulo importa. Se o diferencial perde posto, a positividade definida não segue. Variar rótulos sem uma lei suave pode destruir regularidade.

[OPEN] Realizar/justificar fisicamente P e a leitura assinada, escala e unidades, atlas físico, matéria compatível e correspondência de área. O exemplo categórico tem obstrução explícita ao matching de área para a curva afim em todas as direções nulas fora do ponto uniforme; a curva não deve ser confundida com os protocolos Gibbs quadráticos. Einstein não foi acrescentado como hipótese nem conclusão desta folha.

Preservação: nenhum um.py foi executado/importado. Nenhum original ou módulo congelado foi alterado. O builder foi copiado byte a byte do builder83. As tentativas e os backups imediatos de bytes permanecem na pasta. Compilação nova da folha/importador, com fronteiras diretas e biblioteca83 medidas; não é recompilação integral de todas as dependências transitivas.

A próxima composição possível é usar este registro métrico e covetores dP_j nos protocolos Gibbs já existentes. Isso pode eliminar covetores livres e derivar fechamento por simetria da Hessiana; as equações de onda e de área permanecem obrigações próprias. Ela não foi incluída neste recibo.
