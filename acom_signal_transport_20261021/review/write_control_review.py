from pathlib import Path
import datetime,hashlib,json
W=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def line(p,needle):return next(i for i,s in enumerate(Path(p).read_text(encoding='utf-8').splitlines(),1) if needle in s)
manifest=json.loads((W/'CONTROL_FROZEN_MANIFEST_R1.json').read_bytes())
pins=[dict(**f,verified=sha(f['path'])==f['sha256'] and Path(f['path']).stat().st_size==f['bytes']) for f in manifest['files']]
assert all(x['verified'] for x in pins)
science=json.loads((W/'science/SOURCE_FINDINGS_R2.json').read_bytes())
science_pins=[dict(id=s['id'],path=s['path'],sha256=sha(s['path']),matches=sha(s['path'])==s['sha256']) for s in science['sources']]
assert all(s['matches'] for s in science_pins)
independent=json.loads((W/'review/r1/independent_checks.json').read_bytes())
reproduced=json.loads((W/'review/r1/prototype_tests_R2.json').read_bytes())
assert reproduced['count']==55 and all(reproduced['checks'].values())
code=W/'prototype/acom_signal_codec.py';bench=W/'prototype/test_benchmark.py'
report={
 'status':'BLOCK', 'scope':'FROZEN_GENERIC_CONTROL_ONLY_NOT_ATOM_OR_RUNTIME',
 'reviewer':'codex-readability-reviewer', 'unit':'F9.ACOM_SIGNAL_TRANSPORT_20261021',
 'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'manifest_sha256':sha(W/'CONTROL_FROZEN_MANIFEST_R1.json'),
 'code_sha256':sha(code),'benchmark_R3_sha256':sha(W/'benchmark_R3.json'),
 'frozen_files':pins,
 'findings':[
  {'id':'CONTROL-01','severity':'MEDIO','status':'OPEN','file':str(code),'line':line(code,"tmp=path.with_name(path.name+'.tmp')"),
   'title':'Temporário de bloco órfão impede recuperação após interrupção',
   'reproduction':'Injeção local de interrupção entre fsync e os.rename no primeiro bloco de Store._put; fechar/reabrir SQLite e reapresentar exatamente os mesmos frames/ID. O .tmp permanece; tmp.open(xb) levanta FileExistsError. requests não contém a unidade.',
   'impact':'Store durável não consegue concluir essa unidade após interrupção sem intervenção manual. Nenhum byte incorreto foi admitido e nenhum modelo foi chamado; falha é de recuperação/disponibilidade, dentro do controle C06.',
   'required_fix':'Implementar recuperação idempotente de temporário local no escopo exclusivo do protótipo: validar destino/temporário por tamanho e hash, publicar ou substituir com segurança, preservar conflito e isolamento. Não converter a correção local em retry de execução remota. Acrescentar regressão neste ponto antes de novo congelamento.',
   'evidence':str(W/'review/r1/independent_checks.json')},
  {'id':'CONTROL-02','severity':'BAIXO','status':'DECLARED_RESIDUAL','file':str(bench),'line':line(bench,"hs=headers(list(p.encode(a,'counts'"),
   'title':'Decomposição de framing usa ID diferente do pacote medido',
   'evidence':'manifest_framing_bytes+payload_bytes fica8–20bytes abaixo de binary_packet_bytes nos12casos cold/warm: contador usa counts e medição usa fixture_mode_k.',
   'impact':'Totais de wire, escolhas e tamanhos de arquivos foram reproduzidos; inconsistência restrita à decomposição de metadados.',
   'recommendation':'Derivar componentes dos frames exatos medidos ou identificar explicitamente a diferença; corrigir aritmética junto à próxima entrega, sem rodada exclusiva por achado baixo.'}
 ],
 'validation':{'author_checks_reproduced':55,'synthetic_fixtures_reproduced':6,'independent_checks':independent['checks'],'source_and_prototype_execution':'Somente codec congelado stdlib e testes em W/review; nenhuma fonte científica executada/importada.', 'environment_note':'Primeira cópia isolada excedeu comprimento de caminho Windows e falhou no fixture; reprodução em W/review/r1 com os mesmos bytes passou. Artefatos congelados preservados.'},
 'measurement_assessment':[
  'R3 corrige contabilização de setup binary/JSON e declara que cold não era store/disco vazio. Medianas são3observações locais; setup não teve tempo registrado.',
  'Os6fixtures e totais de bytes foram reproduzidos. Textos sintéticos muito repetidos favorecem gzip; referências ganham sobretudo em reuso de dados incompressíveis quando setup/cache são contabilizados.',
  '2/10/50Mbps são cálculos de serialização, não medições de rede/TTFB/provedor. Tracemalloc mede decoder Python, excluindo buffers completos do harness. Nenhum ganho causal do átomo ou de tokens demonstrado.',
  'CHAT_WIRE_CONTRACT é proposta distinta do controle de blocos: não foi implementada/testada nem autorizada por este parecer.'
 ],
 'science_update':{'source_findings_R2_sha256':sha(W/'science/SOURCE_FINDINGS_R2.json'),'source_pins':science_pins,'assessment':'R2 localiza o uso computacional LUMINIDIO V13 e LUMINIDIC_CHIRP Trinity/Unified; corrige a lacuna de localização do uso ACOM em R1. ENVELOPE_CHIRP tem variantes distintas, exigindo gerador/versionamento explícitos. A localização não demonstra proteção quântica ou bytes exatos; predictor+resíduo ainda não é artefato final e não foi auditado aqui.','prior_science_contract':'review/SCIENCE_CONTRACT.json preservado como retrato anterior; esta atualização vai ao lado, sem negar outras provas no acervo.'},
 'limits':['Context autenticado/CSRF é simulador confiável, não implementação de autenticação.','Store é protótipo single-process sem cifragem, quotas/GC e locks multiworker; esses limites já são declarados.','8MiB é testcap; não altera contrato de produção.','Não confundir replay de recibo de transporte com autorização/reexecução de chamada remota; ledger do app continua necessário.'],
 'evidence':[{'path':str(W/n),'sha256':sha(W/n)} for n in ['review/r1/prototype_tests_R2.json','review/r1/benchmark_R2.json','review/r1/independent_checks.json','review/control_independent.py','science/SOURCE_FINDINGS_R2.json']],
 'integration_approved':False,'atom_implementation_approved':False,'runtime_modified':False,'memory_modified':False,'board_modified':False,'network_calls':0,'provider_calls':0
}
out=W/'review/CONTROL_REVIEW_R1.json'
if out.exists():
 old=out.read_bytes();bak=out.with_name(out.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));bak.write_bytes(old);assert bak.read_bytes()==old
raw=json.dumps(report,ensure_ascii=False,indent=2).encode();tmp=out.with_suffix('.json.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(out)
print(json.dumps({'status':report['status'],'findings':[f['id'] for f in report['findings']],'path':str(out),'sha256':sha(out)}))
