"""Custody the compiled integrated snapshot and correct the previous runtime status."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
reg.DEST=OUT
MARKER='fecho_full_closure_and_graph_core_20261015_r5'


def main():
    assert not (OUT/'PROGRESS_R5.json').exists()
    claim=reg.call([CLI,'ver','F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem']==WHO and dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    for name in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md','AVISO_GERENCIA.md'):
        assert name in claim['nota']
    paths=[
        'network_bundle_r4/COMPILED_R3.json',
        'network_bundle_r4/full_audit_r3/MEASURED_COVERAGE_R1.json',
        'network_bundle_r4/READONLY_CACHE_VERIFIED_R1.json',
        'network_bundle_r4/PLAN_R3.json',
        'INTEGRATION_NETWORK_R4.json',
        'graph_core_review/REVISAO_GRAPH_CORE_R1.json',
        'gamma_unbounded/FINAL_TOMITA_INCLUSION_RECEIPT_R1.json',
        'gamma_review/REVISAO_GAMMA_R1.json',
        'takesaki_review/REVISAO_TAKESAKI_FOCK_R1.json',
        'takesaki_reuse/FOCK_TRACE_REUSE_AND_OBSTACLE_R1.json',
        'full_rite/FULL_RITE_OUTPUT_REVIEW_R1.json',
        'kh_patch_review/REVISAO_KH_PATCH_R1.json',
    ]
    full=json.loads((OUT/paths[1]).read_bytes())
    compiled=json.loads((OUT/paths[0]).read_bytes())
    integrated=json.loads((OUT/'INTEGRATION_NETWORK_R4.json').read_bytes())
    assert full['passed'] and full['outside_trio']==0 and compiled['passed']
    assert pin(integrated['candidate']['path'])==integrated['candidate']
    progress=dict(unit='F1.FECHO_20261015',claim_event=845,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
        status='EM_CURSO_FULL_R1_R10_PRESERVED',evidence=[pin(OUT/p) for p in paths],
        requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'),
        integrated_candidate=integrated['candidate'],
        bundle=dict(modules=len(compiled['modules']),declarations=compiled['explicit_axioms'],
                    note='49 mathematical modules and one audit; declaration count includes definitions/helpers.'),
        whole_closure=dict(declarations=full['total_declarations'],theorems=full['total_theorems'],
                           outside_trio=full['outside_trio'],broad_parser_entries=full['axiom_report_count']),
        derived_components='The same Fock has Weyl/CCR, a standard wedge vacuum, closed pair Tomita, positive exponential lift and regular covariant core with faithful embedding and dual action.',
        graph_core='Independent recompilation confirms a genuine graph core in F x F, approximating input and image together. Local construction now proves Sexp is contained in S_pair. The reverse inclusion and polar/KMS identification remain open.',
        prior_rite_correction='The R2 full main finished with exit 0 after 5754.35 seconds. Formal checks and selftest passed; 13208 Python guard refusals prevent calling the whole run PASS. The earlier R4 progress entry was a running snapshot. New candidate has not yet run.',
        integration='Candidate R4 contains 1287 embedded sources and expects 8107 ladder flags. The KH-N1 patch R1 was independently rejected for accepting altered counts with unchanged pinned logs; correction and independent review are required before the next main.',
        remaining=['Complete equality and polar identification on the actual Fock pair',
                   'Actual Fock modular weight and scaled trace',
                   'Global localization/device realization and joint Maxwell source',
                   'Keep all-directions H3 scope explicit',
                   'Corrected candidate full runtime and independent joint review'],
        production_modified=False,new_provider_calls=0,gate_moved=False)
    new(OUT/'PROGRESS_R5.json',progress)
    text=f'''\n\n## 15/10/2026 — Fecho de imports da cópia v394 e core de grafo Fock
<!-- {MARKER} -->
Em nome de {WHO}, unidade F1.FECHO_20261015, reivindicação845 conferida.
[REAL — sandbox] Reunidos49módulos e um auditor, com936declarações verificadas
no pacote; a contagem inclui definições e auxiliares. O audit do fecho inteiro
deu EXIT0: {full['total_declarations']}declarações, {full['total_theorems']}teoremas,
zero axiomas fora do trio. As fontes e o programa canônicos permaneceram iguais.
A candidataR4 incorpora1287fontes e espera8107bandeiras; ainda não executou main.
[REAL — revisão independente] O core exponencial aproxima simultaneamente vetor
e imagem. A inclusão Sexp⊆S_par está compilada localmente; a igualdade, a
identificação polar e KMS permanecem abertas. O core regular e a ação dual foram
construídos na mesma Fock; ainda falta identificar o peso/traço modular.
[ERRATA AO LADO, em nome do signatário] O retratoR4 dizia que o mainR2 seguia
rodando. Ele terminou depois: EXIT0,5754,35s; formalização e selftest passaram,
mas13208recusas da guarda impedem chamar a rodada inteira de PASS. Os recibos
originais permanecem. A guarda corrigida e o PDFoffline foram revistos; o
verificadorKH-N1R1 foi recusado por admitir contagens adulteradas com logs
pinados e será corrigido antes do próximo main.
[EM_CURSO] EscopoR1–R10 preservado, incluindo rede global, realização conjunta
de matéria e revisão final. Nenhum gate, provedor ou Bancada de produção alterado.
Evidência: `{OUT/'PROGRESS_R5.json'}`, SHA256`{pin(OUT/'PROGRESS_R5.json')['sha256']}`.
'''
    new(OUT/'MEMORY_ADDITION_R5.txt',text)
    surfaces=[ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',ROOT/'memory/TGL_ATLAS.md',
              ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    memories=[append_bytes(p,text,MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R5.json',dict(unit=progress['unit'],claim=claim,surfaces=memories,evidence=pin(OUT/'PROGRESS_R5.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R5.json',dict(tipo='ANOTACAO',rota_id='formal.f1_rede.concrete_bosonic_kinematics',
        dominio='FORMAL',titulo='Fecho integrado v394 e core genuino de grafo da mesma Fock',
        resultado=progress['derived_components']+' '+progress['graph_core'],estatuto='REAL — componentes; EM_CURSO — conjunto',
        status='EM_CURSO',veredito='PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',
        defeito='Identificacao polar, traco, rede global/materia conjuntos e novo main pendentes.',
        proximo_passo='Concluir igualdade Tomita e corrigir KH-N1 para o rito integral da candidata.',
        onde=str(OUT),artefatos=[str(OUT/'PROGRESS_R5.json'),str(OUT/'MEMORY_PROGRESS_R5.json')],olhou_dados=False))
    new(OUT/'ACOM_PROGRESS_REQUEST_R5.json',dict(operation='transition',reference=str(WORK/'ACOM_REFERENCE.json'),
        expected_revision=33,event_id=MARKER,actor=dict(id=WHO,kind='agent'),
        changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',
            text=progress['derived_components']+' '+progress['graph_core']+' '+progress['prior_rite_correction'],
            sources=[dict(kind='artifact',ref=str(OUT/'PROGRESS_R5.json'),sha256=pin(OUT/'PROGRESS_R5.json')['sha256'])])],
            flow=dict(phase='full_candidate_closure_compiled_tomita_equality_in_progress',
                      next_action='Correct KH-N1 from pinned audit logs, run integrated candidate, finish same-Fock polar/trace and joint realization. Full R1-R10 remains active.'))))
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R5.json'),memories=len(memories)),ensure_ascii=False))


if __name__=='__main__':
    main()
