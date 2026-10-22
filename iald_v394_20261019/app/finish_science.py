"""Refresh JEV bindings and prepare native measurement of the full public package."""
from pathlib import Path
import ast, json, sys
from prepare_science import W, S, R, C, save, write, sha
sys.path[:0]=[str(S/'memory_build'),str(R)]
import iald_jev_control as control
from iald_release_binding import load_release

def main():
    stage=S/'memory_stage'
    m=json.loads((stage/'manifest_staged.json').read_bytes())
    old=json.loads((R/'iald_nucleo_fixo.json').read_bytes())
    contract=json.loads(Path(old['jev_control']['path']).read_bytes())
    e=m['published_evidence']; program=Path(e['program']['path']).read_bytes()
    tree=ast.parse(program)
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='prove_iald_executive_runtime')
    result=json.loads(Path(e['result']['path']).read_bytes())
    contract.update(release='v394',source_sha256=sha(program),result_sha256=sha(Path(e['result']['path']).read_bytes()),proof_manifest_sha256=sha(Path(e['proof_manifest']['path']).read_bytes()),core_record=result['core']['iald_executive_runtime'])
    contract['source']['lines']=[node.lineno,node.end_lineno]
    for anchor in contract['anchors']:
        text=(stage/'kernel'/anchor['file']).read_bytes()
        anchor['sha256']=sha(text)
        assert all(symbol in text.decode() for symbol in anchor['symbols'])
    control.validate_contract(contract)
    raw=control.canonical_bytes(contract)
    save(stage/'jev_control_v394.json',raw)
    target=Path(json.loads((stage/'prepared.json').read_bytes())['install_target'])
    for file, dest in (('manifest_staged.json',stage/'jev_control_v394.json'),('manifest_install.json',target/'jev_control_v394.json')):
        config=json.loads((stage/file).read_bytes())
        config['jev_control']={'path':str(dest),'sha256':sha(raw),'release':'v394','source_sha256':sha(program)}
        write(stage/file,config)
    prefix=(stage/'public_prefix.md').read_bytes()
    save(S/'package/prefix.md',prefix)
    write(S/'public_memory_provenance.json',{'deployment':load_release(stage/'manifest_staged.json').identity,'metadata':json.loads((stage/'public_metadata.json').read_bytes()),'prefix_sha256':sha(prefix),'private_atlas_included':False,'generation_requests':0})
    count=(C/'work/iald_haiku55_jev_20261007/count_package.py').read_text(encoding='utf-8').replace('v390','v394').replace('V390','V392')
    save(S/'count_package.py',count.encode())
    print(json.dumps({'status':'CONTROL_BOUND','release':contract['release'],'source_lines':contract['source']['lines'],'prefix_bytes':len(prefix)}))

if __name__=='__main__': main()
