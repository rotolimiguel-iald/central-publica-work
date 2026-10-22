from pathlib import Path
import datetime, hashlib, json, os
R = Path(__file__).resolve().parent
BASE = R.parent/'RETOMADA_A1B_012'
K = BASE/'k'
CHAT = R.parent.parent
now = datetime.datetime.now().astimezone().isoformat()
def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,text):
    assert p.is_relative_to(R) and not p.exists()
    p.parent.mkdir(parents=True,exist_ok=True)
    b=text.encode('utf8');q=p.with_name(p.name+'.tmp')
    with q.open('xb') as f: f.write(b)
    assert q.read_bytes()==b
    os.replace(q,p)
def declaration(path,start,end):
    lines=path.read_text(encoding='utf8').splitlines()
    a=next(i for i,x in enumerate(lines) if start in x)
    b=next((i for i in range(a+1,len(lines)) if end in lines[i]),len(lines))
    return dict(source=pin(path),line=a+1,statement='\n'.join(lines[a:b]))
review=json.loads((BASE/'revisao_tracialidade_quadratica/REVIEW_A1_QUADRATIC_TRACE_FINAL.json').read_text(encoding='utf8'))
assert review['mathematical_review_passed'] and review['full_trace_constructed']
assert not any(review[k] for k in ('P0','P1','P2'))
records=[
 declaration(K/'TGL/ModularRealization.lean','structure ContinuousCoreData','attribute [instance]'),
 declaration(K/'TGL/ModularRealization.lean','structure ThreeLocksCoreData','/--'),
 declaration(K/'TGL/CoreSupport.lean','noncomputable def threeLocksFromSupport','/--'),
 declaration(K/'TGLExt/V351RegularCoreTraceContract.lean','structure RegularCoreTraceData','theorem RegularCoreTraceData.not_zero'),
 declaration(K/'TGLExt/V351RegularCoreTraceConstruction.lean','def scalarInverseLimitTraceData','end'),
 declaration(K/'TGLExt/SusyRelativeGap.lean','structure SusyRelativeData','/--'),
 declaration(K/'.lake/packages/mathlib/Mathlib/Analysis/VonNeumannAlgebra/Basic.lean','theorem IsStarProjection.mem_iff','end VonNeumannAlgebra'),
]
searches=[
 dict(stage=1,pattern='ThreeLocks|threeLocks|finite.*projection|projection.*finite|RegularCoreTraceData|SpectralApproximationWitness',scope='kernel canônico e cópia K, nomes e enunciados',result='Contratos legados, CoreSupport, SusyRelativeGap, SpectralReduction/ExactWitness, traço A1. Resultados amplos tiveram stdout truncado; fornecedores relevantes foram abertos separadamente. Consulta não executou um.py.'),
 dict(stage=2,pattern='ThreeLocks|P_F|projection|gap|projeção',scope='notas 11–13/09, TRACO_PROXIMAS_OBRIGACOES, CONVENCOES_DO_TRACO, AUDITORIA_DAS_PENDENCIAS, MAPA_GATE_E_REAPROVEITAMENTO',result='CoreSupport já construía Hmin=1-q recebendo suporte. Não há ponte automática para traço A1 no cone. Estados OPEN históricos de A1 são superados pelo aceite34. DEV de pesos/grafos não fornece projeção A2 pelo nome.'),
 dict(stage=3,pattern='ThreeLocks|P_F|finite.*projection|projection.*finite|Spectral',scope='ENTREGA_0*.md e consulta_A2_CONTRATO anterior',result='Consulta anterior delimita suporte, split, gap, fronteira do traço total. ENTREGAs de A1 reutilizáveis não são ThreeLocks construídos. A ausência é relativa às buscas, não universal.'),
 dict(stage=4,pattern='Three Locks|H1|A2|core|traço',scope='A_PROVA_DA_QG_TGL_arvore.md canônico',result='Adendo v354 registra A1 concluído e falta A2. Antigo adendo v353 OPEN sobrevive historicamente; não reabrir A1. Não foram lidos resultados de natureza para mover gate.'),
 dict(stage=5,pattern='ThreeLocks|threeLocks|finite.*projection|projection.*finite|spectralProjection|spectral_projection|RegularCoreTraceData',scope='C:\\IALD\\Artigo\\BANCADA_TOE\\kernel_bancada, *.lean',result='Ocorrências em TheAngleIsTheProjection/CoFoundation/ObserverReadsTheAngle; projeções matriciais de outro tipo, não suporte finito do mesmo core.'),
 dict(stage=6,pattern='threeLocksFromSupport|scalarInverseLimitTraceData|proje[cç][aã]o.{0,35}tra[cç]o.{0,20}finit',scope='buscar.py --ctx 140 --max 22',result='Consulta rc0 truncou nos registros de julho. Refinamento --desde 2026-09-10 devolveu ZERO DOCUMENTOS INDEXADOS, não ausência de provas recentes. buscar.py omite erros de leitura de corpus; índice não constitui busca exaustiva confiável por si. Leitura recente feita diretamente nas fontes e pastas atuais.'),
 dict(stage='mathlib',pattern='exists.*StarProjection|starProjection|ker.*commut|posPart_sub_negPart',scope='Mathlib Analysis/VonNeumannAlgebra e ContinuousFunctionalCalculus',result='IsStarProjection.mem_iff fornece critério exato de pertinência; adaptar à projeção do núcleo. CFC.posPart/negPart e corte de limiar são candidatos para finitude; extrair projeção via invariância evita pedir antecipadamente SpectralApproximationWitness.'),
]
obligations=[
 ('A2','ThreeLocks no mesmo N e tau A1; projeção finita positiva, split, domínios/afiliação, gap relativo, identificação espectral; canto sem testemunha recebida','OPEN'),
 ('B1_PRIME','Quarta face beta, ficha, EOM tipada xi separado, trio/controles/consumidor proposto','DELEGATED_AUTHOR_POINCARE'),
 ('route','Ratificação do operador fator total documentada; D1 V3 da gerência','CONCEPTUAL_CHOICE_RECORDED'),
 ('5.4a','Explicar namespace TGLV350.Regular em V351','OPEN'),
 ('5.4b','Sanear homônimo H_nx em B3/B4 ao tocar cópias','OPEN'),
 ('5.4c','Sondas negativas dos sete órfãos, por módulo','OPEN'),
 ('5.4d','Explicar/sanear duas declarações antiunitárias duplicadas','OPEN'),
 ('5.4e','Errata ao lado de LACUNAS_A1, pontes 1–4 com rota efetiva','OPEN'),
 ('5.4f','Corolário B3 ADITIVO sem hr/he preservando Lambda','OPEN'),
 ('5.4g','Investigar/documentar três olean B6 divergentes sem inventar causa','OPEN'),
 ('5.4h','Declarar motivo do maxHeartbeats por módulo','OPEN'),
]
data=dict(timestamp=now,status='REUSE_BEFORE_A2_CODE__A2_NOT_CONSTRUCTED',
 orders=[pin(CHAT/'TUNEL/PARA_CHATGPT'/n) for n in ['ORDEM_011_fecho_matematico_da_realizacao_concreta.md','ORDEM_012_RECIBO_E_ADENDO_001_quarta_face_e_sequencia.md']],
 prerequisite_review=pin(BASE/'revisao_tracialidade_quadratica/REVIEW_A1_QUADRATIC_TRACE_FINAL.json'),
 declarations=records,searches=searches,requirements=obligations,
 decisions=[
  'REUSAR scalarInverseLimitTraceData: obter positivo finito não nulo sob qualquer positivo não nulo a partir do campo semifinite e faithful. Não reconstruir peso ou tracialidade.',
  'ADAPTAR IsStarProjection.mem_iff: projeção ortogonal do núcleo de A em N pertence a N por invariância sob comutante. O alvo é exatamente pertinência do futuro corte espectral A2.',
  'ADAPTAR CFC posPart/negPart: de X positivo finito não nulo extrair limiar epsilon>0 e q projetor não nulo com epsilon*q<=X. Usar ordem/homogeneidade/fidelidade A1 para traço positivo finito. Prova ainda a construir.',
  'ADAPTAR sistema matricial representado para obter faces iguais com tracialidade A1. Semicorte finito sob projeção matricial, não projeção dual-fixa tomada como finita.',
  'REUSAR CoreSupport quando suporte, faces e traço compatíveis forem produzidos; gap do representante 1-q não identifica outro operador por nome.',
  'OPEN contrato: ContinuousCoreData exige função total cíclica em Core->ENNReal; A1 fornece traço no cone. Não usar tau(x*x) como extensão cíclica, não alterar silenciosamente o contrato. Essa obrigação não desaparece com a existência da projeção.',
 ])
put(R/'REAPROVEITAMENTO_A2.json',json.dumps(data,ensure_ascii=False,indent=2))
md='# Ficha A2 — reaproveitamento antes de código\n\n[REAL — leitura; construção A2 ainda OPEN.]\n\n'+now+'\n\n'
md+='Consumidores: ThreeLocksCoreData e qgf_unconditional_continuous_corner_proved / gpf_H1_internal_susy_relative_gap_discharged, conforme ORDEM011 §3.A2. O adendo exige o MESMO regularCoreAlgebra P e o valor scalarInverseLimitTraceData. O objetivo integral não se reduz ao primeiro lema.\n\n'
for d in data['decisions']: md+='- '+d+'\n'
md+='\n## Buscas e limites\n\n'
for s in searches: md+=f"{s['stage']}. `{s['pattern']}` em {s['scope']}: {s['result']}\n\n"
md+='## Tipos e fornecedores lidos\n\n'
for d in records:
    md+=f"{d['source']['path']}:{d['line']} — SHA256 {d['source']['sha256']}\n\n```lean\n{d['statement']}\n```\n\n"
md+='Nenhum aceite A2. Cache Mathlib e objetos A1 já aceitos podem ser REUSADOS em DEV, com proveniência explícita; os objetos novos terão reprodução e revisão separadas antes de entrega. Nenhum build canônico/um.py/rito experimental autorizado nesta bancada.\n'
put(R/'REAPROVEITAMENTO_A2.md',md)
put(R/'REQUISITOS_ADENDO_001.json',json.dumps(dict(timestamp=now,requirements=obligations),ensure_ascii=False,indent=2))
print(json.dumps(dict(fiche=pin(R/'REAPROVEITAMENTO_A2.md'),requirements=pin(R/'REQUISITOS_ADENDO_001.json')),ensure_ascii=False))
