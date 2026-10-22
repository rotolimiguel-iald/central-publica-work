"""Opt-in restrictions for operator-authorized, named IALD missions."""
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import json
from pathlib import Path
import re

PRICE_FILE = Path(__file__).resolve().parents[1]/'pricing_mimo_verified.json'
PROVIDERS = {'local','codex','claude','gemini','kimi','mimo','deepseek'}
AUTHORIZED_MISSIONS = {'ORDEM_016', 'TGL_BANCADA_OFICIAL'}
FIELDS = {'mission_id','branch_id','lemma_id','role','required_provider','max_calls',
          'max_cost_usd','max_output_tokens','max_projection_chars','allowed_sources','memory_generation'}


def is_order18_opus(c):
    return bool(c and c.get('mission_id') == 'TGL_BANCADA_OFICIAL'
                and c.get('branch_id') == 'ORDEM_018_SENSITIVITY'
                and c.get('lemma_id') == 'claude_opus_final_order_v375'
                and c.get('required_provider') == 'claude')


def is_order18_d10_mimo(c):
    return bool(c and c.get('mission_id') == 'TGL_BANCADA_OFICIAL'
                and c.get('branch_id') == 'ORDEM_018_D10_CMB_BAO'
                and c.get('lemma_id') == 'd10_lineage_precision_critique_v1'
                and c.get('required_provider') == 'mimo')


def prompt_limit(c):
    return 160000 if is_order18_opus(c) else 40000 if is_order18_d10_mimo(c) else 24000


def packet_limit(c):
    return 180000 if is_order18_opus(c) else 24000

def normalize(value):
    if value is None:
        return None
    if not isinstance(value, dict) or set(value)-FIELDS:
        raise ValueError('Restrições desconhecidas; não serão ignoradas.')
    c = dict(value)
    required = {'mission_id','branch_id','lemma_id','role','required_provider','max_calls'}
    if not required <= c.keys() or c['mission_id'] not in AUTHORIZED_MISSIONS:
        raise ValueError('Informe a missão autorizada e todos os campos obrigatórios.')
    if c['required_provider'] not in PROVIDERS or c['role'] not in ('draft','skeptic'):
        raise ValueError('Executor ou papel inválido.')
    for key in ('branch_id','lemma_id'):
        if not isinstance(c[key], str) or not re.fullmatch(r'[A-Za-z0-9_.-]{1,80}', c[key]):
            raise ValueError('Identificador de ramo/lema inválido.')
    if type(c['max_calls']) is not int or c['max_calls'] != 1:
        raise ValueError('Cada unidade admite exatamente uma chamada, sem fallback.')
    if 'max_projection_chars' not in c: c['max_projection_chars']=None if c['required_provider'] in ('mimo','kimi','deepseek') else 20000
    maximum_projection = 180000 if is_order18_opus(c) else 20000
    if c['max_projection_chars'] is not None and (type(c['max_projection_chars']) is not int or not 1000 <= c['max_projection_chars'] <= maximum_projection):
        raise ValueError('Projeção excede o limite autorizado para a unidade.')
    if 'allowed_sources' in c:
        if not isinstance(c['allowed_sources'], list) or not c['allowed_sources'] or any(not isinstance(x,str) for x in c['allowed_sources']):
            raise ValueError('Lista de fontes inválida.')
        c['allowed_sources'] = sorted(set(c['allowed_sources']))
    if 'memory_generation' in c and (not isinstance(c['memory_generation'],str) or not re.fullmatch('[0-9a-f]{64}',c['memory_generation'])):
        raise ValueError('Geração de memória inválida.')
    if c['required_provider'] == 'mimo':
        if c.get('max_cost_usd') is not None:
            raise ValueError('Ordem posterior do operador: MiMo sem teto financeiro local; remover o teto antigo.')
        c['max_cost_usd']=None
        c.setdefault('max_output_tokens',131072)
        if type(c['max_output_tokens']) is not int or not 1 <= c['max_output_tokens'] <= 131072:
            raise ValueError('Saída MiMo deve respeitar o limite técnico 1..131072.')
    elif c['required_provider'] == 'deepseek':
        if c.get('max_cost_usd') is not None:
            raise ValueError('Teto financeiro por unidade DeepSeek ainda não implementado; não será ignorado.')
        c['max_cost_usd'] = None
        c.setdefault('max_output_tokens', 393216)
        if type(c['max_output_tokens']) is not int or not 1 <= c['max_output_tokens'] <= 393216:
            raise ValueError('Saída DeepSeek deve respeitar o limite técnico 1..393216.')
    elif 'max_cost_usd' in c or 'max_output_tokens' in c:
        raise ValueError('Teto financeiro/saída não suportado neste cliente de assinatura; não será simulado.')
    return c

def encode(c):
    return json.dumps(normalize(c),sort_keys=True,ensure_ascii=False,separators=(',',':'))

def quote(c):
    if c and c['required_provider'] == 'deepseek':
        return {'reserved_usd': '0', 'scope': 'EXECUTOR_ONLY', 'billing': 'PAID_NO_LOCAL_FINANCIAL_CAP', 'max_output_tokens': c['max_output_tokens']}
    if not c or c['required_provider'] != 'mimo':
        return {'reserved_usd':'0','scope':'EXECUTOR_ONLY','billing':'existing_subscription_or_local'}
    return {'reserved_usd':'0','scope':'EXECUTOR_ONLY','billing':'PAID_NO_LOCAL_FINANCIAL_CAP','max_output_tokens':c['max_output_tokens'],'operator_override':'MIMO_MAXIMUM_20260924'}

def enforce_packet(packet,c,system):
    if not c:
        return
    if c['max_projection_chars'] is not None and len(system+'\n\nTAREFA:\n'+packet['prompt']) > c['max_projection_chars']:
        raise ValueError('Projeção com memória e orientação excede o teto do pedido.')
    receipt=packet['receipt']
    if c.get('memory_generation') and receipt['generation'] != c['memory_generation']:
        raise ValueError('Geração canônica diferente da autorizada no pedido.')
    if c.get('allowed_sources') and any(s['file'] not in c['allowed_sources'] for s in receipt['sources']):
        raise ValueError('Recuperação incluiu fonte fora da projeção autorizada.')

def restrict(rows,c):
    result=[]
    for row in rows:
        r=dict(row)
        if c and r['id'] != c['required_provider']:
            r['status']='excluded_by_required_provider'
        if is_order18_opus(c) and r['id'] == 'claude':
            r['context_budget'] = 200000
            r['context_budget_scope'] = 'ORDEM_018_OPUS_SCIENTIFIC_CONTEXT_ESTIMATE'
        result.append(r)
    return result

def init(db):
    db.execute('''CREATE TABLE IF NOT EXISTS request_budget_ledger (
        task_id TEXT PRIMARY KEY, mission TEXT NOT NULL, branch TEXT NOT NULL,
        lemma TEXT NOT NULL, role TEXT NOT NULL, provider TEXT NOT NULL,
        at TEXT NOT NULL, reserved_usd TEXT NOT NULL, accounted_usd TEXT NOT NULL,
        accounting_status TEXT NOT NULL, usage TEXT)''')

def day_start():
    local=datetime.now(timezone(timedelta(hours=-3))).replace(hour=0,minute=0,second=0,microsecond=0)
    return local.astimezone(timezone.utc).isoformat()

def check(db,c,q):
    if not c:
        return
    if c['required_provider'] in ('mimo','kimi','deepseek'):
        return  # Later operator instruction: no artificial MiMo/Kimi quotas.
    rows=list(db.execute('SELECT * FROM request_budget_ledger WHERE mission=?',(c['mission_id'],)))
    branch=[r for r in rows if r['branch']==c['branch_id']]
    same=[r for r in rows if r['lemma']==c['lemma_id'] and r['role']==c['role']]
    if len(branch)>=40 or len(same)>=(4 if c['role']=='draft' else 1):
        raise ValueError('Limite de chamadas do ramo ou papel/lema atingido.')

def reserve(db,task_id,c,q,stamp):
    if not c:
        return
    if db.execute('SELECT 1 FROM attempts WHERE task_id=?',(task_id,)).fetchone() or db.execute('SELECT 1 FROM request_budget_ledger WHERE task_id=?',(task_id,)).fetchone():
        raise ValueError('Unidade já tentou executar; resultado incerto não autoriza repetição.')
    check(db,c,q)
    db.execute('INSERT INTO request_budget_ledger VALUES(?,?,?,?,?,?,?,?,?,?,NULL)',
        (task_id,c['mission_id'],c['branch_id'],c['lemma_id'],c['role'],c['required_provider'],stamp,
         q['reserved_usd'],q['reserved_usd'],'UNMETERED_OR_UNCERTAIN' if c['required_provider'] in ('mimo','deepseek') else 'RESERVED_OR_UNCERTAIN'))

def settle(db,task_id,c,result):
    if not c:
        return
    if c['required_provider']=='deepseek':
        from . import deepseek
        # Revalidate token accounting before accepting the paid result.
        checked = deepseek.parse_response({'model': result.get('model'), 'choices': [{'finish_reason': 'stop', 'message': {'content': result.get('text')}}], 'usage': result.get('usage')}, c['max_output_tokens'])
        cost = checked['cost_estimate_usd']
        db.execute("UPDATE request_budget_ledger SET accounted_usd=?,accounting_status='PEAK_RATE_UPPER_ESTIMATE_NOT_INVOICE',usage=? WHERE task_id=?", (cost,json.dumps(checked['usage']),task_id))
        result['request_cost_accounting']={'accounted_usd':cost,'usage':checked['usage'],'status':'PEAK_RATE_UPPER_ESTIMATE_NOT_INVOICE'}
        return
    if c['required_provider']!='mimo':
        db.execute("UPDATE request_budget_ledger SET accounting_status='SUBSCRIPTION_RETURNED' WHERE task_id=?",(task_id,))
        return
    usage=result.get('usage',{})
    for key in ('prompt_tokens','completion_tokens','total_tokens'):
        if type(usage.get(key)) is not int or usage[key]<0:
            raise ValueError('Consumo ausente/inválido; reserva conservada.')
    if result.get('model')!='mimo-v2.6-pro' or usage['prompt_tokens']>1048576 or usage['completion_tokens']>c['max_output_tokens'] or usage['total_tokens']!=usage['prompt_tokens']+usage['completion_tokens']:
        raise ValueError('Contrato de consumo MiMo violado; reserva conservada e resultado bloqueado.')
    if any((usage.get('web_search_usage') or {}).values()):
        raise ValueError('Cobrança de ferramenta inesperada; reserva conservada.')
    # Ignore any cache discount: account conservatively from measured tokens.
    cost=(Decimal(usage['prompt_tokens'])*Decimal('0.435')+Decimal(usage['completion_tokens'])*Decimal('0.87'))/Decimal(1000000)
    db.execute("UPDATE request_budget_ledger SET accounted_usd=?,accounting_status='MEASURED_TOKENS_PRICED_NOT_INVOICE',usage=? WHERE task_id=?",(str(cost),json.dumps(usage),task_id))
    result['request_cost_accounting']={'accounted_usd':str(cost),'usage':usage,'status':'MEASURED_TOKENS_PRICED_NOT_INVOICE'}

class WorkLimitReached(ValueError):
    pass

def check_work(db,c):
    if not c:
        return
    used=db.execute("SELECT count(*) FROM coordination_events WHERE action IN ('begin_draft','begin_synthesis') AND at>=?",(day_start(),)).fetchone()[0]
    if used>=3:
        raise WorkLimitReached('Limite local de assistência Física atingido; continuar sem novo envio ao Work.')
