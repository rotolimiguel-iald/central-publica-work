from pathlib import Path
import datetime, hashlib, json, os, re, subprocess

out = Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.FECHO_20261015')
base = out / 'maxwell_global'
work = Path(r'C:\IALD\Central de Patentes\work\memoria_missao_20261016')
kernel = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt')
ref = work / 'FECHO_MISSION_REFERENCE.json'
actor = {'kind': 'agent', 'id': 'codex-r49-maxwell-gap-inventory'}

def pin(p):
    p = Path(p)
    b = p.read_bytes()
    return {'path': str(p), 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}

paths = {
 'certificate': base/'AxisCompactMaxwellCertificateR4.lean',
 'regular': base/'AxisCompactRegularR2.lean',
 'nonzero': base/'AxisCompactFockNonzeroEnergyR4.lean',
 'charge': base/'CompactFockNullPlaneChargeR1.lean',
 'calibrated': base/'RegularFockMaxwellCalibratedR1.lean',
 'calibration_bridge': base/'CalibratedFockStressDomainBridgeR1.lean',
 'fock_tensor': base/'UnitaryFourierFockStressR1.lean',
 'fock_form': base/'RegularFockPointStressR4.lean',
 'coherent_stress': base/'CoherentPointStressR2.lean',
 'coherent_wave': base/'CoherentPointMaxwellR1.lean',
 'real_wave_stress': base/'RealProfileMaxwellStressR4.lean',
 'stress_polynomial': base/'MaxwellStressJetAlgebraR3.lean',
 'calibration': base/'UnitaryFourierRealStressR2.lean',
 'field': base/'PhysicalSchwartzMaxwellR1.lean',
 'weak_field': base/'WeakSegalDistributionR3.lean',
 'field_maxwell': base/'WeakMaxwellEquationR3.lean',
 'pairing': base/'PhysicalSmearWavePairingR2.lean',
 'wick': base/'WickQuadraticFormR6.lean',
 'circular_domain': base/'RegularCircularTransportR2.lean',
 'circular_smear': out/'orbital_rotation/PhysicalSmearTranslationR2.lean',
 'circular_basis': out/'orbital_rotation/ScreenCircularBasisR2.lean',
 'compact_localization': out/'orbital_rotation/PhysicalCompactNetCovarianceR1.lean',
 'physical_net': out/'orbital_rotation/PhysicalCanonicalNetCompleteR1.lean',
 'fock_net': out/'orbital_rotation/PhysicalFockNetRealizationR2.lean',
 'net_covariance': out/'orbital_rotation/PhysicalFockSpacetimeCovarianceR2.lean',
 'core_input': out/'weyl_net_wiring/CanonicalModularCoreAssemblyR1.lean',
 'contract': kernel/'TheImportedSecondQuantization.lean',
 'h3_contract': kernel/'ContratoQG_v31.lean',
 'null_solution': kernel/'O16/TeleologicalNullSolution_v2.lean',
 'null_consumer': kernel/'O16/NullSolutionConsumerReuse.lean',
 'curved_ligand': kernel/'LiganteLeiCampoCurvo.lean',
 'curved_control': kernel/'LiganteLeiCampoCurvoTestemunha.lean',
 'curved_source': kernel/'GeneralSourceEinsteinBridge.lean',
 'record': kernel/'GravitationalResponseRecord.lean',
 'record_decoder': kernel/'GeneralSourceResponseReconstruction.lean',
 'historical_inventory': out/'matter_h3_inventory/INVENTARIO_R8_R9_R1.md',
 'r48_progress': out/'PROGRESS_R48.json',
 'r48_review': out/'mission_review_20261016/R48_NONZERO_CERTIFICATE_INDEPENDENT_REVIEW_R1.json',
}
texts = {k: p.read_text(encoding='utf-8-sig') for k,p in paths.items()}
catalog = {k: pin(p) for k,p in paths.items()}
def loc(key, needle, last=None):
    lines=texts[key].splitlines()
    i=next(i for i,line in enumerate(lines) if needle in line)
    end=i if last is None else next(j for j in range(i,len(lines)) if last in lines[j])
    return {'source':key,'line':i+1,'end_line':end+1,'anchor':needle}
def decl(key, needle):
    lines=texts[key].splitlines()
    i=next(i for i,line in enumerate(lines) if needle in line)
    collected=[]
    for line in lines[i:]:
        collected.append(line)
        if ':=' in line or line.endswith(' where'):
            break
    return '\n'.join(collected).split(':=',1)[0].removesuffix(' where').strip()

builds=[]
checked={}
def verify(obj):
    if isinstance(obj,dict):
        if 'path' in obj and 'sha256' in obj:
            key=(obj['path'],obj['sha256'])
            if key not in checked:
                got=pin(obj['path'])
                assert got['sha256']==obj['sha256'], got
                if 'bytes' in obj: assert got['bytes']==obj['bytes']
                checked[key]=got
        for value in obj.values(): verify(value)
    elif isinstance(obj,list):
        for value in obj: verify(value)

progress=json.loads(texts['r48_progress'])
for comp in progress['components']:
    if Path(comp['source']['path']).name=='AxisCompactMaxwellCertificateR4.lean':
        verify(comp)
        receipt=json.loads(Path(comp['build']['path']).read_text(encoding='utf-8-sig'))
        verify(receipt)
        assert receipt['exit_code']==0
        assert Path(receipt['source']['path']).read_bytes()==paths['certificate'].read_bytes()
        ax=Path(comp['build']['path']).parent/'AXIOMS.txt'
        s=ax.read_text(encoding='utf-8')
        axlists=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',s)
        assert len(axlists)==5 and 'sorryAx' not in s and 'error:' not in s
        assert all(set(x.strip() for x in t.split(',')) <= {'propext','Classical.choice','Quot.sound'} for t in axlists)
        builds.append({'source':'certificate','receipt':pin(Path(comp['build']['path'])),
            'axioms':pin(ax),'exit_code':0,'seconds':receipt['seconds'],'axiom_lists':len(axlists)})
assert len(builds)==1
for key in ['physical_net','circular_domain','pairing','wick','field_maxwell','calibration_bridge']:
    found=[]
    for root in [out/'orbital_rotation/attempts',out/'kms_strip/attempts']:
        for candidate in root.glob('*/'+paths[key].name):
            rp=candidate.parent/'RECEIPT.json'
            if not rp.exists(): continue
            r=json.loads(rp.read_text(encoding='utf-8-sig'))
            if r.get('exit_code')!=0 or candidate.read_bytes()!=paths[key].read_bytes(): continue
            assert r['source']['sha256']==catalog[key]['sha256']
            ax=candidate.parent/'AXIOMS.txt'
            if not ax.exists(): continue
            s=ax.read_text(encoding='utf-8')
            axlists=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',s)
            assert axlists and 'sorryAx' not in s and 'error:' not in s
            assert all(set(x.strip() for x in t.split(',')) <= {'propext','Classical.choice','Quot.sound'} for t in axlists)
            found.append({'source':key,'receipt':pin(rp),'axioms':pin(ax),
                'exit_code':0,'seconds':r['seconds'],'axiom_lists':len(axlists)})
    assert found, key
    builds.append(found[-1])

rows=[
 {'id':'literal_certificate','status':'REAL_COMPILED_CONDITIONAL','refs':[loc('certificate','def axisCompactMaxwellCertificate'),loc('contract','structure MaxwellCertificate'),loc('certificate','theorem axisCompact_calibrated_regular_nontrivial')],
  'finding':'Todos os campos literais MaxwellCertificate foram construídos: domínio denso AxisCompact, vácuo/translação, tensor calibrado, charge_link, Regular integral e estado normalizado de energia modular não nula. Não há hipótese adicional de derivada, carga ou não vacuidade neste construtor.',
  'exact_signature':decl('certificate','def axisCompactMaxwellCertificate'),
  'remaining':'Para habitar esse tipo sobre a rede escolhida, fornecer A : RemainingModularCoreInput D. N é parâmetro explícito; selecionar um relógio físico pertence ao R4. Não refazer charge/Regular/testemunha.'},
 {'id':'same_network','status':'REAL_NETWORK_AVAILABLE__ASSEMBLY_SPECIALIZATION_PENDING','refs':[loc('physical_net','def physicalCanonicalNet'),loc('fock_net','def net'),loc('core_input','structure RemainingModularCoreInput'),loc('core_input','def RemainingModularCoreInput.toCertificate')],
  'finding':'D não precisa ser novo postulado: physicalCanonicalNet já foi construído e compilado; PhysicalFockNet.net é FieldWeyl.R dessa rede. A deve ser indexado por esse D explícito. A contém dados/leis de traço e PF do núcleo representado; não foi habitado por R48.',
  'typed_target':'(A : RemainingModularCoreInput F1Fecho.MaxwellLocalization.physicalCanonicalNet) (N : KillingNormalization) : MaxwellCertificate A.toCertificate := axisCompactMaxwellCertificate A N'},
 {'id':'tensor_from_maxwell_waves','status':'REAL_EXPLICIT_CONSTRUCTION','refs':[loc('calibration_bridge','theorem calibratedStress_eq_unitaryFourierFock'),loc('fock_tensor','def unitaryFourierPointStressForm'),loc('fock_form','def pointStressForm'),loc('coherent_stress','def coherentProfileStress'),loc('coherent_wave','def coherentProfileWave'),loc('stress_polynomial','def stress')],
  'finding':'O tensor não é uma função arbitrária que passa pelo tipo. É a parte real da forma sesquilinear de somas coerentes únicas, cujo kernel é exp(inner h k) vezes o polinômio de Maxwell aplicado às ondas coerentes efetivas; multiplicado por c=(2π)^(-3). Isso prova proveniência por ondas Maxwell, ainda distinta de identificar o Wick local do campo operador smeared.'},
 {'id':'symmetry_conservation','status':'REAL_CONSTRUCTED_AND_TRANSPORTED','refs':[loc('coherent_wave','theorem coherentProfileJet_bianchi'),loc('coherent_wave','theorem coherentProfileJet_divergence'),loc('coherent_stress','theorem coherentProfileStress_conserved'),loc('fock_tensor','theorem unitaryFourierPointStressForm_symmetric'),loc('fock_tensor','theorem unitaryFourierPointStressForm_weak_conserved'),loc('calibrated','def scaleMaxwellQuadraticForm')],
  'finding':'Antissimetria, Bianchi e divergência da onda dão conservação do polinômio. Somatório finito e calibração preservam simetria e conservação distribucional de Minkowski. Não confundir essa lei plana com conservação covariante para uma métrica curva a determinar.'},
 {'id':'field_exists','status':'REAL_DISTINCT_FIELD_COMPONENT','refs':[loc('field','def physicalSmearCLM'),loc('field','def physicalField'),loc('field','theorem exists_nonzero_physicalField_vacuum'),loc('weak_field','def weakPhysicalField'),loc('field_maxwell','theorem weakPhysicalField_spacetimeDivergence_zero'),loc('pairing','theorem physicalSmear_inner_wave')],
  'finding':'O campo de Segal físico e sua distribuição fraca existem no mesmo Fock; há excitação não nula do vácuo e identidade Maxwell de divergência. physicalSmear_inner_wave liga a smearing às ondas do mesmo H1, conservando a contração 1/2. Essa igualdade linear não identifica por si o produto de Wick coincidente.'},
 {'id':'wick_local_normalization','status':'OPEN_MATERIAL_PROVENANCE_LINK','refs':[loc('wick','def quadratic'),loc('wick','theorem coherent_kernel'),loc('fock_form','No density'),loc('calibration','def unitaryFourierStressScale'),loc('field','def physicalField')],
  'finding':'WickQuadraticFormR6 constrói uma forma bilocal normalmente ordenada a partir de aniquilação; o consumidor que restringe ao ponto coincidente e contrai seus índices para obter pointStressForm não foi localizado. physicalField usa physicalSmearCLM sem o fator c. O tensor certificado é c·pointStressForm; a identificação correta deve construir o campo normalizado por r=sqrt(c), provar r²=c e consumir essa normalização, sem parâmetro físico ajustável e sem alterar o campo antigo.',
  'next_exact_target':'let r : ℂ := (Real.sqrt unitaryFourierStressScale : ℂ); ∀ f g h k : H1, F1Fecho.WickForm.quadratic (r • f) (r • g) (F1Fecho.WickForm.expDomain h) (F1Fecho.WickForm.expDomain k) = (unitaryFourierStressScale : ℂ) * F1Fecho.WickForm.quadratic f g (F1Fecho.WickForm.expDomain h) (F1Fecho.WickForm.expDomain k)',
  'next_after_scaling':'Usar physicalSmear_inner_wave + coherent_kernel para a fórmula bilocal smeared; construir a restrição coincidente nos perfis regulares por aproximação explícita de testes, contrair o polinômio stress e estender por finiteKernel. Exigir igualdade com unitaryFourierPointStressForm, não defini-la como premissa.'},
 {'id':'circular_representation','status':'OPEN_EXPLICIT_LINK__DOMAIN_TRANSPORT_EXISTS','refs':[loc('circular_smear','def circularSmear'),loc('compact_localization','def compactSupportedGenerators'),loc('circular_domain','def regularCircular'),loc('circular_domain','theorem strongRegularProfile_fiberLift'),loc('circular_basis','theorem fiberLift_U1'),loc('circular_basis','theorem fiberLift_B0')],
  'finding':'A rede compacta é gerada por circularSmear=circularH1.symm∘physicalSmearCLM. O campo antigo usa physicalSmearCLM diretamente. A identidade do espaço H1 não basta para identificar esses campos locais. Reutilizar regularCircular e o entrelaçamento com U1/B0; transportar também o domínio AxisCompact, os estados e o tensor ou provar a igualdade exigida. Não afirmar invariância do tensor sob circularH1 sem prova.',
  'next_exact_target':'let r : ℂ := (Real.sqrt unitaryFourierStressScale : ℂ); ∀ (f g : SchwartzTensor) (h k : H1), F1Fecho.WickForm.quadratic (r • F1Fecho.MaxwellLocalization.circularSmear f) (r • F1Fecho.MaxwellLocalization.circularSmear g) (F1Fecho.WickForm.expDomain h) (F1Fecho.WickForm.expDomain k) = F1Fecho.WickForm.quadratic (r • physicalSmearCLM f) (r • physicalSmearCLM g) (F1Fecho.WickForm.expDomain (F1Fecho.OrbitalScreen.circularH1 h)) (F1Fecho.WickForm.expDomain (F1Fecho.OrbitalScreen.circularH1 k))',
  'shortcut':'coherent_kernel, circularH1.apply_symm_apply, inner_map_map, gamma_exponential e RegularCircularTransportR2; nenhum desses lemas autoriza omitir a mudança dos vetores h,k.'},
 {'id':'standard_h3_source','status':'EXISTING_CONSUMER__SPECIALIZATION_PENDING','refs':[loc('contract','def lightH3 '),loc('contract','def lightH3v32 '),loc('contract','def lightImport '),loc('null_solution','def construct_null_solution'),loc('null_consumer','def responseOf'),loc('h3_contract','structure ContratoH3')],
  'finding':'Com M=axisCompactMaxwellCertificate A N, lightH3/lightH3v32/lightImport já consomem exatamente M.T, Regular, charge_link e nontrivial. G>0 permanece parâmetro explícito. A geometria produzida é resposta linearizada de tela diag(0,0,-a,-a) à fonte T_nn ao longo de nullDir=(1,1,0,0), em todo ponto; o fator 8πG está no propagador construído.',
  'exact_signature':decl('contract','def lightH3v32 '),
  'typed_consumer':'(A : RemainingModularCoreInput D) (N : KillingNormalization) (G : ℝ) (hG : 0 < G) : ContratoH3v32 (lightNet A.toCertificate) (lightRealization A.toCertificate) N (lightBoost A.toCertificate) (axisCompactMaxwellCertificate A N).T := lightH3v32 (axisCompactMaxwellCertificate A N) N G hG',
  'remaining':'Compor e auditar esse consumidor específico; não reconstruir a solução nula. O alvo não fornece uma métrica curva global que satisfaça todas as componentes de Einstein.'},
 {'id':'curved_source_boundary','status':'OPEN_STRONGER_REALIZATION__R9_CLASSIFICATION_RETAINED','refs':[loc('curved_ligand','def NamedAtlasH3'),loc('curved_ligand','theorem passage_h3_to_connected_smooth_atlas_einstein'),loc('curved_control','theorem s5_local'),loc('curved_source','theorem general_source_einstein_from_area'),loc('record','def recordSource'),loc('record_decoder','theorem ten_responses_reconstruct_source_field')],
  'finding':'O antecedente de H3 curvo quantifica sobre toda carta, ponto e direção nula não zero. Não é consequência automática da equação na direção nullDir. A rota existente requer identificar o mesmo tensor Maxwell como recordSource, construir métrica/telas compatíveis, conservação covariante e a lei de área/Ricci para esses mesmos dados. O controle s5_local explicita o conteúdo Ricci dessa obrigação.',
  'typed_source_identification':'(A : RemainingModularCoreInput D) (ψ : regularFockDomain) (U : Set Coordinate4) (R : GravitationalResponseRecord U) : ∀ x ∈ U, recordSource R x = (toStress (regularMaxwellCalibratedForm A)).T ψ.val x',
  'typed_geometric_target':'NamedAtlasH3 ((4 * G)⁻¹) U R screens',
  'scope':'R9 já está satisfeito como classificação de alcance, não como prova do antecedente físico. Este inventário não reabre R9 nem adiciona Einstein curvo ao tipo MaxwellCertificate. Se a fonte geométrica de R8 pretendida for essa rota forte, a ligação continua aberta; para H3 da cunha padrão, a composição anterior basta sob A,N,G.'},
]

req={'operation':'project','reference':str(ref),'actor':actor,'max_chars':100000}
response=json.loads(subprocess.run([r'C:\Python314\python.exe','-B','-X','utf8',r'C:\IALD\MEMORIA_IALD\mission_cli.py'],input=json.dumps(req),text=True,encoding='utf-8',capture_output=True,check=True).stdout)
assert response['ok'], response
p=response['result']
r8=next(x for x in p['projection']['active'] if x['id']=='R8')
r9=next(x for x in p['projection']['settled'] if x['id']=='R9')
report={
 'schema':'iald-r8-gap-inventory/v1','status':'DERIVED_SOURCE_INVENTORY__R8_OPEN',
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'actor':actor,'handle':'r49-maxwell-gap-inventory','reference':pin(ref),
 'mission_receipt':p['receipt'],'projection_sha256':p['projection_sha256'],
 'requirement':{k:r8[k] for k in ['id','criterion','status','epoch']},
 'r9_preserved':{k:r9[k] for k in ['id','criterion','status']},
 'conclusion':'Para o tipo literal MaxwellCertificate, A é a obrigação de existência restante depois de fixar a rede construída D; N permanece parâmetro. Isso não encerra a realização conjunta mais forte de R8: faltam identificar o Wick local do campo normalizado com o tensor calibrado e explicitar o transporte circular na mesma rede. H3 padrão tem consumidor pronto para composição; H3 curvo mantém seus antecedentes classificados, não derivados.',
 'rows':rows,'sources':catalog,'build_evidence':builds,
 'verification':{'certificate_receipt_and_component_pins_checked':len(checked),
     'checked_bytes':sum(x['bytes'] for x in checked.values()),
     'certificate_axiom_lists':5,'certificate_only_standard_trio':True,
     'additional_direct_green_receipts':len(builds)-1,
     'no_new_build':True,'no_production_or_provider':True,
     'search_scope':'Inspected Maxwell sources, physical net/circular transport, existing Wick and weak fields, R48 custody, prior matter/H3 inventory and exact kernel geometric consumers. Absence claims are limited to this source chain; type sketches in inventory are proposed consumers, not newly compiled declarations.'},
 'reuse_update':'O inventário R8/R9 de 15/10 fica histórico: suas lacunas de Regular, carga e testemunha foram descarregadas em R47/R48. Não repetir esses alvos. Permanecem distintas a identificação Wick, a representação circular e a interpretação geométrica forte.',
 'requirement_satisfied':False,'mission_mutations':False,'script':pin(Path(__file__))
}
dst=base/'R49_MAXWELL_GAP_INVENTORY_R1.json'
data=(json.dumps(report,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
assert not dst.exists()
tmp=dst.with_name(dst.name+'.tmp_r49')
with tmp.open('xb') as f:
    f.write(data);f.flush();os.fsync(f.fileno())
assert tmp.read_bytes()==data
os.rename(tmp,dst)
print(json.dumps({'report':pin(dst),'rows':len(rows),'sources':len(catalog),'verified_pins':len(checked),'direct_green_receipts':len(builds),'revision':p['receipt']['revision']},ensure_ascii=False))
