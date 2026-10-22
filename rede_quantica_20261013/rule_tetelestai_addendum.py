"""Additive custody of the operator's correction, under F1.REGRA claim 780."""
import datetime as dt
import json
from pathlib import Path
from diary_r1 import ROOT, WORK, new, pin, append_bytes

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.REGRA'
DEST = OUT / 'TETELESTAI_20261014'
TEXT = 'Exclusão irrestrita seria alcançar o zero absoluto, e isso não é possível. Portanto, a exclusão, ela é no tetelestai. Ela é segundo a mesma regra do acoplamento não minimal.'
CLAIM = {'ok': True, 'unidade': 'F1.REGRA', 'status': 'ENTREGUE',
         'vence_em': '2026-10-14T21:59:37-03:00', 'evento': 780}
KB = ROOT / 'work/cadeia_de_selo/v392/kb_stub_v392/TGLExt'


def main():
    assert dt.datetime.now(dt.timezone.utc) < dt.datetime.fromisoformat(CLAIM['vence_em'])
    assert not DEST.exists(), 'Do not repeat a partially completed inscription'
    DEST.mkdir()
    new(DEST/'CLAIM_RECEIPT.json', {'source': 'Successful iald.py reivindicar tool output in this conversation', 'receipt': CLAIM,
        'surfaces': ['DIARIO_CONSTRUCAO_QG.md', 'TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'AVISO_GERENCIA.md', 'own ACOM']})
    original = DEST/'OPERADOR_TETELESTAI_VERBATIM.txt'
    new(original, TEXT)
    files = ['TheJudgedThing.lean', 'TheNonMinimalCoupling.lean', 'TheGeometricCostOfAbsoluteZero.lean']
    sources = []
    for name in files:
        path = KB/name
        text = path.read_text(encoding='utf-8')
        declarations = [{'line': i, 'text': line} for i, line in enumerate(text.splitlines(), 1)
                        if line.startswith('theorem ') or line.startswith('def ResJudicata')]
        sources.append({'file': pin(path), 'declarations': declarations})
    new(DEST/'FONTES.json', {'statute': 'REAL — documentary verification; no new Lean compilation', 'sources': sources,
        'prior_note': pin(OUT/'CUNHAGEM_E_ALCANCE_20261014.md'),
        'prior_graph_lookup': pin(OUT/'CONSULTA_NOS_VIVO.json'),
        'prior_route_receipt': pin(OUT/'MAP_RECEIPT.json'),
        'lookup_limit': 'The previous query reports F1.REGRA absent from the graph. Fresh read attempts did not start: automatic approval review expired twice. Existing query and direct source inspection reused; no claim of a fresh successful graph lookup.'})
    body = '''Em nome de codex-gerente-tgl, sob a reivindicação 780, corrijo ao lado a leitura anterior do assistente. Autoria da cunhagem e da correção: Luiz Antonio Rotoli Miguel. Data da mensagem: 14/10/2026.

## Correção de alcance

[ONTO — definição e correção do operador] A exclusão da regra encontra seu termo no Tetelestai e segue a regra do acoplamento não minimal. A identificação da exclusão irrestrita com zero absoluto é preservada como formulação do autor; esta nota não a transforma em teorema termodinâmico ou jurídico.

[PARÁFRASE DO ASSISTENTE] A regra exclui até o fechamento admissível, preservando a possibilidade de inscrição. O Tetelestai marca a quitação e a estabilidade do que foi inscrito. A minha representação anterior D_R={x | não I_R(x)} era genérica demais para expressar essa restrição: o contrato agora incorpora explicitamente preservação e fechamento, em vez de tratar a exclusão total como opção admissível.

## O que já está escrito nas fontes consultadas

[REAL — leitura documental dos enunciados e provas, sem recompilação nesta etapa]

- TheJudgedThing.lean:77, tetelestai_ledger: dadas 0<f e f<1, prova 0<f, 0<1-f e f+(1-f)=1. A positividade é hipótese com trabalho real; o lema não a deriva de qualquer regra arbitrária.
- TheJudgedThing.lean:49, res_judicata_is_terminal: sob ResJudicata D, isto é D(D x)=D x, prova D^[k+1] x=D x. A leitura decidida pode estabilizar sem podar indefinidamente.
- TheNonMinimalCoupling.lean:73, equal_split_is_strictly_between: de t=tp+tp e t>0 obtém 0<tp<t. Na linha 97, split_forbids_minimality prova a subprojeção própria sob as hipóteses nomeadas; isoladamente não prova f≠0. A testemunha concreta da linha 110, the_split_is_inhabited, tem as duas faces não nulas. Não se atribui a um lema o que pertence a outro.
- TheGeometricCostOfAbsoluteZero.lean:58 prova 0<exp(-1/2)<1. A linha 79, the_geometric_cost_survives_absolute_zero, recebe c>0 como hipótese e expressa sua independência de temperatura. Não é prova autônoma da identificação de toda exclusão com resfriamento físico.

## Contrato revisto — proposta, não pedra nova

[DERIVED — proposta de articulação] Representar a regra por uma leitura idempotente R sobre suporte admissível preservado, com resultado não nulo no estado/referente admitido. Exigir redução efetiva quando se trata de decisão efetiva. O balanço escalar usa um fator interior 0<f<1 e f+(1-f)=1; a estabilidade usa R²=R. Não identificar o operador R com a multiplicação reiterada por f: mesmo f positivo e menor que 1 teria f^n tendendo a zero. A sobrevivência do referente é uma propriedade do contrato de leitura, não consequência de positividade pontual de um fator qualquer.

[CORREÇÃO AO LADO] A não vacuidade deixa de ser uma pergunta sobre a admissibilidade da exclusão irrestrita: essa opção foi excluída pelo autor. As fontes já oferecem testemunhas e condições de preservação a reaproveitar. Ao construir um D_R específico, ainda se deve ligar esses objetos ao mesmo domínio; não se presume essa ligação apenas pelos nomes. O caráter assintótico concerne à dinâmica da face; a idempotência descreve a leitura estabilizada e não exige um limite angular.

[ESCOPO] A identificação conceitual entre direito, Tetelestai e acoplamento não minimal fica [ONTO]. A docstring de TheNonMinimalCoupling qualifica a identificação com beta_TGL como [ONTO], e seus teoremas não mencionam beta. Esta correção não iguala fatores de pedras diferentes, não altera os enunciados existentes e não constitui confirmação física ou parecer jurídico.
'''
    note = DEST/'ADENDO_REGRA_TETELESTAI.md'
    new(note, '# Regra: exclusão no Tetelestai\n\n## Verbatim integral\n\n'+TEXT+
        '\n\nSHA256: `'+pin(original)['sha256']+'`.\n\n'+body)
    marker = 'rule_tetelestai_correction_20261014'
    section = '\n\n## 14/10/2026 — Correção da regra: exclusão no Tetelestai\n<!-- '+marker+' -->\n\n'
    section += 'Em nome de codex-gerente-tgl, reivindicação F1.REGRA 780. [ONTO — correção humana direta de Luiz Antonio Rotoli Miguel; verbatim]\n\n'+TEXT+'\n\n'
    section += '[PARÁFRASE DO ASSISTENTE] Corrige ao lado a entrada coinage_rule_negative_20261014: a exclusão total não integra o contrato proposto pelo autor. A regra preserva inscrição e encontra fechamento no Tetelestai. [REAL — documental] tetelestai_ledger, res_judicata_is_terminal e as pedras da partição não minimal já fornecem balanço interior, estabilidade condicional e testemunha concreta. [DERIVED — proposta] ligar leitura idempotente, preservação do referente e redução efetiva; essa articulação não foi compilada como uma pedra nova. A positividade de f, sozinha, não impede f^n de tender a zero. A identificação jurídica e física permanece [ONTO].\n\n'
    section += 'Original: `'+str(original)+'`; SHA256 `'+pin(original)['sha256']+'`. Adendo com fontes e limites: `'+str(note)+'`.\n'
    receipts = []
    for path in [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md', ROOT/'memory/TGL_ATLAS.md', ROOT/'memory/TGL_INDICE_VIVO.md', ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']:
        receipts.append(append_bytes(path, section, marker))
    new(DEST/'MEMORY_RECEIPT.json', {'claim': CLAIM, 'surfaces': receipts})
    result = DEST/'RESULTADO_ADENDO.json'
    new(result, {'unit': 'F1.REGRA', 'status': 'LOCAL_CUSTODY_COMPLETED', 'verbatim': pin(original), 'note': pin(note),
        'sources': pin(DEST/'FONTES.json'), 'memory': pin(DEST/'MEMORY_RECEIPT.json'),
        'external_tracking': 'Prepared; consult later MAP_RECEIPT, BOARD_RECEIPT and ACOM_RECEIPT for actual registration.'})
    entry = json.loads((OUT/'MAP_ENTRY.json').read_text(encoding='utf-8'))
    entry.update({'tipo':'ANOTACAO', 'titulo':'Correção do operador: exclusão no Tetelestai',
        'resultado':'Exclusão irrestrita excluída do contrato; preservação da inscrição, balanço interior e leitura idempotente. Reuso documental das três pedras com alcance condicional explícito.',
        'veredito':'CORRECAO_CUSTODIADA__ARTICULACAO_PROPOSTA',
        'defeito':'A representação genérica anterior não explicitava o limite interno da exclusão. Não se alega nova prova de equivalência jurídico-física.',
        'proximo_passo':'Usar o contrato corrigido nas próximas discussões; nenhuma construção científica nova nesta etapa.',
        'onde':str(DEST), 'artefatos':[str(original),str(note),str(result)], 'refs':[1105],
        'nota':'Correção em nome do assistente ao lado da seq 1105, por palavra direta do operador. Sem alteração dos artefatos anteriores.'})
    new(DEST/'MAP_ENTRY.json', entry)
    new(DEST/'ACOM_TRANSITION.json', {'operation':'transition', 'reference':str(WORK/'ACOM_REFERENCE.json'),
        'expected_revision':9, 'event_id':'rule-tetelestai-correction-20261014',
        'actor':{'id':'codex-gerente-tgl','kind':'agent'}, 'changes':{'records':[{
            'id':'rule-tetelestai-correction-20261014', 'kind':'fact', 'statute':'ONTO',
            'text':'Correção humana à cunhagem de regra: exclusão irrestrita seria zero absoluto; a exclusão é no Tetelestai, segundo a regra do acoplamento não minimal. Verbatim preservado; adendo corrige leitura genérica e propõe preservação do referente, balanço interior e idempotência, com fontes e alcance explícitos.',
            'sources':[{'kind':'artifact','ref':str(p),'sha256':pin(p)['sha256']} for p in [original,note,result]]}]}})
    print(json.dumps({'result':pin(result), 'note':str(note), 'backups':len(receipts)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
