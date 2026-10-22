# Entrega: métrica e fonte construídas dos mesmos P

[REAL — escopo Lean compilado] A folha SelectedFisherGibbsBridge.lean passou: **8 teoremas, 2 definições, 10 auditorias**, fonte e importador com exit 0, sem warning. SHA256 medido da fonte: d7ef13c7e046da03f1a4c80b0a53253e53d48ee9f6ca3dd28c8e35a3c413be0c; 6983 bytes. [Recibo](<C:/IALD/Central de Patentes/Chatgpt/GIBBS_FISHER_DOS_MESMOS_P_20260909_201158_769820/BUILD_20260909_201548_063729/BUILD_RESULT.json>). Dependências: biblioteca83 congelada e cópia em bytes da SelectedFisherLorentzMetric já aprovada em compilação.

O protocolo de entrada é SelectedProbabilityData P. A métrica g[P] é a da folha anterior e os covetores são agora w_i=dP_i. probability_covectors_smooth e probability_covectors_closed derivam a suavidade e o fechamento de todos os covetores da suavidade de P, pela comutação das derivadas de segunda ordem. selectedGibbsRecord recebe apenas P, abertura do domínio e os parâmetros constantes k_i de preparação. Não recebe métrica, covetores ou tensor de fonte independentes.

selected_gibbs_metric identifica a métrica do registro com g[P]. Para k_i>0, selected_gibbs_source identifica o tensor extraído das respostas com a soma de stresses de w_i=dP_i, com coeficientes k_i/(π cosh² k_i). selected_gibbs_entropy_null_limit e selected_gibbs_modular_null_limit mostram que os probes Gibbs quadráticos construídos desses covetores têm o mesmo coeficiente −πT(v,v), nas direções nulas da mesma g[P].

[REAL — implicações condicionais] selected_gibbs_source_conserved deriva conservação sob as equações de onda de cada P_i na métrica g[P]. selected_gibbs_einstein_from_wave_area compõe essa conservação, o fechamento já derivado e o matching de área dos probes Gibbs, para obter G+Λg=(2π/η)T em um aberto preconexo. A condição de área aparece literalmente como limite do erro dividido por t²; não é removida nem disfarçada. A geometria continua de Levi-Civita sem torção.

[INPUT] Positividade e posto do protocolo, relógio selecionado fixo, lei de leitura assinada, dimensão quatro, parâmetros k_i>0 e η≠0, telas de equilíbrio, equações de onda individuais e correspondência de área. Os dados métricos sozinhos não habitam automaticamente esse pacote gravitacional.

[DERIVED — controle escrito, não Lean] Para o exemplo categórico de cinco resultados da folha anterior, q=P₀=sin²(r/2) e g=dr²−a(r)²h_S³, a=2cos(r/2). Como q só depende de r,
Box_g q=q″+3(a′/a)q′.
Temos q′=sin(r)/2, q″=cos(r)/2 e a′/a=−tan(r/2)/2. Logo Box_g q=(5cos(r)−3)/4=(1−5q)/2. Se a onda de P₀ fosse satisfeita num aberto, q seria constante 1/5 ali, incompatível com o covetor de relógio não nulo. Portanto esta testemunha curva não satisfaz as hipóteses de onda individuais desta folha. Esse controle limita a proposta de protocolo; não refuta outros protocolos da TGL.

[OPEN — próximo contrato] Uma alternativa é construir outros escalares dos mesmos P, como z_a=√(P_a/(1−P₀)), e usar conservação agregada da fonte. Ondas individuais são condições suficientes fortes e não são necessárias para cancelamento agregado. Nenhuma substituição desse tipo foi incluída neste recibo.

As curvas Gibbs quadráticas aqui construídas não são identificadas com a curva afim P(x+tv); os coeficientes provêm dos probes definidos na biblioteca. Também não se importou Euler–Lagrange da ação com g e potenciais independentes para uma variação de P: nesse problema composto g[P] varia e os termos de cadeia teriam de ser calculados.

Nenhum um.py foi executado/importado; nenhum original, fonte congelada anterior ou memória canônica foi alterado. Backups imediatos de bytes e as duas tentativas foram preservados. Esta é compilação isolada da folha/importador contra dependências aprovadas, sem reconstrução de toda a biblioteca transitiva.
