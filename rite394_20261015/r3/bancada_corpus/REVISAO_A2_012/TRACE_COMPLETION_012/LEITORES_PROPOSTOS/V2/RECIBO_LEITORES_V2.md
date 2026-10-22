# Adendo independente — leitores V2 ativos

**[REAL — delta verificado] VERIFICADO_V2_ATIVA_P2_READERS_01_CORRIGIDO. P0=0; P1=0; P2=0 em aberto no escopo copiado.**

Carver, agent_id `01a0a5b5-e12d-70c1-a68a-c6f13373e3c0`, revisor independente e não autor; identidade fornecida pela principal [INPUT]. Este adendo torna V2 a proposta ativa para este recibo, sem integrar o canônico.

**P2-READERS-01: herdado no snapshot/V1 e corrigido na V2.** A comparação de bytes demonstra que a única alteração executável foi inserir `and type(kf.get("audit_returncode")) is int` imediatamente antes da comparação com zero. Os mapas de contratos, consumidores, escopos e a exigência dos cinco casts permanecem idênticos. Não foi acrescentada função Python ou alias Lean. A proposta V1 e todos os artefatos do seu manifesto continuam com bytes e hashes anteriores; o achado histórico não foi apagado ou reclassificado retrospectivamente.

Foram registradas 28 verificações próprias do delta, incluindo onze casos de rc nas duas vias existentes (build completo e incremental com hashes verificados). O inteiro `0` é aceito. Inteiros `1` e `-1`, booleanos `False` e `True`, strings `"0"` e `"1"`, floats `0.0` e `1.0`, `None` e campo ausente são recusados. Os dados positivos usam o axiom report real de sessenta nomes da revisão independente paga. Com rc inteiro zero, todos os resultados da V1 se preservam. Com rc booleano falso, a sonda reproduz a aceitação antiga na V1, confirma a recusa na V2 e verifica a rejeição de flags obsoletas pelos consumidores do helper.

O mapa V2 e seu diff conferem com os bytes medidos; o diff autoral é contra o snapshot, enquanto [DELTA_V1_V2.diff](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/TRACE_COMPLETION_012/LEITORES_PROPOSTOS/V2/DELTA_V1_V2.diff>) isola a linha entre V1 e V2. O relatório autoral informa 66 checks e foi lido, sem execução ou inclusão na contagem própria. Resultados detalhados: [TESTES_DELTA_V2.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/TRACE_COMPLETION_012/LEITORES_PROPOSTOS/V2/TESTES_DELTA_V2.json>). Leituras, hashes e bytes: [LEITURAS_DELTA_V2.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/TRACE_COMPLETION_012/LEITORES_PROPOSTOS/V2/LEITURAS_DELTA_V2.json>).

**Nenhuma execução Lean ou canônica nesta revisão de delta.** Os cinco casts e as recusas de True já pagos permanecem válidos no escopo anterior. Continua sendo requisito de integração inserir esses casts no Audit canônico realmente executado, conservar a proveniência/hashes e manter H1 restrito ao representante mínimo. Os limites físicos, H2/H3, BW, transformação limitada padrão, adendo inteiro e gate não foram ampliados. A negativa anterior de acesso ao original não foi repetida; a proveniência canônica continua [DECLARADO — captura AST autoral], com as cópias verificadas independentemente.

Histórico preservado: [PARECER_LEITORES.md](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/TRACE_COMPLETION_012/LEITORES_PROPOSTOS/PARECER_LEITORES.md>) e [SELO_LEITORES.json](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_A2_012/TRACE_COMPLETION_012/LEITORES_PROPOSTOS/SELO_LEITORES.json>). Proposta ativa: [PROPOSTA_LEITORES_EXISTENTES_V2.py](<C:/IALD/Central de Patentes/Chatgpt/A2_TRACE_COMPLETION_012/PROPOSTA_LEITORES_EXISTENTES_V2.py>); mapa ativo: [PROPOSTA_MAPA_CONSUMIDORES_V2.json](<C:/IALD/Central de Patentes/Chatgpt/A2_TRACE_COMPLETION_012/PROPOSTA_MAPA_CONSUMIDORES_V2.json>).

| Entrada V2 lida integralmente | Bytes | SHA-256 |
|---|---:|---|
| [PROPOSTA_LEITORES_EXISTENTES_V2.py](<C:/IALD/Central de Patentes/Chatgpt/A2_TRACE_COMPLETION_012/PROPOSTA_LEITORES_EXISTENTES_V2.py>) | 5811 | `70db8370e0ca8ebb95d352de837bd870cf26745643608d6aa91851b67d5bbcfb` |
| [PROPOSTA_LEITORES_EXISTENTES_V2.diff](<C:/IALD/Central de Patentes/Chatgpt/A2_TRACE_COMPLETION_012/PROPOSTA_LEITORES_EXISTENTES_V2.diff>) | 7635 | `e3860f89fd84fb20064f0e9de6675bf368087fa6cd493e133f7301e4bcfc01f8` |
| [PROPOSTA_MAPA_CONSUMIDORES_V2.json](<C:/IALD/Central de Patentes/Chatgpt/A2_TRACE_COMPLETION_012/PROPOSTA_MAPA_CONSUMIDORES_V2.json>) | 3530 | `0763849f53694bcce28fb610368c7c8abbc5456762b5ebfe0c4e843dbd7043eb` |
| [TESTES_LEITORES_COPIADOS_V2.json](<C:/IALD/Central de Patentes/Chatgpt/A2_TRACE_COMPLETION_012/TESTES_LEITORES_COPIADOS_V2.json>) | 9450 | `24bda0318a15b4b4f24ebd764794fe6f1bd058a62e0361b93fbfb0e4e1a23706` |
