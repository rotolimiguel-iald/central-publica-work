from datetime import datetime
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
manifest = json.loads((WORK/'manifest_staged.json').read_bytes())
record = {
    'at': datetime.now().astimezone().isoformat(),
    'status': 'EXPLICIT_USER_APPROVAL_RECEIVED',
    'user_reply_verbatim': 'ative o app para mim e para quem eu quiser enviar convite (como falei, para minha mãe e para minha esposa por enquanto)',
    'preceding_request': 'Autoriza enviar o texto integral de IALD_Kernel_v5.txt e do novo IALD_TGL_MEMORY_CORE_v1_20260915.md à API OpenAI (api.openai.com), junto às fontes públicas, usá-los nas conversas do app e fazer um teste de até US$ 0,03? O teste não inclui o Atlas privado.',
    'interpretation': 'Ordem direta de ativação em resposta à revisão e à autorização específica apresentadas; não baseada no antigo faça tudo.',
    'destination': 'https://api.openai.com/v1',
    'max_test_usd': .03,
    'kernel_sha256': manifest['mother_instruction']['sha256'],
    'core_sha256': manifest['operational_core']['sha256'],
    'private_atlas_in_test': False,
}
path = WORK/'explicit_approval.json'
data = json.dumps(record, ensure_ascii=False, indent=2).encode()
temp = path.with_suffix('.tmp')
assert not path.exists()
with temp.open('xb') as handle:
    handle.write(data)
assert temp.read_bytes() == data
temp.replace(path)
print('Recorded the new activation instruction and its exact prior disclosure scope.')
