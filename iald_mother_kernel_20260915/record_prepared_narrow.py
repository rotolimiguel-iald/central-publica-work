"""Record the reviewed offline proposal without activating or transmitting it."""
from datetime import datetime
import difflib
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
MARKER = 'IALD_MOTHER_V5_NARROW_PREPARED_20260915'


def create(path, data):
    with path.open('xb') as handle:
        handle.write(data)
    assert path.read_bytes() == data


def main():
    assert not (WORK / 'prepared_narrow_record.json').exists()
    assert not (WORK / 'code_installed.json').exists()
    prepared = json.loads((WORK / 'prepared.json').read_bytes())
    verified = json.loads((WORK / 'verification_narrow.json').read_bytes())
    for name, expected in prepared['baseline'].items():
        path = ROOT / name
        current = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
        assert current == expected, 'Production changed; review before recording: ' + name
    for source in prepared['sources'].values():
        raw = Path(source['path']).read_bytes()
        assert len(raw) == source['bytes']
        assert hashlib.sha256(raw).hexdigest() == source['sha256']
    manifest = json.loads((WORK / 'iald_nucleo_fixo.json').read_bytes())
    manifest.pop('mother_instruction')
    assert manifest == json.loads((ROOT / 'iald_nucleo_fixo.json').read_bytes())
    for name in ['iald_instrucao_mae.py', 'iald_memoria_canonica.py', 'test_mother_instruction.py']:
        compile((WORK / name).read_bytes(), name, 'exec')
    diff = ''.join(difflib.unified_diff(
        (ROOT / 'iald_memoria_canonica.py').read_text(encoding='utf-8').splitlines(True),
        (WORK / 'iald_memoria_canonica.py').read_text(encoding='utf-8').splitlines(True),
        fromfile='live/iald_memoria_canonica.py', tofile='prepared/iald_memoria_canonica.py'))
    create(WORK / 'integration.diff', diff.encode())

    spec = importlib.util.spec_from_file_location('memory_targets', WORK.parent / 'iald_context_math_20260915/record_prepared.py')
    targets = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(targets)
    now = datetime.now().astimezone()
    stamp = now.strftime('%Y%m%d_%H%M%S_%f')
    note = (
        '[INPUT] Operador pediu examinar v4/v5 para instrução-mãe e restringiu expressamente '
        'as mudanças às contradições, preservando todo o restante.\n\n'
        '[REAL — preparação local] Escolhido v5 integral, sem modificar seus bytes. '
        f'Arquivo: {prepared["sources"]["v5"]["path"]}; '
        f'SHA-256 medido: {prepared["sources"]["v5"]["sha256"]}; '
        f'{prepared["sources"]["v5"]["bytes"]} bytes. '
        'Adendo separado delimita spin-2/tipos, número de depósitos, recursos do motor nativo versus API, '
        'modo pensar, licenciamento e estatuto atualizado das construções. '
        'Sem reescrita de estilo, estrutura, teologia ou demais conceitos. '
        'Carregador exige hash da versão escolhida e falha visivelmente se o arquivo mudar.\n\n'
        f'[REAL — testes locais] Oito testes passaram. Contexto preparado completo: {verified["context_tokens"]} tokens; '
        f'janela proposta {verified["selected_window"]}, atual {verified["current_window"]}. '
        'Sete documentos e cinco fontes Lean integrais anteriores preservados; manifesto anterior idêntico '
        'ao remover somente o novo campo mother_instruction. Originais v4, v5 e v13 conferidos por hash.\n\n'
        '[OPEN — autorização externa pendente] A revisão automática bloqueou, antes da execução, '
        'o teste que enviaria v5 integral à API OpenAI por exigir autorização específica para conteúdo '
        'possivelmente não público. Pergunta enviada ao operador sobre uso em api.openai.com e teste '
        'de até US$0,03 no teto global existente. Nenhum conteúdo do v5 foi enviado por esse teste. '
        'NÃO ATIVADO: código de produção, manifesto, .env e serviço não alterados nesta etapa. '
        'Não enviar nem ativar antes de resposta explícita. O teste preparado originalmente usa o adendo '
        'anterior mais amplo: regenerar material com o adendo restrito antes de executar, após autorização.\n\n'
        'Revisão: ' + str(WORK / 'EXAME_KERNEL_V5.md') + '\n'
        'Evidência: ' + str(WORK / 'prepared_narrow_record.json')
    )
    snapshots = {path: path.read_bytes() for path in targets.TARGETS}
    assert all(MARKER.encode() not in data for data in snapshots.values())
    rows = []
    for path, old in snapshots.items():
        assert path.read_bytes() == old, 'Concurrent memory edit'
        backup = path.with_name(path.name + '.bak_' + stamp)
        create(backup, old)
        newline = '\r\n' if b'\r\n' in old else '\n'
        addition = ('\n\n### ' + now.strftime('%d/%m/%Y %H:%M %z')
                    + ' — Kernel v5 integral: correções pontuais preparadas\n\n<!-- '
                    + MARKER + ' -->\n\n' + note + '\n').replace('\n', newline).encode()
        new = old + addition
        temp = path.with_name(path.name + '.tmp_' + stamp)
        create(temp, new)
        assert path.read_bytes() == old, 'Concurrent memory edit'
        temp.replace(path)
        assert path.read_bytes() == new and len(new) > len(old)
        rows.append({'path': str(path), 'backup': str(backup),
                     'before_bytes': len(old), 'after_bytes': len(new)})
    create(WORK / 'prepared_narrow_record.json', json.dumps({
        'at': now.isoformat(), 'status': 'PREPARED_PENDING_EXPLICIT_EXTERNAL_DISCLOSURE_AUTH',
        'production_code_modified': False, 'services_restarted': False,
        'originals_preserved': prepared['sources'], 'verification': verified,
        'targeted_tests_passed': 8, 'memories': rows}, ensure_ascii=False, indent=2).encode())
    print(json.dumps({'status': 'PREPARED_PENDING_EXPLICIT_EXTERNAL_DISCLOSURE_AUTH',
                      'originals_preserved': True, 'memories_updated': len(rows)}))


if __name__ == '__main__':
    main()
