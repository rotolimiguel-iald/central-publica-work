from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_074_20260910'
created = []


def link(label, path):
    path = Path(path).resolve()
    assert path.is_relative_to(ROOT) and path.is_file(), str(path)
    return f'[{label}](<{path.as_posix()}>)'


def new(path, content):
    path = path.resolve()
    assert path.is_relative_to(ROOT) and path.parent.is_dir() and not path.exists()
    for target in re.findall(r'\]\(<(C:/[^>]+)>\)', content):
        assert Path(target).is_file(), target
    raw = content.encode('utf-8')
    temporary = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temporary.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert raw and temporary.read_bytes() == raw
    temporary.rename(path)
    assert path.read_bytes() == raw
    created.append({'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})


documentary_paths = list(ROOT.glob('REVISAO_DOCUMENTAL_RELATORIO_074_*/PARECER_RELATORIO_074.md'))
assert len(documentary_paths) == 1, [str(p) for p in documentary_paths]
doc_path = documentary_paths[0]
report = link('relatório074', OUT / 'REEXAME_SUFICIENCIA.md')
normal = link('translação normal', ROOT / 'HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/TRANSLACAO_NORMAL_E_CURVATURA_BRST.md')
frame = link('adendo de frame local', ROOT / 'HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/PRECISAO_FRAME_LOCAL_074.md')
normal_review = link('parecer da translação e frame', ROOT / 'REVISOES_RAIZ_074_20260910/PARECER_TRANSLACAO_NORMAL_E_FRAME_074.md')
rees = link('completação por laços e valência', ROOT / 'COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md')
rees_review = link('parecer da completação', ROOT / 'REVISAO_COMPLETACAO_REES_074_20260910_015708_288616/PARECER_COMPLETACAO_REES_074.md')
natural = link('normalização e Euler', ROOT / 'NATURALIDADE_E_CURVATURA_B0_074_20260910/NORMALIZACAO_S_E_OBSTRUCAO_EULER.md')
natural_frame = link('adendo métrico e frame de referência', ROOT / 'NATURALIDADE_E_CURVATURA_B0_074_20260910/PRECISAO_METRICA_E_FRAME_DE_REFERENCIA.md')
natural_review = link('parecer da normalização e Euler', ROOT / 'REVISOES_RAIZ_074_20260910/PARECER_NORMALIZACAO_E_EULER_074.md')
documentary = link('revisão documental do relatório', doc_path)

adendum = f'''# Adendo de revisões — entrega074

10/09/2026. [DERIVED — escopos das demonstrações escritas] [REAL — leitura dos pareceres e integridade]. Complemento ao {report}, sem alterar seus bytes.

## Revisões e correções que acompanham a entrega

O {normal_review} confere a {normal} junto com o {frame}. A raiz identificou o termo −dA A⁻¹ na transformação do ghost Lorentz convencional e solicitou a correção de alcance, registrada pelo autor em arquivo separado. A conclusão aceita é a naturalidade na apresentação MÉTRICA mínima, que é a apresentação efetiva de Q2. A receita b_Nλ=0 não foi aprovada como operador natural sob frames locais arbitrários.

O {rees_review}, por leitor distinto do autor, confere a {rees}. Explicita o lift cotangente sigma e Ψ_t*ω_BV=t²ω_can, evitando duplicar t⁻² no antibracket normalizado. Também registra que R_L é um espaço homogêneo e que uma saída até t^N pode exigir entrada até t^(N+4). O rótulo inicial de revisão pendente no manifesto da fonte é histórico; o parecer posterior não o altera.

O {natural_review} confere a {natural}, consumida com o {natural_frame}. A projeção de tipos tensoriais finitos de Lorentz é usada na referência normal de um ponto e na apresentação métrica. Ela não faz do ghost Lorentz convencional uma variável tensorial sob mudanças locais de gauge de frame.

A {documentary} examina o relatório e sua correspondência com as fontes. É uma revisão documental e de escopo; não constitui uma nova prova Lean nem uma auditoria analítica integral de toda a literatura importada. O trabalho posterior075 não integra os resultados074.

## Estatuto utilizável

1. [DERIVED] b_N natural métrico, C_N(∇̄c)=−R̄ e conjugação exata s+E_N+C_N, com E_N²=−{{s,C_N}}. Não apagar o termo de curvatura, inclusive no FRW.
2. [DERIVED] A translação conserva a completação R_L por laços/valência, no domínio declarado. Laços positivos não ganham expoentes negativos por essa operação. Isso não atesta todos os demais homotópicos.
3. [DERIVED — condicional] Uma primitiva ordinária de s já existente na mesma classe formal pode ser naturalizada. Não se presume que uma série formal arbitrária possua tal primitiva a partir do teorema suave073.
4. [DERIVED] Euler(g0) é um contraexemplo à promoção genérica de exatidão coordenada para exatidão natural modulo d_H na classe universal regular. Ele está em ghost zero, forma quatro; não é uma anomalia física calculada nem um contraexemplo ao teorema ordinário073 de anomalias.
5. [DERIVED] A diferença Euler(g)−Euler(g0) tem uma transgressão natural formal. O termo diagonal Euler(g0) não foi removido.
6. [OPEN] Permanecem as primitivas de s na classe correta, os dois grupos horizontais com coeficientes, a descida natural e o consumo admissível na hierarquia causal. O critério espectral da fonte enuncia antecedentes suficientes; não os declara satisfeitos.

## Obrigações gerais preservadas

O fechamento da anomalia precisa de localidade, regularidade, escala por aridade, realidade, independência funcional, inserções marcadas e contatos. Depois precisam ser construídas a corrente/carga e as identidades quânticas. Acordo perturbativo, fundos/estados compatíveis, reconstrução geral pelos mesmos dados TGL e justificação UV permanecem no objetivo.

P0 e o critério condicional da comutante073 são preservados. Fase, ramo, H3 interno e falsificadores existentes não são reabertos. Integração canônica e formalização continuam tarefas distintas da evidência escrita.

Somente arquivos novos em Chatgpt. Nenhum original, Atlas, índice, memória canônica ou gate foi alterado. Zero CAS/Lean, diagramas ou testes de natureza novos. Os controles do manifesto final são documentais; o objetivo geral permanece ativo.
'''
new(OUT / 'ADENDO_REVISOES_074.md', adendum)
adendum_link = link('adendo de revisões074', OUT / 'ADENDO_REVISOES_074.md')
tunnel = f'''# Entrega espontânea074 — translação natural, curvatura e completação

10/09/2026. Para a sessão que codifica um.py. [DERIVED — matemática escrita, não Lean] [REAL — documentação medida]. Entrada: {report}, acompanhado obrigatoriamente pelo {adendum_link}.

## Peças para integração

- {normal} + {frame}: operador de translação natural na apresentação MÉTRICA mínima; C_N(∇̄c)=−R̄; conjugação s+E_N+C_N. E_N²=−{{s,C_N}}, portanto não renomear E_N como o diferencial externo ordinário073. A extensão b_Nλ=0 a frames locais convencionais foi retirada.
- {rees} + {rees_review}: organização R_L=∏E t^(E+2L−2)P_E, preservada pela translação; coeficiente de saída usa até E+4. Para truncagem até N, guardar entrada até N+4 quando necessário. Usar antibracket canônico normalizado e lift cotangente sigma; não duplicar a escala t⁻².
- {natural} + {natural_frame}: transporte condicionado de primitivas de s que já existam na mesma completação; contraexemplo Euler em ghost0/forma4; transgressão natural de Euler(g)−Euler(g0). Nenhuma anomalia física não nula foi calculada.

Pareceres matemáticos da raiz: {normal_review} e {natural_review}. A revisão documental do relatório está vinculada no adendo.

## Tipagem das pendências

Ainda não declarar H¹,⁴ natural nulo. O critério da nota requer primitivas de s na classe formal correta, dois grupos horizontais com coeficientes e a descida natural. Depois é necessário satisfazer a família causal de contratermos, inserções e contatos. O trabalho075 em elaboração não é consumido por este pacote.

P0_073 permanece realizado no modelo/fundo/domínio declarado. A carga interagente, QME, acordo perturbativo, estados compatíveis, reconstrução geral e UV continuam com as obrigações anteriores. Preservar fase/ramo/H3 interno e os falsificadores existentes.

A captura074 encontrou o mesmo canônico da entrega073; ausências e pins estão em ESTADO_CANONICO_074.json. Nenhum um.py foi executado/importado ou editado. Nenhum Atlas, índice, memória canônica, selo ou gate mudou. O manifesto final reúne hashes e controles documentais, sem convertê-los em teoremas formais.
'''
new(ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_074_ESPONTANEA_translacao_natural_curvatura_e_completacao.md', tunnel)

config = {
    'source_directories': [
        'HOMOTOPIA_NORMAL_COVARIANTE_074_20260910',
        'COMPLETACAO_REES_BRST_074_20260910',
        'REVISAO_COMPLETACAO_REES_074_20260910_015708_288616',
        'NATURALIDADE_E_CURVATURA_B0_074_20260910',
        'REVISOES_RAIZ_074_20260910',
        doc_path.parent.name
    ],
    'new_cas_controls': 0,
    'new_lean_compilations': 0,
    'status': 'WRITTEN_METRIC_NATURAL_TRANSLATION_AND_REES_COMPLETION__CURVATURE_OBSTRUCTION_AND_S_PRIMITIVE_TRANSFER__NATURAL_ANOMALY_COHOMOLOGY_OPEN',
    'written_results': [
        'Natural metric ghost-jet translation, explicit curvature defect and exact conjugation s+E_N+C_N.',
        'Correction withdrawing equivariance of b_N lambda=0 under arbitrary local conventional Lorentz frames.',
        'Rees loop/valence completion preserved by the finite translation, with bounded truncation loss and normalized BV scaling.',
        'Conditional naturalization of s primitives in the same formal tensor-polynomial completion.',
        'Euler spectator counterexample in ghost zero/form four, natural relative Euler transgression and conditional degree-five spectral criterion.'
    ],
    'remaining': [
        'Natural s primitives in the actual formal completion, horizontal E2 groups with dynamic cohomology coefficients, and natural descent.',
        'Admissible all-order anomaly renormalization with regularity/scaling, field independence, insertions and contact identities.',
        'Renormalized current/charge implementation, quantum differential nilpotence and QME.',
        'Perturbative agreement and compatible backgrounds, states and cutoffs.',
        'General gravitational correspondence from the same selected TGL data and justified UV route.',
        'Canonical integration and formalization of written constructions and previously absent modules.'
    ],
    'limits': 'Written internally reviewed mathematics in the declared metric/formal categories. Euler counterexample has ghost zero, not a calculated quantum anomaly. Rees theorem covers the translation, not every cohomological homotopy or causal counterterm map. No CAS/Lean/diagrams/nature tests; originals and canonical memories read-only; no gate change or claim that the full objective is achieved.'
}
new(OUT / 'CONFIG_ENTREGA_074.json', json.dumps(config, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'created_utc': datetime.now(timezone.utc).isoformat(), 'created': created}, ensure_ascii=True))
