"""Record the reviewed polar factor, concrete weight, and spectral condition once."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MARKER='fecho_polar_nonabelian_positive_core_20261015_r7'
reg.DEST=OUT

def main():
    assert not (OUT/'PROGRESS_R7.json').exists()
    claim=reg.call([CLI,'ver','F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem']==WHO and dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    for name in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md','AVISO_GERENCIA.md'):
        assert name in claim['nota']
    paths=[
        'selfadjoint_root_review_r1/REVISAO_SELFADJOINT_ROOT_R1.json',
        'polar_root_review_r1/REVISAO_POLAR_ROOT_R1.json',
        'gamma_unbounded/FINAL_CANONICAL_FOCK_POLAR_RECEIPT_R1.json',
        'gamma_unbounded/FINAL_CANONICAL_FOCK_DELTA_RECEIPT_R1.json',
        'gamma_unbounded/FINAL_CANONICAL_GRAPH_REALIZATION_RECEIPT_R1.json',
        'gamma_unbounded/FINAL_ACTUAL_MODULAR_FLOW_RECEIPT_R1.json',
        'network_review/SQUARE_AND_REGULARIZED_ROOT_SEMANTIC_REVIEW_R1.json',
        'network_review/CANONICAL_GRAPH_REALIZATION_SEMANTIC_REVIEW_R1.json',
        'network_review/ACTUAL_MODULAR_FLOW_SEMANTIC_REVIEW_R1.json',
        'weyl_net_wiring/NONABELIAN_WEDGE_DELIVERY_R1.json',
        'wedge_weight_review/REVISAO_WEDGE_R1.json',
        'wedge_weight_review/REVISAO_FAITHFUL_WEIGHT_R1.json',
        'nonabelian_adapter_review/REVISAO_ADAPTER_R1.json',
        'takesaki_fock/FOCK_FINITE_WEIGHT_RECEIPT_R1.json',
        'network_review/FINITE_WEIGHT_SEMANTIC_REVIEW_ROOT_R1.json',
        'network_review/POSITIVE_CORE_ASSEMBLY_SEMANTIC_REVIEW_R1.json',
        'weyl_net_wiring/attempts/20261015T202725_508417Z/RECEIPT.json',
        'gamma_positive/FINAL_GAMMA_POSITIVE_RECEIPT_R1.json',
        'gamma_unbounded/FINAL_CANONICAL_ONE_PARTICLE_BW_RECEIPT_R1.json',
        'network_review/ONE_PARTICLE_BW_SEMANTIC_REVIEW_R1.json',
        'takesaki_fock/FOCK_WEIGHT_DOMAIN_INVARIANCE_RECEIPT_R1.json',
        'gamma_positive_root_review_r2/REVISAO_GAMMA_POSITIVE_ROOT_R2.json',
    ]
    evidence=[pin(OUT/p) for p in paths]
    polar=json.loads((OUT/paths[1]).read_bytes())
    positive=json.loads((OUT/paths[-1]).read_bytes())
    assert polar['status']=='PASS_WITH_STATED_SCOPE' and positive['status']=='PASS_WITH_STATED_SCOPE'
    progress=dict(unit='F1.FECHO_20261015',claim_event=845,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),status='EM_CURSO_FULL_R1_R10_PRESERVED',
        evidence=evidence,requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'),
        polar='On the same Fock and Weyl/vacuum pair, the positive exponential lift G is self-adjoint and S=JG. The maximal antilinear adjoint and the genuine two-application domain identify Delta=G squared=S-dagger S. Independent root reconstruction covers the bounded tensor/Gamma infrastructure and concrete polar factor.',
        spectral='The actual Tomita square is positive self-adjoint; its regularized graph and spectral imaginary-power unitary group are constructed. The latter is strongly continuous and gives a PairTomita realization for that CFC flow. On H1 the actual resolvent of TW squared and its spectral flow are identified with B0(-2*pi*t). Equality to Gamma(B0) on the full Fock and KMS remain open.',
        wedge='J R(KWR) J equals R(KWR-prime), and these algebras commute. The concrete standard wedge is nonisotropic and its Weyl algebra is nonabelian. Full commutant equality is not asserted.',
        positive='Positive energy is now a theorem for the same Fock: the actual orbital contraction is lifted sectorwise and analyticity extends from the total exponential family by uniform coefficient bounds. Its real boundary is the original Gamma(U1). No Fock analyticity premise is imported.',
        weight='The dual weight on the actual Fock regular core is faithful. A concrete averaged element has quadratic weight exactly one, and the finite-weight ideal is strongly dense. The full scalar finite-weight left ideal and dual invariance have also been constructed. A typed nonzero witness rules out using this invariant weight itself as the exp(-s)-scaled trace; the distinct perturbed trace remains open.',
        adapter='The additive NetworkPositiveCore adapter has 24 explicit remaining fields. Nonabelianity and positive energy are supplied by actual theorems. The global CanonicalNetInput and the whole remaining record have no exhibited joint inhabitant; this is a field count, not a count of independent mathematical problems.',
        review=dict(polar_declarations_including_private=polar['all_declarations_including_private'],
            positive_declarations_including_private=positive['all_declarations_including_private'],
            distinction='Polar and positive-energy review include independent recompilation. Delta, regularized graph, spectral flow, finite weight and the latest positive-core adapter have separate source-semantic reviews, without an additional independent rebuild in those reviews.'),
        remaining=['Equality of the actual modular spectral flow with Gamma(B0), and KMS',
            'Gamma_no_fixed for the general family in the legacy interface',
            'The actual Fock Takesaki scaled trace and finite split projection',
            'Global localized net/device realization and joint Maxwell source',
            'Explicit all-directions H3 scope and final joint independent review',
            'Whole-main terminal receipt and final integration of the newest components'],
        runtime='The real final main is managed in work/rite394_20261015/r3. This progress receipt does not certify its terminal exit or a seal.',
        production_modified=False,gate_moved=False,new_provider_calls=0)
    new(OUT/'PROGRESS_R7.json',progress)
    text=f'''\n\n## 15/10/2026 — Parte polar concreta, cunha não abeliana e energia positiva
<!-- {MARKER} -->
Em nome de {WHO}, unidade F1.FECHO_20261015, reivindicação845 conferida.
[REAL — sandbox e revisão independente] No MESMO Fock e par Weyl/vácuo,
o lift positivo G é auto-adjunto e S=JG; o adjunto antilinear e o domínio
de duas aplicações identificam Δ=G²=S†S. A raiz recompilou a infraestrutura
tensorial/Γ e a parte polar, auditando {polar['all_declarations_including_private']} declarações locais.
A cunha concreta é não isotrópica e sua álgebra de Weyl é não abeliana.
J R(KWR) J=R(KWR′) foi provado, sem afirmar igualdade com todo o comutante.
[REAL — construção com alcance explícito] Δ é positivo auto-adjunto; o
grafo regularizado e seu fluxo espectral CFC foram construídos. O fluxo é
unitário e fortemente contínuo. Em H1, o resolvente real de TW² e seu fluxo
espectral já se identificam com B0(−2πt). Transportar isso para Γ(B0) na
Fock inteira ainda falta.
[REAL — revisão independente] A condição espectral Γ_positive é agora termo
na Fock: multiplicador orbital concreto, Γ limitada e extensão analítica por
totalidade exponencial. A recompilação auditou {positive['all_declarations_including_private']} declarações locais no trio.
O adaptador novo deixa24campos explícitos: não comutatividade e energia positiva
entram por teorema. A contagem não equivale a24problemas matemáticos independentes;
a rede global e o registro conjunto ainda não têm habitante exibido.
[REAL — construção do peso] O peso dual do core regular da mesma Fock é fiel;
há elemento de peso quadrático1 e ideal de peso finito fortemente denso.
Isso ainda não fornece o traço escalado. Revisões de fonte dos consumidores
mais recentes são identificadas separadamente das recompilações independentes.
[OPEN] Identidade modular/boost e KMS, Γ_no_fixed geral, traço escalado,
rede global/dispositivo, matéria conjunta, alcanceH3 e revisão final.
O main integral tem acompanhamento próprio; este registro não declara seu
encerramento. EscopoR1–R10 preservado. Nenhum gate ou produção mudou.
Evidência: `{OUT/'PROGRESS_R7.json'}`, SHA256`{pin(OUT/'PROGRESS_R7.json')['sha256']}`.
'''
    new(OUT/'MEMORY_ADDITION_R7.txt',text)
    surfaces=[ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',ROOT/'memory/TGL_ATLAS.md',ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    memories=[append_bytes(p,text,MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R7.json',dict(unit=progress['unit'],claim=claim,surfaces=memories,evidence=pin(OUT/'PROGRESS_R7.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R7.json',dict(tipo='ANOTACAO',rota_id='formal.f1_rede.concrete_bosonic_kinematics',dominio='FORMAL',
        titulo='Polar concreta e energia positiva na mesma Fock; peso finito não vácuo',
        resultado=progress['polar']+' '+progress['positive']+' '+progress['weight'],estatuto='REAL — componentes; EM_CURSO — conjunto',status='EM_CURSO',
        veredito='PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',defeito='BW/KMS, Γ_no_fixed geral, traço escalado e objetos globais/matéria ainda pendentes.',
        proximo_passo='Identificar fluxo modular com boost; construir Γ_no_fixed e traço da mesma Fock; conferir main integral.',onde=str(OUT),
        artefatos=[str(OUT/'PROGRESS_R7.json'),str(OUT/'MEMORY_PROGRESS_R7.json')],olhou_dados=False))
    new(OUT/'ACOM_PROGRESS_REQUEST_R7.json',dict(operation='transition',reference=str(WORK/'ACOM_REFERENCE.json'),expected_revision=35,event_id=MARKER,
        actor=dict(id=WHO,kind='agent'),changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',
            text=progress['polar']+' '+progress['spectral']+' '+progress['wedge']+' '+progress['positive']+' '+progress['weight']+' '+progress['adapter'],
            sources=[dict(kind='artifact',ref=str(OUT/'PROGRESS_R7.json'),sha256=pin(OUT/'PROGRESS_R7.json')['sha256'])])],
            flow=dict(phase='concrete_polar_positive_energy_and_nonabelian_wedge',next_action='Identify CFC flow with Gamma boost and prove KMS, general Gamma no-fixed, actual scaled trace, global net and joint Maxwell. Verify whole main and preserve R1-R10.'))))
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R7.json'),memories=len(memories)),ensure_ascii=False))

if __name__=='__main__':main()
