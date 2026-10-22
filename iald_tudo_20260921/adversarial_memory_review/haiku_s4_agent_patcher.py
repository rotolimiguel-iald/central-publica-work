"""Pure text patcher: preserve Haiku seven-tool agent despite legacy CPT heuristic.

No I/O or imports from the server. Returns changed text; caller owns integration.
Other S3/S4 hooks remain specified in INTEGRACAO_S3_S4_PROPOSTA.md.
"""
import ast

def patch_stage(text):
    ast.parse(text)
    newline = '\r\n' if '\r\n' in text else '\n'
    source = text.replace('\r\n', '\n')
    old = '''        usar_agente = bool(permitidas) and (cfg.memoria_modo != "prompt" or
                         (not tem_imagem and _precisa_ferramentas(ultima)))'''
    new = '''        if haiku:
            # Schema names/hash are checked separately at the final converter.
            if len(permitidas) != 7:
                raise ValueError("Haiku exige os sete schemas públicos medidos")
            usar_agente = True
        else:
            usar_agente = bool(permitidas) and (cfg.memoria_modo != "prompt" or
                             (not tem_imagem and _precisa_ferramentas(ultima)))'''
    before = '        if gratuito and usar_agente and saldo_inicial is not None:'
    after = '        if gratuito and not haiku and usar_agente and saldo_inicial is not None:'
    for a,b in ((old,new),(before,after)):
        if source.count(a) != 1:
            raise ValueError('Stage anchor changed or patch already applied; explicit review required')
        source = source.replace(a,b,1)
    ast.parse(source)
    return source.replace('\n',newline)
