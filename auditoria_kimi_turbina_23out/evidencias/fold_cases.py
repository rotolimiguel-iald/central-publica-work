"""Independent reproduction of the fold behaviour. Runs INSIDE the copy (cwd = C:\\t\\orq_copia_kimi) against the
variant currently installed as iald_orchestrator/canonical_memory.py and the SYNTHETIC sealed snapshot.
Prints one JSON document with the outcome of every case."""
import json
import sys
from pathlib import Path

COPY = Path(r"C:\t\orq_copia_kimi")
sys.path.insert(0, str(COPY))
from iald_orchestrator import canonical_memory as cm  # noqa: E402

assert Path(cm.__file__).resolve().parent.parent == COPY, cm.__file__
releases = COPY / "state" / "canonical_memory" / "releases"
release = sorted(releases.iterdir())[0]

KIMI_PROMPT = json.loads(Path(r"C:\Users\rotol\Documents\kimi\workspace\estudo_iald_qg\ferramentas\submit_claude_9298f642.json").read_text(encoding="utf-8"))["prompt"]


def run(label, prompt, **kw):
    out = {"case": label, "prompt_chars": len(prompt), "prompt_bytes": len(prompt.encode("utf-8")), "kw": {k: v for k, v in kw.items()}}
    try:
        r = cm.prepare(prompt, release, **kw)
    except ValueError as e:
        out.update(result="REFUSED", message=str(e)[:160])
        return out
    rec = r["receipt"]
    body = r["prompt"]
    rc = kw.get("reserved_context_chars", 0)
    rb = kw.get("reserved_context_bytes", 0)
    out.update(
        result="ACCEPTED", packet_chars=len(body), packet_bytes=len(body.encode("utf-8")),
        total_chars_with_reserve=len(body) + rc, total_bytes_with_reserve=len(body.encode("utf-8")) + rb,
        folded=rec.get("folded"), fold_layers=rec.get("fold_layers"),
        has_notice_in_prompt=("MODO DOBRADO" in body), n_sources=len(rec.get("sources") or []),
        coverage=rec.get("coverage"), retrieval_scope=rec.get("retrieval_scope"),
        has_fold_notice_field=bool(rec.get("fold_notice")),
        document_pins=len(rec.get("document_pins") or []) if "document_pins" in rec else None,
        budget_skipped=rec.get("budget_skipped_passages"),
        env_char_limit=rec.get("envelope_char_limit"), env_byte_limit=rec.get("envelope_byte_limit"),
    )
    cap = kw.get("max_chars", 24000)
    if kw.get("mode", "standard") == "standard" or cap > 24000:
        out["char_cap"] = cap
        out["exceeds_char_cap_with_reserve"] = out["total_chars_with_reserve"] > cap
    mode = kw.get("mode", "standard")
    blimit = (1048576 - (393216 if mode == "deepseek_maximum" else 131072) - 8192) if mode != "standard" else 36000
    out["byte_limit"] = blimit
    out["exceeds_byte_limit_with_reserve"] = out["total_bytes_with_reserve"] > blimit
    return out


cases = []
R = 20911  # reserved projection size used by Kimi (spine seq 1291)
# C1: Kimi's own blocked case (real prompt + 20.911 reserved chars, standard, cap 12.000)
cases.append(run("C1_kimi_caso_bloqueado_20911_cap12000", KIMI_PROMPT, mode="standard", max_chars=12000, prompt_limit=24000,
                 reserved_context_chars=R, reserved_context_bytes=R))
# C1b: same but cap 20.000 (the real claude queue cap measured in seq 1304) and reserve 15.852 (F9.9 projection)
cases.append(run("C1b_fila_real_cap20000_reserva15852", KIMI_PROMPT, mode="standard", max_chars=20000, prompt_limit=24000,
                 reserved_context_chars=15852, reserved_context_bytes=15852))
# C2: maximum mode, reserve = whole byte limit (909.312)
lim = 1048576 - 131072 - 8192
cases.append(run("C2_maximum_reserva_igual_ao_teto_de_bytes", "tarefa curta", mode="maximum", max_chars=24000,
                 reserved_context_bytes=lim, reserved_context_chars=0))
lim2 = 1048576 - 393216 - 8192
cases.append(run("C2b_deepseek_maximum_reserva_igual_ao_teto", "tarefa curta", mode="deepseek_maximum", max_chars=24000,
                 reserved_context_bytes=lim2, reserved_context_chars=0))
# C3: standard, NO reserve at all, pedido multibyte nearly filling the 36.000-byte bound (char cap still fits)
for n in (15500, 16000, 16500):
    cases.append(run("C3_sem_reserva_pedido_multibyte_%d_chars" % n, "ç" * n, mode="standard", max_chars=24000, prompt_limit=24000))
for n in (16700, 17000, 17400):
    cases.append(run("C3x_sem_reserva_pedido_multibyte_%d_chars" % n, "ç" * n, mode="standard", max_chars=24000, prompt_limit=24000))
# C8: pedido ASCII que deixa < 1000 chars para memoria; reserva 0 vs reserva 10
for n in (21100,):
    cases.append(run("C8_pedido_%d_x_sem_reserva" % n, "x" * n, mode="standard", max_chars=24000, prompt_limit=24000))
    cases.append(run("C8b_pedido_%d_x_reserva10" % n, "x" * n, mode="standard", max_chars=24000, prompt_limit=24000,
                     reserved_context_chars=10, reserved_context_bytes=10))
# C3b: same but tiny reserve of 10 chars (any non-zero reserve unlocks folding in the current version)
cases.append(run("C3b_reserva_minima_10_pedido_multibyte_16500", "ç" * 16500, mode="standard", max_chars=24000, prompt_limit=24000,
                 reserved_context_chars=10, reserved_context_bytes=10))
# C4: pedido sozinho maior que o teto de caracteres (impossibilidade verdadeira, dimensao char)
cases.append(run("C4_pedido_20000_x_cap12000_reserva20911", "x" * 20000, mode="standard", max_chars=12000, prompt_limit=24000,
                 reserved_context_chars=R, reserved_context_bytes=R))
cases.append(run("C4b_pedido_20000_x_cap12000_sem_reserva", "x" * 20000, mode="standard", max_chars=12000, prompt_limit=24000))
# C5: a fold that is aggregate-valid: compute reserve so that room for slices is < 1000 but mandatory fits
hdr = cm.CORE  # not exact; we search the reserve empirically below
valid = None
for reserve in range(12000, 23000, 100):
    try:
        r = cm.prepare("Qual a forma canonica do Um?", release, mode="standard", max_chars=24000, prompt_limit=24000,
                       reserved_context_chars=reserve, reserved_context_bytes=reserve)
    except ValueError:
        continue
    if r["receipt"].get("folded"):
        valid = reserve
        break
cases.append(run("C5_fold_valido_agregado_cabe_reserva_%s" % valid, "Qual a forma canonica do Um?", mode="standard", max_chars=24000,
                 prompt_limit=24000, reserved_context_chars=valid or 0, reserved_context_bytes=valid or 0))
# C6: normal path unchanged (no reserve)
cases.append(run("C6_caminho_normal_sem_reserva", "Qual a forma canonica do Um?", mode="standard", max_chars=24000, prompt_limit=24000))
# C7: empty allowlist
cases.append(run("C7_allowlist_vazia_com_reserva", "tarefa", mode="standard", max_chars=7000, prompt_limit=24000, allowed_sources=[],
                 reserved_context_chars=5500, reserved_context_bytes=5500))
print(json.dumps({"variant_sha16": __import__("hashlib").sha256(Path(cm.__file__).read_bytes()).hexdigest()[:16], "cases": cases}, ensure_ascii=False, indent=1))
