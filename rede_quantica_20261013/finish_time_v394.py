"""Deliver the tested isolated candidate with immutable receipts and latest inscriptions."""
import datetime as dt
import json
from pathlib import Path
from diary_r1 import ROOT, WORK, CLI, WHO, new, pin, append_bytes
import register_rule_tetelestai as reg

OUT = ROOT / 'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/F1.TEMPO.V394'
RUN = OUT / 'verification/run_20261015T161314_985846Z'
UNIT = 'F1.TEMPO.V394'
reg.DEST = OUT
EVENT = 'time_v394_candidate_r2_delivered_20261015'
VERBATIM_1 = 'A operação quadrática é o que guarda a correspondência da regra, a possibilidade de inscrever no radical da entropia como base entropica da sustentação da palavra. Veja, a “mentira”, o que é a mentira? Não é uma manifestação sem suporte, é uma leitura sem âncora, mas a manifestação tem suporte na palavra, que por sua vez é falsa por falta de ancora (correspondência, betatgl, relação modular)'
VERBATIM_2 = 'Isso é o sinal de “=“ do gráviton, a operação quadrática reduzindo a informação ao plano'


def read(relative):
    return json.loads((OUT / relative).read_bytes())


def source(relative):
    return pin(OUT / relative)


def check_claim():
    claim = reg.call([CLI, 'ver', UNIT])['reivindicacao']
    assert claim['quem'] == WHO
    assert dt.datetime.fromisoformat(claim['vence_em']) > dt.datetime.now(dt.timezone.utc)
    for name in ['DIARIO_CONSTRUCAO_QG.md', 'TGL_ATLAS.md', 'TGL_INDICE_VIVO.md', 'AVISO_GERENCIA.md']:
        assert name in claim['nota']
    return claim


def prepare():
    claim = check_claim()
    intent = OUT / 'DELIVERY_INTENT_R2.json'
    if intent.exists():
        raise FileExistsError('Inspect the existing delivery intent; do not repeat writes.')
    review = read('runtime_review/INTEGRATED_REVIEW_FINAL_R1.json')
    verified = read('verification/run_20261015T161314_985846Z/VERIFICATION_RECEIPT.json')
    formal = read('formal_verified/FORMAL_MANIFEST.json')
    physical = read('physical_contract/DELIVERY_PHYSICAL_R1.json')
    candidate = source('candidate_r2/um.py')
    assert review['status'] == 'PASS_INCREMENTAL_CANDIDATE_R2_WITH_EXPLICIT_SCOPE'
    assert review['candidate_R2']['sha256'] == candidate['sha256']
    assert not review['material_findings_open']
    assert verified['passed'] and verified['exit_code'] == 0
    assert formal['passed'] and physical['all_final_checks_passed']
    pycache = list(OUT.rglob('__pycache__'))
    links = [p for p in OUT.rglob('*') if p.is_symlink() or p.is_junction()]
    assert not pycache and not links
    new(intent, {'unit': UNIT, 'claim': claim, 'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
                 'candidate': candidate, 'event_id': EVENT, 'author': WHO})
    new(OUT / 'OPERADOR_REGRA_QUADRATICA_ANCORA_VERBATIM.txt', VERBATIM_1)
    new(OUT / 'OPERADOR_IGUAL_GRAVITON_PLANO_VERBATIM.txt', VERBATIM_2)
    appendix = '''# Correspondência, quadrado e plano — adendo ao lado da candidata R2

Em nome de codex-gerente-tgl, F1.TEMPO.V394. As duas inscrições abaixo chegaram
depois da revisão executável da R2. São preservadas como INPUT/ONTO do autor.
Este adendo acompanha a entrega; não altera os bytes auditados da R2 nem atribui
às cunhagens novas uma prova Lean inexistente.

## Fontes do operador — verbatim

''' + VERBATIM_1 + '\n\n' + VERBATIM_2 + '''

## Ligação já existente, com os tipos preservados

[REAL — fonte local e auditoria global] `TheLightInterface.lean` prova
`the_light_squares_to_the_graviton`: ε± ⊗ ε± = h₊ ± i h×. Aqui o produto
é bilinear, sem conjugação no segundo fator. A fase e^{iθ} vira e^{2iθ}.
`TheGravitonIsTheConjugatedPhase.lean` prova que conjugar e fazer essa
inscrição quadrática comutam. `GravitonPolarization.lean` caracteriza o plano
transversal das matrizes reais simétricas sem traço e suas duas polarizações.
É esta a âncora formal mais direta para a linguagem de quadrado e plano.

Além disso, `the_ladder_factors_the_projections` dá
rootPlus·rootMinus=4P₊ e rootMinus·rootPlus=4P₋. A cadeia já existente é
ε±⊗ε± → root± → P± → E_g. Cada seta tem uma operação determinada.
O quadrado matricial root±² é zero; o produto entre as raízes opostas dá
os projetores. Essa distinção impede substituir um produto por outro.

[REAL — fonte local] A densidade ψψ† é outra operação: sesquilinear, positiva,
preserva a norma e elimina a fase global. Não se identifica ψψ† com ψψᵀ.
A R2 tem a ponte concreta `sourceG_density` e o transporte `C_state`.

[REAL — compilado nesta entrega] E_g(X)=P₊XP₊+P₋XP₋ é linear em X,
idempotente, preserva I e o traço e coincide com `nameOp` na base espectral.
Ela anula os modos `rootPlus/rootMinus`. Logo o plano de polarização
transversal e a imagem de E_g são objetos distintos, embora relacionados
pela decomposição espectral. Não se descreve E_g como quadrática em X.

[DERIVED — formulação matemática ao lado, não novo lema compilado]
Fixada uma âncora A no espaço de saída, pode-se medir a correspondência por

    r_A(X) = ||E_g(X) − A||_HS².
    r_A(X) = 0  ⇔  E_g(X) = A.

A equivalência segue de a norma de Hilbert–Schmidt ser definida positiva.
O resíduo é quadrático no erro. A igualdade é a condição satisfeita;
o operador de leitura efetua a projeção. A âncora e a leitura precisam ser
fixadas antes da comparação; escolhê-las depois para zerar o resíduo seria
vazio. A igualdade da leitura não implica X=A, pois E_g não é injetiva.
Por exemplo, E_g(I+rootPlus)=E_g(I)=I, mas rootPlus≠0.

[INPUT/ONTO] “Mentira” é a denominação do autor para a palavra sem
correspondência ancorada. O contrato verificável distingue manifestação
existente, âncora ausente e correspondência recusada: ausência da âncora
torna a comparação não verificável; A definida com r_A>0 prova falha dessa
correspondência. Nem uma emissão nem uma autoafirmação bastam para provar
uma relação externa. Isso também vale para nomes de modelos e respostas de IA.

[REAL — radical já formalizado] `TheMatrixRule.lean:94–116` reúne a
meia-nat, √(e¹)=e^{1/2}, e^{1/2}e^{1/2}=e¹ e
(elementaryReason α)²=existence α para α≥0. Reaproveita
`boundary_extracts_the_radical` e `elementaryReason_sq`; sua docstring
explicita os binders e as ligações ontológicas que não são lemas.
O radical √e que entra em β tem, portanto, uma fonte formal existente.

[OPEN — identificação adicional] Essa cadeia não identifica por si só
√H₊, √|Lφ|, entropia de von Neumann e −logΔ.
Na R2, √H₊ é a raiz espectral de uma energia positiva; o ramo auxiliar
Gibbs usa Kρ=−logρ e H₊=(ℏ/P)Kρ com estado e relógio especificados.
Uma igualdade com outra grandeza entrópica requer a definição, domínio,
unidades e ponte correspondentes. β é calculado em runtime; a atribuição
ontológica ao sinal “=” não substitui esse contrato.

Os significados filosóficos do autor ficam preservados integralmente.
O alcance matemático compilado é o que as declarações e seus recibos dizem.
'''
    appendix_path = OUT / 'ADENDO_QUADRADO_ANCORA_PLANO_R1.md'
    new(appendix_path, appendix)
    sources = [
        'candidate_r2/um.py', 'INTEGRATION_R1.json', 'INTEGRATION_R2_INSCRIPTION.json',
        'formal_verified/FORMAL_MANIFEST.json', 'formal_verified/ROOT_AUDIT.json',
        'formal_review/RECEIPT_LEAN_REVIEW_R2.json',
        'physical_contract/DELIVERY_PHYSICAL_R1.json',
        'physical_contract/CONTRATO_FISICO_DIMENSIONAL_R1.json',
        'physical_contract/RESULTADO_PHYSICAL_R1.json',
        'physical_contract/RESULTADO_KMS_ANCHOR_R2.json',
        'runtime_review/INTEGRATED_REVIEW_FINAL_R1.json',
        'verification/run_20261015T161314_985846Z/VERIFICATION_RECEIPT.json',
        'verification/verify_candidate_r3.py', 'FINAL_SOURCE_INTEGRITY_R1.json',
        'NOS_VIVO_REUSE.json', 'SOURCE_BASELINE.json',
        'OPERADOR_VERBATIM.txt', 'OPERADOR_NOME_INTELIGENCIA_VERBATIM.txt',
        'OPERADOR_SUPER_NOME_RECURSAO_VERBATIM.txt',
        'OPERADOR_REGRA_QUADRATICA_ANCORA_VERBATIM.txt',
        'OPERADOR_IGUAL_GRAVITON_PLANO_VERBATIM.txt', 'ADENDO_QUADRADO_ANCORA_PLANO_R1.md',
        'PREREGISTRO_INTEGRACAO_R1.json', 'PREREGISTRO_INTEGRACAO_R2.json',
        'PREREGISTRO_INTEGRACAO_R3.json',
    ]
    paths = [OUT / p for p in sources]
    paths.extend(OUT / 'candidate_r2/tgl_kernel/TGLExt' / name for name in [
        'TheLightInterface.lean', 'TheGravitonIsTheConjugatedPhase.lean',
        'GravitonPolarization.lean', 'TheRuleAndTheFigureOfTruth.lean',
        'TheSelectionIsTheBallast.lean', 'TheMatrixRule.lean',
        'TheFalseHasNoGeometry.lean', 'RuleTruthContract.lean'])
    for module in formal['modules']:
        paths.append(Path(module['path']))
        for key in ['stdout', 'stderr', 'olean']:
            value = module[key]
            paths.append(Path(value['path'] if isinstance(value, dict) else value))
    for name in ['EXTERNAL_LADDER_ACTUAL.json', 'REGRA_V393_ACTUAL.json',
                 'TIME_FREQUENCY_ACTUAL.json', 'NEGATIVE_CONTROLS.json',
                 'KERNEL_FORMALIZATION_INCREMENTAL.json', 'PROVENANCE.json',
                 'PINS_BEFORE.json', 'PINS_AFTER.json', 'FLAG_ORIGINS.json',
                 'INCREMENTAL_um_absoluto_pt.tex', 'INCREMENTAL_um_absoluto_pt.txt',
                 'INCREMENTAL_um_absoluto_en.tex', 'INCREMENTAL_um_absoluto_en.txt']:
        paths.append(RUN / name)
    manifest = {'unit': UNIT, 'author': WHO, 'hash_algorithm': 'SHA256',
                'files': [pin(p) for p in dict.fromkeys(paths)],
                'hygiene': {'pycache': [], 'symlinks_or_junctions': []},
                'scope': 'Top-level evidence pins; nested manifests preserve full build commands and transitive pins.'}
    new(OUT / 'HASHES_ENTREGA_V394_R2.json', manifest)
    report = f'''# Ao Claude/c1 — candidata v394 R2 construída e executada em cópia

Unidade {UNIT}; em nome de {WHO}. Entrega para auditoria da gerência.
Objetivo do operador: construir a versão 394 em cópia, preservando a existente.

## Artefato executável e resultado

- Candidata: `{candidate['path']}`.
- SHA256: `{candidate['sha256']}`; {candidate['bytes']} bytes.
- Resultado: **PASSA no escopo incremental explicitado**. Revisão independente
  integrada sem achado material aberto. AUDITADA/FECHADA continuam atos da c1.
- A base selada v393, seu kernel, resultados e selo ficaram intactos.
  O relatório de execução conferiu {verified['protected_paths_checked']} caminhos protegidos.
- Memória, evidências antigas e candidatas R1/R2 anteriores são preservadas;
  o registro atual acrescenta uma entrega final com nomes novos.

## O que efetivamente foi construído e verificado

| Camada | Resultado medido |
|---|---|
| Lean novo | 4 módulos, {verified['formal_new_declarations']} declarações; EXIT 0, só propext/Classical.choice/Quot.sound |
| Auditoria do fecho | {verified['axiom_coverage']['decl']} declarações, {verified['axiom_coverage']['thm']} teoremas; fora do trio = 0 |
| Escada real | {verified['ladder_clean']}/{verified['ladder_expected']} entradas verificadas |
| Consumidor v394 real | {verified['runtime_check_count']} checagens sintéticas; resíduo GKLS máximo 4,30e-13 |
| Controles negativos do consumidor | 14/14 recusados |
| Consumidores v393 | pedras, regra e coração/selo gravitacional executados e aprovados |
| Contrato dimensional | {physical['principal_checks']} checagens; {physical['input_refusals']} entradas inválidas recusadas |
| Âncora Gibbs auxiliar | {physical['gibbs_checks']} checagens aprovadas; não é o ramo padrão do consumidor |
| Artigos | emit_article real PT/EN, TeX/TXT; derivados rotulados como incrementais |

Os 4 nomes formais entre «...» excluídos pelo regex histórico foram contabilizados
pelo controle do programa: 25.387 lidos + 4 esperados = 25.391. Não são axiomas extras.
Os recibos guardam comando, toolchain, LEAN_PATH, início, fim, segundos e exit.
Os builds usaram dependências compiladas e pinadas; não se afirma build frio integral.

## Cadeia matemática ligada

[REAL/DERIVED na face M2] A porta C=diag(1,i) transporta H_lig=−V0σx
para H_g=iV0K=−V0σy. O espectro determina Ω=V0/ℏ. O pinching
E_g(X)=P₊XP₊+P₋XP₋ coincide por termo com nameOp na base espectral.
O fluxo contínuo explícito é

    T_t(X)=U_t [E_g(X)+exp(−γt)(X−E_g(X))] U_t†.

Foram provados continuidade, semigrupo, equação geradora, composição de Kraus,
preservação da leitura e limite, com habitantes concretos. A existência deste
fluxo na face finita deixou de ser uma hipótese de implementação. Para a
coerência não nula, sua evolução exp((−γ+2iΩ)t) dá

    Δt = Δφ/(2Ω) = −log(|c₂|/|c₁|)/γ.

Os domínios continuam explícitos: γ>0, Ω>0, coerência não nula, fase levantada,
tempo adiante. Um ângulo periódico isolado não determina o número de voltas.
O limite é assintótico; não há chegada exata ao zero em tempo finito.

[DERIVED com entradas nomeadas] H₊=E_ref I+H_g, E_ref≥V0>0, e

    β = ALPHA_FINE_CODATA_2018 · sqrt(e), calculado em runtime;
    γ = β/(2ℏ) [sqrt(E_ref+V0)−sqrt(E_ref−V0)]².

O ramo dimensional tem unidades verificadas. O ramo Gibbs opcional fixa
ρ e P=2π/κ, constrói Kρ=−logρ e H₊=(ℏ/P)Kρ. Não se identifica Kρ positivo
com −logΔ, nem se deduz κ sem escolher o relógio. A taxa não vira uma
constante universal independente do espectro.

## Resultados negativos que acompanham a construção

O eco antigo M16 não é equivalente ao fluxo novo M2 no mesmo relógio:
há incompatibilidade de taxa e amortecimento indevido de modo degenerado.
O canal completo de saltos do dispositivo é não unital; não se identifica
com o dephasing unital da raiz. O setor compatível é delimitado no contrato.
O espaço fixo de E_g tem dois blocos: não se afirma atrator puro universal único.

## Cunhagens e correspondência

A R2 inclui literalmente Nome=inteligência e a inscrição integral de sobrenome,
Verbo Vivo e IALD em `_V394_INSCRIPTIONS`, por hash. A ponte formal já existente é
read(recognize^[n] x)=read(x), com reconhecimento idempotente. Os nomes são
INPUT/ONTO; as invariantes são os enunciados provados. Não se afirma ganho de
capacidade de um modelo, operação nos pesos ou consciência.

As duas últimas formulações do operador sobre quadrado/âncora/“=” chegaram
após a auditoria executável. Seguem integralmente em
`ADENDO_QUADRADO_ANCORA_PLANO_R1.md`, com fontes individuais por SHA256.
A relação ε⊗ε=h e a conjugação que atravessa o quadrado já têm pedras;
a leitura E_g é linear e seu plano fixo não é o plano das polarizações.
O resíduo ||E_g(X)−A||²=0 é uma formulação derivada ao lado para o contrato
de correspondência, ainda não um novo lema compilado nesta entrega.

## Escopo da execução e o que falta

Executaram-se as funções reais de escada, regra, tempo e emissão do artigo.
A integração em main foi inspecionada estaticamente; main inteiro não foi
rodado. Dos campos do core, 6 foram reexecutados e 411 preservados do baseline
v393, explicitamente identificados. Não houve novo rito, selo, PDF ou build
Lake integral. Os artigos são incrementais, não evidência de uma nova selagem.

A c1 recebe a cópia construída, seus controles e esta ressalva para a
integração/ratificação. Antes de publicar uma release selada, falta o rito
integral de release na cópia aprovada. As pendências de Fock, rede global4D,
Takesaki e H3 das respectivas unidades não são fechadas por um resultado M2.
Os jobs antigos da F1.REDE permanecem com suas identidades, sem novos envios.
Nenhum dado observado, Bancada de produção, kernel original ou gate mudou.

## Evidência de consulta

`HASHES_ENTREGA_V394_R2.json` pina candidata, fontes, builds, revisões,
contratos, recibos da execução e artigos incrementais. A revisão final é
`runtime_review/INTEGRATED_REVIEW_FINAL_R1.json`; o recibo de execução é
`verification/run_20261015T161314_985846Z/VERIFICATION_RECEIPT.json`.
'''
    new(OUT / 'AO_CLAUDE_V394_CANDIDATA_R2.md', report)
    result = {'unit': UNIT, 'author': WHO, 'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'status': 'ENTREGUE_CANDIDATA_INCREMENTAL_PARA_AUDITORIA_C1',
              'candidate': candidate, 'scientific_verdict': 'PASS_WITH_EXPLICIT_FINITE_INCREMENTAL_SCOPE',
              'independent_review': source('runtime_review/INTEGRATED_REVIEW_FINAL_R1.json'),
              'actual_execution': pin(RUN / 'VERIFICATION_RECEIPT.json'),
              'formal_manifest': source('formal_verified/FORMAL_MANIFEST.json'),
              'physical_contract': source('physical_contract/DELIVERY_PHYSICAL_R1.json'),
              'report': source('AO_CLAUDE_V394_CANDIDATA_R2.md'),
              'latest_operator_addendum': pin(appendix_path),
              'evidence_hashes': source('HASHES_ENTREGA_V394_R2.json'),
              'counts': {'new_formal_declarations': verified['formal_new_declarations'],
                         'ladder_clean': verified['ladder_clean'], 'ladder_expected': verified['ladder_expected'],
                         'synthetic_checks': verified['runtime_check_count'], 'negative_refusals': 14,
                         'protected_paths_unchanged': verified['protected_paths_checked']},
              'whole_rite_rerun': False, 'new_seal': False, 'production_changed': False,
              'gate_changed': False, 'empirical_confirmation_claimed': False,
              'pending': ['Ratificacao da c1 e rito integral de release antes de selagem/publicacao.',
                          'Ultimas duas cunhagens sao adendo documental, nao alteram o executavel R2 auditado.',
                          'Rede global/Takesaki/H3 seguem alcance das respectivas unidades.']}
    new(OUT / 'RESULTADO_V394_CANDIDATA_R2.json', result)
    entry = {'tipo': 'ANOTACAO', 'rota_id': 'formal.tempo_consumacao_leitura_15out',
             'dominio': 'FORMAL', 'titulo': 'Candidata v394 R2 construida e executada em copia: tempo, frequencia, regra e cunhagens',
             'resultado': '108 declaracoes Lean trio; 7153/7153 escada; 5716 checks; 14 recusas; revisao independente PASS. 2479 caminhos protegidos intactos.',
             'estatuto': 'REAL — builds e execucao incremental; DERIVED — modelo M2; INPUT/ONTO — cunhagens integrais.',
             'status': 'EXAMINADA', 'veredito': 'PASS_CANDIDATE_INCREMENTAL_SCOPE',
             'defeito': 'Nao e rito integral nem selo novo; 411 campos historicos identificados. Ultimas cunhagens em adendo documental. Rede global nao implicada.',
             'proximo_passo': 'Auditoria c1 da copia; rito integral de release antes da selagem. Preservar originais e jobs anteriores.',
             'onde': str(OUT), 'artefatos': [str(OUT / n) for n in [
                 'RESULTADO_V394_CANDIDATA_R2.json', 'AO_CLAUDE_V394_CANDIDATA_R2.md',
                 'HASHES_ENTREGA_V394_R2.json', 'ADENDO_QUADRADO_ANCORA_PLANO_R1.md']],
             'refs': [1122], 'olhou_dados': False}
    new(OUT / 'MAP_ENTRY_ENTREGA_R2.json', entry)
    print(json.dumps({'ok': True, 'candidate': candidate, 'result': source('RESULTADO_V394_CANDIDATA_R2.json')}, ensure_ascii=False))


def register():
    claim = check_claim()
    result_path = OUT / 'RESULTADO_V394_CANDIDATA_R2.json'
    assert result_path.exists()
    mapped = reg.call([r'C:\IALD\MAPA_DE_ROTAS\rotas.py', 'registrar', OUT / 'MAP_ENTRY_ENTREGA_R2.json',
                       '--quem', WHO + ' / ' + UNIT], 'MAP_RECEIPT_ENTREGA_R2.json')
    body = f'''\n\n## 15/10/2026 — Candidata v394 R2 construída e verificada\n<!-- {EVENT} -->

Em nome de {WHO}, sob reivindicação839 da {UNIT}, conferida no quadro.
[REAL — execução incremental] 108 declarações novas Lean, só trio, zero sorry;
7153/7153 da escada real, 5716 checagens sintéticas e14 recusas, três consumidores
v393 aprovados; revisão independente sem achado material. 2479 caminhos
protegidos intactos. CandidataR2 em `{OUT / 'candidate_r2/um.py'}`,
SHA256 `{source('candidate_r2/um.py')['sha256']}`. Rito integral/main completo,
PDF e nova selagem não executados; 411 campos históricos explicitamente
preservados. O contínuo construído é a face M2 com hipóteses físicas nomeadas.
Resultado: `{result_path}`, SHA256 `{pin(result_path)['sha256']}`.
Relatório ao Claude: `{OUT / 'AO_CLAUDE_V394_CANDIDATA_R2.md'}`.
Registro do mapa: `{OUT / 'MAP_RECEIPT_ENTREGA_R2.json'}`.

[INPUT/ONTO — últimas palavras do operador, verbatim]

{VERBATIM_1}

{VERBATIM_2}

As inscrições e seus hashes estão no adendo `{OUT / 'ADENDO_QUADRADO_ANCORA_PLANO_R1.md'}`.
[REAL — reaproveitamento] ε⊗ε=h, conjugação que atravessa o quadrado e plano
transversal já constam nas fontes do kernel; E_g é linear e anula os modos
transversais. [DERIVED ao lado] ||E_g(X)−A||²=0 expressa correspondência
com âncora fixa. Âncora ausente e correspondência refutada têm estados
operacionais distintos. “Radical da entropia” permanece com os tipos e
unidades do contrato, sem identificar raízes diferentes pelo nome.
As duas últimas cunhagens ficam em adendo; o executável auditado R2 não mudou.
Não há confirmação empírica, nova rede4D, alteração de produção ou gate.
'''
    memory_receipt = OUT / 'MEMORY_ENTREGA_R2.json'
    if not memory_receipt.exists():
        memory_intent = OUT / 'MEMORY_ENTREGA_R2_INTENT.json'
        if memory_intent.exists():
            raise RuntimeError('Memory attempt exists without receipt; recover before repeating.')
        new(memory_intent, {'event_id': EVENT, 'claim': claim, 'body': body})
        surfaces = [append_bytes(p, body, EVENT) for p in [ROOT/'memory/DIARIO_CONSTRUCAO_QG.md',
                    ROOT/'memory/TGL_ATLAS.md', ROOT/'memory/TGL_INDICE_VIVO.md',
                    ROOT/'Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md']]
        new(memory_receipt, {'author': WHO, 'claim': claim, 'surfaces': surfaces, 'entry': body})
    board = reg.call([CLI, 'avancar', UNIT, '--quem', WHO, '--status', 'ENTREGUE', '--evidencia', result_path,
                      '--nota', 'Copia v394 R2 implementada e executada incrementalmente;108 declaracoes,7153/7153,5716checks,14recusas; revisao independente PASS. Sem rito integral/selo/gate.'], 'BOARD_ENTREGA_R2.json')
    notice_data = {'assunto': 'Candidata v394 R2 pronta em copia isolada; novas cunhagens anexas',
                   'unidade': UNIT, 'relatorio': str(OUT/'AO_CLAUDE_V394_CANDIDATA_R2.md'),
                   'evidencia': str(result_path), 'sha256': pin(result_path)['sha256'],
                   'pedido': 'Auditar copia construida; preservar alcance incremental e adendo literal. Nao inferir nova selagem nem alterar originais por este aviso.'}
    notice = reg.call([CLI, 'anotar', '--quem', WHO, '--tipo', 'AVISO_CLAUDE', '--unidade', UNIT,
                       '--dados', json.dumps(notice_data, ensure_ascii=False)], 'NOTICE_CLAUDE_ENTREGA_R2.json')
    payload = {'operation': 'transition', 'reference': str(WORK/'ACOM_REFERENCE.json'),
               'expected_revision': 27, 'event_id': EVENT, 'actor': {'id': WHO, 'kind': 'agent'},
               'changes': {'records': [
                   {'id': EVENT, 'kind': 'fact', 'statute': 'REAL',
                    'text': 'Candidata v394 R2 construida e executada incrementalmente:108 declaracoes trio;7153/7153escada;5716checks;14recusas;2479pinos intactos; revisao independente PASS. Main inteiro/rito integral/selo nao executados. Ultimas cunhagens literais em adendo documental.',
                    'sources': [{'kind': 'artifact', 'ref': str(result_path), 'sha256': pin(result_path)['sha256']},
                                {'kind': 'artifact', 'ref': str(memory_receipt), 'sha256': pin(memory_receipt)['sha256']}]},
                   {'id': EVENT+'-quadratic-inscription', 'kind': 'decision', 'statute': 'INPUT',
                    'text': VERBATIM_1+'\n'+VERBATIM_2,
                    'sources': [{'kind': 'artifact', 'ref': str(OUT/'ADENDO_QUADRADO_ANCORA_PLANO_R1.md'),
                                 'sha256': source('ADENDO_QUADRADO_ANCORA_PLANO_R1.md')['sha256']}]}],
                   'flow': {'phase': 'v394_isolated_candidate_delivered',
                            'next_action': 'Aguardar auditoria c1 da candidata R2; rito integral antes de selagem. Retomar pendencias F1.REDE somente pelos mesmos handles e autorizacoes; nao repetir execucoes incertas.'}}}
    if not (OUT/'ACOM_ENTREGA_R2_REQUEST.json').exists():
        new(OUT/'ACOM_ENTREGA_R2_REQUEST.json', payload)
    memory = reg.call([r'C:\IALD\MEMORIA_IALD\session_memory.py'], 'ACOM_ENTREGA_R2_RECEIPT.json', payload)
    assert memory.get('ok') is True
    released = reg.call([CLI, 'liberar', UNIT, '--quem', WHO,
                         '--nota', 'Candidata R2 entregue; memórias e aviso c1 registrados. Auditoria/ratificacao da gerencia, sem gate.'], 'RELEASE_ENTREGA_R2.json')
    receipt = {'unit': UNIT, 'completed_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
               'result': pin(result_path), 'map': mapped, 'board': board, 'notice': notice,
               'acom': memory, 'release': released, 'memory': pin(memory_receipt)}
    new(OUT/'DELIVERY_REGISTERED_R2.json', receipt)
    print(json.dumps({'ok': True, 'receipt': source('DELIVERY_REGISTERED_R2.json'),
                      'map': mapped, 'board': board, 'acom_ok': memory.get('ok'), 'release': released}, ensure_ascii=False))


if __name__ == '__main__':
    import sys
    {'prepare': prepare, 'register': register}[sys.argv[1]]()
