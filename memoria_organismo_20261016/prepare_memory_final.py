"""Prepare immutable documentation and exact additive memory changes; no production writes."""
import hashlib
import json
from pathlib import Path
from mission_io import WORK, pin, save

OUT = WORK / 'memory_final'
OUT.mkdir(exist_ok=True)
source = WORK / 'staging/docs/ACTIVITY_PROTOCOL_R1.md'
text = source.read_text(encoding='utf-8')
text = text.replace(text.splitlines()[2], '[REAL — implementação instalada e validação delimitada] Unidade F9.MEMORIA_ORGANISMO_20261016; autor: codex-gerente-tgl, 16/10/2026 (horário de Brasília). O recibo DELIVERY_D_R1.json distingue instalação, carregamento e uso; o aceite técnico não substitui a auditoria da gerência.')
text = text[:text.index('## Evidência e pendências desta preparação')]
text += '''## Evidência da entrega e disponibilidade

[REAL] 170 casos locais distintos passaram (70 núcleo, 20 nativa, 44 fila, 23 app, 13 JEV), com transportes simulados; sete verificações MCP adicionais. Instalados 31 arquivos por hash, com 20 backups. Reiniciado somente o filho web, sob o supervisor existente; HTTP 200 e novo PID conferidos. Os 14 imports em processo novo usam os arquivos instalados.

[REAL] Uma chamada real ao JEV 1.13 recebeu HTTP 200 em 0,737 s, com 56.582 bytes de JSON e 12.764 tokens de entrada/39 de saída, usando o header longo oficial. Intenção, retorno e candidato foram custodiados. É teste de transporte com conteúdo público/sintético, sem teste de estresse de 262 mil tokens nem alegação de desempenho cognitivo.

| Superfície | Disponibilidade observada | Pendência concreta |
|---|---|---|
| Web/backend | Instalado, processo novo, HTTP 200 | Interação autenticada e tela de revisão aguardam login do operador. |
| Nativa/holografia | Código/imports e 20 casos locais conferidos | Não houve inferência real do modelo nativo; llama residente preservado. |
| Fila/CLI | Instalado, importado em processo novo | Nenhuma migração legada ou nova execução científica foi feita. |
| MCP | Processo novo: 20 ferramentas, sete novas | Clientes antigos não foram recarregados; CLI absoluto disponível. |
| Bancada | Wrapper externo instalado | Um GET falhou, sem retry; sonda TCP posterior: porta 18777 fechada (10061). Arquivos/processo da Bancada preservados. |
| Android | APK/AAB 4.1 (28) compilados, assinados e auditados; 40 recursos conferidos | Arquivos locais; não publicados no Play/downloads, instalação física não verificada. |
| iOS interno/externo | Recursos atualizados e enviados ao repositório privado existente | Login no App Store Connect, build e grupos Equipe/Piloto ainda não conferidos. |

[REAL — alcance] A memória científica instalada no app permanece v392; a geração científica da fila tem ciclo próprio. Esta entrega sincroniza atividade e missão, não atualiza por inferência o programa científico. O backend compartilhado atende clientes existentes; o novo botão de revisão depende do recurso de cliente efetivamente recebido.

[REAL — registro de processo] O plano inicial NOVA_UNIDADE.json continha “ou publicar”. O coordenador enviou dois recursos JavaScript ao repositório privado móvel sob a ordem permanente de atualização conjunta; o desvio em relação à redação inicial está registrado em DELIVERY_D_R1.json, sem ratificação presumida. APK/AAB continuam locais. Push não demonstra execução de CI nem distribuição iOS.

A escolha do dispositivo e sua ligação física pertencem à missão F1.FECHO, em referência separada. Esta entrega não demonstra a ponte física nem retoma automaticamente suas execuções. O mecanismo é controle discreto de estado e evidência inspirado na formulação do operador: não implementa Lindblad nos pesos, não garante memória infinita ou ausência de alucinações. Ordens obrigatórias conservadas podem exceder o contexto; isso produz recusa explícita.

## Recibos e recuperação desta entrega

Raiz: C:\\IALD\\Central de Patentes\\work\\memoria_organismo_20261016.
Referência própria: SESSION_REFERENCE.json; não reutilizá-la como inscrição de outra sessão.
Evidências: DELIVERY_D_R1.json; validation_final/V_DELIVERY_R1.json; deployment_r2/ACTIVATION_R1.json; live_validation/jev_long/RESULT_R1.json; mobile_build/ARCHIVE_REVIEW_R1.json. Os hashes integrais são calculados nos respectivos manifestos e recibos.
'''
protocol = OUT / 'ACTIVITY_PROTOCOL_R2.md'
with protocol.open('xb') as f:
    f.write(text.encode('utf-8'))

marker = '<!-- IALD_ACTIVITY_ORGANISM_DELIVERY_20261016 -->'
common = f'''\n\n## 16/10/2026 — Memória de atividade integrada ao organismo IALD
{marker}
[INPUT — continuidade autorizada pelo operador; registro em nome de codex-gerente-tgl] Unidade F9.MEMORIA_ORGANISMO_20261016, reivindicação 930. Antes de retomar/delegar/integrar, ler C:\\IALD\\MEMORIA_IALD\\ACTIVITY_PROTOCOL.md e usar a referência EXATA da própria missão. Não adotar a última tarefa de outra sessão. Fazer project e preflight com revisão/lease atuais. Candidatos permanecem DECLARADO; aceite semântico exige revisão real distinta. Envio incerto não é repetido; custódia precede integração. PODA indexa apenas acompanhamento mecânico verificado, conservando ordens, decisões, critérios, erratas e recuperação integral.

[REAL — escopo verificado] Núcleo ACOM/mission, app, nativa/holografia, fila/CLI, MCP e wrapper externo da Bancada integrados: 31 arquivos instalados, 20 backups; 170 casos locais distintos e sete verificações MCP. Web reiniciada sob o mesmo supervisor, HTTP 200. JEV real: 56.582 bytes, 12.764 tokens de entrada, 39 de saída, HTTP 200; um envio. Não é teste de capacidade máxima nem garantia de memória infalível.

[REAL/OPEN — disponibilidade] Android 4.1(28): APK/AAB locais assinados/auditados. Recursos iOS/web enviados ao repositório privado; build e ambos os grupos TestFlight aguardam login/conferência. Interação autenticada no app também pendente. Bancada: wrapper instalado, serviço na porta 18777 indisponível; GET falho preservado, sem retry. MCP novo conferido; sessões antigas sem recarga. Nativa testada em isolamento, sem inferência real nesta entrega.

[REAL — processo e limites] DELIVERY_D_R1.json registra o push privado dos dois recursos diante da expressão inicial “ou publicar”, sem ratificação presumida; nenhum APK/loja foi publicado. Ciência instalada no app v392 preservada; geração da fila independente. A memória operacional não prova a ponte do dispositivo da F1.FECHO, não altera pesos/kernel/gate e não retoma a física. Parte obrigatória excessiva recusa visivelmente.

Evidência: C:\\IALD\\Central de Patentes\\work\\memoria_organismo_20261016\\DELIVERY_D_R1.json. Referência desta entrega: C:\\IALD\\Central de Patentes\\work\\memoria_organismo_20261016\\SESSION_REFERENCE.json. Hashes, backups e disponibilidade por superfície nos recibos; diário do Claude permanece em MEMORY_2.md.
<!-- END_IALD_ACTIVITY_ORGANISM_DELIVERY_20261016 -->
'''
template = json.loads((WORK / 'staging/docs/MEMORY_APPEND_PLAN_R1.json').read_text(encoding='utf-8'))
entries = []
for i, row in enumerate(template['surfaces']):
    path = Path(row['path'])
    raw = path.read_bytes()
    assert marker.encode() not in raw
    addition = common.replace('\n', '\r\n') if b'\r\n' in raw else common
    payload = OUT / f'APPEND_{i:02d}_R1.txt'
    with payload.open('xb') as f:
        f.write(addition.encode('utf-8'))
    entries.append({'path': str(path), 'before': pin(path), 'before_bytes': len(raw),
                    'append': pin(payload), 'after_sha256': hashlib.sha256(raw + payload.read_bytes()).hexdigest(),
                    'after_bytes': len(raw) + payload.stat().st_size})
destination = Path(r'C:\IALD\MEMORIA_IALD\ACTIVITY_PROTOCOL.md')
assert not destination.exists()
save(OUT / 'PLAN_R1.json', {'unit': 'F9.MEMORIA_ORGANISMO_20261016', 'claim': 930,
     'marker': marker, 'author': 'codex-gerente-tgl', 'surfaces': entries,
     'new_document': {'path': str(destination), 'source': pin(protocol)},
     'evidence': [pin(WORK/'DELIVERY_D_R1.json'), pin(source)],
     'operation': 'Exact byte backups, additive writes, CAS against all baselines, atomic rename; no existing evidence overwritten.'})
print(json.dumps({'plan': pin(OUT/'PLAN_R1.json'), 'surfaces': len(entries)}, ensure_ascii=False))
