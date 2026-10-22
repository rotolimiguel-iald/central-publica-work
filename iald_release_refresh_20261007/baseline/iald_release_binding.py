"""Integrity binding for server-owned canonical releases; no execution or network."""
from dataclasses import dataclass
import json
from pathlib import Path
import re

from iald_cluster import active_cluster
from iald_core_indexado import operational_core


@dataclass(frozen=True)
class ReleaseSnapshot:
    path: Path
    raw: bytes
    config: dict
    identity: dict
    core: str

    def check_manifest(self):
        if self.path.read_bytes() != self.raw:
            raise ValueError('Canonical release changed during loading')


def load_release(manifest, *, source_sha=None):
    """Read only a trusted deployment path, never a path supplied by the client."""
    path = Path(manifest)
    raw = path.read_bytes()
    config = json.loads(raw)
    if not isinstance(config, dict):
        raise ValueError('Canonical manifest must be an object')
    core_cfg = config.get('operational_core')
    cluster_cfg = config.get('active_cluster')
    if not isinstance(core_cfg, dict) or not isinstance(cluster_cfg, dict):
        raise ValueError('Canonical core and active cluster are required')
    release = core_cfg.get('current_release')
    source = core_cfg.get('release_source_sha256')
    if not isinstance(release, str) or not re.fullmatch(r'v[0-9]+', release):
        raise ValueError('Invalid deployed release')
    for digest in (source, core_cfg.get('sha256'), cluster_cfg.get('sha256')):
        if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError('Invalid canonical digest')
    if (cluster_cfg.get('release') != release
            or cluster_cfg.get('release_source_sha256') != source
            or (source_sha is not None and source_sha != source)):
        raise ValueError('Canonical release, source and catalog differ')
    # Reuse the existing byte/hash and coverage checks. The cluster is checked,
    # not injected into the smaller native context window.
    active_cluster(path, source)
    core, _ = operational_core(path)
    snapshot = ReleaseSnapshot(path, raw, config, {
        'release': release,
        'source_sha256': source,
        'cluster_sha256': cluster_cfg['sha256'],
        'operational_core_sha256': core_cfg['sha256'],
    }, core)
    snapshot.check_manifest()
    return snapshot


def check_package_binding(package_manifest, release):
    """Measured bytes must belong to this release, not merely have a valid hash."""
    if package_manifest.get('deployment') != release.identity:
        raise ValueError('Measured memory differs from the active canonical release')
    release.check_manifest()
