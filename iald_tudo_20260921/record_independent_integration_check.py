"""Record actual whole-draft transformation fidelity verification."""
import record_haiku_preparation as record
record.MARKER = 'IALD_HAIKU_INDEPENDENT_INTEGRATION_BYTES_20260922'
record.NOTE = '''[REAL — verificador independente de integração] verify_reviewed_draft.py não importa builder/assembler. Conferiu o rascunho7aff110dc513df5b8639b530473d034f26e28e85c315693a03d7ae19bc63a4b4, seuspareceres/cápsulas/fontes e desfez apenas transformações declaradas:duascápsulas aprovadas e indentação do JSON de evidências. Reconstruiu byte a byte a base37291ddbebbb16bda5ca8424ffd13c088e0a51a60d4ef08784e5d74185e8881a. Demais bytes preservados; fonte pública confere com manifesto. Recibo reviewed_draft_verification_*.json. Isso verifica integração, não cobertura semântica global, compilaçãoLean ou encaixeAnthropic.

[OPEN — tarefa em andamento] Consulta ao handleCicero retornou timeout10s e não estado terminal. Proposta da seção histórica em construção; não reiniciada, não aprovada, não implantada. A base atual do app permanece intacta; nenhuma chamada paga ou nova requisiçãoAPI. Meta180k/integração/testes reais seguem incompletos; objetivo integral ativo.
'''
if __name__ == '__main__':
    record.main()
