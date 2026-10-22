"""Record measured draft preservation and outstanding semantic review."""
import record_haiku_preparation as record

record.MARKER = 'IALD_HAIKU_WITNESS_LAYERS_REPAIR_20260922'
record.NOTE = '''[REAL — correção do rascunho, não implantada] O candidato mantinha frases históricas negativas de interface_is_light mas remetia witness_layers à consulta. O gerador agora preserva integralmente /core/interface_is_light/witness_layers e /light_chain, inclusive flags positivas de construção e canonical_full_witness_term_constructed=false. Estatutos e escopos da fonte permanecem; flags não substituem auditoria Lean. Fonte original intocada. Builder e teste receberam backups imediatos em bytes.

[REAL — validação] 4 testes independentes source-contract passaram; verificador confirmou 325 tópicos, kernel e núcleo integrais, 5 fontes Lean nucleares completas, 7420 referências. Candidato SHA 83870f5abbea7f74ce13dca097a35a5f6590e067ef19d06f4725ee8652f47c92, 174893 o200k. Não é contagem Anthropic; pacote continua DRAFT_NOT_DEPLOYED. Cobertura semântica global ainda não auditada.

[OPEN — revisão semântica] Cicero solicitou correções na cápsula contour_theory: ponto fixo/saturação GKLS e taxas q/alpha, relações do canal neutrínico, inconsistência herdada alpha=sin²(theta)/sqrt(e) em 90°, caminhos inequívocos. Não integrada. Criada também interface_is_light.md, proposta ainda não medida/revisada/integrada. Meta do operador permanece >=180000 tokens Anthropic de memória essencial com kernel, dentro do orçamento total do pedido. Não anunciar ativação Haiku antes de contagem e integração. Sonnet testes autenticados, teste físico mobile e autorização específica JSONpointer continuam pendentes; iOS18 nos dois grupos já concluído conforme registro anterior.
'''

if __name__ == '__main__':
    record.main()
