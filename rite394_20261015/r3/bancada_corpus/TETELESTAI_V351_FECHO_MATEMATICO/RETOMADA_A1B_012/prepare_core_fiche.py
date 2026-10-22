from pathlib import Path
import datetime,hashlib,json,os,re
R=Path(__file__).resolve().parent;K=R/'k'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists(),p
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b and b;os.replace(t,p)
specs=[('V351ScalarImaginaryLeftTransport','matrixUnit_imaginaryPower_left_scaling'),('V351ScalarImaginaryLeftTransport','scalarTomitaImaginaryPower_regular_left_commutes'),('V350MatrixUnitRightSquare','matrixUnit_rightCore_star'),('V350MatrixUnitRightSquare','localEigenvalue_reverse_log'),('V350RegularTowerRepresentation','regular_covariance'),('V350RegularTowerRepresentation','regular_unitary'),('ModularFlowAlgebra','modularConjugation_local'),('ModularFlowSpectrum','flowLevel_single'),('V350LocalBasePolarCommutation','localBaseCore'),('V350LevelExpectationStrongLimit','represented_levelExpectation_strong_tendsto'),('V350BasePolarStrongLimit','commute_of_strong_tendsto'),('V350ScalarGNSGeneratorTransport','scalarGNS_commutation_from_generators')]
providers=[]
for mod,name in specs:
 p=K/'TGLExt'/f'{mod}.lean';s=p.read_text(encoding='utf8')
 m=re.search(r'^(?:theorem|def) '+name+r'\b[\s\S]*?(?= :=| where| :=\n)',s,re.M);assert m,name
 providers.append(dict(name=name,file=pin(p),line=s[:m.start()].count('\n')+1,statement=m[0],decision='REUSAR',status='DEV_NOT_YET_REVIEWED' if mod=='V351ScalarImaginaryLeftTransport' else 'EXISTING_SUPPLIER'))
target='''For all SiteProfile P, t : Real, A : (regularCoreAlgebra P).toStarSubalgebra, x : ScalarGNSHilbert P:
scalarTomitaImaginaryPower P t (scalarGNSRepresentation P A x) =
scalarGNSRepresentation P (regularRightCoreElement P t * A * star (regularRightCoreElement P t)) (scalarTomitaImaginaryPower P t x).
No additional covariance, density, normality, or trace hypothesis. This proves an operator relation on the whole actual represented core, not yet a faithful normal semifinite trace.'''
method='Use ordinary matrix-unit phase by reversing indices in the left-adjoint theorem. Compare U_t with V_t=pi(lambda_t) via D=V_t* U_t (star on V_t). D commutes with matrix units, hence with finite matrices; pass to the base by the existing represented strong limit; use existing generator-to-core commutation; cancel V_t with its adjoint. No new representation, flow, GNS, weight, normality or density construction.'
search=R/'BUSCAS_A1B_ACAO_CORE.json';data=json.loads(search.read_text(encoding='utf8'));assert all(s['returncode'] in (0,1) and not s['stderr_bytes'] for s in data['searches'])
stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,decision='ADAPTAR',consumer=dict(file=str(R.parent/'LACUNAS_A1.md'),line=25,name='regular_dual_weight_modular_implementation',delivery=str(R.parent.parent/'TUNEL/DO_CHATGPT/ENTREGA_011_A1_potencias_imaginarias_mesmo_tomita.md'),delivery_line=69),exact_target=target,method=method,providers=providers,search=pin(search),search_results='Existing strong-limit and generator transport found. No combined core conjugation found in searched files; acervo exact-name query returned zero in 13608 indexed files; no universal absence claim.',remaining=['Extended-weight/trace type bridge','Positive nonsingular selfadjoint affiliated regular generator with imaginary powers equal to the actual regular unitaries','Inverse-generator perturbation yielding a faithful normal semifinite trace and dual scaling'],not_claimed=['Gate movement','KMS identification by name only','Complete A1(b)','Canonical incorporation'])
put(R/'REAPROVEITAMENTO_A1B_ACAO_CORE.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior ao consumidor da ação em todo o core]\n\n# A1(b): ação modular na mesma representação\n\n'+stamp+'\n\nConsumidor: `regular_dual_weight_modular_implementation`, LACUNAS_A1.md:25. A entrega anterior de potências imaginárias, linha69, já nomeia este próximo uso.\n\n```text\n'+target+'\n```\n\n'+method+'\n\n## Fornecedores e tipos\n\n'
for p in providers:s+=f"`{p['file']['path']}:{p['line']}` — `{p['file']['sha256']}` — {p['status']}\n\n```lean\n{p['statement']}\n```\n\n"
s+='## Buscas e critério\n\nSeis modalidades em BUSCAS_A1B_ACAO_CORE.json: kernel, notas, entregas/outras bancadas, árvore, TOE, índice do acervo. As buscas acharam os fornecedores acima, e não um teorema com o tipo final nos recortes consultados. O índice retornou zero em13608arquivos; isso não demonstra ausência fora do índice.\n\nOs dois lemas à esquerda estão em desenvolvimento aceito pelo compilador, ainda não em entrega auditada. São dependências explicitamente pendentes. A aceitação do novo consumidor exige Lake isolado, axiomas no trio, controles negativos pertinentes e revisão independente. Depois dele, a construção do traço continua aberta nos endereços nomeados no JSON. Nenhuma nova camada de GNS, fluxo, normalidade ou peso é autorizada por esta ficha.\n'
put(R/'REAPROVEITAMENTO_A1B_ACAO_CORE.md',s.encode('utf8'))
print(json.dumps(dict(fiche=True,providers=len(providers),target='whole_core_conjugation')))
