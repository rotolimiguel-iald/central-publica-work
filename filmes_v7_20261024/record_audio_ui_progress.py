from pathlib import Path
import hashlib,json
from bootstrap import cli,save,REF,ACTOR

V=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\video_um\delivery_v7')
W=Path(__file__).resolve().parent
def pin(p):return {'file':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
audit=json.loads((V/'audit/AUDIO_PREPARATION.json').read_bytes())
assert audit['final_validation']['status']=='PASS_READY_FOR_ENCODING'
evidence={'status':'AUDIO_COMPLETE_UI_FILM1_VERIFIED_FILM2_RENDERING',
 'audio':audit['final_validation'],'source':pin(V/'audit/AUDIO_PREPARATION.json'),
 'ui_observed':{'film1_seconds':224,'voice_switch_preserved_time':136,'frame_step_from':136,'frame_step_to':136.016666,'speed_half':.5,'advance_10s_from':136.016666,'advance_10s_to':146.016666,'subtitle_ready_languages':['en','pt-BR','fr','zh-Hans'],'caption_card_overlap_fixed':True},
 'screenshots':[pin(W/n) for n in ['FILM1_CAPTION_EN_FR.png','FILM1_CAPTION_ZH.png','FILM1_NATURE_CAPTION_FIXED.png']],
 'limitations':['Subjective pronunciation not auditioned in this tool environment.','Final shrinking return is flagged as transition in render; coverage interpretation under independent review.','Full film2 render and final media validation pending.']}
save('AUDIO_UI_PROGRESS.json',evidence)
script=r'C:\IALD\MEMORIA_IALD\session_memory.py'
state=cli(script,{'operation':'get','reference':str(REF)})['result']
handles=state['p']['handles']
for h in handles:
 if h['id']=='01a16f0a-be0c-7300-97f3-22204c948fb6':h['status']='completed';h['evidence']=str(V/'audit/AUDIO_PREPARATION.json')
handles.extend([
 {'id':'21be2e3bef15424aa5ab7c5aaf8a2a4d','kind':'local_render','status':'completed','task_id':'B','version':'v399'},
 {'id':'1d02d0cad4294527843ce6aa3660991c','kind':'local_render','status':'running','task_id':'B','version':'v399'}])
p=W/'AUDIO_UI_PROGRESS.json'
changes={'records':[{'id':'v7_audio_complete_player_verified','kind':'fact','statute':'REAL','text':'Narração V7 EN/PT concluída:60unidades verificadas, quatro mixes224/360s em -16±1LUFS,26VTT sem sobreposição. Cache-only e resolver padrão reutilizam sucessos. PlayerF1 verificado com idiomas,frame-step,velocidade e posição preservada; legenda reposicionada para deixar cartão legível. CapturaF2 e encodes finais pendentes. Sem auditoria perceptual da pronúncia.','sources':[{'kind':'artifact','ref':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}]}],
 'flow':{'phase':'v399_media_finalization','next_action':'Concluir capturaF2/loop, encodes, revisão visual e manifesto final; preservar autorização limitada e caches.','handles':handles}}
result=cli(script,{'operation':'transition','reference':str(REF),'actor':ACTOR,'expected_revision':state['revision'],'event_id':'v7-audio-complete-player1-verified','changes':changes})
save('TRANSITION_AUDIO_UI_COMPLETE.json',result);print(json.dumps(result,ensure_ascii=False))
