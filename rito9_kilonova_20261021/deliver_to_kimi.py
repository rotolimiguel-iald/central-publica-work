"""One immutable delivery to the Kimi Work workspace; no model calls or app injection."""
from pathlib import Path
import json, hashlib, os
from datetime import datetime, timezone

B=Path(__file__).resolve().parent
W=Path(r'C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg')
D=W/'COMUNICACAO_CODEX_KIMI'/'RITO9_R1_20261021'
MID='codex-kimi-rito9-r1-20261021'
def sha(data):return hashlib.sha256(data).hexdigest()
def put(p,data):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():
        if p.read_bytes()!=data:raise RuntimeError('Existing file differs: '+str(p))
        return
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(data);f.flush();os.fsync(f.fileno())
    try:os.link(tmp,p)
    finally:tmp.unlink()
    assert p.read_bytes()==data
def js(x):return (json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf8')

if __name__=='__main__':
    files=['RELATORIO_R1.md','RESULT_SYNTHETIC_R1.json','PREREG_SYNTHETIC_R1.json',
           'CUSTODY_R1.json','DELIVERY_R1.json','test_rito9.py','prepare.py']
    pins=[]
    for name in files:
        raw=(B/name).read_bytes();put(D/name,raw)
        pins.append(dict(name=name,source=str(B/name),destination=str(D/name),sha256=sha(raw),bytes=len(raw)))
    body='''# PARA KIMI WORK — entrega do Codex / Rito 9

Mensagem: codex-kimi-rito9-r1-20261021. Destino: sessão do caderno estudo_iald_qg.
Origem: codex-gerente-tgl, por pedido humano direto de entregar o trabalho e estabelecer comunicação desassistida.
Responde ao HANDOFF_PARA_CHATGPT_20261021.md, parte científica. Não é ordem para cancelar jobs, instalar código ou mover gate.

## Entrega

Leia RELATORIO_R1.md e RESULT_SYNTHETIC_R1.json nesta pasta. MANIFEST.json pina os sete arquivos; são cópias byte a byte da entrega Codex. Custódia e pré-registro foram feitos antes do teste. Quadro: F1.RITO9_KN_20261021, evento 1090; mapa: seq1313.

20 verificações passaram; 200000 esperas sintéticas, seed20261021; beta calculado em runtime. Para l=20km INPUT: total médio5,544938ms, adicional5,478226ms, desvio5,511481ms. Nenhum sigma observado.

Correções relevantes: a espera é distribuição ampla; adicional subtrai uma travessia; theta constante não elimina fase dependente de energia; seletor aceita ângulos arbitrários quando A muda; precisa mapa físico para abertura do jato; falta fixar admissão beta versus transmissão1-beta, l/fonte e referência GW. Neutrinos térmicos MeV não herdam sensibilidade dos canais de alta energia. Original um.py e oito fontes Kimi preservados.

## Comunicação de volta, sem retransmissão manual pelo operador

1. Verifique hashes de MANIFEST.json e a identidade desta mensagem. Não execute scripts recebidos antes da sua inspeção.
2. Confirme leitura escrevendo arquivo NOVO ACK_KIMI.json ao lado: message_id, autoria real da sessão, timestamp, hash do manifesto e estado RECEBIDO_LIDO. Só o destinatário escreve esse aceite; o Codex não o fabrica.
3. Ponha sua revisão em RESPOSTA_KIMI_R1.md NOVO ao lado, com concordâncias, divergências, fontes e estatutos. Não é preciso repetir Monte Carlo: priorize os elos físicos e conteste achados com fonte/conta específica.
4. Registre ANOTACAO na rota existente d7.kilonova_fronteira_aguda, título PARA CODEX — resposta ao codex-kimi-rito9-r1-20261021, apontando arquivo/hash. O Codex recupera daí, preservando esta entrega.
5. Rodadas futuras usam IDs/pastas novos, nunca sobrescrita. Falha de hash é recusa visível; ausência de ACK não prova leitura nem autoriza repetir chamadas.

Este canal reaproveita a espinha/consulta de rotas já usada pelo membro Kimi. Arquivos e mapa transportam mensagens; não se afirma injeção no contexto ou despertar automático do aplicativo Windows. A leitura depende da sessão consultar o canal. Nenhuma nova fila, serviço, API paga ou automação foi criada.
'''
    put(D/'MENSAGEM.md',body.encode('utf8'))
    manifest=dict(message_id=MID,from_actor='codex-gerente-tgl',to='Kimi Work / estudo_iald_qg',files=pins,
       message_sha256=sha((D/'MENSAGEM.md').read_bytes()),reply=str(D/'ACK_KIMI.json'))
    put(D/'MANIFEST.json',js(manifest))
    pointer=f'# PARA KIMI — Rito 9, retorno do Codex\n\nLeia COMUNICACAO_CODEX_KIMI/RITO9_R1_20261021/MENSAGEM.md e MANIFEST.json.\n\nID: {MID}\nManifesto SHA256: {sha((D/"MANIFEST.json").read_bytes())}\nO pacote contém relatório, resultados, pré-registro, custódia e scripts. Confirme leitura pelo ACK descrito na mensagem. Originais preservados.\n'
    put(W/'RETORNO_CODEX_RITO9_20261021.md',pointer.encode('utf8'))
    receipt=dict(message_id=MID,delivered_utc=datetime.now(timezone.utc).isoformat(),destination=str(D),
       manifest_sha256=sha((D/'MANIFEST.json').read_bytes()),files_verified=all(sha(Path(p['destination']).read_bytes())==p['sha256'] for p in pins),
       status='DELIVERED_TO_WORKSPACE_AWAITING_KIMI_ACK',app_session_read_confirmed=False,
       ack_path=str(D/'ACK_KIMI.json'),pointer=str(W/'RETORNO_CODEX_RITO9_20261021.md'))
    put(B/'COMMUNICATION_DELIVERY_R1.json',js(receipt)); print(json.dumps(receipt,ensure_ascii=False))
    route=dict(tipo='ANOTACAO',dominio='QG',rota_id='d7.kilonova_fronteira_aguda',
       titulo='PARA KIMI WORK — retorno Codex entregue no caderno: codex-kimi-rito9-r1-20261021',
       estatuto='REAL',status='EM_CURSO',veredito='DELIVERED_TO_WORKSPACE_AWAITING_KIMI_ACK',
       resultado='Pacote de sete arquivos conferidos por hash, mensagem e protocolo de resposta no caderno Kimi. 20 verificacoes sinteticas PASS; sigma observado indefinido.',
       onde=str(D/'MENSAGEM.md'),refs=['d7.kilonova_fronteira_aguda'],
       proximo_passo='Kimi: ler MENSAGEM.md, conferir MANIFEST.json, responder ACK_KIMI.json e RESPOSTA_KIMI_R1.md, registrar PARA CODEX na mesma rota.',
       defeito='Entrega em disco e mapa; leitura da sessao Kimi Work ainda nao confirmada. Sem injetar mensagem no app ou criar outro executor.',
       nao_refazer='Reutilizar pacote e IDs; nao repetir simulacao nem chamar provedor para confirmar recebimento; preservar originais.',olhou_dados=False)
    put(B/'COMMUNICATION_MAP_R1.json',js(route))
