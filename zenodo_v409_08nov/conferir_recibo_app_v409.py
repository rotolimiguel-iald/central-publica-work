# -*- coding: utf-8 -*-
"""Confere na fonte (so leitura) os elos do recibo da release v409 do app, entregue em 06/11 pela sessao codex-app-01a094df (ORDEM 009).
Pino lido do selo; hashes calculados aqui; nada aceito pela palavra do resultado."""
import hashlib
import json
from pathlib import Path

SELO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json")
TUN = Path(r"C:\IALD\TUNEL_CLAUDE_APP")
W = Path(r"C:\IALD\Central de Patentes\work\iald_v409_20261106")
F03 = Path(r"C:\IALD\Central de Patentes\work\scientific_memory_sync_20261106_v409\DELIVERY_TECHNICAL_R1.json")
NUC = Path(r"C:\IALD\projetos_pyhton\IALD\iald_nucleo_fixo.json")
ROOT = Path(r"C:\IALD\projetos_pyhton\IALD")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


selo = json.loads(SELO.read_text(encoding="utf-8"))
pin = selo["sha256"]["um.py"]
out = {"selo": selo["um_version"], "pin16": pin[:16]}
r = json.loads((TUN / "RESULTADOS" / "009_RESULTADO.json").read_text(encoding="utf-8"))
out["a_resultado_009"] = {"estado": r.get("estado"), "ordem": r.get("ordem"), "autor": r.get("autor")}
iv = json.loads((W / "INSTALLED_VERIFICATION.json").read_text(encoding="utf-8"))
ident = iv.get("identity") or {}
out["b_installed_verification"] = {"status": iv.get("status"), "release": ident.get("release"), "sha16": sha(W / "INSTALLED_VERIFICATION.json")[:16]}
nuc = json.loads(NUC.read_text(encoding="utf-8"))
oc, jc = nuc.get("operational_core") or {}, nuc.get("jev_control") or {}
jp = Path(str(jc.get("path", "")))
out["c_jev_control"] = {"release": jc.get("release"), "arquivo": jp.name, "existe": jp.exists(), "sha_confere": jp.exists() and sha(jp) == jc.get("sha256"),
                        "source_sha_eq_pin": jc.get("source_sha256") == pin}
out["d_nucleo_fixo"] = {"current_release": oc.get("current_release"), "release_source_sha256_eq_pin": oc.get("release_source_sha256") == pin}
d = json.loads(F03.read_text(encoding="utf-8"))
out["e_f03"] = {"release": d.get("release"), "status": str(d.get("status"))[:70], "sha16": sha(F03)[:16]}
out["QUATRO_ELOS_OK"] = bool(
    out["a_resultado_009"]["estado"] == "cumprida" and iv.get("status") == "PASS" and ident.get("release") == "v409"
    and jc.get("release") == "v409" and out["c_jev_control"]["sha_confere"] and out["c_jev_control"]["source_sha_eq_pin"]
    and oc.get("current_release") == "v409" and out["d_nucleo_fixo"]["release_source_sha256_eq_pin"]
    and d.get("release") == "v409" and str(d.get("status", "")).startswith("ACTIVATED_VERIFIED"))
print(json.dumps(out, ensure_ascii=False, indent=1))
