import re,sys
s=open(sys.argv[1],encoding='utf-8',newline='').read()
s=re.sub(r'(?<![0-9])(405|406)(?![0-9])',lambda m:{'405':'406','406':'407'}[m.group(1)],s)
open(sys.argv[2],'w',encoding='utf-8',newline='').write(s)
