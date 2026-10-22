"""Prepare a recorder with the same byte-preserving custody protocol as the prior stage."""
import ast
from pathlib import Path

root = Path(__file__).resolve().parent
text = (root / 'record_form_transport_progress.py').read_text(encoding='utf-8')
text = text.replace('Record verified transport and faithfulness laws without promoting them to a trace.',
                    'Record proved order normality of dual form evaluations, not a completed trace.')
text = text.replace('TETELESTAI_V350_DUAL_FORM_TRANSPORT_20260911',
                    'TETELESTAI_V350_DUAL_FORM_NORMALITY_20260911')
text = text.replace("MODULES = ['DualFormTransport', 'DualFormFaithfulness']",
                    "MODULES = ['DualCutNormality', 'DualFormNormality']")
text = text.replace('REVIEW_DUAL_FORM_TRANSPORT.md', 'REVIEW_DUAL_FORM_NORMALITY.md')
text = text.replace("ROOT / 'closed_form_custody.json'", "ROOT / 'form_transport_custody.json'")
start = text.index("for name in ('dualQuadraticIntegral_bimodule'")
end = text.index("    target = 'TGLV350.Regular.' + name", start)
text = text[:start] + '''for name in ('intervalIntegral_tendsto_of_uniform', 'dualRealQuadratic_continuous',
             'dualRealQuadratic_mono', 'dualAmbient_tendsto_strong',
             'dualRealQuadratic_uniform_on_compact', 'dualWeightCut_tendsto_quadratic',
             'dualQuadraticIntegral_of_monotone_strong_limit',
             'dualQuadraticIntegral_preserves_positive_isLUB',
             'dualQuadraticIntegral_preserves_internal_isLUB',
             'regularDualForm_preserves_internal_isLUB'):
''' + text[end:]
text = text.replace('RELATORIO_TRANSPORTE_E_FIDELIDADE_DUAL.md', 'RELATORIO_NORMALIDADE_DUAL.md')
start = text.index("report = f'''")
end = text.index("write_atomic(report_path, report.encode('utf-8'))", start)
text = text[:start] + '''report = f\'''# Normalidade da família de formas duais

{DATE}. [REAL — Lean incremental em cópia, com revisão independente delimitada.]

A integral dual preserva agora supremos positivos dirigidos na mesma álgebra
regular. A prova aceita redes não enumeráveis e o supremo **interno** à álgebra;
convergência forte e normalidade não são hipóteses do enunciado final.
O peso com valores na base, sua semifinitude e o traço canônico permanecem abertos.

## Enunciado entregue

Para qualquer tipo de índices ι não vazio, preordenado e dirigido, qualquer rede
A_i≥0 monótona no core regular e qualquer S que seja seu supremo interno, foi provado,
para todo vetor v da mesma representação:

    q_S(v) = sup_i q_(A_i)(v).

`regularDualForm_preserves_internal_isLUB` tem explicitamente a álgebra
`regularCoreAlgebra P` dos módulos anteriores. Seu enunciado não exige que a rede
seja enumerável, não troca um supremo interno por um supremo ambiente presumido e
aceita valores infinitos. A existência de um supremo para redes positivas limitadas
em ordem é fornecida pelo módulo `RegularNormality` já construído; este incremento
prova a preservação desse supremo pela família de avaliações q.

## Como a prova fecha

1. Conjugação pela implementação dual preserva convergência forte em qualquer filtro.
   As avaliações reais são contínuas no parâmetro s e crescem com A.
2. O teorema de Dini da mathlib, cuja assinatura aceita um preordenado arbitrário,
   fornece convergência uniforme em cada compacto. A estimativa da integral pelo
   comprimento do intervalo transforma isso em convergência de cada corte real.
3. Cada corte normalizado está abaixo de q_(A_i)(v). Passando ao limite da rede,
   o corte de S fica abaixo de sup_i q_(A_i)(v). O supremo dos cortes é q_S(v),
   pelo teorema de exaustão já construído. A desigualdade inversa vem da monotonicidade.
   Não se invoca um teorema de convergência monótona de sequências para uma rede arbitrária.
4. O limite forte é construído pelo teorema de operadores positivos monótonos da v350.
   Sua unicidade como supremo o identifica com S. O fechamento da álgebra de von Neumann
   e a equivalência dos supremos internos/ambientes, já provados em `RegularNormality`,
   eliminam a hipótese de convergência forte no enunciado final.

## Alcance no caminho do gate

[REAL] Normalidade **em ordem da família de formas**: preservação de todos os supremos
positivos dirigidos que existem no core regular. Ela se soma à aditividade positiva,
homogeneidade, fechamento, bimodularidade e fidelidade das avaliações já demonstrados.

[OPEN] Identificar essas formas com valores no cone ampliado da **base**; representação
espectral/pontos fixos; domínio/ideal semifinito do peso; peso da base com o grupo modular
correto; gerador afiliado da implementação regular; perturbação que constrói o traço
fiel, normal e semifinito e sua lei τ∘θ_s=e⁻ˢτ. Não há promoção das avaliações a um peso
com valores na base enquanto essa identificação permanecer ausente.

Three Locks no mesmo modelo, H1/H2/H3 físicos compatíveis, setor quântico interagente,
BRST/QME/anomalias/UV, contrato dependente ampliado e runtime monolítico continuam abertos.
Nenhuma das seis flags ainda abertas foi quitada neste incremento. O corpo Python e
o gate permanecem iguais por AST ao estrato anterior; mudaram somente os dois novos
módulos embutidos e as raízes que os importam e auditam.

## Evidência

{len(build['records'])} registros Lean integrados válidos; {tests['passed']} controles
Python aprovados; {tests['axiom_report_entries']} declarações distintas no Audit,
com axiomas restritos ao trio. {integration['embedded_files']} arquivos embutidos.

Base SHA-256 `{integration['base_sha256']}`.
Cópia SHA-256 `{integration['working_sha256']}`.

| Módulo integrado | SHA-256 lido |
|---|---|
{rows}

[Revisão independente](<{review.as_posix()}>). O parecer separa recompilação independente
dos módulos/auditor próprio de inspeção das fontes, hashes e logs da integração do autor.
Tentativas de elaboração que falharam foram preservadas; não integram a evidência aceita.
O controle novo impede que normalidade da família seja contada como construção de peso
com valores na base, traço canônico ou canto de Three Locks.

O original foi conferido por hash e permanece intacto. Runtime integral ainda não executado.
Objetivo integral ativo; nenhum novo selo, transposição canônica, publicação ou confirmação física.
\'''
''' + text[end:]
start = text.index("note = f'''")
end = text.index('surfaces = ', start)
text = text[:start] + '''note = f\'''

## {MARKER} — {DATE}

[REAL — Lean em cópia] `DualCutNormality` e `DualFormNormality`:
q_S(v)=sup_i q_(A_i)(v) para toda rede positiva monótona, em preordenado dirigido
não vazio, com S seu supremo interno ao mesmo core regular. Não há hipótese de
enumerabilidade, normalidade ou convergência forte no enunciado final.
Dini em compactos + limites de cortes + exaustão provam a igualdade; o limite forte
é construído e identificado com o supremo interno usando os módulos anteriores.
Trata-se de normalidade em ordem das avaliações, ainda sem peso com valores na base.

{len(build['records'])} registros Lean, {tests['passed']} controles,
{tests['axiom_report_entries']} declarações distintas no Audit, axiomas no trio.
Base `{integration['base_sha256']}`; cópia `{integration['working_sha256']}`.
Corpo Python/gate inalterado por AST em relação ao estrato anterior.
[Relatório](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

[OPEN] Cone ampliado da base/representação espectral/pontos fixos; domínio e
semifinitude do peso; estado modular da base, gerador afiliado, perturbação e traço;
Three Locks, H1/H2/H3, interações/BRST/QME/anomalias/UV, contrato ampliado e runtime
integral. Nenhuma flag de core/canto/H1/H2/H3/testemunha total foi quitada nesta etapa.
Objetivo integral ativo; nenhum novo selo, transposição ou confirmação física.
\'''
''' + text[end:]
text = text.replace("'ROTA_APOS_CORTES_DUAIS.md', 'RELATORIO_FORMA_DUAL_FECHADA.md')",
                    "'ROTA_APOS_CORTES_DUAIS.md', 'RELATORIO_TRANSPORTE_E_FIDELIDADE_DUAL.md')")
text = text.replace("ROOT / 'form_transport_custody.json', json.dumps(custody",
                    "ROOT / 'form_normality_custody.json', json.dumps(custody")
ast.parse(text)
target = root / 'record_form_normality_progress.py'
assert not target.exists()
raw = text.encode('utf-8')
temporary = target.with_suffix('.py.tmp')
with temporary.open('xb') as handle:
    handle.write(raw)
assert temporary.read_bytes() == raw
temporary.replace(target)
print(str(target))
