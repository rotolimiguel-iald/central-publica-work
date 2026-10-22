from pathlib import Path
import datetime, hashlib, json, os, re, subprocess
helpers=Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016\pin_local_wick_r51_r2.py')
exec(helpers.read_text(encoding='utf-8').split('candidates=[')[0])
ACTOR={'kind':'agent','id':'codex-r52-maxwell-assembly'}
sources=[BASE/'CircularMaxwellCertificateR2.lean',BASE/'PhysicalMaxwellJointRealizationR2.lean']
candidate=[]
for f in sources:
    t=f.read_text(encoding='utf-8')
    assert not re.search(r'\b(sorry|admit)\b|^\s*(axiom|opaque)\s',t,re.M)
    assert 'set_option maxHeartbeats 400000' in t
    assert 'set_option synthInstance.maxHeartbeats 500000' in t
    candidate.append({'source':pin(f),'status':'DECLARADO_CANDIDATE',
      'imports':re.findall(r'^import (.+)$',t,re.M),
      'expected_print_count':len(re.findall(r'^#print axioms ',t,re.M)),
      'public_print_declarations':re.findall(r'^#print axioms (.+)$',t,re.M)})
suppliers=[green(f) for f in [BASE/'AxisCompactMaxwellCertificateR4.lean',
    BASE/'AxisCompactCircularTransportR2.lean',BASE/'PointAnnihilationSmearingR4.lean',
    BASE/'LocalWickStressIdentificationR3.lean',
    OUT/'takesaki_fock/CanonicalFockModularCoreInputR1.lean',
    OUT/'orbital_rotation/PhysicalFockSpacetimeCovarianceR2.lean']]
builds=[green(f,False) for f in sources]
K=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel')
extra=[BASE/'CircularPhysicalFieldTransportR1.lean',BASE/'FockSegalUnitaryTransportR1.lean',
    BASE/'RegularCircularTransportR2.lean',BASE/'R49_MAXWELL_GAP_INVENTORY_R1.json',
    BASE/'UnitaryFourierRealStressR2.lean',BASE/'PhysicalSchwartzMaxwellR1.lean',
    OUT/'orbital_rotation/PhysicalCanonicalNetCompleteR1.lean',
    OUT/'orbital_rotation/PhysicalFockNetRealizationR2.lean',
    OUT/'orbital_rotation/PhysicalCompactNetCovarianceR1.lean',
    OUT/'orbital_rotation/LorentzFutureRepresentationR1.lean',
    OUT/'weyl_net_wiring/CanonicalModularCoreAssemblyR1.lean',
    K/'TGLExt/TheImportedSecondQuantization.lean',K/'TGLExt/ContratoQG_v31.lean',
    K/'TGLExt/ContratoQG_v32.lean',K/'TGLExt/O16/NullSolutionConsumerReuse.lean',
    K/'TGLExt/O16/TeleologicalNullSolution_v2.lean',
    OUT/'PROGRESS_R51.json',OUT/'mission_review_20261016/R51_SMEARING_REVIEW_R1.json']
for f in extra:pin(f)
req={'operation':'project','reference':str(REF),'actor':ACTOR,'max_chars':100000}
run=subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],
    input=json.dumps(req),text=True,encoding='utf-8',capture_output=True,check=True)
response=json.loads(run.stdout);assert response['ok'],response
p=response['result'];r8=next(x for x in p['projection']['active'] if x['id']=='R8')
assert r8['status']=='working'
report={
 'schema':'iald-lean-candidate/v1','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'DECLARADO_PENDING_ROOT_BUILDS_AND_INDEPENDENT_REVIEW','author':ACTOR,
 'requirement':'R8','handle':'r52-maxwell-joint-consumer','requirement_satisfied':False,
 'mission_reference':pin(REF),'mission_receipt':p['receipt'],'projection_sha256':p['projection_sha256'],
 'criterion':r8['criterion'],'lease_observed':r8['lease'],
 'handoff':pin(OUT/'mission_resume_20261016/LIVE_HANDOFF_R8_20261016T210023_853406Z_7f09640e_RECEIPT.json'),
 'repair_scope':{'preserved':[pin(BASE/'CircularMaxwellCertificateR1.lean'),pin(BASE/'PhysicalMaxwellJointRealizationR1.lean')],'failed_receipt':pin(OUT/'orbital_rotation/attempts/20261016T210854_377096Z/RECEIPT.json'),'failed_axioms':pin(OUT/'orbital_rotation/attempts/20261016T210854_377096Z/AXIOMS.txt'),'changes':['Regular iff: explicit conjunct constructors and typed norm equalities.','Modular energy iff: congrArg of typed HasDerivAt predicate followed by convert!.','Joint consumer: only its import changes to CircularMaxwellCertificateR2.'],'statements_and_hypotheses_unchanged':True},
 'sources':candidate,'existing_suppliers':suppliers,'root_builds_observed':builds,
 'direct_reuse':[pin(f) for f in extra],
 'supplier_receipt_pins_verified':len(checked),
 'supplier_receipt_bytes_verified':sum(x['bytes'] for x in checked.values()),
 'analysis_before_candidate':[
  'A fábrica modular R1 agora tem recibo EXIT0 e 11 relatórios; usa ENNReal cyclicTraceCandidate, não uma afirmação nova de traço linear complexo em toda a álgebra.',
  'physicalCanonicalNet já habita CanonicalNetInput. D permanece explícito apenas na fábrica genérica; o consumidor físico o instancia. A rede de Fock é identificada por igualdade com PhysicalFockNet.net.',
  'A rede usa circularSmear, enquanto o tensor calibrado antigo usa a base linear. A ponte R50 exige transportar os estados por regularCircular. Identificar ambos mantendo o mesmo vetor seria um salto; a nova peça transporta explicitamente o tensor e o certificado, sem alterar a fonte antiga.',
  'A simetria, conservação fraca, regularidade integral, carga e testemunha são transportadas por Γ(circularH1), preservando Fock, domínio AxisCompact, translações e boost.',
  'O tensor local continua uma forma Wick genuína de quatro termos no domínio regular, cuja coincidência foi provada em R51; não há avaliação pontual limitada em H1 ou operador pontual limitado em Fock.',
  'O consumidor geométrico H3 existente recebe o mesmo tensor e a mesma testemunha admissível. Seu alcance é a resposta de tela linearizada na direção nula fixa; a afirmação universal/curva mais forte e a realização do dispositivo permanecem separadas.'
 ],
 'construction':[
  'circularCalibratedStress.T ψ = originalCalibratedStress.T (gamma circularH1 ψ). A prova de carga usa a igualdade literal da função de correlação modular, não uma nova premissa de energia/carga.',
  'circularMaxwellCertificate conserva todos os campos do tipo MaxwellCertificate. Dom é o mesmo axisCompactFockDomain denso; não trivialidade vem do vetor antigo aplicado ao unitário inverso.',
  'circularLocalWickStress é o transporte da forma Wick anterior, não uma definição a partir do tensor. normalizedCircularWick_eq_pointSmear já liga o transporte à expressão Segal real smeared.',
  'normalizedCircular_annihilation_point_integral liga o aniquilador circular efetivo, em ambos os lados transportado, ao Bochner do aniquilador pontual; circular_point_integrable fornece sua integrabilidade.',
  'physicalMaxwell_joint_witness reúne em um único ψ de regularFockDomain: AxisCompact, Regular literal, norma 1, energia modular não nula, carga e igualdade com o tensor Wick.',
  'physicalMaxwellH3 e physicalMaxwellImport usam physicalFockCertificate, o mesmo boost e o mesmo T. physicalMaxwellH3_raychaudhuri_wick escreve explicitamente a fonte nn em termos do tensor Wick.',
  'normalizedCircularSmear_compact_mem e normalizedCircularWeyl_local ligam o fator de amplitude fixo à mesma sub-rede compacta; c=(2*pi)^(-3), amplitude=sqrt(c), sem constante ajustável.'
 ],
 'explicit_inputs':['KillingNormalization N','G : real and 0 < G for the existing geometric consumer'],
 'new_physical_premises':[],
 'scope_limits':[
  'A autoria não executou build; os dois novos arquivos continuam candidatos até recibos completos e revisão distinta.',
  'Não há aceite integral de R8, alteração de missão, gate, kernel de produção ou memória global.',
  'Não se afirma classificação de fator II, traço total complexo linear, operador pontual limitado, tensor interagente, geometria não linear universal ou realização do dispositivo.',
  'Não se refaz a covariância existente: PhysicalFockSpacetimeCovarianceR2 cobre FutureLorentz via futureToGenerated; o resíduo R5 é a identificação/realização do dispositivo, não uma lacuna genérica de Lorentz.',
  'A igualdade do tensor circular com o antigo tensor sem transporte do estado não é afirmada.'
 ],
 'verification_scope':'Bytes e recibos dos fornecedores conferidos por script; isto não substitui revisão independente nem compila os candidatos.',
 'write_script':pin(Path(__file__))
}
dest=BASE/'PHYSICAL_MAXWELL_JOINT_CANDIDATES_R52_R2.json'
payload=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
tmp=dest.with_name(dest.name+'.tmp_'+str(os.getpid()))
assert not dest.exists(),dest
with tmp.open('xb') as f:f.write(payload);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==payload
os.rename(tmp,dest)
assert dest.read_bytes()==payload
print(json.dumps({'manifest':pin(dest),'revision':p['receipt']['revision'],
 'pins_verified':len(checked),'candidates':[x['source'] for x in candidate],
 'builds':[{'source':Path(x['source']['path']).name,'status':x['status']} for x in builds]},ensure_ascii=False))
