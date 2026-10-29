"""Extract exact source bytes; execute only dependency-closed numerical functions.
No import/execution of the original um.py. Writes only replay outputs and replay-trust.mjs.
"""
import argparse, ast, builtins, hashlib, json, math, pathlib, symtable, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
ROOTS = ['fractal_dephasing_principle', 'prove_smatrix_closure', 'prove_solder_4d',
         'prove_local_breuer_gap', 'prove_minimal_solder', 'prove_the_schwarzschild_step',
         'prove_graviton_polarization', 'prove_the_TGL_identity_equation', 'prove_light_is_J',
         'prove_powers_ladder']
ALLOWED = set(ROOTS + ['SEALED_CODATA_ALPHA', '_QG_CERTIFICATE_FLAGS',
    'evaluate_quantum_gravity_closure', '_fam_dag', '_clo_locks_superops', '_verb_L',
    '_expm', 'construct_family_projection_from_locks'])
# Absolute tolerances: numerical shadows, not thresholds for scientific credit.
ANCHORS = {
 'omega_I':1e-15, 'HALF':1e-15, 'meia_nat_residual':1e-15, 'S_boundary':1e-15,
 'SQRT_E':1e-14, 'theta_M_rad':1e-12, 'theta_M_deg':1e-10,
 'fractal_dephasing.leak_sin2_thetaM':1e-15,
 'fractal_dephasing.leak_equals_beta_residual':1e-15,
 'smatrix_closure.tau_reflected':1e-15, 'smatrix_closure.tau_transmitted':1e-15,
 'smatrix_closure.tr_norm_eq_sqrt_1_minus_beta':1e-15,
 'smatrix_closure.r_UtI':1e-12, 'smatrix_closure.r_unit':1e-14,
 'solder_4d.wigner_rotation_norm':1e-12,
 'solder_4d.residuals.marca_KK_eq_menosJ3':1e-12,
 'local_breuer_gap.hminus_gap_second_eig':1e-9,
 'local_breuer_gap.zero_mode_weight_quadrature':1e-12,
 'local_breuer_gap.zero_mode_overlap_sech':1e-9,
 'local_breuer_gap.hplus_floor':1e-9,
 'minimal_solder.R_recovered':1e-12, 'minimal_solder.plaquette_order':1e-6,
 'schwarzschild_step.residual_Et':1e-12, 'schwarzschild_step.residual_Er':1e-12,
 'graviton_polarization.residuals.helicity_plus':1e-15,
 'graviton_polarization.values.boundary_deviation_norm_sq':1e-12,
 'graviton_polarization.values.beta_runtime':1e-17,
 'the_TGL_identity_equation.member_true_max_residual':1e-15,
 'the_TGL_identity_equation.member_false_min_residual':1e-15,
 'light_is_J.values.crossing_resid':1e-15, 'light_is_J.values.inversion_resid':1e-15,
 'light_is_J.values.identity_remains_resid':1e-15,
 'powers_ladder.values.ratio_block':1e-15, 'powers_ladder.values.ratio_chain_N8':1e-28,
}
def digest(b): return hashlib.sha256(b).hexdigest()
def encoded(x): return (json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)+'\n').encode('utf8')
def write(p,b):
 if p.exists() and p.read_bytes()!=b:
  import time
  old=p.read_bytes(); backup=p.with_name(p.name+'.bak_'+str(time.time_ns()));backup.write_bytes(old);assert backup.read_bytes()==old
 p.parent.mkdir(parents=True,exist_ok=True)
 t=p.with_name(p.name+'.tmp');t.write_bytes(b)
 if t.read_bytes()!=b: raise RuntimeError('write verification failed')
 t.replace(p)
def get(d,path):
 for k in path.split('.'): d=d[k]
 return d
def global_names(st):
 out={s.get_name() for s in st.get_symbols() if s.is_global() and s.is_referenced()}
 for c in st.get_children(): out |= global_names(c)
 return out
def extract(raw):
 text=raw.decode('utf-8-sig');tree=ast.parse(text);lines=raw.splitlines(keepends=True)
 defs={};imports=[]
 for n in tree.body:
  if isinstance(n,ast.FunctionDef): defs[n.name]=n
  elif isinstance(n,(ast.Assign,ast.AnnAssign)):
   for t in (n.targets if isinstance(n,ast.Assign) else [n.target]):
    if isinstance(t,ast.Name): defs[t.id]=n
  elif isinstance(n,ast.Import) and ast.unparse(n) in ('import math','import numpy as np'): imports.append(n)
 selected={};pending=ROOTS[:]
 while pending:
  name=pending.pop()
  if name in selected: continue
  if name not in ALLOWED: raise RuntimeError('Unreviewed dependency: '+name)
  n=defs[name];selected[name]=n
  chunk=b''.join(lines[n.lineno-1:n.end_lineno]).decode('utf8')
  deps=global_names(symtable.symtable(chunk,'source','exec'))-set(dir(builtins))-{'np','math',name}
  for dep in deps:
   if dep not in defs: raise RuntimeError('Unresolved dependency: '+dep)
   pending.append(dep)
 nodes=[(ast.unparse(n),n) for n in imports]+list(selected.items())
 nodes.sort(key=lambda pair:pair[1].lineno)
 output=b'';ranges=[]
 for name,n in nodes:
  if isinstance(n,ast.FunctionDef) and n.decorator_list: raise RuntimeError('Decorated function not admitted')
  piece=b''.join(lines[n.lineno-1:n.end_lineno]);start=len(output)
  output+=piece+b'\n'
  ranges.append({'name':name,'source_start_line':n.lineno,'source_end_line':n.end_lineno,
    'excerpt_byte_start':start,'excerpt_byte_end':start+len(piece),'sha256':digest(piece)})
 # Exact indented source block; run by a separately identified harness with `if True:`.
 run=defs['run_um'];first=run.body[1];stop=next(n for n in run.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='s_can' for t in n.targets))
 scalar=b''.join(lines[first.lineno-1:stop.end_lineno])
 return output,ranges,scalar,{'source_start_line':first.lineno,'source_end_line':stop.end_lineno,'sha256':digest(scalar)}
def build(source,hud,out):
 if not out.resolve().is_relative_to(ROOT/'replay'): raise ValueError('Output must remain in replay/')
 source=source.resolve();raw=source.read_bytes();seal_path=source.parent/'um_absoluto_selo.json';core_path=source.parent/'um_absoluto.json'
 seal_raw=seal_path.read_bytes();seal=json.loads(seal_raw);core_raw=core_path.read_bytes();core=json.loads(core_raw)['core']
 for name,data in [('um.py',raw),('um_absoluto.json',core_raw)]:
  if seal['sha256'][name]!=digest(data): raise ValueError('NOT_SEALED: '+name)
 excerpt,ranges,scalar,scalar_range=extract(raw)
 expected=[]
 for key,tol in ANCHORS.items():
  value=get(core,key)
  if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value): raise ValueError('Non-numeric anchor: '+key)
  expected.append({'key':'core.'+key,'value':value,'atol':tol})
 hud_raw=hud.read_bytes();h=json.loads(hud_raw)
 if h.get('seal_pin')!=digest(raw) or h.get('seal_version')!=seal['um_version'] or h.get('seal_timestamp')!=seal['timestamp']: raise ValueError('NOT_SEALED: HUD source identity')
 items=h.get('items')
 if not isinstance(items,list): raise ValueError('HUD items missing')
 if len({v['id'] for v in items})!=len(items): raise ValueError('Duplicate HUD id')
 lookup={x['key']:x for x in expected};matched=[];skipped=[]
 for item in items:
  key=item.get('key');anchor=lookup.get(key)
  if anchor:
   value=item['value']
   if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value) or abs(value-anchor['value'])>anchor['atol']: raise ValueError('NOT_SEALED HUD: '+str(key))
   matched.append({'id':item['id'],'key':key})
  else: skipped.append(item['id'])
 if len(matched)<20: raise ValueError('Fewer than 20 numerical HUD anchors')
 files={'um_nucleo_filme.py':excerpt,'um_scalar_excerpt.py':scalar,'anchors.json':encoded(expected),
        'replay_runner.py':(ROOT/'replay/replay_runner.py').read_bytes()}
 assets={}
 for name,data in files.items():
  write(out/name,data);assets[name]={'url':name,'sha256':digest(data),'bytes':len(data)}
 # HUD itself is fetched and hashed at runtime, not copied into recalculation inputs.
 import os
 assets['hud']={'url':os.path.relpath(hud,out).replace('\\','/'),'sha256':digest(hud_raw),'bytes':len(hud_raw)}
 vendor=json.loads((ROOT/'replay/PYODIDE_VENDOR.json').read_bytes())
 for f in vendor['files']:
  p=ROOT/'web/vendor/pyodide'/f['name']
  if digest(p.read_bytes())!=f['sha256']: raise ValueError('Vendor hash mismatch: '+f['name'])
 manifest={'schema':1,'engine':'EXACT_PYTHON_PYODIDE','status':'READY_FOR_INDEPENDENT_REVIEW',
  'source':{'name':'um.py','version':seal['um_version'],'sha256':digest(raw),'bytes':len(raw)},
  'seal':{'sha256':digest(seal_raw),'timestamp':seal['timestamp']},'core_sha256':digest(core_raw),
  'excerpt_ranges':ranges,'scalar_range':scalar_range,'roots':ROOTS,'assets':assets,
  'hud_compared':matched,'hud_documentary_only':skipped,'anchor_count':len(expected),
  'vendor':vendor,'vendor_url':os.path.relpath(ROOT/'web/vendor/pyodide',out).replace('\\','/')+'/',
  'worker_sha256':digest((pathlib.Path('C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\video_um\\delivery_v7\\web\\replay-worker.js')).read_bytes()),
  'scope':'Numerical shadows only; no Lean run, kernel approval or empirical credit. Documentary HUD fields are not recalculated.',
  'tolerance_policy':'Absolute tolerances inherited from exporter; powers chain 1e-28 prevents zero passing. No relative tolerance.'}
 mbytes=encoded(manifest);write(out/'replay-manifest.json',mbytes)
 if out.resolve()==(ROOT/'replay').resolve():
  trust='export const replayTrust = '+json.dumps({'manifestURL':'../replay/replay-manifest.json','sha256':digest(mbytes)},indent=2)+';\n'
  write(ROOT/'replay/replay-trust.mjs',trust.encode())
 return manifest
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',type=pathlib.Path,required=True);p.add_argument('--hud',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,default=ROOT/'replay');a=p.parse_args()
 try:
  m=build(a.source,a.hud,a.out);print(json.dumps({'status':m['status'],'anchors':m['anchor_count'],'hud_compared':len(m['hud_compared']),'vendor_bytes':m['vendor']['total_bytes']}))
 except Exception as e: print('NOT_SEALED: '+str(e),file=sys.stderr);sys.exit(1)
