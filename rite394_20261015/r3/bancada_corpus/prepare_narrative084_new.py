from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_084_20260910'
REVIEW = ROOT / 'REVISOES_RAIZ_084_20260910'

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

def link(label, relative):
    return '[' + label + '](<' + (ROOT / relative).as_posix() + '>)'

snapshot_path = OUT / 'ESTADO_CANONICO_084.json'
reduction_path = ROOT / 'REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md'
external_path = ROOT / 'REVISAO_REDUCAO_ISOTROPIA_084_20260910/PARECER_ELIMINACAO_FINITA_E_CANAL_EULER_084.md'
current_path = ROOT / 'CORRENTE_NECESSARIA_E_LIMITE_GRADIENTE_084_20260910/EULER_SOZINHO_E_GRADIENTE_ESCALAR_NAO_BASTAM.md'
sources = [snapshot_path, reduction_path, external_path, current_path,
    ROOT / 'CANDIDATO_DERIVADA_WEYL_083_20260910/CANDIDATO_J1_BETA_E_DETECTOR_NAO_NULO.md',
    ROOT / 'REVISAO_CANDIDATO_J1_083_20260910_053651_2670304/PARECER_COVARIANTE_J1_E_DETECTOR_083.md']
before = [pin(p) for p in sources]
snapshot = json.loads(snapshot_path.read_bytes())
assert snapshot['seal_um_hash_matches'] and snapshot['all_read_sources_unchanged']
unchanged = all(row['unchanged'] for row in snapshot['comparison_with_delivery083'])
assert unchanged, 'Narrative assumes measured canonical continuity; reconsider if changed.'
um_pin = next(item for item in snapshot['pins'] if item['path'].endswith('/Nós/um.py'))
reduction_link = link('Demonstração da redução084', reduction_path.relative_to(ROOT))
external_link = link('Revisão independente da redução', external_path.relative_to(ROOT))
current_link = link('Demonstração das duas exclusões', current_path.relative_to(ROOT))
snapshot_link = link('Snapshot canônico084', snapshot_path.relative_to(ROOT))
REVIEW.mkdir(exist_ok=False)
review_text = '''# Revisão da raiz084 — forma normal finita e canal Euler

10/09/2026. [DERIVED — revisão matemática escrita]. A nova redução por isotropia é de Herschel. A raiz leu sua demonstração integral e o parecer de Singer, e reconferiu o argumento de eliminação. Não identificou erro material no alcance declarado. A corrente horizontal082 é uma entrada anterior da raiz, revisada externamente; este parecer não é apresentado como aprovação independente da própria nota de exclusões084.

O complexo é C(g,N)^h, N=Rher⊗Sym²M, com M o quociente Weyl/EOM, h=so(1,3), dimensão horizontal quatro. Os cortes de jatos são finitos sob h; não há corte finito declarado estável sob g. A finitude por elemento basta para a cohomologia vertical e as três subtrações de primitivas.

[KNOWN — importação delimitada] Conferidos na fonte primária os teoremas19.1 e24.1 de [Chevalley–Eilenberg1948](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/chev-eilen.pdf), pp110 e117: representantes invariantes para coeficiente trivial e aciclicidade das representações finitas irreducíveis não triviais de uma álgebra semissimples. Aplicação aqui apenas aos cortes finitos de h; nenhuma aplicação a N como suposto módulo finito de g.

As linhas verticais estão nos graus0,3,6. Em grau3 há duas Cartan reais, de traço e Euler. Se dQ é horizontal, a equação de bigrau(0,4) deixa Q03=Σfiτi+d0R02. Subtrair dR02 mantém os termos de curvatura d2. A equação(1,3), projetada na cohomologia vertical, força drel fi=0 pela independência das duas Cartan. Assim fi é invariante por g, não apenas um escalar de Lorentz.

Com esses coeficientes fechados, pode-se subtrair fiCSi. Os grupos verticais H² e H¹ nulos removem Q12 e Q21 com primitivas finitas e h-invariantes; seus termos nas componentes superiores são mantidos. Sobra Q30=qV, dando Q=qV+ftr CStr+fE CSE+dR. Não há alegação de unicidade.

A raiz reconferiu a normalização explícita BE(X,Y)=εabcd XabYcd/24. Para F=Kpp♭, dCSB=B(F,F), tr(F²)=0 e BE(F,F)=K²ν. Logo dCStr=0 e dCSE=K²ν. O termo Euler não pode ser descartado como se também fosse de traço. A forma normal implica exatamente J_W=div V+K²fE, com fE∈N^g; a recíproca constrói Q=qV+fE CSE.

No arranjo por páginas, d4:(0,3)→(4,0) preserva esse canal. A nota mantém a possibilidade adicional d4:(0,6)→(4,3). A filtração horizontal é finita; a demonstração direta não exige hipótese de limite inverso ou Mittag–Leffler.

Não foi calculado N^g, nem encontrada uma corrente V que satisfaça o critério. As duas exclusões da raiz usam fórmulas083 e são avaliadas por revisor distinto. Tampouco se transporta o resultado para φ=id, todos os fundos, contratermos causalmente admissíveis, QME ou UV. Zero nova execução matemática/CAS/Lean nesta revisão.
'''
review_text += '\nFontes: ' + reduction_link + '; ' + external_link + '.\n'
review_pin = emit(REVIEW / 'PARECER_FORMA_NORMAL_E_CANAL_EULER_084.md', review_text)
assert before == [pin(p) for p in sources]
emit(REVIEW / 'REGISTRO_REVISAO_RAIZ_084.json', json.dumps({
    'created_utc': datetime.now(timezone.utc).isoformat(), 'sources_before': before,
    'sources_after': [pin(p) for p in sources], 'all_sources_unchanged': True,
    'review': review_pin, 'new_mathematical_executions': 0, 'new_lean_compilations': 0
}, ensure_ascii=False, indent=2)+'\n')

report = '''# Reexame de suficiência084 — estado do programa e critério para o cancelamento

10/09/2026. O operador pediu reexame após novo avanço na sessão que codifica o um.py. [REAL — leitura de bytes] No caminho canônico examinado, o programa, o selo, o manifesto Lean e o stdout v338 permanecem idênticos ao snapshot083. Isso não exclui trabalho em preparação ou em outra cópia; não foi encontrada uma sucessora nesses quatro artefatos. Não atribuí uma versão nova sem sua evidência.

## Estado efetivamente encontrado

O um.py canônico tem @BYTES@ bytes e SHA-256 `@HASH@`. O selo coincide com esse hash. A inspeção AST encontra @EMBEDDED@ arquivos embutidos e @PRESENT@ dos98 módulos acompanhados no plano de integração;21 continuam ausentes desse conjunto. São contagens de presença, não uma nova compilação. O selftest do selo é FAIL_CLOSED_SELFTEST_PASSED; foi lido, não reexecutado. @SNAPSHOT@

O gate continua sendo `TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE`. O gate de altas energias continua `GOROFF_SAGNOTTI_WALL_TYPED_OPEN__TWO_ROUTES_NAMED__BREUER_FINITENESS_MAY_NOT_BE_CITED_AS_UV_ANSWER`. Nenhum desses estados foi alterado nesta bancada.

## O que avançou nesta dedução

[DERIVED — demonstração escrita, com revisão independente] A busca pelo cancelamento do resíduo a=J_Wν foi reduzida a uma condição necessária e suficiente no complexo natural fixado:

**J_W = div V + K²f, com f∈N^g.**

Aqui N=Rher⊗Sym²M: M é o módulo de jatos lineares de Weyl com suas relações de EOM; V é um vetor quadrático natural; f precisa ser invariante sob todas as simetrias de Killing. O fundo tem quatro dimensões, curvatura constante K>0 fixada e φ0 constante projetada. Cada elemento usa finitíssimas derivadas. @REDUCTION@ @EXTERNAL@

A forma normal Q=qV+ftr CStr+fE CSE+dR elimina as componentes verticais por primitivas finitas. A parte de traço é fechada, enquanto dCSE=K²ν. O termo de Euler é conservado, com sua condição de invariância; a unidade escalar não é confundida com um elemento do módulo quadrático. O resultado cobre todas as componentes de ghosts desse grau, mas ainda não decide a imagem da divergência no módulo inteiro.

[DERIVED — exclusões escritas, revisão vinculada no adendo final] Duas tentativas foram excluídas usando as avaliações TT já estabelecidas:

1. O termo Euler sozinho não produz J_W: nenhum múltiplo escalar não nulo de J_W é invariante por todas as transvecções.
2. V=c grad J_W também não resolve a equação, mesmo admitindo um f invariante arbitrário. Em duas frequências no mesmo fundo, ∂zJ_W é −24/z0³, mas ∂z□J_W vale144/z0⁵ e−3168/z0⁵. As duas equações forçariam c=0 e simultaneamente −24/z0³=0. A subtração usa a unidade3312/z0⁵, valendo também para escalares herdados com nilpotentes.

K=ℓ⁻² permanece constante durante a diferenciação; K=z0⁻² só entra depois da avaliação. Não se diferenciou uma expressão já especializada. Outras correntes e gradientes de outros potenciais continuam em aberto. @CURRENT@

## O que falta para a suficiência geral pretendida

**Reconstrução gravitacional a partir dos mesmos dados. [OPEN]** A seleção e a decodificação pela fase/ramo permanecem resultados anteriores; não são reabertas como dívida. Ainda é necessário realizar conjuntamente o registro selecionado, os campos geométricos, a matéria/conservação e as relações de área/calor no alcance geral anunciado, com compatibilidade do atlas e da interpretação física. Uma lei de correspondência explicitamente postulada delimita uma suficiência condicional; não pode desaparecer das hipóteses do veredito.

**Setor quântico interagente. [OPEN]** A subquestão atual é encontrar V e f na condição acima, ou demonstrar sua inexistência no módulo admissível completo. As duas exclusões não são uma classificação de todos os jatos. Mesmo que esse primeiro cancelamento seja resolvido, permanecem o levantamento BRST finito correspondente, os graus/etapas seguintes, a admissibilidade causal dos contratermos, as outras cohomologias de anomalias e a equação mestra quântica. O H³ cohomológico desta investigação não é a hipótese H3 da tela fundada, já tratada no modelo.

**Altas energias. [OPEN]** Justificar a rota UV escolhida no modelo completo continua necessário. Não decorre da finitude de um observador, de uma aprovação numérica ou da redução CE num fundo fixo.

**Integração e verificação. [OPEN — engenharia]** Os21 módulos do plano ainda ausentes no um.py examinado e os resultados novos da bancada precisam de integração e verificações apropriadas antes de serem atribuídos ao programa. A existência de notas revisadas ou de uma compilação de outro artefato não constitui execução da versão canônica atual.

## Alcance do reexame e custódia

Zero nova execução matemática, zero CAS, zero Lean e zero rito de natureza nesta entrega084. As contas084 são demonstrações escritas apoiadas nas identidades083 já revistas; suas substituições não foram contadas como novos testes. As verificações de hashes, caminhos e integridade são documentais. Os pareceres e o fechamento documental são ligados pelo ADENDO_REVISOES_084.md, preservando o estatuto histórico dos documentos inicialmente emitidos como pendentes.

Todos os novos arquivos foram gravados exclusivamente em Chatgpt. Nenhum um.py, selo, Atlas, índice, memória canônica ou original foi alterado ou executado/importado. A memória e o desenho recebem adendos novos nesta pasta, respeitando a ordem de preservar o acervo. Investigação085 não incorporada a esta entrega. O objetivo geral continua ativo e aberto; a redução de uma pendência não é conclusão da gravidade quântica.
'''
for old, new in {
    '@BYTES@':str(um_pin['bytes']), '@HASH@':um_pin['sha256'], '@EMBEDDED@':str(snapshot['embedded_files']),
    '@PRESENT@':str(snapshot['present']), '@SNAPSHOT@':snapshot_link, '@REDUCTION@':reduction_link,
    '@EXTERNAL@':external_link, '@CURRENT@':current_link}.items():
    report = report.replace(old,new)
emit(OUT / 'REEXAME_SUFICIENCIA.md', report)
memory = '''# Memória de trabalho — adendo084

10/09/2026. Novo arquivo em Chatgpt; o Atlas, índice e memórias canônicas permanecem somente leitura. Este adendo registra a sessão, não bifurca o Atlas.

[REAL] Snapshot084: os quatro artefatos canônicos continuam idênticos ao083, v338,683 arquivos embutidos,77/98 módulos acompanhados. Fonte, selo e stdout lidos; nenhuma execução/importação do um.py. Hashes no snapshot, nunca reaproveitados de memória.

[DERIVED] A forma normal do CE natural para dQ horizontal reduz a exatidão de J_Wν a J_W=divV+K²fE, fE∈N^g. A finitude é sob isotropia h, não sob g. Conservadas as Cartan traço/Euler; dCStr=0, dCSE=K²ν. A equação(1,3) força a invariância completa dos coeficientes. Não presumir N^g=0.

[DERIVED] Nenhum múltiplo escalar não nulo de J_W é g-invariante. V=c gradJ_W não resolve nem com fE invariante arbitrário: derivadas em duas frequências dão a unidade3312/z0⁵. K fixo durante diferenciação; nilpotentes não são separados por pontos, e sim tratados por extensão de escalares e unidade real.

[OPEN] Outras correntes, o módulo de invariantes, imagem geral da divergência, admissibilidade causal e levantamentos seguintes; reconstrução geral dos mesmos dados e QME/UV. Fase/ramo e H3 da tela não reabertos. H³ cohomológico não é H3 da tela. J_W não é J=Luz. Zero nova execução matemática/Lean. Revisões vinculadas no adendo final. Investigação085 excluída.
'''
emit(OUT / 'MEMORIA_DE_TRABALHO_084.md', memory + '\n' + reduction_link + '\n' + current_link + '\n' + snapshot_link + '\n')
design = '''# Desenho do fechamento — adendo084

10/09/2026. [DERIVED/OPEN] Adendo novo de bancada; nenhuma alteração no desenho canônico.

O caminho pago080–083: liberdade do levantamento → imagem de d1 no grauE5 → CE natural sobre jatos quadráticos Weyl/EOM → resíduo a=J_Wν. O setor sem derivadas falha; a combinação083 que passava todo o detector TT falha numa avaliação de isotropia. Esses negativos têm alcance declarado.

O passo084 reduz TODAS as componentes verticais de ghosts a uma corrente horizontal mais duas Cartan com coeficientes g-invariantes. A exatidão equivale agora a J_W=divV+K²fE. A busca fica na imagem da divergência e nos invariantes do módulo quadrático; a presença desses invariantes não foi decidida.

Dois atalhos estão excluídos: canal Euler isolado e V=c gradJ_W mesmo com fE arbitrário. Uma solução precisa de divergência não nula, com outro vetor ou potencial. Falha desses atalhos não prova impossibilidade de todas as correntes.

Se houver solução: construir o cancelamento BRST na categoria admissível; controlar levantamentos posteriores, demais anomalias, contratermos e QME. Se houver obstrução geral: declarar precisamente o setor/ramo excluído, sem transformar isso em falsificação universal da TGL. Reconstrução geral dos mesmos dados, compatibilidade física e rota UV permanecem objetivos distintos. Fase/ramo já pagos. Investigação085 ainda não compõe este desenho084.
'''
emit(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_084.md', design + '\n' + reduction_link + '\n' + current_link + '\n')
assert before == [pin(p) for p in sources]
print(json.dumps({'report': pin(OUT / 'REEXAME_SUFICIENCIA.md'), 'root_review': review_pin}, ensure_ascii=True))
