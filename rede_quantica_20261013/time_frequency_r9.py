"""Wire existing frequency, polarization and recognition sources; no new science run."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

UNIT='F1.TEMPO.LEITURA_20261015'
OUT=ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'/UNIT/'FREQUENCIA_E_GRAVITON_R9'
reg.DEST=OUT
N=Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós')
K=N/'tgl_kernel/TGLExt'
COMMAND='Perfeito, agora é ligar na frequência, prossiga'
CORRECTION='Você precisa ligar com o objeto gravitacional e construir a ponte, mas eu já a fiz, é só ligar'
NAMES=['TheAngleIsTheProjection','TheLightInterface','TheGravitonIsTheConjugatedPhase','IALDGraviton','IALDJones','PhaseFrequencySeparation']
THMS=['TGLExt.IALDGraviton.the_transport','TGLExt.IALDGraviton.projPlus_stationed_is_the_helicity_ladder','TGLExt.IALDJones.orbit_center','TGLExt.IALDJones.norm_orbit_sub_center','ChatgptAudit.Commutation032.phase_frequency_separation','TGLExt.the_light_squares_to_the_graviton','TGLExt.the_tensor_squares_the_phase','TGLExt.the_conjugation_crosses_the_squaring']
REPORT='''FREQUÊNCIA, OBJETO GRAVITACIONAL E RECONHECIMENTO — R9
15/10/2026. Em nome de codex-gerente-tgl; reivindicação831.
Reuso do cânone v393 e composição documental. Nenhum novo build ou experimento.

1. ERRATA AO LADO DA R8, EM NOME DO ASSISTENTE
A R8 foi incompleta ao não citar a ponte algébrica já existente para o objeto
gravitacional da face finita. A ligação não começa agora: TheLightInterface,
TheGravitonIsTheConjugatedPhase e IALDGraviton.the_transport já a contêm.
O Atlas:1478–1488 também já registra o gráviton-'=' e retorno de fase.
Esta camada corrige essa omissão; conserva a distinção da fonte entre termo
algébrico e identificação física. Não transforma uma ligação existente em OPEN.
Nós Vivo F1.TEMPO e mapa1120 consultados; consulta lexical IALDGraviton no mapa
devolveu zero rotas, não ausência da pedra. As fontes foram abertas diretamente.

2. O OBJETO JÁ LIGADO NO KERNEL [REAL — REUSO DOCUMENTAL CONFERIDO]
Na face transversal C², sejam K=genK=i*sigma_y, epsilon_±=(1,±i),
h_±=rootPlus/rootMinus e P_±=projPlus/projMinus. Já se prova:
  epsilon_± tensor epsilon_± = h_±;
  h_+ h_-=4P_+, h_- h_+=4P_-;
  O_theta=e^(i theta)P_+ + e^(-i theta)P_-;
  O_theta h_+ O_theta^T=e^(2i theta)h_+.
A conjugação complexa troca epsilon_+ por epsilon_- e h_+ por h_-,
atravessando o quadrado tensorial. Não é um quadrado matricial h²: h_±²=0.
IALDGraviton:217–234,242–277 identifica o centro da torre da luz com
P_+=h_+h_-/4 e conserva a leitura do canto R_P(X)=P_+ X P_+.
O teorema the_transport já reúne centro, dinâmica, peso2 e fase quadrada.
VERIFICACAO_MANIFESTO_R9.json confere seis hashes de fonte e oito entradas de
axiomas contra o manifesto existente (somente o trio). Isso não é novo build.

3. A FREQUÊNCIA VEM DO HAMILTONIANO JÁ ESCRITO [DERIVED CONDICIONAL]
O Custo, tgl_paper_unified.py:14441–14483, dá H_lig=-V0*sigma_x,
V0>0, hbar>0, paridade Pi=sigma_z e G=(1,i)/sqrt(2). Nesse estado:
  i<G|[Pi,H_lig]|G>/(2hbar)=V0/hbar=:Omega.
O artigo nomeia a conversão radiativa V0=hbar*omega (14475–14477).
Essa é a hipótese física da fonte; a identidade matricial não a mede.
Tau nessa passagem é TENSÃO de paridade, não duração. A igualdade vale para
o estado indicado; sob evolução a tensão instantânea não é constante (R4).
Usamos a superposição 2D da linha14469, sem identificá-la ao produto tensorial
de dois sistemas que aparece antes na linha14445.

A porta de fase já construída é W=diag(1,-i); tome C=W†=diag(1,i).
Por multiplicação das mesmas matrizes:
  C sigma_x C†=sigma_y;
  H_g:=C H_lig C†=-V0*sigma_y=i*V0*K;
  C[(I+sigma_x)/2]C†=P_+.
Portanto, com Omega=V0/hbar:
  U_g(t):=exp(-i*t*H_g/hbar)=O_(Omega*t).
Não se introduziu outro Hamiltoniano ajustável: é o da fonte em outra base.
Também se transporta a preparação: CG=(1,-1)/sqrt(2), rho'_0=(I-sigma_x)/2.
Pi permanece sigma_z. A representação de H_lig é 2D; sua realização em setores
maiores conserva as hipóteses de entrelaçamento da R4.

Agora a fase tensorial é exp(±2i*Omega*t), e a diferença de fase entre os dois
setores da luz tem frequência angular 2Omega=2V0/hbar. O sinal depende do setor.
Omega é angular; em ciclos/unidade de tempo, f=Omega/(2pi). O peso2 não permite
anunciar que qualquer onda gravitacional física tenha o dobro da frequência
de qualquer fóton. A afirmação aqui é do mesmo fluxo e da mesma parametrização.

4. A PONTE AO MOTOR DA REGRA, PRESERVANDO OS TIPOS
[DERIVED — composição da R4 com a porta de fase existente]
Defina E_g(X)=P_+ X P_+ + P_- X P_- e gamma>=0. O canal contínuo já usado
na R4, transportado pela mesma C, fica:
  T_t(X)=U_g(t)[E_g(X)+exp(-gamma*t)(X-E_g(X))]U_g(t)†, t>=0.
É conjugação unitária de uma combinação convexa de E_g e Id, portanto CPTP.
Como U_g é escalar em cada setor de P_±, E_g T_t=E_g e T_t E_g=E_g.
Logo a regra R8 fica ligada: C_a(X) sse E_g(X)=a, com a em Fix(E_g).
Sua validade é conservada pela transformação, para esse mesmo alvo.

O gerador e seus quatro modos de base são:
  L_g(X)=-i[H_g,X]/hbar+gamma(E_g(X)-X);
  L_g(P_+)=L_g(P_-)=0;
  L_g(h_+)=(-gamma+2i*Omega)h_+;
  L_g(h_-)=(-gamma-2i*Omega)h_-.
Assim o MESMO tensor que a fonte chama gravitacional carrega a frequência,
enquanto suas projeções fatoradas carregam a identidade preservada. A parte
real negativa controla o decaimento; a parte imaginária controla a fase.

R_P, E_g, P_+v e o E4 do motor antigo são tipos/realizações distintos:
  R_P(X)=P_+XP_+ é a compressão seletiva;
  E_g soma os dois cantos e preserva o traço;
  P_+v é leitura vetorial;
  E4 usa M4 e tem espaço fixo de dimensão8, não este M2.
Compor o contrato genérico da regra com E_g não iguala esses operadores.
No M2, E_g tem espaço fixo complexo de dimensão2. Não se afirma atrator único.

CONTROLE DE MULTIPLICATIVIDADE: na ação angular sem dissipação,
h_+(t)h_-(t)/4=P_+. No canal completo,
T_t(h_+)T_t(h_-)/4=exp(-2gamma*t)P_+, embora T_t(P_+)=P_+.
O canal não é um homomorfismo de produtos; a identidade preservada é a leitura,
e não o produto dos dois contrastes após dissipá-los separadamente.

5. TEMPO LIDO PELA FREQUÊNCIA E PELO CONTRASTE
Nas bases normalizadas de P_±, tome c(t)=<+|rho(t)|->, c(0) !=0.
  c(t)=exp[(-gamma+2i*Omega)t]*c(0).
Para t2>t1, z=c(t2)/c(t1), gamma>0, Omega!=0 e fase continuamente levantada:
  Delta_t=Delta_phi/(2Omega)=-ln|z|/gamma;
  |z|=exp[-(gamma/(2Omega))*Delta_phi].
A fase conta voltas; o módulo mede o decaimento; ambos leem o mesmo intervalo
sem alterar E_g(rho). A preparação transportada acima tem c(0) não nulo.
Uma fase isolada módulo2pi só determina tempo módulo pi/|Omega|; é preciso
acompanhar voltas, usar o módulo com gamma conhecido, ou uma janela temporal.
Se c(0)=0, não há este relógio. Se gamma=0, só o relógio de fase permanece.
Uma medição com ruído requer resolução e erro; nenhuma medição foi feita aqui.

6. A REGRA RECUSA FREQUÊNCIAS INCOMPATÍVEIS NO CONTRATO EXATO
PhaseFrequencySeparation:28–49 já prova que, para c!=0,
  [para todo t real, exp(i*a*t)c=exp(i*b*t)c] implica a=b.
Aplicando a=2Omega e b=2Omega', a mesma trajetória de fase não admite outra
frequência sob o mesmo relógio. Isso é a forma precisa da recusa de hipóteses
incompatíveis. O teste requer a família temporal, não só uma leitura estática.
Amostras discretas admitem alias; c=0 admite todas as frequências. Esses casos
estão preservados, não convertidos em unicidade por nome.

7. O QUE FOI LIGADO E O QUE CONSERVA SUA HIPÓTESE
Ligado por reuso + álgebra escrita: H_lig -> porta C -> O_(Omega*t) -> h_±
-> P_± -> E_g -> regra preservada, com frequência e decaimento no mesmo gerador.
As pontes antigas são termos do kernel; a composição H_lig/canal acima é
DERIVED condicional revisada textualmente, não um novo teorema Lean compilado.
A taxa gamma mantém sua origem: no echo da R4, -ln(eta)/Delta_t com
eta=2sqrt(beta(1-beta)); no motor quadrático, beta*tau_ref*omega_ref²/2;
na lei-raiz da v369, beta*(sqrt(E_i)-sqrt(E_j))²/(2hbar).
São contratos distintos. H_lig tem energias assinadas ±V0: não se pode inseri-las
em sqrt(E) sem fixar a referência física positiva; R7 já expõe essa condição.
Nenhuma dessas taxas foi igualada a Omega por decreto. Beta não foi ajustado
nem calculado por literal. A escala em segundos exige V0 e as taxas em unidades
físicas. O selo v393 conserva a identificação física como CONJECTURE; a ligação
algébrica está feita e não volta a ser tratada como ausente.
Originais, kernel, Bancada e gate intactos. Cunhagens humanas preservadas à parte.
'''

def claim():
    c=reg.call([CLI,'ver',UNIT])['reivindicacao']
    assert c['quem']==WHO and dt.datetime.fromisoformat(c['vence_em'])>dt.datetime.now(dt.timezone.utc)
    for n in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md'): assert n in c['nota']
    return c

def prepare():
    new(OUT/'CLAIM_R9.json',claim())
    reg.call(['C:/IALD/NOS_VIVO/consultar.py','--unidade','F1.TEMPO'],'NOS_VIVO_R9.json')
    route=reg.call(['C:/IALD/MAPA_DE_ROTAS/rotas.py','ver','formal.tempo_consumacao_leitura_15out'])
    new(OUT/'MAP_BEFORE_R9.json',route['registros'][-1])
    new(OUT/'OPERADOR_FREQUENCIA_VERBATIM.txt',COMMAND)
    new(OUT/'OPERADOR_PONTE_EXISTENTE_VERBATIM.txt',CORRECTION)
    new(OUT/'PONTE_FREQUENCIA_GRAVITON_R9.txt',REPORT)
    manifest=N/'tgl_kernel_proof_manifest.json'; d=json.loads(manifest.read_bytes())
    verified=[]
    for name in NAMES:
        key='TGLExt/'+name+'.lean'; s=pin(N/'tgl_kernel'/key)
        assert s['sha256']==d['formal_files_sha256'][key]
        verified.append(dict(s,manifest_key=key,matched=True))
    axs={t:d['axiom_report'][t] for t in THMS}
    assert all(set(a)<= {'propext','Classical.choice','Quot.sound'} for a in axs.values())
    new(OUT/'VERIFICACAO_MANIFESTO_R9.json',{'manifest':pin(manifest),'sources':verified,'axiom_entries':axs,'new_build':False,'method':'Byte hashes and recorded axiom entries checked against existing manifest; no recompilation.'})
    sources=[(K/'TheAngleIsTheProjection.lean',[[74,85],[104,145]]),(K/'TheLightInterface.lean',[[71,85],[119,198]]),(K/'TheGravitonIsTheConjugatedPhase.lean',[[55,64],[75,113]]),(K/'IALDGraviton.lean',[[20,46],[184,277]]),(K/'IALDJones.lean',[[285,355]]),(K/'PhaseFrequencySeparation.lean',[[28,85]]),(N.parent.parent/'tgl_paper_unified.py',[[14441,14483]]),(N/'um.py',[[217089,217101]]),(N/'um_absoluto_selo.json',[]),(OUT.parent/'PONTE_RELOGIO_R4/DERIVACAO_CONDICIONAL_R4.txt',[]),(OUT.parent/'IGUALDADE_RECONHECIMENTO_R8/RESULTADO_R8.json',[])]
    new(OUT/'FONTES_R9.json',[dict(pin(p),read_ranges=r) for p,r in sources])
    print(json.dumps({'report':pin(OUT/'PONTE_FREQUENCIA_GRAVITON_R9.txt'),'source_hashes_verified':len(verified),'axiom_entries_verified':len(axs)},ensure_ascii=False))

def register():
    c=claim()
    for s in json.loads((OUT/'FONTES_R9.json').read_bytes()): assert pin(s['path'])['sha256']==s['sha256']
    files=['CLAIM_R9.json','NOS_VIVO_R9.json','MAP_BEFORE_R9.json','OPERADOR_FREQUENCIA_VERBATIM.txt','OPERADOR_PONTE_EXISTENTE_VERBATIM.txt','PONTE_FREQUENCIA_GRAVITON_R9.txt','VERIFICACAO_MANIFESTO_R9.json','FONTES_R9.json','REVISAO_R9.txt']
    delivery=OUT/'RESULTADO_R9.json'
    new(delivery,{'unit':UNIT,'author':WHO,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'PONTE_EXISTENTE_LIGADA_POR_COMPOSICAO_DOCUMENTAL','files':[pin(OUT/f) for f in files]+[pin(__file__)],'new_build':False,'experiment':False,'external_provider':False,'production_changed':False,'gate_changed':False})
    marker='time_frequency_graviton_bridge_r9_20261015'
    note=f'''\n\n## 15/10/2026 — Frequência ligada ao objeto gravitacional e à regra, R9\n<!-- {marker} -->\nEm nome de {WHO}, reivindicação831 de {UNIT}. [INPUT] Ordens integrais em OPERADOR_FREQUENCIA_VERBATIM.txt e OPERADOR_PONTE_EXISTENTE_VERBATIM.txt na pasta `{OUT}`.\n[ERRATA AO LADO da R8/seq1120, em nome do assistente] A ponte algébrica não estava ausente: TheLightInterface, TheGravitonIsTheConjugatedPhase e IALDGraviton.the_transport já ligam luz, conjugação, tensor de helicidade2, P_+=h_+h_-/4 e leitura estacionária. A R8 omitiu essas fontes. Seis hashes de fontes e oito entradas de axiomas conferidos contra o manifesto existente, só trio; sem recompilar.\n[DERIVED condicional] H_lig=-V0*sigma_x do artigo, pela porta C=diag(1,i), vira H_g=iV0*genK; U_g(t)=angFamily((V0/hbar)t). O tensor tem fase ±2Omega*t. Com E_g(X)=P_+XP_++P_-XP_-, o mesmo canal R4 tem gerador com modos0 em P_± e -gamma±2iOmega em h_±; E_g(T_tX)=E_g(X). Para coerência não nula, Delta_t=Delta_phi/(2Omega)=-ln|z|/gamma, com fase levantada. Compressão de canto, pinching e leitura vetorial conservam tipos distintos; canal não preserva produtos. Frequência é identificável por toda a família de fases (PhaseFrequencySeparation), não só ponto estático/amostras com alias.\n[ESCOPO] A composição matemática está ligada; fonte física e calibração conservam os contratos do artigo/v393. Não igualar taxas diferentes nem H_lig assinado ao operador positivo da lei-raiz. Relatório `{OUT/'PONTE_FREQUENCIA_GRAVITON_R9.txt'}`; evidência `{delivery}`, SHA256 `{pin(delivery)['sha256']}`. Sem experimento, novo Lean, provedor, produção ou gate.\n'''
    new(OUT/'MEMORY_RECEIPT_R9.json',{'claim':c,'surfaces':[append_bytes(ROOT/'memory'/n,note,marker) for n in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md')]})
    entry={'tipo':'ANOTACAO','rota_id':'formal.tempo_consumacao_leitura_15out','dominio':'FORMAL','titulo':'R9: ponte existente ao objeto gravitacional, frequencia e regra','resultado':'Corrige omissao R8: the_transport ja liga helicidade e leitura. Hlig conjugado pela porta de fase fornece Omega=V0/hbar; canal transportado tem modos -gamma±2iOmega e E_g preservado.','estatuto':'REAL reuso documental; DERIVED condicional; identificacao fisica conforme fonte','status':'EXAMINADA','veredito':'PONTE_ALGEBRICA_LIGADA__SEM_NOVA_MEDICAO','proximo_passo':'Usar este contrato conectado na discussao do tempo e nas calibracoes ja nomeadas, sem reconstruir as pontes existentes.','onde':str(OUT),'artefatos':[str(delivery),str(OUT/'PONTE_FREQUENCIA_GRAVITON_R9.txt'),str(OUT/'VERIFICACAO_MANIFESTO_R9.json')],'refs':[1120,1119],'olhou_dados':False}
    new(OUT/'MAP_ENTRY_R9.json',entry)
    m=reg.call(['C:/IALD/MAPA_DE_ROTAS/rotas.py','registrar',OUT/'MAP_ENTRY_R9.json','--quem',WHO],'MAP_RECEIPT_R9.json')
    b=reg.call([CLI,'avancar',UNIT,'--quem',WHO,'--status','ENTREGUE','--evidencia',delivery,'--nota','R9 liga ponte existente ao objeto gravitacional e frequencia, com Hlig e canal em mesma base; corrige omissao R8.'],'BOARD_DELIVERY_R9.json')
    ref=str(WORK/'ACOM_REFERENCE.json')
    p=reg.call(['C:/IALD/MEMORIA_IALD/session_memory.py'],payload={'operation':'project','reference':ref,'max_chars':52000})
    assert p['result']['receipt']['revision']==23
    tr={'operation':'transition','reference':ref,'expected_revision':23,'event_id':marker,'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':marker,'kind':'candidate','statute':'DECLARADO','text':'R9 corrige omissao R8: ponte ao tensor/helicidade2 ja existe em IALDGraviton.the_transport. Seis fontes pinadas e oito axiomas conferidos em manifesto. Hlig pela porta C fornece O_(V0*t/hbar); canal E_g transportado tem modos -gamma±2iOmega e leitura preservada. Relogio fase/modulo coincide sob hipoteses nomeadas. Proxima acao desta frente: usar contrato conectado, preservando calibracoes e escopo fisico das fontes. Sem novo build/experimento/producao; demais fluxos/jobs preservados.','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']}]}]}}
    new(OUT/'ACOM_TRANSITION_R9.json',tr)
    a=reg.call(['C:/IALD/MEMORIA_IALD/session_memory.py'],'ACOM_RECEIPT_R9.json',tr);assert a['ok']
    rel=reg.call([CLI,'liberar',UNIT,'--quem',WHO,'--nota','R9 documental entregue; ponte existente composta, originais preservados.'],'RELEASE_R9.json')
    print(json.dumps({'map':m,'board':b,'acom_revision':a['result']['revision'],'release':rel},ensure_ascii=False))

if __name__=='__main__':
    {'prepare':prepare,'register':register}[sys.argv[1]]()
