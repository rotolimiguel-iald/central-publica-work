from pathlib import Path
import datetime, hashlib, json, os
R=Path(__file__).resolve().parent
OUT=R.parent/'TUNEL/DO_CHATGPT/ENTREGA_012_B1_mesmo_beta_tres_faces.md'
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def put(p,b):
 assert p.is_relative_to(R) or p==OUT
 assert not p.exists(),p
 q=p.with_name(p.name+'.tmp');q.write_bytes(b)
 assert q.read_bytes()==b and len(b)>0;os.replace(q,p)
audit=json.loads((R/'AUDITORIA_B1.json').read_text(encoding='utf8'))
review=json.loads((R/'revisao/REVIEW_B1_FINAL.json').read_text(encoding='utf8'))
assert review['status']=='B1_DEV_REVIEW_ACCEPTED__INTEGRATION_NOT_REVIEWED'
assert audit['all_trio'] and audit['negative_controls_rejected']
assert all(review[k]==[] for k in ['P0','P1','P2'])
assert review['source']['sha256']==audit['source']['sha256']
independent=json.loads(Path(review['compilation']['path']).read_text(encoding='utf8'))
assert pin(Path(review['compilation']['path']))['sha256']==review['compilation']['sha256']
assert independent['all_accepted_builds_exit_zero'] and independent['axioms_allowed_only']
assert pin(Path(independent['run']['path']))['sha256']==independent['run']['sha256']
assert json.loads(Path(independent['run']['path']).read_text(encoding='utf8'))['returncode']==0
assert not independent['author_project_objects_copied']
stamp=datetime.datetime.now().astimezone().isoformat()
source=Path(audit['source']['path'])
assert pin(source)['sha256']==audit['source']['sha256']
files=[source,R/'kernel/TGLExt/AuditSameBeta.lean',R/'REAPROVEITAMENTO_B1.md',R/'REAPROVEITAMENTO_B1.json',R/'AUDITORIA_B1.json',R/'PROVENIENCIA_B1.json',R/'CUSTODIA_V353_FONTES.json',R/'DEPENDENCIAS_LAKE_V353.json',R/'revisao/REVIEW_B1_FINAL.md',R/'revisao/REVIEW_B1_FINAL.json',Path(review['compilation']['path'])]
files.extend([Path(independent['run']['path']),R/'revisao/B1_BUILD_ROOT_REMAP.json',R/'run_lake.py',R/'audit_b1.py',R/'deliver_b1.py'])
table='\n'.join(f"| `{p}` | `{pin(p)['sha256']}` |" for p in files)
ax='\n'.join(f"| `{name}` | {', '.join(vals) or 'nenhum'} |" for name,vals in audit['axioms'].items())
body=f'''[REAL — B1 pago no módulo compilado e revisto; incorporação ao um.py cabe à gerência. B2–B6 e A1(b) não quitados.]

# ENTREGA 012 / B1 — o mesmo β nas faces de ângulo, custo e fundo

{stamp}

`TGLExt.the_same_beta_reads_three_faces` reúne a reflexão da matriz-S, a forma do custo, as duas identidades de fundo e a taxa de vazamento sobre a MESMA projeção `c.beta`. A estrutura tem apenas β e as provas de 0<β<1. α é definida como β/exp(1/2); sua positividade, seu limite superior e as duas escritas do custo são demonstrados. Não há campo que assuma reflexão, fundo ou vazamento.

Foram compilados {audit['theorems']} teoremas novos, uma estrutura e uma definição. É uma ligação de fornecedores pagos, sem reconstrução deles. **A identidade do custo é uma normalização de forma autorizada por B1; não é dedução do valor de α nem de CODATA.** A reflexão mede β como probabilidade, com amplitude √β. O ângulo lê o acoplamento e não entra no motor cosmológico.

## Critérios da ORDEM 012

| Critério B1 | Resultado e evidência |
|---|---|
| Ficha antes do código | PAGO — MD/JSON anexados; revisão confrontou fontes, linhas e timestamps. |
| Um termo, β real em (0,1) | PAGO — `TGLExt.TGLCoupling`, sem outro escalar de entrada. |
| (i) Reflexão em thetaMiguel β igual a β | PAGO — `TGLExt.TGLCoupling.reflection_weight`, especialização de `the_pruning_threshold_is_the_reflection_amplitude` + `Real.sq_sqrt`. |
| (ii) Forma β=α·exp(1/2), 0<α<1, radical | PAGO — `alpha_pos`, `alpha_lt_one`, `beta_eq_alpha_exp`, `beta_eq_alpha_radical`; reusa `boundary_extracts_the_radical` e `the_minimal_volume_exceeds_one`. |
| (iii) closure_identity e hubble_form no mesmo β | PAGO — aplicações literais na síntese; não se reprovam identidades de anel. |
| (iv) Taxa de vazamento no mesmo β | PAGO — perda estrita com t,g>0 e unicidade sob igualdade dos semigrupos para todo tempo; reusa NoFullWitness. |
| Nenhum numeral atribuído a β/α | PAGO — ambos variáveis/leituras; 0 e 1 limitam o domínio, 1/2 é o expoente e 4/3 vem do fluido já formalizado. |
| Axiomas no trio | PAGO — os dez alvos auditados na cópia do autor e na raiz independente. |
| lake build isolado | PAGO — projeto sem objetos TGL/TGLExt herdados; `lake build` produz a cadeia de dependências e o auditor. Reprodução independente também sem objetos de projeto do autor. |
| Consumidor nomeado | PAGO — proposta `ext_same_beta_reads_three_faces_kernel_proved → TGLExt.the_same_beta_reads_three_faces`; âncoras e hipótese D1 na ficha. Instalação pela gerência ainda não realizada. |

## Alcance e controles

`reflection_rejects_bare_alpha` prova que omitir o custo altera a reflexão. Duas sondas deliberadamente adulteradas foram efetivamente recusadas por incompatibilidade de tipo: `BadReflection.lean` troca β por α na reflexão; `BadCost.lean` remove exp(1/2). Importação e infraestrutura funcionaram: as recusas são de prova, com logs preservados.

As cláusulas de fundo ainda não contêm H, derivadas ou Einstein; a equação métrica pertence a B2–B4. A última cláusula identifica taxas de semigrupos iguais; não seleciona um β numérico nem identifica β separado de um gap desconhecido. Não há nova dinâmica, teste D1, seleção natural, escolha entre rotas, fechamento global, demonstração de G ou mudança de gate.

## Build, procedência e revisão

Build autoral: `{audit['positive_build']}`. Revisão: `{review['compilation']['path']}`. P0/P1/P2 da revisão: 0/0/0 no escopo B1. A revisão verificou tipo, fonte, hipóteses, ficha e compilou fonte/auditores numa raiz própria. A gerência ainda fará sua auditoria de incorporação.

Mathlib e os outros oito pacotes são caches copiados, com revisões confrontadas ao manifesto; não foram reconstruídos a partir de Lean fonte nesta rodada. A toolchain é Lean4.31.0 instalada. Não há olean de projeto canônico reaproveitado: os fornecedores TGL/TGLExt do alvo foram reconstruídos por Lake. Avisos de linters dos fornecedores antigos permanecem nos logs e não foram corrigidos nesta entrega.

A leitura estática do dicionário embutido contou 941 chaves, sem duplicação; `lake-manifest.json` foi copiado separadamente (942 arquivos de configuração/fontes na raiz preparada antes dos dois novos). Essa contagem está discriminada em `PROVENIENCIA_B1.json`, sem transformar o número declarado na ordem em medição. Cópia do monólito e 941 fontes conferidas novamente sem alteração pela auditoria; o monólito não foi importado nem executado.

## Reprodução nesta máquina

Na raiz `{R}`:

```powershell
& 'C:\\Python314\\python.exe' -X utf8 -B '.\\run_lake.py' TGLExt.TheSameBetaReadsThreeFaces TGLExt.AuditSameBeta
```

O script chama a toolchain fixa e `lake build` no diretório kernel, retira LEAN_PATH externo e grava cada tentativa em pasta nova. Para ver os axiomas diretamente, no diretório kernel:

```powershell
& 'C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe' env lean TGLExt/AuditSameBeta.lean
```

As duas sondas em `probes/` devem devolver saída diferente de zero sob `lake env lean ../probes/BadReflection.lean` e `lake env lean ../probes/BadCost.lean`. Logs reais: os caminhos estão em `AUDITORIA_B1.json`. Não há teste empírico nesta reprodução.

## Axiomas, nomes completos

| Alvo | Lista medida |
|---|---|
{ax}

## Arquivos

| Arquivo | SHA256 lido |
|---|---|
{table}

O manifesto `{R / 'MANIFESTO_B1.json'}` e o recibo `{R / 'RECIBO_B1.json'}` indexam também a tentativa autoral B1, sondas e fontes necessárias. As tentativas de B2 ficam fora da custódia de B1. Nenhuma tentativa falha foi apagada; as sondas negativas não são provas admitidas no módulo. A revisão preserva a tentativa em caminho longo que falhou ao localizar um arquivo de cache no Windows e registra a reprodução em raiz curta; essa falha de infraestrutura não é uma recusa matemática.

## Próximos alvos preservados

B2: calcular FLRW na conexão/métrica da casa e instanciar seu teorema geral. B3: continuidade por setor com H_nx nomeada. B4: duas rotas, diferença e fator de entalpia, com todas as condições de denominador e conservação explícitas. B5: reescrita pelo ângulo. B6: tabela de importados/inputs/abertos. A1(b) e os sete módulos pendentes da ORDEM011 retomam depois de B6.

## Ficha de aproveitamento anexada, sem reescrita

'''+(R/'REAPROVEITAMENTO_B1.md').read_text(encoding='utf8')
put(OUT,body.encode('utf8'))
items=[]
for folder in ['attempts/20260914_145521_664130','audit','probes','searches']:
 for p in (R/folder).rglob('*'):
  if p.is_file():items.append(pin(p))
items.extend(pin(p) for p in files)
items.append(pin(OUT))
manifest=dict(timestamp=stamp,status='B1_DELIVERED__B2_B6_AND_A1B_REMAIN_OPEN',files=items,
    canonical_program_written=False,gate_changed=False,acceptance='module proof + independent review; management integration pending')
put(R/'MANIFESTO_B1.json',json.dumps(manifest,ensure_ascii=False,indent=2).encode('utf8'))
put(R/'RECIBO_B1.json',json.dumps(dict(delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B1.json')),ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(delivery=pin(OUT),manifest=pin(R/'MANIFESTO_B1.json')),ensure_ascii=False))
