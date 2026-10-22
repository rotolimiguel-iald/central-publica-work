from pathlib import Path
from datetime import datetime
import json,hashlib,os,re
O=Path(__file__).resolve().parent;R=O.parent;V=R/'v';M=V/'.lake/packages/mathlib/Mathlib'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def fresh(p,b):
 assert p.parent==O and not p.exists()
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b)
 assert t.read_bytes()==b;os.replace(t,p)
specs=[
 (M/'MeasureTheory/Integral/DominatedConvergence.lean',['tendsto_integral_of_dominated_convergence','tendsto_integral_filter_of_dominated_convergence']),
 (M/'MeasureTheory/Function/L2Space.lean',['memLp_two_iff_integrable_sq_norm']),
 (M/'MeasureTheory/Function/LpSpace/Basic.lean',['memLp','aestronglyMeasurable','coeFn_sub']),
 (V/'TGLExt/V350FourierL1L2.lean',['L2_integral_norm_sq']),
 (V/'TGLExt/V350L2PositiveMultiplier.lean',['realScalarMultiplier_ae']),
 (V/'TGLExt/V350ScalarWeightCompletion.lean',['scalarWeightOrbit_rightRegularization_tendsto']),
 (M/'MeasureTheory/Function/LpSpace/Complete.lean',["tendsto_Lp_iff_tendsto_eLpNorm'"]),
 (M/'MeasureTheory/Function/UniformIntegrable.lean',['tendsto_Lp_finite_of_tendsto_ae'])]
providers=[]
for p,names in specs:
 s=p.read_text(encoding='utf8');decl=[]
 for name in names:
  matches=list(re.finditer(r'^(?:protected |nonrec )?(?:theorem|lemma) '+re.escape(name)+r'(?=\s|\{|\()',s,re.M));assert matches,(p,name)
  # The first declaration is the requested root namespace, not intervalIntegral later in the file.
  m=matches[0];end=s.index(':=',m.end());decl.append(dict(name=name,line=s[:m.start()].count('\n')+1,statement=s[m.start():end].rstrip()))
 providers.append(dict(source=pin(p),declarations=decl))
body='''# Consulta curta — DCT para multiplicadores reais em L² vetorial

[REAL — fornecedores locais lidos; DERIVED — aplicação indicada, sem Lean novo ou build.]

O caminho mais curto localizado é `MeasureTheory.tendsto_integral_of_dominated_convergence` (codomínio escalar ℝ), junto de `TGLV350.Fourier.L2_integral_norm_sq`. Este último já está na árvore própria e é genérico em H complexo completo; seu nome de arquivo Fourier não impõe hipótese Fourier/L¹ ao lema. O precedente `TGLV350.Regular.scalarWeightOrbit_rightRegularization_tendsto` já faz exatamente a passagem DCT → norma² → raiz → Tendsto L², com uma cota 4||f||². Aqui a cota pode ser só ||u||².

Fixe u : RegularHilbert H, g_n e g contínuos, 0≤g_n,g≤1 e convergência pontual g_n(x)→g(x). Use funções ESCALARES explícitas

φ_n(x)=(g_n(x)−g(x))² · ||u(x)||²,   bound(x)=||u(x)||².

Então 0≤φ_n≤bound, φ_n→0 pontualmente e φ_n é AEStronglyMeasurable. O integrável dominante sai diretamente de `(memLp_two_iff_integrable_sq_norm (Lp.memLp u).1).mp (Lp.memLp u)`. Não é necessário que u seja contínuo ou que a constante 1 seja integrável em ℝ. A hipótese de medida finita NÃO é necessária ao DCT escolhido.

Para cada n, `realScalarMultiplier_ae` aplicado a g_n e g, mais `MeasureTheory.Lp.coeFn_sub`, identificam a.e. a diferença dos vetores L² com `(ofReal(g_n−g)) • u`. `norm_smul`, a norma do real embutido em ℂ e `sq_abs` dão, por `integral_congr_ae`,

||realScalarMultiplier g_n ... u − realScalarMultiplier g ... u||² = ∫ x, φ_n(x).

É a identidade `L2_integral_norm_sq` aplicada à diferença, na orientação inversa. Cada n usa apenas os três eventos a.e. correspondentes. Escolher φ_n explicitamente, em vez de usar o representante arbitrário da diferença L² na hipótese pontual do DCT, evita exigir uma nova uniformização dos representantes. Não há interseção a.e. sobre todos u ou sobre índices não enumeráveis.

O DCT escalar com limite zero dá que a integral tende a zero. Compor com `Real.continuous_sqrt` e simplificar `Real.sqrt_sq_eq_abs`, `abs_norm`, `Real.sqrt_zero` fornece a convergência das normas; `tendsto_iff_dist_tendsto_zero` e `dist_eq_norm` concluem a convergência no MESMO L². O trecho já existente de ScalarWeightCompletion, linhas da prova que seguem a identidade de norma², é um molde direto — não há motivo para reconstruir DCT/eLpNorm/toReal.

**Consumidor seno.** Tome m=n+1, g_n(x)=sigmoid(m sin(2πx/m)) e g(x)=sigmoid(2πx). A única nova análise escalar é m sin(a/m)→a; a continuidade da sigmoid dá a convergência acima. O DCT já é genérico e não precisa conhecer seno/sigmoid. A conjugação pela mesma regularSpectralCoordinates é contínua/isométrica, logo leva esse limite ao R_n→R original. Auto-adjunção dos multiplicadores fornece o forte-* sem continuidade forte geral da estrela. Nenhuma norma-operador convergente é afirmada.

**Filtros e alternativas.** A versão sequencial usa ℕ/atTop. `tendsto_integral_filter_of_dominated_convergence` também serve, mas exige `[l.IsCountablyGenerated]`; não a anunciar como DCT de rede arbitrária. `Lp.tendsto_Lp_iff_tendsto_eLpNorm'` aceita filtros arbitrários, porém só CONVERTE uma convergência eLpNorm já demonstrada: não é DCT. `tendsto_Lp_finite_of_tendsto_ae` exige IsFiniteMeasure e UnifIntegrable; não é o atalho adequado para volume em toda ℝ. `fibre_tendsto_of_uniformly_bounded` trata operadores constantes no espaço de base, não um campo g_n(x) variável, e também não substitui esta aplicação.

Nenhuma cobertura do predual, separabilidade de H ou resultado tracial entra. Não foi lida como final a fonte de álgebra enquanto instável. Os tipos abaixo são recortes literais das declarações existentes, não código novo testado. Nas duas declarações DCT, variáveis de seção incluem `{μ : Measure α}`, `[NormedAddCommGroup G] [NormedSpace ℝ G]`; aqui G=ℝ. No lema L² próprio, `[NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]`. No critério de norma² de MemLp, basta `[NormedAddCommGroup F]`.
'''
body+='\nData: '+datetime.now().astimezone().isoformat()+'\n'
for p in providers:
 for d in p['declarations']:
  body+='\n['+d['name']+'](<'+p['source']['path']+':'+str(d['line'])+'>)\n\n```lean\n'+d['statement']+'\n```\n'
mp=O/'CONSULTA_DCT_MULTIPLICADORES_L2.md';fresh(mp,body.encode('utf8'))
# Preserve the own binary provenance without reexecuting it.
base=json.loads((R/'revisao_limites_direita/compilation.json').read_bytes())
objects=[x for x in base['objects'] if x['module'] in ['TGLExt.V350FourierL1L2','TGLExt.V350L2PositiveMultiplier','TGLExt.V350ScalarWeightCompletion']]
for x in objects:
 for field in ['source','own','trace']:assert pin(Path(x[field]['path']))==x[field]
data=dict(timestamp=datetime.now().astimezone().isoformat(),status='READ_ONLY_API_CONSULTATION__NO_NEW_LEAN',providers=providers,existing_own_objects=objects,base_compilation=pin(R/'revisao_limites_direita/compilation.json'),report=pin(mp),builds_executed=0,new_lean_targets=0)
jp=O/'CONSULTA_DCT_MULTIPLICADORES_L2.json';fresh(jp,(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf8'))
print(json.dumps(dict(md=pin(mp),json=pin(jp)),ensure_ascii=False))
