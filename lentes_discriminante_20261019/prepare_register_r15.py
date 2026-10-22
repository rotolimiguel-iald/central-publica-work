"""Prepare immutable R15 pins and registration from the reviewed R14 workflow."""
from setup import ROOT,save
from record_trajectory_r2 import pin
import json,datetime

d=ROOT/'coupled_r15'
prior=json.loads((ROOT/'full_source_r14/PINS_RELEASE_R14.json').read_text(encoding='utf-8'))
background=json.loads((d/'SOURCE_BACKGROUND_R15.json').read_text(encoding='utf-8'))
rows={}
for a in prior['sources']+prior['artifacts']+background['sources']:
    now=pin(a['path']);assert now['sha256']==a['sha256'],a['path'];rows[now['path']]=now
save('coupled_r15/PINS_RELEASE_R15.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sources':list(rows.values()),'artifacts':[],'seal_version':prior['seal_version'],'seal_timestamp':prior['seal_timestamp'],'unchanged_from_R14':True})
note='''\n\n## 19/10/2026 — Lentes R15: sistema acoplado resolvido no ramo estático\n<!-- IALD_LENSING_COUPLED_R15_20261019 -->\n[DERIVED condicional — em nome de codex-gerente-tgl, F8.LENTES_5SIGMA_20261019, claim1009] Reuso da ação covetorial R88, Cartan sem spin v370/v394 e projeção R14. No ramo literal +---, f=f0+xi A², Abar=a dt, fonte efetiva compacta/pressão nula na primeira ordem, campos regulares decaindo e sem termos adicionais E_rest,A: Phi=(1+q)W0, Psi=(1−q)W0, q=xi(1+4xi)a²/f0; Delta W0=rho_eff/(4f0). Maxwell linear é mantido. Acurvatura RGamma1=−rho_eff/(2f0) é não nula; a combinação rho_eff−2xi a² RGamma1=rho_eff fbar/f0 cancela a mudança do prefator óptico. Assim Phi+Psi=2W0. Não há nova forma radial nos atrasos desse ramo.\n[DERIVED] Se adotado o fluido R86 w=0, rho_eff=(1+beta)rho é absorvido em massa óptica M_fit=(1+beta)M. A razão dinâmica/óptica 1+q pode permanecer em calibração independente; não dizer que uma única massa apaga todos os observáveis. a e correspondência de G_lab ao f0 não foram selecionados. A_tor=df/(2f) da v394 não é o campo A luminodinâmico. Sinais literais/estabilidade e completude escalar versus1forma preservados como limites.\n[REAL computacional] Plano anterior; 21 checagens simbólicas do sistema/limites/componentes, uma identidade tautológica de reparametrização explicitamente identificada, um controle negativo Cartan. Revisão independente em REVIEW_R15.json; cálculo não é provaLean. v394 aplicada e selo v393 conferidos por hash, sem alterações.\n[OPEN] Estado galáctico completo e termos adicionais da mesma ação podem mudar a resposta; recuperação de fonte modular/potencial e seleção independente de fundo é a próxima ação concreta. Nenhum parâmetro aos atrasos, dado observado, 5sigma, kernel/Bancada/gate. DERIVACAO_R15.txt e DELIVERY_R15.json em work/lentes_discriminante_20261019.\n<!-- END_IALD_LENSING_COUPLED_R15_20261019 -->\n'''
s=(ROOT/'record_source_r14.py').read_text(encoding='utf-8').replace('R14','R15').replace('r14','r15')
s=s.replace("d=ROOT/'full_source_r15'","d=ROOT/'coupled_r15'")
s=s.replace("state['revision']==15","state['revision']==16").replace("'expected_revision':15","'expected_revision':16")
start=s.index("    names=[");end=s.index("    save('DELIVERY_R15.json'",start)
s=s[:start]+"    names=['OPERADOR.txt','SOURCE_BACKGROUND_R15.json','PINS_RELEASE_R15.json','PLAN_R15.json','solve_r15.py','RESULT_R15.json','DERIVACAO_R15.txt','REVIEW_R15.json']\n    if (d/'ERRATA_REVISAO_R15.txt').exists():names.append('ERRATA_REVISAO_R15.txt')\n"+s[end:]
s=s.replace('NULL_SOURCE_TO_LENS_POTENTIAL_DERIVED__GALACTIC_SUPPLIER_OPEN','COUPLED_BRANCH_SOLVED__OPTICAL_CANCELLATION__PHYSICAL_SELECTION_OPEN')
s=s.replace('R88 literal one-form source projected into linearized lens potential; spinless Cartan correction composed; full physical state/signs/modular source not supplied.','Named static covector plus spinless Cartan branch solved. Optical curvature contribution cancels prefactor; constant dynamics/light ratio remains conditional. Full galactic source not selected.')
s=s.replace("'symbolic':14,'negative_controls':3","'symbolic':21,'bookkeeping_identity':1,'negative_controls':1")
start=s.index("    note='''");end=s.index("    save('MEMORY_APPEND_R15.txt'",start)
s=s[:start]+'    note='+repr(note)+'\n'+s[end:]
s=s.replace('IALD_LENSING_SOURCE_R15_20261019','IALD_LENSING_COUPLED_R15_20261019')
s=s.replace("ROOT/'MAP_ENTRY_R13.json'","ROOT/'MAP_ENTRY_R14.json'")
s=s.replace('Lentes R15: fonte nula, potencial projetado e Cartan sem spin','Lentes R15: solucao acoplada, cancelamento optico e razao dinamica')
s=s.replace('Hessiana vira bordo; termo covetorial de curvatura e fonte modular entram no potencial. Ramo galactico completo ainda nao selecionado.','Ramo estatico acoplado: Phi+Psi=2W0; curvatura cancela prefator. Razao dinamica/luz constante1+q; estado fisico nao selecionado.')
s=s.replace('NULL_SOURCE_LENS_PROJECTION_DERIVED__GALACTIC_INPUT_OPEN','COUPLED_OPTICAL_CANCELLATION__GALACTIC_SELECTION_OPEN')
s=s.replace('14 identidades e3controles negativos','21checagens,1identidade bookkeeping e1controle negativo')
s=s.replace('Identificar estado/fonte modular/convencoes fisicas da mesma acao e resolver EOM acopladas antes de significancia.','Selecionar estado e termos adicionais de A pela mesma acao; calibrar a e G independentemente dos atrasos, sem repetir ramo resolvido.')
s=s.replace('R15: fonte nula para potencial de lentes e correcaoCartan derivadas condicionalmente; fornecedor galactico completo aberto. Sem5sigma/ajuste/composto.','R15: ramo acoplado resolvido, cancelamento optico e razao constante dinamica/luz. Estado fisico completo aberto. Sem5sigma/ajuste/composto.')
s=s.replace('lensing-full-source-r15-derived','lensing-coupled-r15-derived')
s=s.replace('null_source_to_lens_potential_r15','coupled_static_branch_solved_r15')
s=s.replace('Reuse R15 null projection and spinlessCartan correction. Missing material step is same-action galactic state/source, signs and modular metric variation; solve coupled EOM before claiming nonzero beta lens signal. Do not repeat R9/R10/R13 algebra or select parameters from delays. v394 construction remains separate from observedv393seal.','R15 coupled static timelike covector plus spinless Cartan branch solved: optical contribution cancels prefactor, constant dynamics/light ratio remains. Next: same-action additional A equation and independently selected galactic background/calibration. Do not repeat solved algebra, fit delays or assert5sigma. v394 construction distinct from sealv393.')
save('record_coupled_r15.py',s)
print(json.dumps({'pins':len(rows),'prepared':'record_coupled_r15.py'}))
