"""Legacy endpoint alias to the corrected self-contained F7.2 inventory.

The old implementation survives in baseline custody, not as a competing live
table. The served contract and requested endpoint are explicit in the result.
"""
from .neutrino_canal_v2 import FonteRecusada, MANIFEST, canal as _current

def canal(manifest_path=MANIFEST):
    result = _current(manifest_path=manifest_path)
    return {**result, "requested_endpoint":"neutrino_canal_f72", "legacy_alias":True}
