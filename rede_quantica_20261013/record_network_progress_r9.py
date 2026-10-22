"""Append scoped progress, preserving prior evidence and byte backups."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MARKER = 'fecho_full_BW_orbital_annihilation_index_20261015_r9'
reg.DEST = OUT


def main():
    assert not (OUT/'PROGRESS_R9.json').exists()
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO and dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    for name in ('DIARIO_CONSTRUCAO_QG.md', 'TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'AVISO_GERENCIA.md'):
        assert name in claim['nota']
    paths = [
        'bw_global_review/REVISAO_BW_GLOBAL_R1.json',
        'network_review/GLOBAL_FOCK_BW_SEMANTIC_REVIEW_R1.json',
        'weyl_net_wiring/FINAL_MODULAR_CORE_ASSEMBLY_RECEIPT_R1.json',
        'orbital_rotation/FINAL_ORBITAL_ROTATION_RECEIPT_R1.json',
        'network_review/ORBITAL_ROTATION_SEMANTIC_REVIEW_ROOT_R1.json',
        'orbital_rotation/FINAL_ORBITAL_CONTINUITY_RECEIPT_R1.json',
        'network_review/ORBITAL_CONTINUITY_SEMANTIC_REVIEW_ROOT_R1.json',
        'maxwell_annihilation/FINAL_ANNIHILATION_RECEIPT_R1.json',
        'network_review/ANNIHILATION_SEMANTIC_REVIEW_R2.json',
        'full_rite/reconciliation_r2/RECONCILIATION.json',
        'full_rite/declaration_sources_r3/RECEIPT.json',
        'full_rite/qualified_index_tests_r2/RESULT.json',
        'full_rite/reconciliation_candidate_r3/TESTS.json',
        'network_review/RECONCILIATION_SEMANTIC_REVIEW_R2.json',
        'network_bundle_r7/PLAN.json']
    evidence = [pin(OUT/p) for p in paths]
    adapter = json.loads((OUT/paths[2]).read_bytes())
    assert adapter['fields_remaining'] == 21 and adapter['status'] == 'REAL_BUILD_EXIT_0'
    claims = {
        'bw': 'The actual CFC modular flow of the same concrete Fock Weyl/vacuum Tomita pair is now equal to Gamma(B0(-2*pi*t)) on every sector, including the vacuum sector. The resulting canonical_pair_tomita supplies the exact PairTomitaAnalyticRealizationMeasured. Source/log/hash reviews by separate hands are pinned; no independent rebuild is claimed by those reviews.',
        'adapter': 'The joint adapter consumes concrete BW and KMS as terms. Twenty-one explicit trace/PF fields remain, together with the separate CanonicalNetInput. This count is an interface count, not twenty-one independent problems, and no joint inhabitant has been exhibited.',
        'spatial': 'On the original massless H1, the whole real spatial orthogonal group has a measure-preserving inverse-pullback unitary action, strongly continuous in the existing operator-norm topology. Covariance of the actual U1 translations holds for every Q. Local finiteness of the orbital measure is derived despite its integrable zero-momentum singularity. The action remains scalar on the helicity coordinates; no Wigner helicity cocycle or full Poincare/global net is claimed.',
        'annihilation': 'The operator a(f) is a well-defined linear partial map on the dense invariant span of exponential vectors in the same Fock, with a(f)e(g)=inner(f,g)e(g), a(f)vacuum=0, and a concrete nonzero-action witness. Two modules, eight printed declarations, only the trio, and a separate source review. Creation, Segal field, physical smearing, stress tensor and Maxwell certificate are not supplied by this receipt.',
        'index': 'The compiler-derived source inventory exports 26797 fully qualified declarations, including generated and quoted Unicode names. The replacement index passes fifteen checks; the additive main reconciliation passes twelve isolated consumer checks, with independent source review. It preserves the axiom, missing-evidence and ambiguous-alias refusals. This is not a fresh execution of the entire modified program.',
        'runtime': 'Seventeen historical full-run differences have a pinned diagnosis. Existing results.json was copied byte-for-byte; the old recorded digest used normalized text while the custody digest uses raw CRLF bytes. The historical evidence records their SHA16 prefixes, not full hashes. No source change is inferred by comparing those different digest schemes. The prior real main still has its visible DES_Y3 offline refusal; no new main or observed-data retrieval occurred.',
        'integration': 'The new transposed bundle contains 155 modules, reuses 48 previously compiled modules, and is compiling the remaining 107 in isolation. Import formatting and Lean namespace-cache resolution failures remain preserved as attempts. Original proof source bytes are pinned; no completed bundle audit is asserted yet.'}
    progress = dict(unit='F1.FECHO_20261015', claim_event=845,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_R1_R10_PRESERVED', evidence=evidence,
        requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'), **claims,
        remaining=['Complete and verify transposed bundle and current program consumers',
            'Full weight-star-domain modular identification, scaled trace and finite split projection',
            'Lorentz/helicity and globally localized net on the same objects',
            'Creation/physical smearing/Maxwell source and explicit all-directions H3 scope',
            'Joint inhabited contract and independent final review'],
        production_modified=False, gate_moved=False, new_provider_calls=0)
    new(OUT/'PROGRESS_R9.json', progress)
    text = f'''\n\n## 15/10/2026 — BW em toda a Fock; rotações orbitais, aniquilação e índice exato
<!-- {MARKER} -->
Em nome de {WHO}, unidade F1.FECHO_20261015, reivindicação845 vigente conferida.
[REAL — sandbox] A igualdade do fluxo modular real com Γ(B0(−2πt)) vale agora
em TODOS os setores da mesma Fock, incluindo o vácuo. canonical_pair_tomita
fornece o tipo exato de Tomita do par Weyl/vácuo. Revisões independentes de
fontes/logs/pinos estão custodiadas; elas não alegam recompilação independente.
[REAL — composição parcial] O adaptador recebe BW e KMS por termo. Restam21
campos explícitos de traço/PF e CanonicalNetInput separado; o conjunto ainda
não tem habitante exibido. Campo de interface não é contagem de problemas.
[REAL] O grupo ortogonal espacial inteiro atua unitariamente e de forma
fortemente contínua no H1 original; a covariância das translações U1 vale
para todo Q. A medida orbital é localmente finita por prova. A ação é escalar
nas coordenadas de helicidade: o cociclo de Wigner e a rede global seguem à parte.
[REAL] a(f)e(g)=⟪f,g⟫e(g) foi construído no span exponencial denso e invariante,
com a(f)Ω=0 e testemunha não nula. Oito declarações impressas no trio e revisão
de fonte separada. Este recibo não fornece criação, smearing ou Maxwell.
[REAL — engenharia] O compilador localizou26797nomes qualificados, incluindo
gerados/Unicode. Índice:15verificações; composição Python:12verificações de
consumidores isolados e revisão independente. Não são um novo main completo.
[ERRATA DE LEITURA AO LADO] O hash histórico de results.json usava texto
normalizado; a custódia atual usa bytes CRLF. A fonte antiga registra prefixos
SHA16. Comparar os dois esquemas não demonstra mudança do arquivo.
[EM_CURSO]155módulos em integração isolada;48reaproveitados e107a compilar.
Tentativas de formatação/importação preservadas. O main anterior continua
com a recusa DES_Y3offline explicitamente registrada, sem PASS global.
[OPEN] Rede Lorentz/helicidade global, traço escalado, matéria conjunta,
alcance H3 e integração final permanecem no objetivo integral R1–R10.
Evidência: `{OUT/'PROGRESS_R9.json'}`, SHA256`{pin(OUT/'PROGRESS_R9.json')['sha256']}`.
Nenhum original de produção, provedor, dado observado ou gate mudou.
'''
    new(OUT/'MEMORY_ADDITION_R9.txt', text)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
        ROOT/'memory/TGL_INDICE_VIVO.md', ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    memories = [append_bytes(p, text, MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R9.json', dict(unit=progress['unit'], claim=claim,
        surfaces=memories, evidence=pin(OUT/'PROGRESS_R9.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R9.json', dict(tipo='ANOTACAO',
        rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='BW global na mesma Fock; ação orbital contínua e aniquilação concretas',
        resultado=' '.join(claims.values()), estatuto='REAL — componentes; EM_CURSO — conjunto',
        status='EM_CURSO', veredito='PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',
        defeito='Rede global, traço escalado, matéria e composição conjunta ainda sem habitante exibido.',
        proximo_passo='Concluir integração isolada e continuar construção sobre o acervo existente.',
        onde=str(OUT), artefatos=[str(OUT/'PROGRESS_R9.json'), str(OUT/'MEMORY_PROGRESS_R9.json')], olhou_dados=False))
    new(OUT/'ACOM_PROGRESS_REQUEST_R9.json', dict(operation='transition',
        reference=str(WORK/'ACOM_REFERENCE.json'), expected_revision=37, event_id=MARKER,
        actor=dict(id=WHO, kind='agent'), changes=dict(records=[dict(id=MARKER,
            kind='fact', statute='REAL', text=' '.join(claims.values()),
            sources=[dict(kind='artifact', ref=str(OUT/'PROGRESS_R9.json'),
                sha256=pin(OUT/'PROGRESS_R9.json')['sha256'])])],
            flow=dict(phase='full_Fock_BW_spatial_continuity_annihilation_and_exact_index',
                next_action='Compile and audit isolated bundle, continue weight modular/trace, full Lorentz/helicity net and Maxwell; preserve all R1-R10.'))))
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R9.json'), memories=len(memories)), ensure_ascii=False))


if __name__ == '__main__':
    main()
