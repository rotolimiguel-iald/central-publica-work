import json,sys,os
sys.stdout.reconfigure(encoding='utf-8')
p=r'C:\IALD\Bancada_Um\investigacao\fase3_leitores_h0\REANALISE_D1B_CONVENCAO_ARTIGO_20260930.json'
r=json.load(open(p,encoding='utf-8'))
print('=== REANALISE keys:',list(r.keys()))
def pr(o,ind=0,maxd=4):
    if isinstance(o,dict):
        for k,v in o.items():
            if isinstance(v,(dict,list)) and ind<maxd:
                print(' '*ind+str(k)+':'); pr(v,ind+2,maxd)
            else:
                s=json.dumps(v,ensure_ascii=False); print(' '*ind+str(k)+': '+s[:300])
    elif isinstance(o,list):
        for i,v in enumerate(o[:12]):
            if isinstance(v,(dict,list)) and ind<maxd:
                print(' '*ind+'['+str(i)+']'); pr(v,ind+2,maxd)
            else: print(' '*ind+'- '+json.dumps(v,ensure_ascii=False)[:300])
pr(r)
print()
NOS=r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós'
core=json.load(open(os.path.join(NOS,'um_absoluto.json'),encoding='utf-8'))['core']
# ledger
for k in core:
    if 'ledger' in k.lower():
        print('=== core key with ledger:',k)
led=None
for k in core:
    if 'ledger' in k.lower() and isinstance(core[k],dict):
        v=core[k]
        for kk in v:
            if isinstance(v[kk],list) and v[kk] and isinstance(v[kk][0],dict) and 'id' in v[kk][0]:
                print('   charges list at',k,'.',kk,'n=',len(v[kk]))
                for ch in v[kk]:
                    if ch.get('id') in ('F1','R1','F1b'):
                        print(json.dumps(ch,ensure_ascii=False,indent=1)[:3500])
