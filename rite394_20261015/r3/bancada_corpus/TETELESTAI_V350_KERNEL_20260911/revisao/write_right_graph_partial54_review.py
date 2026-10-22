from pathlib import Path
import datetime,hashlib,json,os
REV=Path(__file__).resolve().parent;ROOT=REV.parent
load=lambda p:json.loads(Path(p).read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
fixed=Path((REV/'right_fixed_graph_latest_run.txt').read_text().strip())
pair=Path((REV/'right_projection_pair_latest_run.txt').read_text().strip())
blocks=Path((REV/'right_graph_blocks_latest_run.txt').read_text().strip())
runs=[fixed,pair];ms=[load(r/'manifest.json') for r in runs];cs=[load(r/'compilation.json') for r in runs]
for c,n in zip(cs,[48,54]):
    for k in ['complete','all_exit_zero',f'exact_{n}_targets','all_axioms_allowed','new_binary_equals_author','inherited_sources_binaries_preserved','author_source_binary_preserved','dependencies_preserved','external_direct_pins_preserved','read_only_artifacts_preserved','author_final_log_streams_preserved']:assert c[k],k
    assert len(c['records'])==2
for m in ms:
    for s in m['sources'].values():
        assert hf(s['path'])==s['sha256'] and hf(s['author_binary'])==s['author_binary_sha256']
        assert hf(s['author_log'])==s['author_log_sha256'] and hf(s['author_stdout'])==s['author_stdout_sha256']
    for s in m['inherited_partial_review']['sources'].values():assert hf(s['path'])==s['sha256'] and hf(s['author_binary'])==s['author_binary_sha256']
    for d in m['dependencies'].values():assert hf(d['frozen_source'])==d['source_sha256'] and hf(d['frozen_binary'])==d['sha256']
    assert all(hf(p)==h for p,h in m['artifacts_readonly'].items())
helper=load(pair/'helper_static_inspection.json')
assert all(hf(d['path'])==d['sha256'] for d in helper['helpers'].values())
report=REV/'REVIEW_RIGHT_GRAPH_CORE_DEV.md';priorpin=load(blocks/'partial_review_pin.json')
assert hf(report)==priorpin['report_sha256'];old=report.read_bytes()
def link(label,path,line=None):return f'[{label}](<{Path(path).as_posix()}{":"+str(line) if line else ""}>)'
def src(name,line):return link(name+'.lean:'+str(line),ROOT/'kernel/TGLV350'/(name+'.lean'),line)
rows=[]
for m in ms:
    for rel,s in m['sources'].items():rows.append(f'| {Path(rel).stem} | {len(s["declarations"])} | `{s["sha256"]}` | `{s["author_binary_sha256"]}` |')
table='\n'.join(rows)
logs='\n'.join('- '+link(Path(s['author_log']).name,s['author_log'])+f'; log `{s["author_log_sha256"]}`, stdout `{s["author_stdout_sha256"]}`.' for m in ms for s in m['sources'].values())
hpins='\n'.join('- '+link(n,d['path'])+f': `{d["sha256"]}`.' for n,d in helper['helpers'].items())
now=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
text=f'''

## Adendo parcial — genérico de densidade e par concreto; cinco módulos/54 alvos

{now}. **[REAL — leitura integral e recompilação independente] Nenhum P0, P1 ou P2 nas duas fontes acrescentadas: `FixedVectorGraphCore` (9) e `ScalarRightProjectionPair` (6).** Acumulado: cinco arquivos/54 alvos. O sexto wrapper e o manifesto final ainda não integram este aceite; não é emitido marcador final do pacote.

Conferência matemática:

- {src('FixedVectorGraphCore',13)}: a detecção positiva implica `closure E=K` para E⊆K **reais**, K fechado. A prova projeta x em `closure E`; o resíduo z permanece em K, é ortogonal a E e, se não nulo, contradiz a detecção. Não substitui densidade real em K por densidade complexa/Hilbert em H.
- {src('FixedVectorGraphCore',40)}–81: o submódulo real é a imagem por j dos elementos auto-adjuntos de A, fechado sob soma e escala real pela conjugação de escalares. `hF` fornece pertinência em D e o valor F(j a)=j(a*). O fechamento de Fix F deriva do fechamento do gráfico original; a instância real vem de `ClosedSubmodule`. `hdetect` continua hipótese explícita neste genérico, cuja aplicação concreta será conferida no wrapper.
- {src('FixedVectorGraphCore',83)}–151: `(h,k)↦(h+ik,h−ik)` é contínua no produto usual H×H. A estrela de a+ib tem o sinal negativo necessário. Na igualdade final, a inclusão direta usa hF e gráfico fechado; a inversa usa a decomposição `domain_fixed_decomposition`, `closure_prod_eq` e a pré-imagem de um fechado pela mistura contínua. **Não usa continuidade de F ou de j, domínio pleno, I=nν ou igualdade do domínio com a imagem algébrica.** As hipóteses de invariância do domínio, involutividade e densidade real são explícitas; o teorema é sobre o mesmo F recebido.
- {src('ScalarRightProjectionPair',16)}–47: o bloco B fornece `ScalarRightAdjointPair` com vetores Aη e η−Dη, no mesmo H_I e para **todo a∈nν**. O campo `right` usa BΛa=Aπ(a)η e comutação de A; o campo `adjoint` usa B*Λa=(1−D)π(a)η e comutação de D. Fη=η pertence ao adjunto máximo original. Nenhum vetor de adjunto ou graph-core é pedido como campo adicional.
- {src('ScalarRightProjectionPair',55)}–118: soma do par e seu adjunto constrói B+B* na álgebra direita já existente. Autoadjunticidade é demonstrada; o lema `scalarRightPairVector_of_pair` identifica o vetor escolhido com `(A+1−D)η` usando a unicidade previamente provada, não igualdade por nome. A energia estritamente positiva vem do genérico dos blocos e `scalarWeightGNSEmbedding_denseRange`, dando detecção por um **elemento auto-adjunto efetivo**. Os dois auxiliares privados genéricos entram transitivamente no auditor. Não é suposta limitação da multiplicação direita de η.

Reprodução e herança:

- {link('FixedVectorGraphCore: compilação própria e auditor48',fixed/'compilation.json')}: novo módulo rc0 ({cs[0]['records'][0]['seconds']} s) e auditor48 rc0 ({cs[0]['records'][1]['seconds']} s).
- {link('ScalarRightProjectionPair: compilação própria e auditor54',pair/'compilation.json')}: novo módulo rc0 ({cs[1]['records'][0]['seconds']} s) e auditor54 rc0 ({cs[1]['records'][1]['seconds']} s). {link('Tipos/universos e axiomas cumulativos',pair/'logs/RightProjectionPairAudit.stdout.txt')}. Os 54 alvos exatos usam somente `propext`, `Classical.choice`, `Quot.sound`; os dois novos binários próprios são idênticos aos autorais. Nenhuma recompilação dos três módulos anteriores.
- {link('Manifesto do genérico',fixed/'manifest.json')} e {link('manifesto do par',pair/'manifest.json')} fixam respectivamente {len(ms[0]['dependencies'])} e {len(ms[1]['dependencies'])} dependências de projeto herdadas de árvores próprias. A dependência `TGLExt.ClosedAntilinearStandardSubspace` foi recuperada da recompilação independente `closed_antilinear_dependency_independent_20260912_095836_800005`, fonte/binário e compilador relidos; não foi recompilada. Seu corpo pertinente foi relido integralmente. `LEAN_PATH` exclui build autoral, mantendo oito pacotes externos readonly.
- Uma preparação própria interrompeu **antes de Lean** por omissão dessa dependência no catálogo mínimo; registro preservado em {link('preparation_failure.json',REV/'right_fixed_graph_independent_20260913_014601_032324/preparation_failure.json')}. Corrigido apenas o catálogo próprio. Dois rc1 autorais do genérico e um do par foram capturados e excluídos; somente os rc0 finais de fonte/binário atuais contam. Não são achados pendentes das versões corrigidas.

| Fonte | Alvos novos | SHA256 fonte | SHA256 binário autoral = próprio |
|---|---:|---|---|
{table}

Logs autorais aceitos, separados dos próprios:

{logs}

[REAL — inspeção estática, sem execução] Os cinco helpers foram lidos e parseados, com cópias e pins em {link('helper_static_inspection.json',pair/'helper_static_inspection.json')}. Mãe declarada `scalar_vna_custody`; preparar exige `--review-read` e marcador DEV; registrar exige também parecer integrado. O preparador adiciona seis módulos/57 alvos e o grupo de fronteira, prevê 625→682 no batch; esses números são **escopo futuro dos scripts**, não resultado medido desta revisão. Recorder prevê 34 superfícies com backup de bytes, preservação do prefixo e troca temporária; verifier relê fontes/binários e pares backup/prefixo. As verificações de Audit corrente/histórico e flags permanecem no fluxo futuro. Nenhum helper foi executado aqui, nenhum registro de memória/custódia nova é afirmado. A minuta mantém inclusão inversa pelo J original, Δ^it/KMS e traço abertos. Suas afirmações de igualdade concreta do gráfico ficam pendentes da revisão do sexto módulo e do manifesto final.

Pins dos helpers lidos:

{hpins}

Fontes, binários, monólito/gate e pareceres selados pinados foram preservados; todas as escritas desta revisão ficaram em `revisao/`. O prefixo anterior deste parecer foi preservado com backup imediato de bytes. **Escopo parcial encerrado: cinco módulos/54 alvos, sem marcador final.** Falta conferir a composição concreta final das hipóteses no mesmo F; nenhuma aprovação de KMS, traço, inclusão inversa ou gate é antecipada.
'''
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f');backup=report.with_name(report.name+'.bak_'+stamp)
with backup.open('xb') as f:f.write(old)
assert backup.read_bytes()==old;raw=old+text.encode();tmp=report.with_name(report.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and report.read_bytes()==old;os.replace(tmp,report)
assert report.read_bytes()==raw and report.read_bytes().startswith(backup.read_bytes())
pin={'timestamp':now,'report':str(report),'report_sha256':hf(report),'backup':str(backup),'backup_sha256':hf(backup),'prefix_preserved':True,'scope':'PARTIAL_FIVE_MODULES_54_TARGETS','P0':[],'P1':[],'P2':[],'package_final_approval':False,'compilations':{str(r/'compilation.json'):hf(r/'compilation.json') for r in runs},'helper_inspection_sha256':hf(pair/'helper_static_inspection.json')}
q=pair/'partial_review_pin.json';assert not q.exists();b=(json.dumps(pin,ensure_ascii=False,indent=2)+'\n').encode();qt=q.with_name(q.name+'.tmp')
with qt.open('xb') as f:f.write(b)
assert qt.read_bytes()==b;os.replace(qt,q);print(json.dumps(pin,ensure_ascii=False))
