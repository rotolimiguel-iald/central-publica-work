"""Publish a new local handoff from verified build and audit receipts only."""
from pathlib import Path
from datetime import datetime, timezone
import ast
import hashlib
import json
import os
import re
import sys

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def record(path):
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest()}


def write_new(path, raw):
    assert path.resolve().is_relative_to(BASE) and not path.exists()
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    os.rename(temp, path)
    assert path.read_bytes() == raw


def link(label, path, line=None):
    target = path.as_posix() + (f":{line}" if line else "")
    return f"[{label}](<{target}>)"


def main():
    assert len(sys.argv) == 4, "Pass copy folder, transposed receipt and independent copy audit."
    copy_folder, result_path, audit_path = [Path(arg).resolve() for arg in sys.argv[1:]]
    assert all(path.is_relative_to(BASE) for path in [copy_folder, result_path, audit_path])
    inventory = read(OUT / "INVENTARIO_FONTES.json")
    counts = inventory["counts"]
    total, fresh = counts["total"], counts["new_this_continuation"]
    integration_path = copy_folder / "INTEGRATION_RESULT.json"
    integration = read(integration_path)
    result = read(result_path)
    audit = read(audit_path)
    assert integration["status"] == "AST_AND_EMBEDDED_ROUND_TRIP_PASSED__NOT_EXECUTED"
    assert result["status"] == "PASS_TRANSPOSED_SCOPE"
    assert audit["status"] == "PASS_STATIC_INTEGRATION_SCOPE"
    assert audit["counts"]["checks"] == audit["counts"]["passed_checks"]
    assert not audit.get("failed_checks", [])
    cached = result["cached_modules"]
    assert len(cached) + fresh["modules"] == total["modules"]
    assert result["cached_boundary_unchanged"]
    cached_receipt_path = Path(result["cached_build_receipt"]["path"])
    assert record(cached_receipt_path) == result["cached_build_receipt"]
    prior_build = read(cached_receipt_path)
    assert prior_build["status"] == "PASS_TRANSPOSED_SCOPE"
    assert len(prior_build["runs"]) == len(cached) + 3
    assert all(run["valid"] and run["exit_code"] == 0 and run["warning_lines"] == 0
               for run in prior_build["runs"])
    assert all(module["source_bytes_identical"] and module["prior_run"]["valid"]
               and module["prior_run"]["exit_code"] == 0 for module in cached)
    assert len(result["runs"]) == fresh["modules"] + 3
    new_names = {run["module"] for run in result["runs"][:-3]}
    cached_names = {module["module"] for module in cached}
    assert not new_names & cached_names
    assert new_names | cached_names == {module["module"] for module in integration["modules"]}
    assert all(run["valid"] and run["exit_code"] == 0 for run in result["runs"])
    assert sum(run["warning_lines"] for run in result["runs"]) == 0
    assert all(set(row["axioms"]) <= TRIO for run in result["runs"] for row in run["axiom_rows"])
    assert result["input_boundary_unchanged"] and not result["um_py_executed"]
    canonical = record(Path(inventory["canonical"]["path"]))
    assert canonical == inventory["canonical"]
    integrated = record(copy_folder / "um.py")
    snapshot = record(copy_folder / "um_ORIGINAL_SNAPSHOT.py")
    assert integrated == integration["integrated_copy"] == audit["integrated"]
    assert snapshot == integration["original_copy"] == audit["snapshot"]
    assert canonical["sha256"] == snapshot["sha256"] == audit["current_canonical"]["sha256"]
    assert all(integration[key] for key in ["outside_embedded_table_ast_identical",
        "outside_embedded_table_bytes_unchanged", "existing_sources_unchanged_except_root_and_audit",
        "sentinels_flags_and_gate_code_unchanged"])
    assert not integration["new_individual_json_flags_added"]
    modules = integration["modules"]
    assert len(modules) == total["modules"]
    assert len(integration["theorem_names"]) == total["theorems"]
    assert sum(len(module["declarations"]) for module in modules) == total["theorems"] + total["other_declarations"]
    for module in modules:
        assert record(Path(module["source"]["path"])) == module["source"]
        assert record(Path(module["build_result"]["path"])) == module["build_result"]
    dedicated = next(run for run in result["runs"] if run["module"] == "NewModulesAudit")
    assert {row["name"] for row in dedicated["axiom_rows"]} == set(integration["all_declaration_names"])

    def embedded_counts(path):
        tree = ast.parse(path.read_bytes().decode("utf-8"))
        tables = [node.value for node in tree.body if isinstance(node, ast.Assign) and
                  any(isinstance(target, ast.Name) and target.id == "_EMBEDDED_KERNEL_FILES"
                      for target in node.targets)]
        assert len(tables) == 1
        embedded = ast.literal_eval(tables[0])
        return len(embedded), sum(key.endswith(".lean") for key in embedded)
    old_files, old_lean = embedded_counts(copy_folder / "um_ORIGINAL_SNAPSHOT.py")
    new_files, new_lean = embedded_counts(copy_folder / "um.py")
    assert old_files == integration["old_embedded_file_count"]
    assert new_files == integration["new_total_embedded_file_count"]
    assert new_lean - old_lean == total["modules"]

    quantum = BASE / "DUHAMEL_UNITARIO_20260909_153247_640286"
    dynamics = BASE / "DINAMICA_MODULAR_PERTURBADA_20260909_155658_929243/PauliPerturbedDynamics.lean"
    finite = BASE / "COORDENADAS_FINITAS_20260909_153310_253904/FiniteEinsteinNaturality.lean"
    selection = BASE / "ATLAS_GRAVITACIONAL_SELECIONADO_20260909_143404_511881/SelectedGravitationalAtlas.lean"
    atlas = BASE / "COLAGEM_GRAVITACIONAL_20260909_142505_750002/SelectedAtlasGluing.lean"
    empirical = BASE / "REEXAME_FONTE_GERAL_20260909_133220_037525/LASTRO_EMPIRICO_LIDO.md"
    report_path = OUT / "REEXAME_ATUALIZADO_V337_COCICLO_E_COVARIANCIA.md"
    report = f"""# Reexame atualizado — cociclo interagente e covariância finita

09/09/2026. [REAL — escopo formal auditado] O canônico consultado permanece v337, com {canonical['bytes']} bytes e SHA-256 `{canonical['sha256']}`. A leitura final confirmou o mesmo conteúdo. A bancada acrescenta {fresh['modules']} módulos, {fresh['theorems']} teoremas e {fresh['other_declarations']} outras declarações, incluindo instâncias nomeadas. A nova cópia reúne {total['modules']} módulos próprios e {total['theorems']} teoremas. Nenhum `um.py` foi executado ou importado.

## Duas pendências do relatório anterior foram reduzidas

**O cociclo da interação somável foi construído.** Para coeficientes reais certificados por Σ|c_j| < ∞, o potencial V = Σ c_j X_j X_(j+1) atua no Hilbert canônico e pertence ao fator. Os Hamiltonianos modulares finitos são definidos a partir dos logaritmos dos pesos reais da torre. A igualdade entre sua ação e a ação modular canônica foi demonstrada nos níveis correspondentes. A diferença entre Hamiltonianos de níveis distintos comuta com os operadores do nível menor; esse resultado elimina o termo espectador sem supor que V comute com a dinâmica de base.

Os cortes u_N(t) = exp(it(H_N + V_N)) exp(−itH_N) satisfazem a lei torcida da ação canônica. Duhamel fornece controle por |t| vezes a cauda somável. Isso produz um limite em norma, uniforme em intervalos compactos de tempo, sem introduzir sua existência como hipótese. O limite u(t) é unitário, pertence ao fator, é contínuo e satisfaz

`u(s+t) = u(s) α_s(u(t)),    u(0) = 1.`

Sua derivada também foi deduzida dos cortes e do erro linear:

`u′(0) = iV,    u′(t) = u(t) α_t(iV).`

O gerador fica à direita nessa convenção. Para a escolha de um vínculo `singleBondData`, a testemunha prova que o cociclo não é identicamente 1; não afirma ausência de retornos em tempos particulares. {link('Construção do limite concreto', quantum / 'PauliInteractionCocycle.lean')} · {link('Gerador e equação de evolução', quantum / 'PauliCocycleGenerator.lean')}.

Daí foi construída a família efetiva `β_t(A) = u(t) α_t(A) u(t)*`: automorfismos que preservam produto, adjunto, norma e fator, com composição β_s β_t = β_(s+t) e inversa β_(−t). A continuidade temporal foi demonstrada nas órbitas cuja continuidade canônica é conhecida, incluindo V. Não se afirmou continuidade temporal em norma para todo B(H). {link('Dinâmica perturbada', dynamics)}.

**A transformação finita de Einstein foi deduzida.** O resultado trata de métrica Lorentziana suave em dimensão quatro, com Levi-Civita sem torção. Para uma mudança suave invertível φ entre abertos, J = Dφ e g′ = Jᵀ(g∘φ)J, foram demonstradas a transformação de Levi-Civita, a de curvatura, a contração de Ricci, a invariância do escalar e

`G[g′] = Jᵀ (G[g]∘φ) J.`

O resultado também vale quando g′ coincide com esse pullback no aberto de sobreposição. Igualdade métrica em um único ponto não é a hipótese usada: são necessárias as derivadas, daí o acordo no aberto. {link('Transformação finita e sobreposição', finite)}. Isso fornece uma prova para a componente Einstein da antiga premissa `hmatch`, sob condições geométricas explícitas. O teorema anterior de colagem ainda conserva seu enunciado; o novo lema fornece condições suficientes para aplicar aquela componente, não constrói sozinho um atlas completo. {link('Contrato da colagem', atlas)}.

## O que ainda falta

| Frente | Pendência precisa após estes resultados |
|---|---|
| Seleção e informação física | Identificar o caráter completo usado pelo decodificador com a seleção física e com o seletor operatorial pretendido. A inversa formal recupera a classe admissível de g e T, usando informação exata infinita, codificada por amostras densas e cortes racionais, em cada domínio/carta; falta a correspondência operacional e o controle para dados finitos com erro. |
| Área, matéria e gravitação | Ligar a interação/estado e as respostas do registro à fonte física T, à área induzida das telas e à conservação. A condição de erro de área o(t²) continua sendo hipótese do teorema geral. Dimensão quatro, assinatura lorentziana e atribuição física região–andar permanecem com seus estatutos próprios. |
| Estado quântico perturbado | Construir ou importar com hipóteses verificadas o estado/funcional apropriado, sua normalização e a identificação modular/KMS pretendida. Um cociclo unitário da ação modular não foi aqui identificado com o cociclo Connes–Radon–Nikodym de um estado normalizado. Uma fase central de normalização pode ser invisível à fórmula Ad_u. |
| Atlas global | Fornecer mudanças suaves reais entre as cartas selecionadas, compatibilidade métrica no aberto e compatibilidade da matéria; conferir a consistência nas interseções. A lei finita de transformação de Einstein já está demonstrada e deixa de ser uma obrigação independente sob essas condições. |
| Alcance quântico geral | Ampliar a classe XX somável ao setor geral reivindicado, tratar anomalias da teoria interagente e justificar a rota de altas energias. Os vínculos XX entre si comutam; a interação atestada envolve observáveis locais. O limite em número de sítios com potencial limitado não é, por si, uma construção do limite ultravioleta relativista. |

[DERIVED — suficiência condicional] O teorema de reconstrução do caráter já devolve os campos e a equação de Einstein para parâmetro do caráter t ≠ 0, domínio aberto não vazio preconexo, registro admissível, telas e η ≠ 0, quando as hipóteses de área, conservação e regularidade são satisfeitas. A nova covariância finita permite derivar a transformação de Einstein de dados usuais de transição suave. O novo cociclo fornece dinâmica interagente concreta na classe certificada. A ligação entre essas duas construções e a correspondência física listada acima ainda não foi demonstrada. {link('Hipóteses da reconstrução', selection, 291)}.

Não se reabre genericamente H3 como escolha de tela: o índice registra a resposta do operador sobre a tela fundada. A identificação física com horizonte causal e a extensão além das cunhas têm escopo próprio. Também não se reabre JS positivo auto-adjunto: o snapshot contém `continuous_modular_positive_square_root`, com o domínio do objeto formal especificado. A indicação antiga de raiz aberta no índice vivo está superada pela fonte.

## Falsificadores e suficiência do lastro

Os resultados que contrariam previsões já constam do programa. Este reexame os reconhece e não exige sua criação novamente. Nenhum rito empírico novo foi executado aqui. Os registros lidos distinguem canais com poder, canais armados, pendentes de revelação, não identificáveis e uma formulação retirada; não autorizam dizer que todos os dados públicos possíveis foram submetidos a testes completos independentes. {link('Resultados e critérios efetivamente lidos', empirical)}.

O lastro formal pode ser declarado suficiente para os enunciados e hipóteses acima. O lastro empírico pode ser declarado nos canais e sensibilidades registrados. Essas delimitações não exigem esperar todos os dados futuros; evitam ampliar a conclusão além da evidência presente. `NOT_FALSIFIED` permanece distinto de `CONFIRMED`. Nenhum gate foi promovido.

## Entrega, verificação e preservação

[REAL] A compilação conjunta aprovou {len(result['runs'])}/{len(result['runs'])} processos, incluindo os {fresh['modules']} módulos novos transpostos, a raiz TGLExt e as duas auditorias. Os {len(cached)} módulos anteriores foram reutilizados do build aprovado de {len(prior_build['runs'])} processos, após comparação exata das fontes e dos pins de dependência. A raiz e a auditoria dedicada carregam os {total['modules']} módulos juntos; a auditoria dedicada verifica todas as {total['theorems'] + total['other_declarations']} declarações, incluindo as instâncias nomeadas. Zero avisos. As declarações auditadas não dependem de axiomas além de `propext`, `Classical.choice` e `Quot.sound`. {link('Recibo do build conjunto', result_path)}.

[REAL] A auditoria estática independente aprovou {audit['counts']['passed_checks']}/{audit['counts']['checks']} verificações. Os arquivos embutidos passaram de {integration['old_embedded_file_count']} para {integration['new_total_embedded_file_count']}; especificamente, as fontes Lean passaram de {old_lean} para {new_lean}. Fora da tabela embutida, bytes e AST permanecem idênticos ao canônico. Entre entradas antigas, somente raiz e auditoria receberam acréscimos. Flags, gate e sentinelas foram preservados; não foram criadas flags JSON individuais. {link('Auditoria independente', audit_path)}.

Esta verificação incremental usa as fontes novas transpostas e cópias de bytes de dependências locais, com os binários Mathlib existentes. Os hashes dos binários das 45 folhas reaproveitadas foram medidos na reutilização; o recibo anterior certificava as execuções e fontes, mas não fixava hashes dos binários produzidos. As fronteiras de entrada e as cópias reutilizadas foram conferidas antes e depois. A tentativa sequencial inicial foi interrompida para esta reutilização e permanece preservada, sem ser contada como um build conjunto concluído. Não recompila todas as fontes transitivas, não executa o programa e não constitui uma nova rodada de natureza ou custódia. A nova cópia é material de incorporação para a sessão que mantém o canônico; se esse canônico avançar, o delta precisa ser refeito.

{link('Nova cópia de trabalho do um.py', copy_folder / 'um.py')}: {integrated['bytes']} bytes, SHA-256 `{integrated['sha256']}`.

Atlas, índice, diário e memórias canônicas permanecem somente leitura. Este relatório novo e a entrega no túnel registram o avanço sem alterar o acervo originário. O documento sucede as pendências de cociclo e covariância finita da entrega 059; as fontes e os relatórios anteriores permanecem intactos.

## Inventário novo desta continuação

| Módulo | Teoremas | Outras declarações |
|---|---:|---:|
"""
    for module in inventory["modules"]:
        if module["new_this_continuation"]:
            report += f"| {Path(module['source']).stem} | {module['theorems']} | {module['other_declarations']} |\n"
    report += "\nOs hashes medidos, as fontes e os recibos individuais estão no INVENTARIO_FONTES.json e no INTEGRATION_RESULT.json.\n"
    write_new(report_path, report.encode("utf-8"))
    evidence = [report_path, result_path, integration_path, audit_path, cached_receipt_path,
                OUT / "INVENTARIO_FONTES.json", OUT / "CONFIG_COCICLO_COVARIANCIA.json"]
    manifest = {"status": "PASS_CONSOLIDATED_WORKING_COPY_SCOPE",
        "created_utc": datetime.now(timezone.utc).isoformat(), "canonical": canonical,
        "integrated_copy": integrated, "counts": counts,
        "processes_passed": len(result["runs"]), "warnings": 0,
        "fresh_leaf_modules_compiled": fresh["modules"], "cached_leaf_modules": len(cached),
        "cached_build_processes_passed": len(prior_build["runs"]),
        "independent_static_checks_passed": audit["counts"]["passed_checks"],
        "evidence": [record(path) for path in evidence], "canonical_modified": False,
        "um_py_executed_or_imported": False, "all_transitive_sources_rebuilt": False,
        "empirical_tests_run": False, "gate_promoted": False, "qg_goal_complete": False}
    manifest_path = OUT / "ENTREGA_CONSOLIDADA.json"
    write_new(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    tunnel = BASE / "TUNEL/DO_CHATGPT"
    numbers = [int(match.group(1)) for path in tunnel.iterdir()
               if (match := re.match(r"ENTREGA_(\d+)", path.name))]
    number = max(numbers, default=0) + 1
    handoff_path = tunnel / f"ENTREGA_{number:03d}_ESPONTANEA_cociclo_interagente_covariancia_finita.md"
    handoff = f"""# Entrega {number:03d} — cociclo interagente e covariância finita

09/09/2026. [REAL — bancada compilada e auditada; originais preservados.]

{link('Reexame atualizado e pendências', report_path)} · {link('Manifesto', manifest_path)} · {link('Nova cópia um.py', copy_folder / 'um.py')}.

Base v337 relida e estável. Novos {fresh['modules']} módulos, {fresh['theorems']} teoremas e {fresh['other_declarations']} outras declarações; integração total de {total['modules']} módulos e {total['theorems']} teoremas. Build incremental: {len(result['runs'])} processos novos PASS, zero avisos; {len(cached)} folhas anteriores reutilizadas com fontes idênticas. A raiz e as auditorias carregam todos os {total['modules']} módulos. Auditoria estática independente: {audit['counts']['passed_checks']}/{audit['counts']['checks']}.

Agora demonstrados: cociclo unitário infinito do potencial XX somável na ação modular canônica; controle uniforme dos cortes; gerador iV e ODE; grupo β_t=Ad_u(t)∘α_t que preserva o fator; transformação finita de Levi-Civita/Ricci/escalar/Einstein e lei de transformação de Einstein nas sobreposições métricas abertas.

Continuam explícitos: seleção física/caracterização operacional; área e fonte física T; estado perturbado normalizado e identificação modular/KMS; transições suaves e compatibilidade global do atlas/matéria; anomalias e UV da teoria geral. A componente Einstein da antiga hmatch tem agora condições suficientes demonstradas, mas um atlas completo não foi construído automaticamente.

Fontes e recibos: INVENTARIO_FONTES.json; configuração de incorporação: CONFIG_COCICLO_COVARIANCIA.json. Caso o canônico avance, refazer delta. Sem executar/importar um.py, sem flags novas, sem alterar gate, ritos, selos ou memórias canônicas. Esta entrega sucede as pendências reduzidas da entrega 059, preservando-a.

SHA-256 medido da cópia: `{integrated['sha256']}`.
"""
    write_new(handoff_path, handoff.encode("utf-8"))
    receipt_path = OUT / "RECIBO_ENTREGA_FINAL.json"
    write_new(receipt_path, (json.dumps({"report": record(report_path),
        "manifest": record(manifest_path), "handoff": record(handoff_path)},
        ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"status": manifest["status"], "report": report_path.as_posix(),
        "handoff": handoff_path.as_posix(), "manifest": manifest_path.as_posix()}))


if __name__ == "__main__":
    main()
