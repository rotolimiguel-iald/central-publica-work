from pathlib import Path
import json
import record_haiku_preparation as record
W=Path(__file__).resolve().parent
matches=[]
for p in W.glob('haiku_native_wire_count_*.json'):
    value=json.loads(p.read_bytes())
    if Path(value.get('draft_path','')).name=='haiku_metadata_proposal_20260922_140341_172857.md':matches.append((p,value))
assert len(matches)==1
p,value=matches[0]
b=value['budget']
record.MARKER='IALD_HAIKU_METADATA_NATIVE_COUNT_20260922'
record.NOTE=f'''[REAL — medição gratuita] {p.name}: permanente {b['permanent_tokens']}, pedido com sete ferramentas {b['request_input_tokens']}, saída4096/margem1024; saldo {b['remaining_tokens']}. Duas contagens gratuitas na Anthropic, zero gerações. Modelo {value['model']}. O pedido mínimo cabe, mas ready=true do avaliador significa somente esse pedido; NÃO autoriza declarar conversa pronta: perfil/histórico/resultados faltam. Para reserva dinâmica10k ainda faltam7137tokens de redução. Respeitado mínimo180k. Pacote não implantado.

[REAL — revisão documental] Parecer independente de código source_metadata_code_review_20260922_165920_460112.json aprovou reversibilidade estrutural de132JSONs. Reversão de bytes exige fonte pai preservada, não apenas decoder. verify_metadata_draft.py passou a conferir também linhagem, protocolo exato e região permitida. Revisão integral23paresV5 registrada topic_v5_positive23_20260922_140741_509336.json; alpha_inversion_v2 corrige apenas abreviação da razão de impedâncias. Aprovação documental não é prova física/Lean nem integração. Sete cápsulas sem economia excluídas; fontes originais intactas. Próximo: integrarV5, preservar âncoras e medir; V6 com agente existente. Sonnet pago/cache, visualCentral e exportações físicas ainda pendentes.
'''
if __name__=='__main__':record.main()
