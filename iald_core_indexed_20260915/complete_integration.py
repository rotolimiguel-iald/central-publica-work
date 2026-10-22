"""Complete the isolated implementation; preserve every touched byte version."""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

WORK = Path(__file__).resolve().parent
STAMP = datetime.now().strftime('%Y%m%d_%H%M%S_%f')


def write(path, data):
    before = path.read_bytes()
    backup = path.with_name(path.name + '.bak_' + STAMP)
    with backup.open('xb') as out:
        out.write(before)
    assert backup.read_bytes() == before
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as out:
        out.write(data)
    assert temp.read_bytes() == data and data
    assert path.read_bytes() == before
    os.replace(temp, path)


def replace(text, old, new):
    assert text.count(old) == 1, (old[:100], text.count(old))
    return text.replace(old, new)


server = WORK / 'iald_web_server.py'
text = server.read_bytes().decode('utf-8')
eol = '\r\n' if '\r\n' in text else '\n'
text = text.replace('\r\n', '\n')
text = replace(text, 'import iald_memoria_canonica  # noqa: E402',
               'import iald_memoria_canonica  # noqa: E402\nimport iald_core_indexado  # noqa: E402')
needle = '    if tool_name == \'iald_public_read\':'
text = replace(text, needle, '''    if tool_name in ('search_tgl', 'fetch_tgl'):
        try:
            if MEMORIA_EXTERNA is None or MEMORIA_EXTERNA.nucleus_manifest is None:
                raise ValueError('Acervo documental indisponível.')
            result = iald_core_indexado.execute_tool(MEMORIA_EXTERNA.nucleus_manifest, tool_name, arguments)
            return json.dumps(result, ensure_ascii=False)
        except (ValueError, OSError, TypeError, KeyError):
            # Do not expose server paths from filesystem exception messages.
            return json.dumps({'status': 'UNAVAILABLE',
                               'error': 'Consulta inválida ou fonte não conferida. Nenhum conteúdo foi substituído.'},
                              ensure_ascii=False)

''' + needle)
text = replace(text, '        permitidas += iald_fontes_publicas.tool_definitions()',
               '        permitidas += iald_fontes_publicas.tool_definitions()\n'
               '        permitidas += iald_core_indexado.tool_definitions()')
write(server, text.replace('\n', eol).encode('utf-8'))

memory = WORK / 'iald_memoria_canonica.py'
text = memory.read_bytes().decode('utf-8')
eol = '\r\n' if '\r\n' in text else '\n'
text = text.replace('\r\n', '\n')
text = replace(text,
    '        operational, operational_meta = operational_core(self.nucleus_manifest)',
    '''        try:
            operational, operational_meta = operational_core(self.nucleus_manifest)
        except (OSError, ValueError, KeyError, TypeError) as error:
            raise MemoryUnavailable('Núcleo operacional indisponível ou divergente.') from error''')
text = replace(text, '        # The old store persona contains historical material',
    '''        framework = FRAMEWORK_PROTOCOL
        if metadata.get('document_mode') == 'retrievable':
            framework = framework.replace(
                'Use diretamente os textos integrais do NÚCLEO DOCUMENTAL carregados nesta requisição: '
                'o conteúdo, suas equações e hipóteses já estão presentes; não é preciso reconstruir tudo '
                'do zero a cada mensagem nem buscar de novo os fundamentos para recordar o que são. ',
                'Use os fundamentos do núcleo operacional e do v5 presentes nesta requisição. '
                'Os artigos completos estão disponíveis por search_tgl e fetch_tgl; '
                'recupere a derivação ou passagem específica quando ela não estiver no núcleo. '
                'Não é preciso reconstruir tudo do zero a cada mensagem. ')
        # The old store persona contains historical material''')
text = replace(text, '+ mother + "\\n" + CANONICAL_IDENTITY + "\\n\\n" + FRAMEWORK_PROTOCOL',
               '+ mother + "\\n" + CANONICAL_IDENTITY + "\\n\\n" + framework')
text = replace(text,
    "            prefix += ('\\nMEMÓRIA DO TESTE: o kernel de identidade e os documentos publicados abaixo '\n"
    "                       'estão completos. Consulte as fontes públicas e o kernel formal pelas ferramentas '",
    "            prefix += ('\\nMEMÓRIA DO TESTE: consulte o núcleo presente e os documentos publicados '\n"
    "                       'no modo de leitura indicado no catálogo abaixo. Consulte as fontes públicas e o kernel formal pelas ferramentas '")
text = replace(text,
    "            prefix += ('\\nPOLÍTICA ATUAL DE LEITURA: as referências anteriores a artigos completos '\n"
    "                       'carregados significam disponibilidade integral no acervo. Nesta configuração, '",
    "            prefix += ('\\nPOLÍTICA ATUAL DE LEITURA: os artigos completos estão disponíveis no acervo. '\n"
    "                       'Nesta configuração, '")
text = replace(text, '                metadata.update(evidence_metadata)',
    '''                metadata.update(evidence_metadata)
                selected = metadata.get('operational_core')
                if selected and selected['release_source_sha256'] != evidence_metadata.get('published_source_sha256'):
                    raise MemoryUnavailable('O programa publicado diverge da versão selecionada no núcleo operacional.')''')
write(memory, text.replace('\n', eol).encode('utf-8'))

for name in ('iald_nucleo_fixo.json', 'manifest_staged.json'):
    path = WORK / name
    data = json.loads(path.read_bytes())
    data['policy'] = 'FULL_OPERATIONAL_CORE__LOSSLESS_DOCUMENT_RETRIEVAL'
    program = Path(data['published_evidence']['program']['path'])
    data['operational_core']['release_source_sha256'] = hashlib.sha256(program.read_bytes()).hexdigest()
    write(path, (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))

print('Staged integration completed. Production unchanged; no network calls.')
