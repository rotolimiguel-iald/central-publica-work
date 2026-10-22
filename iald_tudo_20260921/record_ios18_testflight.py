"""Record verified internal and external TestFlight availability and open tests."""
import record_haiku_preparation as record

record.MARKER = 'IALD_IOS18_TESTFLIGHT_BOTH_GROUPS_20260922'
record.NOTE = '''[REAL — compilação e processamento] Xcode Cloud execução9e2530cb-e3f9-4643-a633-0a3e8e9c6b67 terminou SUCCESS,9min, commit e87d3b52d9d774b3dda06c46e745e161efdc184b. GitHub status success em22/09/2026 14:22:11UTC. Cinco avisos de plugins (variáveis não usadas/imutável e coerção String?), nenhum erro. TestFlight binário4.1(18),ID4ef5b36b-9e8c-410c-abe1-4b06d14fbc1e, validado,br.ia.IALD,iPhone+iPad,iOSmínimo15. Data de carregamento exibida22/09/2026 11:17.

[REAL — distribuição autorizada concluída] Texto O que testar salvo exatamente como ordem: Exportar conversa (texto, Markdown e PDF) pelo compartilhar do aparelho; tocar no nome do modelo e trocar de modelo; consentimento de IA de terceiros por provedor. Selecionados IALD Equipe e IALD Piloto, envio para revisão beta concluído com notificação automática selecionada. Depois conferidos os dois grupos individualmente:4.1(18) EM TESTES em ambos, expira em90dias (texto Apple observado). Não inferir timestamp exato dessa contagem; metadados não mostraram vencimento e atributos DOM do indicador tampouco.

[REAL — participação] IALD Equipe tem operador Luiz Antonio Rotoli Miguel como tester interno; painel ainda apontava instalada4.1(17), portanto18 está DISPONÍVEL, não confirmar instalada no aparelho do operador. IALD Piloto4testers; Alana e Liana constam CONVIDADAS, sem instalação confirmada. Link público vigente https://testflight.apple.com/join/A5XEdy1H,2de10entradas do link usadas. Há registro anônimo de18instalada; não atribuir a pessoa específica. Nenhum novo convite duplicado criado.

[MATRIZ] Web/servidor: janelaSonnet ajustada e filho76756 saudável conforme nota anterior, sem alteração de cliente nesta etapa. iOSinterno18EMTESTES; iOSexterno18EMTESTES. Android17 APK/AAB compilados, download autenticado e GooglePlay pendentes. Testes físicos txt/md/pdf/cancelamento no iPhone,iPad,Android14 e≤10(sehouver) ainda pendentes; não declarar exportação resolvida só por compilação.

[REAL/OPEN — memória/modelos] Contagem gratuita atual do rascunho Haiku SHA70344cd27bca5f733b52a1d5bfce121ee99abf5deb41fc5ed208c4cdf42fcbc5:220651tokensAnthropic,baseline9,14:21:32UTC; nenhum pedido de geração. Precisa reduzir~40k até180k preservando essenciais. Revisor adversarial Cicero,agent01a0c97e-fb7b-7510-8d5d-1ec2bbea845e, está revisando somente pacote/localauditoria na pasta adversarial_memory_review; não editar produção, nãoAPIpaga. Wait10s retornou timeout, não terminal; não duplicar agente. Tarefa paralela justificada pela regra AGENTS quem constrói não aprova. Sonnet testes/cache aguardam loginluiz (aba10 /login); consentimento e tetosUS$2+0,30 já autorizados. fetch_tgl.pointer continua aguardando autorização específica, não contornar rejeição. Objetivo integral ativo/incompleto.
'''

if __name__ == '__main__':
    record.main()
