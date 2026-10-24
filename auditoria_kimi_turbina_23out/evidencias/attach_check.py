"""Second-gate check (runs inside the copy): nos_packet.prepare_queue -> operational_memory.attach -> request_controls.enforce_packet
with the variant currently installed. Synthetic sealed memory, synthetic projection text ('P'*N)."""
import hashlib
import json
import sys
from pathlib import Path

COPY = Path(r"C:\t\orq_copia_kimi")
sys.path.insert(0, str(COPY))
from iald_orchestrator import canonical_memory as cm, operational_memory as opmem, nos_packet, providers  # noqa: E402

# make prepare() resolve the synthetic ACTIVE pointer of the copy (BASE-relative, already the copy)
KIMI_PROMPT = json.loads(Path(r"C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg\ferramentas\submit_claude_9298f642.json").read_text(encoding="utf-8"))["prompt"]


def projection(n):
    text = "P" * n
    return {"text": text, "objective": "", "receipt": {"projection_sha256": opmem.digest(text)},
            "included_record_ids": [], "omitted_record_ids": []}


def case(label, prompt, cap, n):
    c = {"required_provider": "claude", "max_projection_chars": cap}
    out = {"case": label, "cap": cap, "projection_chars": n}
    try:
        r = nos_packet.prepare_queue(prompt, c, providers.SYSTEM, "claude", operational_projection=projection(n))
    except ValueError as e:
        out.update(result="REFUSED", message=str(e)[:140])
        return out
    rec = r["receipt"]
    total = len(providers.SYSTEM + "\n\nTAREFA:\n" + r["prompt"])
    out.update(result="ACCEPTED_BY_ALL_GATES", final_chars_system_plus_prompt=total, over_cap=total > cap,
               folded=rec.get("folded"), retrieval_scope=rec.get("retrieval_scope"), n_sources=len(rec.get("sources") or []),
               notice_in_final_prompt="MODO DOBRADO" in r["prompt"], receipt_has_fold_fields=all(k in rec for k in ("folded", "fold_layers", "fold_notice")),
               receipt_keys_op="operational_memory" in rec)
    return out


res = [
    case("A_kimi_caso_20911_cap12000", KIMI_PROMPT, 12000, 20911),
    case("B_fila_real_15852_cap20000", KIMI_PROMPT, 20000, 15852),
    case("C_fold_agregado_valido_cap24000_proj21300", "Qual a forma canonica do Um?", 24000, 21300),
    case("D_sem_fold_cap24000_proj2000", "Qual a forma canonica do Um?", 24000, 2000),
]
print(json.dumps({"variant_sha16": hashlib.sha256(Path(cm.__file__).read_bytes()).hexdigest()[:16], "cases": res}, ensure_ascii=False, indent=1))
