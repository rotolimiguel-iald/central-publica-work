"""Write this new review only; preserve all prior reports and author files."""
from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_root_latest_run.txt').read_text().strip())
D=max(p for p in RUN.glob('final_integrated_*') if (p/'verification.json').exists())
load=lambda p:json.loads(Path(p).read_bytes());hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
V=load(D/'verification.json');SV=load(V['static_verification_path']);C=load(RUN/'compilation.json');M=load(RUN/'manifest.json')
S=Path(V['static_verification_path']).parent
def link(label,path,line=None):return '['+label+'](<' +Path(path).as_posix()+((':'+str(line)) if line else '')+'>)'
def artifact_table(names):return '\n'.join('| '+link(n,ROOT/n)+' | `'+V['artifacts'][n]+'` |' for n in names)
for n,h in V['artifacts'].items():assert hf(ROOT/n)==h,n
for n,h in SV['artifacts'].items():assert hf(ROOT/n)==h,n
assert hf(ROOT/'um.py')==V['working_sha256']
devreview=REV/'REVIEW_SCALAR_TOMITA_ROOT.md';assert hf(devreview)==V['own_DEV_closure']['review_sha256']
out=REV/'REVIEW_SCALAR_TOMITA_ROOT_INTEGRATED.md';assert not out.exists()
module_rows=[]
for n,t in V['transposition'].items():
    row=next(r for r in V['new_records'] if r['file']=='TGLExt/V350'+n+'.lean')
    module_rows.append('| '+n+' | `'+t['dev_sha256']+'` | `'+row['source_sha256']+'` | `'+row['binary_sha256']+'` |')
log_rows=['| '+link(r['file'],ROOT/'kernel'/r['file'])+' | '+link(r['log_name'],D/'logs'/r['log_name'])+' | 0 / sim |' for r in V['new_records']]
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''# Revisão da integração do resolvente e da raiz positiva de Tomita

INTEGRATED_TOMITA_ROOT_REVIEW

{now}. Escopo: cinco módulos/30 alvos, transposição DEV→TGLExt, duas raízes, evidências incrementais, controle novo, recorder/verifier e reexame documental. **Exame concluído com um P2 aberto no verifier de custódia; nenhum P0/P1 e nenhum defeito encontrado na transposição matemática.** Esta conclusão não é uma declaração de custódia sem ressalvas.

**P2 — o verifier não relê os binários compilados.** Em {link('verify_tomita_root_custody.py:19',ROOT/'verify_tomita_root_custody.py',19)}–31, os loops conferem hashes dos artefatos JSON, pareceres, superfícies e fontes DEV/integradas. Nenhum `.olean` é aberto ou comparado a `output_sha256`. Assim, depois do registro inicial, alterar um binário mantendo fontes/JSON iguais não altera nenhuma observação desse verifier: ele ainda pode emitir `custody_ok=True`. Isto decorre do fluxo lido; não adulterei binários para testar a situação. O recorder faz a conferência inicial nas linhas 71–74, mas ela não cobre uma alteração posterior. Restaurar no verifier a leitura dos registros e o confronto atual fonte/binário/rc0, como nas linhas 40–46 do verifier da mãe square. **Os 130 binários atuais conferiram independentemente nesta revisão**; o achado é a lacuna da verificação posterior, não uma falha atual das provas. SHA da versão com o achado: `{V['artifacts']['verify_tomita_root_custody.py']}`.

A correção autoral da cadeia de mães está correta em {link('record_tomita_root_progress.py:64',ROOT/'record_tomita_root_progress.py',64)}–65: `draft.integrated_working_sha256 == square.working_sha256 == parent.working_sha256`, e `parent.parent_sha256 == sha(square)`. O campo inexistente `draft.parent_custody_sha256` não é mais consultado. Não resta achado nessa correção.

| Evidência | Alcance efetivamente conferido |
|---|---|
| Recompilação própria anterior | Cinco DEV e auditor próprio: {len(C['records'])} rc0, 30 tipos/axiomas; somente `propext`, `Classical.choice`, `Quot.sound`. Herança de dependências da árvore revisada; nenhum build autoral de projeto no `LEAN_PATH` próprio. {link('compilation.json',RUN/'compilation.json')}; {link('parecer DEV preservado',devreview)}. |
| Esta rodada independente | Comparação literal de fontes/imports/embutidos, AST Python, leitura e hash dos 130 pares fonte/binário, logs JSON/stdout/stderr, extração própria dos axiomas dos streams e leitura dos scripts/documentos. **Zero novas execuções Lean ou de scripts autorais.** |
| Compilação do autor | 130 registros rc0: 123 conservam os mesmos hashes de fonte/binário da mãe square; sete registros novos correspondem aos cinco módulos e duas raízes. Não são 130 recompilações novas. |
| Controles do autor | 78/78 em `gate_tests.json`; conferi o relatório e o único controle adicional por AST. Não reexecutei os testes. |
| Audit do autor, reextraído aqui | 6.539 nomes distintos, todos dentro do trio; as 30 entradas novas coincidem com o auditor próprio DEV e os 6.509 nomes anteriores foram preservados. |

Snapshot medido: cópia `{V['working_sha256']}`, **832 embutidos**. Original relido por hash `{V['original_sha256']}`; mãe matemática `{V['parent_working_sha256']}`. Não executei/importei original ou cópia. A leitura inicial do original foi negada pelo sandbox; a leitura autorizada subsequente conferiu o pin, com saídas exclusivamente em `revisao/`.

Os cinco DEV coincidem com o congelamento revisado. As cópias integradas diferem **somente** pela troca literal, em linhas de importação, de `TGLV350.` para `TGLExt.V350`; nomes de namespace, termos e hipóteses permanecem iguais. Os embutidos reproduzem os bytes dessas fontes. Em relação à mãe, foram acrescentadas exatamente essas cinco chaves; somente as duas raízes mudaram entre as chaves anteriores. Cada raiz importa cada módulo uma vez e o Audit acrescenta exatamente os 30 alvos.

| Módulo | SHA256 DEV | SHA256 integrado | SHA256 `.olean` integrado |
|---|---|---|---|
{chr(10).join(module_rows)}

| Fonte compilada pelo autor | Registro final relido e preservado na revisão | rc / fonte inalterada |
|---|---|---|
{chr(10).join(log_rows)}

Todos os JSON desses registros coincidem com as entradas de `integrated_compile.json`; os sete streams não contêm erros nem warnings. Fonte/binário/stdout/stderr/JSON de todos os 130 registros estão pinados em {link('verification.json',D/'verification.json')}. O stdout final do Audit tem SHA `{V['final_Audit_stdout_sha256']}`. Os campos globais `audit_stdout_sha256` e `audit_capture_sha256_full` do evidence continuam com o hash histórico `{V['inherited_Audit_summary_hash_fields']['audit_stdout_sha256']['stored']}`, igual ao da mãe; **não os utilizei como pin do Audit atual**. Essa limitação herdada fica explícita; a contagem atual vem do stream específico acima, cujo mapa coincide integralmente com `axiom_report`.

O diff de `integrate_v350.py` acrescenta os cinco nomes ao batch cumulativo: **27 módulos/182 alvos distintos = 99 + 53 + 30**. O diff de `compile_integrated.py` insere os cinco antes de `TGLExt.lean` e `TGL/Audit.lean`; o mecanismo anterior de reutilização por fonte/binário e frescor de dependências permanece. A comparação AST do teste, removida apenas a nova entrada `bounded_Tomita_resolvent_and_exact_positive_root`, reproduz a versão anterior. O controle adicional {link('no teste',ROOT/'test_gate_extension.py',409)} exige seis nomes do incremento e preserva as mesmas condições de fronteira; não constitui novo gate ou prova de uma obrigação física.

O AST do corpo Python de `um.py`, excluído apenas `_EMBEDDED_KERNEL_FILES`, coincide com a cópia da mãe localizada pelo hash. `gate_extension.py` é byte a byte igual à versão custodiada. As seis flags maiores lidas em evidence são falsas; `legacy_gate_changed`, `full_plan_complete` e `full_monolithic_runtime_run` também são falsos. O nome legado do gate é apenas o valor histórico preservado, sem nova aprovação.

**Reexame documental e custódia proposta.** Li integralmente `RELATORIO_REAPROVEITAMENTO.md` e `source_evidence.json`, e conferi a estrutura, hashes e 34 pares efetivos de `custody.json`. Mãe documental SHA `{SV['documentary_parent_sha256']}`; mãe matemática square SHA `{SV['mathematical_parent_sha256']}`. As 34 superfícies atuais reproduzem seus pins, e cada backup na mesma pasta é o prefixo exato em bytes, com crescimento posterior. A contagem planejada pelo novo recorder é 34, herdada dessa mãe documental.

O inventário permite recontar 73.711 caminhos, 339 fontes selecionadas, 159 hashes distintos, 261 correspondências normalizadas em 99 basenames. Conferi os 339 pins e os 18 pins de leituras específicas. As seis entradas Audit citadas coincidem com o evidence anterior pinado. **Não repeti a normalização do acervo nem recertifiquei a matemática dos arquivos selecionados**: presença/nome/importação, leitura e recompilação são estatutos distintos. O relatório delimita inventário/consulta, não novos teoremas ou promoção de gate; suas referências físicas e seu roteiro de reaproveitamento não substituem as hipóteses necessárias.

Li inteiros o recorder atual (189 linhas) e o verifier (46 linhas), por inspeção estática. O recorder verifica a cadeia acima, pins de fontes/binários e 30 axiomas, e propõe backup imediato em bytes, temporário conferido, substituição e preservação de prefixo nas 34 superfícies. Essa rotina está descrita corretamente; **não foi executada por mim e não certifico aqui sua execução futura**. Os novos relatório integrado, custody e resultado de verifier ainda estavam ausentes na captura. O P2 acima limita a verificação posterior dos binários.

A minuta interpolada mantém os mesmos objetos: `A=S†S`, resolvente limitado `R=(I+A)⁻¹`, `0≤R≤I`, injetividade, raiz positiva auto-adjunta parcial `B` com `B²=A` e domínio sucessivo exato, energia apenas em `D(A)`. Núcleo trivial não é gap. A nota acrescentada nas linhas 119–121 e 150–154 separa os dois módulos/10 alvos posteriores como DEV sem revisão/integração e sem `D(B)=D(S)`. Seus pins documentais constam abaixo; conferi apenas a segregação, inclusive ausência desses módulos/alvos dos embutidos/Audit, **sem ler suas fontes/provas ou validar seus logs**.

| Artefato final lido | SHA256 |
|---|---|
{artifact_table(['integration.json','integrated_compile.json','gate_tests.json','kernel_incremental_evidence.json','integrate_v350.py','compile_integrated.py','test_gate_extension.py','record_tomita_root_progress.py','verify_tomita_root_custody.py','graph_core_draft_status.json','RELATORIO_DOMINIO_GRAFICO_DEV.md'])}

Os pins do reexame, diffs dos helpers/raízes, verificação dos 34 pares e transposição estão em {link('verification_static.json',S/'verification_static.json')}; as evidências finais estão em {link('verification.json',D/'verification.json')}, {link('axioms.json',D/'axioms.json')} e {link('module_axioms.json',D/'module_axioms.json')}. Os scripts próprios de captura estão em {link('capture_tomita_root_static.py',REV/'capture_tomita_root_static.py')} e {link('capture_tomita_root_final.py',REV/'capture_tomita_root_final.py')}. As tentativas internas de captura interrompidas foram preservadas; a divergência inicial da comparação de listas de axiomas era apenas a ordem da lista, corrigida no script próprio pela normalização, sem alteração autoral.

**Limites e encerramento.** A transposição e os resultados integrados delimitados estão conferidos. A análise solicitada está encerrada, com P2 de custódia ainda aberto; sua correção exige somente reexame documental do verifier. O exame matemático e a recompilação DEV anteriores são herdados, assim como os pacotes/base não recompilados; esta leitura de 130 registros não equivale a rebuild global. `D(B)=D(S)`, energia nesse domínio inteiro, fator polar/J, KMS, traço, Three Locks, condições físicas e consumo de certificado/runtime não são conclusões deste pacote. Nenhum parecer anterior, original, fonte, memória, integração ou custódia foi alterado. Este parecer novo não promove gate ou QG.
'''
raw=text.encode('utf-8');temp=out.with_name(out.name+'.tmp_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with temp.open('xb') as f:f.write(raw)
assert temp.read_bytes()==raw and len(raw)>0;temp.replace(out);assert out.read_bytes()==raw
closure={'timestamp':now,'review_path':str(out),'review_sha256':hf(out),'bytes':len(raw),'lines':len(text.splitlines()),
 'verification_path':str(D/'verification.json'),'verification_sha256':hf(D/'verification.json'),
 'DEV_review_preserved_sha256':hf(devreview),'findings':V['findings'],'integration_inspection_complete':True,'custody_P2_open':True}
p=D/'review_closure.json';b=json.dumps(closure,ensure_ascii=False,indent=2).encode();q=p.with_suffix('.tmp')
assert not p.exists()
with q.open('xb') as f:f.write(b)
assert q.read_bytes()==b;q.replace(p)
print(json.dumps(closure,ensure_ascii=False,indent=2))
