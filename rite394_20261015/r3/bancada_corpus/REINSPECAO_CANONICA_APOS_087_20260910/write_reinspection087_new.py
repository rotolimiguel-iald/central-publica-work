from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import re

OUT = Path(__file__).resolve().parent
ROOT = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós")
OLD = Path("C:/IALD/Central de Patentes/Chatgpt/INSPECAO_CANONICO_NAVEGACAO_086_20260910/ESTADO_CANONICO_INSPECAO_086.json")
NAMES = ["um.py", "um_absoluto_selo.json", "tgl_kernel_proof_manifest.json", "rodada_v338_stdout.txt"]
INPUTS = [Path(__file__).resolve(), OLD] + [ROOT / name for name in NAMES]
def pin(p):
    raw = p.read_bytes()
    st = p.stat()
    return {"path": p.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(),
            "mtime_ns": st.st_mtime_ns,
            "mtime_utc": dt.datetime.fromtimestamp(st.st_mtime, dt.timezone.utc).isoformat()}
def emit(name, raw):
    dest = OUT / name
    tmp = OUT / (name + ".pending_new")
    if dest.exists() or tmp.exists():
        raise FileExistsError(str(dest))
    with tmp.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if tmp.read_bytes() != raw:
        raise RuntimeError("Temporary verification failed")
    os.rename(tmp, dest)
    if dest.read_bytes() != raw:
        raise RuntimeError("Final verification failed")
    return pin(dest)

before = [pin(p) for p in INPUTS]
old = json.loads(OLD.read_bytes())
old_by_path = {entry["path"].casefold(): entry for entry in old["pins"]}
comparison = []
for p, now in zip(INPUTS[2:], before[2:]):
    prior = old_by_path[p.as_posix().casefold()]
    comparison.append({"name": p.name, "equal_bytes_hash": now["bytes"] == prior["bytes"] and now["sha256"] == prior["sha256"],
                       "current": now, "capture086": prior})
if not all(item["equal_bytes_hash"] for item in comparison):
    raise RuntimeError("Canonical delta found: preserve helper and perform a dedicated delta review; no unchanged note emitted")

um_lines = (ROOT / "um.py").read_text(encoding="utf-8").splitlines()
seal_lines = (ROOT / "um_absoluto_selo.json").read_text(encoding="utf-8").splitlines()
stdout_lines = (ROOT / "rodada_v338_stdout.txt").read_text(encoding="utf-8").splitlines()
anchors = {
    "um.py": [{"line": n, "text": um_lines[n-1]} for n in list(range(3247, 3251)) + list(range(21553, 21577))],
    "um_absoluto_selo.json": [{"line": n, "text": seal_lines[n-1]} for n in [19, 20, 21, 79]],
    "rodada_v338_stdout.txt": [{"line": n, "text": stdout_lines[n-1]} for n in [418, 422, 437, 440, 777]]
}
all_rounds = []
recent = []
for p in ROOT.iterdir():
    if not p.is_file():
        continue
    st = p.stat()
    entry = {"name": p.name, "bytes": st.st_size,
             "mtime_utc": dt.datetime.fromtimestamp(st.st_mtime, dt.timezone.utc).isoformat(),
             "mtime_ns": st.st_mtime_ns}
    recent.append(entry)
    match = re.fullmatch(r"rodada_v(\d+)_stdout(?:_.*)?\.txt", p.name, re.IGNORECASE)
    if match:
        all_rounds.append({**entry, "named_version": int(match.group(1))})
all_rounds.sort(key=lambda v: v["mtime_ns"], reverse=True)
recent.sort(key=lambda v: v["mtime_ns"], reverse=True)
max_version = max(v["named_version"] for v in all_rounds)
if max_version != 338 or all_rounds[0]["name"] != "rodada_v338_stdout.txt":
    raise RuntimeError("Successor or newer stdout found; unchanged conclusion is not appropriate")
after = [pin(p) for p in INPUTS]
unchanged = before == after
if not unchanged:
    raise RuntimeError("Input changed inside inspection window")
present = sum(bool(v["present"]) for v in old["modules"])
total = len(old["modules"])
if present != old["present"] or total-present != old["absent"]:
    raise RuntimeError("Inconsistent capture086 module inventory")
created = dt.datetime.now(dt.timezone.utc).isoformat()
table = "\n".join("| " + c["name"] + " | " + str(c["current"]["bytes"]) + " | " +
                  c["current"]["sha256"] + " | " + c["current"]["mtime_utc"] + " |"
                  for c in comparison)
note = f"""# Reinspeção do caminho canônico após a entrega087

[REAL — leitura documental] Janela encerrada em {created}. Os quatro arquivos abaixo têm os mesmos tamanhos e SHA-256 da captura086. Não há sucessor de v338 identificado neste caminho:
C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós.

| Arquivo | Bytes | SHA-256 medido | mtime UTC |
|---|---:|---|---|
{table}

[REAL] A listagem de nomes/metadados diretamente nesse diretório mantém rodada_v338_stdout.txt como stdout mais recente; o maior número de versão entre os nomes rodada_vN_stdout*.txt é {max_version}. A inspeção não abrange outras cópias ou trabalhos em preparação noutra sessão.

[REAL — referência estática preservada] A captura086 identificou {present}/{total} módulos presentes e {total-present} ausentes, mediante AST e BUILD_PLAN. Esta reinspeção não repetiu o AST nem compilou: a igualdade integral dos bytes de um.py preserva aquele resultado para esse mesmo conjunto de módulos. Portanto, não surgiu nesta fonte a incorporação das 21 folhas que faltavam na captura086.

As seguintes delimitações foram relidas na fonte atual:

- [DECLARADO na fonte] um.py:21553–21576 apresenta o lote058..062, os 77 módulos e a auditoria descrita pela sessão codificadora. Em21558–21560 a reconstrução de Einstein do registro depende das leis de área e conservação.
- [DECLARADO na fonte] um.py:21566–21568 descreve interação local somável, cociclo e estado perturbado de Araki, este último rotulado como derivação analítica com literatura. Esse trecho não declara QME interagente geral.
- [OPEN na própria fonte] um.py:21571–21573 preserva a correspondência física seletor–registro, matéria/conservação/área para os mesmos dados, compatibilidade física do atlas, extensão além da classe globalmente limitada, anomalias e UV.
- [DECLARADO na fonte] um.py:3247–3250 conserva o programa de perturbações gerais e anomalias quânticas, com delimitação de PDEs, distribuições e renormalização.
- [DECLARADO em evidência de rodada armazenada] rodada_v338_stdout.txt:418–422 delimita cinemática de spin2, dinâmica condicional e interação/renormalização abertas;437–440 registra interação/anomalias abertas;777 delimita o resultado de ondas planas. São trechos históricos da mesma rodada, não uma execução nova.
- [DECLARADO no selo armazenado] um_absoluto_selo.json:21 contém o veredito interno já existente;79 mantém GOROFF_SAGNOTTI_WALL_TYPED_OPEN e proíbe usar a finitude de Breuer como resposta UV. O selo não mudou.

Não foi identificado pagamento adicional dessas pendências por alteração dos quatro artefatos desde086. Isso não nega os resultados separados da bancada Chatgpt posteriores à integração, nem atribui a eles incorporação canônica ou execução que esta inspeção não encontrou.

[REAL] Os seis arquivos lidos para medição (helper novo, captura086 e quatro arquivos canônicos) permaneceram idênticos em bytes, hash e mtime durante a janela registrada. Não executei/importei um.py, não executei Lean/CAS, não alterei originais, Atlas, índice, memórias ou arquivos congelados. A única execução foi deste helper novo de leitura, comparação e emissão documental.

Referência anterior: [captura086](<{OLD.as_posix()}>). Recibo desta reinspeção: [REGISTRO_REINSPECAO_CANONICA_087.json](<{(OUT / 'REGISTRO_REINSPECAO_CANONICA_087.json').as_posix()}>).
"""
note_pin = emit("PARECER_REINSPECAO_CANONICA_APOS_087.md", note.encode("utf-8"))
result = {
    "status": "READ_ONLY_CANONICAL_UNCHANGED_VS_086",
    "created_utc": created,
    "scope": "Only canonical files and direct directory metadata; no other copies or repositories scanned",
    "canonical_comparison": comparison,
    "capture086_created_utc": old["created_utc"],
    "previous_ast_inventory_not_rerun": {"present": present, "total": total, "absent": total-present},
    "anchors_read_now": anchors,
    "latest_round_names_metadata": all_rounds[:12],
    "maximum_named_stdout_version": max_version,
    "recent_canonical_entries_metadata": recent[:18],
    "pins_before": before,
    "pins_after": after,
    "all_six_inputs_preserved": unchanged,
    "note": note_pin,
    "um_executed_or_imported": False,
    "mathematical_programs_executed": 0,
    "lean_executed": False,
    "originals_or_memories_written": False,
    "new_files_only_in_Chatgpt": True,
    "independent_mathematical_approval_claimed": False
}
receipt_pin = emit("REGISTRO_REINSPECAO_CANONICA_087.json",
                   (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"status": result["status"], "note": note_pin, "receipt": receipt_pin,
                  "sources_preserved": len(INPUTS), "new_mathematics": 0}, ensure_ascii=False))

