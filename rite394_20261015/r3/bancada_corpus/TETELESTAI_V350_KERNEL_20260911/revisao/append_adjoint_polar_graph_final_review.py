from pathlib import Path
import datetime, hashlib, json, os

REV = Path(__file__).resolve().parent
ROOT = REV.parent
RUN = Path((REV / 'adjoint_polar_graph_final_latest_run.txt').read_text().strip())
FIRST = Path((REV / 'adjoint_polar_first_latest_run.txt').read_text().strip())
hf = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
load = lambda p: json.loads(Path(p).read_bytes())
m, c = load(RUN / 'manifest.json'), load(RUN / 'compilation.json')
fm, fc = load(FIRST / 'manifest.json'), load(FIRST / 'compilation.json')
assert c['complete'] and all(x is True for x in c.values() if isinstance(x, bool))
assert fc['complete'] and all(x is True for x in fc.values() if isinstance(x, bool))
d = load(ROOT / 'adjoint_polar_graph_draft_status.json')
assert c['records'][-1]['axioms'] == d['targets'] and len(d['targets']) == 17
assert all(hf(p) == h for p, h in m['artifacts_readonly'].items())
assert all(hf(p) == h for p, h in m['document_pins'].items())
assert hf(FIRST / 'manifest.json') == m['inherited_first_review']['manifest_sha256']
assert hf(FIRST / 'compilation.json') == m['inherited_first_review']['compilation_sha256']
rows = []
for name, x in d['modules'].items():
    p = ROOT / 'kernel/TGLV350' / (name + '.lean')
    source_info = (fm if name == 'ScalarTomitaAdjointPolar' else m)['sources']['TGLV350/' + name + '.lean']
    comp_info = (fc if name == 'ScalarTomitaAdjointPolar' else c)['records'][0]
    assert hf(p) == hf(source_info['snapshot']) == x['source_sha256']
    assert hf(source_info['author_binary']) == hf(comp_info['command'][2]) == x['binary_sha256']
    log = load(x['final_log'])
    assert hf(x['final_log']) == x['final_log_sha256'] and log['returncode'] == log['lean_returncode'] == 0
    assert hf(log['stdout']) == x['stdout_sha256'] and hf(log['stderr']) == x['stderr_sha256']
    assert not Path(comp_info['stderr']).read_bytes()
    assert 'warning:' not in Path(comp_info['stdout']).read_text(encoding='utf-8')
    rows.append({'module':name, **x, 'own_record':comp_info})
history = load(FIRST / 'author_history.json') + load(RUN / 'author_history.json')
failed = [x for x in history if x['returncode'] != 0]
assert len(failed) == 3
assert set(x['log'] for x in failed) == {p for x in d['modules'].values() for p in x['failed_attempts']}
date = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def link(label,p):
    return f'[{label}](<{Path(p).as_posix()}>)'

v = {'timestamp':date,'scope':'DEV_TWO_MODULES_17_TARGETS','complete':True,
     'first_module_recompiled_again':False,'records':rows,'own_final_auditor_record':c['records'][-1],
     'first_compilation_sha256':hf(FIRST/'compilation.json'),'final_compilation_sha256':hf(RUN/'compilation.json'),
     'draft_sha256':hf(ROOT/'adjoint_polar_graph_draft_status.json'),'report_sha256':hf(d['report_path']),
     'parent_custody_sha256':hf(d['parent_custody_path']),'all_17_types_and_axioms_read':True,
     'private_helpers_transitive':3,'excluded_author_Lean_rc1':failed,'P0':[],'P1':[],'P2':[],
     'author_recorder_execution_verified':False,'integrated_review':False,'memory_written':False}
def new_atomic(p, raw):
    assert p.resolve().is_relative_to(REV) and not p.exists()
    q=p.with_name(p.name+'.tmp_'+stamp)
    with q.open('xb') as f:f.write(raw)
    assert q.read_bytes()==raw
    os.replace(q,p)
    assert p.read_bytes()==raw
new_atomic(RUN/'verification.json',(json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode())
table='\n'.join(f'| {x["module"]} | {x["targets"]} | `{x["source_sha256"]}` | `{x["binary_sha256"]}` |' for x in rows)
text=f'''

---

{date} — **ADJOINT_POLAR_GRAPH_DEV_REVIEW**

[REAL — revisão DEV cumulativa concluída] **Sem P0, P1 ou P2 nos dois módulos/17 alvos.** O estrato10 anterior está preservado. Nesta continuação foram recompilados somente `ScalarRightConjugateGraph` e o auditor cumulativo17, usando o primeiro módulo próprio já verde. Manifesto e relatório finais foram lidos integralmente e seus pins conferidos nos arquivos.

O segundo módulo foi examinado integralmente:

- **Linhas13–40:** três auxiliares privados genéricos tratam reversão de imagem por involução, composição de imagens/ranges e transporte de valor entre gráficos. No último, existência de pertinência ao domínio e igualdade de valor são recebidas separadamente e descarregadas pela aplicação concreta; diferenças entre provas de pertinência não alteram o vetor. Cobertura axiomática transitiva, sem axiom/sorry/unsafe novo.
- **Linhas44–70:** J×J é um **homeomorfismo** do produto H_I×H_I, com inversa igual a si mesmo. Sua continuidade vem do J antiunitário original. O gráfico de F é enviado exatamente ao de S pela igualdade anterior e involutividade; não se presume continuidade de S ou F.
- **Linhas73–99:** a inscrição a↦Jj(a) é corretamente **semilinear para starRingEnd ℂ**. Está no domínio do S original, e S(Jj(a))=Jj(a*) usa o F original e a estrela da mesma álgebra de pares, sem troca por torção modular ou alegação de identificação de álgebras.
- **Linhas103–123:** `Homeomorph.image_closure` justifica a troca entre imagem e fecho. O graph-core de F vem do teorema já provado, e a conclusão é **closure range(a↦(Jj(a),Jj(a*)))=graph S**. A igualdade é de gráficos inteiros, não apenas uma inclusão ou densidade Hilbert. Todos os objetos permanecem no mesmo H_I.

O auditor17 confirma os tipos sem premissas residuais além de P e dos elementos/domínios explícitos. O primeiro módulo preserva F=BJ=JSJ com D(F)=J⁻¹D(B)=J⁻¹D(S); o segundo compõe essa ponte com o graph-core anterior. Não há argumento circular ou nova raiz/J no pacote.

| Fonte | Alvos | SHA256 fonte final | SHA256 binário próprio = autoral |
|---|---:|---|---|
{table}

Reprodução: primeiro módulo/auditor10 rc0 **{fc['records'][0]['seconds']} s / {fc['records'][1]['seconds']} s**, já registrados; segundo módulo/auditor17 rc0 **{c['records'][0]['seconds']} s / {c['records'][1]['seconds']} s**. Os dois binários coincidem byte a byte com os autorais. Os 17 prints próprios coincidem exatamente com o mapa do draft e dependem somente de `propext`, `Classical.choice`, `Quot.sound`. Não houve warning nos módulos próprios; os stderr estão vazios.

Árvore final com **{len(m['dependencies'])} dependências de projeto pinadas**, provenientes das árvores próprias da involução, do graph-core e do primeiro módulo desta etapa. Elas foram reutilizadas sem rebuild. O LEAN_PATH contém só o build próprio e oito caminhos de pacotes externos readonly; não contém build de projeto autoral. Pins de fontes/binários/companions e dez dependências externas diretas foram reconferidos pelo runner. A leitura dos binários do autor serviu apenas à comparação, nunca à resolução de imports.

Histórico excluído: **três rc1 autorais Lean** (uma do primeiro módulo, duas do segundo). Foram lidos e preservados os streams com timeout, erro de transporte de pertinência e prints com `sorryAx`/constantes inválidas; nenhum foi aceito. A falha inicial própria de catálogo, antes de Lean, permanece registrada no estrato anterior. [DECLARADO pelo autor] A primeira emissão do draft falhou por f-string antes de criar arquivos; essa execução não serve de evidência. Aqui foram consumidos apenas os arquivos finais existentes e os logs Lean finais pinados; o recorder de draft não foi executado pelo revisor.

Documentação: `RELATORIO_ADJUNTO_POLAR_GRAFOS_ORIGINAIS_DEV.md` distingue domínio inteiro, inscrição conjugado-linear, gráfico original e ausência de reconstrução do comutante. Suas afirmações matemáticas correspondem aos enunciados. O draft retém corretamente o estatuto de emissão com revisão/integração pendentes; não foi editado para produzir aprovação.

- Manifesto autoral final: `{v['draft_sha256']}`.
- Relatório autoral final: `{v['report_sha256']}`.
- Mãe `right_graph_core_custody.json`: `{v['parent_custody_sha256']}`.
- Compilação própria final: `{v['final_compilation_sha256']}`.
- Verificação própria: `{hf(RUN/'verification.json')}`.

{link('Verificação cumulativa e pins',RUN/'verification.json')}; {link('compilação própria final',RUN/'compilation.json')}; {link('manifesto próprio/dependências',RUN/'manifest.json')}; {link('17 tipos com universos e axiomas',RUN/'logs/AdjointPolarGraphFinalAudit.stdout.txt')}.

[OPEN] O transporte de gráficos não prova JRJ∈π(N), uma estimativa de multiplicação dos quadrados ou a inclusão inversa. Também não identifica Δ^it/KMS, traço, Three Locks ou consumo físico/por gate. Não se afirma que a imagem algébrica de j seja todo domínio, nem I=nν. Esta conclusão é **DEV dos dois módulos/17 alvos**, sem revisão de integração, novos testes autorais ou runtime. Nenhum monólito/helper/recorder foi executado pelo revisor; originais, fontes autorais, memórias e pareceres anteriores não foram alterados. **Escopo DEV delimitado encerrado.**
'''
p=REV/'REVIEW_ADJOINT_POLAR_GRAPH_DEV.md'
before=p.read_bytes()
assert hf(p)==load(FIRST/'partial_review_pin.json')['report_sha256']
assert b'ADJOINT_POLAR_GRAPH_DEV_REVIEW' not in before
bak=p.with_name(p.name+'.bak_'+stamp)
new_atomic(bak,before)
raw=before+text.encode()
tmp=p.with_name(p.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and p.read_bytes()==before
os.replace(tmp,p)
assert p.read_bytes()==raw and raw.startswith(bak.read_bytes())
pin={'timestamp':date,'report':str(p),'report_sha256':hf(p),'backup':str(bak),'backup_sha256':hf(bak),
     'prefix_bytes':len(before),'final_marker':'ADJOINT_POLAR_GRAPH_DEV_REVIEW','scope':'TWO_MODULES_17_TARGETS',
     'verification_sha256':hf(RUN/'verification.json'),'P0':[],'P1':[],'P2':[]}
new_atomic(RUN/'final_review_pin.json',(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(pin,ensure_ascii=False))
