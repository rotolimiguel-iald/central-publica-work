"""Offline fixtures from real public schemas; no server import or credentials."""
import ast
import json
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import urlparse
from claude_memory_package import load_package
from claude_context_snapshot import load_snapshot

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
STAGE = WORK / 'claude_routes_stage_20260922_154903_859968/iald_web_server.py'
PACKAGE_DIR = WORK / 'haiku_package_20260922_141841_074636'

def definitions_module(name):
    source = ROOT / (name + '.py')
    tree = ast.parse(source.read_text(encoding='utf8'))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'tool_definitions']
    assert len(nodes) == 1
    namespace = {'__file__': str(source), 'Path': Path, 'json': json, 'urlparse': urlparse}
    if name == 'iald_fontes_publicas':
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ('tool_definitions', 'catalog')]
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(source), 'exec'), namespace)
    return SimpleNamespace(tool_definitions=namespace['tool_definitions'])

KERNEL = definitions_module('iald_kernel')
PUBLIC = definitions_module('iald_fontes_publicas')
CORE = definitions_module('iald_core_indexado')

def definitions():
    return KERNEL.tool_definitions() + PUBLIC.tool_definitions() + CORE.tool_definitions()

def measured():
    return load_snapshot(PACKAGE_DIR, load_package)

def extract(names, namespace):
    tree = ast.parse(STAGE.read_text(encoding='utf8'))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names]
    assert len(nodes) == len(names)
    for node in nodes:
        node.decorator_list = []
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(STAGE), 'exec'), namespace)
