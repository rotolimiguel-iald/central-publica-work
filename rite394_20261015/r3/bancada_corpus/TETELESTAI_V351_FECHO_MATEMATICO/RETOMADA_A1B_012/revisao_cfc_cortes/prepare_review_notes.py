from pathlib import Path
import sys,re
OUT=Path(__file__).resolve().parent;R=OUT.parent
sys.path.insert(0,str(OUT))
from build_delta import pin,save,now,ck,load,uncomment

history=[]
for p in sorted((R/'dev_cutoff_cfc').glob('*/run.json')):
 j=load(p);sp=pin(p.parent/'V351InverseCutoffCFC.lean')
 assert sp['bytes']==j['source']['bytes'] and sp['sha256']==j['source']['sha256']
 diagnostics=[]
 for f in ['stdout','stderr']:
  ck(j[f]);t=Path(j[f]['path']).read_text(encoding='utf8')
  diagnostics += [line for line in t.splitlines() if ': error:' in line or ': warning:' in line]
 history.append(dict(run=pin(p),source_snapshot=sp,historical_location=j['source']['path'],returncode=j['returncode'],stdout=j['stdout'],stderr=j['stderr'],diagnostics=diagnostics))
assert [h['returncode'] for h in history]==[1,1,0]
save(OUT/'history_read.json',dict(timestamp=now(),attempts=history,rc1_excluded=2,accepted_final_dev=history[-1]['run'],current_source=pin(R/'k/TGLExt/V351InverseCutoffCFC.lean')))
code=uncomment((R/'k/TGLExt/V351InverseCutoffCFC.lean').read_text(encoding='utf8'))
priv=[dict(kind=m[0],name=m[1]) for m in re.findall(r'^private (def|theorem) (\S+)',code,re.M)]
assert len(priv)==2 and all(p['kind']=='theorem' for p in priv)
save(OUT/'private_declarations.json',dict(source=pin(R/'k/TGLExt/V351InverseCutoffCFC.lean'),declarations=priv,private_theorems=2,private_definitions=0,public_target_count=7,axiom_scope='Whole source compiled; private proofs transitively included in public target axioms; no extra standalone private prints',consumers={'regularResolvent_cfc_coordinate':'regularInverseGeneratorCutoff_cfc','hilbertPositiveSqrt_complex_cfc':'scalarRightAction_sqrt -> regularInverseGeneratorCutoff_sqrt_right'}))
notes=dict(review_complete=True,findings=[],status='A1_CUTOFF_CFC_REVIEW_ACCEPTED__PERTURBED_WEIGHT_TRACE_OPEN',report_name='REVIEW_A1_CUTOFF_CFC_FINAL',title='Revisão independente — CFC dos cortes inversos e raízes originais',paragraphs=[
'[REAL] REAPROVEITAMENTO_A1B_CFC_CORTES MD/JSON e ADENDO_FICHA_CFC_RAIZ_HILBERT MD/JSON foram lidos integralmente e seus pins conferidos. A ficha antecede o código. O adendo declara honestamente ser posterior ao DEV e anterior ao aceite: explicita o fornecedor hilbertPositiveSqrt já existente. GeneralExpectationCP é apenas um molde numa álgebra distinta, não um teorema usado como se tivesse o mesmo tipo.',
'[REAL] São 7 declarações públicas (6 teoremas + 1 definição) com auditor próprio #check/pp.universes e #print axioms. Há separadamente 2 teoremas privados, regularResolvent_cfc_coordinate e hilbertPositiveSqrt_complex_cfc, lidos integralmente e compilados no módulo. Seus axiomas são incluídos transitivamente nos alvos públicos consumidores; não se alegam dois prints privados adicionais. A fonte inteira tem 8 teoremas e 1 definição.',
'[REAL] inverseCutoffFunction é uma função escalar total; os teoremas de continuidade, identificação e consumo exigem explicitamente ε>0. O denominador max(min(1,ε),1+(ε−1)Re z) é ≥min(1,ε)>0 em todo ℂ. No símbolo sigmoid a, a combinação convexa limita o denominador inferiormente e permite retirar max. A identidade final é ofReal((ε+exp(−a))⁻¹), com o sinal negativo correto e sem hipótese de gap de h.',
'[REAL] O helper de coordenadas usa o MESMO regularSpectralCoordinates e regularSpectralResolvent. A naturalidade CFC é aplicada com continuidade global e normalidade descarregada por positividade do multiplicador. realScalarMultiplier_cfc_ae continua recebendo o símbolo sigmoid em [0,1]; o corte completo não é indevidamente tratado como contração quando ε<1.',
'[REAL] Para Y=cfc Fε R e todo x, a prova obtém (Yx,x−εYx) no grafo do MESMO regularPositiveGenerator pela identificação espectral já existente. As igualdades a.e. de subtração/escala são usadas apenas para esse vetor fixo. O iff bilateral de regularInverseGeneratorCutoff, aplicado ao par, produz Bε((x−εYx)+εYx)=Yx e portanto Bεx=Yx. Não se redefine o inverso, não se assume a igualdade desejada, não se exige x∈D(h), e não se trata h como limitado.',
'[REAL] regularInverseGeneratorCutoff_right consome a ação direita de R que foi reproduzida e aceita no parecer seno11, aplica scalarRightAction_cfc e transporta a pertinência pela igualdade exata de operadores. A ação é na mesma scalarPolarRightAlgebra, cuja propriedade herdada quantifica todo A∈nν e usa o GNS/π/J originais. Não há família aproximante ou pertinência à álgebra direita como premissa residual do teorema concreto.',
'[REAL] A raiz é exatamente hilbertPositiveSqrt do fornecedor V350AntiunitaryPositiveConjugation:15, cuja definição é CFC.sqrt com instâncias fixadas em Hilbert genérico. O helper genérico usa CFC.sqrt_eq_real_sqrt com h0, cfcₙ_eq_cfc com continuidade de Real.sqrt e sqrt(0)=0, e cfc_real_eq_complex com autoadjunção derivada de h0. Assim não introduz raiz concorrente nem postula positividade. scalarRightAction_sqrt recebe b∈E e b≥0; o corolário concreto descarrega ambos usando o corte existente e ε>0.',
'[REAL] Histórico em history_read.json: dois DEV rc1 excluídos (cast/equações e ajuste de instâncias), seguidos do final 20260914_212240_170889 rc0 sem avisos, com os mesmos bytes do snapshot próprio e do Lake autoral. Nenhum print de tentativa falha foi aceito. A auditoria autoral e os streams foram relidos: BadCutoffCFCMirror é recusado por Type mismatch ao substituir R por I−R no CFC. É controle autoral relido, não reexecutado nesta revisão.'
],limits=[
'Este delta paga Bε=cfc Fε R e a ação direita do corte e da sua raiz positiva ORIGINAL para ε>0. Não constrói peso perturbado, limite/ordem das avaliações, tracialidade ou o traço final.',
'Não há novo h, inverso, J, GNS ou condição do gate; nenhum monólito, memória, fonte autoral ou parecer anterior foi modificado. A1(b) completo permanece aberto.'
])
save(OUT/'semantic_notes.json',notes)
print('SEMANTIC_REVIEW_COMPLETE')
