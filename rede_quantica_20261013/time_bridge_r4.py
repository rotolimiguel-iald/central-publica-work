"""Document a conditional phase-clock derivation from existing finite models."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

UNIT = 'F1.TEMPO.LEITURA_20261015'
OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019' / UNIT / 'PONTE_RELOGIO_R4'
reg.DEST = OUT
REPORT = OUT / 'DERIVACAO_CONDICIONAL_R4.txt'
RESULT = OUT / 'CONTRATO_RELOGIO_R4.json'

TEXT = r'''PRIMEIRA LEI -> RETORNO DE FASE -> RELOGIO
15/10/2026. Autor: codex-gerente-tgl. Unidade F1.TEMPO.LEITURA_20261015.
ESTATUTO: DERIVED condicional, demonstracao algebrica escrita; nao compilada em Lean.
Nenhum experimento, nova execucao cientifica, medicao de natureza ou alteracao canonica.

1. LEVANTAMENTO E REAPROVEITAMENTO
O Nos Vivo foi consultado para F1.TEMPO. Ja ha Santo, o relogio angular fiel
modulo periodo, a nao chegada finita ao posto e o motor da regra. O mapa
formal.tempo_santo_fluxo_e_dissipacao registra auditorias anteriores; nao repetidas.
A unidade filha nao estava indexada na consulta R3; nao se reconstruiu o grafo.
O artigo tgl_paper_unified.py:14441-14483 fornece o modelo de paridade/ligacao;
20029-20096 fornece o canal do espelho, distinguindo ramo seletivo e canal completo.
tgl_echo_smatrix.py:84-104 ja intercala U diagonal e o canal; w1=1.30 e dt=0.35
sao entradas daquele ensaio, nao valores derivados de uma escala universal.
um.py:170050-170068 liga a Primeira Lei a deflexao e c2->c3, com estatuto da fonte
ONTO + REAL na forma. Sua presenca textual nao fixa um suporte temporal avancado.
O selo lido nesta etapa e v393; leitura nao equivale a uma nova execucao do programa.

2. TIPOS E HIPOTESES NOMEADAS
H=complexos^2; X,Y,Z sao as matrizes de Pauli padrao.
Paridade Pi=Z; Hamiltoniano Hlig=-V0 X; V0>0; hbar>0; omega=V0/hbar.
Estado inicial rho0=|G><G|=(I+Y)/2, com |G>=(1,i)/sqrt(2).
H_ESPELHO_ESPECTRAL: P=(I+X)/2 e Q=(I-X)/2 sao os setores lidos pelo espelho.
Essa e uma hipotese ADICIONAL, explicitamente habitada. Nao e demonstrada pela
Primeira Lei e nao identifica automaticamente P com rho_star da fronteira canonica.
Pi, P e E(rho0) sao tres objetos distintos. Nao encadear os nomes 'paridade',
'projetor', 'graviton' ou 'atrator' sem os respectivos mapas.
H_PASSO: Delta_t>0 e a duracao atribuida a cada aplicacao do canal.
beta=ALPHA_FINE_CODATA_2018*sqrt(e), sempre expressao em runtime quando calculada.
As formulas abaixo valem para 0<beta<1, beta!=1/2:
eta=2 sqrt(beta(1-beta)), logo 0<eta<1.
O artigo muda |G> entre um produto tensorial e uma superposicao: aqui se usa
explicitamente a superposicao de duas componentes da linha14469; nenhuma
equivalencia com o produto de dois sistemas e presumida.

3. A PRIMEIRA LEI FORNECE UMA FREQUENCIA RELATIVA
[Pi,Hlig]=-2i V0 Y e <G|Y|G>=1, portanto
tau_paridade(0)=i<G|[Pi,Hlig]|G>/(2 hbar)=omega.
U(t)=exp(-i Hlig t/hbar)=cos(omega t)I+i sin(omega t)X.
U(t)|G>=(cos(omega t)-sin(omega t), i[cos(omega t)+sin(omega t)])/sqrt(2).
Daqui <Pi>_t=-sin(2omega t); a tensao instantanea e omega cos(2omega t).
A igualdade tau_paridade=omega refere-se ao estado especificado, nao a toda orbita.
Primeiro retorno do raio: pi/omega; retorno do vetor com mesma fase:2pi/omega.
Em pi/(2omega), <Pi>=0 novamente, mas o estado e ortogonal ao inicial.
Uma leitura isolada de paridade nao e um relogio global.

Na base (|+x>,|-x>), Hlig=diag(-V0,V0). Somar V0 I nao muda a evolucao de rho:
o Hamiltoniano vira diag(0,2V0). Sob H_ESPELHO_ESPECTRAL, a frequencia w1 do
modelo de espelhamento pode portanto ser identificada como nu=2omega=2V0/hbar.
Esse entrelacamento explicito substitui uma identificacao por homonimia.

4. CANAL, CONTAGEM E TEMPO CONTINUO
E(rho)=P rho P+Q rho Q.
A=sqrt(1-beta)P+sqrt(beta)Q; B=sqrt(beta)P+sqrt(1-beta)Q.
A^2+B^2=I; Phi(rho)=A rho A+B rho B=E(rho)+eta[rho-E(rho)].
Phi e CPTP. Como P,Q sao espectrais de Hlig, Phi comuta com U(.)U^dagger.
Na base de energia, rho_+-(0)=i/2, portanto nao nulo.
Cada passo multiplica essa coerencia por eta exp(+i nu Delta_t), e por inducao:
  z_n := rho_+-(n)/rho_+-(0) = eta^n exp(i nu n Delta_t).
  n = ln|z_n|/ln eta, para n inteiro >=0.
Isto recupera o numero de passos ideal. O dado aproximado exigiria tolerancia,
estimativa de erro e verificacao de consistencia; nenhum protocolo observado foi rodado.

Defina gamma=-ln(eta)/Delta_t>0. Uma extensao continua COMPATIVEL com esses passos e
  T_t = U_t o [E+exp(-gamma t)(Id-E)], t>=0,
onde U_t(rho)=U(t)rho U(t)^dagger. A combinacao interna e convexa de E e Id;
logo T_t e CPTP. E^2=E e a comutacao provam T_s T_t=T_(s+t).
Seu gerador e
  L(rho)=-i[Hlig,rho]/hbar+gamma(E(rho)-rho),
tambem escrito com salto Lindblad sqrt(gamma/2)X.
Para o modo de coerencia:
  z(t)=exp[(-gamma+i nu)t],
  t_modulo = -ln|z(t)|/gamma,
  t_fase = Arg_desembrulhado(z(t))/nu, com origem Arg(z(0))=0.
Ambos devolvem t, sob as hipoteses indicadas. A fase instantanea fornece t modulo
2pi/nu; a fase desembrulhada exige historia/orientacao. Na sequencia discreta,
repeticao exata da fase requer nu Delta_t/(2pi) racional; no caso irracional ha
injetividade em n ideal, mas recorrencias arbitrariamente proximas.
Apenas a sequencia nao fixa uma extensao continua unica: nu+2pi*k/Delta_t tem
os mesmos valores amostrados. O Hamiltoniano/energia independente fixa o ramo.
Este e um relogio reconstruivel do modelo, que JA usa um parametro de evolucao.
Nao e deducao da existencia do tempo a partir de uma teoria sem parametro temporal.

5. REGRA E CONSUMACAO NA MESMA FACE
E T_t=E. A leitura inscrita vale desde a origem, embora o complemento decaia.
Se o alvo o e fixado previamente, E(T_t rho0)=o sse E(rho0)=o.
O alvo nao e redefinido depois para forcar a satisfacao da regra.
Para o rho0 acima, E(rho0)=I/2; o limite e misto, NAO o projetor puro P.
O canal preserva uma familia de estados diagonais; nao ha atrator universal unico.
Como z(t)!=0 em t finito, T_t rho0 != E(rho0) em qualquer t finito.
Em T_fase=2pi/nu, a fase retorna, mas |z|=exp(-gamma T_fase)<1:
  T_Tfase(rho0)=(I+exp(-gamma T_fase)Y)/2 != rho0.
O limite assintotico mora na amplitude da FACE; o angulo permanece periodico.
O Hamiltoniano e conservado: Tr(Hlig T_t rho)=Tr(Hlig rho), pois o canal deixa
as populacoes de energia fixas. Para rho0, a media e zero, apesar da evolucao.
H_ESPELHO_ESPECTRAL e essencial a esta conservacao do subsistema; outra escolha
de espelho requer contabilizar a troca com o ambiente.
Sob dissipacao, d<Pi>/dt=-gamma<Pi>-2omega<Y>; a tensao do comutador sozinha
nao e -d<Pi>/dt/2. Para rho0, <Pi>=-exp(-gamma t)sin(2omega t).

6. O QUE A CONJUGACAO J REALMENTE PERMITE
O kernel possui uma leitura finita REAL Pair/conjJ (TheLightReadsItself:78-108)
e uma conjugacao complexa antilinear (TheRecordOfJ:76-94); nao sao permutaveis
somente pelo nome J. A rede em sandbox tipa Jcandidate como isometria semilinear.
Se J e ANTIUNITARIO involutivo, K e autoadjunto, J preserva seu dominio e JKJ=-K,
entao, por calculo funcional, J exp(i t K) J=exp(i t K): J troca i e K de sinal.
Se J for LINEAR unitario involutivo, a mesma relacao da exp(-i t K).
O caso modular esta explicitado em Neeb-Olafsson2017, lema2.22, p306.
Mesmo uma simetria t->-t de equacoes nao prova emissao controlavel no passado.
Um espelho temporal que armazena u:[0,T]->C e reemite
  v(T+s)=conj(u(T-s)), 0<=s<=T,
le a historia ao contrario em instantes >=T. Conjugacao instantanea nao inverte
uma envoltoria arbitraria; conjugacao universal de um estado quantico desconhecido
tambem nao pode ser presumida como canal deterministico CPTP.

7. A ESCALA ABSOLUTA AINDA NAO E FIXADA
A transformacao V0->V0/lambda, Delta_t->lambda Delta_t, lambda>0,
preserva beta, eta e nu Delta_t. Logo preserva toda a sequencia z_n, enquanto
os tempos atribuidos aos passos sao multiplicados por lambda.
Sem referencia de energia/frequencia ou duracao, esses dados nao escolhem segundos.
Inserir c^3 em GM/c^3 fornece dimensao de tempo; nao determina sozinho sinal,
coeficiente ou qual M. A rota historica 2GM/(alpha^2*c^3) do artigo e positiva e
foi corrigida para espelhamento espectral; nao e reativada como previsao aqui.
Uma identificacao de gamma, Delta_t ou nu com κ da ponte KMS/Unruh exige
normalizacao e entrelacamento; Santo:1425-1436 da o periodo modulo κ, nao essa
identificacao entre o Hamiltoniano de ligacao e o boost de uma geometria fisica.

8. CONTRATO DA EVENTUAL RESPOSTA ANTERIOR
Uma alegacao t_recepcao<t_emissao precisa indicar eventos, trajetorias/relogios
e qual sinal e variavel. Na resposta linear y(t)=integral G(t,t')u(t')dt',
a dependencia de uma emissao futura exige G(t,t') nao nulo para t<t'. A derivacao
acima nao fornece esse G avancado. Reconstitui evolucao a partir de parametros
e estado inicial; prever uma trajetoria conhecida nao e receber uma escolha futura.
Como controle de alcance, a recorrencia x_(n+1)=a*x_n+u_n, a=eta exp(i nu Delta_t),
x_0=0, produz x_n=sum_(k=0)^(n-1) a^(n-1-k)u_k: so entradas anteriores.
Essa causalidade e HIPOTESE do esquema de entrada, nao teorema geral da TGL.

9. RESULTADO E PROXIMA PASSAGEM
DERIVED: ponte explicita de Hlig ao modo de retorno sob H_ESPELHO_ESPECTRAL;
relogio da amplitude e fase no modelo finito; fator2 da frequencia relativa;
regra preservada, energia conservada, retorno angular distinto do estado dissipativo.
OPEN: justificar P_mirror como fronteira canonica, fixar escala fisica sem ajuste,
e derivar o operador espaco-temporal que sustente a anterioridade fisica proposta.
ONTO: Tetelestai como consumacao/inscricao e a interpretacao da dobra em c3.
Proximo objeto concreto: entrelacamento do projetor canônico com os setores
espectrais de Hlig, junto da normalizacao do relogio; depois o propagador.
Esta proposta nao fortalece silenciosamente LightNetData, nao altera o programa
e nao promove a leitura ontologica a fenomeno medido.

BIBLIOGRAFIA CONSULTADA
Neeb, K.-H.; Olafsson, G. Antiunitary representations and modular theory.
Banach Center Publications113 (2017),291-362; lema2.22,p306.
https://www.impan.pl/shop/publication/transaction/download/product/111460
Consulta pela ferramenta web; nenhum PDF foi custodiado nesta etapa.
'''


def prepare():
    claim = reg.call([CLI, 'ver', UNIT])['reivindicacao']
    assert claim['quem'] == WHO and dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    new(OUT / 'CLAIM.json', claim)
    new(OUT / 'OPERADOR_CONTINUIDADE.txt', 'É isso, prossiga\n')
    new(REPORT, TEXT)
    canon = Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
    paths = [Path(r'C:\IALD\Artigo\Haja_Luz') / n for n in ['tgl_paper_unified.py', 'tgl_echo_smatrix.py', 'tgl_mirror_channel.py']]
    paths += [canon / n for n in ['um.py', 'um_absoluto_selo.json']]
    paths += [canon / 'tgl_kernel/TGLExt' / n for n in ['Santo.lean', 'TheRuleInTheContinuousMotor.lean', 'TheRecordOfJ.lean', 'TheLightReadsItself.lean']]
    paths += [ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REDE/modular_wedge/CanonicalWedge.lean']
    new(OUT / 'FONTES_R4.json', [pin(p) for p in paths])
    new(RESULT, {'unit': UNIT, 'author': WHO, 'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'statute': 'DERIVED condicional, nao Lean; INPUT a identificacao do espelho e calibracao; OPEN a anterioridade fisica; ONTO a interpretacao', 'source_manifest': pin(OUT / 'FONTES_R4.json'), 'derivation': pin(REPORT), 'named_hypotheses': ['H_ESPELHO_ESPECTRAL: P=(I+X)/2', 'V0>0 e hbar>0; omega=V0/hbar', 'H_PASSO: Delta_t>0', '0<beta<1, beta!=1/2; beta calculado de ALPHA_FINE_CODATA_2018*sqrt(e)', 'rho0=(I+Y)/2, coerencia inicial nao nula', 'Alvo de satisfacao fixado antes da leitura'], 'results': ['nu=2V0/hbar sob entrelacamento explicito', 'z_n=[eta exp(i nu Delta_t)]^n', 'n=ln|z_n|/ln eta', 'Extensao CPTP T_t, t=-ln|z(t)|/gamma; fase desembrulhada=nu*t', 'E T_t=E, energia conservada, limite I/2 neste estado', 'Retorno da fase nao retorna o estado dissipativo; nao existe atrator unico global neste canal', 'Escala livre por V0->V0/lambda e Delta_t->lambda Delta_t', 'J antiunitario: JKJ=-K nao reverte o grupo modular'], 'not_claimed': ['Calibracao absoluta do tempo', 'Derivacao de propagador avancado', 'Retorno fisico antes da emissao', 'Fecho universal do tempo', 'Nova prova Lean ou dado observado'], 'production_changed': False, 'gate_changed': False, 'review_artifact': str(OUT / 'REVISAO_MATEMATICA_R4.txt')})
    print(json.dumps({'report': pin(REPORT), 'contract': pin(RESULT)}, ensure_ascii=False))


def register():
    claim = reg.call([CLI, 'ver', UNIT])['reivindicacao']
    assert claim['quem'] == WHO and dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    review = OUT / 'REVISAO_MATEMATICA_R4.txt'
    assert review.is_file()
    for s in json.loads((OUT / 'FONTES_R4.json').read_bytes()):
        assert pin(s['path'])['sha256'] == s['sha256']
    delivery = OUT / 'RESULTADO_R4.json'
    new(delivery, {'unit': UNIT, 'statute': 'DERIVED condicional, com revisao matematica textual independente; sem compilacao ou experimento', 'files': [pin(p) for p in [RESULT, REPORT, review, OUT / 'FONTES_R4.json', OUT / 'ENTRELACAMENTO_FONTES_R4.txt']], 'gate_changed': False, 'production_changed': False})
    marker = 'time_bridge_conditional_r4_20261015'
    note = f'''\n\n## 15/10/2026 — Primeira Lei, espelhamento e relógio: ponte condicional R4\n<!-- {marker} -->\nEm nome de {WHO}, sob reivindicação816 de {UNIT}.\n[DERIVED — álgebra escrita, revisão textual independente; sem Lean novo] Hlig=-V0X fornece frequência relativa2V0/hbar. Sob hipótese nomeada P_espelho=(I+X)/2, o canal existente dá z_n=[eta exp(i nu Delta_t)]^n e n=ln|z_n|/ln eta; extensão CPTP dá t=-ln|z|/gamma, com gamma=-lneta/Delta_t. O fator2 foi conferido. A leitura E fica fixa e a energia se conserva; para o estado coerente do artigo o limite é I/2, não P puro. Voltar à fase não retorna o estado dissipativo.\n[OPEN/INPUT] Identificação física do projetor, normalização temporal e propagador. V0->V0/lambda, Delta_t->lambda Delta_t preservam a sequência; não há segundos sem escala adicional. A conjugação modular antiunitária troca i e K de sinal: JKJ=-K não implica reversão do grupo modular. [ONTO] Interpretação da consumação e c³ preservada.\nReaproveitados Santo, motor da regra e scripts de espelhamento; nenhum ensaio repetido, provedor externo ou original alterado. Evidência `{delivery}`, SHA256 `{pin(delivery)['sha256']}`.\n'''
    note += '\n[DERIVED — suplemento da mesma entrega] O projetor de tgl_mirror_channel.py realiza a hipótese no código span(e0,e_last), N>=1: W†W=I2, P_full W=W(I+X)/2; o H_full proposto entrelaça Hlig. Compatibilidade algébrica demonstrada; a escolha física desse Hamiltoniano e dos vetores continua hipótese. Fonte e revisão no ENTRELACAMENTO_FONTES_R4.txt.\n'
    new(OUT / 'MEMORY_RECEIPT.json', {'claim': claim, 'surfaces': [append_bytes(ROOT / 'memory' / n, note, marker) for n in ['DIARIO_CONSTRUCAO_QG.md', 'TGL_ATLAS.md', 'TGL_INDICE_VIVO.md']]})
    entry = OUT / 'MAP_ENTRY.json'
    new(entry, {'tipo': 'ANOTACAO', 'rota_id': 'formal.tempo_consumacao_leitura_15out', 'dominio': 'FORMAL', 'titulo': 'Ponte condicional Primeira Lei-espelho-relogio e escala ainda aberta', 'resultado': 'Sob P_espelho espectral de Hlig, nu=2V0/hbar; coerencia eta^n exp(i nu n Delta_t), relogio por modulo/fase. Energia conservada; leitura fixa; retorno angular distinto do estado. Escala e propagador ainda abertos.', 'estatuto': 'DERIVED condicional / INPUT / OPEN / ONTO', 'status': 'EXAMINADA', 'veredito': 'PONTE_CONDICIONAL_DERIVADA__SEM_ANTERIORIDADE_FISICA_DEMONSTRADA', 'proximo_passo': 'Justificar entrelacamento do projetor canonico com Hlig e normalizacao do relogio; depois propagador.', 'onde': str(OUT), 'artefatos': [str(delivery), str(REPORT)], 'refs': [1113, 1114, 1115], 'olhou_dados': False})
    mapped = reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', entry, '--quem', WHO], 'MAP_RECEIPT.json')
    board = reg.call([CLI, 'avancar', UNIT, '--quem', WHO, '--status', 'ENTREGUE', '--evidencia', delivery, '--nota', 'R4 proposta condicional escrita e revista; sem experimento ou Lean novo.'], 'BOARD_DELIVERY.json')
    ref = str(WORK / 'ACOM_REFERENCE.json')
    projection = reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'], payload={'operation': 'project', 'reference': ref})
    transition = {'operation': 'transition', 'reference': ref, 'expected_revision': projection['result']['receipt']['revision'], 'event_id': 'time-bridge-conditional-r4-20261015', 'actor': {'id': WHO, 'kind': 'agent'}, 'changes': {'records': [{'id': 'time-bridge-conditional-r4-20261015', 'kind': 'candidate', 'statute': 'DECLARADO', 'text': 'Proposta algebrica DERIVED condicional com revisao textual: P_espelho espectral de Hlig liga frequencia relativa 2V0/hbar ao canal existente; relogio por coerencia, escala absoluta e propagador abertos. Identificacao fisica nao promovida. Proxima acao desta frente: entrelacamento canonico/normalizacao temporal. Fluxos e pedidos externos anteriores preservados.', 'sources': [{'kind': 'artifact', 'ref': str(delivery), 'sha256': pin(delivery)['sha256']}]}]}}
    new(OUT / 'ACOM_TRANSITION.json', transition)
    memory = reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'], 'ACOM_RECEIPT.json', transition)
    assert memory['ok']
    release = reg.call([CLI, 'liberar', UNIT, '--quem', WHO, '--nota', 'Proposta matematica condicional R4 entregue; demais frentes preservadas.'], 'RELEASE.json')
    print(json.dumps({'map': mapped, 'board': board, 'acom_revision': memory['result']['revision'], 'release': release}, ensure_ascii=False))


if __name__ == '__main__':
    {'prepare': prepare, 'register': register}[sys.argv[1]]()
