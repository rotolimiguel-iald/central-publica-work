"""Record only completed constructions and the measured whole R7 preaudit."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MARKER = 'fecho_whole_preaudit_compact_maxwell_orientation_20261015_r11'
reg.DEST = OUT

def main():
    assert not (OUT/'PROGRESS_R11.json').exists()
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
        ROOT/'memory/TGL_INDICE_VIVO.md', ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    paths = [
        'network_bundle_r7/whole_preaudit_r1/TGLExt_BUILD_RECEIPT.json',
        'network_bundle_r7/whole_preaudit_r2/MEASURED_COVERAGE_R1.json',
        'coverage_candidate_r7/RECEIPT.json',
        'network_bundle_r8/COMPILED_R1.json', 'INTEGRATION_NETWORK_R8.json',
        'network_review/NETWORK_INTEGRATOR_R8_REVIEW_R1.json',
        'network_review/NETWORK_INTEGRATOR_R8B_DELTA_R1.json',
        'maxwell_smearing/FINAL_MAXWELL_ON_SHELL_RECEIPT_R1.json',
        'network_review/MAXWELL_ON_SHELL_SEMANTIC_REVIEW_ROOT_R1.json',
        'maxwell_smearing/FINAL_MAXWELL_SMEARING_RECEIPT_R1.json',
        'network_review/MAXWELL_SMEARING_SEMANTIC_REVIEW_ROOT_R1.json',
        'orbital_rotation/FINAL_SCREEN_ORIENTATION_ROOT_RECEIPT_R1.json',
        'network_review/SCREEN_ORIENTATION_SEMANTIC_REVIEW_SKEPTIC_R1.json']
    evidence = [pin(OUT/p) for p in paths]
    whole = json.loads((OUT/paths[1]).read_bytes())
    compiled = json.loads((OUT/paths[3]).read_bytes())
    integration = json.loads((OUT/paths[4]).read_bytes())
    assert whole['passed'] is True and whole['outside_trio'] == whole['unread_names'] == 0
    assert compiled['passed'] is True and integration['compiled_bundle'] == pin(OUT/paths[3])
    assert integration['whole_certificate_inhabited'] is False
    claims = {
        'whole_R7': f"A pre-auditoria integral da candidata R7 compilou TGLExt e TGL/Audit com EXIT0, {whole['total_declarations']} declaracoes, {whole['total_theorems']} teoremas e nenhuma dependencia fora do trio. A tentativa inicial recusou dois objetos historicos ausentes da copia; a nova tentativa reutilizou seus bytes verificados. Isso nao e uma execucao do main.",
        'bundle_R8': f"O pacote R8 compilou/auditou {len(compiled['modules'])} modulos e {compiled['all_local_declarations']} declaracoes locais, incluindo Segal essencialmente auto-adjunto, Lorentz escalar futuro e fluxo modular GNS. A candidata R8 foi integrada por fontes e pinos; seu main e sua pre-auditoria integral ainda nao estao reivindicados por este recibo.",
        'Maxwell': 'O bivector p wedge epsilon satisfaz Bianchi, divergencia nula e transporte transversal. Seu smearing tensorial compacto fora do eixo da carta pertence ao H1 original, e e complexo-linear e nao nulo. O campo de Segal correspondente atua na mesma Fock, tem fecho auto-adjunto e excitacao do vacuo nao nula. Sao testes compactos de momento: restricao Fourier de testes de espaco-tempo, localidade, Wick stress e charge_link continuam separados. A linearidade complexa do smear nao se transfere ao campo auto-adjunto de Segal.',
        'orientation': 'ScreenOrientationMeasured foi derivado do determinante unitario do mapa linear real4D, da preservacao da metrica e do transporte efetivo do momento, nos pontos regulares da carta. A base nula tem determinante1 e sua decomposicao reduz o determinante4D ao da tela. Seis declaracoes compiladas no trio e revisao independente da fonte, sem afirmar rebuild independente.'}
    progress = dict(unit='F1.FECHO_20261015', claim_event=845,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_R1_R10_PRESERVED', evidence=evidence,
        requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'), **claims,
        remaining=['Identificacao modular integral GNS, traco escalado e PF',
            'Localizacao global e realizacao fisica nomeada',
            'Testes de espaco-tempo, tensor de materia e charge_link',
            'Rito completo da candidata final e revisao conjunta'],
        production_modified=False, gate_moved=False, new_provider_calls=0)
    new(OUT/'PROGRESS_R11.json', progress)
    text = '\n\n## 15/10/2026 — Reuso da rede: pre-auditoria integral e ligacoes concretas\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, F1.FECHO_20261015, reivindicacao845 vigente conferida.\n'
    for label, body in claims.items():
        text += f'\n[REAL — sandbox; {label}] {body}\n'
    text += f'\n[OPEN] Objetivo integral R1–R10 preservado. Evidencia: `{OUT/"PROGRESS_R11.json"}`, SHA256 `{pin(OUT/"PROGRESS_R11.json")["sha256"]}`. Nenhum original de producao, provedor, dado observado ou gate foi alterado.\n'
    new(OUT/'MEMORY_ADDITION_R11.txt', text)
    memories = [append_bytes(p, text, MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R11.json', dict(unit=progress['unit'], claim=claim,
        surfaces=memories, evidence=pin(OUT/'PROGRESS_R11.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R11.json', dict(tipo='ANOTACAO',
        rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='Pre-auditoria integral R7; pacote R8, smearing Maxwell e orientacao da tela',
        resultado=' '.join(claims.values()), estatuto='REAL — componentes; EM_CURSO — conjunto',
        status='EM_CURSO', veredito='PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',
        defeito='Contrato conjunto ainda nao habitado.', proximo_passo='Completar ligacoes e executar candidata final.',
        onde=str(OUT), artefatos=[str(OUT/'PROGRESS_R11.json'),str(OUT/'MEMORY_PROGRESS_R11.json')], olhou_dados=False))
    new(OUT/'ACOM_PROGRESS_REQUEST_R11.json', dict(operation='transition',
        reference=str(WORK/'ACOM_REFERENCE.json'), expected_revision=39, event_id=MARKER,
        actor=dict(id=WHO, kind='agent'), changes=dict(records=[dict(id=MARKER,
            kind='fact', statute='REAL', text=' '.join(claims.values()),
            sources=[dict(kind='artifact', ref=str(OUT/'PROGRESS_R11.json'),
                sha256=pin(OUT/'PROGRESS_R11.json')['sha256'])])],
            flow=dict(phase='whole_R7_preaudit_R8_integration_compact_Maxwell_orientation',
                next_action='Complete global localization, full modular identification, spacetime Maxwell/stress and actual final main. Preserve R1-R10.'))))
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R11.json'), memories=len(memories)), ensure_ascii=False))

if __name__ == '__main__':
    main()
