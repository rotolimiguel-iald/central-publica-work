"""Create the completed three-module DEV review without touching sealed reports."""
from pathlib import Path
import datetime
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
REVIEW=Path(__file__).resolve().parent;ROOT=REVIEW.parent
RUN=Path((REVIEW/'gns_orbit_latest_run.txt').read_text(encoding='utf-8'))
M=json.loads((RUN/'manifest.json').read_bytes())
C=json.loads((RUN/'compilation.json').read_bytes())
V=json.loads((RUN/'verification_dev.json').read_bytes())
DATE=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
sha=lambda raw:hashlib.sha256(raw).hexdigest()

def create(p,raw):
    assert p.resolve().is_relative_to(REVIEW) and not p.exists()
    tmp=p.with_name(p.name+'.tmp')
    with tmp.open('xb') as f:f.write(raw)
    assert tmp.read_bytes()==raw and tmp.stat().st_size==len(raw)>0
    tmp.replace(p)
    assert p.read_bytes()==raw

def link(p,label=None,line=None):
    return f'[{label or p.name}](<{p.as_posix()}{":"+str(line) if line else ""}>)'

def source(name,line):return link(ROOT/'kernel/TGLV350'/(name+'.lean'),name+'.lean',line)

assert V['four_compiles_rc0'] and V['exact_target_set'] and V['all_axioms_allowed']
assert all(sha(Path(r['path']).read_bytes())==r['sha256'] for r in M['sources'].values())
assert all(sha(Path(p).read_bytes())==h for p,h in M['previous_reviews'].items())
assert all(r['own_binary_equals_author'] and r['source_equals_status_and_frozen']
    and r['author_binary_equals_status_and_log'] and r['author_log_rc0_source_unchanged']
    and r['target_names_exact'] and r['author_streams_frozen_equal'] for r in V['records'].values())
rows=[];logrows=[]
for rel,r in M['sources'].items():
    name=Path(rel).stem;v=V['records'][name]
    rows.append(f'| {name} | {len(r["declarations"])} | `{r["sha256"]}` | `{v["own_binary_sha256"]}` |')
    logrows.append(f'| {Path(v["author_log"]).name} | `{v["author_log_sha256"]}` |')
audit=C['records'][-1]
exception=V['dependency_comment_only_exceptions']['TGLV350.DualSemifiniteIdeal']
live_um=sha((ROOT/'um.py').read_bytes())
body=f'''# Revisão independente — inscrição GNS por órbita e ação ambiente

{DATE}. **Parecer DEV concluído: três fontes, 14 alvos, rota documental e recompilação próprias.**

**Conclusão e achados.** [REAL — inspeção/recompilação independentes] Não encontrei P0/P1/P2 nas versões finais examinadas. As três fontes foram lidas integralmente (63, 91 e 53 linhas); seus 14 enunciados foram conferidos por `#check` com universos explícitos e `#print axioms`. Os três módulos e o auditor próprio passaram com rc0. Todos os alvos dependem apenas de `propext`, `Classical.choice` e `Quot.sound`. Os três .olean próprios coincidem byte a byte com os .olean DEV finais do autor. Nenhuma análise solicitada do escopo DEV ficou pendente.

O resultado é a inscrição linear complexa injetiva **sobre o ideal I já construído**, com norma dada pela avaliação escalar de q_(A*A), e uma ação limitada no Hilbert ambiente que entrelaça multiplicação à esquerda. Este parecer não atesta completamento GNS, representação empacotada no fecho, Tomita, KMS, traço ou consumo de certificado pelo gate.

**Mesmos objetos e domínio.** Para o mesmo `P : SiteProfile`, H=`TowerHilbert P`, K=`RegularHilbert H` é `Lp H 2 (volume : Measure ℝ)`, N=`regularCoreAlgebra P`, η=`regularVacuum P` é eΩ e I=`finiteDualLeftIdeal P` é o submódulo complexo de N definido por `HasFiniteDualSquare`. O Hilbert de chegada é o **novo ambiente exterior L²(ℝ,K)=L²(ℝ,L²(ℝ,H))**, mantendo a representação regular original como fibra. As duas cópias de Lebesgue e as coerções duplas do subtipo A∈I⊂N aparecem corretamente nos tipos. I exige uma única cota para q_(A*A)(v) em **todos** os vetores v; não é identificado aqui com o domínio escalar máximo 𝔫_ν, nem com D(q_A) de uma forma em H.

**Órbita, fator Haar e integral.** Em {source('ScalarGNSOrbit',15)}, o lema genérico aceita A limitado e `HasFiniteDualSquare A`; não precisa assumir A∈N para a integrabilidade isolada. Ao definir Λ_ν em I, essa hipótese vem da própria pertinência ao subtipo, sem premissa residual adicional. `HasFiniteDualSquare.scalar_finite` dá q_(A*A)(η)<∞. A identidade anterior `dualQuadraticIntegrand_star_mul` escreve esse valor como `ofReal(c)·∫⁻s ofReal(‖θ_s(A)η‖²)`, com c=`dualHaarFactor`=(2π)⁻¹. A positividade estrita de c fornece `ofReal(c)≠0`; se a integral fosse ∞, a multiplicação seria ∞, contradizendo a finitude. A prova não usa a conversão de ∞ para zero. A ocorrência de `ENNReal.toReal_ofNat` na linha 35 concerne ao expoente literal 2 da caracterização de `MemLp`, não ao valor de q ou de uma integral infinita.

A continuidade **forte** de s↦θ_s(A)η fornece a mensurabilidade forte quase em toda parte; não há pressuposto de continuidade em norma operatorial, separabilidade de H ou avaliação pontual arbitrária de uma classe L². A definição na linha 39 é exatamente

`Λ_ν(A) = sqrt(c) • toLp (s ↦ θ_s(A)η)`.

Na linha 45, `MemLp` é primeiro convertido em integrabilidade real de ‖θ_s(A)η‖². Só depois são usadas a identidade norma–integral do L² e a passagem da integral real não negativa à integral ENNReal. O quadrado de sqrt(c) recompõe c, e o resultado é **`ENNReal.ofReal (‖Λ_ν(A)‖²) = q_(A*A)(η)`**, que é ν(A*A) para esse elemento positivo da mesma N. Não há perda de fator 2π ou nova convenção de Fourier introduzida. O lema de `FourierL1L2` utilizado aqui é a identidade de norma do `toLp`, não um novo teorema de identificação Fourier da normalização escolhida.

**Linearidade e fidelidade.** {source('ScalarGNSLinear',19)} explicita a função representante apenas por igualdade **quase em toda parte**. Adição e escala complexa usam `Lp.ext` e um número finito de igualdades a.e. para A, B e c já fixados. Não se toma interseção não enumerável de conjuntos conulos. A escala sqrt(c_Haar) é real, mas comuta com a escala complexa; `map_smul` de θ_s e `smul_comm` produzem a homogeneidade complexa correta, sem conjugação do escalar da entrada.

`scalarGNSLinear` (linha 55) é um **`LinearMap` sobre ℂ** cujo `toFun` é essa mesma órbita. Não é declarado `ContinuousLinearMap` na norma operatorial herdada por I; também não se declara uma isometria nessa norma. Sua identidade de norma é a do peso ν(A*A). Na linha 61, Λ_ν(A)=0 implica q_(A*A)(η)=0 pela identidade anterior; A*A é explicitamente provado positivo e pertencente à mesma N antes de aplicar a fidelidade do vácuo. Seguem A*A=0 e A=0 por `CStarRing.star_mul_self_eq_zero_iff`, com as duas coerções de subtipo eliminadas corretamente. A volta usa `map_zero` da aplicação linear já construída, sem circularidade. Aplicar esse resultado a A−B prova a injetividade na linha 77.

**Ação ambiente e ordem dos fatores.** Em {source('ScalarGNSAction',12)}, `scalarGNSLeftProduct P B A` é BA em I, para B∈N e A∈I, mediante fechamento do mesmo ideal à esquerda. Não se exige B∈I. A ação `scalarGNSAmbientAction P B` é `operatorFieldLift (dualIntegralFamily B.val)` no **mesmo L² exterior**. A família tem operador em s igual a θ_s(B), continuidade forte e cota uniforme ‖B‖; a cota resulta da conjugação unitária de θ_s. Portanto o operador contínuo linear construído satisfaz **‖L_B‖≤‖B‖** no Hilbert ambiente, sem medida nova ou fator Haar adicional na ação.

O entrelaçamento na linha 30 é exatamente **L_B Λ_ν(A)=Λ_ν(BA)**. Após combinar as três igualdades a.e. pertinentes, a igualdade pontual usada é θ_s(B)(sqrt(c)·θ_s(A)η)=sqrt(c)·θ_s(BA)η. `map_smul` e `map_mul` preservam a ordem **B seguido de A** na multiplicação de operadores; não se obtém uma ação oposta ou uma ação pela adjunta. Não se presume θ_sη=η. O resultado refere-se à aplicação concreta sobre I, não apenas à existência de alguma representação abstrata.

**Evidência própria e hashes.** Árvore {link(RUN,RUN.name)}. Compilador `{M['lean_version']}`, SHA256 lido `{M['compiler_sha256']}`. Foram executados apenas os três módulos autorizados e `GNSOrbitFullAudit.lean`; os quatro processos terminaram rc0. A lista de 14 alvos corresponde exatamente ao status congelado (3+7+4), e todos os tipos/axiomas da saída própria foram lidos. Não foram reexecutados testes do autor, raízes ou bibliotecas.

| Fonte DEV | Alvos | SHA256 fonte lido | SHA256 .olean próprio = autor |
|---|---:|---|---|
{chr(10).join(rows)}

Os logs finais do autor foram usados **como evidência lida**, com rc0, fonte inalterada e hashes de fontes/binários conferidos diretamente no disco. São distintos das quatro execuções próprias. Seus JSONs foram congelados byte a byte em `author_logs/`:

| Log DEV final do autor | SHA256 do JSON |
|---|---|
{chr(10).join(logrows)}

{link(RUN/'compilation.json')} contém comandos, retornos, hashes e mapas de axiomas próprios. {link(RUN/'verification_dev.json')} registra separadamente hashes de stdout/stderr autorais e próprios, correspondência ao status, identidade dos binários e preservação dos pareceres. {link(RUN/'manifest.json')} contém fontes, fechamento de imports e `LEAN_PATH`. Auditor: fonte `{V['own_auditor_source_sha256']}`, .olean `{V['own_auditor_binary_sha256']}`, stdout `{V['own_auditor_stdout_sha256']}`. A {link(Path(audit['stdout']),'saída integral de tipos/axiomas')} foi inspecionada; nenhum alvo está apenas declarado sem recompilação nesta revisão.

**Dependências e limites de herança.** Foram congeladas **{V['project_dependency_count']} dependências de projeto**, reutilizando fontes e binários de árvores próprias previamente revisadas, a partir do catálogo da etapa modular. O `LEAN_PATH` contém o build próprio seguido dos pacotes instalados somente para leitura; não contém build autoral do projeto. Não foram recompiladas dependências, Mathlib ou raízes, e não se afirma reauditoria integral dos pacotes nesta rodada. A declaração `RegularScalarWeightCertificate`, cujo binário divergira na etapa anterior, não pertence ao fechamento de imports desta etapa.

A única diferença documental medida entre fonte de dependência congelada e viva é a errata já revisada de `DualSemifiniteIdeal`: fonte congelada `{exception['source_sha256']}`, binário `{exception['sha256']}`, fonte viva corrigida `{exception['live_source_sha256']}`. A troca literal dos bytes do comentário reproduz toda a fonte viva, sem mudança de provas. As demais 373 fontes coincidem com as vivas no congelamento. As fontes e binários herdados permanecem pinados no manifest; as limitações históricas dessa herança não são apagadas por esta revisão. Fontes novas, dependências congeladas e pareceres anteriores foram verificados novamente após a compilação e preservados.

**Rota documental e fronteiras.** {link(ROOT/'ROTA_GNS_RASCUNHO.md')} foi lida integralmente e congelada, SHA **`{V['route_sha256']}`**, igual ao pin do status. Não encontrei exagero de estatuto: distingue I do domínio máximo, inscrição da órbita de completamento da imagem e ação ambiente de *-representação no fecho. Também distingue corretamente aproximação forte de A_h/A_h* em N de convergência na norma ν ou de propriedade de core em norma de grafo de Tomita. As estimativas futuras por convergência dominada/multiplicação à direita estão marcadas como rota a testar; não são promovidas a resultados deste pacote nem foram investigadas como novos teoremas por mim.

Permanecem fora do escopo: fecho da imagem como Hilbert GNS, leis empacotadas de *-representação nesse fecho, extensão ao domínio escalar máximo, densidade de Λ_ν(I∩I*) na norma ν, operador de Tomita fechado e seus domínios, identificação modular/KMS, traço, interface geral de peso operatorial/predual, Three Locks/H1–H3, física, contrato consumido pelo gate e runtime integral. Não se deduz fidelidade de uma representação completada apenas do nome `scalarGNSAmbientAction`; o que foi provado aqui é a injetividade da inscrição e o entrelaçamento indicado.

**Custódia e integração: distinção temporal.** `gns_draft_status.json` congelado tem SHA `{V['status_sha256']}`; seu rótulo de ausência de revisão é histórico, anterior a este parecer, e não foi editado por mim. A custódia precedente `modular_domain_custody.json`, SHA `{V['custody_sha256']}`, corresponde ao parecer modular selado `{V['previous_modular_review_sha256']}`, que permaneceu intacto. Seus **84 registros / 67 controles / 6281 Audit** e working `{V['historical_custody_counts']['working_sha256']}` pertencem à etapa modular anterior. Não foram usados como prova integrada dos três módulos GNS.

Esta entrega encerra o escopo **DEV** autorizado, sem esperar integração futura. A cópia `um.py` foi apenas lida para hash na finalização: `{live_um}`. Não foi importada/executada; não se realizou nova inspeção integrada ou execução de controles nesta etapa. Eventual integração desses três módulos requer evidência separada e, se solicitada, adendo com backup imediato, antes de nova custódia. Todos os pareceres já selados, fontes autorais, originais, memórias e recorders permaneceram intocados. Todas as escritas ocorreram exclusivamente em `revisao/`.
'''
report=REVIEW/'REVIEW_GNS_ORBIT.md'
create(report,body.encode('utf-8'))
closure={'timestamp':DATE,'complete_DEV':True,'scope':'THREE_DEV_MODULES_14_TARGETS_AND_ROTA_ONLY',
    'findings_P0_P1_P2':[],'own_compiles_rc0':4,'own_audited_targets':14,'own_type_checks':14,
    'three_own_binaries_equal_author':True,'integration_reviewed':False,
    'report':str(report),'report_sha256':sha(report.read_bytes()),'report_bytes':report.stat().st_size,
    'route_sha256':V['route_sha256'],'draft_status_sha256':V['status_sha256'],
    'previous_modular_review_preserved':V['previous_modular_review_equals_custody'],
    'all_previous_reviews_preserved':V['previous_reviews_preserved'],
    'working_um_sha256_read_only':live_um,'author_monolith_recorders_tests_executed':False}
create(RUN/'closure_dev.json',json.dumps(closure,ensure_ascii=False,indent=2).encode('utf-8'))
print(json.dumps(closure,ensure_ascii=False,indent=2))
