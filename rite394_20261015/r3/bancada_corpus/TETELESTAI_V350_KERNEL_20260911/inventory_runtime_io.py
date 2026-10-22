"""Inventory syntactic I/O sites without executing or importing the monolith.

This is a conservative list, not a resolution of dynamic paths or runtime clearance.
"""
import ast
import datetime
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'um.py'
raw = SOURCE.read_bytes()
tree = ast.parse(raw)
FILE_CALLS = {'open', 'write_text', 'write_bytes', 'read_text', 'read_bytes',
              'remove', 'unlink', 'rename', 'replace', 'mkdir', 'makedirs',
              'rmtree', 'copy', 'copy2', 'copyfile', 'copytree', 'move', 'chdir',
              'savefig', 'save', 'savetxt', 'savez', 'load', 'loadtxt', 'genfromtxt',
              'to_csv', 'to_json', 'to_excel'}
PREFIXES = ('subprocess.', 'requests.', 'urllib.', 'http.', 'shutil.')
EXACT = {'os.system', 'os.popen', 'eval', 'exec', 'run_process_checked', 'compile_pdf'}
PRIVATE = ('iald_stack_v7', 'iald_psion_state', '.env', 'password', 'api_key', 'token')


def expression(node):
    text = ast.unparse(node)
    if any(word in text.lower() for word in PRIVATE):
        return '[REDACTED_EXPRESSION]'
    return text if len(text) <= 350 else text[:350] + ' [TRUNCATED_EXPRESSION]'


def inventory(parsed, origin):
    rows = []

    class Visitor(ast.NodeVisitor):
        scope = []

        def visit_FunctionDef(self, node):
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        visit_AsyncFunctionDef = visit_FunctionDef

        def visit_ClassDef(self, node):
            self.scope.append(node.name)
            self.generic_visit(node)
            self.scope.pop()

        def visit_Call(self, node):
            name = ast.unparse(node.func)
            leaf = node.func.attr if isinstance(node.func, ast.Attribute) else name
            if leaf in FILE_CALLS or name.startswith(PREFIXES) or name in EXACT:
                rows.append({'origin': origin, 'scope': '.'.join(self.scope) or '<module>',
                             'line': node.lineno, 'callee': name,
                             'args': [expression(arg) for arg in node.args[:3]],
                             'keywords': {kw.arg: expression(kw.value) for kw in node.keywords
                                          if kw.arg in {'cwd', 'mode', 'shell', 'timeout'}}})
            self.generic_visit(node)

    Visitor().visit(parsed)
    return rows


embedded_assignment = next(n for n in tree.body if isinstance(n, ast.Assign) and
    any(isinstance(t, ast.Name) and t.id == '_EMBEDDED_KERNEL_FILES' for t in n.targets))
embedded = ast.literal_eval(embedded_assignment.value)
rows = inventory(tree, 'um.py')
helpers = {}
parse_failures = []
for name, text in embedded.items():
    if not name.endswith('.py'):
        continue
    try:
        helper_tree = ast.parse(text)
    except SyntaxError as error:
        parse_failures.append({'file': name, 'line': error.lineno, 'error': error.msg})
        continue
    helper_rows = inventory(helper_tree, name)
    helpers[name] = {'sha256': hashlib.sha256(text.encode()).hexdigest(),
                     'io_sites': len(helper_rows)}
    rows.extend(helper_rows)
result = {'timestamp': datetime.datetime.now().astimezone().isoformat(),
          'status': 'STATIC_SYNTACTIC_IO_INVENTORY__DYNAMIC_TARGETS_UNRESOLVED__NOT_RUNTIME_CLEARANCE',
          'source_sha256': hashlib.sha256(raw).hexdigest(), 'source_unchanged': SOURCE.read_bytes() == raw,
          'monolith_executed_or_imported': False, 'python_helpers': helpers,
          'parse_failures': parse_failures, 'sites': rows,
          'limitations': ['Call aliases, generated code, imported packages, Lean and TeX I/O are not resolved.',
                          'Arguments are syntax, not resolved absolute write targets.',
                          'Library and process outputs need separate isolation before runtime.']}
assert result['source_unchanged']
target = ROOT / 'runtime_io_inventory.json'
assert not target.exists(), 'Retain this snapshot and choose a new name for a later inventory.'
payload = json.dumps(result, ensure_ascii=False, indent=2).encode()
temp = target.with_suffix('.json.tmp')
with temp.open('xb') as handle:
    handle.write(payload)
assert temp.read_bytes() == payload and len(payload) > 0
temp.replace(target)
assert target.read_bytes() == payload
print(json.dumps({'source_sha256': result['source_sha256'], 'sites': len(rows),
                  'embedded_python_helpers': len(helpers), 'parse_failures': parse_failures,
                  'runtime_clearance': False, 'executed_monolith': False}))
