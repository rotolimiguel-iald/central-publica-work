from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_079_20260910'
REVIEW = ROOT / 'REVISAO_GL_ORTOGONAL_079_20260910_042420_0634935'

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def new_file(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    temp = path.with_name(path.name + '.tmp_new')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

sources = [OUT / 'finalize_delivery079.py', REVIEW / 'PROVENIENCIA_CORRECAO_HELPER_REVISAO_079.json',
           REVIEW / 'measure_review079_v2.py', REVIEW / 'PARECER_GL_ORTOGONAL_079.md',
           REVIEW / 'RECIBO_REVISAO_GL_ORTOGONAL_079.json']
before = [pin(path) for path in sources]
provenance = json.loads(sources[1].read_bytes())
historical = provenance['new_draft']
final = pin(sources[3])
assert not Path(historical['path']).exists()
assert historical['sha256'] == final['sha256'] and historical['bytes'] == final['bytes']
receipt = json.loads(sources[4].read_bytes())
assert receipt['report'] == final
assert 'pending.rename(report)' in sources[2].read_text(encoding='utf-8')
assert not (OUT / 'RESULTADO_ENTREGA_079.json').exists()
assert not (OUT / 'MANIFESTO_ENTREGA_079.json').exists()

old = sources[0].read_text(encoding='utf-8')
needle = "            actual = pin(p)\n"
replacement = '''            if p.is_file():
                actual = pin(p)
            else:
                matches = [row for row in historical_renames['renames']
                           if row['historical'] == value]
                check('missing_path_has_exact_recorded_rename:' + origin, len(matches) == 1)
                row = matches[0]
                actual = pin(row['final']['path'])
                check('renamed_final_pin:' + origin, actual == row['final'])
'''
assert old.count(needle) == 1
new = old.replace(needle, replacement)
needle2 = "snapshot = read_json(OUT / 'ESTADO_CANONICO_079.json')"
assert new.count(needle2) == 1
new = new.replace(needle2, "historical_renames = read_json(OUT / 'RESOLUCAO_RENOME_HISTORICO_079.json')\n" + needle2)
needle3 = "'ADENDO_REVISOES_079.md']"
assert new.count(needle3) == 1
new = new.replace(needle3, "'ADENDO_REVISOES_079.md', 'ADENDO_FINALIZACAO_E_RENOME_079.md']")
ast.parse(new)
new_pin = new_file(OUT / 'finalize_delivery079_renames.py', new.encode('utf-8'))
adendum = '''# Adendo de finalização079 — referência histórica renomeada

10/09/2026. [REAL — verificação documental por bytes].

A primeira execução de `finalize_delivery079.py` terminou com FileNotFoundError antes de
emitir RESULTADO_ENTREGA_079.json ou MANIFESTO_ENTREGA_079.json. O objeto `new_draft` da
proveniência da revisão GL aponta ao temporário PARECER_GL_ORTOGONAL_079.md.pending_v2.
O auxiliar da revisão contém a operação de renome para PARECER_GL_ORTOGONAL_079.md, e o
recibo da revisão aponta ao destino final. O arquivo temporário já não existe.

A leitura atual verifica que o destino final tem exatamente o tamanho e o SHA-256
registrados para aquele temporário. Isso comprova a correspondência de conteúdo; o
histórico de execução do renome é registrado pelo auxiliar e pelo recibo, sem pretender
reproduzir esse evento passado. Não há restauração fictícia de um temporário ausente.

O mapa RESOLUCAO_RENOME_HISTORICO_079.json registra a única resolução autorizada por essa
medição. O finalizador novo só a aceita quando o objeto histórico completo coincide,
o caminho histórico está ausente e o destino final confere byte-count e hash. Qualquer
outra ausência continua sendo erro visível. O finalizador anterior e todas as fontes
permanecem intactos. A primeira tentativa não é contada como sucesso.

Este adendo esclarece a custódia documental; não altera as demonstrações, seus limites,
as contagens CAS/Lean ou o estado canônico. A suficiência geral permanece aberta.
'''
adendum_pin = new_file(OUT / 'ADENDO_FINALIZACAO_E_RENOME_079.md', adendum.encode('utf-8'))
after = [pin(path) for path in sources]
assert before == after
record = {'status': 'EXACT_HISTORICAL_REFERENCE_CONTENT_MATCH',
          'created_utc': datetime.now(timezone.utc).isoformat(),
          'renames': [{'historical': historical, 'final': final}],
          'sources_before': before, 'sources_after': after,
          'originals_preserved': True, 'prior_attempt_succeeded': False,
          'new_finalizer': new_pin, 'adendum': adendum_pin,
          'scope': 'Resolve only this exact absent historical temporary reference by measured final-file identity; the historical rename is not rerun.'}
record_pin = new_file(OUT / 'RESOLUCAO_RENOME_HISTORICO_079.json',
                      (json.dumps(record, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'new_finalizer': new_pin, 'adendum': adendum_pin, 'record': record_pin}, ensure_ascii=True))
