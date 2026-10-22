"""Assemble a source-only manifest; read whole texts, never run canonical um.py."""
import hashlib
import json
import os
from pathlib import Path
import sys

WORK = Path(__file__).parent
NATIVE = Path(r'C:\IALD\projetos_pyhton\IALD')
PREVIOUS = WORK.parent / 'iald_openai_motor_20260914'
sys.path[:0] = [str(WORK), str(PREVIOUS / 'dependencies')]
os.environ['TIKTOKEN_CACHE_DIR'] = str(PREVIOUS / 'tokenizer_cache')
from iald_memoria_canonica import CanonicalMemory
from iald_kernel import build_bundle, KernelCatalog
from iald_motores import estimar_tokens


def main():
    manifest_path = WORK / 'iald_nucleo_fixo.json'
    if manifest_path.exists():
        raise RuntimeError('Manifest exists: preserve the prepared version')
    public = Path(r'C:\IALD\Artigo\the_boundary')
    canonical = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
    measurement = json.loads((WORK / 'fixed_kernel_measurement.json').read_bytes())
    rows = measurement['files']
    entries = []
    for name, identifier in [('paper_PT.tex', 'custo_geometrico_integral'),
                             ('A Ponte Einstein Cartan Miguel.tex', 'ponte_integral'),
                             ('README.md', 'readme_publico_integral'),
                             ('read-brief.md', 'indice_publico_dos_conceitos_integral')]:
        matching = [row for row in rows if Path(row['path']).name == name]
        assert len(matching) == 1
        row = matching[0]
        path = public / row['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256'], 'Source changed during preparation'
        entries.append({'id': identifier, 'path': str(path),
                        'role': 'Texto integral da edição publicada; versão conforme o documento. Não é uma execução nova.'})
    for name, identifier in [('um_grande_atrator_pt.txt', 'um_artigo_local_integral'),
                             ('um_grande_atrator_forma_canonica.md', 'um_forma_canonica_integral'),
                             ('um_grande_atrator_selo.json', 'um_selo_local_integral')]:
        entries.append({'id': identifier, 'path': str(canonical / name),
                        'role': 'Artefato integral local gerado pelo um.py; rodada conforme o artefato. Sua leitura não é nova execução.'})
    data = json.dumps({'format': 1, 'policy': 'FULL_TEXT_EVERY_REQUEST__NO_TRUNCATION',
                       'entries': entries}, ensure_ascii=False, indent=2).encode('utf-8')
    temp = manifest_path.with_suffix('.json.tmp')
    temp.write_bytes(data)
    assert temp.read_bytes() == data
    temp.replace(manifest_path)
    # Public navigation configuration already audited in the original integration.
    (WORK / 'iald_fontes_publicas.json').write_bytes((NATIVE / 'iald_fontes_publicas.json').read_bytes())
    bundle = build_bundle(canonical / 'um.py', WORK / 'bundles')
    catalog = KernelCatalog(bundle)
    memory = CanonicalMemory(WORK.parent.parent / 'memory/TGL_ATLAS.md', 'nucleo_kernel')
    prompt, info = memory.prompt('', catalog)
    report = {'kernel': catalog.status(), 'bundle_path': str(bundle),
              'nucleus': info, 'estimated_tokens_by_existing_budget': estimar_tokens(prompt),
              'proposed_window': 400000, 'original_um_executed': False}
    assert info['context_tokens'] + 4096 + 8000 < 400000, 'Actual context exceeds the proposed window'
    assert estimar_tokens(prompt) + 4096 + 8000 < 400000, 'Existing budget estimator rejects the context'
    payload = json.dumps(report, ensure_ascii=False, indent=2).encode('utf-8')
    (WORK / 'nucleus_prepared.json').write_bytes(payload)
    print(json.dumps({k: report[k] for k in ('kernel', 'estimated_tokens_by_existing_budget', 'proposed_window')}))
    print(json.dumps({k: info[k] for k in ('fixed_nucleus_tokens', 'context_tokens', 'fixed_nucleus_complete')}))


if __name__ == '__main__':
    main()
