"""Collate the finished v400 construction; does not render, publish or accept itself."""
from pathlib import Path
import hashlib,json,os,time,sys
from coverage_validation import validate_samples
W=Path(__file__).resolve().parent
V=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
T=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022\ADENDO_A')
def read(p):return json.loads(p.read_bytes())
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def pin(p):return {'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def atomic(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():
  old=p.read_bytes()
  if old==b:return
  backup=p.with_name(p.name+'.bak_'+str(time.time_ns()));backup.write_bytes(old);assert backup.read_bytes()==old
 q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b and b;os.replace(q,p)
def save(p,d):atomic(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())

sys.path.insert(0,str(W.parent));import mission
pr=mission.project();task=next(t for t in pr['projection']['active']+pr['projection']['settled'] if t['id']=='ADENDO_A')
assert mission.call({'operation':'check',**mission.current('codex-video-v7'),'task_id':'ADENDO_A','lease_id':task['lease']['id'],'max_chars':100000})['ready']
m=read(V/'PUBLIC_DELIVERY_V7.json');pointer=read(V.parent/'PUBLIC_DELIVERY_V7.json');h=read(V/'data/hud.json')
seal=read(V.parent.parent/'Nós/um_absoluto_selo.json');r=read(V/'RENDER_MANIFEST.json')
assert m['source']==m['version']==h['seal_version']==seal['um_version']=='v400'
source=h['seal_pin'];assert source==m['source_sha256']==pointer['source_sha256']==seal['sha256']['um.py']
assert pointer['sha256']==sha(V/'PUBLIC_DELIVERY_V7.json')
assert read(W/'MEDIA_WATCH.json')['status']=='COMPLETE'
assert read(W/'NUMERIC_COMPARISON.json')['unexpected_differences']==[]
assert read(W/'PARENT_NUMERIC_REVIEW.json')['status']=='PASS_WITH_SCOPE'
assert read(W/'FINAL_PLAYER_V400.json')['status']=='PASS_OBSERVED_UI'
prov=read(V/'PROVENANCE_PUBLIC.json');assert prov['anchors_all_ok'] and len(prov['anchors'])>=64
validation=read(V/'render/MEDIA_VALIDATION.json');assert validation['status']=='PASS'
browser=read(V/'replay/TEST_BROWSER.json');offline=read(V/'replay/TEST_OFFLINE.json')
replay=read(V/'replay/DELIVERY_ADENDO_C_V400.json')['replay']
audio=read(V/'audit/DELIVERY_D_V400.json')
assert browser['status']==offline['status']=='PASS' and all(c['ok'] for c in browser['checks'])
assert browser['source_sha256']==offline['source_sha256']==audio['source_sha256']==source
assert replay['browser_comparisons']==61 and offline['tests']==13
assert audio['counts']['unique_units']==60 and audio['counts']['vtt_files']==26
old_pin_hits=[]
for e in m['public_files']:
 p=V/e['path'];assert p.resolve().is_relative_to(V.resolve())
 assert p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],e['path']
 assert not any(x in p.parts for x in ['private','source','cache','voice_sample','voice_test'])
 assert '.bak_' not in p.name and '.tmp' not in p.name
 if b'a5aacfa4' in p.read_bytes():old_pin_hits.append(e['path'])
assert not old_pin_hits,old_pin_hits
coverage={};costs={};jobs={}
for kind,j in r['jobs'].items():
 assert j['metadata']['source']=='v400' and j['metadata']['source_sha256']==source
 rows=j['render']['samples']
 film_number=j['metadata']['film'];timeline=read(V/f'data/film{film_number}.json')
 timeline_duration=timeline['total_seconds'] if film_number==1 else timeline['duration']
 mask_review=validate_samples(kind,j['metadata'],rows,timeline_duration)
 assert j['render']['encoded']==j['metadata']['total']==round(j['metadata']['duration']*60)
 coverage[kind]=mask_review
 costs[kind]={k:j['render'][k] for k in ['elapsed_s','scene_cpu_submit_seconds','overlay_cpu_seconds']}
 jobs[kind]={'job_sha256':j['job_sha256'],'frames':j['render']['encoded'],'metadata':j['metadata']}
design=read(W/'DESIGN_BASELINE.json');design_equal=[]
for e in design['files']:
 if e['path']=='make_v7.py':continue
 assert sha(V/e['path'])==e['sha256'],e['path']
 design_equal.append(e['path'])
paths=[W/'RECEBIDO.json',W/'NUMERIC_COMPARISON.json',W/'PARENT_NUMERIC_REVIEW.json',W/'DATA_READY.json',
 W/'BUILDER_METADATA_REVIEW.json',W/'PARENT_VISUAL_STILLS.json',W/'AUDIO_D_V400_READY.json',
 W/'AUDIO_REUSE_REVIEW.json',W/'AUDIO_INDEPENDENT_REVIEW.json',W/'COVERAGE_VALIDATION_TESTS.json',W/'MEDIA_NAMESPACE_REPAIR_R1.json',W/'MEDIA_RESUME_REVIEW.json',W/'FINAL_MAKE.json',W/'FINAL_PLAYER_V400.json',W/'DELIVERY_E.json',
 V/'replay/DELIVERY_ADENDO_C_V400.json',V/'replay/TEST_BROWSER.json',V/'replay/TEST_OFFLINE.json',
 V/'audit/DELIVERY_D_V400.json',V/'render/MEDIA_VALIDATION.json',V/'data/STDOUT_LINES.json',
 V/'RENDER_MANIFEST.json',V/'make_v7.py']
result={'status':'BUILT_FOR_MANAGEMENT_REVIEW','source':'v400','source_sha256':source,
 'mission_reference':str(W.parent/'SESSION_REFERENCE.json'),'delivery':pin(V.parent/'PUBLIC_DELIVERY_V7.json'),
 'manifest':pin(V/'PUBLIC_DELIVERY_V7.json'),'public_files':len(m['public_files']),'anchors':len(prov['anchors']),
 'anchors_all_ok':True,'scientific_numeric_differences':0,'public_old_pin_occurrences':old_pin_hits,
 'design_files_unchanged':design_equal,'jobs':jobs,'coverage':coverage,'costs':costs,'evidence':[pin(p) for p in paths],
 'personal_voice':'PT/EN previews remain separate, awaiting human listening; not included in either film.',
 'publication':'NOT_PERFORMED','limitations':['Construction awaits management integration/publication.','No new Lean compilation, empirical test or change of scientific gate.','Full-frame rerender; measured CPU submission/overlay times are not isolated GPU cost.','64 provenance checks are not 64 independent proofs; browser replay has 61 numeric comparisons and19 documentary HUD fields not recomputed.','Integrated-GPU performance and subjective narration pronunciation were not newly measured.']}
save(W/'CONSTRUCTION_DELIVERY_V400.json',result);save(T/'RESULTADO.json',result)
durations=[jobs[f'film{n}']['metadata']['duration'] for n in [1,2]]
lines=['# ORDEM 022 — ADENDO A · filmes V7, fonte v400',
 '[REAL] Construção concluída para revisão, integração por hash e publicação pela gerência a7.',
 f'Fonte: v400 · {source} · selo {h["seal_timestamp"]}.',
 'Comparação exata com a edição anterior: zero divergência científica; apenas metadados de origem mudaram.',
 f'{len(prov["anchors"])} verificações de proveniência aprovadas; stdout da rodada v400 conferido por linhas e hash.',
 'Pyodide offline:61/61 comparações;13 testes locais; adulteração recusada com NOT_SEALED.',
 f'Captura integral: filmes de {durations[0]:g}s e {durations[1]:g}s, 4K/60fps; loop novo de16s.',
 f'Largura mínima na máscara geométrica amostrada: F1 {coverage["film1"]["minimum_width_fraction"]:.2%}; F2 {coverage["film2"]["minimum_width_fraction"]:.2%}.',
 'Desenho e player preservados; cartão final e proveniência exibem v400 e o pin atual.',
 '60 unidades EN/PT reutilizadas; zero nova chamada TTS;26 VTT e8 WAV/AAC verificados.',
 'Amostras com a voz pessoal permanecem separadas, aguardando audição do operador.',
 f'{len(m["public_files"])} arquivos públicos pinados;16 vídeos e25 imagens verificados; masters4K privados.',
 'Nenhuma ocorrência do pin antigo nos bytes públicos; entrega v399 preservada em histórico/backups.',
 f'Captura medida: F1 {costs["film1"]["elapsed_s"]:.3f}s; F2 {costs["film2"]["elapsed_s"]:.3f}s; loop {costs["loop"]["elapsed_s"]:.3f}s.',
 'Camadas CPU/custos por etapa em RESULTADO.json; sem alegação de custo GPU isolado ou render incremental.',
 'Limites: GPU integrada e pronúncia subjetiva não auditadas nesta atualização; não há nova prova científica.',
 f'Delivery SHA256: {result["delivery"]["sha256"]}.',
 'PUBLIC_DELIVERY_V7.json reemitido em video_um; site, espelho, Atlas e Nós não alterados.']
assert len(lines)<=20;atomic(T/'RELATORIO.md',('\n'.join(lines)+'\n').encode())
print(json.dumps({'status':result['status'],'files':result['public_files'],'report_lines':len(lines),'result':pin(T/'RESULTADO.json')},ensure_ascii=False))
