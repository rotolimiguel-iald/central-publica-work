# Obrigações quânticas ainda abertas — reexame da fonte

[REAL — leitura estática, revisão independente] O programa mantém expressamente as três aberturas abaixo. A verificação foi feita no snapshot/cópia de seis módulos, preservado, sem importar ou executar Python. As referências permanecem válidas nesse arquivo histórico; não transportar seus números de linha automaticamente à sucessora.

1. [OPEN] **Perturbações gravitacionais gerais.** Completar a decomposição do setor físico além da família de ondas planas, justificar a ação Fierz–Pauli completa no modelo contínuo e estender a ausência de modos físicos de norma negativa ao setor geral. [Limites em prove_the_spectrum](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_112805_465076/um.py:134460>).

   [REAL] general_null_tt_ricci_zero já cobre qualquer direção nula; qgPhysicsCertificate_helicities descreve o quociente TT/gauge como R² no cone padrão; qgPhysicsCertificate_ghostfree prova a positividade da classe física. Portanto não cabe dizer que faltam todas as direções ou qualquer prova de positividade.

2. [OPEN] **Simetria na teoria quântica com interações.** Formular os objetos interagentes relevantes e demonstrar o resultado de ausência ou cancelamento de suas anomalias.

   [REAL] A bandeira relevant_anomalies_absent aponta para [qgPhysicsCertificate_anomaly](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_112805_465076/um.py:86118>), invariância algébrica do símbolo do Ricci linearizado para k, epsilon e xi arbitrários. Esse certificado paga o Ward clássico-linear. Seu enunciado não contém quantização nem interação. A limitação aparece em prove_the_spectrum e no escopo de matéria interagente de RGStability. Não rebaixar o certificado existente; não ampliar seu domínio pelo nome da bandeira.

3. [OPEN] **Critério UV da rota escolhida.** Definir e provar como a realização modular resolve ou evita o problema ultravioletas em seus próprios observáveis. A obrigação precisa especificar observáveis, escala/limite e noção de controle que pretende satisfazer; o critério concreto deve vir da rota física adotada, não de um requisito genérico imposto por analogia.

   [REAL] [prove_the_renormalization_wall](<C:/IALD/Central de Patentes/Chatgpt/COPIA_INTEGRADA_20260909_112805_465076/um.py:138985>) mantém o veredito WALL_TYPED_OPEN. Os checks certificam a tipagem e o registro das rotas, não a solução UV. A unitariedade e a nova identidade óptica exata estão demonstradas, mas esses enunciados não incluem escala UV ou controle do limite correspondente. Não se exige, por decreto, que a rota modular seja a renormalização perturbativa da métrica.

[DERIVED] Os três critérios acima decorrem das aberturas expressas na fonte; não são resultados adicionais de fechamento. O selo mantém a delimitação linearized_spin2_sector_proved. A revisão não encontrou bandeira posterior cujo enunciado amplie os certificados para os três domínios gerais.

Revisão independente: review_remaining_hypotheses. Originais intactos; nenhum programa executado.

[REAL — errata de leitura histórica] A string o_que_resta de prove_the_spectrum ainda inclui 'Einstein geral'. Essa frase histórica não autoriza afirmar ausência de teorema geral: GeometricEinsteinReconstruction já possui um, e GeneralMetricEinstein desta entrega reduz sua interface geométrica. A abertura atual é a correspondência geral dos dados selecionados com suas hipóteses físicas, conforme o relatório principal.
