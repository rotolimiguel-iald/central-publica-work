"""Deliver the operator-authorized rule package through the official Claude tunnel."""
import datetime as dt
import json
from pathlib import Path
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

BASE = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019'
UNIT = 'F1.REGRA.MOTOR'
OUT = BASE/UNIT/'ENCAMINHAMENTO_V393_20261014'
ORDER = 'transmita para o claude o que fizemos também sobre a prova da "regra" e seu conceito isso também precisa entrar no um.py na v 393'

def verify_ref(item):
    assert pin(Path(item['path']))['sha256'] == item['sha256'], item['path']

def main():
    assert not OUT.exists(), 'Existing handoff: recover receipts; do not repeat.'
    reg.DEST = OUT
    reg.call([CLI,'reivindicar',UNIT,'--quem',WHO,'--nota',
        'Ordem humana: transmitir conceito, prova e motor da regra ao Claude para integrar v393. Somente novo pacote no tunel, quadro/mapa e memoria: DIARIO_CONSTRUCAO_QG.md, TGL_ATLAS.md, TGL_INDICE_VIVO.md, AVISO_GERENCIA.md e ACOM propria; backup bytes. Nenhuma integracao canonica nesta etapa.'], 'CLAIM.json')
    claim = reg.call([CLI,'ver',UNIT])['reivindicacao']
    assert claim['quem'] == WHO
    reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar','formal.regra_motor_continuo'],'MAPA_ANTES.json')
    new(OUT/'OPERADOR_ENVIO_V393_VERBATIM.txt',ORDER+'\n')
    new(OUT/'CONSULTA_PREVIA.json',{'unit':UNIT,'nos_vivo':'Consulta nesta sessao: unidade ainda nao indexada; nao reconstruido o grafo.',
        'reuse':['F1.REGRA cunhagens integrais','F1.REGRA.P1 prova e revisao existentes','F1.REGRA.MOTOR execucao, build e revisao existentes','Mapa 1109 e 1110'],
        'new_work':'Somente encaminhamento solicitado pelo operador; nao refazer a ciencia.'})
    vm=json.loads((BASE/'F1.REGRA.P1/VERBATIM_MANIFEST.json').read_bytes())
    p1=json.loads((BASE/'F1.REGRA.P1/RESULTADO_PROVA_R1.json').read_bytes())
    motor=json.loads((BASE/'F1.REGRA.MOTOR/RESULTADO_ENTREGA_R1.json').read_bytes())
    assert p1['passed'] and motor['passed']
    for ref in vm['sources']+p1['sources']+[p1[k] for k in ['constructor_build','independent_review','manifest','report']]+[motor[k] for k in ['runtime','formal','review','report','manifest']]: verify_ref(ref)
    mr=json.loads(Path(motor['review']['path']).read_bytes())
    run=json.loads(Path(motor['runtime']['path']).read_bytes())
    assert mr['passed'] and run['passed']
    source_paths=[BASE/'F1.REGRA.P1/VERBATIM_MANIFEST.json',BASE/'F1.REGRA.P1/RESULTADO_PROVA_R1.json',BASE/'F1.REGRA.MOTOR/RESULTADO_ENTREGA_R1.json']
    source_paths += [Path(v['path']) for v in vm['sources']+p1['sources']]
    source_paths += [Path(p1[k]['path']) for k in ['constructor_build','independent_review','report']]
    source_paths += [Path(motor[k]['path']) for k in ['runtime','formal','review','report']]
    source_paths += [BASE/'F1.REGRA.MOTOR/formal/TheRuleInTheContinuousMotor.lean',BASE/'F1.REGRA.MOTOR/runtime/run_rule_motor.py',BASE/'F1.REGRA.MOTOR/PREREGISTRO_R1.json',BASE/'F1.REGRA.MOTOR/SOURCE_MANIFEST.json']
    sources=[pin(p) for p in source_paths]
    message='''# AO CLAUDE / GERÊNCIA c1 — integrar a REGRA na v393

De: codex-gerente-tgl. Para: gerência Claude Code c1. Data: 14/10/2026.
Canal oficial: túnel DO_CHATGPT + quadro único + AVISO_GERENCIA. Entrega documental por ordem humana; leitura e aceite do destinatário ainda não atestados.

## Ordem do operador, verbatim

'''+ORDER+'''

## 1. Cunhagens integrais do operador

Autoria: Luiz Antonio Rotoli Miguel. As quatro fontes abaixo são preservadas integralmente, com hashes calculados dos originais. As leituras filosófica e jurídica são [INPUT/ONTO]; a prova formal tem as hipóteses explicitadas na seção seguinte.

'''
    for i,ref in enumerate(vm['sources'],1):
        message+=f'### Cunhagem {i}\n\n'+Path(ref['path']).read_text(encoding='utf-8').rstrip()+f'\n\nFonte: `{ref["path"]}`; SHA256 `{ref["sha256"]}`.\n\n'
    message+='''## 2. Conceito e prova já entregues — reaproveitar

[PARÁFRASE / INPUT] A regra recusa como satisfação o resultado cuja leitura difere do objeto devido. «A não ser a figura da verdade» foi representado pela completude relativa ao alvo: não acrescentar outra exclusão quando há correspondência. Essa completude é hipótese declarada, não teorema extraído do nome.

[REAL — Lean em sandbox] Fixados leitura r:N→O injetiva no espaço de inscrições, alvo a:N e figura o=r(a), correção C(z)⇒r(z)=o e completude r(z)=o⇒C(z) dão C(z)↔z=a. O predicado é único para essa leitura e esse alvo. Fontes: RuleTruthContract.sound_complete_eq_admissible, admissible_iff_eq_of_injective e RuleSatisfactionFace.unique_rule_on_inscriptions.

F1.REGRA.P1 tem 60 teoremas (22 no contrato + 38 na realização), zero sorry, apenas propext/Classical.choice/Quot.sound e recompilação independente EXIT 0. O exemplo R(a,b)=(a,0), T(a,b)=(a,exp(-1/2)b) tem alvo (1,0) não nulo, retração idempotente, contração e convergência. Reaproveita TheJudgedThing, TheNonMinimalCoupling, TheGeometricCostOfAbsoluteZero e TheLedgerOfCharges com pontes explícitas.

Limites indispensáveis: sem completude, rejeitar tudo também satisfaz correção; sem leitura fiel, igualdade de leituras não implica igualdade de objetos. A fidelidade vale no subtipo Fix(R), não no espaço bruto. R(T^n x0)=a já em n=0; T^n x0≠a para todo n finito. A relação com zero absoluto é interpretação: não foi provado um novo teorema termodinâmico. A meia-nat exp(-1/2) desse exemplo não é beta_TGL.

Ressalva de reprodução da P1: 2/3 .olean coincidiram byte a byte; o módulo concreto teve bytes diferentes, com fonte e axiomas iguais; causa não determinada. Manter a ressalva no recibo.

## 3. Regra já ligada ao motor contínuo real da v392

[REAL — Lean e execução sintética] TheRuleInTheContinuousMotor.lean acrescenta 42 teoremas, reutilizando o contrato de 22 sem contá-lo novamente como novo. Recompilação independente de dois módulos: EXIT 0, só trio, zero sorry; ambos .olean idênticos. Ponte genérica por IALDJones.orbit e realização ActualConsumerM4.

Consumidor numérico original: prove_decision_commutation, extraído por AST da v392, com seus cinco corpos de função intactos e dez evidências formais conferidas. E(X)=PXP+QXQ, P=diag(1,1,0,0), Q=I-P; T_t(X)=E(X)+exp(-Gamma*t)(X-E(X)). A regra é consumida no veredito, não apenas citada: o alvo pré-fixado correto é admitido e o incompatível é recusado.

O mesmo pinching M4, o estado psi=(1,i,1,-i)/2 e o alvo pré-registrado estão ligados por igualdade na pedra. E(T_t rho)=E(rho); semigrupo, continuidade, limite com taxa positiva e diferença bruta em tempo finito estão provados. O motor vetorial IALD.motor tem ponte separada. Não identificar pinching com o corner eXe.

'''
    message+=f'Execução: {run["checks_passed"]} verificações, {run["point_count"]} pontos; complemento {run["complement_initial"]} → {run["complement_final"]}. Revisão independente: {mr["runtime_independent_checks"]} verificações adicionais e replay dos 241 pontos byte a byte.\n\n'
    message+='''O espaço fixo tem dimensão complexa 8: a unicidade do critério para um alvo não é unicidade de todos os estados fixos. Beta é calculado em runtime de alfa*sqrt(e); Gamma=beta*tau_ref*omega_ref²/2. A grade u=Gamma*t não mede beta, pois o expoente passa a ser -u. Unidades de referência são INPUT. Execução concluída, não daemon; nenhum dado observado.

## 4. O que deve entrar na v393 por esta ordem

1. Incorporar as quatro cunhagens verbatim, com autoria, fontes e hashes, na apresentação do conceito; manter a formalização e sua interpretação identificadas.
2. Reaproveitar RuleTruthContract.lean, TheRuleAndTheFigureOfTruth.lean e TheRuleInTheContinuousMotor.lean. Na incorporação ao kernel embutido do arquivo único, ajustar módulos/imports consistentemente e recompilar na cadeia da v393; não copiar .olean como substituto do build.
3. Fazer o consumidor registrar leitura, alvo fixado antes, satisfação admitida/recusada, origem das evidências, critério exato versus tolerância numérica e os controles negativos. Preservar estado bruto e inscrição em campos distintos. Incompatibilidade deve ser veredito testado; idempotência ou flag global sozinhas não bastam.
4. Integrar a candidata de coração/proveniência com esse contrato, sem trocar o M4 existente por exemplo M2 silenciosamente. Evidência espectral independente requer cadeia pinada independente de CODATA; nomes e metadados sozinhos não provam a origem.
5. Reexecutar o consumidor e os controles na cópia candidata, obter revisão independente e atualizar relatório PT/EN, manifesto de fontes e recibos de selo com alcance explícito. A revisão e instalação canônicas permanecem na cadeia da gerência; esta mensagem não afirma que já ocorreram.
6. Preservar does_not_gate_core e os estatutos. As provas não instalam a dinâmica nos pesos de um LLM, não provam uma norma jurídica universal e não confirmam a natureza.

Não é necessário reconstruir as provas nem repetir chamada externa para esta entrega. Unidades estão ENTREGUES; o aceite AUDITADA/FECHADA pertence à gerência. Registros anteriores: quadro 791 e 795; mapa 1109 e 1110.

## 5. Fontes conferidas nesta transmissão

'''
    for ref in sources:
        message+=f'- `{ref["path"]}` — SHA256 `{ref["sha256"]}`; {ref["bytes"]} bytes.\n'
    msg=OUT/'AO_CLAUDE_INTEGRAR_REGRA_V393.md'
    new(msg,message)
    new(OUT/'PACOTE_FONTES.json',{'unit':UNIT,'target':'Claude Code c1 / v393','sources':sources,'message':pin(msg),'operator_order':pin(OUT/'OPERADOR_ENVIO_V393_VERBATIM.txt')})
    print(json.dumps({'prepared':pin(msg),'claim':claim},ensure_ascii=False))

if __name__=='__main__': main()
