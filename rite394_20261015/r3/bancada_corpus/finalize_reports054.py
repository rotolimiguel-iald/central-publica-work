"""Create exclusive continuation054 reports after final audit and linked review.

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
MODULES = [
    "PolarizerModularCost",
    "PolarizerCostSeries",
    "TowerModularCost",
    "ModularCostDerivative",
]
BUILD = ROOT / "CONTINUACAO054_CLEAN_BUILD.json"
AUDITOR = ROOT / "audit_continuation054.py"
RUNNER = ROOT / "clean_continuation054.py"
REVIEW = ROOT / "CONTINUACAO054_REVISAO_INDEPENDENTE.md"
INFRA_REVIEW = ROOT / "CONTINUACAO054_REVISAO_INFRA_NEWTON.md"
REPORT = ROOT / "CONTINUACAO054_PARECER.md"
DELIVERY = ROOT / "TUNEL/DO_CHATGPT/ENTREGA_054_custo_modular_do_polarizador.md"
DERIVATIONS = [
    "CONTINUACAO054_DERIVACAO_PREVIA.md",
    "DERIVACAO054_INFRA.md",
    "DERIVACAO054_GENERICO.md",
    "DERIVACAO054_SERIE.md",
    "DERIVACAO054_TORRE.md",
    "DERIVACAO054_DERIVADA.md",
]
ORDER010 = ROOT / (
    "TUNEL/PARA_CHATGPT/"
    "ORDEM_010_horizontes_concretos_aperiodico_e_o_relogio_apos_a_obstrucao.md"
)
REQUIRED_DECLARATIONS = {
    "PolarizerModularCost": [
        "polarizerModularCost", "polarizerCostDomain",
        "polarizer_modular_cost_smul", "polarizer_modular_cost_zero_iff",
        "polarizer_modular_cost_covariant", "polarizer_cost_domain_covariant",
        "polarizer_modular_cost_eq_of_hasSum", "polarizer_modular_cost_lowerSemicontinuous",
    ],
    "PolarizerCostSeries": [
        "polarizer_cost_hasSum", "polarizer_cost_weights_hasSum",
        "polarizer_cost_scalar_ennreal", "polarizer_cost_of_weight_norm_powers",
    ],
    "TowerModularCost": [
        "tower_modular_cost_centralizer", "tower_modular_cost_response_kernel",
        "tower_modular_cost_covariant", "tower_modular_domain_covariant",
        "tower_local_mem_cost_domain", "tower_cost_domain_dense_real",
        "tower_local_cost_symmetric_formula",
        "first_pauli_modular_cost", "double_flip_modular_cost",
    ],
    "ModularCostDerivative": [
        "unitary_energy_second_derivative", "quadratic_response_from_velocity",
        "finite_modular_energy_first_zero", "local_modular_double_coefficient",
        "finite_modular_energy_second", "finite_modular_energy_quadratic_limit",
        "global_cost_is_modular_response",
    ],
}


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
        *sorted(ROOT.glob("DERIVACAO054_*.md")),
        *sorted(ROOT.glob("NOTA054_*.md")),
        *sorted(ROOT.glob("CONTINUACAO054_REVISAO_*.md")),
        *[ROOT / (name + ".lean") for name in MODULES],
        ROOT / "CONTINUACAO045_UPSTREAM.json",
        ROOT / "CONTINUACAO053_MANIFESTO.json",
        ROOT / "CONTINUACAO053_CLEAN_BUILD.json",
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
        raise RuntimeError("Auditor did not accept the final054 batch")
    data = read_json(BUILD)
    if (data.get("schema") != "chatgpt.clean054.build.v1"
            or data.get("status") != "PASS" or data.get("development_only") is not False
            or data.get("fresh_clean_build") is not True
            or data.get("source054_copies_exact") is not True
            or data.get("inputs_stable") is not True
            or data.get("modules") != MODULES or data.get("build_order") != MODULES
            or data.get("baseline_modules") != []
            or data.get("integration_module") != "Imports054All"):
        raise RuntimeError("Unexpected final054 build marker")
    if [step["module"] for step in data["steps"]] != MODULES + ["Imports054All"]:
        raise RuntimeError("Missing final serial or integration step")
    clean = Path(data["clean_directory"]).resolve(strict=True)
    if clean.parent != ROOT or not clean.name.startswith("CONTINUACAO054_CLEAN_"):
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
        required = {"ChatgptAudit.Cost054." + name
                    for name in REQUIRED_DECLARATIONS[row["module"]]}
        if not required <= set(row["expected_axiom_rows"]):
            raise RuntimeError("A declaration needed by the report is absent: " + row["module"])
    require_stable(before)
    timestamp = datetime.now(timezone.utc).isoformat()
    meanings = {
        "PolarizerModularCost": "Custo estendido, domínio real finito, escala, radical, covariância e semicontinuidade inferior.",
        "PolarizerCostSeries": "Série convergente do logaritmo, ambos os sinais, pesos positivos e passagem para ENNReal.",
        "TowerModularCost": "Mesmo D global053, domínio denso no setor real, custo local e dois controles sem normalizar o segundo vetor.",
        "ModularCostDerivative": "Derivadas da curva unitária efetiva e limite quadrático ligados ao mesmo custo local.",
    }
    table = [
        "| Módulo054 | Teoremas | Definições | Instâncias | Prints | Alcance |",
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
    review_notes = [path for path in inputs if path.name.startswith("CONTINUACAO054_REVISAO_")]
    reviews_text = "; ".join(link(path) for path in review_notes)
    report = f"""# Continuação054 — custo modular pelo polarizador global

[REAL — alcance das declarações compiladas e auditadas] Emissão UTC: {timestamp}

A054 constrói um custo não negativo estendido a partir do mesmo polarizador real global D da053. Prova o domínio de custo finito, sua densidade no setor real pertinente, a semicontinuidade inferior e a covariância por todos os TowerHorizon do mesmo perfil. Nos vetores locais autoadjuntos, o custo coincide com o coeficiente quadrático da variação da energia modular de uma curva unitária efetiva. H3, área física e reconstrução gravitacional geral permanecem [OPEN].

## Objeto, domínio e alcance real

Para um Hilbert real H e D:H→L[ℝ]H, definir:

    C_D(x) = Σ_(n≥0) ofReal( 2/(2n+1) · ‖D^(n+1)x‖² ) ∈ ℝ≥0∞,
    Dom(C_D) = {{x : C_D(x)<∞}}.

Uma série divergente conserva o valor infinito; não é convertida em zero por uma soma real totalizada. Não se supõe ‖D‖<1 globalmente. Mesmo a cota ‖D‖≤1 não garante custo finito para todo vetor.

Os teoremas provam C_D(a x)=ofReal(a²)C_D(x), a estimativa de adição que torna Dom(C_D) um submódulo REAL e C_D(x)=0↔Dx=0. Também provam semicontinuidade inferior de C_D com valores estendidos. Uma isometria linear real bijetiva que entrelaça D preserva o custo, inclusive quando infinito, e o domínio finito.

Na torre, D é literalmente statePolarizer P=P_R(−i)P_R, com R=realStateSubspace P construído na053. A implementação GNS W_h de cada h:TowerHorizon P entrelaça D. Logo:

    C_D(W_h x)=C_D(x), para todo x;
    W_h x∈Dom(C_D) ↔ x∈Dom(C_D).

Para A autoadjunto e pertencente ao fator M, o custo de AΩ é zero exatamente quando A pertence ao centralizador de ω, equivalentemente quando todas as respostas reais infinitesimais do estado em testes autoadjuntos são zero. A classificação não é afirmada para operadores arbitrários fora desse setor.

Os vetores locais autoadjuntos têm custo finito, e as esperanças de prefixo aproximam AΩ. O resultado formal de densidade é:

    closure(Dom(C_D) ∩ R)=R.

É densidade na topologia Hilbert. O lote não demonstra que os vetores locais formam um núcleo da forma, nem anuncia uma forma quadrática fechada, uma polarização bilinear global ou um operador não limitado associado. A semicontinuidade inferior e o domínio não são usados para encobrir essas distinções.

## A série e o cálculo dos cortes

Para |d|<1, incluindo d=0 e d<0, a série REAL é somável e satisfaz:

    Σ_(n≥0) 2 d^(2n+2)/(2n+1) = d[log(1+d)−log(1−d)].

A prova usa a série ímpar do logaritmo já demonstrada na Mathlib. Somente após provar somabilidade e não negatividade dos termos a soma é transportada para ENNReal.

Para wi,wj>0, tomar d=(wi−wj)/(wi+wj). Então |d|<1 e o valor é d(log wi−log wj). A identidade não divide por d; pesos iguais não são excluídos.

No prefixo N, os pesos wi=towerW P N i e a matriz local a=a* pertencem à mesma torre. A053 já liga D à matriz de entradas i·dij·aij. A054 itera essa identidade e calcula a norma GNS:

    ‖D^n(towerPi(a)Ω)‖² = Σ_j Σ_i wj · dij^(2n) · |aij|².

Distribuir a série pelas somas finitas e usar a autoadjunção dá:

    C_D(towerPi(a)Ω)
      = ofReal( 1/2 · Σ_i Σ_j (wi−wj)(log wi−log wj)|aij|² ).

O fator 1/2 pertence à soma sobre pares ORDENADOS. Cada par não ordenado contribui uma vez. Nenhuma densidade trace-class global é introduzida para essa igualdade.

## Derivada efetiva e fator dois

Fixar K_N=towerPi(diag(−log wi)), A=towerPi(a), U(t)=exp(i t A) e:

    f(t)=Re ω(U(t)* K_N U(t)).

A exponencial e a regra do produto fornecem as derivadas; o custo não é definido como uma derivada escolhida. A primeira derivada no zero é zero porque a densidade diagonal do corte comuta com K_N. A segunda derivada usa:

    −A²K_N + 2 A K_N A − K_N A².

A soma matricial é precisamente:

    f''(0)=2·localModularCost(P,N,a),
    lim_(t→0, t≠0) [f(t)−f(0)]/t²=localModularCost(P,N,a).

O limite bilateral é provado por L'Hôpital com as derivadas efetivas e a primeira derivada nula. Em consequência, C_D(AΩ)=ofReal(f''(0)/2). Isso liga o custo global avaliado no vetor local à leitura de energia modular do MESMO corte. Não é apenas a coincidência de dois números definidos separadamente.

K_N é um observável limitado do corte finito. O resultado não identifica um logΔ global com domínio, não define uma entropia relativa global de Araki e não toma a entropia diagonal por entropia total. A leitura formalizada aqui é a variação de energia; outras interpretações requerem suas próprias definições e pontes.

## Dois vetores fixos da053

Na referência estacionária thirdThermalReference, com p=1/3, os controles preservam os mesmos vetores:

| Vetor | Norma GNS ao quadrado | Custo |
|---|---:|---:|
| X₁Ω, Pauli no primeiro sítio | 1 | log2/3 |
| X₂Ω, flip00↔11 no prefixo de dois sítios | 5/9 | 2log2/3 |

O segundo vetor permanece bruto, sem normalização para norma um. O custo distingue as duas frequências. O perfil de referência é estacionário e periódico; o uso de construções gerais da torre não o transforma em perfil aperiódico.

A053 provou insuficiência de covariância mais uma calibração comum para selecionar uma forma. A054 fornece uma expressão que reproduz a resposta energética local. Esse requisito é um critério matemático adicional. O lote não prova unicidade entre todas as formas que coincidam num conjunto apenas Hilbert-denso; tal inferência exigiria hipóteses adicionais de núcleo e continuidade pertinentes.

## O que permanece aberto

[OPEN] Interpretar esse custo como calor físico ou área de horizonte, selecionar regiões e observadores físicos, fixar escala dimensional e relacionar estado, tela, matéria, relógio e curvatura sem ajustes destinados a impor o balanço. Os contratos microscópicos hheat/harea e a reconstrução gravitacional geral não são consequências desta série.

C_D não é inducedArea nem constructedHeat por definição. A054 não escolhe mass, η ou curvatura para forçar uma igualdade. Também não transforma a ação de todo TowerHorizon de um perfil em uma localização física já selecionada.

## Verificação, falhas anteriores e custódia

{table_text}

Total054: {counts['theorems']} teoremas, {counts['definitions']} definições, {counts['instances']} instâncias nomeadas, {counts['axiom_prints']} prints. Lote final: {steps}/{steps} etapas, incluindo Imports054All. O auditor verificou cobertura exata, zero avisos/erros, ausência de sorryAx e somente propext, Classical.choice e Quot.sound nos prints.

Diretório final: {clean.as_posix()}

Build SHA256: {build_hash}

O auditor mediu separadamente {audit['build_files']} arquivos do build e {audit['historical_records']} registros históricos. Esses números não são somados como conjuntos disjuntos. Os quatro fontes054 foram copiados por bytes e compilados em diretório exclusivo. Dependências históricas pinadas, incluindo053, foram verificadas e copiadas; não foram recompiladas neste lote. Os imports externos diretos e seus companheiros são medidos, sem alegar reconstrução exaustiva de todo o fecho externo.

As tentativas intermediárias não foram todas aprovadas: houve falhas de elaboração e ajustes antes do lote final. Seus marcadores, logs e backups permanecem como história, sem valor de prova, e integram a coleta histórica da custódia quando presentes. Somente o build final ligado ao hash acima sustenta esta emissão.

A revisão final deve identificar literalmente esse build e seu diretório; o gerador recusa sua ausência ou divergência. A autoria e a revisão cruzada são documentadas na nota, não autenticadas semanticamente pelo parser. Notas de revisão disponíveis: {reviews_text}. A nota de infraestrutura {link(INFRA_REVIEW)} registra inspeção do contrato, reexecução histórica e controles da instrumentação; não é um BUILD_PASS final nem aprovação científica dos módulos. Seu alcance datado não é ampliado retroativamente pela presente emissão.

Parecer e entrega são novos, de criação exclusiva, e seus hashes são lidos dos bytes. A selagem ocorre separadamente após os documentos. Esta emissão não altera originais, Atlas, um.py, kernel ou memórias canônicas; canonical_gate_changed=false descreve o escopo das escritas, não uma auditoria de alterações de terceiros. Não se declara QG confirmada, resolvida ou provada.

Revisão final: {link(REVIEW)}. Entrega: {output_link(DELIVERY)}.
"""
    require_stable(before)
    new_bytes(REPORT, report.encode("utf-8"))
    report_record = record(REPORT)
    artifacts = inputs + [REPORT.resolve(strict=True)]
    hash_rows = ["| Artefato | Bytes | SHA256 lido dos bytes |", "|---|---:|---|"]
    for path in artifacts:
        item = record(path)
        hash_rows.append(f"| {link(path)} | {item['bytes']} | {item['sha256']} |")
    delivery = f"""# Entrega054 — custo modular do polarizador

[REAL — alcance compilado e auditado] Emissão UTC: {timestamp}

A054 constrói, do mesmo D global053, o custo estendido:

    C_D(x)=Σ_(n≥0) ofReal(2‖D^(n+1)x‖²/(2n+1)).

A divergência permanece infinita. O domínio finito é um submódulo real; seu encontro com o setor real R é Hilbert-denso em R. O custo é semicontínuo inferior e preservado por todos os TowerHorizon do mesmo perfil, por meio da implementação GNS efetiva. Para A autoadjunto no fator, custo zero equivale ao centralizador e ao núcleo das respostas reais do estado.

Nos cortes fiéis, a série convergente prova:

    C_D(aΩ)=ofReal(1/2 Σij (wi−wj)(log wi−log wj)|aij|²).

O fator 1/2 refere-se à soma ordenada. Para a curva efetiva U(t)=exp(i t towerPi(a)) e a leitura f(t)=Reω(U(t)*K_N U(t)), K_N=towerPi(diag(−log wi)), o lote prova f'(0)=0, f''(0)=2·localModularCost e o limite [f(t)−f(0)]/t² igual a localModularCost. Logo C_D(aΩ)=ofReal(f''(0)/2).

Os mesmos vetores da referência p=1/3 dão C_D(X₁Ω)=log2/3 e C_D(X₂Ω)=2log2/3. O segundo vetor é bruto, com norma GNS ao quadrado 5/9. Esse é um custo energético local demonstrado, sem identificação com área física ou calor construído.

{table_text}

Total054: {counts['theorems']}T/{counts['definitions']}D/{counts['instances']}I/{counts['axiom_prints']} prints; {steps}/{steps} etapas PASS. Zero avisos/erros, cobertura exata e somente o trio de axiomas permitido. Parecer: {link(REPORT)}. Revisão final: {link(REVIEW)}.

Diretório final: {clean.as_posix()}

Build SHA256: {build_hash}

## Artefatos medidos

{chr(10).join(hash_rows)}

As dependências históricas foram pinadas e copiadas, não recompiladas nesta rodada; a cadeia inclui053. A fronteira externa é medida nos imports diretos e companheiros, não em todo o fecho transitivo. As sondas intermediárias com falhas e os respectivos backups são preservados como histórico; não se confundem com o lote final aprovado.

A selagem é separada desta emissão e cria CONTINUACAO054_MANIFESTO.json somente depois dos documentos. Verificação posterior do selo, apenas leitura:

    C:\\Python314\\python.exe -B "{AUDITOR}"

[OPEN] Forma fechada e núcleo da forma não são anunciados. Tampouco entropia relativa global de Araki, logΔ global, área física, escala dimensional, região↔álgebra, hheat/harea, H3 ou reconstrução gravitacional geral. Coincidência em conjunto Hilbert-denso não é anunciada como unicidade entre todas as formas. Somente Chatgpt recebe as escritas desta emissão; originais e selos anteriores permanecem intactos. NOT_FALSIFIED não é CONFIRMED.
"""
    require_stable(before)
    if record(REPORT) != report_record:
        raise RuntimeError("Report changed before delivery")
    new_bytes(DELIVERY, delivery.encode("utf-8"))
    require_stable(before)
    if record(REPORT) != report_record:
        raise RuntimeError("Report changed during delivery creation")
    print(json.dumps({
        "status": "REPORTS_CREATED",
        "report": str(REPORT), "report_bytes": REPORT.stat().st_size,
        "report_sha256": digest(REPORT),
        "delivery": str(DELIVERY), "delivery_bytes": DELIVERY.stat().st_size,
        "delivery_sha256": digest(DELIVERY), "hash_table_rows": len(artifacts),
        "counts": counts, "build_sha256": build_hash,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
