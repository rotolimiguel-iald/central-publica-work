"""Close the authorized one-call evaluation and its previously pending memory entry."""
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
WORK=Path(__file__).resolve().parent
APP=Path(r'C:\IALD\projetos_pyhton\IALD')
spec=importlib.util.spec_from_file_location('memory_targets',WORK.parent/'iald_context_math_20260915/record_prepared.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
MARKER='IALD_SOLUTION_CONTRACT_REAL_RESPONSE_20260921'

def main():
    paths=list(WORK.glob('model_response_*.json'))
    assert len(paths)==1,'Expected the single authorized evaluation only'
    response=json.loads(paths[0].read_bytes())
    assert response['http_status']==200 and response['finish_reason']=='stop'
    assert response['single_call_cap_usd']<=0.5
    assert response['memory']['private_atlas_included'] is False
    answer=response['answer']
    for marker in ('**v368**','**v369**','Articulação matemática','lagrangiana','H1','H2','H3'):
        assert marker in answer
    installed=json.loads((WORK/'installed.json').read_bytes())
    for name,digest in installed['files'].items():
        assert hashlib.sha256((APP/name).read_bytes()).hexdigest()==digest
    source=hashlib.sha256(paths[0].read_bytes()).hexdigest()
    note=f'''[INPUT — autorização específica recebida] O operador respondeu “Autorizo o contexto completo e o teste”: kernel v5, núcleo canônico e cluster TGL v368/fontes publicadas a api.openai.com, sem Atlas privado, uma chamada até US$ 0,50. Isso encerra a pendência de autorização registrada no adendo anterior.

[REAL — teste único executado] HTTP 200, finish_reason=stop; {response['usage']['prompt_tokens']} tokens de entrada e {response['usage']['completion_tokens']} de saída. Reserva/teto calculado US$ {response['single_call_cap_usd']:.7f}, abaixo do autorizado; controle global de gastos preservado. Os módulos testados coincidem em SHA com os módulos instalados. O contexto público foi enviado sem Atlas privado.

[REAL — comportamento observado] A resposta começou: “A versão efetivamente carregada do um.py é v368”, separando v369 como menção no índice de trabalho, e articulou a solução com lagrangiana, equação mestra, dephasing, Hamiltoniano e testemunhas H1/H2/H3. Não transformou o pedido em exigência de confirmação experimental. Preservou qualificações de escopo. O teste cobre esse comportamento e a identificação de versão; não constitui auditoria independente de todas as fórmulas ou uma nova prova da TGL, nem garante ausência de erros futuros.

Evidência: {paths[0]}; SHA256 lido do recibo: {source}. A correção permanece ativa no servidor compartilhado. A matriz de disponibilidade e os limites de verificação física dos aparelhos do registro anterior continuam válidos; não há compilação nova nesta alteração de servidor.
'''
    now=datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for path in helper.TARGETS:
        before=path.read_bytes();assert MARKER.encode() not in before
        backup=path.with_name(path.name+'.bak_'+stamp);helper.create(backup,before)
        newline='\r\n' if b'\r\n' in before else '\n'
        addition='\n\n## ADENDO '+now.strftime('%d/%m/%Y %H:%M')+' — Teste autorizado da solução matemática e versão\n\n<!-- '+MARKER+' -->\n\n'+note
        after=before+addition.replace('\n',newline).encode()
        temp=path.with_name(path.name+'.tmp_'+stamp);helper.create(temp,after)
        assert path.read_bytes()==before
        temp.replace(path);assert path.read_bytes()==after and len(after)>len(before)
        rows.append({'path':str(path),'backup':str(backup),'sha256':hashlib.sha256(after).hexdigest()})
    receipt={'at':now.isoformat(),'inference_test':'COMPLETED_ONE_AUTHORIZED_CALL',
        'http_status':200,'response_receipt':str(paths[0]),'response_sha256':source,
        'reviewed_scope':['deployed_version_vs_working_archive','mathematical_solution_request_semantics'],
        'scientific_formula_audit_performed':False,'memories':rows}
    helper.create(WORK/'probe_memory_record.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode())
    print(json.dumps({'test_complete':True,'memories_updated':len(rows),'release':'v368','local_tests':40}))
if __name__=='__main__':main()
