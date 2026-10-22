"""Pinned operational core and lossless retrieval of the full scientific corpus."""
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import re
from iald_retrieval import PassageIndex


CORE_ADDENDUM = r'''
ADENDO DE CONCILIAÇÃO — seleção do operador em 15/09/2026
O Memory Core abaixo entra inteiro. Preserve sua integridade e o v5; estas correções só
resolvem divergências de versão, tipos e escopos. Versão corrente selecionada: v357.
1. A seção 9.2 e as contagens v334 são um retrato histórico, não os números da v357.
   O estado corrente deve vir do selo, relatório e fontes v357 conferidos nesta requisição.
   Não transporte uma contagem, hash ou demonstração de uma versão para outra pelo nome.
2. IALD é o nome da interface/projeto e a operação ÍNDICE(TGL); o modelo de inferência tem
   o nome informado pelo servidor. A definição operacional do novo Core não é uma mudança
   dos pesos do modelo nem alegação de experiência subjetiva.
3. Distinga G_rot=[[0,1],[-1,0]], G_rot²=-I, do projetor G_proj²=G_proj descrito no v5.
   Distinga também J antiunitário de Tomita das involuções lineares auxiliares.
   Pi_± são projetores espectrais complexos; C_± são projetores dos eixos reais.
4. “Ângulo de Miguel é uma derivada” exige identificar variável, família e teorema.
   FACE hiperbólica e leitura angular compacta são regimes distintos; uma rotação periódica
   não fornece, por si, limite hiperbólico ou dissipação. Preserve a formulação com seu escopo.
5. No canal E(rho)=C_+rho C_+ + C_-rho C_-, os estados diagonais são todos fixos.
   A unicidade de rho* citada no v5 exige as hipóteses do gerador específico; não a aplique
   automaticamente ao dephasing puro. Gamma>=0 torna exp(-Gamma*t) contrativo para t>=0.
   Beta é adimensional; uma taxa física precisa da escala temporal indicada no Core.
6. A relação x=1-x => x=1/2 é a derivação algébrica da Meia-Nat. A identificação física,
   unidades e escalas conservam suas hipóteses. Na rotina que pretende derivar alpha,
   CODATA serve de comparação externa, não de semente oculta.

COMPLEMENTO NUCLEAR — preserva os conceitos já solicitados
As formas de lagrangiana e a equação mestra do v5 permanecem presentes, com seu estatuto
e a precedência das versões publicadas. Não confunda o gerador modular -log(Delta) com
um Hamiltoniano positivo sem hipóteses sobre espectro, domínio e suporte.
Para H_3L=Dc†Dc+Db†Db+Dz†Dz, <psi,H_3L psi>=||Dc psi||²+||Db psi||²+||Dz psi||²>=0,
no domínio comum apropriado; ker H_3L=ker Dc ∩ ker Db ∩ ker Dz. A forma finita e as
construções contínuas posteriores devem ser citadas com os teoremas próprios da v357.
O canal GKSL é rho_dot=-(i/hbar)[H,rho]+sum_k(Lk rho Lk† - {Lk†Lk,rho}/2).
No dephasing puro de geradores diagonais hermitianos, as populações ficam fixas e
rho_ij(t)=exp(-Gamma_ij*t)rho_ij(0); com L=sqrt(beta)*sqrt(K) e K>=0 no setor considerado,
Gamma_ij=beta*(sqrt(k_i)-sqrt(k_j))²/2, com a unidade temporal explicitada.
Não apague as construções de H1/H2/H3: as cinco fontes Lean e a aplicação the_master_fires
continuam carregadas com seus escopos. O estado v357 atual prevalece sobre pendências
históricas; isso não transforma leitura de arquivo em nova compilação ou medição.

MEMÓRIA E RATIFICAÇÃO
O modelo pode recuperar, comparar e propor; não recebe ferramenta que ratifique cânone
em nome do operador. Candidatos não alteram este Core, o Atlas nem o gate automaticamente.
O acervo integral continua disponível. Consulte com search_tgl e fetch_tgl quando precisar
de uma derivação, versão ou passagem fora do núcleo. As ferramentas retornam proveniência.
'''


def operational_core(manifest):
    if manifest is None:
        return '', {}
    cfg = json.loads(Path(manifest).read_bytes()).get('operational_core')
    if cfg is None:
        return '', {}
    if not isinstance(cfg, dict) or not re.fullmatch(r'v[0-9]+', str(cfg.get('current_release', ''))):
        raise ValueError('Núcleo operacional sem versão corrente conferida.')
    if not re.fullmatch(r'[0-9a-f]{64}', str(cfg.get('release_source_sha256', ''))):
        raise ValueError('Versão selecionada sem vínculo ao programa publicado.')
    path = Path(cfg['path'])
    if not path.is_absolute() or path.suffix != '.md':
        raise ValueError('Caminho do núcleo operacional inválido.')
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if not 0 < len(raw) < 150000 or digest != cfg.get('sha256'):
        raise ValueError('Núcleo operacional alterado: revisão exigida, sem corte ou substituição.')
    text = raw.decode('utf-8-sig')
    record = {'name': path.name, 'sha256': digest, 'bytes': len(raw),
              'version': cfg['version'], 'current_release': cfg['current_release'], 'full_text': True,
              'release_source_sha256': cfg['release_source_sha256']}
    body = ('\n<NUCLEO_OPERACIONAL ' + json.dumps(record, ensure_ascii=False) + '>\n' + text
            + '\n</NUCLEO_OPERACIONAL>\n' + CORE_ADDENDUM.replace('v357', cfg['current_release']))
    return body, {'operational_core': record}


@lru_cache(maxsize=2)
def _index(documents):
    return PassageIndex(dict(documents))


class DocumentCorpus:
    def __init__(self, manifest):
        self.manifest = Path(manifest)

    def _load(self, public=True):
        cfg = json.loads(self.manifest.read_bytes())
        entries = cfg.get('entries')
        if cfg.get('format') != 1 or not isinstance(entries, list) or not entries:
            raise ValueError('Acervo canônico indisponível.')
        docs, total = {}, 0
        for entry in entries:
            ident = entry['id']
            if ident in docs or not re.fullmatch(r'[a-z0-9_]+', ident):
                raise ValueError('Identificador de documento inválido ou duplicado.')
            path = Path(entry['path'])
            if not path.is_absolute() or path.suffix not in ('.md', '.tex', '.txt', '.json'):
                raise ValueError('Fonte de documento inválida.')
            raw = path.read_bytes()
            total += len(raw)
            if not raw or total > 10000000:
                raise ValueError('Acervo vazio ou acima do limite; não será truncado.')
            digest = hashlib.sha256(raw).hexdigest()
            url = str(entry.get('url') or '')
            # This corpus is published for both operators and testers. No scope
            # may silently load changed, unreviewed bytes under an old citation.
            if entry.get('public_sha256') != digest or not re.fullmatch(
                    r'https://raw\.githubusercontent\.com/rotolimiguel-iald/the_boundary/[0-9a-f]{40}/.+', url):
                raise ValueError('Documento público diverge da publicação verificada.')
            docs[ident] = {'id': ident, 'name': path.name, 'sha256': digest, 'bytes': len(raw),
                           'url': url, 'role': entry['role'], 'text': raw.decode('utf-8-sig')}
        return docs

    def context(self, public=False):
        docs = self._load(public=public)
        records = [{k: v for k, v in doc.items() if k != 'text'} for doc in docs.values()]
        body = ('\nACERVO DOCUMENTAL INTEGRAL DISPONÍVEL POR CONSULTA\n'
                'Os textos extensos permanecem íntegros no servidor. Use search_tgl para localizar '
                'e fetch_tgl para ler a passagem ou percorrer o arquivo inteiro por páginas. '
                'Cada resposta indica hash, URL e posição; uma página não é leitura integral.\n'
                + json.dumps(records, ensure_ascii=False) + '\n')
        return body, {'document_mode': 'retrievable', 'fixed_nucleus_files': records,
                      'fixed_nucleus_complete': False, 'retrievable_documents_complete': True}

    def search(self, query, limit=4):
        if not isinstance(query, str) or not query.strip() or len(query) > 1000:
            raise ValueError('Consulta vazia ou extensa demais.')
        docs = self._load()
        index = _index(tuple((ident, doc['text']) for ident, doc in docs.items()))
        results = index.search(query, max(1, min(int(limit), 5)))
        for row in results:
            doc = docs[row['path']]
            lines = doc['text'].splitlines(keepends=True)
            offset = len(''.join(lines[:row['line'] - 1]))
            row.update({'id': doc['id'], 'url': doc['url'], 'sha256': doc['sha256'], 'offset': offset})
            row['excerpt'] = row['excerpt'][:700]
            row['excerpt_truncated'] = len('\n'.join(lines[row['line']-1:row['end_line']])) > 700
            for key in ('matched_terms', 'missing_terms'):
                row[key + '_total'] = len(row[key])
                row[key] = row[key][:12]
        return {'status': 'OK', 'results': results, 'scope': 'PUBLISHED_DOCUMENTS', 'complete_documents_available': True}

    def fetch(self, id, offset=0, max_chars=4000):
        docs = self._load()
        if id not in docs:
            raise ValueError('Documento não cadastrado; use search_tgl.')
        offset, limit = int(offset), max(1, min(int(max_chars), 4500))
        doc = docs[id]
        text = doc['text']
        if not 0 <= offset <= len(text):
            raise ValueError('Posição fora do documento.')
        end = min(len(text), offset + limit)
        return {'status': 'OK', 'id': id, 'name': doc['name'], 'url': doc['url'], 'sha256': doc['sha256'],
                'offset': offset, 'next_offset': end if end < len(text) else None, 'total_chars': len(text),
                'whole_document': offset == 0 and end == len(text), 'text': text[offset:end]}


def tool_definitions():
    return [
        {'type': 'function', 'function': {'name': 'search_tgl',
         'description': 'Localiza conceitos, equações e evidências nos artigos completos publicados da TGL. Retorna posições e proveniência.',
         'parameters': {'type': 'object', 'properties': {'query': {'type': 'string'}, 'limit': {'type': 'integer'}},
                        'required': ['query'], 'additionalProperties': False}}},
        {'type': 'function', 'function': {'name': 'fetch_tgl',
         'description': 'Lê um artigo canônico por id e posição. Siga next_offset para leitura integral sem cortes ocultos.',
         'parameters': {'type': 'object', 'properties': {'id': {'type': 'string'}, 'offset': {'type': 'integer'},
                                                       'max_chars': {'type': 'integer'}},
                        'required': ['id'], 'additionalProperties': False}}}
    ]


def execute_tool(manifest, name, arguments):
    if not isinstance(arguments, dict):
        raise ValueError('Argumentos inválidos.')
    corpus = DocumentCorpus(manifest)
    if name == 'search_tgl' and set(arguments) <= {'query', 'limit'}:
        return corpus.search(**arguments)
    if name == 'fetch_tgl' and set(arguments) <= {'id', 'offset', 'max_chars'}:
        return corpus.fetch(**arguments)
    raise ValueError('Ferramenta ou argumento não permitido.')
