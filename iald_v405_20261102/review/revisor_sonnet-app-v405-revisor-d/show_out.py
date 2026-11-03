import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
print('n',d['n'],'ok',d['ok'],'| web',d['web_pid'],'sup',d['supervisor_pid'],'login',d['login'],'files_seen',d['files_seen'])
only=set(sys.argv[2].split(',')) if len(sys.argv)>2 else None
for c in d['checks']:
    if only and c['D'] not in only and str(c['n']) not in only:continue
    print('%2d [%s] %-12s %s | %s'%(c['n'],c['D'],c['grupo'],'OK ' if c['ok'] else 'FALHA',c['descricao'][:150].replace('\n',' ')))
    if (not c['ok']) or (len(sys.argv)>3):
        print('      achado:',json.dumps(c['achado'],ensure_ascii=False)[:int(sys.argv[3]) if len(sys.argv)>3 else 1500])
