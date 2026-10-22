from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
from deploy import atomic,backup,snapshot

W=Path(__file__).parent;R=Path(r'C:\IALD\projetos_pyhton\IALD')
MARKER='IALD_OPERATOR_BENCH_AND_RESEARCH_MAP_20261002'

def main():
    live=json.loads((W/'live_validation.json').read_bytes());assert live['status']=='PASS'
    deployed=json.loads((W/'deployment.json').read_bytes());checks=json.loads((W/'validation/final_checks.json').read_bytes())
    assert checks['passed'] and snapshot()==live['bench_after']
    assert all(hashlib.sha256((R/name).read_bytes()).hexdigest()==v['stage'] for name,v in deployed['files'].items())
    surfaces=[Path(x['path']) for x in json.loads((W/'stage/restart_inventory.json').read_bytes())['memory_surfaces']]
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S_%f');entries=[]
    text=f'''

## 02/10/2026 — Bancada científica pelo chat: classe operador e mapa de rotas

<!-- {MARKER} -->

[INPUT] O operador pediu controle da bancada existente pelo chat, coordenação pelo JEV, RAM residente e inscrição de cada rota para evitar repetir pesquisas. A classe `operador` está autorizada somente para Luiz nesta entrega.

[REAL — implantação] Sete módulos de servidor instalados com baseline conferido e backups imediatos de bytes. `classe_usuario=operador` foi acrescentada somente a `luiz`; exige também admin booleano verdadeiro e ausência de ambos os bloqueios. Os outros dez registros de conta, faturamento, consentimentos, permissões de modelos e clientes foram preservados. O JEV recebe as capacidades científicas e escolhe um gestor com ferramentas; a delegação de raciocínio continua no fluxo existente. Nenhuma nova fila de modelos ou automação periódica foi criada. A instrução é contexto operacional e adaptadores, não treinamento dos pesos.

[REAL — ferramentas] `bench_capabilities`, `bench_query`, `bench_plan`, `bench_run`, `bench_result`, `bench_map`. Catálogo com 34 operações existentes: acervo/localizadores, álgebra e dephasing, strain residente, modelo/evento de ringdown, cosmologia/BAO, cenários e exportações. URLs/portas e parâmetros são fixados pelo adaptador; sem shell, URL livre, execução de um.py, reinício da bancada ou liberação de RAM. Usuários comuns, familiares e outros administradores não recebem as ferramentas; a autorização é relida antes de cada etapa. Artefatos pertencem exclusivamente a luiz.

[REAL — mapa] `.iald_runtime/research/map.sqlite3` em {R} é o journal operacional append-only (routes/events/claims/legacy). Plano registra objetivo, hipótese, falsificador, parâmetros normalizados, proveniência, hash e parent_id antes do cálculo. Identidade usa operação/parâmetros/proveniência; variar a descrição não permite duplicar. Claim durável precede despacho; resultado incerto não é reenviado automaticamente e bloqueia novo despacho até reconciliação. Há leitura de resultados em páginas e JSON privado completo. As fontes disponíveis de histórico foram importadas em leitura, incluindo inquiry_events e vínculos, preservando originais. Na validação: {live['map_counts']['routes']} rota nova e {live['map_counts']['legacy']} nós históricos/evidências importados. Este mapa cresce com as inscrições; não alega cobrir toda pesquisa histórica ou todo o universo físico.

[REAL — RAM e estados] Conservados os 180 arquivos GW, {live['bench_after']['gw']['resident_bytes']} bytes de arrays residentes (~22,5 GiB), mesma carga e mesmos hashes de strain. Cosmologia conservou a carga e a geração verificadas. Carga READY completa retorna ALREADY_RESIDENT sem recarregar. ACK LOADING é PENDING_BACKEND, não conclusão; acompanhamento consulta domínio/load_id/generation sem repetir POST. Resultado parcial, falha e fonte alterada continuam explícitos. O health cosmológico passivo não atesta load_id; pins em disco não provam a geração do código já importado no processo. GPU hoje oferece telemetria/visualização; não foi criado solver GPU. Protocolos que só eram localizadores continuam sem replay conectado.

[REAL — segurança e validação] {checks['total_tests']} testes locais aprovados, incluindo revisão adversarial. Corrigido DNS rebinding no fetch público: IP público validado é o IP conectado; Host/SNI e verificação TLS preservados, sem proxy ambiental. Consulta HTTPS pública ao app e llms.txt da TGL retornou 200. Um teste numérico real de dephasing passou com tolerância 1e-12: rota {live['route_id']}; registros nativos de runs passaram de {live['native_runs_before']} para {live['native_runs_after']}; segunda solicitação de execução recuperou o resultado, sem novo cálculo. Artefato de outro proprietário foi recusado. Zero chamadas pagas de IA nesta validação. Não se afirma avaliação end-to-end de qualidade do JEV/LLM nem teste físico de natureza.

[DISPONIBILIDADE] Web pública e servidor do app ativos. Mudança exclusivamente de servidor, utilizável pelo chat em modo Automático no site/iOS/Android existentes; nenhum recurso nativo ou arquivo de cliente mudou, portanto nova build não é necessária. Somente o processo web foi reiniciado pelo supervisor já existente; serviços de bancada e RAM permaneceram ligados. Não foi verificada instalação física nova nos aparelhos nem alterada a distribuição das lojas. Nenhum kernel, gate, um.py ou fonte científica original foi modificado.

[EVIDÊNCIAS] {W}: deployment.json, restart.json, live_validation.json, http_validation.json, validation/final_checks.json e validation/review_final.txt. Código implantado em {R}: iald_operator_bench.py, iald_research_routes.py, iald_bench_catalog.py, iald_public_fetch.py, mais integração em iald_web_server.py, iald_auto_router.py e iald_app_providers.py. Resultados operacionais não promovem inferência a cânone. Para usar: no chat Automático, pedir ao JEV o estado da bancada/RAM e o mapa; definir hipótese, parâmetros e falsificador para uma rota admitida.
'''
    for path in surfaces:
        original=path.read_bytes()
        if MARKER.encode() in original:raise AssertionError('Already recorded; inspect existing memory')
        dest=backup(path,stamp);addition=text.replace('\n','\r\n').encode('utf-8') if b'\r\n' in original else text.encode('utf-8')
        raw=original+addition
        assert path.read_bytes()==original,'Concurrent memory edit'
        atomic(path,raw);assert path.stat().st_size>len(original) and path.read_bytes().startswith(original)
        entries.append({'path':str(path),'backup':dest,'bytes_before':len(original),'bytes_after':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
    atomic(W/'memory_updates.json',json.dumps(entries,indent=2).encode())
    delivery={'utc':datetime.now(timezone.utc).isoformat(),'status':'ACTIVE_SERVER_INTEGRATION_VALIDATED','operator':'luiz',
        'tests':checks['total_tests'],'operations':live['catalog_operations'],'map_counts':live['map_counts'],
        'resident_preserved':True,'paid_model_tests':0,'web':'active','ios':'same server; no new binary required',
        'android':'same server; no new binary required','physical_device_test':'not performed in this delivery',
        'model_orchestration_test':'transport tested offline; no new paid inference','memory_surfaces_updated':len(entries),
        'research_route':live['route_id'],'artifact':live['artifact']}
    atomic(W/'delivery.json',json.dumps(delivery,ensure_ascii=False,indent=2).encode())
    print(json.dumps({'status':delivery['status'],'memory_surfaces':len(entries),'tests':delivery['tests'],'paid_calls':0}))

if __name__=='__main__':main()
