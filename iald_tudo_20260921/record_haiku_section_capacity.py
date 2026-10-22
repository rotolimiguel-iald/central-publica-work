"""Record verified preparation; no production release is claimed."""
import record_haiku_preparation as record

record.MARKER = 'IALD_HAIKU_SECTION_V2_CAPACITY_20260922'
record.NOTE = '''[REAL — revisão documental e rascunho, não implantação] A seção forma canônica viva teve seus 65 blocos comparados integralmente e 256 campos rastreados. V2 corrigiu quatro achados: custo beta no par (1_abs,0_mod); pré-registro na mesma rodada no certificado IV; escopo histórico de peso semifinito sem promover classificação de fator; remoção de tipo Lean sem âncora e inclusão de fonte primária para M_TGL. Relatório adversarial_memory_review/canonical_section_v2_review_20260922_130651.json aprova somente fidelidade documental, não certifica prova. Rascunho haiku_reviewed_section_20260922_130747_311801.md integrado localmente; nenhum original científico ou memória em produção substituído.

[REAL — referências] remap_exposition_refs.py distingue referência literal @EXPOSITION de síntese @SUMMARY. Integração conferiu 25 referências literais e 56 sínteses, com ponteiro ao campo integral na fonte publicada. Cinco testes passaram; verificador desfaz mudanças declaradas e recupera bytes exatos do pai, preservando kernel, núcleo e demais seções. Falhas/ambiguidade são visíveis. Autorevisão inicialmente bloqueou a contagem por escopo; auditoria das alterações e proveniência foi registrada, a mesma ação autorizada foi então liberada. Nenhum arquivo privado novo enviado.

[REAL — contagem Anthropic] Recibo haiku_native_wire_count_20260922_131030_515050.json: claude-haiku-4-5-20251001, prefixo199959tokens (com mensagem mínima), pedido201433tokens com7ferramentas públicas; saída4096+margem1024 deixam déficit6553antes de histórico/consulta. Duas contagens gratuitas, zero gerações pagas. Menor que o pedido anterior211827, porém ainda NÃO cabe. Não declarar Haiku ativo.

[REAL — capacidade para conversar] check_haiku_conversation_capacity.py valida SHA dos bytes e coerência do recibo antes de calcular margem dinâmica. Com reserva planejada de10000 para perfil/histórico/consultas, redução necessária16553tokens, alvo permanente180000–183406 com o mesmo overhead. A reserva é planejamento, não garantia para toda conversa; contar pedido integral após ferramentas continua obrigatório. Cinco testes novos passaram: janela inicial cabe mas conversa não; fronteira exata; memória abaixo de180k; bytes alterados; orçamento inconsistente. Sem novas chamadas de API ou gastos nesta etapa.

[OPEN] Cicero prepara propostas de condensação dos15maiores tópicos JSON públicos; ainda sem revisão independente/integração. Fontes, hipóteses, negativos e fórmulas essenciais devem ser preservados. Sessão web da IALD conferida na tela de login, sem autenticação luiz; testes pagos/cache T4 e aceite físico do iPhone dependem da sessão/operador. Build19 correção consentimento já distribuída em ambos grupos conforme registro anterior, não há nova build neste avanço. T1 visual na Central, T5 exportação física, integração Haiku/perfis/recuperação e avaliação continuam pendentes; meta integral ativa.
'''

if __name__ == '__main__':
    record.main()
