"""Write the completed five-module DEV review without changing any earlier review."""
from pathlib import Path
import datetime,hashlib,json
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_root_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
M=load(RUN/'manifest.json');C=load(RUN/'compilation.json');V=load(RUN/'verification_dev.json')
assert all(v for v in C.values() if isinstance(v,bool))
assert V['all_5_own_binaries_byte_equal_author'] and V['all_30_types_exact'] and V['all_axioms_trio']
for p,h in M['previous_reviews'].items():assert sha(Path(p).read_bytes())==h
for s in M['sources'].values():assert sha(Path(s['path']).read_bytes())==s['sha256']
assert sha((ROOT/'tomita_root_draft_status.json').read_bytes())==M['draft_status_sha256']
assert sha((ROOT/'RELATORIO_RAIZ_TOMITA_DEV.md').read_bytes())==M['report_sha256']
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
def link(label,p,line=None):return f'[{label}](<{Path(p).as_posix()}{":"+str(line) if line else ""}>)'
def src(name,line):return link(name+'.lean',ROOT/'kernel/TGLV350'/(name+'.lean'),line)
rows='\n'.join(f"| {Path(rel).stem} | {len(s['declarations'])} | `{s['sha256']}` | `{s['author_binary_sha256']}` |" for rel,s in M['sources'].items())
process='\n'.join(f"| {r['module']} | {r['returncode']} | {r['seconds']} |" for r in C['records'])
logs='\n'.join(f"| {Path(s['author_log']).name} | `{s['author_log_sha256']}` |" for s in M['sources'].values())
aud=C['records'][-1]
text=f'''# Revisão independente DEV — resolvente e raiz positiva de S†S

{date}. **[REAL — cinco módulos/30 alvos revisados e recompilados; nenhum achado P0, P1 ou P2.]** Escopo fechado: `PartialPositiveResolvent` (12), `ScalarTomitaResolvent` (9), `ScalarTomitaPositiveRoot` (6), `PartialSquareEnergy` (1) e `ScalarTomitaRootEnergy` (2). Foram lidos integralmente as cinco fontes, o manifesto e o relatório DEV. Nenhuma fonte posterior, integração nova, recorder, memória ou parecer custodiado foi alterado ou incluído.

**Conclusão:** para o mesmo A=`scalarTomitaSquare P`=S†S no mesmo H_I, constrói-se R=(I+A)⁻¹ limitado, injetivo, auto-adjunto e 0≤R≤I. O operador parcial B construído pelos grafos das raízes CFC limitadas é positivo, auto-adjunto, fechado, densamente definido e satisfaz **B²=A como mapas parciais, incluindo o domínio sucessivo inteiro**. A igualdade **‖Bx‖²=‖Sx‖² é provada em D(A)**. B tem núcleo trivial. **D(B)=D(S), extensão dessa energia, identificação polar/KMS e traço não são conclusões deste pacote.**

## Hipóteses, domínios e composição conferidos

{src('PartialPositiveResolvent',16)}: `hp` é a hipótese explícita `∀x∈D(T), 0≤Re⟨x,Tx⟩`; `hr` é a sobrejetividade de x↦x+Tx **de D(T) para todo H**. A estimativa coerciva resulta de ‖x‖²≤Re⟨x,x+Tx⟩≤‖x‖‖x+Tx‖, sem dividir por ‖x‖ e sem perder x=0. Aplicada a x−y, dá injetividade de `partialOneAdd` (linha 29). `LinearEquiv.ofBijective` (linha 38) fornece uma equivalência **linear**, não uma equivalência topológica postulada, entre D(T) e H. A função inversa toma valores no subtipo D(T); a inclusão em H recebe sua prova explícita de norma ≤1 em `mkContinuous` (linha 43). Não se usa teorema da aplicação aberta sobre domínio supostamente completo, nem se pressupõe D(T)=H, T limitado ou inversa limitada de T. A inversa limitada construída é a de **I+T**.

Os lemas `equation` e `inverse` (linhas 54–62) verificam os dois sentidos com a pertinência ao domínio: Rz é representado por x∈D(T), x+Tx=z, e R(x+Tx)=x. A injetividade de R (linha 70) usa igualdade dos representantes no subtipo e as equações; não afirma que R seja sobrejetivo como operador H→H. A norma provada é ‖Rz‖≤‖z‖ para todo z. Os tipos impressos confirmam que `hs` **não** aparece na construção, na coerção, na injetividade, na estimativa ou na igualdade de grafos.

{src('PartialPositiveResolvent',78)}: `hs : T.IsFormalAdjoint T` entra exatamente nos três resultados de simetria/ordem. Substituindo z=x+Tx e w=y+Ty, `hs x y` dá ⟨Rz,w⟩=⟨z,Rw⟩ com a convenção complexa correta. `nonneg_iff_isPositive` combina essa simetria com Re⟨Rz,z⟩=‖x‖²+Re⟨x,Tx⟩≥0. Para R≤I (linha 100), prova-se que I−R é auto-adjunto e que Re⟨(I−R)z,z⟩≥0 por Cauchy–Schwarz e a contração. Portanto a ordem é a ordem positiva dos operadores complexos; não é uma comparação apenas nominal de partes reais sem simetria.

{src('PartialPositiveResolvent',122)}: a igualdade `resolventGraphOperator R _ = T` é obtida pelas **duas inclusões dos grafos inteiros** na ordem de `LinearPMap`. Se (x,y) satisfaz (I−R)x=Ry, resolve-se u+Tu=x+y; então u=R(x+y)=x e Tu=y, produzindo um elemento real de D(T). No sentido inverso, um par (x,y) do gráfico de T satisfaz R(x+y)=x pela lei inversa e, logo, (I−R)x=Ry. A conclusão inclui igualdade de domínio e valores; não usa uma extensão escolhida nem apenas igualdade num núcleo algébrico. Também não exige `hs`.

{src('ScalarTomitaResolvent',14)} aplica o genérico ao **mesmo `scalarTomitaSquare P`**, usando `scalarTomitaSquare_positive P` e `scalarTomitaSquare_resolvent_surjective P` já revisados. A simetria necessária à ordem vem de `scalarTomitaSquare_symmetric P` (linhas 35–39). Não se supõe que A possua resolvente ou seja auto-adjunto para definir artificialmente R: a sobrejetividade anterior foi provada pelo gráfico real de S. Os nove tipos concretos têm somente P e os vetores explicitados como parâmetros; não acrescentam a P uma hipótese residual de domínio total, gap, simetria ou inversibilidade. `scalarTomitaResolvent_graph` (linha 45) identifica exatamente o grafo reconstruído com A.

{src('ScalarTomitaPositiveRoot',15)} especializa a construção anterior `resolventSquareRoot` em R sobre **H_I inteiro**, sem trocar para outro suporte, representação ou projeção finita. Relidos os fontes congelados das dependências `ResolventSquareRoot`, `ResolventGraph` e `PartialOperatorSquare`: o grafo de B é parametrizado por **(√R v, √(I−R) v)**, e D(B)=Ran√R. A injetividade de √R decorre de (√R)²=R e da injetividade de R; a auto-adjunticidade de √R e essa injetividade dão domínio denso. As duas raízes CFC são operadores **limitados**; B é um `LinearPMap`, não um CLM indevidamente definido em todo H_I.

As hipóteses 0≤R e R≤I garantem que os quadrados CFC são R e I−R; a comutação e a soma dos quadrados igual a I fornecem fechamento, simetria e auto-adjunticidade do grafo de B. A positividade usa o produto das duas raízes positivas que comutam. Na linha 35, a igualdade anterior `partialOperatorSquare (resolventSquareRoot R _ _) = resolventGraphOperator R _` é composta literalmente com `scalarTomitaResolvent_graph P`. O domínio de `partialOperatorSquare` exige x∈D(B) **e Bx∈D(B)**; seu lema de grafo exige duas aplicações sucessivas reais. Não se assume invariância geral de D(B) por B, nem se aplica CFC diretamente ao operador parcial A.

{src('PartialSquareEnergy',11)}: o auxiliar só exige B formalmente adjunto a si e **B²=A como mapas parciais**. Para x∈D(A), a igualdade transporta o par (x,Ax) ao gráfico de B² e fornece (x,z) e (z,Ax) no gráfico de B. A simetria dá ⟨z,z⟩=⟨x,Ax⟩, logo ‖z‖²=Re⟨x,Ax⟩. O resultado devolve **u∈D(B) com ↑u=↑x**; a igualdade ambiente resolve a coerção dos subtipos sem presumir que seus domínios sejam iguais. Não exige auto-adjunticidade, positividade adicional ou domínio pleno de B para esse passo algébrico.

{src('ScalarTomitaRootEnergy',14)} compõe esse auxiliar com a simetria já provada da raiz, B²=A e `scalarTomitaSquare_quadratic P`. A conclusão é existencial no subtipo D(B), para cada x∈D(A), com o mesmo vetor e energia igual à de S aplicada à inclusão efetiva de x em D(S). Isso prova D(A)⊆D(B) e a energia nesse domínio; **não prova D(B)=D(S)**. Na linha 28, Bx=0 coloca esse x no domínio sucessivo porque 0∈D(B) e B0=0; o par (x,0) passa ao gráfico de A. O núcleo trivial de A então dá x=0. Não se pressupõe que todo x∈D(B) já pertença a D(A), e não se deduz gap ou inversa limitada de B.

Os tipos genéricos impressos usam `H : Type` com estruturas de Hilbert complexo e `CompleteSpace H`; não reivindico aqui generalização automática a outros universos. Não há instâncias locais novas, axiomas declarados, `sorry`, `admit`, `unsafe` ou alteração de redutibilidade/transparência nas cinco fontes. As opções são `autoImplicit false`, `maxHeartbeats 1000000` e, em quatro arquivos, desativação do linter de variáveis de seção não usadas. O auxiliar `partialOneAdd` (linha 26) foi lido integralmente, embora não esteja entre os 30 alvos impressos; sua definição é coberta transitivamente pelos axiomas dos alvos que a usam. Não foi contabilizado como alvo 31.

## Evidência independente e pins lidos

| Fonte DEV | Alvos | SHA256 fonte | SHA256 .olean próprio = autor |
|---|---:|---|---|
{rows}

| Processo próprio | rc | Segundos |
|---|---:|---:|
{process}

**Seis processos próprios rc0: cinco fontes e um auditor/30**, sem rebuild dos pacotes ou dependências anteriores. Os cinco binários foram comparados também por bytes com os finais autorais, e são idênticos. O auditor faz 30 `#check` com universos explícitos e 30 `#print axioms`; todos os tipos foram lidos e todos os alvos usam somente **propext, Classical.choice, Quot.sound**. O conjunto é exatamente o dos 30 alvos do manifesto e das fontes. Não foi aceito resultado de tentativa fracassada nem ausência de axiomas inferida de timeout.

Árvore própria: {link('manifest.json',RUN/'manifest.json')}; resultados {link('compilation.json',RUN/'compilation.json')} e {link('verification_dev.json',RUN/'verification_dev.json')}; {link('30 tipos/axiomas completos',aud['stdout'])}. Auditor: fonte `{aud['source_sha256']}`, binário `{aud['output_sha256']}`, stdout `{aud['stdout_sha256']}`. Compilador `{M['compiler_sha256']}`, {M['lean_version']}.

Foram congeladas **{V['dependencies_count']} dependências de projeto próprias** a partir da árvore anteriormente revisada, com fontes, binários, caminhos de origem e hashes registrados. O LEAN_PATH contém apenas o build próprio consolidado e os oito pacotes externos somente leitura; **nenhum build autoral de projeto**. Os pacotes e os artefatos herdados não foram recompilados, preservando os limites de proveniência e a errata histórica exclusivamente de comentário de `DualSemifiniteIdeal`. O grafo de {V['project_import_graph_modules']} módulos de projeto é acíclico, e nenhuma dependência antiga importa os cinco novos: não há circularidade introduzida na construção de R, na raiz ou na energia.

| Log autoral final aceito | SHA256 JSON |
|---|---|
{logs}

{link('author_history.json',RUN/'author_history.json')} preserva **oito tentativas: cinco rc0 finais e três rc1 históricos**, com JSONs e streams pinados. Li os dois fracassos de `PartialPositiveResolvent` (coerções `RCLike.re`/`Complex.re`, reescritas, simetria e extensionalidade de grafos) e o timeout de `ScalarTomitaRootEnergy`. Este último chegou a imprimir que o alvo de energia “does not depend on any axioms” **depois do erro de elaboração**: esse texto não certifica o teorema e foi expressamente excluído da evidência. A versão final, fatorada pelo auxiliar genérico, foi recompilada aqui e apresenta o trio esperado. Não há falha histórica pendente identificada nas fontes finais.

## Documentação, preservação e limites

O manifesto `tomita_root_draft_status.json`, SHA **`{V['draft_status_sha256']}`**, e o relatório integral `RELATORIO_RAIZ_TOMITA_DEV.md`, SHA **`{V['report_sha256']}`**, coincidem com seus pins e com o escopo verificado. A redação distingue inversa de I+A, igualdade de mapas parciais, energia apenas em D(A), ausência de identificação polar e núcleo trivial sem gap. **Nenhum P2 documental encontrado.** As indicações de revisão/integração pendentes são o estatuto do snapshot autoral anterior a este parecer, não uma alegação de integração já feita.

Custódia antecessora lida: `tomita_square_custody.json`, SHA `{V['custody_sha256']}`; verificação autoral, SHA `{V['custody_verification_sha256']}`, registra rc0/32 pares exatos. Conferi pins, coerência e os pareceres nela vinculados; não reexecutei seu verifier nem reauditei integralmente os 32 backups. **`REVIEW_SCALAR_TOMITA_ADJOINT.md` e todos os pareceres anteriores permanecem intactos.** Original relido `{V['original_sha256']}`; cópia integrada antecedente relida `{V['working_sha256']}`. Os cinco DEV não foram adicionados às contagens integradas por esta revisão; nenhuma integração nova foi examinada.

Todas as saídas próprias estão em `revisao/`. Não alterei fontes autorais, raízes, monólito, memórias, logs ou custódias; não executei/importei monólito, integrador, recorder, verifier ou testes autorais. Trabalho posterior sobre domínio/núcleo de gráfico foi excluído.

**[OPEN — não concluído aqui]** D(B)=D(S), igualdade da energia em todo esse domínio, identificação de B como fator polar de S, construção/identificação de J e dos dados modulares do peso, KMS, traço e escala dual, gap, runtime e fechamento global. Nenhuma flag/gate é promovida. **Nenhuma análise DEV necessária resta dentro dos cinco módulos/30 alvos; revisão delimitada encerrada.**
'''
P=REV/'REVIEW_SCALAR_TOMITA_ROOT.md';assert not P.exists(),'New review already exists; preserve and inspect before appending.'
raw=text.encode('utf-8');tmp=P.with_name(P.name+'.tmp_'+stamp)
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and len(raw)>0;tmp.replace(P)
assert P.read_bytes()==raw and all(sha(Path(p).read_bytes())==h for p,h in M['previous_reviews'].items())
close={'timestamp':date,'status':'DEV_COMPLETE_NO_P0_P1_P2','review_path':str(P),'review_sha256':sha(raw),
 'review_bytes':len(raw),'review_lines':len(raw.splitlines()),'modules':5,'targets':30,'own_Lean_processes_rc0':6,
 'own_5_bins_byte_equal_author':True,'all_30_axioms_trio':True,'findings':[],'necessary_DEV_analysis_remaining':False,
 'previous_reviews_preserved':True,'new_integration_inspected':False,'author_programs_executed':False,'working_sha256':V['working_sha256']}
q=RUN/'closure_dev.json';assert not q.exists();b=json.dumps(close,ensure_ascii=False,indent=2).encode();t=q.with_suffix('.tmp')
with t.open('xb') as f:f.write(b)
assert t.read_bytes()==b;t.replace(q)
print(json.dumps(close,ensure_ascii=False,indent=2))
