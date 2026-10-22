from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_085_20260910'
REVIEW = ROOT / 'REVISOES_RAIZ_085_20260910'
QNOTE = ROOT / 'INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md'
QREVIEW = ROOT / 'REVISAO_INVARIANTES_KILLING_085_20260910_061730_221515/PARECER_KT_LINEAR_E_INVARIANTES_085.md'
GNOTE = ROOT / 'PRIMEIRA_PAGINA_TODOS_GRAUS_085_20260910/COHOMOLOGIA_S0_GERAL_E_INVARIANTES_POSITIVOS.md'

def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

def emit(path, text):
    raw = text.encode('utf-8')
    assert path.resolve().is_relative_to(ROOT) and not path.exists() and raw
    temp = path.with_name(path.name + '.tmp_new')
    with temp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    temp.rename(path)
    assert path.read_bytes() == raw
    return pin(path)

def link(label, path):
    return '[' + label + '](<' + path.as_posix() + '>)'

sources = [QNOTE, QREVIEW, GNOTE, OUT / 'ESTADO_CANONICO_085.json',
    ROOT / 'REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md',
    ROOT / 'CORRENTE_NECESSARIA_E_LIMITE_GRADIENTE_084_20260910/EULER_SOZINHO_E_GRADIENTE_ESCALAR_NAO_BASTAM.md']
before = [pin(path) for path in sources]
snapshot = json.loads((OUT / 'ESTADO_CANONICO_085.json').read_bytes())
assert snapshot['seal_um_hash_matches'] and snapshot['all_read_sources_unchanged']
assert all(item['unchanged'] for item in snapshot['comparison_with_delivery084'])
um_pin = next(item for item in snapshot['pins'] if item['path'].endswith('/Nós/um.py'))
REVIEW.mkdir(exist_ok=False)
review = '''# Revisão da raiz085 — nulidade do módulo invariante quadrático

10/09/2026. [DERIVED — revisão matemática escrita da prova de Turing]. A raiz leu integralmente a nota085 e o parecer independente de Herschel; conferiu a aplicação primária e o retorno ao módulo original. Não identificou erro material no alcance fixado. Este parecer não é apresentado como aprovação independente da generalização escrita pela própria raiz.

O primeiro passo é algébrico: M=kerγ/EOM injeta em U/EOM porque HR0=0; como as relações são lineares, Sym(U)/(EOM)=Sym(U/EOM). Uma inclusão de espaços vetoriais reais cinde, portanto Sym²M injeta no grau dois da álgebra on-shell. A nota não presume liberdade dos geradores Weyl nem radicaliza um ideal pela anulação em soluções.

O novo pagamento de regularidade KT inclui os dois extremos. PH=0 implica P=BD pelo algoritmo finito de Bianchi; ZD=0 força o símbolo ζ_a z_b+ζ_b z_a a zero, e a indução na ordem dá Z=0. Isso exclui identidades de segunda etapa, não seções Killing. Os cortes h_I:|I|+1, p_I:|I|+3, q_I:|I|+4 são estáveis e as primitivas ficam finitas. Em frame local, as matrizes de jatos têm posto constante na espaço-forma fixada. A contração dos pares na álgebra simétrica graduada divide somente por inteiros positivos, preservando o grau polinomial e a ordem finita por elemento.

[KNOWN — importação conferida] Os teoremas6.2 e6.5(i) e a prova6.B de [BBH2000](https://arxiv.org/pdf/hep-th/0002245v3) fornecem a passagem de funções horizontalmente constantes ao grupo KT relativo de grau quatro e sua nulidade no sistema irreducível estritamente linear. O encerramento após(6.49) elimina os restos quando a ação é quadrática e os geradores independem de h. A aplicação085 usa esse caso, não a extensão apenas linearizável por série formal.

Um elemento invariante por g tem representante escalar natural num corte finito de isotropia. As transvecções atuam por derivada covariante no ponto, com transporte à carta pelas isometrias da referência. Da invariância resulta d_HF=0 no quociente on-shell auxiliar. O resultado primário dá F−c no ideal das EOM. Ao avaliar num ponto, os coeficientes C∞(x) tornam-se escalares e a igualdade pertence ao mesmo ideal pontual; δ não diferencia x. Como F tem grau dois e o ideal é homogêneo, h=0 força c=0. A injeção inicial devolve n=0 em Sym²M.

O retorno só requer igualdade zero, não naturalização de uma primitiva coordenada não nula. Esse detalhe limita corretamente o resultado: ele não constrói a corrente natural de divergência J_W. Para Rher inerte, tensorizar o mapa injetivo v↦(ρ_XAv)_A por uma álgebra sobre R conserva a injetividade, inclusive com nilpotentes. Não há avaliação multiplicativa dos coeficientes herdados.

A consequência correta para084 é retirar f∈N^g do critério J_W=divV+K²f. Sobra J_W=divV. A existência ou inexistência de V permanece aberta. O grau horizontal zero usado na prova não é o grau horizontal quatro desse problema. Nenhuma conclusão de QME, causalidade integral, transporte ao fundo φ=id, K variável ou UV segue daqui.

Zero execução matemática, CAS ou Lean nesta revisão. As fontes foram pinadas antes/depois. A frase final do parecer de Herschel sobre084 encerrada antecipou sua finalização documental:084 só foi efetivamente fechada em09:19:06 UTC pelo resultado correspondente. Essa precisão temporal será registrada no adendo085, sem alterar o parecer congelado.
'''
review += '\n' + link('Nota085', QNOTE) + '\n' + link('Parecer independente085', QREVIEW) + '\n'
review_pin = emit(REVIEW / 'PARECER_NULIDADE_INVARIANTES_QUADRATICOS_085.md', review)
assert before == [pin(path) for path in sources]
emit(REVIEW / 'REGISTRO_REVISAO_RAIZ_085.json', json.dumps({
    'created_utc': datetime.now(timezone.utc).isoformat(), 'sources_before': before,
    'sources_after': [pin(path) for path in sources], 'all_sources_unchanged': True,
    'review': review_pin, 'new_mathematical_executions': 0, 'new_lean_compilations': 0
}, ensure_ascii=False, indent=2)+'\n')

report = '''# Reexame de suficiência085 — invariantes eliminados e primeira página geral

10/09/2026. A entrega084 foi progresso: deu a forma normal por isotropia e excluiu dois candidatos de cancelamento. Esta entrega085 paga a determinação do módulo invariante que ela mantinha aberta e descreve a cohomologia do diferencial linear em todas as valências finitas. O objetivo geral continua aberto.

## Resultado quadrático aceito

[DERIVED — demonstração escrita com revisão independente] Na referência espaço-forma de quatro dimensões, K>0 real fixado, κ não nulo fixado, setor métrico mínimo com φ0 constante projetada, escalares herdados inertes e finitíssimos jatos por expressão,

**(Rher⊗Sym²M)^g = 0.**

M é o módulo linear Weyl/EOM; g é TODA a álgebra de Killing. Não é uma afirmação apenas de invariância de Lorentz. A prova injeta o módulo quadrático na álgebra polinomial on-shell original, paga a resolução KT estritamente linear e usa a cohomologia característica de grau zero. Um invariante daria uma constante, mas a homogeneidade positiva força essa constante a zero. A extensão real inerte mantém os nilpotentes; não depende de testes TT separarem o módulo.

@QNOTE@
@QREVIEW@

## O critério de cancelamento ficou menor

A condição084 era J_W=divV+K²f, com f∈N^g. O resultado acima força f=0. Portanto, no MESMO complexo natural,

**J_Wν é CE-exato ⇔ existe V natural, quadrático e finito com divV=J_W.**

Os coeficientes quadráticos de ambas as Cartan, traço e Euler, desaparecem. A unidade do anel é de grau zero e não entra nesse módulo quadrático. A exclusão084 de V=c gradJ_W permanece válida; outras contrações e jatos superiores ainda não foram classificados nesta entrega.

Isso é uma redução necessária e suficiente para esta etapa. Não é uma construção da corrente V, nem uma prova de que nenhuma corrente exista. A nulidade de funções horizontalmente constantes é um problema de grau zero; o alvo de divergência é de grau quatro.

## Generalização da raiz em todas as valências finitas

[DERIVED — demonstração escrita; revisão específica ligada no adendo final] A exatidão completa da cadeia linear deixa H(L)=M⊕G[1], com G os dez jatos de Killing. Künneth e a simetrização graduada, seguidas de invariantes sob a isotropia h, dão

H^q(s0)|_E = Rher⊗[Sym^(E−q)M⊗Λ^qG]^h,
para 0≤q≤min(E,10), e zero fora dessa faixa.

E é valência total; q é número de ghost. É a primeira página da análise filtrada, não H¹ e não a cohomologia total do BRST interagente. As identidades082 são sobre geradores, então Leibniz identifica o primeiro diferencial em cada m=E−q com C^•(g,Rher⊗Sym^mM)^h.

A prova de invariantes usa somente homogeneidade m>0 e se estende a todo m positivo. Assim (Rher⊗Sym^mM)^g=0 para m>0; os invariantes da álgebra polinomial algébrica inteira são somente Rher em grau zero. A forma normal084 estende-se pelo mesmo argumento finito: qualquer alvo horizontal Pν de grau positivo é exato precisamente quando P=divV na classe natural correspondente.

O caso m=0 fica separado: coeficientes constantes de Euler continuam possíveis. Não se estende a fórmula a produtos completados sem fixar sua categoria. @GNOTE@

## O que ainda falta no objetivo completo

[OPEN] No setor em investigação, decidir se J_W pertence à imagem da divergência natural em TODAS as ordens finitas admissíveis. Uma solução precisa produzir a primitiva BRST e seus levantamentos seguintes; uma obstrução precisa delimitar exatamente o ramo excluído. Nem um dos dois resultados é antecipado aqui.

[OPEN] Resolver as demais cohomologias de anomalias, os diferenciais superiores, os contratermos causalmente admissíveis e a equação mestra quântica da teoria interagente. O primeiro diferencial descrito em todas as valências não elimina automaticamente os seguintes.

[OPEN] Construir a reconstrução gravitacional geral e as relações de matéria/conservação/área/calor para os mesmos dados selecionados, com o alcance físico e os postulados de correspondência explicitados; justificar a rota UV. A fase/ramo e H3 da tela permanecem reconhecidos como pagos no modelo. H³ cohomológico não reabre H3 da tela.

## Estado canônico e verificação

[REAL — leitura] O snapshot085 mede os mesmos quatro artefatos de084. O um.py ainda tem @BYTES@ bytes, SHA-256 `@HASH@`,683 arquivos embutidos e77 dos98 módulos acompanhados;21 continuam ausentes no programa canônico examinado. O selo coincide com os bytes. Não foi localizada nem atribuída uma nova versão a esse caminho. @SNAPSHOT@

O gate canônico e o gate UV permanecem os mesmos lidos em084. O selftest registrado foi lido, não reexecutado. Presença AST não equivale a compilação nesta rodada. Não se atribuem as demonstrações085 ao um.py antes de sua integração e verificação próprias.

Zero nova execução matemática, CAS, Lean ou rito de natureza em085. Os recibos conferem integridade documental; os resultados são demonstrações escritas revisadas, não teoremas recém-compilados. Nenhum original, Atlas, índice, memória canônica, selo ou gate foi alterado; somente arquivos novos em Chatgpt. A memória e o desenho recebem adendos novos nesta pasta. A investigação086 está excluída desta entrega. Não há conclusão geral da gravidade quântica.
'''
for old, new in {
    '@QNOTE@':link('Demonstração quadrática085',QNOTE), '@QREVIEW@':link('Revisão independente da demonstração',QREVIEW),
    '@GNOTE@':link('Demonstração da primeira página geral',GNOTE), '@BYTES@':str(um_pin['bytes']), '@HASH@':um_pin['sha256'],
    '@SNAPSHOT@':link('Snapshot085',OUT/'ESTADO_CANONICO_085.json')}.items():
    report = report.replace(old,new)
emit(OUT / 'REEXAME_SUFICIENCIA.md', report)
memory = '''# Memória de trabalho — adendo085

10/09/2026. Novo documento de sessão em Chatgpt; o Atlas canônico não é copiado, bifurcado ou alterado.

[DERIVED] N^g=0 no módulo quadrático de jatos finitos da referência K>0 fixada, projeção métrica φ0 constante, escalares herdados inertes. Prova: M↪U/EOM, Sym²M↪Sym(U/EOM); KT linear acíclica por PH=BD e ZD=0; BBH6.2/6.5 no caso estritamente linear; invariância dá d_HF=0, homogeneidade dois força a constante zero; injeção e planura real retornam ao módulo, inclusive com nilpotentes.

[DERIVED] Critério084 agora é J_Wν exato ⇔ J_W=divV com V natural quadrático e finito. Nenhum coeficiente quadrático de Cartan sobrevive. Unidade escalar tem grau zero. V não foi construído ou excluído no módulo inteiro; c gradJ_W continua excluído084.

[DERIVED — generalização da raiz com revisão específica no adendo] H(L)=M⊕G[1]; H^q(s0)_E=Rher⊗[Sym^(E−q)M⊗Λ^qG]^h, 0≤q≤min(E,10), demais zero. Primeiro diferencial CE em todo m=E−q. Invariantes de Sym^mM são zero para todo m>0; na álgebra polinomial inteira sobram apenas os escalares. Forma normal para alvos horizontais positivos reduz a divV. m=0 é exceção explícita para Euler. Primeira página não é cohomologia interagente total.

[REAL — snapshot] Quatro artefatos canônicos idênticos a084: v338,683 embutidos,77/98 módulos acompanhados e21 ausentes. Hashes lidos do snapshot; nenhuma execução/importação de um.py. Zero novos controles matemáticos/CAS/Lean. [OPEN] Corrente geral, anomalias/QME, causalidade, reconstrução geral dos mesmos dados e UV. Fase/ramo e H3 da tela não reabertos. Investigação086 excluída.
'''
emit(OUT / 'MEMORIA_DE_TRABALHO_085.md', memory+'\n'+link('Prova085',QNOTE)+'\n'+link('Primeira página geral',GNOTE)+'\n')
design = '''# Desenho do fechamento — adendo085

10/09/2026. [DERIVED/OPEN] Novo adendo de bancada; nenhum desenho canônico modificado.

O arco080–084 havia reduzido a liberdade do levantamento à imagem CE sobre o módulo quadrático e depois ao critério J_W=divV+K²f, f∈N^g. A etapa085 paga N^g=0. O canal residual é exclusivamente a divergência de uma corrente natural: J_W=divV.

Já excluído: V=c gradJ_W, por084. Ainda não decidido: todas as outras correntes de ordem finita. O próximo resultado precisa construir uma corrente admissível, ou excluir a imagem completa por um argumento que preserve as relações do módulo. Não basta um teste isolado, uma primitiva que saia da classe natural ou a palavra Pontryagin.

A generalização085 descreve s0 e o primeiro CE em todas as valências finitas, eliminando invariantes positivos em todo grau simétrico. Isso organiza também possíveis etapas seguintes, mas não paga s2,s3,... nem a equação mestra quântica. A nulidade do grau horizontal zero não decide o alvo de grau quatro.

Se houver cancelamento: recuperar a primitiva finita BRST, satisfazer admissibilidade causal e prosseguir nos levantamentos. Se houver obstrução: registrar o setor exato atingido, sem confundir falha desse levantamento com refutação universal da TGL. Permanecem os objetivos gerais de reconstrução dos mesmos dados, compatibilidade física e rota UV. Fase/ramo já pagos. Investigação086 separada.
'''
emit(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_085.md', design+'\n'+link('Prova085',QNOTE)+'\n'+link('Primeira página geral',GNOTE)+'\n')
assert before == [pin(path) for path in sources]
print(json.dumps({'report':pin(OUT/'REEXAME_SUFICIENCIA.md'),'root_review':review_pin},ensure_ascii=True))
