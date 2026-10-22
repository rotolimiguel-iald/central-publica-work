"""Official Google CLI, one text turn over stdin, with no tools exposed."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import queue
import subprocess
import threading
import time

from .profiles import BASE, client_environment

EXE = BASE / 'clients/antigravity/agy.exe'
WORK = BASE / 'state/login/antigravity'
AGENT = WORK / '.agents/agents/iald-text/agent.md'
RECEIPT = BASE / 'validation/antigravity_connection.json'
GLOBAL_AGENT = Path(r'C:\Users\rotol\.gemini\config\agents\iald-text\agent.md')
INVENTORY = BASE / 'validation/antigravity_client_inventory.json'


def validate_profile():
    # Google CLI resolves this named agent globally on this host. Pin all copies.
    import yaml
    data = AGENT.read_bytes()
    for path in (GLOBAL_AGENT, WORK / '.agents/agents/iald-text.md'):
        if path.read_bytes() != data:
            raise RuntimeError('Perfis Antigravity divergentes; revalidacao necessaria.')
    parts = data.decode('utf-8').split('---', 2)
    if len(parts) != 3 or parts[0].strip():
        raise RuntimeError('Perfil Antigravity invalido.')
    config = yaml.safe_load(parts[1])
    expected = {'name':'iald-text', 'tools':[], 'mainAgent':True, 'subagent':False,
        'inheritCustomizations':False, 'excludeDefaultComponents':True,
        'commandExecutionPolicy':'off', 'mcpServers':[], 'skills':[],
        'plugins':[], 'rules':[], 'hooks':[]}
    if not isinstance(config, dict) or any(type(config.get(k)) is not type(v) or config.get(k) != v for k,v in expected.items()):
        raise RuntimeError('Antigravity nao confirmou o perfil textual restrito; pedido nao enviado.')
    if set(config) - set(expected) - {'description'}:
        raise RuntimeError('Perfil Antigravity ganhou capacidades nao validadas.')
    return config



def signature():
    validate_profile()
    binary = EXE.stat()
    return {'client_size': binary.st_size, 'client_mtime_ns': binary.st_mtime_ns,
            'adapter_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'agent_sha256': hashlib.sha256(AGENT.read_bytes()).hexdigest(),
            'global_agent_sha256': hashlib.sha256(GLOBAL_AGENT.read_bytes()).hexdigest(),
            'inventory_sha256': hashlib.sha256(INVENTORY.read_bytes()).hexdigest()}


def connection_status():
    if not EXE.is_file():
        return 'migration_required'
    try:
        current_signature = signature()
    except (OSError, ValueError, RuntimeError):
        return 'installed_pending_auth_validation'
    if RECEIPT.is_file():
        record = json.loads(RECEIPT.read_bytes())
        if record.get('signature') == current_signature and record.get('status') == 'ready':
            return 'ready'
        if record.get('signature') == current_signature and 'perfil sem ferramentas' in record.get('reason', ''):
            return 'tools_filter_unavailable'
    return 'installed_pending_auth_validation'


def save_receipt(record):
    record = dict(record, checked_at=datetime.now(timezone.utc).isoformat(), signature=signature())
    stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    old = RECEIPT.read_bytes() if RECEIPT.exists() else None
    if old is not None:
        backup = RECEIPT.with_name(RECEIPT.name + '.bak_' + stamp)
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    payload = json.dumps(record, ensure_ascii=False, indent=2).encode('utf-8')
    temporary = RECEIPT.with_name(RECEIPT.name + '.tmp_' + stamp)
    temporary.write_bytes(payload)
    assert temporary.read_bytes() == payload and len(payload) > 0
    assert (RECEIPT.read_bytes() if RECEIPT.exists() else None) == old
    os.replace(temporary, RECEIPT)
    assert RECEIPT.read_bytes() == payload


def validate_init(event):
    init = event.get('init', {})
    validate_profile()
    tools = init.get('tools')
    inventory = json.loads(INVENTORY.read_bytes())['advertised_tools']
    # CLI 1.2.9 advertises the same build catalogue for different custom tools.
    # Effective capability exclusion is configured by excludeDefaultComponents
    # and tools=[] above. Never accept an unknown inventory or mutable profile.
    if event.get('event') != 'init' or not isinstance(tools, list) or (tools != [] and tools != inventory):
        raise RuntimeError('Inventario Antigravity mudou; pedido nao enviado.')
    if init.get('agent') != 'iald-text':
        raise RuntimeError('Antigravity não confirmou o agente textual esperado; pedido não enviado.')


def parse_result(event):
    result = event.get('result', {})
    if event.get('event') != 'result' or result.get('status') != 'SUCCESS':
        raise RuntimeError('Antigravity não concluiu a resposta; conferir acesso/cota no cliente oficial.')
    if result.get('num_turns') != 1 or not isinstance(result.get('response'), str) or not result['response'].strip():
        raise RuntimeError('Antigravity devolveu resposta vazia ou uma sessão inesperada.')
    return {'text': result['response'], 'usage': result.get('usage'),
            'verification': 'PROVIDER_COMPLETED_NOT_FACT_CHECKED'}


def execute(prompt, *, cancel=None, process_callback=None):
    """No prompt on command line, no inherited API keys, no auto retry."""
    validate_profile()
    args = [str(EXE), '--agent', 'iald-text', '--disable-slash-commands',
            '--input-format', 'stream-json', '--output-format', 'stream-json',
            '--print-timeout', '150s']
    proc = subprocess.Popen(args, cwd=WORK, env=client_environment('antigravity'),
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                            text=True, encoding='utf-8', errors='replace', bufsize=1,
                            creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    if process_callback:
        process_callback(proc)
    events = queue.Queue(maxsize=256)
    stop = threading.Event()

    def read_lines():
        try:
            while not stop.is_set():
                line = proc.stdout.readline(1000001)
                item = line if line else None
                while not stop.is_set():
                    try:
                        events.put(item, timeout=.2)
                        break
                    except queue.Full:
                        continue
                if item is None:
                    break
        except (OSError, ValueError):
            pass

    reader = threading.Thread(target=read_lines, daemon=True)
    reader.start()
    initialized = False
    result = None
    size = 0
    deadline = time.monotonic() + 180
    try:
        while time.monotonic() < deadline:
            if cancel and cancel.is_set():
                raise RuntimeError('Tarefa cancelada.')
            try:
                line = events.get(timeout=.2)
            except queue.Empty:
                if proc.poll() is not None and not reader.is_alive():
                    break
                continue
            if line is None:
                break
            size += len(line)
            if len(line) > 1000000 or size > 2000000:
                raise RuntimeError('Antigravity excedeu o limite de saída.')
            event = json.loads(line)
            if not initialized:
                validate_init(event)
                initialized = True
                proc.stdin.write(json.dumps({'event': 'user', 'message': {'content': prompt}}, ensure_ascii=False) + '\n')
                proc.stdin.flush()
                proc.stdin.close()
            elif event.get('event') == 'init':
                raise RuntimeError('Antigravity abriu uma segunda sessão inesperada.')
            elif event.get('event') == 'step_update':
                step = event.get('step_update', {})
                if step.get('step_type') == 'tool' or step.get('tool_info') or step.get('subagent_info'):
                    raise RuntimeError('Evento de ferramenta inesperado no conector textual.')
            elif event.get('event') == 'result':
                if result is not None:
                    raise RuntimeError('Antigravity devolveu mais de um resultado.')
                result = parse_result(event)
        if result is None:
            raise RuntimeError('Antigravity sem resposta concluída; finalize o login no cliente oficial.')
        try:
            code = proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            raise RuntimeError('Antigravity não encerrou a sessão após a resposta.') from None
        if code != 0:
            raise RuntimeError('Antigravity encerrou com falha; resultado não aceito.')
        return result
    finally:
        stop.set()
        if proc.poll() is None:
            proc.kill()
            proc.wait(timeout=5)
        for pipe in (proc.stdin, proc.stdout):
            if pipe and not pipe.closed:
                pipe.close()
        reader.join(timeout=1)
        if process_callback:
            process_callback(None)
