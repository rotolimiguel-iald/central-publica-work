"""Prepared adapter for counting the final native Anthropic request.

Schema checked against installed SDK and official documentation on 2026-09-22:
https://platform.claude.com/docs/en/api/messages/count_tokens
Credentials and client ownership remain with the existing server integration.
"""
import json

COUNT_FIELDS = frozenset(('model', 'messages', 'system', 'tools', 'tool_choice',
                          'thinking', 'output_config', 'cache_control'))
# These two fields are emitted by the current converter but are not prompt data
# accepted by count_tokens. Output reservation is enforced by the request guard.
NON_COUNT_FIELDS = frozenset(('max_tokens', 'metadata'))

def native_count_parameters(request):
    if not isinstance(request, dict):
        raise ValueError('Native request must be an object')
    if set(request) - COUNT_FIELDS - NON_COUNT_FIELDS:
        raise ValueError('Unreviewed native request fields; count adapter update required')
    if not isinstance(request.get('model'), str) or not request['model']:
        raise ValueError('Model missing')
    if not isinstance(request.get('messages'), list) or not request['messages']:
        raise ValueError('Messages missing')
    result = json.loads(json.dumps({k:v for k,v in request.items() if k in COUNT_FIELDS},
                                   ensure_ascii=False, allow_nan=False))
    if 'tools' in result:
        if not isinstance(result['tools'], list) or not all(isinstance(t,dict) for t in result['tools']):
            raise ValueError('Tools must be native tool objects')
        for tool in result['tools']:
            # Haiku 5.5 binds thinking to the exact tool list, including this flag.
            # The official count endpoint accepted it on 2026-10-07. Keep
            # earlier model behavior unchanged; never strip signed 5.5 tools.
            if result['model'] != 'claude-haiku-5-5':
                tool.pop('eager_input_streaming', None)
    return result

def count_native_request(client, request):
    parameters = native_count_parameters(request)
    response = client.messages.count_tokens(**parameters)
    value = response.get('input_tokens') if isinstance(response,dict) else getattr(response,'input_tokens',None)
    if type(value) is not int or value <= 0:
        raise ValueError('Provider returned no valid token measurement')
    return value
