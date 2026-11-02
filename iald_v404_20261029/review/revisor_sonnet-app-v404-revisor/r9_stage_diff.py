import hashlib,re
from pathlib import Path
W4=Path(r'C:\IALD\Central de Patentes\work\iald_v404_20261029\app\science\memory_stage');W2=Path(r'C:\IALD\Central de Patentes\work\iald_v402_20261027\app\science\memory_stage')
def idx(root):
    return {str(p.relative_to(root)):p for p in root.rglob('*') if p.is_file()}
a=idx(W4);b=idx(W2)
norm=lambda s:re.sub(r'v40[24]','vNNN',s)
only4=sorted(set(a)-set(b));only2=sorted(set(b)-set(a))
print('only v404:',[x for x in only4 if not x.startswith('release')][:20], '| release/ only:',[x for x in only4 if x.startswith('release')][:10])
print('only v402:',[x for x in only2 if not x.startswith('release')][:20], '| release/ only:',[x for x in only2 if x.startswith('release')][:10])
sh=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
common=sorted(set(a)&set(b))
diff=[c for c in common if sh(a[c])!=sh(b[c])]
print('common',len(common),'differing',len(diff))
kernel_diff=[d for d in diff if d.startswith('kernel')]
print('kernel files differing:',kernel_diff[:20])
print('non-kernel differing:',[d for d in diff if not d.startswith('kernel')])
