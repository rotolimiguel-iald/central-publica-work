from pathlib import Path
from datetime import datetime
import json,hashlib,os,sys
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'REEXAME_SUFICIENCIA_079_20260910'
doc=Path(sys.argv[1]).resolve()
gl=Path(sys.argv[2]).resolve()
assert doc.is_relative_to(ROOT) and doc.is_dir() and doc.name.startswith('REVISAO_DOCUMENTAL_RELATORIO_079')
assert gl.is_relative_to(ROOT) and gl.is_dir() and '079' in gl.name
def one_review(folder):
    paths=list(folder.glob('PARECER*.md'));assert len(paths)==1
    return paths[0]
dp,gp=one_review(doc),one_review(gl)
def link(p,label):return '['+label+'](<'+p.as_posix()+'>)'
created=[]
def new(p,s):
    p=p.resolve();assert p.is_relative_to(ROOT) and not p.exists()
    b=s.encode('utf-8');q=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with q.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    assert q.read_bytes()==b;q.rename(p);assert p.read_bytes()==b
    created.append(dict(path=p.as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
new(OUT/'ADENDO_REVISOES_079.md',"""# Adendo de revisões079

10/09/2026. [DERIVED — matemática escrita revisada] [REAL — 12 controles simbólicos e integridade documental].

A nota do sistema e da projeção sigma, de Singer, foi revisada por Herschel e pela raiz. As duas precisões necessárias receberam adendo autoral e confirmação independente: o núcleo é o ideal FECHADO por valência na completação, e o alvo Einstein conserva o anel de coeficientes herdado. Não se usa uma categoria menor nem uma recíproca não demonstrada.

O funcional ímpar e o cálculo quadrático são da raiz. Herschel leu integralmente nota, script e recibo e aprovou a prova e a implementação no alcance declarado. O manifesto da nota, criado antes do CAS, conserva a contagem histórica zero; o recibo posterior registra12 controles. A revisão foi estática, sem repetir o CAS. A entrada foi pinada antes dos cálculos e conferida depois. O registro inicial da revisão da raiz conserva o estado pendente daquele momento; o parecer independente posterior é a evidência efetivamente consumida nesta entrega.

A fatoração do subsetor puro em antifields, de Herschel, foi lida integralmente e revisada pela raiz. Turing conferiu apenas as identidades algébricas de símbolo; essa contribuição parcial não é apresentada como revisão integral. A raiz conferiu também as normalizações, a indução natural e a primitiva. O teorema exige o ciclo puro b4=Q=0; não elimina os antifields de correções mistas.

Os dois candidatos de Weyl, de Turing, foram revistos por Herschel e pela raiz. A exclusão vale para membros não nulos da família restrita ao teste. Não exclui b4=0 com outros Q/R nem coeficientes que se anulam neste fundo e não em outros. O teste tem C(p)³=0 e anulaA6; não substitui o detector ímpar de valência seis.

A comparação GL–ortogonal, de Singer, foi revisada pela raiz e no parecer independente:
"""+link(gp,'Revisão independente das conexões')+"""

O primeiro auxiliar de geração dessa nota continha um byte NUL e foi rejeitado pela análise sintática antes de executar. Uma cópia NOVA removeu somente esse byte, com proveniência medida; o auxiliar defeituoso foi preservado. A integridade documental de um arquivo histórico não significa aprovação de sua execução. Não houve rejeição de aprovação automática de uma ação nesta etapa.

A revisão documental do relatório, memória, desenho e captura é:
"""+link(dp,'Parecer documental079')+"""

As fontes e seus manifestos mantêm estados históricos anteriores às revisões; estas são registradas ao lado e não reescrevem aqueles bytes. Os novos auxiliares de captura/finalização têm cópia e substituições registradas em PROVENIENCIA_AUXILIARES_079.json.

Os12 controles matriciais não se somam aos122 da078 nem aos checks documentais. Não há nova compilação Lean, execução/importação de um.py, rito de natureza ou alteração de originais, Atlas, índice, memórias canônicas, selo ou gate. A investigação080 está excluída. −[A6]∈δ(Kcal), o setor interagente geral e o objetivo completo permanecem abertos.
""")
new(ROOT/'TUNEL/DO_CHATGPT/ENTREGA_079_ESPONTANEA_liberdade_de_correcao_e_funcional_impar.md',"""# Entrega079 — liberdade de correção e detector ímpar

10/09/2026. Para a sessão que codifica o um.py. [DERIVED — matemática escrita revisada] [REAL — 12 controles matriciais simbólicos].

Incorporar conjuntamente as notas, adendos e revisões do relatório:

1. Sistema de espécies E4/E5/E6 e condições s0b4=0, s0b5+s1b4=0, s0b6+s1b5=−r6. Conservar antifields, jatos e pareamentos pontuais.
2. Projeção sigma coeficiente a coeficiente, ideal FECHADO por valência, alvo Einstein com coeficientes herdados. Não substituir pelo fundoφ=id ou por anel menor.
3. Funcional L_k da diferença entre h_k e h_−k: L_k(s0B)=0, L_k(A6)=−4k/z0 e L_k(s1(u*R))=0 para toda espécie u*C⁴. Logo qualquer solução precisa de Q métrico com L_k(s1 Q/2)=+4k/z0. Q=0 excluído; R continua possível no fechamento conjunto.
4. Subsetor puro fechado u*C⁴ com b4=Q=0 é s0-exato por fatoração natural das identidades por Bianchi; primitivaχ5 e correção+s1χ5 especificadas.
5. Família não nula W1CCm/dual falha a equação de quinta valência: outro testeKilling dá−2/z0,+2k. Não classifica todosP; esse detector anulaA6.
6. CorrenteJ2 recebe completamento explícito na segunda equação, mas F(L) falha a primeira. τort−τGL=sB por homotopiaformal: mesma classeC5 já obstruída, não alternativa.

O cálculo Einstein quadrático passou12 controles, com revisão estática independente. No pontoF2=diag(3/4,−1/4,−1/4,−1/4); sua contribuição é eliminada por paridade, não por nulidade. ZeroLean novo.

O canônico permanecev338, quatro pins iguais078, 77/98 módulos acompanhados presentes e21 ausentes. A integração e a suficiência matemática geral são pendências distintas. Nenhum original foi executado/importado ou alterado.

"""+link(OUT/'REEXAME_SUFICIENCIA.md','Relatório completo')+'\n\n'+
link(OUT/'ADENDO_REVISOES_079.md','Revisões e precisões')+'\n\n'+
link(OUT/'MEMORIA_DE_TRABALHO_079.md','Memória da etapa')+'\n\n'+
link(OUT/'DESENHO_DO_FECHAMENTO_ADENDO_079.md','Desenho do caminho crítico')+'\n\n'+
link(OUT/'MANIFESTO_ENTREGA_079.json','Manifesto de integridade')+"""

Ainda falta decidir−[A6]∈δ(Kcal) para outras classes admissíveis, controlar a torre real e concluir anomalia/contratermos/QME, compatibilidades, reconstrução pelos mesmos dados e rotaUV. H3 interno, fase/ramo e falsificadores permanecem preservados. Investigação080 excluída.
""")
config={
'source_directories':[
'LIBERDADE_DE_LEVANTAMENTO_079_20260910',
'REVISAO_LIBERDADE_LEVANTAMENTO_079_20260910_040031_574533',
'SUBSETOR_ANTIFIELD_PURO_079_20260910_041018_659161',
'FUNCIONAL_IMPAR_TT_079_20260910',
'CONTROLE_EINSTEIN_QUADRATICO_079_20260910',
'REVISAO_FUNCIONAL_IMPAR_TT_079_20260910_041719_325801',
'CANDIDATOS_WEYL_E_OBSTRUCAO_079_20260910_041607_7604358',
'REVISAO_CANDIDATOS_WEYL_079_20260910_042539_816261',
'COMPLETAMENTO_GL_ORTOGONAL_079_20260910',
gl.name,'REVISOES_RAIZ_079_20260910',doc.name],
'new_cas_controls':12,'new_lean_compilations':0,
'status':'LOWER_CORRECTION_SYSTEM_TYPED__ODD_DETECTOR_REQUIRES_METRIC_QUADRATIC_PART__PURE_ANTIFIELD_AND_WEYL_FAMILIES_CONTROLLED__FULL_LIFT_OPEN',
'written_results':[
'Complete ghost3 species through valence6 and local correction equations, with sigma projection onto inherited coefficients and closed ideal in the completion.',
'Odd TT evaluation annihilates all direct physical-antifield contributions to s1b5, preserves A6 and imposes a nonzero necessary condition on the metric quadratic correction Q.',
'12 exact symbolic matrix controls establish full-function parity of quadratic Einstein and metric-density source; independent static review, no rerun.',
'Natural finite factorization through Bianchi makes every isolated closed pure-antifield b5 exact on the Einstein/constant-sigma reference.',
'Nonzero members of the two Weyl-CCm candidate family fail the valence5 completion equation, including arbitrary finite-jet antifield corrections.',
'Explicit GL quadratic-current completion and formal transgression homotopy show GL and orthogonal descriptions represent the same obstructed C5 class.'
],
'remaining':[
'Exhaustive admissible classification/reduction of other P,Q and mixed corrections; decide whether minus[A6] is in delta(kernel(H3(C5)->H3(C3))).',
'Actual truncation cohomology, inverse-limit comparison and other anomaly-criterion channels.',
'Admissible anomaly primitive, causal counterterms, interacting current/charge and QME.',
'Compatible references, states and cutoffs; general gravitational reconstruction from the same selected data; justification of the UV route.',
'Canonical integration and appropriate formal verification of approved written constructions and missing tracked modules.'
],
'limits':'Classical minimal finite-jet cochains on the declared constant-sigma Einstein test; coefficient completion and inherited ring preserved. Odd detector does not remove antifields from mixed closure equations. Two Weyl candidates are not classified as exhaustive. GL homotopy preserves a class, not a new solution. No full delta(kernel) verdict, no anomaly removal or QME. 12 symbolic matrix checks and documentary checks have different scopes; no independent CAS rerun, Lean, um execution/import, nature test, original/memory edit or gate change. Stage080 excluded.'
}
new(OUT/'CONFIG_ENTREGA_079.json',json.dumps(config,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(created,ensure_ascii=True))

