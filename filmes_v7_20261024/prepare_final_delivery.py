"""Collate verified V7 construction artifacts; never publish or accept a mission."""
from pathlib import Path
import hashlib,json,os,time,sys

W=Path(__file__).resolve().parent
V=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
T=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_022')
def read(p):return json.loads(Path(p).read_bytes())
def sha(p):
 with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def pin(p):
 p=Path(p);return {'file':str(p),'bytes':p.stat().st_size,'sha256':sha(p)}
def atomic(p,data):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists():
  old=p.read_bytes()
  if old==data:return
  p.with_name(p.name+'.bak_'+str(time.time_ns())).write_bytes(old)
 q=p.with_name(p.name+'.tmp');q.write_bytes(data);assert q.stat().st_size==len(data)>0;os.replace(q,p)
def save(p,d):atomic(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))

manifest=read(V/'PUBLIC_DELIVERY_V7.json')
pointer=read(V.parent/'PUBLIC_DELIVERY_V7.json')
assert pointer['sha256']==sha(V/'PUBLIC_DELIVERY_V7.json')
h=read(V/'data/hud.json');p=read(V/'PROVENANCE_PUBLIC.json');r=read(V/'RENDER_MANIFEST.json')
seal=read(V.parent.parent/'Nós/um_absoluto_selo.json')
assert h['seal_pin']==manifest['source_sha256']==seal['sha256']['um.py']
assert h['seal_version']==seal['um_version'] and p['anchors_all_ok']
media=read(V/'render/MEDIA_VALIDATION.json');assert media['status']=='PASS'
for entry in manifest['public_files']:
 path=V/entry['path'];assert path.is_relative_to(V) and path.stat().st_size==entry['bytes'] and sha(path)==entry['sha256'],entry['path']
 assert not any(x in path.parts for x in ['private','source','cache','voice_sample','work']),entry['path']
 assert '.bak_' not in path.name and 'APPROVAL' not in path.name
cost={};coverage={}
for key,j in r['jobs'].items():
 rows=j['render']['samples'];duration=j['metadata']['duration'];assert len(rows)==int(duration)
 nontrans=[x for x in rows if not x['transition']]
 assert nontrans and min(x['width_fraction'] for x in nontrans)>=.6
 if key!='loop':assert sum(x['transition'] for x in rows)<=5
 cost[key]={k:j['render'][k] for k in ['elapsed_s','scene_cpu_submit_seconds','overlay_cpu_seconds']}
 coverage[key]={'samples':len(rows),'nontransition_samples':len(nontrans),'minimum_width_fraction':min(x['width_fraction'] for x in nontrans),'transition_samples':sum(x['transition'] for x in rows)}
audio=read(V/'audit/DELIVERY_D.json')
ui=read(W/'FINAL_PLAYER_CHECKS.json');assert ui['status']=='PASS_OBSERVED_UI'
critical=[V/'replay/REVIEW_FROZEN_PREVIEW_CAPTIONS.json',V/'replay/REVIEW_V399_STUDY_REPLAY.json',W/'CONTENT_CHECKS_V399.json',W/'REPRODUCTION_V399.json',W/'PARENT_REPLAY_V399.json',W/'FINAL_PLAYER_CHECKS.json',V/'audit/DELIVERY_D.json',V/'render/MEDIA_VALIDATION.json']
critical.append(W/'TAMPER_V399_UI.json')
critical.append(W/'REPRODUCTION_V399_FINAL_BUILDER.json')
critical.append(V/'replay/REVIEW_CAPTION_WRAP_SUPPLEMENT_R1.json')
critical.append(V/'replay/CURRENT_SEAL_METADATA_RECONCILIATION.json')
critical.append(V/'replay/REVIEW_B_FINAL_JOBS_R1.json')
critical.append(V/'audit/DELIVERY_E.json')
critical.append(W/'FINAL_MAKE.json')
assert read(W/'REPRODUCTION_V399_FINAL_BUILDER.json')['status']=='PASS'
evidence=[pin(x) for x in critical]
limitations=[
 'Construction delivered for management review/integration/publication; no website or canonical science changed.',
 'Scene geometry is ONTO and presentation environment INPUT; recorded data retains its hypotheses. No new Lean or empirical test.',
 'Full frame rerender is still required when numbers change; CPU layer submission costs are not isolated GPU costs.',
 'Integrated-GPU performance was not measured. RTX5090 test and fallback controls have limited separate evidence.',
 'Narration loudness/timing were measured; subjective pronunciation was not auditioned in this tool environment.',
 'Personal voice sample was assessed locally only and is excluded from the public delivery; no clone was created.',
 'The 64 provenance checks include 12 serialization checks; 61 browser comparisons cover 34 core and27 HUD values, with19 documentary HUD fields not recomputed.',
 'The current seal gained four metadata fields after the frozen source snapshot; its prior fields, timestamp and14 source hashes are unchanged, independently reconciled.',
]
parts={
 'A':{'status':'BUILT_VERIFIED_FOR_REVIEW','anchors':len(p['anchors']),'anchors_all_ok':True,'source':h['seal_version'],'source_sha256':h['seal_pin'],'reproduction':pin(W/'REPRODUCTION_V399_FINAL_BUILDER.json'),'builder':pin(V/'make_v7.py')},
 'B':{'status':'BUILT_VERIFIED_FOR_REVIEW','durations_seconds':[224,360],'coverage':coverage,'exact_stdout':pin(V/'data/STDOUT_LINES.json'),'framing_correction':pin(W/'CLOSING_FINITE_PATCH.json')},
 'C':{'status':'BUILT_VERIFIED_FOR_REVIEW','receipt':pin(V/'replay/DELIVERY_C.json'),'browser':pin(W/'PARENT_REPLAY_V399.json'),'tamper_control':pin(W/'TAMPER_V399_UI.json'),'runtime_bytes':16910221},
 'D':{'status':'BUILT_VERIFIED_FOR_REVIEW','receipt':pin(V/'audit/DELIVERY_D.json'),'audio':'Separate EN/PT-BR MP4s;26 VTT;60 cached units, no new TTS in final capture'},
 'E':{'status':'BUILT_VERIFIED_FOR_REVIEW','receipt':pin(V/'audit/DELIVERY_E.json'),'validation':pin(V/'render/MEDIA_VALIDATION.json'),'web':pin(V/'audit/WEB_BUILD.json'),'player':pin(W/'FINAL_PLAYER_CHECKS.json'),'background_gpu':pin(W/'BG_PARENT_DIAGNOSTICS.json'),'public_files':len(manifest['public_files'])},
}
result={'status':'BUILT_FOR_MANAGEMENT_REVIEW','partes':parts,'delivery':str(V.parent/'PUBLIC_DELIVERY_V7.json'),'delivery_sha256':sha(V.parent/'PUBLIC_DELIVERY_V7.json'),'manifest':pin(V/'PUBLIC_DELIVERY_V7.json'),'anchors':len(p['anchors']),'anchors_all_ok':True,'costs':cost,'cost_scope':'Measured browser CPU submission/overlay and total capture wall-clock; no isolated GPU cost or claimed incremental speedup.','evidence':evidence,'limitations':limitations,'mission_reference':str(W/'SESSION_REFERENCE.json'),'publication':'NOT_PERFORMED'}
save(W/'FINAL_CONSTRUCTION_DELIVERY.json',result)
save(V/'audit/DELIVERY_AB.json',{'partes':{k:parts[k] for k in ['A','B']},'evidence':evidence,'limitations':limitations,'publication':'NOT_PERFORMED'})
save(T/'RESULTADO.json',result)
lines=[
 f'# ORDEM022 — dois filmes V7, fonte {h["seal_version"]}',
 '[REAL] Construção entregue para revisão, integração e publicação pela gerência a7.',
 f'A — {len(p["anchors"])} checagens de proveniência aprovadas; cinco arquivos reproduzidos byte a byte em cópia do snapshot usado no render.',
 'As checagens incluem12 de serialização; não constituem64 provas independentes.',
 f'Fonte: {h["seal_version"]} · SHA256 {h["seal_pin"]} · selo {h["seal_timestamp"]}.',
 'Selo atual ganhou quatro campos de metadados; conteúdo anterior e 14 hashes preservados. Snapshot original e reconciliação conservados.',
 'B — Filmes de 224 s e 360 s, masters privados 4K/60 fps; espelho/J, solda, Schwarzschild, spin 2, PÊNTADA e 18 bandeiras (15+3).',
 'Stdout real vinculado por hash; z_disc, p unilateral e limiar 5σ simultâneos. Sem alteração do kernel ou gate.',
 f'Enquadramento: mín.F1={coverage["film1"]["minimum_width_fraction"]:.4%},F2={coverage["film2"]["minimum_width_fraction"]:.4%}; máscara1fps, exclusão só2s iniciais/3s finais.',
 'Negativo preservado: retorno anterior de 56 s indevidamente tratado como transição; corrigido e recapturado.',
 'C — Pyodide local de 16,91 MB sob clique; recorte Python; 61/61 comparações observadas; 19 campos documentais não recalculados.',
 'D — Narração EN/PT-BR em MP4s separados; quatro idiomas de legendas por voz, 26 VTT; -16±1 LUFS; sem música.',
 'Sessenta unidades completas reutilizadas; autorizações e falhas anteriores preservadas; sem novo TTS no fechamento.',
 f'E — {len(manifest["public_files"])} arquivos públicos com bytes/SHA; H264/VP9/720p,loop,pôsteres/stills e contrato bg_scene.',
 'Player: capítulos, velocidade, quadro e inspeção de métricas; troca de voz conserva posição; legendas acima do cartão.',
 'GPU: p95=3,851584 ms em RTX 5090, 920x518, q=0,75; GPU integrada não medida; fallback com controles locais.',
 'Narração sem auditoria perceptual de pronúncia; amostra pessoal ficou local e fora da entrega.',
 'Títulos EN propostos: The emergence of gravity / From identity to geometry.',
 'Camadas: scene_cpu_submit/overlay_cpu medidos; GPU isolada não medida; atualização numérica ainda exige render integral.',
 *[f'{k}: captura={d["elapsed_s"]:.3f}s;sceneCPU={d["scene_cpu_submit_seconds"]:.3f}s;overlayCPU={d["overlay_cpu_seconds"]:.3f}s.' for k,d in cost.items()],
 f'Delivery: {result["delivery"]}',
 f'SHA256 delivery: {result["delivery_sha256"]}',
 'Recibos e limitações completos em RESULTADO.json. V6, originais e renders anteriores preservados.',
 'Gerência confere os critérios e publica; esta entrega não escreveu no site, espelho, Atlas ou Nós.',
]
assert len(lines)<=40;atomic(T/'RELATORIO.md',('\n'.join(lines)+'\n').encode('utf-8'))
route={'tipo':'RESULTADO','rota_id':'site.filmes.v7.ordem022','dominio':'SITE_E_PUBLICACAO','titulo':'Construção dos dois filmesV7 entregue para revisão da gerência','resultado':f'{h["seal_version"]};224/360s;{len(p["anchors"])}checagens;61comparaçõesbrowser;26VTT;{len(manifest["public_files"])}arquivos públicos pinados.','veredito':'BUILT_FOR_MANAGEMENT_REVIEW','estatuto':'REAL','status':'EXAMINADA','olhou_dados':False,'defeito':'Sem benchmark GPU integrada nem auditoria perceptual da pronúncia; render numérico ainda integral.','nao_refazer':'Reutilizar manifestos,áudio verificado e recortePython; não repetir enviosTTS incertos.','proximo_passo':'Gerência a7 revisa,integra porhash e publica.','onde':str(V),'artefatos':[str(T/'RESULTADO.json'),str(V.parent/'PUBLIC_DELIVERY_V7.json')],'refs':[],'nota':'Construção operacional,não teste de natureza ou mudança de gate.'}
save(W/'FINAL_ROUTE.json',route)
print(json.dumps({'status':result['status'],'files':len(manifest['public_files']),'report_lines':len(lines),'result':pin(T/'RESULTADO.json')},ensure_ascii=False))
