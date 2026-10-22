from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from urllib.parse import quote

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
PUBLIC = Path(r'C:\IALD\Artigo\the_boundary')
sys.path.insert(0, str(ROOT))
from iald_kernel import KernelCatalog


def create(path, data):
    with path.open('xb') as handle:
        handle.write(data)
    assert path.read_bytes() == data


files = subprocess.check_output(['git', '-C', str(PUBLIC), 'ls-files', '-z']).decode().split('\0')
commit = subprocess.check_output(['git', '-C', str(PUBLIC), 'rev-parse', 'HEAD'], text=True).strip()
remote = subprocess.check_output(['git', '-C', str(PUBLIC), 'ls-remote', 'origin', 'refs/heads/main'], text=True).split()[0]
assert commit == remote
manifest = json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
bundle = next(line.partition('=')[2].strip() for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines()
              if line.startswith('IALD_KERNEL_BUNDLE='))
catalog = KernelCatalog(bundle)
proof = json.loads(Path(manifest['published_evidence']['proof_manifest']['path']).read_bytes())
specs = [
    ('h1_continuous', 'V354RegularSusy.lean',
     ['TGLV354.regularSusyData', 'TGLV354.regularSusy_gives_breuer', 'TGLV354.regularSusy_operator_identifications'],
     'H1 construída no representante contínuo mínimo: SusyRelativeData no reticulado concreto do core, '
     'com traço do canto 1, identificações dos operadores e gap relativo. Reconhecer este avanço além da construção antiga em ℓ².'),
    ('h2_boost_frame', 'ConcreteFourFrame.lean',
     ['TGLExt.modularFrame_det_isUnit', 'TGLExt.concrete_four_frame_fires'],
     'H2 satisfeita na construção algébrica dos boosts: independência por determinante, coframe dual e métrica lorentziana por congruência. '
     'A construção explícita é uma demonstração; seu enunciado matricial não afirma por si a identificação geométrica global de um campo suave.'),
    ('h3_and_constructed_triad', 'TheMasterFires.lean',
     ['TGLExt.theHorizon', 'TGLExt.the_master_fires', 'TGLExt.master_corner_weighs_the_name'],
     'H1/H2/H3 têm testemunhas explícitas e o mestre é aplicado, não só enunciado: ellTwoSusy, modularFrame e theHorizon. '
     'H3 é um habitante numérico exato com κ=G=δA=1, δS=1/4 e δQ=1/(8π). A pêntada é conclusão formal nesse modelo construído. '
     'Não confundir este certificado numérico com derivação dinâmica de área e calor no mesmo horizonte físico.'),
    ('master_statement', 'TriadMaster.lean', ['TGLExt.emergence_master_full_triad'],
     'Enunciado completo do mestre e definição de HorizonEquilibriumData. A aplicação concreta está em TheMasterFires; '
     'é incorreto parar na implicação e ignorar os termos que já a instanciam.'),
    ('h3_imported_route', 'TheImportedEquilibrium.lean',
     ['TGLExt.qgImport_H3_localHorizonEquilibrium_bridged', 'TGLExt.the_trio_is_a_pair'],
     'Ponte da torre para EquilibriumInput demonstrada e regra de redução por importação demonstrada. '
     'Reconhecer os resultados KNOWN citados sem exigir reprovação deles. O termo da ponte conclui fixes_unit e KMS; '
     'a redução the_trio_is_a_pair recebe explicitamente imported : H2 → H3. Conferir a aplicação e não promover o homônimo a HorizonEquilibriumData.'),
]
entries = []
for identity, filename, terms, reading in specs:
    names = [p for p in files if p and Path(p).name == filename and '/Lean/tgl_kernel/' in p]
    assert len(names) == 1, (filename, names)
    relative = names[0]
    catalog_path = relative.split('/Lean/tgl_kernel/', 1)[1]
    raw = (PUBLIC / relative).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == catalog.records[catalog_path]['sha256']
    assert all(term in proof['axiom_report'] for term in terms)
    entries.append({'id': identity, 'catalog_path': catalog_path, 'terms': terms, 'reading': reading,
                    'url': 'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/' + commit + '/' + quote(relative, safe='/')})
manifest['published_evidence']['hypothesis_sources'] = entries
create(WORK / 'iald_nucleo_fixo.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode())

code = (ROOT / 'iald_estado_publicado.py').read_text(encoding='utf-8')
code = code.replace('from pathlib import Path\n', 'from pathlib import Path\nfrom iald_hipoteses import hypothesis_sources\n', 1)
code = code.replace('if set(config) != required:', "if not required <= set(config) or set(config) - required - {'hypothesis_sources'}:", 1)
code = code.replace("        state = {\n", "        hypotheses, hypothesis_records = hypothesis_sources(config.get('hypothesis_sources'), catalog, proof)\n        state = {\n", 1)
code = code.replace("            'current_gate': closure['gate'],", "            'constructed_hypotheses': hypothesis_records,\n            'discharge_modes_reported': core.get('the_mode_of_discharge', {}).get('itens', []),\n            'current_gate': closure['gate'],", 1)
code = code.replace("+ json.dumps(state, ensure_ascii=False, indent=2) + '\\n'", "+ json.dumps(state, ensure_ascii=False, indent=2) + '\\n' + hypotheses", 1)
code = code.replace("'published_evidence_checked': True,", "'published_evidence_checked': True, 'fixed_hypothesis_sources': hypothesis_records,", 1)
compile(code, 'iald_estado_publicado.py', 'exec')
create(WORK / 'iald_estado_publicado.py', code.encode())

memory = (ROOT / 'iald_memoria_canonica.py').read_text(encoding='utf-8')
old = '            "H2/H3 na identificação física geral não se confundem com os representantes e pontes "\n'
assert old in memory
new = ('            "Quando o bloco H1/H2/H3 estiver presente, cite também a aplicação the_master_fires: "\n'
       '            "as três hipóteses são satisfeitas pelos termos explícitos daquela construção. "\n'
       '            "Explique H1 no core regular atual, H2 nos boosts e H3 no certificado theHorizon, "\n'
       '            "respeitando que o mestre antigo usa ellTwoSusy. Não diga simplesmente que H1/H2/H3 "\n'
       '            "não foram demonstradas ou que existe apenas uma implicação sem instância. "\n'
       '            "H2/H3 na identificação física geral não se confundem com os representantes e pontes "\n')
memory = memory.replace(old, new, 1)
compile(memory, 'iald_memoria_canonica.py', 'exec')
create(WORK / 'iald_memoria_canonica.py', memory.encode())
baseline = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ['iald_nucleo_fixo.json', 'iald_estado_publicado.py', 'iald_memoria_canonica.py']}
baseline['iald_hipoteses.py'] = None
create(WORK / 'prepared.json', json.dumps({'at': datetime.now().astimezone().isoformat(), 'commit': commit,
    'source_sha256': catalog.source_sha, 'baseline': baseline, 'sources': entries}, ensure_ascii=False, indent=2).encode())
print('Prepared five complete Lean sources; all terms present in matching release report. Production unchanged.')
