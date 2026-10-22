"""Prepare and deliver the authorized time/frequency handoff to Claude c1."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

UNIT = 'F1.TEMPO.LEITURA_20261015'
BASE = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'
FRONT = BASE/UNIT
OUT = FRONT/'ENCAMINHAMENTO_V394_20261015'
reg.DEST = OUT
ORDER = 'Você precisa passar tudo isso ao Claude para a v 394, e mais, o que ainda falta provar, porque agora resolvemos por\nCompleto a passagem\nDo contínuo , não é mais condicional, é derivado'
MARKER = 'time_frequency_claude_v394_handoff_20261015'
SURFACES = [ROOT/'memory'/n for n in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md')] + [BASE/'AVISO_GERENCIA.md']
PRIMARY = ['ANALISE_TEMPO_R1.json','RETORNO_FASE_R2/LEITURA_R2.json','PRIMEIRA_LEI_R3/LEITURA_PRIMEIRA_LEI_R3.json','PONTE_RELOGIO_R4/RESULTADO_R4.json','LEVANTAMENTO_TRES_ARTIGOS_R5/RESULTADO_R5.json','CONTRATO_RESPOSTA_R6/RESULTADO_R6.json','DISPOSITIVO_E_ESPECTRO_R7/RESULTADO_R7.json','IGUALDADE_RECONHECIMENTO_R8/RESULTADO_R8.json','FREQUENCIA_E_GRAVITON_R9/RESULTADO_R9.json']

REVIEW = '''REVISÃO INDEPENDENTE DE ESCOPO — /root/tempo_math_review, 15/10/2026
Síntese do retorno textual do subagente, preservado no histórico desta tarefa; notação matemática normalizada pelo coordenador. Não é verbatim. Sem nova compilação ou experimento.
1. PASS_WITH_SCOPE: “passagem ao contínuo DERIVADA” é correto como construção e dedução do semigrupo no modelo M₂ especificado.
2. Na R9, §§3–4, a porta C transporta o Hamiltoniano existente: H_g=iV₀K, U_g(t)=O_(Ωt), Ω=V₀/ℏ; essa identificação matricial está demonstrada.
3. O canal T_t, sua propriedade CPTP, composição temporal, gerador e modos 0,0,−γ±2iΩ seguem por álgebra desse contrato.
4. Também seguem E_g T_t=E_g, preservação da regra e os relógios de fase/módulo quando a coerência inicial não é nula.
5. V₀>0, ℏ>0, γ≥0 e t≥0 são parâmetros/domínios do modelo; γ>0 e Ω≠0 são condições adicionais dos dois relógios simultâneos.
6. A hipótese espectral da R4 foi realizada pela conjugação C; não deve continuar apresentada como ausência da ponte matricial.
7. Não foi derivada unicidade de toda extensão contínua a partir de amostras: a R4 preserva os ramos de frequência que dão o mesmo canal discreto.
8. O Hamiltoniano especificado seleciona o fluxo considerado; a constância da leitura, sozinha, não seleciona frequência, taxa ou unidade temporal.
9. A ponte dimensional pendente é atribuir V₀, γ e o parâmetro temporal ao mesmo sistema físico e relógio calibrado, preservando as origens distintas das taxas.
10. A identificação do tensor transversal com o objeto gravitacional físico conserva o estatuto da fonte; a ligação algébrica ao tensor já existe.
11. A lei-raiz exige referência energética positiva fixada: os níveis assinados ±V₀ não podem ser inseridos diretamente em √E.
12. Ainda não compilado como nova composição Lean: transporte de H_lig por C, canal E_g, gerador/modalidades, instanciação da regra e reconstrução temporal reunidos no contrato R9.
13. As pedras anteriores são reutilizadas; revisão textual e verificação de manifesto não equivalem a esse novo build.
14. Formulação recomendada: “Derivamos o semigrupo contínuo e seu relógio no modelo M₂ ligado ao Hamiltoniano da fonte; a composição está demonstrada por escrito e aguarda formalização Lean e a identificação física especificada.”
'''

BODY = '''# AO CLAUDE / GERÊNCIA c1 — tempo, frequência, regra e objeto gravitacional para v394

[REAL — entrega documental; DERIVED — composição matemática em M₂; OPEN — nova composição Lean e identificação física especificada]
De: codex-gerente-tgl. Para: claude-c1. Data: 15/10/2026.
Canal: túnel oficial + AVISO_GERENCIA + quadro. Integração solicitada pelo operador; leitura e aceite do destinatário ainda não atestados.

## 1. Leitura vigente, ao lado das R4 e R9

**Derivamos o semigrupo contínuo e seu relógio no modelo M₂ ligado ao Hamiltoniano da fonte.**
A hipótese espectral H_ESPELHO_ESPECTRAL da R4 ganhou uma realização explícita pela porta de fase C da R9. Não a registrar mais como ponte matricial ausente. O objeto tensorial, o fator de helicidade dois e sua ligação a P₊ já estavam no kernel, especialmente em IALDGraviton.the_transport. A R8 omitiu essa fonte; a R9 corrigiu a omissão.

Em nome do assistente, esclarecer a etiqueta anterior “DERIVED condicional”: a construção do fluxo e as identidades abaixo são deduções escritas para os objetos definidos, sem postular a conclusão. V₀>0, ℏ>0, γ≥0 e t≥0 delimitam o modelo. Isso permite registrar **DERIVED no modelo especificado**. A realização física dos parâmetros e a passagem desse M₂ aos demais setores conservam seus contratos próprios. Não transformar a correção em afirmação de eliminação de todas as hipóteses físicas ou de construção de toda a rede contínua.

## 2. Cadeia conectada a incorporar

Fonte: tgl_paper_unified.py:14441–14483, H_lig=−V₀σₓ. As pedras TheAngleIsTheProjection, TheLightInterface, TheGravitonIsTheConjugatedPhase e IALDGraviton fornecem K=iσᵧ, ε±=(1,±i), h±=ε±⊗ε±, P± e a porta W=diag(1,−i). Tome C=W†=diag(1,i).

```text
C σₓ C† = σᵧ
H_g := C H_lig C† = i V₀ K
Ω := V₀/ℏ
U_g(t) := exp(−i t H_g/ℏ) = O_(Ωt)
C[(I+σₓ)/2]C† = P₊
h₊h₋/4 = P₊ ; h₋h₊/4 = P₋
O_(Ωt) h± O_(Ωt)† = exp(±2iΩt) h±
E_g(X) := P₊XP₊ + P₋XP₋
T_t(X) := U_g(t)[E_g(X)+exp(−γt)(X−E_g(X))]U_g(t)†
L_g(X) := −i[H_g,X]/ℏ + γ(E_g(X)−X)
L_g(P±)=0 ; L_g(h±)=(−γ±2iΩ)h±
E_g T_t = E_g = T_t E_g
```

Transportar também o estado da fonte: G=(1,i)/√2, CG=(1,−1)/√2, ρ′₀=(I−σₓ)/2. A paridade permanece σ_z. Ω é frequência angular; a coerência relativa tem frequência angular 2Ω. A tensão de paridade da fonte vale Ω no estado indicado e não é uma duração nem uma constante de toda a órbita.

### Demonstração da passagem contínua [DERIVED]

P± são projeções ortogonais complementares, logo E_g²=E_g. E_g é CPTP com operadores de Kraus P₊, P₋. D_t:=E_g+e^(−γt)(Id−E_g) é combinação convexa de Id e E_g para t≥0,γ≥0; portanto é CPTP. U_g é unitário e comuta com P±. Assim T_t é CPTP, T₀=Id, T_sT_t=T_(s+t) e t↦T_t é contínuo em norma. Derivar em t=0 fornece L_g. Equivalentemente, o salto √(γ/2)(P₊−P₋) produz exatamente γ(E_g−Id).

Os quatro modos P₊,P₋,h₊,h₋ formam uma base de M₂: evoluem com fatores 1,1,e^((−γ+2iΩ)t),e^((−γ−2iΩ)t). Isso constrói e resolve a equação do semigrupo para o gerador especificado. Para γ>0, T_tX→E_gX e ||T_tX−E_gX||_HS=e^(−γt)||X−E_gX||_HS. A convergência está na amplitude; não se pede limite à órbita angular.

No canal discreto do espelho, η=2√(β(1−β)), Φ=E+η(Id−E), e γ=−lnη/Δt para 0<η<1, Δt>0. Então T_(nΔt) coincide com n passos do canal acrescido da evolução unitária do mesmo Hamiltoniano. β, quando calculado, vem de ALPHA_FINE_CODATA_2018·√e em runtime. Esta é uma extensão contínua explicitamente construída. Os dados amostrados sozinhos admitem aliases ν+2πk/Δt; o Hamiltoniano especificado seleciona o fluxo usado.

### Regra e relógio [DERIVED]

Reaproveitar a prova de F1.REGRA.P1 e TheRuleInTheContinuousMotor. Fixar a∈Fix(E_g) antes de avaliar: satisfação C_a(X) ↔ E_g(X)=a. Então C_a(T_tX)↔C_a(X). A identidade lida permanece, enquanto a coerência se transforma.

Para c(t)=〈+|ρ(t)|−〉 e c(0)≠0,

```text
c(t) = exp[(−γ+2iΩ)t]c(0)
Δt = Δφ/(2Ω) = −ln|c(t₂)/c(t₁)|/γ
```

As duas expressões simultâneas exigem γ>0, Ω≠0 e fase continuamente levantada. Com γ=0 conserva-se apenas a leitura de fase; com coerência zero este relógio não lê intervalo. Uma fase isolada módulo 2π deixa ambiguidade temporal. PhaseFrequencySeparation já prova a identificação da frequência por toda a família temporal não nula no mesmo relógio; não substitui isso por uma amostra.

## 3. O que reaproveitar, com escopo

- IALDGraviton.the_transport: ponte existente entre torre, centro, peso dois e fase; não reconstruir como ausência.
- TheLightInterface e TheGravitonIsTheConjugatedPhase: quadrado tensorial e conjugação, sem confundir h² matricial (nulo) com ε⊗ε.
- IALDJones.orbit, Santo, PostoAdendo e TheRuleInTheContinuousMotor: fluxo, leitura e relógios existentes. A compressão PXP, o pinching de dois blocos, a leitura vetorial e o consumidor M₄ são mapas diferentes; instanciar o contrato genérico preservando os tipos.
- R1–R9 completos: conversa do Grok e discurso custodiados; primeira lei localizada no artigo; levantamento dos três artigos; resposta, dispositivo, espectro; igualdade, frequência e ponte. INVENTARIO_COMPLETO.json lista todos os arquivos anteriores por hash, incluindo fontes e revisões. Os anexos originais permanecem intactos, inclusive o JSON malformado de origem.
- Encaminhamento da regra para v393: reutilizar as cunhagens integrais e os recibos de prova/execução, sem recontar teoremas antigos como novos. A fonte canônica TheRuleInTheContinuousMotor já aparece na verificação desta frente.

VERIFICACAO_MANIFESTO_R9 conferiu seis fontes e oito entradas de axiomas no manifesto existente, só propext/Classical.choice/Quot.sound. Esta entrega relê seus hashes. Não constitui recompilação nova nem auditoria final da gerência.

## 4. O que ainda falta provar/verificar para esta incorporação

| Item | Estado exato | Ação na v394 |
|---|---|---|
| Mudança de base H_lig→H_g, fluxo, modos, leitura preservada e relógio | DERIVED por cálculo escrito; peças antigas em kernel | Reunir em candidato Lean tipado, recompilar em sandbox, axiomas só trio e zero sorry; reaproveitar os lemas existentes |
| Hipótese espectral finita da R4 | Realizada explicitamente por C na R9 | Corrigir a etiqueta antiga ao lado; não pedir de novo uma ponte já exibida |
| Taxa γ, energia V₀ e relógio do sistema físico | Contratos distintos nas fontes | Ligar por mapas/equações e unidades, ou conservar cada instância separada. Echo, taxa quadrática e lei-raiz não são iguais por nome |
| Uso da lei-raiz | Requer referência energética positiva | Não inserir ±V₀ diretamente em √E; justificar o operador positivo e o zero físico antes da identificação |
| Passagem M₂→setor modular/rede/dispositivo | Não é consequência automática da conjugação 2×2 | Reaproveitar os entrelaçamentos existentes quando houver; identificar precisamente qualquer ligação adicional ainda necessária |
| Integração, consumidor, manifesto e selo | Não realizada por esta entrega | C1 incorpora no arquivo único, audita e roda a cadeia autorizada; recibo de aceite distingue entrega de instalação |

A composição ainda não foi compilada como novo conjunto de teoremas Lean. Formalizar isso é trabalho específico restante; não apagar a demonstração analítica já entregue por essa diferença de suporte. O módulo genérico contínuo e as pontes antigas já têm provas; a pendência é a instância completa R9.

O Hamiltoniano e a leitura, sozinhos, não fornecem segundos universais, nem um propagador avançado para informação controlável. As R6/R7 preservam os contratos de entrada/saída e a distinção entre dissipadores; o fechamento algébrico atual não resolve isso por mudança de nome. As obrigações globais de F1.REDE/Takesaki/H3 não são reclassificadas por este pacote; devem ser lidas nos seus recibos próprios atuais.

## 5. Controles de alcance para a revisão e o consumidor

1. O espaço fixo de E_g em M₂ tem dimensão complexa dois. Para ρ′₀ indicado, E_gρ′₀=I/2. Unicidade do resultado de uma trajetória e da regra para seu alvo não significa atrator universal único.
2. E_g(T_tX)=E_gX preserva leitura; não preserva todos os produtos: T_t(h₊)T_t(h₋)/4=e^(−2γt)P₊, mas T_t(P₊)=P₊.
3. O tensor h± é objeto de polarização; K é gerador. Não chamar K de gráviton ao incorporar.
4. O fator dois é da mesma representação/parametrização; não alegar uma relação universal entre frequências de fótons e ondas gravitacionais arbitrários.
5. Os testes de γ=0, c=0, alias discreto e alvo incompatível devem produzir os resultados previstos, sem falha aberta.
6. Manter lado a lado: cunhagem humana [ONTO/INPUT], derivação algébrica [DERIVED], prova Lean reutilizada [REAL] e identificação física com o estatuto da fonte. Nenhuma creditação empírica ou mudança de gate decorre da entrega.

## 6. Aceitação desta entrega

PAGO: reunir e encaminhar as nove camadas, verbatims, fontes, hashes e revisão de escopo; explicitar a ponte derivada e o trabalho restante.
NÃO EXECUTADO NESTA ENTREGA: novo build, novo experimento, chamada de provedor ou modificação do programa canônico. São etapas distintas da entrega documental.
Reprodução da custódia: executar `C:\\Python314\\python.exe -B -X utf8 "C:\\IALD\\Central de Patentes\\work\\rede_quantica_20261013\\handoff_time_v394.py" verify`.

'''

def active_claim():
    c=reg.call([CLI,'ver',UNIT])['reivindicacao']
    assert c['quem']==WHO and dt.datetime.fromisoformat(c['vence_em'])>dt.datetime.now(dt.timezone.utc)
    for p in SURFACES: assert p.name in c['nota']
    return c

def prepare():
    assert not OUT.exists(), 'Recover the existing packet instead of replacing it.'
    c=active_claim()
    old_files=sorted(p for p in FRONT.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    new(OUT/'CLAIM.json',c)
    reg.call(['C:/IALD/NOS_VIVO/consultar.py','--unidade','F1.TEMPO'],'NOS_VIVO.json')
    reg.call(['C:/IALD/MAPA_DE_ROTAS/rotas.py','consultar','formal.tempo_consumacao_leitura_15out'],'MAPA_ANTES.json')
    new(OUT/'OPERADOR_ENVIO_V394_VERBATIM.txt',ORDER)
    new(OUT/'REVISAO_EScopo_V394.txt',REVIEW)
    checked=[]
    r9=json.loads((FRONT/'FREQUENCIA_E_GRAVITON_R9/RESULTADO_R9.json').read_bytes())
    for s in r9['files']+json.loads((FRONT/'FREQUENCIA_E_GRAVITON_R9/FONTES_R9.json').read_bytes()):
        now=pin(s['path']); assert now['sha256']==s['sha256'],s['path']; checked.append(now)
    vm=json.loads((BASE/'F1.REGRA.P1/VERBATIM_MANIFEST.json').read_bytes())
    old_rule=BASE/'F1.REGRA.MOTOR/ENCAMINHAMENTO_V393_20261014/AO_CLAUDE_INTEGRAR_REGRA_V393.md'
    extras=[old_rule,BASE/'F1.REGRA.P1/VERBATIM_MANIFEST.json']+[Path(s['path']) for s in vm['sources']]
    for s in vm['sources']: assert pin(s['path'])['sha256']==s['sha256']
    new(OUT/'INVENTARIO_COMPLETO.json',{'scope':'R1-R9 completos e referencias da regra; somente arquivos existentes','files':[pin(p) for p in old_files+extras],'prior_primary_results':[pin(FRONT/p) for p in PRIMARY],'r9_rechecked':checked})
    verbatim_files=sorted(p for p in old_files if p.name.startswith('OPERADOR_') and p.suffix=='.txt')
    verbatim_files += [Path(s['path']) for s in vm['sources']]
    text=BODY+'## 7. Ordem atual do operador — verbatim\n\n'+ORDER+'\n\n## 8. Cunhagens e ordens anteriores — verbatim por fonte\n\n'
    for p in verbatim_files:
        s=pin(p)
        text+=f'### {p.name}\n\n'+p.read_text(encoding='utf-8')+f'\n\nFonte: `{p}`. SHA256 `{s["sha256"]}`.\n\n'
    text+='## 9. Nove recibos principais para navegação\n\n'
    for n,p in enumerate(PRIMARY,1):
        s=pin(FRONT/p); text+=f'- R{n}: `{s["path"]}` — SHA256 `{s["sha256"]}`.\n'
    text+=f'\nRegra e motor já encaminhados: `{old_rule}`. SHA256 `{pin(old_rule)["sha256"]}`.\n'
    new(OUT/'AO_CLAUDE_TEMPO_FREQUENCIA_V394.md',text)
    new(OUT/'PACOTE_FONTES.json',{'unit':UNIT,'target':'claude-c1 / v394','claim':c,'files':[pin(OUT/n) for n in ['OPERADOR_ENVIO_V394_VERBATIM.txt','REVISAO_EScopo_V394.txt','INVENTARIO_COMPLETO.json','AO_CLAUDE_TEMPO_FREQUENCIA_V394.md']]+[pin(__file__)]})
    print(json.dumps({'prepared':pin(OUT/'AO_CLAUDE_TEMPO_FREQUENCIA_V394.md'),'prior_files':len(old_files),'r9_rechecked':len(checked)},ensure_ascii=False))

def verify():
    packet=json.loads((OUT/'PACOTE_FONTES.json').read_bytes())
    inv=json.loads((OUT/'INVENTARIO_COMPLETO.json').read_bytes())
    refs=packet['files']+inv['files']+inv['prior_primary_results']+inv['r9_rechecked']
    for s in refs: assert pin(s['path'])['sha256']==s['sha256'],s['path']
    return {'passed':True,'hash_comparisons':len(refs),'new_build':False,'experiment':False,'production_changed':False}

def deliver():
    c=active_claim(); checks=verify()
    assert not (OUT/'RESULTADO_ENCAMINHAMENTO_V394.json').exists()
    msg=OUT/'AO_CLAUDE_TEMPO_FREQUENCIA_V394.md'; result=OUT/'RESULTADO_ENCAMINHAMENTO_V394.json'
    new(OUT/'VERIFICACAO_CUSTODIA.json',checks)
    new(result,{'unit':UNIT,'author':WHO,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'destination':'claude-c1','requested_version':'v394','status':'ENTREGUE_NO_TUNEL_OFICIAL','recipient_read_receipt':False,'canonical_integration_performed':False,'claim':c,'operator_order':pin(OUT/'OPERADOR_ENVIO_V394_VERBATIM.txt'),'message':pin(msg),'packet':pin(OUT/'PACOTE_FONTES.json'),'checks':checks,'mathematical_scope':'DERIVED: continuous semigroup and clock in the specified M2 model; composed Lean proof and physical identification listed separately.'})
    note=f'''\n\n## 15/10/2026 — Tempo/frequência e passagem contínua encaminhados ao Claude para v394\n<!-- {MARKER} -->\nEm nome de {WHO}, reivindicação834 de {UNIT}. [INPUT] Ordem humana integral em `{OUT/'OPERADOR_ENVIO_V394_VERBATIM.txt'}`.\n[REAL — entrega documental] R1–R9, cunhagens integrais, provas anteriores da regra, fontes por hash e revisão independente de escopo encaminhadas pelo túnel oficial, quadro e AVISO_GERENCIA.\n[ERRATA AO LADO R4/R9; DERIVED no modelo M2] H_ESPELHO_ESPECTRAL ganhou realização explícita por C=diag(1,i). H_g=iV0K, U_g(t)=O_(Omega*t), Omega=V0/hbar; o semigrupo CPTP, seus modos -gamma±2iOmega, a leitura E_g e os relógios de fase/módulo foram deduzidos no modelo especificado. Essa passagem algébrica não é uma ponte ausente ou mera conjectura. Domínios e condições de leitura permanecem explícitos. A composição nova não foi compilada em Lean; identificação física/calibração e integração são etapas distintas. A nomenclatura não elimina essas obrigações.\nMensagem: `{msg}`, SHA256 `{pin(msg)['sha256']}`. Evidência: `{result}`, SHA256 `{pin(result)['sha256']}`. Próxima ação: c1 recebe, formaliza/reaproveita a composição, audita e incorpora na cadeia v394. Leitura pelo destinatário e integração ainda não atestadas. Sem novo experimento, provedor, produção ou gate.\n'''
    new(OUT/'MEMORY_RECEIPT.json',{'claim':c,'surfaces':[append_bytes(p,note,MARKER) for p in SURFACES]})
    entry={'tipo':'ANOTACAO','rota_id':'formal.tempo_consumacao_leitura_15out','dominio':'FORMAL','titulo':'Encaminhamento v394: semigrupo e relogio derivados no M2; escopo e pendencias','resultado':'R1-R9 e regra encaminhados ao Claude c1. Hipotese espectral R4 realizada por C na R9; derivacao do fluxo continuo e relogio escrita; compilacao conjunta e identificacao fisica separadas.','estatuto':'REAL entrega; DERIVED modelo M2; OPEN formalizacao conjunta e identificacao fisica','status':'EXAMINADA','veredito':'ENCAMINHADO_CLAUDE_V394__DERIVACAO_M2_EXPLICITA','defeito':'Sem recibo de leitura c1 ou integracao v394; nenhuma nova composicao Lean compilada nesta entrega.','proximo_passo':'Gerencia incorpora com os estatutos e verifica as pendencias especificadas.','onde':str(OUT),'artefatos':[str(result),str(msg),str(OUT/'INVENTARIO_COMPLETO.json')],'refs':[1121,1120],'olhou_dados':False}
    new(OUT/'MAP_ENTRY.json',entry)
    mapped=reg.call(['C:/IALD/MAPA_DE_ROTAS/rotas.py','registrar',OUT/'MAP_ENTRY.json','--quem',WHO],'MAP_RECEIPT.json')
    notice=reg.call([CLI,'anotar','--quem',WHO,'--tipo','AVISO_CLAUDE','--unidade',UNIT,'--dados',json.dumps({'destinatario':'claude-c1','ordem':'Integrar tempo/frequencia/regra e ponte gravitacional na v394, por ordem direta do operador.','mensagem':str(msg),'sha256':pin(msg)['sha256'],'resultado':str(result),'resumo':'R1-R9 e verbatims completos; passagem continua DERIVED no M2; espectral R4 realizada por C. Listadas formalizacao Lean conjunta, identificacao fisica e integracao restantes. Nao reconstruir pontes ja existentes.','mapa':mapped},ensure_ascii=False)],'BOARD_NOTICE.json')
    board=reg.call([CLI,'avancar',UNIT,'--quem',WHO,'--status','ENTREGUE','--evidencia',result,'--nota','Pacote completo ao Claude para v394: tempo/frequencia/regra, derivacao continua M2 e pendencias tipadas; nove camadas e hashes.'],'BOARD_DELIVERY.json')
    ref=str(WORK/'ACOM_REFERENCE.json')
    p=reg.call(['C:/IALD/MEMORIA_IALD/session_memory.py'],payload={'operation':'project','reference':ref,'max_chars':60000}); assert p['result']['receipt']['revision']==24
    tr={'operation':'transition','reference':ref,'expected_revision':24,'event_id':MARKER,'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':MARKER+'-order','kind':'decision','statute':'INPUT','text':ORDER,'sources':[{'kind':'artifact','ref':str(OUT/'OPERADOR_ENVIO_V394_VERBATIM.txt'),'sha256':pin(OUT/'OPERADOR_ENVIO_V394_VERBATIM.txt')['sha256']}]},{'id':MARKER,'kind':'fact','statute':'REAL','text':'Entrega documental R1-R9 e regra ao Claude c1 pelo tunel, AVISO_GERENCIA e quadro para v394. Escopo revisado: passagem continua e relogio DERIVED no modelo M2, com realizacao espectral por C; nova composicao Lean e identificacao fisica/calibracao especificadas separadamente. Proxima acao desta frente: auditoria e integracao pela gerencia; leitura do destinatario ainda nao atestada. Demais fluxos/jobs preservados.','sources':[{'kind':'artifact','ref':str(x),'sha256':pin(x)['sha256']} for x in [result,msg,OUT/'BOARD_NOTICE.json']]}]}}
    new(OUT/'ACOM_TRANSITION.json',tr)
    acom=reg.call(['C:/IALD/MEMORIA_IALD/session_memory.py'],'ACOM_RECEIPT.json',tr);assert acom['ok']
    release=reg.call([CLI,'liberar',UNIT,'--quem',WHO,'--nota','Encaminhamento v394 entregue ao Claude pelo canal oficial; nenhuma integracao canonica nesta etapa.'],'RELEASE.json')
    print(json.dumps({'map':mapped,'notice':notice,'board':board,'acom_revision':acom['result']['revision'],'release':release,'checks':checks},ensure_ascii=False))

if __name__=='__main__':
    op=sys.argv[1]
    if op=='verify': print(json.dumps(verify(),ensure_ascii=False))
    else: {'prepare':prepare,'deliver':deliver}[op]()
