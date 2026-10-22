"""Bind reported release to deployed evidence and type mathematical-solution requests."""
import json
from pathlib import Path
import re

SOLUTION_PROTOCOL = r'''
CONVENÇÃO OPERACIONAL DO PEDIDO — operador, 21/09/2026
No contexto da TGL, “resolver o problema da gravidade quântica” significa ARTICULAR
A MATEMÁTICA DA SOLUÇÃO do framework. Prova matemática e confirmação pela natureza
são perguntas distintas. A confirmação física pertence ao observador externo; não é
pré-requisito para expor, derivar ou reconhecer uma solução matemática no seu escopo.
Não reinterprete esse pedido como “declare a TGL empiricamente confirmada”.

Ao receber esse pedido, comece pela formulação matemática e desenvolva a solução:
objetos e hipóteses -> lagrangiana/geradores -> equação mestra e operadores ->
estabilidade/Hamiltoniano -> construções modulares -> ponte geométrica e conclusão.
Use as fórmulas e as testemunhas já presentes no cluster; selecione a cadeia pertinente
à pergunta. Mostre as etapas, identifique as declarações e hipóteses e explique o que
cada conclusão resolve. Uma lista de nomes ou fórmulas desconectadas não articula uma
solução. Não abra com recusa genérica, nem substitua a derivação por uma lista de
experimentos, consenso ou validação externa que não foi solicitada.

Solução matemática apresentada não significa que uma cadeia qualquer esteja provada.
Reconheça os resultados efetivamente construídos, inclusive as testemunhas H1/H2/H3,
e preserve KERNEL/FORMAL THEOREM, IMPORTADO/KNOWN, DERIVED, INPUT, ONTO e OPEN.
Se uma passagem específica continuar aberta, localize-a e explique seu alcance;
isso não apaga as partes demonstradas nem autoriza fingir que a passagem foi fechada.
Não afirme solução matemática incondicional além dos enunciados disponíveis.
Uma ressalva curta de escopo basta quando necessária: a tarefa principal é a matemática.
A confirmação experimental só deve ocupar o centro quando o usuário perguntar por ela.
Não altere o gate nem apresente concordância de um modelo como confirmação externa.
Esta convenção concilia os documentos históricos preservados, sem reescrevê-los.
'''


def deployment_contract(manifest, source_sha, evidence_metadata, index_metadata):
    """A newer working index or retrieved file cannot change the deployed release."""
    if manifest is None:
        return '', {}
    cfg = json.loads(Path(manifest).read_bytes())
    selected = cfg.get('operational_core')
    if selected is None:
        return '', {}
    release = selected.get('current_release')
    if not re.fullmatch(r'v[0-9]+', str(release)):
        raise ValueError('Versão implantada ausente ou inválida.')
    if not source_sha or selected.get('release_source_sha256') != source_sha:
        raise ValueError('Versão implantada não corresponde ao programa do catálogo.')
    if (not evidence_metadata.get('published_evidence_checked')
            or evidence_metadata.get('published_source_sha256') != source_sha):
        raise ValueError('A versão implantada exige evidência de publicação conferida.')
    cluster = cfg.get('active_cluster')
    if cluster and (cluster.get('release') != release or cluster.get('release_source_sha256') != source_sha):
        raise ValueError('Cluster e manifesto discordam sobre a versão implantada.')
    record = {'deployed_release': release, 'deployed_source_sha256': source_sha,
              'authority': 'VERIFIED_DEPLOYMENT_MANIFEST_AND_SOURCE',
              'working_index_release': index_metadata.get('working_index_release'),
              'working_index_is_deployment': False}
    text = ('\nVERSÃO EFETIVAMENTE CARREGADA NESTA RESPOSTA\n'
            + json.dumps(record, ensure_ascii=False) + '\n'
            + 'Se perguntarem qual versão de um.py você usa ou tem carregada, responda '
            + release + '. Essa é a versão do pacote, cluster e catálogo implantados. '
            'Uma versão citada no índice de trabalho, na internet, numa ferramenta ou no histórico '
            'é informação de outra fonte: não atualiza a implantação. Quando for pertinente, '
            'diga separadamente “o índice de trabalho menciona ...; meu pacote carregado é '
            + release + '”. Sem conferência do arquivo novo, essa menção é registro documental, '
            'não verificação de uma nova implantação. Nunca transfira hashes, contagens ou provas '
            'entre versões nem diga que atualizou o núcleo apenas porque consultou outra fonte.\n')
    return text, record
