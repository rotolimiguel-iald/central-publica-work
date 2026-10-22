"""Record an additive Takesaki stage without editing scientific originals."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import sqlite3

ROOT = Path(r'C:\IALD\Central de Patentes')
WORK = ROOT / 'work/takesaki_qg_20261013'
OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TAKESAKI'
V = ROOT / 'work/cadeia_de_selo/v392'
K = V / 'kb_stub_v392/TGLExt'
QUEUE = ROOT / 'Chatgpt/IALD_ORQUESTRACAO_20260923'
STAMP = dt.datetime.now(dt.timezone.utc).isoformat()

def pin(path):
    path = Path(path)
    data = path.read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}

def new_file(name, data):
    path = OUT / name
    if path.exists():
        raise FileExistsError(path)
    raw = (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode() if not isinstance(data, str) else data.encode()
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())
    assert tmp.stat().st_size == len(raw)
    os.rename(tmp, path)  # Windows refuses an existing destination.
    return pin(path)

c = sqlite3.connect((QUEUE / 'state/tasks.sqlite3').as_uri() + '?mode=ro', uri=True)
c.row_factory = sqlite3.Row
row = dict(c.execute('select * from coordination_jobs where id=?', ('ff9a08c5-5b3a-4b17-b0ea-319d59a978a2',)).fetchone())
c.close()
queue_state = {k: row.get(k) for k in ['id', 'request_id', 'stage', 'version', 'execution_task_id', 'execution_constraints', 'updated_at']}
queue_pin = new_file('QUEUE_STATUS_ETAPA_R1.json', {'observed_at': STAMP, 'read_only_snapshot': queue_state})

local = json.loads((OUT / 'local_lemmas/RESULTADO_LOCAL_R1.json').read_text(encoding='utf-8'))
verified = []
for entry in local['all_local_artifacts'] + [local['report'], local['build_receipt']]:
    actual = pin(entry['path'])
    if actual['sha256'] != entry['sha256'] or actual['bytes'] != entry['bytes']:
        raise ValueError({'pin_changed': entry, 'actual': actual})
    verified.append(actual)
verification_pin = new_file('VERIFICACAO_PINS_LOCAL_R1.json', {'observed_at': STAMP, 'all_match': True, 'entries': verified})

review_pin = new_file('REVISAO_LOCAL_INDEPENDENTE_R1.json', {
    'reviewer': '/root/v392_scope', 'medium': 'collaboration agent report in current thread',
    'scope': 'Read-only mathematical and source review; no independent recompilation.',
    'source_pins': [pin(OUT / 'DERIVACAO_LOCAL_R1.md'), pin(OUT / 'local_lemmas/TakesakiAlgebraicCore.lean'), pin(OUT / 'sources/Hiai_2020_2004.02383v1.pdf')],
    'report_verbatim': 'Sem defeito material encontrado. Sinais e regularizador coincidem com Hiai Thm10.15 pp99–100: θ_s(h)=e⁻ˢh, θ_s(B)=eˢB e θ_−s(Bε)=e⁻ˢ B_{e⁻ˢε}. A filiação de h ao centralizador de φ está na prova citada (segue σφ_t(λ(u))=λ(u)); ela sustenta a definição do peso perturbado. Os cinco teoremas são elementares condicionais, sem promessa de construção de core.',
    'report_kind': 'Faithful compact transcription of reviewer messages, not c1 approval.',
    'centralizer_clarification': 'Additive clarification to DERIVACAO_LOCAL_R1.md: h is affiliated with the centralizer of the dual weight; this supports the perturbation construction.',
    'accepted_locally': True, 'management_audit': 'PENDING'
})

nos = Path(r'C:\IALD\NOS_VIVO')
backups = sorted(nos.glob('nos_vivo.sqlite3.bak_20261013*'), key=lambda p: p.stat().st_mtime)
process_pin = new_file('RECIBO_PROCESSO_INDICE_R1.json', {
    'observed_at': STAMP,
    'incident': 'construir.py --help invoked to inspect usage, but the script ignores arguments and executed main(), regenerating the derived index.',
    'reason_for_lookup': 'The newly claimed F1.TAKESAKI was absent from the previous graph and blocked the mandatory scientific preview.',
    'local_observed_result': {'exit_code': 0, 'nodes': 10466, 'edges': 16208, 'seconds_reported': 10.4},
    'coordination_report': 'The coordination thread reported a second --help-triggered rebuild before reading this thread warning. Order between the two backup timestamps is not attributed without additional evidence.',
    'backup_files_observed': [pin(p) for p in backups[-2:]],
    'builder_pin': pin(nos / 'construir.py'),
    'backup_limit': 'The builder copies database bytes before replace. Its resumo() replaces NOS_VIVO.md without a prior backup; no backup of that pre-rebuild summary is claimed.',
    'affected_objects': ['derived nos_vivo.sqlite3', 'derived NOS_VIVO.md'],
    'source_mutation_by_builder': False,
    'followup': 'Use reviewed explicit CLI operations; reject unknown flags before mutations. No third rebuild was requested.'
})

source_paths = [V / 'um_v392_candidato.py', V / 'kernel/POS_BUILD_v392.json']
source_paths += [K / name for name in ['QGSolutionComplete.lean', 'TheImportedSecondQuantization.lean', 'LightNetStandardWedgeDataBGL.lean', 'V351DualScalingBridge.lean', 'AgapeNonVacuity.lean', 'LiganteLeiCampoCurvo.lean']]
source_paths += [ROOT / 'work/memoria_acom_fix_12out/9_R2_2/recibos_producao_r2_2/RECIBO_IMPLANTACAO_20261013_120100_439153.json']
sources = [pin(p) for p in source_paths]
source_pin = new_file('FONTES_DIAGNOSTICO_V392_MEMORIA_R1.json', sources)

report = '''# F1.TAKESAKI — diagnóstico v392 e primeira etapa

Autor: codex-gerente-tgl. Unidade criada no evento 732 e reivindicada no 733.
Base: v392 candidata autorizada pelo operador para raciocinar; ratificação e versão instalada são estados distintos. Fontes e hashes em FONTES_DIAGNOSTICO_V392_MEMORIA_R1.json.

## O que já existe e o que falta

[REAL — fontes/build custodiados] A cadeia QG é um teorema condicional, com LightNetData, FockCertificate e MaxwellCertificate. A implicação Clausius em todas as telas nulas + conservação → Einstein no atlas suave conexo, com Λ único, já existe. Isso não constrói a métrica nem deriva H3 do estado.

| Frente | Disponível | Obrigação construtiva restante |
|---|---|---|
| Core/traço | Escala V351 por termo, subcone finito não vazio e aplicação de Ágape | Identificação fiel com o produto cruzado pretendido, entrelaçando ações e pesos; construção geral de Takesaki |
| Rede da luz | Contratos BGL/Fock, operadores e resultados modulares reutilizáveis | Ponte Fubini L² vetorial → Fourier parcial → J e Δ → habitante concreto com as propriedades exigidas |
| Matéria/gravitação | Implicação geométrica condicional, H3 nomeado, conservação no registro | Ligação do T ao MaxwellCertificate/StressTensorData e realização física de H3 em todas as direções; não prometer deduzir H3 do estado sem hipótese adicional |
| Realização conjunta | Existem testemunhas contratuais e resultados parciais | Construir e identificar o objeto canônico que realize simultaneamente os contratos; não confundir com dizer que todo FullTGLWitness é vazio |

P_ker K ↔ P_F não deve ser reaberto como igualdade literal de operadores: a luz fornece uma metade por termo, e a passagem ao core usa a ponte conhecida Haagerup/Terp, em tipos próprios. O que falta é a realização/identificação pertinente, não uma igualdade mal tipada.

## Resultado imediato de Takesaki

[DERIVED sobre KNOWN] DERIVACAO_LOCAL_R1.md apresenta o caminho M,ω → M⋊σ^ωℝ → peso dual φ → densidade h → τ=φ_(h⁻¹), com τ∘θ_s=e⁻ˢτ. Explicita onde ω∘σ^ω=ω é consumida e faz a passagem por regularizadores limitados. Hiai, teorema10.15, foi conferido; Takesaki1973 foi custodiado como fonte original.

[REAL — compilação local] Cinco teoremas Lean4.31: EXIT0, somente propext/Classical.choice/Quot.sound, zero sorry. Incluem obstrução unital finita, reponderação condicional, contraexemplo à invariância isolada, testemunha algébrica não nula e sua lei de escala. O modelo ℝ² é somente algébrico. Não se anuncia o teorema geral de Takesaki compilado. A revisão independente foi de leitura, sem recompilação; aprovação da gerência continua pendente.

## Orquestração

O contrato foi completado para o pedido existente, sem nova identidade: request9fec8d26-d3b7-4262-b4e6-e3a5aa450760, jobff9a08c5-5b3a-4b17-b0ea-319d59a978a2. A prévia seleciona Kimi. O pacote canônico recuperado permanece identificado por sua geração histórica; as fontes v392 são suplemento explícito.

A API instalada não sabia ligar o suplemento à inscrição imutável. A coordenação relatou protótipo com18controles e recebeu ordem de concluir a integração mínima, com revisão, CAS e outbox. O estado lido nesta etapa está em QUEUE_STATUS_ETAPA_R1.json. Entregar o contrato à coordenação não significa que o provedor recebeu ou respondeu. A unidade permanece EM_CURSO.

## Memória e stack

[REAL — conferência somente leitura] ACOMv2 já está implantada:15/15arquivos conferidos contra o recibo; a auditoria registra278/278controles em cópia. Deltas, CAS, diário durável e replay já existem. Não é trabalho a repetir. A janela pós-implantação com heartbeat/llama online ainda não estava demonstrada no recibo de verificação anterior à implantação.

[DERIVED — prioridades propostas]
1. Resolvedor de versão por tarefa: programa, kernel, memória científica, pacote enviado, suplemento e auditoria devem ter identidades separadas e verificáveis. Não misturar v391 recuperada com v392 autorizada sem rótulo.
2. Memória científica por afirmação: fonte/hash/linhas, hipóteses, enunciado, prova/build, revisão e estatuto. Uma frase candidata de modelo não vira REAL por persistir no banco.
3. Projeção de contexto que elimine repetições da apresentação e preserve todas as ocorrências, correções e originais. A leitura integral de bytes do Atlas encontrou8.763.084bytes; o índice exato por linha ocupa menos texto, mas não demonstra por si só compressão semântica sem perda ou ganho cognitivo.
4. Avaliar recuperação após troca de sessão/compactação com casos da casa: recordação das restrições, versão correta, erros de promoção de estatuto, custo e latência. Ganho só após medição.
5. Fixar retenção/arquivamento e medir custo com crescimento do banco; o replay e a verificação ainda têm componentes lineares. A matemática de idempotência da memória não prova automaticamente correção do software SQLite/CLI.
6. Completar o protocolo aditivo de suplementos; a falha encontrada hoje é um caso concreto de melhoria operacional da memória comum e da fila.

Cobertura: o Atlas inteiro foi lido por script para hash/índice; a leitura semântica do modelo foi por seções relevantes. Não se declara que8,76MBcabem integralmente no contexto de uma chamada. As quatro famílias do Atlas permanecem preservadas, com as fontes primárias como autoridade.

## Processo e limites

RECIBO_PROCESSO_INDICE_R1.json registra que construir.py --help regenerou o índice em vez de mostrar ajuda, inclusive a limitação de backup do resumo. Nenhum original científico, um.py, kernel, Bancada de produção ou gate foi editado nesta etapa. Não houve abertura de dados observados. Validade matemática não é creditação física.
'''
report_pin = new_file('RELATORIO_ETAPA_R1.md', report)
result = {
    'unit': 'F1.TAKESAKI', 'at': STAMP, 'status': 'EM_CURSO',
    'working_basis': 'v392 explicitly authorized, ratification distinct',
    'local_build': {'exit_code': local['build']['exit_code'], 'theorems': len(local['axiom_reports']), 'seconds': local['build']['seconds'], 'axioms_only_trio': True, 'sorry_count': local['forbidden_proof_tokens']},
    'general_takesaki_lean_construction': 'OPEN', 'queue': queue_state,
    'pins': [pin(OUT / 'CONTRATO_TAKESAKI_R1.json'), pin(OUT / 'DERIVACAO_LOCAL_R1.md'), pin(OUT / 'local_lemmas/RESULTADO_LOCAL_R1.json'), pin(OUT / 'PREVIEW_KIMI_R2.json'), pin(OUT / 'sources/CUSTODY_R1.json'), pin(WORK / 'ATLAS_FULL_SCAN_R1.json'), queue_pin, verification_pin, review_pin, process_pin, source_pin, report_pin],
    'next_action': 'Integrate additive contract binding and dispatch same request once; then verify returned candidate against sources and local Lean obligations.',
    'no_nature_claim': True, 'gate_changed': False
}
result_pin = new_file('RESULTADO_ETAPA_R1.json', result)
entry = {
    'tipo': 'ROTA', 'rota_id': 'formal.f1_takesaki.modular_identity_to_scaling', 'dominio': 'KERNEL_FORMAL',
    'titulo': 'Takesaki: contrato dedicado, derivação por peso dual e cinco lemas locais',
    'pergunta': 'Quais hipóteses levam da dinâmica modular à escala do traço canônico e quais pontes da v392 restam construir?',
    'dados': ['v392 autorizada pelo operador', 'Hiai2004.02383 Thm10.15', 'fontes Lean V351/Fundacao existentes'],
    'metodo': 'Consulta Nós vivo, custódia por hash, derivação com regularizadores, Lean4.31 em sandbox e revisão independente de leitura.',
    'resultado': 'Cinco teoremas, EXIT0, trio, zero sorry; generalização analítica e identificação de produto cruzado permanecem abertas. Contrato suplementar pronto; integração da fila em curso.',
    'veredito': 'LOCAL_ALGEBRA_PASS_GENERAL_CONSTRUCTION_OPEN', 'estatuto': 'DERIVED', 'status': 'EM_CURSO', 'olhou_dados': False,
    'defeito': 'API anterior não liga suplemento preservando âncora imutável; corrigir coordenadamente. Não confundir modelo algébrico com core de von Neumann.',
    'nao_refazer': 'Escala e não vacuidade V351/F1.2 já provadas. ACOMv2 já corrigida e implantada.',
    'proximo_passo': result['next_action'], 'onde': str(OUT),
    'artefatos': [result_pin['path'], report_pin['path'], str(OUT / 'DERIVACAO_LOCAL_R1.md'), str(OUT / 'local_lemmas/RESULTADO_LOCAL_R1.json')],
    'refs': ['formal.f1_2.v351_dual_scaling_bridge'],
    'nota': 'Nenhuma aprovação gerencial ou creditação física inferida; incidente de índice descrito no recibo.'
}
new_file('MAP_ENTRY_ETAPA_R1.json', entry)
print(json.dumps({'result': result_pin, 'local_verified_files': len(verified), 'queue_stage': queue_state['stage']}, ensure_ascii=False))
