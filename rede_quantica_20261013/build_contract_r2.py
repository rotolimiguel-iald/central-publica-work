"""Consolidate a complete additive R2 after local and remote-source review."""
from pathlib import Path
import datetime as dt
import hashlib,json,os
R=Path(r'C:\IALD\Central de Patentes')
O=R/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE'
def pin(p):
    b=p.read_bytes();return {'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def new(n,x):
    p=O/n;t=p.with_name(p.name+'.tmp')
    if p.exists():raise FileExistsError(p)
    b=(x if isinstance(x,str) else json.dumps(x,ensure_ascii=False,indent=2,allow_nan=False)).encode('utf-8')
    with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert t.read_bytes()==b;os.rename(t,p)

c=json.loads((O/'CONTRATO_REDE_R1.json').read_text(encoding='utf-8'))
c['schema']='iald-network-contract/v2'
c['created_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
c['predecessor']=pin(O/'CONTRATO_REDE_R1.json')
c['review_basis']=[pin(O/'review_contract/REVIEW_CONTRACT_R1.json'),pin(O/'review_deepseek/REVIEW_DEEPSEEK_R1.json')]
device=json.loads((O/'finite_device/RESULTADO_DEVICE_R1.json').read_text(encoding='utf-8'))
c['beta_rule']['measured_runtime']=device['beta_runtime']
c['beta_rule']['value_source']=pin(O/'finite_device/RESULTADO_DEVICE_R1.json')
c['provider_request'].update({'stage':'completed','executor_attempts':1,'response_status':'DECLARADO — useful parts and errors discriminated by local review','result':pin(O/'provider/DEEPSEEK_RESULT_R1.json'),'transport_receipt':pin(R/'work/rede_transport_20261013/DELIVERY_R1.json')})

bs={b['id']:b for b in c['blocks']}
bs['N6_REFINEMENT']['obligations'].extend([
 'RC1: V is a surjective complex-linear isometry on the specified physical one-particle sector.',
 'RC1: for EVERY proper Poincare g, V U_device(g)=U_can(g) V, including the antiunitary component/reflection with its appropriate type.',
 'RC1: require V K_device(W)=K_can(W) for every wedge, or derive this equality from intertwining the actual modular construction. U1 and one B0 alone are insufficient.',
 'The bridge from finite cells to this physical sector must be a defined refinement/continuum construction; H1 cannot be the finite single-site Hilbert by renaming.'
])
bs['N6_REFINEMENT']['falsifier'] += ' The full Poincare, reflection or localized wedge identification fails despite matching translations/one boost.'
bs['N7_BGL_H1']['obligations'][0]='D1a.1 REAL in sandbox: canonicalFub, canonicalPartialFourier, sections AE, and boost intertwining constructed and independently recompiled; use these terms.'
bs['N7_BGL_H1']['obligations'].extend([
 'RC2: T must be positive: forall x in T.domain, 0 <= Re(inner x (T x)). Selfadjointness alone is insufficient.',
 'RC2: construct the maximal multiplication graph T = Phi^(-1) M_exp(sigma/2) Phi with sigma(xi)=4*pi^2*xi, then prove selfadjointness and positivity.',
 'RC2: identify J as the antiunitary polar factor of S=JT. A label or an arbitrary conjugation not tied to localization is insufficient.',
 'Existing D1a3OutputBGL does not carry explicit positivity of T. This R2 proposes the additional proof obligation; it does not modify that kernel structure.',
 'For T -> -T with J fixed, S -> -S and S* S is unchanged, while Fix(S) -> i Fix(S). This is the explicit negative control excluded by RC2.'
])
bs['N7_BGL_H1']['falsifier'] += ' A negative or sign-flipped T passes only the old type without the positive-root proof.'
bs['N2_PHYSICAL_CHANNEL']['obligations'].extend([
 'Do not impose beta on all conventional dissipators: the selected source distinguishes L_diss from beta*gamma_Lambda D[L_holo].',
 'Do not identify a GKLS jump with sqrt(-log Delta) without a proved bridge and a positive operator; -log Delta is not generally positive.',
 'Uniqueness of a stationary state requires a named irreducibility/primitivity or contraction hypothesis and verification.',
 'Dimensional unit check: source OH frequency is 1.667,359 MHz = 1.667359 GHz (Portuguese notation); the reduced synthetic model uses dimensionless INPUT frequencies, not this calibration.'
])
bs['N8_FOCK_WEYL']['obligations'].append('A(O) acts on Gamma_s(H1), not on H1. K(O) is the one-particle real subspace; keep the two representation spaces distinct.')
c['metric_reading']={
 'source':pin(R/'Patentes/MQC - Microprocessador Cúbico/mqc_pi_inpi_relatorio descritivo.pdf'),
 'anchor':'p.8, Eq.(18), visually checked using MQC_PAGE_8_R1.png',
 'render':pin(O/'sources/MQC_PAGE_8_R1.png'),
 'status':'DERIVED_CONDITIONAL_ON_LORENTZIAN_METRIC_INTERPRETATION',
 'equation':'ds^2=A*c^2*dt^2-A^(-1)*dL^2-L^2*dOmega^2; A=1-alpha_hist^2/alpha_c^2',
 'domain':'A>0, radial null curve; alpha_hist is the notation of that source, not a silent reassignment of alpha_EM.',
 'derivation':'0=A*c^2-A^(-1)*(dL/dt)^2 implies abs(dL/dt)=c*A; static proper distance/time are dl=dL/sqrt(A), dtau=sqrt(A)*dt, so abs(dl/dtau)=c.',
 'limit':'As A approaches 0 from above, the coordinate speed approaches 0. At A=0 this static chart is singular; the formula does not derive instantaneous physical communication.',
 'interpretation_limit':'The source calls it informational spacetime. If v_info denotes correlation/inscription, its relation to signal propagation is an additional contract; do not identify the two without proof.',
 'causal_control':'A group-velocity bound alone is not equivalent to relativistic signal causality; use causal support/commutators or a justified front-velocity criterion.'
}
c['verified_deliveries']=[
 pin(O/'light_ray/RESULTADO_LIGHT_RAY_R1.json'),pin(O/'review_light_ray/REVIEW_LIGHT_RAY_R1.json'),
 pin(O/'fubini/DELIVERY_R1.json'),pin(O/'review_fubini/20261013T213537_597067Z/REVIEW_RESULT.json'),
 pin(O/'finite_device/RESULTADO_DEVICE_R1.json'),pin(O/'review_device_r2/REVIEW_DEVICE_R1.json'),
 pin(O/'sources/PUBLIC_PRIMARY_CUSTODY_R1.json')]
c['remote_review_disposition']={
 'accepted_as_already_supported':'Layer separation, coherence normalization, CPTP versus classical coding, GKLS versus modular, explicit refinement obligations.',
 'not_adopted':'Wrong beta decimal; OH factor1000 error; local algebras placed on H1; finite-site reuse of infinite H1; all jumps multiplied by beta; sqrt(-log Delta) without positivity/bridge; unconditional uniqueness; group velocity used as causal criterion.',
 'no_new_remote_theorem_or_lean_inhabitant':True,
 'review':pin(O/'review_deepseek/REVIEW_DEEPSEEK_R1.json')}

appendix = r'''

## 10. R2 — revisão incorporada, em nome de codex-gerente-tgl

Esta versão conserva a R1 em arquivo próprio e incorpora uma revisão local e a
conferência da chamada única DeepSeek. São **dez** blocos, N0–N9. A resposta remota
é [DECLARADO]; não trouxe um habitante Lean nem uma construção 4D concluída.

### Identificação completa da rede (RC1)

O mapa V deve ser unitário entre os setores físicos declarados. Exige-se
VU_device(g)=U_can(g)V para toda a representação de Poincaré considerada,
incluindo a reflexão antiunitária. Exige-se também VK_device(W)=K_can(W), ou a
prova dessa igualdade a partir da construção modular. Entrelaçar apenas U1 e um
boost B0 não determina as outras rotações nem a localização. H1 não pode ser
identificado a um sítio finito por uma troca de nomes.

### Raiz positiva e conjugação polar (RC2)

O contrato antigo tipa T auto-adjunto, mas isso não seleciona a raiz positiva:
trocar T por −T troca S=JT por −S, deixa S†S igual e troca Fix(S) por iFix(S).
A R2 exige T≥0 e o grafo máximo do multiplicador exp(σ/2) após Φ, além de
identificar J com a conjugação polar pertinente. Isso é uma proposta tipada
adicional ao contrato: nenhum tipo do kernel foi editado.

### D1a.1 efetivamente construído

Fubini e Fourier parcial já são objetos no H1 canônico. A ação por seções a.e.,
norma, linearidade, sobrejetividade e o entrelaçamento com B0 foram provados e
recompilados independentemente. Para a convenção da casa, σ(ξ)=4π²ξ e
Φ B0(−2πt) Φ⁻¹ é multiplicação por exp(i t σ(ξ)). Essa identidade espectral,
sozinha, ainda não é a identificação com o modular de uma cunha construída.

A revisão da cópia de Fubini recompilou com EXIT0 e somente o trio; o `.olean`
difere em bytes do original e essa diferença está registrada. Não se afirma
identidade binária. Na rede da reta, a revisão obteve `.olean` idêntico.

### Canal finito e leitura da métrica

O H/salto do Supercondutor foi testado num truncamento 2×2×2, com pré-registro e
142 verificações reproduzidas. As 54 arestas da geometria são [INPUT]; não foi
simulado o Hilbert completo de 27 qubits. A primeira tentativa independente usou
um runtime sem SciPy e falhou; o log foi preservado. A reprodução no mesmo
runtime científico do construtor passou.

Na Eq.(18) do MQC, p.8, escrevendo A=1−α_hist²/α_c², uma curva radial nula em
A>0 satisfaz |dL/dt|=cA. Um observador estático mede velocidade própria c.
Assim A→0⁺ não deriva velocidade coordenada infinita; em A=0 a carta é singular.
O PDF chama essa geometria de informacional: se v_info significar correlação ou
inscrição, a sua relação com a propagação de um sinal precisa ser explicitada.
Não se substitui causalidade por uma simples desigualdade de velocidade de grupo.

### Correções da resposta externa

As álgebras de Weyl atuam no Fock, enquanto K(O) está em H1. Um salto GKLS não
foi identificado a √(−log Δ); −log Δ pode ter ambos os sinais. β multiplica o
termo holográfico da fonte, não todos os dissipadores convencionais. Unicidade
estacionária exige hipótese própria. O decimal β e a conversão de MHz da resposta
externa não foram usados. O valor vigente foi lido do resultado calculado em
runtime; a notação 1.667,359 MHz da fonte corresponde a 1,667359 GHz.

Os detalhes e os pins estão em `review_deepseek/REVIEW_DEEPSEEK_R1.json`,
`review_contract/REVIEW_CONTRACT_R1.json` e `CONTRATO_REDE_R2.json`.
'''

md=(O/'CONTRATO_REDE_R1.md').read_text(encoding='utf-8')
md=md.replace('versão R1','versão R2',1)
md=md.replace('A ponte Fubini está em construção separada desta R1 e não é promovida\na equivalência pronta por este documento.', 'A ponte Fubini foi construída e recompilada independentemente nesta unidade;\nsua entrega e alcance estão atualizados na seção 10.')
md=md.replace('contém nove blocos N0–N9','contém dez blocos N0–N9')
md=md.replace('`CONTRATO_REDE_R1.json` contém','`CONTRATO_REDE_R2.json` contém')
new('CONTRATO_REDE_R2.json',c)
new('CONTRATO_REDE_R2.md',md+appendix)
new('CONTRATO_REDE_R2_PINS.json',{'files':[pin(O/'CONTRATO_REDE_R2.json'),pin(O/'CONTRATO_REDE_R2.md')],'generator':pin(Path(__file__)),'predecessor':pin(O/'CONTRATO_REDE_R1_PINS.json')})
print(json.dumps({'contract':pin(O/'CONTRATO_REDE_R2.json'),'blocks':len(c['blocks'])},ensure_ascii=False))
