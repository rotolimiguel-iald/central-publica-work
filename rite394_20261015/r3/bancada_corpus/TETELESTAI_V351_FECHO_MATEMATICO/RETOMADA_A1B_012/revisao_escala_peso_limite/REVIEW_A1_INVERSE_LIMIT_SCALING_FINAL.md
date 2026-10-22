# Revisão independente — escala dual do peso limite

2026-09-14T23:06:55.788351-03:00

**A1_INVERSE_LIMIT_SCALING_REVIEW_ACCEPTED__SEMIFINITE_TRACIAL_OPEN**

[REAL] **Sem achados P0/P1/P2.** Quatro teoremas públicos + um helper privado, zero definições. Módulo completo e auditor próprios rc0; quatro #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.

[REAL — identidade e contrato] Quatro teoremas públicos e um helper privado, zero definições. O peso é scalarInverseLimitWeight P; a ação sobre o MESMO PositiveCoreInput é TGLV351.positiveDual P, definida no contrato antigo por regularDualAction, cuja coerção é dualAmbient. O tipo final é ∀s X, value(positiveDual P s X)=ofReal(exp(-s))*value(X), exatamente o campo RegularCoreTraceData.dual_scaling ao especializar value:=scalarInverseLimitWeight P. Não foi construído um habitante do contrato, nem recebido outro peso/cone/ação como parâmetro.

[REAL — raiz e positividade] O helper recebe uma StarAlgEquiv complexa f e f(A)=r•B, com A,B≥0 e r≥0. Mostra que f(sqrt A) e sqrt(r)•sqrt B são positivos e têm o mesmo quadrado; CFC.mul_self_eq_mul_self_iff identifica-os. A raiz é sempre o wrapper antigo hilbertPositiveSqrt=CFC.sqrt, sem definição nova ou inversa. Na aplicação concreta todas essas hipóteses são descarregadas por positividade dos cortes e regularInverseGeneratorCutoff_dual; r=exp(s)>0 e o novo regulador εexp(s)>0. O caso genérico r=0 é permitido pelo helper; não há hipótese de comutação adicional.

[REAL — sinal da avaliação] scalarInverseCutoffWeight_dual transporta o sanduíche INTEIRO por dualAmbient(-s), usando a invariância da integral original. O input dualAmbient(s)X retorna a X por simetria da mesma StarAlgEquiv. Cada raiz recebe sqrt(exp(-s)); estrela conjuga esse escalar REAL sem trocar seu valor. As duas raízes produzem exp(-s), e a homogeneidade da mesma dualQuadraticIntegral fornece Wε(θ_sX)=ofReal(exp(-s))*W_(εexp(-s))(X). Não há substituição de invariância por tracialidade nem uso de domínio GNS/valor finito.

[REAL — cofinalidade e supremos] Para r>0, o lema escalado prova as duas desigualdades. Para cada n escolhe m com 1/(m+1)<r/(n+1); no sentido inverso escolhe 1/(m+1)<[1/(n+1)]/r, obtendo r/(m+1)≤1/(n+1). A antitonia já entregue e le_iSup_of_le dão igualdade dos supremos; não se afirma uma bijeção dos índices ou comutação indevida de limites. O último teorema usa r=exp(-s), a identidade aritmética (1/(n+1))*r=r/(n+1), e ENNReal.mul_iSup. Valores infinitos permanecem cobertos, sem toReal/cancelamento de infinito.

[REAL — fontes antigas e cronologia] V351RegularCoreTraceContract e V350CoreContractCounterexample foram copiados das fontes OLD/kernel após comparação byte a byte com K, e compilados por este Lake próprio; nenhum objeto foi herdado do autor. São dois fornecedores ANTIGOS, separados dos quatro alvos novos. O contrato antigo continua recusando o traço zero e ν como fornecedor direto; sua recompilação não declara traço novo. A ficha 22:53:53 antecede o primeiro DEV. O adendo 22:59:23 é POSTERIOR ao DEV final 22:58:45 e registra a reprodução antiga 22:56:00, não se apresenta como busca pré-código. Doze entradas de fornecedores foram confrontadas por nomes, linhas, enunciados e pins.

[REAL — histórico e negativo] Três DEV rc1 foram relidos e excluídos: 22:55:10 falhou na carga de objeto ausente, 22:56:43 teve coerções/recursão de simp e 22:57:46 ainda recursão de simp. Nenhum print parcial dessas falhas autoriza a prova. O final 22:58:45 é rc0 sem avisos. Pins históricos usam os snapshots reais, mantendo o path antigo apenas como localização textual. O negativo autoral substitui exp(-s) por exp(s) e falha por Type mismatch, não por ambiente; foi relido/pinado, não reexecutado. O módulo completo e auditor4 próprios passaram; o helper é coberto pelos axiomas transitivos públicos, e os 14 prints dos dois fornecedores antigos também foram conferidos separadamente.

[REAL — proveniência] 684 objetos próprios anteriores preservados; construídos alvo, auditor e dois fornecedores antigos, total 688. Dois fornecedores antigos reproduzidos de fonte; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em 68.298 s; zero avisos do alvo/auditor e 178 mensagens de fornecedores com origem separada no JSON. O stderr preserva ainda o aviso do cache aesop com alterações locais, já presente na base; não é aviso do alvo. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.

| Artefato | SHA256 lido |
|---|---|
| Fonte final (K=cópia própria) | 2aa1344d9f0ebbf8b3b87b1354b9ec20e10f0fd8b842789e925819c0c2b097ab |
| .olean próprio | 58d172b3a569a355d7f3bbdfe0d07ce29072ada548af7601df567ea457ee7ec2 |
| .olean autoral standalone, apenas comparação | 58d172b3a569a355d7f3bbdfe0d07ce29072ada548af7601df567ea457ee7ec2 |

Igualdade binária medida: True.

[OPEN — limites] Aceite exclusivo de quatro teoremas públicos e um helper privado; duas fontes antigas reproduzidas não aumentam essa contagem. ε>0 nos dois alvos de corte; r>0 na cofinalidade; o alvo final cobre todo s real e todo X:PositiveCoreInput P, inclusive peso infinito. Paga a escala dual do mesmo candidato ao campo exato do contrato. Semifinitude e tracialidade permanecem OPEN; não há habitante final de RegularCoreTraceData nem promoção de A1(b)/gate. Os 22/23 e todos os anteriores permaneceram intactos. Consultas de semifinitude não são provas adicionais deste delta. Cache de pacotes e objetos próprios anteriores reutilizados; nenhum objeto de projeto autoral/DEV, monólito, writer, recorder ou memória executado/modificado.

Artefatos de evidência:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_peso_limite\compilation.json>) — SHA256 07457b4724331f0cad601e73c401b6e9e86b0ee2d22e89133521671a7955c6c9.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_peso_limite\independent_20260914_230053_826820\run.json>) — SHA256 c5335f9979122d27b08777051bd07aea16a4b61e654cbfbce849e15207e6b967.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_peso_limite\independent_20260914_230053_826820\type_axiom_audit.json>) — SHA256 a4e945c4e88a9cc7c5afc182851a197bdddff7161e6057ac275b0bc0e47f0f00.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_peso_limite\history_read.json>) — SHA256 993b5f6812f72c35f6d5f2d235204672c810e4dca641565ba7c2e19cbc2c356b.
- [fornecedores da ficha](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_peso_limite\provider_checks.json>) — SHA256 0153a595e13e53cdc69e674a860356ab9b7abe6a4532ea407c490e76240274e7.
