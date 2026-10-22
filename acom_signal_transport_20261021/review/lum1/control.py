"""Synthetic control only; Python math port, not bitwise Torch identity.

Formula provenance and measured source pins are in PROVENANCE.json.
XOR preserves bytes, independently of predictor accuracy. SHA is integrity,
not authentication. This format is NOT iald-signal-blocks/1.
"""
import gzip
import hashlib
import json
import math
import struct
import zlib

MAX_BYTES = 1024 * 1024
MAX_HEADER = 4096
MAGIC = b'LCTRL1\0'
PARAMS = {'position', 'scale', 'f_start', 'chirp_rate', 'alpha2', 'amplitude'}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()


def predictor(n, dtype, params):
    need(type(n) is int and n >= 2, 'sample count')
    need(dtype in ('<f4', '<f8'), 'dtype')
    size = 4 if dtype == '<f4' else 8
    need(n * size <= MAX_BYTES, 'object limit')
    need(type(params) is dict and set(params) == PARAMS, 'parameters')
    need(all(type(v) in (int, float) and math.isfinite(v) and abs(v) <= 1e6
             for v in params.values()), 'finite bounded parameters')
    need(1e-6 <= params['scale'] <= 1e6 and 1e-6 <= params['alpha2'] < 1, 'scale/alpha2')
    values = []
    for i in range(n):
        t = i / (n - 1)  # Explicit fixture grid; no assertion of Torch equality.
        tau = t - params['position']
        xi = tau / params['scale']
        envelope = math.exp(-abs(xi)) * (1 - params['alpha2'] *
                    math.exp(-abs(xi) / (params['alpha2'] * 10)))
        phase = 2 * math.pi * (params['f_start'] * tau + params['chirp_rate'] * tau**2 / 2)
        values.append(params['amplitude'] * envelope * math.sin(phase))
    return struct.pack('<' + ('f' if size == 4 else 'd') * n, *values)


def frame(header, compressed):
    h = canonical(header)
    need(len(h) <= MAX_HEADER, 'header limit')
    body = MAGIC + struct.pack('>I', len(h)) + h + compressed
    return body + hashlib.sha256(body).digest()


def encode(raw, dtype, params):
    need(type(raw) is bytes and len(raw) <= MAX_BYTES, 'input bytes')
    need(dtype in ('<f4', '<f8'), 'dtype')
    size = 4 if dtype == '<f4' else 8
    need(len(raw) % size == 0, 'alignment')
    n = len(raw) // size
    pred = predictor(n, dtype, params)
    residual = bytes(a ^ b for a, b in zip(raw, pred))
    h = dict(version=1, dtype=dtype, n=n, params=params,
             original_sha256=sha(raw), predictor_sha256=sha(pred),
             residual_sha256=sha(residual), bytes=len(raw))
    return frame(h, gzip.compress(residual, compresslevel=9, mtime=0))


def split(packet):
    need(type(packet) is bytes and 43 <= len(packet) <= MAX_BYTES + MAX_HEADER + 2048, 'wire limit')
    body = packet[:-32]
    need(hashlib.sha256(body).digest() == packet[-32:], 'packet integrity')
    need(body[:7] == MAGIC, 'magic')
    length = struct.unpack('>I', body[7:11])[0]
    need(0 < length <= MAX_HEADER and 11 + length < len(body), 'header length')
    def unique(pairs):
        result = {}
        for k, v in pairs:
            need(k not in result, 'duplicate key')
            result[k] = v
        return result
    h = json.loads(body[11:11+length], object_pairs_hook=unique)
    return h, body[11+length:]


def decode(packet):
    h, compressed = split(packet)
    need(type(h) is dict and set(h) == {'version','dtype','n','params','original_sha256',
         'predictor_sha256','residual_sha256','bytes'}, 'header schema')
    need(type(h['version']) is int and h['version'] == 1, 'version')
    pred = predictor(h['n'], h['dtype'], h['params'])
    need(type(h['bytes']) is int and h['bytes'] == len(pred), 'length')
    need(sha(pred) == h['predictor_sha256'], 'predictor mismatch')
    dec = zlib.decompressobj(31)
    residual = dec.decompress(compressed, len(pred) + 1)
    need(len(residual) == len(pred) and dec.eof and not dec.unused_data and
         not dec.unconsumed_tail, 'residual bounds/stream')
    need(sha(residual) == h['residual_sha256'], 'residual integrity')
    raw = bytes(a ^ b for a, b in zip(pred, residual))
    need(sha(raw) == h['original_sha256'], 'original integrity')
    return raw, h['dtype']
