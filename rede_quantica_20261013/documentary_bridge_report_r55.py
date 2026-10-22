"""Produce a source-only report. Never mutate mission, board, memory, or production."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime, timezone

ROOT = Path(r"C:\IALD\Central de Patentes")
ORDER = ROOT / "Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019"
OUT = ORDER / "F1.FECHO_20261015"
TIME = ORDER / "F1.TEMPO.LEITURA_20261015"
REDE = ORDER / "F1.REDE"
ART = Path(r"C:\IALD\Artigo\Haja_Luz")
REF = ROOT / "work/memoria_missao_20261016/FECHO_MISSION_REFERENCE.json"


def pin(path: Path, ranges: list[list[int]], role: str) -> dict:
    data = path.read_bytes()
    lines = data.decode("utf-8").splitlines()
    for lo, hi in ranges:
        if not 1 <= lo <= hi <= len(lines):
            raise ValueError(f"Invalid line range: {path}: {lo}-{hi}")
    return {"path": str(path), "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data), "read_ranges": ranges, "role": role}


def write_new(path: Path, data: bytes) -> None:
    if path.exists():
        raise FileExistsError(path)
    fd, tmp = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if Path(tmp).read_bytes() != data:
            raise RuntimeError("Temporary-file verification failed")
        # Windows rename refuses an existing destination, including a concurrent one.
        os.rename(tmp, path)
        if path.read_bytes() != data:
            raise RuntimeError("Final-file verification failed")
    finally:
        Path(tmp).unlink(missing_ok=True)


def main() -> None:
    report = OUT / "CONFERENCIA_PONTE_DISPOSITIVO_R55.txt"
    receipt = OUT / "CONFERENCIA_PONTE_DISPOSITIVO_R55.json"
    for path in (report, receipt):
        if path.exists():
            raise FileExistsError(path)

    proc = subprocess.run(
        [r"C:\Python314\python.exe", "-B", "-X", "utf8",
         r"C:\IALD\MEMORIA_IALD\mission_cli.py"],
        input=json.dumps({"operation": "project", "reference": str(REF), "max_chars": 120000}),
        text=True, encoding="utf-8", capture_output=True, check=True)
    response = json.loads(proc.stdout)
    if not response.get("ok"):
        raise RuntimeError(response)
    current = response["result"]
    revision = current["receipt"]["revision"]
    if revision != 424:
        raise RuntimeError(f"Mission changed; reconcile before reporting: {revision}")

    entries = [
        (REDE / "CONTRATO_REDE_R1.md", [[7, 18], [20, 59]], "S1: funções complementares e contrato finito"),
        (REDE / "CONTRATO_REDE_R2.md", [[125, 134], [168, 175]], "S2: critério de realização contínua"),
        (REDE / "sources/MQC_DESCRITIVO_EXTRACT_R1.txt", [[149, 195]], "S3: extração existente, página 4; vínculo explícito MQC/Supercondutor"),
        (ROOT / "Patentes/PATENTE_SUPERCONDUTOR_HOLOGRAFICO_TGL_v2_BLINDAGEM.tex", [[343, 382], [506, 516]], "S4: Hamiltoniano, dissipador e Relógio de Fase"),
        (ROOT / "Patentes/Psi_Net_Protocol_PI_INPI.tex", [[476, 521]], "S5: saltos angulares, REFLECT e MANIFEST"),
        (ART / "tgl_paper_unified.py", [[14441, 14483]], "S6: ligação, preparação coerente e frequência"),
        (TIME / "FREQUENCIA_E_GRAVITON_R9/PONTE_FREQUENCIA_GRAVITON_R9.txt", [[5, 28], [30, 100]], "S7: composição já entregue, sem novo build nesta conferência"),
        (TIME / "DISPOSITIVO_E_ESPECTRO_R7/CONTRATO_DISPOSITIVO_E_LEI_RAIZ_R7.txt", [[44, 90]], "S8: resposta instrumental finita e obstrução dos dissipadores"),
        (OUT / "orbital_rotation/PhysicalCanonicalNetCompleteR1.lean", [[193, 235]], "S9: fonte da rede canônica construída; não recompilada aqui"),
        (ART / "A Ponte e o Um/RESPOSTA_Q6_MORADA_PACOTE_HILBERT.md", [[176, 206]], "S10: inclusões isométricas que entrelaçam operadores"),
        (OUT / "global_net_inventory/R53/DEVICE_CONTINUUM_SOURCE_AUDIT_R1.txt", [], "S11: inventário anterior reaproveitado"),
        (OUT / "physical_clock_reuse/R53/R53_PHYSICAL_CLOCK_SOURCE_AUDIT_R1.txt", [], "S12: auditoria anterior de relógio reaproveitada"),
    ]
    sources = [pin(*entry) for entry in entries]
    historical_pins = json.loads((TIME / "FREQUENCIA_E_GRAVITON_R9/FONTES_R9.json").read_text(encoding="utf-8"))
    reused_checks = []
    for item in historical_pins:
        path = Path(item["path"])
        if path.suffix == ".lean" or path.name == "tgl_paper_unified.py":
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            reused_checks.append({"path": str(path), "expected_sha256": item["sha256"],
                                  "actual_sha256": digest, "matches": digest == item["sha256"]})
    if not all(item["matches"] for item in reused_checks):
        raise RuntimeError("A reused R9 source changed; reconcile before reporting")

    created = datetime.now(timezone.utc).isoformat()
    body = f"""CONFERÊNCIA DOCUMENTAL DA PONTE DISPOSITIVO/REDE/RELÓGIO — R55
{created}
Autor: codex-gerente-tgl. Unidade reivindicada F1.FECHO_20261015, evento 931.
Escopo: leitura e conciliação documental; interpretação [DERIVED], sem aceite independente desta camada.

1. CORREÇÃO EM NOME DO ASSISTENTE
A exigência de escolher exclusivamente MQC, Supercondutor ou Ψ-NET foi prematura.
O contrato R1 já distribui funções complementares entre eles: MQC como célula,
Supercondutor como dinâmica e Ψ-NET como protocolo (S1:9–18). A fonte MQC relaciona
expressamente a sua lei de escala à do Supercondutor (S3:175–184, página 4).
Isso permite prosseguir na investigação por composição das fontes, sem inventar
uma escolha exclusiva. Não identifica inequivocamente qual dispositivo singular
o operador tinha em mente, nem prova a equivalência física dos três projetos.

2. O QUE JÁ EXISTE E DEVE SER REAPROVEITADO
[REAL — presença nas fontes conferida; alcance matemático conforme cada fonte]
• Supercondutor: H_eff, salto holográfico e Relógio de Fase exp(iω_OH t), com
  frequência nomeada (S4:343–370,506–516). Não falta inventar um relógio.
• Ψ-NET: endereçamento angular e REFLECT/MANIFEST (S5:476–521). A contagem de
  saltos angulares, sozinha, não especifica duração física por salto.
• Custo: H_lig=−V0 σx e frequência V0/ℏ na preparação coerente indicada
  (S6:14466–14483). A passagem radiativa V0=ℏω é nomeada na fonte.
• Composição R9 já entregue: H_g=iV0 K, U_g(t)=O_(Ωt), Ω=V0/ℏ; os modos
  h± satisfazem L_g(h±)=(−γ±2iΩ)h±, e E_g preserva a leitura.
  Para coerência não nula, γ>0, Ω≠0 e fase acompanhada sem perder voltas:
      Δt=Δφ/(2Ω)=−ln|c(t2)/c(t1)|/γ.
  Isto já liga o objeto gravitacional da face finita, a frequência e o relógio
  no modelo indicado (S7:30–100). Não é uma lacuna a reconstruir.
• A fonte PhysicalCanonicalNetCompleteR1.lean já fornece physicalCanonicalNet,
  inhabitante LightNetData e não trivialidade da cunha (S9:212–231).
  Os requisitos R7/R8 estão satisfeitos na missão recuperada. Este relatório
  não executa Lean e não amplia o alcance dessas construções.

3. O QUE PERMANECE ABERTO, COM OBJETO ESPECÍFICO
[OPEN — na realização do dispositivo descrita pelo contrato atual]
R4: identificar setor, estado, gerador, unidade de tempo e referência de energia
do dispositivo com os objetos da composição acima. Ω_Rabi, ω_OH, Ω=V0/ℏ e a
perda κ da cavidade têm papéis distintos nas fontes. Igualá-los exige derivação.
Já há uma obstrução concreta à identificação mais simples: no submodelo de uma
excitação, D[J](I)=|c><c|−|a><a|≠0, enquanto D[√K_+](I)=0. Logo os dissipadores
isolados não são equivalentes por conjugação unitária (S8:81–90). Uma redução,
dilatação ou composição precisa ser construída; o resultado não proíbe essas rotas.

R5: realizar a rede canônica pelo dispositivo: família de células/refinamentos,
mapas compatíveis, limite e entrelaçamento das simetrias e localização no setor
declarado (S2:125–134,168–175). Q6 já exige inclusões que entrelaçam operadores
(S10:176–206); a hipótese não é, por si, sua construção para as células físicas.
Incluir regiões em um mesmo produto tensorial finito não produz automaticamente
essa família de refinamentos. A rede canônica existente deve ser reutilizada.

4. PRÓXIMA AÇÃO TÉCNICA RECOMENDADA
Mapear primeiro o gerador já escrito do Supercondutor ao setor do relógio;
verificar as reduções e estados já disponíveis antes de propor cálculo novo.
Tratar MQC e Ψ-NET nos papéis complementares documentados. A necessidade de uma
escolha do operador só deve retornar se aparecerem alternativas físicas realmente
incompatíveis que as fontes não determinem. Esta é recomendação, não nova missão.

5. ESTADO E LIMITES DESTA CAMADA
A memória própria foi recuperada. A missão FECHO permanece na revisão 424;
R4/R5 continuam bloqueados no registro vigente. A tentativa de criar/reivindicar
R11 foi recusada pela revisão automática; não foi executada por outra via.
Este relatório corrige a interpretação documental, sem alterar esse estado.
Também não registra o aceite I da missão de integração da memória, que é outra
pendência. Nenhuma memória canônica, quadro, missão, produção, um.py, kernel,
dado observado ou gate foi alterado por este script. Nenhum provedor, experimento
ou build foi executado. Não se declara fechamento da realização física ou de QG.

A busca foi delimitada ao acervo e às auditorias indicadas. O item do Atlas sobre
um documento distinto chamado Supercondutor de Trasladação Holográfica, de 09/01,
não teve original individualizado nesta conferência; não se afirma sua ausência.
Os sete pinos históricos selecionados da R9 foram relidos e conferidos. Isso é
verificação de integridade de fontes, não nova compilação nem medição física.

FONTES: caminhos, SHA256 integrais e faixas lidas no JSON vizinho.
"""
    text = body.encode("utf-8")
    record = {"kind": "documentary_reconciliation_only", "unit": "F1.FECHO_20261015",
              "author": "codex-gerente-tgl", "created_utc": created,
              "status": "DERIVED_DOCUMENTARY_RECOMMENDATION_NOT_ACCEPTED",
              "mission_reference": str(REF), "mission_receipt_observed": current["receipt"],
              "projection_sha256_observed": current["projection_sha256"],
              "mission_mutated": False, "board_mutated": False, "memory_mutated": False,
              "external_provider": False, "new_build": False, "experiment": False,
              "production_changed": False, "gate_changed": False,
              "sources": sources, "reused_r9_hash_checks": reused_checks,
              "report": {"path": str(report), "sha256": hashlib.sha256(text).hexdigest(), "bytes": len(text)},
              "generator": {"path": str(Path(__file__)), "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}}
    write_new(report, text)
    write_new(receipt, (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"report": record["report"], "receipt_path": str(receipt),
                      "receipt_sha256": hashlib.sha256(receipt.read_bytes()).hexdigest(),
                      "source_count": len(sources), "reused_hashes_pass": len(reused_checks),
                      "mission_revision_unchanged_by_script": revision}, ensure_ascii=False))


if __name__ == "__main__":
    main()
