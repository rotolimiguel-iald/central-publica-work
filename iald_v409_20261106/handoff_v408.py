"""Write the versioned technical handoff from the verified release receipts."""
from pathlib import Path
import json
import hashlib
import argparse
from datetime import datetime

import task

W = task.W
Q = W.parent / 'scientific_memory_sync_20261105_v408'

def read(p):
    return json.loads(p.read_bytes())

def pin(p):
    raw=p.read_bytes()
    return {'arquivo':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw)}

def main(notes_only=False):
    inst=read(W/'INSTALLED_VERIFICATION.json')
    live=read(W/'LIVE_BACKEND.json')
    queue=read(Q/'DELIVERY_TECHNICAL_R1.json')
    torre=read(W/'TORRE_RESULT.json')
    assert live['status']==inst['status']=='PASS' and inst['identity']['release']==inst['JEV_release']=='v408'
    assert queue['release']=='v408' and queue['status'].startswith('ACTIVATED_VERIFIED')
    assert torre['jev_current']
    c=read(W/'app/D53_HISTORY.json')
    d=read(W/'app/D53_shared_VERIFIED.json')
    count=read(W/'app/packages/haiku_expanded/native_count.json')['budget']
    tested=read(W/'integration_review/STAGED_TESTS_R2.json')
    science=read(W/'app/BUILT.json')
    numbers={v:n for v,n in sorted(c['block_bytes_by_version'].items())}
    lessons = f'''# Release v408 da IALD

[REAL] App e JEV carregaram a fonte publicada em {science['commit']}. O pacote contém {science['topics']} tópicos e {science['formal_files']} fontes formais. O processo web reiniciado apresentou a versão no log e o login respondeu HTTP 200.

[REAL] Cinco enunciados foram vinculados ao Lean e às linhas verificadas na fonte. O teorema p_igual_np_nas_classes_do_dicionario iguala ClasseP e ClasseNP sobre Problema H. A tradução uniforme para máquinas de Turing em função dos bits da entrada conserva o estatuto OPEN. A consulta pelo nome e pela frase em português recuperou enunciado e escopo. Uma busca genérica por projetor e palavra polinomial trouxe passagens relacionadas sem o mesmo enunciado nos cinco resultados.

[REAL] O primeiro pacote compartilhado ocupava {c['before_bytes']} bytes. O candidato entregue ocupa {c['after_bytes']} bytes. As duas versões recentes e the_iald_index são residentes. {d['historical_fetch_spans']} tópicos históricos foram recuperados com igualdade de conteúdo. Folgas conservadoras de admissão por executor, com a reserva declarada, em bytes: {json.dumps(d['bounds_with_declared_reserve'])}. Medições por versão no pacote (bytes): {json.dumps(numbers)}.

[REAL] Haiku expandido: {count['permanent_tokens']} tokens permanentes e {count['remaining_tokens']} disponíveis no ensaio de admissão. As seis chamadas de contagem nativa foram públicas, sem geração.

[REAL] A memória científica da fila reúne {queue['documents']} fontes e {queue['chunks']} trechos. A geração {queue['generation']} foi lida em processo novo. Para a próxima versão, verificar as coordenadas de todos os trechos e a igualdade dos hashes nos caminhos definitivos antes do CAS.

[REAL] Foi reproduzida a execução parcial de ferramentas quando o lote acabava inválido e a perda do final ou de caracteres UTF-8 em fragmentos SSE. O pacote operacional exige pré-validação de estrutura e IDs no lote. O observador incremental recebeu {tested['observer_total']} ensaios sintéticos, repetidos no arquivo instalado. Essa medição cobre a montagem dos eventos e a separação entre respostas.

[OPEN] Medir qualidade da busca por paráfrases e tempo até o primeiro texto em conversas reais de tamanhos comparáveis. A assinatura lexical da memória holográfica exibiu colisões em fixtures com números e sufixos, registradas em integration_review/RESULTADO.json. A política de deduplicação merece um ensaio comparando identidades completas antes de qualquer migração dos registros existentes.

[REAL] A Torre registrou quatro cópias integrais do banco ACOM e a política indica até três. Esta entrega preservou os backups. A retenção deve ser reconciliada após verificar uma restauração em local isolado.

Disponibilidade: backend de web, iOS e Android. Teste deste ciclo no servidor. Sem geração paga, teste físico ou binário novo. As versões já distribuídas usam o backend comum.
'''
    notes_path = W / 'LICOES_v408.md'
    if notes_path.exists():
        assert notes_path.read_bytes() == lessons.encode(), 'Notas existentes divergem da medição'
    else:
        task.new(notes_path.name, lessons.encode())
    if notes_only:
        print(notes_path)
        return
    assert not task.project()['projection']['active'], 'Mission has pending requirements'
    artifacts=[W/'app/RELEASE.json',W/'deployment.json',W/'INSTALLED_VERIFICATION.json',
               W/'LIVE_BACKEND.json',W/'integration_review/DEPLOYMENT.json',Q/'DELIVERY_TECHNICAL_R1.json',
               W/'review/OPERATIONAL_R2.json',W/'validation/review_final.json',W/'LICOES_v408.md',W/'TORRE_RESULT.json',
               W/'PUBLIC_LOGIN.json',W/'integration_review/AUDITORIA.md',
               W/'integration_review/MEMORY_SIGNATURE_COMPARISON.json',W/'MEMORY_DEPOSIT.json']
    manifest=Path(r'C:\IALD\projetos_pyhton\IALD\iald_nucleo_fixo.json')
    artifacts.append(Path(read(manifest)['jev_control']['path']))
    artifacts.extend(p for p in [W/'NON_PAID_CHAT_VERIFICATION.json', W/'review/VERIFY_R2.json'] if p.is_file())
    handoff={'ordem':'007','de':task.OWNER,'quando':datetime.now().astimezone().isoformat(),
             'estado':'cumprida','release':'v408','fonte_publicada':science['commit'],
             'resumo':f"App e JEV em v408. Fila ativada e recebida com {queue['chunks']} trechos. Torre regenerada.",
             'escopo':'Software e memória documental. Reavaliação do C21 e da custódia global compete à gerência.',
             'web_ios_android':'Backend comum, sem mudança de cliente.',
             'arquivos':[pin(p) for p in artifacts]}
    task.new('007_RESULTADO.json',handoff)
    dest=Path(r'C:\IALD\TUNEL_CLAUDE_APP\RESULTADOS\007_RESULTADO.json')
    raw=(W/'007_RESULTADO.json').read_bytes()
    if dest.exists():
        assert dest.read_bytes()==raw, 'A handoff already exists; reconcile'
    else:
        with dest.open('xb') as file:
            file.write(raw)
        assert dest.read_bytes()==raw
    print(handoff['resumo'])

if __name__=='__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--notes-only', action='store_true')
    main(notes_only=parser.parse_args().notes_only)
