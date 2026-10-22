"""Write a new evidence-bound handoff after the live integration build passes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
COPY = BASE / "COPIA_INTEGRADA_20260909_150458_780534"
BUILD = COPY / "BUILD_TRANSPOSED_20260909_150513_725803"


def record(path):
    data = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def write_new(path, data):
    assert path.resolve().is_relative_to(BASE) and not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == data
    os.rename(temp, path)
    assert path.read_bytes() == data


def link(label, path, line=None):
    target = path.as_posix() + (f":{line}" if line else "")
    return f"[{label}](<{target}>)"


def main():
    result_path = BUILD / "TRANSPOSED_RESULT.json"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    assert result["status"] == "PASS_TRANSPOSED_SCOPE"
    assert len(result["runs"]) == 48
    assert all(run["valid"] and run["exit_code"] == 0 for run in result["runs"])
    assert result["input_boundary_unchanged"]
    assert not result["um_py_executed"]
    warnings = sum(run["warning_lines"] for run in result["runs"])
    assert warnings == 0
    integration_path = COPY / "INTEGRATION_RESULT.json"
    integration = json.loads(integration_path.read_text(encoding="utf-8"))
    audit_path = COPY / "AUDITORIA_INDEPENDENTE/AUDITORIA_ESTATICA_INTEGRACAO.json"
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    assert audit["status"] == "PASS_STATIC_INTEGRATION_SCOPE"
    assert audit["counts"]["checks"] == audit["counts"]["passed_checks"] == 618
    current_copy = record(COPY / "um.py")
    snapshot = record(COPY / "um_ORIGINAL_SNAPSHOT.py")
    assert current_copy == integration["integrated_copy"] == audit["integrated"]
    assert snapshot == integration["original_copy"] == audit["snapshot"]
    assert audit["current_canonical"]["sha256"] == snapshot["sha256"]
    modules = integration["modules"]
    assert len(modules) == 45
    theorem_names = integration["theorem_names"]
    assert len(theorem_names) == len(set(theorem_names)) == 653
    total = sum(len(module["declarations"]) for module in modules)
    assert total == 853
    fresh_names = {"GravitationalChartGluing", "TopologicalAtlasGluing", "SelectedAtlasGluing",
                   "SelectedGravitationalAtlas", "LieMetricJets", "LeviCivitaLieVariation",
                   "RicciLieNaturality", "MetricEinsteinVariation", "SummablePauliInteraction",
                   "PauliInteractionWitness", "AdmissiblePauliInteraction",
                   "ScalarEinsteinLieNaturality", "EulerMetricPullback"}
    fresh = [module for module in modules if module["module"] in fresh_names]
    fresh_theorems = sum(item["kind"] == "theorem" for module in fresh for item in module["declarations"])
    fresh_other = sum(len(module["declarations"]) for module in fresh) - fresh_theorems
    assert (len(fresh), fresh_theorems, fresh_other) == (13, 162, 43)
    for module in modules:
        assert record(Path(module["source"]["path"])) == module["source"]
        assert record(Path(module["build_result"]["path"])) == module["build_result"]
    dedicated = next(run for run in result["runs"] if run["module"] == "NewModulesAudit")
    assert {row["name"] for row in dedicated["axiom_rows"]} == set(theorem_names)
    assert all(set(row["axioms"]) <= {"propext", "Classical.choice", "Quot.sound"}
               for run in result["runs"] for row in run["axiom_rows"])

    selected = BASE / "ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean"
    gluing = BASE / "COLAGEM_GRAVITACIONAL_20260909_142505_750002/SelectedAtlasGluing.lean"
    lie = BASE / "NATURALIDADE_ESCALAR_EINSTEIN_20260909_145442_429378/ScalarEinsteinLieNaturality.lean"
    euler = BASE / "PULLBACK_EULER_LIE_20260909_145850_073045/EulerMetricPullback.lean"
    interaction = BASE / "INTERACAO_LOCAL_SOMAVEL_20260909_143042_266556/AdmissiblePauliInteraction.lean"
    empirical = BASE / "REEXAME_FONTE_GERAL_20260909_133220_037525/LASTRO_EMPIRICO_LIDO.md"
    report_path = OUT / "REEXAME_FINAL_V337_E_COPIA45.md"
    report = f"""# Reexame v337 e continuação formal — 09/09/2026

[REAL — escopo verificado] A base canônica lida é a v337. A bancada integra 45 módulos próprios, com 653 teoremas e 200 outras declarações, em uma nova cópia do programa. Desses, esta continuação acrescentou 13 módulos, 162 teoremas e 43 outras declarações aos 32 módulos anteriores. Nenhum original foi alterado; nenhum `um.py` foi executado ou importado.

## O que deixou de faltar

1. **Reconstrução a partir do caráter completo.** A continuidade dos registros, uma sequência densa no domínio e os cortes racionais tornam completas as observações codificadas. O caráter canônico separa as classes dos registros e sua inversa na imagem recupera os mesmos campos g e T em todo o aberto U. A preparação de 48 resultados é preservada. O teorema transporta a equação de Einstein do registro original para o reconstruído, usando as relações de área e conservação do original. {link('Fonte e hipóteses', selected, 291)}.
2. **Uma constante cosmológica nas cartas compatíveis.** A conexão por sobreposições é derivada de uma cobertura aberta de espaço preconexo. A não nulidade da métrica força a igualdade das constantes locais; resulta uma única constante válida nas cartas decodificadas. Há um caráter por carta. As hipóteses de compatibilidade de g, T e Einstein constam expressamente do enunciado. {link('Composição seleção–cartas', gluing)}.
3. **Naturalidade infinitesimal em uma carta curva.** As derivadas reais de Levi-Civita, Ricci, escalar e Einstein foram calculadas. Para h = Lie_V g, obteve-se δRic = Lie_V Ric, δR = V(R) e δG = Lie_V G. A última identidade inclui a variação da inversa e dos dois fatores em (R/2)g. {link('Naturalidade de Einstein', lie, 215)}. A direção h é também a derivada do pullback métrico efetivo por phi_t(x)=x+tV(x), cujo Jacobiano espacial foi provado: {link('Pullback e Jacobiano', euler)}.
4. **Potencial de interação concreto.** No Hilbert/fator canônicos foi construído V = Σ c_j X_j X_(j+1), para coeficientes reais com certificado de Σ|c_j| finita. V é auto-adjunto, pertence ao fator e seus cortes convergem em norma, com erro limitado pela cauda dos coeficientes. O exemplo de um vínculo tem duplo comutador bipartido não nulo; no perfil não tracial indicado, está fora do centralizador. {link('Interface com somabilidade certificada', interaction)}.
5. **Registro de fase e ramo.** Os módulos anteriores desta bancada continuam incluídos. No peso 1/2, o registro completo distingue o ramo mesmo quando o ângulo de peso coincide. A inversa vale na imagem admissível do registro; não inverte uma operação irreversível depois de apagar essa informação.

Também não se deve reabrir genericamente a positividade/auto-adjunticidade de JS: o snapshot v337 já contém `continuous_modular_positive_square_root`, com domínio, positividade, auto-adjunticidade e quadrado Δ no objeto formal especificado. A correspondência com um fluxo físico tem escopo próprio. A caracterização acrescentada na v337 (`TheNameIsTheCharacterization`) foi preservada integralmente.

## O que permanece aberto, precisamente

| Frente | O que já existe | Obrigação ainda necessária |
|---|---|---|
| Seleção física → registro | Decodificador exato da classe e instância concreta de `IALDState` | Ligar esse caráter e essa seleção ao processo físico e ao seletor operatorial pretendidos. A escolha de representante do quociente não foi identificada automaticamente com a projeção original em ℓ². |
| Área, calor e matéria | Preparação explícita, respostas que recuperam T e teorema Einstein condicional | Justificar ou postular explicitamente a lei de correspondência entre as respostas, a fonte física, a área induzida das telas e a conservação. A hipótese de erro de área o(t²) permanece visível. |
| Geometria global | Igualdade de constantes em cobertura conectada; naturalidade infinitesimal | Construir a compatibilidade de um atlas diferenciável completo: matrizes de transição como Jacobianos, consistência nas interseções e transformação finita de Einstein. `hmatch` ainda recebe essa transformação finita. |
| Interação quântica | Potencial limitado auto-adjunto e limite em norma | Construir o cociclo da dinâmica perturbada e seu estado apropriado, identificar observáveis e fonte gravitacional, e demonstrar as propriedades físicas requeridas. Os vínculos XX comutam entre si; a não comutatividade atestada refere-se a observáveis locais/centralizador. |
| Alcance quântico geral | Setores lineares e cálculos clássicos novos | Completar o setor de perturbações gerais pretendido, tratar as anomalias da teoria interagente e justificar a rota de altas energias adotada. A convergência em número de sítios não constitui, por si, limite ultravioleta relativista. |

[INPUT/OPEN] O caráter completo usa infinitas observações exatas e escolhas clássicas não computáveis. O teorema prova identificabilidade matemática na imagem declarada. Não fornece uma capacidade experimental finita nem estabilidade a erro de medida. Essa limitação não anula a inversa demonstrada; delimita sua aplicação.

[DERIVED — suficiência condicional] Admitindo explicitamente as correspondências físicas, a regularidade, as telas/lei de área, a conservação e as compatibilidades de transição listadas, a cadeia agora entrega os campos reconstruídos e a equação G + Λg = (2π/η)T, com Λ único no recobrimento conectado. Esse é o lastro formal deste setor. As obrigações quânticas interagentes e UV não aparecem como consequências desse teorema.

## Próximo trabalho que pode reduzir as pendências

A próxima folha quântica deve construir o cociclo do potencial certificado, demonstrar unitariedade/composição e controlar sua aproximação pelos cortes. Uma estimativa de Duhamel em termos de |t| vezes a cauda dos coeficientes é um alvo concreto, após precisar a dinâmica modular de base. Depois vem o estado perturbado e sua ligação às respostas/T. No setor geométrico, a próxima folha deve substituir a hipótese de transformação finita de Einstein por um teorema de mudança de coordenadas. Essas conclusões não foram declaradas como demonstradas neste lote; a transformação finita permanece em `hmatch`.

## Evidências de integração e limites de execução

[REAL] {len(result['runs'])}/{len(result['runs'])} processos Lean aprovados: 45 módulos transpostos, raiz TGLExt, auditoria TGL completa e auditoria dedicada dos 653 teoremas novos. Zero avisos; nenhuma dependência axiomática fora de `propext`, `Classical.choice` e `Quot.sound` nas linhas auditadas. Entradas medidas estáveis ao final. {link('Recibo da compilação conjunta', result_path)}.

[REAL] A auditoria estática independente passou 618/618 verificações. Os 606 arquivos embutidos tornaram-se 651; especificamente, 602 fontes Lean tornaram-se 647. Fora da tabela embutida, bytes e AST são idênticos. Entre as entradas antigas, somente a raiz e a auditoria receberam acréscimos. Flags, sentinelas, gate e lógica Python não foram alterados; não foram acrescentadas flags JSON individuais. {link('Auditoria independente', COPY / 'AUDITORIA_INDEPENDENTE/RELATORIO_AUDITORIA_INDEPENDENTE.md')}.

O build recompilou as fontes novas transpostas e as raízes/auditorias citadas, usando cópias de bytes das dependências locais canônicas e binários Mathlib existentes. Não recompilou todas as fontes transitivas e não executou o programa, os ritos empíricos ou uma nova custódia. Portanto, a integração do kernel não equivale a uma rodada completa do `um.py`.

Snapshot v337: {snapshot['bytes']} bytes; SHA-256 `{snapshot['sha256']}`.

Cópia integrada: {current_copy['bytes']} bytes; SHA-256 `{current_copy['sha256']}`. {link('um.py de trabalho', COPY / 'um.py')}.

## Contorno empírico e preservação

Os critérios que contrariam previsões já existem no programa; este reexame não os tratou como ausentes. Nenhum teste empírico novo foi realizado nesta continuação. Os resultados anteriores e seus estados distintos estão em {link('lastro empírico lido', empirical)}. A evidência intermediária v337 que reutiliza ritos não foi convertida em nova execução completa. `NOT_FALSIFIED` permanece distinto de `CONFIRMED` e não demonstra que todos os dados públicos foram esgotados.

Este documento sucede o mapa inicial da continuação: a linha que dizia “naturalidade de Einstein em construção” descrevia o estado anterior e está superada pelo PASS registrado aqui. Também esclarece a contagem: 606 era o total de arquivos embutidos, incluindo quatro arquivos que não são `.lean`.

Atlas, índice, diário e memórias canônicas permanecem somente leitura por ordem do operador. Este registro novo e a entrega no túnel conservam o progresso para a sessão que mantém o canônico, sem alterar o acervo originário. Não houve publicação, selo novo ou promoção do gate.

## Inventário para incorporação

| Módulo | Teoremas | Outras declarações |
|---|---:|---:|
"""
    for module in modules:
        theorems = sum(item["kind"] == "theorem" for item in module["declarations"])
        report += f"| {module['module']} | {theorems} | {len(module['declarations']) - theorems} |\n"
    report += "\nOs caminhos, hashes e recibos individuais constam do INTEGRATION_RESULT.json da cópia e foram relidos pelo script que emitiu este relatório.\n"
    write_new(report_path, report.encode("utf-8"))
    evidence = [result_path, BUILD / "BUILD_PLAN.json", integration_path,
                COPY / "CONFIG_APROVADA.json", audit_path,
                OUT / "AUDITORIA_ESTATICA_CONTINUACAO.json",
                OUT / "ADENDO_EVIDENCIA_EINSTEIN_LIE.json", report_path]
    manifest = {"status": "PASS_CONSOLIDATED_WORKING_COPY_SCOPE",
                "created_utc": datetime.now(timezone.utc).isoformat(),
                "snapshot": snapshot, "integrated_copy": current_copy,
                "modules": 45, "theorems": 653, "other_declarations": 200,
                "new_this_continuation": {"modules": 13, "theorems": 162, "other_declarations": 43},
                "processes_passed": 48, "warnings": warnings,
                "independent_static_checks_passed": 618,
                "evidence": [record(path) for path in evidence],
                "canonical_modified": False, "um_py_executed_or_imported": False,
                "all_transitive_sources_rebuilt": False, "empirical_tests_run": False,
                "gate_promoted": False, "qg_goal_complete": False}
    manifest_path = OUT / "ENTREGA_CONSOLIDADA.json"
    write_new(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    tunnel = BASE / "TUNEL/DO_CHATGPT"
    numbers = [int(match.group(1)) for path in tunnel.iterdir()
               if (match := re.match(r"ENTREGA_(\d+)", path.name))]
    number = max(numbers, default=0) + 1
    handoff_path = tunnel / f"ENTREGA_{number:03d}_ESPONTANEA_reexame_v337_copia45.md"
    handoff = f"""# Entrega {number:03d} — reexame v337 e cópia integrada de 45 módulos

09/09/2026. [REAL — bancada auditada; não é nova versão canônica nem nova rodada de natureza.]

{link('Relatório completo e pendências', report_path)} · {link('Manifesto com hashes medidos', manifest_path)} · {link('Cópia um.py', COPY / 'um.py')}.

Base v337 exata; 45 módulos, 653 teoremas, 200 outras declarações. Esta continuação acrescentou 13 módulos/162 teoremas/43 outras declarações. Build conjunto: 48/48 processos PASS, zero avisos. Auditoria estática independente: 618/618. Arquivos embutidos: 606→651; fontes Lean: 602→647. Flags/gate/Python fora da tabela intactos.

Avanços: caráter completo reconstrói g/T/Einstein condicionado à área e conservação; colagem fornece Λ único nas cartas compatíveis; naturalidade infinitesimal de Ricci/escalar/Einstein em carta curva e direção de pullback efetivo; potencial XX somável auto-adjunto com cauda em norma e exemplo de acoplamento atestado.

Pendências: correspondência da seleção física e das respostas/área; compatibilidades finitas de atlas; cociclo/estado da interação e ligação à fonte; perturbações quânticas gerais, anomalias e rota UV. O caráter usa dados exatos infinitos, um por carta, e seleção de representante; não foi automaticamente identificado com o seletor operatorial original.

Para incorporar, usar CONFIG_APROVADA.json e INTEGRATION_RESULT.json; se o canônico avançar além deste snapshot, refazer o delta antes de compor. A cópia não foi executada/importada, não tem novas flags individuais nem selo. O build usa dependências locais copiadas e binários existentes, sem rebuild transitivo completo. Nenhum original ou memória canônica foi alterado; documentação nova somente em Chatgpt.

SHA-256 da cópia lido: `{current_copy['sha256']}`.
"""
    write_new(handoff_path, handoff.encode("utf-8"))
    receipt_path = OUT / "RECIBO_ENTREGA_FINAL.json"
    write_new(receipt_path, (json.dumps({"report": record(report_path),
        "manifest": record(manifest_path), "handoff": record(handoff_path)},
        ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"status": manifest["status"], "report": report_path.as_posix(),
                     "handoff": handoff_path.as_posix(), "manifest": manifest_path.as_posix()}, ensure_ascii=True))


if __name__ == "__main__":
    main()
