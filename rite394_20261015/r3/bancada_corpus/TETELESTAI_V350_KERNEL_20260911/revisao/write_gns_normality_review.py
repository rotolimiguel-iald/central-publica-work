"""Create only the new DEV GNS-normality review and its measured closure record."""
from pathlib import Path
import ast,datetime,hashlib,json
R=Path(__file__).resolve().parent;ROOT=R.parent
RUN=Path((R/'gns_normality_latest_run.txt').read_text(encoding='utf-8'))
M=json.loads((RUN/'manifest.json').read_bytes());C=json.loads((RUN/'compilation.json').read_bytes())
V=json.loads((RUN/'verification_dev.json').read_bytes());K=json.loads((RUN/'tomita_domain_custody.json').read_bytes())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for k in ['complete','all_exit_zero','full_audit_names_exact','all_axioms_allowed','sources_unchanged','dependencies_unchanged','previous_reviews_preserved']:assert C[k],k
for k in ['three_compiles_rc0','exact_target_set','axioms_match_status','all_axioms_allowed','dependencies_frozen_preserved','author_project_builds_excluded','status_unchanged','route_equals_status_and_frozen','custody_equals_status','previous_tomita_review_equals_custody','previous_reviews_preserved']:assert V[k],k
for row in V['records'].values():assert all(v for v in row.values() if isinstance(v,bool))
assert len(V['records'])==2 and V['audited_targets']==7 and V['type_checks']==7
for p,h in M['previous_reviews'].items():assert sha(Path(p))==h,p
assert sha(ROOT/'gns_normality_draft_status.json')==M['draft_status_sha256']
assert sha(ROOT/'ROTA_NORMALIDADE_GNS_RASCUNHO.md')==M['route_sha256']
assert sha(ROOT/'tomita_domain_custody.json')==M['custody_sha256']
assert all(sha(Path(r['path']))==r['sha256'] for r in M['sources'].values())
warnings={Path(row['module']).stem:[s for s in Path(row['stdout']).read_text(encoding='utf-8').splitlines() if 'warning:' in s] for row in C['records']}
assert all(not w for w in warnings.values())
def link(p,label=None):return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
table='\n'.join('| '+name+' | '+str(len(M['sources']['TGLV350/'+name+'.lean']['declarations']))+' | `'+row['source_sha256']+'` | `'+row['own_binary_sha256']+'` |' for name,row in V['records'].items())
logs='\n'.join('| '+name+' | '+Path(row['author_log']).name+' | `'+row['author_log_sha256']+'` |' for name,row in V['records'].items())
ex=V['dependency_comment_only_exceptions']['TGLV350.DualSemifiniteIdeal']
text=f'''# Revisão independente — normalidade em ordem da representação GNS

{date}. **DEV concluído: dois módulos/sete alvos. Nenhum achado P0, P1 ou P2 nas fontes finais e na rota examinada.** [REAL — leitura integral, recompilação e auditor independente] A mesma representação π_I de N em B(H_I) é positiva, monótona e preserva supremos internos de famílias positivas crescentes, não vazias e dirigidas, com resultado de supremo no ambiente B(H_I). O limite forte necessário é construído dentro da prova; não é premissa do teorema de normalidade.

Escopo novo: `ScalarGNSStrongContinuity.lean` (1 alvo) e `ScalarGNSNormality.lean` (6). A rota `ROTA_NORMALIDADE_GNS_RASCUNHO.md` foi lida integralmente. {link(R/'REVIEW_TOMITA_INITIAL_DOMAIN.md')} e todos os pareceres/custódias anteriores permanecem somente leitura. Não se construiu fechabilidade nem se examinou nova integração.

## Enunciados, ordem e composição

**ScalarGNSStrongContinuity.lean:16–27.** O teorema transporta para o mesmo H_I um limite forte **dado** na representação regular: recebe Tᵢ∈N, B∈N, `∀i, ‖Tᵢ‖≤C` e `∀v, Tᵢv→Bv` ao longo de `l : Filter ι`, para `ι : Type u` arbitrário. Aplica a transferência ambiente já revisada ao vetor `v.val` e `tendsto_subtype_rng` à restrição que define π_I. Não troca o espaço nem a ação por um homônimo; a coerção de π_I é a mesma representação ambiente restrita ao subespaço fechado. A conclusão é convergência em norma de H_I para cada vetor, não convergência em norma de operador. O filtro é arbitrário, sem topologia, enumerabilidade, separabilidade ou condição de não trivialidade adicional. A hipótese SOT deste lema de transferência é explícita e adequada; ela será **provada**, não pressuposta, na aplicação de normalidade.

**ScalarGNSNormality.lean:12–37 — positividade e monotonicidade (4 alvos).** A ordem é a ordem de Loewner herdada da Mathlib: A≤B significa positividade do operador B−A. `operator_le_of_sub_nonneg` usa essa ordem, não uma ordem escalar ou ponto a ponto inventada. `dualOrbitRepresentation_nonneg` usa a instância de monotonicidade do `StarAlgHom` ambiente e `map_zero`; não recebe positividade/normalidade da representação como hipótese. Na restrição a H_I, `isPositive_iff_complex` preserva tanto a realidade quanto a não negatividade de ⟨Tv,v⟩, via `v.val` e o produto interno herdado. Não se verificou somente a parte real deixando de exigir simetria. A monotonicidade de π_I segue da positividade de π_I(B−A), `map_sub` e positividade da diferença. Nenhuma premissa de normalidade é usada nesses passos.

**ScalarGNSNormality.lean:41–59 — IsLUB interno → IsLUB ambiente.** O tipo exato recebe `[Preorder ι] [IsDirectedOrder ι] [Nonempty ι]`, T:ι→N, B∈N, `∀i,0≤Tᵢ`, `Monotone T` e `IsLUB (range T) B` **no subtipo N**. A conclusão é `IsLUB (range (π_I∘T)) (π_I B)` **em todos os CLM de H_I**. O índice conserva o universo livre `u_1` no auditor; não há redução a sequências ou conjuntos enumeráveis. O Hilbert é o H_I concreto associado ao mesmo `SiteProfile P`.

A cadeia foi conferida nos termos e nas dependências congeladas:

1. `Tᵢ≤B` vem apenas da parte de majorante do IsLUB interno. Positividade dá `‖Tᵢ‖≤‖B‖` pela ordem C*. A cota é derivada, e `‖B‖≥0`. Não se exige uma nova hipótese `0≤B`: ela também segue de positividade e não vazio da família, e o lema de norma não a pede separadamente.
2. `vonNeumann_exists_positive_isLUB` (`RegularNormality.lean:52–67`) constrói um limite forte D ambiente pela convergência monótona de operadores positivos limitados. O fechamento WOT da mesma N coloca D em N; só depois o supremo ambiente de D é restringido a um IsLUB interno. **Não usa normalidade de π_I nem a promoção de um IsLUB interno arbitrário a ambiente como premissa.**
3. A unicidade entre o IsLUB interno recém-construído e o hB dado prova D=B. Assim obtém-se Tᵢ→B fortemente dentro da prova. A direção ambiente→interno na construção e a unicidade impedem circularidade na passagem inversa.
4. O lema de transferência fornece π_I(Tᵢ)v→π_I(B)v. A monotonicidade já provada permite aplicar `monotone_strong_limit_isLUB` (`TGLExt/MonotoneOperatorLimit.lean:204–220`). Esse lema aceita **qualquer majorante ambiente D em B(H_I)**: a positividade de D−π_I(Tᵢ) passa ao limite, dando D−π_I(B)≥0. A conclusão não se limita a majorantes pertencentes a π_I(N).

Não vazio e direção asseguram `atTop.NeBot`, usado na conservação de positividade, na pertença ao fechado WOT e na construção do limite. Portanto os passos de fechamento não exploram limites vacuamente válidos num filtro vazio. A transferência isolada aceita todos os filtros; o teorema de supremo usa especificamente a rede dirigida com `atTop`. Nenhuma convergência forte, continuidade SOT geral ou normalidade aparece como premissa final.

**ScalarGNSNormality.lean:63–82 — conjuntos dirigidos.** O último alvo recebe um conjunto S⊆N explicitamente **não vazio**, dirigido e positivo, com supremo interno B. O subtipo S fornece o índice e suas instâncias, a inclusão é monótona, e as igualdades entre `range` e S, e entre `range` da representação e π_I''S, são provadas. Conclui supremo contra todos os majorantes de B(H_I), com as mesmas hipóteses de ordem. Não presume existência universal de supremos de famílias não limitadas ou inclui o conjunto vazio.

O alcance demonstrado é **normalidade em ordem**, por preservação dos supremos positivos dirigidos internos. Não se afirma uma equivalência Lean geral com continuidade ultra-fraca/predual, nem se empacota aqui uma nova interface de representação normal. Esse limite não é um defeito das proposições solicitadas.

## Evidência independente

**Dois módulos + auditor, três processos rc0, sem warnings.** O auditor próprio faz sete `#check` com universos visíveis e sete `#print axioms`, cobrindo exatamente todas as declarações nomeadas das duas fontes. Sua saída foi lida integralmente. Todos os alvos dependem apenas de `propext`, `Classical.choice`, `Quot.sound`; não há `sorryAx` ou axioma extra. Os dois binários independentes são byte a byte iguais aos autorais finais.

| Fonte DEV | Alvos | SHA256 fonte viva = congelada | SHA256 .olean próprio = autoral |
|---|---:|---|---|
{table}

| Fonte | Log autoral final lido, não executado | SHA256 JSON do log |
|---|---|---|
{logs}

Em {link(RUN/'compilation.json')} estão os comandos próprios, tempos, rc e hashes. {link(RUN/'verification_dev.json')} registra comparação com status/log autoral, fonte inalterada durante o build, hash do binário, hashes de stdout/stderr e igualdade dos streams às cópias congeladas. Tentativas de elaboração anteriores não foram tratadas como erros pendentes dos bytes finais. Não houve falha de compilação própria nesta etapa.

Auditor: fonte `{V['own_auditor_source_sha256']}`, binário `{V['own_auditor_binary_sha256']}`, stdout `{V['own_auditor_stdout_sha256']}`. Tipos completos: {link(RUN/'logs/GNSNormalityAudit.stdout.txt')}. Os sete conjuntos de axiomas coincidem com o status, não apenas com o número declarado pelo autor.

**Herança e isolamento.** {link(RUN/'manifest.json')} pina as 383 dependências de projeto necessárias, fontes e binários provenientes da árvore própria anterior de Tomita/GNS. Nenhum build autoral de projeto entrou no `LEAN_PATH`; a entrada de projeto é somente `revisao/.../build`, seguida dos pacotes existentes, usados readonly. As dependências e a biblioteca não foram recompiladas. Versão `{M['lean_version']}`; compilador SHA256 `{M['compiler_sha256']}`. Fonte do autor e originais não foram editados.

A exceção histórica continua explícita: `DualSemifiniteIdeal` usa a fonte própria `{ex['source_sha256']}` e o binário próprio `{ex['sha256']}`; a fonte viva corrigida é `{ex['live_source_sha256']}`. A diferença literal exclusivamente de comentário, já revisada, foi novamente reconhecida ao congelar; provas intactas. Não se afirma reprodução binária integral da cadeia herdada. A limitação anterior de `RegularScalarWeightCertificate` não é usada, pois esse módulo não integra o fecho de imports atual. Todos os pins próprios e pareceres anteriores foram preservados.

## Documento, bibliografia e limites

Status autoral congelado: `{V['status_sha256']}`. Rota integralmente lida: `{V['route_sha256']}`. As linhas 11–17 descrevem corretamente a rede **positiva crescente com supremo interno** e a conclusão ambiente; o texto não omite essas hipóteses. O último teorema corresponde ao conjunto não vazio dirigido mencionado. As linhas 26–31 mantêm separados fechabilidade, fidelidade, normalidade e domínio máximo; não generalizam a propriedade separante de η, antes obtida para F, à álgebra N.

A referência bibliográfica das linhas 33–39 foi conferida no texto primário: o Teorema 3.12 e seu esboço, p. 45, tratam a correspondência com álgebras de Hilbert e destacam a fechabilidade da involução; o esboço usa a aproximação de um peso por funcionais normais positivos dominados. Isso sustenta a orientação documental, sem prover uma prova Lean deste peso. O livro remetido não foi consultado nem se investigou a próxima construção. [Masuda, Teorema 3.12, p. 45](https://www.math.okayama-u.ac.jp/mjou/mjou60/_02_Masuda.pdf). Consulta via PDF na web, sem pin binário do PDF; os pins acima são dos arquivos locais efetivamente medidos.

Custódia anterior: `{V['custody_sha256']}`; pin do parecer Tomita confirmado por hash vivo `{V['previous_tomita_review_sha256']}`. O snapshot anterior `{K['working_sha256']}`, {K['integrated_records']} registros/{K['controls']} controles/{K['audit_declarations']} Audit, é **herança da custódia do domínio inicial**. Não são contagens de integração dos dois módulos novos. Não foram repetidos recorder/verifier nem os backups dessa custódia.

**Conclusão DEV encerrada sem achados pendentes.** Foram conferidos sete alvos novos: transferência de limites fortes uniformemente limitados, positividade/monotonicidade e preservação de supremos positivos dirigidos na mesma representação. Não houve inspeção ou certificação de nova integração, build de raízes, execução de controles, monólito, recorders ou verifiers autorais. Toda saída nova está em `revisao/`.

Continuam fora deste parecer: fechabilidade/univalência do fecho do gráfico de Tomita, operador fechado e decomposição polar, identificação do domínio máximo de ν, KMS/identificação modular, traço, interface geral espectral/predual/operatorial, Three Locks/H1–H3/física, consumo de certificado pelo gate e runtime. Nenhuma análise necessária dos dois módulos finais ficou incompleta; não se promoveu gate nem se estendeu a revisão a fontes posteriores. Pareceres congelados permanecem intocados.
'''
p=R/'REVIEW_GNS_NORMALITY.md';assert not p.exists()
b=text.encode('utf-8');tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b and len(b)>500;tmp.replace(p)
result={'timestamp':date,'status':'DEV_COMPLETE_NO_P0_P1_P2','review_path':str(p),'review_sha256':sha(p),'review_bytes':len(b),'new_sources':2,'new_targets':7,'own_compiler_processes_rc0':3,'own_bins_equal_author':all(r['own_binary_equals_author'] for r in V['records'].values()),'previous_reviews_preserved':all(sha(Path(p))==h for p,h in M['previous_reviews'].items()),'integrated_inspection_performed':False,'author_programs_executed':False,'working_sha256_at_close':sha(ROOT/'um.py')}
out=RUN/'closure_dev.json';assert not out.exists();raw=json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8');tmp=out.with_suffix('.tmp');tmp.write_bytes(raw);assert tmp.read_bytes()==raw;tmp.replace(out)
print(json.dumps(result,ensure_ascii=False,indent=2))
