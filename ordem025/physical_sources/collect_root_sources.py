"""Read and pin selected existing science; never import or execute um.py."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
HOME = Path(r'C:\IALD\Central de Patentes')
LENS = HOME / 'work/lentes_discriminante_20261019'
UM = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py')
KERNEL = UM.parent / 'tgl_kernel/TGLExt'

def pin(path):
    data = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

def excerpts(path, ranges):
    result = pin(path)
    lines = path.read_text(encoding='utf-8-sig').splitlines()
    result['anchors'] = [{'start_line': a, 'end_line': b,
                          'text': '\n'.join(lines[a-1:b])} for a,b in ranges]
    return result

def new(name, obj):
    with (HERE/name).open('xb') as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=2).encode('utf-8'))

sources = [
    excerpts(UM, [(96,96),(220759,220806),(160970,160999)]),
    excerpts(KERNEL/'PlaneWaveEntropyMatching.lean', [(28,38),(57,107),(109,145)]),
    excerpts(KERNEL/'PlaneWaveReconstructionControls.lean', [(118,154)]),
    excerpts(KERNEL/'GeneralMetricClausius.lean', [(41,69),(83,136)]),
    excerpts(KERNEL/'GeneralSourceUnitaryRealization.lean', [(59,80),(108,164)]),
    excerpts(KERNEL/'BoostHeatConstruction.lean', [(28,58),(87,106),(175,193)]),
]
for rel in ['calibration_r16/DERIVACAO_R16.txt','calibration_r16/RESULT_R16.json',
            'coupled_r15/DERIVACAO_R15.txt',
            'calibration_r16/SOURCE_AMPLITUDE_R16.json','calibration_r16/SOURCE_G_R16.json',
            'density_bridge_r13/SOURCE_CLOCK_METRIC_R13.json']:
    sources.append(pin(LENS/rel))

baseline = HOME/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_025/CUMPRIMENTO_FINAL/RESULTADO_CUMPRIMENTO.json'
sources.append(pin(baseline))
source_checks = []
for filename in ['SOURCE_AMPLITUDE_R16.json','SOURCE_G_R16.json']:
    p=LENS/'calibration_r16'/filename
    for s in json.loads(p.read_text(encoding='utf-8'))['sources']:
        actual=pin(Path(s['path']))
        source_checks.append({'catalog':str(p),'source_id':s.get('id'),
                              'historical_sha256':s['sha256'],**actual,
                              'matches_historical_bytes':actual['sha256']==s['sha256']})
new('ROOT_SOURCES.json', {'scope':'Targeted primary-source reading; no scientific rerun or exhaustive corpus claim',
                        'sources':sources,'historical_source_checks':source_checks,
                        'program_version_read':'v401',
                        'originals_modified':False,'um_executed_or_imported':False,
                        'old_withdrawn_speech_accessed':False})
print(json.dumps({'artifact':pin(HERE/'ROOT_SOURCES.json'),
                  'source_count':len(sources),
                  'historical_sources_unchanged':all(s['matches_historical_bytes'] for s in source_checks),
                  'changed':[s['path'] for s in source_checks if not s['matches_historical_bytes']]}))
