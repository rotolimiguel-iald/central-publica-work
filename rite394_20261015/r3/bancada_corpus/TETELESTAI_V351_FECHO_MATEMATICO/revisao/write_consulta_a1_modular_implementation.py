from pathlib import Path
from datetime import datetime
import hashlib
import json
import os
import re

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO')
OUT = ROOT / 'revisao'
ML = ROOT.parent / 'TETELESTAI_V350_KERNEL_20260911/r/tgl_kernel/.lake/packages/mathlib/Mathlib'
STAMP = datetime.now().astimezone()
NAME = 'CONSULTA_A1_IMPLEMENTACAO_MODULAR_MESMO_GNS'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def atomic(p, data):
    assert p.parent == OUT
    if p.exists():
        old = p.read_bytes()
        backup = p.with_name(p.name + '.bak_' + STAMP.strftime('%Y%m%d_%H%M%S_%f'))
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    tmp = p.with_name(p.name + '.tmp_' + STAMP.strftime('%Y%m%d_%H%M%S_%f'))
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data
    os.replace(tmp, p)

selection = {
 'V350ScalarWeightTomitaIdentification': ['scalarClosedTomita_graph_eq_weight','scalarClosedTomita_extends_weight_star'],
 'V350ScalarTomitaSelfAdjoint': ['scalarTomitaSquare_selfadjoint','scalarTomitaSquare_zero_only'],
 'V350ScalarTomitaResolvent': ['scalarTomitaResolvent_equation','scalarTomitaResolvent_inverse','scalarTomitaResolvent_injective','scalarTomitaResolvent_nonneg','scalarTomitaResolvent_le_one','scalarTomitaResolvent_graph'],
 'V350ScalarTomitaPolarFactor': ['scalarTomitaPolarFactor','scalarTomitaPolarFactor_factorization'],
 'V350ScalarTomitaPolarInvolution': ['scalarTomitaPolar_conjugate_resolvent','scalarTomitaPolar_conjugate_complement','scalarTomitaPolarFactor_involutive'],
 'V350AntiunitaryPositiveConjugation': ['antiunitaryConjugate','antiunitaryConjugate_mul','antiunitaryConjugate_sqrt'],
 'V350BoundedInjectivePolar': ['boundedMapModulus','boundedInjectivePolar','boundedInjectivePolar_modulus'],
 'V350PositiveRootIntertwining': ['real_cfc_intertwines','positive_sqrt_intertwines'],
 'V350ScaledPositiveResolvent': ['scaledResolventDenominator','scaledResolventDenominator_positive','scaledPositiveResolvent','scaledPositiveResolvent_complement','scaledPositiveResolvent_le_one'],
 'V350MatrixUnitResolventScaling': ['matrixUnit_resolvent_denominator_identity','matrixUnit_resolvent_right_scaling'],
 'V350MatrixUnitRightSquare': ['matrixUnitRightGNS_star_reverse','matrixUnit_TomitaSquare_right_scaling'],
 'V350ScalarRegularRightPolar': ['scalarTomitaResolvent_regular_right_commutes','scalarTomitaPolar_conjugate_regular_right'],
 'V350ScalarRegularPolarCommutation': ['regularRightGNS_commutes_left','scalarTomitaPolar_regular_generator'],
 'V350ScalarRegularRightContinuity': ['scalarGNSRegular_strongly_continuous','regularRightGNS_strongly_continuous'],
 'V350ScalarRegularRightGNS': ['regularRightAmbient','regularRightGNS_intertwines','regularRightGNS_mul','regularRightGNS_star','regularRightGNS_unitary'],
 'V350MatrixUnitPolarCommutation': ['homogeneousRightGNS_commutes_left','matrixUnit_polar_conjugate_generator'],
 'V350HomogeneousRightData': ['HomogeneousRightData','homogeneousRightAmbient','matrixUnitRightData'],
 'V350ScalarHomogeneousRightOrbit': ['scalarOrbit_right_homogeneous','scalarWeight_right_homogeneous_finite','scalarOrbit_right_matrixUnit'],
 'V350ScalarHomogeneousRightGNS': ['homogeneousRightGNS_intertwines','homogeneousRightGNS_adjoint','scalarWeight_right_adjoint_pairing'],
 'V350RegularTowerRepresentation': ['regularUnitary','regular_covariance','regular_covariance_on_factor'],
 'V350RegularDualAction': ['dualAmbient_regular'],
 'V350L2CharacterMultiplier': ['characterPhase'],
 'ModularFlowLevel': ['modularPhase'],
 'ModularFlowAlgebra': ['modularConjugation_local'],
 'ModularFlowSpectrum': ['localEigenvalue','flowLevel_single','delta_eigenvector','localEigenvectors_total','modularFlow_spectral_unique'],
 'ModularPower': ['deltaImaginaryPower','deltaImaginaryPower_spectral'],
 'V350LevelExpectationStrongLimit': ['represented_levelExpectation_strong_tendsto'],
 'V350ScalarGNSGeneratorTransport': ['scalarGNS_commutation_from_generators'],
 'V350ScalarRightRegularization': ['scalarRightRegularization_embedding','scalarRightRegularization_tendsto','scalarRegularizationVector','scalarRightRegularization_vector'],
 'V350ScalarRightAdjointPair': ['ScalarRightAdjointPair','scalarRightAdjointPair_maximal'],
 'V350RegularFiniteWeight': ['regularAverage_dualQuadraticIntegral'],
 'V350ScalarWeightCompletion': ['scalarWeightOrbit_rightRegularization_tendsto','scalarWeight_completion_eq','scalarWeightGNSEmbedding'],
}
manifest_path = ROOT / 'DEPENDENCIAS_A1_MARCO_BASE.json'
manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
entries = {x['module']: x for x in manifest['entries']}
pins = []
loc = {}

def extract(p, names):
    raw = p.read_bytes()
    txt = raw.decode('utf-8-sig')
    decls = []
    for n in names:
        pat = r'(?m)^(?:(?:private|protected|noncomputable)\s+)*(?:theorem|lemma|def|abbrev|structure)\s+' + re.escape(n) + r'(?=\s|[({:\[])'
        match = re.search(pat, txt)
        if not match:
            raise ValueError(f'Declaration not located: {p.name}:{n}')
        tail = txt[match.start():]
        ends = [i for i in [tail.find(' :=', 1), tail.find(' where', 1)] if i >= 0]
        excerpt = tail[:min(ends)] if ends else tail.split('\n\n', 1)[0]
        line = txt[:match.start()].count('\n') + 1
        item = {'name': n, 'line': line, 'statement': excerpt}
        decls.append(item)
        loc[n] = (p, line)
    return {'path': str(p), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(), 'declarations': decls}

for stem, names in selection.items():
    p = ROOT / 'kernel/TGLExt' / (stem + '.lean')
    entry = extract(p, names)
    inherited = entries.get('TGLExt.' + stem)
    if inherited:
        obj = Path(inherited['object'])
        entry['manifest_source_match'] = entry['sha256'] == inherited['source_sha256']
        entry['object'] = {'path': str(obj), 'sha256': sha(obj), 'manifest_match': sha(obj) == inherited['object_sha256']}
        entry['evidence_scope'] = 'Leitura de fonte e pins herdados; nenhuma compilação nesta consulta.'
    else:
        entry['evidence_scope'] = 'Leitura da fonte; não consta neste manifesto específico, sem nova certificação de build.'
    pins.append(entry)

for rel, names in {
 'Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unital.lean': ['cfc_mul','cfc_star','cfc_comp'],
 'Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unique.lean': ['StarAlgHom.map_cfc'],
 'Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Isometric.lean': ['norm_cfc_le'],
 'Analysis/InnerProductSpace/Adjoint.lean': ['orthogonal_range','ker_self_comp_adjoint'],
}.items():
    entry = extract(ML / rel, names)
    entry['evidence_scope'] = 'API local lida, trechos pertinentes; não recompilada.'
    pins.append(entry)

def link(name):
    p, line = loc[name]
    return f'[{name}](<{p.as_posix()}:{line}>)'

key = [
 ('Mesmo peso e gráfico original', 'scalarClosedTomita_graph_eq_weight'),
 ('Mesmo Δ e resolvente, domínio incluído', 'scalarTomitaResolvent_graph'),
 ('Complemento transportado pelo J original', 'scalarTomitaPolar_conjugate_resolvent'),
 ('Polar linear de mapa injetivo de imagem densa', 'boundedInjectivePolar'),
 ('CFC entre dois operadores, sem inversão do entrelaçador', 'real_cfc_intertwines'),
 ('Escala matricial já paga', 'matrixUnit_resolvent_right_scaling'),
 ('Denominador estritamente positivo', 'scaledResolventDenominator_positive'),
 ('Resolvente comuta com direita regular', 'scalarTomitaResolvent_regular_right_commutes'),
 ('J original troca esquerda/direita matricial', 'matrixUnit_polar_conjugate_generator'),
 ('J original troca esquerda/direita regular', 'scalarTomitaPolar_regular_generator'),
 ('Níveis finitos aproximam toda base no mesmo GNS', 'represented_levelExpectation_strong_tendsto'),
 ('Geração concreta, hgen descarregada', 'scalarGNS_commutation_from_generators'),
 ('Sinal da covariância regular', 'regular_covariance_on_factor'),
 ('Autovetores totais somente no Hilbert da torre', 'localEigenvectors_total'),
 ('Potências imaginárias existentes somente da torre', 'deltaImaginaryPower_spectral'),
]
table = '\n'.join(f'| {role} | {link(n)} |' for role, n in key)
hash_table = '\n'.join(f"| `{Path(e['path']).name}` | `{e['sha256']}` |" for e in pins if Path(e['path']).stem in {
 'V350ScalarTomitaResolvent','V350ScalarTomitaPolarInvolution','V350BoundedInjectivePolar','V350PositiveRootIntertwining','V350MatrixUnitResolventScaling'})

text = r'''# Consulta A1 — potências imaginárias do Tomita do mesmo peso

Data: @DATE@. Estatuto: **[DERIVED — proposta matemática, sem novo Lean]**.

A rota amortecida proposta nesta continuação é válida e mais econômica que começar por uma nova descrição completa de autovetores do GNS. Ela usa o resolvente do **Δν=scalarTomitaSquare P=S†S original**, constrói suas fases por CFC contínuo e permite transportar a escala matricial já demonstrada. O passo seguinte pode identificar a ação de Δν^{it} em toda π(N), sem predual abstrato novo, sem Stone/PVM geral e sem assumir Jπ(N)J=π(N)'. A igualdade literal entre duas unitárias implementadoras merece um enunciado separado; igualdade de suas conjugações não a prova.

Nenhum módulo foi compilado, criado ou modificado nesta consulta. Foram lidos fornecedores delimitados, com pins no JSON acompanhante. Builds anteriores são herdados; esta leitura não é uma nova auditoria de axiomas. A1(b) permanece **[OPEN]**.

## 1. Objetos e sinal

Escrevo Γ(a)=scalarWeightGNSEmbedding P a, Hν=ScalarGNSHilbert P, J=scalarTomitaPolarFactor P, Δ=scalarTomitaSquare P e T=scalarTomitaResolvent P. Uso λ_t=regularUnitary P t para a unitária do core; ela atua em **H_reg**, enquanto L_t=πν(λ_t) e R_t=regularRightGNS P t atuam em **Hν**.

As definições e os entrelaçamentos existentes dão

\[
R_t\Gamma(a)=\Gamma(a\lambda_t),\qquad
V_t:=L_tR_{-t}=L_tJ L_tJ^{-1},\qquad
V_t\Gamma(a)=\Gamma(\lambda_ta\lambda_{-t}).
\]

O sinal na direita é **−t**. `characterPhase s t=exp(−i s t)`, enquanto `modularPhase t c=exp(i t c)`. Na realização ambiental L²(s,L²(x,H_torre)), o produto da ação esquerda de λ_t com a direita de λ_{−t} cancela o caráter externo e as translações internas: resta a amplificação, duas vezes, de `modularFlowCLM P t`. Esta última identidade de operadores é uma consequência algébrica a empacotar; não foi localizada como um teorema pronto. Não troca Hν pelo Hilbert da torre.

Para unidades matriciais, r_ij=w_i/w_j>0, ω_ij=log r_ij; o fluxo candidato na base é **+it log r_ij**. A translação s−ω_ij da fórmula `scalarOrbit_right_matrixUnit` é compatível com esse sinal, não o oposto.

V_t já tem os fornecedores de grupo, unitariedade, continuidade forte e implementação da ação. Essas propriedades, isoladas, ainda não o identificam com Δ^{it}.

## 2. Construção amortecida: prova e condições realmente necessárias

Assuma no lema genérico H complexo completo, T limitado, 0≤T≤1, `Injective T` e `Injective (1−T)`. Na aplicação, T é o resolvente original. A primeira injetividade está pronta; a segunda segue de JTJ^{-1}=1−T e da primeira, sem gap.

Ponha b(x)=x(1−x), K=b(T). K≥0, é injetivo e tem imagem densa: o produto dos dois fatores injetivos é injetivo; K auto-adjunto implica Ran(K)^⊥=ker K. **Injetividade de um operador limitado arbitrário, sozinha, não implica imagem densa.**

Em 0<x<1, defina

\[
g_t(x)=b(x)\exp\bigl(it\log((1-x)/x)\bigr),\qquad g_t(0)=g_t(1)=0.
\]

|g_t(x)|=b(x) prova a continuidade nas duas extremidades, apesar de a fase sem amortecimento não ter limite ali. Para reutilizar literalmente `real_cfc_intertwines`, que exige **Continuous f em ℝ**, estenda Re g_t e Im g_t continuamente por zero fora [0,1]; não passe apenas uma prova `ContinuousOn` a essa API. Construa C_t pela CFC complexa, ou pela soma da CFC real de Re g_t e i vezes a de Im g_t.

As identidades pontuais no espectro dão

\[
C_t^*C_t=C_tC_t^*=K^2,\quad C_t^*=C_{-t},\quad
C_sC_t=K C_{s+t},\quad C_0=K.
\]

Aqui é necessário registrar **também C_t C_t^*=K²**, ou normalidade de C_t: dela vem ker C_t*=0 e a imagem densa de C_t. Assim `boundedInjectivePolar C_t hi hd` se aplica efetivamente H→H. Seu módulo é √(C_t*C_t)=K por positividade e unicidade da raiz. A identidade fornecida é

\[
U_tK=C_t.
\]

O argumento não usa K^{-1} limitado. A unicidade por Ran K densa dá comutação de U_t com funções contínuas de T. A igualdade de grupo é verificada sobre Ran K² usando C_sC_t=K C_{s+t}, e estendida por densidade. U_0=I e U_t*=U_{−t} seguem do mesmo modo. Continuidade forte: t↦g_t é contínua uniformemente em [0,1] (controle b nas pontas e continuidade uniforme no interior); logo t↦C_t é contínua em norma. U_tK=C_t dá continuidade em Ran K, estendida a H por ||U_t||=1. Não resulta continuidade de U em norma.

**Identidade intrínseca com Δ.** T=(I+Δ)^{-1} não foi escolhido por covariância: é o resolvente do S†S previamente construído, com igualdade de grafos. A igualdade U_t b(T)=g_t(T), com b(T) de imagem densa, caracteriza unicamente a fase funcional exp(it log Δ). Isso fornece uma definição concreta e verificável de Δ^{it} via seu resolvente; não basta definir U como um grupo qualquer que preserve ν e atribuir-lhe o nome. Uma API geral de potências imaginárias de LinearPMap não foi localizada nesta busca limitada; a definição nova deve vir acompanhada dessa caracterização, grupo e continuidade.

## 3. Escala: o amortecimento também precisa ser transportado

A fonte existente já prova T R_ij=R_ij Q_r, com

\[
D_r=rI+(1-r)T,\qquad Q_r=T D_r^{-1},\qquad 0\le Q_r\le I.
\]

`scaledResolventDenominator_positive` paga a inversa **limitada de D_r**, para r>0. Isso não é inversão de R_ij, K, da raiz ou de Δ. Use as funções contínuas das duas partes de g_t em `real_cfc_intertwines`. Resultam K R_ij=R_ij b(Q_r) e C_t R_ij=R_ij g_t(Q_r).

Com E_r=r D_r^{-2}, as identidades escalares exatas são

\[
b(Q_r)=K E_r,\qquad g_t(Q_r)=r^{it} C_t E_r.
\]

E_r é limitado, invertível, comuta com T e com U_t; b(Q_r) tem imagem densa. Portanto

\[
U_t R_{ij} b(Q_r)=C_tR_{ij}
=R_{ij}g_t(Q_r)
=r^{it}R_{ij}U_t b(Q_r).
\]

A densidade cancela **à direita** e produz U_t R_ij=r_ij^{it}R_ij U_t. Não há que refazer root scaling; reaproveita-se seu fornecedor anterior de resolvente. Um cancelamento formal de b(T) por uma suposta inversa limitada seria inválido.

## 4. Do transporte à esquerda, e daí a TODO core

O fornecedor JTJ^{-1}=1−T, combinado com

\[
\overline{g_t(1-x)}=g_t(x),\quad b(1-x)=b(x),
\]

permite provar **JU_tJ^{-1}=U_t**, não U_{−t}: a antiunitariedade conjuga i e a troca T↔1−T inverte o log; os dois sinais se cancelam. Falta empacotar o transporte da CFC real por conjugação antiunitária. Pode-se construir o homomorfismo de *-álgebras sobre ℝ e usar `StarAlgHom.map_cfc`, ou adaptar a indução real já usada em `real_cfc_intertwines`. `antiunitaryConjugate_sqrt` sozinho não é uma API de todas as funções contínuas.

As identidades prontas com o **J original** são

\[
J\pi(e_{ij})J^{-1}=\sqrt{r_{ji}}R_{ji},\qquad
J\pi(\lambda_s)J^{-1}=R_{-s}.
\]

Consequentemente, a escala direita recém-obtida dá

\[
U_t\pi(e_{ij})U_{-t}=r_{ij}^{it}\pi(e_{ij}).
\]

Também U_t comuta com R_s pela comutação já provada de T com R_s e pela densidade de Ran K. Conjugando por J, U_t comuta com π(λ_s). Esses são precisamente os dois tipos de geradores da ação candidata.

Para passar a toda base, use `represented_levelExpectation_strong_tendsto`: os aproximantes matriciais possuem a cota já provada 4||a||. Para passar de base+λ a toda N, ponha W_t=V_{−t}U_t. A igualdade das ações nos geradores significa que W_t comuta com suas representações. Use `scalarGNS_commutation_from_generators`; a hipótese de geração é efetivamente descarregada nesse fornecedor. Conclui-se

\[
\boxed{\ U_t\pi(a)U_{-t}=\pi(\lambda_t a\lambda_{-t})\quad(a\in N).\ }
\]

**Este é o consumidor modular concreto:** depois de U estar caracterizado como Δν^{it}, a equação identifica σν com Ad λ na representação fiel do mesmo peso. Não depende de completar o predual, provar primeiro a inclusão inversa dos comutantes, assumir TT/KMS, nem construir um segundo GNS. Os lemas novos acima ainda precisam de provas Lean; esta nota não os aceita como já compilados.

## 5. Igualdade literal de implementadores e alternativa por autovetores

A caixa anterior não prova automaticamente U_t=V_t: ela só dá V_{−t}U_t∈π(N)'. Se o consumidor exigir a igualdade **de unitárias no Hν**, além da igualdade da automorfia, resta fixar essa ambiguidade em vetores cujas órbitas à esquerda sejam totais. Não usar Γ(1): a unidade não pertence ao ideal escalar finito.

Uma ponte concreta, sem reconstruir GNS, é a seguinte **[DERIVED, ainda a formalizar]**. Tome X_h=regularAverage P h, h>0. Primeiro prove a identidade integral forte da média direita com h^{-1}∫₀ʰ R_s ds e seu adjunto; daí obtenha o par `ScalarRightAdjointPair` com vetores Γ(X_h), Γ(X_h*). A igualdade X_h*=λ_{−h}X_h fornece sua finitude, por mudança de variável no intervalo; não presumir que o ideal esquerdo é fechado por estrela.

Então b_h=X_h*X_h está no ideal e é positivo. A multiplicação direita por b_h é Q_h=R_h R_h* (atenção à ordem da antirrepresentação direita), tem vetor ξ_h=Γ(b_h) e é auto-adjunta. `scalarRightAdjointPair_maximal` dá Fξ_h=ξ_h; a extensão da estrela pelo S original dá Sξ_h=ξ_h. Logo Δξ_h=ξ_h. Pela raiz positiva e S=JB, Jξ_h=ξ_h. As médias R_h e seus adjuntos convergem fortemente a I, logo Q_h→I e Q_hΓ(a)=π(a)ξ_h mostra que as órbitas π(N)ξ_h, tomadas conjuntamente, são totais.

Pelo CFC do resolvente, U_t fixa ξ_h (Tξ_h=ξ_h/2); V_t também fixa, pois b_h comuta com λ_t. Como W_t comuta com π(N), a totalidade anterior implica W_t=I. Assim se obtém a igualdade literal U_t=L_tR_{−t} **sem um campo de cyclicidade novo**.

A rota de autovetores é, portanto, viável mas não é a primeira recomendação após a proposta amortecida. Partindo de ξ_h, palavras nos R_ij e R_s ficam em D(Δ) e são autovetores com autovalor positivo produto dos r_ij, pelas leis completas de domínio já prontas. Sua totalidade pode ser provada usando Jξ_h=ξ_h, as fórmulas Jπ(gerador)J e geração concreta; não decorre simplesmente de `localEigenvectors_total`, cujo espaço é TowerHilbert. Obtida totalidade, seu span é core de Δ: aproximar (I+Δ)x por y_n no span e usar x_n=T y_n; então Δx_n=y_n−x_n. Nenhuma passagem de mera densidade Hilbert para densidade de gráfico é presumida.

## 6. Próximos enunciados propostos, em ordem de consumo

Nomes abaixo são **sugestões, não declarações existentes**:

1. `dampedResolventPhase_unitary`: sob 0≤T≤1 e injetividades dos extremos, construir U_t com U_t b(T)=g_t(T), grupo e continuidade forte.
2. `dampedResolventPhase_scaled_intertwining`: TR=RQ_r ⇒ U_tR=exp(it log r) RU_t. Registrar E_r e a densidade usada no cancelamento.
3. `dampedResolventPhase_antiunitary_flip`: JTJ^{-1}=1−T ⇒ JU_tJ^{-1}=U_t; nenhuma involução presumida antes de aplicar o J concreto.
4. `scalarDualWeight_modular_covariance`: especializar T/J originais e consumir os geradores/limites acima para a equação em toda π(N). Esse é o próximo pagamento de `regular_dual_weight_modular_implementation`.
5. Somente se a interface exigir a unitária literal: `regularAverage_right_adjoint_pair` → `regularAverageSquare_modular_fixed_total` → U_t=π(λ_t)R_{−t}.

O passo 4 identifica o fluxo modular do S†S do peso completo. Um teorema separado de condição KMS em faixa, uma perturbação que construa o traço e seu consumo A1 não foram demonstrados nesta consulta. Não há promoção de gate nem alegação de A1(b) pago.

## 7. Fornecedores locais efetivamente lidos

Nomes qualificados: os V350 abaixo estão em `TGLV350.Regular`, os módulos ModularFlowSpectrum/ModularPower em `ChatgptAudit`. Links trazem a linha exata; o JSON contém enunciados extraídos, caminho e SHA256 completo de cada fonte, além do confronto dos pins herdados quando disponíveis.

| Papel | Declaração e localização |
|---|---|
@TABLE@

APIs Mathlib locais consultadas: @API1@, @API2@, @API3@, @API4@, @API5@. São fornecedores de álgebra/CFC/densidade, não um teorema pronto de identificação modular.

Pins centrais, relidos nesta consulta:

| Fonte | SHA256 |
|---|---|
@HASH_TABLE@

## 8. Literatura e alcance

**[KNOWN]** Hiai, *Lectures on Selected Topics in von Neumann Algebras*, teoremas 10.12–10.13 e 10.15(1), descreve o peso dual e a identificação σ^{φ̃}_t=Ad λ_t no produto cruzado pela ação modular. O texto confirma o sinal e separa esse resultado da construção posterior do traço por perturbação. Aplicar diretamente esse teorema aqui exigiria identificar seus objetos e hipóteses com o peso e a representação concretos; a mera palavra “dual” não faz a aplicação. [Fonte primária consultada](https://arxiv.org/pdf/2004.02383), pp. 95–100 na paginação impressa, especialmente 99–100 para o teorema 10.15.

A proposta acima usa os fornecedores locais para evitar construir a interface abstrata inteira desse teorema. Não houve busca exaustiva no acervo, revisão científica geral, novo axioma, execução de um.py, compilação ou escrita fora de revisao. A construção amortecida e os próximos enunciados permanecem **[DERIVED/OPEN — não compilados]**; os fornecedores têm o estatuto de leitura e proveniência explicitado no JSON.
'''
replacements = {
 '@DATE@': STAMP.isoformat(), '@TABLE@': table, '@HASH_TABLE@': hash_table,
 '@API1@': link('cfc_mul'), '@API2@': link('cfc_comp'), '@API3@': link('StarAlgHom.map_cfc'),
 '@API4@': link('norm_cfc_le'), '@API5@': link('orthogonal_range'),
}
for a, b in replacements.items():
    text = text.replace(a, b)
report_path = OUT / (NAME + '.md')
atomic(report_path, text.encode('utf-8'))
evidence = {
 'time': STAMP.isoformat(),
 'status': 'CONSULTA_DERIVED_NOT_COMPILED__A1B_OPEN',
 'scope': 'Mesma scalarDualWeight/S/J; CFC amortecido do resolvente e consumo por geradores; nenhuma nova implementação.',
 'report': {'path': str(report_path), 'sha256': sha(report_path)},
 'inherited_manifest': {'path': str(manifest_path), 'sha256': sha(manifest_path), 'scope': 'Comparados somente os fornecedores selecionados, sem reaudit completo.'},
 'gap_document': {'path': str(ROOT / 'LACUNAS_A1.md'), 'sha256': sha(ROOT / 'LACUNAS_A1.md')},
 'sources': pins,
 'sources_checked_against_inherited_manifest': sum('manifest_source_match' in e for e in pins),
 'all_selected_manifest_matches': all(e.get('manifest_source_match', True) and e.get('object', {}).get('manifest_match', True) for e in pins),
 'builds_executed': 0,
 'monolith_executed_or_imported': False,
 'author_sources_written': False,
 'memory_written': False,
 'new_Lean_theorems_claimed': 0,
 'web': [{'url': 'https://arxiv.org/pdf/2004.02383', 'sections': ['10.12','10.13','10.15(1)'], 'scope': 'Conferência da formulação e sinal, não importação de teorema Lean.'}],
}
atomic(OUT / (NAME + '.json'), (json.dumps(evidence, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'report': str(report_path), 'sha256': sha(report_path), 'sources': len(pins), 'matched_selected': evidence['sources_checked_against_inherited_manifest'], 'all_matches': evidence['all_selected_manifest_matches']}, ensure_ascii=False))
