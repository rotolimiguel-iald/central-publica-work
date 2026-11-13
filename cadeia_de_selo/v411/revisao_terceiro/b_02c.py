from b_lib import *
t = pt()
print(t[62100:65500])
print("=====HEAD of v410 H0DN section")
import re
for m in re.finditer(r"^== .*H0DN.*==$", t, re.M): print(m.start(), m.group(0)[:200])
for m in re.finditer(r"^== .*==$", t[:130000], re.M): print(m.start(), m.group(0)[:150])
