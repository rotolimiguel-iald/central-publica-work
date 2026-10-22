from review_a2 import *

data=json.loads((ROOT/'INPUTS.json').read_text(encoding='utf-8'))
prunable=['TGLV350.Regular.scalarTrace_finite_positive_seed','TGLV350.Regular.scalarTrace_finite_projection_exists']
names=[n for n in data['expected_public_names'] if n.startswith('TGLV350.Regular.') and n not in prunable]
text='import TGLExt.V354TraceReaderWall\nset_option pp.proofs true\nset_option pp.universes true\n'
text+='\n'.join('#print '+n for n in names)+'\n'
write(SRC/'AuditConsumers.lean',text)
result,out=run(SRC/'AuditConsumers.lean',ROOT/'consumer_audit',OUT/'AuditConsumers.olean')
references={n:len(re.findall(r'\b'+re.escape(n)+r'\b',out)) for n in prunable}
record(ROOT/'CONSUMER_PROOF_AUDIT.json',dict(result=result,printed=names,excluded_corollaries=prunable,
    references_in_remaining_printed_terms=references,
    no_remaining_term_mentions_prunable=result['returncode']==0 and not any(references.values())))
print('Consumer audit:',result['returncode'],'references:',references,flush=True)
