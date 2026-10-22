from support import *
import re,collections
D=ROOT/'heartbeat'
rows=json.loads((D/'POR_MODULO.json').read_text(encoding='utf-8'))
mods={r['module'] for r in rows}
# Refine attribution from the exact diagnostic, never a later error in the context window.
refined=[]
for e in json.loads((D/'TIMEOUTS_OBSERVADOS.json').read_text(encoding='utf-8')):
 lines=Path(e['local_log']).read_text(encoding='utf-8-sig').splitlines();n=e['line']-1
 owner=[]
 for l in reversed(lines[max(0,n-30):n+1]):
  owner=[m for m in mods if re.search(re.escape(m)+r'\.lean:\d+',l)]
  if owner:break
 if e['module'] not in owner:continue
 diagnostic=lines[n]
 kind='synthInstance.maxHeartbeats' if 'typeclass' in diagnostic or 'synthInstance.maxHeartbeats' in '\n'.join(lines[n:n+5]) else 'maxHeartbeats'
 vals=re.findall(r'maximum number of heartbeats \((\d+)\)',diagnostic)
 e.update(kind=kind,reported_budget=int(vals[0]) if vals else None,diagnostic=diagnostic)
 refined.append(e)
record(D/'TIMEOUTS_ATRIBUIDOS.json',refined)
bmods={'TheSameBetaReadsThreeFaces':1,'FLRWGeometry':2,'FLRWFieldEquations':2,'SectorFluidClosure':3,'SectorFriedmann':3,'ThermodynamicFriedmann':4,'SectorRouteComparison':5,'TheAngleReachesTheMetric':5}
for r in rows:
 m=r['module'];r['observed_timeouts']=[e for e in refined if e['module']==m]
 for c in r['caps']:c['scope']='local command' if re.search(r'\bin\s*$',c['text']) else 'remaining source file'
 r['declared_budget_mentions']=[q for q in r['declared_budget_mentions'] if re.search(r'heartbeat|budget|or[cç]amento|expensive|timeout',q['text'],re.I) and (m not in bmods or f'ENTREGA_012_B{bmods[m]}_' in q['source'] or q['source']==r['source']['path'])]
 r['declared_scope']='Mencoes documentais sao citacoes de contexto; contar limite ou relatar timeout nao explica por si a escolha do numero final. Fontes de entrega conjunta podem descrever outro modulo; prevalece a atribuicao literal.'
 r['general_timeout_events']=sum(e['kind']=='maxHeartbeats' for e in r['observed_timeouts'])
 r['typeclass_timeout_events']=sum(e['kind']=='synthInstance.maxHeartbeats' for e in r['observed_timeouts'])
 r['observed_mechanisms']=sorted(set(re.findall(r'timeout at `([^`]+)`','\n'.join(e['diagnostic'] for e in r['observed_timeouts']))))
 r['historical_attempts_with_timeout']=len({e['log']['path'] for e in r['observed_timeouts']})
 r['interpretation']=('OBSERVADO: '+', '.join(r['observed_mechanisms'])+' esgotou orçamento em '+str(r['historical_attempts_with_timeout'])+' stream(s) histórico(s). Snapshots e orçamento de cada diagnóstico estão pinados. Esse fato não estabelece a necessidade do limite final.' if r['observed_timeouts'] else 'ABERTO: não foi localizado diagnóstico de esgotamento atribuível ao módulo no corpus lido. Não se afirma que ele nunca ocorreu.')
record(D/'POR_MODULO_INTERPRETADO.json',rows)
# Pin the actual toolchain defaults; the units are thousands of small allocations, not seconds.
defaults=[]
for sub in ['Lean/CoreM.lean','Lean/Meta/SynthInstance.lean']:
 p=BIN.parent/'src/lean'/sub;s=p.read_text(encoding='utf-8');lines=s.splitlines();opts=[]
 for i,l in enumerate(lines):
  if re.match(r'register_builtin_option (?:maxHeartbeats|synthInstance.maxHeartbeats) ',l):opts.append(dict(line=i+1,excerpt='\n'.join(lines[i:i+4])))
 defaults.append(dict(path=str(p),sha256=digest(p),options=opts))
record(D/'DEFAULTS_TOOLCHAIN.json',defaults)
counts=dict(modules=len(rows),explicit_general_caps=sum(any(c['kind']=='maxHeartbeats' for c in r['caps']) for r in rows),observed_modules=sum(bool(r['observed_timeouts']) for r in rows),general_timeout_modules=sum(r['general_timeout_events']>0 for r in rows),typeclass_timeout_modules=sum(r['typeclass_timeout_events']>0 for r in rows),diagnostics=len(refined),not_44_recompiled='Leitura historica dos 44; compilacao desta entrega cobre o fecho alterado, nao um perfil de custo de todos os 44.')
record(D/'CONTAGEM_FINAL.json',counts)
text=['[REAL — leitura documental e medição de fontes; OPEN — motivo exato de vários orçamentos]','',
'# Recibo h — heartbeat por módulo','',
'Foram lidas as 35 entregas A1 da retomada, as seis B1–B6 e os streams e snapshots inventariados em CORPUS_LIDO.json. As quatro entregas A1 da manhã estão identificadas separadamente. Não se atribui independência de autoria às revisões históricas.',
'',f'A contagem dos fontes é **{counts["explicit_general_caps"]}/44**, e não 34/44. O módulo aditivo novo não entra nesses 44. A origem da contagem 34 não foi estabelecida; o número do adendo não foi ajustado silenciosamente.',
'',f'Diagnósticos atribuíveis a {counts["observed_modules"]} módulos: {counts["general_timeout_modules"]} com orçamento geral esgotado e {counts["typeclass_timeout_modules"]} com orçamento de síntese esgotado; há sobreposição. São {counts["diagnostics"]} diagnósticos, não igual número de tentativas.',
'', 'Lean 4.31 declara padrão 200000 por comando e synthInstance.maxHeartbeats 20000 por problema de resolução de instâncias. As unidades representam milhares de pequenas alocações; não segundos. Os trechos e hashes estão em DEFAULTS_TOOLCHAIN.json.',
'', 'OBSERVADO designa mensagem real do elaborador. DECLARADO designa texto da entrega, sem transformá-lo em medição. INFERIDO designa apenas candidatos de custo presentes no fonte. Os limites finais não foram reduzidos, nem se mediu o mínimo necessário. Timeouts em versões com outros erros não isolam a causa do custo.',
'', '| Módulo | maxHeartbeats (linha:valor) | Diagnósticos geral / instâncias | Motivo observado ou lacuna |','|---|---|---:|---|']
for r in rows:
 cap=', '.join(f'L{c["line"]}:{c["value"]}'+(' local' if c['scope']=='local command' else '') for c in r['caps'] if c['kind']=='maxHeartbeats') or 'padrão; sem opção local'
 obs=', '.join(r['observed_mechanisms']) if r['observed_timeouts'] else ('Sem elevação a justificar' if not any(c['kind']=='maxHeartbeats' for c in r['caps']) else 'Escolha exata não documentada por diagnóstico localizado')
 text.append(f'| `{r["module"]}` | {cap} | {r["general_timeout_events"]} / {r["typeclass_timeout_events"]} | {obs} |')
for r in rows:
 text += ['',f'## {r["module"]}','',f'Fonte: [{Path(r["source"]["path"]).name}](<{r["source"]["path"]}>), SHA256 `{r["source"]["sha256"]}`.', '',r['interpretation']]
 for kind in ['maxHeartbeats','synthInstance.maxHeartbeats']:
  es=[e for e in r['observed_timeouts'] if e['kind']==kind]
  if es:
   e=es[0];sp=e['snapshot']
   text += ['',f'Exemplo {kind}: [stream L{e["line"]}](<{e["local_log"]}:{e["line"]}>), SHA256 `{e["log"]["sha256"]}`.', '', '```text',e['diagnostic'],'```']
   if sp:text += ['',f'Snapshot `{sp["path"]}`, SHA256 `{sp["sha256"]}`; coincide com o fonte final: {sp["matches_final"]}. Os demais exemplos e respectivas configurações estão no JSON.']
   else:text += ['', 'Snapshot do mesmo diretório ausente; não se presume que o fonte atual seja o fonte da falha.']
 if r['declared_budget_mentions']:
  text += ['','[DECLARADO — contexto da entrega; não é automaticamente motivo para a escolha numérica]']
  for q in r['declared_budget_mentions']:text+=['',f'[{Path(q["source"]).name}, L{q["line"]}](<{q["source"]}:{q["line"]}>)', '', '> '+q['text']]
 else:text+=['','[OPEN] Nenhuma justificativa explícita do número escolhida pelo autor foi localizada nas menções de orçamento dos fontes/entregas associados.']
 text+=['',r['inferred_reason']]
 for feat in r['source_features'][:3]:
  if r['caps']:
   hit=feat['examples'][0];text+=[f'- Ocorrência observada para a inferência ({feat["feature"]}), L{hit["line"]}: `{hit["text"].replace("`", "")}`.']
 text+=['',r['remaining']]
atomic(D/'RECIBO_H.md','\n'.join(text)+'\n')
print(counts)
