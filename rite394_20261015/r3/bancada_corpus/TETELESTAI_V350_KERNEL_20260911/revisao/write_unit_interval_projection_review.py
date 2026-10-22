"""Record the bounded four-source review, preserving all prior reviews."""
from pathlib import Path
import datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding="utf-8")
REVIEW=Path(__file__).resolve().parent;ROOT=REVIEW.parent
RUN=Path((REVIEW/"unit_interval_projection_latest_run.txt").read_text(encoding="utf-8"))
M=json.loads((RUN/"manifest.json").read_bytes());C=json.loads((RUN/"compilation.json").read_bytes())
D=json.loads((RUN/"author_projection_draft_status.json").read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
assert all(C[k] for k in ["complete","all_exit_zero","full_audit_names_exact","all_axioms_allowed","sources_unchanged","dependencies_unchanged","previous_reviews_preserved"])
assert len(C["records"])==5 and len(C["records"][-1]["axioms"])==17 and len(M["all_named_declarations"])==28
assert C["records"][-1]["axioms"]==D["targets"]
for row in M["sources"].values():assert sha(Path(row["path"]).read_bytes())==row["sha256"]
for row in M["dependencies"].values():
    assert sha(Path(row["frozen_source"]).read_bytes())==row["source_sha256"]
    assert sha(Path(row["frozen_binary"]).read_bytes())==row["sha256"]
for p,h in M["previous_reviews"].items():assert sha(Path(p).read_bytes())==h
custody_raw=(ROOT/"fixed_locality_custody.json").read_bytes();custody=json.loads(custody_raw)
assert sha((REVIEW/"REVIEW_FIXED_CORE_LOCALITY.md").read_bytes())==custody["review_sha256"]
p=RUN/"previous_fixed_locality_custody.json"
if p.exists():assert p.read_bytes()==custody_raw
else:
    with p.open("xb") as f:f.write(custody_raw)
same={n:C["records"][i]["output_sha256"]==s["author_binary_sha256"] for i,(n,s) in enumerate(M["sources"].items())}
assert sum(same.values())==3
table='\n'.join(f'| `{Path(n).stem}` | {s["lines"]} | {len(s["declarations"])} | `{s["sha256"]}` |' for n,s in M['sources'].items())
builds='\n'.join(f'| `{Path(r["module"]).name}` | rc0 | {r["seconds"]} s | `{r["output_sha256"]}` |' for r in C['records'])
loglist='\n'.join(f'- `{Path(s["author_log"]).name}`.' for s in M['sources'].values())
stamp=datetime.datetime.now().astimezone();report=REVIEW/"REVIEW_UNIT_INTERVAL_PROJECTION.md"
assert not report.exists(),"An existing report requires an immediate byte backup and a dated append."
text=f'''# Revisão independente — projeção no intervalo unitário e candidato de fibra

{stamp.isoformat(timespec="seconds")}. **[REAL — revisão de fontes e recompilação própria] Escopo das quatro fontes concluído, sem achados P0, P1 ou P2.** Foram conferidos 17 alvos impressos, os auxiliares necessários, os tipos elaborados e a composição. A certificação deste parecer é **dev**, sem inspeção ou certificação de integração deste novo lote.

O pacote constrói a isometria e, o adjunto por integral no intervalo, a projeção Q=e e*, sua expressão como recorte de integral forte das translações e o candidato C=e*Be com as duas identidades de entrelaçamento. Não presume ou conclui a igualdade global B=fibre(C), a pertença de C à álgebra original ou F=base.

## Objetos e distinções de tipo

Em todos os módulos, H é um Hilbert complexo completo e `RegularHilbert H = Lp H 2 (volume : Measure ℝ)`. Nos resultados sobre F, H é exatamente `TowerHilbert P` e F é `dualFixedCore P` da mesma representação.

| Objeto | Tipo/significado efetivo |
|---|---|
| e, `testEmbeddingCLM` | H→L², v↦1_(0,1]·v; vem de uma isometria complexa. |
| e* | L²→H, f↦∫_(0,1] f, pelo adjunto Mathlib. |
| P_I, `unitCut` | L²→L², multiplicação pela indicadora de I=(0,1]. |
| Q, `unitIntervalProjection` | L²→L², e e*: projeta sobre e(H), as funções constantes em I e nulas fora. |
| C, `fibreCandidate B` | H→L[ℂ]H, e*Be; operador limitado extraído do mesmo B. |

**P_I e Q não são confundidos.** O primeiro conserva qualquer função L² suportada em I; o segundo conserva apenas o subespaço e(H). Q não é uma projeção de dimensão finita quando H é infinito-dimensional, nem o P_F de outros contratos. A construção não coloca uma função constante não nula em todo ℝ dentro de L².

## Enunciados e provas conferidos

**`UnitIntervalProjection.lean:16–26,28–52,55–87`.** A linearidade da isometria é provada a partir do mesmo `testVector`: adição por indicadoras constantes e escalares por `fibre_testVector` aplicado a c·I. A norma vem de `testVector_norm`; a dependência congelada `L2OperatorLift.lean:70–76` usa **volume(I)=1**. Não há fator de normalização omitido. A fórmula do adjunto recebe qualquer f∈L²: sua restrição a I é L¹ pela medida finita, e o produto interno com e(v) coincide com o integral restrito. O movimento do funcional `innerSL` pela integral é legítimo e usa integrabilidade explícita.

O auxiliar `testEmbedding_adjoint_embedding` demonstra e*e=I pela preservação do produto interno da isometria; essa igualdade não é hipótese de entrada. Dela seguem Q²=Q; Q*=Q segue de `adjoint_comp` e `adjoint_adjoint`. A fórmula de Qf é exatamente e(∫_I f). O adjunto é o de operadores contínuos do Hilbert complexo, não um adjunto formal postulado.

**`TranslationCorrelation.lean:13–25,27–52`.** `realInnerBilinear` é **bilinear sobre ℝ com valores em ℂ**, pois o produto interno complexo é conjugado-linear no primeiro argumento. Isso preserva o valor complexo completo; não o substitui pela parte real nem o trata indevidamente como bilinear complexo. A continuidade usa a cota de Cauchy–Schwarz.

Para f,g:ℝ→H **integráveis**, o lema de convolução aplicado a g e f∘neg demonstra integrabilidade conjunta de (t,x)↦⟨g(x),f(x−t)⟩ em `volume.prod volume`. Só então `integral_integral_swap` aplica Fubini. A substituição t↦x−t conserva Lebesgue, com Jacobiano absoluto um. A integração no primeiro argumento conjugado-linear é tratada explicitamente por `integral_conj` e simetria conjugada, produzindo **⟨∫g,∫f⟩**, na ordem correta. Não se conclui essa identidade informativa a partir de integrais sem hipótese L¹.

**`UnitIntervalShiftProjection.lean:13–50`.** Os recortes literais `unitCutFunction f = 1_I f` são L¹ porque f∈L² e I tem medida finita. A identidade `inner_unitCut_shift` é provada **para cada t fixado**: a igualdade ae do recorte é transportada pela aplicação preservadora de medida x↦x−t. Não é tomada uma interseção não enumerável de conjuntos de medida plena para todos os t, f e g.

A prova de suporte é pontual para os **indicadores literais**, o que é válido para qualquer representante escolhido de f/g: se x e x−t pertencem a I, t=x−(x−t) é diferença de pontos de I e pertence à janela (−2,2]. Fora dela um dos indicadores é zero. Essa prova não exige avaliação pontual contínua de L² nem escolhe representantes com continuidade inexistente.

**`UnitIntervalShiftProjection.lean:52–87`.** `shiftIntegralFamily` usa as **translações ordinárias** S_t f(x)=f(x−t), não os unitários regulares torcidos pelo fluxo modular. A família é fortemente contínua e tem norma ≤1. `intervalShiftIntegral` é a integral de **vetores L²** promovida a CLM pela construção prévia `StrongIntegral.operatorIntegral`; não é uma integral de Bochner em norma de B(H).

Para provar **Q=P_I(∫_−2^2 S_t dt)P_I**, o funcional contínuo f↦⟨g,P_I f⟩ passa pela integral vetorial. O produto interno vira a correlação dos dois recortes L¹. Seu suporte permite estender o integral da janela para ℝ e aplicar Fubini; o resultado ⟨∫_I g,∫_I f⟩ é exatamente ⟨g,Qf⟩. A extensionalidade para todos f,g dá igualdade dos operadores, preservando também a parte imaginária. A orientação a≤b é demonstrada; a notação intervalar Lean corresponde a (−2,2] para o integral restrito, compatível com o integral usual em [−2,2] sob Lebesgue.

**Não há fator 1/4**: a janela contém o suporte da correlação, mas a construção é um integral, não uma média nessa janela. A normalização de e e Q vem de volume(I)=1. O argumento não substitui uma convergência em norma por convergência forte nem presume integrabilidade operatorial em norma.

**`UnitIntervalShiftProjection.lean:89–111`.** A hipótese geral pede comutação de B com todos os S_t e com P_I. `operatorIntegral_commutes` transporta a primeira pela integral forte; a álgebra de produtos dá QB=BQ, com as orientações/simetrias corretas. No resultado final para B∈F, ambas as premissas são fornecidas pelos lemas da localidade já custodiada. Não sobra uma hipótese de comutação com Q que faria a construção circular. Não se exige positividade, auto-adjunção ou unitariedade de B.

**`ConstantFibreCandidate.lean:14–15,17–54`.** C=e*Be é uma composição de CLMs, portanto está tipado em H→L[ℂ]H. Qe=e e e*Q=e* são consequências da isometria. Aplicando QB=BQ a e(v), obtém-se **B(e(v))=e(Cv)** para todo v∈H. Aplicando e* à mesma comutação, obtém-se **e*(Bf)=C(e*f)** para todo f∈L². São as identidades Be=eC e e*B=Ce* em sua forma pontual/extensional, para o mesmo e, Q e C; não há escolha de um C diferente por vetor. A última especialização recebe somente B∈F e fornece a comutação de Q pela prova anterior.

Essas identidades descrevem o subespaço de teste e sua leitura por e*. **Não controlam, por si, toda a ação de B fora desse subespaço**, nem demonstram C∈`theFactorObject P`. A igualdade global B=fibre(C) e a identificação da base não foram introduzidas por definição, por nome ou como premissa escondida.

## Evidência de recompilação independente

Fontes finais lidas, congeladas e recompiladas:

| Módulo em `kernel/TGLV350` | Linhas | #print axioms | SHA-256 dev |
|---|---|---|---|
{table}

O arquivo do autor `projection_draft_status.json` foi congelado sem modificação: SHA **`{sha((RUN/'author_projection_draft_status.json').read_bytes())}`**. Seus quatro hashes de fonte e binário foram confrontados com os bytes existentes e os logs rc0 com fonte inalterada; o conjunto e os axiomas dos 17 alvos coincidem exatamente com o auditor próprio. O estatuto original `DEVELOPMENT_COMPILED__NOT_INTEGRATED__NOT_INDEPENDENTLY_REVIEWED` permanece como registro histórico do autor. Este parecer acrescenta a verificação independente, sem reescrever aquele status ou promover sua coluna de integração.

Logs do autor efetivamente conferidos, distintos dos processos próprios abaixo:

{loglist}

Foi congelado apenas o fecho dos imports de projeto necessários: **{len(M['dependencies'])} dependências**, reutilizadas de fontes e `.olean` próprios verificados. Todos os hashes foram conferidos; as fontes dessas dependências coincidem byte a byte com as fontes vivas correspondentes no congelamento. Não houve reconstrução de dependências ou pacotes. A lista completa de origem, destino e hashes está em [manifest.json](<{(RUN/'manifest.json').as_posix()}>).

`LEAN_PATH` usa o build próprio e os pacotes instalados somente para leitura, sem builds de projeto do autor. TMP/TEMP e saídas estão na árvore isolada de `revisao/`. Compilador: `{M['lean_version']}`; SHA lido **`{M['compiler_sha256']}`**.

| Processo executado pelo revisor | Resultado | Tempo | SHA-256 `.olean` próprio |
|---|---|---|---|
{builds}

**Quatro módulos + um auditor, cinco processos rc0.** Três dos quatro `.olean` dev próprios coincidem em SHA com os do autor. `UnitIntervalProjection` tem binário próprio `{C["records"][0]["output_sha256"]}` e binário do autor `{M["sources"]["TGLV350/UnitIntervalProjection.lean"]["author_binary_sha256"]}`. A fonte é idêntica, recompilou rc0 e seus tipos/axiomas passaram; **a identidade binária desse módulo não foi obtida e a causa da diferença não foi determinada**. Não uso igualdade de binários como evidência para ele. As dependências usadas estão pinadas no manifest. Uma asserção excessiva no gerador deste relatório detectou a diferença antes de publicar; foi corrigida no script de revisão, sem edição Lean ou nova compilação. O auditor tem SHA de fonte **`{C['records'][-1]['source_sha256']}`**; realizou `#check` das **28 declarações nomeadas** e `#print axioms` dos **17 alvos impressos**. Os 11 auxiliares adicionais, incluindo e*e=I, a integral forte, a forma real-bilinear e a definição de C, foram lidos e estão auditados transitivamente pelos alvos; não foram contados como novos alvos impressos. O stdout dos tipos elaborados foi lido integralmente.

Todos os 17 alvos têm somente **`propext`, `Classical.choice`, `Quot.sound`**. Não aparecem `sorryAx`, `trustCompiler` ou axiomas customizados na auditoria transitiva. [compilation.json](<{(RUN/'compilation.json').as_posix()}>) registra conjunto exato de alvos, hashes preservados de fontes/dependências e pareceres antigos intocados, todos verdadeiros. Não houve falha de compilação na árvore própria.

## Limites, integração e preservação

**Atualização de escopo recebida:** L2CutIntegral, ZeroFromTranslatedCuts e ConstantFibreIdentification foram autorizados como complemento. Neste estrato, seu exame ainda está pendente; a conclusão conjunta de sete módulos dependerá do adendo próprio.

**[OPEN]** B=fibre(C) em todo L²; C pertencente à álgebra original/F=base; correspondência geral espectral/predual e interface padrão de peso operatorial; estado/gerador/perturbação e traço canônico; Three Locks/H1–H3 e física; contrato ampliado e runtime integral. São limites do pacote, não defeitos das quatro provas reivindicadas. A igualdade global não integra a conclusão deste primeiro estrato; será examinada no adendo autorizado de três fontes.

**Integração não examinada:** este pacote foi recebido em dev. Não atribuo aos quatro módulos as contagens integradas ou os controles do estrato anterior. O snapshot integrado referenciado pelo status do autor é `{D['integrated_working_sha256']}`, como proveniência histórica, não como uma integração destes 17 alvos. Não executei monólito, recorder, verifier ou testes Python do autor; não aprovei gate, traço, QG ou runtime.

Custódia anterior `fixed_locality_custody.json` lida: timestamp `{custody['timestamp']}`, SHA **`{sha(custody_raw)}`**. O parecer `REVIEW_FIXED_CORE_LOCALITY.md` coincide com seu `review_sha256` **`{custody['review_sha256']}`** e permaneceu intocado, assim como todos os demais pareceres custodiados registrados no manifest. Nenhuma escrita em fontes autorais, integrações, originais, logs ou memórias; todas as saídas estão em `revisao/`.

Este novo parecer foi criado por temporário, verificação de bytes e substituição. Adendos posteriores exigem backup imediato byte a byte e append, preservando o presente estrato. **Conclusão: revisão das quatro fontes e dos 17 alvos encerrada, sem achados P0–P2 ou análise específica pendente dentro desse escopo dev.**
'''
raw=text.encode('utf-8');tmp=report.with_name(report.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and len(raw)>0;tmp.replace(report);assert report.read_bytes()==raw
receipt={'timestamp':stamp.isoformat(),'report':str(report),'report_sha256':sha(raw),'report_bytes':len(raw),'four_source_review_complete':True,'integration_reviewed':False,'findings_P0_P1_P2':[],'independent_source_compiles_rc0':4,'independent_auditor_rc0':1,'printed_targets':17,'named_types_checked':28,'pinned_project_dependencies':len(M['dependencies']),'own_binaries_equal_author':same,'draft_status_sha256':sha((RUN/'author_projection_draft_status.json').read_bytes()),'own_axioms_equal_draft_targets':True,'previous_reviews_preserved':True,'later_global_fibre_identity_reviewed':False,'monolith_or_recorder_executed':False}
with (RUN/'source_review_receipt.json').open('xb') as f:f.write(json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(receipt,ensure_ascii=False,indent=2))
