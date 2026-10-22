"""Append SDK installation evidence with immediate byte backups and safe retries."""
from datetime import datetime
import importlib.util
import json
from pathlib import Path
import time

WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('targets',WORK.parent/'iald_context_math_20260915/record_prepared.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)

def main():
    verification=json.loads((WORK/'sdk_verification_20260922.json').read_bytes())
    assert verification['packages']['anthropic']=='1.7.0'
    assert verification['packages']['idna']=='3.20'
    now=datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f')
    note='''[INPUT] Operador autorizou expressamente “Autorizar a atualização de idna para 3.20, com verificação dos serviços”. Essa decisão resolve a pergunta anterior sobre preservar a versão 3.11; ela não autoriza outras atualizações de pacotes existentes.

[REAL] Instalados do PyPI oficial: anthropic 1.7.0, httpx2/httpcore2 2.13.0, idna 3.20, jiter 0.17.0, sniffio 1.3.1, truststore 0.10.4. Recibo pip anthropic_installed_20260922.json e verificação sdk_verification_20260922.json. Cliente SDK importado e construído localmente com valor fictício, sem chamada à Anthropic, sem chave real, sem gasto. requests/httpx/pydantic mantêm versões anteriores. Saúde dos serviços conforme códigos do recibo.

[REAL] A consulta pip check não é inteiramente verde: acusa xformers ausente e datasets 4.8.4 incompatível com as restrições de unsloth/unsloth-zoo. Esses pacotes de treinamento não foram alterados por esta instalação; não corrigi suas versões fora de escopo. Não houve reinício dos servidores.

[REAL] DNS: controle parental do Linksys desligado; nenhuma regra do roteador alterada. Cache Windows continha 100.127.127.77 para files.pythonhosted.org enquanto DNS consultado diretamente no roteador respondia Fastly. Clear-DnsClientCache liberou HTTPS, porém a entrada incorreta reapareceu antes da primeira instalação (que falhou sem instalar). Nova limpeza e instalação na mesma execução concluíram com certificado verificado. Origem da recorrência ainda OPEN; não chamar o problema de DNS definitivamente resolvido.

[OPEN] Console Anthropic aberto para login pessoal do operador. Pendentes saldo/tier, chave via formulário protegido, medição e duas chamadas de teste nos tetos autorizados, builds iOS18/Android17 e testes físicos. Não declarar Claude ativo no app antes dessas verificações.

[LINHAGEM] O registro intermediário record_sdk_gate.py atualizou as três primeiras superfícies e foi interrompido por PermissionError na substituição atômica do Atlas. Original do Atlas preservado, backup e temporário mantidos; este adendo registra o estado final, sem apagar a passagem histórica. Consultar sdk_memory_record_20260922.json para o resultado por superfície.
'''
    marker='IALD_CLAUDE_SDK_INSTALLED_20260922'
    rows=[]
    for path in helper.TARGETS:
        before=path.read_bytes()
        if marker.encode() in before:
            rows.append({'path':str(path),'status':'already_recorded'});continue
        backup=path.with_name(path.name+'.bak_'+stamp);helper.create(backup,before)
        newline='\r\n' if b'\r\n' in before else '\n'
        addition='\n\n## '+now.strftime('%d/%m/%Y %H:%M')+' — Codex: SDK Claude instalado; autorização idna\n\n<!-- '+marker+' -->\n\n'+note
        after=before+addition.replace('\n',newline).encode()
        tmp=path.with_name(path.name+'.tmp_'+stamp);helper.create(tmp,after)
        for attempt in range(3):
            assert path.read_bytes()==before
            try:
                tmp.replace(path)
                assert path.read_bytes()==after and len(after)>len(before)
                rows.append({'path':str(path),'status':'updated','backup':str(backup)})
                break
            except PermissionError:
                if attempt==2:rows.append({'path':str(path),'status':'permission_error_original_preserved','backup':str(backup),'temp':str(tmp)})
                else:time.sleep(1)
    helper.create(WORK/'sdk_memory_record_20260922.json',json.dumps({'at':now.isoformat(),'surfaces':rows,'goal_complete':False},ensure_ascii=False,indent=2).encode())
    print(json.dumps(rows))

if __name__=='__main__':main()
