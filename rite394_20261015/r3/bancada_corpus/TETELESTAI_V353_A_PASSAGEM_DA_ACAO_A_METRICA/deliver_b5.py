from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
OUT=R.parent/'TUNEL/DO_CHATGPT/ENTREGA_012_B5_angulo_le_a_metrica.md'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) or p==OUT
    assert not p.exists(),p
    q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b and b;os.replace(q,p)
def load(p):return json.loads(p.read_text(encoding='utf8'))
a=load(R/'AUDITORIA_B5.json');v=load(R/'revisao_b5/REVIEW_B5_FINAL.json');c=load(Path(v['compilation']['path']))
assert v['status']=='B5_DEV_REVIEW_ACCEPTED__INTEGRATION_NOT_REVIEWED' and all(not v[k] for k in ['P0','P1','P2'])
assert a['all_trio'] and a['negative_controls_rejected'] and c['all_accepted_builds_exit_zero']
assert c['all_axioms_allowed'] and not c['author_project_objects_copied'] and not c['new_warnings']
assert c['exact_target_count']==len(a['targets'])==4 and load(Path(v['run']['path']))['returncode']==0
files=set()
def accept(x):
    if isinstance(x,dict):
        if {'path','bytes','sha256'}<=x.keys():
            p=Path(x['path']);assert pin(p)=={k:x[k] for k in ['path','bytes','sha256']},p;files.add(p)
        for y in x.values():accept(y)
    elif isinstance(x,list):
        for y in x:accept(y)
accept(a);accept(v);accept(c)
for x in v['new_source_object_pins']:
    if x['author'] is not None:assert x['equal_to_author']
main=[Path(x['path']) for x in a['sources']]+[R/x for x in ['REAPROVEITAMENTO_B5.md','REAPROVEITAMENTO_B5.json','AUDITORIA_B5.json','ALVOS_B5.json','revisao_b5/REVIEW_B5_FINAL.md','revisao_b5/REVIEW_B5_FINAL.json','revisao_b5/compilation.json','run_b5_lake.py','audit_b5.py','prepare_b5_ficha.py','prepare_b5_audit.py','deliver_b5.py']]
files.update(main)
for folder in ['audit_B5','probes_B5','searches_B5']:
    files.update(p for p in (R/folder).rglob('*') if p.is_file())
attempts=[]
for p in sorted((R/'attempts').glob('*/run.json')):
    if p.parent.name>'20260914_170027_789047':continue
    x=load(p)
    if any('TheAngleReachesTheMetric' in str(s) or 'AuditMetricAngle' in str(s) for s in x['command']):
        attempts.append(dict(directory=str(p.parent),returncode=x['returncode'],command=x['command']))
        files.update(q for q in p.parent.rglob('*') if q.is_file())
stamp=datetime.datetime.now().astimezone().isoformat()
ax='\n'.join(f"| `{k}` | {', '.join(w) or 'nenhum'} |" for k,w in a['axioms'].items())
table='\n'.join(f"| `{p}` | `{pin(p)['sha256']}` |" for p in main)
body=f'''[REAL — B5 pago como reescrita angular das equações condicionais B3/B4. Quatro teoremas; nenhum conteúdo dinâmico novo. Integração pela gerência.]

# ENTREGA 012 / B5 — o ângulo lê a métrica

{stamp}

Os quatro corolários unem a mesma variável beta de TGLCoupling, a reflexão da matriz-S e as equações já demonstradas em B3/B4. Não acrescentam um segundo parâmetro ou uma segunda lei de fundo.

## Critérios

| Critério B5 | Resultado |
|---|---|
| Ficha e aproveitamento anteriores ao código | PAGO; cinco fornecedores conferidos por hash/linha; buscas com falhas de leitura repetidas e corte histórico declarado. |
| Mesmo beta e mesma matriz-S | PAGO; coupling_eq_sin_sq compõe c.reflection_weight com normSq_reflection. Beta é sin²(thetaMiguel beta), não amplitude sin(theta). |
| Φ=1+sin²(thetaMiguel beta)|1+w| | PAGO; the_angle_reaches_the_metric reescreve entropyFactor. |
| Segunda equação angular | PAGO condicional; the_passage aplica B4 com o mesmo HubbleHorizonInput, mantendo suas entradas físicas e o sinal −4πG. |
| Primeira equação angular | PAGO condicional; the_angle_reads_sector_first aplica B3, mantendo H_nx, H_null e Λ existencial. |
| Regra dos dois regimes | PAGO; nenhum theta foi inserido em r_s, D_M, l_A ou H(z); runtime não foi tocado. Não há limite ou dinâmica angular nova. |
| Axiomas e reprodução | PAGO; quatro teoremas no trio, Lake autoral e próprio independente rc0, sem avisos novos. |
| Controles adversariais | PAGO; duas adulterações de conteúdo rejeitadas por Type mismatch. |
| Aceite | PAGO no escopo DEV B5, P0/P1/P2=0/0/0; integração não revisada. |

## Conclusões e hipóteses preservadas

```text
c.reflection_weight + normSq_reflection
 -> c.beta = sin(thetaMiguel c.beta)^2
 -> Φ = 1+sin(thetaMiguel c.beta)^2 |1+w|
 -> B4: H' = -4πG [1+sin²θ_M |1+w|](ρ+p)
 -> B3: existe Λ, H²=(8πG/3)ρ_tot[1+sin²θ_M |1+w_eff|]-Λ/3
```

As duas últimas linhas são aplicações separadas de teoremas anteriores, **não uma identificação entre as duas rotas que B4 distinguiu**. B4 mantém H>0, G>0, Φ>0, diferenciabilidade, fluxo com raio de horizonte, lei diferencial de entropia e Clausius. B3 mantém setores sem troca H_nx, w_i constantes, U aberto/preconexo, a suave/positivo, tempo em I, G>0, rhoTot>0 e entalpia≥0, além de H_null para o stress corrigido. O termo −Λ/3 não foi descartado.

O kernel usa beta variável; a forma geométrica não deriva o valor experimental de alpha. O ângulo lê o mesmo fator e não seleciona lei por ajuste ou por resultado cosmológico. Nenhum observável independente foi criado, nenhum fechamento global ou perturbativo foi provado.

## Reprodução e falhas preservadas

Run final autoral `{a['positive_build']['path']}` rc0, fontes antes/depois idênticas. Na bancada `{R}`, run_b5_lake.py invoca `lake build TGLExt.TheAngleReachesTheMetric TGLExt.AuditMetricAngle` na raiz kernel. AuditMetricAngle e sondas são executados por `lake env lean`; BadAngleAmplitude troca sin² por sin; BadAngleFactor remove o termo unitário. Ambos falham por Type mismatch, sem falha de import.

O revisor compilou `lake build TGLExt.TheAngleReachesTheMetric TGLExt.AuditMetricAngle TGLExt.ReviewMetricAngle` em s, run `{v['run']['path']}`, rc0. Três novos objetos próprios; 117 objetos próprios anteriores preservados, 120 no total. Os dois objetos B5 são iguais aos autorais. Nenhum olean de projeto autoral foi copiado; Mathlib e oito pacotes auxiliares permanecem caches herdados/pinados, sem alegação de reconstrução destes.

O revisor leu fontes, ficha e controles autorais, executou sua própria auditoria de tipos/axiomas, mas não repetiu os negativos nem a varredura de 941 fontes-base e um.py. A preservação ampla foi medida pelo auditor autoral. Não houve falha de Lean ou aviso novo nas tentativas B5, nem na revisão. Falhas anteriores de acesso durante buscas foram registradas e repetidas; resultados negativos de busca não se confundem com falhas de leitura.

## Nomes completos e axiomas

| Alvo | Axiomas |
|---|---|
{ax}

## Arquivos e hashes lidos

| Arquivo | SHA256 |
|---|---|
{table}

MANIFESTO_B5 e RECIBO_B5 vinculam entrega, fontes, objetos, runs, controles e revisão. Os consumidores ext_* constam na ficha como propostas para a gerência. Nenhum gate, dado, protocolo, runtime, original, Atlas ou memória foi alterado.

## Ficha integral

'''+(R/'REAPROVEITAMENTO_B5.md').read_text(encoding='utf8')
put(OUT,body.encode('utf8'));files.add(OUT)
m=dict(timestamp=stamp,status='B5_DELIVERED__INTEGRATION_PENDING',attempts=attempts,files=[pin(p) for p in sorted(files,key=str)])
put(R/'MANIFESTO_B5.json',json.dumps(m,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'RECIBO_B5.json',json.dumps(dict(timestamp=stamp,delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B5.json')),ensure_ascii=False,indent=2).encode('utf8'))
for f in m['files']:assert pin(Path(f['path']))==f
print(json.dumps(dict(delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B5.json'),files=len(files)),ensure_ascii=False))
