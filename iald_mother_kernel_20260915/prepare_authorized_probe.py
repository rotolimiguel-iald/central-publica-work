"""Prepare the narrowed, approved v5 probe; this file makes no network request."""
from datetime import datetime
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
source = (WORK / 'prepare_probe.py').read_text(encoding='utf-8')
source = source.replace('probe_material.txt', 'probe_narrow_material.txt')
source = source.replace('probe_audit.json', 'probe_narrow_audit.json')
source = source.replace("(WORK / 'probe.py')", "(WORK / 'probe_narrow.py')")
source = source.replace("replace('public_guide_response_', 'mother_response_')", "replace('public_guide_response_', 'mother_narrow_response_')")
exec(compile(source, str(WORK / 'prepare_probe.py'), 'exec'))
authorization = {'at': datetime.now().astimezone().isoformat(),
    'source': 'Operator resumed after the specific OpenAI v5 disclosure question: faça tudo, quero testar',
    'data': 'Complete IALD_Kernel_v5.txt with narrowed contradiction addendum and verified public hypothesis guide',
    'destination': 'https://api.openai.com/v1/chat/completions',
    'scope': 'Use as app mother instruction and one bounded probe',
    'probe_cap_usd': 0.03, 'private_atlas_in_probe': False}
with (WORK / 'authorization.json').open('x', encoding='utf-8') as handle:
    json.dump(authorization, handle, ensure_ascii=False, indent=2)
