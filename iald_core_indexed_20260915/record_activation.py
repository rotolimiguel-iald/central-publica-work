"""Record actual activation and remaining distribution blockers, with byte backups."""
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
ROOT = Path(r'C:\IALD\projetos_pyhton\IALD')
spec = importlib.util.spec_from_file_location('prior_memory_recorder',WORK.parent/'iald_context_math_20260915/record_prepared.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
MARKER = 'IALD_INDEXED_CORE_V357_ACTIVE_20260916'


def main():
    live = json.loads((WORK/'runtime_live.json').read_bytes())
    suite = json.loads((WORK/'suite_gate.json').read_bytes())
    login = json.loads((WORK/'review_login_verified.json').read_bytes())
    probe_path = sorted(WORK.glob('model_response_*.json'))[-1]
    probe = json.loads(probe_path.read_bytes())
    installed = json.loads((WORK/'code_installed.json').read_bytes())
    assert live['local_health'] == live['public_health'] == 200 and suite['passed']
    assert probe['http_status'] == 200 and login['model_available']
    for item in installed['files']:
        assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() == item['sha256']
    now = datetime.now().astimezone()
    note = f'''[INPUT — autorização expressa recebida] Operador: “Sim, autorizo esses arquivos para api.openai.com e o teste”, respondendo à pergunta que nomeou IALD_Kernel_v5.txt e IALD_TGL_MEMORY_CORE_v1_20260915.md, envio integral à api.openai.com, uso no app e teste até US$0,03. A interpretação anterior de “ative o app” foi recusada pela revisão automática antes de qualquer chamada; rejeição e nova resposta ficam preservadas em explicit_approval.json e backup. Não há bloqueio restante de autorização para esse payload.

[REAL — ATIVO] Instalados núcleo operacional v357 + v5 integral + conciliações ao lado, cinco fontes Lean nucleares completas e estado publicado; sete documentos íntegros via search_tgl/fetch_tgl. Janela 480000 e .env preservados. Regra pública de contexto para plano gratuito evita enviar Atlas privado e diário. Não confundir esta busca lexical LOCAL com Vector Store remoto/MCP/Conversations API: esses serviços não foram criados. Originais científicos e download preservados; não houve treinamento de pesos ou movimento do gate.

[REAL — avaliação externa] Uma chamada autorizada ao gpt-5.6-luna com contexto público, v5 e novo MD: HTTP200, {probe['usage']['prompt_tokens']} tokens de entrada, {probe['usage']['completion_tokens']} de saída, fim stop, teto calculado US${probe['single_call_cap_usd']:.8f} (menor que US$0,03). Reconheceu autoria Luiz Antonio Rotoli Miguel, versão v357/v334 histórica, H_3L≥0/GKSL/dephasing, distinção Pi±/C± e G_rot/G_proj, aplicação the_master_fires e H1 contínua posterior, ratificação reservada ao operador e diferença entre contexto e treinamento. Avaliação específica de seis perguntas; não garantia de todas as respostas. Arquivo {probe_path.name}; nenhum Atlas privado enviado nesse teste.

[REAL — regressão e serviço] 33 suítes: os mesmos 24 resultados verdes e 9 vermelhos históricos, zero regressões. 18 testes específicos e 53 verificações de rotas já registrados. Atualizadas somente assinaturas de mocks e expectativas das duas ferramentas novas. Web reiniciado UMA vez: PID antigo74548, novo{live['web_pid']}; supervisor{live['supervisor_pid']} e nativa{live['native_pid']} preservados. Saúde local/pública200. Navegador autenticado mostrou Online e gpt-5.6-luna após recarga; app aberto novamente na aba17. A atualização de servidor vale para binário4.1(16) existente, sem novo build.

[REAL — revisão beta] Criada conta exclusiva iald_review_beta por autorização prévia expressa: plano gratuito, motorOpenAI, adminFalse, acesso_nativaFalse, cota própria, sem consentimento inventado. Senha aleatória apenas em C:\\Users\\rotol\\.iald_keys\\apple-beta\\review-account.json, pasta restrita ao usuário e SYSTEM; nunca imprimir senha/token. Login real local200, modelo disponível, ferramentas search_tgl/fetch_tgl presentes, ferramentas do Atlas privado ausentes, bloqueio por consentimento confirmado SEM inferência externa. Os demais usuários foram preservados; backup de bytes no mesmo diretório.

[OPEN — TestFlight NÃO ENVIADO] Grupo externo IALD Piloto (a2f7c246-06e1-4f7c-8fcd-d0c2a79cc345), app6760655636, build4.1(16). Modal “Informações de teste” da aba10 ainda aberto, usuário iald_review_beta preenchido, início de sessão obrigatório marcado, senha vazia. Contato autorizado já preenchido. Tentativa de transferência por área de transferência entre abas não funcionou; campo mascarado não retornou valor à automação. Revisão automática REJEITOU criar formulário de senha visível; NÃO contornar nem imprimir credencial. Pergunta enviada ao usuário para preencher apenas Senha na Apple usando o arquivo local e responder “preenchi”; sem resposta neste registro. Dois servidores locais de transferência foram encerrados e a aba temporária fechada; variável de senha limpa. Depois do preenchimento manual, concluir próximos passos e enviar à revisão beta; não desmarcar login obrigatório. Não há link externo de TestFlight liberado, convite enviado, aprovação beta ou instalação física confirmada nesta etapa.

[OPEN — família] Mãe e esposa usam iPhone. Pedido assíncrono de nome/e-mail da conta Apple de cada uma ainda sem resposta. Não criar identidades Apple por e-mail sem autenticação válida, não compartilhar conta admin e não abrir cadastro irrestrito. Preparar convites externos após revisão beta; o operador quer encaminhar convites. AndroidAPK4.1(16) segue existente; GooglePlay continua pendente de cadastro/D-U-N-S.

Evidências: code_installed.json, additional_test_fixtures.json, suite_gate.json, runtime_live.json, review_account_created.json, review_login_verified.json, completion.json. O antigo REVISAO_NUCLEO_V357.md ganhou adendo de ativação; preservar a preparação como histórico.
'''
    targets = list(prior.TARGETS)+[WORK/'REVISAO_NUCLEO_V357.md']
    initial = {path:path.read_bytes() for path in targets}
    assert not any(MARKER.encode() in raw for raw in initial.values())
    stamp = now.strftime('%Y%m%d_%H%M%S_%f')
    records = []
    for path,before in initial.items():
        assert path.read_bytes() == before
        backup = path.with_name(path.name+'.bak_'+stamp)
        prior.create(backup,before)
        eol = '\r\n' if b'\r\n' in before else '\n'
        addition = '\n\n### '+now.strftime('%d/%m/%Y %H:%M %z')+' — Núcleo v357 ATIVO; TestFlight aguarda etapa manual\n\n'
        addition += '<!-- '+MARKER+' -->\n\n'+note
        after = before+addition.replace('\n',eol).encode()
        temp = path.with_name(path.name+'.tmp_'+stamp)
        prior.create(temp,after)
        assert path.read_bytes() == before
        temp.replace(path)
        assert path.read_bytes() == after and len(after)>len(before)
        records.append({'path':str(path),'backup':str(backup),'sha256':hashlib.sha256(after).hexdigest()})
    result = {'at':now.isoformat(),'app_core_status':'ACTIVE','distribution_status':'APPLE_REVIEW_PASSWORD_ENTRY_PENDING',
              'family_accounts_status':'AWAITING_NAMES_AND_APPLE_EMAILS','runtime':live,'regression':suite,
              'review_login':login,'evaluation_file':str(probe_path),'memory_records':records,
              'mobile_build_changed':False,'physical_installation_verified':False}
    prior.create(WORK/'completion.json',json.dumps(result,ensure_ascii=False,indent=2).encode())
    print(json.dumps({'app_core_status':result['app_core_status'],'distribution_status':result['distribution_status'],
                      'memory_surfaces_updated':len(records),'receipt':str(WORK/'completion.json')}))


if __name__ == '__main__':
    main()
