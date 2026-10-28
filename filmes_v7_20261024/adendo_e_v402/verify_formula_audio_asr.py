"""Offline CPU transcription of the two public formula excerpts; no audio edits."""
from pathlib import Path
import datetime, hashlib, json, os, sys, time

E = Path(__file__).resolve().parent
W = E.parent
sys.path.insert(0, str(W))
import mission

def pin(path):
    path = Path(path)
    with path.open('rb') as stream: digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'path':str(path), 'bytes':path.stat().st_size, 'sha256':digest}

def main():
    output = E/'FORMULA_AUDIO_ASR.json'
    assert not output.exists(), 'Recover existing result, do not repeat'
    state = mission.project()
    task = next(t for t in state['projection']['active'] if t['id']=='V402_FORMULA_NARRATION')
    preflight = mission.call({'operation':'check', **mission.current('codex-video-v7'),
                             'task_id':task['id'],'lease_id':task['lease']['id'],'max_chars':100000})
    assert preflight['ready']
    library = Path(sys.executable).parent/'Library/bin'
    assert (library/'sndfile.dll').is_file()
    os.environ['PATH'] = str(library)+os.pathsep+os.environ.get('PATH','')
    dll_directory = os.add_dll_directory(str(library))
    sys.path.insert(0, str(W/'voice_test'))
    import offline_preview as local
    os.environ['OMP_NUM_THREADS'] = os.environ['MKL_NUM_THREADS'] = '2'
    import torch
    torch.set_num_threads(2)
    downloads = json.loads((W/'voice_test/MODEL_DOWNLOADS.json').read_bytes())
    model_record = next(m for m in downloads['models'] if m['repo']=='openai/whisper-small')
    model_path = Path(model_record['path'])
    model_pins = [pin(p) for p in sorted(model_path.rglob('*')) if p.is_file()]
    preview_record = json.loads((E/'FORMULA_LISTENING_PREVIEWS.json').read_bytes())
    approval = json.loads((E/'FORMULA_NARRATION_PARENT_REVIEW.json').read_bytes())
    plan = json.loads(Path(approval['plan']['path']).read_bytes())
    assert plan['plan_sha256'] == preview_record['plan_sha256']
    started = time.perf_counter()
    asr = local.make_asr(str(model_path))
    results = []
    for language, code, filename in [('pt-BR','pt','preview_formula_pt.wav'),('en','en','preview_formula_en.wav')]:
        path = E/filename
        before = pin(path)
        bound = next(r for r in preview_record['previews'] if r['language']==language)
        assert before == bound['preview']
        expected = ' '.join(cue[language] for segment in plan['films']['film1']['segments']
                            if segment['key'] in ['boundary','mirror'] for cue in segment['cues'])
        result = local.transcribe(asr, path, code)
        assert pin(path)==before
        results.append({'language':language,'audio':before,'expected':expected,
                        'asr':result,'word_error_rate':local.wer(expected,result['text'])})
        print(json.dumps({'language':language,'status':'TRANSCRIBED_OFFLINE'},ensure_ascii=False),flush=True)
    receipt = {'status':'AUTOMATIC_TRANSCRIPTION_COMPLETED_REVIEW_REQUIRED','actor':'codex-video-v7',
               'preflight':preflight,'plan_sha256':plan['plan_sha256'],
               'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'elapsed_seconds':time.perf_counter()-started,'model':model_record['repo'],
               'model_files':model_pins,'runtime':pin(sys.executable),'helper':pin(local.__file__),
               'cpu_threads':2,'network_blocked':True,'connection_attempts':len(local.BLOCKED),
               'audio_modified':False,'results':results,
               'limits':['Automatic recognition is not perceptual listening or proof of correct pronunciation.',
                         'Number and proper-name spelling can differ in automatic transcription.']}
    raw = (json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode()
    temporary=output.with_suffix('.tmp')
    with temporary.open('xb') as stream:stream.write(raw)
    assert temporary.read_bytes()==raw
    os.replace(temporary,output)
    print(json.dumps({'status':receipt['status'],'output':str(output)}),flush=True)

if __name__=='__main__':main()
