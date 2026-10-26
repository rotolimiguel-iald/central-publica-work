"""Pin the bounded inventory search and read-through for requirement D."""
from task import *
import re
OUT=Path('C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_025')
D=OUT/'CUMPRIMENTO_FINAL'
INV=Path('C:/IALD/Central de Patentes/memory/INVENTARIO_BANCADA_CHATGPT.md')
K=Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt')
def dump(path,obj):
    data=json.dumps(obj,ensure_ascii=False,indent=2).encode('utf8')
    with path.open('xb') as f:f.write(data)
    assert path.read_bytes()==data
def excerpt(path,start,end):
    ls=path.read_text(encoding='utf8').splitlines()
    return {'source':pin(path),'lines':[{'line':i+1,'text':s} for i,s in enumerate(ls) if start<=i+1<=end]}
p=project();t=next(x for x in p['projection']['active'] if x['id']=='compliance_final')
assert act('check',task_id=t['id'],lease_id=t['lease']['id'])['ready']
patterns=[r'pPlus|p⁺|frente de luz',r'calibra',r'H_modular_equals_geometric',
          r'(?:traço|peso|tau|τ).{0,100}(?:energia|corpo|massa)',
          r'(?:energia|corpo|massa).{0,100}(?:traço|peso|tau|τ)',
          r'metric_einstein_from_screen_clausius|metric_unitary_matching_produces_clausius']
ls=INV.read_text(encoding='utf8').splitlines()
queries=[{'regex':q,'flags':'re.IGNORECASE','matches':[{'line':i+1,'text':s} for i,s in enumerate(ls) if re.search(q,s,re.I)]} for q in patterns]
data={'status':'RECORTE_CONSULTADO_COM_FONTES_LIDAS','inventory':pin(INV),'queries':queries,
 'read_through':[excerpt(INV,54,70),excerpt(K/'GeneralMetricClausius.lean',41,63),
                 excerpt(K/'GeneralMetricClausius.lean',83,115),excerpt(K/'V351DualScalingBridge.lean',18,34),
                 excerpt(OUT/'PonteDaEscalaDual.lean',200,218)],
 'ordered_residue':[
  {'class':1,'item':'Instancia e lift equivarante do peso regular para pPlus','evidence':pin(OUT/'PonteDaEscalaDual.lean')},
  {'class':2,'item':'Fluxo de tela e passagem Clausius/Einstein; tambem ha metric_unitary_matching_produces_clausius, que recebe UnitaryScreenMatching como entrada.'},
  {'class':3,'item':'Interpretacao BW e equilibrio local: citacoes ja existentes, nao reauditoria da literatura nesta camada.'},
  {'class':4,'item':'Nao localizada no recorte uma calibracao canonica deste tau para energia de um corpo especifico, nem realizacao do tensor T a partir deste lift. Nao se afirma ausencia em todo o acervo.'}],
 'limits':[
  'Inventario nao e completo nem automaticamente atual: buscas DualScalingData/regularCoreDualScalingData deram zero apesar de fontes existentes e reutilizadas. Zero textual nao e prova de inexistencia.',
  'H_modular_equals_geometric OPEN no inventario e retrato documental, nao classificacao universal de toda versao mais recente.',
  'A nao selecao da massa pela lei de escala nao depende de resultado negativo de busca: lift_mass_not_selected demonstra familias distintas para o mesmo tau positivo.',
  'As funcoes prontas de Clausius consomem T, regularidade, conservacao e hclausius ou matching; sua existencia nao fornece esses dados pelo lift escalar.',
  'O recorte autorizado da quarta fala nao e uma fonte matematica que substitui o teorema nem calibracao experimental.'
 ],'original_sources_modified':False,'withdrawn_speech_accessed':False}
dump(D/'D_INVENTARIO_E_RESIDUO.json',data)
print(json.dumps({'queries':[{ 'regex':q['regex'],'matches':len(q['matches'])} for q in queries],'evidence':str(D/'D_INVENTARIO_E_RESIDUO.json')},ensure_ascii=False))
