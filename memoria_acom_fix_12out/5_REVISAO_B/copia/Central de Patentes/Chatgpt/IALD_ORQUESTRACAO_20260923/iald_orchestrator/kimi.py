"""Text-only K3 subscription adapter, using the unmodified official Node CLI."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time
import tomllib

from .profiles import BASE, PROFILES, client_environment
from .safe_files import save_json, utc_now

MODEL = 'kimi-code/k3'
CONTEXT_WINDOW = 1048576
OUTPUT_RESERVE = 131072
MAX_INPUT_BYTES = CONTEXT_WINDOW - OUTPUT_RESERVE - 4096
MAX_RESPONSE_BYTES = 32_000_000
PROFILE = PROFILES / 'kimi-apple'
AGENT = Path(__file__).with_name('kimi_text_agent.md')
LAUNCHER = Path(__file__).with_name('kimi_stdin.mjs')
PACKAGE = BASE / 'clients/node_modules/@moonshot-ai/kimi-code'
RECEIPT = BASE / 'validation/kimi_connection.json'


def preflight():
    config = tomllib.loads((PROFILE/'config.toml').read_text(encoding='utf-8'))
    if json.loads((PACKAGE/'package.json').read_bytes())['version'] != '2.0.2':
        raise RuntimeError('Versão Kimi alterada; revalidar o conector.')
    if any(config.get(k) is not False for k in ('auto_session_title', 'builtin_product_skills', 'merge_all_available_skills')):
        raise RuntimeError('Configuração dedicada Kimi não confere.')
    if config.get('telemetry') is not True:
        raise RuntimeError('Kimi telemetry preference differs from operator consent.')
    if config.get('hooks') or config.get('extra_skill_dirs') or config.get('extra_agent_dirs'):
        raise RuntimeError('Extensões inesperadas no perfil Kimi.')
    if config.get('loop_control', {}).get('max_attempts_per_step') != 1:
        raise RuntimeError('Limite de tentativas Kimi não confere.')
    if config.get('background', {}).get('print_background_mode') != 'exit':
        raise RuntimeError('Modo de saída Kimi não confere.')
    if any((PROFILE/name).exists() for name in ('mcp.json', 'plugins', 'settings.json', 'hooks.json')):
        raise RuntimeError('Integrações extras no perfil Kimi exigem revisão.')
    model = config['models'][MODEL]
    if model['provider'] != 'managed:kimi-code' or model['model'] != 'k3':
        raise RuntimeError('Modelo Kimi não corresponde à assinatura validada.')
    if config.get('thinking',{}).get('effort') != 'max' or config.get('thinking',{}).get('enabled') is not True:
        raise RuntimeError('K3 deve usar raciocínio máximo explicitamente habilitado.')
    if model.get('max_context_size') != CONTEXT_WINDOW:
        raise RuntimeError('K3 deve manter a janela de contexto de 1M.')
    header = AGENT.read_text(encoding='utf-8').split('---', 2)[1]
    if not all(line in header.splitlines() for line in ('name: iald-text', 'tools: []', 'subagents: []')):
        raise RuntimeError('Perfil Kimi deve desabilitar ferramentas e delegação.')


def signature():
    paths = [Path(__file__), LAUNCHER, AGENT, Path(__file__).with_name('profiles.py'),
             PACKAGE/'dist/main.mjs', PROFILE/'config.toml']
    return {'profile': str(PROFILE), 'files': {str(p.relative_to(BASE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}}


def connection_status():
    try:
        preflight()
        receipt = json.loads(RECEIPT.read_bytes())
        if receipt.get('status') == 'ready' and receipt.get('signature') == signature():
            return 'ready'
    except (OSError, ValueError, KeyError, RuntimeError):
        pass
    return 'installed_pending_auth_validation'


def save_receipt(record):
    save_json(RECEIPT, dict(record, checked_at=utc_now(), signature=signature()))


def parse_stdout(output):
    """Require the version, one final answer and the post-completion marker."""
    events = [json.loads(line) for line in output.splitlines() if line.strip()]
    if len(events) != 3 or events[0].get('type') != 'system.version' or events[0].get('version') != '2.0.2':
        raise RuntimeError('Sequência de resposta Kimi inesperada.')
    answer, final = events[1:]
    if answer.get('role') != 'assistant' or answer.get('tool_calls') or not isinstance(answer.get('content'), str) or not answer['content'].strip():
        raise RuntimeError('Kimi não devolveu uma resposta textual única.')
    if len(answer['content']) > MAX_RESPONSE_BYTES or final.get('type') != 'session.resume_hint':
        raise RuntimeError('Kimi não confirmou a conclusão da resposta.')
    session = final.get('session_id', '')
    if not re.fullmatch(r'session_[0-9a-f-]{36}', session):
        raise RuntimeError('Identificador de sessão Kimi inválido.')
    return answer['content'], session


def parse_evidence(events):
    """Read only structural/usage fields from the official local session record."""
    bound = snapshots = requests = completions = stops = 0
    usage = {'prompt_tokens': 0, 'completion_tokens': 0, 'cached_input_tokens': 0}
    usage_count = 0
    for e in events:
        kind = e.get('type')
        if kind == 'profile.bind':
            if any(e.get(k) != v for k, v in {'profileName':'iald-text', 'modelAlias':MODEL,
                    'activeToolNames':[], 'subagents':[], 'agentsMdPaths':[]}.items()):
                raise RuntimeError('A sessão Kimi não respeitou o perfil textual isolado.')
            bound += 1
        elif kind == 'llm.tools_snapshot':
            if e.get('tools') != []:
                raise RuntimeError('Ferramentas inesperadas na solicitação Kimi.')
            snapshots += 1
        elif kind == 'llm.request':
            if e.get('model') != 'k3' or e.get('modelAlias') != MODEL:
                raise RuntimeError('Modelo executado diferente de K3.')
            if e.get('thinkingEffort') != 'max':
                raise RuntimeError('Kimi não confirmou raciocínio max na solicitação real.')
            requests += 1
        elif kind == 'usage.record':
            if e.get('usageScope') != 'turn' or e.get('model') != MODEL:
                raise RuntimeError('Consumo Kimi com escopo inesperado.')
            u = e['usage']
            keys = ('inputOther','inputCacheRead','inputCacheCreation','output')
            if not all(type(u.get(k)) is int and u[k] >= 0 for k in keys):
                raise RuntimeError('Consumo Kimi não informado corretamente.')
            usage['prompt_tokens'] += sum(u[k] for k in keys[:3])
            usage['completion_tokens'] += u['output']
            usage['cached_input_tokens'] += u['inputCacheRead']
            usage_count += 1
        elif kind == 'turn.ended':
            if e.get('reason') != 'completed':
                raise RuntimeError('Rodada Kimi incompleta.')
            completions += 1
        elif kind == 'context.append_loop_event':
            event = e.get('event', {})
            if 'finishReason' in event:
                if event.get('finishReason') != 'end_turn' or event.get('rawFinishReason') != 'stop':
                    raise RuntimeError('Resposta Kimi truncada ou sem conclusão.')
                stops += 1
    if (bound, snapshots, requests, completions, stops, usage_count) != (1,1,1,1,1,1):
        raise RuntimeError('Registro Kimi incompleto ou com múltiplas chamadas.')
    usage['total_tokens'] = usage['prompt_tokens'] + usage['completion_tokens']
    return usage


def session_evidence(session):
    matches = list((PROFILE/'sessions').glob(f'*/{session}/agents/main/wire.jsonl'))
    if len(matches) != 1 or matches[0].stat().st_size > 128_000_000:
        raise RuntimeError('Registro local Kimi ausente, ambíguo ou excessivo.')
    with matches[0].open(encoding='utf-8') as stream:
        return parse_evidence(json.loads(line) for line in stream if line.strip())


def execute(prompt, *, cancel=None, process_callback=None):
    from .providers import client_command, ProviderLimitError
    if cancel and cancel.is_set():
        raise RuntimeError('Tarefa cancelada.')
    if not isinstance(prompt,str) or not prompt.strip() or len(prompt.encode('utf-8')) > MAX_INPUT_BYTES:
        raise ValueError('Contexto Kimi excede o envelope técnico de entrada.')
    preflight()
    command = client_command('kimi')
    env = client_environment('kimi')
    if Path(env['KIMI_CODE_HOME']).resolve() != PROFILE.resolve():
        raise RuntimeError('Login Kimi ativo não corresponde ao perfil validado.')
    # Clear runtime injection and temporary model/config overrides; keep official OAuth.
    for key in list(env):
        if key.startswith(('KIMI_', 'NODE_')) and key not in ('KIMI_CODE_HOME', 'KIMI_DISABLE_TELEMETRY'):
            env.pop(key)
    root = BASE/'state/kimi-runs'
    root.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='text-', dir=root) as folder:
        (Path(folder)/'.git').mkdir()
        proc = subprocess.Popen([command[0], str(LAUNCHER)], cwd=folder, env=env,
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding='utf-8', errors='replace',
                                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        if process_callback:
            process_callback(proc)
        deadline = time.monotonic() + 7200
        payload = json.dumps(prompt, ensure_ascii=False)
        try:
            while True:
                if cancel and cancel.is_set():
                    raise RuntimeError('Tarefa cancelada.')
                try:
                    output, diagnostic = proc.communicate(payload, timeout=.25)
                    break
                except subprocess.TimeoutExpired:
                    payload = None
                    if time.monotonic() > deadline:
                        raise RuntimeError('Kimi excedeu 7200 segundos.') from None
            if proc.returncode:
                if any(term in diagnostic.lower() for term in ('429', 'usage limit', 'quota exceeded', 'rate limit')):
                    raise ProviderLimitError('Kimi informou limite de consumo; conferir a assinatura.')
                raise RuntimeError('Kimi encerrou com falha; conferir acesso e cota no cliente oficial.')
            if len(output.encode('utf-8')) > MAX_RESPONSE_BYTES:
                raise RuntimeError('Saída Kimi excessiva.')
            text, session = parse_stdout(output)
            usage = session_evidence(session)
            return {'text': text, 'usage': usage, 'model': MODEL, 'thinking_effort':'max',
                    'context_window':CONTEXT_WINDOW,
                    'verification': 'PROVIDER_COMPLETED_NOT_FACT_CHECKED'}
        finally:
            if proc.poll() is None:
                proc.kill()
            proc.communicate()
            if process_callback:
                process_callback(None)
