from datetime import datetime
import hashlib,importlib.util,json
from pathlib import Path
WORK=Path(__file__).resolve().parent
ROOT=Path(r'C:\IALD\projetos_pyhton\IALD')
spec=importlib.util.spec_from_file_location('memory_targets',WORK.parent/'iald_context_math_20260915/record_prepared.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
load=lambda name:json.loads((WORK/name).read_bytes())
source=load('source_inspection.json');activation=load('activation.json');suite=load('suite_gate.json');live=load('runtime_live.json')
responses=list(WORK.glob('public_response_*.json'));assert len(responses)==1
response=json.loads(responses[0].read_bytes())
assert response['http_status']==200 and response['finish_reason']=='stop'
assert suite['passed'] and live['local_health']==live['public_health']==200
installed=load('code_installed.json')
for row in installed['files']:
    assert hashlib.sha256(Path(row['path']).read_bytes()).hexdigest()==row['sha256'],'Concurrent source edit'
manifest=json.loads((ROOT/'iald_nucleo_fixo.json').read_bytes())
notes=(
    '[INPUT] Operador relatou resposta desatualizada sobre o fechamento TGL, pediu incorporar o um.py recém-publicado e uma IALD mais assertiva como espelho. A orientação aplicada permite atestar resultados e a leitura das provas no alcance demonstrado, sem fabricar confirmação física, probabilidade ou nova execução.\n\n'
    '[REAL — causa encontrada] O catálogo Lean já correspondia ao um.py v357, mas três entradas integrais do manifesto ainda apontavam a um_grande_atrator_pt.txt, forma_canonica.md e selo.json de 25/08/2026. Foram substituídas no manifesto pelas versões públicas atuais um_absoluto_pt.txt, um_absoluto_forma_canonica.md e um_absoluto_selo.json. Originais históricos preservados. Os sete documentos integrais agora são públicos, com URLs derivadas dos nomes rastreados. HEAD local e remoto main conferiram; commit lido no source_inspection.json.\n\n'
    '[REAL — mecanismo instalado] Novo iald_estado_publicado.py relê programa (somente bytes), selo, resultados e relatório de provas; verifica hashes do selo, correspondência com o catálogo e lista de axiomas antes de gerar o estado corrente para cada requisição. 1.003 fontes Lean do catálogo coincidem com o relatório publicado (1.008 arquivos formais; 8.514 termos; _check_damming.lean é fonte auxiliar adicional no relatório). Isto é conferência documental e de hashes, não nova compilação Lean. O estado gerado diferencia os booleanos atuais da prosa histórica ainda existente nos JSONs: H1 no representante mínimo e Ato III pagos; H2/H3 no alcance geral e identificações físicas nomeadas continuam com seus escopos. Dados completos, escores e source hashes nos recibos; nenhum gate alterado.\n\n'
    '[REAL — núcleo e tom] Núcleo integral com estado publicado: 422.484 tokens na preparação; janela 400.000→480.000 para acomodá-lo. Única alteração no .env foi IALD_OPENAI_JANELA. Cotas, chaves, contas e modelos preservados, incluindo luiz somente no teto global US$3/dia. Orientação: iniciar por resultados construídos, explicar as hipóteses específicas uma vez, corrigir pendências antigas, distinguir KERNEL/IMPORTADO/ABERTO; atestar cálculo/prova/leitura quando sustentado, sem exigir experimento para reconhecer matemática. IALD como espelho é função de leitura; concordância de LLM não substitui evidência independente da natureza. Probabilidade de tokens não é probabilidade da teoria.\n\n'
    '[REAL — fonte probabilística] O JSON da publicação registra p_joint=0.5458727599916506, 3 canais admitidos de35, boolean=False e JOINT_COINCIDENCE_NOT_EXCLUDED_AT_THRESHOLD. O produto de resíduos ~5.55e-31 é marcado inválido na fonte. Estatística do protocolo não é P(TGL verdadeira) nem P(TGL falsa), e não refuta sozinha toda a teoria. Este registro atual supera apenas a afirmação histórica de que ainda não havia cálculo; preserva o sinal efetivamente emitido.\n\n'
    '[REAL — validação e operação] Seis testes adversariais de integridade/publicação passaram. Suíte protegida: 24 verdes, mesmos nove vermelhos antigos, zero regressões. Somente filho web reiniciado; novo PID46580, supervisor47020 e llama34128 preservados, saúde local e pública200. O helper de espera não reconheceu a retomada dentro do prazo; conferência independente confirmou o serviço e não houve segundo reinício. UI autenticada mostrou janela469k (480.000/1024), motorLuna, sem cota individual e globalUS$3. Binário móvel16 continua válido: alteração de servidor, sem novo build.\n\n'
    '[REAL — alcance do teste externo] Revisão automática rejeitou a avaliação com o prefixo completo por potencial conteúdo privado. Não foi contornada: preparada alternativa sem Atlas privado, memória do operador ou prefixo interno. Sete arquivos foram relidos via HTTP200 do GitHub e comparados byte a byte aos documentos locais (public_payload_audit.json). A alternativa foi aprovada e executada uma vez, máximo reservado US$0,30, no mesmo razão/teto global. Luna respondeu HTTP200: 409.418 tokens de entrada,681 de saída, limite500.000TPM; reconheceu realização contínua/H1/AtoIII e preservou False no teste de coincidência. É uma avaliação de leitura das fontes públicas, não teste externo do prefixo integral instalado. A resposta ainda faz ressalvas por item; não se afirma que o tom de toda resposta futura ficou garantido.\n\n'
    '[OPEN] Nenhuma nova compilação do kernel nem novo rito da natureza nesta etapa. Escopos abertos da v357 preservados. Google Play/D-U-N-S, privacidade/hospedagem e outras pendências anteriores não fazem parte desta correção. Nenhum envio do Atlas privado foi feito no teste autorizado nesta etapa.'
)
now=datetime.now().astimezone();stamp=now.strftime('%Y%m%d_%H%M%S_%f');rows=[]
for path in module.TARGETS:
    old=path.read_bytes();marker='IALD_V357_PUBLIC_CORE_20260915'
    assert marker.encode() not in old
    bak=path.with_name(path.name+'.bak_'+stamp);module.create(bak,old)
    nl='\r\n' if b'\r\n' in old else '\n'
    addition=('\n\n### '+now.strftime('%d/%m/%Y %H:%M %z')+' — Núcleo atualizado para a publicação v357 e leitura assertiva com escopo\n\n<!-- '+marker+' -->\n\n'+notes+'\n\nEvidências: '+str(WORK/'completion.json')+'\n').replace('\n',nl).encode()
    new=old+addition;tmp=path.with_name(path.name+'.tmp_'+stamp);module.create(tmp,new)
    assert path.read_bytes()==old,'Concurrent memory change'
    tmp.replace(path);assert path.read_bytes()==new and len(new)>len(old)
    rows.append({'path':str(path),'backup':str(bak),'before_bytes':len(old),'after_bytes':len(new)})
summary={'at':now.isoformat(),'status':'ACTIVE_UPDATED_PUBLIC_CORE','note':notes,
         'sources_commit':source['remote_commit'],'kernel_source_sha256':source['kernel']['source_sha256'],
         'context_tokens':activation['nucleus']['context_tokens'],'window':480000,'runtime':live,
         'suite_gate':{'passed':True,'green':24,'known_red':9,'new_failures':0},
         'external_test_scope':'PUBLIC_GITHUB_DOCUMENTS_ONLY__NOT_FULL_RUNTIME_PREFIX',
         'external_test_receipt':str(responses[0]),'memories_updated':rows,
         'source_links':{e['id']:e['url'] for e in manifest['entries']},
         'new_compilation':False,'new_physical_confirmation':False}
module.create(WORK/'completion.json',json.dumps(summary,ensure_ascii=False,indent=2).encode())
print(json.dumps({'receipt':str(WORK/'completion.json'),'memories_updated':len(rows),'status':summary['status']},ensure_ascii=False))
