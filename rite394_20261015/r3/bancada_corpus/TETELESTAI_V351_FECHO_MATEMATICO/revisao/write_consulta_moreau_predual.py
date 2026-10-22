from pathlib import Path
import json, hashlib, datetime, os
root = Path(r'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO')
out = root / 'revisao'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def atomic(p, text):
    assert not p.exists(), str(p)
    b = text.encode('utf-8')
    t = p.with_name(p.name + '.tmp')
    with t.open('xb') as f: f.write(b)
    assert t.read_bytes() == b
    os.replace(t, p)
ficha = json.loads((root / 'REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json').read_text(encoding='utf-8-sig'))
records = []
for p in ficha['providers']:
    path = Path(p['file'])
    actual = sha(path)
    assert actual == p['sha256'], path
    records.append({'file': str(path), 'sha256': actual, 'declaration': p['declaration'], 'status': p.get('status', 'PIN_CONFERIDO')})
stamp = datetime.datetime.now().astimezone().isoformat()
report = out / 'CONSULTA_A1_MOREAU_PREDUAL.md'
text = r'''# Consulta A1 — aproximantes de Moreau e valores no predual

DATA

**[DERIVED, condicionado aos aproximantes propostos] A rota basta para construir cada valor m_A no cone positivo estendido do predual.** Não é necessário um isomorfismo geral entre todas as formas afiliadas e esse cone. Não há aceitação de V351BaseMoreauApproximants nesta consulta: sua fonte em correção não foi lida nem compilada.

[REAL] Ficha MD/JSON lida inteira; pins dos nove registros de fornecedores conferidos. Foram relidos os enunciados pertinentes de DualVariational, DualEnergyOnResolvent e ExtendedBaseDualWeight. O registro `exists_dual_form_representation` continua apenas `NAO_LOCALIZADO_POR_ESSE_NOME`, não é fornecedor aceito. Nenhum build ou teste novo nesta consulta.

## 1. O passo variacional é suficiente, inclusive no setor infinito

Notação: q é a mesma dualQuadraticIntegral, Hreg a Hilbert regular, M a base; ι(D)=fibre D. Para c>0, R_c é o resolvente já construído do input A/c. Multiplicar a energia mínima por c e usar a identidade finita no minimizador dá

    q_A(R_c v) + c‖R_c v-v‖² = Re⟨v,c(I-R_c)v⟩.

Logo, se B_c=c(I-R_c)∈F e ι(D_c)=B_c, obtém-se o mínimo pretendido e 0≤D_c≤cI pela equivalência de ordem existente. A identidade com `toReal` só se usa no minimizador, onde a finitude já foi provada; nunca em q_A(v) arbitrário.

Comparar os mesmos competidores prova crescimento em c. Escolha c_n=n+1 para não dividir por zero. Ponha L=sup_n Re⟨v,ι(D_n)v⟩, sempre em ENNReal. O competidor w=v dá L≤q_A(v). Se L<∞, a identidade do mínimo implica q_A(R_n v)≤L e ‖R_n v-v‖²≤L.toReal/(n+1). Portanto R_n v→v e a semicontinuidade inferior dá q_A(v)≤liminf q_A(R_n v)≤L. Se L=∞, a primeira desigualdade já força q_A(v)=∞. Assim o supremo recupera toda q, sem domínio finito denso presumido.

Alerta de notação: Re⟨v,ι(D_n)v⟩ é a forma quadrática **limitada** do operador amplificado D_n. Não é a aplicação de `dualQuadraticIntegral` novamente a ι(D_n), que introduziria outra integral dual.

## 2. Definição do valor estendido e propriedades mínimas

Para ψ∈M_*^+ concreto, defina

    m_A(ψ) := sup_n ENNReal.ofReal(Re ψ(D_n(A))).

A positividade torna Re ψ(D_n) não negativa. Cada avaliação é contínua no predual; o supremo é semicontínuo inferior. O crescimento comum da sequência permite

    sup_n [ψ(D_n)+χ(D_n)] = sup_n ψ(D_n)+sup_n χ(D_n),

inclusive se um valor é infinito. Isto prova aditividade em ψ; a homogeneidade para escala real finita não negativa segue analogamente, tratando escala zero explicitamente (0·∞=0). Um supremo arbitrário de avaliações sem crescimento não justificaria essa aditividade.

Estas são exatamente as propriedades da apresentação predual do cone positivo estendido; não exigem construir PVM. A referência para o estatuto é [Hiai, definição 8.1 e operações que a seguem](https://arxiv.org/pdf/2004.02383). A dedução acima usa os aproximantes específicos, sem invocar o teorema geral de representação espectral 8.3.

## 3. Ponte pequena que ainda precisa ser tipada

Primeiro demonstrar, para todo v da Hilbert da base,

    m_A(ω_v) = (baseDualWeight P A).value v,
    ω_v(D)=⟨v,Dv⟩.

Daí ν(A)=m_A(ω_hOmega), preservando também infinito. Isto é mais que renomear: o novo valor atua em todos os funcionais normais positivos, e essa identidade o liga ao valor vetorial já construído.

Para transportar todas as leis, não basta verificar somente ω_hOmega, nem presumir que cada ψ é um único estado vetorial nesta representação. Basta um lema restrito a **supremos crescentes de operadores positivos limitados**: uma decomposição normal positiva ψ=Σ_k ω_v_k, com Σ_k‖v_k‖²<∞, implica

    m_A(ψ)=Σ_k (baseDualWeight P A).value v_k.

A prova troca supremo crescente e soma não negativa. A representação de funcionais normais positivos por soma de funcionais vetoriais, ou uma extensão normal positiva equivalente, é a ponte funcional a fornecer/reutilizar explicitamente; não foi localizada como Lean nesta consulta. Não requer separabilidade de H. Esse lema também dá independência dos aproximantes e extensionalidade desta família, sem exigir isomorfismo geral de cones.

Aplicando-o às leis já existentes das formas, restam os seguintes consumidores concretos:

- **Família em A:** zero, soma e escala, ordem e fidelidade. Os aproximantes de A+B não precisam ser somas dos aproximantes de A e B; provar a igualdade no limite.
- **Bimódulo:** m_(ι(b)*Aι(b))(ψ)=m_A(ψ_b), onde ψ_b(D)=ψ(b*Db). A orientação é essa: ψ_b=ω_bv quando ψ=ω_v.
- **Normalidade:** para supremo interno dirigido positivo S=sup_i A_i, m_S(ψ)=sup_i m_Ai(ψ). Transportar a normalidade vetorial existente com convergência monótona; não reduzir o índice i a sequência.
- **Outputs limitados já fornecidos:** q_A=forma de ι(D) implica m_A(ψ)=ψ(D). Isto preserva o ideal fortemente denso de quadrados com outputs limitados, sem inferir que todo A tenha valor limitado ou finito.

Os tipos devem representar funcionais **normais positivos** da mesma M e sua topologia predual; dar esse nome a um funcional arbitrário não fornece a ponte. As provas podem ser específicas a esta M e a estes outputs.

## 4. Identificação dual e limite para A1

Se o consumidor exige a interpretação por média dual, a igualdade em toda Hreg oferece uma verificação direta adicional: para Φ normal positivo ambiente,

    sup_n Φ(ι(D_n(A))) = dualHaarFactor · ∫ Φ(dualAmbient_s(A)) ds.

Usam-se decomposição vetorial normal e convergência monótona/Tonelli, com o **mesmo** fator Haar. A esquerda depende só da restrição de Φ a ι(M); a igualdade torna a leitura da direita independente da extensão ambiente. Não avaliar ψ diretamente em dualAmbient_s(A) antes de uma ponte de tipos: esse operador mora no core, não necessariamente na base.

Este é um avanço real para `regular_scalar_weight_is_dual_weight`: valor predual específico, compatibilidade escalar e, com as leis acima, estrutura de peso com valores na base. Não se pede teorema de Fourier novo nem identificação espectral geral. A1(b) como existência do traço escalado e sua perturbação continua [OPEN]; os aproximantes não a demonstram sozinhos.

**Próximos enunciados econômicos:** (i) representação crescente D_n e supremo da forma; (ii) `m_A` aditivo/homogêneo/LSC e avaliação vetorial; (iii) extensionalidade desta família nos funcionais normais positivos; (iv) transporte de soma/bimódulo/normalidade e outputs limitados. São obrigações novas delimitadas, não alegações Lean já aceitas. Não há impedimento conceitual identificado na rota proposta.
'''.replace('DATA', stamp, 1)
atomic(report, text)
evidence = {
    'time': stamp,
    'status': 'CONCEPTUAL_CONDITIONAL_NOT_LEAN_REVIEW',
    'ficha_md_sha256': sha(root / 'REAPROVEITAMENTO_A1_APROXIMANTES_BASE.md'),
    'ficha_json_sha256': sha(root / 'REAPROVEITAMENTO_A1_APROXIMANTES_BASE.json'),
    'provider_pins': records,
    'report': {'path': str(report), 'sha256': sha(report)},
    'candidate_source_read': False,
    'candidate_compiled': False,
    'new_lean_written': False,
    'writes_only_revisao': True
}
atomic(out / 'CONSULTA_A1_MOREAU_PREDUAL_pins.json', json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(evidence['report'], ensure_ascii=False))
