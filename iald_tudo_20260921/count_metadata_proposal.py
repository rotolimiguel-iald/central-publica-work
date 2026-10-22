"""Free provider count of the byte-pinned, reversible metadata derivative."""
from pathlib import Path
import hashlib
import json
import sys
from verify_metadata_draft import verify

W=Path(__file__).resolve().parent

def audited_verify(path):
    path=Path(path).resolve()
    assert path.parent == W
    result=verify(path)
    review=json.loads((W/'adversarial_memory_review/source_metadata_code_review_20260922_165920_460112.json').read_bytes())
    assert review['status']=='APROVADO_CODIGO_NO_ESCOPO_JSON_ESTRUTURAL_COMPOSTO'
    assert review['required_changes_current_candidate']==[]
    for name in ('compact_source_fields.py','compact_source_items.py'):
        assert hashlib.sha256((W/name).read_bytes()).hexdigest()==review['pins'][name]['sha256']
    receipt=json.loads(path.with_suffix('.json').read_bytes())
    baseline=Path(review['candidate']['path'])
    assert baseline.parent==W and hashlib.sha256(baseline.read_bytes()).hexdigest()==review['candidate']['sha256']
    # New parents are accepted only through the full reviewed lineage checked
    # by verify_metadata_draft: pinned source, approved capsules, exact undo.
    # The verifier permits only reversibly grouped source metadata and a fixed
    # explanatory paragraph. The previously audited corpus cannot gain data.
    return result

if __name__=='__main__':
    import count_native_reviewed_draft as counter
    counter.verify=audited_verify
    counter.main()
