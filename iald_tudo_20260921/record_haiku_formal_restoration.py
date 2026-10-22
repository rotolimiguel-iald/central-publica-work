"""Record correction of the missing nuclear Lean sources in the draft."""
import record_haiku_preparation as record
record.MARKER = 'IALD_HAIKU_NUCLEAR_LEAN_RESTORED_20260922'
record.NOTE = '''[REAL — auditoria de completude] audit_haiku_formal_coverage.py comparou o rascunho com published_evidence do servidor. O candidato antes medido184555 NÃO continha as cinco fontes Lean nucleares de H1/H2/H3; nem todos os nomes qualificados das declarações estavam presentes. Assim a medição de186033 com ferramentas e saldo8847 provava tamanho daquela composição incompleta, não um perfil suficiente para implantação. Corrigida a interpretação anterior, sem apagar a evidência histórica.

[REAL — restauração] build_haiku_candidate.py agora incorpora published_evidence após conferir catálogo, programa/selo/JSON/relatório e fontes. V354RegularSusy, ConcreteFourFrame, TheMasterFires, TriadMaster e TheImportedEquilibrium entram integrais com seus escopos e metadados. Auditoria refeita: cinco fontes completas e todos os termos qualificados selecionados presentes. Compilador NÃO executado. Esse bloco soma16458 tokens o200k, que não é contagem Haiku.

[REAL — nova contagem oficial] Candidato corrigido:204859 tokens Haiku com mensagem mínima, baseline9; haiku_count.json vincula SHA atualizado. Está ACIMA da janela200k e da meta180k. NÃO ATIVAR. Recibo de requisição com ferramentas anterior agora tem outro hash; count_haiku_app_request.py verifica essa identidade e recusa medição reaproveitada. Nenhuma geração paga nem implantação.

[REAL — testes reforçados] verify_haiku_candidate.py agora exige todas as cinco fontes formais completas, além do kernel v5/Memory Core integrais, equivalência das cápsulas,7321 referências e652 linhas da exposição preservadas fora dos metadados permitidos. Passou; cobertura semântica geral permanece aberta. O sucesso não certifica prova nem orçamento.

[OPEN] Reorganizar detalhes acessórios para acomodar o bloco formal obrigatório com alvo mínimo180k e requisição completa dentro200k. Extensão pointer continua aguardando autorização específica exigida por auto-review; não executada. Integração dos perfis/recuperação, Sonnet testes pagos/cache, T5 iOS18/Android17 e testes físicos continuam pendentes. Objetivo integral não concluído.
'''
if __name__ == '__main__':
    record.main()
