"""Record root-verified helpers and physical geometry; no independent audit claimed."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
MARKER = 'fecho_root_domain_localization_20261016_r30'
reg.DEST = OUT

def main():
    assert not (OUT/'PROGRESS_R30.json').exists()
    claim = reg.call([CLI, 'ver', 'F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    surfaces = [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md',
        ROOT/'memory/TGL_INDICE_VIVO.md', ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    assert all(p.name in claim['nota'] for p in surfaces)
    paths = ['network_review/ROOT_DOMAIN_LOCALIZATION_REVIEW_R1.json',
        'PROVENIENCIA_V393_REUSO_V351_R1.json']
    evidence = [pin(OUT/p) for p in paths]
    review=json.loads((OUT/paths[0]).read_bytes())
    assert review['verdict']=='PASS_WITH_STATED_SCOPE'
    claims = {'root_domain': 'O auxiliar genérico transporta o grafo e o domínio completo da raiz positiva quando o operador comuta com a resolvente. A equivalência dos domínios exige o inverso à esquerda comutante nomeado.', 'spacelike_neighborhoods': 'Cada par separado espacialmente admite vizinhanças abertas de raios positivos em cunhas opostas do mesmo referencial transladado. Não se afirmou a existência de uma dupla comum para conjuntos arbitrários.', 'compact_partition': 'Testes de Schwartz de suporte compacto se decompõem subordinados a uma cobertura aberta finita; as partes têm suporte compacto, conservam o suporte original e são múltiplos reais ponto a ponto.', 'physical_partition': 'A aplicação concreta preserva a condição de realidade dos testes de Maxwell. Isso fornece uma peça da prova de localidade; localidade global ainda não foi concluída.', 'review_scope': 'Quatro módulos, nove impressões de axiomas no trio e 152 pinos conferidos. Fontes nomeadas lidas integralmente pela raiz e construídas/revisadas por ela. Sem auditoria independente nem recompilação independente deste lote.', 'current_basis': 'Programa e selo v393 novamente conferidos por SHA256. V351 designa módulos históricos incorporados à v393. Novas construções permanecem candidatas v394 em sandbox.', 'pending_modular': 'As aplicações concretas ModularIdentificationR16 e RightRootR6 deram exit1 e não foram aceitas. R16 passou as três primeiras impressões, mas falhou na conversão das definições das potências imaginárias. Revisões R17 e R7 preparadas e em compilação; nenhum enunciado foi enfraquecido.'}
    progress = dict(unit='F1.FECHO_20261015', claim_event=881,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_R1_R10_PRESERVED', evidence=evidence,
        requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'), **claims,
        remaining=['Identificacao modular integral GNS, traco escalado e PF',
            'Localizacao global e realizacao fisica nomeada',
            'Testes de espaco-tempo, tensor de materia e charge_link',
            'Rito completo da candidata final e revisao conjunta'],
        production_modified=False, gate_moved=False, new_provider_calls=0)
    new(OUT/'PROGRESS_R30.json', progress)
    text = '\n\n## 16/10/2026 — Domínio da raiz, vizinhanças de cunhas e partição real de testes\n'
    text += f'<!-- {MARKER} -->\nEm nome de {WHO}, F1.FECHO_20261015, reivindicacao881 vigente conferida.\n'
    for label, body in claims.items():
        text += f'\n[REAL — sandbox; {label}] {body}\n'
    text += f'\n[OPEN] Objetivo integral R1–R10 preservado. Evidencia: `{OUT/"PROGRESS_R30.json"}`, SHA256 `{pin(OUT/"PROGRESS_R30.json")["sha256"]}`. Nenhum original de producao, provedor, dado observado ou gate foi alterado.\n'
    new(OUT/'MEMORY_ADDITION_R30.txt', text)
    memories = [append_bytes(p, text, MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R30.json', dict(unit=progress['unit'], claim=claim,
        surfaces=memories, evidence=pin(OUT/'PROGRESS_R30.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R30.json', dict(tipo='ANOTACAO',
        rota_id='formal.f1_rede.concrete_bosonic_kinematics', dominio='FORMAL',
        titulo='Domínio da raiz, vizinhanças de cunhas e partição real de testes',
        resultado=' '.join(claims.values()), estatuto='REAL — componentes; EM_CURSO — conjunto',
        status='EM_CURSO', veredito='PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',
        defeito='Contrato conjunto ainda nao habitado.', proximo_passo='Completar ligacoes e executar candidata final.',
        onde=str(OUT), artefatos=[str(OUT/'PROGRESS_R30.json'),str(OUT/'MEMORY_PROGRESS_R30.json')], olhou_dados=False))
    new(OUT/'ACOM_PROGRESS_REQUEST_R30.json', dict(operation='transition',
        reference=str(WORK/'ACOM_REFERENCE.json'), expected_revision=58, event_id=MARKER,
        actor=dict(id=WHO, kind='agent'), changes=dict(records=[dict(id=MARKER,
            kind='fact', statute='REAL', text=' '.join(claims.values()),
            sources=[dict(kind='artifact', ref=str(OUT/'PROGRESS_R30.json'),
                sha256=pin(OUT/'PROGRESS_R30.json')['sha256'])])],
            flow=dict(phase='root_domain_and_localization_partitions',
                next_action='Complete global localization, full modular identification, spacetime Maxwell/stress and actual final main. Preserve R1-R10.'))))
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R30.json'), memories=len(memories)), ensure_ascii=False))

if __name__ == '__main__':
    main()
