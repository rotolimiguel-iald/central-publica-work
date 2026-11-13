from b_lib import *
import re
old = rd(NOS + r"\um_absoluto_pt.txt"); new = pt()
for nm, tx in (("old", old), ("new", new)):
    print(nm, "count '$--, --, --$':", tx.count("$--, --, --$"), " '--, --' :", len(re.findall(r"\$--(?:, --)*\$", tx)))
i = new.index("$--, --, --$"); print(new[i-900:i+120])
# interface_is_light in core old/new
co = json.loads(rd(NOS + r"\um_absoluto.json"))["core"]; cn = core()["core"]
for k in ("interface_is_light",):
    for nm, c in (("old", co), ("new", cn)):
        v = c[k]; print(nm, k, {x: (v[x] if not isinstance(v[x], (dict, list)) else "..") for x in list(v)[:12]})
