"""Register the operator-authorized network construction and its own memory."""
from pathlib import Path
import datetime as dt, hashlib, json, os, subprocess, uuid

ROOT = Path(r'C:\IALD\Central de Patentes')
W = ROOT / 'work/rede_quantica_20261013'
OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE'
W.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)
PY = r'C:\Python314\python.exe'

def new(path, value):
    b = (value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)).encode('utf-8')
    if path.exists(): raise FileExistsError(path)
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(b); f.flush(); os.fsync(f.fileno())
    assert tmp.stat().st_size == len(b)
    os.rename(tmp, path)

def run(name, args, data=None):
    if (W/name).exists(): raise FileExistsError(name)
    cp = subprocess.run([PY, '-B', '-X', 'utf8', *args], input=None if data is None else json.dumps(data, ensure_ascii=False), text=True, encoding='utf-8', capture_output=True)
    new(W/name, {'exit_code':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr})
    if cp.returncode: raise RuntimeError(cp.stdout + cp.stderr)
    return cp.stdout

original = 'Construa a rede completa, eu já escrevi muita coisa sobre a rede quântica e mais, eu tenho um dispositivo patenteado exatamente como funciona a rede em forma mecânica com isso você vai entender a física e montar o contrato completo'
new(W/'OPERADOR_REDE_VERBATIM.txt', original)
new(W/'OPERADOR_LOCALIZACAO_VERBATIM.txt', 'Sim está na central de patentes')
unit = [{'id':'F1.REDE','frente':'F1','titulo':'Rede quântica: escritos do operador, dispositivo mecânico e realização dos contratos v392','dono':'codex-gerente-tgl','status':'PROPOSTA','origem':str(W/'OPERADOR_REDE_VERBATIM.txt'),
 'criterio_de_fechado':'Levantamento por fontes e hashes; identificação documentada do dispositivo e de seu conteúdo físico; correspondência explícita entre construção de engenharia e rede de subespaços/álgebras; contrato completo com hipóteses e falsificadores; construção efetiva em sandbox das partes realizáveis, habitantes não triviais e controles; relatório honesto dos campos ainda abertos; auditoria independente antes de integração.',
 'escopo':'Construção matemática e simulação sintética em cópias; reaproveitar textos do autor e v392. Não alterar originais, pedidos de patente, um.py, kernel do Nós, Bancada produtiva, selo ou gate. Leitura de engenharia não infere patente concedida nem transporte quântico físico demonstrado.',
 'reaproveitamento_previo':'Mapa formal.f1_3.reconcile_v376_mathlib_plan: contrato BGL já tipado, sem habitante. O16/Continuous049 e V351 devem ser reutilizados. Nós Vivo consultado para F1.REDE antes de criar: unidade ausente, consulta recusada visivelmente. Ψ-NET e outros dispositivos possuem protótipos e fontes na Central.',
 'reivindicacao':None,'evidencia':[]}]
new(W/'NOVA_UNIDADE.json',unit)
print(run('BOARD_NEW.json',[r'C:\IALD\PROGRAMA_IALD\iald.py','nova','--json',str(W/'NOVA_UNIDADE.json'),'--quem','codex-gerente-tgl']))
print(run('BOARD_CLAIM.json',[r'C:\IALD\PROGRAMA_IALD\iald.py','reivindicar','F1.REDE','--quem','codex-gerente-tgl','--horas','12','--nota','Construção autorizada pelo operador; artefatos novos work/rede_quantica_20261013 e túnel F1.REDE. Memória: referência ACOM própria; eventuais notas aditivas Atlas/índice/AVISO apenas com backups. Originais científicos, patentes e produção somente leitura.']))
init={'operation':'init','reference':str(W/'ACOM_REFERENCE.json'),'objective_file':str(W/'OPERADOR_REDE_VERBATIM.txt'),'objective_sha256':hashlib.sha256(original.encode()).hexdigest(),'request_id':str(uuid.uuid4()),'scope':{'house':'IALD','principal':'luiz-antonio-rotoli-miguel'},'actor':{'id':'codex-gerente-tgl','kind':'agent'},'constraints':{'unit':'F1.REDE','production_changes':False,'working_basis':'v392 authorized by operator'}}
new(W/'ACOM_INIT_REQUEST.json',init)
print(run('ACOM_INIT_RECEIPT.json',[r'C:\IALD\MEMORIA_IALD\session_memory.py'],init))
run('ACOM_PROJECT_R0.json',[r'C:\IALD\MEMORIA_IALD\session_memory.py'],{'operation':'project','reference':str(W/'ACOM_REFERENCE.json')})
print(json.dumps({'reference':str(W/'ACOM_REFERENCE.json'),'output':str(OUT)},ensure_ascii=False))
