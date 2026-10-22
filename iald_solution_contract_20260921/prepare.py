from datetime import datetime
import hashlib
import json
from pathlib import Path

APP=Path(r'C:\IALD\projetos_pyhton\IALD')
WORK=Path(__file__).resolve().parent

def create(path,raw):
    with path.open('xb') as out:out.write(raw)
    assert path.read_bytes()==raw

def main():
    name='iald_memoria_canonica.py'
    original=(APP/name).read_bytes()
    text=original.decode('utf-8')
    changes=[
        ('from iald_cluster import active_cluster',
         'from iald_cluster import active_cluster\nfrom iald_response_contract import deployment_contract, SOLUTION_PROTOCOL'),
        ("return selected, {'current_index_sha256': hashlib.sha256(data).hexdigest(),\n                              'current_index_scope': 'GENERATED_STATE_AND_FRONTIER__NOT_NEW_PROOF'}",
         """version = re.search(r'(?m)^\\| versão \\| \\*\\*(v[0-9]+)\\*\\* \\|', selected)
            return selected, {'current_index_sha256': hashlib.sha256(data).hexdigest(),
                              'working_index_release': version.group(1) if version else None,
                              'current_index_scope': 'WORKING_ARCHIVE_RECORD__NOT_DEPLOYED_RELEASE'}"""),
        ('ESTADO RECENTE — ÍNDICE DERIVADO, LIDO NESTA REQUISIÇÃO',
         'ACERVO DE TRABALHO — ÍNDICE DERIVADO; NÃO É A VERSÃO IMPLANTADA'),
        ("'Este índice situa a versão e as fronteiras com remissões. Não é prova primária. '",
         "'Este índice situa o acervo externo ao pacote implantado e suas remissões. Não é prova primária nem prova de atualização do app. '"),
        ('"confronte as fontes carregadas e os registros históricos do Atlas com o índice recente; "',
         '"confronte as fontes e evidências do pacote implantado, separando os registros do acervo de trabalho; "'),
        ('metadata["context_tokens"] = count_tokens(prefix)',
         '''contract, contract_meta = deployment_contract(self.nucleus_manifest,
            getattr(catalog, 'source_sha', None), metadata, current_metadata)
        if contract:
            prefix = contract + prefix + "\\n" + SOLUTION_PROTOCOL + contract
            metadata.update(contract_meta)
        metadata["context_tokens"] = count_tokens(prefix)''')
    ]
    # Normalize only the staging text; the original byte backup remains exact.
    text=text.replace('\r\n','\n')
    for old,new in changes:
        assert text.count(old)==1,old
        text=text.replace(old,new,1)
    create(WORK/name,text.encode())
    pins={name:hashlib.sha256(original).hexdigest(),
          'manifest_sha256':hashlib.sha256((APP/'iald_nucleo_fixo.json').read_bytes()).hexdigest()}
    create(WORK/'prepared.json',json.dumps(pins,indent=2).encode())
    print('Response contract staged; canonical source files unchanged.')

if __name__=='__main__':main()
