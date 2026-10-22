"""Append factual engineering delivery to the established eight surfaces, with immediate byte backups."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os
from task import W,new,check
check('deploy')
d=json.loads((W/'delivery.json').read_bytes());assert d['ios_internal']=='4.1(36) Em testes' and d['ios_external']=='4.1(36) Em testes'
marker='IALD_READABILITY_RELIABLE_TOOLS_20261021'
raw=('\n\n## 21/10/2026 — Interface mais compacta e anexos confiáveis\n<!-- '+marker+' -->\n'
'[REAL] Unidade F9.APP_READABILITY_RELIABLE_TOOLS_20261021:12arquivos instalados por plano/revisão distinta, backups de bytes, reinício somente filho web HTTP200. Tarja permanente removida; prosa15,5px, entrada/edição16px; fórmulas/código preservam tamanho. Áudio/vídeo novos ocultos e recusados no cliente/backend; histórico/custódia antigos preservados. Projeção apenas de envio representa mídia histórica por metadados explícitos, sem upload nem alegar análise; correçãoR2 passou revisão. Documentos/imagens/múltiplos mantidos:6anexos por mensagem, PDF25MB,texto2MB,até3imagens8MBcada; limites de contexto/extração continuam.50MBbase64 não é teto geral de documentos.\n'
'[REAL/DECLARADO] DeepSeek:aliasdeepseek-flash preservado; identificação documentalV4.1-Flash-1017, fontes oficiais conferidas21/10. Atualização17/10 mantém API/tarifas; ganhos de eficiência são declarados pelo fornecedor, sem benchmark novo da IALD. Estimativa conservadora de pico e faixas fora de pico identificadas; sem mudar preferênciaJEV, direitos, carteira ou habilitar ferramentas/visão não integradas. Ciência/kernelv394 preservados; zero chamada nova de modelo para esses ajustes.\n'
'[REAL] Web conferida autenticada:sem tarja, fontes medidas,dois textos anexados e áudio recusado. Android4.1(31):APK/AABassinados,auditados,download autenticado com hash e anônimo302/login; GooglePlay não publicado. iOS4.1(36):Cloudsucesso no commit'+d['commit']+',Equ1/Pil6,ambos Em testes; não é instalação física.\n'
'[DERIVED/OPEN] PropostaACOM/transporte registrada em ACOM_TRANSPORT_PROPOSAL.json, não implantada:ACOM conserva inscrição/estado/proveniência; gzip/Brotli sem perdas é camada distinta,anexos por referências. Não reduz tokens após descompactação nem demonstra ganho de latência; medir upload/roteamento/primeirotoken/stream antes. Nenhum um.py/Lean executado ou gate alterado.\n'
'[EVIDÊNCIAS] '+str(W/'delivery.json')+';validation/review_final.json;deployment.json;restart.json;INSTALLED_VERIFICATION.json;WEB_LIVE_VALIDATION.json;mobile_stage/AUDIT.json;IOS_DISTRIBUTION.json;ANDROID_AUTH_DOWNLOAD.json. Referência própria SESSION_REFERENCE.json.\n<!-- END_'+marker+' -->\n').encode()
old=W.parent/'mimo_media_capacity_20261020/memory_stage/FINAL_R4/PLAN.json'
stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f');receipts=[]
for item in json.loads(old.read_bytes())['surfaces']:
    p=Path(item['path']);before=p.read_bytes();assert marker.encode() not in before
    bak=p.with_name(p.name+'.bak_'+stamp);bak.open('xb').write(before);assert bak.read_bytes()==before
    after=before+raw;tmp=p.with_name(p.name+'.tmp_'+stamp);tmp.open('xb').write(after);assert tmp.read_bytes()==after
    assert p.read_bytes()==before;os.replace(tmp,p);assert p.read_bytes()==after
    receipts.append(dict(path=str(p),backup=str(bak),before_sha256=hashlib.sha256(before).hexdigest(),after_sha256=hashlib.sha256(after).hexdigest()))
new('MEMORY_APPLIED.json',dict(status='APPLIED_8_ADDITIVE_SURFACES',surfaces=receipts))
print('8 operational memory surfaces appended and verified')
