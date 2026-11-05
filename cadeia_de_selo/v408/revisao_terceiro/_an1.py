import json,collections
d=json.load(open('h_guardas_out.json',encoding='utf-8'))
for k,v in d['varredura_propria'].items():
    if k.startswith('a TGL prova') or k.startswith('nao trata') or k.startswith('a TGL nao'):
        for x in v: print(k,'|',x[0],x[1],x[2][:170])
c=collections.Counter(x[0] for x in d['p_igual_np_sem_proximidade']); print(c)
rend=[x for x in d['p_igual_np_sem_proximidade'] if 'harness' in x[0] or x[0].endswith('.txt') or x[0].endswith('.md')]
for x in rend: print('REND',x[0],x[1],x[2],x[3])
print(collections.Counter(x[0].replace(chr(92),'/').split('/')[-1] for x in d['varredura_propria']['P = NP esta provado (sem do dicionario)']))
