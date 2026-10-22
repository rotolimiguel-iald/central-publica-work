"""Load server-owned measured memory; no client paths or provider credentials."""
from dataclasses import dataclass
from pathlib import Path
import hashlib
import json
from claude_profiles import HAIKU, profile_for, context_budget
from claude_request_guard import MemoryMeasurement
from iald_release_binding import load_release, check_package_binding

@dataclass(frozen=True)
class MemoryPackage:
    prefix: str
    measurement: MemoryMeasurement
    reserved_output_tokens: int
    available_dynamic_tokens: int
    tools_sha256: str

def load_package(directory, *, canonical_manifest=None, source_sha=None, expected_model=None):
    """The configured directory must be operator/server controlled, never HTTP input.

    Hashes detect drift, not malicious replacement of both manifest and data.
    Request/profile/tool-result counts must still be checked before every send.
    """
    profile = profile_for(expected_model or HAIKU.model)
    root=Path(directory).resolve()
    # Legacy fixtures must supply a staged canonical manifest. Production never
    # accepts an unbound package, even when its old prefix hash is still valid.
    if canonical_manifest is None:
        canonical_manifest = Path(__file__).with_name('iald_nucleo_fixo.json')
    release = load_release(canonical_manifest, source_sha=source_sha)
    manifest_path=root/'manifest.json'
    manifest_raw=manifest_path.read_bytes()
    manifest=json.loads(manifest_raw)
    if not isinstance(manifest,dict):
        raise ValueError('Memory manifest must be an object')
    if manifest.get('schema')!='iald.claude.memory.v1' or manifest.get('model')!=profile.model:
        raise ValueError('Unknown memory package schema or model')
    if manifest.get('prefix_file')!='prefix.md':
        raise ValueError('Only the fixed package prefix is allowed')
    prefix_path=root/'prefix.md'
    if prefix_path.resolve().parent!=root:
        raise ValueError('Memory path leaves package directory')
    raw=prefix_path.read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=manifest.get('prefix_sha256'):
        raise ValueError('Memory changed since provider measurement')
    b=manifest['budget']
    if not isinstance(b,dict):
        raise ValueError('Memory budget must be an object')
    if b.get('reserved_output_tokens')!=profile.default_output or b.get('margin_tokens')!=1024:
        raise ValueError('Manifest differs from the reserved Haiku output/margin policy')
    checked=context_budget(profile.model,counted_model=profile.model,
        permanent_tokens=b['permanent_tokens'],request_input_tokens=b['request_input_tokens'],
        reserved_output_tokens=b['reserved_output_tokens'],margin_tokens=b['margin_tokens'])
    if checked!=b or not checked['ready'] or checked['remaining_tokens']<10000:
        raise ValueError('Memory lacks the planned conversation reserve')
    tools_hash=manifest.get('tools_sha256')
    if not isinstance(tools_hash,str) or len(tools_hash)!=64 or any(c not in '0123456789abcdef' for c in tools_hash):
        raise ValueError('Missing measured tool identity')
    if manifest_path.read_bytes()!=manifest_raw or prefix_path.read_bytes()!=raw:
        raise ValueError('Package changed during loading')
    check_package_binding(manifest, release)
    return MemoryPackage(raw.decode('utf-8'),MemoryMeasurement(profile.model,digest,b['permanent_tokens']),
                         b['reserved_output_tokens'],b['remaining_tokens'],tools_hash)
