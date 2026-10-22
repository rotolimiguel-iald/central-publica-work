"""Record DNS recovery and the installation gate without changing packages."""
from datetime import datetime
import importlib.metadata as md
import importlib.util
import json
from pathlib import Path

WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('targets',WORK.parent/'iald_context_math_20260915/record_prepared.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)

def main():
    plan=json.loads((WORK/'anthropic_dry_run_20260922.json').read_bytes())
    rows=[]
    for item in plan['install']:
        name=item['metadata']['name']; planned=item['metadata']['version']
        try: current=md.version(name)
        except md.PackageNotFoundError:current=None
        rows.append({'package':name,'installed':current,'planned':planned,
                     'changes_existing':current is not None and current!=planned})
    assert [r['package'] for r in rows if r['changes_existing']]==['idna']
    now=datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f')
    report={'at':now.isoformat(),'status':'INSTALLATION_STOPPED_EXISTING_VERSION_CHANGE',
        'router_login':'operator_completed','router_settings_changed':False,
        'parental_filter_enabled':False,'windows_cached_address_before':'100.127.127.77',
        'router_dns_answers':['151.101.0.223','151.101.64.223','151.101.128.223','151.101.192.223'],
        'action':'Clear-DnsClientCache','tls_after':'HTTP response received with certificate verification',
        'official_pypi_downloads_after':'pip dry-run downloaded metadata successfully',
        'packages_installed':False,'plan':rows,'operator_decision':'pending'}
    helper.create(WORK/'sdk_gate_20260922.json',json.dumps(report,indent=2).encode())
    note='''[REAL] Operador entrou pessoalmente no Linksys EA9500. Controle de conteúdo carregado mostrou DESLIGADO. Nenhuma configuração do roteador foi alterada; telas fechadas com Cancelar. A alegação anterior de bloqueio pelo roteador não foi confirmada. O Windows resolvia files.pythonhosted.org para 100.127.127.77; consulta direta ao DNS do roteador retornou endereços públicos Fastly. Limpeza do cache temporário do Windows (Clear-DnsClientCache) restaurou resolução e conexão HTTPS, com certificados verificados. A origem da entrada incorreta anterior não foi determinada.

[REAL] pip install --dry-run anthropic completou downloads oficiais e gerou anthropic_dry_run_20260922.json. Plano: anthropic 1.7.0, httpx2/httpcore2 2.13.0, jiter 0.17.0, sniffio 1.3.1, truststore 0.10.4, além de mudança em idna 3.11 → 3.20. Conferência importlib.metadata confirmou idna como única mudança em pacote existente. NENHUM pacote instalado ou atualizado.

[OPEN] Gate T2 aplicado: a ordem manda parar quando a instalação altera versão existente. Pergunta enviada ao operador: preservar versões e procurar combinação compatível, ou autorizar atualização pontual de idna com verificação dos serviços. A decisão permanece pendente. Não avançar com instalação dependente sem resposta. T3 chave/crédito Anthropic, T4 medição/testes e T5 builds continuam pendentes. Recibo: work/iald_tudo_20260921/sdk_gate_20260922.json. Preservadas todas as restrições de segredos, gastos e coordenação.
'''
    marker='IALD_CLAUDE_SDK_DNS_RECOVERY_GATE_20260922'
    for path in helper.TARGETS:
        before=path.read_bytes();assert marker.encode() not in before
        backup=path.with_name(path.name+'.bak_'+stamp);helper.create(backup,before)
        newline='\r\n' if b'\r\n' in before else '\n'
        addition='\n\n## '+now.strftime('%d/%m/%Y %H:%M')+' — Codex: DNS recuperado; gate SDK Claude\n\n<!-- '+marker+' -->\n\n'+note
        after=before+addition.replace('\n',newline).encode()
        tmp=path.with_name(path.name+'.tmp_'+stamp);helper.create(tmp,after)
        assert path.read_bytes()==before
        tmp.replace(path);assert path.read_bytes()==after and len(after)>len(before)
    print(json.dumps({'receipt':'sdk_gate_20260922.json','memories_updated':len(helper.TARGETS),'packages_installed':False}))

if __name__=='__main__':main()
