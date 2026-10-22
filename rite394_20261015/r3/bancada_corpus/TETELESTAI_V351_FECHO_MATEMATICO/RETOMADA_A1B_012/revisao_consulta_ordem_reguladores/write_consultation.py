from pathlib import Path
from datetime import datetime
import hashlib,json,os
R=Path(r'C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012')
O=R/'revisao_consulta_ordem_reguladores'
O.mkdir(exist_ok=True)
refs=[
('TGLExt/V351InverseGeneratorCutoff.lean',[(13,20),(24,30),(50,54),(99,104)]),
('TGLExt/V351InverseCutoffCFC.lean',[(12,23),(62,69)]),
('TGLExt/V351RegularPositiveGraph.lean',[(78,87)]),
('TGLExt/V351ScaledResolventCalculus.lean',[(14,19),(27,30)]),
('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unital.lean',[(904,907),(926,933),(1037,1040)]),
('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Instances.lean',[(292,301),(343,355)]),
('.lake/packages/mathlib/Mathlib/Algebra/Algebra/Spectrum/Quasispectrum.lean',[(414,418)]),
('.lake/packages/mathlib/Mathlib/Algebra/Order/GroupWithZero/Basic.lean',[(1275,1277)])]
def pin(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
records=[]
for f,rs in refs:
 p=R/'v'/f;ls=p.read_text(encoding='utf-8-sig').splitlines()
 records.append({'file':pin(p),'read_ranges':[{'start':a,'end':b,'text':'\n'.join(ls[a-1:b])} for a,b in rs]})
def link(f,line,label):
 return '['+label+'](<'+str(R/'v'/f).replace('\\','/')+':'+str(line)+'>)'
u='.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/'
text=f"""# Consulta — ordem dos reguladores originais
Data: {datetime.now().astimezone().isoformat()}

[DERIVED] A rota mínima é **CFC real no mesmo R**, usando a extensão com max já definida. Hipóteses: P arbitrário e **0 < ε ≤ η**. Conclusão proposta: regularInverseGeneratorCutoff P η ≤ regularInverseGeneratorCutoff P ε. Esta consulta não compila nem acrescenta teorema; a formalização dessa conclusão permanece [OPEN].

[REAL — leitura de fontes] A identificação exata Bε = cfc Fε R já está em {link('TGLExt/V351InverseCutoffCFC.lean',62,'regularInverseGeneratorCutoff_cfc')}, com ε>0. A função Fε é complexa de valor real, dada em :12 pela razão x/max(min(1,ε),1+(ε−1)x), x=Re z. Não é preciso redefinir corte, grupo ou gerador.

## Passo mínimo

Escreva apenas na demonstração fε(x)=x/dε(x), dε(x)=max(min(1,ε),1+(ε−1)x), para x real. Para x≥0 e ε≤η:

1. min(1,ε)≤min(1,η) e 1+(ε−1)x≤1+(η−1)x; portanto dε(x)≤dη(x).
2. 0<min(1,ε)≤dε(x), por ε>0.
3. Logo x/dη(x)≤x/dε(x), exatamente a orientação de {link('.lake/packages/mathlib/Mathlib/Algebra/Order/GroupWithZero/Basic.lean',1275,'div_le_div_of_nonneg_left')}: (ha : 0 ≤ a) (hc : 0 < c) (h : c ≤ b) : a / b ≤ a / c.

**Manter o max é mais econômico:** não precisamos removê-lo, calcular sigmoid, restringir a x≤1 ou inverter um operador. A comparação vale em todo x≥0. O espectro real de R está nessa semirreta: {link('TGLExt/V351RegularPositiveGraph.lean',84,'regularSpectralResolvent_nonneg')} e {link('.lake/packages/mathlib/Mathlib/Algebra/Algebra/Spectrum/Quasispectrum.lean',414,'spectrum_nonneg_of_nonneg')} já fornecem o requisito.

A continuidade real de fε vem da expressão com denominador positivo, ou da composição real de inverseCutoffFunction_continuous. Converter as duas igualdades complexas para CFC real com {link(u+'Instances.lean',352,'cfc_real_eq_complex')}, usando a auto-adjunção decorrente de R≥0. Seu tipo é cfc f a = cfc (fun x ↦ f x.re : ℂ → ℂ) a; esta é precisamente a forma de Fε após desdobrar a definição. Há uso local desse adaptador em {link('TGLExt/V351ScaledResolventCalculus.lean',27,'scaledResolventCoordinate_cfc')}.

Aplicar então {link(u+'Unital.lean',926,'cfc_mono')} com f=fη, g=fε, a=R. Ele pede desigualdade pontual **no espectro** e ContinuousOn das duas funções. A desigualdade resulta na ordem dos CLM do Hilbert regular; a conversão anterior identifica esses CLM com os B originais. cfc_le_iff (:1037 do mesmo arquivo) também serve, mas traz uma equivalência e hipótese de auto-adjunção explícita desnecessárias para a etapa final. Trabalhar no ambiente B(H) aproveita as instâncias existentes; não instalar CompleteSpace no subtipo N.

## Alternativa pelo grafo

[DERIVED] É válida, mas acrescenta passos para obter somente ordem. Do fornecedor {link('TGLExt/V351InverseGeneratorCutoff.lean',50,'regularInverseGeneratorCutoff_graph')} aplicado a Bηx e do {link('TGLExt/V351InverseGeneratorCutoff.lean',99,'graph_iff')} com ε resulta:
Bε(x + (ε−η) Bηx) = Bηx.
Por linearidade e extensionalidade:
Bε − Bη = (η−ε) • (Bε * Bη).

Ainda é preciso demonstrar que Bε e Bη comutam e que o produto é positivo. A comutação pode vir do mesmo CFC; {link(u+'Instances.lean',292,'Commute.mul_nonneg')} dá então positividade a partir das duas positividades e da comutação. Com η−ε≥0, a identidade fornece a ordem. Isso exige identidade de CLM, comutação e produto positivo além dos adaptadores. É útil se o próximo consumidor também exigir a identidade resolvente; para a ordem isolada, recomendo a primeira rota. Não se usa inversa limitada de h nem positividade de produto arbitrário não comutante.

## Fronteira e proveniência

[REAL] Nomes, tipos, linhas e hashes dos oito arquivos consultados estão no JSON anexo. Busca delimitada aos módulos dos cortes e APIs pertinentes; não é inventário exaustivo de toda a casa. Não localizei nos dois módulos dos cortes um lema pronto de antitonia; a ligação escalar/CFC acima é a obrigação residual concreta.

[OPEN] A ordem não é afirmada para parâmetros sem positividade; a definição totalizada em ε=0 não autoriza tal extensão. Esta consulta não paga ordem de pesos por si só nem tracialidade, não revisa V351AllPositiveWeightOrder e não modifica os 19 deltas entregues. Nenhuma execução Lean/Lake, monólito, auditoria autoral ou memória.
"""
data={'timestamp':datetime.now().astimezone().isoformat(),'status':'CONSULTA_DERIVED__NO_NEW_LEAN_PROOF','scope':'antitonicidade dos mesmos regularInverseGeneratorCutoff','recommended_route':'real_cfc_mono_with_existing_max_denominator','assumptions':['P : SiteProfile','0 < epsilon','epsilon <= eta'],'conclusion_proposed':'regularInverseGeneratorCutoff P eta <= regularInverseGeneratorCutoff P epsilon','new_theorems':0,'compilation_executed':False,'author_sources_modified':False,'memory_modified':False,'supplier_records':records,'search_exhaustive':False,'remaining':['formalizar comparação escalar e aplicar CFC real; conclusão ainda não compilada nesta consulta'],'trace_open':True}
def fresh(p,b):
 assert p.resolve().is_relative_to(O.resolve()) and not p.exists(),p
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b)
 assert t.read_bytes()==b;os.replace(t,p)
fresh(O/'CONSULTA_ORDEM_REGULADORES.md',text.encode('utf-8'))
data['report']=pin(O/'CONSULTA_ORDEM_REGULADORES.md')
fresh(O/'CONSULTA_ORDEM_REGULADORES.json',(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps({'md':data['report'],'json':pin(O/'CONSULTA_ORDEM_REGULADORES.json')},ensure_ascii=False))

