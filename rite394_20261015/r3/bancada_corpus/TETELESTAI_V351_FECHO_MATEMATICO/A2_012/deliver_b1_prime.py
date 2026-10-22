from pathlib import Path
import hashlib,json,datetime,os,re
ROOT=Path(__file__).resolve().parent
CHAT=ROOT.parents[1]
B=CHAT/'B1_PRIME_012'; V=CHAT/'REVISAO_B1_PRIME_012'
OUT=CHAT/'TUNEL/DO_CHATGPT'
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
    assert p.is_relative_to(CHAT) and not p.exists() and b
    t=p.with_suffix(p.suffix+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
seal=json.loads((V/'SELO_REVISAO.json').read_text(encoding='utf8'))
for p in seal['files']: assert pin(Path(p['path']))==p
audit=json.loads((V/'AUDITORIA_INDEPENDENTE.json').read_text(encoding='utf8'))
assert audit['decision']=='ACEITAVEL_NO_ESCOPO_CONDICIONAL_DO_ADENDO_012_PARAGRAFO_4'
assert not audit['findings']
sources=[B/'kernel/TGLExt'/n for n in ['TheSameBetaReadsFourFaces.lean','ActionCouplingControls.lean','AuditSameBetaFourFaces.lean']]
counts=[]
for p in sources:
    s=p.read_text(encoding='utf8')
    counts.append(dict(**pin(p),theorems=len(re.findall(r'^\s*theorem\s+\w+',s,re.M)),
        definitions=len(re.findall(r'^\s*(?:noncomputable\s+)?def\s+\w+',s,re.M))))
files=sources+[B/n for n in ['REAPROVEITAMENTO_B1_PRIME.md','REAPROVEITAMENTO_B1_PRIME.json','ADENDO_REAPROVEITAMENTO.md',
    'AUDITORIA_B1_PRIME.json','LIMITES.md','PROPOSTA_CONSUMIDOR.json','ERROS_E_CORRECOES.md','MANIFESTO_B1_PRIME.json']]
files += [V/n for n in ['REVISAO_B1_PRIME.md','AUDITORIA_INDEPENDENTE.json','SELO_REVISAO.json','BUILD.json','AUTHOR_CONTROLS_RERUN.json','INDEPENDENT_CONTROLS.json']]
files += [ROOT/'primary'/n for n in ['ARTIGO_A_EXCERTOS.md','PROVENIENCIA_ARTIGO_A.json']]
manifest=OUT/'ENTREGA_012_B1_PRIME_quarta_face_manifesto.json'
put(manifest,json.dumps(dict(timestamp=datetime.datetime.now().astimezone().isoformat(),files=[pin(p) for p in files],
    source_counts=counts,review=seal['decision'],integration=False,gate_changed=False),ensure_ascii=False,indent=2).encode('utf8'))
text='''[REAL — B1′ compilado e revisto independentemente no escopo CONDICIONAL do §4; incorporação não executada]

# ENTREGA 012 — quarta face do mesmo β

A hipótese nomeada da EOM foi tipada com ξ separado de β e K∂ explicitamente fornecido. `the_same_beta_reads_four_faces` consome B1 diretamente e acrescenta a EOM declarada no Artigo A. Sua prova é uma conjunção de B1 com essa hipótese: não é derivação variacional, seleção independente de β ou solução física.

## Critérios do adendo

| Critério | Estado e alcance |
|---|---|
| Ficha anterior ao código, fornecedores e consumidor | PAGO: REAPROVEITAMENTO_B1_PRIME.md/json e adendo; ext_pb_same_beta_four_faces_kernel_proved proposto, não instalado |
| Campo, ξ, curvatura, operador e K∂ tipados | PAGO condicionalmente em ActionCouplingData; o tipo não constrói um d’Alembertiano nem o gerador diferencial da torre |
| Preservar B1 e reunir a quarta face | PAGO: aplicação de the_same_beta_reads_three_faces e hEOM, sem reprová-los |
| Axiomas e controles | PAGO: 27 nomes autorais e 12 próprios do revisor, somente propext/Classical.choice/Quot.sound ou subconjunto; 9 controles autorais reexecutados e 2 mutações próprias recusadas |
| Revisão adversarial | PAGO no escopo condicional: Carver, convocado pela principal sob o escopo autorizado; autor Poincare; P0=0/P1=0/P2=0 |
| Fonte primária do Artigo A | PAGO como leitura textual dos excertos10106–10249; EOM em10203–10218 e ξ=1/6 em10132–10140. Acesso inicialmente negado ficou preservado, seguido do recibo de leitura da principal |
| Natureza realiza EOM; ξ=1/6 derivado; gerador efetivo da torre | NÃO PAGO, e não reivindicado por B1′ |

A revisão recompilou 47 fontes locais TGL/TGLExt em raiz própria. Mathlib e pacotes auxiliares são caches de terceiros, não reconstruídos integralmente. O autor usou uma raiz distinta. Os tipos admitem o campo zero; os controles de identificabilidade exigem fonte não nula. ξ e β têm papéis separados, o que não proíbe coincidência numérica em um dado particular.

## Reprodução

Os comandos por módulo, ambiente, fonte, objeto e rc da execução independente estão em REVISAO_B1_PRIME_012/BUILD.json; os controles estão nos dois relatórios ligados abaixo. Reprodução incremental autoral nesta máquina:

```powershell
Set-Location -LiteralPath 'C:\\IALD\\Central de Patentes\\Chatgpt\\B1_PRIME_012'
& 'C:\\Python314\\python.exe' -X utf8 -B .\\build.py TGLExt.TheSameBetaReadsFourFaces TGLExt.ActionCouplingControls TGLExt.AuditSameBetaFourFaces
& 'C:\\Python314\\python.exe' -X utf8 -B .\\negative_controls.py
& 'C:\\Python314\\python.exe' -X utf8 -B .\\audit.py
```

Não repetir os preparadores/finalizadores de execução única para reproduzir prova. A gerência tem a via de recompilação independente pelos comandos registrados e decide a incorporação. Nenhum um.py, D1, Atlas ou kernel canônico foi escrito. Os fracassos de desenvolvimento e descoberta permanecem em ERROS_E_CORRECOES.md e attempts, distinguindo erro de infraestrutura de recusa semântica.

## Arquivos e custódia desta entrega

'''
for c in counts:
    p=Path(c['path']);text+=f"- [{p.name}](<{p.as_posix()}>) — {c['theorems']} declarações theorem, {c['definitions']} def; SHA256 `{c['sha256']}`.\n"
for p in files[len(sources):]:
    rec=pin(p);text+=f"- [{p.name}](<{p.as_posix()}>) — SHA256 `{rec['sha256']}`.\n"
mp=pin(manifest);text+=f"\nManifesto: [{manifest.name}](<{manifest.as_posix()}>) — SHA256 `{mp['sha256']}`.\n"
target=OUT/'ENTREGA_012_B1_PRIME_quarta_face.md';put(target,text.encode('utf8'))
print(json.dumps(pin(target),ensure_ascii=False))
