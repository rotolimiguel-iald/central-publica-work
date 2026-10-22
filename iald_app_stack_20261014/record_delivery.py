"""Append the verified operational result, with byte backups on every surface."""
from pathlib import Path
from datetime import datetime,timezone
import json,ast
from transaction import write_evidence,backup,atomic,digest
W=Path(__file__).resolve().parent
OLD=W.parent/'iald_monthly_wallet_20261007/record_memory.py'
def main():
    install=json.loads((W/'installed_verification.json').read_bytes())
    restart=json.loads((W/'restart.json').read_bytes())
    live=json.loads((W/'live_validation.json').read_bytes())
    assert install['status']==restart['status']==live['status']=='PASS'
    mobile=json.loads((W/'mobile/distribution.json').read_bytes())
    marker='IALD_APP_V392_KIMI_MIMO_PREFERENCE_20261014'
    namespace={'Path':Path}
    node=next(n for n in ast.parse(OLD.read_bytes()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='paths' for t in n.targets))
    exec(compile(ast.Module(body=[node],type_ignores=[]),'memory_surface_list','exec'),namespace)
    text=f'''\n\n## 14/10/2026 — App v392, preferência Kimi/MiMo e exame do stack\n\n<!-- {marker} -->\n\n[INPUT — ordem do operador] Atualizar o app com a última versão selada/publicada do um.py, preferir Kimi e MiMo na conversação, priorizar Kimi na implementação de código e preservar temporariamente Claude. Estudar Gemini Argon e indicar melhorias. Não muda permissões, consentimentos, carteira ou isenções.\n\n[REAL — memória instalada] Pacote v392 conferido contra originais selados, commit público imutável e recibos HTTP; release isolada preserva v390 e anteriores. Cluster411tópicos (32novos) reconstruíveis;1230fontes formais conferidas. Kernelv5 preservado byte a byte, núcleo anterior mantido com adendo. Revisão independente de fidelidade:21verificações. Parte dos campos históricos/formais é recuperável por referência, não literal em todos os prompts; a atualização não executou um.py nem Lean, não emitiu custódia nova e não moveu gate. H3/F8.1 mantêm o alcance e as ressalvas das fontes.\n\n[REAL — contexto e roteamento] Haiku5.5 manual recebe o pacote público medido em648972tokens permanentes; conectores Kimi/MiMo/DeepSeek usam representação compacta dos411tópicos e fontes completas recuperáveis,314674tokens pela contagem Anthropic apenas como proveniência. A admissão de cada conector continua própria. DeepSeek reserva a maior saída tecnicamente possível mantendo máximo393216 e piso16384, sem truncar memória/histórico, antes de chave/rede. Corrigida aceitação das ferramentas ACOM geradas pelo servidor no pacote Haiku. JEV vinculado àv392; preferência automática Kimi>MiMo>OpenAI>DeepSeek>nativa filtrada por direitos, consentimento, capacidade e orçamento. Claude fora da seleção automática; manual deLuiz preservado. Kimi é textual sem ferramentas interativas: MiMo gerencia ferramentas/artefatos e Kimi é preferido para rascunhos delegados de código. Sandbox Python Anthropic permanece recurso separado; não se promete gastoClaudezero se solicitado.\n\n[REAL — instalação] Plano1257arquivos por hash, backups de bytes, testes offline e revisão independente. A revisão encontrou corrida entre ociosidade e nova admissão; corrigida com suspensão breve do supervisor e do filho web, verificação da fila congelada e parada somente do filho antes da troca. Supervisor existente retomado emfinally; novo filho/HTTP verificados. Nenhuma conta alterada, nenhuma bancada/llama reiniciada. Resultado real do chat em live_validation.json; evidências e limites nesse recibo.\n\n[DECLARADO — Argon] Documentação Google13/10:gemini-4-argon, janela unificada1048576, entrada multimodal/saída textual, ferramentas/código/busca; não gera imagens/áudio nem ofereceLiveAPI. APIpaga:US$2/Mentrada eUS$10/Msaída até30/11/2026;US$4/20 desde01/12. Não ativado noapp, nenhuma chave/cobrança Google criada. Antigravity textual existente não comprova execuçãoArgon. Recomendado piloto interno para revisão/pesquisa, medindo custo por resultado aprovado. URLs e plano de melhorias em stack_assessment.json.\n\n[DISPONIBILIDADE] Backend compartilhado web/iOS/Android atualizado, sem necessidade de novo binário para ciência/roteamento. ContratoAppleLYL260 aceito14/10 com autorização expressa. Builds30/31 falharam no lockHomebrew; scriptCI corrigido comNode oficialpinado+SHA ebuild32 concluída. Estado observado da distribuição: {mobile['summary']} Instalação física não verificada. Android4.1(27) mantém APK/AAB preparados anteriormente; GooglePlay não publicado nestaentrega.\n\n[EVIDÊNCIAS] {W}:science/v392_verified_handoff.json,science_review/DELIVERY.json,validation/review_final.json,validation/final_checks.json,validation/wallet_regression.json,install_plan.json,deployment.json,restart.json,installed_verification.json,live_validation.json,mobile/distribution.json. ACOM própria SESSION_REFERENCE.json; unidadeF9.APP_STACK_20261014. Nenhum original científico ou acervo jurídico foi alterado.\n'''
    text += '\n[REAL — teste e limite de precisão] Uma resposta automática MiMo concluiu em67,933s (primeiro texto63,325s),228663tokens de entrada e280de saída; custo estimadoUS$0,099712005. Acertou versão/autoria/alcanceH3, mas acrescentou data incorreta do selo:14/10 é a implantação; timestamp do selo científico é2026-10-13 17:54:43. Fontes preservadas, divergência registrada; este teste não certifica exatidão irrestrita das respostas. Reutilização de contexto em cache e streaming são prioridades recomendadas.\n'
    rows=[]
    for path in namespace['paths']:
        old=path.read_bytes()
        if marker.encode() in old:rows.append({'path':str(path),'status':'already_present'});continue
        old.decode('utf-8-sig');newline='\r\n' if b'\r\n' in old else '\n'
        raw=old+text.replace('\n',newline).encode()
        saved=backup(path)
        assert path.read_bytes()==old
        atomic(path,raw)
        assert path.read_bytes().startswith(old) and len(raw)>len(old)
        rows.append({'path':str(path),'status':'appended','backup':saved,'sha256':digest(raw)})
    write_evidence(W/'memory_delivery.json',{'status':'PASS','surfaces':rows,'marker':marker})
    records=[
      {'id':'deployed-v392-stack','kind':'fact','statute':'REAL','text':'v392 instalada; preferência Kimi/MiMo; manutenção controlada e teste vivo verificados. Escopo e limites nas evidências.','sources':[{'kind':'artifact','ref':str(W/'installed_verification.json'),'sha256':digest((W/'installed_verification.json').read_bytes())},{'kind':'artifact','ref':str(W/'live_validation.json'),'sha256':digest((W/'live_validation.json').read_bytes())}]},
      {'id':'apple-contract-and-build-update','kind':'erratum','statute':'REAL','text':'LYL260 autorizado e aceito14/10; build32 concluída. '+mobile['summary'],'supersedes':'apple-current-state','sources':[{'kind':'artifact','ref':str(W/'mobile/distribution.json'),'sha256':digest((W/'mobile/distribution.json').read_bytes())}]}
    ]
    write_evidence(W/'memory_completion.json',{'operation':'transition','reference':str(W/'SESSION_REFERENCE.json'),'actor':{'id':'codex-app-01a094df','kind':'agent'},'expected_revision':1,'event_id':'app-stack-v392-delivered-20261014','changes':{'records':records,'flow':{'phase':'delivered','next_action':'Acompanhar somente pendências explicitadas na matriz; Argon proposto para piloto, não ativado; preservar a preferência até nova ordem.','handles':[{'id':'delivery','path':str(W/'delivery.json')}]}}})
    print(json.dumps({'surfaces':len(rows),'state_payload':'memory_completion.json'}))
if __name__=='__main__':main()
