import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
print('n',d['n'],'ok',d['ok'],'| web',d['web_pid'],'sup',d['supervisor_pid'],'login',d['login'],'files_seen',d['files_seen'],'rev',d['revision'])
lim=int(sys.argv[2]) if len(sys.argv)>2 else 0
for c in d['checks']:
    print('%2d [%s] %-12s %s | %s'%(c['n'],c['V'],c['grupo'],'OK ' if c['ok'] else 'FALHA',c['descricao'][:140].replace('\n',' ')))
    if (not c['ok']) or lim:
        print('      achado:',json.dumps(c['achado'],ensure_ascii=False)[:max(lim,1500)])
