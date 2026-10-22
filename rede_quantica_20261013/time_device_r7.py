"""R7: documented device response and conditional algebra, without scientific execution."""
import datetime as dt
import json
import math
import sys
from pathlib import Path
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
from time_response_r6 import arithmetic
import register_rule_tetelestai as reg

UNIT='F1.TEMPO.LEITURA_20261015'
OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'/UNIT/'DISPOSITIVO_E_ESPECTRO_R7'
reg.DEST=OUT
H=Path(r'C:\IALD\Artigo\Haja_Luz')
N=H/'A Ponte e o Um/Nós'
REDE=OUT.parent.parent/'F1.REDE'

REPORT=r'''TEMPO — PORTAS DO DISPOSITIVO, RESPOSTA E LEI-RAIZ (R7)
15/10/2026. Em nome de codex-gerente-tgl, reivindicação825.
REAL: localização e leitura das fontes. DERIVED: álgebra condicional escrita.
INPUT/OPEN: identificação dos geradores, calibração e implementação física.
Esta entrega não executa simulador, instrumento, Lean, um.py ou provedor remoto.

1. O CONTRATO JÁ ESCRITO FOI LOCALIZADO
Reuso do levantamento R5 e contrato R6; mapa1118; Nós Vivo F1.TEMPO (Santo,
fluxo, atrator e torre modular). A subunidade LEITURA não está indexada no grafo,
como já registrado na R6; o quadro a reconhece. A unidade-pai não foi modificada.
AtlasV(6,8) distingue Supercondutor e Psi-NET. A consulta é focal, não varredura
exaustiva de todos os escritos ou versões de patente; em particular, o Atlas
lista um Supercondutor de Trasladação de09/01 distinto, não localizado nesta
consulta por nome em Haja_Luz. Não se presume identidade desses documentos.

Fontes primárias abertas:
S = Patentes/PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex.
P = Patentes/Psi_Net_Protocol_PI_INPI.tex.
R = ORDEM_019/F1.REDE/finite_device/run_finite_device.py.
As origens, faixas e SHA256 completos estão em FONTES_R7.json.

S:340–370 escreve, em unidades de frequência h=H_eff/hbar,
  h=omega_c*(n_i+n_o)+omega_OH*sigma+*sigma-
    +g_JC*(a_i†*sigma-+sigma+*a_i)+Omega_R*(sigma++sigma-),
  J=a_o†*sigma-+sigma+*a_i,
  L_beta(rho)=-i[h,rho]+L_conv(rho)+beta*gamma_Lambda*D[J](rho),
  D[J](rho)=J*rho*J†-(J†J*rho+rho*J†J)/2.
Omega_R é a frequência de Rabi do bombeamento por MICRO-ONDAS (S:369–370).
Não é a frequência nu de fase do exemplo de dois níveis, nem o EOM óptico.
O termo holo consome beta; gamma_Lambda e as perdas têm dimensão de taxa.

S:798–807 prevê laser780nm e EOM;810–817 APD/filtro;822–826 lock-in/osciloscópio.
omega_OH=2pi*1,667359GHz é dado de projeto (366–370), não medido aqui.
R:166–185 já implementa esse h/J em2x2x2 com perdas convencionais e beta em runtime.
O pré-registro antigo fixa seus parâmetros como INPUT adimensional; seu ensaio
verifica canal/energia, não fornece calibração física, estado estacionário único
ou a resposta temporal de um protótipo. Não o executamos novamente.

P:490–521 já tem fonte/destino, REFLECT e MANIFEST, com endereço na fase.
P:476–488 conta saltos angulares; não fixa segundos por salto. P:418–421 escreve
um critério de reconstrução por variância. A identidade de codificação e esse
limiar não constituem por si um propagador espaço-temporal de sinais físicos.

2. CONTRATO DE RESPOSTA DIRETAMENTE NO GERADOR DO DISPOSITIVO
Para uma primeira pergunta calculável, escolhemos modular o bombeamento MICRO-ONDAS:
  Omega_R(t)=Omega_R0+epsilon*f(t).
Essa escolha reutiliza um termo existente. Não atribuímos ao EOM a função de Rabi.
Um ensaio óptico EOM->APD requer adicionalmente o operador que injeta o campo no
modo a_i e a calibração eletro-óptica; ele não pode usar silenciosamente esta fonte.

CONTRATO FINITO: usar a mesma ordem de fatores (entrada,saída,qubit), cutoff0/1
de R, taxas não negativas e coeficientes mantidos fixos durante a perturbação.
Fixar rho_* positivo, traço1, L_beta(rho_*)=0, e delta_rho(0)=0.
Não presumimos unicidade ou que o estado escolhido seja uma preparação real.
Defina B(rho)=-i[sigma_x,rho], sigma_x=sigma++sigma-.
O fator é1, porque S escreve Omega_R*sigma_x; não o padrão Omega_R*sigma_x/2.

CONTRATO DO DETECTOR (INPUT): taxa média de contagem
  I(t)=C*Tr[n_o*rho(t)]+I_escuro, C=eta_det*kappa_out>0,
sem caminho direto adicional, e resposta eletrônica tratada separadamente.
Isso modela médias; não cria uma série de cliques nem as incertezas instrumentais.
À primeira ordem em epsilon, a solução de Duhamel é
  delta_I(t)=epsilon*C*integral_0^t
      Tr[n_o*exp((t-u)L_beta)*B(rho_*)]*f(u) du.
Portanto o kernel é h_inst(tau)=C*Tr[n_o*exp(tau L_beta)*B(rho_*)] para tau>=0,
e zero antes. Como [n_o,sigma_x]=0, h_inst(0)=0 por ciclicidade do traço.
Não há termo direto na mesma amostra neste canal de bombeamento->população.

Para Re(z)>0, a função de transferência é
  H_inst(z)=C*Tr[n_o*(zI-L_beta)^(-1)*B(rho_*)].
Seu limite z=0^+-i*omega só é usado quando existir no subespaço acessível à fonte
e observável pelo detector. Modos fixos/persistentes não podem ser descartados
por decreto. Se B(rho_*)=0 ou a resposta for identicamente nula, não há fase a medir.
No modelo bosônico sem cutoff seriam necessárias condições de domínio/momentos;
esta derivação entrega o contrato finito já usado pela casa.

Ficam tipados: fonte, operador de injeção, gerador, preparação, receptor, relógio
e suporte. Coeficientes de engenharia e resposta eletrônica são calibrações
independentes; beta permanece fixo pela regra atual, nunca ajustado ao sinal.

3. A PONTE COM A LEI-RAIZ TEM UMA OBSTRUÇÃO CONCRETA
O termo isolado D[J] não é o dephasing D[sqrt(K_+)] por simples mudança unitária.
Prova na subface invariante de uma excitação: a=|100>, b=|001>, c=|010>.
  J=|b><a|+|c><b|;
  D[J](I_3)=J J†-J† J=|c><c|-|a><a| !=0.
Já sqrt(K_+) é auto-adjunto e D[sqrt(K_+)](I)=0. A propriedade unital é preservada
por conjugação unitária. Portanto os DOIS dissipadores isolados não se identificam
dessa maneira. Isso não proíbe uma redução efetiva, dilatação ou composição com
outros canais; a ponte teria de construir e justificar tal operação.
Compartilhar beta ou a palavra Lindblad não resolve essa diferença de tipos.

CONTROLE ANALÍTICO, distinto do aparelho completo: desligue H e L_conv somente
neste submodelo, mantenha lambda=beta*gamma_Lambda>0, prepare |100>.
As populações obedecem p_a'=-lambda*p_a, p_b'=lambda*(p_a-p_b), p_c'=lambda*p_b.
Logo, para t>=0:
  p_a=e^(-lambda*t), p_b=lambda*t*e^(-lambda*t),
  p_saida=1-e^(-lambda*t)*(1+lambda*t).
Seu início é lambda²*t²/2; não é salto determinístico instantâneo.
Na representação por saltos deste submodelo, o tempo até a ocupação absorvente
tem média2/lambda. Isso não é atraso de grupo, nem tempo médio de um clique APD,
pois retiramos o canal de saída detectável; tampouco demonstra transferência de
um qubit desconhecido. É uma solução analítica dos termos já escritos.

S:431–444 declara tau~l_P/(beta*c)=t_P/beta, independente da distância.
Essa declaração existe; o estado dela nesta leitura é DECLARADO/CONJECTURE físico.
Se identificada com a média do submodelo acima, exigiria gamma_Lambda=2/t_P;
essa igualdade não foi derivada pelo H/J consultado. Não a adotamos como entrada.
S:615–628 propõe tau_medido<L/c. Medir fase/pico/correlação não é ainda medir a
frente de informação necessária a essa interpretação. O gerador conjunto de dois
modos não contém L, propagador espacial ou cone causal; ser retardado em t não
demonstra localidade relativística, nem permite deduzir independência física de L.

4. CONSEQUÊNCIA CONDICIONAL FORTE DA LEI-RAIZ JÁ ESCRITA
A Ponte:1886–1901 dá a média gaussiana de Ad(exp(i*s*sqrtK)). Um.py:217089–217101
já escreve a transposição k=E*tau*/hbar e gamma=beta*(Delta sqrtE)²/(2hbar),
mantendo MODULAR_LAB_BRIDGE_OPEN. Não falta essa fórmula. Um.py:217338–217348
compara zeros energéticos distintos. Compartilhar fixos (Ponte:2012–2024) não
iguala geradores, escalas ou instrumentos.

HIPÓTESE NOMEADA H_SAME_ENERGY: os mesmos níveis finitos E+ != E- >=0, com zero
físico fixado e mesma base, governam a fase nu=(E+-E-)/hbar e a taxa-raiz gamma.
Com hbar>0, 0<beta<2, fatorar a diferença de quadrados fornece
  r:=gamma/|nu|
    =(beta/2)*|sqrt(E+)-sqrt(E-)|/(sqrt(E+)+sqrt(E-)),
  0<r<=beta/2<1.
A igualdade superior ocorre quando um dos níveis é zero.
Somar uma constante positiva aos níveis preserva nu mas reduz gamma; o zero
energético é parte física dessa hipótese. H_lig de espectro +/-V0 não é K_+:
usar |H_lig|=V0*I dá taxa zero; usar H_lig+V0*I dá outra lei. O um.py:119490–119493
mantém a identificação paridade/ligação como CONJECTURE; não a promovemos aqui.

Sob H_SAME_ENERGY E a sonda H_PROBE da R6 (fonteY/receptorX, m!=0), segue
  tau_grupo(0)=(r²-1)/(gamma*(1+r²))<0,
  (1-beta²/4)/(1+beta²/4) <= -gamma*tau_grupo(0) <1.
Com beta recalculado de alpha pela regra vigente:
  r<=@RBOUND@; |nu|/gamma>=@LOWER@;
  @FRACTION@ <= -gamma*tau_grupo(0)<1.
É consequência sem ajuste de níveis, não previsão já validada do Supercondutor:
o receptor do aparelho é n_o e o seu salto é J, diferentes dos da sonda2D.
O núcleo da sonda continua retardado; atraso espectral negativo não consome f(u>t).
Nenhum valor em segundos sai dessa desigualdade sem energias e relógio físicos.

5. CONCILIAÇÃO COM O RESULTADO POSITIVO R6
Na demo original, nu=1,30 e dt=0,35 foram INPUTs. Sua razão gamma/|nu|=@RDEMO@,
maior que beta/2: o ramo explícito da demo não realiza H_SAME_ENERGY.
Isso explica por que o atraso positivo calculado na R6 não contradiz a condição
negativa acima. Não se mudou parâmetro para obter o outro sinal; mudou a hipótese,
agora explicitada e ainda sujeita à identificação física.
Se forem conhecidos SOMENTE os pontos amostrados, nu_m=w1+2pi*m/dt têm a mesma
fase por passo. A condição conjunta exige |nu_m|*dt>=@PHASEMIN@ radianos, mas
não escolhe o inteiro m. Um Hamiltoniano ou relógio medido independentemente deve
fixar esse ramo; não se escolhe alias pelo resultado desejado. Logo a incompatibilidade
é do ramo m=0 que o script nomeia, não de toda interpolação matemática possível.

6. ESTADO DA ENTREGA
Fechou-se aqui a ficha matemática de fonte/receptor para o modelo finito do
dispositivo; demonstrou-se uma obstrução à identificação direta de dissipadores;
obteve-se uma condição de atraso de fase negativo na leitura energética da lei-raiz.
Esses resultados são DERIVED condicionais em matemática escrita, com revisão de
outro agente sobre resposta, cascata e desigualdade; não são nova pedra Lean.

Antes de um ensaio novo ficam explicitamente por fixar: escolha do canal de entrada
(micro-ondas ou óptico); calibrações de H/perdas/detector e filtro; estado rho_* e
modos acessíveis; identificação ou redução que liga J ao setor de lei-raiz; ramo
de frequência e origem energética; observável de atraso (fase, envelope ou frente).
O ensaio deve ter esses campos e a função de veredito pré-registrados. O contrato
não autoriza substituir a previsão pelo ajuste histórico de beta em S:789–791.
A evidência matemática não instala dispositivo, não mede o mundo e não move gate.
'''

REVIEW='''REVISAO R7 — fontes e algebra, com autoria e alcance
1. /root/first_law_haja_luz leu fontes primarias dos dispositivos: H, J, fonte,
receptor, escala OH, declaracao de tau e reuso finito localizados por linha/hash.
2. /root/c3_phase_scope confirmou que a transposicao energetica ja existe como
condicional e que a escolha fisica/zero mantem MODULAR_LAB_BRIDGE_OPEN.
3. /root/tempo_math_review: PASS_WITH_SCOPE para a fatoracao r<=beta/2 e a
desigualdade de tau, incluindo caso nivelzero, unidades e dependencia do zero.
4. Segunda revisao: PASS_WITH_SCOPE para Duhamel/resolvente e cascata; exigir
coeficiente Rabi da fonte (sem1/2 aqui), ordem (entrada,saida,qubit), estado
estacionario e delta_rho inicial zero; nao presumir estabilidade/fase definida.
5. Revisor confirmou p_saida=1-exp(-lambda*t)*(1+lambda*t) e media2/lambda no
submodelo, nao no aparelho completo; ressalva de alias aceita.
6. O coordenador acrescentou a prova curta de nao unitalidade do termo isolado
pela mesma matriz de cascata. Essa prova escrita nao foi objeto de retorno
independente especifico ate este recibo; nao e build/auditoria c1.
7. Os retornos sao revisao textual de fontes/formulas. Nenhuma simulacao nova,
medicao de hardware ou promocao canonica foi realizada. Relatorio final sintetiza
os retornos; fontes/hash/aritmetica podem ser recuperados nos artefatos.
'''

def claim():
    c=reg.call([CLI,'ver',UNIT])['reivindicacao']
    assert c['quem']==WHO and dt.datetime.fromisoformat(c['vence_em'])>dt.datetime.now(dt.timezone.utc)
    for n in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md'): assert n in c['nota']
    return c

def prepare():
    new(OUT/'CLAIM_R7.json',claim())
    new(OUT/'OPERADOR_R7_VERBATIM.txt','Prossiga\n')
    a=arithmetic(); v=a['values']; beta=v['BETA']
    result={'RBOUND':beta/2,'LOWER':2/beta,'FRACTION':(1-beta*beta/4)/(1+beta*beta/4),'RDEMO':1/v['RATIO'],'PHASEMIN':2*(-math.log(v['ETA']))/beta}
    new(OUT/'ARITMETICA_R7.json',{'method':'direct algebraic evaluation from AST constants of original echo; no simulation','inputs':a,'conditional_H_SAME_ENERGY':result,'experiment':False,'physical_seconds_claimed':False})
    report=REPORT
    for k,x in result.items(): report=report.replace('@'+k+'@',format(x,'.16g'))
    assert '@' not in report
    new(OUT/'CONTRATO_DISPOSITIVO_E_LEI_RAIZ_R7.txt',report)
    new(OUT/'REVISAO_R7.txt',REVIEW)
    sources=[
        (ROOT/'Patentes/PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex',[(246,267),(298,370),(431,444),(611,629),(789,828)]),
        (ROOT/'Patentes/Psi_Net_Protocol_PI_INPI.tex',[(411,421),(476,521)]),
        (REDE/'CONTRATO_REDE_R2.json',[]),(REDE/'finite_device/PREREGISTRO_DEVICE_R1.json',[(84,122)]),
        (REDE/'finite_device/run_finite_device.py',[(155,187)]),
        (H/'A Ponte e o Um/A Ponte Einstein Cartan Miguel.tex',[(1886,1901),(2012,2025)]),
        (N/'um.py',[(119484,119493),(217043,217101),(217338,217348)]),
        (N/'um_absoluto_selo.json',[]),(H/'tgl_echo_smatrix.py',[(32,33),(83,96)]),
        (OUT.parent/'CONTRATO_RESPOSTA_R6/RESULTADO_R6.json',[]),
        (OUT.parent/'CONTRATO_RESPOSTA_R6/CONTRATO_E_RESULTADO_R6.txt',[])]
    new(OUT/'FONTES_R7.json',[dict(pin(p),read_ranges=r) for p,r in sources])
    reg.call([r'C:\IALD\NOS_VIVO\consultar.py','--unidade','F1.TEMPO'],'NOS_VIVO_R7.json')
    new(OUT/'MAP_BEFORE_R7.json',reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','ver','formal.tempo_consumacao_leitura_15out']))
    print(json.dumps({'report':pin(OUT/'CONTRATO_DISPOSITIVO_E_LEI_RAIZ_R7.txt'),'conditional_values':result},ensure_ascii=False))

def register():
    c=claim()
    for s in json.loads((OUT/'FONTES_R7.json').read_bytes()): assert pin(s['path'])['sha256']==s['sha256'],s['path']
    files=['CLAIM_R7.json','OPERADOR_R7_VERBATIM.txt','ARITMETICA_R7.json','CONTRATO_DISPOSITIVO_E_LEI_RAIZ_R7.txt','REVISAO_R7.txt','FONTES_R7.json','NOS_VIVO_R7.json','MAP_BEFORE_R7.json']
    delivery=OUT/'RESULTADO_R7.json'
    new(delivery,{'unit':UNIT,'author':WHO,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'CONTRATO_DOCUMENTAL_E_DERIVACAO_CONDICIONAL','files':[pin(OUT/f) for f in files]+[pin(__file__)],'sources_simulated':False,'new_lean_build':False,'external_provider_called':False,'production_changed':False,'gate_changed':False,'scope':'Device generator/actuator/detector recovered; conditional finite response, cascade and energy-root bound derived; physical mapping remains named.'})
    marker='time_device_energy_bridge_r7_20261015'
    note=f'''\n\n## 15/10/2026 — Tempo: portas do dispositivo e lei-raiz, R7\n<!-- {marker} -->\nEm nome de {WHO}, reivindicação825 de {UNIT}, adendo à seq1118. [REAL — fontes] Supercondutor:340–370 já tem H, salto J=a_out†sigma-+sigma+a_in e beta*gamma_Lambda D[J]; Omega_R é bombeamento de micro-ondas, distinto do EOM óptico. Fontes/detector já especificados; Psi-NET já codifica fonte/destino, sem duração física por salto.\n[DERIVED condicional] Resposta ao bombeamento: deltaI=epsilon*C*integral Tr[n_out exp((t-u)L_beta)(-i[sigma_x,rho_*])]f(u)du; h(0)=0. Preparação estacionária, calibração e detector são hipóteses. O termo holo isolado é não unital na cascata de uma excitação, diferindo de D[sqrtK]; uma ponte exige redução/identificação justificada. No controle analítico sem H/outras perdas, p_out=1-exp(-lambda*t)*(1+lambda*t), lambda=beta*gamma_Lambda, média de absorção2/lambda. Não é leitura de cliques ou resultado do aparelho completo.\n[DERIVED/INPUT] Sob H_SAME_ENERGY, mesmos níveis positivos em fase e lei-raiz, gamma/|nu|<=beta/2=0,0060156502. Com a sonda2D específica R6, isso implica atraso de fase negativo; não é a resposta APD do dispositivo nem sinal futuro. A demo com nu=1,3 usa ramo incompatível com essa identificação; somente amostras deixam alias em aberto. Zero energético pesa na lei-raiz. [OPEN] identificação física/redução, referência, estado e calibrações permanecem nomeados.\nEvidência imutável `{delivery}`, SHA256 `{pin(delivery)['sha256']}`. Revisão algébrica textual delimitada, sem simulação nova, Lean, provedor, produção ou gate; memórias com backup de bytes.\n'''
    new(OUT/'MEMORY_RECEIPT_R7.json',{'claim':c,'surfaces':[append_bytes(ROOT/'memory'/n,note,marker) for n in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md')]})
    entry={'tipo':'ANOTACAO','rota_id':'formal.tempo_consumacao_leitura_15out','dominio':'FORMAL','titulo':'R7: dispositivo fonte-receptor, obstrucao de unitalidade e limite da lei-raiz','resultado':'H/J e portas recuperados; resposta ao bombeamento escrita. Termo holo isolado difere de dephasing unital. Mesmas energias positivas em fase/raiz implicam gamma/|nu|<=beta/2; atraso negativo apenas sob a sonda2D nomeada, nao previsao APD.','estatuto':'REAL leitura / DERIVED condicional / INPUT / OPEN','status':'EXAMINADA','veredito':'CONTRATO_DOCUMENTADO__PONTE_FISICA_NOMEADA__SEM_RESULTADO_EXPERIMENTAL','proximo_passo':'Justificar reducao de gerador/instrumento ou manter modelos distintos; fixar calibracoes e estado antes de ensaio novo.','onde':str(OUT),'artefatos':[str(delivery),str(OUT/'CONTRATO_DISPOSITIVO_E_LEI_RAIZ_R7.txt'),str(OUT/'ARITMETICA_R7.json')],'refs':[1118],'olhou_dados':False}
    new(OUT/'MAP_ENTRY_R7.json',entry)
    m=reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',OUT/'MAP_ENTRY_R7.json','--quem',WHO],'MAP_RECEIPT_R7.json')
    b=reg.call([CLI,'avancar',UNIT,'--quem',WHO,'--status','ENTREGUE','--evidencia',delivery,'--nota','R7 leitura de dispositivos e derivacoes condicionais: fonte/receptor e obstrucao de geradores; nenhuma simulacao nova.'],'BOARD_DELIVERY_R7.json')
    ref=str(WORK/'ACOM_REFERENCE.json')
    p=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],payload={'operation':'project','reference':ref,'max_chars':48000})
    assert p['result']['receipt']['revision']==21
    tr={'operation':'transition','reference':ref,'expected_revision':21,'event_id':marker,'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':marker,'kind':'candidate','statute':'DECLARADO','text':'R7 fontes de Supercondutor/PsiNET localizadas. Derivacao condicional de resposta a Rabi microondas e leitura nout; termo holo nao unital difere de dephasing raiz. Controle cascata analitico, sem simular. H_SAME_ENERGY implica gamma/|nu|<=beta/2 e atraso de fase negativo na sonda2D R6; nao demonstra resposta APD nem entrada futura. Residuo: reducao/identificacao, zero energetico e calibracoes. Proxima acao desta frente: justificar ponte ou conservar modelos separados antes de ensaio. Demais fluxos/jobs preservados.','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']}]}]}}
    new(OUT/'ACOM_TRANSITION_R7.json',tr)
    a=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_RECEIPT_R7.json',tr);assert a['ok']
    rel=reg.call([CLI,'liberar',UNIT,'--quem',WHO,'--nota','R7 documental entregue; nenhum experimento/alteracao de producao.'],'RELEASE_R7.json')
    print(json.dumps({'map':m,'board':b,'acom_revision':a['result']['revision'],'release':rel},ensure_ascii=False))

if __name__=='__main__':
    {'prepare':prepare,'register':register}[sys.argv[1]]()
