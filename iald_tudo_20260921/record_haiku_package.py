from pathlib import Path
import record_haiku_preparation as record
from claude_memory_package import load_package
W=Path(__file__).resolve().parent
folder=W/'haiku_package_20260922_141841_074636'
p=load_package(folder)
record.MARKER='IALD_HAIKU_MEASURED_PACKAGE_PREPARED_20260922'
record.NOTE=f'''[REAL — pacote preparado, não ativado] {folder.name}/prefix.md + manifest.json guardam prefixo já autorizado/medido, modelo, hash, orçamento e identidade das ferramentas. Loader claude_memory_package.py confere modelo/schema, arquivo fixo sem escape de diretório, hash, orçamento recomputado, reserva>=10k, identidade ferramentas e alteração concorrente. Prefixo={p.measurement.permanent_tokens},dinâmico={p.available_dynamic_tokens},saída{p.reserved_output_tokens}. Seis testes locais passaram: carga,drift,escape,cross-model,orçamento inconsistente,reserva insuficiente. Hash detecta mudança, não substitui permissões do diretório nem aprovação de implantação; contagem por turno continua obrigatória.

[REAL — pontos de integração lidos] iald_web_server.py ainda usa CLAUDE_CFG único, pode_usar_claude ligado a acesso_nativa/lista, _chat_externo e seletor6290aprox. post_como_openai reconverte payload antes de stream; pipeline novo deve evitar dupla conversão que reintroduza parâmetros Sonnet. _max_tokens prioriza max_completion_tokens/max_tokens sobre cfg.max_saida: perfilHaiku precisa estabelecer4k de forma explícita, não herdar16kSonnet. Sem alteração no servidor nesta etapa. Próxima integração deve preservar consentimento por provedor,cotas,stream e ferramentas,Sonnet sóluiz,Haiku para contas aprovadas. RevisãoV6 solicitada ao agente; nenhuma geração paga nem envioAPI neste turno. Objetivo integral ativo.
'''
if __name__=='__main__':record.main()
