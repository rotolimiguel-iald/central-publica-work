"""Append independently reviewed same-Fock Tomita and dual-weight progress."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.FECHO_20261015'
reg.DEST=OUT
MARKER='fecho_tomita_equality_dual_weight_20261015_r6'

def main():
    assert not (OUT/'PROGRESS_R6.json').exists()
    claim=reg.call([CLI,'ver','F1.FECHO_20261015'])['reivindicacao']
    assert claim['quem']==WHO and dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    for name in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md','AVISO_GERENCIA.md'):
        assert name in claim['nota']
    paths=[
        'gamma_unbounded/FINAL_TOMITA_EQUALITY_RECEIPT_R1.json',
        'final_component_review/REVISAO_TOMITA_R1.json',
        'final_component_review/REVISAO_DUALIDADE_R1.json',
        'final_component_review/REVISAO_PESO_E_ADAPTADOR_R1.json',
        'star_graph_root_review_r1/REVISAO_STAR_GRAPH_ROOT_R1.json',
        'takesaki_fock/FOCK_DUAL_WEIGHT_RECEIPT_R1.json',
        'takesaki_fock/TRACED_CORE_ASSEMBLY_RECEIPT_R1.json',
        'network_integration_review/REVISAO_CANDIDATA_R4_KH_R1.json',
        'kh_patch_review/REVISAO_KH_PATCH_R3.json',
        'CANDIDATE_R4_KH_RECEIPT_R1.json',
    ]
    started=ROOT/'work/rite394_20261015/r3/RITE_STARTED.json'
    run=json.loads(started.read_bytes())
    assert pin(run['execution_copy_path'])['sha256']==run['execution_copy_sha256']
    progress=dict(unit='F1.FECHO_20261015',claim_event=845,
        created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),status='EM_CURSO_FULL_R1_R10_PRESERVED',
        evidence=[pin(OUT/p) for p in paths]+[pin(started)],requirements=pin(OUT/'REQUISITOS_ORIGINAIS_R1.json'),
        tomita='On the same canonical Fock, the closed Tomita graph of the concrete Weyl algebra and vacuum equals the exponential Tomita graph. Domains and actions agree. Independent recompilation and the real graph-closure proof were reviewed by separate hands.',
        one_particle='The concrete one-particle antiunitary maps KWR exactly onto its symplectic complement; proved using the genuine domain of the self-adjoint half-modular multiplier.',
        core='The actual dual weight on the same Fock regular core is additive, homogeneous, monotone and dual-invariant; its value at the unit is infinite. It is not the scaled trace. Nine core/embedding/action fields are supplied by terms, with 26 remaining fields explicit and no full inhabitant asserted.',
        review='Six final component recompilations exited 0; 186 declarations audited with only propext, Classical.choice and Quot.sound. Separate root review rebuilt the two-vector/star-graph bridge and audited all 61 declarations including private helpers.',
        runtime=dict(status='RUNNING_NOT_VERIFIED_COMPLETE',start_utc=run['start_utc'],pid=run['pid'],candidate=pin(run['execution_copy_path']),
            note='Entire main launched after final candidate review, with corrected KH/guard/PDF and historical assets. This snapshot does not certify final exit, outputs or a seal.'),
        scope_correction='The previous R5 open reverse-Tomita inclusion is now discharged by the reviewed equality. Positive self-adjoint polar identification, KMS and scaled trace are still open.',
        remaining=['Self-adjoint exponential lift and polar/modular identification',
            'Actual Fock Takesaki scaled trace and finite split projection',
            'Global localization/device realization and joint Maxwell source',
            'Explicit all-directions H3 scope',
            'Complete candidate runtime and final joint independent review'],production_modified=False,gate_moved=False,new_provider_calls=0)
    new(OUT/'PROGRESS_R6.json',progress)
    text=f'''\n\n## 15/10/2026 — Igualdade de Tomita na mesma Fock; peso dual e rito integral
<!-- {MARKER} -->
Em nome de {WHO}, unidade F1.FECHO_20261015, reivindicação845 conferida.
[REAL — sandbox e revisão independente] O Tomita do par efetivo (R(KWR),vácuo)
é o Tomita exponencial: grafos, domínios e ações coincidem. A inclusão reversa
que estava aberta no PROGRESS_R5 foi paga. A ponte de fechamento do grafo real
foi revista separadamente pela raiz, com61declarações incluindo auxiliares.
A revisão final recompilou6componentes e conferiu186declarações, só no trio.
Em uma partícula, J(KWR)=KWR′ foi provado a partir do domínio efetivo do adjunto.
[REAL — alcance] O peso dual foi construído no core regular da mesma Fock;
é invariante pela ação dual e vale infinito na unidade. Ainda não é o traço
com escala exp(-s). O adaptador substitui9campos por construções concretas e
deixa26campos explícitos; nenhum habitante conjunto foi afirmado.
[REAL — execução iniciada] A candidata final revista foi lançada em cópia às
{run['start_utc']}, main inteiro, PID{run['pid']}, com guard/KH/PDF corrigidos.
Este registro é um retrato de execução iniciada, sem PASS integral nem selo.
[OPEN] Autoadjunção/polar/KMS, traço escalado, rede global e matéria conjuntas,
alcance de H3 e revisão final. EscopoR1–R10 preservado. Nenhum gate ou produção mudou.
Evidência: `{OUT/'PROGRESS_R6.json'}`, SHA256`{pin(OUT/'PROGRESS_R6.json')['sha256']}`.
'''
    new(OUT/'MEMORY_ADDITION_R6.txt',text)
    surfaces=[ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',ROOT/'memory/TGL_ATLAS.md',ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    memories=[append_bytes(p,text,MARKER) for p in surfaces]
    new(OUT/'MEMORY_PROGRESS_R6.json',dict(unit=progress['unit'],claim=claim,surfaces=memories,evidence=pin(OUT/'PROGRESS_R6.json')))
    new(OUT/'MAP_ENTRY_PROGRESS_R6.json',dict(tipo='ANOTACAO',rota_id='formal.f1_rede.concrete_bosonic_kinematics',dominio='FORMAL',
        titulo='Igualdade Tomita na Fock concreta e peso dual; rito integral iniciado',
        resultado=progress['tomita']+' '+progress['core'],estatuto='REAL — componentes; EM_CURSO — conjunto',status='EM_CURSO',
        veredito='PARTIAL_VERIFIED_PROGRESS_FULL_SCOPE_PRESERVED',defeito='Polar/KMS, traco escalado, rede/materia conjuntos e encerramento do rito ainda pendentes.',
        proximo_passo='Pagar autoadjuncao do lift exponencial e ligacao modular/trace; conferir main integral.',onde=str(OUT),
        artefatos=[str(OUT/'PROGRESS_R6.json'),str(OUT/'MEMORY_PROGRESS_R6.json')],olhou_dados=False))
    new(OUT/'ACOM_PROGRESS_REQUEST_R6.json',dict(operation='transition',reference=str(WORK/'ACOM_REFERENCE.json'),expected_revision=34,event_id=MARKER,
        actor=dict(id=WHO,kind='agent'),changes=dict(records=[dict(id=MARKER,kind='fact',statute='REAL',
            text=progress['tomita']+' '+progress['one_particle']+' '+progress['core']+' Whole main has started but is not yet certified complete.',
            sources=[dict(kind='artifact',ref=str(OUT/'PROGRESS_R6.json'),sha256=pin(OUT/'PROGRESS_R6.json')['sha256'])])],
            flow=dict(phase='same_fock_tomita_equality_reviewed_full_main_running',next_action='Finish exponential-lift self-adjointness, polar/KMS and actual Fock trace; continue joint net/matter construction and verify whole main. R1-R10 remains active.'))))
    print(json.dumps(dict(progress=pin(OUT/'PROGRESS_R6.json'),memories=len(memories)),ensure_ascii=False))

if __name__=='__main__': main()
