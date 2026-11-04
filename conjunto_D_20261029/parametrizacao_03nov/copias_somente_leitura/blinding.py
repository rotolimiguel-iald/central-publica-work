"""Program-only offset access. The analyst receives shifted columns and hashes.

The local seed is committed by SHA256 in E2; its bytes and offsets must not be
printed, placed in the tunnel, or returned by analysis tools before unblinding.
This is procedural blinding on one host, not a separate human custodian.
"""
import hashlib,hmac,math,re
from numbers import Real
from pathlib import Path
import numpy as np
from registration_guard import contained,sha

FIELDS=('dtau220','dtau440','domega220','domega440')

def shifted_samples(columns,event,registration):
    if not set(FIELDS)<=set(columns):raise ValueError('All four deformation fields required')
    lengths={len(columns[k]) for k in FIELDS}
    if len(lengths)!=1 or next(iter(lengths))<2:raise ValueError('Paired nonempty samples required')
    seedpath=contained(registration['blinding']['seed_relative_to_Chatgpt'])
    if sha(seedpath)!=registration['blinding']['seed_commitment_sha256']:raise ValueError('Blinding commitment differs')
    seed=seedpath.read_bytes()
    if len(seed)!=32:raise ValueError('Invalid blinding seed length')
    scale=float(registration['blinding']['offset_half_range'])
    if not np.isfinite(scale) or scale<=0:raise ValueError('Invalid offset range')
    output={}
    for name in FIELDS:
        if name not in columns:continue
        a=np.asarray(columns[name],dtype=float)
        if a.ndim!=1 or not np.isfinite(a).all():raise ValueError('Invalid samples before blinding')
        digest=hmac.new(seed,('013BIS:'+event+':'+name).encode(),hashlib.sha256).digest()
        u=(int.from_bytes(digest[:8],'big')+.5)/(2**64)
        output['blinded_'+name]=(a+scale*(2*u-1)).tolist()
    if not output:raise ValueError('No deformation samples to blind')
    return {'status':'BLINDED_SAMPLES__NO_UNBLINDING_AUTHORIZATION',
      'event':event,'columns':output,'seed_commitment_sha256':registration['blinding']['seed_commitment_sha256'],
      'warning':'Offset-censored; means and signs have no physical interpretation. Parameter estimation private intermediates remain unread by analyst.'}

def unblinding_allowed(registration,reading,information,systematic_gate,receipt):
    """A per-reading permission check, not a physical-significance verdict."""
    if systematic_gate is not True or not isinstance(reading,str):return False
    if not isinstance(registration,dict) or not isinstance(receipt,dict):return False
    config=registration.get('blinding',{})
    if not isinstance(config,dict):return False
    identity=registration.get('registration_id');seed_pin=config.get('seed_commitment_sha256')
    if not isinstance(identity,str) or not identity or not isinstance(seed_pin,str) or re.fullmatch('[0-9a-f]{64}',seed_pin) is None:return False
    targets=config.get('minimum_information_to_unblind_by_reading',{})
    if not isinstance(targets,dict):return False
    threshold=targets.get(reading)
    def finite_positive(x):
        return isinstance(x,Real) and not isinstance(x,(bool,np.bool_)) and math.isfinite(x) and x>0
    if not finite_positive(threshold) or not finite_positive(information) or information<threshold:return False
    pin=receipt.get('dataset_sha256');expected=config.get('unblinding_dataset_sha256')
    if not isinstance(pin,str) or re.fullmatch('[0-9a-f]{64}',pin) is None or pin!=expected:return False
    return bool(receipt.get('status')=='REGISTERED_UNBLINDING_GATE_MET' and
                receipt.get('reading')==reading and receipt.get('scope')=='per-reading' and
                receipt.get('independent_review_passed') is True and
                receipt.get('seed_commitment_sha256')==config.get('seed_commitment_sha256') and
                receipt.get('information')==information and receipt.get('systematic_gate') is True and
                receipt.get('registration_id')==registration.get('registration_id'))


def select_authorized_reading(columns,registration,reading,information,systematic_gate,receipt):
    """Select already prepared reading-labelled columns; never accesses the seed.

    This does not decrypt a posterior or certify global evidence. Raw shared posterior
    columns are intentionally not a per-reading release: they would expose other readings.
    """
    if not unblinding_allowed(registration,reading,information,systematic_gate,receipt):
        raise ValueError('Per-reading release not authorized')
    allowed=registration['blinding'].get('release_columns_by_reading',{}).get(reading)
    if not isinstance(allowed,list) or not allowed or len(allowed)!=len(set(allowed)):
        raise ValueError('Explicit unique release columns required')
    if any(not isinstance(name,str) or not name.startswith(reading+':') for name in allowed):
        raise ValueError('Release must contain only columns labelled by this reading')
    if receipt.get('released_columns')!=allowed or not set(allowed)<=set(columns):
        raise ValueError('Receipt/available release columns differ')
    return {'status':'PER_READING_COLUMNS_SELECTED_NOT_GLOBAL_CLAIM','reading':reading,
            'columns':{name:columns[name] for name in allowed},'dataset_sha256':receipt['dataset_sha256']}
