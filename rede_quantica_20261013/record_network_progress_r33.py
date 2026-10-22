"""Record root-verified helpers and physical geometry; no independent audit claimed."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MARKER = 'fecho_actual_polar_decomposition_20261016_r33'
reg.DEST = OUT

def main():
    assert not (OUT/'PROGRESS_R33.json').exists()
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
        ROOT/'memory/TGL_INDICE_VIVO.md', ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    paths = ['network_review/ACTUAL_POLAR_DECOMPOSITION_REVIEW_R1.json',
        'PROVENIENCIA_V393_REUSO_V351_R1.json']
    evidence = [pin(OUT/p) for p in paths]
    review=json.loads((OUT/paths[0]).read_bytes())
    assert review['verdict']=='PASS_WITH_STATED_SCOPE'
    claims = {'actual_polar': 'No mesmo GNS do peso dual de Fock, a raiz positiva da resolvente de S†S construída independentemente tem exatamente o domínio do Tomita fechado; S = J raiz por termo. Nenhuma identidade polar, igualdade de grupos modulares ou tracialidade foi fornecida como hipótese.', 'root_properties': 'A mesma raiz é auto-adjunta e injetiva e tem imagem densa. São nove declarações concretas no trio.', 'closed_real_spans': 'A ortogonalidade simplética dos geradores estende-se aos seus fechos lineares reais. A ortogonalidade dos geradores físicos para regiões gerais ainda precisa ser fornecida pela construção de localidade.', 'review_scope': 'Dois módulos,10 impressões de axiomas só no trio,619 pinos conferidos. Fontes nomeadas lidas integralmente e revistas pela raiz; não é auditoria independente nem recompilação independente.', 'current_basis': 'Programa e selo v393 novamente conferidos por SHA256; módulos históricos V351 são reutilizados de dentro dessa versão. Candidatas v394 permanecem em sandbox.', 'pending': 'A troca da resolvente por J, a identificação polar da ação direita e o transporte da dualidade para outros referenciais estão em compilação. O traço escalado/PF, a rede global, o vínculo Maxwell da carga e a execução integral com revisão independente permanecem em curso. A decomposição polar deixa de ser pendência desta etapa.'}
    progress = dict(unit='F1.FECHO_20261015', claim_event=881,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_R1_R10_PRESERVED', evidence=evidence,
        requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'), **claims,
        remaining=['Identificacao polar da acao direita, traco escalado e PF na mesma realizacao',
            'Localizacao global e realizacao fisica nomeada',
            'Testes de espaco-tempo, tensor de materia e charge_link',
            'Rito completo da candidata final e revisao conjunta'],
        production_modified=False, gate_moved=False, new_provider_calls=0)
    new(OUT/'PROGRESS_R33.json', progress)
    text = '\n\n## 16/10/2026 — Decomposição polar no GNS físico e extensão aos fechos reais\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, F1.FECHO_20261015, reivindicacao881 vigente conferida.\n'
    for label, body in claims.items():
        text += f'\n[REAL — sandbox; {label}] {body}\n'
    text += f'\n[OPEN] Objetivo integral R1–R10 preservado. Evidencia: `{OUT/"PROGRESS_R33.json"}`, SHA256 `{pin(OUT/"PROGRESS_R33.json")["sha256"]}`. Nenhum original de producao, provedor, dado observado ou gate foi alterado.\n'
    new(OUT/'MEMORY_ADDITION_R33.txt', text)
    memories = [append_bytes(p, text, MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R33.json', dict(unit=progress['unit'], claim=claim,
        surfaces=memories, evidence=pin(OUT/'PROGRESS_R33.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R33.json', dict(tipo='ANOTACAO',
        rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='Decomposição polar no GNS físico e extensão aos fechos reais',
        resultado=' '.join(claims.values()), estatuto='REAL — componentes; EM_CURSO — conjunto',
        status='EM_CURSO', veredito='PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',
        defeito='Contrato conjunto ainda nao habitado.', proximo_passo='Completar ligacoes e executar candidata final.',
        onde=str(OUT), artefatos=[str(OUT/'PROGRESS_R33.json'),str(OUT/'MEMORY_PROGRESS_R33.json')], olhou_dados=False))
    new(OUT/'ACOM_PROGRESS_REQUEST_R33.json', dict(operation='transition',
        reference=str(WORK/'ACOM_REFERENCE.json'), expected_revision=61, event_id=MARKER,
        actor=dict(id=WHO, kind='agent'), changes=dict(records=[dict(id=MARKER,
            kind='fact', statute='REAL', text=' '.join(claims.values()),
            sources=[dict(kind='artifact', ref=str(OUT/'PROGRESS_R33.json'),
                sha256=pin(OUT/'PROGRESS_R33.json')['sha256'])])],
            flow=dict(phase='actual_fock_dual_weight_polar_decomposition_verified',
                next_action='Complete global localization, full modular identification, spacetime Maxwell/stress and actual final main. Preserve R1-R10.'))))
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R33.json'), memories=len(memories)), ensure_ascii=False))

if __name__ == '__main__':
    main()
