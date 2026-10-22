from support import *
import re
K=ROOT/'kernel'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def pin(p):p=Path(p);return dict(path=str(p),sha256=digest(p),bytes=p.stat().st_size)
bp=read(ROOT/'BUILD_ATUAL.json');ap=read(ROOT/'AXIOMAS_ATUAL.json');cp=read(ROOT/'CONTROLES_ORPHANS_ATUAL.json');gp=read(ROOT/'binary/AXIOMAS_ATUAL.json')
assert all(x['ok'] for x in [bp,ap,cp,gp])
build=read(bp['report']);ax=read(ap['report']);controls=read(cp['report']);fc=[];graph=read(ROOT/'GRAFO_REBUILD.json');pres=read(ROOT/'PRESERVACAO_FONTES.json');assert pres['all_unchanged']
for r in build['runs']:
 p=K/Path(*r['module'].split('.')).with_suffix('.lean');assert digest(p)==r['source_sha256']
 for a in r['artifacts']:assert digest(Path(a['path']))==a['sha256']
stdout=Path(ax['run']['stdout']).read_text(encoding='utf-8')
for name in ['antiunitaryConjugate_add','antiunitaryConjugate_smul']:
 assert 'SUPPLIER TGLV350.Regular.'+name+' = TGLExt.V350LocalBasePolarCommutation' in stdout
 occurrences=[]
 for p in (K/'TGLExt').glob('*.lean'):
  if re.search(r'^theorem '+name+r'\b',p.read_text(encoding='utf-8-sig'),re.M):occurrences.append(str(p))
 assert occurrences==[str(K/'TGLExt/V350LocalBasePolarCommutation.lean')]
counts=read(ROOT/'heartbeat/CONTAGEM_FINAL.json');rows=read(ROOT/'heartbeat/POR_MODULO_INTERPRETADO.json')
capped_without_timeout=[r['module'] for r in rows if any(c['kind']=='maxHeartbeats' for c in r['caps']) and not r['observed_timeouts']]
records={
'b':dict(status='PAGO',qualification='No snapshot lido; proposta autoral',result='H_sector_nonexchange setorial e H_singlefluid_continuity no fluido único; nenhum H_nx restante nos fontes Lean finais do snapshot; fecho reverso recompilado.',modules=graph['closures']['b']),
'c':dict(status='PAGO',qualification='Sete recusas semânticas de aplicação',result='Sete pares: positivos rc0; negativos rc1 por Type mismatch. Duas sondas históricas preservadas por bytes e reexecutadas; cinco acrescentadas.',controls=controls,limit='Não prova falsidade universal de cada variante em todo caso degenerado.'),
'd':dict(status='PAGO',qualification='Deduplicação por importação; grafo acíclico',result='As duas declarações existem somente em V350LocalBasePolarCommutation. V351AntiunitaryResolventPhase importa esse fornecedor e não repete as provas. Lean identificou o fornecedor pelo ambiente.',modules=graph['closures']['d'],supplier_lines=[l for l in stdout.splitlines() if l.startswith('SUPPLIER ')]),
'f':dict(status='PAGO',qualification='Somente o corolário geral compilado; sem hr/he',result='H² = (8*pi*G/3)*sum rho_i^TGL - Lambda/3, tanto sob equação métrica explícita quanto com Lambda existencial único no domínio preconexo.',proposed_flag='ext_pb_tgl_friedmann_sector_additive_kernel_proved',consumer='ChatgptAudit.FLRW.tgl_friedmann_from_sector_closure_additive',controls=fc,limit='Não se prova unicidade de Lambda por existência apenas: "único no domínio" significa uma mesma constante escolhida para todo U. Sem hipótese de unicidade numérica adicional. SectorFluid.rho_nonneg, H_sector_nonexchange, H_null, suavidade, a>0 e G>0 continuam no contrato.'),
'g':dict(status='PAGO',qualification='Investigação e medição entregues; causalidade histórica completa limitada',result='Três recompilações rc0, 25 declarações no trio, localização das janelas de caminhos e ensaio ABA de AreaScale. Causa de cada byte histórico de AreaScale permanece OPEN.',report=pin(ROOT/'binary/RECIBO_G.md'),axioms=gp),
'h':dict(status='PAGO',qualification='Declaração por módulo; decisão atual separada da história NÃO RECUPERADA',result='44 módulos documentados; 39 com maxHeartbeats explícito, contra 34 no adendo. 35 entregas A1, seis B e 1566 arquivos de tentativas consultados; 16 módulos com timeout observado (14 geral; seis síntese, com sobreposição).',unresolved_capped_modules_without_localized_timeout=capped_without_timeout,impediment='Não se recuperou a motivação histórica exata de todos os valores. A cláusula documental está atendida pela declaração ATUAL por módulo, sem fazer passar essa decisão por história medida; não se pede mínimo empírico.',report=pin(ROOT/'heartbeat/RECIBO_H.md'))}
records['f']['historical_control_scope']=pin(ROOT/'ALCANCE_CONTROLE_F_HISTORICO.json')
records['f']['active_controls']=False
records['h']['current_policy_report']=pin(ROOT/'heartbeat/POLITICA_ATUAL_POR_MODULO.json')
# Avoid a numerical-uniqueness claim not present in the theorem.
records['f']['result']='Somente tgl_friedmann_from_sector_closure_additive: H² = (8*pi*G/3)*sum rho_i^TGL - Lambda/3, com uma mesma constante Lambda existencial em todo o domínio preconexo. O corolário pontual sem consumidor funcional foi podado após leitura do principal.'
records['f']['limit']='A existência de uma constante comum não é teorema de unicidade numérica. SectorFluid.rho_nonneg, H_sector_nonexchange, H_null, suavidade, a>0 e G>0 continuam no contrato.'
for label in ['b','d']:
 selected=[r for r in build['runs'] if r['module'] in records[label]['modules']]
 records[label]['commands']=[r['command'] for r in selected]
 records[label]['all_compiled']=len(selected)==len(records[label]['modules']) and all(r['returncode']==0 for r in selected)
 assert records[label]['all_compiled']
record(ROOT/'RECIBOS.json',dict(author_only=True,operator_acceptance=False,root=str(ROOT),timestamp_utc=stamp(),items=records,build=pin(bp['report']),audit=pin(ap['report']),audited_declarations=len(ax['expected']),axiom_union=ax['union'],axioms_missing=ax['missing'],axioms_outside=ax['outside_trio'],originals_preservation=pin(ROOT/'PRESERVACAO_FONTES.json')))
for label in ['b','c','d','f']:
 r=records[label];lines=[f'[REAL — {r["status"]} no escopo autoral; exame do operador pendente]','',f'# Recibo {label}','',r['result'],'',r['qualification']+'.']
 if label in ['b','d']:
  lines+=['',f'Fecho reverso: {len(r["modules"])} módulos; todos rc0. O grafo antes/depois foi verificado acíclico.']
  for run in build['runs']:
   if run['module'] in r['modules']:lines+=['',f'- `{run["module"]}` — fonte SHA256 `{run["source_sha256"]}`, rc{run["returncode"]}; [stdout](<{run["stdout"]}>).']
 if label in ['c','f']:
  for pair in r['controls']:lines+=['',f'- `{pair["module"]}`: [positivo](<{pair["positive"]["stdout"]}>), rc{pair["positive"]["returncode"]}; [negativo](<{pair["negative"]["stdout"]}>), rc{pair["negative"]["returncode"]}; {pair["mutation"]}']
 if label=='d':lines+=['','```text',*r['supplier_lines'],'```','', 'Não foram criadas provas substitutas ou aliases de prova. O fornecedor V350 conservou seus bytes originais. A importação adicional conserva os nomes e tipos públicos.']
 if label=='b':lines+=['','O campo setorial e a hipótese do fluido único continuam objetos distintos. Foram atualizados os dois usos F.H_nx e os comentários correspondentes, além do binder de B4. O fecho presente compila; consumidores externos não lidos que usem o nome antigo precisam migrar.']
 if label=='f':lines+=['','Fonte: [SectorFriedmannAdditive.lean](<'+str(K/'TGLExt/SectorFriedmannAdditive.lean')+'>).','', 'Consumidor proposto, não instalado: `'+r['proposed_flag']+'` → `'+r['consumer']+'`.', '',r['limit']]
 if label=='f':lines+=['', (ROOT/'ALCANCE_CONTROLE_F_HISTORICO.md').read_text(encoding='utf-8')]
 if label=='c':lines+=['',r['limit']]
 lines+=['',f'Auditoria comum: {len(ax["expected"])} declarações, zero faltantes, zero axiomas fora do trio. A união efetivamente impressa é `'+', '.join(ax['union'])+'`.', '', f'[Axiomas e comandos completos](<{ap["report"]}>) — SHA256 `{digest(Path(ap["report"]))}`.', '',f'[Build por módulo](<{bp["report"]}>) — SHA256 `{digest(Path(bp["report"]))}`.', '',f'[Recibos estruturados com comandos de cada item](<{ROOT/"RECIBOS.json"}>).']
 atomic(ROOT/f'RECIBO_{label.upper()}.md','\n'.join(lines)+'\n')
entry=['[REAL — entrega autoral para exame; sem incorporação e sem aceite final]','','# Saneamento do adendo 001 da Ordem 012','',
'Raiz exclusiva: `'+str(ROOT)+'`. B1′ e A2 permaneceram fora deste trabalho. Nenhum monólito, D1, gate, Atlas, memória ou túnel foi editado.',
'', '| Item | Estatuto | Recibo |','|---|---|---|']
for label in records:
 p=(ROOT/f'RECIBO_{label.upper()}.md') if label in ['b','c','d','f'] else Path(records[label]['report']['path'])
 entry.append(f'| {label} | **{records[label]["status"]}** — {records[label]["qualification"]} | [ler](<{p}>) |')
entry += ['','O build aceito tem **28/28 rc0**: os 27 módulos do fecho b/d/f e um fornecedor sem objeto, ModularFlowAlgebra. A tentativa Lake ampla interrompida não conta como aprovação. A auditoria comum verificou **108 declarações**; a dos três objetos B6, **25**. Todos os conjuntos de axiomas impressos ficaram no trio; nenhuma declaração esperada faltou.',
'', 'As sete sondas dos órfãos têm positivos rc0 e negativos rc1 por Type mismatch. O corolário pontual e seu controle autoral foram retirados da superfície final após leitura semântica do principal, por ausência de consumidor funcional. O histórico permanece; somente o alvo aditivo geral e a auditoria afetada foram reexecutados após a poda.',
'', 'Em h, cada módulo recebeu a decisão ATUAL de manter sua configuração para preservar o escopo desta rodada, sem otimização empírica. A motivação histórica não localizada permanece NÃO RECUPERADA; a política atual não a converte em medição. O item fica PAGO no alcance literal documental, sem novos builds.',
'', 'Em g, as diferenças de MixedLadder/SecondCone ficam integralmente na janela do caminho do fonte e dos 24 bytes anteriores. O ensaio ABA demonstrou o efeito da grafia do caminho em AreaScale. A causa de cada alteração do par histórico AreaScale não foi estabelecida. Não se acrescenta hipótese de cache à evidência.',
'', f'A preservação final releu **{pres["files"]}** entradas de fontes, ordens, entregas e artefatos B6: todas conservaram o hash medido inicialmente. O escopo desse cotejo está no relatório; não se afirma rehash final de todo o cache.',
'', 'Artefatos para exame:']
for label,p in [('Ficha anterior ao código',ROOT/'FICHA_SANEAMENTO.md'),('Ficha estruturada',ROOT/'FICHA_SANEAMENTO.json'),('Proposta em patch',ROOT/'PROPOSTA.patch'),('Fontes e hashes do delta',ROOT/'DELTA_FONTES.json'),('Comandos e recibos por item',ROOT/'RECIBOS.json'),('Auditoria Lean',K/'TGLExt/AuditSanitation.lean'),('Axiomas efetivamente lidos',Path(ap['report'])),('Preservação por bytes',ROOT/'PRESERVACAO_FONTES.json'),('Falhas e limites',ROOT/'FALHAS_E_LIMITES.md'),('Manifesto',ROOT/'MANIFESTO.json')]:entry+=['',f'- [{label}](<{p}>)'+(f' — SHA256 `{digest(p)}`.' if p.exists() and p.name!='MANIFESTO.json' else '.')]
entry+=['','PAGO qualifica o trabalho autoral delimitado neste recibo. A confirmação da incorporação e o aceite continuam sendo atos do operador/revisor. Nenhum estado canônico foi atualizado.']
atomic(ROOT/'ENTREGA.md','\n'.join(entry)+'\n')
# Hash all authored/evidence artifacts outside the copied project/cache, plus project sources and live rebuilt outputs.
files=[]
for base,dirs,names in os.walk(ROOT):
 dirs[:]=[d for d in dirs if d not in ['kernel','kernel.copying','__pycache__','tmp']]
 for name in names:
  p=Path(base)/name
  if name in ['MANIFESTO.json','SELOS.json'] or name.startswith(('MANIFESTO.json.bak_','SELOS.json.bak_')):continue
  files.append(p)
files+=list((K/'TGL').rglob('*.lean'))+list((K/'TGLExt').rglob('*.lean'))+list(K.glob('*.lean'))
for name in ['lakefile.toml','lake-manifest.json','lean-toolchain']:
 if (K/name).exists():files.append(K/name)
for r in build['runs']:files += [Path(a['path']) for a in r['artifacts']]
files=sorted(set(files),key=str)
manifest=dict(status='AUTHOR_WORK_FOR_OPERATOR_EXAM',created_utc=stamp(),root=str(ROOT),item_status={k:v['status'] for k,v in records.items()},artifacts=[pin(p) for p in files],compiler=[pin(BIN/'lean.exe'),pin(BIN/'lake.exe')],exclusions=['Cache integral .lake e intermediarios Python/tmp; proveniencia e hashes iniciais completos em PROVENIENCIA_COPIA.json.', 'O proprio MANIFESTO e SELOS nao se auto-hasheiam.'],original_inputs_provenance=pin(ROOT/'PROVENIENCIA_COPIA.json'))
record(ROOT/'MANIFESTO.json',manifest)
seal={label:pin(p) for label,p in [('manifest',ROOT/'MANIFESTO.json'),('receipt',ROOT/'ENTREGA.md'),('fiche',ROOT/'FICHA_SANEAMENTO.md'),('patch',ROOT/'PROPOSTA.patch'),('limits',ROOT/'FALHAS_E_LIMITES.md')]}
record(ROOT/'SELOS.json',seal)
print('ITEMS',manifest['item_status']);print('ARTIFACTS',len(files));print(json.dumps(seal,ensure_ascii=False,indent=2))
