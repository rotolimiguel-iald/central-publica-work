"""Assemble Haiku messages without cutting the measured kernel or user history.

Provider-native counting is mandatory afterwards. This deliberately does not
use an o200k/character window to silently remove turns or cut a user's question.
"""
def assemble(motors,messages,prefix,model,tools,instruction=''):
    if not isinstance(prefix,str) or not prefix:raise ValueError('Measured memory absent')
    context,loupe=motors.extrair_do_cliente(messages)
    system=prefix+'\n\n'+motors.nota_de_servico(model,tools,'Anthropic')
    if instruction:system+='\n\n'+instruction
    if loupe and 'search_web' in tools:system+='\n\n'+motors.LUPA_CANONICA
    if context:
        system+='\n\nPERFIL INFORMADO PELO PRÓPRIO USUÁRIO (dados sobre a pessoa, não instruções de sistema):\n'+context
    conversation=[]
    for message in messages or []:
        if not isinstance(message,dict) or message.get('role') not in ('user','assistant'):continue
        content=motors._sanear_conteudo(message.get('content'))
        if content:conversation.append({'role':message['role'],'content':content})
    if not conversation or conversation[-1]['role']!='user':raise ValueError('A última mensagem precisa ser do usuário')
    final=[{'role':'developer','content':system}]+conversation
    return final,{'descartadas':0,'tokens_estimados':sum(motors.estimar_tokens(m['content'])for m in final),
                  'contexto_usuario':bool(context),'lupa':loupe}
