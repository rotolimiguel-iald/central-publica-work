from pathlib import Path
from datetime import datetime
import os,json,hashlib,sys
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'REEXAME_SUFICIENCIA_077_20260910'
doc=Path(sys.argv[1]).resolve()
ce=Path(sys.argv[2]).resolve()
assert doc.is_relative_to(ROOT) and doc.is_dir() and doc.name.startswith('REVISAO_DOCUMENTAL_RELATORIO_077')
assert ce.is_relative_to(ROOT) and ce.is_dir() and '077' in ce.name
def parecer(directory):
    files=list(directory.glob('PARECER*.md'));assert len(files)==1
    return files[0]
dp,cp=parecer(doc),parecer(ce)
created=[]
def link(p,label):return '['+label+'](<'+p.as_posix()+'>)'
def new(p,s):
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    b=s.encode();q=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with q.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert q.read_bytes()==b;q.rename(p);assert p.read_bytes()==b
    created.append({'path':p.as_posix(),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
new(OUT/'ADENDO_REVISOES_077.md',"""# Adendo de revisões077

10/09/2026. [DERIVED — matemática escrita revisada] [REAL — controles exatos/documentais].

A nota dos primeiros cortes, de Turing, deve ser consumida junto da errata Koszul–Tate. Herschel detectou o sinal incompatível com a ação escrita; o autor o corrigiu ao lado e o revisor aprovou o conjunto. O sinal correto é s0u*=+H0u; o segmento s0c*=+R0†u* permanece. A errata não altera os primeiros quocientes sem antifields, mas não pode ser omitida dos próximos cálculos.

A construção de Pontryagin atéC5, de Singer, foi lida integralmente e revisada pela raiz em parecer próprio. Seu dicionário posterior, também lido e revisado pela raiz, relaciona as matrizes por uma fórmula de blocos e fixa α3=−Cartan. A fonte mantém a indicação histórica de primeira transição em revisão; o parecer posterior e a errata pagam essa dependência na presente entrega.

O cálculo CE foi produzido pela raiz com aritmética racional. Sua revisão estática independente é:
"""+link(cp,'Parecer independente do controle CE')+"""

O nome de variável killing do script designa Tr₅(XY), proporcional à forma de Killing; é uma forma invariante não degenerada e não muda a linha cúbica. Os 420 controles são aritméticos finitos. Os números de checks dos recibos e do manifesto são documentais e não devem ser somados como provas da teoria completa.

O parecer documental dos três documentos da entrega é:
"""+link(dp,'Revisão documental do relatório, memória e desenho')+"""

As tentativas de execução que falharam permanecem descritas na leitura do controle CE: biblioteca ausente; bloqueio de rede no ambiente restrito; leitura incompleta do pacote sob restrição. A execução final autorizada passou. Nenhuma dessas falhas foi apresentada como sucesso, e nenhuma rejeição de revisão automática de aprovação ocorreu. Pacotes e temporários foram criados somente na nova pasta de dependências em Chatgpt, sem alterar instalações existentes.

Precisões permanentes: referência simétrica é teste local, não um estado Hadamard físico construído aqui; valência5 não é grau total5; A6 difere do resíduo do truncamento por s0α6. Uma transição não sobrejetiva não prova lim¹ não nulo; a finitude de C3 controla somente as imagens nesse alvo fixo.

Nenhum resultado078 é incorporado. Originais, Atlas, índice e memórias canônicas continuam somente leitura. Zero um.py executado/importado, zero Lean e zero testes de natureza. Selo e gate intactos; objetivo completo aberto.
""")
new(ROOT/'TUNEL/DO_CHATGPT/ENTREGA_077_ESPONTANEA_truncagens_BRST_e_levantamento_Pontryagin_C5.md',"""# Entrega077 — primeiros cortes e levantamento de Pontryagin

10/09/2026. Para a sessão que codifica o um.py. [DERIVED — matemática escrita revisada] [REAL — álgebra CE racional].

Incorporar com as notas, adendos e revisões:
1. Correção obrigatória da convenção: s0u*=+H0u e s0c*=+R0†u* na ação mínima escrita.
2. No teste local natural com g0 de curvatura constante não nula e φ0 constante: W=V⊕Λ²V, invariantes de graus2/3/4 com dimensões0/4/3, H³(C3)=4, imagem desdeC4 com dimensão1 e H⁴(C4)=0.
3. Não presumir sobrejetividade cohomológica universal: os quatro controles regulares estendem-se antes de restringir ao teste.
4. Construção T≤5 da transgressão de Pontryagin, ciclo não trivial emC5. O dicionário matricial dá α3=−Cartan e a imagem C5→C3 tem dimensão1.
5. A_P começa emF6 por trR²=trWeyl² e Weyl0=0. O resíduo truncado é A6−s0α6; sua classe não foi decidida.

Há 420 controles racionais nas três assinaturas, com revisão estática independente. Não há nova compilaçãoLean. Não converter esses resultados em H³ completo, estabilização de todos os cortes, lim¹ nulo, anomalia removida ou QME. Preservar a diferença entre valência e grau total.

O canônico recapturado permanece v338, com quatro pins iguais076; 77/98 módulos acompanhados presentes, 21 ausentes. Nenhum original executado ou alterado.
"""+'\n\n'+link(OUT/'REEXAME_SUFICIENCIA.md','Relatório completo')+'\n\n'+
link(OUT/'ADENDO_REVISOES_077.md','Revisões e precisões')+'\n\n'+
link(OUT/'MEMORIA_DE_TRABALHO_077.md','Memória da etapa')+'\n\n'+
link(OUT/'DESENHO_DO_FECHAMENTO_ADENDO_077.md','Desenho do caminho crítico')+'\n\n'+
link(OUT/'MANIFESTO_ENTREGA_077.json','Manifesto de integridade')+"""

O objetivo geral ainda inclui reconstrução pelos mesmos dados selecionados, compatibilidades e rotaUV. Fase, ramo, H3 interno e falsificadores existentes são preservados. A investigação078 posterior fica fora desta entrega.
""")
new(OUT/'CONFIG_ENTREGA_077.json',json.dumps({
'source_directories':[
'PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771',
'REVISAO_PRIMEIROS_TRUNCAMENTOS_077_20260910_031524_472175',
'ALGEBRA_EXTERIOR_CE_077_20260910_EXECUCAO_02',
'SOBREVIVENTE_PONTRYAGIN_077_20260910',
'REVISOES_RAIZ_077_20260910',
ce.name,doc.name],
'new_cas_controls':420,'new_lean_compilations':0,
'status':'FIRST_NATURAL_BRST_TRANSITION_COMPUTED__PONTRYAGIN_LIFT_THROUGH_VALENCE5__FULL_COMPLETION_AND_ANOMALY_OPEN',
'written_results':[
'Corrected linear BV convention, Killing-jet quotient and first natural truncation groups on constant-curvature reference.',
'Finite rational CE controls in three signatures, with 420 arithmetic checks and separate static review.',
'Regular universal controls refute automatic cohomology surjectivity at the first transition in the category admitting the test.',
'Explicit natural Pontryagin lift through C5; cubic identified with minus Cartan by a matrix-block dictionary.',
'Full transgression residual starts in valence6 by the Weyl identity; truncated residual distinguished from the full one.'
],
'remaining':[
'Admissible correction at valence6 and later orders, including freedom of lower corrections and antifields.',
'All relevant truncation cohomology and stabilized images; inverse-limit comparison and remaining E2 channels.',
'Complete anomaly primitive, causal counterterms, interacting charge/current and QME.',
'Compatible references, states, cutoffs; general gravitational reconstruction from the same selected data; UV route.',
'Canonical integration and appropriate formal verification of written constructions and missing modules.'
],
'limits':'Local minimal classical jet test, not a new physical Hadamard sector. Valence5 is not anomaly total degree5. Finite CE arithmetic is not full BRST cohomology; no lim1 verdict. No Lean or nature tests, no um execution/import, no original or canonical memory edits, no gate modification. Stage078 excluded.'
},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(created,ensure_ascii=True))

