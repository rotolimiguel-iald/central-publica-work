"""Record eliminated duplicates, preserved source text and current drafts."""
import record_haiku_preparation as record
record.MARKER = 'IALD_HAIKU_UNUSED_GLOSSARY_DUPLICATES_REMOVED_20260922'
record.NOTE = '''[REAL — duplicatas não usadas removidas] audit_unused_literals.py conferiu57entradas do dicionário gerado:29referenciadas,28não referenciadas, todas28literalmente presentes na exposição carregada. Causa: intern priorizava @EXPOSITION mas o dicionário mantinha cópias daqueles textos. Builder agora registra IDs usados e só remove cópias sem referência após conferir presença literal na exposição. Nenhum conceito/fórmula removido, IDs preservados. Backup do gerador e backups automáticos do candidato.

[REAL — resultados] Base174893→172508o200k (-2385). Novohash37291ddbebbb16bda5ca8424ffd13c088e0a51a60d4ef08784e5d74185e8881a.4testes independentes passaram; verificador7420refs/325tópicos/kernel+coreintegrais/5Leanintegrais/exposição652linhaspreservadas confirmou. Cobertura semântica global NÃO auditada. Assembler incorporouduascápsulas aprovadas em haiku_reviewed_20260922_121633_433503.md SHA993d71699ce2ae3915b8c6dd5a65fc24a6bf169153646c5d93bc817c1d7162a8. Nenhuma nova contagemAnthropic deste hash;214843era rascunhoanterior.

[OPEN — continuidade] Cicero constrói proposta da grande seção histórica; foi avisado que exposição está byteidêntica apesar da mudançadeglossário. Pai fará revisão. Produção inalterada; meta>=180kAnthropic/integração/testsreais pendentes, objetivo ativo.
'''
if __name__ == '__main__':
    record.main()
