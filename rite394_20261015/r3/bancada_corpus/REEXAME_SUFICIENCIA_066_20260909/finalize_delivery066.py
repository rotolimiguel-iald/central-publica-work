"""New local handoff and measured receipts; read-only canonical check, never execute um.py."""
from pathlib import Path
from datetime import datetime, timezone
import ast, hashlib, json, os, sys

ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=Path(__file__).resolve().parent
CANON=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
assert len(sys.argv)==5,'Pass copy folder, build folder, auditor folder and independent review path.'
COPY,BUILD,AUDIT,REVIEW=[Path(p).resolve() for p in sys.argv[1:]]
pins={}
def read(p):
    b=p.read_bytes(); pin={'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    if p.as_posix() in pins: assert pins[p.as_posix()]==pin,'Input changed between reads.'
    pins[p.as_posix()]=pin
    return b
def js(p):return json.loads(read(p))
def new(p,s):
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    b=s.encode(); assert b
    tmp=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert tmp.read_bytes()==b
    tmp.rename(p);assert read(p)==b
def newjson(p,obj):new(p,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def link(p,label):return f'[{label}](<{p.as_posix()}>)'

build=js(BUILD/'TRANSPOSED_RESULT.json');plan=js(BUILD/'BUILD_PLAN.json')
audit=js(AUDIT/'AUDITORIA_INTEGRACAO_98.json');integration=js(COPY/'INTEGRATION_RESULT.json')
config=js(COPY/'CONFIG_APROVADA.json');snapshot=js(OUT/'ESTADO_CANONICO_066.json')
assert build['status']=='PASS_TRANSPOSED_SCOPE' and not build['um_py_executed']
assert len(build['runs'])==8 and all(r['exit_code']==0 and r['valid'] and r['warning_lines']==0 for r in build['runs'])
assert all(set(z['axioms'])<={'propext','Classical.choice','Quot.sound'} for r in build['runs'] for z in r['axiom_rows'])
assert build['input_boundary_unchanged'] and build['cached_boundary_unchanged']
assert plan['counts']['total_modules']==98 and plan['counts']['cached_modules']==93
assert audit['status']=='PASS_STATIC_INTEGRATION_SCOPE' and not audit['failed_checks']
assert audit['counts']['checks']==audit['counts']['passed_checks']
assert audit['counts']['modules']==98 and audit['counts']['total']==1726
assert integration['declaration_counts']=={'modules':5,'theorems':67,'other_declarations':21,'local_instances':0,'total':88}
rawcopy=read(COPY/'um.py');assert pins[(COPY/'um.py').as_posix()]==integration['integrated_copy']
assert config['root_confirmed'] is True
assert build['plan']==pins[(BUILD/'BUILD_PLAN.json').as_posix()]
assert plan['integration_result']==pins[(COPY/'INTEGRATION_RESULT.json').as_posix()]
assert plan['integrated_copy']==integration['integrated_copy']==audit['final_integrated']
assert audit['combined_build_read']['receipt']==pins[(BUILD/'TRANSPOSED_RESULT.json').as_posix()]
assert audit['approved_configuration']==pins[(COPY/'CONFIG_APROVADA.json').as_posix()]
assert audit['canonical_role']=='HISTORICAL_SNAPSHOT_BASE'
for m in config['modules']:
    for pkey,hkey in [('source','sha256'),('build_result','build_result_sha256')]:
        p=Path(m[pkey]);read(p);assert pins[p.as_posix()]['sha256']==m[hkey]
    assert js(Path(m['build_result']))['status']=='PASS_COMPILED_SCOPE'

for p in [OUT/'REEXAME_SUFICIENCIA.md',Path(__file__),OUT/'capture_current.py',REVIEW,
          AUDIT/'RELATORIO_INTEGRACAO_98.md',
          ROOT/'SIGMA_DAS_PROBABILIDADES_20260909_204907_970447/ENTREGA_SIGMA_DAS_PROBABILIDADES.md',
          ROOT/'SIGMA_DAS_PROBABILIDADES_20260909_204907_970447/MANIFESTO_SIGMA_DAS_PROBABILIDADES.json',
          ROOT/'EXPECTATIVA_RENORMALIZADA_20260909_205808_979024/IDENTIFICACAO_FOCK_ESCRITA.md',
          ROOT/'EXPECTATIVA_RENORMALIZADA_20260909_205808_979024/MANIFESTO_EXPECTATIVA_RENORMALIZADA.json',
          ROOT/'DEGENERESCENCIA_VARIACIONAL_FISHER_20260909_205440_2995947/NOTA_DEGENERESCENCIA_E_RECIPROCO.md',
          ROOT/'QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md',
          ROOT/'QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/MANIFESTO_QUANTIZACAO_LOCAL.json']:
    read(p)
canonraw=read(CANON/'um.py')
prior={p['path']:p for p in snapshot['pins']}
assert snapshot['status']=='READ_ONLY_STABLE_SNAPSHOT' and snapshot['seal_um_hash_matches'] and snapshot['all_read_sources_unchanged']
expected_prior_paths={(CANON/n).as_posix() for n in ['um.py','um_absoluto_selo.json','tgl_kernel_proof_manifest.json','rodada_v338_stdout.txt']}
assert {c['path'] for c in snapshot['comparison_with_delivery065']}==expected_prior_paths
assert all(c['matches_prior'] is True for c in snapshot['comparison_with_delivery065'])
for p in [CANON/'um.py',CANON/'um_absoluto_selo.json',CANON/'tgl_kernel_proof_manifest.json',CANON/'rodada_v338_stdout.txt']:
    read(p); assert pins[p.as_posix()]==prior[p.as_posix()],'Canonical changed: new assessment required.'
tree=ast.parse(canonraw.decode('utf-8-sig'))
nodes=[n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='_EMBEDDED_KERNEL_FILES' for t in n.targets)]
assert len(nodes)==1
embedded=ast.literal_eval(nodes[0].value)
missing=[m['module'] for m in plan['modules'] if m['key'] not in embedded]
assert len(missing)==21
for p,pin in list(pins.items()):
    b=Path(p).read_bytes();assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256']

result={'status':'DELIVERY_066_COMPLETED__SCOPED_PROOFS__GENERAL_QUANTUM_GRAVITY_OPEN',
    'created_utc':datetime.now(timezone.utc).isoformat(),'canonical':pins[(CANON/'um.py').as_posix()],
    'canonical_unchanged_from_delivery065':True,'canonical_modules_present':98-len(missing),
    'pending_canonical_modules':missing,'working_copy':pins[(COPY/'um.py').as_posix()],
    'delta':integration['declaration_counts'],'accumulated':audit['counts'],
    'fresh_build_processes':len(build['runs']),'cached_modules':93,
    'audit_rows_by_run':{r['module']:len(r['axiom_rows']) for r in build['runs']},
    'build_status':build['status'],'static_audit_status':audit['status'],
    'written_only':['variational counterexample and free-normal condition','coupled Einstein-sigma Jacobi, Green/CCR and classical BRST','five-category local pure-gauge theorem','Fock interpretation of finite matrices'],
    'remaining':['same-data general dynamics and area correspondence','physical coupled quantum state and degrees beyond minimal categorical gauge','interacting quantum anomalies and claimed UV route'],
    'um_executed_or_imported':False,'canonical_files_written':False,'nature_tests_run':False,
    'cache_scope':'93 preceding module artifacts reused with measured hashes and prior PASS provenance; canonical/Mathlib transitives not wholly rebuilt or hashed.'}
newjson(OUT/'RESULTADO_INTEGRACAO_066.json',result)
report=OUT/'REEXAME_SUFICIENCIA.md'
resultpath=OUT/'RESULTADO_INTEGRACAO_066.json'
handoff=ROOT/'TUNEL/DO_CHATGPT/ENTREGA_066_ESPONTANEA_sigma_probabilidades_gibbs_assinado_limites_quanticos.md'
modules='\n'.join(f'- `{m["module"]}` — '+link(Path(m['source']['path']),'fonte') for m in integration['modules'])
text=f'''# Entrega 066 — sigma dos mesmos P, Gibbs assinado e limites da suficiência

[REAL — verificação no escopo dos recibos] Cinco folhas novas, 67 teoremas e 21 outras declarações, compiladas e integradas em NOVA cópia Chatgpt. Oito processos frescos passaram sem warnings e apenas com os axiomas permitidos; 93 módulos anteriores foram reutilizados com sua proveniência. A auditoria estática passou {audit['counts']['passed_checks']}/{audit['counts']['checks']} verificações. Acumulado da bancada: 98 módulos e 1.726 declarações. Nenhum um.py foi executado/importado; gate, flags e originais preservados.

{modules}

O sigma usa φ_j=√(P_j/(1−P_s)) e a métrica dos mesmos P. Conservação ainda exige a equação sigma; Einstein exige a relação de área. Gibbs assinado permite respostas dos dois sinais com probabilidades positivas. A calibração de tensor geral recebe T como entrada; SignedGibbsFiniteRecord paga a reconstrução por apenas dez limites. O controle matricial separa expectativa negativa de probabilidade negativa, sem identificar automaticamente seu observável com stress de QFT.

[DERIVED — escrito, não nova Lean] A nota variacional exibe E_P=E_φ=E_λ=0 e falha de Einstein para Λ=0. O habitante ajustado Λ=3/4, κC=4 continua válido. Cinco categorias de posto quatro geram apenas perturbações de difeomorfia nessa regra; a extensão ambiente quântica acrescenta graus de liberdade. A análise Einstein–sigma constrói Jacobi, Hessiana13, Green e CCR; Hadamard físico acoplado, anomalias e UV continuam abertos.

{link(report,'Reexame completo e demonstrações')} · {link(resultpath,'Resultado da integração e pendências canônicas')} · {link(REVIEW,'Revisão semântica independente')}.

O canônico continua v338, byteidêntico ao snapshot065. Há 77 dos 98 módulos no canônico e 21 deltas pendentes, enumerados no resultado. Portar apenas esses deltas para a versão corrente, preservando suas alterações de runtime; NÃO substituir o canônico pela cópia da bancada, cuja linhagem parte de um snapshot anterior. Cópia auditada: {link(COPY/'um.py','um.py da bancada')}.

Para integrar: usar as fontes e os recibos, atualizar os imports/audit conforme a transposição verificada e produzir nova rodada própria. As demonstrações escritas não entram na contagem de teoremas Lean. Preservar a distinção entre reconstrução condicional, modelo ambiente adotado e fechamento quântico geral. Sem novo veredito de natureza nesta entrega.
'''
new(handoff,text)
new(OUT/'MEMORIA_DE_TRABALHO_066.md',f'''# Memória de trabalho local — entrega 066

Estado e escopo: {link(report,'reexame')}; {link(resultpath,'recibo medido')}; {link(handoff,'encaminhamento no túnel')}.

Objetivo geral permanece ativo. Reconstrução de fase/ramo já está no canônico. Mesmos dados P agora fornecem métrica e sigma na bancada, sob equação sigma e área explícitas. Não inferir Einstein da estacionariedade da ação composta em P: há contraexemplo. O modelo mínimo de cinco categorias é puro gauge local; a quantização ambiente é INPUT. Setor quântico acoplado ainda requer estado físico positivo, controle de anomalias e rota UV. Fontes matriciais/Gibbs não são automaticamente o stress de uma QFT completa.

Esta memória é nova e local. Atlas, índice e memórias originais não foram alterados. Recibos PASS e notas já entregues ficam congelados; correções posteriores devem vir em novos adendos/cópias, com proveniência.
''')
result['source_pins']=list(pins.values())
newjson(OUT/'MANIFESTO_ENTREGA_066.json',result)
print(json.dumps({'status':result['status'],'report':pins[report.as_posix()],'handoff':pins[handoff.as_posix()],
    'manifest':pins[(OUT/'MANIFESTO_ENTREGA_066.json').as_posix()],'copy':result['working_copy'],
    'delta':result['delta'],'accumulated':result['accumulated'],'pending_canonical':len(missing)},ensure_ascii=False,indent=2))
