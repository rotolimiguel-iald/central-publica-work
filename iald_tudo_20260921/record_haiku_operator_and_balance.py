"""Record operator-only activation and remaining gates with immediate byte backups."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import record_admin_boundary_verified as record

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
MARKER = 'IALD_HAIKU_OPERATOR_ONLY_AND_BALANCE_20260922'
NOTE = '''[REAL — saldo] Console da organização IALD LTDA lido em22/09/2026 19:07:03.985UTC: US$98,53, recarga automática desativada. Crédito concedido US$100 em22/09/2026; UI diz expira em23/09/2027, sem hora. Script registrar_saldo_openai.py --provedor claude registrou âncora98.53 no instante lido; contador passou de desconhecido para ok. Recibo work/iald_saldo_claude_20260922/ancora.json. A fonte de gastos ainda é só o razão local; não chamar isso de CostAPI conectada. Duas chamadas reais do operador já constam no razãoSonnet: total2.94166USD,1116340entrada,15081saída,cache0; são uso do operador, não execução dos dois testes controlados/cache pelo agente.

[REAL — Haiku contado no payload instalado] Contagem GRATUITA da Anthropic usando memória instalada, sete ferramentas verificadas, nota real de serviço e pergunta curta:184906tokens. Prefixo do manifesto183135(inclui mensagem mínima na medição-base); saída4096+margem1024 deixam9974tokens adicionais neste pedido. É menor que a reserva REFERENCIAL10271 do manifesto: não confundir referência com espaço atual. Pacote cabe e cumpre o mínimo180k. Recibo installed_haiku_runtime_count_20260922_191637_790423.json. Uma contagem, zero gerações pagas; nenhum perfil, histórico ou resultado de ferramenta incluído nessa medição.

[REAL — opção interna habilitada] activate_haiku_operator_only.py alterou APENAS IALD_HAIKU_ATIVO=1, com backup de bytes protegido e CAS. Conferiu preços/configuração, consentimento Anthropic de luiz, pacote medido e ausência de orçamentos públicos. Política oferece Haiku+Sonnet a luiz; Haiku público continua indisponível. Sem alterar credenciais, seleção atual da conta ou teto global15USD/dia; operador mantém apenas o limite geral existente. Recibo haiku_operator_activation_20260922_161833_156319.json. Reiniciado somente filho web ocioso70816 após zero reservas/slots: novo71684, supervisor41020 preservado, início16:19:02, /health local200, log r13. Nenhuma geração do agente.

[REAL — concorrência e teste] Entre a última implantação e esta verificação, o servidor ganhou alterações paralelas do Selo/exportação. Diff contra stage154903 contém revogação de chave, vínculo opaco da conta, nota de resposta cortada e limites/concorrência de PDF; preservadas. Hash atual lido no recibo de runtime desta entrega. Ainda NÃO há entrada CONCLUSÃO—Selo IALD no CLAUDE.md; aguardar antes de build21/20 integral. Harness haiku_smoke_review.py entregue como rascunho offline,11testes sintéticos do limitador passaram; CLI --execute bloqueado. Não importar segunda instância do servidor nem gravar razãoJSON em processo concorrente. Nenhum endpoint administrativo novo criado. Testes pagos e cache ainda não validados.

[OPEN — decisões e acesso] Pergunta específica enviada: criar chave administrativa Anthropic para custos, nome IALD servidor - leitura de custos, vencimento selecionado21/12/2026 17hBRT; ampla permissão administrativa explicitada. Formulário preparado, botão Adicionar NÃO acionado; aguarda decisão. Chave não criada/não salva. Login da IALD no navegador continua expirado; solicitação enviada para luiz entrar, sem senha na conversa. Não inferir resposta pelo tempo. Orçamento Haiku público1USD/pessoa/dia e5USD/grupo/dia permanece pendente. Dois testesSonnet já autorizados≤2.30USD seguem pendentes de sessão; novo testeHaiku pago ainda não executado/autorizado especificamente.

[MATRIZ] Web: servidor reiniciado, Haiku disponível pela política somente a luiz; seletor visual autenticado pendente. iOS4.1(20) interno/externo Em testes e Apple registra operador instalado20; essa build NÃO contém cliente Haiku/X-IALD-Context e o servidor impede uso Haiku por ela. Android4.1(19) APK/AAB idem; GooglePlay cadastro/DUNS pendente. Próxima entrega21/20 deve incluir Haiku e Selo após conclusão da obra paralela. Avisos de validade e saldo seguem exclusivamente na administração. T1visualCentral e T5exportações físicas pendentes. Meta integral permanece ativa; esta etapa não a conclui.
'''

def main():
    now = datetime.now().astimezone()
    stamp = now.strftime('%Y%m%d_%H%M%S_%f')
    runtime = {'checked_at': now.isoformat(), 'web_child': 71684, 'supervisor': 41020,
               'health_local_status': 200, 'log': 'web-server_20260921_142214_r13.log',
               'operator_only': True, 'public_haiku_enabled': False,
               'paid_generation_calls_by_agent': 0,
               'server_sha256': hashlib.sha256((ROOT/'iald_web_server.py').read_bytes()).hexdigest(),
               'client_sha256': hashlib.sha256((ROOT/'app/iald.js').read_bytes()).hexdigest(),
               'ui_authenticated_verification': 'pending login',
               'native_haiku_client': 'pending next build21/20 and Selo completion'}
    runtime_path = WORK / ('haiku_operator_runtime_' + stamp + '.json')
    record.helper.create(runtime_path, json.dumps(runtime, ensure_ascii=False, indent=2).encode('utf8'))
    targets = [p.with_name('MEMORY_2.md') if p.name == 'MEMORY.md' else p for p in record.helper.TARGETS]
    rows = [record.append(p, MARKER, 'Haiku interno habilitado; saldo Claude registrado',
                          NOTE + '\nRecibo runtime: ' + str(runtime_path), stamp, now) for p in targets]
    receipt = WORK / ('haiku_operator_memory_record_' + stamp + '.json')
    record.helper.create(receipt, json.dumps(rows, ensure_ascii=False, indent=2).encode('utf8'))
    print(json.dumps({'surfaces': len(rows), 'runtime': str(runtime_path), 'receipt': str(receipt)}))

if __name__ == '__main__':
    main()
