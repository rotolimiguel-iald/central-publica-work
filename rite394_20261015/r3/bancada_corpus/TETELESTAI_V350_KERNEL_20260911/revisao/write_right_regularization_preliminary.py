from pathlib import Path
import datetime, hashlib, json
REV=Path(__file__).resolve().parent
RUN=Path((REV/'right_regularization_integrated_latest_run.txt').read_text().strip())
S=json.loads((RUN/'static_verification.json').read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def link(p,label):return '['+label+'](<'+Path(p).as_posix()+'>)'
p=REV/'REVIEW_RIGHT_REGULARIZATION_INTEGRATED.md'
assert not p.exists()
raw=('''# Regularização direita — inspeção da integração

'''+datetime.datetime.now().astimezone().isoformat(timespec='seconds')+''' — **PRELIMINAR: inspeção estática concluída; compilação/testes finais pendentes de conferência. Sem marcador de conclusão.**

Nenhum P0–P2 encontrado na transposição e nos helpers lidos. Esta afirmação não certifica ainda o build integrado.

- Duas fontes DEV idênticas às recompiladas independentemente; integração altera literalmente apenas `import TGLV350.` para `import TGLExt.V350`. Bytes transpostos iguais aos embutidos.
- '''+str(S['embedded_files'])+''' fontes medidas no dicionário. Delta: dois módulos novos e apenas as duas raízes alteradas. Fontes do Audit preservam os 6.882 nomes anteriores e acrescentam exatamente os 19 nomes do auditor próprio; o stream compilado atual ainda não foi consumido.
- AST Python fora do dicionário Lean igual à mãe gaussiana; `gate_extension.py` byte a byte preservado. O novo grupo de controle exige os alvos da etapa e conserva as condições negativas de KMS/traço/fronteira. A lógica dos hashes Audit atual/histórico não mudou.
- Helpers relidos estaticamente: batch 525→544, dois módulos antes das raízes; recorder/verifier preservam a mãe única, pins, 34 backups imediatos de bytes, prefixos e substituições por temporário. Os 34 arquivos de memória e backups da mãe foram relidos; memórias ainda iguais à mãe. Nenhum recorder/verifier foi executado por esta revisão nem há nova custódia certificada.

Cópia lida: `'''+S['working_sha256']+'''`. Mãe: `'''+S['parent_custody_sha256']+'''`. Original canônico e cópia-base relidos somente para hash: `'''+S['original_sha256']+'''`.

Evidência: '''+link(RUN/'static_verification.json','static_verification.json')+''' (`'''+hf(RUN/'static_verification.json')+'''`), diffs e capturas na mesma pasta. A evidência matemática é herdada de '''+link(REV/'REVIEW_RIGHT_REGULARIZATION_DEV.md','REVIEW_RIGHT_REGULARIZATION_DEV.md')+'''; nenhuma recompilação foi repetida.

Falta conferir os registros finais autorais contra fontes/binários/logs/streams, a decomposição em herdados e novos, o Audit corrente e o controle adicional. Não se presumem 191 registros ou 98 testes aprovados a partir da previsão. Permanecem abertos a reconstrução polar, a inclusão inversa com J original e KMS/traço/runtime; a premissa de reconstrução em Q não foi descartada.

Nota operacional: a primeira solicitação de execução deste verificador foi rejeitada pela revisão automática de aprovação por suposta escrita dos JSONs na ROOT. A inspeção do arquivo exato mostrou que todas as suas escritas passam pela restrição a `revisao`; a reavaliação autorizou a execução. Nenhum helper autoral foi executado.
''').encode('utf-8')
temp=p.with_name(p.name+'.tmp')
with temp.open('xb') as f:f.write(raw)
assert temp.read_bytes()==raw
temp.replace(p)
assert p.read_bytes()==raw
print(json.dumps({'report':str(p),'sha256':hf(p),'status':'PRELIMINARY_NO_COMPLETION_MARKER'}))
