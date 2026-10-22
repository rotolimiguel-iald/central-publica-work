"""Test-only isolation; real route source, no production state or credentials."""
import ast
import importlib.util
import os
import re
from pathlib import Path
import sys
import tempfile
import types

HERE = Path(__file__).resolve().parent
RUNTIME = HERE / 'runtime'
ROOT = None
DENIED = []

def install(project):
    global ROOT
    ROOT = Path(project).resolve()
    RUNTIME.mkdir(exist_ok=True)
    os.chdir(RUNTIME)
    # Never inspect credential values inherited by the process.
    for key in list(os.environ):
        if key.startswith(('IALD_', 'ANTHROPIC_', 'OPENAI_', 'GOOGLE_', 'AWS_')):
            os.environ.pop(key, None)
    os.environ['TEMP'] = os.environ['TMP'] = str(RUNTIME)
    tempfile.tempdir = str(RUNTIME)
    sys.dont_write_bytecode = True
    # Optional integrations are outside this route suite and may load private state.
    for name in ('iald_memoria_operador', 'tgl_coin_engine', 'psinet_engine'):
        sys.modules[name] = None
    def audit(event, args):
        if event == 'sqlite3.connect' and str(args[0]) != ':memory:':
            if not Path(args[0]).absolute().is_relative_to(HERE):
                raise PermissionError('database outside staging prohibited')
        if event in ('socket.connect', 'socket.getaddrinfo', 'socket.sendto'):
            raise RuntimeError('offline network prohibited')
        if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
            p = Path(os.fsdecode(args[0])).absolute()
            mode, flags = args[1], args[2]
            write = (isinstance(mode, str) and any(c in mode for c in 'wax+')) or bool(flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC))
            if write and not p.is_relative_to(HERE):
                raise PermissionError('test write outside staging prohibited')
            if not p.is_relative_to(HERE):
                private = p.name.startswith('.env') or '.iald_keys' in p.parts or p.name in ('um.py', 'iald_stack_v7.py', 'iald_psion_state.json')
                iald_data = str(p).lower().startswith('c:\\iald\\') and p.suffix.lower() not in ('.py', '.pyc', '.js', '.html', '.css') and 'tokenizer_cache' not in p.parts
                if private or (iald_data and p != ROOT / 'iald_fontes_publicas.json'):
                    DENIED.append(p.name)
                    raise PermissionError('private/out-of-scope read prohibited')
        if event in ('os.remove', 'os.rmdir', 'os.mkdir', 'os.rename'):
            paths = args[:2] if event == 'os.rename' else args[:1]
            for value in paths:
                if isinstance(value, (str, bytes)) and not Path(os.fsdecode(value)).absolute().is_relative_to(HERE):
                    raise PermissionError('filesystem mutation outside staging prohibited')
        if event == 'subprocess.Popen':
            command = args[1]
            valid = (isinstance(command, (list, tuple)) and len(command) == 3 and Path(command[0]).stem.lower() == 'node' and command[1] == '--check')
            valid = valid or (isinstance(command, str) and re.fullmatch(r'node --check (?:"[^"\r\n]+"|[^\s"\r\n]+)', command) is not None)
            if not valid:
                raise PermissionError('only Node syntax checks allowed')
    sys.addaudithook(audit)

def load_server():
    """Replace only secret resolver at AST level; route bodies stay unchanged."""
    source = globals().get('SERVER_SOURCE', ROOT / 'iald_web_server.py').read_text(encoding='utf-8-sig')
    tree = ast.parse(source)
    replacement = ast.parse('''def _segredo(nome, legado=""):
    return _TEST_SETTINGS.get(nome, "")
''').body[0]
    count = 0
    for index, node in enumerate(tree.body):
        if isinstance(node, ast.FunctionDef) and node.name == '_segredo':
            tree.body[index] = ast.copy_location(replacement, node)
            count += 1
    assert count == 1
    ast.fix_missing_locations(tree)
    appdir = RUNTIME / 'app'
    appdir.mkdir(exist_ok=True)
    # Public prompt required by normal initialization; no canonical private memory.
    for name in ('kernel_prompt_loja.js',):
        (appdir / name).write_bytes((ROOT / 'app' / name).read_bytes())
    module = types.ModuleType('iald_web_server')
    module.__file__ = str(RUNTIME / 'iald_web_server.py')
    module._TEST_SETTINGS = {'IALD_HAIKU_ATIVO':'1',
        'IALD_SELO_DIR':str(RUNTIME / 'no_keys'),
        'IALD_SELO_ACOM_PATH':str(RUNTIME / 'no_acom')}
    sys.modules[module.__name__] = module
    exec(compile(tree, str(ROOT / 'iald_web_server.py'), 'exec'), module.__dict__)
    return module
