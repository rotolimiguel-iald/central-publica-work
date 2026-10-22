from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_075_20260910'
REV = ROOT / 'REVISOES_RAIZ_075_20260910'
assert not REV.exists()
REV.mkdir()
pins = []

def pin(path):
    data = path.read_bytes()
    item = {'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    pins.append(item)
    return item

def new(path, content):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    data = content.encode('utf-8')
    assert data
    temporary = path.with_name(path.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temporary.read_bytes() == data
    temporary.rename(path)
    assert path.read_bytes() == data
    return pin(path)

def link(relative, label):
    return '[' + label + '](<' + (ROOT / relative).as_posix() + '>)'

sources = [
    'DESCIDA_NATURAL_SIMBOLOS_075_20260910/DESCIDA_NATURAL_POR_OPERADORES.md',
    'DESCIDA_NATURAL_SIMBOLOS_075_20260910/ADENDO_PRIMEIRO_DESCENDENTE_E_COMPOSICAO_075.md',
    'AUDITORIA_DESCIDA_NATURAL_075_20260910/SIMBOLOS_GRASSMANN_E_PRIMEIRO_DESCENDENTE.md',
    'REVISAO_DESCIDA_E_REES_075_20260910/PARECER_INDEPENDENTE_DESCIDA_E_REES.md',
    'APLICACAO_DESCIDA_OFFSHELL_075_20260910_022420_157704/APLICACAO_OFFSHELL_E_FONTES_CENTRAIS.md',
    'COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md',
    'CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md',
    'COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md',
]
for relative in sources:
    pin(ROOT / relative)

review_descent = r"""# Revisão da raiz: descida natural075

10/09/2026. [DERIVED — revisão matemática escrita]. Li integralmente a prova por operadores, a auditoria Grassmann/topforma, o adendo de composição e o parecer independente de Turing. Nenhum dos quatro textos foi alterado. A conclusão é favorável na categoria declarada.

A identidade de símbolos δh+hδ=(r+n−q)I é correta: o grau polinomial p fornece r, e a contração nas formas fornece n−q. A variação é par, e seus argumentos v são novos geradores livres de mesma paridade dos Z. A comparação de símbolos ocorre antes de v=Z, evitando cancelamentos espúrios na álgebra de Grassmann. Quantizar o símbolo por conexões naturais independentes de Z retira a ordem superior; derivadas dos coeficientes e curvatura permanecem no resíduo. A indução termina pela ordem em v, ainda que aumente finitamente a ordem nos coeficientes.

Em q<n, o residual de ordem zero desaparece; em q=0, a identidade força a própria entrada de ghost positivo a zero. A avaliação final v=Z é um mapa diferencial e produz N_Z vezes a forma. Dividir por N_Z>0 dá a primitiva natural. O enunciado exclui coeficientes ocultos de ghost positivo sem jatos livres.

Para q=n, a prova requer Euler_Z(F)=0, fornecido pela exatidão ordinária inicial ou diretamente pela nulidade do funcional sob todas as variações Z. A integração por partes covariante é finita e dá F_N=d_H(Θ_F[Z]/N). Isso não elimina a classe de Euler(g0), cujo N é zero. Com F=s a4 de ghost dois, paga-se o primeiro descendente; os passos q=3,2,1 e o caso zero completam Ω natural, com (s+d_H)Ω=0.

Na classe Rees, conexões dos fibrados normalizados de B0 têm valência zero. Variar retira uma perna Z e introduz v; substituir v=Z a repõe. Cada escolha horizontal conserva E,N,L e t^(E+2L−2), com entrada e saída no mesmo E. Intercalar s pode misturar E e N; exige-se que s preserve o espaço completo. A conclusão não é que toda a cadeia mantenha um N único. Essa precisão do parecer independente é incorporada.

O alcance é a apresentação métrica efetiva e os fibrados graduados especificados, não o ghost Lorentz cru de transformação afim. Naturalidade sob conexões fixadas por B0 não identifica a operação com a projeção normal de074, que falha em comutar com d_H.

[OPEN] Não há aqui primitiva total de Ω, nulidade de H¹,⁴(s|d_H), família de contratermos com T9/T11 e contatos, QME ou construção de carga interagente. Esta revisão aceita um passo construtivo de descida, não essas conclusões posteriores.

As fontes primárias de contexto foram conferidas: BBH2000, teoremas4.1–4.2, para a distinção entre divergência e operador Euler; Arnold, §3.2, para a estrutura de Koszul. O denominador particular r+n−q e a naturalidade acima foram conferidos diretamente, sem importar por homonímia a graduação diferente de Arnold.

[BBH2000](https://arxiv.org/pdf/hep-th/0002245v3). [Arnold](https://www-users.cse.umn.edu/~arnold/papers/fe-families.pdf).

Zero compilação Lean/CAS ou cálculo de diagramas nesta revisão. Os pins medidos acompanham o registro.
"""
review_application = r"""# Revisão da raiz: aplicação relativa off-shell075

10/09/2026. [DERIVED — auditoria escrita] [KNOWN — importação delimitada]. Li integralmente a nota de aplicação de Herschel e confrontei seu argumento com as notas causais069/072 já lidas. Conferi diretamente Fröb1803.10235v3, teorema7 e sua prova, eqs.137–139 e a distinção anterior A0/I0.

O termo “off-shell” é corretamente atribuído aos argumentos dinâmicos F: a consistência antecede o quociente pelas equações livres. Antifields centrais continuam argumentos polinomiais e não são avaliados em zero. O teorema primário não fornece sozinho a existência de todos os produtos causais do nosso modelo: a aplicação consome o contrato explícito de069/072.

A estabilidade sob relações apenas de B0 é suficiente para a descida relativa. Seja J ideal diferencial dos coeficientes de ghost zero. Variação em Z preserva J, assim como contrações/símbolos, multiplicação pelas conexões, derivadas horizontais, quantização e avaliação v=Z. A identidade de Koszul é válida sobre o anel quociente e divide apenas por inteiros positivos invertíveis. Os jatos v permanecem livres sobre esse anel. Não é preciso que B0 possua jatos irrestritos para esse argumento; é indispensável que J não imponha relações a Z.

A primeira consistência, na região de cutoffs constantes, dá s_ext A_N=0 no nível funcional. Variações compactamente suportadas em todos os Z anulam seus operadores Euler. O complemento de topforma075 fornece a corrente natural diretamente, sem precisar elevar uma corrente coordenada a dado natural. Na ordem de ħ, a inserção de anomalia em anomalia é pelo menos N+1; a nota corretamente não presume 2N sem controle das inserções polarizadas inferiores.

Conferi as três rotas das fontes positivas: incluir ω com seus jatos livres em Z; restringir θ=ω=0 por mapa de complexos; ou, após desfazer o gauge no domínio da retração072, usar B→Φ e Ω→sΦ. A terceira exige seu controle de completação próprio. Não foram acrescentados conjugados B*,Ω* à álgebra de inserções. “Central” não significa “horizontalmente constante”.

A preservação de multigraus pela homotopia horizontal não recategoriza os tadpoles t⁻¹θ como elementos de R_L. Na teoria sem fontes, o resultado Rees se aplica diretamente; na extensão, vale a filtração Laurent efetivamente declarada. Termos dχ de cutoff permanecem presentes ao testar densidades.

Parecer favorável à aplicação RELATIVA na categoria causal admitida. A expressão “universal” dos textos iniciais075 deve ser lida, para esse consumo, como identidade nos jatos dinâmicos livres sobre os coeficientes admissíveis. Não resulta uma identidade em todos os jatos livres de B0. Essa distinção não é editorial: a cohomologia total e os grupos E2 que se pretende usar depois precisam ser calculados nessa categoria, ou acompanhados de um teorema de levantamento.

[OPEN] Permanecem primitiva total, admissibilidade de sua remoção, acordo perturbativo entre T_B e T_ref, corrente/carga/QME, e existência analítica fora do domínio causal já admitido. Esta auditoria não refez toda a construção analítica Q2.

[Fröb, fonte primária](https://arxiv.org/pdf/1803.10235v3). Nenhum original alterado; zero CAS/Lean novos.
"""
new(REV / 'PARECER_DESCIDA_NATURAL_075.md', review_descent)
new(REV / 'PARECER_APLICACAO_RELATIVA_075.md', review_application)
for item in pins:
    raw = Path(item['path']).read_bytes()
    assert len(raw) == item['bytes'] and hashlib.sha256(raw).hexdigest() == item['sha256']
new(REV / 'REGISTRO_REVISOES_RAIZ_075.json', json.dumps({
    'status':'WRITTEN_REVIEW_FAVORABLE_WITH_EXPLICIT_SCOPE',
    'created_utc':datetime.now(timezone.utc).isoformat(),
    'files':list(pins),'sources_stable':True,'originals_written':False,
    'new_lean_compilations':0,'new_cas_controls':0
}, ensure_ascii=False, indent=2) + '\n')

snapshot = json.loads((OUT / 'ESTADO_CANONICO_075.json').read_bytes())
assert snapshot['seal_um_hash_matches']
assert all(p['unchanged'] for p in snapshot['comparison_with_delivery074'])
um_pin = next(p for p in snapshot['pins'] if p['path'].endswith('/Nós/um.py'))
report = """# Reexame de suficiência — entrega075

10/09/2026. [REAL — arquivos conferidos] [DERIVED — demonstrações escritas] [KNOWN — importações delimitadas].

**A pendência encolheu: a descida da anomalia pode ser construída dentro da classe natural do esquema causal declarado. Ainda falta construir a primitiva que permitiria removê-la.** O canônico continua na versão v338 encontrada na última entrega; os avanços desta etapa estão documentados na bancada Chatgpt.

"""
report += "A " + link('REEXAME_SUFICIENCIA_075_20260910/ESTADO_CANONICO_075.json','captura atual') + f" comparou quatro artefatos canônicos com a entrega074: todos conservaram seus bytes. O um.py tem {um_pin['bytes']:,} bytes, {snapshot['embedded_files']} arquivos embutidos e selo correspondente. No conjunto de 98 módulos do integrador anterior, {snapshot['present']} estão presentes e {len(snapshot['absent'])} continuam ausentes. Essa contagem mede aquele conjunto delimitado; não mede toda a prova.\n\n"
report += """O programa não foi executado ou importado. A evidência de rodada anterior foi lida. Não houve Lean, CAS, cálculo de diagramas ou novos testes de natureza nesta etapa. Nenhum arquivo original, Atlas, índice, memória canônica ou gate foi alterado.

## O que ficou demonstrado nesta etapa

Na apresentação métrica e nos fibrados graduados declarados, os ghosts e antifields de ghost não zero têm jatos livres. Linearizar uma forma fechada em variações independentes permite resolver seu símbolo principal por uma identidade algébrica de Koszul. A quantização covariante desse símbolo reduz a ordem do operador; derivadas dos coeficientes e curvaturas permanecem no resíduo. Ao final, a identidade de Euler fornece a primitiva natural nos graus de forma menores que quatro.

O primeiro passo, que envolve uma topforma, usa outro antecedente: a consistência da anomalia implica a nulidade dos operadores Euler dessa topforma. Integração por partes covariante fornece então o primeiro descendente. Com os passos restantes obtemos

\\[
\\Omega=a_4^1+a_3^2+a_2^3+a_1^4+a_0^5,
\\qquad (s+d_H)\\Omega=0.
\\]

"""
report += "A demonstração está na " + link(sources[0],'nota de operadores') + ", completada pelo " + link(sources[1],'adendo do primeiro descendente') + " e pelo " + link(sources[3],'parecer independente') + ". Os operadores horizontais preservam laço, valência e o peso de Rees por componente quando suas conexões são as dos fibrados fixados por B0. Intercalar s pode misturar valências; a classe completa deve continuar preservada.\n\n"
report += """A aplicação ao modelo causal foi conferida separadamente. A consistência vale antes de impor as equações aos argumentos dinâmicos. O fundo B0 pode continuar restrito às referências admitidas: a descida preserva um ideal diferencial que contenha relações apenas desses coeficientes. Os jatos de ghosts e antifields precisam permanecer livres. Fontes centrais positivas como ω devem entrar entre esses geradores, ou ser retiradas por uma projeção compatível.

"""
report += "A " + link(sources[4],'auditoria de aplicação') + " e a " + link('REVISOES_RAIZ_075_20260910/PARECER_APLICACAO_RELATIVA_075.md','revisão da raiz') + " explicitam essa conclusão relativa. A consistência off-shell usada na importação está no [teorema7 de Fröb](https://arxiv.org/pdf/1803.10235v3). Isso não estende automaticamente a identidade a fundos arbitrários nem resolve a cohomologia total.\n\n"
report += """## O que ainda falta

| Obrigação | Estado após esta etapa |
|---|---|
| Remover a anomalia na classe admissível | [OPEN] Construir a primitiva total de Ω. A descida fornece um cociclo fechado; sua exatidão continua por demonstrar. |
| Completar o cálculo cohomológico necessário | [OPEN] Controlar H¹(s), H²(s), H⁵(s) e os canais H¹(Ebar_N;H⁴(s)), H²(Ebar_N;H³(s)) na mesma classe natural formal e na categoria de B0 realmente usada. São condições suficientes da rota074; não se declarou uma anomalia não nula. H³ aqui é cohomologia BRST, não a antiga hipótese H3 de horizonte. |
| Transformar a primitiva em normalização causal | [OPEN] Preservar regularidade, escala por aridade, realidade, independência funcional, inserções e contatos em toda a família de contratermos. Uma corrente ou densidade isolada não fornece essa família. |
| Fechar o setor quântico interagente | [OPEN] Construir corrente/carga renormalizadas, implementação do diferencial, nilpotência e QME no domínio comum; depois consumir o resultado condicional de positividade. P0 no setor livre declarado permanece preservado. |
| Compatibilidade entre referências | [OPEN] Acordo perturbativo e identificação dos esquemas, estados e cutoffs no alcance pretendido. A descida relativa não paga independência quântica geral de fundo. |
| Reconstrução gravitacional geral | [OPEN] Fornecer pelos mesmos dados TGL selecionados os objetos e relações exigidos pelo teorema geral, ou assumir explicitamente uma lei de correspondência e manter a suficiência condicionada a ela. As construções particulares permanecem válidas no alcance já demonstrado. |
| Altas energias | [OPEN] Justificar a rota UV escolhida. O próprio selo canônico mantém aberta a parede de renormalização; finitude de Breuer não foi aceita como resposta automática. |
| Integração verificável | [OPEN] Incorporar e verificar no um.py os materiais aprovados e módulos ainda ausentes. Nota escrita e presença no código não equivalem a compilação auditada. |

Fase complexa e distinção de ramo, H3 interno e falsificadores já existentes não são reabertos. A suficiência pretendida pode usar resultados importados com hipóteses verificadas; não exige refazer a literatura. Exige, porém, demonstrar que as importações e construções pertencem à mesma classe do modelo que as consome.

## Encaminhamento para a sessão que codifica

Incorporar o teorema de descida junto com o complemento de topforma, a precisão de graus e a aplicação relativa. O estatuto é [DERIVED — demonstração escrita revisada], até a verificação formal pertinente. Não criar uma bandeira de remoção da anomalia ou QME com base apenas em (s+d_H)Ω=0.

O próximo alvo matemático é a primitiva total na categoria correta. Investigações posteriores sobre representantes de H³/H⁴ pertencem à etapa076 e não integram o resultado certificado desta entrega.

"""
report += "As revisões matemáticas estão em " + link('REVISOES_RAIZ_075_20260910/PARECER_DESCIDA_NATURAL_075.md','parecer de descida') + " e no parecer de aplicação já ligado acima. A " + link('REEXAME_SUFICIENCIA_074_20260910/REEXAME_SUFICIENCIA.md','entrega074') + " conserva o histórico do termo de curvatura e do critério total. O objetivo geral permanece em aberto; a entrega075 não declara gravidade quântica resolvida ou confirmada.\n"
new(OUT / 'REEXAME_SUFICIENCIA.md', report)
new(OUT / 'MEMORIA_DE_TRABALHO_075.md', """# Memória de trabalho075 — adendo novo da bancada

10/09/2026. Todas as fontes canônicas continuam somente leitura. Este arquivo registra a etapa da bancada; não copia nem bifurca o Atlas.

[REAL] A captura075 manteve os quatro pins canônicos da074 e verificou o selo correspondente. A leitura AST mede presença no conjunto do integrador; nenhuma execução do um.py.

[DERIVED] Desc ida natural, escrita corretamente como descida natural: linearização par em jatos livres Z; identidade δh+hδ=(r+n−q)I; quantização covariante e indução na ordem do operador; avaliação Euler com N>0. Topforma requer operadores Euler nulos, fornecidos pela consistência off-shell. A cadeia natural Ω é fechada para s+d_H.

[DERIVED] As homotopias horizontais conservam E,N,L e peso Rees por componente em conexões B0; s pode misturar graus. Restrição diferencial somente dos coeficientes B0 é compatível com a prova. A aplicação relativa069/072 conta ω entre os jatos livres ou usa projeção compatível. Fontes Laurent conservam sua filtração própria.

[OPEN] Primitiva total e canais cohomológicos na categoria real; admissibilidade da família causal; corrente/carga e QME; acordo perturbativo; reconstrução geral pelos mesmos dados e rota UV; integração canônica. H3 interno, fase/ramo e falsificadores não são reabertos.

Revisões por leitores distintos dos autores foram concluídas nas frentes de composição e aplicação. Zero Lean/CAS/diagramas/natureza novos. Nenhum gate movido. O objetivo geral permanece ativo.

""" .replace('Desc ida natural, escrita corretamente como descida natural:', 'Descida natural:') + link('REEXAME_SUFICIENCIA_075_20260910/REEXAME_SUFICIENCIA.md','Relatório075') + '\n')
new(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_075.md', """# Desenho do fechamento — ADENDO075

10/09/2026. [DERIVED — avanço escrito].

Consistência ordinária off-shell na categoria causal
→ operadores Euler da topforma nulos
→ primeiro descendente natural por integração por partes
→ descida por símbolos em q<4
→ Ω natural, (s+d_H)Ω=0.

Esse trecho fica pago com seus antecedentes, inclusive sobre relações diferenciais exclusivas de B0. As conexões e a contagem de fontes devem ser as da aplicação efetiva.

O trecho seguinte continua aberto:
Ω fechado → primitiva total admissível → normalizações causais compatíveis → Ward/QME sem a quebra → carga interagente no domínio comum → consumo da positividade condicional.

O cálculo H(s)/E2 deve ocorrer na classe natural formal e na categoria de referência realmente usada. Um resultado global C∞ ou com B0 irrestrito precisa de comparação demonstrada antes de ser consumido.

Em paralelo continuam correspondência gravitacional geral a partir dos mesmos dados, compatibilidade de fundos e rota UV. Integração canônica é uma obrigação documental/formal distinta.

Não reabrir fase, ramo, H3 interno ou falsificadores. Não promover descida a remoção de anomalia. Originais e memórias canônicas intactos.

""" + link('REEXAME_SUFICIENCIA_075_20260910/REEXAME_SUFICIENCIA.md','Relatório e obrigações') + '\n')
print(json.dumps({'created':pins,'report':(OUT/'REEXAME_SUFICIENCIA.md').as_posix()},ensure_ascii=True))
