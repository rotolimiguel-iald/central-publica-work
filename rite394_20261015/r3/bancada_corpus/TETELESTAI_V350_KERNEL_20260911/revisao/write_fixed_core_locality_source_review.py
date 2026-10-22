"""Record the completed five-source locality review, without certifying integration."""
from pathlib import Path
import datetime,hashlib,json,sys
sys.stdout.reconfigure(encoding="utf-8")
REVIEW=Path(__file__).resolve().parent;ROOT=REVIEW.parent
RUN=Path((REVIEW/"fixed_core_locality_latest_run.txt").read_text(encoding="utf-8"))
M=json.loads((RUN/"manifest.json").read_bytes());C=json.loads((RUN/"compilation.json").read_bytes())
sha=lambda b:hashlib.sha256(b).hexdigest()
assert all(C[k] for k in ["complete","all_exit_zero","full_audit_names_exact","all_axioms_allowed","sources_unchanged","dependencies_unchanged","previous_reviews_preserved"])
assert len(C["records"])==6 and len(C["records"][-1]["axioms"])==16
for row in M["sources"].values():assert sha(Path(row["path"]).read_bytes())==row["sha256"]
for p,h in M["previous_reviews"].items():assert sha(Path(p).read_bytes())==h
custody_raw=(ROOT/"bounded_values_custody.json").read_bytes();custody=json.loads(custody_raw)
assert sha((REVIEW/"REVIEW_BOUNDED_DUAL_VALUES.md").read_bytes())==custody["review_sha256"]
with (RUN/"previous_bounded_values_custody.json").open("xb") as f:f.write(custody_raw)
table='\n'.join(f'| `{Path(n).stem}` | {s["lines"]} | {len(s["declarations"])} | `{s["sha256"]}` |' for n,s in M['sources'].items())
buildtable='\n'.join(f'| `{Path(r["module"]).name}` | rc0 | {r["seconds"]} s | `{r["output_sha256"]}` |' for r in C['records'])
loglist='\n'.join(f'- `{Path(s["author_log"]).name}`.' for s in M['sources'].values())
same={n:C['records'][i]['output_sha256']==s['author_binary_sha256'] for i,(n,s) in enumerate(M['sources'].items())}
stamp=datetime.datetime.now().astimezone();report=REVIEW/"REVIEW_FIXED_CORE_LOCALITY.md"
assert not report.exists(),"Use a byte-preserving dated addendum for an existing review."
text=f'''# Revisão independente — localidade da álgebra fixa

## Parecer das cinco fontes — {stamp.isoformat(timespec="seconds")}

**[REAL] Exame matemático e recompilação independente das cinco fontes concluídos, sem achados P0, P1 ou P2.** O resultado é a comutação de todo B∈F com os recortes mensuráveis no mesmo L² regular, obtida de pareamentos L¹ e unicidade Fourier. Não pressupõe decomposição em fibras de B, ação constante de B na fibra ou F=base. Este estrato certifica as fontes dev abaixo e o auditor próprio; **integração deste lote ainda não inspecionada aqui**. Eventual inspeção integrada será um adendo separado, com preservação deste texto.

### Fontes e alvos

| Módulo dev em `kernel/TGLV350` | Linhas | #print axioms | SHA-256 lido e congelado |
|---|---|---|---|
{table}

São **16 alvos impressos e 17 declarações nomeadas**: `measurableCutLp_ae` é o auxiliar adicional, não impresso pelo autor. O auditor próprio fez `#check` de todas as 17 declarações, com universos, e `#print axioms` dos 16 alvos exatos. O auxiliar foi lido e é usado transitivamente pelos alvos auditados. Não há alvos importados contados como novos.

### Pontos adversariais conferidos, com linhas

**`FixedCoreShiftCommutation.lean:12,25,44,55`.** A translação ordinária é `shift s`, f(x)↦f(x−s); a família modular regular é `regularUnitary P t = fibre(modularFlowCLM P t) * shift t`. A prova mantém esses dois grupos distintos. Translações comutam com cada gerador de fibra constante e com cada unitário regular, usando `shift_mul` e comutatividade da adição real. A pertença ao comutante passa por `regularCore_minimal` aplicado ao comutante-estrela das translações; as condições envolvendo os adjuntos são demonstradas com `shift_star` e −s. Não se presume que um operador arbitrário de N seja fibra constante. As simetrias na passagem entre a convenção de `mem_centralizer_iff` e `mem_commutant_iff` produzem as orientações declaradas. No último lema, B∈F fornece B∈N e sua invariância dual; a comutação com caracteres vem dessa invariância já demonstrada, não da comutação com translações.

**`FourierUniqueness.lean:16–31`.** O teorema exige f,g:ℝ→H integráveis e igualdade dos Fourier ordinários em todas as frequências; conclui igualdade quase em toda parte para `volume`. Ele não exige continuidade de f/g, L² de f/g ou integrabilidade de suas transformadas. `fourier_test_pairing` é aplicado a 𝓕⁻φ para φ de Schwartz; `fourier_fourierInv_eq` devolve φ, preservando a convenção da transformada. A igualdade das transformadas dá igualdade dos pareamentos com todas essas funções teste. Os testes reais suaves de suporte compacto são embutidos em ℂ pelo mapa contínuo `Complex.ofRealCLM` e convertidos em Schwartz; a unicidade de funções localmente integráveis dá a conclusão ae. A hipótese L¹ é usada nessa cadeia, impedindo a vacuidade que seria possível ao tratar integrais de funções não integráveis como informação suficiente.

**`CharacterLocality.lean:16,28,40`.** `characterPhase s x = exp(−i s x)` é a fase efetiva do mesmo multiplicador dual. A identidade Fourier usa **s=2πξ**, com sinal negativo; não muda a normalização ou troca frequência angular por frequência sem o fator. O produto interno é conjugado-linear no primeiro argumento e linear no segundo: por isso a fase multiplica g em `⟨f,D_(2πξ)g⟩`, como mostram `inner_smul_right` e `L2.inner_def`.

Os dois pareamentos pontuais `⟨(B.adjoint f)(x),g(x)⟩` e `⟨f(x),(Bg)(x)⟩` pertencem a L¹ por `L2.integrable_inner`, para B contínuo complexo-linear no mesmo L². A igualdade das transformadas segue de `adjoint_inner_left` e da hipótese **∀s, D_s B = B D_s**, na orientação efetivamente necessária. Não se exige B positivo, auto-adjunto ou unitário; o adjunto existe no Hilbert completo. A conclusão é uma igualdade ae para **cada par fixado f,g**. O conjunto excepcional pode depender do par; a prova seguinte nunca promove essa conclusão a uma igualdade pontual simultânea para todos os vetores. Não se introduz separabilidade da fibra H nem um teorema de operadores decomponíveis.

**`L2MeasurableCut.lean:12–17,19–47,51–65`.** `measurableCutLp` usa `MemLp.indicator` e `toLp` no quociente L² existente. O auxiliar ae vincula o representante ao indicador; adição e escalares usam as igualdades ae de Lp, não igualdade arbitrária de representantes. A norma do recorte é ≤‖f‖ pelo limite pontual de normas, e `mkContinuous 1` constrói o operador complexo-linear limitado. A fórmula do produto interno é o integral restrito do pareamento L¹, por `integral_indicator` e congruência ae.

O conjunto S é **mensurável e pode ter volume finito, infinito ou zero**; não há hipótese de medida finita, intervalo, compacidade ou interior. A medida do espaço, porém, continua sendo **Lebesgue em ℝ**: estes enunciados não estão quantificados sobre uma medida arbitrária μ ou conjuntos não mensuráveis. “Qualquer medida do recorte” deve ser entendido como ausência de restrição ao valor de `volume S`, não como troca da medida-base. O recorte espacial não é a projeção finita P_F de outras etapas, nem a projeção posterior sobre funções constantes em um intervalo.

**`FixedCoreLocality.lean:16–28,32–37`.** Para cada S mensurável, a extensionalidade do operador e do produto interno reduz a igualdade `M_S B = B M_S` à identidade de pareamentos integrados sobre S. A identidade ae da etapa Fourier é restringida com `ae_restrict_of_ae`; isso funciona para qualquer S mensurável, sem uniformizar os conjuntos excepcionais em f,g. A posição do adjunto em `⟨B* f,M_S g⟩` e a simetria final estão corretas. O último lema compõe essa prova com a comutação por caracteres de B∈F. Não acrescenta premissa residual de localidade, decomposição, identidade F=base ou constância da fibra.

Todos os enunciados atuam no mesmo `RegularHilbert H = Lp H 2 (volume : Measure ℝ)`, especializado a H=`TowerHilbert P` nos resultados sobre N/F. Não se extrai informação de uma leitura em um único vetor, de uma função não integrável ou de um `toReal` aplicado a ∞; as novas fontes não usam essa conversão. A passagem decisiva usa integrabilidade dos pareamentos escalares, não integração em norma de B(H).

### Evidência independente e proveniência

Foi copiado apenas o fecho transitivo dos imports de projeto necessários às cinco fontes: **{len(M['dependencies'])} módulos**, com fontes e `.olean` de árvores próprias previamente verificadas. Cada par foi conferido por SHA-256; **todas essas fontes de dependência coincidem byte a byte com as fontes vivas correspondentes** no congelamento. O fecho não inclui `DualSemifiniteIdeal`, `BoundedDualValues` ou `BoundedFiniteSquares`; portanto não herda a diferença de comentário documentada na etapa anterior. Os mapas completos de origem e destino estão no [manifest.json](<{(RUN/'manifest.json').as_posix()}>).

O `LEAN_PATH` aponta para o build isolado e para os pacotes instalados somente para leitura, sem os builds de projeto do autor. TMP/TEMP e todas as saídas estão na árvore própria em `revisao/`. Não recompilei Mathlib nem as dependências de projeto. Compilador: `{M['lean_version']}`; SHA do executável lido **`{M['compiler_sha256']}`**.

| Processo executado pelo revisor | Resultado | Tempo | SHA-256 `.olean` próprio |
|---|---|---|---|
{buildtable}

Os cinco binários próprios coincidem com os respectivos binários dev do autor: **{all(same.values())}** (confronto individual no recibo desta revisão). Fonte do auditor SHA **`{C['records'][-1]['source_sha256']}`**. Todos os 16 alvos têm somente `propext`, `Classical.choice`, `Quot.sound`; não há axioma customizado, `sorryAx` ou `trustCompiler` em suas dependências transitivas auditadas. Os tipos elaborados do auditor foram lidos. [compilation.json](<{(RUN/'compilation.json').as_posix()}>) registra seis processos rc0, conjunto exato de alvos, hashes das fontes/dependências preservados e pareceres anteriores intocados.

Os logs dev do autor abaixo foram copiados e confrontados com os hashes de fonte e binário; são evidência adicional do autor, distinta dos seis processos próprios:

{loglist}

### Limites e preservação

**[OPEN]** Constância da ação de B na fibra; identificação F=base original; construção/interface padrão do peso operatorial e correspondência geral espectral/predual; traço canônico, Three Locks/H1–H3, física, contrato ampliado e runtime integral. A localidade por recortes aqui provada não é uma prova dessas identificações posteriores, nem uma hipótese delas assumida retroativamente. A etapa posterior de projeção da componente constante num intervalo está fora deste exame.

A integração deste lote não foi inspecionada neste estrato; contagens de build/testes/Audit do pacote anterior não são atribuídas às novas fontes. Não executei monólito, recorder, verifier ou controles Python do autor. Nenhuma flag ou QG foi aprovada.

Custódia anterior lida: `bounded_values_custody.json`, timestamp `{custody['timestamp']}`, SHA `{sha(custody_raw)}`. O parecer custodiado `REVIEW_BOUNDED_DUAL_VALUES.md` permanece igual ao hash `{custody['review_sha256']}`. Todos os pareceres anteriores mantêm os hashes do manifest desta revisão. Não os modifiquei, nem alterei fontes do autor, originais, monólito, logs ou memórias. Este novo parecer foi criado por temporário verificado e substituição; qualquer adendo preservará seus bytes por backup imediato e append.

**Conclusão delimitada das fontes: nenhum P0–P2 encontrado; cinco módulos e auditor próprio concluídos, 16 alvos no trio, sem análise matemática pendente nas fontes recebidas.**
'''
raw=text.encode('utf-8');tmp=report.with_name(report.name+'.tmp')
with tmp.open('xb') as f:f.write(raw)
assert tmp.read_bytes()==raw and len(raw)>0;tmp.replace(report);assert report.read_bytes()==raw
receipt={'timestamp':stamp.isoformat(),'report':str(report),'report_sha256':sha(raw),'report_bytes':len(raw),'source_review_complete':True,'integration_review_complete':False,'findings_P0_P1_P2':[],'own_source_compiles_rc0':5,'own_auditors_rc0':1,'printed_targets':16,'named_types_checked':17,'source_binary_equal_author':same,'previous_reviews_preserved':True,'sources_and_frozen_dependencies_preserved':True}
with (RUN/'source_review_receipt.json').open('xb') as f:f.write(json.dumps(receipt,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(receipt,ensure_ascii=False,indent=2))
