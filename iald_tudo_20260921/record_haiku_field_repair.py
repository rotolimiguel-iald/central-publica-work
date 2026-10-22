"""Record measured extraction defects and their repair, without claiming deployment."""
import record_haiku_preparation as record

record.MARKER = 'IALD_HAIKU_ESSENTIAL_FIELD_REPAIR_20260922'
record.NOTE = '''[REAL — auditoria e correção do rascunho] audit_haiku_density.py mediu o candidato anterior: repetição literal de linhas economizaria apenas 960 tokens o200k brutos; não resolve a janela. audit_haiku_essential_fields.py comparou 656 campos textuais selecionados por nome de fórmula/enunciado/escopo/estatuto com o candidato e encontrou 92 ausências literais. A seleção anterior protegia principalmente nomes ingleses e omitia campos de listas detalhadas.

[REAL — código de preparação corrigido, app inalterado] build_haiku_candidate.py recebeu proteção de nomes portugueses (equação, hipótese, premissa, escopo, estatuto, veredito, teorema, comutação) e dos campos essenciais dentro de listas. Backup de bytes antes da mudança; candidato e recibo regenerados com backups imediatos. A auditoria nova encontrou 32 ausências, TODAS caminhos de hashes em /core/kernel_formalization/formal_files_sha256, catálogo explicitamente recuperável. Os 60 campos textuais restantes passaram a estar presentes literalmente. Isto é cobertura lexical desta seleção, não certificação de compreensão ou cobertura semântica completa.

[REAL — verificação] verify_haiku_candidate.py passou: 7321 referências, 325 tópicos, kernel-mãe e núcleo completos, cinco fontes Lean nucleares completas, valores compactados equivalentes, 652 linhas de exposição preservadas exceto metadados declarados. Nenhuma prova Lean reexecutada. O número zero do detector display_math é limitação desse detector; não equivale a ausência de fórmulas.

[OPEN — orçamento e implantação] Novo candidato tem 178804 tokens o200k, NÃO tokens Anthropic. SHA e fontes estão nos recibos haiku_candidate.json e haiku_essential_fields_*.json. A medição Anthropic de204859 pertence ao candidato anterior e NÃO se aplica ao atual. Nenhuma nova contagem remota ou geração paga nesta etapa. Ainda necessário compactar conteúdo acessório com cobertura, medir no Haiku e integrar/admitir o orçamento completo. Não anunciar180k instalado. fetch_tgl.pointer continua sem execução, aguardando autorização específica após rejeição automática. Sonnet/cache, iOS18 e testes físicos seguem pendentes; Android17 já compilado permanece conforme recibo anterior. Nenhum servidor reiniciado ou arquivo de produção alterado nesta etapa.
'''

if __name__ == '__main__':
    record.main()
