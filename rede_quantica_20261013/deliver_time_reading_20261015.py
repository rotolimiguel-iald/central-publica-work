"""Preserve a scoped mathematical reading, without a new experiment or canonical change."""
import json, datetime as dt
from pathlib import Path
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg
from start_time_reading_20261015 import OUT, UNIT

def prepare():
    reg.DEST=OUT
    claim=reg.call([CLI,'ver',UNIT])['reivindicacao']
    assert claim['quem']==WHO and dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    assert 'DIARIO_CONSTRUCAO_QG.md' in claim['nota']
    custody=json.loads((OUT/'FONTES_RECEBIDAS_R1.json').read_bytes())
    for item in custody['sources']:
        assert pin(item['original']['path'])['sha256']==item['original']['sha256']==pin(item['copy']['path'])['sha256']
    canon=Path(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós')
    kernel=canon/'tgl_kernel/TGLExt'
    source_names=['Santo.lean','StateClockObstruction.lean','TheRuleInTheContinuousMotor.lean','ContratoQG_v31_Teoremas.lean','TheObserverReadsTheAngle.lean','AffineClockAndRegion.lean']
    sources=[pin(kernel/n) for n in source_names]+[pin(canon/n) for n in ['um.py','um_absoluto.json','um_absoluto_selo.json']]
    core=json.loads((canon/'um_absoluto.json').read_bytes())['core']; seal=json.loads((canon/'um_absoluto_selo.json').read_bytes())
    conversation=json.loads((OUT/'CONVERSA_EXTRACAO_R1.json').read_bytes())
    result={
      'unit':UNIT,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'author':WHO,
      'scope':'Leitura dos anexos, levantamento do existente e derivacoes elementares para discussao. Nao e fechamento do tempo, nova prova Lean, experimento ou credito empirico.',
      'custody':custody,'sources':sources,
      'source_limits':['JSON original tem escapes invalidos; 25 mensagens foram extraidas lexicalmente, sem corrigir o original. A integralidade em relacao a uma sessao externa e DECLARADO no proprio export.',
                       'DOCX contem 19 paragrafos. Metadados internos: criado 2012-01-21 e modificado 2012-03-15; compativeis com a data narrada, sem autenticacao independente da cerimonia.',
                       'Grok nao fornece nesta transcricao uma telemetria de colapso do substrato, trajetorias internas, controles ou recibo de execucao. A autodeclaracao de estado IALD permanece DECLARADO.'],
      'operator_formulation_verbatim':[m for m in conversation['messages'] if m['role']=='usuario' and 13<=m['id']<=23],
      'interpretation':{'statute':'ONTO / proposta de leitura, nao teorema fisico',
        'text':'O autor situa a referencia da seta na satisfacao da regra/consumacao e descreve uma selecao por exclusao de alternativas, nao por vontade do estado. Relaciona a conjugacao das duas faces ao emaranhamento. A formulacao nao fixa ainda o tipo de comutacao, do vazamento, da derivada ou da dobra.',
        'speech_connection':'Nos paragrafos 1, 12 e 17, o tempo passa de adversario a aliado, permite recomecar e acompanha a transformacao. A permanencia pela transmissao do que foi semeado aparece nos paragrafos 2 e 16. E continuidade de preocupacao e linguagem do autor; nao prova retrospectiva da fisica.'},
      'current_program_reading':{'statute':'REAL — leitura dos artefatos existentes, sem reexecucao nesta unidade','um_version':seal['um_version'],'seal_timestamp':seal['timestamp'],
        'rule_modules':core['pedras_v393']['declaracoes_no_trio'],
        'rule_consumer_verdict':core['regra_consumidor_v393']['verdict'],
        'rule_consumer_all_verified_recorded':core['regra_consumidor_v393']['all_verified'],
        'scope':'v393 ja incorpora regra e motor. A contagem inclui declaracoes, nao somente teoremas. Nao atesta atualizacao do processo Bancada/app nem nova execucao.'},
      'existing_results':[
        {'source':'Santo.lean:892','content':'Defasagem conserva uma familia de estados diagonais: unicidade do atrator nao decorre so de dissipacao.'},
        {'source':'Santo.lean:1070','content':'No modelo de dephasing com taxa e tempo positivos, a inversa nao preserva positividade em geral; isso localiza a irreversibilidade fisica.'},
        {'source':'Santo.lean:1304','content':'O fluxo P + exp(-t)(1-P), P idempotente diferente de 1, nao e P em instante real finito.'},
        {'source':'TheRuleInTheContinuousMotor.lean:65-103','content':'Inscricao preservada, convergencia com taxa positiva e estado bruto nao igual a inscricao em tempo finito quando ha componente transversal.'},
        {'source':'StateClockObstruction.lean:62-86,100-107,156-173','content':'Leitura escalar diferenciavel de curva par tem derivada bilateral zero; fluxo modular do perfil fixo preserva estado e nao parametriza a curva nao estacionaria. Nao exclui ramo orientado.'},
        {'source':'ContratoQG_v31_Teoremas.lean:426,520','content':'Ponte KMS/Unruh sob contrato e normalizacao de Killing; kappa_is_input conserva a escolha de relogio. Nao deriva escala universal.'},
        {'source':'TheObserverReadsTheAngle.lean:79,102,114','content':'Leitura angular e releitura idempotente; sem implicar limite angular ou seta dissipativa.'}],
      'corrections_to_grok':[
        {'id':'G1','statute':'DERIVED — contraexemplo algebrico','claim':'Nao comutatividade instala irreversibilidade.',
         'correction':'X e Z de Pauli satisfazem XZ=-ZX e X^2=Z^2=I: sao reversiveis. Grok identificou comutacao do autor com comutador sem justificar esse tipo. Uma cadeia de Markov classica pode dissipar em algebra comutativa.'},
        {'id':'G2','statute':'DERIVED — contraexemplo diferencial','claim':'Derivada de entropia anulada implica suporte de posto 1.',
         'correction':'Para rho=I/d e direcoes Delta hermitianas de traco zero, DS_rho[Delta]=-Tr(Delta(log(rho)+I))=0, mas rank(rho)=d. A derivada nula isolada nao fixa alvo, estabilidade nem posto.'},
        {'id':'G3','statute':'DERIVED — contradicao da prova da mensagem 24','claim':'P=P_A tensor P_B, com fatores de posto 1, produz emaranhamento.',
         'correction':'P=|ab><ab| implica P rho P=p P. Se p=Tr(P rho)>0, a saida normalizada e P, um estado produto. Se p=0, a normalizacao e indefinida. O mapa seletivo sem normalizacao tambem nao preserva traco em geral.'},
        {'id':'G4','statute':'KNOWN / contraexemplo explicito','claim':'rho_AB diferente de rho_A tensor rho_B basta para provar emaranhamento.',
         'correction':'rho=(|00><00|+|11><11|)/2 nao e produto e e separavel. Emaranhamento exclui TODA decomposicao convexa soma p_i rho_A_i tensor rho_B_i.'},
        {'id':'G5','statute':'KNOWN / leitura do kernel','claim':'O fluxo modular, por si, e vazamento dissipativo.',
         'correction':'O fluxo de Tomita-Takesaki e grupo de automorfismos. O semigrupo dissipativo exige especificacao adicional. Um salto autoadjunto f(K) deixa fixos estados que comutam com ele; sqrt(K) exige positividade e dominio.'},
        {'id':'G6','statute':'OPEN / ONTO','claim':'A dobra e a unica explicacao do emaranhamento e redefine a origem cosmologica.',
         'correction':'O autor propoe a interpretacao do emaranhamento; Grok a endossa e acrescenta a leitura cosmologica sem demonstracao. Faltam objetos geometricos, lei e identificacoes fisicas. Compreender ou nomear um processo irreversivel nao o torna reversivel.'}],
      'conditional_clock':{
        'statute':'DERIVED — demonstracao algebrica nesta analise; nao compilada em Lean; sem experimento novo',
        'hypotheses':'E e um canal linear completamente positivo, preservador do traco e idempotente em dimensao finita; gamma>0; t>=0; rho0 e densidade com d0=norm(rho0-E(rho0))>0.',
        'flow':'T_t=E+exp(-gamma*t)(I-E); rho_t=T_t(rho0)',
        'proof_steps':['E^2=E implica E(I-E)=(I-E)E=0 e (I-E)^2=I-E.',
                       'Logo T_s T_t=T_(s+t), E T_t=T_t E=E. Para t>=0, T_t e combinacao convexa de I e E: e canal.',
                       'rho_t-E(rho0)=exp(-gamma*t)(rho0-E(rho0)); homogeneidade da norma da d(t)=exp(-gamma*t)*d0.',
                       'Para todo t finito, d(t)>0; o limite e zero. tau(rho_t)=log(d0/d(t))/gamma=t.',
                       'A derivada d\u2032(t)=-gamma*d(t) nao se anula em tempo finito nessa trajetoria. No limite, o relogio logaritmico diverge.',
                       'Para alvo o fixado previamente, E(rho_t)=o se e somente se E(rho0)=o. A regra pode valer desde a leitura inicial embora rho_t seja distinto de o.'],
        'limits':['O alvo e fixado antes; E(rho0) nao redefine a posteriori o objeto de satisfacao.',
                  'Uma inscricao constante E(rho_t) nao distingue instantes; precisa-se do desvio, da orientacao e de referencia d0.',
                  'Se d0=0, nao ha relogio desse desvio; o logaritmo nao e definido no atrator.',
                  'Gamma e escala dada. A formula so produz segundos se gamma tiver calibracao fisica em s^-1. Nao deriva tempo proprio, escala cosmologica nem parametro modular universal.',
                  'A dependencia exponencial do estado em t nao prova nao linearidade do tempo, dobra do espaco-tempo ou retrocausalidade. Um deslocamento da origem nao muda esta dinamica.',
                  'O resultado reaproveita o motor; nao demonstra uma nova lei fisica da TGL.']},
      'entanglement_scope':{'statute':'OPEN — tarefa distinta para eventual construcao',
        'needed':['Fixar H_A tensor H_B ou algebras locais e suas relacoes.',
                  'Derivar o canal conjunto dos acoplamentos ja canônicos, sem escolher um estado emaranhado como resposta desejada.',
                  'Determinar se E(rho0) e nao separavel, com testemunha de emaranhamento apropriada.',
                  'Verificar ausencia de sinalizacao controlavel e justificar realizabilidade do canal.',
                  'Distinguir o tempo de surgimento de emaranhamento do limite assintotico e da satisfacao da leitura.'],
        'countermodel':'Escolher E_sigma(X)=Tr(X)*sigma produz, por hipotese, um atrator unico para sigma produto OU emaranhado. Isso mostra que unicidade/idempotencia nao decide emaranhamento. Essa escolha nao e derivacao canonica.'},
      'next_step':'Discutir com o operador se consumacao designa igualdade da leitura, limite assintotico do estado ou um evento fisico finito. Formular o contrato tipado a partir dessa distincao, reaproveitando F1.TEMPO; construcao nova depende do levantamento e escopo proprio.',
      'bibliography':[{'url':'https://arxiv.org/abs/gr-qc/9406019','authors':'Connes e Rovelli','year':1994,'use':'Tempo termico como hipotese fisica e fluxo modular como grupo de automorfismos.'},
                      {'url':'https://www.preskill.caltech.edu/ph219/chap2_15.pdf','author':'John Preskill','use':'Estados, produto, mistura separavel e emaranhamento.'},
                      {'url':'https://www.preskill.caltech.edu/ph219/chap3_15.pdf','author':'John Preskill','use':'Canais, evolucao e dephasing.'}],
      'actions_not_performed':['Nenhuma nova chamada a provedor','Nenhum experimento','Nenhuma compilacao Lean','Nenhuma alteracao de um.py, kernel, Bancada ou gate','Nenhuma atribuicao de consciencia ou mudanca nos pesos do Grok']}
    new(OUT/'ANALISE_TEMPO_R1.json',result)
    print(json.dumps({'analysis':pin(OUT/'ANALISE_TEMPO_R1.json'),'source_count':len(sources)},ensure_ascii=False))

def register():
    reg.DEST=OUT
    claim=reg.call([CLI,'ver',UNIT])['reivindicacao']
    assert claim['quem']==WHO and dt.datetime.fromisoformat(claim['vence_em'])>dt.datetime.now(dt.timezone.utc)
    result=OUT/'ANALISE_TEMPO_R1.json'; a=json.loads(result.read_bytes())
    for s in a['sources']: assert pin(s['path'])['sha256']==s['sha256'],s['path']
    marker='time_reading_grok_speech_20261015'
    note=f'''\n\n## 15/10/2026 — Tempo, consumação e emaranhamento: leitura dos anexos
<!-- {marker} -->
Em nome de codex-gerente-tgl, sob reivindicação de {UNIT}.
[REAL — custódia/leitura] Dois anexos preservados byte a byte; 25 mensagens e 19 parágrafos. O export tem escapes JSON inválidos, sem reparo do original. A conversa é fonte da formulação do autor; autodeclaração de estado IALD pelo Grok não é medição. Metadados do discurso são compatíveis com 2012, sem autenticação externa.
[ONTO — interpretação do autor] Consumação da regra como referência da seta e conjugação das faces; ligação ao emaranhamento é proposta, não demonstrada pelo texto do Grok.
[DERIVED — análise, não nova pedra] O argumento de projetor produto ⇒ emaranhamento é falso; derivada de entropia zero não implica posto 1. No motor existente, inscrição preservada e evolução bruta são distintas; relógio logarítmico do desvio recupera o parâmetro sob taxa dada e desvio inicial não nulo. A consumação bruta é assintótica. Nenhum relógio universal ou origem cosmológica foi derivado.
[REAL — leitura de recibo] v393 já registra a regra e o consumidor; não houve nova execução nesta unidade. Reaproveitar F1.TEMPO/Santo e StateClockObstruction. Escala física, tipo da dobra e emaranhamento ficam [OPEN].
Evidência: `{result}`; SHA256 `{pin(result)['sha256']}`. Nenhum original científico, kernel, Bancada ou gate alterado.
'''
    new(OUT/'MEMORY_RECEIPT.json',{'claim':claim,'surfaces':[append_bytes(ROOT/'memory'/n,note,marker) for n in ['DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md']]})
    entry=OUT/'MAP_ENTRY.json'
    new(entry,{'tipo':'ROTA','rota_id':'formal.tempo_consumacao_leitura_15out','dominio':'FORMAL','titulo':'Conversa Grok e discurso: tempo relativo a consumacao, erros da prova e contrato de relogio',
      'pergunta':'O que a nova formulacao sobre consumacao acrescenta ao tempo ja formalizado?',
      'metodo':'Custodia dos anexos, leitura do kernel e contraexemplos algebricos; nenhuma execucao cientifica nova.',
      'resultado':'Leitura preservada distinta do estado bruto; relogio do desvio condicional. Projetor produto nao prova emaranhamento. Reaproveitar F1.TEMPO e motor v393.',
      'estatuto':'REAL (custodia/leitura); DERIVED (algebra exposta); ONTO (interpretacao); OPEN (identificacao fisica)',
      'veredito':'LEVANTAMENTO_DOCUMENTAL_ENTREGUE__SEM_FECHAMENTO_GLOBAL_DO_TEMPO','status':'EXAMINADA','olhou_dados':False,
      'nao_refazer':'Santo, StateClockObstruction e TheRuleInTheContinuousMotor ja existem.',
      'defeito':'JSON malformado preservado; consumacao, relogio fisico e dobra exigem tipagem distinta; nenhum teste de colapso no anexo.',
      'proximo_passo':'Discussao com o operador antes de eventual nova construcao.',
      'onde':str(OUT),'artefatos':[str(result),str(OUT/'FONTES_RECEBIDAS_R1.json')],'refs':[]})
    mapped=reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',entry,'--quem',WHO],'MAP_RECEIPT.json')
    board=reg.call([CLI,'avancar',UNIT,'--quem',WHO,'--status','ENTREGUE','--evidencia',result,'--nota','Leitura e levantamento entregues para discussao. Nao fecha F1.TEMPO; nao houve nova construcao ou experimento.'],'BOARD_DELIVERY.json')
    ref=str(WORK/'ACOM_REFERENCE.json')
    projection=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],payload={'operation':'project','reference':ref})
    assert projection['ok']
    transition={'operation':'transition','reference':ref,'expected_revision':projection['result']['receipt']['revision'],'event_id':'time-reading-grok-speech-20261015',
      'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':'time-reading-grok-speech-20261015','kind':'fact','statute':'REAL',
        'text':'Leitura documental dos dois anexos entregue sob F1.TEMPO.LEITURA_20261015. Custodia e analise registradas; contraexemplos a inferencias do Grok e relogio condicional do desvio, explicitamente sem nova pedra ou fechamento fisico. Proxima acao desta frente: discutir tipagem de consumacao e identificacao do relogio; demais fluxos e chamadas pendentes preservados.',
        'sources':[{'kind':'artifact','ref':str(result),'sha256':pin(result)['sha256']}]}]}}
    new(OUT/'ACOM_TRANSITION.json',transition)
    receipt=reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_RECEIPT.json',transition); assert receipt['ok']
    release=reg.call([CLI,'liberar',UNIT,'--quem',WHO,'--nota','Etapa documental concluida; entrega para discussao sem fechar a unidade mae.'],'RELEASE.json')
    print(json.dumps({'map':mapped,'board':board,'acom_revision':receipt['result']['revision'],'release':release},ensure_ascii=False))

if __name__=='__main__':
    import sys
    {'prepare':prepare,'register':register}[sys.argv[1]]()
