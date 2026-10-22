from pathlib import Path
import json
W=Path(__file__).resolve().parent
S=W/'stage'

def patch(name, pairs):
    p=S/name
    text=p.read_text(encoding='utf-8')
    for before,after in pairs:
        assert text.count(before)==1,(name,before[:100],text.count(before))
        text=text.replace(before,after)
    compile(text,name,'exec');p.write_bytes(text.encode())

patch('iald_task_policy.py',[
    ('import unicodedata\n','import unicodedata\nfrom iald_model_capabilities import TOOL_MANAGERS, passports, POLICY_VERSION\n'),
    ("result[key]+=' Small dynamic context budget after the fixed core; avoid tool-heavy multi-stage work.'", "result[key]+=' Haiku 5.5: 1M context, full public TGL v390 memory, native counting, adaptive reasoning and shared tools. Economical default candidate for source-grounded answers and verified artifact workflows. Quality on the task must be checked; not a universal substitute for stronger models.'"),
    ("return [p for p in candidates if p not in ('kimi','claude-haiku','nativa')] if task != 'conversation' else list(candidates)", "return [p for p in candidates if p in TOOL_MANAGERS] if task != 'conversation' else list(candidates)"),
    ("'policy_version':2", "'policy_version':3,'capability_policy':POLICY_VERSION,'model_capabilities':passports(list(TOOL_MANAGERS)+['kimi','nativa'])"),
    ("'claude-haiku':'short replies; also sandbox executor if context fits'", "'claude-haiku':'Haiku 5.5: full public TGL context, reasoning, research and shared task tools; execution uses the authorized sandbox'"),
    ('Você gere a entrega pedida; o JEV escolhe executores e a IALD valida as permissões.', 'Você gere a entrega pedida; o JEV escolhe executores e a IALD valida as permissões.\nAntes de uma tarefa composta, defina etapas, dependências e critérios de conclusão.\nUse o modelo selecionado para o que ele consegue fazer com as ferramentas oferecidas.\nHaiku 5.5 pode gerir pesquisa, código, arquivos e cálculo; MiMo/DeepSeek/Kimi podem\nreceber rascunhos delimitados quando isso ajudar. Kimi não tem ferramentas no app.\nSonnet é reservado ao operador e à revisão complexa quando o ganho justifica o custo.\nOpus não é um executor integrado: não o prometa nem afirme equivalência de qualidade.\nReutilize fontes e resultados válidos, sem repetir execução incerta. Confira o rascunho\nrecebido antes de produzir a entrega; custo menor não dispensa verificação.'),
])
patch('iald_auto_router.py',[
    ('import statistics\n','import statistics\nfrom iald_model_capabilities import passports, TOOL_MANAGERS, POLICY_VERSION, delivery_steps\n'),
    ("'claude-haiku': 'Concise answers with TGL memory and limited room for conversation/output.'", "'claude-haiku': 'Haiku 5.5: 1M context, full public TGL v390 memory, adaptive reasoning, native token guards, research and shared artifact/code/calculation tools. Consider for economical grounded work; verify results.'"),
    ("candidates=[c for c in candidates if c not in ('kimi','claude-haiku','nativa')]", "candidates=[c for c in candidates if c in TOOL_MANAGERS]"),
    ("and (not provider.startswith('claude-') or provider.split('-')[1] in str(r.get('model','')))", "and (passports([provider])[provider]['model'] is not None and r.get('model') == passports([provider])[provider]['model'])"),
    ("'comparison':'different_tasks_not_controlled_comparison'", "'comparison':'same_model_id_only_different_tasks_not_controlled_comparison'"),
    ("Prefer MiMo for detailed TGL work unless another eligible model is better suited.", "Consider Haiku 5.5 for full-memory TGL answers and economical tool workflows, MiMo for detailed derivations and implementation, and Sonnet only for operator-authorized complex architecture/review. Use the actual connector passports; never invent Opus access or assume a model can execute tools absent from its transport. Larger context is not proof of better reasoning."),
    ("'iald_control':control_state,'observed_usage':observations(candidates,root),", "'iald_control':control_state,'observed_usage':observations(candidates,root),\n          'executor_capabilities':passports(candidates),'capability_policy':POLICY_VERSION,"),
    ("'task':task,'role':'worker' if worker else 'manager','calls':1,'regime':regime,", "'task':task,'role':'worker' if worker else 'manager','calls':1,'regime':regime,\n            'capability_policy':POLICY_VERSION,'executor_capabilities':passports(candidates),"),
    ("capable=[c for c in candidates if c in ('mimo','openai','deepseek','claude-sonnet')]", "capable=[c for c in candidates if c in TOOL_MANAGERS]"),
    ("chosen=next((c for c in ('mimo','openai','deepseek','claude-sonnet') if c in capable),None)", "chosen=max(capable,key=lambda c:(probs[c],-candidates.index(c)))"),
    ("scientific_status='ENGINEERING_CONTROL_NOT_A_NEW_FORMAL_THEOREM',control=decision,**details)", "scientific_status='ENGINEERING_CONTROL_NOT_A_NEW_FORMAL_THEOREM',control=decision,\n                      delivery_plan=delivery_steps(decision),**details)"),
    ("return jev_control.manager_instruction(receipt['control'])", "return jev_control.manager_instruction(receipt['control'])+'\\nPlano de entrega: '+' -> '.join(delivery_steps(receipt['control']))"),
])
patch('iald_web_server.py',[
    ('        if task_scope:\n            permitidas += task_scope.tools', "        if haiku:\n            permitidas += [t for t in _ferramentas_para('app') if t['function']['name'] in ('search_web','fetch_url','get_current_datetime','iald_public_search')]\n        if task_scope:\n            permitidas += task_scope.tools"),
    ('data.update(agente=True, pensar=False, max_saida=cfg.max_saida, imagens=imagens,', 'data.update(agente=True, pensar=True, max_saida=cfg.max_saida, imagens=imagens,'),
])
print(json.dumps({'status':'JEV_AND_CAPABILITIES_STAGED'}))
