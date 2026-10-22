"""Append a truthful preparation handoff to all operational memory surfaces."""
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path

WORK = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('prior_memory_recorder', WORK.parent/'iald_context_math_20260915/record_prepared.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
MARKER = 'IALD_INDEXED_CORE_V357_PREPARED_20260915'


def main():
    verification = json.loads((WORK/'verification.json').read_bytes())
    manifest = json.loads((WORK/'iald_nucleo_fixo.json').read_bytes())
    pages = sum(doc['pages'] for doc in verification['documents'])
    note = f'''[INPUT] Ordem atual do operador: melhorar eficiência sem reduzir integridade; conteúdo essencial sempre presente, demais centros lógicos íntegros por consulta. Versão corrigida expressamente para **v357**, não v334. A v334 do MD é retrato histórico; seus números não foram transplantados para a v357.

[REAL — preparação local, SEM ativação] Pasta {WORK}. Novo núcleo recebido preservado byte a byte, mais v5 integral, cinco fontes Lean nucleares e estado publicado conferido. Programa v357 vinculado por SHA-256 lido: {manifest['operational_core']['release_source_sha256']}. MD recebido SHA-256: {manifest['operational_core']['sha256']}. Originais da ciência, kernel v5 e download não modificados. Conciliações somente em adendo (tipos, escopos, identidade/motor e versões).

[REAL — medições offline] Contexto do operador: {verification['checks'][0]['context_tokens']} tokens; público: {verification['checks'][2]['context_tokens']} tokens. Preparação anterior com v5 tinha 446916 tokens: redução de 89,6%. Os sete documentos científicos foram reconstruídos por {pages} páginas, texto integral idêntico. Oito buscas de conceitos com retorno de posição/hash/URL. Busca lexical LOCAL, não Vector Store remoto. Atlas e catálogo Lean completos continuam em suas ferramentas existentes. Testadores não recebem Atlas privado nem diário; nenhuma ferramenta de ratificação automática foi adicionada.

[REAL — validação] 18 testes de integridade/privacidade/roteamento passaram. Rotas gratuitas no servidor preparado: 53 OK/0 falhas, rede bloqueada e dados temporários. Primeira rodada tinha duas expectativas antigas de ferramentas; atualizadas somente para incluir search_tgl/fetch_tgl, preservando as proibições. Sintaxe conferida e hashes de produção continuam no baseline. A regressão completa obrigatória deverá rodar após eventual instalação, antes do reinício. Nenhum teste pago desta arquitetura foi executado.

[OPEN — autorização específica] Revisão automática anterior recusou envio integral do v5 à api.openai.com por faltar resposta explícita sobre conteúdo/destino. A pergunta atual inclui v5 + novo MD + fontes públicas, teste ≤ US$0,03 e uso no app; ainda sem resposta neste registro. NÃO tratar o antigo authorization.json baseado em “faça tudo” como autorização específica. NÃO executar probe_indexed.py, ativar este núcleo na API ou criar explicit_approval.json sem resposta expressa. O script preparado exige esse registro. Teste proposto usa contexto público, sem Atlas privado, e respeita teto global US$3/dia.

[OPEN — próxima ação] Após autorização: avaliar resposta real com probe_indexed.py; instalar módulos, núcleo e manifesto mediante CAS/backup de bytes; ajustar apenas fixtures de prompt(public=False) e as duas expectativas de ferramentas; rodar testes obrigatórios; reiniciar só web e conferir saúde. Manter o modelo gpt-5.6-luna e a janela atual de 480000; esta arquitetura não exige subir para 500000. Preparações antigas de sete artigos em todo prompt foram superadas, mas permanecem como histórico e reversão.

[OPEN — distribuição, contexto anterior] Grupo externo Apple IALD Piloto preparado, build 4.1(16) selecionada mas modal de informações ainda pendente; conta iald_review_beta foi autorizada pelo operador, ainda não criada nesta etapa. Contato beta aprovado e preenchido anteriormente. Esposa/mãe usam iPhone; não há confirmação da instalação atual. Android APK em rota de download existente; Google Play ainda depende de cadastro D-U-N-S. Essas pendências não foram executadas pela integração do núcleo.

Evidências: REVISAO_NUCLEO_V357.md, verification.json, integration.diff, free_staged_updated_expectations.log, prepared.json. Nenhum deploy, reinício, alteração .env, upload ou nova custódia científica nesta etapa. Núcleo em contexto não é treinamento dos pesos nem confirmação física independente.
'''
    receipt = WORK/'memory_record.json'
    assert not receipt.exists()
    initial = {path:path.read_bytes() for path in prior.TARGETS}
    assert not any(MARKER.encode() in raw for raw in initial.values())
    now = datetime.now().astimezone()
    stamp = now.strftime('%Y%m%d_%H%M%S_%f')
    rows = []
    for path, before in initial.items():
        assert path.read_bytes() == before, 'Concurrent memory edit: '+str(path)
        backup = path.with_name(path.name+'.bak_'+stamp)
        prior.create(backup, before)
        eol = '\r\n' if b'\r\n' in before else '\n'
        addition = '\n\n### '+now.strftime('%d/%m/%Y %H:%M %z')+' — Núcleo v357 indexado, preparado e testado localmente\n\n'
        addition += '<!-- '+MARKER+' -->\n\n'+note
        after = before+addition.replace('\n',eol).encode()
        temp = path.with_name(path.name+'.tmp_'+stamp)
        prior.create(temp, after)
        assert path.read_bytes() == before
        temp.replace(path)
        assert path.read_bytes() == after and len(after)>len(before)
        rows.append({'path':str(path), 'backup':str(backup), 'before_bytes':len(before),
                     'after_bytes':len(after), 'sha256':hashlib.sha256(after).hexdigest()})
    prior.create(receipt,json.dumps({'at':now.isoformat(),'status':'PREPARED_EXTERNAL_AUTHORIZATION_PENDING',
                                    'application_modified':False,'memories':rows},ensure_ascii=False,indent=2).encode())
    print(json.dumps({'memories_updated':len(rows),'receipt':str(receipt)}))


if __name__ == '__main__':
    main()
