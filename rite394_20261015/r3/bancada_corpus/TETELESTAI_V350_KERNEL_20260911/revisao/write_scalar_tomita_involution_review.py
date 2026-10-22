"""Write the delimited DEV review from independently verified artifacts only."""
from pathlib import Path
import datetime, hashlib, json, sys
sys.stdout.reconfigure(encoding='utf-8')
REV=Path(__file__).resolve().parent;ROOT=REV.parent
RUN=Path((REV/'scalar_tomita_involution_latest_run.txt').read_text().strip())
load=lambda p:json.loads(Path(p).read_bytes())
hf=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
M=load(RUN/'manifest.json');C=load(RUN/'compilation.json');V=load(RUN/'verification_dev.json')
D=load(RUN/'tomita_involution_draft_status.json');aux=load(RUN/'new_dependency_compilation.json')
assert all(v for v in C.values() if isinstance(v,bool))
assert V['all_19_types_printed'] and V['all_axioms_trio'] and V['all_4_own_binaries_byte_equal_author']
assert all(hf(s['path'])==s['sha256'] for s in M['sources'].values())
assert all(hf(p)==h for p,h in M['previous_reviews'].items())
assert hf(ROOT/'tomita_involution_draft_status.json')==M['draft_status_sha256']
assert hf(ROOT/'RELATORIO_INVOLUCAO_POLAR_TOMITA_DEV.md')==M['report_sha256']
link=lambda p,label=None,line=None:f'[{label or Path(p).name}](<{Path(p).as_posix()}{":"+str(line) if line else ""}>)'
src=lambda n,line:link(ROOT/'kernel/TGLV350'/(n+'.lean'),n+'.lean:'+str(line),line)
stamp=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
rows=[];pins=[]
for rel,s in M['sources'].items():
    name=Path(rel).stem;r=next(r for r in C['records'] if r['module']==rel);p=D['modules'][name]
    rows.append(f"| {src(name,1)} | {len(s['declarations'])} | rc0 / {r['seconds']:.3f} s | idêntico por bytes |")
    pins.append(f"| {name} | `{s['sha256']}` | `{r['output_sha256']}` |")
aud=C['records'][-1]
text=f'''# Revisão independente DEV — involução polar de Tomita

{stamp}. **[REAL — escopo DEV concluído] Nenhum achado P0, P1 ou P2 nas quatro fontes/19 alvos congelados.** Leitura integral das fontes, manifesto e relatório autoral; recompilação própria dos quatro módulos e auditor de todos os tipos, com universos, e axiomas. O resultado final é a involução do mesmo fator antiunitário já construído no mesmo `ScalarGNSHilbert P`. Não há premissa de involutividade de U no resultado nem na conjugação positiva que o sustenta.

Manifesto {link(ROOT/'tomita_involution_draft_status.json')}, SHA256 `{M['draft_status_sha256']}`; relatório documental {link(ROOT/'RELATORIO_INVOLUCAO_POLAR_TOMITA_DEV.md')}, SHA256 `{M['report_sha256']}`. Ambos relidos e coincidentes com os snapshots. O parecer trata estes quatro DEV; não constitui revisão de nova integração, consumo de certificado ou promoção de gate.

**Provas e tipos conferidos.** Escrevo S=`scalarClosedTomita P`, A=`scalarTomitaSquare P`=S†S, R=`scalarTomitaResolvent P`, B=`scalarTomitaPositiveRoot P` e U=`scalarTomitaPolarFactor P`, todos os objetos anteriores, sem nova escolha de representação. Os 19 alvos são 16 teoremas e três definições. Os sete genéricos de conjugação têm `H : Type` (universo 0), estrutura de Hilbert complexo e os parâmetros/hipóteses explícitos impressos; os doze concretos recebem P e, quando pertinente, vetores ou membros de domínio, sem hipótese residual sobre U, R ou densidade.

- {src('ScalarTomitaResolventFlip',12)} e {src('ScalarTomitaResolventFlip',20)}: a equação `(I+A)u=x`, com `u=Rx∈D(A)`, paga a pertinência de Rx a D(S). Para x∈D(S), `w=x−u=Au` pertence simultaneamente a D(S) e D(S†); a segunda pertinência vem da invariância do domínio de S†. Com `v=Sw`, as involuções anteriores de S e S† dão `v∈D(A)`, `Av=Su` e `(I+A)v=Sx`. Aplicar o inverso já construído fornece `SRx=Sx−RSx`. Não se assume x∈D(A), nem que A ou S tenham domínio total.
- {src('ScalarTomitaPolarResolvent',14)} e {src('ScalarTomitaPolarResolvent',22)}: a comutação reflexiva de R consigo mesmo transporta o grafo efetivo de B, provando `(Rx,RBx)∈graph B` para x∈D(B). As igualdades dos subtipos são justificadas por `Subtype.ext`; a fatoração S=UB e a identidade anterior dão `UR=(I−R)U` primeiro em Ran B. A densidade já provada de Ran B e a continuidade das duas aplicações estendem a igualdade a todo H_I. Não se usa continuidade do operador não limitado B em H_I.
- {src('AntiunitaryPositiveConjugation',21)}: `antiunitaryConjugate U T` é o operador complexo-linear limitado `x↦U(T(U⁻¹x))`. A composição de duas semilinearidades conjugadas retorna o escalar complexo usual. A multiplicatividade preserva a ordem T·V; isto não afirma que a aplicação T↦UTU⁻¹ seja complexo-linear no argumento T. Em {src('AntiunitaryPositiveConjugation',33)}, a realidade e não negatividade do pareamento são ambas verificadas: `⟨UTU⁻¹x,x⟩=conj⟨TU⁻¹x,U⁻¹x⟩`. A fonte utiliza `antiunitary_inner_conj`, cujo tipo NÃO tem `Function.Involutive`; `antiunitary_pairing_flip`, que tem essa hipótese, não é utilizado pelos quatro módulos.
- {src('AntiunitaryPositiveConjugation',52)}: `CFC.sqrt_unique` é aplicado ao candidato positivo `U√T U⁻¹`, cujo quadrado foi identificado com `UTU⁻¹`, com `hT : 0≤T` explícito. Conferi a assinatura na Mathlib usada. O wrapper {src('AntiunitaryPositiveConjugation',15)} é literalmente `CFC.sqrt` no Hilbert complexo genérico, sem instância local adicional. As especializações e coerções elaboram contra o mesmo grafo de B; não introduzem uma raiz alternativa. `hilbertComplement_nonneg` exige T≤I, suficiente para I−T≥0.
- {src('ScalarTomitaPolarInvolution',13)} a {src('ScalarTomitaPolarInvolution',45)}: os dois conjugados são obtidos com a inversa verdadeira `U.symm`, antes de provar U²=I. A positividade de R e I−R vem de `scalarTomitaResolvent_nonneg` e `scalarTomitaResolvent_le_one`. Resultam `U√R=√(I−R)U` e `U√(I−R)=√R U`, com a orientação correta.
- {src('ScalarTomitaPolarInvolution',56)} e {src('ScalarTomitaPolarInvolution',63)}: `scalarTomitaRootLift v` é um elemento de D(B) cujo vetor subjacente é exatamente √R v, via `boundedGraphLift`; a aplicação de B é √(I−R)v. A inclusão previamente provada D(B)⊆D(S) fornece um argumento legítimo para S, dando `S(√R v)=U√(I−R)v`.
- {src('ScalarTomitaPolarInvolution',72)}: a igualdade de subtipos identifica `S(√R v)` com o lift de Uv, permitindo a segunda aplicação de S no domínio correto. S²=I e as duas trocas dão U²√R v=√R v. Aqui `scalarTomitaPositiveRoot_dense` é densidade de D(B), que por definição é Ran√R; não é uma troca indevida com Ran B. A conclusão passa à aderência por continuidade de U² e da identidade. Não se supõe Ran√R=H_I, inversa limitada de √R, gap ou U⁻¹=U. O grafo de imports de {V['project_import_graph_modules']} módulos de projeto é acíclico e nenhuma dependência herdada importa os quatro novos, afastando a circularidade entre a construção de U e sua involução.

Tipo final efetivamente impresso pelo auditor:

```lean
TGLV350.Regular.scalarTomitaPolarFactor_involutive (P : TGLExt.SiteProfile) :
  Function.Involutive (TGLV350.Regular.scalarTomitaPolarFactor P)
```

**Evidência própria.** Árvore {link(RUN,RUN.name)}. {link(RUN/'compilation.json')} SHA256 `{hf(RUN/'compilation.json')}`; {link(RUN/'verification_dev.json')} SHA256 `{hf(RUN/'verification_dev.json')}`. Auditor {link(RUN/'sources/ScalarTomitaInvolutionAudit.lean')} e {link(aud['stdout'],'saída integral dos 19 tipos/axiomas')}, stream SHA256 `{aud['stdout_sha256']}`. Os 19 alvos são exatamente os do manifesto e todos dependem somente de `propext`, `Classical.choice`, `Quot.sound`; não há `sorryAx`, `trustCompiler`, axioma novo, `sorry`, `admit`, `unsafe` ou alteração de transparência nas fontes finais. O auditor também imprime os tipos dos dois lemas antiunitários antigos para tornar visível a diferença de hipóteses; esses dois tipos não são somados aos 19 alvos novos.

| Módulo | Alvos | Recompilação própria | .olean próprio versus autoral |
|---|---:|---|---|
{chr(10).join(rows)}

Auditor próprio: rc0, {aud['seconds']:.3f} s. Portanto **cinco execuções próprias rc0 para o pacote/auditor**, além da dependência canônica necessária abaixo. As quatro fontes permaneceram inalteradas durante a revisão; todos os hashes dos logs finais e de seus streams coincidem com o manifesto. Três avisos de depreciação de nomes (`mul_apply`, `sub_apply`, `one_apply`) permanecem nos dois últimos módulos; são avisos de API sem lacuna de prova e não constituem P2.

| Fonte DEV | SHA256 fonte | SHA256 .olean autoral = próprio |
|---|---|---|
{chr(10).join(pins)}

Logs autorais finais aceitos, com hashes completos também no manifesto congelado e em `verification_dev.json`:
'''
for n,p in D['modules'].items():
    text+=f"\n- {link(p['final_log'])}: JSON `{p['final_log_sha256']}`; stdout `{p['stdout_sha256']}`."
text+=f'''

**Proveniência e limites de execução.** {len(M['dependencies'])} dependências de projeto pinadas: 420 reaproveitadas da árvore própria polar anterior (fontes e binários relidos por hash) e uma adicional, `TGLExt.GenericAntilinearAdjoint`, ausente daquela árvore. A primeira preparação detectou essa ausência e parou antes de qualquer compilação; o snapshot dessa preparação foi preservado. A dependência foi então congelada, confrontada por bytes com a fonte canônica embutida na cópia já selada e compilada por mim, rc0 em {aux['seconds']:.3f} s. Fonte `{aux['source_sha256']}`, .olean próprio `{aux['output_sha256']}`; {link(RUN/'new_dependency_compilation.json')}. Sua fonte foi lida, com atenção ao lema de polarização usado; suas 15 impressões de axiomas ficaram no trio e são evidência da dependência antiga, não 15 resultados novos deste pacote.

O `LEAN_PATH` registrado no {link(RUN/'manifest.json')} contém apenas o build desta revisão e oito caminhos de pacotes externos read-only. Nenhum build autoral de projeto foi usado para resolver imports. Compilador herdado {M['lean_version']}, binário SHA256 `{M['compiler_sha256']}` relido; pacotes Mathlib/bibliotecas não recompilados. As duas fontes Mathlib consultadas têm pins em `verification_dev.json`. Mantém-se a herança explicitada no manifesto, inclusive a errata apenas de comentário já documentada em dependência anterior. Não se declara rebuild independente do kernel inteiro ou dos pacotes.

Histórico preservado em {link(RUN/'author_history.json')}: 13 registros/streams, dos quais quatro rc0 finais aceitos, dois rc0 anteriores de `AntiunitaryPositiveConjugation` superados, cinco rc1 dos módulos e dois rc1 do probe descartado. Os rc1, inclusive impressões eventualmente produzidas sob falha, não sustentam a conclusão. Nenhum probe foi importado ou recompilado. Os registros autorais são relidos; as seis execuções Lean próprias (uma dependência, quatro DEV e auditor) têm evidência separada. Nenhum programa autoral, recorder, integrador, teste autoral ou monólito foi executado/importado.

**Custódia e alcance documental.** Mãe {link(ROOT/'tomita_polar_custody.json')} SHA256 `{V['custody_sha256']}`, com verificação autoral pinada `{V['custody_verification_sha256']}`. Cópia ainda `{V['working_sha256']}`; original relido `{V['original_sha256']}`. Os pareceres anteriores e os pins matemáticos da mãe foram preservados. As atualizações documentais paralelas autorizadas ao autor não integram esta revisão e não foram tratadas como mudança das fontes congeladas. A ausência dos 19 alvos no mapa Audit integrado atual foi conferida; contagens, controles e flags da integração anterior não foram reexecutados nesta rodada DEV.

O relatório autoral foi lido integralmente e não excede a prova: U é agora uma antiunitária involutiva da decomposição polar deste S em H_I. A frase sobre parâmetros finais se aplica aos resultados concretos; os auxiliares genéricos preservam expressamente H, U e positividade onde necessária. [OPEN] A identificação modular do peso e seu domínio máximo, a ponte I=n_ν, KMS/fluxo modular, identificação com outros candidatos J, traço, Three Locks, condições físicas e runtime integral não seguem deste pacote. Núcleo trivial não fornece gap; o domínio de B não é promovido a todo H_I.

**Conclusão delimitada:** sem P0–P2 e sem análise DEV necessária restante para estas quatro fontes/19 alvos. Está conferida U²=I para o U original, além das identidades e pertinências utilizadas. Nova integração e qualquer consumo em gate exigem seu próprio escopo; este parecer não os realiza. Escritas exclusivamente em `revisao/`; originais, fontes autorais, memórias, logs autorais e pareceres selados permanecem intocados pelo revisor.
'''
out=REV/'REVIEW_SCALAR_TOMITA_INVOLUTION.md';data=text.encode('utf-8')
backup=None
if out.exists():
    before=out.read_bytes();backup=out.with_name(out.name+'.bak_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with backup.open('xb') as f:f.write(before)
    assert backup.read_bytes()==before
    data=before+b'\n\n'+data
tmp=out.with_name(out.name+'.tmp_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
with tmp.open('xb') as f:f.write(data)
assert tmp.read_bytes()==data and len(data)>0;tmp.replace(out);assert out.read_bytes()==data
closure={'timestamp':stamp,'report':str(out),'sha256':hf(out),'bytes':len(data),'lines':len(data.splitlines()),'backup':str(backup) if backup else None,'findings_P0_P2':[],'scope_complete':True,'compilation_sha256':hf(RUN/'compilation.json'),'verification_sha256':hf(RUN/'verification_dev.json')}
p=RUN/'closure_dev.json';assert not p.exists();q=p.with_suffix('.tmp');raw=json.dumps(closure,ensure_ascii=False,indent=2).encode();q.write_bytes(raw);assert q.read_bytes()==raw;q.replace(p)
print(json.dumps(closure,ensure_ascii=False,indent=2))
