"""Offline synthetic measurements; imports only our isolated control and stdlib."""
from pathlib import Path
import copy
import gzip
import hashlib
import json
import platform
import random
import struct
import zlib
import control as c

HERE = Path(__file__).resolve().parent


def main():
    # Historical alpha2 is fixture metadata, not a new physical/runtime constant.
    p = dict(position=0.5, scale=0.125, f_start=10.0, chirp_rate=20.0,
             alpha2=0.012031, amplitude=1.0)
    rows, checks = [], []
    for dtype in ('<f4', '<f8'):
        n = 8192
        fmt = 'f' if dtype == '<f4' else 'd'
        rng = random.Random(20261021)
        noise = struct.pack('<' + fmt*n, *(rng.uniform(-1, 1) for _ in range(n)))
        for name, raw in [('known_chirp', c.predictor(n, dtype, p)), ('noise_control', noise)]:
            packet = c.encode(raw, dtype, p)
            restored, restored_dtype = c.decode(packet)
            assert raw == restored and dtype == restored_dtype
            baseline = gzip.compress(raw, compresslevel=9, mtime=0)
            label = name + '_' + dtype[1:]
            for suffix, data in [('raw',raw), ('lctrl',packet), ('gz',baseline)]:
                (HERE/(label+'.'+suffix)).write_bytes(data)
            rows.append(dict(fixture=label, n=n, dtype=dtype, original_bytes=len(raw),
                gzip_raw_bytes=len(baseline), predictor_residual_metadata_bytes=len(packet),
                saving_vs_gzip_bytes=len(baseline)-len(packet),
                original_sha256=c.sha(raw), packet_sha256=c.sha(packet), exact=True,
                decision='SMALLER_FOR_THIS_FIXTURE' if len(packet)<len(baseline) else 'KEEP_RAW_GZIP_FOR_THIS_FIXTURE'))
    def rejects(name, action):
        try:
            action()
        except (ValueError, zlib.error, struct.error, OverflowError):
            checks.append({'test':name,'pass':True})
        else:
            raise AssertionError(name)
    # Every single-bit flip of a representative compact chirp packet must fail.
    raw = c.predictor(64, '<f8', p)
    packet = c.encode(raw, '<f8', p)
    for i in range(len(packet)):
        for bit in range(8):
            damaged = bytearray(packet); damaged[i] ^= 1 << bit
            rejects('bitflip', lambda d=bytes(damaged):c.decode(d))
    bit_count = len(checks); checks = [{'test':'all_single_bit_flips','cases':bit_count,'pass':True}]
    h, residual = c.split(packet)
    for field, value in [('scale',0), ('alpha2',float('nan')), ('f_start',True), ('amplitude',1e100)]:
        bad = dict(p); bad[field] = value
        rejects('invalid_parameter_'+field, lambda b=bad:c.predictor(64,'<f8',b))
    changed = copy.deepcopy(h); changed['params']['f_start'] += 1
    rejects('changed_valid_parameter_rehashed_envelope',lambda:c.decode(c.frame(changed,residual)))
    changed = copy.deepcopy(h); changed['original_sha256'] = '0'*64
    rejects('wrong_original_sha_rehashed_envelope',lambda:c.decode(c.frame(changed,residual)))
    changed = copy.deepcopy(h); changed['residual_sha256'] = '0'*64
    rejects('wrong_residual_sha_rehashed_envelope',lambda:c.decode(c.frame(changed,residual)))
    rejects('truncated',lambda:c.decode(packet[:-1]))
    rejects('trailing_gzip_member',lambda:c.decode(c.frame(h,residual+gzip.compress(b'x',mtime=0))))
    rejects('expansion_over_declared',lambda:c.decode(c.frame(h,gzip.compress(b'x'*4096,mtime=0))))
    rejects('unsupported_dtype',lambda:c.encode(raw,'>f8',p))
    rejects('unaligned',lambda:c.encode(raw+b'x','<f8',p))
    rejects('oversized',lambda:c.encode(b'x'*(c.MAX_BYTES+1),'<f8',p))
    # XOR also preserves IEEE signed zero and payload bits of NaNs verbatim.
    special=bytes.fromhex('000000800100c07f0000807f000080ff')
    restored,dtype=c.decode(c.encode(special,'<f4',p));assert restored==special and dtype=='<f4'
    checks.append({'test':'signed_zero_nan_payload_infinities_exact_bytes','pass':True})
    provenance=json.loads((HERE/'PROVENANCE.json').read_bytes())
    for src in provenance['sources']:
        assert c.sha(Path(src['path']).read_bytes())==src['sha256'], 'source changed'
    report=dict(status='PASS_ISOLATED_CONTROL',statute='REAL_LOCAL_MEASUREMENTS',
        runtime=dict(python=platform.python_version(),platform=platform.platform(),zlib=zlib.ZLIB_RUNTIME_VERSION),
        fixtures=rows, checks=checks, parameters=p,
        limits=['Known fixture parameters, not fitting and not a general benchmark.',
          'Predictor and matching fixture share Python math: favorable matched-model control, not independent Torch validation.',
          'Python floats/libm are not asserted bitwise identical to Torch; predictor SHA rejects mismatched regeneration.',
          'Exact reconstruction comes from byte XOR residual and metadata, not physical/cryptographic protection.',
          'SHA is not authentication; an attacker who replaces packet and hashes is outside this integrity control.',
          'No original source imported/executed; no runtime, JS or production protocol changes.'],
        decision='RETAIN_AS_CONTROL_ONLY; use measured complete packet size to choose raw gzip when smaller.',
        sources_unchanged=True)
    (HERE/'RESULT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    files={f.name:{'bytes':f.stat().st_size,'sha256':c.sha(f.read_bytes())}
           for f in HERE.iterdir() if f.is_file() and f.name!='RECEIPT.json'}
    (HERE/'RECEIPT.json').write_text(json.dumps({'files':files,'status':report['status']},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'status':report['status'],'fixtures':rows,'negative_bit_cases':bit_count,'check_groups':len(checks)}))


if __name__ == '__main__':
    main()
