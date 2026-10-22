from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) and not p.exists() and b
 t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
f=json.loads((R/'REAPROVEITAMENTO_A1B_FIDELIDADE_PESO_LIMITE.json').read_text(encoding='utf8'));s=Path(f['searches']['path']);assert pin(s)==f['searches']
for q in json.loads(s.read_text(encoding='utf8')):
 assert q['returncode'] in (0,1) and q['stderr']['bytes']==0
 p=Path(q['stdout']['path']);assert pin(p)==q['stdout'];print(q['label'],p.read_text(encoding='utf8'))
reason='Consulta lida antes do código: basta ε=1; a alternativa RXR=0 é válida. Reusar diretamente positive_sqrt_injective e resolventSquareRoot_dense, que já fornecem injetividade/imagem densa da raiz limitada. Não acrescentar teorema de densidade novo. Um auxiliar genérico apenas cancela os dois lados usando essas propriedades e a auto-adjunção da mesma raiz. O exemplo antigo denseAntilinearExtension_norm mostra a forma da indução de DenseRange; consultar o corpo não o transforma em prova de fidelidade. Escala dual será outro alvo.'
d=dict(timestamp=datetime.datetime.now().astimezone().isoformat(),status='FICHE_ROUTE_RECORDED_BEFORE_FAITHFUL_CODE',reason=reason,searches=pin(s),consultation=pin(R/'revisao_consulta_limite_fidelidade/CONSULTA_LIMITE_FIDELIDADE.md'),induction_pattern=pin(R/'k/TGLExt/V350DenseAntilinearExtension.lean'))
stem='ADENDO_FICHA_FIDELIDADE_ROTA';put(R/(stem+'.json'),json.dumps(d,ensure_ascii=False,indent=2).encode('utf8'));put(R/(stem+'.md'),('[OPEN — escolha da rota antes do código]\n\n'+d['timestamp']+'\n\n'+reason+'\n').encode('utf8'))
