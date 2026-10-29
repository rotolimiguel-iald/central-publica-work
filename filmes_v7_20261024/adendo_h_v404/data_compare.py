"""Blocking exact data comparison; allowed values independently read from sealed source."""
import ast,copy,datetime,hashlib,importlib.util,json,re,sys,traceback
import context as c
from data_manage import check,FILES
sys.path.insert(0,str(c.E))
import compare_v402 as reference
B=c.B;S=c.S;sha=c.sha
reference.S=S;reference.B=B
read=c.read;pin=c.pin;save=c.save
differences=reference.differences;digest=reference.digest
def expected_from(old,new):
    d=copy.deepcopy(old['docs']); ns=new['seal']; nc=new['counts']; nd=new['docs']
    h=d['hud.json']; p=d['PROVENANCE_PUBLIC.json']; st=d['STDOUT_LINES.json']
    h['extra'].update(nc)
    by_id={'theorems':'proof_ladder_clean','n_formal':'formal_count',**{k:k for k in nc}}
    for item in h['items']:
        if item['id'] in by_id:
            item['value']=nc[by_id[item['id']]]
            item['text']=f"{nc['proof_ladder_clean']}/{nc['proof_ladder_total']}" if item['id']=='theorems' else str(item['value'])
        elif item['id']=='um_sha16':item['value']=item['text']=ns['sha256']['um.py'][:16]
    for field in ['seal_timestamp','selo_timestamp']:h[field]=ns['timestamp']
    h.update(seal_version=ns['um_version'],seal_pin=ns['sha256']['um.py'],result_hash16=ns['result_hash'][:16])
    d['scene.json']['source_sha256']=ns['sha256']['um.py']
    old_ratio=f"{old['counts']['proof_ladder_clean']}/{old['counts']['proof_ladder_total']}"
    new_ratio=f"{nc['proof_ladder_clean']}/{nc['proof_ladder_total']}"
    assert len(st['lines'])==len(nd['STDOUT_LINES.json']['lines'])
    for before,after in zip(st['lines'],nd['STDOUT_LINES.json']['lines']):
        expected_text=before['text']
        if re.search(r'teoremas limpos:\s*'+re.escape(old_ratio),expected_text):
            expected_text=expected_text.replace(old_ratio,new_ratio,1)
        # Exact expected text is compared by the complete recursive diff below.
        assert after['chapter']==before['chapter']
        before.update(line=after['line'],text=expected_text,line_sha256=after['line_sha256'],text_sha256=digest(expected_text.encode()))
    st['source']=nd['STDOUT_LINES.json']['source'];st['source_sha256']=sha(S/'source'/st['source'])
    h['stdout_lines']=copy.deepcopy(st['lines']);h['stdout_sha256']=st['source_sha256']
    anchor_counts={'proof ladder clean':'proof_ladder_clean','proof ladder expected':'proof_ladder_total',
                   'kernel formal files':'formal_count','kernel declarations':'declaration_count',
                   **{'HUD '+k:k for k in nc}}
    for a in p['anchors']:
        if a['name'] in anchor_counts:a['json_value']=a['live_value']=nc[anchor_counts[a['name']]]
    p['kernel'].update(theorems_clean=nc['proof_ladder_clean'],theorems_total=nc['proof_ladder_total'],
                       axiom_report_entries=nc['declaration_count'],formal_files=nc['formal_count'],
                       formal_source_hash=new['proof']['formal_source_hash'])
    p['seal_version']=ns['um_version'];p['generated_at']=ns['timestamp'];p['um_sha16']=ns['sha256']['um.py'][:16]
    p['selo'].update(timestamp=ns['timestamp'],result_hash=ns['result_hash'])
    p['sources']=copy.deepcopy(nd['PROVENANCE_PUBLIC.json']['sources'])
    assert set(p['sources'])=={'um.py','um_absoluto.json','um_absoluto_selo.json','tgl_kernel_proof_manifest.json',st['source']}
    # Section differences are reported separately, including the G-authorized gate implementation.
    p['source_code_sections']=copy.deepcopy(nd['PROVENANCE_PUBLIC.json']['source_code_sections'])
    d['MANIFEST.json']=copy.deepcopy(p)
    return d

def run():
 preflight=check();c.stable_seal()
 old=reference.inspect(B);new=reference.inspect(S)
 assert old['seal']['um_version']=='v402' and new['seal']['um_version']=='v404'
 core=read(S/'source/um_absoluto.json')['core'];oldcore=read(B/'source/um_absoluto.json')['core']
 rec=core['bandeiras_do_gate_v403'];values=rec['values']
 expected=expected_from(old,new)
 # All amended values are read from the core, then independently checked against runtime-derived exports.
 changes={'flags_computed':values['n_calculated'],'flags_literal':values['n_literal']}
 expected['hud.json']['extra'].update(changes)
 for item in expected['hud.json']['items']:
  if item['id'] in changes:item['value']=changes[item['id']];item['text']=str(item['value'])
 g=expected['frames.json']['gate'];g['computed_count']=values['n_calculated'];g['literal_count']=values['n_literal']
 for f in g['flags']:
  if f['name'] in values['informative']:f['origin']='computed from recorded inputs'
 g.update(informative_flags=values['informative'],n_read_by_the_verdict=values['n_read_by_the_verdict'],flag_scope_source='core.bandeiras_do_gate_v403.values')
 p=expected['PROVENANCE_PUBLIC.json'];p['gate_flag_origins']={'literal':[],'computed_count':values['n_calculated']}
 for a in p['anchors']:
  key=a['name'].removeprefix('HUD ')
  if a['name'].startswith('HUD ') and key in changes:a['json_value']=a['live_value']=changes[key]
 expected['MANIFEST.json']=copy.deepcopy(p)
 results=[];unexpected=[]
 for name in FILES:
  bad=differences(expected[name],new['docs'][name]);unexpected += [{'file':name,**x} for x in bad]
  results.append({'file':name,'before':pin(B/'data'/name),'after':pin(S/'data'/name),'differences':differences(old['docs'][name],new['docs'][name]),'unexpected':bad})
 # Extract exact replay bytes without executing source. Scientific replay must be identical.
 spec=importlib.util.spec_from_file_location('v404_replay_build',S/'replay/build_replay.py');build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
 excerpt,ranges,scalar,srange=build.extract((S/'source/um.py').read_bytes())
 replay=[]
 for name,raw in [('um_nucleo_filme.py',excerpt),('um_scalar_excerpt.py',scalar)]:
  prior=(B/'replay'/name).read_bytes();same=prior==raw
  replay.append({'file':name,'identical_bytes':same,'before_sha256':digest(prior),'after_sha256':digest(raw)})
  if not same:unexpected.append({'file':'replay/'+name,'path':'/','kind':'scientific_text','before':prior.decode(),'after':raw.decode()})
 sections=[]
 for name,before in old['sections'].items():
  after=new['sections'][name];changed=before!=after
  sections.append({'name':name,'identical_bytes':not changed,'before_sha256':digest(before),'after_sha256':digest(after),'authorization':'Adendo G/F8.1 gate calculation' if name=='prove_qg_closure_gate' else None})
  if changed and name!='prove_qg_closure_gate':unexpected.append({'file':'source/um.py','path':name,'before':before.decode(),'after':after.decode(),'kind':'scientific_text'})
  if changed and name=='prove_qg_closure_gate':save(c.H/'DATA_GATE_SOURCE_DIFF.json',{'before':before.decode(),'after':after.decode(),'order':pin(c.G.parent.parent.parent.parent/'dummy') if False else pin(c.ORDER),'scope':'Gate code change explicitly covered by G/H; exact full before/after for distinct review.'})
 # No nature text, number, or verdict is exempted.
 unexpected += [{'file':'source/um_absoluto.json','path':'/core/teste_de_veracidade_fase9_v397'+x['path'],**{k:v for k,v in x.items() if k!='path'}} for x in differences(oldcore['teste_de_veracidade_fase9_v397'],core['teste_de_veracidade_fase9_v397'])]
 assert oldcore['qg_closure']['gate']==core['qg_closure']['gate']
 # Derive gate readership directly from AST and source constants, independently of declared count.
 tree=ast.parse((S/'source/um.py').read_bytes());defs={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)}
 gatefn=defs['evaluate_quantum_gravity_closure'];reads={k:set() for k in ('formal','physics','experiment')}
 for n in ast.walk(gatefn):
  if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and isinstance(n.func.value,ast.Name) and n.func.value.id in reads and n.func.attr=='get' and n.args and isinstance(n.args[0],ast.Constant):reads[n.func.value.id].add(n.args[0].value)
 # Formal keys are collected through the source tuple used by the verdict.
 for n in ast.walk(gatefn):
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='formal_required' for t in n.targets):reads['formal'].update(ast.literal_eval(n.value))
 assert sum(map(len,reads.values()))==values['n_read_by_the_verdict']
 assert [len(reads[k]) for k in ('formal','physics','experiment')]==values['read_by_the_verdict']
 assert len(new['docs']['frames.json']['gate']['flags'])==values['n_flags']
 gate_evidence={'source_values':values,'ast_direct_reads':{k:sorted(v) for k,v in reads.items()},'verdict_unchanged':True,'source_record':pin(S/'source/um_absoluto.json')}
 negatives=[]
 for label,alter in [('other_number',lambda x:x['hud.json']['extra'].__setitem__('threshold_sigma',99)),('array_length',lambda x:x['hud.json']['items'].pop()),('unapproved_text',lambda x:x['STDOUT_LINES.json']['lines'][0].__setitem__('text','alterado')),('new_field',lambda x:x['scene.json'].__setitem__('unapproved_field',True))]:
  bad=copy.deepcopy(expected);alter(bad);refused=any(differences(expected[n],bad[n]) for n in FILES);assert refused;negatives.append({'name':label,'refused':refused})
 report={'status':'STOP_UNAUTHORIZED_DELTA' if unexpected else 'PASS_NUMERIC_PENDING_DISTINCT_REVIEW','source':'v404','source_sha256':sha(S/'source/um.py'),'preflight':preflight,'order':pin(c.ORDER),'source_capture':pin(c.H/'SOURCE_CAPTURE.json'),'baseline':pin(c.H/'DATA_BASELINE_MANIFEST.json'),'method':'Exact recursive comparison of six complete JSON trees; allowed changes constructed from pinned source, not copied wholesale from candidate. No numerical tolerance for tree comparison.','files':results,'unexpected_differences':unexpected,'counts':new['counts'],'gate':gate_evidence,'source_sections':sections,'replay_text':replay,'nature_record_identical':oldcore['teste_de_veracidade_fase9_v397']==core['teste_de_veracidade_fase9_v397'],'negative_controls':negatives,'release_for_render':False,'limits':['Distinct verification required before parent render','No TTS/render/network/Lean','Scientific source function gate differs explicitly under G; replay numerical excerpt must not differ']}
 c.stable_seal();save(c.H/'NUMERIC_COMPARISON.json',report)
 print(json.dumps({'status':report['status'],'unexpected_count':len(unexpected),'first_differences':unexpected[:4],'counts':new['counts'],'gate_reads':gate_evidence['ast_direct_reads']},ensure_ascii=False))
 return report
if __name__=='__main__':run()
