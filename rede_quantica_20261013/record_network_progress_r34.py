"""Record root-verified helpers and physical geometry; no independent audit claimed."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MARKER = 'fecho_polar_flip_wedge_closure_20261016_r34'
reg.DEST = OUT

def main():
    assert not (OUT/'PROGRESS_R34.json').exists()
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
        ROOT/'memory/TGL_INDICE_VIVO.md', ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    paths = ['network_review/POLAR_FLIP_WEDGE_CLOSURE_REVIEW_R1.json',
        'PROVENIENCIA_V393_REUSO_V351_R1.json']
    evidence = [pin(OUT/p) for p in paths]
    review=json.loads((OUT/paths[0]).read_bytes())
    assert review['verdict']=='PASS_WITH_STATED_SCOPE'
    claims = {'polar_flip': 'No mesmo GNS do peso dual de Fock, o J construído conjuga a resolvente de Tomita R em 1-R, por termo. Nenhuma troca modular é fornecida como hipótese.', 'physical_frames': 'A ortogonalidade simplética das cunhas físicas opostas é transportada para cunhas transladadas em referenciais de Lorentz gerados, usando as representações e a covariância física já construídas.', 'right_closure': 'A álgebra da identidade polar direita, ainda com J explícito, é fechada em norma e estável pelo CFC ambiente. Identidades direitas provadas passam a limites fortes-estrela uniformemente limitados, com as aproximações nomeadas.', 'test_space_typing': 'A forma simplética bilinear foi provada para uma aplicação complexa linear sobre um módulo, sem impor norma ao espaço de testes. Isso corrige a exigência incompatível com a topologia de Schwartz; a aplicação concreta corrigida ainda compila.', 'review_scope': 'Cinco módulos,16 impressões no trio e1177 pinos conferidos. Revisão de fontes pela raiz, incluindo autoria própria; não é auditoria independente nem recompilação independente.', 'current_basis': 'SHA256 do programa e do selo v393 conferidos novamente. V351 é o nome histórico de módulos presentes nessa versão; candidatas v394 ficam em sandbox.', 'pending': 'Ação direita pelo polar, cortes/ordem, traço escalado/PF, localidade global, comparação das redes e vínculo Maxwell da carga continuam em curso. Tentativas ClosureOrderR9 e PhysicalSymplecticPairingR6 falharam e não foram aceitas. O fechamento de norma/CFC e a troca da resolvente deixam de ser pendências desta etapa.'}
    progress = dict(unit='F1.FECHO_20261015', claim_event=881,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_R1_R10_PRESERVED', evidence=evidence,
        requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'), **claims,
        remaining=['Identificacao polar da acao direita, traco escalado e PF na mesma realizacao',
            'Localizacao global e realizacao fisica nomeada',
            'Testes de espaco-tempo, tensor de materia e charge_link',
            'Rito completo da candidata final e revisao conjunta'],
        production_modified=False, gate_moved=False, new_provider_calls=0)
    new(OUT/'PROGRESS_R34.json', progress)
    text = '\n\n## 16/10/2026 — Troca modular, cunhas em referenciais e fechamento da álgebra direita\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, F1.FECHO_20261015, reivindicacao881 vigente conferida.\n'
    for label, body in claims.items():
        text += f'\n[REAL — sandbox; {label}] {body}\n'
    text += f'\n[OPEN] Objetivo integral R1–R10 preservado. Evidencia: `{OUT/"PROGRESS_R34.json"}`, SHA256 `{pin(OUT/"PROGRESS_R34.json")["sha256"]}`. Nenhum original de producao, provedor, dado observado ou gate foi alterado.\n'
    new(OUT/'MEMORY_ADDITION_R34.txt', text)
    memories = [append_bytes(p, text, MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R34.json', dict(unit=progress['unit'], claim=claim,
        surfaces=memories, evidence=pin(OUT/'PROGRESS_R34.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R34.json', dict(tipo='ANOTACAO',
        rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='Troca modular, cunhas em referenciais e fechamento da álgebra direita',
        resultado=' '.join(claims.values()), estatuto='REAL — componentes; EM_CURSO — conjunto',
        status='EM_CURSO', veredito='PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',
        defeito='Contrato conjunto ainda nao habitado.', proximo_passo='Completar ligacoes e executar candidata final.',
        onde=str(OUT), artefatos=[str(OUT/'PROGRESS_R34.json'),str(OUT/'MEMORY_PROGRESS_R34.json')], olhou_dados=False))
    new(OUT/'ACOM_PROGRESS_REQUEST_R34.json', dict(operation='transition',
        reference=str(WORK/'ACOM_REFERENCE.json'), expected_revision=62, event_id=MARKER,
        actor=dict(id=WHO, kind='agent'), changes=dict(records=[dict(id=MARKER,
            kind='fact', statute='REAL', text=' '.join(claims.values()),
            sources=[dict(kind='artifact', ref=str(OUT/'PROGRESS_R34.json'),
                sha256=pin(OUT/'PROGRESS_R34.json')['sha256'])])],
            flow=dict(phase='actual_polar_flip_frame_wedge_and_right_closure_verified',
                next_action='Complete global localization, full modular identification, spacetime Maxwell/stress and actual final main. Preserve R1-R10.'))))
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R34.json'), memories=len(memories)), ensure_ascii=False))

if __name__ == '__main__':
    main()
