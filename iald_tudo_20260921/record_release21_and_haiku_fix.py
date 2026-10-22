"""Append verified delivery/runtime state with immediate byte backups."""
from datetime import datetime
import json
from pathlib import Path
import record_admin_boundary_verified as record

W=Path(__file__).resolve().parent
MARKER='IALD_RELEASE21_HAIKU_TOOL_WINDOW_FIXED_20260923'
NOTE='''[REAL — distribuição coordenada, 23/09/2026] Web e recursos mobile compartilhados sincronizados com Haiku, Selo IALD e exportação de conversas, preservando a separação dos avisos internos. iOS4.1(21) compilado com sucesso no Xcode Cloud e Em testes tanto no IALD Equipe quanto no IALD Piloto, conferidos na Apple. Notificação automática do grupo externo marcada. Build b0da2779-223c-4470-854f-32bfb5b806a4. A Apple mostrou90dias, não data exata; expires_at continua null no registro administrativo. Android4.1(20) APK/AAB compilados e assinados; APK disponível em https://demo.iald.ia.br/downloads/IALD-4.1-20.apk (exige login). GooglePlay continua dependente de cadastro/DUNS. Recibos: release21_audit_20260923_083516_617371.json, android20_20260923_083715_070156.json, release21_delivery_20260923_085432_825498.json. Commit privado lido/conferido no registro de implantação; nenhum servidor, .env ou chave enviado ao repositório mobile.

[INPUT/REAL — aparelho] O operador confirmou: “Atualizei e salvei os três formatos”, referindo-se ao iPhone com21, Texto/Markdown/PDF→Compartilhar→Salvar em Arquivos. O PDF enviado posteriormente contém apenas uma pergunta,0respostas, e diz corretamente SEM SELO; não certifica uma resposta que o modelo não chegou a produzir. Os testes anteriores82Selo/exportação e6clienteHaiku passaram. Convites por email de Alana e Liana ainda aparecem Convidado. Há2participantes anônimos pelo link público (não atribuir identidades por hipótese). Link conferido https://testflight.apple.com/join/A5XEdy1H, limite10/2utilizados; versão21 disponível ao grupo, instalação de familiares não confirmada.

[REAL — causa do erro Haiku] O aviso “A memória, a conversa e a resposta excedem a janela configurada; nada foi enviado” ocorreu após consultas de ferramentas, não na carga inicial. Log r15 registrou kernel_list, README/search_tgl e leituras Lean. Razão de23/09 observado antes da correção:3chamadasHaiku, não zero. O contador nativo gratuito mediu a pergunta inicial em184924tokens; list100+search5 em194705, restando175depois de saída4096+margem1024, antes do README e outras diferenças da conversa. Não confundir reconstrução representativa com captura literal da requisição.

[REAL — correção instalada] claude_tool_budget.py limita explicitamente somente os resultados do último lote de ferramentas quando faltaria espaço. Mantém núcleo183135, conversa, pergunta, texto/argumentos do assistente e os7schemas. Preserva metadados, estatutos/negativos, hash do resultado original, trechos integrais por linha/entrada e indicação de retomada; excerto é parcial, não prova completa. Conta o payload nativo final, reserva4096+1024 e força conclusão sem novas ferramentas quando necessário. Se não couber, recusa visível; sem remoção silenciosa de histórico ou redução do núcleo. Aviso distingue primeira recusa de próxima volta bloqueada após chamadas anteriores. Nenhuma mudança de fontes/cânone/gate. O modelo ainda precisa articular corretamente o que leu: orçamento caber não prova correção científica.

[REAL — regressões e revisão] Stage haiku_window_final_20260923_090543_249253:7contratos do orçamento,5fluxos chat/agente/conta/transport,139rotasClaude e62acessoNativo passaram (213/0). Provedor e contagens nesses testes são fixtures. Reprodutor falhava no código anterior e passou no corrigido. Revisão independente do merge/guardaIDs confirmou quatro funções de servidor previstas e demais bytes intactos, inclusive Selo. R1 foi integrado: seleção de modelo respeita SDK/contexto realmente disponíveis e recusa antes de gravar a escolha. Contagem GRATUITA adicional com núcleo real+5resultados públicos representativos:200048→193773 de entrada; mais4096saída+1024margem deixa1107. Recibo haiku_final_case_measurement.json vincula hash do helper.8contagens gratuitas nesta investigação, zero novas gerações pagas feitas pelo agente; as chamadas do operador são separadas.

[REAL — produção] haiku_window_installed_20260923_090800_020864.json: três arquivos instalados com bases pinadas, backups imediatos byte a byte e replace atômico. Antes do reinício:0reservas,0slotsnativosprocessando. Reiniciado somente web62324; supervisor41020 preservado. Novo web34516 em23/09/2026 09:08:29, logr16. Hashes dos3arquivos instalados conferem com manifesto; /health200 e /app/iald.js200; /api/alertas401 e /admin/api/prazos401 sem sessão. Ajuste de servidor vale para web/iOS21/Android20 sem recompilar. Prazos/saldo continuam somente na administração, nunca no app ou no contexto da IA.

[REAL — saldo administrativo] Anthropic UI observada2026-09-23T11:40:18.351Z:US$96.24, registrada pelo script existente. Recarga automática desativada; crédito com data23/09/2027, sem hora publicada. Não confundir âncora com saldo após novas chamadas. Nenhuma AdminAPIkey criada e nenhum pagamento executado.

[OPEN] Reteste físico de geração Haiku após correção solicitado ao operador; não declarar resposta real validada só por fixtures/contagem. Haiku continua apenasLuiz enquanto orçamento público não aprovado. Duas mensagens/cacheSonnet ainda não certificadas nesta entrega; saldo via APIadministrativa continua aguardando decisão específica. Central Usuáriosdoapp: validação visual do operador pendente. Android: teste físico/GooglePlay pendentes. LoginsApple/IALD e handoffSelo, antigos bloqueios, foram resolvidos; não pedir novamente sem expiração observada. Preservar atualização conjunta e este estado nas próximas sessões.
'''

def main():
    now=datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f')
    targets=[p.with_name('MEMORY_2.md') if p.name=='MEMORY.md' else p for p in record.helper.TARGETS]
    rows=[record.append(p,MARKER,'iOS21/Android20 distribuídos; janela de ferramentas Haiku corrigida',NOTE,stamp,now) for p in targets]
    receipt=W/('release21_haiku_memory_'+stamp+'.json')
    record.helper.create(receipt,json.dumps(rows,ensure_ascii=False,indent=2).encode('utf8'))
    print(json.dumps({'surfaces':len(rows),'receipt':str(receipt)}))

if __name__=='__main__':main()
