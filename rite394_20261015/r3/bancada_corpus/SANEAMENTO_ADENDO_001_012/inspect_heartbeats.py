from support import *
import re,collections
A=ROOT.parent/'TETELESTAI_V351_FECHO_MATEMATICO'/'RETOMADA_A1B_012'
B=ROOT.parent/'TETELESTAI_V353_A_PASSAGEM_DA_ACAO_A_METRICA'
T=ROOT.parent/'TUNEL'
f=json.loads((ROOT/'FICHA_SANEAMENTO.json').read_text(encoding='utf-8'))
mods={Path(r['path']).stem:r for r in f['modules44']}
D=ROOT/'heartbeat';D.mkdir(exist_ok=True)
def pin(p):return dict(path=str(p),sha256=digest(p),bytes=p.stat().st_size)
def caps(s):
 return [dict(line=n,text=l,kind=k,value=int(v)) for n,l in enumerate(s.splitlines(),1) for k,v in re.findall(r'set_option\s+(maxHeartbeats|synthInstance.maxHeartbeats)\s+(\d+)',l)]
exclude={'ENTREGA_011_A1_avaliacao_funcional_leis_normalidade.md','ENTREGA_011_A1_contrato_forte_e_peso_dual.md','ENTREGA_011_A1_forma_base_semifinitude_aproximantes.md','ENTREGA_011_A1_potencias_imaginarias_mesmo_tomita.md'}
deliveries=[]
for p in sorted(T.rglob('ENTREGA_*.md')):
 isa1=p.name.startswith('ENTREGA_011_A1')
 isb=bool(re.match(r'ENTREGA_012_B[1-6]_',p.name))
 if not(isa1 or isb):continue
 s=p.read_text(encoding='utf-8-sig'); obj=pin(p);obj['excluded_morning']=p.name in exclude
 obj['modules_in_body']=[m for m in mods if m in s]
 obj['primary_modules']=[m for m in mods if re.search(r'\|\s*`'+re.escape(m)+r'`\s*\|',s)]
 obj['budget_mentions']=[dict(line=n,text=l) for n,l in enumerate(s.splitlines(),1) if re.search(r'heartbeat|or[cç]amento|elabora[cç][aã]o|custo computacional',l,re.I)]
 obj['a1']=isa1;obj['copy']=str(D/'deliveries'/p.name)
 atomic(Path(obj['copy']),p.read_bytes());deliveries.append(obj)
assert sum(x['a1'] and not x['excluded_morning'] for x in deliveries)==35
record(D/'ENTREGAS_LIDAS.json',deliveries)
# Read actual attempt streams, not reported verdict strings.
corpus=[];events=[];runs=[]
for base in [A,B]:
 for top in sorted(base.iterdir()):
  if not top.is_dir() or not (top.name.startswith(('dev_','replay_','audit_')) or top.name.endswith(('_attempts','_validation')) or top.name in ['attempts','sequential_validation']):continue
  for p in sorted(top.rglob('*')):
   if not p.is_file() or p.suffix.lower() not in ['.txt','.log','.json','.lean']:continue
   if any(x=='.lake' for x in p.relative_to(top).parts):continue
   try:s=p.read_text(encoding='utf-8-sig')
   except UnicodeError:continue
   item=pin(p);corpus.append(item)
   if p.name=='run.json':
    try:
     o=json.loads(s);ms=[m for m in mods if m in s];rc=o.get('returncode',o.get('exit_code'))
     runs.append(dict(**item,modules=ms,returncode=rc,kind=top.name))
    except json.JSONDecodeError:pass
   if p.suffix.lower() not in ['.txt','.log']:continue
   lines=s.splitlines()
   for n,l in enumerate(lines):
    if not re.search(r'(deterministic.*timeout|maximum number of heartbeats|heartbeats.*exceeded|exceeded.*heartbeats)',l,re.I):continue
    context='\n'.join(lines[max(0,n-3):min(len(lines),n+5)])
    ms=[m for m in mods if re.search(re.escape(m)+r'\.lean',context)]
    # A short diagnostic continuation may need its nearest preceding location.
    if not ms:
     for prev in reversed(lines[max(0,n-30):n+1]):
      found=[m for m in mods if re.search(re.escape(m)+r'\.lean:\d+',prev)]
      if found:ms=found;break
    for m in ms:
     snap=p.parent/(m+'.lean');so=None
     if snap.exists():
      ss=snap.read_text(encoding='utf-8-sig');so=dict(**pin(snap),caps=caps(ss),matches_final=digest(snap)==digest(Path(mods[m]['path'])))
      atomic(D/'snapshots'/base.name/top.name/p.parent.name/snap.name,snap.read_bytes())
     dest=D/'logs'/base.name/p.relative_to(base);atomic(dest,p.read_bytes()) if not dest.exists() else None
     events.append(dict(module=m,log=item,local_log=str(dest),line=n+1,context=context,snapshot=so,association='module filename at diagnostic or nearest preceding location; no inference from directory nickname'))
record(D/'CORPUS_LIDO.json',corpus);record(D/'TIMEOUTS_OBSERVADOS.json',events);record(D/'RUNS_LIDOS.json',runs)
features=[(r'\bcfc\w*','cálculo funcional contínuo'),(r'\blintegral\w*|∫⁻','integrais de Lebesgue no cone estendido'),(r'\btendsto\w*|Tendsto','passagem a limites'),(r'\bsum\w*|∑|Finset\.sum','somas finitas'),(r'\bfun_prop\b','busca de propriedades funcionais'),(r'\b(?:simp|simp_all|simpa)\b','simplificação de expressões'),(r'\b(?:ring|ring_nf|field_simp|linarith|nlinarith)\b','normalização algébrica'),(r'ContDiff|HasDerivAt|\bfderiv\b|\bderiv\b','derivadas e regularidade')]
rows=[]
for m,base in sorted(mods.items()):
 p=Path(base['path']);s=p.read_text(encoding='utf-8-sig');cs=caps(s);ev=[x for x in events if x['module']==m]
 ds=[x for x in deliveries if m in x['primary_modules'] and not x['excluded_morning']]
 # If no table exists, keep explicit all-body references without promoting them to primary.
 if not ds:ds=[x for x in deliveries if m in x['modules_in_body'] and not x['excluded_morning']]
 declared=[]
 for n,l in enumerate(s.splitlines(),1):
  if re.search(r'heartbeat|budget|expensive|elaboration|elaborat|custo|or[cç]amento',l,re.I) and 'set_option' not in l:
   declared.append(dict(source=str(p),line=n,text=l))
 for d in ds:
  declared.extend(dict(source=d['path'],**v) for v in d['budget_mentions'])
 feats=[]
 for pat,title in features:
  hits=[dict(line=n,text=l[:240]) for n,l in enumerate(s.splitlines(),1) if re.search(pat,l)]
  if hits:feats.append(dict(feature=title,occurrences=len(hits),examples=hits[:3]))
 row=dict(module=m,source=pin(p),caps=cs,delivery_sources=[d['path'] for d in ds],observed_timeouts=ev,declared_budget_mentions=declared,source_features=feats,
  interpretation=('OBSERVADO: houve esgotamento em snapshot(s) histórico(s); isso não prova o orçamento mínimo nem a necessidade exata do limite final.' if ev else 'ABERTO: não localizado esgotamento atribuível a este módulo no corpus lido; não se afirma que ele nunca ocorreu.'),
  inferred_reason=('INFERIDO, não história autoral: '+', '.join(x['feature'] for x in feats)+', presentes nas linhas pinadas, são candidatos a custo de elaboração. Não isolamos qual consumiu o orçamento.' if cs else 'Sem elevação maxHeartbeats neste fonte; não há motivo de elevação a justificar.'),
  remaining='Não determinado o orçamento mínimo do fonte final nem, salvo declaração explícita citada, por que foi escolhido esse número exato. Nenhum limite alterado neste saneamento.')
 rows.append(row)
record(D/'POR_MODULO.json',rows)
summary=dict(modules=len(rows),with_explicit_maxHeartbeats=sum(any(c['kind']=='maxHeartbeats' for c in r['caps']) for r in rows),adendo_count=34,deliveries_a1=35,deliveries_b=sum(not d['a1'] for d in deliveries),corpus_files=len(corpus),observed_timeout_events=len(events),modules_with_observed_timeout=sum(bool(r['observed_timeouts']) for r in rows),method='Ler bytes UTF-8; diagnóstico em stdout/stderr/log; associar módulo por localização explícita; comparar snapshot quando presente. Zero inferência de causa a partir de rc1 isolado.')
record(D/'RESUMO.json',summary)
print(json.dumps(summary,ensure_ascii=False))
for r in rows:print(r['module'], 'caps='+str([c['value'] for c in r['caps'] if c['kind']=='maxHeartbeats']), 'timeouts='+str(len(r['observed_timeouts'])), 'mentions='+str(len(r['declared_budget_mentions'])))
