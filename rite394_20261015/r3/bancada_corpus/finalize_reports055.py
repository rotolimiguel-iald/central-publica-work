"""Create exclusive continuation055 reports after final audit and linked review.

Inert on import. This script never compiles, seals, overwrites reports, or edits
historical sources. It emits only the two new documentary outputs under Chatgpt.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
MODULES = ['ExchangeEntropyResponse', 'ExchangeMicroscopicDynamics', 'ExchangeModularCost']
BUILD = ROOT / "CONTINUACAO055_CLEAN_BUILD.json"
AUDITOR = ROOT / "audit_continuation055.py"
RUNNER = ROOT / "clean_continuation055.py"
REVIEW = ROOT / "CONTINUACAO055_REVISAO_INDEPENDENTE.md"
INFRA_REVIEW = ROOT / "CONTINUACAO055_REVISAO_INFRA_ROOT.md"
REPORT = ROOT / "CONTINUACAO055_PARECER.md"
DELIVERY = ROOT / "TUNEL/DO_CHATGPT/ENTREGA_055_troca_conservada_e_entropia_regional.md"
DERIVATIONS = ['CONTINUACAO055_DERIVACAO_PREVIA.md', 'DERIVACAO055_INFRA.md', 'DERIVACAO055_ENTROPIA.md', 'DERIVACAO055_DINAMICA.md', 'DERIVACAO055_CUSTO.md']
ORDER010 = ROOT / (
    "TUNEL/PARA_CHATGPT/"
    "ORDEM_010_horizontes_concretos_aperiodico_e_o_relogio_apos_a_obstrucao.md"
)
REQUIRED_DECLARATIONS = {'ExchangeEntropyResponse': ['exchange_first_law', 'exchange_relative_quadratic_zero', 'exchange_entropy_quadratic_limit', 'exchange_coefficient_zero_iff', 'exchange_coefficient_reference', 'exchange_coefficient_reference_pos'], 'ExchangeMicroscopicDynamics': ['exchange_unitary_eq_boundedPhase', 'exchange_marginal0', 'exchange_marginal1', 'exchange_heat0_formula', 'exchange_heat1_formula', 'exchange_generator_conserves_energy', 'exchange_total_energy_conserved', 'exchange_current0_commutator', 'exchange_current1_commutator', 'exchange_currents_cancel', 'exchange_heat0_current_derivative', 'exchange_heat1_current_derivative', 'exchange_weight0_formula', 'exchange_weight1_formula'], 'ExchangeModularCost': ['exchange_modular_matrix_split', 'exchange_generator_global_cost', 'exchange_modular_energy_increment', 'exchange_pair_entropy_cost_limit', 'exchange_heat_matching_iff', 'exchange_no_common_heat_rate', 'exchange_measured_pair_entropy_cost_limit', 'exchange_actual_first_law', 'exchange_state_not_preserved']}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def unique_object(pairs):
    result = {}
    for name, value in pairs:
        if name in result:
            raise RuntimeError("Duplicate JSON key: " + name)
        result[name] = value
    return result


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"),
                      object_pairs_hook=unique_object)


def record(path):
    path = Path(path).resolve(strict=True)
    raw = path.read_bytes()
    return {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def link(path, label=None):
    path = Path(path).resolve(strict=True)
    return "[" + (label or path.name) + "](<" + path.as_posix() + ">)"


def output_link(path):
    if path not in (REPORT, DELIVERY):
        raise RuntimeError("Unknown prospective output")
    return "[" + path.name + "](<" + path.as_posix() + ">)"


def new_bytes(path, raw):
    if path.exists() or not path.resolve().is_relative_to(ROOT) or not raw:
        raise RuntimeError("Exclusive nonempty output required: " + str(path))
    if not path.parent.is_dir():
        raise RuntimeError("Output parent must already exist")
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.stat().st_size != len(raw) or temporary.read_bytes() != raw or path.exists():
        raise RuntimeError("Temporary verification failed")
    temporary.rename(path)
    if path.read_bytes() != raw:
        raise RuntimeError("Final verification failed")


def documentary_inputs():
    paths = [
        *[ROOT / name for name in DERIVATIONS],
        *sorted(ROOT.glob("DERIVACAO055_*.md")),
        *sorted(ROOT.glob("NOTA055_*.md")),
        *sorted(ROOT.glob("CONTINUACAO055_REVISAO_*.md")),
        *[ROOT / (name + ".lean") for name in MODULES],
        ROOT / "CONTINUACAO045_UPSTREAM.json",
        ROOT / "CONTINUACAO054_MANIFESTO.json",
        ROOT / "CONTINUACAO054_CLEAN_BUILD.json",
        ORDER010, RUNNER, AUDITOR, Path(__file__).resolve(), BUILD, REVIEW, INFRA_REVIEW,
    ]
    result, seen = [], set()
    for path in paths:
        actual = path.resolve(strict=True)
        key = os.path.normcase(str(actual))
        if key not in seen:
            result.append(actual)
            seen.add(key)
    return result


def require_stable(snapshot):
    for expected in snapshot:
        if record(expected["path"]) != expected:
            raise RuntimeError("Documentary input changed: " + expected["path"])
    if [os.path.normcase(str(p)) for p in documentary_inputs()] != [
            os.path.normcase(row["path"]) for row in snapshot]:
        raise RuntimeError("Documentary input inventory changed")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if sys.argv[1:]:
        raise RuntimeError("This generator accepts no arguments")
    if REPORT.exists() or DELIVERY.exists():
        raise RuntimeError("Reports already exist; exclusive creation refused")
    inputs = documentary_inputs()
    before = [record(path) for path in inputs]
    result = subprocess.run(
        [sys.executable, "-B", str(AUDITOR), "--build-only"],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stdout.decode("utf-8", errors="replace"))
    audit = json.loads(result.stdout.decode("utf-8"), object_pairs_hook=unique_object)
    if (audit.get("status") != "BUILD_PASS" or audit.get("sealed") is not False
            or audit.get("canonical_gate_changed") is not False
            or audit.get("modules") != MODULES):
        raise RuntimeError("Auditor did not accept the final055 batch")
    data = read_json(BUILD)
    if (data.get("schema") != "chatgpt.clean055.build.v1"
            or data.get("status") != "PASS" or data.get("development_only") is not False
            or data.get("fresh_clean_build") is not True
            or data.get("source055_copies_exact") is not True
            or data.get("inputs_stable") is not True
            or data.get("modules") != MODULES or data.get("build_order") != MODULES
            or data.get("baseline_modules") != []
            or data.get("integration_module") != "Imports055All"):
        raise RuntimeError("Unexpected final055 build marker")
    if [step["module"] for step in data["steps"]] != MODULES + ["Imports055All"]:
        raise RuntimeError("Missing final serial or integration step")
    clean = Path(data["clean_directory"]).resolve(strict=True)
    if clean.parent != ROOT or not clean.name.startswith("CONTINUACAO055_CLEAN_"):
        raise RuntimeError("Unexpected final directory")
    build_hash = digest(BUILD)
    review_text = REVIEW.read_text(encoding="utf-8-sig")
    if ("BUILD_PASS" not in review_text or "Build SHA256: " + build_hash not in review_text
            or "Diretório final: " + clean.as_posix() not in review_text):
        raise RuntimeError("Independent review does not identify this final build")
    counts = audit["counts"]
    if any(type(counts.get(key)) is not int or counts[key] < 0 for key in
           ("theorems", "definitions", "instances", "axiom_prints")):
        raise RuntimeError("Invalid measured census")
    if counts["axiom_prints"] != counts["theorems"] + counts["definitions"] + counts["instances"]:
        raise RuntimeError("Declaration census does not equal print census")
    sources = data["sources"]
    if [row["module"] for row in sources] != MODULES:
        raise RuntimeError("Unexpected source order")
    measured_counts = {
        "theorems": sum(row["theorems"] for row in sources),
        "definitions": sum(row["definitions"] for row in sources),
        "instances": sum(len(row["instances"]) for row in sources),
        "axiom_prints": sum(len(row["expected_axiom_rows"]) for row in sources),
    }
    if measured_counts != counts or audit["steps"] != len(data["steps"]):
        raise RuntimeError("Auditor/marker census mismatch")
    for row in sources:
        current = ROOT / (row["module"] + ".lean")
        copied = Path(row["source"]).resolve(strict=True)
        if copied.parent != clean or current.read_bytes() != copied.read_bytes():
            raise RuntimeError("Current source differs from audited local copy")
        required = {"ChatgptAudit.Exchange055." + name
                    for name in REQUIRED_DECLARATIONS[row["module"]]}
        if not required <= set(row["expected_axiom_rows"]):
            raise RuntimeError("A declaration needed by the report is absent: " + row["module"])
    require_stable(before)
    timestamp = datetime.now(timezone.utc).isoformat()
    meanings = {'ExchangeEntropyResponse': 'Curvas regionais fiéis, primeira lei, limites pelo passado e sinal do coeficiente.', 'ExchangeMicroscopicDynamics': 'Troca de excitações, órbita unitária literal, marginais efetivas e corrente conservada.', 'ExchangeModularCost': 'Mesmo custo054, incremento modular, resposta entrópica regional e normalização necessária do calor.'}
    table = [
        "| Módulo055 | Teoremas | Definições | Instâncias | Prints | Alcance |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in sources:
        table.append(
            f"| {link(ROOT / (row['module'] + '.lean'))} | {row['theorems']} | "
            f"{row['definitions']} | {len(row['instances'])} | "
            f"{len(row['expected_axiom_rows'])} | {meanings[row['module']]} |"
        )
    table_text = "\n".join(table)
    steps = len(data["steps"])
    review_notes = [path for path in inputs if path.name.startswith("CONTINUACAO055_REVISAO_")]
    reviews_text = "; ".join(link(path) for path in review_notes)
    report = f"""# Continuação055 — corrente conservada e entropia regional

[REAL — alcance das declarações compiladas e auditadas] Emissão UTC: {timestamp}

A055 constrói uma transferência de energia conservada entre os dois primeiros sítios da torre fiel e identifica suas marginais efetivas. A soma das transferências ponderadas pelos fatores modulares coincide com o incremento do mesmo K local; seu coeficiente quadrático coincide com o custo054 do mesmo vetor GΩ. A área física e a reconstrução gravitacional geral continuam [OPEN].

## Dados e identidade dos objetos

[INPUT] Para qualquer SiteProfile P fixo, p=P.w0 e q=P.w1 estão em (0,1). Escolhemos energias locais com níveis0 e1 e interação

    E0=diag(0,1)⊗I; E1=I⊗diag(0,1);
    G=(X⊗X+Y⊗Y)/2; U(t)=exp(i t G).

O prefixo chainIdx1 tem dois sítios. A dinâmica inteira permanece no mesmo TowerHilbert P. Interação, nível energético unitário e parâmetro t são entradas microscópicas; não foram derivados como energia, tempo de boost ou escala gravitacional físicos.

O módulo de dinâmica prova a fórmula U=I+(cos t−1)G²+i sin t G e sua identificação com boundedPhase no towerPi. As marginais são restrições do estado efetivo ω_t(B)=ω(U*BU), com igualdade para toda matriz2×2 de cada sítio:

    p_t=p+(q−p)sin²t; q_t=q+(p−q)sin²t.
    Q0=Δω(E0)=(p−q)sin²t; Q1=−Q0.

[REAL, no protocolo] A energia nua total se conserva. As correntes i(EjG−GEj) são ligadas às derivadas das expectativas e somam zero. O estado em geral muda quando p≠q; esta órbita não é apresentada como horizonte preservador de ω.

## Entropia, custo e filtros dos limites

Com ν(p)=log p−log(1−p), a primeira lei regional exata é

    S(p_t)−S(p)=ν(p)Q0−D_Bernoulli(p_t||p).

O relativo regional dividido por t² tende a zero pelo passado. As marginais são fiéis em todo t. A soma das entropias REGIONAIS tem coeficiente

    C(p,q)=(p−q)(ν(p)−ν(q))≥0.

Essa soma não é a entropia conjunta; a órbita unitária não deve ser confundida com uma produção de entropia total. O lote não implementa uma nova entropia relativa global de Araki.

O observável054 se decompõe literalmente como K1=−(log p+log q)I+ν(p)E0+ν(q)E1. Por isso:

    Δ<K1>=ν(p)Q0+ν(q)Q1=C(p,q)sin²t;
    towerModularCost P (GΩ)=ofReal(C(p,q)).

O limite entrópico usado é 𝓝[<]0; o limite modular reaproveitado054 é bilateral perfurado 𝓝[≠]0. O coeficiente quadrático é metade da segunda derivada.

C=0 exatamente quando p=q. Na referência estacionária anterior, esta interação tem transferência e custo nulos, embora G não seja zero. O controle p=2/3,q=3/4 tem C=(log3−log2)/12>0, em outro perfil fiel fixo durante a órbita. Não é ajuste de curvatura nem afirmação de corrente não nula na referência estacionária.

## O casamento microscópico com calor permanece uma condição

No contrato Micro021 existente, para a transferência escolhida, o erro é

    heatError=(1−rate·ν(p)/(2π))Q0.

Quando p≠q, hheat é equivalente a rate·ν(p)=2π. Para dois pesos fiéis distintos, um mesmo rate não pode satisfazer os dois contratos. Essa incompatibilidade é restrita ao protocolo e à normalização comum: não proíbe temperaturas regionais distintas, outros estados de equilíbrio ou gravidade quântica. Não se divide por ν no domínio fiel, que inclui p=1/2.

Nada aqui identifica automaticamente Q0 com constructedHeat, fluxo de T_ab sobre a tela ou variação de área. H3 ainda exige identificação física de energia/tempo/temperatura, localização, orientações e o limite harea. A relação nula de Ricci não foi escolhida para obter a igualdade.

## Critérios e verificação

{table_text}

Censo medido: {counts['theorems']} teoremas, {counts['definitions']} definições, {counts['instances']} instâncias nomeadas, {counts['axiom_prints']} prints; {steps}/{steps} etapas PASS, incluindo Imports055All. Zero avisos/erros e cobertura exata de axiomas, limitada a propext, Classical.choice e Quot.sound.

- Derivação anterior ao código, incluindo notas de calor e emissão.
- Mesmos objetos: U explícita=boundedPhase, marginais para toda matriz local, K e custo054 reaproveitados literalmente.
- Corrente e conservação derivadas; escolhas microscópicas declaradas.
- Entropia regional, custo e critério de calor verificados nos filtros e hipóteses dos enunciados.
- Casos iguais e controle distinto preservados, sem parâmetros geométricos ajustados.
- Revisão científica independente: {link(REVIEW)}. Revisões cruzadas: {reviews_text}.
- Dependências históricas, incluindo054, pinadas e copiadas; não recompiladas neste lote. Imports externos diretos e companheiros medidos, sem alegar fecho transitivo externo exaustivo.
- Fontes anteriores/canônicos/memórias não receberam escritas desta emissão. Tentativas intermediárias e backups permaneceram como evidência, sem promoção a build final.

Diretório final: {clean.as_posix()}

Build SHA256: {build_hash}

Auditor: {link(AUDITOR)}; runner: {link(RUNNER)}; marcador: {link(BUILD)}. A emissão documental não é o selo: o auditor --seal cria depois o manifesto exclusivo e revalida os dados.

H3=OPEN; physical_reconstruction=OPEN; broad_quantum_gravity_goal=OPEN; canonical_gate_changed=false. NOT_FALSIFIED não é CONFIRMED.
"""
    require_stable(before)
    new_bytes(REPORT, report.encode("utf-8"))
    report_record = record(REPORT)
    artifacts = [REPORT, REVIEW, INFRA_REVIEW, BUILD, RUNNER, AUDITOR,
                 *[ROOT / (name + ".lean") for name in MODULES]]
    hash_rows = ["| Artefato | Bytes | SHA256 |", "|---|---:|---|"]
    for path in artifacts:
        item = record(path)
        hash_rows.append(f"| {link(path)} | {item['bytes']} | {item['sha256']} |")
    delivery = f"""# Entrega055 — troca conservada e entropia regional

[REAL — alcance compilado e auditado] Emissão UTC: {timestamp}

A055 liga corrente microscópica conservada, marginais efetivas e o mesmo custo054, no protocolo de troca G=(X⊗X+Y⊗Y)/2 entre os dois primeiros sítios da torre fiel. A interação, o nível energético e o tempo são [INPUT], sem escolha de geometria para ajustar o resultado.

    Q0=(p−q)sin²t, Q1=−Q0;
    ΔS0=ν(p)Q0−D(p_t||p);
    C=(p−q)(ν(p)−ν(q))≥0;
    Δ<K1>=C sin²t e towerModularCost(GΩ)=ofReal(C).

U explícita é provada igual a boundedPhase; as marginais são leituras da mesma órbita para toda matriz local. Os limites entrópicos são pelo passado; o modular é bilateral perfurado. C=0 se e somente se p=q, portanto a referência estacionária anterior não apresenta corrente para esta interação. O controle não estacionário2/3,3/4 dá (log3−log2)/12>0.

No próprio contrato Micro021, para p≠q, hheat exige rate·ν(p)=2π. Dois pesos fiéis distintos não admitem o mesmo rate nos dois contratos. Isso não é proibição de normalizações regionais diferentes nem fechamento da física de H3.

{table_text}

Total: {counts['theorems']}T/{counts['definitions']}D/{counts['instances']}I/{counts['axiom_prints']} prints; {steps}/{steps} etapas PASS. Critérios e limites no {link(REPORT)}; revisão científica final em {link(REVIEW)}.

Diretório final: {clean.as_posix()}

Build SHA256: {build_hash}

## Artefatos medidos
{chr(10).join(hash_rows)}

As dependências históricas, incluindo054, são fixadas por hash e copiadas, não reconstruídas aqui. Fronteira externa medida nos imports diretos e companheiros. O manifesto055 é emitido separadamente após estes documentos. Verificação posterior somente leitura:

    "{sys.executable}" -B "{AUDITOR}"

[OPEN] Localização física, fluxo material/boost/temperatura, escala dimensional, área e harea, H3, assinatura e reconstrução gravitacional geral. Não há confirmação física nem alteração do gate nesta emissão. NOT_FALSIFIED não é CONFIRMED.
"""
    require_stable(before)
    if record(REPORT) != report_record:
        raise RuntimeError("Report changed before delivery")
    new_bytes(DELIVERY, delivery.encode("utf-8"))
    require_stable(before)
    if record(REPORT) != report_record:
        raise RuntimeError("Report changed during delivery")
    print(json.dumps({"status":"REPORTS_CREATED","report":record(REPORT),
                      "delivery":record(DELIVERY),"counts":counts,
                      "build_sha256":build_hash},ensure_ascii=False))

if __name__ == "__main__":
    main()
