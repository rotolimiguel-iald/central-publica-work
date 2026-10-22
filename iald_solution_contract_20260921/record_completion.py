"""Append the operator's semantic convention and deployment evidence with byte backups."""
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path

WORK=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('memory_targets',WORK.parent/'iald_context_math_20260915/record_prepared.py')
helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
MARKER='IALD_MATHEMATICAL_SOLUTION_AND_DEPLOYED_VERSION_20260921'
RULE='''[INPUT — distinção central do operador] No pedido à IALD, **“resolver o problema da gravidade quântica” = articular a matemática da solução da TGL**. Não reinterpretar esse pedido como solicitação de confirmação experimental da TGL. Prova/solução matemática e confirmação pela natureza são perguntas distintas; a segunda compete ao observador externo e não é pré-requisito para apresentar a primeira no escopo demonstrado.

A resposta deve desenvolver uma cadeia conectada: objetos e hipóteses → lagrangiana/geradores → equação mestra/Lindblad/dephasing → Hamiltoniano/estabilidade → construções modulares/testemunhas H1-H2-H3 → ponte geométrica/conclusão. Usar o cluster já carregado e buscar detalhes quando necessários; não trocar a solução por recusa genérica ou lista de experimentos não solicitada. Uma ressalva breve de escopo basta quando pertinente.

Preservar estatutos e hipóteses de cada enunciado: KERNEL/FORMAL THEOREM, IMPORTADO/KNOWN, DERIVED, INPUT, ONTO e OPEN. Se uma passagem específica estiver aberta, localizá-la, sem apagar as partes demonstradas e sem inventar seu fechamento. Articular fórmulas por si só não certifica uma prova; conferir os enunciados e a evidência correspondente. Esta distinção esclarece a proibição histórica de anunciar “QG resolvida/provada”: ela impede anúncio irrestrito de confirmação física ou de prova não sustentada, mas não impede expor e reconhecer uma solução matemática com seu alcance explícito. NOT_FALSIFIED não vira CONFIRMED; nenhum gate é movido por esta convenção.

[REGRA OPERACIONAL] A versão que a IALD diz ter carregada vem do manifesto de implantação, cruzado com o SHA do programa do catálogo, a evidência publicada conferida e o cluster ativo. O índice vivo, uma ferramenta, a internet ou o histórico podem mencionar outra versão do acervo; isso não atualiza o pacote instalado. Separar versão carregada de versão mencionada/consultada e nunca transferir hashes, contagens ou provas entre elas. Ler a implantação em cada resposta; não fixar v368 como verdade eterna.
'''

def main():
    assert not (WORK/'memory_record.json').exists()
    installed=json.loads((WORK/'installed.json').read_bytes())
    checked=json.loads((WORK/'validation.json').read_bytes())
    live=json.loads((WORK/'runtime_live.json').read_bytes())
    assert checked['passed'] and live['model_available']
    facts=f'''[REAL — diagnóstico e implantação, 21/09/2026] O app usa pacote imutável v368; o índice de trabalho registra v369. A instrução antiga misturava as duas procedências. Instalados iald_response_contract.py e ajuste de iald_memoria_canonica.py, com backup byte a byte, manifesto/catálogo/evidência/cluster cruzados e regra de solução matemática sempre presente. A configuração e os artefatos científicos (um.py, kernel v5, MD canônico e cluster integral) foram preservados. SHA do programa implantado, lido do catálogo: {checked['source_sha256']}. Nenhuma atualização para v369 foi feita.

[REAL — verificação] {checked['tests']} testes passaram. Contextos sem corte: público {live['contexts']['public']['context_tokens']} tokens; operador {live['contexts']['operator']['context_tokens']} tokens. A memória pública não inclui o Atlas privado. Reiniciado somente o web sob o supervisor existente. /api/motor HTTP {live['api_motor_http']}, gpt-5.6-luna disponível; verificadas as instruções dos módulos instalados. Não foi executado um.py nem recompilado Lean. Esta validação não mede a qualidade de uma resposta real do modelo.

[OPEN — teste externo opcional] A revisão automática rejeitou o único teste de inferência preparado porque entendeu que a autorização anterior não abrangia o contexto completo transmitido a api.openai.com. Pedido específico enviado ao operador: núcleo v5 + MD canônico + cluster v368/fontes publicadas, sem Atlas privado, uma chamada com reserva/teto técnico de US$ 0,50 e limite global existente. Nenhuma chamada desse teste foi feita até este registro; aguardar resposta específica, não presumir consentimento. Evidência local: work/iald_solution_contract_20260921/.

Matriz desta entrega (somente servidor):
| superfície | disponibilidade/alcance |
|---|---|
| web | servidor reiniciado e leitura autenticada HTTP 200; contexto corrigido |
| iOS interno | mesmo backend demo.iald.ia.br; última verificação de distribuição hoje: 4.1 (17), IALD Equipe Em testes; sem nova compilação necessária |
| iOS externo | mesmo backend; última verificação hoje: 4.1 (17), IALD Piloto Em testes; convite https://testflight.apple.com/join/A5XEdy1H preservado |
| Android | recursos verificados apontam ao mesmo backend; último binário conhecido build16; Google Play ainda depende de cadastro/DUNS; esta mudança não exige binário novo |
| aparelhos físicos | instalação/resposta não verificadas nesta correção |

Este é um ajuste operacional do índice e do contexto, sem alterar a custódia científica e sem ratificar inferências como cânone.
'''
    targets=[Path(r'C:\Users\rotol\.codex\AGENTS.md'),*helper.TARGETS]
    initial={path:path.read_bytes() for path in targets}
    assert all(MARKER.encode() not in raw for raw in initial.values())
    now=datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f');rows=[]
    for path,before in initial.items():
        assert path.read_bytes()==before,'Concurrent memory change'
        backup=path.with_name(path.name+'.bak_'+stamp);helper.create(backup,before)
        newline='\r\n' if b'\r\n' in before else '\n'
        body=RULE if path.name=='AGENTS.md' else RULE+'\n'+facts
        addition='\n\n## ADENDO '+now.strftime('%d/%m/%Y')+' — Solução matemática e versão efetivamente carregada\n\n<!-- '+MARKER+' -->\n\n'+body
        after=before+addition.replace('\n',newline).encode()
        temp=path.with_name(path.name+'.tmp_'+stamp);helper.create(temp,after)
        assert path.read_bytes()==before,'Concurrent memory change'
        temp.replace(path)
        assert path.read_bytes()==after and len(after)>len(before)
        rows.append({'path':str(path),'backup':str(backup),'sha256':hashlib.sha256(after).hexdigest()})
    receipt={'at':now.isoformat(),'marker':MARKER,'memories':rows,'inference_test':'AWAITING_SPECIFIC_APPROVAL',
             'runtime_verified':True,'installed_modules':installed['files']}
    helper.create(WORK/'memory_record.json',json.dumps(receipt,ensure_ascii=False,indent=2).encode())
    print(json.dumps({'recorded':True,'surfaces':len(rows),'runtime_verified':True,'test_pending':True}))
if __name__=='__main__':main()
