[REAL — escopo compilado] Pullback métrico efetivo de Euler: 15 teoremas, 3 definições, 18 auditorias, dois processos exit 0, sem advertências. A derivada temporal em zero coincide com coordinateMetricLie canônico, e o Jacobiano usado foi demonstrado como a derivada espacial verdadeira.

# Entrega — pullback de Euler e direção de Lie

09/09/2026 · Bancada /root/selected_geometry_design · Fonte congelada após PASS e revisão semântica favorável do agente raiz.

## Objeto e resultado

Definições efetivas:

φ_t(x) = x + t V(x)  
J_t(x) = I + t DV_x  
g_t(x) = J_t(x)ᵀ g(φ_t(x)) J_t(x)

vector_fderiv_is_jacobian representa a derivada de Fréchet de V por vectorJacobian. euler_map_hasFDerivAt prova Dφ_t(x)=J_t(x) como aplicação linear contínua, e euler_jacobian_is_spatial_derivative identifica também o Jacobiano coordenado de φ_t com J_t. A ação matricial reutilizada é boostMatrixAction, cuja definição canônica é a aplicação linear de uma matriz arbitrária, explicitada pelo lema boost_matrix_action_apply; não se assume um fluxo de boost para V.

A regra da cadeia fornece a derivada de g(φ_t(x)) em zero como ∑_k V^k ∂_k g. A regra do produto matricial fornece

d g_t(x)/dt|₀ = (DV_x)ᵀ g(x) + ∑_k V^k(x) ∂_k g(x) + g(x) DV_x
              = coordinateMetricLie g V x.

A igualdade final usa coordinate_metric_lie_matrix_formula de LieMetricJets. A conclusão é HasDerivAt da função com valores matriciais, além da versão canônica HasMatrixDerivAt por componentes.

## Critérios

| Elo | Estatuto | Teorema |
|---|---|---|
| Jacobiano como derivada espacial efetiva | PAGO | euler_map_hasFDerivAt |
| Igualdade com o Jacobiano coordenado canônico | PAGO | euler_jacobian_is_spatial_derivative |
| Pullback em zero devolve g | PAGO | euler_pullback_zero |
| Derivada do pullback igual à direção de Lie | PAGO | euler_metric_pullback_hasDerivAt |
| Corolário conjunto com g e V suaves em U | PAGO | smooth_euler_pullback_realizes_lie |
| det J positivo perto de zero | PAGO, em cada x fixo | euler_jacobian_det_positive_near |
| Permanência de φ_t(x) em U | PAGO, localmente | euler_map_mem_near |
| Certificado local conjunto | PAGO | smooth_euler_local_certificate |
| Fluxo exato, inversa global e atlas diferenciável | NÃO AFIRMADOS | Fora deste enunciado |

## Hipóteses e limites

As provas do Jacobiano espacial usam diferenciabilidade de V em x. A derivada temporal do pullback exige diferenciabilidade das componentes de g em x; nessa parte, x é fixo e J_t é uma curva matricial explícita. O corolário conjunto recebe g e V suaves no aberto U e deriva os requisitos pontuais das APIs canônicas. Não há necessidade de uma métrica especial, simetria, assinatura lorentziana ou um campo V restrito para essa identidade cinemática.

A positividade de det J_t decorre de sua continuidade e det J_0=1. J_t é invertível para t suficientemente próximo de zero em cada x fixo. O teorema não oferece raio uniforme em todos os x, não constrói uma inversa da aplicação φ_t e não a declara difeomorfismo global.

A família de Euler não é apresentada como fluxo exato de V, nem recebe lei de grupo. O módulo não afirma naturalidade finita não linear do tensor de Einstein ou deriva temporalmente sua curvatura ao longo desta família; estabelece o elo métrico efetivo e sua direção de Lie. Não introduz condição de área, conservação ou correspondência física.

## Evidência e reprodução

Fonte: [EulerMetricPullback.lean](<C:/IALD/Central de Patentes/Chatgpt/PULLBACK_EULER_LIE_20260909_145850_073045/EulerMetricPullback.lean>)  
Bytes: 9315  
SHA-256: ef30f5939ec3e44b11a56d3b00312ba460b2fafba10e866dfa37e25d0372523a

Recibo: [BUILD_RESULT.json](<C:/IALD/Central de Patentes/Chatgpt/PULLBACK_EULER_LIE_20260909_145850_073045/BUILD_20260909_150232_847826/BUILD_RESULT.json>)  
SHA-256: 29313836e74190e9c70eb7db05f047a7e06a01d20c7a0da9b74faa258a557b10

Derivação prévia: [DERIVACAO_PREVIA.md](<C:/IALD/Central de Patentes/Chatgpt/PULLBACK_EULER_LIE_20260909_145850_073045/DERIVACAO_PREVIA.md>)  
Revisão recebida: [REVISAO_REGISTRADA.md](<C:/IALD/Central de Patentes/Chatgpt/PULLBACK_EULER_LIE_20260909_145850_073045/REVISAO_REGISTRADA.md>)  
Configuração: [CACHE_EULER.json](<C:/IALD/Central de Patentes/Chatgpt/PULLBACK_EULER_LIE_20260909_145850_073045/CACHE_EULER.json>)

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\PULLBACK_EULER_LIE_20260909_145850_073045\build_euler_pullback.py' 'C:\IALD\Central de Patentes\Chatgpt\PULLBACK_EULER_LIE_20260909_145850_073045\CACHE_EULER.json' EulerMetricPullback
```

A nova folha e um importador foram compilados em processos separados. Cada declaração foi auditada por #print axioms; as 18 auditorias usam somente propext, Classical.choice e Quot.sound. As 5 dependências locais PASS foram copiadas em bytes de seus builds aprovados e conferidas contra fonte/recibo. A fronteira monitorada permaneceu com os mesmos hashes antes e depois.

Este build não recompilou nem mediu todos os arquivos transitivos das dependências canônicas/Mathlib. O campo independent_review=false do recibo descreve o builder; o parecer independente recebido do agente raiz está registrado separadamente.

A primeira tentativa BUILD_20260909_150059_028533 permanece intacta com FAIL_VISIBLE, log de erros de elaboração e advertências de nomes depreciados. As correções preservaram enunciados e hipóteses. O backup imediato da fonte anterior foi mantido em bytes.

Nenhum um.py foi executado/importado. Nenhum original, módulo congelado anterior, memória canônica, Atlas ou selo foi alterado. Todas as escritas ocorreram nesta nova pasta Chatgpt. Este módulo encerra a frente solicitada.
