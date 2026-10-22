"""Record the short ordinary-directory sandbox required by Windows path limits."""
import datetime as dt
import json
from diary_r1 import ROOT, CLI, WHO
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
reg.DEST = OUT
claim = reg.call([CLI,'ver','F1.FECHO_20261015'])['reivindicacao']
assert claim['quem'] == WHO and dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
data = {'claim_event':845, 'actor':WHO,
        'additional_workspace':str(ROOT/'work/rite394_20261015'),
        'reason':'Windows MAX_PATH during ordinary byte-copy of existing Lean packages; short physical path, no junctions/hardlinks.',
        'scope':'Same isolated full-rite task, candidate R3; copy historical admitted caches only; no new observed-data opening, production stop, canonical write, provider call or gate change.',
        'evidence_destination':str(OUT/'full_rite'),
        'memory_surfaces_unchanged':['memory/DIARIO_CONSTRUCAO_QG.md','memory/TGL_ATLAS.md','memory/TGL_INDICE_VIVO.md','Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']}
result = reg.call([CLI,'anotar','--quem',WHO,'--tipo','ESCOPO_DE_REIVINDICACAO','--unidade','F1.FECHO_20261015','--dados',json.dumps(data,ensure_ascii=False)],'CLAIM_SHORT_RITE_SCOPE.json')
print(json.dumps(result,ensure_ascii=False))
