from b_lib import *
import re
o = rd(NOS + r"\um_absoluto_manifest.md")
print(len(o))
hs = [(m.start(), m.group(0)) for m in re.finditer(r"^#{1,3} .*$", o, re.M)]
print(len(hs)); 
for p, h in hs[:25]: print(p, h[:100])
for m in list(re.finditer(r"h0dn_bg1_v410", o))[:6]: print(m.start(), repr(o[max(0, m.start()-100): m.start()+200]))
n = man()
hs2 = [(m.start(), m.group(0)) for m in re.finditer(r"^#{1,3} .*$", n, re.M)]
print("NEW manifest headings:", len(hs2))
for p, h in hs2[:25]: print(p, h[:100])
