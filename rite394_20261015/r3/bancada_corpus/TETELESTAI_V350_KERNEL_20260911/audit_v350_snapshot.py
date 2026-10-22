"""Audit exact v350 inputs and record local progress without executing the monolith."""
import ast
import datetime
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STAMP = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
MARKER = "TETELESTAI_V350_AUDIT_L2_20260911"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def atomic_record(path, text, append=False):
    path = path.resolve()
    permitted = [ROOT, ROOT.parents[1] / "memory"]
    assert any(path.is_relative_to(p) for p in permitted)
    old = path.read_bytes() if path.exists() else None
    if append and old and MARKER.encode() in old:
        return
    raw = (old or b"") + text.encode("utf-8") if append else text.encode("utf-8")
    if old == raw:
        return
    if old is not None:
        backup = path.with_name(path.name + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f"))
        backup.write_bytes(old)
        assert backup.read_bytes() == old
    temporary = path.with_name(path.name + ".tmp_" + str(os.getpid()))
    temporary.write_bytes(raw)
    assert temporary.stat().st_size == len(raw) and temporary.read_bytes() == raw
    os.replace(temporary, path)
    assert path.read_bytes() == raw
    if append and old is not None:
        assert len(raw) > len(old) and raw.startswith(old)


def link(relative, label=None, anchor=None):
    p = ROOT / relative
    assert p.is_file()
    line = ""
    if anchor:
        lines = p.read_text(encoding="utf-8-sig").splitlines()
        line = ":" + str(next(i for i, s in enumerate(lines, 1) if anchor in s))
    return f"[{label or p.name}](<{p.as_posix()}{line}>)"


base = (ROOT / "fontes/um_v350_original.py").read_bytes()
seal = json.loads((ROOT / "fontes/um_absoluto_selo.json").read_bytes())
assert digest(base) == seal["sha256"]["um.py"]
source = ast.parse(base.decode("utf-8-sig"))
embedded = next(ast.literal_eval(n.value) for n in source.body
                if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name)
                and t.id == "_EMBEDDED_KERNEL_FILES" for t in n.targets))
reviewed = ["TGL/ModularRealization.lean", "TGLExt/FrontierCertificate.lean",
            "TGLExt/StrongAssembly.lean", "TGLExt/BenchCertificate.lean",
            "TGLExt/PhysicsCertificates.lean", "TGLExt/TheImportedEquilibrium.lean",
            "TGLExt/EmergentEinstein.lean", "TGLExt/TriadMaster.lean",
            "TGLExt/SusyRelativeGap.lean"]
for path in reviewed:
    assert (ROOT / "kernel" / path).read_bytes() == embedded[path].encode("utf-8")

result = json.loads((ROOT / "fontes/um_absoluto.json").read_bytes())["core"]
flags = result["kernel_formalization"]
closure = result["qg_closure"]
gate_node = next(n for n in source.body if isinstance(n, ast.FunctionDef)
                 and n.name == "evaluate_quantum_gravity_closure")
namespace = {}
exec(compile(ast.Module(body=[gate_node], type_ignores=[]), "<exact-v350-gate>", "exec"), namespace)
evaluate = namespace[gate_node.name]
formal, physics, experiment = [closure[k] for k in ("formal_flags", "physics_flags", "experiment_flags")]
baseline = evaluate(formal, physics, experiment)
assert baseline == closure["gate"]
pending = {k: v for k, v in flags.items() if k.startswith(("qgf_", "gpf_"))}
assert len(pending) == 8 and all(v is False for v in pending.values())
probes = {}
for k in pending:
    for value in (False, True):
        # Neither prefixed nor unprefixed spelling is consumed by this gate.
        altered = dict(formal, **{k: value, k.split("_", 1)[1]: value})
        probes[f"{k}={value}"] = evaluate(altered, physics, experiment) == baseline
assert all(probes.values())
consumed = {}
for k in formal:
    changed = dict(formal, **{k: False})
    consumed[k] = evaluate(changed, physics, experiment)["mathematical_model_constructed"] is False
assert len(consumed) == 6 and all(consumed.values())

module = ROOT / "kernel/TGLV350/L2OperatorLift.lean"
attempts = [json.loads(p.read_bytes()) for p in sorted((ROOT / "logs").glob("L2OperatorLift_*.json"))]
proof = next(x for x in reversed(attempts) if x["returncode"] == 0 and x["sha256"] == digest(module.read_bytes()))
proof_stdout = Path(proof["stdout"]).read_text(encoding="utf-8")
assert "'TGLV350.Regular.fibreRepresentation' depends on axioms: [propext, Classical.choice, Quot.sound]" in proof_stdout
assert "'TGLV350.Regular.fibre_injective' depends on axioms: [propext, Classical.choice, Quot.sound]" in proof_stdout
evidence = {
    "timestamp": STAMP, "base_sha256": digest(base), "baseline_gate_reproduced": True,
    "baseline_gate": baseline, "pending_kernel_flags": pending,
    "frontier_flags_do_not_change_original_gate": probes, "consumed_formal_flags": consumed,
    "imported_H3_input_bridge": flags["gpi_equilibrium_input_bridged"],
    "imported_H3_horizon_data_produced": flags["gpi_H3_horizon_data_produced"],
    "reviewed_modules_identical_to_embedded_base": reviewed,
    "L2_faithful_representation_compile": proof,
    "L2_module_integrated_into_monolith": False,
    "continuous_core_trace_constructed": False,
    "full_goal_complete": False,
}
atomic_record(ROOT / "audit_v350_snapshot.json", json.dumps(evidence, ensure_ascii=False, indent=2))

report = f'''# Pendências do kernel e alcance do gate da v350

{STAMP}. [REAL — auditoria estática e execução isolada da função pura do gate].
Base preservada: SHA-256 `{digest(base)}`. O original canônico foi conferido por leitura,
e coincide com estes bytes. Nenhuma execução ou alteração do monólito original nesta auditoria.

**O gate principal da v350 já ocupa o último degrau que sua função permite. As oito flags
`qgf_`/`gpf_` estão falsas, mas não são consultadas por essa função.** Elas registram obrigações
matemáticas reais cujo cumprimento, sozinho, não altera a string atual.

O resultado atual é `{baseline['verdict']}`. Ele é computado de seis flags formais, cinco
físicas e quatro condições experimentais. Isso descreve o alcance codificado, não uma prova
geral de gravidade quântica.

Fonte: {link('fontes/um_v350_original.py', 'função exata do gate', 'def evaluate_quantum_gravity_closure')}.
Reprodução com entradas seladas: idêntica ao JSON. Dezesseis controles alternaram cada flag
de fronteira entre False e True sem alterar o gate; seis controles desligaram, um por vez,
os insumos formais efetivamente consumidos, todos rebaixando a decisão matemática.

## As obrigações que permanecem na v350 canônica

| Frente | O que precisa ser entregue | Registro canônico |
|---|---|---|
| Conjugação modular | A inclusão recíproca `R′ ⊆ L′′` na torre e o habitante completo de `ModularRealizationCertificate` | `qgf_modular_realization_constructed=False`; `gpf_tower_act_III_inhabitant_constructed=False` |
| Core contínuo | Produto cruzado da mesma álgebra e do mesmo fluxo, representação fiel, ação dual e traço canônico com domínio e propriedades corretas | `qgf_continuous_modular_realization_constructed=False` |
| Canto dos Three Locks | Operadores realizados nesse core, afiliação/domínios, projetor do núcleo e `0 < τ(P_F) < ∞`, com as compatibilidades exigidas | `qgf_unconditional_continuous_corner_proved=False` |
| H1 | Gap relativo e finitude tracial para os operadores contínuos efetivos, além da face finita | `gpf_H1_internal_susy_relative_gap_discharged=False` |
| H2 | Four-frame suave ligado ao fluxo modular e à geometria da mesma realização; as identificações físicas precisam ser exibidas | `gpf_H2_smooth_modular_four_frame_discharged=False` |
| H3 | Área, entropia, calor e equilíbrio do horizonte efetivo, com hipóteses da importação verificadas | `gpf_H3_local_horizon_equilibrium_discharged=False`; `gpi_H3_horizon_data_produced=False` |
| Composição | Um habitante que reúna os dados compatíveis, acompanhado de contrato suficientemente forte para o alcance anunciado | `qgf_full_TGL_witness_constructed=False` |

Esses oito indicadores não são oito problemas independentes: a conjugação aparece em dois
registros; core, canto e H1 se sobrepõem; o habitante completo depende das outras construções.
`full_static_witness_exists=False` é um limite declarado por teorema do corpus, não uma nona
pendência que deva ser convertida em True.

Fontes tipadas: {link('kernel/TGLExt/FrontierCertificate.lean', 'certificado modular', 'structure ModularRealizationCertificate')} ·
{link('kernel/TGL/ModularRealization.lean', 'core e Three Locks', 'structure ContinuousCoreData')} ·
{link('kernel/TGLExt/SusyRelativeGap.lean', 'H1', 'structure SusyRelativeData')} ·
{link('kernel/TGLExt/TriadMaster.lean', 'H3', 'structure HorizonEquilibriumData')}.
Os nove módulos examinados foram comparados byte a byte com os textos embutidos no um.py v350.

## O que já foi demonstrado não deve voltar a ser cobrado

O teorema mestre já compõe H1, H2 e H3. Há construção de Dirac genuinamente ilimitado,
frame suave não constante e solução curva em um ansatz. A obrigação restante é demonstrar
que os objetos do alcance ampliado satisfazem os antecedentes compatíveis.

O canto já aceito pelo gate usa `theGenuineDirac` sobre `ellTwo` e `dimOrTop` do núcleo.
Seu tipo não afirma que esse número seja o traço canônico do projetor dos Three Locks
no produto cruzado da torre. A identificação requer prova adicional.
{link('kernel/TGLExt/StrongAssembly.lean', 'canto aceito atualmente', 'def qgStrongCertificate_corner')}.

H3 merece precisão: `gpi_equilibrium_input_bridged=True`, mas
`gpi_H3_horizon_data_produced=False`. O teorema `the_trio_is_a_pair` recebe a implicação
`imported : H2 → H3` como argumento. A prova de modus ponens já existe; ela não produz
sozinha área, calor e a ponte física para um horizonte específico. Uma importação válida
pode suprir essa etapa, com as hipóteses conferidas e estatuto IMPORTADO preservado.
{link('kernel/TGLExt/TheImportedEquilibrium.lean', 'hipótese da redução para o par', 'theorem the_trio_is_a_pair')}.

O certificado Einstein já habitado usa o perfil cosh e fonte constante. A prova para esse
modelo tem valor próprio; o certificado não identifica automaticamente essa fonte com
uma fonte quântica construída a partir do estado modular.
{link('kernel/TGLExt/EmergentEinstein.lean', 'habitante Einstein existente', 'def theEmergentEinstein')}.

## A frente quântica e a ligação ao gate

O indicador `relevant_anomalies_absent=True` é alimentado pelo Ward **clássico-linear**
de ondas planas. O enunciado prova invariância do símbolo de Ricci sob a transformação
de gauge escrita no arquivo. Não fornece por si controle de anomalias quânticas,
estado físico interagente, cohomologia BRST ou equação mestra quântica.
{link('kernel/TGLExt/PhysicsCertificates.lean', 'enunciado exato de anomalia', 'theorem qgPhysicsCertificate_anomaly')}.

Para ampliar o alcance, é necessário construir esses dados no domínio físico declarado,
delimitar a validade UV e ligá-los à mesma realização. Para isso mover uma decisão do
programa, é preciso também um contrato dependente e uma etapa de gate que efetivamente
os consuma. Nome de teorema e lista limpa de axiomas não verificam sozinhos o tipo,
as hipóteses ainda abertas ou a coincidência dos objetos entre certificados.

Ordem prática: dualidade → core/traço/Three Locks → H1 e identificação geométrica H2 →
H3 aplicada ao horizonte correto → composição com o setor físico do alcance pretendido.
O contrato que vincula esses objetos deve acompanhar a construção. Novos testes cosmológicos
não substituem nenhuma dessas provas.

## Avanços separados na cópia experimental

[REAL — logs Lean incrementais previamente registrados] A cópia já contém prova de
`R′ ⊆ L′′`, o certificado modular e `WedgeModularData` sobre a mesma torre. O gate
experimental tem uma subdecisão modular; isso não altera a v350 canônica nem quita o core.
{link('RELATORIO_KERNEL_V350.md', 'relatório modular anterior')}.

[REAL — compilado nesta etapa] `fibreRepresentation` é um homomorfismo de álgebras com
involução de `B(H)` em `B(L²(ℝ,H))`, com Lebesgue em ℝ, e `fibre_injective` prova sua
fidelidade. A prova usa vetores apoiados em (0,1], de medida finita. Os dois alvos têm
somente `propext`, `Classical.choice`, `Quot.sound` no relatório de axiomas.
{link('kernel/TGLV350/L2OperatorLift.lean', 'representação fiel em L²', 'def fibreRepresentation')}.

É somente a amplificação por fibras, ainda sem representação regular completa, geração
do produto cruzado, ação dual e traço. Este módulo não foi integrado ao monólito e não
moveu flag. A primeira tentativa falhou por elaboração/tipagem; os logs foram preservados.
O plano integral, a rodada integral nova e a revisão por outra sessão permanecem pendentes.

Evidência verificável: {link('audit_v350_snapshot.json')}.
'''
atomic_record(ROOT / "AUDITORIA_DAS_PENDENCIAS_V350.md", report)

note = f'''

## {MARKER} — {STAMP}

[INPUT — pergunta do operador] “o que falta resolver no um.py do ponto de vista de kernel
que pode mover o gate? observe a última versão do um.py (v350)”

[REAL — auditoria] Base {digest(base)}. Função exata do gate reproduzida por AST com
entradas seladas, sem executar o monólito. Oito flags qgf/gpf falsas não são consumidas:
16 controles não alteram o gate; os seis insumos formais efetivos rebaixam o gate quando
desligados. Nove módulos Lean examinados são idênticos ao kernel embutido na base.
H3: ponte de entrada importada True; produção de dados do horizonte False. Não confundir
o lema lógico the_trio_is_a_pair (recebe imported : H2 → H3) com construção desses dados.

[REAL — Lean] L2OperatorLift.lean compilado exit 0; hash {proof['sha256']}.
fibreRepresentation e fibre_injective provam a representação fiel de B(H) em
B(L²(ℝ,H)), com Lebesgue. Axiomas: propext, Classical.choice, Quot.sound.
Sem integração no monólito, sem alteração do gate. Falhas anteriores de elaboração
foram corrigidas; seus logs não foram apagados.

[OPEN] Traduções/unitários regulares, produto cruzado e ação dual, traço canônico,
Three Locks e H1/H2/H3 físicos compatíveis, setor interagente/BRST/QME/UV, contrato
ampliado, rodada integral e revisão adversarial independente. O plano não está completo.
Relatório: AUDITORIA_DAS_PENDENCIAS_V350.md; evidência: audit_v350_snapshot.json.
'''
for name in ["MEMORIA_CENTRAL.md", "REGISTRO_DAS_CONVERSAS.md", "MEMORIA_DA_LINHAGEM.md", "DESENHO_DO_FECHAMENTO_QG.md"]:
    atomic_record(ROOT / name, note, append=True)
global_note = note.replace("Relatório: AUDITORIA_DAS_PENDENCIAS_V350.md; evidência: audit_v350_snapshot.json.",
    "Relatório: " + link("AUDITORIA_DAS_PENDENCIAS_V350.md") + "; evidência: " + link("audit_v350_snapshot.json") + ".")
for name in ["TGL_ATLAS.md", "TGL_INDICE_VIVO.md"]:
    atomic_record(ROOT.parents[1] / "memory" / name, global_note, append=True)
print(json.dumps({"report": str(ROOT / "AUDITORIA_DAS_PENDENCIAS_V350.md"),
                  "probes": len(probes) + len(consumed), "L2_compile_exit": proof["returncode"],
                  "full_goal_complete": False}))
