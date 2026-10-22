"""Create a new review; previous reviews are never modified."""
from pathlib import Path
import datetime,hashlib,json
R=Path(__file__).resolve().parent;ROOT=R.parent
RUN=Path((R/'gns_representation_latest_run.txt').read_text(encoding='utf-8'))
M=json.loads((RUN/'manifest.json').read_bytes());V=json.loads((RUN/'verification_dev.json').read_bytes())
PREV=Path(M['previous_run']);PM=json.loads((PREV/'manifest.json').read_bytes())
def link(p,label=None):return '['+(label or p.name)+'](<'+p.as_posix()+'>)'
date=datetime.datetime.now().astimezone().isoformat(timespec='seconds')
counts={'OperatorFieldAlgebra':5,'ScalarGNSCompletion':9,'DualOrbitRepresentation':2,'ReducingStarRepresentation':1,'ScalarGNSRepresentation':4}
table='\n'.join('| '+n+' | '+str(counts[n])+' | `'+r['source_sha256']+'` | `'+r['own_binary_sha256']+'` |' for n,r in V['records'].items())
logtable='\n'.join('| '+n+' | '+Path(r['author_log']).name+' | `'+r['author_log_sha256']+'` |' for n,r in V['records'].items())
docsha=V['documents_current_sha256']
text=f'''# Revisão independente — representação GNS no fecho do ideal finito

Estrato DEV encerrado em {date}. Integração e controles finais ainda aguardam o estrato de inspeção abaixo; não são resultados de recompilação própria.

**Parecer matemático delimitado: nenhum achado P0, P1 ou P2 nas cinco fontes finais.** [REAL — leitura integral e recompilação independente] Os 21 alvos novos elaboram, o auditor cumulativo confere seus tipos e axiomas, e a construção entrega uma representação complexa unital fiel da mesma álgebra N sobre o Hilbert H_I, fecho da imagem do ideal I. Não há premissa residual de fidelidade, densidade do domínio máximo ou continuidade forte da operação adjunta.

Este parecer acrescenta **cinco módulos/21 alvos** ao pacote anterior de três módulos/14 alvos. O status autoral de oito módulos/35 alvos é cumulativo. Os três anteriores foram reutilizados a partir da árvore independente aprovada em {link(R/'REVIEW_GNS_ORBIT.md')}, que permanece intocada; não foram recompilados nesta etapa. Hash lido desse parecer: `{V['sealed_orbit_review_sha256']}`.

## Enunciados e composição conferidos

- **OperatorFieldAlgebra.lean:12–69.** Constantes, soma, produto, escala complexa e adjunta são compatíveis com o lift. A ordem do produto é F(s)G(s), aplicada como F(s)(G(s)v). As igualdades em L² usam interseções finitas de conjuntos de medida total para cada vetor fixado, sem uniformização a.e. não enumerável. O lema da adjunta (57–69) recebe **duas famílias já fortemente contínuas e uniformemente limitadas**, com G(s)=F(s)*; a prova por produtos internos integrados não constrói continuidade forte de F* a partir da de F. Na aplicação dual, a segunda família é a família efetiva de A*, e a igualdade vem de `map_star`.
- **ScalarGNSCompletion.lean:13–60.** H_I é literalmente o submódulo `(scalarGNSLinear P).range.topologicalClosure` de L²(ℝ,L²(ℝ,TowerHilbert P)), com as duas medidas de Lebesgue herdadas. A completude vem do fecho em um Hilbert; a inscrição é a mesma aplicação linear com contradomínio restrito. A ação preserva primeiro a imagem, pois BA pertence ao mesmo ideal esquerdo I, e depois o fecho pela continuidade do operador ambiente. A norma da restrição é ≤‖B‖ e o entrelaçamento é π(B)Λ(A)=Λ(BA). Trata-se da norma induzida pela inscrição/ν, não de uma afirmação de que a inscrição seja limitada na norma de operador herdada por I.
- **DualOrbitRepresentation.lean:14–37.** O campo θ_s(A) define um `StarAlgHom` unital sobre o L² exterior. Soma, produto e escala usam as leis da mesma `dualAmbient`; a unidade é o lift do campo constante identidade. A operação `star` é a adjunta Mathlib do CLM no Hilbert exterior. A representação ambiente está definida em todos os operadores limitados do Hilbert regular; a composição final restringe sua entrada ao subtipo N.
- **ReducingStarRepresentation.lean:14–53.** A restrição genérica exige um submódulo completo e invariância para **todo** elemento da álgebra, portanto também para as adjuntas. Essa hipótese basta para a identidade ⟨w,ρ(a*)v⟩=⟨ρ(a)w,v⟩ na restrição. Não se deduz redutibilidade de mera invariância por um único operador. No módulo final, completude e invariância são fornecidas pelos resultados concretos anteriores; não ficam como premissas novas.
- **ScalarGNSRepresentation.lean:14–26.** `scalarGNSRepresentation P` compõe a inclusão de N com a representação ambiente e a restrição ao mesmo `scalarGNSSubspace P`. A aplicação subjacente é a já chamada `scalarGNSAction`, como verifica a elaboração do entrelaçamento na prova seguinte. `scalarGNSEmbedding_denseRange` demonstra agora explicitamente a densidade, via fatoração pela imagem e inclusão no fecho; não pressupõe a continuidade da inscrição na norma de operador de I.
- **ScalarGNSRepresentation.lean:28–65.** Fidelidade: π(B)=0 implica Λ(BA)=Λ(0) para todo A∈I; injetividade da inscrição dá BA=0 na representação regular original. Para h>0, X_h pertence a I e BX_h→B fortemente, lema herdado com os mesmos P e B. Para cada vetor v, a família é eventualmente zero no filtro `𝓝[>] (0:ℝ)`, que é não trivial, e a unicidade do limite no Hilbert força Bv=0. `ext1 v` mantém a igualdade de vetores L², sem presumir representantes pontuais contínuos. O caso reverso vem de `map_zero`; a injetividade usa B−C. O enunciado final só recebe P, e a equivalência de nulidade recebe adicionalmente B∈N.

Nos tipos auditados não há hipótese de separabilidade de H, vetor η fixado pela ação dual, identificação I=n_ν, GNS de domínio máximo, nem fidelidade da representação dada como hipótese. Não foi introduzida conversão de um valor infinito por `toReal` nestas cinco fontes. A identidade de norma herdada conserva sua tipagem: `ENNReal.ofReal ‖Λ(A)‖² = ν(A*A)`.

## Evidência própria e pins

Primeiro estrato: {link(PREV/'compilation.json', 'quatro recompilações + auditor de 17 alvos')}. Segundo estrato: {link(RUN/'compilation.json', 'quinto módulo + auditor cumulativo de 21 alvos')}. Resultado: **cinco módulos e dois auditores, sete processos rc0**, sem warnings nas cinco fontes finais. O auditor cumulativo contém **22 `#check`** (inclui o abreviador `ScalarGNSHilbert`) e **21 `#print axioms`**; cada alvo depende somente de `propext`, `Classical.choice`, `Quot.sound`. Conjuntos exatos comparados ao status e às declarações das fontes.

| Fonte DEV | Alvos | SHA256 fonte lida | SHA256 .olean próprio = autoral |
|---|---:|---|---|
{table}

| Fonte | Log final autoral conferido | SHA256 JSON do log |
|---|---|---|
{logtable}

Os logs autorais acima são **evidência inspecionada**, distinta das execuções próprias. Foram conferidos rc0, fonte inalterada durante a compilação, hash do binário presente, stdout/stderr e correspondência com o status congelado. Os cinco binários independentes são byte a byte iguais aos autorais finais. Todos esses vínculos, hashes dos streams e ausência de warnings constam de {link(RUN/'verification_dev.json')}. Status congelado de oito módulos/35 alvos: `{V['status_sha256']}`.

Auditor cumulativo: fonte `{V['own_auditor_source_sha256']}`; binário `{V['own_auditor_binary_sha256']}`; stdout `{V['own_auditor_stdout_sha256']}`. A saída impressa foi lida, incluindo o `StarAlgHom` final e os tipos de densidade/fidelidade sem hipóteses extras.

**Proveniência e limite binário.** {link(PREV/'manifest.json', 'Manifesto dos quatro módulos')} pina 377 dependências de projeto vindas das árvores independentes anteriores, incluindo os três GNS já revisados. O quinto reutiliza esses 377 e os quatro novos binários próprios: 381 módulos herdados, materializados numa única árvore própria para a resolução dos imports. {link(RUN/'manifest.json', 'Manifesto do quinto')} registra os hashes, fontes congeladas, caminhos, versão e `LEAN_PATH` efetivo; nenhum build de projeto do autor entrou no `LEAN_PATH`. Pacotes e compilador foram reutilizados somente para leitura, sem reconstrução da biblioteca. Compilador: `{M['lean_version']}`; SHA256 `{V['compiler_sha256']}`.

Permanece a exceção histórica explícita `DualSemifiniteIdeal`: fonte própria congelada `6af7365befd3125fa1b8a9a03f26bcd96d723659d035d2b52e73a8ced09b70b3`, binário próprio `6a242f29df8816cf7e741cb043f6c24f88fb9e844fc60f90d3bce25a4c1f26df`; fonte viva `f1c93aa724c9eb82df3d1ec74d040cdab6a78f0b57f51b224f60656669128da3`. O congelamento conferiu a diferença literal exclusivamente no comentário já objeto de errata, com provas intactas. Não se afirma identidade binária de toda a cadeia herdada nem se revogam limitações de revisões anteriores. `RegularScalarWeightCertificate`, cujo parecer anterior registrou divergência binária, não pertence a este fecho de imports.

Uma tentativa própria inicial do quinto falhou antes da elaboração por resolução de imports: a primeira entrada `LEAN_PATH` continha o prefixo TGLV350, mas não `ScalarGNSCompletion.olean`; a segunda entrada não supriu esse prefixo. Evidência preservada em {link(R/'gns_representation5_independent_20260912_073201_614035'/'compilation.json')}. Corrigiu-se apenas a montagem da árvore própria, copiando os binários já pinados; a nova execução acima passou. Essa falha de ambiente não é ocultada nem contada entre os sete rc0. Nenhuma fonte Lean foi editada.

## Documentação e fronteira

A minuta {link(ROOT/'MINUTA_REPRESENTACAO_GNS.md')} foi lida integralmente: SHA256 `{docsha['MINUTA_REPRESENTACAO_GNS.md']}`. As afirmações nas linhas 5–25 correspondem à inscrição anterior e às cinco fontes finais: completude do fecho de I, densidade da inscrição, ação limitada, *-homomorfismo unital e fidelidade pelo aproximante forte. A fidelidade que era apenas anunciada antes do quinto rc0 agora tem prova conferida. Os placeholders de contagens são destinados ao registro integrado; não foram tomados por resultados já medidos. Os scripts de registro/custódia são inspecionados estaticamente, nunca executados pelo revisor; sua versão final e a nota posterior serão delimitadas no adendo integrado.

**Limites mantidos [OPEN / fora deste parecer]:** identificar I com n_ν máximo ou estender a inscrição a esse domínio; densidade GNS de Λ(I∩I*); normalidade da representação; construção/fechabilidade de Tomita, identificação modular e KMS; traço canônico e interfaces operatoriais/preduais; Three Locks/H1–H3/física, consumo do certificado pelo gate e runtime integral. A norma ≤‖B‖ de cada operador da representação não é um teorema de normalidade de π. A densidade de Λ(I) no fecho que a define não resolve as outras densidades.

Desenvolvimentos posteriores de limites fortes, aproximação/densidade por I∩I* e gráfico inicial não foram lidos, congelados ou compilados nesta revisão. Uma nota autoral separada sobre eles não os inclui nos 21 alvos revisados ou no pacote cumulativo de 35. Pareceres anteriores, originais, fontes autorais, memórias e logs permanecem intocados. Sem execução/importação de monólito, recorders, verifiers ou testes autorais, e sem aprovação de QG/gate/runtime.
'''
p=R/'REVIEW_GNS_REPRESENTATION.md';assert not p.exists()
b=text.encode('utf-8');tmp=p.with_name(p.name+'.tmp');tmp.write_bytes(b);assert tmp.read_bytes()==b and len(b)>500;tmp.replace(p)
print(json.dumps({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'status':'DEV_COMPLETE_INTEGRATED_INSPECTION_PENDING'}))
