from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
OUT=R.parent/'TUNEL/DO_CHATGPT/ENTREGA_012_B2_flrw_na_metrica_da_casa.md'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) or p==OUT
    assert not p.exists();q=p.with_name(p.name+'.tmp');q.write_bytes(b)
    assert q.read_bytes()==b and b;os.replace(q,p)
def load(p):return json.loads(p.read_text(encoding='utf8'))
audit=load(R/'AUDITORIA_B2.json');review=load(R/'revisao_b2/REVIEW_B2_FINAL.json')
assert review['status']=='B2_DEV_REVIEW_ACCEPTED__INTEGRATION_NOT_REVIEWED'
assert all(not review[k] for k in ['P0','P1','P2'])
assert audit['all_trio'] and audit['negative_controls_rejected']
comp=load(Path(review['compilation']['path']))
assert comp['all_accepted_builds_exit_zero'] and comp['all_axioms_allowed'] and not comp['author_project_objects_copied']
assert comp['exact_target_count']==len(audit['targets'])==32
assert not comp['new_warnings']
files=set()
def accept(v):
    if isinstance(v,dict):
        if {'path','bytes','sha256'}<=v.keys():
            p=Path(v['path']);assert pin(p)=={k:v[k] for k in ['path','bytes','sha256']},p
            files.add(p)
        for x in v.values():accept(x)
    elif isinstance(v,list):
        for x in v:accept(x)
accept(audit);accept(review);accept(comp)
for r in comp['runs']:assert load(Path(r['run']['path']))['returncode']==0
for p in audit['sources']+audit['objects']:assert pin(Path(p['path']))==p
for p in review['new_source_object_pins']:
    if p['author'] is not None:assert p['equal_to_author']
main=[R/'kernel/TGLExt'/f'{n}.lean' for n in ['FLRWGeometry','FLRWFieldEquations','AuditFLRW']]
main += [R/p for p in ['REAPROVEITAMENTO_B2.md','REAPROVEITAMENTO_B2.json','AUDITORIA_B2.json','ALVOS_B2.json','revisao_b2/REVIEW_B2_FINAL.md','revisao_b2/REVIEW_B2_FINAL.json','revisao_b2/compilation.json','run_b2_lake.py','audit_b2.py','prepare_b2_audit.py','deliver_b2.py','CUSTODIA_V353_FONTES.json']]
files.update(main)
for folder in ['audit_B2','probes_B2','searches_B2']:
    files.update(p for p in (R/folder).rglob('*') if p.is_file())
attempts=[]
for p in sorted((R/'attempts').glob('*/run.json')):
    if p.parent.name>'20260914_162109_507348':continue
    run=load(p)
    if any('FLRW' in str(s) or 'GeneralMetricEinstein' in str(s) for s in run['command']):
        attempts.append(dict(directory=str(p.parent),returncode=run['returncode'],command=run['command']))
        files.update(q for q in p.parent.rglob('*') if q.is_file())
stamp=datetime.datetime.now().astimezone().isoformat()
table='\n'.join(f"| `{p}` | `{pin(p)['sha256']}` |" for p in main)
axioms='\n'.join(f"| `{k}` | {', '.join(v) or 'nenhum'} |" for k,v in audit['axioms'].items())
body=f'''[REAL — B2 pago: FLRW compilado e revisto na maquinaria geométrica existente. Incorporação ao um.py permanece com a gerência.]

# ENTREGA 012 / B2 — FLRW na métrica da casa

{stamp}

Foram construídos **26 teoremas e seis definições** para a métrica espacialmente plana diag(1,−a²,−a²,−a²), assinatura (+---). A inversa é identificada com `metricInverse`; a conexão é a `leviCivitaField` dessa métrica; Ricci, Einstein e a divergência do fluido são calculados pelas definições gerais existentes.

O consumidor `ChatgptAudit.FLRW.flrw_friedmann_from_general_metric` aplica de fato `metric_only_einstein_equation`. Obtém uma constante Λ em U aberto preconexo e lê as equações FLRW. Nenhuma componente Ricci/Einstein ou equação de Friedmann foi colocada como campo de entrada dessa especialização.

## Critérios, um a um

| Critério B2 | Resultado |
|---|---|
| Ficha MD/JSON anterior ao código; fornecedores por tipo/linha/hash | PAGO; 24 localizadores conferidos pela revisão. Ficha integral anexa. |
| FLRW em Coordinate4/TensorField4, assinatura da casa | PAGO; `flrw_metric_lorentz`, `flrw_metric_inverse`, `flrw_connection`, `flrw_ricci`. |
| G00, Gii e componentes fora da diagonal | PAGO; `flrw_einstein_tensor` calcula matriz completa; leituras `flrw_einstein_00` e `flrw_einstein_spatial`. |
| Ricci no cone nulo | PAGO; `flrw_null_ricci`, para o mesmo g e a mesma conexão. |
| Primeira e segunda Friedmann, aceleração | PAGO; `flrw_friedmann_first`, `flrw_friedmann_second`, `flrw_acceleration`; hE é descarregada pelo consumidor geral. |
| Continuidade do fluido | PAGO; `flrw_stress_divergence` calcula as quatro componentes, `flrw_continuity` consome divergência temporal zero. |
| Instanciar Einstein/Clausius existente | PAGO; `flrw_friedmann_from_general_metric` aplica `metric_only_einstein_equation`, sem reconstruí-lo. |
| Coeficiente 8πG/3 | PAGO sob eta=1/(4G), G>0 [INPUT]; `flrw_newton_coefficient` usa `einstein_coefficient_from_clausius`. |
| Axiomas no trio | PAGO; 32 nomes, auditor autoral e auditor independente. |
| Lake em raiz isolada | PAGO; cadeia própria recompilada e segunda reprodução própria sem objetos de projeto autorais. |
| Revisão adversarial independente | PAGO no escopo B2; P0/P1/P2 = 0/0/0. Integração da gerência ainda não revisada. |

## Equações e hipóteses que permanecem

Com κ=2π/eta e convenção `G_tensor + Λ*g = κ*T`:

```text
H = a'/a
G00 = 3H²
Gii = -(2aa''+(a')²)  (i espacial)
Ric(k,k) = 2(H²-a''/a)(k0)²  se g(k,k)=0
H² = κρ/3 - Λ/3
a''/a = -κ(ρ+3p)/6 - Λ/3
H' = -κ(ρ+p)/2
ρ' + 3H(ρ+p) = 0
```

U é aberto e preconexo; a é suave e positiva nas coordenadas temporais de U. rho e pressão são diferenciáveis localmente. **H_null e H_conservation são hipóteses explícitas**. B2 não afirma que a torre ou a natureza as fornecem. Não se divide por H; H=0 não foi excluído. Lambda é existencial e não é automaticamente zero. A identificação com outra convenção física de Lambda exige explicitar o sinal. O teorema algébrico admite eta real com a divisão total de Lean; a leitura física de Newton usa G>0 e a calibração indicada.

Não há beta nesta etapa. B3 conecta setores conservados e o mesmo beta de B1 a estes fornecedores; B4 examina separadamente a importação termodinâmica. H3, G, o Lema3 global e o fechamento perturbativo não são quitados aqui. O monólito não foi executado/importado; não foram tocados gate, dados, workers, Atlas ou fontes canônicas.

## Reprodução, auditoria e procedência

Na bancada `{R}`:

```powershell
& 'C:\\Python314\\python.exe' -X utf8 -B '.\\run_b2_lake.py' TGLExt.FLRWFieldEquations TGLExt.AuditFLRW
```

O runner chama Lake4.31.0 na raiz kernel, remove LEAN_PATH/LEAN_SRC_PATH externos e preserva snapshots dos três arquivos FLRW em nova pasta. Run autoral aceito: `{audit['positive_build']['path']}`; rc0, fontes inalteradas durante a execução.

Reprodução independente em `{R/'s'}`: primeiro `lake build TGLExt.GeneralMetricEinstein`; depois `lake build TGLExt.FLRWGeometry TGLExt.FLRWFieldEquations TGLExt.AuditFLRW TGLExt.ReviewFLRW`. Ambos rc0; 92 objetos de projeto construídos na raiz própria. Os três objetos novos coincidem byte a byte com os autorais. Os nove pacotes, incluindo Mathlib, são caches copiados e pinados; **não** houve reconstrução independente de Mathlib/toolchain. 59 avisos herdados de fornecedores, nenhum novo nos arquivos B2. O auditor próprio imprimiu tipos, universos e axiomas.

As duas sondas válidas (`probes_B2`) rejeitam por Type mismatch a troca 3→4 em G00 e a troca de sinal de Λ. Imports funcionam. A revisão leu os streams dessas sondas, sem afirmar reexecução delas. O autor relê os 941 arquivos-base e a cópia do um.py; a revisão não repetiu essa auditoria integral de preservação, e diz isso expressamente.

## Tentativas falhas preservadas

Compilações intermediárias falharam em especializações de derivadas/instâncias, avaliação de componentes e simplificação algébrica; não foram apagadas. A primeira rodada de sondas tinha erro lexical e foi **excluída** como controle matemático; os arquivos FAILED_SYNTAX e logs estão preservados ao lado da rodada corrigida. Preparação independente teve erro de encoding, interrupção e recusa Git por propriedade de diretório; retomada em cópia conferida, com safe.directory apenas no ambiente do processo. Por isso todas as compilações **aceitas** têm rc0, mas nem toda tentativa teve rc0.

O manifesto lista cada tentativa B2 selecionada por comando e seus hashes. Os primeiros runners nem sempre copiavam dependências editadas; não se reivindica snapshot completo de cada tentativa falha. A execução final aceita e a reprodução independente pinam os três arquivos finais integralmente.

## Axiomas por nome completo

| Alvo | Axiomas medidos |
|---|---|
{axioms}

## Arquivos principais

| Arquivo | SHA256 lido |
|---|---|
{table}

`MANIFESTO_B2.json` indexa também streams, objetos, revisões, runs e sondas. `RECIBO_B2.json` pina entrega e manifesto. Ambos ficam na bancada; a entrega fica na via de volta do túnel. Nenhuma entrada ext_* foi instalada no um.py: essa ação pertence à gerência, com a própria auditoria de integração.

## Ficha integral, preservada

'''+(R/'REAPROVEITAMENTO_B2.md').read_text(encoding='utf8')
put(OUT,body.encode('utf8'));files.add(OUT)
manifest=dict(timestamp=stamp,status='B2_DELIVERED__INTEGRATION_PENDING',author_audit=pin(R/'AUDITORIA_B2.json'),review=pin(R/'revisao_b2/REVIEW_B2_FINAL.json'),attempts=attempts,
 files=[pin(p) for p in sorted(files,key=str)],scope='B2 only; B3/B4 live artifacts excluded')
put(R/'MANIFESTO_B2.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'RECIBO_B2.json',json.dumps(dict(timestamp=stamp,delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B2.json')),ensure_ascii=False,indent=2).encode('utf8'))
for f in manifest['files']:assert pin(Path(f['path']))==f
print(json.dumps(dict(delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B2.json'),files=len(files),attempts=len(attempts)),ensure_ascii=False))
