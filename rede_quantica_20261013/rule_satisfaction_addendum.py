"""Custody and additive registration of the operator's satisfaction definition."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as register

UNIT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REGRA'
DEST = UNIT/'SATISFACAO_20261014'
TEXT = 'Regra é a inadmissao que o resultado da operação seja distinto do objeto de sua satisfação (pagamento, comutação)'
KB = ROOT/'work/cadeia_de_selo/v392/kb_stub_v392/TGLExt'


def main():
    assert not DEST.exists(), 'Inspect existing receipts; do not repeat inscription'
    register.DEST = DEST
    claim = register.call([CLI,'ver','F1.REGRA'])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    assert 'TGL_ATLAS.md' in claim['nota']
    DEST.mkdir()
    new(DEST/'CLAIM_RECEIPT.json', {'claim':claim,'event_observed_in_tool_output':783})
    original = DEST/'OPERADOR_REGRA_SATISFACAO_VERBATIM.txt'
    new(original,TEXT)
    sources = [KB/'TheNameAndItsReferent.lean', KB/'TheLedgerOfCharges.lean', KB/'TheJudgedThing.lean']
    new(DEST/'FONTES.json', {'files':[pin(p) for p in sources],
        'previous_addendum':pin(UNIT/'TETELESTAI_20261014/ADENDO_REGRA_TETELESTAI.md'),
        'graph_query':'Fresh consultar.py --unidade F1.REGRA returned: unidade não está no grafo: F1.REGRA (rode construir.py). No graph rebuild performed.',
        'route_query':'Fresh route query returned conceitual.regra.negatividade_juridica, 2 records, latest annotation seq1106.',
        'verification':'Documentary reading only; no new Lean compilation.'})
    body = '''Em nome de codex-gerente-tgl, sob reivindicação F1.REGRA 783. Autoria: Luiz Antonio Rotoli Miguel; mensagem humana direta de 14/10/2026. Os registros anteriores permanecem íntegros.

## Alcance da precisão

[ONTO — definição do operador] A regra inadmite que o resultado da operação seja distinto do objeto de sua satisfação. Pagamento e comutação são as operações mencionadas pelo autor. O verbatim é conservado sem correção ortográfica.

[PARÁFRASE DO ASSISTENTE] A regra exige que o resultado realize o objeto cuja satisfação está em questão. A exclusão incide sobre a divergência entre resultado e objeto devido. O Tetelestai corresponde à quitação dessa obrigação no alcance definido anteriormente pelo autor.

[DERIVED — contrato candidato] Quando resultado r e objeto devido o pertencem ao mesmo tipo Y, escrever Admissivel(r,o) := não (r ≠ o); na lógica clássica, equivale a r=o. Para uma operação F:X→Y, o teste é Admissivel(F(x),o). Isso não impõe F=id: o estado inicial x pode ser de outro tipo e a operação pode transformar. Se resultado e objeto forem representações de tipos distintos, declarar a leitura pi:Y→O e comparar pi(F(x))=o. A leitura pi e o objeto o devem estar especificados para que a igualdade tenha conteúdo; definir o como a própria saída examinada tornaria a verificação tautológica. A equivalência admitida não pode ser afrouxada depois de observar o resultado para forçar satisfação.

[DERIVED — diferença em relação ao adendo anterior] R²=R estabelece estabilidade sob releitura. A definição atual exige também correspondência com o objeto devido. Uma leitura constante R(x)=c é idempotente, mas falha em satisfazer um objeto o distinto de c. Logo a idempotência isolada não encerra esse contrato. O novo critério recusa uma saída divergente como satisfação; não afirma que toda operação existente produzirá necessariamente a saída correta. Estipular o contrato e exibir uma operação que o cumpra são etapas distintas.

## Reaproveitamento documental

[REAL — leitura dos arquivos, sem nova compilação] TheNameAndItsReferent.lean, the_identity_contract_discriminates e the_trivial_contract_does_not_discriminate, já distingue exigir o próprio conteúdo de aceitar qualquer resultado. TheJudgedThing.lean, res_judicata_is_terminal, fornece estabilidade condicional por idempotência. TheLedgerOfCharges.lean declara pagamento na face, custo no reflexo e leis de leitura próprias; the_rule_is_constant_in_the_ledger é rfl por construção, não prova que um pagamento concreto satisfaz seu objeto. Esses antecedentes motivam a articulação, mas nenhum deles é apresentado aqui como demonstração da nova definição integral.

[ESCOPO] O termo «comutação» permanece na acepção do autor, ainda sem identificação automática com comutatividade AB=BA. A cunhagem não transporta por homonímia um teorema físico ao direito. A proposta de representação fica [DERIVED]; a identificação conceitual fica [ONTO]. Nenhum original científico, kernel, Bancada, dado observado ou gate é alterado.
'''
    note = DEST/'ADENDO_REGRA_SATISFACAO.md'
    new(note,'# Regra e objeto da satisfação\n\n## Verbatim integral\n\n'+TEXT+
        '\n\nSHA256: `'+pin(original)['sha256']+'`.\n\n'+body)
    marker='rule_satisfaction_definition_20261014'
    section='\n\n## 14/10/2026 — Regra: resultado e objeto da satisfação\n<!-- '+marker+' -->\n\n'
    section+='Em nome de codex-gerente-tgl, reivindicação F1.REGRA 783. [ONTO — definição humana direta de Luiz Antonio Rotoli Miguel; verbatim]\n\n'+TEXT+'\n\n'
    section+='[PARÁFRASE DO ASSISTENTE] A exclusão incide sobre a divergência entre resultado e objeto devido. [DERIVED — contrato candidato] Admissivel(F(x),o) := não (F(x) ≠ o), com os termos no mesmo tipo, ou leitura tipada pi(F(x))=o. Idempotência estabiliza a leitura; é necessário também que o resultado satisfaça o objeto especificado. Uma leitura constante pode ser idempotente e falhar para outro objeto. Não se identifica comutação automaticamente com AB=BA. [REAL — documental] Reaproveitados TheNameAndItsReferent, TheJudgedThing e TheLedgerOfCharges, sem nova prova Lean.\n\n'
    section+='Original: `'+str(original)+'`; SHA256 `'+pin(original)['sha256']+'`. Adendo: `'+str(note)+'`. Complementa os registros coinage_rule_negative_20261014 e rule_tetelestai_correction_20261014.\n'
    surfaces=[ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',ROOT/'memory/TGL_ATLAS.md',ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    receipts=[append_bytes(p,section,marker) for p in surfaces]
    new(DEST/'MEMORY_RECEIPT.json',{'claim':claim,'surfaces':receipts})
    result=DEST/'RESULTADO_ADENDO.json'
    new(result,{'unit':'F1.REGRA','status':'CUSTODY_COMPLETED','original':pin(original),'note':pin(note),
        'sources':pin(DEST/'FONTES.json'),'memory':pin(DEST/'MEMORY_RECEIPT.json'),
        'registration':'Read MAP_RECEIPT, BOARD_RECEIPT, ACOM_RECEIPT and RELEASE for actual registration outcomes.'})
    entry=json.loads((UNIT/'TETELESTAI_20261014/MAP_ENTRY.json').read_text(encoding='utf-8'))
    entry.update({'titulo':'Precisão do operador: resultado e objeto da satisfação',
        'resultado':'Regra inadmite resultado distinto do objeto da satisfação; contrato candidato exige correspondência tipada, além da estabilidade por idempotência.',
        'defeito':'Idempotência isolada não identifica o resultado com o objeto devido; leitura constante errada é contraexemplo.',
        'veredito':'DEFINICAO_CUSTODIADA__CONTRATO_PROPOSTO','onde':str(DEST),
        'artefatos':[str(original),str(note),str(result)],'refs':[1105,1106],
        'nota':'Definição humana integral; interpretação do assistente separada; nenhuma prova nova reivindicada.'})
    new(DEST/'MAP_ENTRY.json',entry)
    mapped=register.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',DEST/'MAP_ENTRY.json','--quem',WHO+' / F1.REGRA'],'MAP_RECEIPT.json')
    board=register.call([CLI,'avancar','F1.REGRA','--quem',WHO,'--status','ENTREGUE','--evidencia',result,'--nota','Precisao humana custodiada: regra exige resultado correspondente ao objeto da satisfacao. Memoria aditiva sob reivindicacao783.'],'BOARD_RECEIPT.json')
    transition={'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),
        'expected_revision':10,'event_id':'rule-satisfaction-definition-20261014',
        'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':'rule-satisfaction-definition-20261014','kind':'fact','statute':'ONTO',
        'text':'Definicao humana: Regra é a inadmissao que o resultado da operação seja distinto do objeto de sua satisfação (pagamento, comutação). Verbatim custodiado. Contrato candidato exige correspondencia tipada entre resultado e objeto devido; idempotencia sozinha nao basta. Nenhuma nova prova Lean.',
        'sources':[{'kind':'artifact','ref':str(p),'sha256':pin(p)['sha256']} for p in [original,note,result]]}]}}
    new(DEST/'ACOM_TRANSITION.json',transition)
    memory=register.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_RECEIPT.json',transition)
    assert memory['ok']
    released=register.call([CLI,'liberar','F1.REGRA','--quem',WHO,'--nota','Definicao humana e comentario entregues com backups; unidade liberada.'],'RELEASE.json')
    print(json.dumps({'original':pin(original),'note':str(note),'map':mapped,'board':board,'acom_revision':memory['result']['revision'],'release':released},ensure_ascii=False))


if __name__=='__main__':
    main()
