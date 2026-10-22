from pathlib import Path
from datetime import datetime
import hashlib,json,os,re

R=Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012')
V=R/'v'; OUT=R/'revisao_consulta_peso_perturbado'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def fresh(p,b):
    assert p.resolve().is_relative_to(OUT.resolve()) and not p.exists()
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b;os.replace(t,p)

suppliers={
 'V350ScalarRightAverage':['scalarOrbit_right_average_norm_le','scalarOrbit_right_average_tendsto','scalarWeight_right_average_le'],
 'V350DualSemifiniteIdeal':['HasFiniteDualSquare.left_mul','regularAverage_hasFiniteDualSquare'],
 'V350RegularApproximation':['regularAverage_apply','regularAverage_tendsto_identity'],
 'V350ScalarWeightDomain':['finiteDualLeftIdeal_le_scalarWeight'],
 'V350DualWeightForm':['dualQuadraticIntegrand_measurable','dualQuadraticIntegral'],
 'V350ScalarWeightCompletion':['scalarWeightOrbit_rightRegularization_tendsto'],
 'V350ScalarDualWeight':['scalarDualWeight','scalarDualWeight_normal'],
 'V350DualFixedWeightLaws':['PositiveCoreInput.conjugate'],
 'V350RegularNormality':['vonNeumann_exists_positive_isLUB','vonNeumann_isLUB_coe'],
 'V351ScalarImaginaryCoreAction':['scalarTomitaImaginaryPower_core_conjugation'],
 'V351RegularImaginaryPowers':['regularSpectralCoordinates_character','regularPositiveGenerator_imaginaryPower'],
 'V351InverseCutoffCFC':['regularInverseGeneratorCutoff_cfc','regularInverseGeneratorCutoff_sqrt_right'],
 'V351PerturbedWeightNorm':['scalarWeight_right_perturbed_norm','scalarWeight_inverseCutoff_perturbed_norm'],
}
records=[]
for module,names in suppliers.items():
    p=V/'TGLExt'/(module+'.lean');txt=p.read_text(encoding='utf-8-sig');decl=[]
    for name in names:
        m=re.search(r'^(?:noncomputable\s+)?(?:def|theorem)\s+'+re.escape(name)+r'(?=\s|\()',txt,re.M)
        assert m,(module,name)
        decl.append(dict(name=name,line=txt[:m.start()].count('\n')+1))
    records.append(dict(source=pin(p),declarations=decl))
p=V/'.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Add.lean'
txt=p.read_text(encoding='utf-8-sig');m=re.search(r'^theorem lintegral_liminf_le\b',txt,re.M);assert m
records.append(dict(source=pin(p),declarations=[dict(name='lintegral_liminf_le',line=txt[:m.start()].count('\n')+1)]))
timestamp=datetime.now().astimezone().isoformat()
body=r'''# Consulta — peso dos cortes em todos os positivos e limite

[DERIVED — proposta matemática, sem novos teoremas Lean ou testes nesta consulta]

**Há uma ponte concreta pelos regularizadores existentes. Ela paga recuperação de valores e permite transportar a ordem dos coeficientes aos pesos. A tracialidade continua sendo uma obrigação modular distinta.**

Escrevo N para o mesmo core, ν para scalarDualWeight, J para o polar original no H_I, Bε=(h+ε)⁻¹ e sε=√Bε, ε>0. Não identifico o gerador h na Hilbert regular com Δν no H_I.

1. **Definir os pesos não exige estender a inscrição.** Para X∈N₊, νε(X):=ν(sε X sε) já faz sentido em ENNReal, inclusive ∞. É necessário apenas empacotar a positividade e pertinência do sanduíche. PositiveCoreInput.conjugate não é esse adaptador: recebe um operador de dualFixedCore, enquanto os cortes estão em N. As leis zero/soma/escala vêm de ν; normalidade exige explicitar que o sanduíche leva o supremo interno positivo dirigido ao supremo correspondente, usando o limite forte já disponível. Nenhum novo predual é necessário aqui.

2. **Recuperação sem minorantes.** Tome δ_n=1/(n+1)>0 e e_n=regularAverage P δ_n. Para TODO a∈N, a e_n∈I⊆nν. A cota scalarWeight_right_average_le vale sem hipótese de finitude; a convergência scalarOrbit_right_average_tendsto também. Aplicar Fatou aos integrandos ENNReal de norma-quadrado, com a mesma constante positiva finita dualHaarFactor, dá

   ν(a*a) ≤ liminf_n ν((a e_n)*(a e_n)) ≤ limsup_n ν((a e_n)*(a e_n)) ≤ ν(a*a).

   Portanto há convergência no intervalo estendido, inclusive quando o valor final é ∞, e igualdade com o supremo desses valores. Não se afirma monotonia da sequência. O fornecedor lintegral_liminf_le aceita a sequência atTop; não é necessário nem alegado um Fatou para redes arbitrárias. A versão DCT da convergência GNS existente continua restrita a a∈nν.

3. **A comutação que falta explicitar.** Para aplicar a recuperação ao mesmo input X em todos os pesos dos cortes, provar [e_n,sε]=0. Uma rota já sustentada por fornecedores: regularSpectralCoordinates_character põe λ_t em multiplicação por caracteres nas coordenadas onde R é multiplicação por sigmoid; logo [λ_t,R]=0. CFC transporta isso para sε, e regularAverage_apply transporta ao integral de λ_t. Não localizei um lema pronto com essa conclusão na busca nominal delimitada; registro-o como adaptador a provar. Não deduzo essa comutação de b∈E para um b arbitrário.

4. **Extensão efetiva da comparação.** Para X≥0 ponha a=√X e X_n=e_n* X e_n=(a e_n)*(a e_n). Esses X_n têm peso ν finito. Com a comutação do item 3,

   νε(X_n)=ν(((a sε)e_n)*((a sε)e_n)),  νε(X)=sup_n νε(X_n).

   O novo teorema de norma, aplicado a a e_n, expressa νε(X_n) por ofReal da forma quadrática de π(Bε) no vetor J⁻¹Λ(a e_n). Assim Bε≤Bη implica νε(X_n)≤νη(X_n) e, tomando sup_n, νε(X)≤νη(X) para TODO X≥0. A ordem Bε≤Bη para ε≥η é uma comparação escalar dos mesmos cortes CFC de R. **Não** se utiliza sε X sε≤sη X sη. Tampouco X_n≤X: essas compressões não são a família falsa de minorantes finitos de ν.

5. **O limite ainda precisa de sua própria semifinitude.** Depois da ordem anterior, τ(X)=sup_m ν_{1/(m+1)}(X) é o candidato crescente; soma e normalidade seguem das respectivas leis e troca de supremos. A cofinalidade fornece a leitura sup_{ε>0}. Não basta dizer que cada νε é semifinito: um supremo crescente de pesos semifinitos pode perder essa propriedade.

   Uma opção concreta, sem PVM, é d_k=√(1−δ_k Bδ_k), δ_k=1/(k+1). São funções CFC do mesmo R, pertencem a E, e os símbolos dão d_k→1 fortemente e Bε d_k²≤δ_k⁻¹ I. A identidade de norma para b=d_k sε então dá τ((a d_k)*(a d_k))≤δ_k⁻¹ν(a*a) para a∈nν. Como a d_k→a fortemente e nν é fracamente denso, obtém-se a densidade usual de nτ. Estes cálculos e a transferência de limites ainda são lemas a formalizar, não resultados novos certificados por esta nota. A fidelidade pode ser tratada pela fidelidade de ν e imagem densa de sε. Só DEPOIS da tracialidade cabe pagar o campo de semifinitude por minorantes do contrato do traço.

6. **Onde entra Tomita/KMS de verdade.** A norma atual já consome o J original pela ação direita. Isso não demonstra que o limite é traço. O fornecedor scalarTomitaImaginaryPower_core_conjugation identifica a ação das potências do Tomita original com Ad λ_t, e regularPositiveGenerator_imaginaryPower identifica λ_t com h^{it}. A ponte de perturbação ainda necessária é a especialização

   σ_t^τ(X)=h^(−it) σ_t^ν(X) h^(it),

   para o τ efetivamente construído acima; então os fatores cancelam e o grupo modular de τ é trivial. A literatura fornece precisamente a perturbação por operador positivo afiliado ao centralizador modular, com construção crescente e fórmula do grupo modular: Hiai, §9, Lema 9.1, Proposição 9.3, Teorema 9.4 e aplicação 9.9. Essa é a etapa modular/KMS, não mera invariância. Aqui ela permanece uma obrigação de transporte formal para os objetos concretos, não um axioma admitido. [Fonte primária](https://arxiv.org/pdf/2004.02383).

   Alternativamente, provar diretamente τ(a*a)=τ(aa*) para todo a∈N, incluindo valores infinitos, exige a correspondente identidade de formas e um domínio/core que justifique sua extensão. A fórmula de norma isolada não fornece essa identidade. Não é necessário reconstruir GNS nem exigir uma equivalência geral de preduais; também não basta renomear a covariância já paga como o teorema de perturbação.

[OPEN] Menor sequência restante: recuperação ENNReal por médias; comutação média/corte; comparação e leis dos pesos em todos os positivos; construção e densidade do domínio do limite; identidade de perturbação modular/tracialidade. A consulta não acrescenta requisitos a gate/métrica, não modifica a errata de semifinitude de ν e não altera os pareceres entregues.
'''
body+='\n\n[REAL — fornecedores locais consultados; leitura, não recompilação nesta nota]\n\n'
for rec in records:
    p=rec['source']
    body+='- '+', '.join('['+d['name']+'](<'+p['path']+':'+str(d['line'])+'>)' for d in rec['declarations'])+' — SHA256 `'+p['sha256']+'`.\n'
meta=dict(timestamp=timestamp,status='DERIVED_CONSULTATION__ALL_POSITIVE_ADAPTERS_AND_TRACE_OPEN',new_lean_theorems=0,compilation_performed_for_consultation=False,sourcepins=records,source_scope='Targeted local suppliers, not exhaustive search',formal_norm_review=pin(R/'revisao_peso_perturbado_norma/REVIEW_A1_PERTURBED_WEIGHT_NORM_FINAL.json'),fiche=pin(R/'REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA.json'),primary_reference=dict(url='https://arxiv.org/pdf/2004.02383',sections=['9.1','9.3','9.4','9.9'],role='Known perturbation theorem; not imported as a new Lean premise'),open_obligations=['ENNReal regular-average recovery including infinity','commutation of regular averages with original cutoff roots','coefficient order transferred to all positive inputs','semifinite limit domain via bounded damping, or equivalent justified supplier','specialized modular perturbation identity / full traciality'],false_finite_minorants_of_nu_used=False,author_sources_modified=False,memories_modified=False)
OUT.mkdir(exist_ok=True)
mp=OUT/'CONSULTA_PESO_PERTURBADO_TODOS_POSITIVOS.md';fresh(mp,('Data: '+timestamp+'\n\n'+body).encode())
meta['note']=pin(mp)
jp=OUT/'CONSULTA_PESO_PERTURBADO_TODOS_POSITIVOS.json';fresh(jp,(json.dumps(meta,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(dict(note=pin(mp),evidence=pin(jp)),ensure_ascii=False))
