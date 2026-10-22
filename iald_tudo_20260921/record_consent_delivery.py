from pathlib import Path
from datetime import datetime
import json,os
import record_haiku_preparation as record
p=Path(r'C:\IALD\projetos_pyhton\IALD\iald_deadlines.json')
raw=p.read_bytes();data=json.loads(raw)
stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
for key,group in [('testflight_internal','IALD Equipe'),('testflight_external','IALD Piloto')]:
 data['items'][key].update(label='IALD 4.1 (19) — '+group,expires_at=None,
 source='App Store Connect, 22/09/2026: Em testes; Expira em 90 dias. Data exata não exibida; não inferida.',
 build='4.1 (19)',status='Em testes')
data['checked_at']=datetime.now().astimezone().isoformat()
p.with_name(p.name+'.bak_'+stamp).write_bytes(raw)
tmp=p.with_name(p.name+'.tmp_'+stamp)
new=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
tmp.write_bytes(new);assert tmp.read_bytes()==new and p.read_bytes()==raw
os.replace(tmp,p)
record.MARKER='IALD_CONSENT_BUILD19_DELIVERED_20260922'
record.NOTE='''[REAL — entrega corretiva concluída na distribuição] Commit bad5257ed5ea4823ffe2ed97861d1330f843ecfc publicado no destino privado autorizado. Cloud19 cd90c711-fc3a-4877-9459-de7220ea9d50 gerou TestFlight4.1(19), id23f7df19-2604-40c8-a3f3-d7eef2941bac; carregamento22/09/2026 12:47BRT. Vínculo interno IALD Equipe confirmado Em testes; vínculo externo IALD Piloto confirmado Em testes após envio das notas e revisão. Notificação automática aos testers mantida. Mãe e esposa já pertencem ao grupo. Confirmada participação de Luiz Antonio Rotoli Miguel no grupo interno, cuja última instalação exibida pela Apple ainda é4.1(17) em22/09. Instalação19 e aceite físico precisam do operador; não declarados feitos.

[REAL — causa adicional] git show7487412:www/iald.js (build17) confirmou consentirEContinuar chama responderConsentimento(true) sem provedor/versão. Servidor trata provedor ausente comoOpenAI legado e recusa409 quando motorClaude. Build18 já transportava Anthropic; build19 acrescenta correção de layout e robustez. Isto explica o bloqueio se o aparelho ainda roda17, versão que a Apple registra. Nenhuma autorização foi gravada em nome do usuário durante a correção.

[REAL — validação] Seis regressões NodeVM sobre funções reais passaram: aceite/provedor/versão, clique duplicado, offline, JSONinválido, provedor divergente, conflito409 e aviso incompleto (casos combinados em6testes). Bancada CUA validou retrato/paisagem e rodapé44px visível. Android18 APK/AAB compilados, assinatura oficial mesma da17, assetsinternos idênticos aos três arquivos corrigidos; cópia em downloads/IALD-4.1-18.apk, recibo android18_20260922_124536.json. Web arquivos atuais em disco e rota send_from_directory conferida; acesso remoto anônimo leva ao login, validação web autenticada pendente. Sem reinício web.

[MATRIZ] Web: fonte atualizada, recarregamento autenticado pendente. iOS interno:4.1(19)Em testes, operador confirmado. iOS externo:4.1(19)Em testes, grupo4testers. Android:18APK disponível em downloads, AABlocal; GooglePlay não enviado(cadastro/DUNS). Instalação/teste físico:pendente. Link público existente https://testflight.apple.com/join/A5XEdy1H preservado, não recriado. Prazos operacionais atualizados com rótulo19/status; expiração exata nula pois Apple exibiu apenas90dias. Não inferir horário de vencimento.

[OPEN — objetivo maior] Sonnet teste pago/cache e Haiku>=180k não concluídos. Cicero entregou proposta section_capsules/form_canonica_viva.md, provenance.json e LIMITACOES.md: economia6880o200k, ainda não aprovada/integrada; revisão independente e remapeamento61@EXPOSITIONpendentes. Contagem nativa anterior continua excedendo janela Haiku. Nenhuma memória científica original alterada.
'''
record.main()
