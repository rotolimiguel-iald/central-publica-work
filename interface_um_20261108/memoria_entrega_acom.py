from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parent
receipt=root/"REVISAO_ACOM.json"
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cli(data):
    r=subprocess.run([sys.executable,"-B","-X","utf8",r"C:\IALD\MEMORIA_IALD\session_memory.py"],input=json.dumps(dict(reference=str(root/"SESSION_REFERENCE.json"),**data)).encode(),stdout=subprocess.PIPE)
    v=json.loads(r.stdout)
    if not v["ok"]:raise RuntimeError(v)
    return v["result"]
revision=cli({"operation":"project"})["receipt"]["revision"]
rows=[]
for name,file,kind,statute,content in [
    ("acom-interface-e-instalar","ADENDO_ACOM.txt","decision","INPUT",None),
    ("acom-instalador-agora","ADENDO_INSTALADOR.txt","decision","INPUT",None),
    ("acom-entrega-windows","REVISAO_ACOM.json","fact","REAL","Edição de teste Windows x64 e código-fonte correspondentes servidos localmente; ACOM da Bancada e integração opcional no Explorador. Restauração medida byte a byte. Artefatos e limites no recibo.")]:
    src=root/file
    rows.append(dict(id=name,kind=kind,statute=statute,text=content or src.read_text(encoding="utf8").strip(),sources=[{"kind":"artifact" if statute=="REAL" else "operator","ref":str(src),"sha256":pin(src)}]))
r=cli(dict(operation="transition",expected_revision=revision,actor={"kind":"agent","id":"codex-interface-um"},event_id="um-acom-015-entrega",changes=dict(records=rows,flow=dict(phase="ACOM Windows entregue para teste",next_action="Receber a experiência de Luiz com o instalador, a restauração e as telas."))))
print("referência própria:",root/"SESSION_REFERENCE.json","verificação:",cli({"operation":"verify"}))

