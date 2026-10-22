from pathlib import Path
from datetime import datetime
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = Path(__file__).resolve().parent
assert OUT.is_relative_to(ROOT)


def write_new(path, content):
    path = path.resolve()
    assert path.is_relative_to(ROOT) and path.parent.is_dir()
    assert not path.exists(), 'Existing files are read-only: ' + str(path)
    raw = content.encode('utf-8')
    assert raw
    temp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.stat().st_size == len(raw) and temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


adendum = r'''# Adendo final: corolário de anomalia e alcance das revisões 071

10/09/2026. [DERIVED — demonstração escrita e revisão matemática interna] [KNOWN — comparação importada com hipóteses explícitas] [REAL — artefatos lidos]. Este adendo acompanha o relatório, a memória e o desenho locais sem alterar suas versões já escritas. Os originais e a memória canônica permanecem somente leitura.

## O corolário acrescentado

A [nota de grau cinco e anomalia local](<C:/IALD/Central de Patentes/Chatgpt/COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/COROLARIO_H5_E_ANOMALIA_LOCAL.md>) completa a composição que o relatório principal ainda descrevia como disponível para consumo. Com a cohomologia característica covariante de grau dois nula, obtém-se

\[
H^5(s,\mathcal B)=0,\qquad
H^5(s,\mathcal A_{\rm sm})=0,\qquad
H^{1,4}(s\mid d_H;\mathcal A_{\rm sm})=0.
\]

B é o complexo covariante dos campos completos da ação ambiente Einstein–sigma, com g e phi independentes, conexão de Levi-Civita e alvo S³. Na redução por KT e cohomologia de Lorentz, o único par possível de grau total cinco é grau dois em ghosts de translação e grau três em cohomologia de Lorentz. O coeficiente é precisamente uma classe característica covariante de grau dois; a demonstração principal o elimina.

A_sm permite coeficientes suaves conjuntos nos valores do vielbein em GL⁺(4,R) e nos valores do alvo, com dependência polinomial finita nos jatos diferenciados, ghosts e antifields. A retração polar e a contração de de Rham no grupo compacto SO(4) são usadas parametricamente nos coeficientes. Não se identifica C∞(e,y) a um produto tensorial algébrico de funções separadas. Os graus 0, 3 e 6 do fator dos vielbeins dão, no grau total cinco, H⁵(B), H²(B) e H⁻¹(B); todas essas parcelas são nulas. O grau seis permanece no cálculo, embora a dimensão do espaço-tempo seja quatro.

A última comparação é a de grau de forma máximo em [BBH1995, equação (6.15)](https://arxiv.org/pdf/hep-th/9505173v2), com gauge de difeomorfismos e em carta contrátil de espaço-tempo. O alvo é tratado globalmente; o espaço-tempo arbitrário não recebe, por isso, um teorema global. A classe de volume de S³ não foi apagada.

O resultado significa que um cociclo local de ghost um e forma quatro nessa álgebra admite a primitiva correspondente nessa mesma álgebra. O passo lógico exigido para a teoria causal continua sendo demonstrar que a quebra efetivamente produzida e sua primitiva podem ser relacionadas por operações admissíveis no espaço Q2.

## Limites que acompanham a equação

Não se transfere automaticamente a conclusão suave para um anel estritamente racional em todo o vielbein. Há um controle explícito: d(det e)/det e restringe-se a dt/t em diag(t,1,1,1), cuja primitiva é log t e não uma função racional. Isso não desfaz a primitiva natural covariante de grau dois, construída por outra via.

Também não se identifica automaticamente A_sm ao espaço Q2 com fundos externos fixos sob o BRST quântico. Permanecem as condições de covariância local, dependência dos fundos, suporte, analiticidade e escalamento exigidos pelo esquema, realidade, fontes e termos de contato. A normalização O(4) já construída fornece equivariância da família, mas não remove a dependência dos fundos. É essa comparação que deve preceder a remoção indutiva da quebra e a identidade quântica causal em todas as ordens.

Portanto a lista local de faltas deve retirar a classificação H¹,⁴ na classe completa suave especificada, além de M₂ ordinário e H²_char,cov. Deve conservar a admissibilidade Q2 e a QME. Setor físico interagente, positividade, condições finitas, questões globais, correspondência gravitacional geral e UV mantêm os alcances e pendências registrados no relatório.

## Revisões concluídas e precisão de graduação

O [parecer independente da covariantização](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_COVARIANTIZACAO_071_20260910_001522/PARECER_COVARIANTIZACAO_SUAVE.md>) examinou avaliação dos pares, coeficientes suaves, finitude, colagem de Čech e retorno à primitiva básica. Seu [adendo independente sobre H⁵ e anomalia](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_COVARIANTIZACAO_071_20260910_001522/ADENDO_REVISAO_H5_E_ANOMALIA_LOCAL.md>) examinou separadamente o corolário, inclusive a comparação de BBH e o fator GL⁺. Não identificou erro material nos passos examinados, no alcance declarado.

A [precisão do autor](<C:/IALD/Central de Patentes/Chatgpt/COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/PRECISAO_GRADUACAO_E_COMPOSICAO.md>) registra a observação de graduação: se alpha=s beta, gh(beta)=gh(alpha)−1; o teto inicial é antigh(beta)≤11−gh(alpha). Para alpha de grau dois, beta tem teto nove. A equação de exatidão e o argumento de finitude permanecem os mesmos. Esta precisão está ao lado das fontes congeladas.

As [revisões da raiz](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_071_20260910/PARECER_COVARIANTIZACAO.md>) e o [parecer da CME dimensional](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CME_DIMENSIONAL_071_20260910_001300_721043/PARECER_CME_DIMENSIONAL.md>) permanecem disponíveis. A [revisão documental do relatório principal](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_DOCUMENTAL_RELATORIO_071_20260910_001955_036954/PARECER_RELATORIO_071.md>) conferiu as afirmações e vínculos daquela versão. Ela não é apresentada como aprovação deste adendo ou dos documentos criados depois de seu parecer.

Estas são revisões internas feitas por agentes, com leitura das demonstrações e fontes indicadas; não constituem revisão externa independente, validação experimental ou certificação Lean. Nesta entrega há zero novas compilações Lean, zero controles CAS e zero cálculos de diagramas. A integridade dos arquivos é verificada separadamente pelo manifesto da entrega.

## Continuidade para a sessão codificadora

O [relatório principal](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_071_20260910/REEXAME_SUFICIENCIA.md>), este adendo, a [memória local](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_071_20260910/MEMORIA_DE_TRABALHO_071.md>) e o [desenho local](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_071_20260910/DESENHO_DO_FECHAMENTO_ADENDO_071.md>) devem ser lidos em conjunto. O desenho ganha agora o elo escrito H²_char,cov→H⁵(B)→H⁵(A_sm)→H¹,⁴(A_sm), antes da obrigação Q2. Nada é regravado por cima das memórias anteriores.

Os resultados escritos ainda precisam de formalização e integração no programa vivo, preservando suas hipóteses. Os 21 módulos anteriores são uma pendência de integração distinta das novas demonstrações. Não substituir o canônico pela cópia histórica que contém 98 módulos. Fase e ramo, seletor, H3 interno e falsificadores já presentes continuam reconhecidos. O objetivo geral permanece ativo.
'''

tunnel = r'''# Entrega espontânea 071 — primitivas suaves e covariância

10/09/2026. Da bancada Chatgpt para a sessão codificadora. [DERIVED — provas escritas com revisões internas] [REAL — leitura e integridade documental]. Todos os arquivos novos estão em Chatgpt; originais preservados.

O resíduo suave da entrega 070 foi tratado. A cadeia escrita e revisada é: M₂ relativo ordinário com coeficientes suaves → transporte e colagem em S³ → H²_char,cov=0 → H⁵(s,B)=0 → H⁵(s,A_sm)=0 → H¹,⁴(s|d_H;A_sm)=0. O último grupo usa a classe completa suave no vielbein e carta contrátil de espaço-tempo. A ação é Einstein–sigma ambiente, g e phi independentes, conexão de Levi-Civita.

A construção causal Q2 agora tem uma normalização O(4) equivariante da própria família de produtos e de sua quebra. Também foi escrita a ação BV dimensional que satisfaz a identidade clássica exatamente no regulador tensorial, com os contratos necessários para a rota dimensional.

**Próxima obrigação:** comparar a classe da anomalia e de sua primitiva com os contratermos admissíveis Q2, incluindo fundos, fontes e contatos; então remover a quebra em todas as ordens. A nulidade na álgebra suave de campos completos não declara essa transferência pronta. A rota dimensional também requer realização e comparação do esquema. Permanecem setor físico interagente, positividade, condições finitas, questões globais, correspondência gravitacional geral e UV.

Documentos para integração:

- [Relatório principal](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_071_20260910/REEXAME_SUFICIENCIA.md>).
- [Adendo final: corolário e revisões](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_071_20260910/ADENDO_REVISOES_071.md>).
- [Memória local](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_071_20260910/MEMORIA_DE_TRABALHO_071.md>) e [desenho do caminho](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_071_20260910/DESENHO_DO_FECHAMENTO_ADENDO_071.md>).
- [Resultado estruturado](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_071_20260910/RESULTADO_ENTREGA_071.json>) e [manifesto de integridade](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_071_20260910/MANIFESTO_ENTREGA_071.json>).

A captura canônica 071 encontrou v338, 683 arquivos embutidos e 77 dos 98 módulos comparados presentes; os 21 ausentes estão enumerados no resultado estruturado. Essa ausência é de integração no programa lido, não uma declaração de que os resultados da bancada não existem. Integrar por deltas sobre o programa vivo; não o substituir pela cópia histórica de 98 módulos.

Zero novas compilações Lean, zero CAS e zero diagramas nesta entrega. Nenhum um.py executado ou importado. Revisões matemáticas internas e verificações de bytes são evidências de naturezas diferentes. Nenhum gate, teste de natureza ou veredito de confirmação foi alterado. Fase e ramo, seletor, H3 interno e falsificadores existentes não são reabertos.
'''

config = {
    'source_directories': [
        'M2_SUAVE_RELATIVO_071_20260910_000347',
        'COVARIANTIZACAO_SUAVE_071_20260910_001058_826723',
        'NORMALIZACAO_O4_CAUSAL_071_20260910_000602_682931',
        'CME_DIMENSIONAL_EINSTEIN_SIGMA_071_20260910',
        'REVISOES_RAIZ_071_20260910',
        'REVISAO_CME_DIMENSIONAL_071_20260910_001300_721043',
        'REVISAO_COVARIANTIZACAO_071_20260910_001522',
        'REVISAO_DOCUMENTAL_RELATORIO_071_20260910_001955_036954',
    ],
    'new_cas_controls': 0,
    'new_lean_compilations': 0,
    'status': 'WRITTEN_SMOOTH_COVARIANT_COHOMOLOGY_AND_LOCAL_ANOMALY_CLASS_DERIVED__Q2_COMPARISON_QME_PHYSICAL_SECTOR_AND_UV_OPEN',
    'written_results': [
        '[DERIVED] Smooth ordinary relative M2 primitive, finite polynomial differentiated jets, including horizontal degrees zero and one.',
        '[DERIVED] Natural covariant H2_char=0 globally in the S3 target for ambient Einstein-sigma with independent metric and matter and Levi-Civita connection.',
        '[DERIVED, KNOWN] H5(s,B)=H5(s,A_sm)=H1,4(s|d_H;A_sm)=0 in the specified full smooth-vielbein algebra, locally in spacetime; not a Q2 admissibility theorem.',
        '[DERIVED, KNOWN] Exactly O4-equivariant causal normalization and extracted anomaly as a transported family of backgrounds.',
        '[DERIVED] Exact dimensionally continued classical BV master equation with sources and gauge fixing.',
        '[KNOWN, CONDITIONAL] Dimensional renormalization route and causal transfer contracts stated with regulator, infrared, truncation and admissibility obligations.'
    ],
    'remaining': [
        '[OPEN] Compare full-field smooth cohomology with the admissible Q2 counterterm complex including inert backgrounds, sources, contact terms and reality; construct an admissible primitive for the produced breaking.',
        '[OPEN] Inductive finite renormalization satisfying the causal quantum master identity in all orders, or realization and comparison of the dimensional scheme.',
        '[OPEN] Interacting physical sector and state, positivity, background independence and global or discrete issues within the stated scope.',
        '[OPEN] Finite renormalization conditions, physical running and UV completion or controlled alternative route.',
        '[OPEN] Physical correspondence and general scope of selection-to-gravity reconstruction; independent P measure and vertical BRST if claimed.',
        '[OPEN] Integrate the 21 previously delivered modules into the current canonical program and formalize/integrate the new written proofs with their hypotheses.'
    ],
    'limits': 'Written derivations with internal agent reviews and delimited primary imports; documentary integrity is not machine-checked mathematics or external peer review. No new CAS, Lean, diagrams or nature tests. Canonical originals and gate unchanged; the overall goal is not complete.'
}

destinations = [OUT / 'ADENDO_REVISOES_071.md',
                ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_071_ESPONTANEA_primitivas_suaves_e_covariancia.md',
                OUT / 'CONFIG_ENTREGA_071.json']
assert all(not path.exists() for path in destinations)
results = [write_new(destinations[0], adendum), write_new(destinations[1], tunnel),
           write_new(destinations[2], json.dumps(config, ensure_ascii=False, indent=2) + '\n')]
print(json.dumps({'status': 'NEW_DOCUMENTS_WRITTEN_VERIFIED', 'files': results}, ensure_ascii=True))
