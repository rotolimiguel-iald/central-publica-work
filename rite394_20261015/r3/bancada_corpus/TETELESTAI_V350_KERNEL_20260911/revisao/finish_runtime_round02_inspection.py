"""Read-only inspection of emitted artifacts; no author code is executed."""
import ast
import copy
import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V350_KERNEL_20260911')
OUT = ROOT/'revisao/runtime_seals_preliminary_20260913_100700_656494'
FORMAL = ROOT/'revisao/full_runtime_formal_stage_20260913_093418_886098/evidence.json'
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
pins = {}

def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        while b := f.read(4*1024*1024):
            h.update(b)
    return h.hexdigest()

def pin(p):
    return {'path':str(p), 'bytes':p.stat().st_size, 'sha256':digest(p),
            'mtime':datetime.datetime.fromtimestamp(p.stat().st_mtime).astimezone().isoformat()}

def capture(alias, p):
    raw = p.read_bytes()
    pins[alias] = pin(p)
    (OUT/('final_'+alias+p.suffix)).write_bytes(raw)
    return json.loads(raw) if p.suffix == '.json' else raw.decode('utf-8-sig')

current = capture('current', ROOT/'r/um_absoluto.json')
seal = capture('seal', ROOT/'r/um_absoluto_selo.json')
proof = capture('proof', ROOT/'r/tgl_kernel_proof_manifest.json')
process = capture('process', ROOT/'r/runtime_process_02.json')
stdout = capture('stdout', ROOT/'r/runtime_stdout_02.txt')
stage = capture('inputs_manifest', ROOT/'runtime_inputs_pending/manifest.json')
contract = capture('contract', ROOT/'CONTRATO_ATIVO_GATE_V350.json')
formal = json.loads(FORMAL.read_bytes())
baseline = json.loads((OUT/'baseline.json').read_bytes())
baseline_seal = json.loads((OUT/'baseline_seal.json').read_bytes())
core = current['core']
kf = core['kernel_formalization']
source = (ROOT/'um.py').read_text(encoding='utf-8')
tree = ast.parse(source)
assignments = {}
functions = {}
for n in tree.body:
    if isinstance(n, ast.Assign):
        for t in n.targets:
            if isinstance(t,ast.Name):
                try: assignments[t.id] = ast.literal_eval(n.value)
                except (ValueError,TypeError): pass
    elif isinstance(n,ast.FunctionDef): functions[n.name] = n

def axmap(txt):
    result, conflicts = {}, []
    pat = r"'([\w.']+)'\s+(?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)"
    for m in re.finditer(pat, txt):
        value = [s.strip() for s in (m.group(2) or '').split(',') if s.strip()]
        if m.group(1) in result and set(result[m.group(1)]) != set(value): conflicts.append(m.group(1))
        result[m.group(1)] = value
    return result, conflicts

selftest = {}
for phase in ['tampered','restored']:
    audit_txt = capture('audit_'+phase, ROOT/f'r/tgl_kernel_audit_capture_selftest_{phase}.txt')
    build_txt = capture('build_'+phase, ROOT/f'r/tgl_kernel_build_capture_selftest_{phase}.txt')
    amap, conflicts = axmap(audit_txt)
    selftest[phase] = {
        'audit_rc':int(re.search(r'# returncode: (-?\d+)',audit_txt)[1]),
        'build_rc':int(re.search(r'# returncode: (-?\d+)',build_txt)[1]),
        'unique_axioms':len(amap), 'conflicts':conflicts,
        'forbidden':{n:a for n,a in amap.items() if not set(a)<=ALLOWED},
        'matches_approved_audit':amap == formal['axiom_report']}

embedded = assignments['_EMBEDDED_KERNEL_FILES']
half = ROOT/'r/tgl_kernel/TGL/HalfNat.lean'
restored_half = half.read_bytes() == embedded['TGL/HalfNat.lean'].encode('utf-8')
pins['restored_HalfNat'] = pin(half)
pins['program'] = pin(ROOT/'um.py')
pins['run_program'] = pin(ROOT/'r/um.py')
pins['gate_extension'] = pin(ROOT/'gate_extension.py')
pins['formal_evidence_reused'] = pin(FORMAL)

seal_hashes = []
for name, expected in seal['sha256'].items():
    p = ROOT/'r'/name
    row = {'name':name, 'expected':expected, 'exists':p.is_file()}
    if row['exists']:
        row.update(pin(p)); row['matches'] = row['sha256']==expected
    else: row['matches'] = False
    seal_hashes.append(row)

qg = core['qg_closure']
gate_entries = []
for flaggroup, mapname, prefix in [('formal_flags','_QG_CERTIFICATE_FLAGS','qgc_'),('physics_flags','_QG_PHYSICS_FLAGS','qgp_')]:
    for flag, declaration in assignments[mapname].items():
        gate_entries.append({'flag':prefix+flag, 'declaration':declaration,
            'current_value':qg[flaggroup].get(flag), 'baseline_value':baseline['core']['qg_closure'][flaggroup].get(flag),
            'kernel_value':kf.get(prefix+flag), 'axioms':proof['axiom_report'].get(declaration)})

contracts = assignments['_V350_MODULAR_CONTRACTS']
# Independent predicates for the proposed repair; do not execute extracted author functions.
def clean_names(data,names):
    a = data.get('axiom_report') or {}
    build = data.get('lake_build_ok') is True or (data.get('incremental_build_ok') is True and
        data.get('dependency_hashes_verified') is True and data.get('changed_source_hashes_verified') is True)
    return bool(build and data.get('audit_returncode')==0 and data.get('all_verified') is True and all(
        isinstance(a.get(n),list) and all(isinstance(x,str) and x in ALLOWED for x in a[n]) for n in names))

def validate_frontier(data, flag):
    return flag in contracts and clean_names(data, contracts[flag])

assembly_node = functions['prove_the_assembly_and_the_single_debt']
clauses_assign = next(n for n in ast.walk(assembly_node) if isinstance(n,ast.Assign) and
    any(isinstance(t,ast.Name) and t.id=='clausulas' for t in n.targets))
clause_flags = []
for item in clauses_assign.value.elts:
    getter = next(n for n in ast.walk(item.elts[1]) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='get')
    clause_flags.append(ast.literal_eval(getter.args[0]))
clause_names = {f:contracts[f] if f in contracts else [assignments['_REDUCTION_FLAGS'][f[4:]]] for f in clause_flags}

def proposed_assembly(data):
    return all(data.get(f) is True and clean_names(data, names) for f,names in clause_names.items())

def proposed_atlas(data):
    active = [k for k,v in data.items() if k.startswith(('qgf_','gpf_')) and v is True]
    return all(validate_frontier(data,k) for k in active)

correction_simulation = {'method':'Independent predicates only; no patched monolith executed',
    'current_assembly_proofs_pass':proposed_assembly(kf),
    'current_atlas_active_flags_have_typed_proofs':proposed_atlas(kf),
    'active_frontier':{k:contracts.get(k) for k,v in kf.items() if k.startswith(('qgf_','gpf_')) and v is True},
    'clause_providers':{f:{'names':names,'flag':kf.get(f),'audited':clean_names(kf,names)} for f,names in clause_names.items()}}
negatives = {}
for case in ['missing_bridge','sorry_bridge','failed_audit','missing_old_clause','unknown_frontier']:
    data=copy.deepcopy(kf)
    if case=='missing_bridge':
        for names in contracts.values(): data['axiom_report'].pop(names[1],None)
    elif case=='sorry_bridge':
        for names in contracts.values(): data['axiom_report'][names[1]]=['sorryAx']
    elif case=='failed_audit': data['audit_returncode']=1
    elif case=='missing_old_clause': data['axiom_report'].pop(clause_names[clause_flags[0]][0],None)
    elif case=='unknown_frontier': data['qgf_unconditional_continuous_corner_proved']=True
    negatives[case]={'assembly':proposed_assembly(data),'atlas_frontier':proposed_atlas(data)}
correction_simulation['negative_fixtures']=negatives

regressions = {}
for category in ['formais','recusas_de_dado']:
    before=set(baseline_seal['not_sealed_this_run'][category]); after=set(seal['not_sealed_this_run'][category])
    regressions[category]={'before':sorted(before),'after':sorted(after),'added':sorted(after-before),'removed':sorted(before-after)}
    for name in sorted(after-before):
        now=core[name]; old=baseline['core'][name]
        regressions[name]={'current_verdict':now.get('verdict'), 'baseline_verdict':old.get('verdict'),
            'false_checks':[x for x in now.get('checks',[]) if len(x)>1 and x[1] is False],
            'all_verified':now.get('all_verified'), 'does_not_gate_core':now.get('does_not_gate_core')}

def fits_headers(p):
    """Read only FITS headers; skip payload, no scientific recomputation."""
    hdus=[]
    with p.open('rb') as f:
        while f.tell()<p.stat().st_size:
            header={}; done=False
            while not done:
                block=f.read(2880)
                if len(block)!=2880: raise ValueError('Invalid FITS header')
                for i in range(0,2880,80):
                    card=block[i:i+80].decode('ascii')
                    key=card[:8].strip()
                    if key=='END':done=True;break
                    if card[8:10]=='= ':
                        raw=card[10:].split('/')[0].strip()
                        if raw.startswith("'"):val=raw.strip("' ")
                        elif raw in ['T','F']:val=raw=='T'
                        else:
                            try:val=int(raw)
                            except ValueError:val=raw
                        header[key]=val
            n=header.get('NAXIS',0)
            length=math.prod(header.get('NAXIS'+str(i),0) for i in range(1,n+1)) if n else 0
            length=(length+header.get('PCOUNT',0))*header.get('GCOUNT',1)*abs(header.get('BITPIX',8))//8
            hdus.append({k:v for k,v in header.items() if k in ['EXTNAME','XTENSION','NAXIS1','NAXIS2','TFIELDS'] or k.startswith('TTYPE')})
            f.seek(((length+2879)//2880)*2880,1)
    return hdus

staged=[]
for entry in stage['files']:
    p=Path(entry['destination']); row={'manifest':entry,'actual':pin(p)}
    row['matches']=row['actual']['sha256']==entry['sha256'] and row['actual']['bytes']==entry['bytes']
    row['runtime_destination_present']=(ROOT/'r'/entry['relative_to_runtime']).exists()
    if p.suffix=='.fits':row['headers']=fits_headers(p)
    staged.append(row)

external=[]
for p in [Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\results.json'),
          Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\STOKES_A_Prova_do_Contorno.md')]:
    row=pin(p)
    if p.suffix=='.json':
        obj=json.loads(p.read_bytes()); hits=[]
        def find(o,path=''):
            if isinstance(o,dict):
                for k,v in o.items():
                    if k=='beta_acoustic_crosslock':hits.append({'path':path+'.'+k,'value':v})
                    find(v,path+'.'+k)
            elif isinstance(o,list):
                for i,v in enumerate(o): find(v,path+'.'+str(i))
        find(obj); row['beta_acoustic_crosslock']=hits
        row['runtime_candidates']=[{'path':str(x),'exists':x.is_file()} for x in [ROOT/'r/results.json',ROOT/'results.json']]
    external.append(row)

validation={
    'process_rc0':process.get('status')=='PROCESS_EXITED' and process.get('returncode')==0,
    'program_unchanged':pins['program']['sha256']==pins['run_program']['sha256']==contract['working_sha256'],
    'formal_axiom_map_reused_matches_proof_manifest':proof['axiom_report']==formal['axiom_report'],
    'proof_matches_result_axioms':proof['axiom_report']==kf['axiom_report'],
    'proof_stream_hashes_match_approved_captures':all(proof[k]==formal[c]['stdout_utf8_normalized_sha256'] for k,c in [('build_stdout_sha256','build_capture'),('audit_stdout_sha256','audit_capture')]),
    'eleven_gate_inputs_true':len(gate_entries)==11 and all(x['current_value'] is True and x['kernel_value'] is True and isinstance(x['axioms'],list) and set(x['axioms'])<=ALLOWED for x in gate_entries),
    'terminal_reproduced':qg['gate']['verdict']==baseline['core']['qg_closure']['gate']['verdict']==seal['qg_closure_verdict'],
    'six_frontier_flags_stay_false':sum(v is False for k,v in kf.items() if k.startswith(('qgf_','gpf_')))==6,
    'all_seal_file_hashes_match':all(x['matches'] for x in seal_hashes),
    'selftest_reports_passed':seal.get('fail_closed_selftest')=='FAIL_CLOSED_SELFTEST_PASSED' and 'com sorry injetado : verdict=TGL_KERNEL_FORMALIZATION_FAILED ; sorryAx_absent=False' in stdout and 'all_verified=True' in stdout,
    'tamper_exposes_forbidden_axiom':bool(selftest['tampered']['forbidden']),
    'restored_audit_matches_approved':selftest['restored']['matches_approved_audit'],
    'HalfNat_source_restored':restored_half,
    'checkpoint_off':seal['rite_checkpoints']['switch_on'] is False and seal['rite_checkpoints']['reused']==0,
    'staged_inputs_hashes_match':all(x['matches'] for x in staged),
}
result={'timestamp':datetime.datetime.now().astimezone().isoformat(),
    'scope':'ROUND02_COMPLETED__ARTIFACT_VERIFICATION_AND_AUXILIARY_REGRESSION_DIAGNOSIS',
    'no_author_code_executed':True,'no_process_or_session_access':True,'writes_only_revisao':True,
    'pins':pins,'validation':validation,'process':process,'gate_entries':gate_entries,
    'terminal':qg['gate']['verdict'],'selftest':selftest,'seal_hashes':seal_hashes,
    'regressions':regressions,'proposed_guard_evaluation':correction_simulation,
    'staged_inputs':staged,'external_providers':external,
    'limitations':['No replacement runtime or Lean compilation','No altered program executed',
        'Staged inputs not installed; future numeric outputs not predicted',
        'Broad semantic/numeric re-audit of every rite not performed',
        'Successful selftest does not discharge auxiliary consumer defects']}
dest=OUT/'final_inspection.json'
assert not dest.exists()
dest.write_bytes(json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps({'out':str(dest),'validation':validation,'selftest':selftest,
    'guard_evaluation':correction_simulation,'external_providers':external,
    'staged_files':[{'name':Path(x['actual']['path']).name,'matches':x['matches'],
      'hdu_names':[h.get('EXTNAME') for h in x.get('headers',[])]} for x in staged]},ensure_ascii=False,indent=2))
