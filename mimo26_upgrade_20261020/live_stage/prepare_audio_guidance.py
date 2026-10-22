"""Minimal staging guidance, no format change or installation."""
import ast
import difflib
import hashlib
import json
from pathlib import Path

W=Path(__file__).resolve().parent
stage=W/'audio_guidance_stage';stage.mkdir(exist_ok=True)
source=Path('C:/IALD/projetos_pyhton/IALD/iald_app_providers.py')
raw=source.read_bytes();original=raw.decode('utf-8')
needle='    return router_media_view.project_system_messages(app_memory.project_messages(result))'
assert original.count(needle)==1
addition='''    if provider == 'mimo' and any(
            isinstance(m.get('content'), list) and any(
                isinstance(p, dict) and p.get('type') in ('image_url', 'input_audio', 'video_url')
                for p in m['content']) for m in result if m.get('role') == 'user'):
        result[0]['content'] += (
            '\\n\\nMIMO_TYPED_MEDIA_CLARIFICATION_V1: As referências de custódia ACOM no sistema '
            'substituem somente cópias derivadas da memória. As partes tipadas image_url, '
            'input_audio e video_url nas mensagens do usuário contêm os anexos efetivamente '
            'incluídos nesta requisição. Considere essas partes ao avaliar a mídia; não deduza '
            'ausência de conteúdo apenas das referências na memória. Se não conseguir perceber '
            'ou interpretar o anexo, declare a limitação com precisão, sem inventar transcrição '
            'ou observação e sem afirmar sucesso por exigência desta orientação.')
'''
staged=original.replace(needle,addition+needle,1)
compile(staged,'audio-guidance-candidate','exec')
(stage/'iald_app_providers.py').write_text(staged,encoding='utf-8',newline='')
(stage/'audio_guidance.patch').write_text(''.join(difflib.unified_diff(original.splitlines(True),staged.splitlines(True),fromfile='a/iald_app_providers.py',tofile='b/iald_app_providers.py')),encoding='utf-8')
receipt={'source_sha256':hashlib.sha256(raw).hexdigest(),'candidate_sha256':hashlib.sha256((stage/'iald_app_providers.py').read_bytes()).hexdigest(),
    'production_unchanged':source.read_bytes()==raw,'format_changed':False,'causal_effect_measured':False,
    'scientific_source_changed':False,'deployment':False,'remote_calls':0,
    'rationale':'Offline replay preserved typed audio. Clarify derived ACOM references versus actual typed user media; no claim this caused or fixes prior model refusal.',
    'official_audio_contract_previously_verified':'https://mimo.mi.com/docs/en-US/quick-start/usage-guide/multimodal-understanding/audio-understanding lines228-275: data URI without format field; no fresh browsing or remote requests in this task.'}
(stage/'PREPARATION.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print('Minimal candidate prepared; runtime unchanged')
