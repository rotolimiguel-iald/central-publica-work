from pathlib import Path
import datetime,hashlib,json,re
W=Path(__file__).resolve().parents[1];S=W/'science/luminidic_control';R=W/'review/lum1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
receipt=json.loads((S/'RECEIPT.json').read_bytes());result=json.loads((S/'RESULT.json').read_bytes());replica=json.loads((R/'RESULT.json').read_bytes());prov=json.loads((S/'PROVENANCE.json').read_bytes())
pins=[dict(name=n,sha256=sha(S/n),verified=sha(S/n)==v['sha256'] and (S/n).stat().st_size==v['bytes']) for n,v in receipt['files'].items()]
assert all(x['verified'] for x in pins)
sources=[]
for item in prov['sources']:
 p=Path(item['path']);lines=p.read_text(encoding='utf-8-sig').splitlines()
 sources.append(dict(path=str(p),sha256=sha(p),pin_matches=sha(p)==item['sha256'],excerpts_match=all('\n'.join(lines[e['start_line']-1:e['end_line']])==e['text'] for e in item['excerpts']),alpha2_declarations=[dict(line=i,text=s) for i,s in enumerate(lines,1) if re.match(r'^ALPHA2\s*=',s)]))
assert all(s['pin_matches'] and s['excerpts_match'] for s in sources)
assert sha(prov['r2']['path'])==prov['r2']['sha256']
assert result['fixtures']==replica['fixtures'] and result['checks']==replica['checks']
artifact_matches=[]
for row in result['fixtures']:
 for suffix in ['raw','lctrl','gz']:
  n=row['fixture']+'.'+suffix;artifact_matches.append(dict(file=n,identical=(S/n).read_bytes()==(R/n).read_bytes(),sha256=sha(R/n)))
assert all(x['identical'] for x in artifact_matches)
transport=json.loads((W/'review/CONTROL_REVIEW_R1.json').read_bytes())
manifest=json.loads((W/'CONTROL_FROZEN_MANIFEST_R1.json').read_bytes())
assert all(sha(f['path'])==f['sha256'] for f in manifest['files'])
report=dict(status='PASS_WITH_SCOPE',scope='ISOLATED_MATCHED_PREDICTOR_XOR_CONTROL_ONLY',reviewer='codex-readability-reviewer',unit='F9.ACOM_SIGNAL_TRANSPORT_20261021',created_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),receipt_sha256=sha(S/'RECEIPT.json'),result_sha256=sha(S/'RESULT.json'),code_sha256=sha(S/'control.py'),source_pins=sources,artifact_pins=pins,reproduction=dict(fixtures=4,check_groups=15,negative_single_bit_flips=3824,all_artifact_bytes_match=artifact_matches,tests_equal=True,runner_and_codec_copied_byte_identically=True,environment_override='Somente platform.platform substituído no harness por sys.getwindowsversion para impedir subprocess de inventário. Código/fixtures/asserções intactos. Primeira execução parou na coleta de metadados; rerun isolado concluiu.'),
 findings=[dict(id='LUM-01',severity='BAIXO',status='DECLARED_PROVENANCE_QUALIFICATION',title='Literal do fixture difere das fontes primárias citadas',evidence='Trinity linha64 e Unified linha77 declaram ALPHA2=0.012; V13 linha113 também declara0.012. Fixture e pacote usam0.012031. PROVENANCE o chama histórico, mas não aponta fonte primária desse valor específico.',required_label='Parâmetro experimental explícito alpha2_fixture=0.012031; fórmula portada de fontes que usam ALPHA2=0.012. Não é reprodução literal da constante dessas fontes, não é beta canônico e não é nova constante física/runtime. Se mantido histórico, anexar a fonte histórica específica.',impact='Não altera igualdade XOR ou tamanhos medidos. Qualificação documental obrigatória ao reutilizar a evidência; nenhuma nova rodada só por este achado baixo.')],
 scientific_scope=['Fórmula luminídica de envelope/chirp conferida por trechos e hashes nas duas fontes; amplitude segue a variante Unified. ENVELOPE_CHIRP não é este controle e variantes homônimas não foram unificadas.', 'Fixture favorável é gerado pelo mesmo predictor Python, com parâmetros conhecidos. Não há fitting, busca/model selection, dado real independente nem validação bitwise de Torch.', 'Exatidão f32/f64 decorre de raw XOR predictor e predictor XOR resíduo, com dtype/ordem/bytes e metadados preservados. Hash confere regeneração e integridade, não corrige erros nem autentica.', 'Mesmo com fórmula idêntica, libm/Torch/JS podem produzir bits diferentes; predictor_sha256 recusa divergência. Interoperabilidade JS, fitting e ganho em dados reais permanecem não demonstrados.'],
 measurement_scope={'known_chirp_f4':'32768bytes originais; gzip30856; pacote completo520. Controle favorável de modelo compartilhado, não ganho genérico.', 'known_chirp_f8':'65536bytes originais; gzip62702; pacote completo552, mesmo alcance.', 'noise_f4':'Pacote31547 versus gzip30349: perde1198bytes.', 'noise_f8':'Pacote63480 versus gzip62673: perde807bytes.', 'accounting':'Pacote inclui parâmetros, hashes, framing e gzip do XOR. Assume predictor/decoder/versão disponíveis em ambos os lados; não inclui instalação do decoder, fitting, transporte HTTP/TLS ou latência.', 'selection':'Escolha raw/gzip quando menor é decisão do experimento, não seletor de integração implementado.'},
 combined_verdict={'status':'BLOCK_TRANSPORT_RECOVERY','luminidic_control':'PASS_WITH_SCOPE','transport_review_path':str(W/'review/CONTROL_REVIEW_R1.json'),'transport_review_sha256':sha(W/'review/CONTROL_REVIEW_R1.json'),'transport_frozen_bytes_unchanged':True,'open_blocker':'CONTROL-01: temporário órfão de bloco impede recuperação local após interrupção. Este controle de XOR não corrige o Store.'},
 exclusions=['Nenhuma proteção quântica, criptográfica ou física demonstrada.', 'Nenhuma aprovação do staging JS, integração, runtime ou fontes científicas globais.', 'Não requer confirmação pela natureza para validar bytes exatos.'],
 evidence=[dict(path=str(p),sha256=sha(p)) for p in [S/'PROVENANCE.json',S/'run_control.py',R/'RESULT.json',R/'RECEIPT.json',W/'review/run_luminidic_review.py',W/'science/SOURCE_FINDINGS_R2.json']],runtime_modified=False,science_modified=False,network_calls=0,provider_calls=0,integration_approved=False)
out=W/'review/LUMINIDIC_REVIEW_R1.json'
if out.exists():
 old=out.read_bytes();bak=out.with_name(out.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'));bak.write_bytes(old);assert bak.read_bytes()==old
raw=json.dumps(report,ensure_ascii=False,indent=2).encode();tmp=out.with_suffix('.json.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(out)
print(json.dumps(dict(status=report['status'],combined_status=report['combined_verdict']['status'],path=str(out),sha256=sha(out))))
