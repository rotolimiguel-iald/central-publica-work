"""Candidate D-H byte consumer. Trust is supplied by the authenticated caller.

An expected digest is not authentication. The caller must obtain it from an
operator act independently of the untrusted document. This module verifies
scope and bytes and NEVER freezes, opens data or emits a scientific verdict.
The receipt schema is a candidate for c1 approval, not an existing human act.
"""
from pathlib import Path
import hashlib,json,re

class AdmissionError(ValueError): pass

def _sha(value):
    if not isinstance(value,str) or not re.fullmatch('[0-9a-f]{64}',value):
        raise AdmissionError('SHA256_REQUIRED')
    return value

def _read(path,expected,root):
    path=Path(path).resolve(); root=Path(root).resolve()
    if not path.is_relative_to(root):raise AdmissionError('SOURCE_OUTSIDE_ADMITTED_ROOT')
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=_sha(expected):raise AdmissionError('SOURCE_BYTES_CHANGED')
    return raw

def read_admission(receipt_path,*,trusted_receipt_sha256,spec_sha256,
                   verified_readers,known_source_hashes,source_root):
    """Consume an exact D-H act, or fail. No self-asserted role is trusted."""
    try:
        if not trusted_receipt_sha256:raise AdmissionError('AUTHENTICATED_ACT_PIN_MISSING')
        raw=Path(receipt_path).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=_sha(trusted_receipt_sha256):
            raise AdmissionError('ACT_PIN_MISMATCH')
        doc=json.loads(raw)
        if doc['schema']!='iald.fase9.source-admission/v1' or doc['act']!='D-H':
            raise AdmissionError('WRONG_ACT_SCHEMA')
        if doc['witness']!='scalar' or doc['spec_sha256']!=_sha(spec_sha256):
            raise AdmissionError('ACT_SCOPE_MISMATCH')
        if doc['decision']!='ADMIT':raise AdmissionError('ACT_NOT_ADMISSION')
        if not isinstance(doc['authority_evidence'],str) or not doc['authority_evidence'].strip():
            raise AdmissionError('AUTHORITY_PROVENANCE_MISSING')
        entries=doc['readers']
        if not isinstance(entries,list) or not entries:raise AdmissionError('EMPTY_ADMISSION')
        admitted=set(); evidence=[]
        if not isinstance(verified_readers,dict) or not verified_readers:raise AdmissionError('INVENTORY_REQUIRED')
        if not set(known_source_hashes).issubset(verified_readers):raise AdmissionError('KNOWN_SOURCE_OUTSIDE_INVENTORY')
        for entry in entries:
            rid=entry['reader_id']
            if rid not in verified_readers or rid in admitted:raise AdmissionError('UNKNOWN_OR_DUPLICATE_READER')
            sources=entry['sources']
            if not isinstance(sources,list) or not sources:raise AdmissionError('ADMITTED_SOURCE_REQUIRED')
            hashes=set()
            for source in sources:
                digest=_sha(source['sha256'])
                _read(source['path'],digest,source_root)
                hashes.add(digest);evidence.append({'reader_id':rid,'sha256':digest})
            if not set(known_source_hashes.get(rid,[])).issubset(hashes):
                raise AdmissionError('ACT_DOES_NOT_COVER_BOUND_SOURCE')
            admitted.add(rid)
        verified=set()
        for rid,record in verified_readers.items():
            if not isinstance(record,dict) or not isinstance(record.get('status'),str):
                raise AdmissionError('MALFORMED_DOCUMENTARY_STATUS')
            if record['status']=='REAL_DOCUMENTARY_HASH_ONLY':verified.add(rid)
        declared=sorted(set(verified_readers)-verified-admitted)
        return {'admission_receipt_sha256':trusted_receipt_sha256,
                'admitted_reader_ids':sorted(admitted),'declared_unverified_reader_ids':declared,
                'n_alvos_declarados':len(declared),
                'required_sources_admitted':set(verified_readers).issubset(admitted),
                'source_evidence':evidence,'scope':'entire_V1x_inventory',
                'authority_verified_by_this_module':False,
                'may_open_data':False,'v2_frozen':False,'verdict':None}
    except AdmissionError:raise
    except (KeyError,TypeError,ValueError,OSError) as exc:
        raise AdmissionError('MALFORMED_OR_UNREADABLE_ADMISSION: '+str(exc)) from exc
