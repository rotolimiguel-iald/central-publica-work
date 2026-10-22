

## 16/10/2026 — Capacidade do repasse pelo MCP

O MCP `iald_mission_handoff` aceita `max_chars`, assim como a sincronização. Passe a mesma capacidade explícita às duas operações (por exemplo, 100000 para a missão atual). O padrão continua 24000 para compatibilidade. Capacidade insuficiente ou inválida provoca recusa sem truncamento; recupere a revisão e a projeção atuais antes de tentar novamente. A capacidade maior não exige imprimir o pacote inteiro na saída do coordenador: conserve o recibo completo e apresente apenas o resumo pertinente. Processos antigos precisam de recarga; o CLI absoluto funciona imediatamente. Esta correção não reinicia processos existentes nem altera a missão científica.
