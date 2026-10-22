from pathlib import Path
import datetime
import hashlib
import json
import os

root = Path(__file__).resolve().parent
stamp = datetime.datetime.now().astimezone().isoformat()
suffix = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

def pin(path):
    data = path.read_bytes()
    return {'path': str(path), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def put(path, data, memory=False):
    assert path.is_relative_to(root) and data
    if path.exists():
        assert memory, f'Existing immutable artifact: {path}'
        previous = path.read_bytes()
        backup = path.with_name(path.name + '.bak_' + suffix)
        assert not backup.exists()
        backup.write_bytes(previous)
        assert backup.read_bytes() == previous
        assert len(data) >= len(previous), 'Append-only memory update expected'
    temporary = path.with_name(path.name + '.tmp_' + suffix)
    temporary.write_bytes(data)
    assert temporary.read_bytes() == data
    os.replace(temporary, path)
    assert path.read_bytes() == data

sources = [pin(root/'k/TGLExt'/name) for name in (
    'V351ScalarWeightSemifiniteness.lean', 'V351RegularCoreTraceContract.lean')]
review = [pin(root/'revisao_core'/name) for name in (
    'CONSULTA_SEMIFINITUDE_PESO_VS_TRACO.md', 'CONSULTA_SEMIFINITUDE_PESO_VS_TRACO.json')]
text = f'''[DERIVED — correção de roteiro, com revisão escrita independente; sem novo teorema Lean]

# Semifinitude do peso e semifinitude do traço

{stamp}

O requisito por minorantes positivos pertence ao futuro traço τ. Não deve ser cobrado como propriedade geral do peso dual ν. A fonte existente já fornece a semifinitude usual deste peso: `TGLV351.scalarWeight_square_finite_wot_closure`, em `V351ScalarWeightSemifiniteness.lean`, é a densidade WOT do domínio quadrado-finito no mesmo core. A consulta não recompila esse fornecedor nem cria outro objeto.

[KNOWN] Hiai, *Concise lectures on selected topics of von Neumann algebras*, §7.1, Definição 7.1, p.63, usa a densidade fraca do ideal quadrado-finito para a semifinitude de pesos. A definição não exige minorantes finitos abaixo de todo positivo. [Fonte primária](https://arxiv.org/pdf/2004.02383#page=63).

[DERIVED — prova escrita, não Lean] Em B(ℓ²(N≥1)), seja φ(A)=Σ n²⟨eₙ,Aeₙ⟩ para A≥0. É um peso fiel normal: somas finitas de funcionais vetoriais positivos são normais, os supremos comutam, e φ(A)=0 implica A¹ᐟ²eₙ=0 para toda a base. Para p_N a projeção coordenada finita e x limitado, φ((xp_N)*(xp_N))=Σ_(n≤N) n²‖xeₙ‖²<∞. Como xp_N→x fortemente, o ideal quadrado-finito é denso.

Escolha ξₙ=c/n, com c>0 normalizando ‖ξ‖=1. Então φ(Pξ)=∞. Todo 0≤B≤Pξ é bPξ, 0≤b≤1: a positividade anula B¹ᐟ² em ξ⊥. Só b=0 tem peso finito. Portanto sup{{φ(B):0≤B≤Pξ, φ(B)<∞}}=0≠φ(Pξ). Isto refuta a ponte geral para pesos, não a existência do traço nem uma propriedade de uma projeção específica do core construído.

Para um traço normal semifinito τ, tome projeções e_i↑1 com τ(e_i)<∞. Para A≥0 limitado, B_i=A¹ᐟ²e_iA¹ᐟ²≤A e B_i↑A. A tracialidade dá τ(B_i)=τ(e_iAe_i)≤‖A‖τ(e_i)<∞; a normalidade fornece τ(A)=sup_i τ(B_i). Assim o campo `RegularCoreTraceData.semifinite` continua exigido e pode ser pago usando tracialidade. Não removemos nem enfraquecemos esse contrato.

A revisão independente escrita em `revisao_core/CONSULTA_SEMIFINITUDE_PESO_VS_TRACO.md` aceita o argumento. Ela não é uma compilação ou construção de τ. Nenhum relatório selado, contrato ou memória canônica foi modificado. A menção anterior a `scalarWeightLeftIdeal_wotDense` era um nome aproximado incorreto; o fornecedor exato é o acima.

[OPEN] Identificação das potências do gerador regular, afiliação, escala dual e perturbação para o traço. A correção retira uma exigência falsa sobre ν, sem dispensar as obrigações de τ.

## Custódia lida nesta gravação

'''
for entry in sources + review:
    text += f"- `{entry['path']}` — {entry['bytes']} bytes — SHA256 `{entry['sha256']}`.\n"
md = root/'ADENDO_SEMIFINITUDE_PESO_VS_TRACO.md'
put(md, text.encode('utf-8'))
record = {'timestamp': stamp, 'status': 'WRITTEN_ARGUMENT_INDEPENDENTLY_REVIEWED__TRACE_OPEN',
          'sources': sources, 'independent_written_review': review, 'document': pin(md),
          'new_lean_theorems': 0, 'trace_contract_changed': False,
          'exact_existing_provider': 'TGLV351.scalarWeight_square_finite_wot_closure',
          'weight_finite_minorants_required': False, 'trace_finite_minorants_required': True}
js = root/'ADENDO_SEMIFINITUDE_PESO_VS_TRACO.json'
put(js, json.dumps(record, ensure_ascii=False, indent=2).encode('utf-8'))
memory = root/'MEMORIA_RETOMADA_A1B_012.md'
addition = f'''\n\n## Adendo {stamp} — peso versus traço

A frase anterior “semifinitude por minorantes positivos também permanece” refere-se EXCLUSIVAMENTE ao contrato do futuro traço τ. Para o peso dual ν, o fornecedor existente `TGLV351.scalarWeight_square_finite_wot_closure` já entrega o critério usual. Não procurar nem postular uma ponte geral de densidade quadrado-finita para minorantes de cada positivo: ela é falsa para pesos não traciais. O contraexemplo fiel normal semifinito em B(ℓ²), a fonte primária e a revisão escrita estão em `ADENDO_SEMIFINITUDE_PESO_VS_TRACO.md/json`. Zero novos teoremas Lean; zero alteração de contrato. Os dados e a existência do traço continuam abertos. Preservar este adendo em checkpoints posteriores.
'''
put(memory, memory.read_bytes() + addition.encode('utf-8'), memory=True)
memory_json = root/'MEMORIA_RETOMADA_A1B_012.json'
current = json.loads(memory_json.read_text(encoding='utf-8'))
current.setdefault('append_only_corrections', []).append({'timestamp': stamp,
    'document': pin(md), 'record': pin(js), 'scope': 'finite-minorant property required for trace only'})
put(memory_json, json.dumps(current, ensure_ascii=False, indent=2).encode('utf-8'), memory=True)
print(json.dumps({'document': pin(md), 'record': pin(js), 'memory': pin(memory)}, ensure_ascii=False))
