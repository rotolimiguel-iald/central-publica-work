"""Append the measured app delivery to existing memories; byte backups + CAS."""
from pathlib import Path
from datetime import datetime
import hashlib, json, os, subprocess

work=Path(__file__).parent
root=Path(r'C:\IALD\projetos_pyhton\IALD')
stamp=datetime.now().astimezone().strftime('%Y%m%d_%H%M%S_%f')
now=datetime.now().astimezone().isoformat()
marker='IALD_APP_PERSONAL_MODELS_AND_STREAM_20260930'
previous=json.loads((work.parent/'iald_user_identity_20260923/delivery_20260923_205659_521301.json').read_text(encoding='utf-8'))
installed=json.loads((work/'installed_20260930_144614_971864.json').read_text(encoding='utf-8'))
android=json.loads((work/'android_delivery.json').read_text(encoding='utf-8'))
calls=json.loads((work/'live_evaluation.json').read_text(encoding='utf-8'))
success=next(r for r in calls if r['status']=='completed')
commit=subprocess.check_output([r'C:\Program Files\Git\cmd\git.exe','rev-parse','HEAD'],cwd=root/'iald-app',text=True).strip()
report={'at':now,'mobile_commit':commit,
 'web':'installed, supervisor restarted, authenticated UI verified',
 'ios':{'build':'4.1 (25)','id':'a96a9ea7-e28d-469d-9960-ff4ddfb8ddf2',
  'cloud_run':'8f0f51f0-098a-4675-88b6-6125dcc17e2a','cloud':'Processada com sucesso',
  'internal':'Em testes','internal_testers':1,'external':'Em testes','external_testers':6,
  'physical':'User says Ainda vou testar','invite':'https://testflight.apple.com/join/A5XEdy1H'},
 'android':android,'metrics':calls,
 'validation':{'transport_cases':16,'route_cases':9,'stream_math_checks':149,'dom_checks':65,
  'android_build':'assembleRelease + bundleRelease successful','ios_build':'Xcode Cloud successful',
  'new_paid_app_probe':'one controlled DeepSeek probe completed; separate prior uncertain record preserved',
  'kimi_mimo':'transport offline tests and existing stack readiness; no new complete app generation verified'},
 'files':{p:{'bytes':Path(p).stat().st_size,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in installed},
 'memory':[]}

note=f'''

## 30/09/2026 — App: avaliação pessoal de modelos e correção do streaming

<!-- {marker} -->

[INPUT] Novos Kimi, DeepSeek e MiMo disponíveis SOMENTE para luiz, conforme resposta expressa do operador. Atualização conjunta das superfícies afetadas. Nenhuma alteração do cânone, kernel científico, gate ou originais de um.py; fine-tuning permanece adiado.

[REAL — implementação] iald_app_providers.py integra DeepSeek deepseek-flash (V4.1 Flash documentado, alias), MiMo mimo-v2.6-pro e Kimi kimi-code/k3. Reutiliza os cofres/clientes existentes, sem nova chave, sem credenciais no app e sem mutações da fila científica. Restrição de conta aplicada no servidor, consentimento separado por provedor, sem fallback/repetição após envio incerto. DeepSeek e MiMo têm SSE e ferramentas públicas científicas restritas; Kimi usa CLI textual, recuperação prévia e resposta completa ao final, sem simular streaming. Sonnet configurado como claude-sonnet-5-5; último Haiku confirmado na documentação consultada permanece 4.5. Não modificar .env nem conta pública para promover modelos.

[REAL — memória] Os três novos motores recebem o MESMO pacote fixo verificado do kernel/core/cluster usado pelo Haiku, preservado por bytes, com consultas de detalhes. Pacote medido antes do envio: 485.985 bytes; 183.135 tokens são a contagem Anthropic, não o tokenizer dos outros provedores. A chamada DeepSeek concluída mediu {success['calls'][0]['input_tokens']} tokens de entrada com seu envelope. O hash do prefixo lido do recibo é {success['memory_sha256']}. Não é o acervo integral, nem treinamento nos pesos, nem demonstração de compreensão integral. Limite conservador por bytes e reserva de saída, sem redução silenciosa do núcleo. Atlas privado da Central não enviado.

[REAL — interface] Parser SSE trata UTF-8 e fronteiras CR/LF, eventos multilinha e encerramento ausente. Renderização preserva fórmulas parciais, cache KaTeX limitado e nós completos durante streaming; correção PT-BR não altera TeX/código. Teste real identificou cabeçalho exibindo a Nativa após selecionar DeepSeek: api/active-model corrigido para os três motores, com janela e visão coerentes. Aceite, cadastro, exportação e correção UIScene existentes preservados.

[REAL — painel interno] /admin/avaliacao-modelos e /admin/api/avaliacao-modelos exigem operador luiz e localhost. Registros em .iald_runtime/app_evaluation/metrics.sqlite3 guardam modelo, tempos, uso/cache, custo estimado e hash da memória, sem prompts/respostas/chaves. Conversas dos transportes antigos observadas sem alterar seus bytes; consumo ausente fica desconhecido. Kimi é assinatura, não custo zero. Métricas/prazos não aparecem no chat. Jev permanece não habilitado como chat: possível auxiliar de decisão estruturada, sem atuação como juiz de prova.

[REAL — verificação] 16 casos de transporte, 9 de rotas reais isoladas, 149 verificações SSE/TeX e 65 DOM passaram. Releases Android e iOS compilaram. Um teste controlado DeepSeek na UI autenticada confirmou autor, beta e nome do núcleo: primeiro texto {success['first_text_seconds']} s, total {success['elapsed_seconds']} s, saída {success['calls'][0]['output_tokens']} tokens, cache {success['calls'][0]['cached_tokens']} tokens, custo estimado US$ {success['calls'][0]['cost_estimate_usd']}. Não é benchmark de física ou custo sem cache. Há outro registro anterior failed_or_uncertain/ValueError, sem consumo conhecido, preservado e não repetido por esta verificação; sua causa não foi recuperada do registro. MiMo/Kimi têm testes de transporte simulados e conexão do stack existente, sem nova geração completa do app certificada nesta entrega.

[REAL — distribuição] Commit mobile {commit}. Web instalada e conferida autenticada; iOS 4.1 (25), build a96a9ea7-e28d-469d-9960-ff4ddfb8ddf2, Cloud 8f0f51f0-098a-4675-88b6-6125dcc17e2a processada com sucesso; IALD Equipe (1) e IALD Piloto (6) vinculados e Em testes, notificação automática habilitada. Convite existente https://testflight.apple.com/join/A5XEdy1H. Android 4.1 (22), APK/AAB assinados, assets conferidos contra web; link autenticado {android['download']}, APK SHA256 {android['apk_sha256']} ({android['apk_bytes']} bytes). Google Play continua sem publicação nesta entrega: pendência anterior de cadastro/DUNS não resolvida. Vencimento exato TestFlight não exibido; registrar apenas observação 90 dias e data de checagem na administração, sem inventar data exata.

[OPEN — físico] Operador respondeu “Ainda vou testar” após liberação da 25. Instalação/teste em iPhone/iPad/Android não confirmados. Avaliação comparativa de qualidade/custo deve usar perguntas equivalentes e conferir hashes/cobertura de memória; não atribuir ganho matemático só pela renderização. Evidências: {work}/delivery.json e live_evaluation.json.
'''

def replace_with_backup(path,data):
    before=path.read_bytes()
    backup=Path(str(path)+'.bak_'+stamp)
    backup.write_bytes(before)
    assert backup.read_bytes()==before
    temp=Path(str(path)+'.tmp_'+stamp)
    temp.write_bytes(data)
    assert temp.read_bytes()==data and path.read_bytes()==before
    os.replace(temp,path)
    assert path.read_bytes()==data
    return {'path':str(path),'backup':str(backup),'sha256':hashlib.sha256(data).hexdigest()}

for item in previous['memory']:
    path=Path(item['path']);old=path.read_bytes()
    assert marker.encode() not in old,'Already recorded; inspect rather than duplicate'
    data=old+note.encode('utf-8')
    assert len(data)>len(old)
    report['memory'].append(replace_with_backup(path,data))

path=root/'iald_deadlines.json'
deadlines=json.loads(path.read_text(encoding='utf-8'));deadlines['checked_at']=now
for key,group in [('testflight_internal','IALD Equipe'),('testflight_external','IALD Piloto')]:
    deadlines['items'][key].update(expires_at=None,label='IALD 4.1 (25) — '+group,
       build='4.1 (25)',status='Em testes',
       source='App Store Connect '+now+': Em testes; Expira em 90 dias; data/hora exatas não exibidas.')
report['deadline_record']=replace_with_backup(path,(json.dumps(deadlines,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
target=work/'delivery.json'
assert not target.exists()
data=json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8')
temp=target.with_suffix('.json.tmp');temp.write_bytes(data)
assert temp.read_bytes()==data;os.replace(temp,target)
print(json.dumps({'delivery':str(target),'memories_updated':len(report['memory']),'mobile_commit':commit},ensure_ascii=False))
