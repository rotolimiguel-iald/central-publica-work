"""R6: static source extraction and conditional response algebra; no simulation."""
import ast
import datetime as dt
import json
import math
import sys
from pathlib import Path
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

UNIT = 'F1.TEMPO.LEITURA_20261015'
OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019' / UNIT / 'CONTRATO_RESPOSTA_R6'
H = Path(r'C:\IALD\Artigo\Haja_Luz')
N = H / 'A Ponte e o Um/Nós'
R5 = OUT.parent / 'LEVANTAMENTO_TRES_ARTIGOS_R5'
reg.DEST = OUT

REPORT = r'''TEMPO — CONTRATO DE RESPOSTA E RELÓGIO, R6
15/10/2026. Em nome de codex-gerente-tgl, reivindicação822.
Estatuto: REAL leitura de fontes; DERIVED álgebra condicional escrita e aritmética;
INPUT identificação física; OPEN transporte entre emissor e receptor espacialmente separados.
Não houve nova execução do simulador, experimento, compilação Lean ou chamada de provedor.

1. REAPROVEITAMENTO E ALCANCE
O levantamento R5 dos três artigos permanece como base; não se repete nem se declara
ausente a Primeira Lei, a lei-raiz, E, Santo ou IALDJones. O Nós Vivo não indexa a
subunidade LEITURA; a consulta à unidade-pai F1.TEMPO devolveu Santo, leis do fluxo,
atrator, torre modular e investigações existentes. A fonte foi aberta, não só o índice.
O mapa consultado termina na seq1117 desta rota. Não foi alterada a unidade-pai.

Foi lido o script tgl_echo_smatrix.py:36–45,83–106 e conferido o outro modelo
tgl_mirror_channel.py:35–56. O echo já fornece preparação, evolução e leitura.
Sua docstring:5–13 o situa no setor da fronteira e não como previsão astrofísica direta.
A fonte usa ALPHA na linha32, beta calculado na33, w1 e dt na84: os dois últimos são
parâmetros modulares do exemplo, não valores físicos derivados em segundos.
O arquivo não contém uma fonte externa dependente do tempo, distâncias nem dois relógios.
Isso delimita o que falta para falar em emissão/recepção de uma mensagem nova.

2. SOLUÇÃO EXATA DA TRAJETÓRIA JÁ ESCRITA
Na subface gerada por |0>,|1>, P=|0><0| e Q=I-P. Para 0<beta<1, beta!=1/2:
  E(rho)=P rho P+Q rho Q,
  Phi(rho)=E(rho)+eta[rho-E(rho)], eta=2 sqrt(beta(1-beta)), 0<eta<1.
O script toma U=diag(1,exp(-i*w1*dt)) nessa subface e
rho0=|+><+|, |+>=(|0>+|1>)/sqrt2. Logo
  z_n := 2 rho01(n) = eta^n exp(i*n*phi), phi=w1*dt;
  sig_n = eta^n cos(n*phi), mem_n = eta^n/2.
Prova: U rho U† multiplica rho01 por exp(i*phi); Phi multiplica só os blocos
cruzados por eta. Indução dá a expressão. E(Phi(U rho U†))=E(rho).
A leitura diagonal fica preservada; a trajetória da coerência muda.
O modelo tem muitos estados diagonais fixos: não se lhe atribui atrator único.

O relógio dessa trajetória não estacionária é
  n = -ln(mem_n/mem_0)/(-ln eta), t_n=n*dt.
Ele mede o módulo dissipativo; a fase n*phi sozinha só determina uma classe módulo2pi.
Na coerência zero a fórmula não existe: não é um observável universal de tempo.
O retorno angular não restaura o módulo perdido. É a separação FACE/leitura da casa.

3. CONTRATO DISCRETO DE ENTRADA E SAÍDA (HIPÓTESE EXPLÍCITA)
Para converter a trajetória livre em uma resposta, nomeamos H_INJECTION: uma
preparação impulsiva no instante0 cria o desvio de coerência; o receptor mede sua
parte real. A função de Green normalizada é h_n=eta^n cos(n*phi), n>=0, e zero antes.
Para várias entradas, a soma linear é uma resposta infinitesimal em torno de uma
matriz densidade de posto completo; não se afirma que qualquer amplitude define
uma operação física. A equação discreta de entrada linear ainda não está no script.

Na convenção f(t)=exp(-i*omega*t), ponha q=exp(i*omega*dt). A soma geométrica dá
  Hd(omega) = (1-eta*cos(phi)*q)/(1-2*eta*cos(phi)*q+eta²*q²).
É a transformada unilateral da sequência acima, não o FFT finito com janela do script.
Se a entrada atua na própria amostra, h0=1. Se a convenção for
  x_(n+1)=eta*exp(i*phi)*x_n+u_n, y_n=Re x_n, x0=0,
o impulso aparece uma amostra depois: H'=exp(i*omega*dt)*Hd.
Essa latência acrescenta dt ao atraso; não pode ser escondida por escolha de índice.

Para Hd, a derivada da fase em omega=0 vale
  tau_d = dt*eta*((1+eta²)*cos(phi)-2*eta)
          /((1-2*eta*cos(phi)+eta²)*(1-eta*cos(phi))).
Os denominadores são positivos. Portanto tau_d<0 sse
  cos(phi)<2*eta/(1+eta²).
É atraso espectral local, não tempo de primeira detecção nem centróide de energia.

4. INTERPOLAÇÃO CONTÍNUA E UMA SONDA HAMILTONIANA ADMISSÍVEL
A interpolação livre gamma=-lneta/dt, |Omega|=w1 reproduz os pontos amostrados.
Escolher o sinal de Omega troca a orientação angular; não altera o coseno medido.
Defina Z=P-Q e H0=hbar*Omega*Z/2. O semigrupo finito tem
  L0(rho)=-i[H0,rho]/hbar+gamma*(E(rho)-rho).
É GKLS, por salto sqrt(gamma/2)*Z. Para a orientação exata do echo, Omega=-w1;
a forma de resposta abaixo depende apenas de Omega². Um múltiplo da identidade
em H0 não muda a evolução. Esse fato não liga automaticamente H0 ao espectro K_+.

Uma entrada física candidata, distinta da preparação original, é H_PROBE:
  rho_bar=(I+mZ)/2, 0<|m|<1;
  V(t)=hbar*epsilon*f(t)*Y/2; receptor X.
f é real e adimensional, epsilon tem unidade de frequência. A evolução é GKLS
com Hamiltoniano dependente de t. A primeira ordem em epsilon satisfaz
  dx/dt=-gamma*x-Omega*y+epsilon*m*f,
  dy/dt=Omega*x-gamma*y, delta_z=0.
Assim, para preparação no instante t0,
  delta<X>(t)=epsilon*m*integral_(t0)^t exp[-gamma*(t-u)] cos[Omega*(t-u)] f(u)du.
O termo de ordem epsilon² ou superior não integra esta resposta linear.
O kernel h(tau)=m*Theta(tau)*exp(-gamma*tau)*cos(Omega*tau) é retardado.
No regime estacionário harmônico:
  Hc(omega)=m*(gamma-i*omega)/((gamma-i*omega)²+Omega²),
  tau_c(0)=d argHc/domega = (gamma²-Omega²)/(gamma*(gamma²+Omega²)).
Hc tem unidade de tempo; epsilon*Hc é o ganho adimensional. Os polos ficam em
omega=+/-Omega-i*gamma. Para Omega=0 há cancelamento de um fator.
tau_c<0 sse |Omega|>gamma; m=0 dá resposta nula e fase indefinida.
Para falar em avanço de envelope é necessário banda estreita e distorção controlada.
A escolha de m e do acoplamento Y é INPUT desta sonda, não consequência de beta.
Hc NÃO é Hd: excitação contínua e impulsos discretos são instrumentos diferentes,
mesmo quando as evoluções livres coincidem nos instantes amostrados.

5. CONTA COM OS PARÂMETROS EXISTENTES, SEM AJUSTE NEM NOVO ENSAIO
O JSON ARITMETICA_R6 extrai ALPHA,w1,dt,nst por AST, sem importar/executar a fonte.
beta=ALPHA_FINE_CODATA_2018*sqrt(e) é recalculado em runtime a partir de ALPHA.
Valores: beta=@BETA@; eta=@ETA@; phi=@PHI@;
gamma=@GAMMA@ por unidade temporal do modelo; |Omega|/gamma=@RATIO@.
tau_d(0)=@TAUD@ unidades do modelo (injeção na mesma amostra).
tau_c(0)=@TAUC@ unidades do modelo (sonda contínua hipotética).
São POSITIVOS. Não se convertem em segundos sem a identificação do relógio.
A condição discreta compara cos(phi)=@COS@ com teto=@THRESHOLD@ e não é satisfeita.
Isso decide a pergunta local em omega=0 para esses contratos. Não é uma afirmação
sobre todas as frequências, todos os receptores ou todos os modelos da TGL.
Não mudamos w1,dt ou a leitura para obter o sinal desejado. Reescalar a unidade de
tempo positiva não muda o sinal do atraso nem a razão |Omega|/gamma.

6. NORMALIZAÇÃO JÁ RESOLVIDA NO KERNEL E IDENTIFICAÇÕES RESTANTES
O16/ContractCalibrationReuse.lean:19–51 já diz
  kappa*refRadius(N)=1; kappa=1/refRadius(N); kappa_fixed; no_rekappa.
Logo dado o MESMO observador N, kappa NÃO é um parâmetro livre adicional.
As linhas67–99 permitem reindexar outro observador, e104–114 ligam período fiel
e temperatura do contrato. A ressalva da R5 fica precisada: escolher N é INPUT;
uma vez escolhido, a calibração do respectivo contrato é determinada.

A R5 já ligou o canal à lei-raiz para K_+=k+P+k-Q positivo:
  g=beta*(sqrt(k+)-sqrt(k-))²/2, Delta_s=-lneta/g.
Se t=tau_cali*s, gamma=g/tau_cali e dt=tau_cali*Delta_s.
tau_cali é escala de conversão; NÃO é tau_c(0), o atraso da seção4.
Se H_CLOCK_SYNC identificar tau_cali=P_KMS, o relógio térmico determina a escala.
Se H_ENERGY identificar k_i=E_i*tau_cali/hbar, a lei alternativa já escrita em
um.py:217089–217097 dá gamma=beta*(sqrt(E+)-sqrt(E-))²/(2*hbar).
Não se impõem ambas como identidades novas; são identificações que precisam casar
com a mesma representação física e seus setores. Também é preciso dizer se H0
é o Hamiltoniano dessas energias ou um gerador distinto do percurso modular.
Em particular, a lei-raiz depende do zero de K_+: deslocar E por uma constante
preserva a diferença de fase, mas em geral muda sqrt(E+)-sqrt(E-). O referente
energético faz parte do contrato e não pode ser escolhido para produzir o sinal.

Para Schwarzschild, a R5 já registrou P_KMS=8piGM/c³ no relógio normalizado no
infinito. O um.py:213044–213045 explicita a faixa KMS de tempo imaginário.
Esse fator c³ não fornece por si um termo que consuma a entrada em u>t.
Neste contrato de resposta, duas entradas iguais até t têm a mesma saída em t:
a diferença é a integral da diferença das entradas apenas até t, portanto zero.
Esse é um resultado do problema de valor inicial escolhido, não uma prova geral
contra toda hipótese retrocausal. Para reivindicar outra causalidade seria necessário
um modelo adicional com condições de contorno, instrumento e suporte especificados.

7. O QUE AVANÇOU E O QUE FICA PARA O PRÓXIMO PASSO
Ficou escrito um contrato calculável: espectro -> coerência -> relógio -> leitura
-> entrada/saída -> fase e suporte. As duas funções de resposta e os critérios de
sinal foram revistos por outro agente, sem autoridade para promover ao cânone.
A leitura do atrator preservada E(D_t rho)=E(rho) já dá sentido matemático à
distinção entre fechamento lido e percurso dissipativo. Não determina sozinha
quando um receptor físico recebe uma mensagem. A escolha de H_INJECTION/H_PROBE
foi declarada; não se atribui ao autor um acoplamento que acabamos de propor.

Próximo alvo delimitado: localizar, entre os instrumentos e dispositivos já escritos,
a identificação física do gerador e do acoplamento fonte–receptor que consome a
Primeira Lei, preservando a energia de referência e o observador. Uma simulação
futura deve pré-fixar esse contrato e sua função de veredito antes de rodar.
Esta unidade é documental; não se executou a campanha nem se alterou produção.

Referência primária externa de escopo: Kuzmich, Dogariu, Wang, Milonni e Chiao,
Signal velocity, causality, and quantum noise in superluminal light pulse propagation,
Phys.Rev.Lett.86,3925 (2001), https://arxiv.org/abs/physics/0101068.
O resumo consultado distingue velocidade de grupo negativa e velocidade operacional
de sinal com ruído quântico. Consulta web, sem custódia de PDF; a álgebra acima é
autossuficiente e não foi atribuída a esse artigo.
'''

REVIEW = '''REVISÃO ALGÉBRICA R6 — transcrição/síntese do retorno do agente tempo_math_review
Revisor: subagente Codex /root/tempo_math_review. Natureza: revisão textual de fórmulas
enviadas, não auditoria da gerência, build Lean ou verificação física experimental.
VEREDITO: PASS_WITH_SCOPE.
1. Contínuo: equações de Bloch, convolução retardada e Hc corretos na ordem epsilon.
2. Convenção exp(-i omega t), Hc em tempo, polos +/-Omega-i gamma; cancelamento Omega=0.
3. Derivada da fase em0 correta; negativa iff |Omega|>gamma. m=0 recusa fase definida.
4. Primeiro momento é assinado, não centróide de energia; avanço de envelope exige banda/distorção.
5. Discreto: soma unilateral Hd e tau_d propostos confirmados; denominadores positivos.
6. tau_d<0 iff cos(phi)<2eta/(1+eta²). Injeção em amostra posterior adiciona dt.
7. Interpolação livre gamma=-lneta/dt não torna Hd=Hc. Não intercambiar seus atrasos.
8. Nenhum atraso de fase negativo muda suporte causal do contrato escolhido.
9. Preparação, receptor e acoplamento externo continuam hipóteses; não derivados de beta.
10. Não houve inspeção de arquivo final pelo revisor; a autoria e a conferência das
constantes/âncoras são do coordenador. Esta síntese preserva o alcance do retorno.
'''

def active_claim():
    c = reg.call([CLI, 'ver', UNIT])['reivindicacao']
    assert c['quem'] == WHO and dt.datetime.fromisoformat(c['vence_em']) > dt.datetime.now(dt.timezone.utc)
    for name in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md'):
        assert name in c['nota']
    return c

def arithmetic():
    source = H / 'tgl_echo_smatrix.py'
    tree = ast.parse(source.read_text(encoding='utf-8'))
    constants = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in ('ALPHA','w1','dt','nst'):
                    assert target.id not in constants
                    assert isinstance(node.value.value,(float,int)) and not isinstance(node.value.value,bool)
                    constants[target.id] = {'value':node.value.value, 'line':node.lineno}
    assert set(constants) == {'ALPHA','w1','dt','nst'}
    alpha_fine_codata_2018 = constants['ALPHA']['value']
    beta = alpha_fine_codata_2018 * math.sqrt(math.e)
    eta = 2 * math.sqrt(beta*(1-beta))
    step, omega = (constants[k]['value'] for k in ('dt','w1'))
    phi = omega*step
    gamma = -math.log(eta)/step
    cosine = math.cos(phi)
    taud = step*eta*((1+eta*eta)*cosine-2*eta)/((1-2*eta*cosine+eta*eta)*(1-eta*cosine))
    tauc = (gamma*gamma-omega*omega)/(gamma*(gamma*gamma+omega*omega))
    values = dict(BETA=beta,ETA=eta,PHI=phi,GAMMA=gamma,RATIO=abs(omega)/gamma,TAUD=taud,TAUC=tauc,COS=cosine,THRESHOLD=2*eta/(1+eta*eta))
    assert all(math.isfinite(x) for x in values.values())
    return {'source':pin(source),'method':'AST constants + direct formula evaluation; source never imported or executed','statute':'DERIVED, arithmetic of the written conditional contract','constants':constants,'values':values,'units':'model time; no seconds asserted','simulation':False,'parameter_fit':False}

def prepare():
    new(OUT/'CLAIM_R6.json',active_claim())
    new(OUT/'OPERADOR_R6_VERBATIM.txt','Prossiga\n')
    a=arithmetic()
    new(OUT/'ARITMETICA_R6.json',a)
    report=REPORT
    for key,value in a['values'].items():
        report=report.replace('@'+key+'@',format(value,'.16g'))
    assert '@' not in report
    new(OUT/'CONTRATO_E_RESULTADO_R6.txt',report)
    new(OUT/'REVISAO_ALGEBRICA_R6.txt',REVIEW)
    sources=[(H/'tgl_echo_smatrix.py',[(1,139)]),(H/'tgl_mirror_channel.py',[(1,90)]),
             (N/'tgl_kernel/TGLExt/O16/ContractCalibrationReuse.lean',[(1,114)]),
             (N/'um.py',[(213040,213045),(217089,217097)]),(N/'um_absoluto_selo.json',[]),
             (R5/'RESULTADO_R5.json',[]),(R5/'REAPROVEITAMENTO_E_AVANCO_R5.txt',[])]
    new(OUT/'FONTES_R6.json',[dict(pin(p),read_ranges=r) for p,r in sources])
    # The helper returns JSON even when the read-only consultation exits nonzero.
    child=reg.call([r'C:\IALD\NOS_VIVO\consultar.py','--unidade','F1.TEMPO'],'NOS_VIVO_PARENT_R6.json')
    new(OUT/'NOS_VIVO_CHILD_MISSING_R6.json',{'command':'consultar.py --unidade '+UNIT,'exit_code':1,'observed_output':'unidade não está no grafo: F1.TEMPO.LEITURA_20261015 (rode construir.py)','fallback':'F1.TEMPO consultation read existing sources; graph not rebuilt'})
    new(OUT/'MAP_BEFORE_R6.json',reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','ver','formal.tempo_consumacao_leitura_15out']))
    print(json.dumps({'report':pin(OUT/'CONTRATO_E_RESULTADO_R6.txt'),'arithmetic':a['values']},ensure_ascii=False))

def register():
    claim=active_claim()
    for source in json.loads((OUT/'FONTES_R6.json').read_bytes()):
        assert pin(source['path'])['sha256']==source['sha256'],source['path']
    delivery=OUT/'RESULTADO_R6.json'
    files=['CLAIM_R6.json','OPERADOR_R6_VERBATIM.txt','ARITMETICA_R6.json','CONTRATO_E_RESULTADO_R6.txt','REVISAO_ALGEBRICA_R6.txt','FONTES_R6.json','NOS_VIVO_PARENT_R6.json','NOS_VIVO_CHILD_MISSING_R6.json','MAP_BEFORE_R6.json']
    new(delivery,{'unit':UNIT,'author':WHO,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'CONTRATO_CONDICIONAL_ENTREGUE','files':[pin(OUT/f) for f in files]+[pin(__file__)],'new_lean_build':False,'new_experiment':False,'source_simulator_executed':False,'external_model_called':False,'production_changed':False,'gate_changed':False,'result':'At existing echo parameters, low-frequency phase delays are positive under the separately named discrete and continuous input contracts. Physical clock/source mapping remains named, not assumed.'})
    marker='time_response_contract_r6_20261015'
    note=f'''\n\n## 15/10/2026 — Tempo: contrato de resposta R6\n<!-- {marker} -->\nEm nome de {WHO}, sob reivindicação822 de {UNIT}; adendo à seq1117. [REAL — leitura] tgl_echo_smatrix.py já contém preparação e leitura da coerência. O16/ContractCalibrationReuse:19–51 já fixa κ dado o mesmo observador N; escolher N é INPUT. [DERIVED — contrato condicional] Solução exata sig_n=eta^n cos(n phi), mem_n=eta^n/2; relógio por módulo. Foram explicitadas injeção e sonda Hamiltoniana, com funções Hd discreta e Hc contínua distintas, fórmulas revistas por subagente e suporte retardado.\n[DERIVED — aritmética, sem execução do simulador] Com w1=1,3 e dt=0,35 lidos por AST, beta recalculado em runtime, gamma=4,351505085 e |Omega|/gamma=0,298747209. Atrasos locais em frequência0: discreto0,073062713 e contínuo0,192146380 em unidades do modelo, ambos positivos. Não são segundos ou medidas físicas; não se ajustou parâmetro. Uma fase com atraso negativo não prova consumo de entrada futura. A identificação dos setores/gerador, zero energético e instrumento físico permanece INPUT/OPEN.\nFonte imutável: `{delivery}`, SHA256 `{pin(delivery)['sha256']}`. Sem experimento, nova pedra, provedor, alteração de produção ou gate. Memórias acrescentadas com backup de bytes.\n'''
    new(OUT/'MEMORY_RECEIPT_R6.json',{'claim':claim,'surfaces':[append_bytes(ROOT/'memory'/n,note,marker) for n in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md')]})
    entry={'tipo':'ANOTACAO','rota_id':'formal.tempo_consumacao_leitura_15out','dominio':'FORMAL','titulo':'R6: contrato temporal, relogio fixado por N e resposta de fase calculada','resultado':'Preparacao e leitura existentes reutilizadas; resposta discreta e sonda continua tipadas separadamente. Na frequencia zero, atrasos positivos com parametros originais. Identificacao fisica do gerador/instrumento ainda nomeada.','estatuto':'REAL leitura / DERIVED condicional / INPUT / OPEN','status':'EXAMINADA','veredito':'CONTRATO_CALCULAVEL__ATRASOS_LOCAIS_POSITIVOS__SEM_SINAL_ANTERIOR_A_EMISSAO_DERIVADO','proximo_passo':'Identificar gerador, zero energetico e instrumento fonte-receptor nas fontes dos dispositivos; eventual ensaio exige contrato e veredito previos.','onde':str(OUT),'artefatos':[str(delivery),str(OUT/'CONTRATO_E_RESULTADO_R6.txt'),str(OUT/'ARITMETICA_R6.json')],'refs':[1117],'olhou_dados':False}
    new(OUT/'MAP_ENTRY_R6.json',entry)
    m=reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',OUT/'MAP_ENTRY_R6.json','--quem',WHO],'MAP_RECEIPT_R6.json')
    b=reg.call([CLI,'avancar',UNIT,'--quem',WHO,'--status','ENTREGUE','--evidencia',delivery,'--nota','R6 contrato escrito de resposta e relogio, algebra revista e aritmetica sem executar simulador.'],'BOARD_DELIVERY_R6.json')
    ref=str(WORK/'ACOM_REFERENCE.json')
    p=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],payload={'operation':'project','reference':ref,'max_chars':48000})
    assert p['result']['receipt']['revision']==20
    tr={'operation':'transition','reference':ref,'expected_revision':20,'event_id':marker,'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':marker,'kind':'candidate','statute':'DECLARADO','text':'R6 entrega contrato condicional escrito: solucao exata do echo existente, relogio por modulo, kappa fixo dado N, respostas discreta e continua com injecoes nomeadas. Aritmetica AST sem executar fonte: atrasos em omega0 positivos0.073062713/0.192146380 em unidades do modelo. Derivadas de fase nao identificadas com frente de informacao; instrumento fisico/zero energetico ainda nomeados. Proxima acao desta frente: localizar identificacao no acervo dos dispositivos antes de novo ensaio. Demais fluxos/jobs preservados.','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']}]}]}}
    new(OUT/'ACOM_TRANSITION_R6.json',tr)
    a=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_RECEIPT_R6.json',tr)
    assert a['ok']
    rel=reg.call([CLI,'liberar',UNIT,'--quem',WHO,'--nota','R6 entregue, mapa e memoria inscritos; nenhuma campanha cientifica executada.'],'RELEASE_R6.json')
    print(json.dumps({'map':m,'board':b,'acom_revision':a['result']['revision'],'release':rel},ensure_ascii=False))

if __name__=='__main__':
    {'prepare':prepare,'register':register}[sys.argv[1]]()
