"""Consolidate the formally checked JS result without modifying the source archive."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
assert ROOT.name == 'Chatgpt'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def new_file(path, data):
    assert not path.exists(), path
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(data)
    assert temp.stat().st_size == len(data) > 0
    temp.rename(path)

def append_with_backup(name, text):
    path = ROOT / name
    before = path.read_bytes()
    backup = path.with_name(path.name + '.bak_' + stamp)
    new_file(backup, before)
    assert backup.read_bytes() == before
    after = before + text.encode('utf-8')
    temp = path.with_name(path.name + '.append_' + stamp)
    new_file(temp, after)
    assert len(after) > len(before)
    temp.replace(path)
    assert path.read_bytes() == after
    return {'file':name, 'backup':backup.name, 'backup_sha256':sha(backup), 'new_sha256':sha(path)}

proofs = []
for name in ['LocalTowerProjections','ModulatorSelfAdjoint','ModulatorPositive','ModulatorPolar']:
    source = ROOT / (name + '.lean')
    metadata_path = sorted(ROOT.glob(name + '.*.json'))[-1]
    metadata = json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    assert metadata['exit_code'] == 0 and metadata['source_stable'], metadata
    assert metadata['proof_sha256'] == sha(source), name
    log = (ROOT / metadata['log']).read_text(encoding='utf-8-sig')
    assert not any(word in log for word in ['sorryAx','error:','warning:']), log
    code = source.read_text(encoding='utf-8-sig')
    assert not re.search(r'\b(sorry|admit|axiom)\b',code), name
    proofs.append({'module':name, 'source_sha256':sha(source),
                   'olean_sha256':sha(ROOT/(name+'.olean')),
                   'theorems':len(re.findall(r'^theorem ',code,re.M)),
                   'verification':metadata_path.name, 'log':metadata['log']})

manifest = json.loads((ROOT/'manifesto_fontes.json').read_text(encoding='utf-8-sig'))
rows = []
for entry in manifest:
    try:
        current = sha(Path(entry['source']))
        rows.append({'source':entry['source'], 'initial_sha256':entry['sha256'],
                     'current_sha256':current,'unchanged':current == entry['sha256'].upper()})
    except OSError as exc:
        rows.append({'source':entry['source'],'unchanged':False,'error':str(exc)})
changed = sum(not row['unchanged'] for row in rows)
preservation_name = f'preservacao_polar_{stamp}.json'
new_file(ROOT/preservation_name,json.dumps({'files':len(rows),'changed_or_unreadable':changed,
         'rows':rows},ensure_ascii=False,indent=2).encode())
assert changed == 0, 'Original source mismatch; preservation result records the failure'

note = '''

## ADENDO — 05/09/2026: JS positivo e auto-adjunto agora verificado no Lean

[REAL — Lean] A continuação provou `JS_positive_selfadjoint` para o próprio `closedModulatorCandidate P`, no domínio completo. `LocalTowerProjections.lean` constrói as projeções ortogonais dos andares e sua convergência. `ModulatorSelfAdjoint.lean` caracteriza o gráfico inteiro por testes locais e prova igualdade com o adjunto. `ModulatorPositive.lean` passa a forma quadrática positiva local ao limite em norma de gráfico. `ModulatorPolar.lean` prova injetividade, imagem densa e reúne a fatoração S=J(JS) com parte positiva auto-adjunta.

Esta rota supera a pendência de formalizar uma base infinita para obter positividade e auto-adjunticidade: a conclusão foi verificada sem precisar dessa representação. A demonstração escrita por diagonalização continua disponível. [OPEN — Lean] O objeto Δ no domínio do quadrado, a identidade com S†S e o cálculo espectral ainda não foram tipados nesta bancada. A reconstrução geométrica e as hipóteses físicas continuam abertas.

O estado atual e as provas estão descritos em `FECHO_FORMAL_JS.md`. As verificações finais dos quatro módulos retornaram código 0, sem avisos ou sorryAx. Os principais teoremas imprimiram somente propext, Classical.choice e Quot.sound. Os metadados consolidam hashes lidos dos fontes e dos objetos compilados. Não houve selo canônico, aprovação independente nem alteração dos originais ou das memórias canônicas.
'''
updates = [append_with_backup(name,note) for name in ['RELATORIO.md','JS_POSITIVO_AUTOADJUNTO.md']]
updates.append(append_with_backup('RECONSTRUCAO_GRAVITACIONAL_GERAL.md','''

## ADENDO — 05/09/2026: avanço formal da análise modular

[REAL — Lean] A parte positiva JS agora tem positividade, auto-adjunticidade, injetividade, imagem densa e fatoração S=J(JS) verificadas sobre a torre completa. Consulte `FECHO_FORMAL_JS.md`. Esse resultado atualiza a primeira linha da tabela de pontes acima. As obrigações de localização, dimensão, assinatura, escala e correspondência termodinâmica permanecem [OPEN]; elas não são consequências automáticas da análise funcional concluída.
'''))
result = {'timestamp':datetime.now().isoformat(),'proofs':proofs,
          'new_theorems':sum(item['theorems'] for item in proofs),
          'JS_positive_selfadjoint_formalized':True,'polar_characterization_formalized':True,
          'Delta_square_and_spectral_calculus_formalized':False,
          'physical_gravity_reconstruction_complete':False,
          'originals_checked':len(rows),'originals_changed':changed,
          'preservation':preservation_name,'memory_updates_in_workbench':updates,
          'current_report':'FECHO_FORMAL_JS.md','current_report_sha256':sha(ROOT/'FECHO_FORMAL_JS.md')}
new_file(ROOT/f'verificacao_polar_{stamp}.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(result,ensure_ascii=False,indent=2))
