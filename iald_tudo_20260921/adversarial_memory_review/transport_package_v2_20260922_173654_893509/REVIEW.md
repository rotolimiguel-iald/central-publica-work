# Reavaliação — quatro achados corrigidos

24 testes fornecidos passaram. SDK Anthropic 1.7.0 com httpx.MockTransport: 429, 500 e timeout produziram exatamente uma tentativa de geração cada, além da contagem sintética. Cliente derivado com retries0; cliente base permaneceu retries2.

Falhas de envio e ValueError/RuntimeError após abertura retornaram502 claude_generation_uncertain, conservaram a decisão e não foram classificadas como recusa sem cobrança pelo adaptador real. Mismatch403 antes do cliente e reserva4096/margem1024 passaram nas regressões.

Aprovação restrita às quatro correções nos hashes de review.json. Sem novos achados reproduzidos nesse escopo. Não aprova rotas stage, autenticação, ledger, produção ou semântica da memória. Sem rede/API; contagens sintéticas.
