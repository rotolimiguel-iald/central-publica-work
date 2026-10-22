from pathlib import Path
import datetime,hashlib,json,os,re,subprocess
R=Path(__file__).resolve().parent;K=R/'k';CHAT=R.parent.parent
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists(),p
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
search=R/'BUSCAS_A1B_ABSORCAO_REGULAR.json';data=json.loads(search.read_text(encoding='utf8'))
assert all(r['returncode'] in (0,1) and r['stderr_bytes']==0 for r in data['searches'])
cmd=['rg','-l','regularFlowAbsorptionUnitary|regularFlowField|regularUnitary_shift_conjugate',str(CHAT),'-g','*.lean','-g','!**/.lake/**','-g','!**/attempts/**','-g','!*.bak*']
p=subprocess.run(cmd,capture_output=True)
if p.returncode not in (0,1) or p.stderr:
 stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
 put(R/('search_absorption/other_failure_'+stamp+'.stdout.txt'),p.stdout)
 put(R/('search_absorption/other_failure_'+stamp+'.stderr.txt'),p.stderr)
 raise RuntimeError('Search incomplete; stdout/stderr preserved under search_absorption')
put(R/'search_absorption/other_workbenches.stdout.txt',p.stdout);put(R/'search_absorption/other_workbenches.stderr.txt',p.stderr)
put(R/'BUSCA_A1B_ABSORCAO_OUTRAS.json',json.dumps(dict(command=cmd,returncode=p.returncode,stdout_bytes=len(p.stdout),stderr_bytes=len(p.stderr)),indent=2).encode('utf8'))
specs=[('V350OperatorFieldAlgebra','operatorFieldLift_star'),('V350OperatorFieldAlgebra','operatorFieldLift_mul'),('V350OperatorFieldAlgebra','operatorFieldLift_constant'),('V350StrongOperatorField','operatorFieldLift_ae'),('V350RegularTowerRepresentation','regularUnitary'),('V350L2Translation','shift_ae'),('TheModularFlowIsAHorizon','modularFlowCLM_mul'),('TheModularFlowIsAHorizon','modularFlowCLM_star'),('V350RegularTowerRepresentation','modularFlowCLM_isometry')]
providers=[]
for mod,name in specs:
 sfile=K/'TGLExt'/f'{mod}.lean';s=sfile.read_text(encoding='utf8');m=re.search(r'^(?:def|theorem) '+name+r'\b[\s\S]*?(?= :=| where)',s,re.M);assert m,name
 providers.append(dict(name=name,file=pin(sfile),line=s[:m.start()].count('\n')+1,statement=m[0],decision='REUSAR'))
target='''Build W : unitary (RegularHilbert (TowerHilbert P) →L[Complex] RegularHilbert (TowerHilbert P)) from the existing field x ↦ modularFlowCLM P x. For every P,t, prove W.val * shift t * star W.val = regularUnitary P t. Use operatorFieldLift; prove its adjoint/group/zero identities with field argument scale a only to supply W and its inverse. No new L2, Fourier, modular flow, or GNS. W need not belong to the regular core; do not assert this.'''
stamp=datetime.datetime.now().astimezone().isoformat()
d=dict(timestamp=stamp,status='OPEN__FICHE_BEFORE_REGULAR_ABSORPTION',decision='ADAPTAR',consumer=dict(name='regular_unitary_positive_generator',path=str(R.parent/'LACUNAS_A1.md'),line=31,route=pin(R/'ROTA_GERADOR_REGULAR_A1B.md')),exact_target=target,providers=providers,searches=[pin(search),pin(R/'BUSCA_A1B_ABSORCAO_OUTRAS.json')],current_scope='Two definitions and four theorem candidates. The auxiliary real argument a indexes field composition; the actual unitary W uses a=1, its inverse a=-1. It is not a new physical coupling or a choice of beta.',not_claimed=['positive generator','affiliation of W to N','trace','completed A1(b)','gate movement'])
put(R/'REAPROVEITAMENTO_A1B_ABSORCAO.json',json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'))
s='[OPEN — ficha anterior à equivalência do grupo regular com a translação]\n\n# A1(b): absorção do fluxo pela coordenada regular\n\n'+stamp+'\n\nConsumidor: `regular_unitary_positive_generator`, LACUNAS_A1.md:31. A rota explícita está em ROTA_GERADOR_REGULAR_A1B.\n\n```text\n'+target+'\n```\n\nO campo é uma instanciação do operatorFieldLift já existente. a é argumento auxiliar da composição de campos; não é parâmetro físico, nem beta. Duas definições (família, unitário) e quatro lemas usados na construção e no consumo. W não é presumido elemento de N. Sem declarar Fourier, traço ou gerador como construídos.\n\n## Fornecedores\n\n'
for q in providers:s+=f"`{q['file']['path']}:{q['line']}` — `{q['file']['sha256']}`\n\n```lean\n{q['statement']}\n```\n\n"
s+='## Buscas\n\nSeis modalidades e recorte adicional em outras bancadas nos JSONs pinados. Foram localizados os fornecedores genéricos e o alvo nomeado nas entregas, não a identidade completa nos recortes consultados. O alcance do índice não é todo o computador. Nenhum fornecedor antigo será alterado. A aceitação exige compilação própria, axiomas e revisão, em entrega separada dos5lemas de ação no core.\n'
put(R/'REAPROVEITAMENTO_A1B_ABSORCAO.md',s.encode('utf8'));print(json.dumps(dict(fiche=True,providers=len(providers),other_matches=len(p.stdout))))
