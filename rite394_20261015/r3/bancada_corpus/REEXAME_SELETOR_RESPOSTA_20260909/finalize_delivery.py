"""Freeze delivery 062 only after joint Lean compilation and independent static review."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, sys

BASE = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
COPY = BASE / "COPIA_INTEGRADA_20260909_174634_173402"
BUILD = BASE / "INTEGRADOR_SELETOR_LOCALIDADE_20260909_174443_581582/BUILD_SUCCESSOR_20260909_174751_385895"
REVIEW = BASE / "REVISAO_REEXAME_SELETOR_20260909_174847_493034"
TRIO = {"propext", "Classical.choice", "Quot.sound"}

def rec(path):
    raw = path.read_bytes()
    return {"path": path.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}

def read(path):
    return json.loads(path.read_text(encoding="utf-8"))

def new(path, raw):
    assert path.resolve().is_relative_to(BASE) and not path.exists()
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    with temp.open("xb") as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    assert temp.read_bytes() == raw
    os.rename(temp, path)
    assert path.read_bytes() == raw

def link(path, label):
    assert path.is_file()
    return f"[{label}](<{path.as_posix()}>)"

def main():
    assert len(sys.argv) == 2, "Pass the independent integration audit JSON."
    audit_path = Path(sys.argv[1]).resolve()
    assert audit_path.is_relative_to(BASE)
    audit = read(audit_path)
    assert audit["status"].startswith("PASS") and not audit["failed_checks"]
    assert audit["checks_passed"] == audit["checks_total"] and audit["checks_total"] > 0
    plan_path = BUILD / "BUILD_PLAN.json"
    result_path = BUILD / "TRANSPOSED_RESULT.json"
    plan, result = read(plan_path), read(result_path)
    assert result["status"] == "PASS_TRANSPOSED_SCOPE" and result["plan"] == rec(plan_path)
    assert result["input_boundary_unchanged"] and result["cached_boundary_unchanged"]
    assert len(result["runs"]) == 8
    for run in result["runs"]:
        assert run["valid"] and run["exit_code"] == 0 and run["warning_lines"] == 0
        assert all(set(row["axioms"]) <= TRIO for row in run["axiom_rows"])
    expected = {"cached_modules":72,"new_modules":5,"new_processes":8,"total_modules":77,
                "theorems":1065,"other_declarations":293,"all_declarations":1358}
    assert plan["counts"] == result["counts"] == expected
    assert rec(COPY / "um.py") == plan["integrated_copy"] == audit["integrated"]
    integration = read(COPY / "INTEGRATION_RESULT.json")
    assert integration["sentinels_flags_and_gate_code_unchanged"]
    assert integration["outside_embedded_table_ast_identical"]
    assert integration["outside_embedded_table_bytes_unchanged"]
    inventory = read(OUT / "INVENTARIO_CINCO_FONTES.json")
    canonical = inventory["canonical"]
    assert rec(Path(canonical["path"])) == canonical
    for item in inventory["modules"]:
        assert rec(Path(item["source"]["path"])) == item["source"]
        assert rec(Path(item["receipt"]["path"])) == item["receipt"]
    report = OUT / "REEXAME_ATUALIZADO.md"
    assert rec(report)["sha256"] == "31fbd7a97187a2a041faeb4af892d22097860024bd9fa20bd4b677126dfc5f7f"
    for target in re.findall(r"\]\(<(C:/[^>]+)>\)", report.read_text(encoding="utf-8")):
        assert Path(re.sub(r":\d+$", "", target)).is_file(), target
    reviews = [REVIEW / "PARECER_REEXAME_ATUALIZADO.md", REVIEW / "EVIDENCIA_PARECER.json",
        BASE / "REVISAO_SELETOR_REGISTRO_20260909_174107_580231/AUDITORIA_SELETOR_REGISTRO.json",
        BASE / "ENTRELACAMENTO_SELETOR_20260909_172718_478310/MANIFESTO_ENTRELACAMENTO.json",
        BASE / "LOCALIDADE_EXTENSIVA_20260909_172820_609568/ADENDO_REVISAO_INDEPENDENTE.json",
        BASE / "ESTADO_RESPOSTA_SELETOR_ARAKI_20260909_173508_109929/MANIFESTO.json"]
    refs = [rec(path) for path in reviews]
    copy_pin = rec(COPY / "um.py")
    full_rows = next(len(run["axiom_rows"]) for run in result["runs"] if run["module"] == "FullTGLAudit")
    new_rows = next(len(run["axiom_rows"]) for run in result["runs"] if run["module"] == "NewModulesAudit")
    assert full_rows == 5557 and new_rows == 1358
    validation = f"""# Validação e incorporação da entrega 062

[REAL — compilação e auditoria] Cinco folhas novas: 93 teoremas + 29 outras declarações. O lote acumulado contém 77 módulos, 1.065 teoremas + 293 outras declarações, incluindo sete instâncias locais nomeadas herdadas. A compilação conjunta executou cinco folhas e três agregadores: oito exits 0, sem avisos. O Audit integral leu {full_rows} termos; o Audit das 77 folhas leu {new_rows}, todos dentro do trio padrão.

{link(COPY / 'um.py', 'Cópia integrada do programa')}: {copy_pin['bytes']:,} bytes; SHA-256 `{copy_pin['sha256']}`. O arquivo foi analisado por AST e não foi executado nem importado. Seu snapshot é a cópia anterior de 72 módulos, identificada no recibo, não uma nova captura do canônico.

{link(result_path, 'Recibo da compilação conjunta')} · {link(audit_path, 'Auditoria estática independente')}: {audit['checks_passed']}/{audit['checks_total']} verificações. Código fora da tabela de fontes, sentinelas, flags e código do gate preservados. Não foram adicionadas flags JSON individuais para as novas folhas.

Os 72 módulos anteriores foram reutilizados com igualdade exata de fontes e proveniência recursiva dos recibos 72 → 63 → 45; os artefatos e pins disponíveis foram conferidos. As dependências transitivas canônicas/Mathlib não foram todas reconstruídas nem todas hashadas. Esse limite consta do recibo; não se trata de uma compilação limpa de todo o universo de dependências.

As provas foram transpostas apenas pela adição do prefixo TGLExt aos imports locais necessários. A raiz e os dois Audits foram compilados em conjunto, conferindo coexistência. Cada nova declaração possui auditoria de axiomas.

Para a sessão codificadora: revisar o delta de cinco fontes e seus enunciados, incorporar aditivamente ao estado canônico corrente, preservar as classificações REAL / DERIVED+KNOWN / INPUT / OPEN e emitir a rodada correspondente. A análise escrita de Araki permanece identificada como aplicação de literatura; ela não entrou no kernel como axioma. Esta entrega não modifica o selo ou o veredito empírico.

O {link(report, 'reexame atualizado')} recebeu revisão independente favorável. Originais, Atlas, índice vivo e memórias canônicas permanecem intactos.
"""
    validation_path = OUT / "VALIDACAO_E_INCORPORACAO.md"
    new(validation_path, validation.encode("utf-8"))
    receipt = {"status":"PASS_DELIVERY_SCOPE", "created_utc":datetime.now(timezone.utc).isoformat(),
        "canonical":canonical,"integrated_copy":copy_pin,"build":rec(result_path),"plan":rec(plan_path),
        "static_audit":rec(audit_path),"report":rec(report),"validation":rec(validation_path),
        "source_inventory":rec(OUT / "INVENTARIO_CINCO_FONTES.json"),"reviews":refs,"counts":expected,
        "new_theorems":93,"new_other_declarations":29,"um_py_executed_or_imported":False,
        "canonical_modified":False,"physical_confirmation_claimed":False,
        "transitive_dependencies_all_rebuilt":False,"transitive_dependencies_all_hashed":False}
    receipt_path = OUT / "RECIBO_CONSOLIDADO.json"
    new(receipt_path, (json.dumps(receipt, ensure_ascii=False, indent=2)+"\n").encode())
    tunnel = BASE / "TUNEL/DO_CHATGPT/ENTREGA_062_ESPONTANEA_seletor_registro_fase_resposta.md"
    assert not list(tunnel.parent.glob("ENTREGA_062*")), "Delivery number already occupied."
    delivery = f"""# ENTREGA 062 — seletor canônico, registro, fase relativa e resposta do estado

09/09/2026. [REAL] Entrega aditiva à 061, sobre o canônico v337 conferido em leitura. Originais intocados. Nenhum um.py executado/importado.

Cinco novas folhas: CanonicalSelectorBorn (15T+3D), SelectorRecordReconstruction (12T+4D), AngularSelectorIntertwining (24T+7D), RelativePhaseCharacter (24T+8D), BondLocalityEstimates (18T+7 outras). Total: 93 teoremas + 29 outras declarações. Os 77 módulos acumulados passaram no escopo de compilação incremental descrito no recibo.

- {link(report, 'Reexame atualizado e lista residual')}.
- {link(validation_path, 'Validação, limites e instruções de incorporação')}.
- {link(receipt_path, 'Recibo consolidado com pins medidos')}.
- {link(COPY / 'um.py', 'Cópia integrada de trabalho')}.
- {link(BASE / 'ESTADO_RESPOSTA_SELETOR_ARAKI_20260909_173508_109929/DERIVADA_NORMALIZADOR_ARAKI.md', 'Primeira variação de Araki — dedução escrita')}.

Ganho: o seletor efetivo reconhece o caráter codificado de R; seu peso preservado recupera g,T. O vetor selecionado normalizado perde o escalar nessa família. O entrelaçamento com as matrizes é explícito; duas probabilidades de interferência recuperam a fase relativa, e a família completa caracteriza o registro. R continua entrada; o decodificador exato não demonstra preparação física ou estabilidade de recuperação com dados finitos.

O bloco extensivo paga suporte, estabilização e majorante de comutadores sem somabilidade global; o limite dinâmico permanece a próxima prova. A análise de Araki fornece Z′(0)=ω(W) e a resposta do estado normalizado, no domínio declarado; área, calor, conservação, cobertura efetiva e alcance quântico geral permanecem discriminados no reexame.

Os critérios de falsificação existentes foram considerados. As conclusões de lastro ficam limitadas aos enunciados, hipóteses e canais documentados. Nenhum gate foi movido.
"""
    new(tunnel, delivery.encode("utf-8"))
    final = {"status":"DELIVERED_062","delivery":rec(tunnel),"receipt":rec(receipt_path),
             "report":rec(report),"created_utc":datetime.now(timezone.utc).isoformat()}
    new(OUT / "RECIBO_ENTREGA_FINAL.json", (json.dumps(final, ensure_ascii=False, indent=2)+"\n").encode())
    print(json.dumps(final, ensure_ascii=False))

if __name__ == "__main__":
    main()
