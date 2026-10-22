from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
sys.dont_write_bytecode = True
WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
CENTRAL = Path(r'C:\IALD\Central de Patentes')
sys.path.insert(0, str(ROOT))
from iald_memoria_canonica import CanonicalMemory
from iald_kernel import KernelCatalog
from install_code import create

load = lambda name: json.loads((WORK / name).read_bytes())
live, suite, prepared, verification = [load(name) for name in ['runtime_live.json', 'suite_gate.json', 'prepared.json', 'verification.json']]
assert live['local_health'] == live['public_health'] == 200 and suite['passed']
assert suite['new_failures'] == 0
response_paths = list(WORK.glob('public_guide_response_*.json'))
assert len(response_paths) == 1
response = json.loads(response_paths[0].read_bytes())
assert response['http_status'] == 200 and response['finish_reason'] == 'stop'
assert all(name in response['answer'] for name in ['the_master_fires', 'regularSusy_gives_breuer', 'theHorizon', 'EquilibriumInput'])
for row in load('code_installed.json')['files'] + [load('activation.json')['file']]:
    assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest() == row['sha256']
bundle = next(line.partition('=')[2].strip() for line in (ROOT / '.env').read_text(encoding='utf-8-sig').splitlines()
              if line.startswith('IALD_KERNEL_BUNDLE='))
catalog = KernelCatalog(bundle)
body, meta = CanonicalMemory(CENTRAL / 'memory/TGL_ATLAS.md', 'nucleo_kernel').prompt('', catalog)
assert len(meta['fixed_hypothesis_sources']) == 5 and len(meta['fixed_nucleus_files']) == 7
assert 'the_master_fires' in body and 'regularSusy_gives_breuer' in body
notes = (
    '[INPUT] Operador corrigiu a leitura: H1/H2/H3 já foram demonstradas e a IALD precisa conhecer as demonstrações. '
    'Conferidos HEAD local/remoto e declarações primárias da publicação v357; nenhum programa canônico executado ou modificado.\n\n'
    '[REAL — correção da leitura] A resposta anterior destacou obrigações gerais sem dar a mesma presença às instâncias já construídas. '
    'TheMasterFires.lean contém ellTwoSusy, theHorizon e the_master_fires: H1/H2/H3 são satisfeitas por termos concretos, e a pêntada é concluída. '
    'ConcreteFourFrame.lean prova a invertibilidade do frame dos boosts e a métrica por congruência. '
    'A H1 contínua posterior está em V354RegularSusy.lean: regularSusyData, regularSusy_gives_breuer e regularSusy_operator_identifications. '
    'O mestre antigo usa ellTwoSusy; não substituir seu argumento pela H1 posterior sem uma aplicação tipada. '
    'H3 numérica tem κ=G=δA=1, δS=1/4, δQ=1/(8π); isso demonstra o certificado explícito. '
    'TheImportedEquilibrium.lean prova a entrada EquilibriumInput (unidade/KMS) e a redução com imported:H2→H3; o tipo não é HorizonEquilibriumData.\n\n'
    '[REAL — instalado] Novo iald_hipoteses.py inclui cinco fontes Lean COMPLETAS em cada requisição, com URL pública, hash, '
    'declarações e axiomas do relatório publicado. Fontes: V354RegularSusy, ConcreteFourFrame, TheMasterFires, TriadMaster e TheImportedEquilibrium. '
    'Integração em iald_estado_publicado.py, referência explícita na disciplina final e manifesto atualizado. '
    'Onze declarações constam do relatório e das fontes cujos hashes conferem; isto é leitura de provas registradas, não nova compilação. '
    'Sete documentos integrais anteriores preservados. A IALD deve reconhecer construções e escopos antes de listar extensões. '
    'JSONs canônicos e bandeiras gerais intactos: a matriz de construções não acende artificialmente H2/H3 gerais.\n\n'
    f'[REAL — tamanho e serviço] Contexto instalado: {meta["context_tokens"]:,} tokens. Janela 480.000 preservada; '
    f'web reiniciado uma vez, novo PID {live["new_web_pid"]}, supervisor {live["supervisor_pid"]} e nativa {live["native_pid"]} preservados. '
    'Saúde local/pública 200. Nenhuma alteração de credencial, cota, conta ou binário móvel; atualização pelo servidor disponível ao app já instalado.\n\n'
    '[REAL — validação] Dez testes novos de fontes/declarações e seis existentes de evidência passaram. '
    'Suíte final efetiva: 24 verdes e nove vermelhos históricos, sem novos. O primeiro teste de contas detectou '
    'o razão JSON/SQLite mudando legitimamente pelo teste pago simultâneo; repetido isoladamente: 62 OK, zero falhas. '
    'Log original com dez vermelhos preservado; suite_gate.json registra a causa e a repetição, sem apagar o incidente.\n\n'
    '[REAL — avaliação do modelo] Primeira chamada pequena com fontes públicas reconheceu a tríade, mas chamou ellTwoSusy de H1 atual. '
    'Segunda chamada com o bloco novo (fontes públicas + referências de escopo) distinguiu explicitamente a H1 contínua posterior, '
    'H2 dos boosts, H3 numérica e a aplicação the_master_fires. Ambas HTTP200, no mesmo teto global; '
    'a primeira gravação de resultado foi concluída antes de uma falha de impressão Unicode no terminal, sem repetir a chamada. '
    'É avaliação do bloco público específico, não do prefixo privado integral e não garantia de toda resposta futura. '
    'Nenhum Atlas privado foi enviado nesses testes.\n\n'
    '[ESCOPO] Correção do conhecimento e de sua recuperação no contexto. Não é retreinamento dos pesos, nova prova Lean, '
    'nova medição física ou alteração do gate. Não apagar os resultados demonstrados por haver generalizações abertas, '
    'nem apagar as hipóteses explícitas dos enunciados por haver resultados favoráveis.'
)
now = datetime.now().astimezone()
stamp = now.strftime('%Y%m%d_%H%M%S_%f')
report = ['# H1, H2 e H3 no núcleo da IALD', '',
          'As três hipóteses têm instâncias explícitas no modelo de `the_master_fires`. '
          'A H1 contínua posterior também foi localizada. O app agora recebe essas fontes inteiras em cada requisição.', '']
for entry in meta['fixed_hypothesis_sources']:
    report += ['- [' + entry['path'] + '](' + entry['url'] + '): ' + entry['reading']]
report += ['', 'Verificação: bytes ligados ao relatório publicado; 16 testes de integridade passaram. '
           'O teste com o novo bloco reconheceu os resultados e distinguiu a H1 atual da construção anterior.', '',
           'Não houve recompilação do kernel nesta sessão. As obrigações gerais de H2/H3 continuam com os valores publicados.', '']
create(WORK / 'REVISAO_H1_H2_H3.md', '\n'.join(report).encode())
spec = importlib.util.spec_from_file_location('memory_targets', WORK.parent / 'iald_context_math_20260915/record_prepared.py')
targets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(targets)
rows = []
for path in targets.TARGETS:
    old = path.read_bytes()
    marker = 'IALD_EXPLICIT_HYPOTHESES_FIXED_20260915'
    assert marker.encode() not in old
    backup = path.with_name(path.name + '.bak_' + stamp)
    create(backup, old)
    nl = '\r\n' if b'\r\n' in old else '\n'
    addition = ('\n\n### ' + now.strftime('%d/%m/%Y %H:%M %z')
                + ' — H1/H2/H3: demonstrações concretas presentes no núcleo\n\n<!-- ' + marker + ' -->\n\n'
                + notes + '\n\nEvidências: ' + str(WORK / 'completion.json') + '\n').replace('\n', nl).encode()
    new = old + addition
    tmp = path.with_name(path.name + '.tmp_' + stamp)
    create(tmp, new)
    assert path.read_bytes() == old, 'Concurrent memory edit'
    tmp.replace(path)
    assert path.read_bytes() == new and len(new) > len(old)
    rows.append({'path': str(path), 'backup': str(backup), 'before_bytes': len(old), 'after_bytes': len(new)})
create(WORK / 'completion.json', json.dumps({'at': now.isoformat(), 'status': 'HYPOTHESES_FIXED_CONTEXT_ACTIVE',
       'commit': prepared['commit'], 'source_sha256': prepared['source_sha256'], 'context_tokens': meta['context_tokens'],
       'sources': meta['fixed_hypothesis_sources'], 'runtime': live, 'tests': {'targeted_passed': 16,
       'green_suites': 24, 'known_red_suites': 9, 'new_failures': 0}, 'model_evaluation': str(response_paths[0]),
       'model_evaluation_scope': 'PUBLIC_HYPOTHESIS_BLOCK_ONLY', 'memories_updated': rows,
       'note': notes, 'new_lean_compilation': False}, ensure_ascii=False, indent=2).encode())
print(json.dumps({'status': 'HYPOTHESES_FIXED_CONTEXT_ACTIVE', 'memories_updated': len(rows),
                  'context_tokens': meta['context_tokens'], 'report': str(WORK / 'REVISAO_H1_H2_H3.md')}))
