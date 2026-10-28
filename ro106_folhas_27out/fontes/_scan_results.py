import glob, collections, os
from PIL import Image
os.chdir(r'C:\IALD\Central de Patentes\patents\BR102026003460-6_MQC')
rows = collections.defaultdict(list)
for f in sorted(glob.glob('results/*/figures/MQC_fig*.png')):
    f = f.replace('\\', '/')
    try:
        im = Image.open(f)
    except Exception as e:
        continue
    k = os.path.basename(f)[4:8]
    rows[k].append((f.split('/')[1], im.size))
for k in sorted(rows):
    print(k, collections.Counter(s for _, s in rows[k]).most_common(6))
want = {'fig5': (4772, 1471), 'fig7': (4171, 1469)}
for k, (w, h) in want.items():
    print(k, 'largura ~', w, [(d, s) for d, s in rows[k] if abs(s[0] - w) <= 3][:8])
