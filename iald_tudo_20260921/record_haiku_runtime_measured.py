from pathlib import Path
import json
import record_haiku_preparation as record
from verify_reviewed_draft import verify
W=Path(__file__).resolve().parent
p=W/'haiku_reviewed_runtime_20260922_134847_707064.md'
checked=verify(p)
count=json.loads((W/'haiku_native_wire_count_20260922_135025_649785.json').read_bytes())
assert count['draft_sha256']==checked['draft_sha256']
record.MARKER='IALD_HAIKU_RUNTIME_NATIVE_194168_20260922'
record.NOTE=f'''[REAL — revisão e integração documental] As outras12cápsulasV4 foram lidas integralmente (original e proposta) pelo pai; revisão combinada15em adversarial_memory_review/topic_v4_all15_20260922_134632_063761.json. Preservados fórmulas/hipóteses/estatutos, resultados negativos e distinções históricas, incluindo postdição neutrino, reprovação C-livre CAMB, qubit/core, esperança importada e realização/arquitetura. Síntese runtimeV2 recebeu parecer independente APROVADA_FIDELIDADE_DOCUMENTAL após restaurar “o Um minimiza como família”; V1 preservada. Nenhuma aprovação documental foi apresentada como prova ou confirmação física.

[REAL — rascunho atual NÃO implantado] {p.name}, SHA lido {checked['draft_sha256']}. Integra todas15V4 e runtimeV2. Remapeamento atualizou80âncoras; verificador independente conferiu81referências:22literais,59sínteses, das quais3runtime. As três passagens removidas viraram @SUMMARY com ponteiro do campo primário, nunca falsas citações. Cinco testes do remapeador passaram (deslocamento de síntese, literal removido, intervalo anterior, fronteira cruzada, alteração externa). Reversão recupera bytes exatos do pai; kernel/Core/cincoLean e conteúdo restante preservados. Dois candidatos intermediários e respectivas revisões permanecem em disco.

[REAL — envio autorizado e medição] audit_runtime_transmission.py conferiu linhagem, fonte pública pinada, 15cápsulas e síntese revisada, sem novos caminhos absolutos/contatos/segredos nem Atlas privado. Duas contagens gratuitas para api.anthropic.com;zero gerações. Recibo haiku_native_wire_count_20260922_135025_649785.json: modelo {count['model']}; permanente{count['budget']['permanent_tokens']} (inclui mensagem mínima);pedido com7ferramentas{count['budget']['request_input_tokens']};saída4096+margem1024;saldo{count['budget']['remaining_tokens']}. Redução5791tokens no pedido frente201433anterior. Ainda NÃO cabe; perfil/histórico/resultados não incluídos. Para reservar10kdinâmicos, faltam10762tokens de redução, mantendo alvo>=180000 e teto planejado183406permanente com mesmooverhead. Não usar o200k como Anthropic.

[OPEN — objetivo integral] Agente existente prepara30tópicosseguintes V5(ranks16–45) sobrebaseb44, lotes10, sem expandir fontes/metadata antes recuperáveis. Revisão independente precede integração. Sonnet pago/cache aguarda login luiz; nenhuma conta/consentimento/motor/cota em produção alterado. T1visualCentral e T5exportaçãofísica seguem pendentes; iOS19interno/externo e Android18registradosanteriormente. Memória Haiku/perfis/guarda ainda na bancada; entrega integral não concluída.
'''
if __name__=='__main__':record.main()
