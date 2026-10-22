from pathlib import Path
import json
import record_haiku_preparation as record
from verify_metadata_draft import verify
W=Path(__file__).resolve().parent
name='haiku_metadata_proposal_20260922_141021_331116.md'
checked=verify(W/name)
counts=[(p,json.loads(p.read_bytes()))for p in W.glob('haiku_native_wire_count_*.json')]
matches=[(p,v)for p,v in counts if Path(v.get('draft_path','')).name==name]
assert len(matches)==1
p,v=matches[0];assert v['draft_sha256']==checked['draft_sha256']
b=v['budget']
record.MARKER='IALD_HAIKU_V5_NATIVE_186546_20260922'
record.NOTE=f'''[REAL — integração de bancada] V5 positivo23 integrado sobre V4; alpha_inversionV2 aprovado. Runtime reaplicado e81âncoras verificadas (22literais/59sínteses,3runtime). Metadados compactados depois. Derivado {name}, SHA lido {checked['draft_sha256']}; verificação recursiva recupera pai original e confere revisões/hash. Kernel/Core/exposição fora dos intervalos declarados preservados. Não implantado.

[REAL — Anthropic] {p.name}: permanente{b['permanent_tokens']},pedido{b['request_input_tokens']},saída4096,margem1024,saldo{b['remaining_tokens']}. Duas contagens gratuitas,zero gerações. Redução3997tokens nativos frenteproposta anterior. Ainda faltam3140para reservar10kdinâmicos; ready do avaliador refere-se apenas pedido mínimo, não sessão completa. Perfil/histórico/ferramentas futuras não inclusos. V6 em trabalho com agente existente; solicitada revisão da integraçãoV5. Sonnet pago/cache depende loginluiz; Centralvisual/exportaçõesfísicas pendentes. Nenhuma liberação pública prematura.
'''
if __name__=='__main__':record.main()
