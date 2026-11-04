# sonda do runtime pinado do WSL (/opt/lal_env): so versoes; nenhum dado
import json, sys
from importlib import metadata
pk = ["bilby", "dynesty", "lalsuite", "numpy", "scipy", "h5py", "gwpy", "astropy"]
out = {"python": ".".join(map(str, sys.version_info[:3])), "pacotes": {}}
for p in pk:
    try:
        out["pacotes"][p] = metadata.version(p)
    except metadata.PackageNotFoundError:
        out["pacotes"][p] = None
import lalsimulation as ls
out["lalsimulation_modulo"] = getattr(ls, "__version__", None)
print(json.dumps(out, sort_keys=True))
