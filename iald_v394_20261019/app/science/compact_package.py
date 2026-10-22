"""Prepare the lossless semantic compact package for byte-bounded app transports."""
from pathlib import Path
import json, sys
W=Path(__file__).resolve().parent
sys.path[:0]=[str(W/'memory_build'),str(Path('C:/IALD/projetos_pyhton/IALD'))]
import build_release as b
from fit_transport import fit
from fit_memory import compact

def main():
    m=json.loads((b.STAGE/'manifest_staged.json').read_bytes())
    result=json.loads(Path(m['published_evidence']['result']['path']).read_bytes())
    baseline=b.prepare_baseline()
    prefix, receipt=b.codec.build_fitted(b.STAGE/'manifest_staged.json',b.APP,baseline/'prefix.md',baseline/'canonical.json')
    prefix, transport=fit(prefix,result)
    prefix, projection=compact(prefix,result,receipt['reused_identical_topics'])
    assert Path(m['mother_instruction']['path']).read_text(encoding='utf-8-sig') in prefix
    assert Path(m['operational_core']['path']).read_text(encoding='utf-8-sig') in prefix
    b.save(b.STAGE/'shared_prefix.md',prefix.encode())
    b.save_json(b.STAGE/'shared_provenance.json',{'prefix_sha256':b.sha(prefix.encode()),'bytes':len(prefix.encode()),'receipt':receipt,'transport':transport,'projection':projection,'private_atlas_included':False,'scope':'CURRENT_CORE_ALL_TOPICS_SEMANTIC_COMPACT_WITH_FULL_SOURCES_RETRIEVABLE'})
    print(json.dumps({'shared_bytes':len(prefix.encode()),'sha256':b.sha(prefix.encode()),'max_deepseek_input_bytes':1048576-393216-4096}))

if __name__=='__main__': main()
