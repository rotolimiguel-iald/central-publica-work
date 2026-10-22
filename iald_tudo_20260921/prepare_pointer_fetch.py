"""Prepare JSON-pointer retrieval in the existing published-document tool."""
import hashlib
import json
from pathlib import Path
from build_haiku_candidate import store

ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
WORK = Path(__file__).resolve().parent
source = ROOT / 'iald_core_indexado.py'
before = source.read_bytes()
text = before.decode('utf-8')
newline = '\r\n' if '\r\n' in text else '\n'
text = text.replace('\r\n', '\n')
helper = '''def json_pointer_value(text, pointer):
    """Resolve RFC6901 against a verified published JSON document only."""
    if not isinstance(pointer, str) or len(pointer) > 2000 or (pointer and not pointer.startswith('/')):
        raise ValueError('Ponteiro JSON inválido.')
    node = json.loads(text)
    if pointer == '':
        return node
    for encoded in pointer[1:].split('/'):
        if re.search(r'~(?![01])', encoded):
            raise ValueError('Escape inválido no ponteiro JSON.')
        key = encoded.replace('~1', '/').replace('~0', '~')
        if isinstance(node, dict):
            if key not in node:
                raise ValueError('Campo não localizado na fonte publicada.')
            node = node[key]
        elif isinstance(node, list):
            if not re.fullmatch(r'0|[1-9][0-9]*', key) or int(key) >= len(node):
                raise ValueError('Índice fora da coleção publicada.')
            node = node[int(key)]
        else:
            raise ValueError('Ponteiro atravessa um valor escalar.')
    return node


'''
assert 'def json_pointer_value' not in text
text = text.replace('class DocumentCorpus:', helper + 'class DocumentCorpus:', 1)
old = 'def fetch(self, id, offset=0, max_chars=4000):'
assert text.count(old) == 1
text = text.replace(old, 'def fetch(self, id, offset=0, max_chars=4000, pointer=None):')
old = "        text = doc['text']\n        if not 0 <= offset <= len(text):"
new = """        text = doc['text']
        selected = {}
        if pointer is not None:
            if not doc['name'].endswith('.json'):
                raise ValueError('Ponteiro JSON exige documento JSON publicado.')
            value = json_pointer_value(text, pointer)
            text = json.dumps(value, ensure_ascii=False, separators=(',', ':'))
            selected = {'pointer': pointer, 'offset_scope': 'SELECTED_JSON_VALUE',
                        'value_sha256': hashlib.sha256(text.encode('utf-8')).hexdigest()}
        if not 0 <= offset <= len(text):"""
assert text.count(old) == 1
text = text.replace(old, new)
old = "'whole_document': offset == 0 and end == len(text), 'text': text[offset:end]}"
new = """'whole_document': pointer is None and offset == 0 and end == len(text),
                'whole_selection': offset == 0 and end == len(text),
                'text': text[offset:end], **selected}"""
assert text.count(old) == 1
text = text.replace(old, new)
text = text.replace("'Lê um artigo canônico por id e posição. Siga next_offset para leitura integral sem cortes ocultos.'",
                    "'Lê documento publicado por id e posição; pointer opcional seleciona caminho JSON /core/... . Com pointer, offset e next_offset referem-se ao valor selecionado, não ao arquivo. Uma página não é leitura integral.'")
old = "'max_chars': {'type': 'integer'}},"
assert text.count(old) == 1
text = text.replace(old, "'max_chars': {'type': 'integer'}, 'pointer': {'type': 'string'}},")
text = text.replace("set(arguments) <= {'id', 'offset', 'max_chars'}:",
                    "set(arguments) <= {'id', 'offset', 'max_chars', 'pointer'}:")
after = text.replace('\n', newline).encode('utf-8')
compile(after, str(source), 'exec')
store(WORK / 'iald_core_indexado_candidate.py', after)
store(WORK / 'pointer_fetch_prepared.json', json.dumps({
    'source': str(source), 'before_sha256': hashlib.sha256(before).hexdigest(),
    'after_sha256': hashlib.sha256(after).hexdigest(), 'deployed': False}, indent=2).encode())
print('POINTER_FETCH_PREPARED=true')
