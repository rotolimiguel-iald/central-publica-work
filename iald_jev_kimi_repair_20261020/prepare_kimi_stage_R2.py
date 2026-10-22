"""Prepare only isolated staging; never import runtime or scientific programs."""
from pathlib import Path
import ast, hashlib, json

W = Path(__file__).resolve().parent
R = Path(r'C:\IALD\projetos_pyhton\IALD')
K = Path(r'C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg')
S = W / 'stage_kimi'
S.mkdir(exist_ok=True)
sha = lambda raw: hashlib.sha256(raw).hexdigest()
def new(name, raw):
    p = S / name
    if not isinstance(raw, bytes): raw = json.dumps(raw, ensure_ascii=False, indent=2).encode()
    with p.open('xb') as f: f.write(raw)
    assert p.read_bytes() == raw
    return p

baseline = {n: (R/n).read_bytes() for n in ('iald_jev_control.py','iald_auto_router.py','iald_nucleo_fixo.json')}
control = baseline['iald_jev_control.py'].decode('utf-8-sig').replace('\r\n','\n')
router = baseline['iald_auto_router.py'].decode('utf-8-sig').replace('\r\n','\n')
manifest = json.loads(baseline['iald_nucleo_fixo.json'])
original_path = Path(manifest['jev_control']['path'])
original_raw = original_path.read_bytes()
assert sha(original_raw) == manifest['jev_control']['sha256']
contract = json.loads(original_raw)
packet = (K/'core_packet_v394.txt').read_bytes()
cpname = 'core_packet_v394_bound_R2.txt'
contract['core_packet'].update(arquivo=cpname,sha256=sha(packet),regra='Raw bytes pinned; UTF-8 BOM/newline normalization only for comparison with verified canonical first 8000 characters. No extra excerpt.')
contractname = 'jev_control_v394_v2_bound_R2.json'
contractpath = new(contractname,contract)
new(cpname,packet)

helper = '''def load_core_packet(root, contract):
    """Verify bytes, release and canonical excerpt; never execute a source."""
    try:
        root = Path(root).resolve(strict=True)
        manifest_raw, manifest = _read_json(_local_file(root, "iald_nucleo_fixo.json"), 1000000)
        cp = contract["core_packet"]
        _validate_v2_extensions(contract)
        if cp["um_version"] != manifest["active_cluster"]["release"]:
            raise ControlError("Core packet release mismatch")
        path = _local_file(root, cp["arquivo"])
        if path.stat().st_size > 65536:
            raise ControlError("Core packet exceeds byte bound")
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != _sha(cp["sha256"]):
            raise ControlError("Core packet raw hash mismatch")
        entry = next(e for e in manifest["entries"] if e["id"] == "um_forma_canonica_integral")
        if not entry["url"].startswith("https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/"):
            raise ControlError("Unverified canonical source URL")
        canonical = _local_file(root, entry["path"]).read_bytes()
        if hashlib.sha256(canonical).hexdigest() != _sha(entry["public_sha256"]):
            raise ControlError("Canonical excerpt source hash mismatch")
        normalize = lambda value: value.decode("utf-8-sig").replace("\\r\\n", "\\n").replace("\\r", "\\n")
        text = normalize(raw)
        if text != normalize(canonical)[:8000]:
            raise ControlError("Core packet differs from canonical excerpt")
        if _local_file(root, "iald_nucleo_fixo.json").read_bytes() != manifest_raw:
            raise ControlError("Active manifest changed during packet verification")
        return text, dict(packet_sha256=hashlib.sha256(raw).hexdigest(), packet_bytes=len(raw),
            source_sha256=hashlib.sha256(canonical).hexdigest(), url=entry["url"],
            release=contract["release"], release_source_sha256=contract["source_sha256"],
            first_character=0, characters=len(text), coverage="COMPLETE_BOUND_ROUTING_PACKET_PARTIAL_CANONICAL",
            sha256_da_fonte=hashlib.sha256(raw).hexdigest(), estatuto="REAL",
            inscrito_por={"kind":"host", "id":"iald_jev_control", "scope":"byte_verification_not_source_authorship"})
    except (OSError, KeyError, TypeError, UnicodeError, StopIteration) as exc:
        raise ControlError("Core packet unavailable or invalid") from exc


'''
control = control.replace('def load_contract(root):',helper+'def load_contract(root):',1)
needle = '        # Fence the exact bytes captured before verification'
assert needle in control
control = control.replace(needle,'        if contract["schema"] == SCHEMA_V2:\n            load_core_packet(root, contract)\n'+needle,1)
control = control.replace('def new_receipt(request, source_sha256, candidates):','def new_receipt(request, source_sha256, candidates, *, contract=None):',1)
control = control.replace('    return dict(schema=1, identity=identity, identity_sha256=digest(identity),\n                original_candidates=candidates, candidates=list(candidates), history=["prepared"], state="prepared")', '''    receipt = dict(schema=1, identity=identity, identity_sha256=digest(identity),
                original_candidates=candidates, candidates=list(candidates), history=["prepared"], state="prepared")
    if contract is not None and contract["schema"] == SCHEMA_V2:
        validate_contract(contract)
        policy = contract["stopping_criterion"]
        if set(policy["terminais"]) != {"resolved", "refused", "uncertain"}:
            raise ControlError("Host requires all graph terminal states")
        if policy["max_transicoes"] < 3:
            raise ControlError("Transition budget cannot admit one complete route")
        receipt["host_policy"] = dict(max_transicoes=policy["max_transicoes"], contract_sha256=digest(contract))
    return receipt''',1)
needle='        out.update(state=target, candidates=narrowed, history=history + [target])'
assert needle in control
control=control.replace(needle,'''        policy = out.get("host_policy")
        if policy is not None:
            cap = policy["max_transicoes"]
            if type(cap) is not int or not 3 <= cap <= 32:
                raise ControlError("Invalid host transition budget")
            _sha(policy["contract_sha256"])
            # Reserve one edge for an honest terminal receipt before nonterminal work.
            if len(history) > cap or (GRAPH[target] and len(history) >= cap):
                raise ControlError("Host transition budget exhausted; no retry")
'''+needle+'''
        if policy is not None and not GRAPH[target]:
            out["stopping_receipt"] = dict(verdict=target, transitions=len(history),
                history_sha256=digest(out["history"]), identity_sha256=out["identity_sha256"],
                contract_sha256=policy["contract_sha256"], reentry="forbidden",
                estatuto="REAL", inscrito_por={"kind":"host", "id":"iald_jev_control"})''',1)

router=router.replace('def memory_slice(root=ROOT):','def memory_slice(root=ROOT, contract=None):\n    if contract is not None and contract["schema"] == jev_control.SCHEMA_V2:\n        return jev_control.load_core_packet(root, contract)',1)
router=router.replace('memory,source=memory_slice(root)','memory,source=memory_slice(root,contract)',1)
router=router.replace("control_state['source_sha256'],candidates)","control_state['source_sha256'],candidates,contract=contract)",1)
router=router.replace("        if len(state['canonical_memory']) > 1024:","        if not source.get('packet_sha256') and len(state['canonical_memory']) > 1024:",1)

projection = '''def _auditable_projection(common):
    """Existing scoped ledger receipt is a pointer, never invented full-state custody."""
    try:
        receipt, coverage = common["projection_receipt"], common["coverage"]
        if (type(common["projection"]) is not str or type(receipt) is not dict
                or type(receipt["revision"]) is not int or receipt["revision"] < 0
                or receipt["context_id"] != common["memory_id"]):
            raise jev_control.ControlError("Invalid operational projection binding")
        for key in ("state_sha256", "event_hash"):
            value = receipt[key]
            if type(value) is not str or len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                raise jev_control.ControlError("Invalid operational custody receipt")
        actual = hashlib.sha256(common["projection"].encode("utf-8")).hexdigest()
        if actual != coverage["projection_sha256"] or len(common["projection"]) != coverage["actual_chars"]:
            raise jev_control.ControlError("Operational projection hash mismatch")
        if (type(coverage["omitted_records"]) is not int or coverage["omitted_records"] < 0
                or type(coverage["required_chars"]) is not int
                or not 0 <= coverage["required_chars"] <= coverage["actual_chars"]):
            raise jev_control.ControlError("Invalid operational projection coverage")
        return dict(schema="iald.audit-projection.v1", full_state_pointer=dict(receipt),
            projection_sha256=actual, omitted_optional_records=coverage["omitted_records"],
            sha256_da_fonte=receipt["state_sha256"], estatuto="DERIVED",
            inscrito_por={"kind":"host", "id":"iald_auto_router", "scope":"projection_not_original_authorship"},
            recovery="same authenticated memory_id/revision; older revisions require journal replay",
            authority="scoped_data_only_no_new_permissions")
    except (KeyError, TypeError, UnicodeError) as exc:
        raise jev_control.ControlError("Operational projection unavailable or invalid") from exc


'''
router=router.replace('def _fit_routing_payload(body):',projection+'def _fit_routing_payload(body):',1)
needle="    target = common['coverage']['actual_chars'] if common else 0"
assert needle in router
router=router.replace(needle,needle+'''
    bound_packet = bool(source.get('packet_sha256'))
    if bound_packet and common is not None:
        state['holographic_projection'] = _auditable_projection(common)''',1)
needle="            common = projected\n            state['common_memory'] = projected"
assert needle in router
router=router.replace(needle,needle+'''
            if bound_packet:
                state['holographic_projection'] = _auditable_projection(projected)''',1)

for name,text in [('iald_jev_control.py',control),('iald_auto_router.py',router)]:
    ast.parse(text)
    # Match current baseline newline encoding, without importing modules.
    new(name,text.replace('\n','\r\n').encode('utf-8'))
manifest['jev_control'].update(path=str(R/contractname),sha256=sha(contractpath.read_bytes()))
new('iald_nucleo_fixo.json',manifest)
files=[]
for name in ('iald_jev_control.py','iald_auto_router.py',cpname,contractname,'iald_nucleo_fixo.json'):
    dest=R/name
    files.append(dict(source=str(S/name),destination=str(dest),sha256=sha((S/name).read_bytes()),
        baseline=sha(baseline[name]) if name in baseline else (sha(dest.read_bytes()) if dest.exists() else None)))
new('install_plan_R2.json',dict(schema='iald.transaction.plan.v1',status='STAGING_ONLY_REQUIRES_REAL_REVIEW',files=files))
new('BUILD_EVIDENCE_R2.json',dict(original_v2=dict(path=str(original_path),sha256=sha(original_raw)),
    kimi_packet=dict(path=str(K/'core_packet_v394.txt'),sha256=sha(packet),bytes=len(packet)),
    manifest_changes=['/jev_control/path','/jev_control/sha256'],
    baseline={n:sha(b) for n,b in baseline.items()},
    runtime_untouched=all((R/n).read_bytes()==b for n,b in baseline.items()),
    changes={'control':['load_core_packet','load_contract','new_receipt','transition'],
             'router':['memory_slice','_auditable_projection','_fit_routing_payload','choose']},
    limits=['No physical holography, learned metric or new memory engine is implemented.',
            'Original record provenance stays in existing scoped ACOM projection; wrapper authorship is the host only.',
            'Custody pointer uses existing ACOM receipt; this does not independently replay/verify the ledger.',
            'Main lease owns submission; no acceptance, deployment, generation, calibration or shadow activation.']))
print(json.dumps(dict(stage=str(S),files=len(files),packet_sha256=sha(packet),runtime_untouched=True)))
