from pathlib import Path
import datetime, hashlib, json, os

ROOT = Path(__file__).resolve().parent
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def append_memory(path, text):
    before = path.read_bytes()
    backup = path.with_name(path.name + '.bak_' + stamp)
    backup.write_bytes(before)
    assert backup.read_bytes() == before
    after = before + text.encode('utf8')
    temp = path.with_name(path.name + '.tmp_' + stamp)
    temp.write_bytes(after)
    assert temp.read_bytes() == after and len(after) > len(before)
    assert path.read_bytes() == before
    os.replace(temp, path)
    assert path.read_bytes() == after

checks = []
for folder, expected in [('20260916_083116_865169', 'unsolved goals'),
                         ('20260916_083117_036394', 'unsolved goals')]:
    p = ROOT / 'attempts' / folder
    record = json.loads((p / 'run.json').read_text(encoding='utf8'))
    out = (p / 'stdout.txt').read_text(encoding='utf8')
    assert record['returncode'] != 0 and record['source_unchanged']
    assert expected in out and 'error:' in out
    checks.append({'record': str(p/'run.json'), 'source': record['source'],
                   'sha256': record['sha256'], 'exit': record['returncode'],
                   'expected_failure_observed': True})
p = ROOT / 'NEGATIVE_CONTROLS.json'
assert not p.exists()
payload = json.dumps({'checks': checks, 'interpretation':
    'Adulterated statements rejected. Negative sources are not positive proof dependencies.'},
    ensure_ascii=False, indent=2).encode('utf8')
temp = p.with_suffix('.tmp'); temp.write_bytes(payload)
assert temp.read_bytes() == payload
os.replace(temp, p)

append_memory(ROOT/'MEMORIA_CENTRAL.md', '''

## Checkpoint 16/09/2026 — provas e controles

[REAL] Quatro fontes positivas compiladas, 34 teoremas auditados no recibo
AUDIT_20260916_083016_642974.json. Duas adulterações recusadas por erros de prova;
NEGATIVE_CONTROLS.json guarda os localizadores. 33 controles numéricos finitos passaram.
Nenhum desses números afirma geometricidade física universal.

Atlas: leitura integral ainda em curso. Cobertura contínua confiável desta retomada:
linhas 211–1944; o começo 1–210 teve saída truncada em chamadas agregadas e deverá
ser conferido em chamada isolada. Não declarar Haja Luz integralmente carregado.
Não copiar o Atlas. O hash de referência está em REQUISITOS.json.

Próximo trabalho formal: ligar a derivada do cociclo matricial existente ao resto
com o sinal correto e explicitar a normalização de Gibbs, sem inventar novo fluxo.
Integrais resolventes/primeira variação estão demonstradas no texto e verificadas
numericamente, mas não foram formalizadas em Lean nesta bancada até este ponto.
Handoff deste objetivo ainda não entregue. Objetivo permanece ativo.
''')
append_memory(ROOT/'REGISTRO_DAS_CONVERSAS.md', '''

16/09/2026 — retomada: confirmadas as duas recusas de adulteração, sem reexecutar
os controles válidos. Usuário será informado do alcance finito/algébrico das provas
e das hipóteses necessárias para a aplicação à teoria física de um diamante.
''')
print(json.dumps({'negative_controls': len(checks), 'checkpoint': stamp}))
