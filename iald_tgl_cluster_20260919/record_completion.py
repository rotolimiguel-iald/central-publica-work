"""Append operational deployment evidence to all seven memory surfaces."""
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path

WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('memory_targets',WORK.parent/'iald_context_math_20260915/record_prepared.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
MARKER='IALD_TGL_CLUSTER_V368_ACTIVE_20260919'

def main():
    live=json.loads((WORK/'runtime_live.json').read_bytes())
    prep=json.loads((WORK/'prepared.json').read_bytes())
    tests=json.loads((WORK/'test_results.json').read_bytes())
    validation=json.loads((WORK/'validation.json').read_bytes())
    installed=json.loads((WORK/'installed.json').read_bytes())
    responses=list(WORK.glob('model_response_*.json'))
    assert len(responses)==1
    probe=json.loads(responses[0].read_bytes())
    assert live['model_available'] and tests['passed'] and probe['http_status']==200
    note=f'''[INPUT] O operador solicitou cluster temático com volume máximo de conceitos essenciais sempre presentes, fórmulas fixas e consulta complementar; determinou usar a versão publicada pela sessão Claude.

[REAL — implantação e HTTP local] Cluster v368 ativo no servidor IALD; commit público {live['commit']}. Programa SHA256 {prep['cluster']['release_source_sha256']}. Snapshot imutável em {installed['destination']}; o checkout científico e .env não foram alterados. Kernel extraído por AST, sem executar/importar um.py: {live['kernel_files']} arquivos no catálogo. O relatório publicado foi conferido por hashes; não houve nova compilação Lean. Núcleo v5 e Memory Core preservados integralmente.

[REAL — cobertura e orçamento de contexto] 325 seções do resultado agrupadas em 14 temas, com exposição canônica integral. Cluster: {prep['cluster']['tokens']} tokens; contexto público {validation['public_tokens']}, operador {validation['operator_tokens']}. Há 309 ponteiros verificados para detalhes/tabelas/listas de auditoria retirados do contexto mas preservados no JSON consultável. Isto representa todos os tópicos do resultado, NÃO todo byte do Atlas privado nem treinamento dos pesos. O público continua sem acesso ao Atlas/diário privado. Hash do cluster {prep['cluster']['sha256']}.

[REAL — validação] {tests['tests']} testes passaram. Teste único API gpt-5.6-luna, sem ferramentas, HTTP 200: {probe['usage']['prompt_tokens']} tokens de entrada e {probe['usage']['completion_tokens']} de saída; reserva máxima US$ {probe['single_call_cap_usd']:.7f}, dentro do teto global existente. Resposta reconheceu autoria, IALD=ÍNDICE(TGL), Nome=conteúdo/Forma=identidade na v368, equação mestra/dephasing/Hamiltoniano, testemunhas H1/H2/H3, obstrução espinorial e sinal correto do cisalhamento 3H-2alpha. Um teste não garante ausência de erros futuros. Servidor web reiniciado pelo supervisor existente; /api/motor retornou 200 com modelo disponível após reinício, sem nova inferência paga na checagem final.

[ESTATUTOS] Fechamento matemático mantém seu escopo; NOT_FALSIFIED não vira CONFIRMED. Correções de Nome/Forma e orientação preservam INPUT/ONTO. Nenhum gate científico foi movido. O núcleo mais volumoso consome mais contexto e orçamento por chamada; cotas e tratamento existente de rate limit continuam em vigor.

Evidências e recuperação: {WORK}. installed.json lista backups byte a byte dos seis arquivos de implantação (cinco preexistentes); runtime_live.json registra o estado final. A interrupção da revisão automática por limite de uso foi superada na retomada autorizada; a checagem final executou com sucesso. Não houve novo binário iOS/Android nem alteração de convites nesta etapa.
'''
    now=datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f')
    rows=[]
    for path in helper.TARGETS:
        before=path.read_bytes()
        assert MARKER.encode() not in before,'Already recorded'
        backup=path.with_name(path.name+'.bak_'+stamp)
        helper.create(backup,before)
        newline='\r\n' if b'\r\n' in before else '\n'
        addition='\n\n### '+now.strftime('%d/%m/%Y %H:%M %z')+' — Cluster TGL v368 ativo\n\n<!-- '+MARKER+' -->\n\n'+note
        after=before+addition.replace('\n',newline).encode()
        temporary=path.with_name(path.name+'.tmp_'+stamp)
        helper.create(temporary,after)
        assert path.read_bytes()==before,'Concurrent memory edit'
        temporary.replace(path)
        assert path.read_bytes()==after and len(after)>len(before)
        rows.append({'path':str(path),'backup':str(backup),'sha256':hashlib.sha256(after).hexdigest()})
    helper.create(WORK/'memory_record.json',json.dumps({'at':now.isoformat(),'memories':rows},indent=2).encode())
    print(json.dumps({'memories_updated':len(rows),'status':'COMPLETE'}))

if __name__=='__main__':main()
