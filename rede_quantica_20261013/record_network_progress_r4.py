"""Record verified wedge progress without promoting the still-open joint contract."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
reg.DEST = OUT
MARKER = 'fecho_standard_wedge_pair_tomita_20261015_r4'


def main():
    if (OUT/'PROGRESS_R4.json').exists():
        raise FileExistsError('Recover receipt; do not repeat memory append')
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    for name in ('DIARIO_CONSTRUCAO_QG.md', 'TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'AVISO_GERENCIA.md'):
        assert name in claim['nota']
    evidence = [
        'wedge_exponential/FINAL_WEDGE_EXPONENTIAL_RECEIPT_R1.json',
        'wedge_cyclic/FINAL_WEDGE_CYCLIC_RECEIPT_R1.json',
        'wedge_review/REVISAO_CUNHA_R1.json',
        'weyl_review/REVISAO_WEYL_CONTINUIDADE_CAMPO_R1.json',
        'pair_wiring_review/REVISAO_PAIR_WIRING_R1.json',
        'gamma_unbounded/FINAL_EXPONENTIAL_LIFT_RECEIPT_R1.json',
        'gamma_unbounded/FINAL_LIFT_POSITIVITY_RECEIPT_R1.json',
        'full_rite/guard_review/REVISAO_GUARD_R3_R4_R1.json',
    ]
    builds = []
    for name in ('CanonicalWeylAssemblyR5', 'CanonicalWedgeFlowR2',
                 'PairTomitaClosabilityR2', 'PairClosedTomitaR2',
                 'OneParticleSymplecticR2', 'WedgePairTomitaR2', 'WeylAntiunitaryR4'):
        source = OUT/'weyl_net_wiring'/(name+'.lean')
        candidates = []
        for p in (source.parent/'attempts').glob('*/RECEIPT.json'):
            d = json.loads(p.read_bytes())
            if d.get('exit_code') == 0 and d.get('source', {}).get('sha256') == pin(source)['sha256']:
                candidates.append((p, d))
        assert candidates, name
        p, d = sorted(candidates)[-1]
        assert all(pin(a['path']) == a for a in d['artifacts'])
        assert 'sorryAx' not in (p.parent/'AXIOMS.txt').read_text(encoding='utf-8')
        builds.append(dict(source=pin(source), receipt=pin(p), exit=0, seconds=d['seconds']))
    progress = dict(unit='F1.FECHO_20261015', claim_event=845,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_PARTIAL_VERIFIED_CONSTRUCTION_FULL_R1_R10_PRESERVED',
        requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'),
        evidence=[pin(OUT/p) for p in evidence], builds=builds,
        constructed='Exp(K) totality, cyclic and separating vacuum for R(K), concrete standard wedge boost flow, actual closed densely defined involutive pair Tomita, and Gamma(J)/Weyl intertwining on the same Fock.',
        independent_review='Four wedge recompilations and seven pair/wiring recompilations passed. Pair checker covers 181 declarations with no axioms outside the trio. Five of seven pair oleans are identical; assembly and antiunitary differ, without an asserted cause.',
        assembly='Two former hypotheses, wedge_cyclic and wedge_separating, are now derived terms. Ten original interface fields are supplied by constructed components; the remaining analytic record has not been inhabited.',
        unbounded='Closed dense symmetric exponential lift and its positivity compiled; independent review of these newest modules remains pending. Self-adjointness and identification with the pair polar operator are not asserted.',
        rite='Earlier full main still running at this snapshot, without terminal PASS. Corrected Python guard reviewed 17/17; it is not OS isolation. Offline MiKTeX patch being independently reviewed. New candidate integration is under preparation.',
        remaining=['Identify actual pair Tomita polar factors and modular KMS',
                   'Global localization/device realization',
                   'Actual Fock core and modular weight/trace identification',
                   'Joint nontrivial Maxwell/stress realization and all-directions H3 scope',
                   'New candidate full main and independent joint review'],
        no_new_provider_or_production_change=True)
    new(OUT/'PROGRESS_R4.json', progress)
    text = f"""\n\n## 15/10/2026 — Cunha padrão e Tomita do par na realização Fock existente
<!-- {MARKER} -->
Em nome de {WHO}, unidade F1.FECHO_20261015, reivindicação845 conferida.
[REAL — termos em sandbox e revisão independente] A totalidade das exponenciais
da cunha foi ligada ao vácuo cíclico e separante de R(K). Esses dois campos saíram
das hipóteses da montagem: agora são termos derivados. O fluxo de boosts preserva
a cunha construída. O fechamento do grafo de Tomita do par concreto fornece S
fechado, densamente definido e involutivo; Γ(J) entrelaça W com W(-Jf).
Quatro recompilações da cunha e sete do par/fiação deram EXIT0; o checker do par
conferiu181declarações sem axiomas fora do trio. Cinco de sete oleans do par são
idênticos; assembly e antiunitário diferem em bytes, sem causa atribuída.
[REAL — compilação local; revisão pendente] O lift exponencial de Δ_W^1/2
foi construído fechado, denso, simétrico e positivo. Auto-adjunção e igualdade
com o fator polar do S do par permanecem abertas. A montagem fornece dez campos
originais, mas não reivindica habitante do certificado analítico restante.
[EM_CURSO] Integração numa nova cópia v394 e rito integral; o main anterior ainda
não tem PASS terminal neste retrato. A guarda Python foi revista17/17 e não é
isolamento do sistema operacional. Permanecem os requisitosR1–R10, inclusive
localização global, core/traço na mesma representação e matéria/H3 conjuntos.
Evidência: `{OUT/'PROGRESS_R4.json'}`, SHA256`{pin(OUT/'PROGRESS_R4.json')['sha256']}`.
Nenhum original científico, provedor, Bancada de produção ou gate alterado.
"""
    new(OUT/'MEMORY_ADDITION_R4.txt', text)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
                ROOT/'memory/TGL_INDICE_VIVO.md', ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    memories = [append_bytes(p, text, MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R4.json', dict(unit=progress['unit'], claim=claim,
        surfaces=memories, evidence=pin(OUT/'PROGRESS_R4.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R4.json', dict(tipo='ANOTACAO',
        rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='Vácuo padrão e Tomita fechado construídos na mesma cunha Fock',
        resultado=progress['constructed'], estatuto='REAL — componentes; EM_CURSO — conjunto',
        status='EM_CURSO', veredito='PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',
        defeito='Polaridade/KMS, core/traço, realização global/conjunta e rito integral pendentes.',
        proximo_passo='Identificar fatores polares, integrar módulos construídos e concluir rito da nova cópia.',
        onde=str(OUT), artefatos=[str(OUT/'PROGRESS_R4.json'), str(OUT/'MEMORY_PROGRESS_R4.json')], olhou_dados=False))
    new(OUT/'ACOM_PROGRESS_REQUEST_R4.json', dict(operation='transition',
        reference=str(WORK/'ACOM_REFERENCE.json'), expected_revision=32, event_id=MARKER,
        actor=dict(id=WHO, kind='agent'), changes=dict(records=[dict(id=MARKER,
        kind='fact', statute='REAL', text=progress['constructed']+' '+progress['assembly']+' '+progress['unbounded'],
        sources=[dict(kind='artifact', ref=str(OUT/'PROGRESS_R4.json'), sha256=pin(OUT/'PROGRESS_R4.json')['sha256'])])],
        flow=dict(phase='standard_wedge_pair_tomita_constructed_modular_identification_in_progress',
                  next_action='Integrate verified network components into new v394 copy; identify polar factors, actual core trace and joint realization. Full R1-R10 remains active.'))))
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R4.json'), memories=len(memories)), ensure_ascii=False))


if __name__ == '__main__':
    main()
