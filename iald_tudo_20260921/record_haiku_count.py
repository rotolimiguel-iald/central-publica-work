"""Record first Haiku measurement without claiming a deployable package."""
import record_haiku_preparation as record
record.MARKER = 'IALD_HAIKU_FIRST_MEASURED_CANDIDATE_20260922'
record.NOTE = '''[REAL — preparação, não implantação] Criado build_haiku_candidate.py, derivado do JSON público fixado no manifesto v368, com325 tópicos, kernel v5, Memory Core e exposição canônica integrais. Arquivos originais intactos; rascunhos e recibos anteriores têm backups imediatos. Coleções/relatórios extensos possuem ponteiros JSON exatos. O primeiro extrato do JSON completo ficou maior que o cluster anterior; refinado para remissões de detalhes e indicadores individuais de auditoria. Isto não ratifica novos conceitos.

[REAL — medição oficial] count_haiku_candidate.py fez somente duas contagens gratuitas em api.anthropic.com, modelo claude-haiku-4-5-20251001: linha de base9 e candidato231679 tokens, com mensagem mínima. Recibo haiku_count.json vincula SHA lido ao candidato. A contagem o200k local do mesmo texto é183748; não equivale a180k Haiku. CANDIDATO NÃO CABE na janela200k e NÃO FOI IMPLANTADO. Nenhuma geração paga, alteração de credencial ou conta. Conteúdo transmitido: kernel/core já autorizados e fontes públicas, sem Atlas privado.

[REAL — verificação estrutural] verify_haiku_candidate.py resolve todos os ponteiros gerados contra o JSON original, confere hashes, presença integral do kernel/core e unicidade dos325 tópicos. Essa verificação não certifica cobertura semântica nem prova matemática. A exposição preserva a história; protocolos de identidade/solução acompanham o rascunho.

[OPEN — próximo passo] Reduzir cerca de52k tokens Haiku de detalhes acessórios, mantendo núcleo/fórmulas e cápsulas de todos os tópicos; contar novamente até atingir a meta180k com orçamento da requisição completa. Revisar semanticamente antes de instalar. Implementação de perfis, recuperação automática, testes pagos autorizados, Sonnet interno e distribuição iOS18/Android17 ainda pendentes. Não anunciar ativação ou entrega integral.
'''
if __name__ == '__main__':
    record.main()
