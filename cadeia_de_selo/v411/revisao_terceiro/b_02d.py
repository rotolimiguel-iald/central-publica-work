from b_lib import *
import re
t = pt(); e = en()
print("CRLF in pt:", t.count("\r\n"), " lone LF:", t.count("\n")-t.count("\r\n"))
for name, tx in (("pt", t), ("en", e)):
    hs = [(m.start(), m.group(0).strip()) for m in re.finditer(r"^== .*==\s*$", tx, re.M)]
    print(name, len(hs))
    for p, h in hs[:16]: print("  ", p, h[:170])
