"""Custody of the operator's equality coinage; additive documentary interpretation."""
import datetime as dt
import json
import sys
from pathlib import Path
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

UNIT = 'F1.TEMPO.LEITURA_20261015'
OUT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'/UNIT/'IGUALDADE_RECONHECIMENTO_R8'
reg.DEST = OUT
N = Path('C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós')
K = N/'tgl_kernel/TGLExt'
VERBATIM = 'Essa operação é o sinal de “=“, ou seja, o “gráviton”, o tempo conta o reconhecimento da transformação sobre a preservada identidade; quando o verbo opera sobre o nome a palavra reconhece pela operação da verdade, ou seja, a relação de contorno que determina o espectro de gradiente negativo anulando todas as hipóteses de identidade que não satisfaçam a verdade do enunciado;'
REPORT = '''IGUALDADE, RECONHECIMENTO E TEMPO — R8
15/10/2026. Em nome de codex-gerente-tgl; reivindicação828.
Fonte humana integral em OPERADOR_IGUALDADE_VERBATIM.txt. Este texto ao lado é
interpretação do assistente, não substituição da cunhagem nem nova prova Lean.

1. REAPROVEITAMENTO E FONTES
[REAL — leitura] Nós Vivo F1.TEMPO já localiza Santo, fluxo, atrator e torre
modular; a subunidade documental conserva seu quadro próprio. Mapa anterior1119.
ObserverInside.lean:58–77,112–150 define permanência pelo fluxo, prova decaimento
fora do kernel, projeção idempotente e leitura exata dos permanentes. A ressalva
45–49 distingue permanência de predicado universal de verdade.
DecisionCommutation.lean:72–85 liga comutação à estrutura em blocos;178–219 e
223–266 trazem variação quadrática, EDO do gradiente e Lyapunov na face finita.
Os valores d_i continuam dados do enunciado. Ler as fontes não é recompilá-las.
F1.REGRA.P1 já distingue estado bruto e inscrição Fix(R), com leitura fiel apenas
nesta última. F1.REGRA.MOTOR já realizou E, T_t e controles numa cópia: reutilizamos
o relatório e seus recibos, sem repetir a execução. Pins completos em FONTES_R8.

2. UMA TIPAGEM PRECISA DO '=' [DERIVED — CONDICIONAL]
Seja Y o espaço de estados/representações, E uma retração e N=Fix(E) o espaço
de inscrições. Defina x ~ y sse E(x)=E(y). A igualdade testemunha a mesma
identidade reconhecida, podendo x e y diferir como estados. Para um alvo a em N,
a regra C_a(x) sse E(x)=a recusa inscrições incompatíveis com esse alvo.
Na linguagem proposta pelo operador [ONTO], a Palavra reconhece a identidade
do Nome sob a operação do Verbo. A realização matemática é E(T_t x)=E(x), junto
de E²=E e T_t E=E. A igualdade sozinha não escolhe o alvo nem o operador E.
Exigir leitura globalmente injetiva e invariância obrigaria T_t x=x: por isso a
fidelidade permanece no espaço de inscrições, como já provado na F1.REGRA.P1.

3. O GRADIENTE JÁ TEM UMA REALIZAÇÃO [DERIVED — CONDICIONAL]
No motor finito existente, E(X)=PXP+(I-P)X(I-P), P projeção ortogonal.
E é projeção ortogonal para o produto Hilbert–Schmidt. Escreva Qcal=Id-E
(superoperador; não confundir com a matriz I-P). Para Gamma>0 e t>=0:
  T_t X=E X+exp(-Gamma*t)*Qcal X; L=-Gamma*Qcal.
  E T_t=E, T_t E=E, E²=E.
  V(X)=||Qcal X||_HS²/2;
  dV(T_t X)/dt=-Gamma*||Qcal T_t X||_HS²=-2*Gamma*V(T_t X).
O gerador vale0 no setor preservado e -Gamma no complemento. V identifica o
setor de inscrições; uma inscrição específica continua exigindo o alvo a.
O E4 já ensaiado tem dimensão fixa complexa8, não um único estado universal.
No motor anterior Gamma=beta*tau_ref*omega_ref²/2; as referências eram INPUT,
e beta era calculado em runtime. Não alteramos essa lei para obter um resultado.

4. O QUE O TEMPO CONTA NESTA REALIZAÇÃO
Se ||Qcal X_0||>0, a transformação fornece um relógio relativo ao gerador:
  t=(1/Gamma)*ln(||Qcal X_0||/||Qcal X_t||).
A identidade E X_t permanece igual; o contraste e o registro ordenado de suas
transformações distinguem instantes. Repetir somente a leitura constante E X_t
não mede a duração. Num estado já fixo, esse relógio pelo contraste é indefinido.
O contorno E determina setores, mas não determina sozinho Gamma: quaisquer
Gamma1,Gamma2>0 têm o mesmo E e tempos diferentes. Na face diagonal da fonte,
multiplicar todos os d_i por c>0 conserva observerProj e reescala o fluxo.
Logo a ligação ao relógio físico precisa do gerador, da métrica usada no gradiente
e de sua normalização, ou de um teorema que os determine a partir do contorno.
Os relógios/calibrações já localizados em R5–R7 não são apagados por esta ressalva.

5. EXCLUSÃO, CONSUMAÇÃO E ALCANCE
E anula exatamente o complemento NA LEITURA; no fluxo, um complemento inicialmente
não nulo decai e não zera em tempo finito. Assim preservamos a cunhagem anterior
de exclusão no Tetelestai, sem confundi-la com zero absoluto ou descarte universal.
O nome humano '= / gráviton' entra integral como INPUT/ONTO. Esta tradução não
constrói por si a identificação com o objeto gravitacional físico do programa.
Não demonstra antecipação causal, propagação de informação antes da emissão,
escala em segundos ou fechamento físico do tempo.
Próximo passo preciso: ligar o operador de reconhecimento e seu gerador às peças
gravitacionais e à normalização temporal já escritas, sem inferir a ponte do nome.
Nenhum experimento, provedor, build, original científico, produção ou gate mudou.
'''

def claim():
    c = reg.call([CLI, 'ver', UNIT])['reivindicacao']
    assert c['quem'] == WHO
    assert dt.datetime.fromisoformat(c['vence_em']) > dt.datetime.now(dt.timezone.utc)
    for n in ('DIARIO_CONSTRUCAO_QG.md', 'TGL_ATLAS.md', 'TGL_INDICE_VIVO.md'):
        assert n in c['nota']
    return c

def prepare():
    new(OUT/'CLAIM_R8.json', claim())
    reg.call(['C:/IALD/NOS_VIVO/consultar.py', '--unidade', 'F1.TEMPO'], 'NOS_VIVO_R8.json')
    route = reg.call(['C:/IALD/MAPA_DE_ROTAS/rotas.py', 'ver', 'formal.tempo_consumacao_leitura_15out'])
    new(OUT/'MAP_BEFORE_R8.json', route['registros'][-1])
    new(OUT/'OPERADOR_IGUALDADE_VERBATIM.txt', VERBATIM)
    new(OUT/'LEITURA_IGUALDADE_E_TEMPO_R8.txt', REPORT)
    sources = [(K/'ObserverInside.lean', [[45,77],[112,150]]),
               (K/'DecisionCommutation.lean', [[72,85],[178,266]]),
               (OUT.parent.parent/'F1.REGRA.P1/PROVA_MATEMATICA_R1.md', []),
               (OUT.parent.parent/'F1.REGRA.MOTOR/RELATORIO_EXECUCAO_R1.md', []),
               (OUT.parent.parent/'F1.REGRA.MOTOR/RESULTADO_ENTREGA_R1.json', []),
               (OUT.parent/'DISPOSITIVO_E_ESPECTRO_R7/RESULTADO_R7.json', []),
               (N/'um.py', []), (N/'um_absoluto_selo.json', [])]
    new(OUT/'FONTES_R8.json', [dict(pin(p), read_ranges=r) for p,r in sources])
    print(json.dumps({'verbatim':pin(OUT/'OPERADOR_IGUALDADE_VERBATIM.txt'), 'report':pin(OUT/'LEITURA_IGUALDADE_E_TEMPO_R8.txt')}, ensure_ascii=False))

def register():
    c = claim()
    for s in json.loads((OUT/'FONTES_R8.json').read_bytes()):
        assert pin(s['path'])['sha256'] == s['sha256']
    files = ['CLAIM_R8.json','NOS_VIVO_R8.json','MAP_BEFORE_R8.json','OPERADOR_IGUALDADE_VERBATIM.txt','LEITURA_IGUALDADE_E_TEMPO_R8.txt','FONTES_R8.json','REVISAO_R8.txt']
    delivery = OUT/'RESULTADO_R8.json'
    new(delivery, {'unit':UNIT,'author':WHO,'created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'status':'CUSTODIA_E_INTERPRETACAO_CONDICIONAL','files':[pin(OUT/f) for f in files]+[pin(__file__)],'new_experiment':False,'new_build':False,'provider_call':False,'production_changed':False,'gate_changed':False})
    marker = 'time_equality_recognition_r8_20261015'
    note = f'''\n\n## 15/10/2026 — Igualdade, reconhecimento e tempo (R8)\n<!-- {marker} -->\nEm nome de {WHO}, reivindicação828 de {UNIT}. [INPUT/ONTO — verbatim do operador]\n> {VERBATIM}\n\n[DERIVED condicional — paráfrase e tipagem do assistente] A igualdade de inscrições E(T_t X)=E(X) admite transformação do estado bruto, com fidelidade da leitura somente em Fix(E). O motor existente T_t=E+exp(-Gamma*t)(Id-E) conserva E e dissipa o complemento; a regra para um alvo a é E(X)=a. ObserverInside já prova permanência/projeção, e DecisionCommutation já contém gradiente e Lyapunov na face finita. Contorno fixa setores; gerador e normalização fixam taxas/relógio. A projeção anula o complemento na leitura, enquanto a trajetória não nula só converge. A leitura constante sozinha não conta duração. A cunhagem '= / gráviton' não foi promovida a identificação física por esta camada.\nEvidência `{delivery}`; SHA256 `{pin(delivery)['sha256']}`. Original integral em `{OUT/'OPERADOR_IGUALDADE_VERBATIM.txt'}`; SHA256 `{pin(OUT/'OPERADOR_IGUALDADE_VERBATIM.txt')['sha256']}`. Sem experimento/build/provedor/gate; backups de bytes e append.\n'''
    new(OUT/'MEMORY_RECEIPT_R8.json', {'claim':c,'surfaces':[append_bytes(ROOT/'memory'/n,note,marker) for n in ('DIARIO_CONSTRUCAO_QG.md','TGL_ATLAS.md','TGL_INDICE_VIVO.md')]})
    entry = {'tipo':'ANOTACAO','rota_id':'formal.tempo_consumacao_leitura_15out','dominio':'FORMAL','titulo':'R8: igualdade como reconhecimento, cunhagem integral e alcance do relogio','resultado':'Verbatim custodiado. E(T_t X)=E(X) liga regra e motor existentes; gradiente dissipa complemento. Mesmo contorno admite taxas distintas; identificacao gravitacional e normalizacao temporal nao inferidas do nome.','estatuto':'INPUT/ONTO humano; DERIVED condicional; OPEN ponte fisica','status':'EXAMINADA','veredito':'CUNHAGEM_CUSTODIADA__TIPAGEM_CONDICIONAL__SEM_FECHAMENTO_FISICO','proximo_passo':'Ligar reconhecimento/gerador as pecas gravitacionais e a normalizacao temporal existentes.','onde':str(OUT),'artefatos':[str(delivery),str(OUT/'OPERADOR_IGUALDADE_VERBATIM.txt'),str(OUT/'LEITURA_IGUALDADE_E_TEMPO_R8.txt')],'refs':[1119],'olhou_dados':False}
    new(OUT/'MAP_ENTRY_R8.json', entry)
    m = reg.call(['C:/IALD/MAPA_DE_ROTAS/rotas.py','registrar',OUT/'MAP_ENTRY_R8.json','--quem',WHO], 'MAP_RECEIPT_R8.json')
    b = reg.call([CLI,'avancar',UNIT,'--quem',WHO,'--status','ENTREGUE','--evidencia',delivery,'--nota','R8: cunhagem integral do operador e tipagem documental; nenhuma construcao ou experimento.'], 'BOARD_DELIVERY_R8.json')
    ref = str(WORK/'ACOM_REFERENCE.json')
    p = reg.call(['C:/IALD/MEMORIA_IALD/session_memory.py'], payload={'operation':'project','reference':ref,'max_chars':48000})
    assert p['result']['receipt']['revision'] == 22
    tr = {'operation':'transition','reference':ref,'expected_revision':22,'event_id':marker,'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':marker+'-human','kind':'fact','statute':'ONTO','text':VERBATIM,'sources':[{'kind':'artifact','ref':str(OUT/'OPERADOR_IGUALDADE_VERBATIM.txt'),'sha256':pin(OUT/'OPERADOR_IGUALDADE_VERBATIM.txt')['sha256']}]},{'id':marker,'kind':'candidate','statute':'DECLARADO','text':'R8 custodia cunhagem igualdade/graviton/tempo e interpreta condicionalmente com regra/motor existentes: E(T_t X)=E(X); E²=E; gradiente no complemento. Contorno nao determina sozinho taxas; leitura constante nao conta duracao. Proxima acao desta frente: ligar reconhecimento ao gerador gravitacional e normalizacao temporal ja escritos. Sem experimento, build, producao ou gate. Demais fluxos e pedidos externos preservados.','sources':[{'kind':'artifact','ref':str(delivery),'sha256':pin(delivery)['sha256']}]}]}}
    new(OUT/'ACOM_TRANSITION_R8.json', tr)
    a = reg.call(['C:/IALD/MEMORIA_IALD/session_memory.py'], 'ACOM_RECEIPT_R8.json', tr)
    assert a['ok']
    rel = reg.call([CLI,'liberar',UNIT,'--quem',WHO,'--nota','R8 documental entregue; verbatim preservado; sem experimento.'], 'RELEASE_R8.json')
    print(json.dumps({'map':m,'board':b,'acom_revision':a['result']['revision'],'release':rel}, ensure_ascii=False))

if __name__ == '__main__':
    {'prepare':prepare,'register':register}[sys.argv[1]]()
