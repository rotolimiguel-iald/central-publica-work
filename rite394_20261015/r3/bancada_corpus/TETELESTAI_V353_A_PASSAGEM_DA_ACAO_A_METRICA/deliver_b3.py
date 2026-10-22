from pathlib import Path
import datetime,hashlib,json,os
R=Path(__file__).resolve().parent
OUT=R.parent/'TUNEL/DO_CHATGPT/ENTREGA_012_B3_conservacao_setorial_friedmann.md'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(R) or p==OUT
    assert not p.exists();q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b and b;os.replace(q,p)
def load(p):return json.loads(p.read_text(encoding='utf8'))
audit=load(R/'AUDITORIA_B3.json');review=load(R/'revisao_b3/REVIEW_B3_FINAL.json')
assert review['status']=='B3_DEV_REVIEW_ACCEPTED__INTEGRATION_NOT_REVIEWED'
assert all(not review[k] for k in ['P0','P1','P2']) and audit['all_trio'] and audit['negative_controls_rejected']
comp=load(Path(review['compilation']['path']))
assert comp['all_accepted_builds_exit_zero'] and comp['all_axioms_allowed'] and not comp['author_project_objects_copied']
assert comp['exact_target_count']==len(audit['targets'])==22 and not comp['new_warnings']
files=set()
def accept(v):
    if isinstance(v,dict):
        if {'path','bytes','sha256'}<=v.keys():
            p=Path(v['path']);assert pin(p)=={k:v[k] for k in ['path','bytes','sha256']},p;files.add(p)
        for x in v.values():accept(x)
    elif isinstance(v,list):
        for x in v:accept(x)
accept(audit);accept(review);accept(comp)
assert load(Path(review['run']['path']))['returncode']==0
for p in review['new_source_object_pins']:
    if p['author'] is not None:assert p['equal_to_author']
main=[R/'kernel/TGLExt'/f'{n}.lean' for n in ['SectorFluidClosure','SectorFriedmann','AuditSector']]
main += [R/p for p in ['REAPROVEITAMENTO_B3.md','REAPROVEITAMENTO_B3.json','AUDITORIA_B3.json','ALVOS_B3.json','BUSCAS_B3_GRUPOS.json','revisao_b3/REVIEW_B3_FINAL.md','revisao_b3/REVIEW_B3_FINAL.json','revisao_b3/compilation.json','run_b3_lake.py','audit_b3.py','prepare_b3_audit.py','deliver_b3.py']]
files.update(main)
for folder in ['audit_B3','probes_B3','searches_B3']:
    files.update(p for p in (R/folder).rglob('*') if p.is_file())
attempts=[]
for p in sorted((R/'attempts').glob('*/run.json')):
    if p.parent.name>'20260914_164047_491748':continue
    x=load(p)
    if any('SectorFluidClosure' in str(s) or 'SectorFriedmann' in str(s) or 'AuditSector' in str(s) for s in x['command']):
        attempts.append(dict(directory=str(p.parent),returncode=x['returncode'],command=x['command']))
        files.update(q for q in p.parent.rglob('*') if q.is_file())
stamp=datetime.datetime.now().astimezone().isoformat()
ax='\n'.join(f"| `{k}` | {', '.join(v) or 'nenhum'} |" for k,v in audit['axioms'].items())
table='\n'.join(f"| `{p}` | `{pin(p)['sha256']}` |" for p in main)
body=f'''[REAL — B3 pago no escopo condicional declarado: conservação setorial ligada a B2. O caso sem Λ exige H_zero_cosmological. Incorporação pela gerência.]

# ENTREGA 012 / B3 — de H_nx à primeira equação de Friedmann

{stamp}

**14 teoremas, sete definições e a estrutura SectorFluid**, compilados e revistos independentemente. A conservação exigida pela camada Einstein é demonstrada a partir da não-troca setorial; o consumidor não a assume novamente. A conclusão geral conserva a constante cosmológica de B2.

## Critérios da ordem

| Critério B3 | Resultado |
|---|---|
| Ficha anterior ao código, seis buscas e fornecedores por tipo | PAGO; MD/JSON anexos, 14 locadores conferidos na revisão. Erros iniciais de acesso foram repetidos e registrados. |
| Setores finitos, rho_i≥0, w_i constante | PAGO; `SectorFluid`, w sem argumento temporal. |
| Não-troca nomeada | PAGO; campo `H_nx : HasDerivAt rho_i (-3H(1+w_i)rho_i)`. É INPUT, não conclusão microscópica. |
| Reescalonamento conserva a mesma continuidade | PAGO; `sector_rescaling_preserves_continuity`, depois `weighted_continuity`/`corrected_continuity`. |
| Soma corrigida e cancelamento do vácuo | PAGO; `corrected_closure`; o corolário de três setores invoca `closure_identity` e `hubble_form` existentes. |
| Mesmo beta de B1 | PAGO; `c : TGLCoupling`, uma única projeção c.beta em todos os fatores. |
| w_eff definido e leitura absoluta | PAGO; wEff=pTot/rhoTot; `effective_enthalpy` exige rhoTot>0 e enthalpy≥0. |
| Equação 00 sob B2 | PAGO com Λ existencial; `tgl_friedmann_from_sector_closure` aplica B2 e descarrega sua conservação. |
| Forma sem termo cosmológico | PAGO **condicionalmente** em `tgl_friedmann_zero_cosmological`; H_zero_cosmological é explícita. Não foi provado Λ=0. |
| Axiomas e reprodução isolada | PAGO; 22 alvos no trio, Lake autoral e Lake independente, sem objetos de projeto autorais copiados. |
| Revisão e negativos | PAGO no escopo DEV B3; P0/P1/P2=0/0/0; duas adulterações recusadas por Type mismatch. |

## Cadeia efetivamente consumida

```text
c:TGLCoupling (B1)
rhoT_i=(1+c.beta*(1+w_i))*rho_i
H_nx -> continuidade de rhoT_i -> continuidade do total corrigido
 -> sector_covariant_conservation (divergência da métrica B2)
 -> flrw_friedmann_from_general_metric (H_null permanece INPUT)
 -> existe Λ constante em U:
    H²=(8πG/3)*rhoTot*(1+c.beta*abs(1+wEff))-Λ/3
    H'=-4πG*(correctedTotalRho+correctedTotalPressure)
```

A identidade aditiva `rhoTtot=rhoTot+beta*enthalpy` vale sem sinal de entalpia. A reescrita absoluta requer rhoTot>0 e enthalpy≥0. Não se afirma positividade de cada densidade corrigida para w_i arbitrário; isso exigiria uma hipótese sobre seu fator. O suporte de densidades pode conter setores phantom nesta construção algébrica, desde que as hipóteses particulares de cada conclusão sejam satisfeitas.

U é aberto preconexo, a é suave/positiva nas coordenadas temporais de U, e esses tempos pertencem ao domínio I de H_nx. **H_null é o balanço nulo para o stress corrigido concreto**, não um teorema de realização física. G>0 e eta=1/(4G) continuam calibração INPUT. Não se divide por H. Não se declara existência de solução física não vazia. A convenção de B2 `G_tensor+Λg=κT` explica o sinal −Λ/3.

O corolário zero recebe a equação tensorial hE e H_zero_cosmological, não a própria conclusão escalar H². O resultado não autoriza eliminar a constante existencial em outro consumidor. A distinção entre rota total e setorial na segunda equação fica para B4; B3 não a resolve por escolha.

## Reprodução e alcance da revisão

Na bancada `{R}`:

```powershell
& 'C:\\Python314\\python.exe' -X utf8 -B '.\\run_b3_lake.py' TGLExt.SectorFriedmann TGLExt.AuditSector
```

Run aceito `{audit['positive_build']['path']}`: rc0; snapshots finais conferidos. Auditoria em AUDITORIA_B3. Duas sondas em probes_B3 devem falhar sob `lake env lean`: BadSectorClosure troca +beta por −beta; BadSectorAbs troca a entalpia pelo negativo. Ambas efetivamente deram Type mismatch com imports funcionais.

A revisão independente executou `lake build TGLExt.TheSameBetaReadsThreeFaces TGLExt.SectorFluidClosure TGLExt.SectorFriedmann TGLExt.AuditSector TGLExt.ReviewSector` em s, rc0. Acrescentou 17 fornecedores B1 ainda ausentes e os quatro arquivos B3/auditor: 21 objetos novos, mantendo os 92 objetos próprios de B2 idênticos (113 no total). Nenhum olean autoral foi copiado. Os três objetos do candidato coincidem byte a byte. Mathlib/toolchain e oito outros pacotes são caches herdados, pinados; não se reivindica reconstrução independente desses componentes.

O revisor leu as sondas autorais e seus streams, mas não as reexecutou. A preservação de 941 fontes-base e um.py foi medida pelo auditor autoral, sem revarredura integral pelo revisor. Não houve aviso novo; dois avisos herdados de fornecedores B1 ficaram nos logs.

## Falhas preservadas

Tentativas autorais intermediárias falharam por instâncias de derivadas, simplificação de somas, namespace da inversa, limite de heartbeats e igualdade do vetor nulo. Os snapshots/logs permanecem. A criação inicial do runner falhou na citação de string do comando Python, antes de criar arquivo; foi refeita com entrada literal. Na revisão, a primeira geração do parecer usou `lambda` como nome de argumento Python e falhou antes de gravar o parecer; histórico preservado, sem efeito no build Lean. Nenhuma falha foi promovida a prova negativa.

## Axiomas medidos

| Alvo completo | Axiomas |
|---|---|
{ax}

## Arquivos principais

| Arquivo | SHA256 lido |
|---|---|
{table}

MANIFESTO_B3/RECIBO_B3 na bancada indexam entrega, fontes, objetos, runs, revisão e sondas. Consumidores propostos: ext_tgl_friedmann_from_sector_closure_kernel_proved, ext_sector_rescaling_preserves_continuity_kernel_proved e ext_sector_effective_equation_of_state_kernel_proved. Instalação no um.py e auditoria de integração são da gerência. D1, gate, originais, memórias, TGL-S/TGL-L e Lema3 global não foram alterados.

## Ficha integral preservada

'''+(R/'REAPROVEITAMENTO_B3.md').read_text(encoding='utf8')
put(OUT,body.encode('utf8'));files.add(OUT)
manifest=dict(timestamp=stamp,status='B3_DELIVERED__INTEGRATION_PENDING',attempts=attempts,files=[pin(p) for p in sorted(files,key=str)],scope='B3 only; later live artifacts excluded')
put(R/'MANIFESTO_B3.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'RECIBO_B3.json',json.dumps(dict(timestamp=stamp,delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B3.json')),ensure_ascii=False,indent=2).encode('utf8'))
for f in manifest['files']:assert pin(Path(f['path']))==f
print(json.dumps(dict(delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B3.json'),files=len(files)),ensure_ascii=False))
