"""ORDEM 022/D: local narration planning; Edge TTS only on explicit exact-plan approval."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid
import wave


# BEGIN edge-tts upstream DRM helpers, LGPL-3.0; source and license in README.txt
# Upstream SHA256: b29c37e2a0c11284adb2a1ffc04f0f231e1ba2d921494a912797218b05d64c4a
import struct
from functools import lru_cache
from typing import List, Tuple, Optional
TRUSTED_CLIENT_TOKEN = "6A5AA1D4EAFF4E9FB37E23D68491D6F4"
WIN_EPOCH = 11644473600

S_TO_NS = 1e9

_SHA256_INITIAL = (
    0x6A09E667,
    0xBB67AE85,
    0x3C6EF372,
    0xA54FF53A,
    0x510E527F,
    0x9B05688C,
    0x1F83D9AB,
    0x5BE0CD19,
)

_SHA256_STATE = (
    0xFD9FBEA2,
    0x91243CE7,
    0xBE499094,
    0xCD2E1E0A,
    0x6C006F49,
    0x04BD35AB,
    0xFEB0A7E4,
    0x03EFFBD2,
)

_SHA256_SCHEDULE = (
    0xEB24BF9E,
    0x1558691F,
    0xA0C09EE2,
    0x0CFA32BA,
    0xA622EE8C,
    0xD1DD9491,
    0xC0DD25A0,
    0xF9E70AB6,
    0xF0C31573,
    0x7058CE4E,
    0x7188E606,
    0x00E5AB33,
    0xD258B060,
    0x72766564,
)

_SHA256_ROUND_CONSTANTS = (
    0x428A2F98,
    0x71374491,
    0xB5C0FBCF,
    0xE9B5DBA5,
    0x3956C25B,
    0x59F111F1,
    0x923F82A4,
    0xAB1C5ED5,
    0xD807AA98,
    0x12835B01,
    0x243185BE,
    0x550C7DC3,
    0x72BE5D74,
    0x80DEB1FE,
    0x9BDC06A7,
    0xC19BF174,
    0xE49B69C1,
    0xEFBE4786,
    0x0FC19DC6,
    0x240CA1CC,
    0x2DE92C6F,
    0x4A7484AA,
    0x5CB0A9DC,
    0x76F988DA,
    0x983E5152,
    0xA831C66D,
    0xB00327C8,
    0xBF597FC7,
    0xC6E00BF3,
    0xD5A79147,
    0x06CA6351,
    0x14292967,
    0x27B70A85,
    0x2E1B2138,
    0x4D2C6DFC,
    0x53380D13,
    0x650A7354,
    0x766A0ABB,
    0x81C2C92E,
    0x92722C85,
    0xA2BFE8A1,
    0xA81A664B,
    0xC24B8B70,
    0xC76C51A3,
    0xD192E819,
    0xD6990624,
    0xF40E3585,
    0x106AA070,
    0x19A4C116,
    0x1E376C08,
    0x2748774C,
    0x34B0BCB5,
    0x391C0CB3,
    0x4ED8AA4A,
    0x5B9CCA4F,
    0x682E6FF3,
    0x748F82EE,
    0x78A5636F,
    0x84C87814,
    0x8CC70208,
    0x90BEFFFA,
    0xA4506CEB,
    0xBEF9A3F7,
    0xC67178F2,
)

_SHA256_ADJUSTMENT = 0xC9DC06A7

_SHA256_BLOCK_CONSTANTS = (
    _SHA256_ROUND_CONSTANTS[:14] + (_SHA256_ADJUSTMENT,) + _SHA256_ROUND_CONSTANTS[15:]
)

_SHA256_SIGMA0_ADJUSTMENT = 0x059C0B80

_SHA256_SIGMA1_ADJUSTMENT = 0x000B92C0

_CS64_COEFFICIENTS = (
    (0xE82E91B1, 0xB32700D0),
    (0x44DE24C6, 0x88DFF51D),
    (0x3BEB65BC, 0x29514038),
    (0xC89C5933, 0xB328CBDF),
    (0x8D1EC211, 0xD405B4D5),
    (0x314EF5D5, 0x26E55F3C),
    (0xE92491B1, 0x607801C6),
    (0xF0A5B9D5, 0x82B2C1FB),
    (0x06064CF3, 0xFA51A3DA),
    (0xDA79FA60, 0x207CC464),
    (0xBED20560, 0x3C3C74F3),
    (0x89F9C9F8, 0xD2D14B61),
    (0x35FA38C6, 0xBB04A2C1),
    (0xCB49E3C6, 0xC5626167),
)

_CS64_FACTOR = 0x82893933

_CS64_ADJUSTMENT0 = 0xF2F90B1A

_CS64_ADJUSTMENT1 = 0x0B1A0000

_U32_MASK = 0xFFFFFFFF

def _rol16(value: int) -> int:
    """Rotate a 32-bit value left by 16 bits."""
    value &= _U32_MASK
    return ((value << 16) | (value >> 16)) & _U32_MASK

def _words_le4_even(data: bytes) -> List[int]:
    """Split data into little-endian 32-bit words, zero-padded to an even count."""
    padded = data + b"\x00" * ((-len(data)) % 4)
    if not padded:
        return []
    words = list(struct.unpack(f"<{len(padded) // 4}I", padded))
    if len(words) % 2:
        words.append(0)
    return words

def _sigma0(value: int) -> int:
    """SHA-256 small sigma zero, truncating the combined rotations once."""
    return (
        (value >> 7) ^ (value << 25) ^ (value >> 18) ^ (value << 14) ^ (value >> 3)
    ) & _U32_MASK

def _sigma1(value: int) -> int:
    """SHA-256 small sigma one, truncating the combined rotations once."""
    return (
        (value >> 17) ^ (value << 15) ^ (value >> 19) ^ (value << 13) ^ (value >> 10)
    ) & _U32_MASK

def _sha256_rounds(
    state: Tuple[int, ...], words: List[int], first_round: int = 0
) -> Tuple[int, ...]:
    """Run SHA-256 rounds, optionally resuming inside the first block."""
    a, b, c, d, e, f, g, h = state
    mask = _U32_MASK
    constants = (
        _SHA256_BLOCK_CONSTANTS if first_round == 14 else _SHA256_ROUND_CONSTANTS
    )
    # Multiplying a 32-bit word by 2**32 + 1 repeats it in 64 bits.
    # A right shift then has ROTR's low 32 bits, with no separate left shift.
    # The final additions mask off the unused high bits.
    aligned = min(64, ((first_round + 7) // 8) * 8)
    for index in range(first_round, aligned):
        rot_e = e * 0x100000001
        rot_a = a * 0x100000001
        t1 = (
            h
            + ((rot_e >> 6) ^ (rot_e >> 11) ^ (rot_e >> 25))
            + (g ^ (e & (f ^ g)))
            + constants[index]
            + words[index]
        )
        t2 = ((rot_a >> 2) ^ (rot_a >> 13) ^ (rot_a >> 22)) + ((a & b) | (c & (a | b)))
        a, b, c, d, e, f, g, h = (t1 + t2) & mask, a, b, c, (d + t1) & mask, e, f, g
    # Eight rounds return the working-register names to their original order.
    # Rotate their roles in the expressions instead of moving eight values
    # after every round; only the two updated registers need assignments.
    for index in range(aligned, 64, 8):
        rot_e = e * 0x100000001
        rot_a = a * 0x100000001
        t1 = (
            h
            + ((rot_e >> 6) ^ (rot_e >> 11) ^ (rot_e >> 25))
            + (g ^ (e & (f ^ g)))
            + constants[index]
            + words[index]
        )
        d = (d + t1) & mask
        h = (
            t1
            + ((rot_a >> 2) ^ (rot_a >> 13) ^ (rot_a >> 22))
            + ((a & b) | (c & (a | b)))
        ) & mask
        rot_e = d * 0x100000001
        rot_a = h * 0x100000001
        t1 = (
            g
            + ((rot_e >> 6) ^ (rot_e >> 11) ^ (rot_e >> 25))
            + (f ^ (d & (e ^ f)))
            + constants[index + 1]
            + words[index + 1]
        )
        c = (c + t1) & mask
        g = (
            t1
            + ((rot_a >> 2) ^ (rot_a >> 13) ^ (rot_a >> 22))
            + ((h & a) | (b & (h | a)))
        ) & mask
        rot_e = c * 0x100000001
        rot_a = g * 0x100000001
        t1 = (
            f
            + ((rot_e >> 6) ^ (rot_e >> 11) ^ (rot_e >> 25))
            + (e ^ (c & (d ^ e)))
            + constants[index + 2]
            + words[index + 2]
        )
        b = (b + t1) & mask
        f = (
            t1
            + ((rot_a >> 2) ^ (rot_a >> 13) ^ (rot_a >> 22))
            + ((g & h) | (a & (g | h)))
        ) & mask
        rot_e = b * 0x100000001
        rot_a = f * 0x100000001
        t1 = (
            e
            + ((rot_e >> 6) ^ (rot_e >> 11) ^ (rot_e >> 25))
            + (d ^ (b & (c ^ d)))
            + constants[index + 3]
            + words[index + 3]
        )
        a = (a + t1) & mask
        e = (
            t1
            + ((rot_a >> 2) ^ (rot_a >> 13) ^ (rot_a >> 22))
            + ((f & g) | (h & (f | g)))
        ) & mask
        rot_e = a * 0x100000001
        rot_a = e * 0x100000001
        t1 = (
            d
            + ((rot_e >> 6) ^ (rot_e >> 11) ^ (rot_e >> 25))
            + (c ^ (a & (b ^ c)))
            + constants[index + 4]
            + words[index + 4]
        )
        h = (h + t1) & mask
        d = (
            t1
            + ((rot_a >> 2) ^ (rot_a >> 13) ^ (rot_a >> 22))
            + ((e & f) | (g & (e | f)))
        ) & mask
        rot_e = h * 0x100000001
        rot_a = d * 0x100000001
        t1 = (
            c
            + ((rot_e >> 6) ^ (rot_e >> 11) ^ (rot_e >> 25))
            + (b ^ (h & (a ^ b)))
            + constants[index + 5]
            + words[index + 5]
        )
        g = (g + t1) & mask
        c = (
            t1
            + ((rot_a >> 2) ^ (rot_a >> 13) ^ (rot_a >> 22))
            + ((d & e) | (f & (d | e)))
        ) & mask
        rot_e = g * 0x100000001
        rot_a = c * 0x100000001
        t1 = (
            b
            + ((rot_e >> 6) ^ (rot_e >> 11) ^ (rot_e >> 25))
            + (a ^ (g & (h ^ a)))
            + constants[index + 6]
            + words[index + 6]
        )
        f = (f + t1) & mask
        b = (
            t1
            + ((rot_a >> 2) ^ (rot_a >> 13) ^ (rot_a >> 22))
            + ((c & d) | (e & (c | d)))
        ) & mask
        rot_e = f * 0x100000001
        rot_a = b * 0x100000001
        t1 = (
            a
            + ((rot_e >> 6) ^ (rot_e >> 11) ^ (rot_e >> 25))
            + (h ^ (f & (g ^ h)))
            + constants[index + 7]
            + words[index + 7]
        )
        e = (e + t1) & mask
        a = (
            t1
            + ((rot_a >> 2) ^ (rot_a >> 13) ^ (rot_a >> 22))
            + ((b & c) | (d & (b | c)))
        ) & mask
    return a, b, c, d, e, f, g, h

def _expand_sha256_schedule(words: List[int], first_word: int = 16) -> None:
    """Expand SHA-256 words, combining rotations before modular addition."""
    mask = _U32_MASK
    for index in range(first_word, 64):
        x, y = words[index - 2], words[index - 15]
        # Rotations can retain their high bits until the final sum is masked.
        sigma1 = (x >> 17) ^ (x << 15) ^ (x >> 19) ^ (x << 13) ^ (x >> 10)
        sigma0 = (y >> 7) ^ (y << 25) ^ (y >> 18) ^ (y << 14) ^ (y >> 3)
        words.append((sigma1 + words[index - 7] + sigma0 + words[index - 16]) & mask)

@lru_cache(maxsize=1)
def _sha256_init(data: bytes) -> Tuple[int, ...]:
    """Compute the initial SHA-256 state for token data."""
    mask = _U32_MASK
    words = [0] * 14 + [int.from_bytes(data[:3], "big")]
    words.append(int.from_bytes(data[3:7], "big"))
    for index in range(16, 30):
        value = _SHA256_SCHEDULE[index - 16]
        if index - 2 >= 14:
            value += (
                (_sigma1(words[index - 2]) ^ _SHA256_SIGMA1_ADJUSTMENT)
                if index == 16
                else _sigma1(words[index - 2])
            )
        if index - 7 >= 14:
            value += words[index - 7]
        if index - 15 >= 14:
            value += (
                (_sigma0(words[index - 15]) ^ _SHA256_SIGMA0_ADJUSTMENT)
                if index == 29
                else _sigma0(words[index - 15])
            )
        words.append(value & mask)
    words.append(
        (
            _sigma1(words[28])
            + words[23]
            + _sigma0(words[15])
            + words[14]
            + _SHA256_ADJUSTMENT
            - _SHA256_ROUND_CONSTANTS[14]
        )
        & mask
    )
    _expand_sha256_schedule(words, 31)
    working = _sha256_rounds(_SHA256_STATE, words, 14)
    return tuple((x + y) & mask for x, y in zip(_SHA256_INITIAL, working))

def _sha256_digest(data: bytes) -> bytes:
    """Compute the SHA-256 digest for token data."""
    if len(data) < 7:
        raise ValueError("Token salt must contain at least seven bytes")
    mask = _U32_MASK
    length = 57 + len(data)
    padded = data[7:] + b"\x80" + b"\x00" * ((55 - length) % 64)
    padded += struct.pack(">Q", length * 8)
    state = _sha256_init(data[:7])
    for offset in range(0, len(padded), 64):
        words = list(struct.unpack(">16I", padded[offset : offset + 64]))
        _expand_sha256_schedule(words)
        working = _sha256_rounds(state, words)
        state = tuple((x + y) & mask for x, y in zip(state, working))
    return struct.pack(">8I", *state)

def _cs64_digest(data: bytes, digest: bytes) -> Tuple[int, int]:
    """Compute the CS64 digest words for token data."""
    mask = _U32_MASK
    key_a, key_b = struct.unpack_from("<II", digest)
    key_a |= 1
    key_b |= 1
    factors = (
        (key_a * _CS64_FACTOR) & mask,
        (key_b * _CS64_FACTOR) & mask,
    )
    terms = [
        (coefficient * factors[index % 2]) & mask
        for index, (coefficient, _) in enumerate(_CS64_COEFFICIENTS)
    ]
    offsets = [offset for _, offset in _CS64_COEFFICIENTS]
    for index, word in enumerate(_words_le4_even(b"\x00" + data)):
        term = word * (key_a if index % 2 == 0 else key_b)
        offset = _rol16(word) * (0xEF0569FB if index % 2 == 0 else 0xC31713DB)
        if index == 0:
            term += _CS64_ADJUSTMENT0 * factors[0]
            offset += _CS64_ADJUSTMENT1
        terms.append(term & mask)
        offsets.append(offset & mask)
    swap_acc = swap_last = state = acc = 0
    for index in range(0, len(terms), 2):
        x, y = terms[index], terms[index + 1]
        t = _rol16((offsets[index] + x) & mask)
        q = (t * 0x76F50F34) & mask
        swap_acc += (_rol16(q) * 0xC3EFEA97 + q) & mask
        t = _rol16((offsets[index + 1] + y) & mask)
        q = (t * 0x1881CE3C) & mask
        swap_last = (_rol16(q) * 0x35BD1EC9 + q) & mask
        swap_acc = (swap_acc + swap_last) & mask

        state = (state * key_a + x) & mask
        state = (_rol16(state) * 0xCF98B111) & mask
        state = (_rol16(state) * 0x87085B9F) & mask
        state = (_rol16(state) * 0x12CEB96D) & mask
        state = (_rol16(state) * 0x257E1D83) & mask
        acc += state
        t = (state * key_b + y) & mask
        t = (_rol16(t) * 0xA27416F5) & mask
        t = (_rol16(t) * 0xD38396FF) & mask
        state = (_rol16((_rol16(t) * 0x7C932B89) & mask) * 0xBFA49F69) & mask
        acc = (acc + state) & mask
    return swap_last ^ state, swap_acc ^ acc

@lru_cache(maxsize=1)
def _token_hash(data: bytes) -> Tuple[str, str]:
    """Compute the token hash components."""
    digest = _sha256_digest(data)
    cs64 = struct.pack("<II", *_cs64_digest(data, digest)).hex().upper()
    return cs64, digest.hex().upper()

def generate_sec_ms_gec_v2(unix_timestamp: Optional[float] = None) -> str:
    """
    Generates a v2 Sec-MS-GEC token value.

    The token combines CS64 and SHA256 digests in the format
    "<16 hex>-<64 hex>".

    Args:
        unix_timestamp (float): Value to use instead of the current time, for
            testing.

    Returns:
        str: The generated v2 token value.
    """
    if unix_timestamp is None:
        ticks = time.time()
    else:
        ticks = float(unix_timestamp)
    ticks += WIN_EPOCH
    ticks -= ticks % 300
    ticks *= S_TO_NS / 100
    str_to_hash = f"{ticks:.0f}{TRUSTED_CLIENT_TOKEN}".encode("ascii")
    cs64, sha256 = _token_hash(str_to_hash)
    return f"{cs64}-{sha256}"
# END edge-tts upstream DRM helpers

LANGS = ("en", "pt-BR", "fr", "zh-Hans")
VOICES = {"en": "en-US-AndrewMultilingualNeural", "pt-BR": "pt-BR-AntonioNeural"}
RATE = "+0%"
FORMAT = "AUDIO_24KHZ_96KBITRATE_MONO_MP3"
HERE = Path(__file__).resolve().parent
# Reused transport/format from ../narrate.js and ../interactive_v5/narrate_v5.cjs.
# Those scripts are never imported/executed: they have generation side effects.
EDGE_JS = r"""
const fs=require('fs'),path=require('path');
let p, networkAttempted=false, speechSendIntent=false, phase='boot';
function event(name,extra={}){
 phase=name;
 const line=JSON.stringify({phase:name,attempt_id:p.attempt_id??null,time:new Date().toISOString(),network_attempted:networkAttempted,speech_send_intent:speechSendIntent,...extra})+'\n';
 const fd=fs.openSync(p.event_log,'a');
 try {fs.writeSync(fd,line);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}
}
function message(e){
 return String(e?.message||e).replace(/(?:https?|wss?):\/\/[^\s"']+/gi,'[URL_OMITTED]').slice(0,1800);
}
(async()=>{
 p=JSON.parse(fs.readFileSync(0,'utf8'));
 event('local_payload_loaded');
 const {MsEdgeTTS,OUTPUT_FORMAT}=require(path.join(p.modules,'msedge-tts'));
 if(require(path.join(p.modules,'msedge-tts/package.json')).version!=='2.0.7')throw Error('UNREVIEWED_EDGE_CLIENT_VERSION');
 if(!/^[A-F0-9]{16}-[A-F0-9]{64}$/.test(p.gec))throw Error('INVALID_GEC_V2');
 const getSynthUrl=MsEdgeTTS.getSynthUrl;
 MsEdgeTTS.getSynthUrl=async function(){
  const url=new URL(await getSynthUrl.call(MsEdgeTTS));
  if(url.hostname!=='speech.platform.bing.com'||url.pathname!=='/consumer/speech/synthesize/readaloud/edge/v1')throw Error('EDGE_DESTINATION_CHANGED');
  url.searchParams.set('Sec-MS-GEC',p.gec);
  url.searchParams.set('Sec-MS-GEC-Version','2-143.0.3650.96');
  return url.toString();
 };
 const t=new MsEdgeTTS();
 let connectionCount=0;
 const init=t._initClient.bind(t);
 t._initClient=()=>{if(++connectionCount!==1)throw Error('AUTOMATIC_RECONNECT_DISABLED');return init();};
 event('local_dependency_ready',{client:'msedge-tts@2.0.7',gec_version:2});
 try {
  networkAttempted=true;event('metadata_connection_intent');
  await t.setMetadata(p.voice,OUTPUT_FORMAT[p.format]);
  event('metadata_ready');
  t._ws.on('close',(code,reason)=>event('socket_closed',{close_code:code,reason:message(reason.toString())}));
  // Record the actual library request ID durably BEFORE ws.send; never record SSML.
  if(!t._ws || typeof t._ws.send!=='function')throw Error('TRANSPORT_OBSERVABILITY_UNAVAILABLE');
  const originalSend=t._ws.send;
  t._ws.send=function(data,...args){
   const frame=String(data);
   if(frame.includes('Path:ssml')){
    const match=/X-RequestId:([a-f0-9]+)\r?\n/i.exec(frame);
    if(!match)throw Error('REQUEST_ID_UNAVAILABLE_BEFORE_SEND');
    speechSendIntent=true;
    event('speech_send_intent',{request_id:match[1]});
    const result=originalSend.call(this,data,...args);
    event('speech_queued_locally',{request_id:match[1]});
    return result;
   }
   return originalSend.call(this,data,...args);
  };
  const {audioStream}=t.toStream(p.text,{rate:p.rate}),chunks=[];
  let size=0;
  await new Promise((resolve,reject)=>{
   audioStream.on('data',c=>{chunks.push(c);size+=c.length;if(p.partial_audio)fs.appendFileSync(p.partial_audio,c);});
   audioStream.once('end',resolve);audioStream.once('error',reject);
  });
  event('audio_stream_ended',{bytes:size});
  const audio=Buffer.concat(chunks);
  await new Promise((resolve,reject)=>process.stdout.write(audio,e=>e?reject(e):resolve()));
  event('audio_returned_to_parent',{bytes:audio.length});
 }finally{t.close();}
})().catch(e=>{
 const error={name:e?.name||'Error',code:e?.code||null,message:message(e),at_phase:phase};
 try {if(p?.event_log)event('transport_failed',error);}catch{}
 process.stderr.write(JSON.stringify({...error,network_attempted:networkAttempted,speech_send_intent:speechSendIntent})+'\n');
 process.exitCode=1;
});

"""

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def encoded(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n").encode("utf-8")

def io_path(p):
    # Extended Windows paths keep atomic temporaries and diagnostics addressable.
    p = Path(p).absolute()
    if os.name == "nt" and not str(p).startswith("\\\\?\\"):
        value = str(p)
        p = Path("\\\\?\\UNC\\" + value[2:] if value.startswith("\\\\") else "\\\\?\\" + value)
    return p


def read_json(p):
    return json.loads(io_path(p).read_text("utf-8-sig"))

def atomic(p, data):
    p = io_path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp_" + uuid.uuid4().hex)
    try:
        with tmp.open("xb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        require(tmp.stat().st_size == len(data), "SHORT_WRITE")
        os.replace(tmp, p)
    finally:
        if tmp.exists():
            tmp.unlink()

def exclusive(p, data):
    p = io_path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("xb") as f:
        f.write(encoded(data))
        f.flush()
        os.fsync(f.fileno())

def safe_text(text):
    require(isinstance(text, str) and text.strip(), "EMPTY_TEXT")
    require(not re.search(r"[<>{}\r\n]", text), "MARKUP_OR_UNRESOLVED_TOKEN")
    require(not re.search(r"\bconfirm(?:ed|ad[ao]s?|ée?s?|ation|ação)\b|(?:未)?确认", text, re.I), "FORBIDDEN_CREDITATION_WORD")
    return text

def fill(text, values, lang, formats):
    def replacement(m):
        key = m.group(1)
        require(key in values, "MISSING_HUD:" + key)
        val = values[key]
        require(isinstance(val, (str, int, float)) and not isinstance(val, bool), "INVALID_HUD:" + key)
        if isinstance(val, (int, float)):
            require(math.isfinite(val), "NONFINITE_HUD:" + key)
            spec = formats.get(key)
            val = format(val, spec) if spec else (str(int(val)) if val == int(val) else str(val))
            if lang in ("pt-BR", "fr"):
                val = val.replace(".", ",")
        return str(val)
    return safe_text(re.sub(r"\{(\w+)\}", replacement, text))

def validate_templates(t):
    require(t["schema"] == "iald.narration.templates.v7.1", "TEMPLATE_SCHEMA")
    for name, count in (("film1", 9), ("film2", 10)):
        segments = t["films"][name]["segments"]
        require(len(segments) == count, "TEMPLATE_COUNT")
        for s in segments:
            count_cues = len(s["text"]["en"])
            require(count_cues > 0, "NO_CUES")
            for lang in LANGS:
                texts = s["text"][lang]
                require(len(texts) == count_cues, "TRANSLATION_ALIGNMENT")
                for en, text in zip(s["text"]["en"], texts):
                    require(sorted(re.findall(r"\{\w+\}", text)) == sorted(re.findall(r"\{\w+\}", en)), "TRANSLATION_VALUES:" + s["key"])
                    clean = re.sub(r"\{\w+\}", "VALUE", text)
                    safe_text(clean)
                    # Subscript indices in hypothesis labels are identifiers, not measured values.
                    require(not re.search(r"[0-9]", clean), "LITERAL_NUMBER")
                    if "{z_disc}" in text:
                        require("{p_disc}" in text and "{threshold_sigma}" in text, "THRESHOLD_SAME_CUE")

def hud_values(h):
    values = {}
    for item in h["items"]:
        require(item["id"] not in values, "DUPLICATE_HUD_ID")
        values[item["id"]] = item["value"]
    for key, val in h.get("extra", {}).items():
        require(key not in values or values[key] == val, "HUD_EXTRA_CONFLICT:" + key)
        values[key] = val
    for key in ("seal_version", "seal_pin", "seal_timestamp"):
        require(key in h, "MISSING_SEAL_FIELD:" + key)
        values[key] = h[key]
    # Selected fields only. No verdict, console, history or source prose enters text.
    return values

def timeline_rows(film, count, seconds):
    rows = film if isinstance(film, list) else (film.get("chapters", film.get("scenes")) if count == 10 else film.get("scenes", film.get("chapters")))
    require(isinstance(rows, list) and len(rows) == count, "FILM_SCENE_COUNT")
    result, cursor = [], 0.0
    for i, row in enumerate(rows):
        start = float(row.get("start", cursor))
        duration = float(row.get("duration", float(row.get("end", start)) - start))
        end = float(row.get("end", start + duration))
        require(all(math.isfinite(x) for x in (start, end, duration)), "NONFINITE_TIME")
        require(abs(start - cursor) < .001 and duration > .6 and abs(end - start - duration) < .001, "FILM_TIME_CONTRACT")
        result.append({"index": i + 1, "source_key": row.get("key", row.get("id")), "start": start, "end": end, "duration": duration})
        cursor = end
    if isinstance(film, dict):
        for key in ("total_seconds", "duration"):
            if key in film:
                require(abs(float(film[key]) - cursor) < .001, "FILM_TOTAL_CONFLICT")
    if isinstance(film, dict) and "scenes" in film and "chapters" in film:
        other = film["scenes"] if count == 10 else film["chapters"]
        alt = timeline_rows(other, count, seconds)
        require(all(abs(a[k] - z[k]) < .001 for a, z in zip(result, alt) for k in ("start", "end", "duration")), "SCENES_CHAPTERS_TIME_CONFLICT")
    return result


def speech_budget(segment):
    """Planning heuristic, never an Edge duration measurement or a speed command."""
    estimates = {}
    for lang in VOICES:
        text = " ".join(c[lang] for c in segment["cues"])
        numbers = re.findall(r"[+-]?\d+(?:[.,]\d+)?(?:e[+-]?\d+)?", text, re.I)
        lexical = re.sub(r"[+-]?\d+(?:[.,]\d+)?(?:e[+-]?\d+)?", " ", text, flags=re.I)
        units = len(re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:[’'-][A-Za-zÀ-ÖØ-öø-ÿ]+)*", lexical))
        for number in numbers:
            digits = len(re.sub(r"\D", "", number))
            if "e" in number.lower():
                units += digits + 5
            elif "." in number or "," in number:
                units += digits + 2
            else:
                units += 1 if digits < 3 else digits + 2
            if number.startswith("-"):
                units += 1
        # H-subscript labels are spoken as a letter plus its index.
        units += len(re.findall(r"H[₁₂₃]", text))
        overhead = .6 + .25 * max(0, len(segment["cues"]) - 1)
        low, high = units * 60 / 165 + overhead, units * 60 / 130 + overhead
        estimates[lang] = {
            "approximate_spoken_units": units, "estimated_seconds": [round(low, 1), round(high, 1)],
            "scheduled_seconds": segment["duration"], "may_need_extension": high > segment["duration"],
            "recommended_review_seconds": math.ceil(high / 2) * 2,
        }
    return estimates


def make_plan(root, template_path):
    t = read_json(template_path)
    validate_templates(t)
    hp = root / "data/hud.json"
    h = read_json(hp)
    values = hud_values(h)
    require(float(values["z_disc"]) < float(values["threshold_sigma"]), "THRESHOLD_RELATION_CHANGED_REVIEW_NARRATIVE")
    require(values["flags_computed"] + values["flags_literal"] == values["flags"], "FLAG_COUNT_CONFLICT")
    pins = {"hud_sha256": sha(hp.read_bytes()), "template_sha256": sha(template_path.read_bytes()), "builder_sha256": sha(Path(__file__).read_bytes())}
    films = {}
    for name in ("film1", "film2"):
        source = root / ("data/" + name + ".json")
        spec = t["films"][name]
        times = timeline_rows(read_json(source), len(spec["segments"]), spec["segment_seconds"])
        pins[name + "_sha256"] = sha(source.read_bytes())
        segments = []
        for row, s in zip(times, spec["segments"]):
            cues = [{lang: fill(s["text"][lang][j], values, lang, t["formats"]) for lang in LANGS} for j in range(len(s["text"]["en"]))]
            segments.append({**row, "key": s["key"], "title": s["title"], "cues": cues,
                "hud_fields": sorted(set(re.findall(r"\{(\w+)\}", " ".join(s["text"]["en"]))))})
        for segment in segments:
            segment["speech_budget"] = speech_budget(segment)
        films[name] = {"total_seconds": times[-1]["end"], "segments": segments}
    body = {"schema": "iald.narration.plan.v7.1", "pins": pins, "voices": VOICES, "format": FORMAT,
        "rate": RATE, "music": False, "films": films, "formats": t["formats"], "format_scope": "Speech and matching subtitles only; original HUD values untouched.", "budget_method": "Heuristic 130-165 spoken units/minute, numeric expansion allowance and cue margins; not measured Edge duration.", "seal_version": values["seal_version"],
        "seal_pin": values["seal_pin"], "seal_timestamp": values["seal_timestamp"],
        "subtitle_method": "Measured utterance intervals after TTS; planned proportional intervals before TTS.",
        "scope": "Narrative preparation. Kernel implications retain hypotheses. Visual analogies retain ONTO/INPUT."}
    return {**body, "plan_sha256": sha(encoded(body))}

def timecode(t):
    ms = round(t * 1000)
    require(ms >= 0, "NEGATIVE_TIME")
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}.{ms % 1000:03d}"

def vtt(cues, lang):
    last_end = -1
    lines = ["WEBVTT", "Kind: subtitles", "Language: " + lang, ""]
    for i, cue in enumerate(cues):
        require(cue["start"] >= last_end - 1e-6 and cue["end"] > cue["start"], "SUBTITLE_OVERLAP")
        require(round(cue["end"] * 1000) > round(cue["start"] * 1000), "SUBTITLE_ROUNDING_COLLAPSE")
        last_end = cue["end"]
        lines.extend([str(i + 1), timecode(cue["start"]) + " --> " + timecode(cue["end"]), safe_text(cue["text"]), ""])
    return ("\n".join(lines) + "\n").encode("utf-8")

def cache_key(voice, text):
    return sha(encoded({"voice": voice, "text": text, "rate": RATE, "format": FORMAT}))

def cache_status(cache, key):
    receipt, audio = cache / (key + ".json"), cache / (key + ".mp3")
    if not receipt.exists():
        require(not audio.exists() and not (cache / (key + ".transport.jsonl")).exists() and not (cache / (key + ".diagnostic.json")).exists(), "ORPHAN_AUDIO_OR_LOG_REQUIRES_RECONCILIATION:" + key)
        return None
    r = read_json(receipt)
    require(r["key"] == key and r["state"] == "completed", "UNCERTAIN_OR_INFLIGHT_NO_RETRY:" + key)
    require(audio.exists() and sha(audio.read_bytes()) == r["audio_sha256"], "CACHE_INTEGRITY:" + key)
    return audio


def capture_diagnostic(cache, key, result=None, exc=None):
    """Preserve transport evidence before raising; never promote an uncertain result."""
    cache = io_path(cache)
    stderr = getattr(result, "stderr", None) if result is not None else getattr(exc, "stderr", None)
    stdout = getattr(result, "stdout", None) if result is not None else getattr(exc, "stdout", None)
    stderr = stderr.decode("utf-8", "replace") if isinstance(stderr, bytes) else str(stderr or "")
    stderr = re.sub(r"(?:https?|wss?)://[^\s\"']+", "[URL_OMITTED]", stderr, flags=re.I)
    events = []
    event_log = cache / (key + ".transport.jsonl")
    if event_log.exists():
        for line in event_log.read_text("utf-8").splitlines():
            try:
                events.append(json.loads(line))
            except ValueError:
                events.append({"phase": "INCOMPLETE_EVENT"})
    diag = {
        "key": key, "returncode": getattr(result, "returncode", None),
        "exception": type(exc).__name__ if exc else None,
        "stderr_sanitized": stderr, "stdout_bytes": len(stdout or b""),
        "events": events, "retry_allowed": False,
        "boundary": "UNDETERMINED" if not events else
            ("NETWORK_ATTEMPT_RECORDED" if any(e.get("network_attempted") for e in events) else "LOCAL_EVENTS_ONLY"),
        "request_ids": sorted({e["request_id"] for e in events if e.get("request_id")}),
    }
    if stdout:
        received = cache / (key + ".received.mp3")
        atomic(received, stdout)
        diag["received_audio"] = {"file": received.name, "sha256": sha(stdout), "usable": False}
    atomic(cache / (key + ".diagnostic.json"), encoded(diag))
    return diag



def load_retry_authorization(file, cache, approved_plan):
    """Caller supplies the real human approval; this file is not an authentication service."""
    file = Path(file).resolve()
    raw = file.read_bytes()
    require(len(raw) <= 65536, "RETRY_AUTHORIZATION_TOO_LARGE")
    auth = json.loads(raw.decode("utf-8-sig"))
    require(auth.get("schema") == "iald.edge.retry-authorization.v1", "RETRY_AUTHORIZATION_SCHEMA")
    require(auth.get("decision") == "APPROVED" and auth.get("human_response_received") is True, "HUMAN_RETRY_APPROVAL_PENDING")
    require(auth.get("destination") == "Microsoft Edge TTS", "RETRY_DESTINATION")
    require(auth.get("approved_plan_sha256") == approved_plan, "RETRY_PLAN_MISMATCH")
    key = auth.get("uncertain_key", "")
    require(re.fullmatch(r"[a-f0-9]{64}", key) is not None, "RETRY_KEY")
    attempt_id = auth.get("new_attempt_id", "")
    require(str(uuid.UUID(attempt_id)) == attempt_id, "RETRY_ATTEMPT_UUID")
    require(auth.get("voice") in VOICES.values(), "RETRY_VOICE_NOT_AUTHORIZED")
    source = auth.get("human_response_source", {})
    require(isinstance(source.get("path"), str) and source["path"], "HUMAN_RESPONSE_SOURCE_MISSING")
    source_path = (file.parent / source["path"]).resolve()
    require(source_path != file, "AUTHORIZATION_CANNOT_BE_ITS_OWN_HUMAN_SOURCE")
    require(source.get("sha256") == sha(source_path.read_bytes()), "HUMAN_RESPONSE_SOURCE_HASH")
    original = cache / (key + ".json")
    require(original.exists() and sha(original.read_bytes()) == auth.get("original_receipt_sha256"), "ORIGINAL_UNCERTAIN_RECEIPT_CHANGED")
    receipt = read_json(original)
    require(receipt.get("key") == key and receipt.get("state") == "uncertain", "ORIGINAL_NOT_UNCERTAIN")
    require(receipt.get("voice") == auth["voice"] and receipt.get("text_sha256") == auth.get("text_sha256"), "RETRY_ORIGINAL_SCOPE")
    require(not (cache / (key + ".mp3")).exists(), "ORIGINAL_AUDIO_APPEARED_RECONCILE_FIRST")
    previous = auth.get("previous_terminal_attempt")
    if previous is not None:
        prior_path = Path(previous["path"]).resolve()
        require(prior_path.is_relative_to((cache / "attempts" / key).resolve()), "PREVIOUS_ATTEMPT_SCOPE")
        require(sha(io_path(prior_path).read_bytes()) == previous["sha256"], "PREVIOUS_RECONCILIATION_CHANGED")
        outcome = read_json(prior_path)
        require(outcome["status"] == "CONNECTION_REJECTED_HTTP403_BEFORE_SPEECH", "PREVIOUS_NOT_KNOWN_PRE_SPEECH_REJECTION")
        prior_intent = prior_path.parent / (key + ".json")
        require(sha(prior_intent.read_bytes()) == outcome["intent_sha256"], "PREVIOUS_INTENT_CHANGED")
        prior = read_json(prior_intent)
        require(prior["key"] == key and prior["voice"] == auth["voice"] and prior["text_sha256"] == auth["text_sha256"], "PREVIOUS_UNIT_CHANGED")
        require(prior["retry_authorization"]["human_response_source_sha256"] == source["sha256"], "PREVIOUS_HUMAN_SOURCE_CHANGED")
        require(outcome["attempt_id"] == prior["retry_authorization"]["new_attempt_id"] != attempt_id, "PREVIOUS_ATTEMPT_ID")
        log = io_path(prior_path.parent / (key + ".transport.jsonl"))
        require(sha(log.read_bytes()) == outcome["event_log_sha256"], "PREVIOUS_EVENTS_CHANGED")
        events = [json.loads(line) for line in log.read_text("utf8").splitlines()]
        require(events and events[-1]["phase"] == "transport_failed" and "Unexpected server response: 403" in events[-1]["message"], "PREVIOUS_403_EVIDENCE")
        require(all(e.get("speech_send_intent") is False and e["phase"] in {"local_payload_loaded", "local_dependency_ready", "metadata_connection_intent", "transport_failed"} for e in events), "PREVIOUS_SPEECH_OR_UNKNOWN_EVENT")
        require(not (prior_path.parent / (key + ".mp3")).exists(), "PREVIOUS_AUDIO_PRESENT")
    return {"authorization": auth, "file": str(file), "file_sha256": sha(raw),
        "source_path": str(source_path), "source_sha256": source["sha256"]}


def retry_attempt_cache(cache, context, voice, text, approved_plan):
    auth = context["authorization"]
    # Re-read all authorization/source/original bytes at the actual unit boundary.
    current = load_retry_authorization(context["file"], cache, approved_plan)
    require(current == context, "RETRY_AUTHORIZATION_CHANGED")
    key = cache_key(voice, text)
    require(key == auth["uncertain_key"] and voice == auth["voice"] and sha(text.encode()) == auth["text_sha256"], "RETRY_UNIT_SCOPE")
    binding = {"uncertain_key": key, "new_attempt_id": auth["new_attempt_id"],
        "authorization_sha256": context["file_sha256"],
        "human_response_source_sha256": context["source_sha256"],
        "original_receipt_sha256": auth["original_receipt_sha256"],
        "approved_plan_sha256": approved_plan}
    parent = cache / "attempts" / key
    # One approval evidence file binds to one new attempt for this original key.
    previous = auth.get("previous_terminal_attempt")
    claim = parent / (("continuation_" + previous["sha256"]) if previous else ("authorization_" + context["source_sha256"]))
    claim = claim.with_suffix(".json")
    try:
        exclusive(claim, binding)
    except FileExistsError:
        require(read_json(claim) == binding, "AUTHORIZATION_ALREADY_BOUND_TO_ANOTHER_ATTEMPT")
    attempt = parent / auth["new_attempt_id"]
    require(attempt.resolve().is_relative_to(cache.resolve()), "RETRY_CACHE_ESCAPE")
    receipt = attempt / (key + ".json")
    if receipt.exists():
        require(read_json(receipt).get("retry_authorization") == binding, "ATTEMPT_BINDING_MISMATCH")
    return attempt, binding


def cached_tts(cache, voice, text, approval, modules, node, retry_authorization=None, attempt_metadata=None):
    key = cache_key(voice, text)
    retry_binding = None
    if retry_authorization is None and attempt_metadata is None:
        reusable = completed_cached_audio(cache, key)
        if reusable:
            return reusable
    if retry_authorization is not None and retry_authorization["authorization"]["uncertain_key"] == key:
        cache, retry_binding = retry_attempt_cache(cache, retry_authorization, voice, text, approval)
    hit = cache_status(cache, key)
    if hit:
        return hit
    receipt, audio = cache / (key + ".json"), cache / (key + ".mp3")
    intent = {"key": key, "state": "intent", "voice": voice, "text_sha256": sha(text.encode()),
        "approval_plan_sha256": approval, "started_at": time.time()}
    if retry_binding is not None:
        intent["retry_authorization"] = retry_binding
    if attempt_metadata is not None:
        intent["bounded_attempt"] = attempt_metadata
    # O_EXCL serializes concurrent attempts; fsync occurs before the child or network exists.
    exclusive(receipt, intent)
    result = None
    try:
        payload = {"gec": generate_sec_ms_gec_v2(time.time()), "modules": str(modules), "voice": voice, "text": text, "format": FORMAT, "rate": RATE, "event_log": str(cache / (key + ".transport.jsonl")), "attempt_id": attempt_metadata["attempt_id"] if attempt_metadata else (retry_binding["new_attempt_id"] if retry_binding else None), "partial_audio": str(cache / (key + ".partial.mp3"))}
        result = subprocess.run([node, "-e", EDGE_JS], input=encoded(payload), capture_output=True, timeout=120,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        if result.returncode != 0 or not result.stdout:
            capture_diagnostic(cache, key, result=result)
        require(result.returncode == 0 and len(result.stdout) > 0, "EDGE_TRANSPORT_FAILED")
        atomic(audio, result.stdout)
        atomic(receipt, encoded({**intent, "state": "completed", "audio_sha256": sha(result.stdout),
            "bytes": len(result.stdout), "finished_at": time.time()}))
        return audio
    except BaseException as exc:
        diagnostic_error = None
        try:
            capture_diagnostic(cache, key, result=result, exc=exc)
        except Exception as diagnostic_exc:
            diagnostic_error = type(diagnostic_exc).__name__
        atomic(receipt, encoded({**intent, "state": "uncertain", "reason": type(exc).__name__, "retry_allowed": False,
            "diagnostic": key + ".diagnostic.json", "event_log": key + ".transport.jsonl", "diagnostic_write_error": diagnostic_error}))
        raise


class PendingUtterance(ValueError):
    pass


def load_bounded_authorization(file):
    file = Path(file).resolve()
    raw = file.read_bytes()
    auth = json.loads(raw.decode("utf-8-sig"))
    require(auth.get("status") == "AUTHORIZED_BY_HUMAN" and auth.get("origin") == "direct_user_reply_this_thread", "BOUNDED_HUMAN_SOURCE")
    require(auth.get("answer_verbatim") == "Autorizar até duas tentativas por fala" and auth.get("maximum_new_attempts_per_failed_utterance") == 2, "BOUNDED_LIMIT_NOT_AUTHORIZED")
    return {"file": str(file), "sha256": sha(raw), "limit": 2}


def completed_cached_audio(cache, key):
    paths = [cache / (key + ".json")]
    for folder in (cache / "attempts" / key, cache / "bounded"):
        if folder.exists():
            paths.extend(io_path(folder).rglob(key + ".json"))
    for receipt in paths:
        if receipt.exists() and read_json(receipt).get("state") == "completed":
            return cache_status(receipt.parent, key)
    return None


def bounded_tts(cache, voice, text, approval, modules, node, context):
    require(voice in VOICES.values(), "BOUNDED_VOICE")
    require(load_bounded_authorization(context["file"]) == context, "BOUNDED_AUTHORIZATION_CHANGED")
    key = cache_key(voice, text)
    hit = completed_cached_audio(cache, key)
    if hit:
        return hit
    original = cache / (key + ".json")
    if not original.exists():
        try:
            return cached_tts(cache, voice, text, approval, modules, node)
        except Exception:
            if not original.exists() or read_json(original).get("state") != "uncertain":
                raise
    elif read_json(original).get("state") != "uncertain":
        raise PendingUtterance("BASE_INFLIGHT_OR_INVALID:" + key)
    for number in range(1, context["limit"] + 1):
        folder = cache / "bounded" / context["sha256"][:16] / key[:16] / str(number)
        slot = folder / "attempt.json"
        binding = {"key": key, "voice": voice, "text_sha256": sha(text.encode()),
            "authorization_sha256": context["sha256"], "attempt_number": number}
        candidate = {**binding, "attempt_id": str(uuid.uuid4())}
        try:
            exclusive(slot, candidate)
            descriptor = candidate
        except FileExistsError:
            descriptor = read_json(slot)
            require(all(descriptor.get(k) == v for k, v in binding.items()), "BOUNDED_SLOT_COLLISION")
        receipt = folder / (key + ".json")
        if receipt.exists():
            state = read_json(receipt)
            require(state.get("bounded_attempt") == descriptor, "BOUNDED_RECEIPT_BINDING")
            if state["state"] == "completed":
                return cache_status(folder, key)
            if state["state"] == "uncertain":
                continue
            raise PendingUtterance("BOUNDED_ATTEMPT_INFLIGHT:" + key)
        try:
            return cached_tts(folder, voice, text, approval, modules, node, attempt_metadata=descriptor)
        except Exception:
            if not receipt.exists() or read_json(receipt).get("state") != "uncertain":
                raise
    raise PendingUtterance("BOUNDED_ATTEMPTS_EXHAUSTED:" + key)


def run_ff(ff, args):
    r = subprocess.run([str(ff), *map(str, args)], capture_output=True, timeout=240,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    require(r.returncode == 0, "FFMPEG_FAILED:" + r.stderr.decode("utf-8", "replace")[-1200:])
    return r.stderr.decode("utf-8", "replace")

def wav_duration(p):
    with wave.open(str(p), "rb") as w:
        require(w.getnframes() > 0, "EMPTY_WAV")
        return w.getnframes() / w.getframerate()

def loud_measure(ff, file):
    stderr = run_ff(ff, ["-hide_banner", "-nostats", "-i", file, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    blocks = re.findall(r'\{\s*"input_i"[\s\S]*?\}', stderr)
    require(blocks, "NO_LOUDNESS_MEASUREMENT")
    m = json.loads(blocks[-1])
    require(math.isfinite(float(m["input_i"])), "INVALID_LOUDNESS")
    return m

def normalize(ff, source, destination):
    before = loud_measure(ff, source)
    fields = {"measured_I": "input_i", "measured_TP": "input_tp", "measured_LRA": "input_lra", "measured_thresh": "input_thresh", "offset": "target_offset"}
    f = "loudnorm=I=-16:TP=-1.5:LRA=11:linear=true:" + ":".join(k + "=" + before[v] for k, v in fields.items())
    run_ff(ff, ["-y", "-hide_banner", "-i", source, "-af", f, "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", destination])
    after = loud_measure(ff, destination)
    require(abs(float(after["input_i"]) + 16) <= 1, "LUFS_OUT_OF_RANGE")
    return {"before": before, "after": after, "sha256": sha(destination.read_bytes())}

def build(plan, root, enable_tts=False, approval=None, node="node", ffmpeg=None, retry_authorization=None, bounded_authorization=None, cache_only=False):
    require(not enable_tts or cache_only or approval == plan["plan_sha256"], "EXACT_PLAN_APPROVAL_REQUIRED")
    if cache_only:
        approval = plan["plan_sha256"]
    modules = Path('C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\video_um\\node_modules')
    cache = root / "audio/cache"
    retry_context = None
    if retry_authorization is not None:
        require(enable_tts, "RETRY_AUTHORIZATION_REQUIRES_EXPLICIT_TTS")
        retry_context = load_retry_authorization(retry_authorization, cache, approval)
        public_keys = {cache_key(voice, cue[lang]) for film in plan["films"].values() for segment in film["segments"] for cue in segment["cues"] for lang, voice in VOICES.items()}
        require(retry_context["authorization"]["uncertain_key"] in public_keys, "RETRY_KEY_NOT_IN_CURRENT_PUBLIC_PLAN")
    ff = ffmpeg
    if enable_tts:
        if not ff:
            r = subprocess.run([node, "-e", "process.stdout.write(require(process.argv[1]).path)", str(modules / "@ffmpeg-installer/ffmpeg")], capture_output=True, check=True, timeout=20)
            ff = r.stdout.decode().strip()
        require(Path(ff).is_file(), "FFMPEG_MISSING")
        # Check dependency resolution before any intent/network operation.
        subprocess.run([node, "-e", "require.resolve(process.argv[1])", str(modules / "msedge-tts")], capture_output=True, check=True, timeout=20)
    resolved, pending = {}, {}
    if bounded_authorization is not None or cache_only:
        require(enable_tts and retry_authorization is None, "BOUNDED_REQUIRES_TTS_AND_NO_SINGLE_RETRY")
        context = load_bounded_authorization(bounded_authorization) if bounded_authorization is not None else None
        units = {}
        for film in plan["films"].values():
            for segment in film["segments"]:
                for cue in segment["cues"]:
                    for lang, voice in VOICES.items():
                        units[cache_key(voice, cue[lang])] = (voice, cue[lang])
        for key, (voice, text) in units.items():
            try:
                if cache_only:
                    hit = completed_cached_audio(cache, key)
                    require(hit is not None, "CACHE_ONLY_MISSING:" + key)
                    resolved[key] = hit
                else:
                    resolved[key] = bounded_tts(cache, voice, text, approval, modules, node, context)
            except Exception as exc:
                pending[key] = {"voice": voice, "reason": str(exc)}
            atomic(root / "audio/NARRATION_PROGRESS.json", encoded({"plan_sha256": approval, "total_unique_units": len(units), "completed": len(resolved), "pending": pending, "processed": len(resolved) + len(pending), "authorization_sha256": context["sha256"] if context else None, "cache_only": cache_only}))
    reports = {}
    for name in plan["films"]:
        prior = root / "data" / (name + "_narration_timeline.json")
        if prior.exists() and not enable_tts:
            require(read_json(prior).get("status") != "AUDIO_MEASURED", "REFUSE_DOWNGRADE_MEASURED_AUDIO")
    atomic(root / "audio/NARRATION_BUILD.json", encoded({"status": "BUILDING", "plan_sha256": plan["plan_sha256"], "tts": enable_tts and not cache_only}))
    for name, film in plan["films"].items():
        film_keys = {cache_key(voice, cue[lang]) for segment in film["segments"] for cue in segment["cues"] for lang, voice in VOICES.items()}
        missing = sorted(film_keys.intersection(pending))
        if missing:
            reports[name] = {"status": "PENDING_AUDIO_UNITS", "keys": missing}
            continue
        timing_by_voice, mixes = {}, {}
        for language, voice in VOICES.items():
            cues, clips = [], []
            for segment in film["segments"]:
                room = segment["duration"] - .6
                if enable_tts:
                    segment_clips = []
                    for cue in segment["cues"]:
                        text = cue[language]
                        mp3 = resolved[cache_key(voice, text)] if bounded_authorization is not None or cache_only else cached_tts(cache, voice, text, approval, modules, node, retry_context)
                        wav = io_path(root / "audio" / "decoded" / (cache_key(voice, text) + ".wav")); wav.parent.mkdir(parents=True, exist_ok=True)
                        run_ff(ff, ["-y", "-hide_banner", "-loglevel", "error", "-i", mp3, "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", wav])
                        segment_clips.append({"file": wav, "duration": wav_duration(wav)})
                    durations = [c["duration"] for c in segment_clips]
                    require(sum(durations) <= room, f"NARRATION_TOO_LONG_REVISE_TEXT_NO_SPEEDUP:{name}:{segment['index']}:{language}")
                    clips.extend(segment_clips)
                else:
                    lengths = [len(c[language]) for c in segment["cues"]]
                    durations = [room * n / sum(lengths) for n in lengths]
                gap = max(0, room - sum(durations)) / max(1, len(durations) - 1)
                at = segment["start"] + .3
                for cue, duration in zip(segment["cues"], durations):
                    cues.append({"scene": segment["index"], "start": at, "end": at + duration, "text": cue[language], "translations": cue})
                    at += duration + gap
            timing_by_voice[language] = cues
            if enable_tts:
                outdir = root / "audio" / name
                outdir.mkdir(parents=True, exist_ok=True)
                raw, wav, aac = [outdir / (language + suffix) for suffix in (".mix.wav", ".wav", ".m4a")]
                args = ["-y", "-hide_banner", "-loglevel", "error", "-f", "lavfi", "-t", str(film["total_seconds"]), "-i", "anullsrc=r=48000:cl=mono"]
                for clip in clips:
                    args.extend(["-i", clip["file"]])
                filters = [f"[{i+1}:a]adelay={round(cues[i]['start']*1000)},apad[a{i}]" for i in range(len(clips))]
                filters.append("[0:a]" + "".join(f"[a{i}]" for i in range(len(clips))) + f"amix=inputs={len(clips)+1}:duration=first:dropout_transition=0,volume={len(clips)+1}[out]")
                args.extend(["-filter_complex", ";".join(filters), "-map", "[out]", "-c:a", "pcm_s16le", raw])
                run_ff(ff, args)
                mixes[language] = normalize(ff, raw, wav)
                require(abs(wav_duration(wav) - film["total_seconds"]) < .05, "MIX_DURATION")
                run_ff(ff, ["-y", "-hide_banner", "-loglevel", "error", "-i", wav, "-c:a", "aac", "-b:a", "160k", aac])
                m = loud_measure(ff, aac)
                require(abs(float(m["input_i"]) + 16) <= 1, "AAC_LUFS_OUT_OF_RANGE")
                mixes[language]["aac"] = {"sha256": sha(aac.read_bytes()), "measurement": m}
        subs = root / "subs" / name.replace("film", "filme")
        for lang in LANGS:
            base = timing_by_voice["pt-BR" if lang == "pt-BR" else "en"]
            atomic(subs / (lang + ".vtt"), vtt([{**c, "text": c["translations"][lang]} for c in base], lang))
        # Each audio track also has a full set of synchronized translations.
        for voice_lang, base in timing_by_voice.items():
            for lang in LANGS:
                atomic(subs / ("sync-" + voice_lang) / (lang + ".vtt"), vtt([{**c, "text": c["translations"][lang]} for c in base], lang))
        atomic(subs / "chapters.vtt", vtt([{"start": s["start"], "end": s["end"], "text": s["title"]["en"]} for s in film["segments"]], "en"))
        tl = {"schema": "iald.narration.timeline.v7.1", "plan_sha256": plan["plan_sha256"], "total_seconds": film["total_seconds"],
            "status": "AUDIO_MEASURED" if enable_tts else "PLANNED_NO_AUDIO", "music": False, "speedup": False,
            "voices": VOICES, "segments": film["segments"], "cues": timing_by_voice, "loudness": mixes}
        atomic(root / "data" / (name + "_narration_timeline.json"), encoded(tl))
        reports[name] = {"status": tl["status"], "loudness": mixes}
    atomic(root / "audio/NARRATION_BUILD.json", encoded({"status": "PARTIAL_PENDING_UNITS" if pending else "COMPLETED", "plan_sha256": plan["plan_sha256"], "tts": enable_tts and not cache_only, "reports": reports, "pending": pending, "tts_inflight": False}))

def self_test(t):
    tests = []
    def check(name, fn):
        fn()
        tests.append(name)
    def rejects(fn):
        try:
            fn()
        except (ValueError, KeyError):
            return
        raise AssertionError("EXPECTED_REFUSAL")
    check("counts / aligned translations / no literal numeric values / same-cue thresholds", lambda: validate_templates(t))
    check("missing HUD refuses", lambda: rejects(lambda: fill("{beta}", {}, "en", {})))
    check("NaN refuses", lambda: rejects(lambda: fill("{beta}", {"beta": float("nan")}, "en", {})))
    check("markup refuses", lambda: rejects(lambda: fill("{beta}", {"beta": "<speak>"}, "en", {})))
    check("rounding carry", lambda: require(timecode(59.9999) == "00:01:00.000", "TIME"))
    check("overlap refuses", lambda: rejects(lambda: vtt([{"start": 0, "end": 2, "text": "a"}, {"start": 1, "end": 3, "text": "b"}], "en")))
    check("zero duration refuses", lambda: rejects(lambda: timeline_rows([{"start": 0, "duration": 0}], 1, 16)))
    check("coordinator extended duration accepted", lambda: timeline_rows([{"start": 0, "duration": 36}], 1, 24))
    check("divergent schedule aliases refuse", lambda: rejects(lambda: timeline_rows({"scenes":[{"start":0,"duration":16}],"chapters":[{"start":0,"duration":24}]},1,16)))
    check("nine-scene schedule", lambda: timeline_rows([{"start": i*16, "duration": 16} for i in range(9)], 9, 16))
    check("ten-chapter schedule", lambda: timeline_rows([{"start": i*24, "duration": 24} for i in range(10)], 10, 24))
    check("cache key binds voice", lambda: require(cache_key(VOICES["en"], "a") != cache_key(VOICES["pt-BR"], "a"), "CACHE"))
    check("cache key binds text", lambda: require(cache_key(VOICES["en"], "a") != cache_key(VOICES["en"], "b"), "CACHE"))
    check("TTS requires exact approval", lambda: rejects(lambda: build({"plan_sha256": "unit-test"}, Path("."), True, "different")))
    return {"status": "PASS", "checks": tests, "network_calls": 0, "scope": "Pure in-memory mechanics; scientific data tested separately against real HUD."}

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", choices=["plan", "build", "self-test"])
    p.add_argument("--root", type=Path, default=HERE.parent)
    p.add_argument("--templates", type=Path, default=HERE / "script_templates.json")
    p.add_argument("--tts", action="store_true")
    p.add_argument("--cache-only", action="store_true", help="Rebuild only from verified completed voice/text caches; never send network or read approval files.")
    p.add_argument("--approved-plan-sha256")
    p.add_argument("--retry-authorization", type=Path, help="Explicit human-approved retry file; one uncertain key and one new attempt UUID.")
    p.add_argument("--bounded-retry-authorization", type=Path)
    p.add_argument("--node", default="node")
    p.add_argument("--ffmpeg")
    a = p.parse_args()
    require(a.retry_authorization is None or (a.command == "build" and a.tts), "RETRY_AUTHORIZATION_ONLY_FOR_EXPLICIT_TTS_BUILD")
    require(a.bounded_retry_authorization is None or (a.command == "build" and a.tts and a.retry_authorization is None), "BOUNDED_ONLY_FOR_EXPLICIT_TTS_BUILD")
    require(not a.cache_only or (a.command == "build" and not a.tts and a.retry_authorization is None and a.bounded_retry_authorization is None), "CACHE_ONLY_ARGUMENTS")
    if a.command == "self-test":
        result = self_test(read_json(a.templates))
    else:
        plan = make_plan(a.root.resolve(), a.templates.resolve())
        if a.command == "plan":
            require(not a.tts, "PLAN_NEVER_SENDS_TTS")
            result = plan
        else:
            build(plan, a.root.resolve(), a.tts or a.cache_only, a.approved_plan_sha256, a.node, a.ffmpeg, a.retry_authorization, a.bounded_retry_authorization, a.cache_only)
            result = {"status": "BUILT", "plan_sha256": plan["plan_sha256"], "tts": a.tts}
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("REFUSED: " + str(exc), file=sys.stderr)
        sys.exit(1)
