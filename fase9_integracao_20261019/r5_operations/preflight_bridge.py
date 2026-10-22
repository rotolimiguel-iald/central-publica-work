"""Consume the existing byte gate's snapshot without reopening the draft.

The caller must invoke the pinned verify_v1x_binding first. This function does
not fabricate a documentary verification or an operator decision. It supplies
admission fields to the future runner and always leaves freeze/opening separate.
"""
from admission import AdmissionError,read_admission

def prepare_with_admission(gate,*,expected_spec_sha256,source_root,
                           admission_path=None,trusted_admission_sha256=None):
    try:
        if gate['spec_sha256']!=expected_spec_sha256:raise AdmissionError('GATE_SPEC_MISMATCH')
        if gate['v2_frozen'] is not False:raise AdmissionError('DRAFT_GATE_SCOPE_CHANGED')
        readers=gate['verified_readers']
        if set(readers)!=set(gate['spec_snapshot']['leitores']):raise AdmissionError('INVENTORY_CHANGED')
        known={rid:[row['source_sha256']] for rid,row in readers.items() if row.get('source_sha256')}
        if admission_path is None:
            if trusted_admission_sha256 is not None:raise AdmissionError('ACT_BYTES_MISSING')
            declared=sorted(rid for rid,row in readers.items() if row['status']!='REAL_DOCUMENTARY_HASH_ONLY')
            result={'admitted_reader_ids':[],'declared_unverified_reader_ids':declared,
                    'n_alvos_declarados':len(declared),'required_sources_admitted':False,
                    'admission_status':'PENDING_D_H'}
        else:
            result=read_admission(admission_path,trusted_receipt_sha256=trusted_admission_sha256,
                spec_sha256=expected_spec_sha256,verified_readers=readers,
                known_source_hashes=known,source_root=source_root)
            result['admission_status']='PINNED_ACT_BYTES_CONSUMED_NOT_AUTHENTICATED_HERE'
        result.update(spec_sha256=expected_spec_sha256,binding_sha256=gate['binding_sha256'],
                      witness='scalar',may_open_data=False,v2_frozen=False,verdict=None,
                      required_separate_acts=['X13','c1_freeze','operator_opening'],
                      n_alvos_scope='entire_V1x_inventory; gate_unverified AND no_pinned_operator_admission')
        return result
    except AdmissionError:raise
    except (KeyError,TypeError,ValueError) as exc:
        raise AdmissionError('MALFORMED_GATE_SNAPSHOT: '+str(exc)) from exc
