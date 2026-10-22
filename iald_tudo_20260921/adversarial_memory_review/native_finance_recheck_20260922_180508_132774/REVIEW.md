# Reavaliação N1–N3

Correções verificadas no escopo unitário; sem achados remanescentes reproduzidos nesses três casos.

N1: falha antes da gravação na primeira ou segunda linha permite retomada, sem duplicar linhas já concluídas; closed só após sucesso. N2: chamada pendente é liquidada pelo hold e impede segunda contagem/reserva nessa tentativa. N3: disponibilidade usa entrada/leitura/saída/escrita efetivas e recusa tarifas inválidas.

6 testes focais independentes passaram. Política pública sem orçamento explícito permanece desligada. Wrapper defer não reserva antes da chamada final, em teste isolado.

Não reexecutados os18 testes do pai que importam ROOT. Cursor em memória não certifica exactly-once após falha ambígua posterior ao commit/process crash. Integração do stage/S3/S4 aguarda versão final; JS/app não inspecionados. Sem alteração de produção, API ou ativação. Hashes em review.json.
