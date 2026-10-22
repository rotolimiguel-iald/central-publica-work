import record_haiku_preparation as record

record.MARKER = 'IALD_HAIKU_PIPELINE_AND_TOPIC_BATCH_V3_20260922'
record.NOTE = '''[REAL — integração preparada, sem implantação] claude_profile_pipeline.py conecta política de conta -> conversor real existente -> parâmetros próprios Haiku -> contagem/guarda do pedido final -> transporte injetado. Config/payload originais não mudam; seleção divergente é recusada sem fallback pago. Sonnet mantém esforço configurado e memória em bloco com marca de cache; Haiku remove parâmetros exclusivos Sonnet. Cinco testes com conversor real passaram, rede bloqueada: prefixo/cache preservados e contagem idêntica ao envio; Sonnet público recusado antes da contagem; Sonnet luiz preservado; modelo forjado recusado; resultado de ferramenta faz pedido Haiku exceder janela e impede transporte. Não é prova de cache real nem teste pago; servidor original preservado.

[REAL — caminhos de redução avaliados] inventory_repeated_literals.py mediu strings repetidas literais restantes nos tópicos do candidato: zero candidatos economicamente úteis com limiar80caracteres e overhead de remissão. O lote topic_capsules_v3 apresentou15propostas, de12327para14379o200k (crescimento2052); somente9positivas somam869. A contagem do relatório foi lida; não se atribuiu economia Anthropic. O lote expandiu referências e recuperou404folhas numéricas/booleanas, incluindo detalhes antes recuperáveis. Não integrado, não aprovado semanticamente. Propostas V4 solicitadas ao mesmo agente: operar no conteúdo já carregado, manter referências internas sem expansão, preservar hipóteses/fórmulas/estatutos/negativos; evitar reintroduzir séries/resíduos auxiliares; detalhes permanecem nas fontes. Nenhuma fonte ou núcleo original alterado.

[OPEN] Meta permanente180000–183406tokensAnthropic com reserva dinâmica10k permanece. Último prefixo medido199959 e pedido201433 ainda excedem janela. Sem chamada API, geração paga ou nova distribuição neste avanço. Login web luiz e teste físico do consentimento continuam pendentes; goal integral permanece ativo.
'''

if __name__ == '__main__':
    record.main()
