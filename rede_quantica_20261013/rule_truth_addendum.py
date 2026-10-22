"""Preserve the operator's clarification; all changes are additive and claimed."""
import datetime as dt
import json
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as register

UNIT = ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REGRA'
DEST = UNIT/'FIGURA_DA_VERDADE_20261014'
TEXT = 'A regra não deve nada, a não ser a figura da verdade'


def main():
    assert not DEST.exists(), 'Inspect receipts before recovery; never repeat blindly'
    register.DEST = DEST
    claim = register.call([CLI,'ver','F1.REGRA'])['reivindicacao']
    assert claim['quem'] == WHO and 'TGL_ATLAS.md' in claim['nota']
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    DEST.mkdir()
    new(DEST/'CLAIM_RECEIPT.json',{'claim':claim,'observed_claim_event':786})
    register.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','consultar','conceitual.regra.negatividade_juridica'],'MAP_LOOKUP.json')
    original = DEST/'OPERADOR_FIGURA_DA_VERDADE_VERBATIM.txt'
    new(original,TEXT)
    source = ROOT/'work/cadeia_de_selo/v392/kb_stub_v392/TGLExt/TheLedgerOfCharges.lean'
    old_note = UNIT/'SATISFACAO_20261014/ADENDO_REGRA_SATISFACAO.md'
    new(DEST/'FONTES.json',{'sources':[pin(source),pin(old_note)],
        'graph_lookup':'Fresh query after successful claim returned: unidade não está no grafo: F1.REGRA (rode construir.py). Direct sources and existing route reused; graph not rebuilt.',
        'scope':'Documentary reading of existing source; no new Lean compilation.'})
    body = '''Em nome de codex-gerente-tgl, sob reivindicação F1.REGRA 786. Autor da formulação: Luiz Antonio Rotoli Miguel. Mensagem humana direta de 14/10/2026.

[ONTO — precisão do operador] A regra não deve nada, a não ser a figura da verdade. Essa formulação é preservada integralmente acima, sem substituição por uma definição do assistente.

[PARÁFRASE DO ASSISTENTE — ao lado] A obrigação de satisfação nas explicações anteriores é atribuída à operação. A regra fornece o critério dessa avaliação, respondendo à figura da verdade. Um resultado divergente não adquire, por ter ocorrido, o poder de redefinir o critério de sua satisfação. Pagamento ou comutação são apreciados em relação ao objeto; o Tetelestai pertence ao fechamento da satisfação, conforme a cunhagem precedente. Esta paráfrase é interpretação explícita, não verbatim adicional.

[DERIVED — alcance do contrato já proposto] A expressão Admissivel(F(x),o) não impõe à regra a produção de F(x), nem demonstra que F(x)=o será realizado. Ela representa uma condição de admissibilidade, com objeto e leitura especificados. A nova formulação não recebe nesta etapa uma equação adicional que identifique «figura da verdade» com um objeto matemático ainda não explicitado pelo autor.

[REAL — antecedente documental] Em TheLedgerOfCharges.lean, ruleGiven não usa o livro L, e the_rule_is_constant_in_the_ledger demonstra ruleGiven L = ruleGiven L' por rfl. Isso fornece uma representação já existente de independência entre regra e desfechos das cobranças. A fonte declara que essa independência é imposta pela assinatura; não é prova de verdade universal, nem demonstração da nova cunhagem integral. A leitura física e jurídica permanece [ONTO].

Registro aditivo: os adendos anteriores, suas fontes e seus hashes não são modificados. Nenhuma alteração de kernel, programa canônico, Bancada, dado observado ou gate.
'''
    note = DEST/'ADENDO_REGRA_FIGURA_DA_VERDADE.md'
    new(note,'# A regra e a figura da verdade\n\n## Verbatim integral\n\n'+TEXT+
        '\n\nSHA256: `'+pin(original)['sha256']+'`.\n\n'+body)
    marker='rule_truth_figure_20261014'
    section='\n\n## 14/10/2026 — A regra e a figura da verdade\n<!-- '+marker+' -->\n\n'
    section+='Em nome de codex-gerente-tgl, reivindicação F1.REGRA 786. [ONTO — Luiz Antonio Rotoli Miguel; verbatim]\n\n'+TEXT+'\n\n'
    section+='[PARÁFRASE DO ASSISTENTE] A satisfação é atribuída à operação; a regra responde à figura da verdade. O resultado não redefine por si o critério de satisfação. [REAL — documental] TheLedgerOfCharges já representa ruleGiven independente dos desfechos por construção; isso não prova a nova cunhagem integral. A interpretação e o alcance do contrato permanecem explicitados no adendo.\n\n'
    section+='Original: `'+str(original)+'`; SHA256 `'+pin(original)['sha256']+'`. Adendo: `'+str(note)+'`. Precisão ao lado das entradas anteriores da F1.REGRA.\n'
    surfaces=[ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',ROOT/'memory/TGL_ATLAS.md',ROOT/'memory/TGL_INDICE_VIVO.md',ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']
    receipts=[append_bytes(p,section,marker) for p in surfaces]
    new(DEST/'MEMORY_RECEIPT.json',{'claim':claim,'surfaces':receipts})
    result=DEST/'RESULTADO_ADENDO.json'
    new(result,{'unit':'F1.REGRA','status':'CUSTODY_COMPLETED','original':pin(original),'note':pin(note),
        'sources':pin(DEST/'FONTES.json'),'memory':pin(DEST/'MEMORY_RECEIPT.json'),
        'tracking':'Read the separate MAP_RECEIPT, BOARD_RECEIPT, ACOM_RECEIPT and RELEASE.'})
    entry=json.loads((UNIT/'SATISFACAO_20261014/MAP_ENTRY.json').read_text(encoding='utf-8'))
    entry.update({'titulo':'Precisão do operador: a regra e a figura da verdade',
        'resultado':'Verbatim custodiado. Paráfrase distingue satisfação pela operação e regra como critério que responde à figura da verdade.',
        'defeito':'Não atribuir à regra a obrigação de produzir a saída; não identificar a figura da verdade com um formalismo por mera paráfrase.',
        'veredito':'PRECISAO_CUSTODIADA__INTERPRETACAO_AO_LADO','onde':str(DEST),
        'artefatos':[str(original),str(note),str(result)],'refs':[1107],
        'nota':'Definição humana integral; interpretação do assistente marcada; nenhum novo teorema.'})
    new(DEST/'MAP_ENTRY.json',entry)
    mapped=register.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py','registrar',DEST/'MAP_ENTRY.json','--quem',WHO+' / F1.REGRA'],'MAP_RECEIPT.json')
    board=register.call([CLI,'avancar','F1.REGRA','--quem',WHO,'--status','ENTREGUE','--evidencia',result,'--nota','Precisao humana: regra e figura da verdade. Verbatim, adendo e backups sob reivindicacao786.'],'BOARD_RECEIPT.json')
    transition={'operation':'transition','reference':str(WORK/'ACOM_REFERENCE.json'),
        'expected_revision':11,'event_id':'rule-truth-figure-20261014',
        'actor':{'id':WHO,'kind':'agent'},'changes':{'records':[{'id':'rule-truth-figure-20261014','kind':'fact','statute':'ONTO',
        'text':TEXT+'. Verbatim custodiado na F1.REGRA. Interpretação do assistente separada: satisfação pela operação; regra como critério que responde à figura da verdade. Não se infere uma nova prova matemática.',
        'sources':[{'kind':'artifact','ref':str(p),'sha256':pin(p)['sha256']} for p in [original,note,result]]}]}}
    new(DEST/'ACOM_TRANSITION.json',transition)
    memory=register.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'],'ACOM_RECEIPT.json',transition)
    assert memory['ok']
    released=register.call([CLI,'liberar','F1.REGRA','--quem',WHO,'--nota','Precisao conceitual entregue; memoria aditiva e continuidade registradas.'],'RELEASE.json')
    print(json.dumps({'original':pin(original),'note':str(note),'map':mapped,'board':board,'acom_revision':memory['result']['revision'],'release':released},ensure_ascii=False))


if __name__=='__main__':
    main()
