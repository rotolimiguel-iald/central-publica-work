from review import *

identity=dict(name='Carver',agent_id='01a0a5b5-e12d-70c1-a68a-c6f13373e3c0',
    convened_by='agente principal, no escopo autorizado',
    provenance='INPUT — identidade explicitamente fornecida pelo agente principal na mensagem desta sessão',
    role='revisor adversarial independente; não autor Poincare; não se atribui nova revisão ou aprovação a outro usuário',
    amendment_utc=stamp())
label='Carver — agent_id 01a0a5b5-e12d-70c1-a68a-c6f13373e3c0, convocado pelo agente principal no escopo autorizado; não autor Poincare'
record(ROOT/'IDENTIDADE_REVISOR.json',identity)
for name in ['SEMANTICA_REVISOR.json','AUDITORIA_INDEPENDENTE.json']:
    p=ROOT/name; data=json.loads(p.read_text(encoding='utf-8'))
    data['previous_reviewer_label']=data['reviewer']
    data['reviewer']=label; data['reviewer_identity']=identity
    record(p,data)
p=ROOT/'REVISAO_B1_PRIME.md'
addendum='\n\n## Adendo cadastral — identidade exata do revisor\n\n'
addendum+=f'Data UTC: {identity["amendment_utc"]}. **{label}.**\n\n'
addendum+='[INPUT — identificação fornecida pelo agente principal] Esta identificação corrige ao lado a expressão anterior “convocado pelo operador”. '
addendum+='A revisão foi feita por este agente no escopo autorizado; não se atribui checagem nem aprovação independente a outro usuário. '
addendum+='A concordância comunicada pelo agente principal não conta como segunda auditoria. O conteúdo técnico, os logs aceitos e a decisão B1′ permanecem os mesmos. '
addendum+='O recibo B1′ foi fechado e seu primeiro selo verificado antes de iniciar A2; esta é uma correção cadastral posterior.\n\n'
addendum+='IDENTIDADE_REVISOR.json e AUDITORIA_INDEPENDENTE.json registram o nome e agent_id em campos de máquina. '
addendum+='Os hashes na tabela anterior retratam a primeira emissão; os hashes correntes estão no manifesto e selo novos, com os originais em backups de bytes.\n'
write(p,p.read_bytes()+addendum.encode('utf-8'))
files=[info(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name not in ['MANIFESTO_REVISAO.json','SELO_REVISAO.json']]
record(ROOT/'MANIFESTO_REVISAO.json',dict(created_utc=stamp(),root=str(ROOT),files=files,count=len(files),
    amendment='Identidade exata do revisor; conteúdo técnico inalterado',excludes=['MANIFESTO_REVISAO.json','SELO_REVISAO.json']))
record(ROOT/'SELO_REVISAO.json',dict(created_utc=stamp(),decision=json.loads((ROOT/'AUDITORIA_INDEPENDENTE.json').read_text(encoding='utf-8'))['decision'],
    reviewer_identity=identity,files=[info(ROOT/n) for n in ['MANIFESTO_REVISAO.json','REVISAO_B1_PRIME.md','AUDITORIA_INDEPENDENTE.json','IDENTIDADE_REVISOR.json']]))
print(json.dumps(dict(identity=identity,report=info(ROOT/'REVISAO_B1_PRIME.md')),ensure_ascii=False,indent=2))
