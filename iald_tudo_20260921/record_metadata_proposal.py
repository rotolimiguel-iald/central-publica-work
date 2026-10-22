import json
from pathlib import Path
import record_haiku_preparation as record
from verify_metadata_draft import verify
W=Path(__file__).resolve().parent
target=W/'haiku_metadata_proposal_20260922_140341_172857.md'
result=verify(target)
record.MARKER='IALD_HAIKU_LOSSLESS_METADATA_PROPOSAL_20260922'
record.NOTE=f'''[REAL — preparação, não implantação] Criada proposta de compactação reversível de metadados {target.name}. Verificador independente (sem importar o compressor) recuperou os bytes integrais do pai após desfazer 132 linhas JSON e remover o protocolo explicativo. SHA lido: {result['draft_sha256']}. @SOURCE_FIELDS agrupa referências simples; @SOURCE_ITEMS conserva contagens documentais. Não se trata de conteúdo completo carregado nem de contagem de provas. Prefixo protegido, fórmulas e exposição preservados nesta transformação. 14 testes locais passaram, incluindo colisões, nomes inválidos, contagens inválidas e preservação de hipóteses. Revisão independente do agente ainda pendente. Nenhuma chamada API, geração paga ou alteração de produção nesta etapa.

[OPEN] Última contagem Anthropic válida continua sendo a do pai: permanente194168/pedido195642, ainda sem espaço para margem+saída. A nova proposta ainda não foi medida pelo provedor. V5: 23 pares positivos lidos integralmente na sessão; alpha_inversion exige correção da abreviação Zb/Zl(=q), pois a fórmula expressa q=(Zb−Zl)/(Zb+Zl). Solicitada versão derivada corrigida, sem mudar a fonte original. V6 segue com agente existente. Sonnet pago/cache depende de login luiz; Central visual e exportações físicas pendentes. Objetivo permanece ativo.
'''
if __name__=='__main__':record.main()
