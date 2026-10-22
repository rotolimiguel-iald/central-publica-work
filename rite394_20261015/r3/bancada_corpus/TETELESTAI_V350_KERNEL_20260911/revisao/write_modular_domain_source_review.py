"""Create a new DEV review, preserving all previous sealed reviews."""
from pathlib import Path
import ast
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW=Path(__file__).resolve().parent
ROOT=REVIEW.parent
RUN=Path((REVIEW/'modular_domain_latest_run.txt').read_text(encoding='utf-8'))
M=json.loads((RUN/'manifest.json').read_bytes())
C=json.loads((RUN/'compilation.json').read_bytes())
V=json.loads((RUN/'verification_dev.json').read_bytes())
STAMP=datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
DOC=RUN/('documents_'+STAMP);DOC.mkdir()
sha=lambda raw:hashlib.sha256(raw).hexdigest()

def create(p,raw):
    assert p.resolve().is_relative_to(REVIEW) and not p.exists()
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and len(raw)>0
    tmp.replace(p)
    assert p.read_bytes()==raw

def link(p,label=None,line=None):
    return f'[{label or p.name}](<{p.as_posix()}{":"+str(line) if line else ""}>)'

def source(name,line):
    return link(ROOT/'kernel/TGLV350'/(name+'.lean'),name+'.lean',line)

docs=['MINUTA_DOMINIO_MODULAR.md','record_modular_domain_progress.py','verify_modular_domain_custody.py']
hashes={}
for name in docs:
    raw=(ROOT/name).read_bytes();create(DOC/name,raw);hashes[name]=sha(raw)
    if name.endswith('.py'):ast.parse(raw)
tree=ast.parse((DOC/'record_modular_domain_progress.py').read_bytes())
surface_expr=next(n.value for n in tree.body if isinstance(n,ast.Assign)
    and any(isinstance(t,ast.Name) and t.id=='surfaces' for t in n.targets))
surface_count=len(ast.literal_eval(surface_expr.generators[0].iter))+2
assert surface_count==22
assert V['six_compiles_rc0'] and V['all_axioms_allowed'] and V['status_target_set_exact']
assert all(sha(Path(r['path']).read_bytes())==r['sha256'] for r in M['sources'].values())
assert all(sha(Path(p).read_bytes())==h for p,h in M['previous_reviews'].items())
rows=[];logrows=[]
for rel,r in M['sources'].items():
    name=Path(rel).stem;v=V['records'][name]
    rows.append(f'| {name} | {len(r["declarations"])} | `{r["sha256"]}` | `{v["own_binary_sha256"]}` |')
    logrows.append(f'| {Path(v["author_log"]).name} | `{v["author_log_sha256"]}` |')
cert=V['records']['RegularScalarWeightCertificate']
exception=V['dependency_comment_only_exceptions']['TGLV350.DualSemifiniteIdeal']
audit=next(r for r in C['records'] if r['module']=='ModularDomainFullAudit.lean')
docrows='\n'.join(f'| {name} | `{h}` |' for name,h in hashes.items())
text=f'''# Revisão independente — domínio modular

{DATE}. **Estrato DEV e documental concluído; inspeção integrada pendente dos registros finais do autor.**

**Parecer.** [REAL — leitura integral, recompilação e auditor próprios] Não encontrei P0/P1/P2 nos cinco módulos congelados, nos 17 alvos ou na documentação examinada. As seis execuções próprias — cinco módulos e auditor — passaram com rc0. Os 17 alvos usam somente `propext`, `Classical.choice` e `Quot.sound`. Há um **limite de reprodução binária**, sem falha de elaboração ou de prova: o .olean próprio de `RegularScalarWeightCertificate` difere do autor; os outros quatro coincidem. Os dois hashes são preservados abaixo, sem atribuição de causa não demonstrada.

**Objetos e orientação.** O parâmetro é o mesmo `P : SiteProfile`. N=`regularCoreAlgebra P`, F=`dualFixedCore P`, M=`theFactorObject P`, q=`dualQuadraticIntegral` e ν=`scalarDualWeight P`; o Hilbert regular continua o L² de Lebesgue em ℝ com fibra `TowerHilbert P`. η=`regularVacuum P` é eΩ no intervalo (0,1]. Não há troca de representação nem premissa de separabilidade nova.

Em {source('ScalarModularInvariance',15)}, a identidade é exatamente **Λ_t* A Λ_t = fibre(U_t)* A fibre(U_t)** para A∈N. Com Λ_t=fibre(U_t)S_t, a prova usa S_−t∈N′, a comutação de translação com fibra e S_−t S_t=I; os fatores e sinais estão na ordem correta. O vetor η é fixado por **fibre(U_t)**, usando U_tΩ=Ω (linha 38); não se presume Λ_tη=η. A bimodularidade da q sob fibra, já provada para qualquer operador B da fibra, transporta a avaliação na linha 48. Ela não exige que U_t pertença a M. O lema de avaliação é válido para A∈N sem positividade porque q é uma função total; a lei do peso na linha 62 restringe A ao subtipo positivo. `PositiveCoreInput.regularConjugate` prova separadamente pertinência a N e positividade de Λ_t* A Λ_t. **Invariância não determina KMS nem o sinal da orientação KMS**: esta etapa não identifica esse fluxo como grupo modular de ν.

**Certificado: campos e universo.** {source('RegularScalarWeightCertificate',18)} define uma proposição sobre objetos efetivos, não uma coleção abstrata de escolhas de N, q ou ν. Seus 13 campos foram contados e impressos pelo auditor: `fixed_base`, `base_equivalence_is_amplification`, `zero`, `additive`, `homogeneous`, `monotone`, `faithful`, `normal`, `ideal_left_closed`, `ideal_square_finite`, `ideal_strong_approximation`, `candidate_flow_invariant` e `bounded_value_is_original_state`. O teorema na linha 58 recebe apenas P e entrega `RegularScalarWeightCertificate.{{u}} P`, compondo as provas correspondentes; nenhuma dessas propriedades permanece como hipótese do chamador.

O campo `normal` usa índices `ι : Type u`, preordem dirigida e não vazia, Aᵢ positivos/monótonos e `IsLUB (range A) S` interno à mesma N. A positividade de S é derivada. Não recebe limite SOT, enumerabilidade ou supremo ambiente como premissa. A saída própria confirma tanto estrutura quanto construtor polimórficos em **u arbitrário**, sem fixação em universo zero; cada instância do certificado usa o universo escolhido. O aviso de linter sobre o nome `hmono` (linha 35) refere-se ao nome não utilizado na conclusão, não à remoção da hipótese `Monotone A`, que permanece no tipo impresso. O campo do valor limitado conserva a hipótese de representação para todos os vetores e a parte real do produto interno complexo. Nenhum campo KMS, traço, GNS completo ou consumo pelo gate está presente.

**Limites fortes e adjuntos.** {source('ContractionAdjointLimit',15)} exige ‖Aᵢ‖≤1 e Aᵢv→v para todo v. A estimativa comprovada é

`‖Aᵢ* v−v‖² ≤ 2(‖v‖²−Re⟨v,Aᵢv⟩)`.

A igualdade `⟨Aᵢ* v,v⟩=⟨v,Aᵢv⟩` respeita a convenção do produto interno complexo de Mathlib. O lado direito tende a zero; compressão entre zero e essa cota, seguida da continuidade da raiz real, dá a convergência de Aᵢ*v. A cota de contração é utilizada e não foi substituída por continuidade irrestrita da adjunção em SOT. O filtro é arbitrário, inclusive o trivial; isso não cria vacuidade na aplicação concreta ao filtro não trivial `𝓝[≠] 0` em ℝ. `regularAverage_star_tendsto_identity` aplica o resultado às médias já provadas contrativas para todo h, inclusive zero.

{source('StrongBoundedApplication',15)} prova a versão necessária com vetor móvel usando `‖Aᵢ(vᵢ−v₀)‖≤C‖vᵢ−v₀‖`. Basta vᵢ→v₀ e convergência de Aᵢv₀ no vetor fixo v₀; não assume SOT em todos os vetores nem convergência em norma. A ausência de hipótese separada C≥0 não é falha: a estimativa deriva de ‖Aᵢ‖≤C multiplicada pela norma não negativa; para índice habitado a própria cota força C≥0. Para índice vazio/filtro trivial o enunciado permanece válido.

**Subálgebra e finitudes.** {source('FiniteDualStarCore',16)} constrói `NonUnitalStarSubalgebra ℂ N` com portador `{{A | HasFiniteDualSquare A ∧ HasFiniteDualSquare (star A)}}`, exatamente I∩I*. I é o ideal da cota **uniforme em todos os vetores** para q_(A*A), já construído; não é apenas o domínio finito de uma forma num Hilbert, nem é identificado aqui com o domínio escalar máximo de ν. No produto AB, o fator direito B pertence a I; no adjunto B*A*, o fator direito A* pertence a I. A escala complexa conjugada e a dupla adjunção estão corretas nas linhas 34–43. A estrutura não exige `1_mem`; esta fonte não acrescenta um teorema separado de exclusão da unidade.

Nas linhas 47–72, `regularSandwich P A h` é **A_h=X_h* A X_h**, elemento da mesma N. Para h>0, a finitude de X_h à direita dá A_h∈I, e `A_h*=(A*)_h` dá A_h*∈I. Não se supõe previamente que X_h* tenha quadrado finito. Nas linhas 74–104, a norma ‖A_h‖≤‖A‖ vale para todo h, usando as duas normas de X_h e X_h*. A aplicação limitada com vetor móvel dá X_h*(A(X_hv))→Av; a restrição de `𝓝[≠] 0` a `𝓝[>] 0` usa corretamente h>0⇒h≠0. Repetir o argumento para A* e reescrever a adjunção dá o segundo limite forte nas linhas 108–121. A mesma família satisfaz simultaneamente pertinência, cota e ambos os limites. Finalmente, as duas componentes de I∩I* dão **ν(A*A)<∞ e ν(AA*)<∞** na linha 123; não há conversão indevida de ∞ por `toReal`.

O termo “core” é usado aqui para uma subálgebra algébrica com aproximação forte junto aos adjuntos. Não há teorema de core em norma de grafo de um operador de Tomita, completamento GNS, positividade dos aproximantes para A arbitrário, A_h≤A, convergência em norma ou teorema KMS. Esses limites são compatíveis com a rota e com a minuta, não achados de defeito.

**Recompilação independente e pins.** Árvore {link(RUN,RUN.name)}. Compilador `{M['lean_version']}`, SHA256 lido `{M['compiler_sha256']}`. Foram congeladas 375 dependências de projeto a partir da revisão escalar anterior e dos catálogos próprios herdados. O `LEAN_PATH` usa exclusivamente o build próprio para o projeto, mais pacotes instalados somente para leitura; não contém builds autorais de projeto. Não houve rebuild de dependências, Mathlib ou raízes. Foram executados `#check` das 18 declarações nomeadas, `#print axioms` dos 17 alvos e `#print` completo da estrutura de 13 campos com universos explícitos.

| DEV | Alvos | SHA256 fonte lido | SHA256 .olean próprio |
|---|---:|---|---|
{chr(10).join(rows)}

Todos os hashes das fontes coincidem com `modular_domain_draft_status.json`, fonte congelada e log autoral final, que registra rc0/fonte inalterada. Cada binário autoral foi lido e coincide com seu pin. Os logs JSON aceitos e seus hashes lidos são:

| Log DEV final do autor | SHA256 do JSON |
|---|---|
{chr(10).join(logrows)}

Os hashes dos stdout/stderr autorais e próprios, dos binários e as comparações estão em {link(RUN/'verification_dev.json')}; os logs autorais foram copiados para `author_logs/`, sem alterações nos originais. {link(RUN/'compilation.json')} contém os seis comandos/processos próprios; {link(RUN/'manifest.json')} contém o fechamento de imports, pins e ambiente. {link(Path(audit['stdout']),'Saída integral do auditor')} foi lida, inclusive a estrutura e o construtor. Auditor: fonte `{V['own_auditor_source_sha256']}`, binário `{V['own_auditor_olean_sha256']}`, stdout `{V['own_auditor_stdout_sha256']}`.

**Limite binário explícito.** Em `RegularScalarWeightCertificate`, o .olean do autor é `{cert['author_binary_sha256']}` e o próprio é `{cert['own_binary_sha256']}`. Os tamanhos são 509512 e 509576 bytes, respectivamente, lidos dos arquivos. As fontes são idênticas; ambos os processos terminaram rc0 e ambos imprimem o mesmo alvo com o trio. Os stdout têm o mesmo aviso de `hmono`, apontando naturalmente para caminhos distintos. A causa exata da diferença do binário não foi isolada; não afirmo reprodução byte a byte desse módulo nem atribuo a divergência a uma causa suposta. A prova e os tipos foram verificados contra o binário **próprio** pelo auditor. Nenhum teste adicional de reprodução foi executado para além do escopo.

Há ainda a exceção de proveniência já registrada e revisada da dependência `DualSemifiniteIdeal`: fonte congelada antiga `{exception['source_sha256']}`, binário `{exception['sha256']}`, fonte viva `{exception['live_source_sha256']}`. O congelador verificou que a troca literal do comentário previamente corrigido reproduz os bytes vivos inteiros; não mudou prova alguma. As outras 374 fontes de dependências coincidem com as vivas. Não afirmo que todas as dependências estejam nos bytes documentais mais recentes. Compilador/pacotes instalados são herdados, sem reauditoria integral nesta etapa. Uma primeira tentativa do script de congelamento falhou antes de executar Lean por ponteiro próprio incorreto; o script anterior foi preservado em backup e corrigido. Nenhuma falha do código autoral resulta disso.

**Documentação e custódia.** A rota {link(ROOT/'ROTA_DOMINIO_MODULAR_RASCUNHO.md')} foi lida integralmente e confere com o pin `{V['route_sha256']}`. Também foram lidos integralmente minuta, recorder e verifier, e analisada sua sintaxe por AST, sem executar/importar nenhum deles. A minuta explicita Λ_t* A Λ_t, a distinção KMS, os 13 campos, a subálgebra sem exigência de unidade, as duas finitudes e os dois limites fortes. Não encontrei P2 documental. As contagens futuras são campos de template, não resultados de build tomados como concluídos neste estrato.

O recorder propõe append com preservação exata de prefixo, backup de bytes e substituição atômica em {surface_count} superfícies (20 na bancada, Atlas e índice); exige leitura do parecer e confere fontes/binários/imports/axiomas/AST e flags antes de registrar. O inventário I/O é comparado à fonte histórica da custódia anterior. Isso é **inspeção estática** do mecanismo e da minuta, sem atestado de que a custódia futura foi executada. Cópias examinadas estão em {link(DOC,DOC.name)}.

| Documento ou script | SHA256 lido |
|---|---|
{docrows}

O status DEV congelado tem SHA `{V['draft_status_sha256']}`. A custódia escalar precedente tem SHA `{V['custody_sha256']}` e o parecer escalar selado permanece `{V['sealed_scalar_review_sha256']}`, exatamente o pin da custódia. Os números **79 registros / 66 controles / 6264 Audit**, working `{V['integrated_custody_historical_counts']['working_sha256']}`, pertencem àquela etapa já custodiada; não são evidência integrada dos cinco módulos novos. O autor iniciou a integração durante esta revisão, cujo exame final poderá ser acrescentado em adendo com backup imediato. Não atribuo rc0 à integração em andamento nem executo suas raízes ou controles.

**Estatuto ao encerrar este estrato.** Revisão matemática DEV e documental concluída, sem achado P0–P2; limite de reprodução binária declarado. Permanecem fora deste parecer GNS completo, `ScalarGNSOrbit`, KMS/identificação modular, traço canônico, interface geral de peso operatorial/predual, certificado consumido pelo gate, Three Locks/H1–H3, física e runtime. Nenhum parecer custodiado, fonte autoral, memória, monólito ou recorder foi alterado. Todas as escritas foram feitas exclusivamente em `revisao/`.
'''
report=REVIEW/'REVIEW_MODULAR_DOMAIN.md'
create(report,text.encode('utf-8'))
record={'timestamp':DATE,'source_review_complete':True,'documentary_review_complete':True,
    'integrated_review_complete':False,'findings':[],
    'limitation':'RegularScalarWeightCertificate olean differs; cause not isolated',
    'report':str(report),'report_sha256':sha(report.read_bytes()),'report_bytes':report.stat().st_size,
    'documents':hashes,'document_snapshot':str(DOC)}
create(DOC/'source_review.json',json.dumps(record,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(record,ensure_ascii=False,indent=2))
