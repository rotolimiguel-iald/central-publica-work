"""Record root-verified helpers and physical geometry; no independent audit claimed."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MARKER = 'fecho_right_root_opposite_wedge_20261016_r32'
reg.DEST = OUT

def main():
    assert not (OUT/'PROGRESS_R32.json').exists()
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
        ROOT/'memory/TGL_INDICE_VIVO.md', ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    paths = ['network_review/RIGHT_ROOT_OPPOSITE_WEDGE_REVIEW_R1.json',
        'PROVENIENCIA_V393_REUSO_V351_R1.json']
    evidence = [pin(OUT/p) for p in paths]
    review=json.loads((OUT/paths[0]).read_bytes())
    assert review['verdict']=='PASS_WITH_STATED_SCOPE'
    claims = {'actual_right_root': 'A ação regular direita comuta com a resolvente de Tomita construída e com sua raiz positiva no mesmo GNS de Fock, preservando o domínio completo da raiz; seis declarações no trio.', 'cuts_and_continuity': 'A identidade polar direita equivale às identidades de cortes consumindo a recuperação por cortes já provada. J segue explícito nesse auxiliar. A representação GNS e a órbita dual são contínuas em norma; a álgebra de von Neumann é fechada em norma.', 'physical_wedge_duality': 'J leva os subespaços reais físicos das cunhas opostas um ao outro. O subespaço físico da cunha esquerda é igual ao complemento simplético de KWR; nenhum axioma de localidade foi fornecido para essa prova.', 'generic_components': 'A anulação local de uma forma bilinear real estende-se por partições a dois suportes compactos. Foram provados também transporte de grafos polares, fechamento de equações/CFC e bilinearidade simplética. As hipóteses desses auxiliares permanecem explícitas.', 'review_scope': 'Oito módulos,21 impressões de axiomas só no trio,859 pinos conferidos. Fontes nomeadas lidas integralmente pela raiz; inclui autoria própria. Sem auditoria independente ou recompilação independente deste lote.', 'current_basis': 'Programa e selo v393 novamente conferidos por SHA256. V351 designa módulos incorporados à v393; novas construções candidatas v394 em sandbox.', 'pending': 'Decomposição polar, identificação da ação direita pelo polar, traço escalado/PF, localidade global e vínculo da carga ainda em curso. Tentativas falhas WeightPolarR8, OppositeWedgeR3 e ClosureOrderR5 não foram aceitas. ClosureOrderR5 encerrada após erros; CutsR1 encerrada por substituição pela R3 aprovada; logs e recibos preservados.'}
    progress = dict(unit='F1.FECHO_20261015', claim_event=881,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_R1_R10_PRESERVED', evidence=evidence,
        requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'), **claims,
        remaining=['Decomposicao polar, traco escalado e PF na mesma realizacao',
            'Localizacao global e realizacao fisica nomeada',
            'Testes de espaco-tempo, tensor de materia e charge_link',
            'Rito completo da candidata final e revisao conjunta'],
        production_modified=False, gate_moved=False, new_provider_calls=0)
    new(OUT/'PROGRESS_R32.json', progress)
    text = '\n\n## 16/10/2026 — Raiz modular, ação direita e dualidade física de cunhas\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, F1.FECHO_20261015, reivindicacao881 vigente conferida.\n'
    for label, body in claims.items():
        text += f'\n[REAL — sandbox; {label}] {body}\n'
    text += f'\n[OPEN] Objetivo integral R1–R10 preservado. Evidencia: `{OUT/"PROGRESS_R32.json"}`, SHA256 `{pin(OUT/"PROGRESS_R32.json")["sha256"]}`. Nenhum original de producao, provedor, dado observado ou gate foi alterado.\n'
    new(OUT/'MEMORY_ADDITION_R32.txt', text)
    memories = [append_bytes(p, text, MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R32.json', dict(unit=progress['unit'], claim=claim,
        surfaces=memories, evidence=pin(OUT/'PROGRESS_R32.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R32.json', dict(tipo='ANOTACAO',
        rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='Raiz modular, ação direita e dualidade física de cunhas',
        resultado=' '.join(claims.values()), estatuto='REAL — componentes; EM_CURSO — conjunto',
        status='EM_CURSO', veredito='PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',
        defeito='Contrato conjunto ainda nao habitado.', proximo_passo='Completar ligacoes e executar candidata final.',
        onde=str(OUT), artefatos=[str(OUT/'PROGRESS_R32.json'),str(OUT/'MEMORY_PROGRESS_R32.json')], olhou_dados=False))
    new(OUT/'ACOM_PROGRESS_REQUEST_R32.json', dict(operation='transition',
        reference=str(WORK/'ACOM_REFERENCE.json'), expected_revision=60, event_id=MARKER,
        actor=dict(id=WHO, kind='agent'), changes=dict(records=[dict(id=MARKER,
            kind='fact', statute='REAL', text=' '.join(claims.values()),
            sources=[dict(kind='artifact', ref=str(OUT/'PROGRESS_R32.json'),
                sha256=pin(OUT/'PROGRESS_R32.json')['sha256'])])],
            flow=dict(phase='right_root_and_opposite_physical_wedge_verified',
                next_action='Complete global localization, full modular identification, spacetime Maxwell/stress and actual final main. Preserve R1-R10.'))))
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R32.json'), memories=len(memories)), ensure_ascii=False))

if __name__ == '__main__':
    main()
