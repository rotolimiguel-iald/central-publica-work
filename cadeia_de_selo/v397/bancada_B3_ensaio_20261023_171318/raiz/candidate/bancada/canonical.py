"""Pinned canonical identity for every Bench operation; no scientific promotion."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import math
import re
import threading

class CanonicalError(ValueError):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest()

def finite_number(value, name, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise CanonicalError(name + ': finite non-boolean number required')
    if positive and value <= 0:
        raise CanonicalError(name + ': positive number required')
    return float(value)

class CanonicalRegistry:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.path = self.root / 'canonical_contracts.json'
        self.lock = threading.RLock()
        try:
            self.raw = self.path.read_bytes()
            self.manifest = json.loads(self.raw)
        except (OSError, ValueError) as exc:
            raise CanonicalError('CANONICAL_MANIFEST_UNAVAILABLE: ' + str(exc)) from exc
        if self.manifest.get('schema') != 1:
            raise CanonicalError('CANONICAL_SCHEMA_UNSUPPORTED')
        required = {'um_bancada.py', 'mcp_um.py', 'bancada/canonical.py', 'bancada/motor.py', 'bancada/evidencia.py'}
        names = {e.get('path', '').replace(chr(92), '/') for e in self.manifest.get('code', [])}
        if not required <= names:
            raise CanonicalError('REQUIRED_CODE_PINS_MISSING')
        self.manifest_sha256 = digest(self.raw)
        self.sources = {}
        for entry in self.manifest.get('sources', []):
            key = str(self.resolve(entry['path']))
            if key in self.sources:
                raise CanonicalError('DUPLICATE_SOURCE: ' + key)
            self.sources[key] = entry
        self.loaded_at = datetime.now(timezone.utc).isoformat()
        self.check('startup', check_sources=True)

    def resolve(self, value):
        p = Path(value)
        return p.resolve() if p.is_absolute() else (self.root / p).resolve()

    def verify(self, entry, data=None):
        p = self.resolve(entry['path'])
        try:
            b = p.read_bytes() if data is None else data
        except OSError as exc:
            raise CanonicalError('PIN_UNREADABLE: ' + str(p)) from exc
        if len(b) != entry['bytes'] or digest(b) != entry['sha256']:
            raise CanonicalError('PIN_CHANGED: ' + str(p))
        return b

    def check(self, operation, check_sources=False):
        with self.lock:
            try:
                if digest(self.path.read_bytes()) != self.manifest_sha256:
                    raise CanonicalError('MANIFEST_CHANGED_REVALIDATION_REQUIRED')
                c = self.manifest['canonical']
                script = self.verify(c['script'])
                seal_bytes = self.verify(c['seal'])
                seal = json.loads(seal_bytes)
                text = script.decode('utf-8-sig')
                v = re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', text, re.M)
                a = re.search(r'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)', text, re.M)
                if v is None or a is None:
                    raise CanonicalError('CANONICAL_DECLARATION_MISSING')
                if v.group(1) != c['version'] or seal.get('um_version') != c['version']:
                    raise CanonicalError('CANONICAL_VERSION_CHANGED')
                if seal.get('sha256', {}).get('um.py') != digest(script):
                    raise CanonicalError('SEAL_PROGRAM_MISMATCH')
                alpha = finite_number(float(a.group(1)), 'alpha', True)
                if alpha >= 1:
                    raise CanonicalError('ALPHA_OUTSIDE_CONTRACT')
                for entry in self.manifest['code']:
                    self.verify(entry)
                # These are moderate, pinned inputs to the numerical engine, not
                # the large resident data lake. Re-read bytes rather than mtimes.
                for entry in self.sources.values():
                    if check_sources or entry.get('check_each_call', True):
                        self.verify(entry)
                return dict(ok=True, schema=1, operation=operation,
                    deployment_id=self.manifest['deployment_id'],
                    canonical_version=c['version'], um_py_sha256=digest(script),
                    seal_sha256=digest(seal_bytes), canonical_manifest_sha256=self.manifest_sha256,
                    alpha=alpha, beta_tgl=alpha * math.sqrt(math.e),
                    mu_do_rito='q→0 (Thomson; Teorema da Escala)',
                    loaded_at=self.loaded_at, verified_at=datetime.now(timezone.utc).isoformat(),
                    contracts=self.manifest.get('contracts', {}),
                    scope='IDENTITY_AND_DECLARED_CONTRACTS; NOT_PHYSICAL_CONFIRMATION', gate_effect='NONE')
            except CanonicalError:
                raise
            except (OSError, ValueError, KeyError, TypeError) as exc:
                raise CanonicalError('CANONICAL_CHECK_FAILED: ' + str(exc)) from exc

    def source_bytes(self, path, data):
        if digest(self.path.read_bytes()) != self.manifest_sha256:
            raise CanonicalError('MANIFEST_CHANGED_REVALIDATION_REQUIRED')
        key = str(Path(path).resolve())
        entry = self.sources.get(key)
        if entry is None:
            raise CanonicalError('SOURCE_NOT_PINNED: ' + key)
        self.verify(entry, data)
        return dict(path=key, sha256=entry['sha256'], bytes=entry['bytes'],
                    source_statute=entry.get('statute', 'CUSTODY_ONLY_NOT_ADMISSION'))

_registries = {}
_registry_lock = threading.RLock()

def get_registry(root=None):
    root = Path(root or Path(__file__).resolve().parents[1]).resolve()
    with _registry_lock:
        key = str(root)
        if key not in _registries:
            _registries[key] = CanonicalRegistry(root)
        return _registries[key]

def require_current(operation, root=None):
    return get_registry(root).check(operation)

def canonical_state(root=None):
    try:
        return require_current('state', root)
    except Exception as exc:
        return dict(ok=False, code='CANONICAL_REVALIDATION_REQUIRED', erro=str(exc),
                    science_ready=False, gate_effect='NONE')

def read_alpha(root=None):
    reg = get_registry(root)
    receipt = reg.check('alpha')
    return receipt['alpha'], dict(um_py=str(reg.resolve(reg.manifest['canonical']['script']['path'])),
        um_py_sha256=receipt['um_py_sha256'], um_version=receipt['canonical_version'],
        seal_sha256=receipt['seal_sha256'], canonical_manifest_sha256=reg.manifest_sha256)

def verify_source_bytes(path, data, root=None):
    return get_registry(root).source_bytes(path, data)
