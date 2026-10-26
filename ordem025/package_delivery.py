"""Create a new immutable ORDEM025 delivery after the local build and review."""
from pathlib import Path
import json,hashlib,re,datetime
from task import W,pin,new,check
from analysis_payload import ANALYSIS

OUT=Path('C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_025')
S=W/'sandbox'
K=Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel')
def write(rel,data):
    p=OUT/rel
    p.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(data,(dict,list)): data=json.dumps(data,ensure_ascii=False,indent=2).encode('utf-8')
    if isinstance(data,str): data=data.encode('utf-8')
    with p.open('xb') as f:f.write(data)
    assert p.read_bytes()==data
    return pin(p)
def copy(p,rel):return write(rel,p.read_bytes())

assert not list(OUT.iterdir()),'Delivery exists; never overwrite registered evidence.'
preflight=check()
assert preflight.get('ready') is True,preflight
build=json.loads((W/'BUILD_VERIFIED.json').read_text())
ax=json.loads((W/'AXIOMAS_VERIFIED.json').read_text())
review=json.loads((W/'REVIEW_SEMANTIC.json').read_text())
assert build['status']==ax['status']=='PASS'
src=S/'TGLExt/PonteDaEscalaDual.lean'
assert pin(src)['sha256']==build['source']['sha256']
# The reviewer is a distinct actual subagent; retain its exact receipt and scope.
assert build['source']['sha256'] in json.dumps(review)
assert build['stdout']['sha256'] in json.dumps(review)
new('DELIVERY_PREFLIGHT.json',preflight)
copy(src,'PonteDaEscalaDual.lean')
copy(src.with_suffix('.olean'),'PonteDaEscalaDual.olean')
copy(S/'TGLExt/FalsidadeDaInercia.lean','dependencias/FalsidadeDaInercia.lean')
copy(W/'AXIOMAS_VERIFIED.json','AXIOMAS.json')
copy(W/'BUILD_VERIFIED.json','BUILD_RECEIPT.json')
copy(W/'REVIEW_SEMANTIC.json','REVISAO_SEMANTICA.json')
copy(S/'DEPENDENCY_COPIES.json','DEPENDENCIAS_CACHE.json')
copy(W/'SOURCES_INITIAL.json','FONTES_INICIAIS.json')
copy(W/'RESTART_RECOVERY.json','RETOMADA_APOS_DESLIGAMENTO.json')
copy(W/'verify_build.py','scripts/verify_build.py')
copy(S/'build.py','scripts/build_usado.py')
copy(S/'copy_deps.py','scripts/copy_deps_usado.py')
copy(K/'lake-manifest.json','pins/lake-manifest.json')
copy(K/'lean-toolchain','pins/lean-toolchain')
for p in sorted((S/'logs').iterdir()):
    if p.is_file():copy(p,'tentativas/'+p.name)
for n in ['MAP_inercia.json','MAP_escala_dual.json','MAP_Bisognano.json','NOS_QUERY.txt']:
    copy(W/n,'consultas/'+n)
b=build['build']
log=Path(build['stdout']['path']).read_text(encoding='utf-8')
write('BUILD.log',json.dumps(b,ensure_ascii=False,indent=2)+'\n\n--- SAIDA INTEGRAL DO LEAN ---\n'+log)
sources={
 'GlobalLiftLadder.lean':['structure DualScalingData','fixed_tau_zero'],
 'BisognanoWichmann.lean':['def boost','boost_zero','boost_add'],
 'Solder4D.lean':['def eta4','solder4_lorentzian'],
 'PoincareGroup.lean':['def boostMat'],
 'O16/BoostRepresentationBridges.lean':['boost_is_first_block'],
 'O16/OrbitalBoostCovariance_v2.lean':['shellMomentum_chart_shift'],
 'V351DualScalingBridge.lean':['regularCoreDualScalingData'],
 'AgapeNonVacuity.lean':['finiteTracePositive_has_positive'],
 'ConstructedHeatPrimitive.lean':['screenHeatFlux','constructedHeat'],
 'GeneralMetricClausius.lean':['metric_einstein_from_screen_clausius','hclausius']}
refs=[]
for rel,terms in sources.items():
    p=K/'TGLExt'/rel
    lines=p.read_text(encoding='utf-8').splitlines()
    anchors={term:[{'line':i+1,'text':line} for i,line in enumerate(lines) if term in line] for term in terms}
    assert all(anchors.values()),(rel,anchors)
    refs.append({**pin(p),'anchors':anchors})
write('REFERENCIAS.json',refs)
fresh=[]
for old in json.loads((W/'SOURCES_INITIAL.json').read_text()):
    current=pin(Path(old['path']))
    fresh.append({'path':old['path'],'initial_sha256':old['sha256'],'current_sha256':current['sha256'],
                  'unchanged':old['sha256']==current['sha256']})
write('CONFERENCIA_FONTES.json',{'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'scope':'Compara as fontes pinadas, não todo o computador. Fontes concorrentes não são alteradas por esta tarefa.',
    'sources':fresh})
write('ANALISE_TECNICA.json',ANALYSIS)
write('ESCOPO_PT.json',{
 'A':'[REAL — sandbox] Instância DualScalingData com tau=pPlus, theta(s)=boost(-s); leis de grupo verificadas.',
 'B':'[REAL — sandbox] Composição com FalsidadeDaInercia, m²=pPlus*pMinus invariante, E variável, inclusão equivarante na eta4 existente; E=mc² sob shell/repouso/sinais explícitos.',
 'ponte_ao_core':'[REAL — sandbox] coreLift compõe a escala dual regular existente com o boost. Há A com tau>0, energia>0 e massa²=mu2 para cada mu2>=0 escolhido.',
 'nao_unicidade':'[REAL — sandbox] lift_mass_not_selected: mu2 diferentes dão realizações diferentes. A lei de escala não seleciona a massa.',
 'obstrucao':'[REAL — sandbox] Um peso positivo que escala por exp(-s) não é invariante; não pode simultaneamente ser a massa de repouso positiva invariante na mesma órbita.',
 'C_assinatura':'[OPEN — inalterado] eta4 já foi escolhida no import; preservar a forma não a deriva da positividade completa.',
 'C_quatro':'[OPEN — inalterado] Fin 4 é escolhido e os dois momentos transversais são zero; não se prova rank(c)=4 nem se paga H2.',
 'clausius':'[OPEN] Falta realização de T simétrico e conservado, fluxo nulo correspondente e equilíbrio local em todas as telas/direções exigidas por hclausius. Os contratos existentes foram localizados, não reconstruídos.',
 'BW':'[OPEN nesta ponte] O parâmetro s é rapidez; o tempo modular envolve convenção e 2π. Ação dual de Takesaki e fluxo modular não são identificados por igualdade de expoentes.',
 'normalizacao':'p±=E±p, E=(p++p-)/2 e c=1. Se p±=(E±p)/sqrt(2), m²=2p+p-. Em 4D geral subtrai-se o momento transversal ao quadrado.',
 'inercia':'Inertial significa fixo por todos os boosts, conforme a definição importada; não significa movimento livre de forças.',
 'fronteira_fisica':'Identificar esta realização com o corpo observado requer calibração de energia, massa/distribuição e fonte física. Não é a mesma coisa que construir a instância matemática.',
 'proveniencia':'attempt005 interrompida sem exit conhecido; attempt006 concluída. A colisão antiga da numeração002 está explicada em tentativas/PROVENANCE_ERRATA.json.',
 'validacao':'Build local do alvo e Falsidade; dependências por caches pinados. Revisão semântica distinta, sem recompilação independente.',
 'scripts':'Scripts usados preservados como evidência; seus caminhos são os do sandbox original. Para nova compilação, criar outro sandbox e novos nomes de evidência; nunca sobrescrever o .olean entregue.',
 'beta':'Não usada nesta construção; nenhum literal beta introduzido.',
 'integracao':'Candidato apenas. Exame/integração pelo gestor; registro de mapa preparado, não aplicado aqui.'})
hash16=build['source']['sha256'][:16]
result=f'''PONTE PARCIAL — a realização da escala dual no momento nulo é termo; a massa/corpo físico e o Clausius completo não são selecionados por ela.
[REAL — sandbox] `PonteDaEscalaDual.lean` sha16 `{hash16}`; Lean 4.31.0; EXIT 0 em {b['duration_seconds']:.3f} s; zero sorry; 40 declarações explícitas (29 teoremas), 65 entradas auditadas incluindo geradas, somente o trio.
[REAL] A: tau=pPlus e theta(s)=boost(-s), com scaling provado e testemunha positiva do núcleo regular já construído.
[REAL] B: inercial (fixo por todo boost) implica pPlus=0; m²=pPlus·pMinus é invariante, E muda e a inclusão em eta4 é equivarante.
[REAL] `coreLift` liga o núcleo regular ao boost para cada massa² escolhida; `lift_rest_energy` compõe o repouso e `rest_energy_eq_mc2` explicita c e as hipóteses físicas.
[REAL] A massa não é selecionada: mu2 distintos produzem realizações distintas; um peso positivo escalante não pode ser a massa de repouso invariante.
[DERIVED — correção] Usamos p±=E±p e c=1; com p±=(E±p)/√2 seria m²=2p+p-, não p+p-. Rapidez não é automaticamente tempo modular BW.
[OPEN] Clausius: fonte T simétrica/conservada, fluxo correspondente e hclausius em toda direção nula permanecem nomeados; não há identificação física/algebraica plena entre os fluxos.
[OPEN] C: assinatura derivada de CP e rank(c)=4 ficam como estavam; eta4 e Fin 4 são dados importados.
[DERIVED] D: classificação ordenada em ANALISE_TECNICA.json, âncoras/hash em REFERENCIAS.json; ausência é restrita ao recorte consultado.
[REAL] Revisão independente semântica no recibo REVISAO_SEMANTICA.json; caches importados não foram integralmente recompilados.
[REAL] Tentativas falhas/interrompida e errata da numeração002 preservadas; BUILD.log contém comando, toolchain, LEAN_PATH, início/fim, duração, exit e stdout.
[INPUT] Mapa preparado para a gerência; candidato não instalado. Nenhuma escrita no Nós, um.py, git, site ou gate por esta entrega.
'''
assert len(result.splitlines())<=15
write('RESULTADO.md',result)
mapentry={'tipo':'ROTA','rota_id':'kernel.ordem025.ponte_escala_dual','dominio':'KERNEL_FORMAL',
 'titulo':'ORDEM025 — realização da escala dual no momento nulo e resíduo físico',
 'pergunta':'Quanto da identificação tau/pPlus e da composição massa/energia já vira termo?',
 'dados':['DualScalingData','boost/eta4 existentes','regularCoreDualScalingData','AgapeNonVacuity','FalsidadeDaInercia'],
 'metodo':'Consulta de fontes e grafo; construção Lean no sandbox próprio; auditoria exaustiva de axiomas e revisão semântica distinta.',
 'resultado':f'EXIT0; 40 declarações explícitas/29 teoremas; trio; {b["duration_seconds"]:.3f}s. Lift equivarante, positivo e não canônico, massa livre; obstrução à identificação peso positivo=massa invariante.',
 'veredito':'PONTE_PARCIAL','estatuto':'DERIVED','status':'EXAMINADA','olhou_dados':False,
 'defeito':'Massa/calibração/corpo e fonte T-H3 não selecionados; CP→assinatura e rank4 não pagos.',
 'nao_refazer':'Não reconstruir escala regular, não confundir ação dual e modular, não identificar pPlus escalante com massa invariante.',
 'proximo_passo':'Gerência audita a candidata e decide integração; mapa ainda não registrado por esta entrega.',
 'onde':str(OUT),'artefatos':[str(OUT/n) for n in ['PonteDaEscalaDual.lean','AXIOMAS.json','BUILD.log','RESULTADO.md','ANALISE_TECNICA.json','ESCOPO_PT.json']],
 'refs':['kernel.v401_falsidade_da_inercia','formal.f1_rede.concrete_bosonic_kinematics'],
 'nota':'Gate intacto. Inercial=fixo por todos os boosts. p± não normalizados; no par normalizado há fator2.'}
write('registro_mapa_ordem_025.json',mapentry)
manifest={'status':'ENTREGA_TECNICA_PONTE_PARCIAL','unit':'F1.PONTE_NOMEADA','reference':str(W/'SESSION_REFERENCE.json'),
 'source':pin(OUT/'PonteDaEscalaDual.lean'),'files':[pin(p) for p in sorted(OUT.rglob('*')) if p.is_file()],
 'management_audit_pending':True,'map_registration_by_management':True,'gate_changed':False}
write('RESULTADO.json',manifest)
for item in manifest['files']:assert pin(Path(item['path']))['sha256']==item['sha256']
new('DELIVERY_LOCAL_VERIFIED.json',{'result':pin(OUT/'RESULTADO.json'),'files_verified':len(manifest['files']),
    'source_sha16':hash16,'build_exit':b['exit_code'],'report_lines':len(result.splitlines())})
print(json.dumps({'result':str(OUT/'RESULTADO.json'),'files':len(manifest['files']),'source_sha16':hash16},ensure_ascii=False))
