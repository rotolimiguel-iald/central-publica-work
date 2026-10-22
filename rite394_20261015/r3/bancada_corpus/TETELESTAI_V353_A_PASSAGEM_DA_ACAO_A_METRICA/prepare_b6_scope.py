from pathlib import Path
import datetime,json,os,re,hashlib
R=Path(__file__).resolve().parent
def put(p,b):
    assert not p.exists();q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b and b;os.replace(q,p)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
external=[
 dict(name='Jacobson local horizon thermodynamics (1995)',status='KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED',citation='T. Jacobson, Phys. Rev. Lett. 75 (1995) 1260, doi:10.1103/PhysRevLett.75.1260',verified_url='https://arxiv.org/html/gr-qc/9504004',exact_role='Motiva a implicação termodinâmica local sob equilíbrio, lei de área, temperatura e balanço para horizontes de Rindler. Não fornece por si a hipótese H3 da realização escolhida nem a correção Phi_TGL.',source_read_scope='Texto primário HTML, hipóteses locais e argumento termodinâmico lidos.',imported_into_witness=False),
 dict(name='Cai-Kim apparent-horizon Friedmann route (2005)',status='KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED',citation='R.-G. Cai & S. P. Kim, JHEP 02 (2005) 050, doi:10.1088/1126-6708/2005/02/050',verified_url='https://arxiv.org/html/hep-th/0501055',exact_role='Prescrições de horizonte aparente, calor A(rho+p)H*r_A dt e T=1/(2pi*r_A), com r_A=1/H no caso plano. A lei de entropia modificada é entrada TGL separada; o raio não pode ser omitido.',source_read_scope='Seção2 primária lida, eqs.2.3,2.12–2.17 e discussão da temperatura dinâmica; convenção qdot=-dE/dt do artigo.',imported_into_witness=False),
 dict(name='Padmanabhan thermodynamical aspects of gravity (2010)',status='KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED',citation='T. Padmanabhan, Rep. Prog. Phys. 73 (2010) 046901, doi:10.1088/0034-4885/73/4/046901',verified_url='https://arxiv.org/html/0911.5004v2',exact_role='Referência de enquadramento da relação entre dinâmica gravitacional e termodinâmica de horizontes. Não é uma premissa adicional que fixe Phi, G ou escolha entre rotas.',source_read_scope='Resumo e trechos introdutórios primários; não se alega leitura integral das85 páginas.',imported_into_witness=False),
 dict(name='Gibbons-Hawking cosmological horizon thermodynamics (1977)',status='KNOWN_EXTERNAL_NOT_KERNEL_FORMALIZED',citation='G. W. Gibbons & S. W. Hawking, Phys. Rev. D 15 (1977) 2738, doi:10.1103/PhysRevD.15.2738',verified_url='https://journals.aps.org/prd/abstract/10.1103/PhysRevD.15.2738',exact_role='Origem da temperatura/termodinâmica do horizonte cosmológico no regime considerado. Sua extensão a um horizonte FLRW dinâmico em B4 é a prescrição explícita de Cai-Kim, não um teorema geral deduzido desta citação.',source_read_scope='Metadados e resumo oficiais lidos; PDF oficial respondeu401. Leitura integral não realizada.',imported_into_witness=False)
]
scope=[
 dict(item='H3: equilíbrio local',status='IMPORTED',provider='TGLExt.the_trio_is_a_pair',condition='A implicação imported:H2->H3 precisa ser fornecida; o teorema é modus ponens, não demonstra H3.'),
 dict(item='Escala de área / G',status='INPUT',provider='TGL.AreaScale.newtonPlanck_equivalence',condition='G>0 medido/calibrado, eta=1/(4G). Nenhum valor de G derivado.'),
 dict(item='Não-troca e w_i constante',status='INPUT',provider='ChatgptAudit.FLRW.SectorFluid',condition='H_nx é campo HasDerivAt; w_i tem somente índice de setor.'),
 dict(item='Entropia diferencial modificada',status='INPUT',provider='ChatgptAudit.FLRW.HubbleHorizonInput',condition='differential_entropy é explícita. S=A/(4G Phi(t)) exige o termo de Phi-prime e não é equivalente em geral.'),
 dict(item='Fator total e fator setorial',status='REAL',provider='ChatgptAudit.FLRW.the_two_routes_differ',condition='Teorema condicional; densidade positiva, entalpia não negativa, H_nx onde aplicável. Nenhuma rota ratificada por esta entrega.'),
 dict(item='Unicidade Phi_flux',status='REAL',provider='ChatgptAudit.FLRW.the_entropy_factor_that_reproduces_the_sector_closure',condition='Entalpia total diferente de zero. No fluxo zero não há fator único.'),
 dict(item='Constante de integração',status='INPUT',provider='ChatgptAudit.FLRW.tgl_friedmann_zero_cosmological',condition='O caso sem constante exige H_zero_cosmological; o resultado geral mantém Lambda/C.'),
 dict(item='Lema3 global',status='OPEN',provider='ORDEM_012 §0 e B6(d)',condition='Nenhuma identificação local-global provada nesta ordem.'),
 dict(item='TGL-S versus TGL-L',status='OPEN',provider='ORDEM_012 B6(e); RhoPlusPClosure',condition='Fechamento perturbativo não construído e não escolhido pela bancada.'),
 dict(item='Valor físico de beta',status='INPUT',provider='TGLExt.TGLCoupling',condition='O kernel usa beta variável em(0,1); a forma alpha=beta/exp(1/2) não deriva CODATA. Runtime não foi executado.'),
 dict(item='Ângulo na métrica',status='REAL',provider='ChatgptAudit.FLRW.the_angle_reaches_the_metric',condition='Somente reescrita sin²(thetaMiguel beta)=beta; não acrescenta variável ou observável ao motor.')
]
data=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),schema_version=1,
 external_known_theorems=external,scope=scope,changes_gate=False,implements_runtime=False,chooses_route=False,
 untampered_runtime_fields=['gpf_H3_local_horizon_equilibrium_discharged','gpi_H3_horizon_data_produced','qgf_continuous_modular_realization_constructed'],
 correction_providers=['ChatgptAudit.FLRW.radius_free_flux_consequence','ChatgptAudit.FLRW.variable_entropy_derivative','ChatgptAudit.FLRW.variable_factor_first_equation_defect','ChatgptAudit.FLRW.nonzero_flux_support_does_not_characterize_equality','ChatgptAudit.FLRW.zero_flux_has_no_unique_factor'],
 integration_note='Proposta aditiva para EXTERNAL_KNOWN_THEOREMS e tabela de estatutos; não instalada. Declarações antigas da lista não foram revalidadas ou removidas. O escopo importa hipóteses, não anuncia confirmação física.')
assert len(external)==4 and len({x['name'] for x in external})==4
assert all(x['imported_into_witness'] is False and x['exact_role'] and x['verified_url'].startswith('https://') for x in external)
assert all(x['status'] in {'IMPORTED','INPUT','REAL','OPEN'} for x in scope)
put(R/'PROPOSTA_EXTERNAL_KNOWN_THEOREMS_B6.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
ficha=json.loads((R/'REAPROVEITAMENTO_B6.json').read_text(encoding='utf8'))
names=[]
for row in ficha['providers']:
    n=row['name']
    prefix='TGLExt.' if 'TheImportedEquilibrium' in row['path'] else 'TGL.AreaScale.' if 'AreaScale' in row['path'] else 'ChatgptAudit.FLRW.'
    names.append(dict(kind='structure' if n in ['SectorFluid','HubbleHorizonInput'] else 'theorem',name=prefix+n,source=row['path']))
put(R/'ALVOS_B6.json',json.dumps(names,ensure_ascii=False,indent=2).encode('utf8'))
auditor='import TGLExt.TheAngleReachesTheMetric\nimport TGLExt.TheImportedEquilibrium\nimport TGL.AreaScale\n\n'
auditor+='\n'.join('#check '+x['name']+'\n#print axioms '+x['name'] for x in names)+'\n'
put(R/'kernel/TGLExt/AuditPassageScope.lean',auditor.encode('utf8'))
s=(R/'run_b5_lake.py').read_text(encoding='utf8').replace('B5','B6').replace("['TheAngleReachesTheMetric','AuditMetricAngle']","['AuditPassageScope']").replace('TGLExt.TheAngleReachesTheMetric','TGLExt.AuditPassageScope').replace('error: TGLExt/TheAngle','error: TGLExt/AuditPassageScope').replace("('TheAngleReaches' in line or 'AuditMetricAngle' in line)","'AuditPassageScope' in line")
put(R/'run_b6_lake.py',s.encode('utf8'))
put(R/'VALIDACAO_DOCUMENTAL_B6.json',json.dumps(dict(timestamp=data['timestamp'],proposal=pin(R/'PROPOSTA_EXTERNAL_KNOWN_THEOREMS_B6.json'),entries=4,all_imported_into_witness_false=True,all_statuses_typed=True,changes_gate=False,implements_runtime=False,chooses_route=False),ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(entries=4,scope_rows=len(scope),audit_existing_names=len(names))))
