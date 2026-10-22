from pathlib import Path
import datetime, hashlib, json

W = Path(__file__).resolve().parents[1]
def control(id, subject, requirements, evidence):
    return dict(id=id, subject=subject, requirements=requirements, required_evidence=evidence, status='NOT_EVALUATED')

controls = [
control('C01','Contrato e bytes exatos',[
    'Definir domínio de entrada, formato wire, versão do codec, encoder/decoder e ponto exato da aplicação onde a igualdade é exigida.',
    'decode(encode(x, base), base) deve devolver exatamente os bytes originais, comprimento e ordem; comparação direta além do SHA256.',
    'Preservar UTF8, BOM, CRLF/LF, espaços, Unicode composto/decomposto, bytes nulos, binários e anexos. Canonicalização JSON só pode ser camada distinta explicitamente contratada; não chamar perda de serialização de round-trip byte-exato.',
    'Estado ACOM conserva inscrição, decisões, pendências, fontes, estatutos e handles; candidatos omitidos permanecem recuperáveis e identificados.'
],['Especificação versionada e vetores originais/wire/reconstruídos com tamanhos e hashes calculados.']),
control('C02','Sinal, dobra e representação numérica',[
    'Explicitar o que sinal/dobra representam no software e quais parâmetros, índices, dicionários, amplitudes, fases ou bases são necessários para recuperar cada entrada.',
    'Se houver representação numérica, demonstrar ausência de colisões no domínio admitido e tratar precisão finita, arredondamento, overflow e serialização; testes aproximados não satisfazem bytes exatos.',
    'Contabilizar informação lateral e custo de recuperar o original; inversibilidade de transformação não implica redução de tamanho nem protege por si só contra ruído.'
],['Algoritmo e inversa com hipóteses explícitas; vetores de fronteira; descrição de casos recusados.']),
control('C03','Base, revisão e dependências',[
    'Vincular base imutável por identidade, versão, hash e escopo autenticado; SHA igual não concede permissão de acesso.',
    'Recusar base ausente, truncada, incorreta, obsoleta ou de outra missão/titular; nunca reconstruir silenciosamente contra a base mais recente.',
    'Descrever bootstrap e recuperação autorizada da base, expiração/evicção e custo de transferência; delta pequeno não é transporte autossuficiente.',
    'Snapshot/CAS impedem aplicar transformação sobre revisão diferente; referências de anexos devem ter conteúdo, retenção e acesso verificáveis.'
],['Casos base correta/incorreta/ausente, troca concorrente e cache frio/quente; manifestação completa das dependências.']),
control('C04','Isolamento, autenticação e confidencialidade',[
    'Preservar casa, principal, missão, conta e autorização de cada leitura/escrita e referência; não compartilhar cache com vazamento entre titulares.',
    'Proteger metadados sensíveis e credenciais; hash não é criptografia nem autenticação. Se adversário puder alterar payload e digest, exigir integridade autenticada pelo protocolo existente.',
    'Não contornar consentimento, carteira, política de provedor ou guardas de novos anexos para transportar referências/deltas.',
    'Não registrar payloads privados brutos nos benchmarks; não realizar rede ou chamada de modelo nesta etapa de revisão.'
],['Modelo de ameaça e controles negativos entre escopos; fluxo de autorização e logs sanitizados.']),
control('C05','Integridade e alegação de correção de erros',[
    'Digest pode detectar alteração com as garantias próprias do esquema; não reconstrói informação perdida e não corrige erros.',
    'Testar truncamento, bit flip, duplicação, reordenação, metadados alterados e framing inválido; falha explícita antes de efeito persistente.',
    'Se houver correção de erros, declarar código, redundância, capacidade e modelo de erro; demonstrar recuperação dentro desse limite e comportamento além dele.',
    'Não atribuir propriedades de autenticação, sigilo ou correção a uma transformação apenas por ser reversível.'
],['Matriz de falhas com resultado esperado, bytes recuperados ou recusa; custo de redundância quando aplicável.']),
control('C06','Idempotência e resultado incerto',[
    'ID estável deve vincular payload, base, escopo e operação; mesmo ID com conteúdo diferente recusa.',
    'Reenvio de transporte não pode executar ação de aplicação, upload ou cobrança duas vezes; registrar intenção/resultado e recuperação duráveis.',
    'Queda antes/depois de persistir ou confirmar deve recuperar a mesma unidade; resultado externo incerto não permite repetir chamada com outro ID.',
    'Separar remontagem de chunks e retry de transporte de execução de efeitos externos.'
],['Casos duplicata, concorrência, crash/restart e confirmação perdida, sem provedores reais.']),
control('C07','Limites e recursos',[
    'Definir limites explícitos de bytes comprimidos/descomprimidos, expansão, tamanho de base, chunks, número de referências, CPU, memória e tempo.',
    'Validar comprimentos e metadados antes de alocações; decompression bombs, comprimentos negativos/overflow, aninhamento e entrada hostil recusam.',
    'Sem truncar estado obrigatório para caber; recusa deve identificar limite. Fallback só pelo contrato existente, com a mesma autorização e sem repetir efeitos incertos.',
    'Limites técnicos de anexos, extração, contexto e wire são distintos; preservar os atuais quando a integração for proposta.'
],['Limites declarados, casos de fronteira e consumo medido; comportamento de cancelamento/timeout.']),
control('C08','Streaming e atomicidade',[
    'Documentar framing, sequência, integridade por chunk e final, backpressure, cancelamento e término inequívoco; impedir mistura entre streams.',
    'Definir se partes verificadas podem ser exibidas antes da validação final; apresentação provisória não pode confirmar estado ou disparar efeitos antes do commit válido.',
    'Falha/desconexão não pode transformar saída parcial em sucesso, apagar pendência ou reiniciar provedor.',
    'Não agregar resposta inteira sem medir o impacto no primeiro byte/chunk e na memória.'
],['Casos fragmentação arbitrária, chunk fora de ordem, cancelamento e falha no último chunk; especificação do commit.']),
control('C09','Compressão e contabilidade de bytes',[
    'Comparar original e wire completo: headers, framing, digest/MAC, base/dicionário, índices, referências, redundância, base64 e bootstrap.',
    'Separar custo inicial e amortizado; informar política de cache e taxa de acerto, expansão em payload pequeno/aleatório/já comprimido.',
    'Comparar mesmos bytes com transporte atual e codecs sem perdas disponíveis no ambiente; não impor ganho universal nem ocultar casos negativos.',
    'Tokens após reconstrução devem ser contados separadamente: menos bytes de rede não implica menos tokens de inferência.'
],['Tabela reprodutível por classe de payload, tamanhos absolutos, razão definida, cold/warm e todas as dependências.']),
control('C10','Latência e causalidade',[
    'Medir separadamente encode/decode, carregamento de base, transferência, filas, primeiro byte, primeiro evento útil, stream completo e memória máxima.',
    'Usar relógio monotônico, repetições e condições registradas; publicar n, dispersão e percentis apenas com amostra adequada.',
    'Comparar baseline/candidato com mesmo corpus e condições; resultados locais/simulados não comprovam latência em produção ou do provedor.',
    'Não atribuir melhoria a ACOM, Hilbert ou dobra sem experimento que isole a contribuição; ganho de tamanho não prova ganho de tempo.'
],['Harness offline versionado, dados brutos e ambiente; conclusão limitada ao que foi medido.']),
control('C11','Pacote de Hilbert e luminídio: cadeia de evidência',[
    'Tratar a proteção alegada no CONTEXT como afirmação do operador a verificar, sem confirmá-la nem descartá-la por nomenclatura.',
    'Agente de fontes deve entregar arquivos primários, hashes, trechos/enunciados, hipóteses, estatutos e evidências de prova/execução quando pertinentes.',
    'Explicitar a correspondência entre objeto matemático/físico, pacote digital finito, canal e ameaça; não transferir uma conclusão entre esses objetos sem demonstrar a ponte.',
    'Separar analogia ONTO, teorema condicional, simulação e medição; presença de lema ou menção no Atlas não certifica compilação nem proteção de bytes nesta implementação.',
    'Se a ponte não estiver estabelecida, registrar OPEN e avaliar o codec de engenharia por seus resultados próprios; nenhuma promoção de gate científico.'
],['Mapa afirmação→fonte→hipóteses→artefato→controle aplicável; conclusão explícita sobre alcance e lacunas.']),
control('C12','Corpus e revisão independente final',[
    'Corpus inclui vazio, um byte, texto PT/Unicode, conversas reais sanitizadas, documentos, binários, dados repetidos, aleatórios e já comprimidos; não usar apenas exemplos favoráveis.',
    'Exigir casos determinísticos com seeds, vetores negativos e diferenças adversariais no mesmo escopo; fixtures e resultados devem ser reproduzíveis offline.',
    'Congelar protótipo, fontes, dependências, fixtures e recibos por hash antes do parecer final; quem constrói não aprova seu próprio artefato.',
    'PASS de critérios não é PASS de protótipo nem autorização de instalação. Plano de integração, rollback e política de negociação/versionamento exigem revisão própria se propostos.',
    'Manter ciência/runtime/memórias/board intactos nesta etapa; sinalizar cada controle como PASS, BLOCK ou NOT_EVALUATED com evidência, sem aprovação de artefato inexistente.'
],['Manifesto congelado e relatório de execução do autor; revisão independente separada com escopo, findings e hashes.'])
]

sources=[]
for name in ['CONTEXT.json','OPERADOR.txt','SESSION_REFERENCE.json','UNIT.json']:
    p=W/name;sources.append(dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),role='Contexto da missão; não prova de eficácia'))
atlas=Path(r'C:\IALD\Central de Patentes\memory\TGL_ATLAS.md')
lines=atlas.read_text(encoding='utf-8').splitlines()
start=next(i for i,s in enumerate(lines,1) if s.startswith('**Pacote de Hilbert**'))
sources.append(dict(path=str(atlas),sha256=hashlib.sha256(atlas.read_bytes()).hexdigest(),lines=[start,start+12],role='Índice/remissão de vocabulário apenas; fonte primária e ponte digital pendentes'))
report=dict(status='CRITERIA_PREPARED_NOT_AUDITED',unit='F9.ACOM_SIGNAL_TRANSPORT_20261021',reviewer='codex-readability-reviewer',created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),authority='Pedido explícito humano desta missão; inscrição Prossiga com tudo não amplia o escopo específico de revisão.',scope='Preparação de critérios; fontes em levantamento e protótipo em desenvolvimento. Escrita apenas W/review.',session_reference=str(W/'SESSION_REFERENCE.json'),memory_projection_revision=0,controls=controls,sources=sources,final_review_requires=['Fontes primárias e manifesto hash do agente de fontes','Protótipo e contrato congelados com hashes','Resultados offline e medições comparativas','Identidade do autor e escopo exato da entrega'],acceptance_policy={'lossless_and_isolation':'Qualquer divergência de bytes, fuga de escopo, bypass de autorização ou repetição incerta bloqueia integração.','claims':'Ganho não medido ou proteção Hilbert sem ponte demonstrada permanece OPEN; não pode ser anunciado como confirmado.','performance':'Ausência de ganho não equivale a corrupção, mas impede aprovação da alegação de melhoria; registrar tradeoffs e limite medido.','current_verdict':'Nenhum artefato de implementação aprovado.'},execution={'tests_run':0,'external_api_calls':0,'runtime_modified':False,'memories_modified':False,'board_modified':False,'scientific_gate_changed':False},notification='Este arquivo é o handoff de critérios ao coordenador; revisão final e aviso sobre artefatos dependem de sua disponibilização. Nenhum monitor/agendamento criado.')
out=W/'review/CRITERIA.json'
raw=json.dumps(report,ensure_ascii=False,indent=2).encode('utf-8')
if out.exists():
    old=out.read_bytes();bak=out.with_name(out.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));bak.write_bytes(old);assert bak.read_bytes()==old
tmp=out.with_suffix('.json.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(out)
print(json.dumps(dict(path=str(out),status=report['status'],controls=len(controls),sha256=hashlib.sha256(raw).hexdigest()),ensure_ascii=False))
