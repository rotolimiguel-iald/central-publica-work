
## Adendo de integração — leitor V2 e P2-READERS-01

[REAL — correção em cópia; revisão independente específica anexa] O candidato ativo é **`PROPOSTA_LEITORES_EXISTENTES_V2.py`**, com `PROPOSTA_MAPA_CONSUMIDORES_V2.json` e diff V2. As referências ao mapa sem sufixo no corpo acima descrevem a primeira proposta, que permanece preservada como histórico. Mapas, termos Lean, cinco verificações de tipo e os dois ajustes false-only são iguais em V1 e V2.

Carver encontrou uma falha herdada no leitor canônico: `audit_returncode == 0` também aceita `False`, pois `bool` é subclasse de `int` em Python. A V2 exige `type(audit_returncode) is int` antes da igualdade. Essa é a única alteração de lógica entre V1 e V2. Código de saída 0 inteiro continua válido; bool, string, float e None são recusados. Os códigos dos builds Lean desta entrega já eram inteiros.

`TESTES_LEITORES_COPIADOS_V2.json` registra 66 verificações autorais aprovadas, incluindo as cinco adulterações de tipo adicionais. Isso não é uma rodada canônica. O parecer independente do leitor distingue a aprovação da matemática, já encerrada, da correção desse limite de metadados. A V1 não deve ser integrada no lugar da V2.
