"""Render verified append-only memory plans after final receipts. Never apply."""
import argparse,datetime,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
W=HERE.parent
MARKER='IALD_KIMI_STACK_UPGRADE_20261021_OPERATIONAL'
TARGETS=(Path('C:/Users/rotol/.codex/AGENTS.md'),Path('C:/IALD/Central de Patentes/memory/TGL_INDICE_VIVO.md'),Path('C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory/MEMORY_2.md'))
def sha(raw):return hashlib.sha256(raw).hexdigest()
def require(ok,message):
 if not ok:raise ValueError(message)
def pin(path):
 raw=path.read_bytes();return dict(path=str(path),sha256=sha(raw),bytes=len(raw))
def load(path):return json.loads(path.read_bytes())
def new(path,raw):
 require(path.resolve().is_relative_to(HERE.resolve()),'Output outside memory stage')
 with path.open('xb') as stream:stream.write(raw)
 require(path.read_bytes()==raw,'Staging bytes mismatch')
def emit(path,value):new(path,(json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode())
def validate():
 required=[W/'deployment.json',W/'INSTALLED_VERIFICATION.json',W/'INSTALL_PLAN.json',W/'SCIENCE_BASELINE.json',W/'integration/RANK600_BENCHMARK_OPTIMIZED_R2.json']
 for path in required:require(path.is_file(),'WAITING_FINAL_RECEIPT: '+path.name)
 pins=[pin(path) for path in required];deployment,verification,plan,science,bench=[load(path) for path in required]
 require(str(deployment.get('status','')).upper() in ('PASS','INSTALLED','COMPLETED','DEPLOYED','PASS_INSTALLED','INSTALLED_VERIFIED'),'Deployment success schema not recognized; inspect receipt before changing validator')
 require(verification.get('status')=='PASS','Installed verification not PASS')
 require(verification.get('provider_calls')==0 and verification.get('jobs_created')==0 and verification.get('app_restart') is False,'Unexpected verification scope')
 require(len(science['files'])==5 and verification.get('science_files_unchanged')==5,'Expected five unchanged app-science files')
 for item in science['files']:require(sha(Path(item['path']).read_bytes())==item['current_sha256'],'App science pin changed')
 expected={str(Path(item['destination']).resolve()):item['sha256'] for item in plan['files']}
 observed={str(Path(item['path']).resolve()):item for item in verification['pins']}
 require(set(expected)==set(observed),'Installed pin coverage differs from deployment plan')
 for path,digest in expected.items():
  item=observed[path];require(item['expected']==item['actual']==digest,'Installed receipt pin mismatch')
  require(sha(Path(path).read_bytes())==digest,'Current installed bytes changed')
 cli=verification['fresh_process_cli_result']
 require(cli.get('ok') is True and cli.get('nodes'),'CLI verification missing')
 require(all(item['source']['status']=='VERIFIED_SHA256' for item in cli['nodes']),'CLI source not verified')
 require(cli['coverage']['catalog_nodes']==3,'Pilot catalog size changed; revise narrative')
 require(bench['candidates']==600 and bench['runs']==3 and bench['provider_calls']==0,'Benchmark scope changed')
 rankpath=next(path for path in expected if Path(path).name=='layered_retrieval.py')
 require(bench['module_sha256']==expected[rankpath],'Benchmark module differs from installed ranker')
 # Recheck receipt bytes after source verification to detect concurrent replacement.
 require(pins==[pin(path) for path in required],'Evidence changed during preparation')
 return pins,verification,bench,len(expected)
def render(pins,verification,bench,count):
 date=datetime.datetime.now(datetime.timezone.utc).date().isoformat()
 return ('\n\n## '+date+' — Integração operacional Kimi / recuperação científica local\n<!-- '+MARKER+' -->\n'
 '[REAL — engenharia local] Implantação de '+str(count)+' arquivos conferida pelos recibos deployment.json e INSTALLED_VERIFICATION.json e por SHA256 atual. Escopo CLI local do operador/fila: retrieve_knowledge ocorre antes de importar/instanciar Transport; teste em processo novo sem provedor, sem job e sem restart do app. Não comprova recarga de processos Python/MCP já residentes, app ou JEV live.\n'
 '[REAL — recuperação com escopo] CLI possui catálogo piloto explícito de 3 IDs científicos, não o corpus inteiro. nos_packet usa até 600 candidatos FTS da consulta existente, ranking de relevância e filtros/releitura científicos preexistentes. Blocos preparados entram inteiros; o prefixo de fonte legado de 2400 caracteres continua parcial e explicitado. Hash identifica bytes; seleção parcial não comprova ausência; estatutos e hipóteses permanecem.\n'
 '[REAL — orçamento e limites] API local usa orçamento JSON UTF8 conservador, reserva de 2048 bytes e recusa por overflow obrigatório. Obrigações/erratas/contradições preservadas por metadados e vínculos explícitos; não há garantia lexical de cobertura global. Recência/centralidade são desempates de recuperação, nunca prova de verdade. Nenhuma redução da memória fixa do app é inferida.\n'
 '[REAL — benchmark offline] 600 candidatos sintéticos, 3 execuções CPU; mediana de relógio '+format(bench['median_wall_seconds'],'.6f')+' s, mediana CPU '+format(bench['median_cpu_seconds'],'.6f')+' s. Medição exclui busca no banco e leitura de fontes; não mede qualidade, latência de provedor ou ganho em produção. Cache de pontuação é por chamada, sem alterar o índice FTS.\n'
 '[REAL — preservação] Cinco arquivos científicos/configurações do app da SCIENCE_BASELINE.json permaneceram iguais por hash. Nenhum original científico, kernel, selo, gate ou binário do app foi alterado por esta entrega operacional. Voz experimental não ativada; não anunciar execução live de JEV ou nova ciência.\n'
 '[EVIDÊNCIAS] '+ '; '.join(item['path']+' SHA256 '+item['sha256'] for item in pins)+'. Referência própria: '+str(W/'SESSION_REFERENCE.json')+'.\n<!-- END_'+MARKER+' -->\n').encode('utf8')
def prepare(outname):
 pins,verification,bench,count=validate() # No final text/plan before validation.
 out=(HERE/outname).resolve();require(out.parent==HERE and not out.exists(),'Fresh direct child output required')
 surfaces=load(HERE/'SURFACES.json')['surfaces'];require([Path(s['path']).resolve() for s in surfaces]==[p.resolve() for p in TARGETS],'Exactly three authorized surfaces required')
 chunk=render(pins,verification,bench,count);items=[]
 for target in TARGETS:
  before=target.read_bytes();require(MARKER.encode() not in before,'Marker already present; reconcile instead of duplicate append')
  items.append(dict(path=str(target),before_sha256=sha(before),before_bytes=len(before),after_sha256=sha(before+chunk),after_bytes=len(before+chunk),backup='Raw bytes in SAME target folder, unique timestamp, verified before temp+atomic replacement; retain backup',operation='APPEND_ONLY_NOT_APPLIED'))
 out.mkdir();new(out/'APPEND.txt',chunk)
 emit(out/'PLAN.json',dict(status='PREPARED_VERIFIED_NOT_APPLIED',marker=MARKER,surfaces=items,append=pin(out/'APPEND.txt'),evidence=pins,helper=pin(HERE/'atomic_append.py'),guard='Parent coordination/review and fresh preflight; revalidate ALL evidence and target CAS pins. No new human approval inferred. Per-file atomic, not multi-file transaction.',excluded=['Atlas','Nós','app binaries','scientific originals'],memory_applied=False))
 return pin(out/'PLAN.json')
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--out',default='FINAL_R1');args=parser.parse_args()
 try:print(json.dumps(prepare(args.out),ensure_ascii=False))
 except (OSError,ValueError,KeyError,TypeError) as error:
  print(json.dumps(dict(status='REFUSED_NOT_APPLIED',error=str(error)),ensure_ascii=False));raise SystemExit(2)
