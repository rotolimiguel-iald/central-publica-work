from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_072_20260910'
REV = ROOT / 'REVISOES_RAIZ_072_20260910_004104_732492'
CAUSAL = ROOT / 'COMPARACAO_CAUSAL_FUNDOS_072_20260910'
DOCREV = ROOT / 'REVISAO_DOCUMENTAL_RELATORIO_072_20260910_010204_273150'
POSIT = ROOT / 'POSITIVIDADE_BRST_FORMAL_072_20260910'
RETR = ROOT / 'RETRACAO_BRST_FUNDOS_072_20260910_003743_284187'
LOG = ROOT / 'PRIMITIVA_COVARIANTE_LOGVOLUME_072_20260910_003839_535005'
RETRREV = ROOT / 'REVISAO_RETRACAO_FUNDOS_072_20260910_004627_020318'
inputs = {}
outputs = []

def pin(path):
    path = Path(path).resolve()
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw),
            'sha256': hashlib.sha256(raw).hexdigest()}

def source(path):
    item = pin(path)
    inputs[item['path']] = item
    return item

def link(label, path):
    assert Path(path).is_file(), path
    return f'[{label}](<{Path(path).as_posix()}>)'

def new(path, value):
    path = Path(path).resolve()
    assert path.is_relative_to(ROOT) and not path.exists(), path
    raw = value.encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw and len(raw) > 0
    temp.rename(path)
    assert path.read_bytes() == raw
    outputs.append(pin(path))

def new_json(path, value):
    new(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')

for path in [CAUSAL / 'CONTRATO_ADMISSIBILIDADE_Q2.md',
             CAUSAL / 'TRANSPORTE_E_WARD_REFERENCIA.md',
             CAUSAL / 'MANIFESTO_COMPARACAO_072.json',
             RETR / 'PRECISAO_FONTES_CONJUGADAS_E_REFERENCIA.md',
             POSIT / 'PRECISAO_COMUTADOR_GRADUADO_E_R0.md',
             DOCREV / 'PARECER_RELATORIO_072.md',
             DOCREV / 'REGISTRO_REVISAO_RELATORIO_072.json',
             OUT / 'REEXAME_SUFICIENCIA.md',
             OUT / 'MEMORIA_DE_TRABALHO_072.md',
             OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_072.md']:
    source(path)

review = '''# Parecer da raiz — comparação causal e Ward em referência fixa

10/09/2026. [DERIVED — revisão analítica interna das demonstrações escritas] [KNOWN — importação delimitada] [REAL — pins medidos]. Nenhuma execução/importação de um.py, compilação Lean ou cálculo CAS. Esta revisão é da frente causal072, escrita por outra frente, e não se apresenta como aprovação externa.

**Conclusão: favorável no alcance enunciado.** Foram lidas integralmente as notas de admissibilidade e de transporte/Ward. O reparo do CCR é infinitesimal; a Ward construída é anômala e conserva a referência B0. Não há nesta nota demonstração da remoção geral da anomalia, da QME ou de independência física de fundo.

## Conferência das identidades

1. Na derivada de mu exp(hbar Gamma_H), os operadores de contração com kernels independentes dos campos comutam. A regra do produto produz exatamente o termo adicional hbar mu exp(hbar Gamma_H) Gamma_dotH. Nos observáveis lineares a parte antissimétrica é i hbar dotE. Uma mudança de Wick simétrica fixa esses observáveis e, portanto, não corrige o CCR variável. Trata-se da falha de uma identificação específica, não de uma prova de anomalia física não removível.

2. A diferenciação dos Green com as condições causais dá dotG=-G dotP G. Com E=Gret-Gadv, a expansão de -Gret dotP E-E dotP Gadv cancela os dois termos mistos e reproduz dotE. A adjunção é tomada no par dual previamente identificado, de modo que r*=1-epsilon dotP Gadv. A expansão de r E r* confere com E_epsilon na primeira ordem.

3. O controle escalar usa o modo espacial constante em R x S3. Entre dois tempos separados por menos de pi/m, os dois senos da integral são positivos no suporte de chi. Seu sinal negativo fornece um pareamento não nulo para testes próximos. Esse exemplo controla a variação do propagador; não foi apresentado como diagrama Einstein–sigma.

4. A antissimetrização de w=dotH+Gret dotP H+H dotP Gadv é i vezes dotE+Gret dotP E+E dotP Gadv, que se anula. A nota corretamente exige uma comparação Hadamard compatível para afirmar suavidade. Simetria sozinha não basta. O suporte ampliado de r*f também é conservado como limitação, sem aplicar diretamente a r o requisito de derivação local de inserções.

## Conferência da extensão com fontes

Na referência B0 fixa, d_theta não deriva os propagadores e comuta graduadamente com o diferencial livre, pois atua em fatores distintos. Isso prova D0 ao quadrado igual a zero e a regra graduada de Leibniz. A extensão multilinear dos produtos por coeficientes externos suaves é válida coeficiente a coeficiente; ação por partes inclui as derivadas desses coeficientes. A identidade (13) segue da mesma regra e não constitui uma hipótese de remoção de anomalia.

O domínio exclui os antifields externos theta*, omega*. A parte forte linear theta* omega serve para extrair a CME reduzida. A transformação de gauge mantém o termo omega delta_theta Psi. Separar Sigma0,B0 fornece M(Vext)=0 na região de cutoffs constantes, com s0 clássico distinto de s-hat0. Conservar os termos lineares ao variar fundos arbitrários evita pressupor que o novo fundo continua on-shell.

A filtração explicitada controla tadpoles e alterações quadráticas por grau externo, e os demais vértices por peso perturbativo, laços e truncagem. Deve ser usada como filtração combinada, com parte Laurent negativa finita por grau externo; não é licença para somar uma série não filtrada em t ou ignorar os termos dependentes dos campos. Constantes centrais e seus fatores na matriz relativa foram separados no enunciado.

A Ward original aplicada aos coeficientes e somada à identidade exata de d_theta dá (16), com a mesma normalização i/hbar. As inserções marcadas são obtidas por polarização. A consistência de primeira ordem não removida é (19); ela declara fechamento modulo d, não exatidão. A projeção theta=omega=0 recupera a identidade de B0. Esses passos constroem um levantamento em uma álgebra fixa, não a equivalência de toda família de produtos com operadores livres variáveis.

## Importação e fronteira

Conferi diretamente o Teorema 3 e a equação (154) de [Fröb, 1803.10235v3](https://arxiv.org/pdf/1803.10235). O primeiro exige uma derivação local e covariante da álgebra livre; a segunda conserva expressamente a anomalia na identidade BV. A construção de referência satisfaz a parte relativa às fontes sem postular a ausência da anomalia. A aplicação ao multiplet e aos contatos ainda consome o dicionário e a construção Q2_069 explicitados pela fonte.

A retração age nos doublets adicionados e não na referência B0 dos kernels. A primitiva necessária vive, portanto, na classe admissível com os espectadores ainda presentes, salvo uma prova adicional que elimine sua dependência. O resultado H1,4 de071 para outra classe não foi usado por homonímia. A normalização de acordo perturbativo, sua compatibilidade de gauge, os contatos, a QME, a representação física e UV permanecem obrigações.

Não encontrei erro material nas identidades conferidas. A aprovação é restrita às demonstrações acima e às hipóteses analíticas já identificadas. Não implica uma nova auditoria completa das fontes 067–071 ou compilação de qualquer prova.
'''
new(REV / 'PARECER_COMPARACAO_CAUSAL_072.md', review)
new_json(REV / 'REGISTRO_PARECER_COMPARACAO_CAUSAL_072.json', {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'FAVORABLE_INTERNAL_WRITTEN_REVIEW__ANOMALOUS_REFERENCE_WARD_ONLY',
    'review': pin(REV / 'PARECER_COMPARACAO_CAUSAL_072.md'),
    'sources': [inputs[(CAUSAL / name).as_posix()] for name in
                ['CONTRATO_ADMISSIBILIDADE_Q2.md', 'TRANSPORTE_E_WARD_REFERENCIA.md',
                 'MANIFESTO_COMPARACAO_072.json']],
    'new_cas_controls': 0, 'new_lean_compilations': 0,
    'source_files_written': False,
    'scope': 'First-order CCR transport and anomalous Ward in a fixed reference with formal central sources; no QME or anomaly-removal assertion.'
})

adendum = f'''# Revisões, precisões e fechamento documental — entrega 072

10/09/2026. [DERIVED — demonstrações escritas revisadas internamente] [REAL — integridade documental medida]. Adendo novo: nenhuma fonte congelada foi sobrescrita. Este documento acompanha o {link('relatório 072', OUT / 'REEXAME_SUFICIENCIA.md')} e delimita sua utilização na sessão que codifica.

## Resultados revistos e alcance

| Frente | Revisão e resultado | Limite que acompanha a integração |
|---|---|---|
| Primitiva de logvolume | {link('Parecer da raiz', REV / 'PARECER_PRIMITIVA_LOGVOLUME.md')} favorável para a família explicitada | A identidade produz uma primitiva da densidade f(b) div_barg(C) L; não classifica a anomalia inteira nem normaliza todos os produtos e contatos. |
| Retração de fundos | {link('Parecer independente interno', RETRREV / 'PARECER_RETRACAO_FUNDOS.md')} favorável após precisão de domínio | A retração é formal nas diferenças dos fundos, na vizinhança da diagonal. Ela transporta uma primitiva admissível da projeção, cuja existência ainda precisa ser demonstrada na classe correta. |
| Transporte e Ward | {link('Parecer da raiz', REV / 'PARECER_COMPARACAO_CAUSAL_072.md')} favorável | Transporte do CCR de primeira ordem; Ward com anomalia em B0 fixo. A referência B0 não é eliminada pela retração dos doublets adicionados. |
| Estado interagente formal | {link('Parecer da raiz', REV / 'PARECER_POSITIVIDADE_FORMAL.md')} favorável às provas condicionais, com precisão graduada | P0–P2 exigem representação compatível, domínio comum e carga simétrica/nilpotente. O certificado algébrico de quartetos não realiza por si só esses dados Hadamard/Wick. |
| Relatório de suficiência | {link('Parecer documental independente interno', DOCREV / 'PARECER_RELATORIO_072.md')} favorável | Conferência documental de escopos e links; não é revisão analítica independente de todas as frentes nem recaptura dos originais. |

## Precisões que devem acompanhar as fontes

A {link('precisão do logvolume', LOG / 'PRECISAO_REMISSAO_E_ALCANCE.md')} corrige a remissão para a seção 4 do dicionário BV, sem alterar a prova. A regularidade da primitiva acompanha a dos seus coeficientes: a razão de volumes não transforma uma entrada apenas suave em analítica.

A {link('precisão de fontes conjugadas', RETR / 'PRECISAO_FONTES_CONJUGADAS_E_REFERENCIA.md')} restringe a retração conjugada à subálgebra sem os antifields externos B*, Omega*. O termo linear nesses antifields permite extrair a CME reduzida; uma contração do complexo forte inteiro não foi demonstrada. A seção de avaliação envia Omega para s dos campos, e não para zero.

A {link('precisão de orientação graduada', POSIT / 'PRECISAO_COMUTADOR_GRADUADO_E_R0.md')} corrige a frase sobre trocar a orientação do bracket. Para Q ímpar, [A,Q]_gr = -(-1)^|A| [Q,A]_gr. Trocar uniformemente Q por -Q reproduz a convenção inversa apenas nos observáveis pares. As recorrências e provas de positividade usam a convenção fixa da fonte e permanecem válidas. A raiz leu a precisão e conferiu a identidade após emitir o parecer anterior.

O {link('parecer documental', DOCREV / 'PARECER_RELATORIO_072.md')} explicita ainda que “finita coeficiente a coeficiente”, na seção 3 do relatório, se refere à retração formal nas diferenças dos fundos. Não se afirma convergência, um limite uniforme de jatos ou uma retração global entre configurações arbitrariamente distantes.

## Pendências efetivas

1. Construir a primitiva geral admissível da quebra de Q2, incluindo os coeficientes de B0 ou demonstrando sua eliminação por um levantamento natural. Conferir conjuntamente suporte diagonal, regularidade, escala, inserções e contatos.
2. Normalizar a comparação de fundos e a independência da cisão com o acordo perturbativo do multiplet completo. A Ward anômala em referência fixa não substitui essa identidade.
3. Remover a anomalia em todas as ordens e realizar a QME, a corrente e a carga no domínio comum. Implementar P0 com a mesma álgebra Hadamard/Wick e pagar P1–P2 para consumir a recorrência do estado formal.
4. Resolver as obrigações de colagem/globalidade e de independência de cutoff e fundo dos estados. Positividade formal não é existência não perturbativa.
5. Completar o alcance da correspondência entre os mesmos dados selecionados e a reconstrução geral, preservando os postulados físicos explícitos; completar a rota UV escolhida. O registro de fase e ramo já integrado não é reaberto.
6. Integrar os módulos ainda ausentes e formalizar as novas demonstrações, sem converter afirmações escritas em certificados de compilação.

## Evidência e custódia

A captura 072 e a releitura atual dos quatro artefatos concordam byte a byte. A finalização compara novamente os pins da captura com o disco antes de emitir os recibos. As contagens de módulos são de presença por leitura/AST; os relatórios de execução anteriores foram lidos, sem reexecução.

Os totais finais de integridade estão no [resultado estruturado](<{(OUT / 'RESULTADO_ENTREGA_072.json').as_posix()}>) e no [manifesto 072](<{(OUT / 'MANIFESTO_ENTREGA_072.json').as_posix()}>), gerados por script após as comparações. As verificações são documentais. Há zero novos controles CAS, zero compilações Lean e zero cálculos de diagramas nesta entrega.

A {link('memória 072', OUT / 'MEMORIA_DE_TRABALHO_072.md')} e o {link('adendo ao desenho', OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_072.md')} são arquivos novos exclusivamente em Chatgpt. Atlas, índice, memórias canônicas, um.py original, selo e gate permanecem preservados. O objetivo geral continua aberto.
'''
new(OUT / 'ADENDO_REVISOES_072.md', adendum)

tunnel = f'''# Entrega espontânea 072 — fundos, contratermos e positividade formal

10/09/2026. À sessão que codifica: demonstrações novas e revisões estão disponíveis na bancada Chatgpt. [DERIVED] Provas escritas, condicionadas nos pontos assinalados; [REAL] conferência documental por pins. Nenhum original foi alterado nem um.py executado/importado.

Começar pelo {link('relatório de suficiência', OUT / 'REEXAME_SUFICIENCIA.md')} e ler com o {link('adendo de revisões', OUT / 'ADENDO_REVISOES_072.md')}. Ele contém os pareceres, as correções de sinal/domínio e os limites que acompanham cada construção. A {link('memória de trabalho', OUT / 'MEMORIA_DE_TRABALHO_072.md')} e o {link('desenho atualizado', OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_072.md')} registram a continuidade sem tocar as memórias canônicas.

## Conteúdo pronto para estudo e formalização

- Primitiva local de logvolume para a família f(b) div_barg(C) L, com regularidade, realidade, escala e termos de cutoff explícitos.
- Retração BRST clássica formal de fundos, com seção Omega=s(fields), Log/Exp no alvo S3 e domínio sem os antifields externos. A fórmula transporta uma primitiva admissível; não pressupõe que qualquer cociclo já a tenha.
- Defeito de Leibniz ao variar kernels, reparo retardado do CCR de primeira ordem e Ward estendida com anomalia em referência B0 fixa. Termos lineares/quadráticos e fontes de gauge são mantidos.
- Certificado algébrico de quartetos e recorrência para levantar vetores e estados físicos em séries formais, sob P0–P2. A representação compatível Hadamard/Wick, a carga renormalizada e a QME são obrigações.

## Integração e limites

A captura leu o v338, com 683 arquivos embutidos e 77 dos 98 módulos do comparador; 21 continuam ausentes. Esta entrega não é uma integração no programa canônico. O registro de fase e ramo, H3 interno e os falsificadores existentes continuam reconhecidos.

Não converter a primitiva de uma família em remoção geral de anomalias, a Ward anômala em QME, a retração de doublets em eliminação de B0 ou o quarteto abstrato em uma representação Hadamard construída. A orientação do bracket precisa conservar o fator de paridade da precisão aditiva. Manter explicitamente a correspondência física condicional, globalidade e UV no caminho crítico.

O [resultado 072](<{(OUT / 'RESULTADO_ENTREGA_072.json').as_posix()}>) e o [manifesto 072](<{(OUT / 'MANIFESTO_ENTREGA_072.json').as_posix()}>) registram os pins e verificações finais. Contagens documentais não são números de teoremas. Não há nova compilação Lean ou CAS. Nenhum selo/gate canônico foi alterado. O objetivo geral permanece ativo.
'''
new(ROOT / 'TUNEL/DO_CHATGPT/ENTREGA_072_ESPONTANEA_fundos_contratermos_e_positividade_formal.md', tunnel)

new_json(OUT / 'CONFIG_ENTREGA_072.json', {
    'source_directories': [p.name for p in [RETR, RETRREV, LOG, POSIT, CAUSAL, REV, DOCREV]],
    'new_cas_controls': 0,
    'new_lean_compilations': 0,
    'status': 'WRITTEN_LOGVOLUME_PRIMITIVE__CLASSICAL_FORMAL_BACKGROUND_RETRACTION__ANOMALOUS_REFERENCE_WARD__CONDITIONAL_POSITIVE_FORMAL_STATE',
    'written_results': [
        'Explicit local real covariant logvolume primitive for the specified anomaly family; regularity and scaling inherited with stated conditions.',
        'Classical natural formal retraction of external background doublets, restricted to the algebra without their conjugate antifields.',
        'Kernel Leibniz defect, first-order retarded CCR transport, and anomalous extended Ward identity with formal central sources in fixed reference B0.',
        'Algebraic quartet certificate and formal lifting/positivity recurrence under representation, common-domain, and symmetric nilpotent charge contracts P0-P2.'
    ],
    'remaining': [
        'Admissible primitive of the general causal anomaly including B0 spectators or justified elimination of B0.',
        'Perturbative agreement and background-split Ward normalization for the complete multiplet and marked insertions/contact terms.',
        'All-order causal anomaly removal, QME, renormalized current and charge implementation on a common domain.',
        'Actual auxiliary Hadamard/Wick representation satisfying P0 and interacting contracts P1-P2.',
        'Global and cutoff/background-compatible physical states; no nonperturbative convergence asserted.',
        'General physical reconstruction from the same selected data with explicit correspondence postulates; chosen UV route.',
        'Integration of pending modules and formalization of the new written demonstrations.'
    ],
    'limits': 'Internal written proofs/reviews with explicit inputs. Documentary integrity is not a theorem count, a Lean compilation, a loop computation, or physical confirmation. Originals and canonical gate preserved; goal remains active.'
})

for path, original in inputs.items():
    assert pin(path) == original, 'Changed source: ' + path
print(json.dumps({'status': 'NEW_DOCUMENTS_WRITTEN__INPUT_BYTES_UNCHANGED',
                  'inputs_checked': len(inputs), 'outputs': outputs}, ensure_ascii=True))
