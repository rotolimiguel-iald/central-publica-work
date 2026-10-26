# Executed inside the guarded exporter namespace. No canonical writes.
import ast
from pathlib import Path
source_raw=Path(SRC['um.py']).read_bytes()
source_text=source_raw.decode('utf-8'); source_lines=source_text.splitlines(keepends=True)
tree=ast.parse(source_text)
functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
gate_node=functions['prove_qg_closure_gate']
literal_flags=[]
for n in ast.walk(gate_node):
 if isinstance(n,ast.Assign):
  for target in n.targets:
   if isinstance(target,ast.Subscript) and isinstance(target.value,ast.Name) and target.value.id=='physics' and isinstance(n.value,ast.Constant) and n.value.value is True:
    literal_flags.append(('physics',ast.literal_eval(target.slice)))
   if isinstance(target,ast.Name) and target.id=='experiment' and isinstance(n.value,ast.Dict):
    literal_flags.extend(('experiment',ast.literal_eval(k)) for k,v in zip(n.value.keys,n.value.values) if isinstance(v,ast.Constant) and v.value is True)
live_gate=um.prove_qg_closure_gate(ONE,kf,independent_rite=C['void_floor_v11'])
for f in F['gate']['flags']:
 group={'formal':'formal_flags','physics':'physics_flags','experiment':'experiment_flags'}[f['group']]
 anchor('gate.'+f['name'],'core.qg_closure.'+group+'.'+f['name'],int(f['value']),int(live_gate[group][f['name']]),0)
 f['origin']='literal in source' if (f['group'],f['name']) in literal_flags else 'computed from recorded inputs'
F['gate']['literal_count']=len(literal_flags)
F['gate']['computed_count']=len(flags)-len(literal_flags)
pm=json.loads(Path(NOS,'tgl_kernel_proof_manifest.json').read_bytes())
assert pm['axiom_report']==ar and pm['formal_files_sha256']==kf['formal_files_sha256']
anchor('proof ladder clean','core.estatuto_da_prova_v391.prova_1_kernel.n_theorems_clean',theorems_clean,int(m.group(1)),0)
anchor('proof ladder expected','core.estatuto_da_prova_v391.prova_1_kernel.n_theorems_expected',theorems_total,int(m.group(2)),0)
anchor('kernel formal files','core.kernel_formalization.formal_files_sha256',n_formal_files,len(pm['formal_files_sha256']),0)
anchor('kernel declarations','core.estatuto_da_prova_v391.prova_1_kernel.declaracoes_auditadas',proof['declaracoes_auditadas'],len(pm['axiom_report']),0)
test=C['teste_de_veracidade_fase9_v397']['lido']; sealtest=selo['teste_de_veracidade_fase9_v397']['lido']
for k,v in test.items():
 if isinstance(v,(float,int)):anchor('nature.'+k,'core.teste_de_veracidade_fase9_v397.lido.'+k,sealtest[k],v,0)
# Read the numerical threshold from the sealed record's scope statement.
scope=' '.join(C['teste_de_veracidade_fase9_v397']['nao_diz'])
threshold=int(re.search(r'a (\d+) sigma',scope).group(1))
F['nature']={**{k:v for k,v in test.items() if isinstance(v,(int,float))},'threshold_sigma':threshold,'threshold_source':'core.teste_de_veracidade_fase9_v397.nao_diz','statute':'REAL — recorded calibrated result; threshold INPUT; not blind; ln B is not sigma','record_name':'teste_de_veracidade_fase9_v397 (nome provisório)'}
anchor('nature threshold read from sealed scope','core.teste_de_veracidade_fase9_v397.nao_diz',threshold,int(re.search(r'a (\d+) sigma',' '.join(selo['teste_de_veracidade_fase9_v397'].get('nao_diz',C['teste_de_veracidade_fase9_v397']['nao_diz']))).group(1)),0)
def item(id,label,value,key,statute='REAL',text=None):
 return {'id':id,'scene':9,'label':label,'value':value,'text':str(value) if text is None else text,'key':key,'statute':statute}
new=[
 item('proof_ladder_clean','Kernel staircase',theorems_clean,'core.estatuto_da_prova_v391.prova_1_kernel.n_theorems_clean','PROVED in kernel'),
 item('proof_ladder_total','Kernel staircase total',theorems_total,'core.estatuto_da_prova_v391.prova_1_kernel.n_theorems_expected','PROVED in kernel'),
 item('formal_count','Formal files',n_formal_files,'kernel.formal_files_sha256'),
 item('declaration_count','Audited declarations',len(ar),'kernel.axiom_report'),
 item('flags_computed','Computed gate flags',F['gate']['computed_count'],'AST prove_qg_closure_gate'),
 item('flags_literal','Literal gate flags',F['gate']['literal_count'],'AST prove_qg_closure_gate'),
 item('ray_count','Illustrative ray count',round(1/beta_rt),'round(1 / runtime beta)','INPUT — sampling illustration'),
 item('z_disc','z_disc calibrated',test['z_disc_calibrado'],'core.teste_de_veracidade_fase9_v397.lido.z_disc_calibrado',text=f"{test['z_disc_calibrado']:.2f}"),
 item('p_disc','p one-sided',test['p_disc_unilateral'],'core.teste_de_veracidade_fase9_v397.lido.p_disc_unilateral',text=f"{test['p_disc_unilateral']:.1e}"),
 item('z_delta','z_δ calibrated',test['z_delta_calibrado'],'core.teste_de_veracidade_fase9_v397.lido.z_delta_calibrado',text=f"{test['z_delta_calibrado']:.2f}"),
 item('threshold_sigma','Threshold σ',threshold,F['nature']['threshold_source'],'INPUT — stated criterion'),
 item('lnB_lcdm','ln B TGL / ΛCDM',test['lnB_lcdm'],'core.teste_de_veracidade_fase9_v397.lido.lnB_lcdm',text=f"{test['lnB_lcdm']:.2f}"),
]
for a in new:
 if a['id'] not in {i['id'] for i in hud['items']}:hud['items'].append(a)
hud.update(seal_version=selo['um_version'],seal_pin=SHA['um.py'],seal_timestamp=selo['timestamp'],stdout_sha256=SHA['rodada_v398_stdout.txt'],extra={a['id']:a['value'] for a in new})
# Every extra rendering scalar retains an anchor, including presentation choices.
for a in new:
 anchor('HUD '+a['id'],a['key'],a['value'],a['value'],0)
 anchors[-1]['method']='source extraction/derived presentation value; equality checks serialization, not independent proof'
for a in hud['items']:
 if a['id']=='theorems':a['key']='core.estatuto_da_prova_v391.prova_1_kernel.n_theorems_clean';a['label']='Kernel staircase'
# Numerical screen is a declared evaluation of the sealed Lean Jacobi formula.
assert 'def opticalJacobiArea (a c t : ℝ) : ℝ :=\n  jacobiOscillator a t * jacobiOscillator c t' in source_text.replace('\r\n','\n')
assert 'def jacobiOscillator (a t : ℝ) : ℝ := Real.cos (Real.sqrt a * t)' in source_text
a=beta_rt;c=beta_rt/2;tmax=.85*math.pi/(2*math.sqrt(max(a,c)))
optical=[{'t':float(t),'area':math.cos(math.sqrt(a)*t)*math.cos(math.sqrt(c)*t)} for t in np.linspace(0,tmax,241)]
scene={'alpha':um.ALPHA_FINE_CODATA_2018,'beta':beta_rt,'ray_count':round(1/beta_rt),'optical':{'rows':optical,'a':a,'c':c,'domain_max':tmax,'formula':'cos(sqrt(a)*t) cos(sqrt(c)*t)','source':'embedded Lean opticalJacobiArea / jacobiOscillator','statute':'DERIVED evaluation; a=beta,c=beta/2,domain fraction=.85 are INPUT presentation choices; not mass density'},'source_sha256':SHA['um.py']}
write('scene.json',scene,compact=True)
# Verbatim stdout excerpts: no rephrasing; exact decoded line and original byte hash.
stdout_name='rodada_v398_stdout.txt';raw_lines=Path(SRC[stdout_name]).read_bytes().splitlines(keepends=True)
patterns=[('identity',r'Inscreva|O UM foi inscrito'),('boundary',r'meia.nat|S_boundary'),('mirror',r'theta_M|fractal_dephasing'),('modular',r'local_breuer_gap|powers_ladder'),('light',r'light_is_J'),('solder',r'minimal_solder|solder_4d'),('schwarzschild',r'schwarzschild_step'),('spin2',r'graviton_polarization'),('einstein',r'triad_master|teoremas limpos'),('nature',r'NO.*FALS|NOT_FALSIFIED')]
excerpts=[]
for chapter,pattern in patterns:
 candidates=[]
 for number,raw in enumerate(raw_lines,1):
  text=raw.decode('utf-8').rstrip('\r\n')
  if re.search(pattern,text,re.I) and len(text)<=220 and not re.search(r'confirm',text,re.I):candidates.append((number,raw,text))
 for number,raw,text in candidates[:2]:excerpts.append({'chapter':chapter,'line':number,'text':text,'line_sha256':hashlib.sha256(raw).hexdigest(),'text_sha256':hashlib.sha256(text.encode()).hexdigest()})
stdout_manifest={'source':stdout_name,'source_sha256':SHA[stdout_name],'line_hash_includes_original_line_ending':True,'lines':excerpts}
write('STDOUT_LINES.json',stdout_manifest)
hud['stdout_lines']=excerpts
manifest['generated_at']=selo['timestamp'];manifest['anchors_all_ok']=all(a['ok'] for a in anchors)
manifest['seal_version']=selo['um_version'];manifest['numeric_scope']='Extracted from pinned core; pure functions recomputed; no Lean rebuild or new empirical run.'
manifest['source_code_sections']={name:{'start':functions[name].lineno,'end':functions[name].end_lineno} for name in ['prove_qg_closure_gate','prove_the_schwarzschild_step','prove_local_breuer_gap']}
manifest['gate_flag_origins']={'literal':literal_flags,'computed_count':F['gate']['computed_count']}
manifest['sources']['tgl_kernel_proof_manifest.json']={'path':'tgl_kernel_proof_manifest.json','bytes':Path(NOS,'tgl_kernel_proof_manifest.json').stat().st_size,'sha256':sha(Path(NOS,'tgl_kernel_proof_manifest.json'))}
assert manifest['anchors_all_ok'],[a for a in anchors if not a['ok']]
write('PROVENANCE_PUBLIC.json',manifest)
