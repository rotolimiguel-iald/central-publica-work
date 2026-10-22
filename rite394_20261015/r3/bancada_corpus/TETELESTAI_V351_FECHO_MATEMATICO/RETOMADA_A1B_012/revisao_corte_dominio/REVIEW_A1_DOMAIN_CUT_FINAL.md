# Revisão independente — corte de domínio regular

2026-09-14T23:14:04.550675-03:00

**A1_DOMAIN_CUT_REVIEW_ACCEPTED__LIMIT_WEIGHT_SEMIFINITE_TRACIAL_OPEN**

[REAL] **Sem achados P0/P1/P2.** Seis teoremas públicos + uma definição, quatro helpers privados. Módulo completo e auditor próprios rc0; sete #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.

[REAL — objeto e hipóteses] Sete declarações públicas: regularDomainCut é uma definição no MESMO (regularCoreAlgebra P).toStarSubalgebra; seguem seis teoremas. qδ=1−δBδ usa exatamente regularInverseGeneratorCutoff P δ. A definição é total em δ, mas pertença à álgebra de ação direita, positividade e cotas exigem δ>0; identidades que envolvem Bε exigem também ε>0. Não se introduziu outra realização de h, raiz ou GNS.

[REAL — produto e ordem] A positividade de qδ vem de Bδ≤δ⁻¹I e multiplicação pelo escalar REAL positivo δ; qδ≤I vem de Bδ≥0. A comutação com Bε é deduzida da comutação dos cortes existentes. A identidade Bεqδ=Bδ−εBδBε usa a identidade resolvente antiga, sem divisão por δ−ε e portanto também vale quando os reguladores coincidem. O helper genérico prova Bq²≤Bq por positividade de (Bq)(1−q), demonstrando a comutação necessária. Depois Bεqδ≤Bδ≤δ⁻¹I. Não há multiplicação de desigualdade por operadores não comutantes; a constante depende somente de δ, uniforme em todo ε>0.

[REAL — convergência forte] No mesmo RegularHilbert(TowerHilbert P), R é regularSpectralResolvent P, S=1−R e Dn=δnBδn, δn=1/(n+1). O código prova Dn S=δn R qδn e ||Dn(Sy)||≤δn||y||. A imagem de S é densa pelo fornecedor antigo bounded_graph_domain_dense, cujo domínio é definicionalmente Ran(S), usando S auto-adjunto e a injetividade de 1−R já entregue. As contrações Dn são uniformemente 1-Lipschitz; Equicontinuous.isClosed_setOf_tendsto estende o limite zero da imagem densa a TODO vetor. Finalmente qδn v=v−Dn v→v. Não se troca ponto a ponto por norma de operadores, nem se assume inversa limitada de S ou gap.

[REAL — auxiliares e reuso] Os quatro helpers privados são hilbert_positive_smul, hilbert_contract_norm, hilbert_positive_product e hilbert_commuting_contract_product, todos em Hilbert complexo genérico completo. Suas premissas de positividade/comutação são explicitamente satisfeitas na especialização; o auditor público cobre seus axiomas transitivos. A norma usa CStarAlgebra.norm_le_norm_of_nonneg_of_le e ContinuousLinearMap.norm_id_le, que não exigem que o espaço seja não trivial. As 14 entradas da ficha e os três recortes do adendo foram confrontados com fontes/linhas/pins; as interfaces futuras de finitude/WOT são somente consumidoras previstas, não resultados deste módulo. Em particular V351ScalarWeightSemifiniteness foi lido/pinado em K para a ficha, mas não está na dependência fechada deste delta nem em V; não foi reproduzido nesta revisão.

[REAL — cronologia e evidência] Ficha 23:03:13 e adendo 23:03:55 antecedem a primeira tentativa 23:05:46. Essa tentativa rc1 foi preservada e excluída: o stream mostra norm_one_le ausente, reescrita de produtos, instância CFC concreta, coerção do subtipo e meta final não resolvida. O DEV final 23:07:09 é rc0 sem avisos. Pins históricos apontam para snapshots reais dos respectivos DEV; o caminho vivo antigo fica apenas como localização textual. O autor standalone e o auditor7 passaram; a sonda BadDomainCutProductReversed inverte ≤ e falha por Type mismatch, com imports válidos. O negativo foi relido/pinado, não reexecutado.

[REAL — proveniência] 688 objetos próprios anteriores preservados; construídos somente alvo e auditor, total 690. Nenhum fornecedor antigo recompilado neste delta; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em 44.423 s; zero avisos do alvo/auditor e 178 mensagens de fornecedores com origem separada no JSON. O stderr preserva ainda o aviso do cache aesop com alterações locais, já presente na base; não é aviso do alvo. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.

| Artefato | SHA256 lido |
|---|---|
| Fonte final (K=cópia própria) | 60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9 |
| .olean próprio | 1e187bbe341f51e03141139fd48dc8d6c974b5aceedf87b2211c3e3616710b02 |
| .olean autoral standalone, apenas comparação | 1e187bbe341f51e03141139fd48dc8d6c974b5aceedf87b2211c3e3616710b02 |

Igualdade binária medida: True.

[OPEN — limites] Delta25 somente: seis teoremas públicos, uma definição, quatro helpers privados transitivos; nenhum fornecedor antigo novo precisou ser construído neste delta. ε>0 e δ>0 nas afirmações de produto; a convergência cobre todo vetor do MESMO Hilbert e a sequência δn=1/(n+1). A cota δ⁻¹ é uniforme em ε, não em δ. Não demonstra norma-operador qδn→I, gap, finitude de (a qδ)*a qδ no peso limite, densidade WOT desse ideal, semifinitude usual ou tracialidade. Esses consumidores permanecem OPEN. O peso/contrato anteriores não são redefinidos, e nenhuma condição do gate ou memória é alterada. O campo autoral sobre ação da raiz é herança do delta CFC aceito, não teorema novo deste arquivo. Objetos próprios anteriores e cache de pacotes reutilizados com pins; nenhum objeto de projeto autoral/DEV usado, nenhum monólito/writer/recorder executado; parecer24 e todos os anteriores intactos.

Artefatos de evidência:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\compilation.json>) — SHA256 97e4c7b0aa9f929c8dff0d904e30bfdf4bbbd6740e01c4b887f2730d4530985e.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\independent_20260914_231000_688102\run.json>) — SHA256 a45c0881f1b3a65b8014347d6d01800168e5f2182b8a711c62d6053d2419e7a6.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\independent_20260914_231000_688102\type_axiom_audit.json>) — SHA256 773a008dbe5af6dbfa24e8c5034668f10390e3826347e34c6ccd6a10066d2269.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\history_read.json>) — SHA256 5d23ef305d210eca4048e95647ffc558642e223d10ad068afe56b7eb98a40a26.
- [fornecedores da ficha](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\provider_checks.json>) — SHA256 90f956066aebb6f1cf6325bd231192bfc0c679549afd81fd4e0a4f7da1c02db5.
