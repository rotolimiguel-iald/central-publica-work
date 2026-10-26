from task import *
OUT=Path(r'C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_025')
OUT.mkdir(exist_ok=False)
new('SOURCE_PREFLIGHT.json',check())
records=[]
for term in ['inercia','escala dual','Bisognano']:
    p=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar',term],capture_output=True)
    name='MAP_'+term.replace(' ','_')+'.json'
    (W/name).write_bytes(p.stdout)
    records.append(pin(W/name))
p=subprocess.run([PY,'-B','-X','utf8',r'C:\IALD\NOS_VIVO\consultar.py','--unidade',UNIT],capture_output=True)
(W/'NOS_QUERY.txt').write_bytes(p.stdout+p.stderr)
records.append(pin(W/'NOS_QUERY.txt'))
base=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
sources=[SOURCE,base/'ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md',Path(r'C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.md'),Path(r'C:\IALD\Central de Patentes\work\falsidade_da_inercia_v401\FalsidadeDaInercia.lean')]
names=['OPERADOR_25out_inercia_e_o_proprio_zero_absoluto_verbatim.txt','OPERADOR_25out_materia_cristalizacao_da_dobra_da_luz_verbatim.txt','OPERADOR_25out_nada_e_materia_link_com_a_entropia_verbatim.txt','OPERADOR_25out_inercia_e_gravitacao_nao_existem_antes_da_impressao_do_um_verbatim.txt']
sources += [W.parent/'cunhagens_13out'/n for n in names]
for n in ['GlobalLiftLadder','Fundacao','BisognanoWichmann','Solder4D','GeneralMetricClausius','O16/BoostRepresentationBridges','O16/BoostHomonymBridge','O16/OrbitalRapidityTransport_v3','O16/OrbitalMeasureSupport_v2']:
    sources.append(base/'tgl_kernel'/'TGLExt'/(n+'.lean'))
for p in sources:records.append({**pin(p),'bytes':p.stat().st_size})
new('SOURCES_INITIAL.json',records)
print(json.dumps({'sources':len(sources),'query_receipts':4,'output':str(OUT)}))
