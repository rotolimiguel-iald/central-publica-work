from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_073_20260910'
CREATED = []


def link(label, relative):
    path = (ROOT / relative).resolve()
    assert path.is_relative_to(ROOT) and path.is_file(), str(path)
    return f'[{label}](<{path.as_posix()}>)'


def create(relative, text):
    path = (ROOT / relative).resolve()
    assert path.is_relative_to(ROOT) and path.parent.is_dir() and not path.exists()
    raw = text.encode('utf-8')
    assert raw
    for target in re.findall(r'\]\(<(C:/[^>]+)>\)', text):
        assert Path(target).is_file(), target
    temp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    CREATED.append({'path': path.as_posix(), 'bytes': len(raw),
                    'sha256': hashlib.sha256(raw).hexdigest()})


report = link('relatório 073', 'REEXAME_SUFICIENCIA_073_20260910/REEXAME_SUFICIENCIA.md')
polarization = link('polarização adaptada', 'POLARIZACAO_BRST_HADAMARD_073_20260910/POLARIZACAO_ADAPTADA_E_MAJORANTE.md')
polar_review = link('parecer independente da polarização', 'REVISAO_POLARIZACAO_BRST_073_20260910/PARECER_POLARIZACAO_E_RADICAL.md')
fock = link('Fock, domínio Wick e P0', 'FOCK_HADAMARD_QUARTETOS_073_20260910/FOCK_DOMINIO_WICK_E_P0.md')
fock_review = link('parecer independente da composição', 'REVISAO_FOCK_DOMINIO_073_20260910/PARECER_FOCK_DOMINIO_E_P0.md')
radical_review = link('parecer do radical e reparo', 'REVISOES_RAIZ_073_20260910/PARECER_RADICAL_E_REPARO_073.md')
cohom = link('cohomologia ordinária com B0', 'COHOMOLOGIA_ESPECTADOR_B0_073_20260910/PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md')
cohom_review = link('parecer cohomológico', 'REVISOES_RAIZ_073_20260910/PARECER_COHOMOLOGIA_ESPECTADOR_073.md')
commutant = link('comutante escalar e carga condicional', 'COMUTANTE_FOCK_SUAVE_073_20260910/COMUTANTE_ESCALAR_E_CARGA_CONDICIONAL.md')
commutant_review = link('parecer da comutante', 'REVISOES_RAIZ_073_20260910/PARECER_COMUTANTE_SUAVE_073.md')
documentary = link('parecer documental do relatório', 'REVISAO_DOCUMENTAL_RELATORIO_073_20260910_013647_738543/PARECER_RELATORIO_073.md')
doc_receipt = json.loads((ROOT / 'REVISAO_DOCUMENTAL_RELATORIO_073_20260910_013647_738543/REGISTRO_REVISAO_RELATORIO_073.json').read_text(encoding='utf-8-sig'))

adendum = f'''# Adendo de revisões e corolário posterior — entrega 073

10/09/2026. [DERIVED — demonstrações escritas no escopo declarado] [REAL — leitura dos pareceres]. Complemento ao {report}; o relatório e seus documentos anteriores permanecem intactos.

## Revisões concluídas

- O {radical_review} confere a sequência exata, o contraexemplo auxiliar e o reparo. A falha de uma escolha arbitrária não foi atribuída a todo estado nem a um kernel canônico medido.
- O {polar_review} confere a {polarization}, incluindo pureza, realidade, controle microlocal, majorante e saturação. A revisão foi feita por leitor distinto do autor.
- O {fock_review} confere a composição {fock}: domínio nuclear suave, homotopia efetiva, positividade no kernel e estabilidade Wick na classe compacta polinomial microcausal. O manifesto inicial conservou seu rótulo histórico de revisão pendente; o parecer posterior registra a revisão concluída sem alterar aquele arquivo.
- O {cohom_review} confere a {cohom}, preservando a diferença entre exatidão coordenada ordinária e admissibilidade natural dos contratermos.
- O {documentary} confere a correspondência do relatório com suas fontes. Seu resultado é documental, não uma nova auditoria analítica completa da literatura. Ele não inclui o corolário posterior descrito abaixo.

P0 foi realizado na construção e no domínio declarados. A representação dos coeficientes compactos da teoria causal realiza uma parte de P1. A corrente, a carga renormalizada e as identidades de P2 ainda precisam ser construídas.

## Corolário posterior: termo escalar residual da carga

A nota {commutant}, examinada no {commutant_review}, acrescenta um resultado depois do congelamento do relatório.

Seja D o domínio de funções de onda de Cauchy suaves e de grau de partículas finito construído nesta entrega. Considere operadores contínuos em cada componente nuclear de D e com aumento finito do grau. O campo completo, com testes complexos numa faixa que contém toda a superfície de Cauchy, separa criadores e aniquiladores. Um operador que comuta com todos esses campos manda o vácuo em um múltiplo do vácuo. A comutação estende essa igualdade às palavras de criação; a densidade nuclear e a continuidade a estendem a D. Assim, a comutante nessa classe é escalar. O mesmo argumento se estende por indução aos coeficientes de uma deformação formal.

Consequentemente, se uma carga formal Q já construída nessa classe implementa um diferencial nilpotente, então Q² é central e escalar. Depois de especializar a zero as fontes externas de ghost não nulo, o anel escalar formal possui apenas ghost zero. Como Q² possui ghost dois, Q²=0. Isso remove um possível termo escalar residual **sob essas hipóteses**.

A supercomutante ímpar é nula pelo argumento do vácuo e da densidade. Se o adjunto de Krein da carga existe no domínio comum e o diferencial implementado respeita a involução graduada indicada na nota, segue também Q=Q×. Esse é um critério condicional de simetria, não uma construção do adjunto.

As hipóteses são materiais: o resultado usa o campo completo numa faixa de Cauchy, não a álgebra de uma pequena região; usa continuidade nuclear, não somente densidade Hilbert; e não exclui um escalar de ghost dois quando fontes externas com esse grau continuam no anel. O parecer esclarece também a vírgula tipográfica na fórmula 3.3 como produto de operadores e a notação de simetrização sobre N posições, sem alterar a fonte congelada.

## Caminho crítico atualizado

1. Produzir contratermos naturais e admissíveis para a quebra efetiva de Q2, com B0, regularidade, escala, completação formal, inserções e contatos; provar a remoção coerente das anomalias em todas as ordens.
2. Construir a corrente e uma carga que implementem o diferencial renormalizado no domínio comum. Se esse diferencial for nilpotente e as demais hipóteses acima forem satisfeitas, a comutante resolve o resíduo escalar da carga. Ela não fornece por si a nilpotência do diferencial ou a QME.
3. Estabelecer acordo perturbativo, identidades de mudança de fundo/cisão e compatibilidade dos estados e cutoffs.
4. Completar a correspondência gravitacional geral pelos mesmos dados TGL, mantendo explícita a ação/correspondência assumida, e justificar a rota UV escolhida.
5. Integrar os módulos anteriores ausentes e transportar as novas demonstrações à implementação/verificação pretendida. Fase, ramo, H3 interno e falsificadores existentes não são reabertos.

Esta entrega não contém CAS, Lean, diagramas ou testes de natureza novos. A matemática é escrita e revisada internamente no alcance indicado. O trabalho exploratório seguinte não integra estes resultados. Nenhum original, Atlas, índice, memória canônica ou gate foi alterado; o objetivo geral permanece aberto.
'''
create('REEXAME_SUFICIENCIA_073_20260910/ADENDO_REVISOES_073.md', adendum)
adendum_link = link('adendo final 073', 'REEXAME_SUFICIENCIA_073_20260910/ADENDO_REVISOES_073.md')

memory = f'''# Memória complementar — comutante e revisão final 073

10/09/2026. Registro novo na bancada Chatgpt; complementa a memória073 anterior, sem a modificar. [DERIVED] para a matemática; [REAL] para a documentação medida.

Estado recuperável: {report}; consolidação dos pareceres e da atualização posterior no {adendum_link}. A polarização pura adaptada realiza a saturação do radical; a Fock com domínio nuclear suave realiza P0 e a representação dos coeficientes Wick compactos de Q2. O estado físico067 permanece o bloco físico da construção.

Novo resultado posterior ao relatório: {commutant}, com {commutant_review}. No domínio e na classe de operadores contínuos de aumento finito do grau, a comutante do campo completo numa faixa de Cauchy é escalar; a supercomutante ímpar é zero. Se uma carga implementa um diferencial formal nilpotente e as fontes externas de ghost não nulo foram especializadas a zero, sua quadratura escalar de ghost dois é nula. Com adjunto comum existente e compatibilidade graduada com a involução, a carga é simétrica para Krein. Nada disso constrói a corrente, o implementador ou a QME.

Ponto de continuação: naturalidade/admissibilidade da primitiva geral com B0 e toda a hierarquia causal. A cohomologia ordinária073 trata jatos externos sem apagar d_HB0; a homotopia coordenada não é automaticamente natural. Só depois de construir as identidades renormalizadas e a carga poderão ser consumidas a positividade formal072 e a nova eliminação do termo escalar residual.

Continuam também acordo perturbativo, mudança de fundo/cisão, estados compatíveis, reconstrução geral pelos mesmos dados selecionados e rota UV. A captura073 documenta v338 e os módulos comparados, com pins no próprio arquivo; não usar este texto como fonte de hashes. A finalização deve conferir novamente a estabilidade dos artefatos lidos.

Nenhuma memória canônica foi atualizada, em respeito ao escopo somente Chatgpt. Este complemento e o adendo fornecem o material de integração para a sessão autorizada que codifica. Nenhuma alegação nova é feita sobre trabalho posterior ainda não revisto.
'''
create('REEXAME_SUFICIENCIA_073_20260910/MEMORIA_COMPLEMENTAR_COMUTANTE_073.md', memory)

drawing = f'''# Complemento ao desenho do fechamento — 073, comutante

10/09/2026. Adendo novo ao desenho073; [DERIVED — cadeia condicional]. Consulte o {adendum_link} para fontes e pareceres.

Construído neste modelo: polarização Hadamard adaptada → Fock e domínio Wick comum → Q0 e R0 efetivos → P0.

Construído na classe ordinária: cociclo universal com B0 → primitiva de jatos finitos. A seta para contratermo natural admissível e para toda a hierarquia causal permanece aberta.

Caminho para a interação: contratermos admissíveis e identidades quânticas → corrente/carga implementadora no domínio comum → aplicação do critério da comutante → Q²=0, sob nilpotência prévia do diferencial e anel escalar de ghost zero. O adjunto e a compatibilidade da involução também são hipóteses do critério de simetria. Portanto a comutante encurta a verificação final da carga, mas não pode substituir a construção das identidades que consome.

P0 + P1 integral + P2 permitem consumir o teorema de positividade formal072. Depois permanecem compatibilidade entre fundos/estados, reconstrução geral da mesma informação TGL e UV. Não existe aqui uma soma não perturbativa nem confirmação de natureza.
'''
create('REEXAME_SUFICIENCIA_073_20260910/DESENHO_COMPLEMENTAR_073_COMUTANTE.md', drawing)

tunnel = f'''# Entrega espontânea 073 — polarização BRST, domínio Wick e cohomologia

10/09/2026. Para a sessão que codifica um.py. [DERIVED — demonstrações escritas, não Lean] [REAL — estado documental a conferir no manifesto]. Somente arquivos novos em Chatgpt.

Entrada: {report}. Ler também o {adendum_link}, que registra as revisões e o corolário posterior da comutante. O relatório congelado sozinho não contém esse último resultado.

## Conteúdo disponível para integração

1. {polarization}: projetores Hadamard puros exatamente adaptados ao BRST, preservando o estado físico067; correções suaves e majorante explícita. A seleção auxiliar satisfaz as duas condições de saturação do radical. Um contraexemplo separado mostra por que a família arbitrária068 não autorizava P0 automaticamente.
2. {fock}: domínio comum nuclear suave com número finito de partículas, representação da mesma covariância, Q0²=0 e Q0R0+R0Q0=1−P. Em ker Q0, a norma é a norma física de P; vetores nulos são exatamente im Q0. P0 está realizado neste modelo. Polinômios Wick compactos microcausais preservam o domínio; isso realiza somente a parte representacional de P1.
3. {cohom}: exatidão ordinária de grau total cinco com B0, sB0=0 e derivada horizontal mantida. Não tipar como primitiva natural admissível nem como QME. Ser cociclo na álgebra universal e tratar a completação efetiva continuam condições materiais.
4. {commutant}: comutante escalar na classe de operadores contínuos sobre o domínio suave do campo completo numa faixa de Cauchy. Se a carga já implementa um diferencial nilpotente, Q²=0 decorre de ghost dois depois de zerar fontes externas de ghost não nulo. Simetria também tem critério condicional, exigindo adjunto comum e involução compatível.

## Obrigações preservadas

Contratermos naturais/admissíveis em todas as ordens; corrente e carga interagentes; identidades renormalizadas/QME; acordo perturbativo e mudanças de fundo; estados compatíveis; reconstrução geral pelos mesmos dados e justificação UV. Os módulos anteriores ainda ausentes na captura canônica continuam uma pendência distinta das demonstrações novas.

Não promover a contagem de integridade documental a teoremas Lean. Não promover P0 livre a positividade interagente completa. Não promover exatidão ordinária a remoção causal da anomalia. Nenhuma execução de um.py, teste de natureza ou modificação de original/gate ocorreu nesta entrega. Pareceres e hashes medidos acompanham as fontes e serão reunidos pelo finalizador073. O objetivo geral permanece aberto.
'''
create('TUNEL/DO_CHATGPT/ENTREGA_073_ESPONTANEA_polarizacao_BRST_dominio_Wick_e_cohomologia.md', tunnel)

config = {
    'source_directories': [
        'RADICAL_GNS_BRST_073_20260910',
        'POLARIZACAO_BRST_HADAMARD_073_20260910',
        'REVISAO_POLARIZACAO_BRST_073_20260910',
        'FOCK_HADAMARD_QUARTETOS_073_20260910',
        'REVISAO_FOCK_DOMINIO_073_20260910',
        'COHOMOLOGIA_ESPECTADOR_B0_073_20260910',
        'COMUTANTE_FOCK_SUAVE_073_20260910',
        'REVISOES_RAIZ_073_20260910',
        'REVISAO_DOCUMENTAL_RELATORIO_073_20260910_013647_738543'
    ],
    'new_cas_controls': 0,
    'new_lean_compilations': 0,
    'status': 'WRITTEN_P0_REALIZED_IN_DECLARED_MODEL__ORDINARY_B0_COHOMOLOGY_AND_CONDITIONAL_CHARGE_CRITERION__INTERACTION_OPEN',
    'written_results': [
        'Radical saturation exact sequence, finite negative counterexample to arbitrary auxiliary choices, and repair.',
        'Pure BRST-adapted Hadamard polarization with smooth correction and explicit majorant, preserving physical067.',
        'Fock-Krein realization on a common nuclear smooth Wick domain; actual Q0/R0 contraction, P0 positivity and null=image.',
        'Ordinary finite-jet cohomological primitive with spectator B0 and its horizontal derivative retained.',
        'Scalar commutant and vanishing odd supercommutant in the stated continuous finite-degree operator class; conditional nilpotence and symmetry of an already constructed implementer.'
    ],
    'remaining': [
        'Natural admissible renormalization of the effective anomaly with B0, formal completion, analytic/scaling controls and all causal insertion/contact identities.',
        'Renormalized current and charge implementation on the common domain; quantum differential nilpotence and QME.',
        'Perturbative agreement, split/background identities and compatible states/cutoffs.',
        'General gravitational reconstruction from the same selected TGL data with explicit correspondence assumptions, and justified UV route.',
        'Canonical integration of the absent earlier modules and of the new written constructions.'
    ],
    'limits': 'Written and internally reviewed mathematics in the declared Einstein-sigma background/domain, with delimited literature inputs. Not Lean/CAS, not a natural admissible anomaly-removal theorem, not a constructed interacting charge/QME, not a nonperturbative sum or UV closure. Documentary checks count only artifact integrity. Original files and canonical memories remain read-only; no nature test or gate change.'
}
create('REEXAME_SUFICIENCIA_073_20260910/CONFIG_ENTREGA_073.json',
       json.dumps(config, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'created_utc': datetime.now(timezone.utc).isoformat(), 'created': CREATED}, ensure_ascii=True))
