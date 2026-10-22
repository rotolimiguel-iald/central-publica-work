"""Record a candidate within the window, not an activated or validated release."""
import record_haiku_preparation as record
record.MARKER = 'IALD_HAIKU_184555_CANDIDATE_20260922'
record.NOTE = '''[REAL — candidato, não implantação] Contagem oficial Haiku4.5 do novo candidato com mensagem mínima:184555 tokens; linha de base9; haiku_count.json vincula o SHA da versão medida. Esse valor supera o mínimo de180k desejado pelo operador e cabe sozinho na janela200k, mas ainda não inclui o orçamento operacional de ferramentas/histórico/saída. Não declarar requisição completa validada. Não houve geração paga.

[REAL — alteração de seleção] A lista individual de indicadores da escada auditada passou para recuperação no documento público um_forma_canonica_integral, por offset já suportado por fetch_tgl. Fonte conferida por hash e cada linha localizada literalmente; intervalos em haiku_candidate.json. Cabeçalho/estado geral preservado. Cabeçalhos com vereditos repetidos agora remetem ao tópico cujo valor foi conferido igual. Todos325 tópicos, kernel v5 e Memory Core permanecem carregados. Isso não omite a instrução-mãe nem reescreve fórmulas. exposition_full=false por transparência: metadados individuais da auditoria foram deslocados.

[REAL — verificação] verify_haiku_candidate.py conferiu7321 referências, equivalência dos valores das cápsulas após compactação, presença integral do kernel/core e652 linhas não vazias da exposição preservadas fora dos metadados listados. Recuperou os extremos da lista de auditoria usando a função fetch atual. Regex de blocos $$/\\[ encontrou0, portanto não é evidência autônoma de cobertura; a verificação linha a linha cobre a preservação do texto independentemente de delimitador. Cobertura semântica da seleção inicial continua pendente.

[OPEN — aprovação pontual] Preparação de extensão pointer em iald_core_indexado.py foi rejeitada pela revisão automática por exigir autorização específica de mudança coordenada. Pergunta pendente. Não executada nem contornada; testes propostos da extensão não rodaram. Consulta por offset existente foi usada somente como leitura normal, sem modificar a ferramenta bloqueada.

[OPEN] Antes de ativar Haiku: medir requisição com ferramentas/saída, revisar semanticamente fórmulas/hipóteses/versão, integrar perfis e recuperação automática, validar acesso público versus Sonnet interno e custos reais. Sonnet testes/cache e T5 builds18/17/exportação física continuam pendentes. Não declarar Haiku disponível, nova build enviada ou objetivo completo.
'''
if __name__ == '__main__':
    record.main()
