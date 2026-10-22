"""Server-owned transport capabilities; provider marketing is not an app tool."""
from copy import deepcopy
from claude_profiles import HAIKU, SONNET

POLICY_VERSION = 'haiku55_jev_20261007'
TOOL_MANAGERS = frozenset(('openai', 'mimo', 'deepseek', 'claude-haiku', 'claude-sonnet'))

CATALOG = {
    'claude-haiku': dict(model=HAIKU.model, window=HAIKU.window, output=HAIKU.default_output,
        provider_output=HAIKU.max_output, transport='streaming_tools', memory='full_public_v390_native_counted',
        roles=['manager', 'research', 'artifacts', 'code', 'calculation'],
        prices=dict(input=0.50, cache_read=0.05, output=2.50, cache_write_5m=0.625),
        price_scope='USD_per_million_for_prompts_over_100000',
        source='https://platform.claude.com/docs/en/models/haiku-5-5/overview',
        evidence='account_model_metadata_20261007; task_quality_not_benchmarked'),
    'claude-sonnet': dict(model=SONNET.model, window=SONNET.window, transport='streaming_tools',
        roles=['manager', 'complex_code_review', 'reasoning'], owner_only=True,
        prices=dict(input=2.0, cache_read=0.20, output=10.0),
        price_scope='configured_USD_per_million', evidence='operator_preference_not_quality_benchmark'),
    'openai': dict(model='gpt-5.6-luna', transport='streaming_tools',
        roles=['manager', 'research', 'artifacts', 'code', 'calculation'],
        memory='existing_public_or_authorized_operator_context',
        evidence='installed_connector; use_server_config_for_limits_and_prices'),
    'mimo': dict(model='mimo-v2.6-pro', window=1048576, output=131072, transport='streaming_tools',
        roles=['manager', 'detailed_TGL', 'implementation', 'artifacts', 'calculation'],
        prices=dict(input=0.435, cache_read=0.0036, output=0.87),
        price_scope='configured_USD_per_million_not_invoice',
        evidence='operator_positive_feedback_not_controlled_benchmark'),
    'deepseek': dict(model='deepseek-flash', window=1048576, output=393216, transport='streaming_tools',
        roles=['manager', 'reasoning', 'implementation', 'research', 'artifacts'],
        prices=dict(input=0.30, cache_read=0.006, output=1.20),
        price_scope='configured_peak_USD_per_million_not_invoice',
        evidence='configured_connector; availability_checked_before_dispatch'),
    'kimi': dict(model='kimi-code/k3', window=1048576, transport='buffered_text_only',
        roles=['text_worker', 'code_draft', 'long_analysis'], prices=None,
        evidence='subscription_not_zero_cost; no_app_tool_loop'),
    'nativa': dict(model=None, window=131072, transport='local_streaming_retrieval',
        roles=['brief_conversation', 'public_TGL_retrieval'], prices=None,
        evidence='local_serving_limits_checked; not_a_remote_API_price'),
}

def passports(candidates):
    if any(key not in CATALOG for key in candidates):
        raise ValueError('Unknown executor capability')
    return {key: deepcopy(CATALOG[key]) for key in candidates}

def delivery_steps(control):
    """A plan describes only the tools already admitted by the control decision."""
    path = control['work_path']
    if control.get('worker'):
        return ['Read the supplied evidence', 'Return a draft with uncertainties; no tool execution']
    plans = {
        'answer': ['Use the loaded canon', 'Answer directly with the scope of the sources'],
        'retrieve': ['Find the missing primary source', 'Read the supporting passage', 'Answer with provenance'],
        'create_artifact': ['Define deliverable and checks', 'Delegate a bounded draft only if useful',
            'Create the real file with the artifact tool', 'Read and check the resulting artifact', 'Return its authenticated app link'],
        'execute_calculation': ['Define inputs and expected checks', 'Prepare code and JSON',
            'Execute once in the authorized sandbox', 'Inspect results and errors', 'Deliver code, JSON and evidence'],
        'code_review': ['State requirements and failure cases', 'Delegate a bounded draft if useful',
            'Inspect the complete returned draft', 'Report findings; do not claim execution without a result'],
        'operator_bench': ['Read the route map', 'Reuse a matching completed route when appropriate',
            'Inscribe hypothesis, falsifier and input hashes', 'Execute the authorized route once',
            'Read evidence and preserve inconclusive results'],
    }
    return plans[path]
