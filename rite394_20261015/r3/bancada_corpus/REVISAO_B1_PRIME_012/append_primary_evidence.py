from review import *

primary=ROOT.parent/'TETELESTAI_V351_FECHO_MATEMATICO'/'A2_012'/'primary'
provenance=json.loads((primary/'PROVENIENCIA_ARTIGO_A.json').read_text(encoding='utf-8'))
source_info=info(primary/'ARTIGO_A_EXCERTOS.md')
assert source_info==provenance['excerpt']
copies=[]
for name in ['ARTIGO_A_EXCERTOS.md','PROVENIENCIA_ARTIGO_A.json']:
    p=primary/name; q=ROOT/'inputs'/'primary'/name
    write(q,p.read_bytes()); copies.append(dict(source=info(p),copy=info(q)))
recording=dict(status='REAL_EXCERTOS_PRIMARIOS_LIDOS_COM_PROVENIENCIA_DA_PRINCIPAL',
    reviewer='Carver',agent_id='01a0a5b5-e12d-70c1-a68a-c6f13373e3c0',time_utc=stamp(),files=copies,
    original_metadata_as_recorded_by_principal=provenance['source'],
    original_rehashed_by_this_reviewer=False,direct_original_access_by_this_reviewer=False,
    primary_extraction_by='agente principal, leitura autorizada somente de trechos/contexto, conforme proveniência',
    ranges=provenance['ranges'],variational_derivation_verified=False,Lean_rerun=False,
    conclusion='EOM e posições distintas de xi e beta confirmadas nos excertos; B1 permanece condicional a hEOM')
record(ROOT/'ADENDO_FONTE_PRIMARIA.json',recording)
p=ROOT/'AUDITORIA_INDEPENDENTE.json'; audit=json.loads(p.read_text(encoding='utf-8'))
audit['article_A_historical_access']=audit['article_A']
audit['article_A']=recording
record(p,audit)
p=ROOT/'PRIMARY_ACCESS.json'; access=json.loads(p.read_text(encoding='utf-8'))
access['subsequent_primary_excerpt_consultation']=recording
record(p,access)
p=ROOT/'SEMANTICA_REVISOR.json'; semantic=json.loads(p.read_text(encoding='utf-8'))
semantic['primary_evidence_addendum']=recording
record(p,semantic)
excerpt=copies[0]['copy']; provenance_copy=copies[1]['copy']
addition='\n\n## Adendo documental — consulta aos excertos primários do Artigo A\n\n'
addition+=f'Data UTC: {recording["time_utc"]}. [REAL — excertos primários preservados lidos por Carver] '
addition+='A negativa de acesso direto desta sessão permanece no histórico; a fonte agora foi consultada por meio dos excertos extraídos '
addition+='pelo agente principal e acompanhados de proveniência. A expressão anterior “somente adendo” está superada neste alcance documental.\n\n'
addition+='Os trechos mostram xi·R·|Psi|² e xi=1/6 (10132–10140), o termo modular beta·|1+w_eff| (10147–10165), '
addition+='e a EOM (Box−m²−xiR)Psi=beta·K_partial·Psi (10203–10218). O contexto 10219–10249 também preserva a qualificação '
addition+='do próprio artigo sobre a ponte ao contínuo. [DECLARADO na fonte] A frase de obtenção por variação não foi verificada nesta revisão.\n\n'
addition+='**B1′ continua condicional a hEOM.** Não se reabriu build Lean, não se derivou xi=1/6 e não se elevou a EOM a experimento. '
addition+='O hash do original em PROVENIENCIA_ARTIGO_A.json é medição atribuída à principal; este revisor mediu os arquivos de excertos e proveniência, '
addition+='sem rehashear ou acessar diretamente o original.\n\n'
addition+=f'- [{Path(excerpt["path"]).name}](<{Path(excerpt["path"]).as_posix()}>) — {excerpt["bytes"]} bytes, SHA256 `{excerpt["sha256"]}`.\n'
addition+=f'- [{Path(provenance_copy["path"]).name}](<{Path(provenance_copy["path"]).as_posix()}>) — {provenance_copy["bytes"]} bytes, SHA256 `{provenance_copy["sha256"]}`.\n\n'
addition+='ADENDO_FONTE_PRIMARIA.json contém os caminhos de origem/cópia e os estatutos; o selo/manifesto corrente substitui os hashes documentais anteriores, '
addition+='cujas versões permanecem em backups de bytes. A decisão matemática e os logs aceitos não mudaram.\n'
p=ROOT/'REVISAO_B1_PRIME.md'; write(p,p.read_bytes()+addition.encode('utf-8'))
files=[info(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name not in ['MANIFESTO_REVISAO.json','SELO_REVISAO.json']]
record(ROOT/'MANIFESTO_REVISAO.json',dict(created_utc=stamp(),root=str(ROOT),files=files,count=len(files),
    amendment='Excertos primários com proveniência; conteúdo Lean e decisão técnica preservados',excludes=['MANIFESTO_REVISAO.json','SELO_REVISAO.json']))
record(ROOT/'SELO_REVISAO.json',dict(created_utc=stamp(),decision=audit['decision'],reviewer_identity=audit['reviewer_identity'],
    files=[info(ROOT/n) for n in ['MANIFESTO_REVISAO.json','REVISAO_B1_PRIME.md','AUDITORIA_INDEPENDENTE.json','ADENDO_FONTE_PRIMARIA.json']]))
print(json.dumps(dict(status=recording['status'],receipt=info(ROOT/'REVISAO_B1_PRIME.md')),ensure_ascii=False,indent=2))
