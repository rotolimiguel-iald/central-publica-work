from pathlib import Path
import datetime
import hashlib
import os
import sys

root = Path(__file__).resolve().parent
last = int(sys.argv[1])
atlas = Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md')
data = atlas.read_bytes()
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
note = (f'\n\n## Checkpoint {stamp} — leitura integral do Atlas\n\n'
        f'[REAL] Cobertura contínua lida: linhas 1–{last}. '
        'Linhas exatamente repetidas foram reconhecidas por igualdade de bytes/texto, '
        'mantendo os títulos. Saída agregada truncada de 12650–12767 foi relida isoladamente. '
        f'Atlas fonte única: {len(data)} bytes; SHA256 {hashlib.sha256(data).hexdigest()}.\n'
        f'Próxima linha: {last + 1}. Não declarar leitura integral antes do fim. '
        '37 teoremas positivos, 33 controles numéricos e 2 adulterações Lean recusadas '
        'já entregues. Não repetir provas/testes sem mudança. Handoff e manifesto já existem. '
        'Resta leitura integral e recibo final; original um.py não alterado.\n')
for name in ('MEMORIA_CENTRAL.md', 'REGISTRO_DAS_CONVERSAS.md'):
    path = root / name
    before = path.read_bytes()
    backup = path.with_name(path.name + '.bak_' + stamp)
    backup.write_bytes(before)
    assert backup.read_bytes() == before
    after = before + note.encode('utf8')
    temp = path.with_name(path.name + '.tmp_' + stamp)
    temp.write_bytes(after)
    assert temp.read_bytes() == after and len(after) > len(before)
    assert path.read_bytes() == before
    os.replace(temp, path)
    assert path.read_bytes() == after
print(f'Checkpoint salvo: {last}; próximo {last + 1}')
