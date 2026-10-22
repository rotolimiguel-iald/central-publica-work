"""Persist the explicit minimum-memory admission requirement and regression checks."""
import record_haiku_preparation as record

record.MARKER = 'IALD_HAIKU_MINIMUM_MEMORY_ADMISSION_20260922'
record.NOTE = '''[REAL — módulo preparado corrigido] claude_profiles.py antes retornava action=send para contexto que coubesse, mesmo quando memory_target_met=false. Isso contrariava o pedido explícito do operador de pelo menos180000tokensHaiku de memória fixa. Agora ready exige caber E atingir a meta; memória insuficiente retorna load_required_memory_then_recount. Não preencher com texto inútil para passar esse gate: cobertura essencial continua requisito separado. Fits segue significando somente caber na janela, sem confundir com prontidão.

[REAL — testes] test_claude_profiles.py:7testes passaram. Novos casos recusam memórias0,100000,179999mesmo com espaço livre;180000válido é admitido se sobra orçamento; Sonnet mantém regra separada sem impor mínimoHaiku. Arquivos receberam backup de bytes antes das mudanças. Módulo NÃO integrado ao servidor; nenhuma alteração de produção ou chamada paga nesta etapa.

[OPEN] Revisão adversarial Cicero agent01a0c97e-fb7b-7510-8d5d-1ec2bbea845e segue sem resultado final; wait10s expirou, não terminal. Tem scripts/medições intermediárias somente na subpasta autorizada adversarial_memory_review; não duplicar trabalho. Pacote atual220651tokensAnthropic ainda excede200k e necessita compactação com semântica preservada. Loginluiz e testesSonnet/cache pendentes. Pergunta assíncrona de testes físicos iPhone/iPad enviada após liberar build18nos doisgrupos; aguardar resultado, não afirmar exportação funcional por inferência. Objetivo integral permanece ativo.
'''

if __name__ == '__main__':
    record.main()
