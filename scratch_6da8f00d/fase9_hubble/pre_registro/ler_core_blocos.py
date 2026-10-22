import json,sys
sys.stdout.reconfigure(encoding='utf-8')
NOS=r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
core=json.load(open(NOS+r'\um_absoluto.json',encoding='utf-8'))['core']
def show(name,maxlen=6000):
    o=core.get(name)
    s=json.dumps(o,ensure_ascii=False,indent=1)
    print('=====',name,'len',len(s)); print(s[:maxlen]); print()
for n in ['bancada_fase4_v378','what_was_missed_v378','the_dissipation_law_with_contrast_v378','the_dissipation_law_v377']:
    show(n,9000)
b=core.get('bancada_fases_5_6_7_v380')
print('===== bancada_fases_5_6_7_v380 keys:',list(b.keys()))
for k,v in b.items():
    s=json.dumps(v,ensure_ascii=False)
    if any(t in k.lower() for t in ['fase5','sh0es','ladder','fase_5','verdict','hash','sha','read']):
        print('--',k,':',s[:5000])
cd=core.get('coma_distance_dephasing',{}).get('inputs')
print('===== coma_distance_dephasing.inputs:',json.dumps(cd,ensure_ascii=False)[:2000])
