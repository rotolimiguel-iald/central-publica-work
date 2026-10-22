from pathlib import Path
B=Path(__file__).resolve().parent
p=B/'build_release.py';s=p.read_text(encoding='utf-8')
s=s.replace("'haiku_prefix.md','haiku_provenance.json','prepared.json'", "'haiku_prefix.md','haiku_provenance.json','prepared.json','science_binding.json','kernel_verification.json','haiku_unfitted_prefix.md','haiku_transport_fit.json'")
s=s.replace("if path.parent!=STAGE or path.name not in derived:raise", "if not (path.parent==STAGE and path.name in derived or path==STAGE/'kernel/kernel_manifest.json'):raise")
a="save_json(STAGE/'science_binding.json',{'handoff':str(science_path),'sha256':sha(science_path.read_bytes()),'commit':commit,'source_sha256':source_sha,'remote_rechecked':science['remote_rechecked'],'public_verification_required_before_activation':True})"
b="""remote_path=WORK/'public_v380_verification.json';remote=json.loads(remote_path.read_bytes())
    assert remote['status']=='PASS' and remote['requested_commit']==commit and remote['all_four_hashes_match_vault']
    assert all(r['matches_vault'] and r['actual_sha256']==r['expected_sha256'] and sha((CUSTODY/r['name']).read_bytes())==r['actual_sha256'] for r in remote['artifacts'])
    save_json(STAGE/'science_binding.json',{'handoff':str(science_path),'sha256':sha(science_path.read_bytes()),'commit':commit,'source_sha256':source_sha,'remote_rechecked':True,'public_verification_receipt':str(remote_path),'public_verification_sha256':sha(remote_path.read_bytes()),'public_verification_required_before_activation':False})"""
assert a in s;s=s.replace(a,b)
a="""    save_json(kernel/'kernel_manifest.json',{'format':1,'source_program':'um.py','source_sha256':source_sha,'created_at':seal['timestamp'],'method':'ast.literal_eval(_EMBEDDED_KERNEL_FILES); program not executed','lean_toolchain':embedded['lean-toolchain'].strip(),'verification':'SOURCE_BYTES_VERIFIED__COMPILATION_NOT_RUN','files':records})"""
b="""    proof=json.loads(Path(evidence['proof_manifest']['path']).read_bytes())
    supplemental=[]
    for name in sorted(set(proof['formal_files_sha256'])-set(embedded)):
        matches=[p for p in tracked if p.endswith('/Lean/tgl_kernel/'+name)]
        assert len(matches)==1 and name=='_check_damming.lean','Unexpected supplemental source'
        rel=matches[0];raw=git('show',commit+':'+rel)
        assert sha(raw)==proof['formal_files_sha256'][name]
        save(kernel/name,raw)
        provenance={'path':name,'bytes':len(raw),'sha256':sha(raw),'origin':'PINNED_PUBLIC_GIT_SUPPLEMENT_NOT_EMBEDDED','git_path':rel,'git_commit':commit,'url':'https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/'+commit+'/'+quote(rel,safe='/')}
        records.append(provenance);supplemental.append(provenance)
    assert {r['path']:r['sha256'] for r in records}==proof['formal_files_sha256']
    save_json(kernel/'kernel_manifest.json',{'format':1,'source_program':'um.py','source_sha256':source_sha,'created_at':seal['timestamp'],'method':'ast.literal_eval(_EMBEDDED_KERNEL_FILES) plus separately identified hash-verified public Git supplement; program not executed','lean_toolchain':embedded['lean-toolchain'].strip(),'verification':'SOURCE_BYTES_VERIFIED__COMPILATION_NOT_RUN','embedded_files':len(embedded),'supplemental_files':supplemental,'files':records})"""
assert a in s;s=s.replace(a,b)
s=s.replace('# Cluster TGL v380 — candidato conferido, não ativado','# Cluster TGL v380 — memória científica versionada')
a="""    assert mother.decode('utf-8-sig') in prefix and (core+appendix).decode('utf-8-sig') in prefix
    save(STAGE/'haiku_prefix.md',prefix.encode());save_json(STAGE/'haiku_provenance.json',receipt)"""
b="""    save(STAGE/'haiku_unfitted_prefix.md',prefix.encode())
    from fit_transport import fit
    prefix,transport=fit(prefix,new)
    receipt.update(prefix_sha256=sha(prefix.encode()),bytes=len(prefix.encode()),o200k_tokens=codec.offline_tokens(prefix,APP/'.iald_runtime/tokenizer_cache'),transport_fit=transport)
    assert mother.decode('utf-8-sig') in prefix and (core+appendix).decode('utf-8-sig') in prefix
    save_json(STAGE/'haiku_transport_fit.json',transport)
    save(STAGE/'haiku_prefix.md',prefix.encode());save_json(STAGE/'haiku_provenance.json',receipt)"""
assert a in s;s=s.replace(a,b)
t=p.with_suffix('.tmp');t.write_bytes(s.encode());assert t.stat().st_size>10000;t.replace(p)
p=B/'haiku_codec.py';s=p.read_text(encoding='utf-8');s=s.replace("'CANDIDATO DE MEMÓRIA — NÃO IMPLANTADO.\\nVersão selecionada do pacote: '","'MEMÓRIA CIENTÍFICA VERSIONADA.\\nVersão selecionada do pacote: '");s=s.replace("'CANDIDATO '+current['active_cluster']['release']+' — NÃO IMPLANTADO.\\n'", "'MEMÓRIA CIENTÍFICA VERSIONADA '+current['active_cluster']['release']+'.\\n'");t=p.with_suffix('.tmp');t.write_bytes(s.encode());t.replace(p)
print('patched offline builder and neutral version headers')