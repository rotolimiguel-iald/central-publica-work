"""Append measured runtime status with immediate byte backups and CAS writes."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import tempfile

root = Path(__file__).parent
now = datetime.now().astimezone()
stamp = now.strftime('%Y%m%d_%H%M%S')
bundle = next((root / 'bundles').glob('kernel-*'))
manifest = json.loads((bundle / 'kernel_manifest.json').read_bytes())
catalog_count = len(manifest['files'])
lean_count = sum(r['path'].endswith('.lean') for r in manifest['files'])
initial = json.loads((root / 'behavior_evaluation_20260914_165018.json').read_bytes())
holdout = json.loads((root / 'behavior_evaluation_20260914_165350.json').read_bytes())
spend = sum(r['usd'] for r in holdout['spending'])
stage_hashes = {name: hashlib.sha256((root / 'stage' / name).read_bytes()).hexdigest()
                for name in ('iald_motores.py', 'iald_web_server.py', 'iald_kernel.py',
                             'iald_memoria_canonica.py', 'iald_retrieval.py', 'iald_orcamento.py')}

entry = f'''

### {now.strftime('%d/%m/%Y %H:%M %z')} — IALD como índice: integração OpenAI preparada; implantação aguarda conciliação

[INPUT] Tipagem exigida pelo operador: **TGL = ATLAS; IALD = ÍNDICE(TGL)**. Modo autorizado: núcleo permanente + kernel inteiro + consulta ao Atlas. A definição central está em `iald_memoria_canonica.py`; o núcleo deriva §I e §VII do Atlas canônico a cada mudança da fonte. Não foi criada cópia do Atlas.

[REAL — fontes empacotadas e verificadas] Pacote derivado de `um.py`: {catalog_count} arquivos, {lean_count} fontes Lean; SHA-256 da origem lido no manifesto: `{manifest['source_sha256']}`. Consulta paginada de todo o conjunto, busca local por trechos com acentos/flexões e leitura de recibos de compilação. Uma fonte Lean selecionada foi recompilada com Lean 4.31.0 e axiomas reportados; não houve recompilação integral do kernel nem mudança de gate físico.

[REAL — testes via API] `gpt-5-nano` produziu erros conceituais e citações inexatas nos ensaios, inclusive com esforço medium. `gpt-5.6-luna` com `reasoning_effort=none` respondeu corretamente à tipagem central, à distinção Face/projeção e ao escopo de `iald_is_idempotent`, usando fontes e recibo. O segundo conjunto corrigiu a inversão índice/Atlas e recusou inventar fonte inexistente. **Lacuna observada:** chamou indevidamente de finito o `Basis` de `TheAtlasIndex.lean`; o enunciado não impõe finitude. Foi acrescentada instrução para ler as hipóteses formais sem importar restrições de comentários; essa correção específica ainda precisa de novo ensaio real. Seis sondas não demonstram equivalência a treinamento. Soma conservadora registrada nos testes de comportamento até este recibo: US$ {spend:.8f}.

[REAL — restrição da API] A API recusou `gpt-5.6-luna` + ferramentas + `reasoning_effort=low` em Chat Completions (HTTP 400), orientando `none` ou Responses. A chave existente só autoriza Chat Completions e expira em 14/10/2026. Seu segredo não consta destes registros. A permissão de Moderations/Responses não foi concedida nem alterada.

[REAL — código preparado] 217 verificações de motor, 70 de rotas, 11 de catálogo, 12 de memória/orçamento, 5 de rotas canônicas e 4 de recuperação passaram (319 no total) na versão integrada até a primeira captura paralela. O controle SQLite reserva antes de cada chamada; considera cache escrito e sobretaxa de contexto longo do Luna; falha/interrupção mantém a reserva. O perfil proposto usa janela 131072, motor externo Luna e operador nativo, com teto global local de US$ 1/dia. O `.env` não recebeu essa ativação.

[REAL — estado operacional] **NÃO INSTALADO / NÃO REINICIADO / NÃO PUBLICADO.** A conferência recusou a instalação duas vezes porque a sessão paralela alterou os arquivos. A primeira revisão paralela foi integrada por merge de três vias com backups; outra revisão do servidor chegou durante os testes. A pergunta de coordenação foi enviada ao operador. Processo web medido: PID 44296, Python314, início 13/09/2026 18:41:17 -03; 127.0.0.1:8082. Conferir novamente antes de reiniciar. O llama em 8081 não foi tocado.

[OPEN — integração pendente] A revisão paralela mais nova implementa planos, entrada gratuita, moderação e limites. Integrar essa revisão preservando: (a) núcleo e consultas canônicas também no plano gratuito, dentro das cotas; (b) guardas SQLite em cada volta e integração correta das cotas novas; (c) consentimento; (d) compatibilidade da moderação com a chave restrita. Não ativar Moderations supondo permissão existente. A build móvel antiga 13 não tem consentimento; publicar atualização compatível antes de mudar o motor de todos os testadores. Hospedagem web continua no PC.

Pacote de trabalho: `C:/IALD/Central de Patentes/work/iald_openai_motor_20260914`. `install_runtime.py` permanece apenas preparado, com comparação de hashes e backup; **não forçar a passagem da conferência**. `incoming_manifest.json` é a primeira revisão paralela e já ficou desatualizado para `iald_web_server.py`. Relatórios de comportamento: `behavior_evaluation_20260914_165018.json` e `behavior_evaluation_20260914_165350.json`. A definição/documentação não altera pesos neurais; a correspondência operacional precisa continuar sendo avaliada.
'''

def append(path, text):
    old = path.read_bytes() if path.exists() else b''
    if old:
        backup = path.with_name(path.name + '.bak_' + stamp)
        backup.write_bytes(old)
        if backup.read_bytes() != old:
            raise RuntimeError('Backup differs: ' + str(path))
    new = old + text.encode('utf-8')
    fd, temporary_name = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    temporary.write_bytes(new)
    if temporary.read_bytes() != new or len(new) <= len(old):
        raise RuntimeError('Write verification failed')
    if path.exists() and path.read_bytes() != old:
        raise RuntimeError('Concurrent memory edit: ' + str(path))
    os.replace(temporary, path)
    if path.read_bytes() != new:
        raise RuntimeError('Final memory verification failed')
    print(str(path) + ': appended and verified')

for path in [Path('C:/IALD/Central de Patentes/memory/TGL_ATLAS.md'),
             Path('C:/IALD/Central de Patentes/memory/TGL_INDICE_VIVO.md'),
             Path('C:/IALD/projetos_pyhton/IALD/CLAUDE.md'),
             Path('C:/IALD/projetos_pyhton/IALD/iald-app/HANDOFF_MOTOR_OPENAI_20260914.md')]:
    append(path, entry)
append(root / 'HANDOFF_RUNTIME.md', '# Retomada da integração da IALD\n' + entry + '\nHashes da versão preparada, lidos do disco:\n```json\n' + json.dumps(stage_hashes, indent=2) + '\n```\n')
