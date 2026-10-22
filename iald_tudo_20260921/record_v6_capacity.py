from pathlib import Path
import json
import record_haiku_preparation as record
from verify_metadata_draft import verify
from check_haiku_conversation_capacity import assess
W=Path(__file__).resolve().parent
name='haiku_metadata_proposal_20260922_141555_464161.md'
checked=verify(W/name)
counts=[(p,json.loads(p.read_bytes()))for p in W.glob('haiku_native_wire_count_*.json')]
matches=[(p,v)for p,v in counts if Path(v.get('draft_path','')).name==name]
assert len(matches)==1
p,v=matches[0];assert v['draft_sha256']==checked['draft_sha256']
capacity=assess(v);assert capacity['capacity_ready']
out=W/'haiku_v6_capacity_20260922.json'
with out.open('x',encoding='utf-8')as f:json.dump(capacity,f,ensure_ascii=False,indent=2)
record.MARKER='IALD_HAIKU_V6_CAPACITY_MET_20260922'
record.NOTE=f'''[REAL — capacidade planejada atingida, NÃO produção] V6: todos38pares menores lidos integralmente pelo pai;reading_directionV2 restaura razão/consciência [ONTO] onde V1 trocara por coerência.37aprovados+correção=38,parecer topic_v6_all38_20260922_141529_232866.json. Integrados sobreV5/V4, runtime e compactmetadata depois. {name},SHA lido {checked['draft_sha256']}. Verificação recursiva passou; fonte original intacta. Revisão independente da integraçãoV5+runtime aprovada em v5_runtime_integration_20260922_171238_948761.json; revisão novaV6 pedida ao agente existente. Não criar novas cápsulas: alvo atingido.

[REAL — contagem API gratuita] {p.name}: permanente183135,request184609,output4096,margem1024,reserva10271. Mínimo180k e reserva planejada10k satisfeitos; redução3411nativos frenteV5. haiku_v6_capacity_20260922.json conferido. Duas contagens/zero gerações. Perfil,histórico,resultados ainda precisam contagem completa por turno. Capacity_ready não é implantação nem avaliação de respostas.

[OPEN — próximo] Revisão final integração/metadados, certificado de memória e ligação do pipeline ao servidor/contas/consentimento/cotas; Haiku público e Sonnet somente luiz preservados. Não enviado binário nem reiniciado servidor por esta etapa. Sonnet2mensagens/cache ainda precisa loginluiz; Centralvisual/exportaçõesfísicas pendentes. Objetivo integral ativo.
'''
if __name__=='__main__':record.main()
