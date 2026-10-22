from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent
RUN=Path((REV/'scalar_vna_integrated_latest_run.txt').read_text().strip())
s=json.loads((RUN/'static_verification.json').read_bytes())
assert not s['P0'] and not s['P1'] and not s['P2']
def link(label,p):return f'[{label}](<{Path(p).as_posix()}>)'
text=f'''# Revisão da integração — imagem escalar de von Neumann

{s['timestamp']} — **ESTRATO PRELIMINAR ESTÁTICO; veredito integrado pendente.**

Sem P0–P2 na inspeção estática concluída. O aviso de compilação/testes finais ainda é aguardado; este estrato não atribui resultados atuais aos JSONs da etapa anterior.

[REAL — bytes/AST lidos] Cópia `{s['working_sha256']}`; **903** fontes embutidas. Os quatro novos módulos coincidem com as fontes DEV próprias após substituir somente o prefixo dos imports. Os demais embutidos são idênticos à mãe, exceto as duas raízes, que receberam os quatro imports e os 27 prints esperados. A fonte de Audit contém **6.982 declarações distintas = 6.955 preservadas + 27 do manifesto**, sem perda nem mudança de multiplicidade dos nomes anteriores; isso ainda não é contagem de um stdout integrado corrente.

[REAL — leitura] AST Python fora do dicionário Lean idêntico ao backup da cópia mãe, cujo hash foi relido. `gate_extension.py` preservado. Original canônico e cópia-base relidos somente por hash, iguais a `{s['original_sha256']}`. A mãe é `right_vector_custody.json`, SHA `{s['parent_custody_sha256']}`. As 34 superfícies de memória e os pareceres custodiados conferem com ela.

Conferidos os diffs do integrador (quatro módulos e batch 598→625), compilador (quatro antes das raízes) e teste (um grupo de sete nomes, sem descarregar KMS/traço/fronteira). O grupo exige as seis flags falsas e gate/full-plan inalterados. O AST mantém a distinção: o avaliador legado recebe `formal`, `physics`, `experiment`; as flags qgf/gpf não são entradas diretas, e `kernel_frontier` é anexo posterior.

Os cinco helpers continuam com os hashes já lidos no DEV. Inspeção estática do preparador, recorder e verifier: mãe única; exigência dos pareceres lidos; fonte/binário e transposição; metadados Audit atuais/históricos; 34 backups imediatos de bytes e append/prefixo; releitura dos pares de compilação no verifier. Recorder e verifier desta etapa não foram executados por esta revisão; os artefatos de nova custódia e relatório integrado autoral estavam ausentes na leitura.

{link('Evidência estática, pins e transposições',RUN/'static_verification.json')}. {link('Fiação do gate por AST',RUN/'gate_wiring.json')}. {link('DEV independente preservado',REV/'REVIEW_SCALAR_VNA_DEV.md')}, SHA `{s['own_DEV_review_sha256']}`. Sem nova execução Lean, biblioteca, monólito, integrador, testes autorais ou recorder. Escritas exclusivamente em `revisao/`.

**Falta para concluir:** ler os seis logs finais aceitos (quatro módulos e duas raízes), todos os pares fonte/binário/log/streams atuais e sua herança, o mapa Audit reparsado do stdout corrente contra o anterior e o manifesto27, metadados atual/histórico e controles finais. Contagens esperadas não substituem essas leituras.

O alcance matemático herdado é π(N) igual ao bicomutante no mesmo H_I, transportado pela unitária linear V gaussiana. Não identifica V com J; graph-core de F, reconstrução por J, inclusão inversa, identificação de Δ^it/KMS, traço, consumo tipado e runtime permanecem abertos.
'''
out=REV/'REVIEW_SCALAR_VNA_INTEGRATED.md';raw=text.encode();old=None
if out.exists():
 old=out.read_bytes();bk=out.with_name(out.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
 with bk.open('xb') as f:f.write(old)
 assert bk.read_bytes()==old;raw=old+b'\n\n'+raw
tmp=out.with_name(out.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and (old is None or out.read_bytes()==old)
os.replace(tmp,out);assert out.read_bytes()==raw
print(json.dumps({'report':str(out),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'final':False}))
