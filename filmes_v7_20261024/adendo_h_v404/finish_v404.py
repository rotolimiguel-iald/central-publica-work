"""Collate completed and independently reviewed local films; never publish."""
from context import *
sys.path.insert(0,str(H))
from finalizer_guards import validate_frozen_data, validate_replay, validate_public_pointer, validate_final_receipts, verify_pin
from current_audio_guard import validate_audio
from final_job_guards import validate_worker_jobs, validate_observation_bindings

def main():
 check();stable_seal()
 assert not (T/'RESULTADO.json').exists() and not (H/'CONSTRUCTION_DELIVERY_V404.json').exists()
 source=validate_frozen_data(H,V,N);validate_replay(V,source);validate_audio(H,V,source);validate_final_receipts(H,V,source)
 jobs=validate_worker_jobs(H,V,source);validate_observation_bindings(H,V,source,jobs)
 final_review=read(H/'FINAL_DELIVERY_REVIEW.json')
 assert final_review['status']=='PASS_WITH_SCOPE' and final_review['actor']=='codex-video-v404-final-review'
 assert final_review['source']=='v404' and final_review['source_sha256']==source
 for p in final_review['reviewed_final_pins']:verify_pin(p)
 assert {Path(p.get('path',p.get('file'))).resolve() for p in final_review['reviewed_final_pins']} >= {(H/'MEDIA_FINAL_BINDING.json').resolve(),(V.parent/'PUBLIC_DELIVERY_V7.json').resolve()}
 m=read(V/'PUBLIC_DELIVERY_V7.json');pointer=read(V.parent/'PUBLIC_DELIVERY_V7.json');validate_public_pointer(m,pointer,V)
 assert m['source']==pointer['source']=='v404' and m['source_sha256']==pointer['source_sha256']==source
 public_bytes=0
 old=read(H/'baseline_manifest_v402/PUBLIC_DELIVERY_V7.json')['source_sha256'].encode();old_hits=[]
 for e in m['public_files']:
  p=V/e['path'];verify_pin({**e,'path':str(p)});public_bytes+=e['bytes']
  tail=b''
  with p.open('rb') as stream:
   while block:=stream.read(8*1024*1024):
    combined=tail+block
    if old in combined:old_hits.append(e['path']);break
    tail=combined[-63:]
 assert not old_hits,old_hits
 prov=read(V/'PROVENANCE_PUBLIC.json');assert prov['anchors_all_ok'] and len(prov['anchors'])>=64
 numeric=read(H/'PARENT_NUMERIC_REVIEW.json');assert numeric['status']=='PASS_WITH_SCOPE' and not numeric['unexpected_differences']
 capture=read(H/'PARENT_CAPTURE_AUDIT.json');watch=read(H/'MEDIA_WATCH.json')
 binding=read(H/'MEDIA_FINAL_BINDING.json');assert binding['status']=='PASS_FINAL_BINDING_READY_FOR_INDEPENDENT_REVIEW'
 returns=list(H.glob('AUDIO_SYNTHESIS_RETURN_*.json'));assert len(returns)==6
 plan=read(H/'AUDIO_PLAN.json');assert len(plan['new_units'])==6 and plan['reused_units']==52
 for p in returns:
  d=read(p);assert d['status']=='COMPLETED';verify_pin(d['audio']);verify_pin(d['receipt']);verify_pin(d['intent'])
 names=['ORIGIN_VERIFIED.json','SOURCE_INTAKE.json','SOURCE_CAPTURE.json','NUMERIC_COMPARISON.json','NUMERIC_APPROVED.json','PARENT_DATA_REVIEW.json','PARENT_NUMERIC_REVIEW.json','MEDIA_DATA_READY.json','DATA_ACCEPT.json','AUDIO_PLAN.json','AUDIO_EXECUTION_RELEASE.json','AUDIO_RESULT_REVIEW.json','MEDIA_AUDIO_READY.json','INTEGRATION_REVIEW.json','INTEGRATION.json','INTEGRATION_PROJECTIONS_COMPLETED.json','PARENT_CAPTURE_AUDIT.json','PRE_MAKE_JOB_BINDING.json','FINAL_MAKE.json','FINAL_RENDER_MANIFEST_LINK.json','FINAL_PLAYER_V404.json','MEDIA_FINAL_BINDING.json','FINAL_DELIVERY_REVIEW.json','MEDIA_HANDLE_COMPLETE.json','FINALIZER_INDEPENDENT_REVIEW.json','FINALIZER_INDEPENDENT_REVIEW_R2.json','FINALIZER_CONTROLS.json','FINAL_JOB_GUARD_CONTROLS.json','MEDIA_PROCESS_RECONCILIATION.json']
 result={'status':'BUILT_FOR_MANAGEMENT_INTEGRATION_PUBLICATION','source':'v404','source_sha256':source,
   'seal_timestamp':read(N/'um_absoluto_selo.json')['timestamp'],'mission_reference':str(REF),'request_id':'ordem022-adendo-h-v404',
   'delivery':pin(V.parent/'PUBLIC_DELIVERY_V7.json'),'manifest':pin(V/'PUBLIC_DELIVERY_V7.json'),
   'public_files':len(m['public_files']),'public_bytes':public_bytes,'anchors':len(prov['anchors']),'anchors_all_ok':True,
   'authorized_counts':numeric['expected_counts_read_from_sealed_sources'],'gate_counts':numeric['gate_counts'],
   'unexpected_numeric_differences':[],'public_old_source_pin_occurrences':old_hits,
   'capture':capture['jobs'],'capture_pipelines':1,'worker_elapsed_seconds':watch['elapsed_seconds'],'worker_stages':watch['timings'],
   'media_count':binding['media_count'],'image_count':binding['image_count'],
   'audio':{'new_units':6,'reused_units':52,'unique_units':58,'occurrences':76,'requests':6,'retries':0,'returns':[pin(p) for p in returns]},
   'cost':{'direct_tts_estimate_usd':0,'statute':'DERIVED','basis':'Escopo estimado autorizado no adendo; não é cotação ou fatura do provedor.','provider_bill_measured':False,'local_cpu_energy_monetary_cost_measured':False},
   'personal_voice':'Previews excluded from films; approved EN Andrew/PT Antonio narration retained.',
   'publication':'NOT_PERFORMED_BY_VIDEO_SESSION','evidence':[pin(H/n) for n in names],
   'limits':['No new Lean compilation, empirical test or scientific gate change.','Masks and full decode are engineering checks, not subjective audio audition or exhaustive visual review.','Measured CPU submission/overlay/stage time is not isolated GPU cost.','Management integrates and publishes; this receipt does not claim deployment.']}
 stable_seal();create(H/'CONSTRUCTION_DELIVERY_V404.json',result);create(T/'RESULTADO.json',result)
 counts=result['authorized_counts']
 lines=['# ORDEM 022 — ADENDO H · dois filmes V7, fonte v404',
 '[REAL] Construção local concluída e revisada; integração e publicação pela gerência.',
 f"Fonte: {source}; selo {result['seal_timestamp']}, relido antes da entrega.",
 f"Escada {counts['proof_ladder_clean']}/{counts['proof_ladder_total']}; {counts['formal_count']} arquivos formais; {counts['declaration_count']} declarações.",
 'Gate:18 bandeiras calculadas,0literais;15 lidas pelo veredito,3informativas; gate científico preservado.',
 'Comparação integral: nenhuma outra divergência numérica admitida; natureza preservada.',
 f"{result['anchors']} âncoras; replay13 testes locais e61 comparações no navegador, com negativos preservados.",
 'Filmes224s/360s em4K60; loop16s; única sequência de captura, sem recaptura.',
 'EN/PT:6 novas sínteses autorizadas,52 unidades reutilizadas;58 únicas,76 ocorrências;6 pedidos,0retries.',
 '26VTT; quatro idiomas de legenda; trocas de idioma e reprodução conferidas no player local.',
 f"{result['public_files']} arquivos públicos pinados;16vídeos/25imagens validados; masters4K privados.",
 f"Tempo local do worker:{watch['elapsed_seconds']:.3f}s; tempos de captura/etapas nos recibos.",
 'Estimativa direta TTS:US$0[DERIVED], não fatura/cotação; custo monetário de CPU/energia não medido.',
 'Primeiro launcher sem inicialização foi reconciliado; uma execução observada, sem repetir captura/TTS.',
 'Falhas/revisões anteriores preservadas; verificações finais ligadas aos jobs e arquivos efetivos.',
 'Voz pessoal permanece fora dos filmes; sem nova prova científica ou audição subjetiva integral.',
 f"PUBLIC_DELIVERY_V7.json:SHA256 {result['delivery']['sha256']}.",
 'Sem publicação/commit/push pela sessão do vídeo; originais Nós e gate intactos.']
 assert len(lines)<=20;create(T/'RELATORIO.md','\n'.join(lines)+'\n')
 print(json.dumps({'status':result['status'],'public_files':result['public_files'],'result':pin(T/'RESULTADO.json'),'report_lines':len(lines)}))

if __name__=='__main__':main()
