# -*- coding: utf-8 -*-
"""Confere na fonte os quatro elos do recibo da release v407 do app (custodia v407, 04/11/2026, claude-site-custodia).
So leitura. Pino lido do selo; hashes calculados aqui."""
import glob
import hashlib
import json
from pathlib import Path

SELO = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json")
TUN = Path(r"C:\IALD\TUNEL_CLAUDE_APP")
W = Path(r"C:\IALD\Central de Patentes\work\iald_v407_20261104")
NUC = Path(r"C:\IALD\projetos_pyhton\IALD\iald_nucleo_fixo.json")
ROOT = Path(r"C:\IALD\projetos_pyhton\IALD")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


selo = json.loads(SELO.read_text(encoding="utf-8"))
pin = selo["sha256"]["um.py"]
out = {"versao_selo": selo["um_version"], "pin16": pin[:16]}

r = json.loads((TUN / "RESULTADOS" / "006_RESULTADO.json").read_text(encoding="utf-8"))
out["a_resultado_006"] = {k: r.get(k) for k in ("estado", "ordem", "release", "versao") if k in r}

iv = json.loads((W / "INSTALLED_VERIFICATION.json").read_text(encoding="utf-8"))
ident = iv.get("identity") or {}
out["b_installed_verification"] = {"status": iv.get("status"), "identity.release": ident.get("release"),
                                   "sha16": sha(W / "INSTALLED_VERIFICATION.json")[:16]}

nuc = json.loads(NUC.read_text(encoding="utf-8"))
oc = nuc.get("operational_core") or {}
jc = nuc.get("jev_control") or {}
cands = glob.glob(str(ROOT / "**" / "jev_control_v407.json"), recursive=True)
jfiles = {c: sha(c) for c in cands}
out["c_jev_control"] = {"release": jc.get("release"), "sha16_no_nucleo": str(jc.get("sha256"))[:16],
                        "arquivos": {c: h[:16] for c, h in jfiles.items()},
                        "algum_arquivo_bate": any(h == jc.get("sha256") for h in jfiles.values())}
srcs = set()
for c in cands:
    try:
        srcs.add(json.loads(Path(c).read_text(encoding="utf-8")).get("source_sha256"))
    except Exception as e:  # falha visivel
        srcs.add("ERRO:" + repr(e))
out["c_jev_source_sha_eq_pin"] = srcs == {pin}
out["d_nucleo_fixo"] = {"current_release": oc.get("current_release"),
                        "release_source_sha256_eq_pin": oc.get("release_source_sha256") == pin}

ok = (str(out["a_resultado_006"].get("estado", "")).lower().startswith("cumprid")
      and str(iv.get("status", "")).upper().startswith("PASS") and ident.get("release") == "v407"
      and jc.get("release") == "v407" and out["c_jev_control"]["algum_arquivo_bate"] and out["c_jev_source_sha_eq_pin"]
      and oc.get("current_release") == "v407" and out["d_nucleo_fixo"]["release_source_sha256_eq_pin"])
out["QUATRO_ELOS_OK"] = ok
print(json.dumps(out, ensure_ascii=False, indent=1))
