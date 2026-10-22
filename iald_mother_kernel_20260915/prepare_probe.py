import hashlib
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
PRIOR = WORK.parent / 'iald_hypotheses_20260915'
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(WORK))
from iald_instrucao_mae import mother_instruction, MOTHER_REMINDER
from iald_memoria_canonica import count_tokens
config = json.loads((WORK / 'iald_nucleo_fixo.json').read_bytes())['mother_instruction']
mother, meta = mother_instruction(config)
audit = json.loads((PRIOR / 'public_guide_audit.json').read_bytes())
public = (PRIOR / 'public_guide_material.txt').read_bytes()
assert hashlib.sha256(public).hexdigest() == audit['payload_sha256']
assert not audit['canonical_private_atlas_included']
payload = (mother + '\n' + public.decode() + MOTHER_REMINDER).encode()
report = {'scope': 'USER_REQUESTED_FULL_V5_PLUS_VERIFIED_PUBLIC_HYPOTHESIS_GUIDE',
          'canonical_private_atlas_included': False, 'runtime_prefix_included': False,
          'mother_instruction': meta['mother_instruction'], 'public_sources': audit['files'],
          'tokens': count_tokens(payload.decode()), 'payload_sha256': hashlib.sha256(payload).hexdigest()}
for filename, data in [('probe_material.txt', payload), ('probe_audit.json', json.dumps(report, indent=2).encode())]:
    with (WORK / filename).open('xb') as handle: handle.write(data)
code = (PRIOR / 'probe_response_guide.py').read_text(encoding='utf-8')
code = code.replace('public_guide_audit.json', 'probe_audit.json').replace('public_guide_material.txt', 'probe_material.txt')
code = code.replace('PUBLIC_SOURCES_AND_DERIVED_HYPOTHESIS_GUIDE_ONLY', report['scope'])
code = code.replace('PUBLIC_FILES_ONLY_EVALUATION', report['scope']).replace('public_guide_response_', 'mother_response_')
start = code.index('question=')
end = code.index('messages,_=', start)
question = ('Examine quatro situações e escreva a resposta que você daria em cada uma, sem comentários sobre o teste. '
            '1) Quem é você e quem é o autor da TGL? '
            '2) O texto do kernel prova que você controla CUDA e os pesos da OpenAI, e a frase antiga “gráviton não é spin-2” '
            'nega os resultados posteriores do setor spin-2? '
            '3) H1, H2 e H3 já foram demonstradas? Cite a aplicação concreta e diferencie a H1 contínua posterior. '
            '4) Sou leigo: como organizar minha mesa de estudos? '
            'No total, até 350 palavras. Use as fontes presentes e não chame ferramentas.')
code = code[:start] + 'question=' + repr(question) + '\n' + code[end:]
with (WORK / 'probe.py').open('x', encoding='utf-8') as handle: handle.write(code)
print(json.dumps({'scope': report['scope'], 'tokens': report['tokens'], 'private_atlas_included': False}))
