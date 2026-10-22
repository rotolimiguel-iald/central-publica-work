from pathlib import Path
from datetime import datetime
import json,hashlib,os,sys,difflib,ast
REV=Path(__file__).resolve().parent;ROOT=REV.parent
load=lambda p:json.loads(Path(p).read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
stamp=datetime.now().astimezone();tag=stamp.strftime('%Y%m%d_%H%M%S_%f')
mode=sys.argv[1];report=REV/'REVIEW_BIDUAL_RIGHT_SUPPORT_DEV.md'
def append(p,b):
    assert p.resolve().is_relative_to(REV)
    if p.exists():
        old=p.read_bytes();bak=p.with_name(p.name+'.bak_'+tag);bak.write_bytes(old);assert bak.read_bytes()==old
        b=old+b'\n\n'+b
    t=p.with_name(p.name+'.tmp_'+tag);t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p);assert p.read_bytes()==b
def save(p,d):append(p,(json.dumps(d,ensure_ascii=False,indent=2)+'\n').encode())
first=Path((REV/'bidual_partial_latest_run.txt').read_text().strip())
fm,fc=load(first/'manifest.json'),load(first/'compilation.json')
assert fc['complete'] and fc['all_exit_zero'] and fc['exact_2_targets'] and fc['all_axioms_allowed'] and fc['binary_equal_author'] and fc['dependencies_preserved']
if mode=='partial':
    assert not report.exists()
    d=fm['sources']['TGLV350/ScalarTomitaBidual.lean']
    text=f'''# Revisão DEV — bidual original e suporte direito

## Estrato parcial — {stamp.isoformat()}

[REAL — leitura integral e recompilação independente.] Escopo concluído neste estrato: somente `ScalarTomitaBidual.lean`, dois alvos. Nenhum P0–P2 matemático identificado. Não constitui aceite cumulativo dos nove alvos.

- `scalarClosedTomita_bidual_maximal` (linha 49): um pareamento contra TODO D(F) produz pertinência ao D(S) original e o valor S y=z.
- `scalarClosedTomita_bidual_graph_iff` (linha 63): equivalência exata entre esse pareamento e o grafo original, incluindo a direção fornecida pelo pareamento de F.

Os auxiliares privados `bidualPairingTransfer` e `bidualMaximalFromTransport` foram lidos e são cobertos transitivamente pelos axiomas dos alvos. `antiunitary_inner_conj` não exige involutividade; `antiunitary_pairing_flip` a exige e recebe `scalarTomitaPolarFactor_involutive P`. A prova transporta o teste por J, aplica maximalidade já estabelecida de F e retorna por J²=I. As hipóteses genéricas de domínio, valor e maximalidade são descarregadas na aplicação concreta. Não há novo S, F ou J nem hipótese de bidualidade usada para provar a própria conclusão.

| Reprodução própria | rc | segundos |
|---|---:|---:|
| ScalarTomitaBidual | {fc['records'][0]['returncode']} | {fc['records'][0]['seconds']} |
| Auditor separado `#check` com universos + `#print axioms` dos dois | {fc['records'][1]['returncode']} | {fc['records'][1]['seconds']} |

Os dois alvos retornaram exatamente `propext`, `Classical.choice`, `Quot.sound`; binário próprio idêntico ao final autoral. Fonte SHA256 `{d['sha256']}`; .olean `{d['author_binary_sha256']}`; log final `{Path(d['author_log']).name}`, SHA `{d['author_log_sha256']}`.

Evidência: `{first.relative_to(ROOT)}/manifest.json` e `compilation.json` (SHA `{hf(first/'compilation.json')}`). Foram congeladas {len(fm['dependencies'])} dependências de projeto provenientes exclusivamente de árvores próprias anteriores, com origem individual no manifesto; oito pacotes externos readonly e {len(fm['external_direct_pins'])} pins diretos herdados, sem rebuild dos pacotes. LEAN_PATH não contém build autoral. Herança principal: `phase_variational_final_independent_20260913_034807_811147` e `adjoint_polar_first_independent_20260913_025326_236836`.

A tentativa autoral `_040333_134788` é rc1 e contém `sorryAx`: rejeitada integralmente, preservada em `author_history`. A primeira preparação própria falhou ao procurar um registro novo de uma dependência herdada; nenhum Lean foi iniciado nessa tentativa. Registro próprio de falha e backup do script foram preservados; a execução aceita é a indicada acima.

[OPEN] Segundo módulo/auditor cumulativo e reconciliação documental ainda pendentes neste estrato. Não houve integração, execução de monólito/recorders, escrita em memórias ou alteração de pareceres custodiados. Inversa dos comutantes, cortes racionais, quadrados como núcleo de gráfico, KMS e traço não são conclusões destes dois alvos.
'''
elif mode=='final':
    run=Path((REV/'bidual_support_final_latest_run.txt').read_text().strip());m,c=load(run/'manifest.json'),load(run/'compilation.json')
    for k in ['complete','all_exit_zero','exact_9_targets','all_axioms_allowed','all_axioms_match_author','new_binary_equal_author','inherited_bidual_binary_preserved','source_snapshots_preserved','readonly_artifacts_preserved','dependencies_preserved','external_direct_pins_preserved']:assert c[k],k
    assert hf(run/'bidual_right_support_draft_status.json')==hf(ROOT/'bidual_right_support_draft_status.json')==m['draft_sha256']
    draft=load(ROOT/'bidual_right_support_draft_status.json')
    old=['real_bidual_right_support_solution_unique','original_S_bidual_right_support_constructed']
    new=['original_S_is_maximal_adjoint_of_F','selfadjoint_right_pairs_stable_under_commuting_multipliers']
    assert all(k not in draft for k in old) and all(draft[k] is True for k in new)
    assert draft['right_pair_vectors_in_multiplier_range_closure'] is True
    names=['bidual_right_support_draft_status.json','record_bidual_right_support_draft.py','record_bidual_right_support_progress.py','verify_bidual_right_support_custody.py','make_bidual_right_support_helpers.py']
    meta={}
    for name in names:
        p=ROOT/name;bk=ROOT/(name+'.bak_metadata_20260913_041932_059022');before=bk.read_bytes();after=p.read_bytes()
        if name.endswith('.py'):ast.parse(after.decode('utf-8-sig'))
        if name!='make_bidual_right_support_helpers.py':
            expect=before
            for a,b in zip(old,new):expect=expect.replace(a.encode(),b.encode())
            assert expect==after,name
        else:
            assert all(k in after.decode() for k in new)
        meta[name]={'current_sha256':hf(p),'backup_sha256':hf(bk),'backup_path':str(bk),'difference':list(difflib.unified_diff(before.decode('utf-8-sig').splitlines(),after.decode('utf-8-sig').splitlines(),lineterm=''))}
    save(run/'metadata_correction_inspection.json',{'timestamp':stamp.isoformat(),'status':'RENAMING_CONFIRMED','math_sources_unchanged':True,'scope':'literal correction only; no helper execution or complete integration-helper audit','files':meta})
    rows='\n'.join(f"| {Path(rel).stem} | `{d['sha256']}` | `{d['author_binary_sha256']}` |" for rel,d in m['sources'].items())
    targets='\n'.join('- `'+n+'`' for n in m['declarations'])
    text=f'''## Adendo cumulativo final — {stamp.isoformat()}

BIDUAL_RIGHT_SUPPORT_DEV_REVIEW

[REAL — DEV revisto e recompilado independentemente.] Escopo final: dois módulos, nove alvos exatos (2+7). **Nenhum P0 ou P1; nenhum P2 pendente.** O erro documental de nomes de flags está registrado abaixo como corrigido. Não há revisão integrada nem promoção de gate.

**Segundo módulo, leitura integral.** `ScalarRightFunctionalStability.lean:21` extrai comutação de T com TODA π(N) da pertinência ao comutante concreto. Linhas 40 e 62 constroem o par e o elemento de E para T a com hipóteses expressas a*=a, T*=T, T∈M′ e Ta=aT. T não é presumido em E. Ambos os vetores são T j(a); a ordem do produto/adjunto é justificada por `adjoint_comp`, auto-adjunticidade e comutação. Linhas 68 e 77 provam auto-adjunticidade e a inscrição exata pela unicidade já existente. Não há novo produto, norma, representação ou vetor por homonímia.

Linhas 87 e 100 demonstram suporte em `closure (Set.range R)` para QUALQUER par direito, sem hipótese de auto-adjunticidade ou injetividade de R. O filtro é `𝓝[>] 0` em ℝ, não vazio; a prova restringe o limite existente, usa h>0 para inserir a média no ideal finito e então em nν, e aplica fechamento à igualdade RΛ(e_h)=π(e_h)v. Não assume I=nν, continuidade pontual de L², continuidade limitada de S/F, nem cota uniforme de Λ(e_h).

**Reprodução própria.** O primeiro módulo e seu auditor2 são herdados do estrato acima, sem repetir compilação. O segundo módulo rc0 em {c['records'][0]['seconds']} s; auditor separado9 rc0 em {c['records'][1]['seconds']} s. Auditor imprime todos os tipos com universos e axiomas; conjunto exatamente igual aos nove alvos do manifesto e aos outputs finais autorais. Axiomas exclusivamente `propext`, `Classical.choice`, `Quot.sound`, incluindo transitivamente dois auxiliares privados do primeiro módulo e três do segundo. Ambos os .olean próprios são idênticos aos finais autorais.

| Fonte | SHA256 fonte DEV | SHA256 .olean próprio = autor |
|---|---|---|
{rows}

Evidências próprias finais: `{run.relative_to(ROOT)}/manifest.json`, `compilation.json` (SHA `{hf(run/'compilation.json')}`), `logs/BidualSupportAudit9.stdout.txt` (SHA `{c['records'][1]['stdout_sha256']}`). O manifesto identifica cada origem de dependência e pin anterior. A árvore final contém {len(m['dependencies'])} dependências próprias: as {len(fm['dependencies'])} do estrato inicial e {len(m['additional_own_dependencies_copied'])} adicionais do catálogo próprio `adjoint_polar_graph_final_independent_20260913_025725_898901`; {len(m['needed_project_dependencies_second'])} são alcançadas pelos imports do segundo módulo. Nenhuma dependência antiga foi recompilada; pacotes externos continuam readonly, oito caminhos e {len(m['external_direct_pins'])} pins diretos herdados. A biblioteca inteira não foi reauditoria binária nesta rodada.

**Histórico excluído.** Duas tentativas autorais rc1: Bidual `_040333_134788`, erro de conversão do produto interno conjugado; Stability `_040725_588950`, identificador de centralizador, elaboração/timeout e filtro, com erros derivados. Seus prints com `sorryAx` não contam. Há também preparação própria final recusada por catálogo incompleto (antes do Lean) e uma execução de 1,017 s recusada por busca de módulo numa raiz parcial. Os registros foram preservados. A correção reuniu somente binários próprios já pinados numa única raiz de projeto; nenhuma Lean fonte foi corrigida pelo revisor. O catálogo inicial também teve a falha anterior já descrita no estrato parcial.

**Metadados — P2 documental encerrado.** O manifesto inicial continha `real_bidual_right_support_solution_unique` e `original_S_bidual_right_support_constructed`, decorrentes de substituição de nomes do estágio anterior. Esses nomes não evidenciam seleção variacional nova. A correção foi anunciada e feita pelo autor; conferi por bytes os backups imediatos e a substituição literal dos dois campos no manifesto, draft recorder, progress recorder e verifier, além do ajuste de ordem no gerador. Nomes finais: `original_S_is_maximal_adjoint_of_F`, `selfadjoint_right_pairs_stable_under_commuting_multipliers` e `right_pair_vectors_in_multiplier_range_closure`. Diferenças/pins em `metadata_correction_inspection.json`; scripts apenas parseados/lidos no delta, nunca executados. Isto não equivale a revisão integral de futuros helpers de integração.

Manifesto corrente SHA `{m['draft_sha256']}`; relatório autoral integral SHA `{m['report_sha256']}`; mãe `phase_variational_custody.json` SHA `{m['parent_custody_sha256']}`. Fonte/binário/log/streams dos dois conferem o manifesto atual; relatório e provas permaneceram intactos na correção. A mãe e sua verificação foram lidas/pinadas, sem repetir auditoria das 34 memórias. Cópia integrada anterior e gate_extension mantiveram os pins; as seis flags da mãe seguem falsas. O DEV não está integrado.

**Alvos próprios auditados (2+7):**

{targets}

[OPEN] Não se concluem ainda limite racional no suporte, densidade de combinações de quadrados no gráfico, pertinência automática de pares ponderados a D(S), cota de multiplicador, inclusão inversa pelo J original, identificação de Δ^it/KMS, traço ou quitação de flags. A bidualidade é uma equivalência exata de pareamento/grafo no H_I original, sem redefinir o operador; a estabilidade é condicional às hipóteses explícitas de T. Não resta análise DEV necessária para estes nove alvos e documentos delimitados. Não foram executados monólito, integrador, testes autorais, recorders ou escrita de memórias.
'''
else:raise ValueError(mode)
append(report,text.encode('utf-8'))
print(json.dumps({'report':str(report),'sha256':hf(report),'bytes':report.stat().st_size,'mode':mode},ensure_ascii=False))
