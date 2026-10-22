"""Exercise the new exact index on real receipts and adversarial mutations only."""
from pathlib import Path
import ast,copy,importlib.util,json,sys
from diary_r1 import ROOT,new,pin

out=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015/full_rite'
run=ROOT/'work/rite394_20261015/r3'
module=out/'qualified_index_v394_r2.py'
spec=importlib.util.spec_from_file_location('qualified_index_candidate',module)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
source=run/'um_v394_final.py';tree=ast.parse(source.read_bytes())
names={'_EMBEDDED_KERNEL_FILES','_ESQUELETO_STONES','_LEAN_THEOREM_FLAGS','_QG_CERTIFICATE_FLAGS','_QG_PHYSICS_FLAGS','_QG_FRONTIER_FLAGS','_GRAVITY_PRICE_FLAGS','_REDUCTION_FLAGS','_GRAVITY_IMPORT_FLAGS','_GRAVITY_CITATION_FLAGS'}
ns={}
for node in tree.body:
    if isinstance(node,ast.Assign):
        for target in node.targets:
            if isinstance(target,ast.Name) and target.id in names:
                ns[target.id]=ast.literal_eval(node.value)
assert set(ns)==names
families=[(p,ns[n]) for p,n in [('', '_LEAN_THEOREM_FLAGS'),('qgc_','_QG_CERTIFICATE_FLAGS'),('qgp_','_QG_PHYSICS_FLAGS'),('qgf_','_QG_FRONTIER_FLAGS'),('gpf_','_GRAVITY_PRICE_FLAGS'),('red_','_REDUCTION_FLAGS'),('gpi_','_GRAVITY_IMPORT_FLAGS'),('gpc_','_GRAVITY_CITATION_FLAGS')]]
data=json.loads((run/'um_absoluto.json').read_bytes());core=copy.deepcopy(data['core'])
prov_path=out/'declaration_sources_r3/OUTPUT.txt'
provenance=m.parse_lean_provenance_v394(prov_path.read_text(encoding='utf-8').replace('DECL_SOURCE\t','TGL_DECL_SOURCE\t'))
assert provenance['ok']
capture_candidates=sorted(run.glob('tgl_kernel_audit_capture*.txt'))
assert capture_candidates
capture=next((p for p in capture_candidates if p.name=='tgl_kernel_audit_capture.txt'),capture_candidates[0])
parsed=m.parse_lean_axioms_v394(capture.read_text(encoding='utf-8'))
assert parsed['ok'],parsed['errors'][:5]
core['kernel_formalization']['axiom_report']=parsed['axioms']
assert set(parsed['axioms'])==set(provenance['sources'])
def build(c=core,p=provenance['sources'],f=ns['_EMBEDDED_KERNEL_FILES']):
    return m.build_iald_qualified_index_v394(c,p,f,ns['_ESQUELETO_STONES'],families)
ix=build()
checks={'all_declared_compiler_names_accounted':len(provenance['sources'])==26797,
 'source_hashes_and_audit_exact':ix['proveniencia_ok'],
 'no_true_flag_without_proof_source':not ix['violacoes'],
 'no_present_false_flag':not ix['presente_apagada'],
 'three_named_debts_preserved':ix['n_ausentes']==3,
 'namespace_not_blind':not ix['cegos_de_namespace']}
empty=build(p={});checks['empty_provenance_refused']=not empty['proveniencia_ok'] and bool(empty['violacoes'])
mut=copy.deepcopy(ns['_EMBEDDED_KERNEL_FILES']);rel=next(iter(provenance['sources'].values()));mut[rel]+='\n-- mutation\n'
checks['source_bit_change_refused']=not build(f=mut)['proveniencia_ok']
lost=dict(provenance['sources']);lost.pop(next(iter(lost)))
checks['missing_name_refused']=not build(p=lost)['proveniencia_ok']
bad=m.parse_lean_provenance_v394('TGL_DECL_SOURCE\tn\tTGL.A\nTGL_DECL_SOURCE\tn\tTGLExt.B')
checks['duplicate_source_refused']=not bad['ok']
checks['conflicting_axioms_refused']=not m.parse_lean_axioms_v394("'x' depends on axioms: [propext]\n'x' depends on axioms: [sorryAx]")['ok']
qnames=list(ix['qualificados'])
checks['aliases_do_not_choose']=all(ix['indice'][a]['arquivo'] is None and len(ix['indice'][a]['candidatos_qualificados'])>1 for a in ix['ambiguos'])
checks['aliases_do_not_erase_modes']=all(e['bandeiras']==[] for a,e in ix['indice'].items() if a not in ix['qualificados'])
def flags_of(v):return {b['chave']:b['acesa'] for e in v['qualificados'].values() for b in e['bandeiras']}
checks['flags_read_only']=all(core['kernel_formalization'][k] is v for k,v in flags_of(ix).items())
mut_core=copy.deepcopy(core);mut_core['kernel_formalization']['audit_returncode']=False
checks['boolean_audit_exit_refused']=bool(build(c=mut_core)['violacoes'])
dest=out/'qualified_index_tests_r2';dest.mkdir(exist_ok=False)
new(dest/'RESULT.json',dict(status='PASS' if all(checks.values()) else 'FAIL',checks=checks,
 statistics={k:ix[k] for k in ('n_nomes','n_arquivos','n_com_bandeira','n_ausentes')},
 ambiguous_aliases=len(ix['ambiguos']),errors=ix['proveniencia_erros'],violations=ix['violacoes'],present_false=ix['presente_apagada'],
 missing=[n for n,e in ix['qualificados'].items() if e['tipo']=='AUSENTE_POR_CONSTRUCAO'],
 sources=[pin(p) for p in [source,module,prov_path,capture,run/'um_absoluto.json']],script=pin(__file__),
 scope='Real audit transcript and compiler provenance reread. No um.py import, main, observation or production change. Parsed axioms add four quoted Unicode names omitted by the old regex.'))
print(json.dumps(dict(checks=checks,stats={k:ix[k] for k in ('n_nomes','n_arquivos','n_com_bandeira','n_ausentes')},errors=ix['proveniencia_erros'][:8],violations=ix['violacoes'][:8],present_false=ix['presente_apagada'][:8],receipt=pin(dest/'RESULT.json')),ensure_ascii=False))
raise SystemExit(0 if all(checks.values()) else 2)
