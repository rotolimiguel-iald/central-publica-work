"""Record only completed constructions and the measured whole R7 preaudit."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MARKER = 'fecho_whole_R8_screen_global_Maxwell_full_weight_20261015_r12'
reg.DEST = OUT

def main():
    assert not (OUT/'PROGRESS_R12.json').exists()
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
        ROOT/'memory/TGL_INDICE_VIVO.md', ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    paths = [
        'network_bundle_r8/whole_preaudit_r1/MEASURED_COVERAGE_R1.json',
        'coverage_candidate_r8/RECEIPT.json',
        'orbital_rotation/FINAL_SCREEN_LORENTZ_RECEIPT_R1.json',
        'network_review/SCREEN_LORENTZ_SEMANTIC_REVIEW_ROOT_R1.json',
        'orbital_rotation/FINAL_SCREEN_REFLECTION_RECEIPT_R1.json',
        'network_review/SCREEN_REFLECTION_SEMANTIC_REVIEW_ROOT_R1.json',
        'takesaki_fock/FOCK_FULL_WEIGHT_TOMITA_RECEIPT_R1.json',
        'network_review/FULL_WEIGHT_TOMITA_SEMANTIC_REVIEW_ROOT_R1.json',
        'maxwell_global/FINAL_GLOBAL_MAXWELL_SCHWARTZ_RECEIPT_R1.json',
        'network_review/GLOBAL_MAXWELL_SCHWARTZ_SEMANTIC_REVIEW_ROOT_R1.json']
    evidence = [pin(OUT/p) for p in paths]
    whole = json.loads((OUT/paths[0]).read_bytes())
    assert whole['passed'] is True and whole['outside_trio'] == whole['unread_names'] == 0
    claims = {
        'whole_R8': f"A pre-auditoria integral da candidata R8 compilou TGLExt e TGL/Audit com EXIT0 e {whole['total_declarations']} declaracoes, todas no trio. O refresco de metadados foi gerado como candidato novo. Nao e execucao do main, nem inclui os novos blocos abaixo.",
        'Lorentz': 'A representacao concreta de Lorentz com fases circulares de helicidade no H1 original compilou 188 declaracoes locais. A antiunitaria Theta e a rotacao de meia-volta deram Jcandidate=U(halfTurn)Theta e a conjugacao da acao de Lorentz, em 39 declaracoes locais adicionais. A identificacao Fourier/geometrica de J existente foi reaproveitada. Revisoes de fontes/pinos/recibos passaram no alcance declarado; nao alegam rebuild independente nem localizacao global das cunhas.',
        'full_weight': 'O grafo completo n_nu intersecao n_nu* tem fecho igual ao S ja construido no GNS do mesmo peso do mesmo core regular de Fock. A aproximacao sandwich simultanea paga A e A* em norma GNS. Seis fontes/26 prints no trio e revisao independente de fonte/247 pinos. A identificacao modular com o fluxo regular e o traco escalado continuam obrigacoes separadas.',
        'Maxwell': 'Doze modulos constroem mapa continuo complexo-linear de testes Schwartz de espaco-tempo para o H1 original, por Fourier/restricao a concha, com prova de integrabilidade global e limite por seminormas. Existe teste real nao nulo, e seu campo de Segal tem fecho auto-adjunto na mesma Fock. Sao 40 prints conferidos no trio: o 43 da mensagem do construtor foi erro de soma, corrigido ao lado. Revisao independente de fontes/264 pinos aprovada com alcance. A Fourier original e negativa com 2pi; um adaptador positivo angular e necessario para casar U1/localizacao e esta sendo construido separadamente. Localidade, wedge_glue, stress e charge_link nao seguem deste lote.'}
    progress = dict(unit='F1.FECHO_20261015', claim_event=845,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_R1_R10_PRESERVED', evidence=evidence,
        requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'), **claims,
        remaining=['Identificacao modular integral GNS, traco escalado e PF',
            'Localizacao global e realizacao fisica nomeada',
            'Testes de espaco-tempo, tensor de materia e charge_link',
            'Rito completo da candidata final e revisao conjunta'],
        production_modified=False, gate_moved=False, new_provider_calls=0)
    new(OUT/'PROGRESS_R12.json', progress)
    text = '\n\n## 15/10/2026 — Reuso da rede: Lorentz/J, Maxwell global e Tomita do peso completo\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, F1.FECHO_20261015, reivindicacao845 vigente conferida.\n'
    for label, body in claims.items():
        text += f'\n[REAL — sandbox; {label}] {body}\n'
    text += f'\n[OPEN] Objetivo integral R1–R10 preservado. Evidencia: `{OUT/"PROGRESS_R12.json"}`, SHA256 `{pin(OUT/"PROGRESS_R12.json")["sha256"]}`. Nenhum original de producao, provedor, dado observado ou gate foi alterado.\n'
    new(OUT/'MEMORY_ADDITION_R12.txt', text)
    memories = [append_bytes(p, text, MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R12.json', dict(unit=progress['unit'], claim=claim,
        surfaces=memories, evidence=pin(OUT/'PROGRESS_R12.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R12.json', dict(tipo='ANOTACAO',
        rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='Pre-auditoria R8; Lorentz/J, Maxwell Schwartz e dominio completo do peso',
        resultado=' '.join(claims.values()), estatuto='REAL — componentes; EM_CURSO — conjunto',
        status='EM_CURSO', veredito='PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',
        defeito='Contrato conjunto ainda nao habitado.', proximo_passo='Completar ligacoes e executar candidata final.',
        onde=str(OUT), artefatos=[str(OUT/'PROGRESS_R12.json'),str(OUT/'MEMORY_PROGRESS_R12.json')], olhou_dados=False))
    new(OUT/'ACOM_PROGRESS_REQUEST_R12.json', dict(operation='transition',
        reference=str(WORK/'ACOM_REFERENCE.json'), expected_revision=40, event_id=MARKER,
        actor=dict(id=WHO, kind='agent'), changes=dict(records=[dict(id=MARKER,
            kind='fact', statute='REAL', text=' '.join(claims.values()),
            sources=[dict(kind='artifact', ref=str(OUT/'PROGRESS_R12.json'),
                sha256=pin(OUT/'PROGRESS_R12.json')['sha256'])])],
            flow=dict(phase='whole_R8_preaudit_screen_reflection_global_Maxwell_full_weight',
                next_action='Complete global localization, full modular identification, spacetime Maxwell/stress and actual final main. Preserve R1-R10.'))))
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R12.json'), memories=len(memories)), ensure_ascii=False))

if __name__ == '__main__':
    main()
