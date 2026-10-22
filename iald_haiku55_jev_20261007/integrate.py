"""Integrate the reviewed builder's JEV changes with the main runtime migration."""
from pathlib import Path
W=Path(__file__).resolve().parent
S=W/'stage'
def patch(name,pairs):
    p=S/name;t=p.read_text(encoding='utf-8')
    for before,after in pairs:
        assert t.count(before)==1,(name,before[:100],t.count(before));t=t.replace(before,after)
    compile(t,name,'exec');p.write_bytes(t.encode())

# The builder owns the capability catalog; only the deterministic plan is reused.
source=(S/'iald_model_capabilities.py').read_text(encoding='utf-8')
plan='\n\n'+source[source.index('def delivery_steps('):]
p=S/'iald_task_policy.py';p.write_bytes(p.read_bytes()+plan.encode())
patch('iald_task_policy.py',[
    ("if key=='claude-sonnet':item['account_scope']='operator_only'", "if key=='claude-sonnet':item['account_scope']='operator_only'\n        configured_rates={'claude-haiku':(0.5,0.05,2.5),'claude-sonnet':(2.0,0.2,10.0),\n            'mimo':(0.435,0.0036,0.87),'deepseek':(0.30,0.006,1.20)}\n        item['configured_rates_per_million']=configured_rates.get(key)\n        item['rate_order']='input,cache_read,output; configured rates, not a bill'\n        if key=='claude-haiku':item['price_tier']='prompts_over_100000; Anthropic docs verified 2026-10-07'"),
    ('Você gere a entrega pedida; o JEV escolhe executores e a IALD valida as permissões.', 'Você gere a entrega pedida; o JEV escolhe executores e a IALD valida as permissões.\nDefina etapas e critérios de conclusão antes de trabalho composto. Use a sequência\nde entrega recebida e confira cada resultado antes da próxima etapa. Haiku 5.5\npode gerir as ferramentas oferecidas e consultar mais da TGL diretamente no contexto.\nMaior contexto não prova superioridade em toda tarefa; Sonnet continua opção do\noperador para revisão complexa. Opus não é um executor integrado. Não o prometa.\nDelegue apenas etapas úteis, reaproveite resultados válidos e nunca repita envio incerto.'),
])
patch('iald_auto_router.py',[
    ('Prefer MiMo for detailed TGL work unless another eligible model is better suited.', 'Consider Haiku 5.5 for full-memory TGL answers and economical tool workflows, MiMo for detailed derivations and implementation, and Sonnet only for operator-authorized complex review. Use actual transport capabilities; larger context is not a quality benchmark. Kimi has no interactive app tools; Opus is not integrated.'),
    ("chosen=next((c for c in ('mimo','openai','deepseek','claude-haiku','claude-sonnet') if c in capable),None)", "chosen=max(capable,key=lambda c:(probs[c],-candidates.index(c)))"),
    ("scientific_status='ENGINEERING_CONTROL_NOT_A_NEW_FORMAL_THEOREM',control=decision,**details)", "scientific_status='ENGINEERING_CONTROL_NOT_A_NEW_FORMAL_THEOREM',control=decision,\n                      delivery_plan=task_policy.delivery_steps(decision),**details)"),
    ("return jev_control.manager_instruction(receipt['control'])", "return jev_control.manager_instruction(receipt['control'])+'\\nPlano de entrega: '+' -> '.join(task_policy.delivery_steps(receipt['control']))"),
])
patch('iald_web_server.py',[
    ('        if task_scope:\n            permitidas += task_scope.tools', "        if haiku:\n            permitidas += [t for t in _ferramentas_para('app') if t['function']['name'] in ('search_web','fetch_url','get_current_datetime','iald_public_search')]\n        if task_scope:\n            permitidas += task_scope.tools"),
    ('data.update(agente=True, pensar=False, max_saida=cfg.max_saida, imagens=imagens,', 'data.update(agente=True, pensar=True, max_saida=cfg.max_saida, imagens=imagens,'),
    ('        candidates=[]\n        for row in _opcoes_de_motor(registro,user):', '        candidates=[]\n        candidate_models={}\n        for row in _opcoes_de_motor(registro,user):'),
    ("            if key == 'nativa' or iald_motores.consentiu(registro,consent_provider):candidates.append(key)", "            if key == 'nativa' or iald_motores.consentiu(registro,consent_provider):\n                candidates.append(key)\n                if isinstance(row.get('modelo'),str) and row['modelo']:candidate_models[key]=row['modelo']"),
    ("chosen,receipt=app_router.choose(client[-1]['content'],candidates,operator_context=operator_context)", "chosen,receipt=app_router.choose(client[-1]['content'],candidates,operator_context=operator_context,\n            model_ids={key:candidate_models[key] for key in candidates if key in candidate_models})"),
])
patch('test_migration.py',[]) if False else None
print('INTEGRATED')
