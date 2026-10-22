"""Explicit excerpts of ONLY the latest tool batch; exact native count gates send.

Never edit prefix, user history, assistant text, tool arguments or schemas.
No source writes and no semantic summarization. Excerpts are not complete proofs.
"""
from copy import deepcopy
import hashlib
import json


class ToolResultsDoNotFit(ValueError):
    pass


def excerpt(content, fraction):
    """Keep complete list entries/text lines and retain provenance separately."""
    if not isinstance(content, str):
        raise ToolResultsDoNotFit('Unsupported tool result; no automatic content change.')
    try:
        value = json.loads(content)
    except ValueError:
        value = None
    metadata, part, resume = {}, {}, {}
    if isinstance(value, dict):
        # All non-content fields (including status/negatives) survive unchanged.
        metadata = {k:v for k,v in value.items() if k not in ('text','files','hits','results')}
        for key in ('files','hits','results'):
            if key in value:
                if not isinstance(value[key], list):
                    raise ToolResultsDoNotFit('Unknown result structure; explicit smaller retrieval required.')
                n = int(len(value[key]) * fraction)
                part[key] = value[key][:n]
        if 'text' in value:
            if not isinstance(value['text'], str):
                raise ToolResultsDoNotFit('Unknown text structure.')
            lines=value['text'].splitlines(keepends=True)
            part['text']=''.join(lines[:int(len(lines)*fraction)])
            if type(value.get('start_line')) is int:
                resume['start_line']=value['start_line']+int(len(lines)*fraction)
            if type(value.get('offset')) is int:
                resume['offset']=value['offset']+len(part['text'])
        if isinstance(value.get('files'),list) and type(value.get('total')) is int:
            end=value.get('next_offset')
            if end is None:end=value['total']
            if type(end)is int:
                resume['offset']=end-len(value['files'])+len(part.get('files',[]))
    else:
        lines=content.splitlines(keepends=True)
        part['text']=''.join(lines[:int(len(lines)*fraction)])
    return json.dumps({
        'context_status':'PARTIAL_TOOL_RESULT',
        'scope':'Excerto parcial por limite de contexto. Não é leitura integral nem prova completa. '
                'Responda agora com o núcleo e evidências disponíveis, indicando as lacunas; não alegue ter lido partes omitidas.',
        'recovery':'A chamada de ferramenta imediatamente anterior preserva nome/argumentos. '
                   'Metadados e paginação abaixo pertencem ao resultado ORIGINAL, não ao excerto. '
                   'Solicite depois trecho menor da mesma fonte para recuperar partes omitidas.',
        'original_result_sha256':hashlib.sha256(content.encode()).hexdigest(),
        'original_chars':len(content), 'original_metadata':metadata,
        'excerpt':part, 'excerpt_resume':resume},ensure_ascii=False)


def fit_latest_tool_results(payload, count_request, window, margin=1024):
    """At most six count probes; final exact count is also checked by account/guard.

    A failing smaller candidate never authorizes send. No monotonicity assumption.
    Existing tool batches are immutable; only the consecutive trailing tool results
    from the most recent assistant tool call can be excerpted.
    """
    messages=payload.get('messages',[])
    start=len(messages)
    while start and messages[start-1].get('role')=='tool':
        start-=1
    if start==len(messages):
        return payload
    if not start or messages[start-1].get('role')!='assistant' or not messages[start-1].get('tool_calls'):
        raise ToolResultsDoNotFit('Tool batch lacks its original assistant call.')
    original=deepcopy(payload)
    def remaining(candidate):
        measured=count_request(candidate)
        if type(measured)is not int or measured<=0:
            raise ToolResultsDoNotFit('Native count unavailable; next turn not sent.')
        return window-measured-candidate['max_completion_tokens']-margin
    # Keep a little room for another tool turn; otherwise finish with full evidence.
    if remaining(original)>=1024:
        return payload
    final=deepcopy(original)
    final['tool_choice']='none'
    if remaining(final)>=0:
        return final
    for fraction in (.5,.25,.125,0):
        candidate=deepcopy(final)
        for index in range(start,len(messages)):
            candidate['messages'][index]['content']=excerpt(messages[index].get('content'),fraction)
        if remaining(candidate)>=0:
            return candidate
    raise ToolResultsDoNotFit('Mesmo os marcadores de resultados parciais não cabem; '
                             'prefixo, histórico e pergunta foram preservados. A próxima volta não foi enviada.')
