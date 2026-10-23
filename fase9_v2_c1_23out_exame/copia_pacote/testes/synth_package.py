# -*- coding: utf-8 -*-
"""synth_package.py -- monta um PACOTE SINTETICO (centros FABRICADOS, fontes FABRICADAS) para exercer o runner de ponta a ponta e seus controles negativos.
Nada aqui le a fonte real nem calcula o composto observado. O pacote e' marcado SYNTHETIC_TEST_PACKAGE e o runner rotula tudo como SYNTHETIC_."""
import copy
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "runner"))
import f9v2_background as BG  # noqa: E402
import f9v2_calibration as CAL  # noqa: E402
import f9v2_freeze as FRZ  # noqa: E402

REAL_SPEC = os.path.join(ROOT, "spec", "PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json")
REAL_REG = os.path.join(ROOT, "spec", "REGISTRO_DH_V2_C1.json")
REAL_FUNC = os.path.join(ROOT, "spec", "veredito_fase9_v2_c1.py")


def _w(path, b):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "wb").write(b)


def fabricated_centers(spec, kind="TGL", offsets=None, K=None, mu=68.531):
    """Centros FABRICADOS: previsao TGL (K*mu) ou LCDM (mu) + deslocamentos arbitrarios. NAO sao os centros publicados."""
    K = K or spec["lei"]["K_frozen_V1"]
    base = K * mu if kind == "TGL" else mu
    offs = offsets or {"L1_sh0es_r22": 0.7, "L1b_sh0es_r25": 0.35, "L2_cchp": -0.4, "L3_sbf": 0.2, "L4_masers_5": -0.1, "L4_masers_6": -0.2, "L5_tdcosmo": 1.0, "L6_sirenes": 0.15}
    return {rid: round(base + offs[rid], 3) for rid in spec["leitores"]}


def make_package(tmp, centers=None, kind="SYNTHETIC_TEST_PACKAGE", provider_kw=None, with_freeze=True, with_open=True, cal_mode=None, mutate=None, extra_files=None,
                 provider=None, bancada_pins=None):
    """Devolve {'root':..., 'spec':..., 'register':..., 'provider':...}. `mutate(pkg)` roda ANTES de emitir os recibos (para criar pacotes defeituosos coerentes)."""
    root = os.path.join(tmp, "pkg")
    for d in ("runner", "spec", "fontes", "calibracao", "freeze"):
        os.makedirs(os.path.join(root, d), exist_ok=True)
    for f in os.listdir(os.path.join(ROOT, "runner")):
        if f.endswith(".py"):
            shutil.copyfile(os.path.join(ROOT, "runner", f), os.path.join(root, "runner", f))
    wrap = json.load(open(REAL_SPEC, encoding="utf-8"))
    spec = wrap["spec"]
    reg = json.load(open(REAL_REG, encoding="utf-8"))
    if cal_mode:
        spec["calibracao_de_cauda"]["modo"] = cal_mode
    centers = centers or fabricated_centers(spec)
    # fontes fabricadas: o trecho REAL com o centro trocado pelo fabricado
    for rid, r in reg["leitores"].items():
        real_snip = r["extraido_no_build"]["trecho"]
        H0_lit = None
        for lit in (("%s" % spec["leitores"][rid]["H0"]), ("%.1f" % spec["leitores"][rid]["H0"]), ("%.2f" % spec["leitores"][rid]["H0"])):
            if lit in real_snip.replace(" .", "."):
                H0_lit = lit
                break
        assert H0_lit is not None, ("literal do centro nao encontrado", rid, real_snip, spec["leitores"][rid]["H0"])
        snip = real_snip.replace(" .", ".")
        new_lit = ("%.2f" % centers[rid]) if len(H0_lit.split(".")[1]) == 2 else ("%.1f" % centers[rid])
        snip2 = snip.replace(H0_lit, new_lit, 1)
        if rid in ("L4_masers_5", "L4_masers_6"):   # o mesmo texto para os dois (como o PDF real)
            snip2 = "NGC 4258 %s+3.1 -3.0 Fit using all galaxies: %s+3.0 -3.0 (2) Fit for" % ("%.1f" % centers["L4_masers_5"], "%.1f" % centers["L4_masers_6"])
        body = ("<html><body><p>SINTETICO FABRICADO %s: %s</p></body></html>" % (rid, snip2)).encode("utf-8")
        rel = "fontes/%s/fonte_sintetica.html" % rid
        _w(os.path.join(root, *rel.split("/")), body)
        r["file"], r["kind"] = rel, "html"
        r.pop("page", None)
        import hashlib
        r["sha256"], r["bytes"] = hashlib.sha256(body).hexdigest(), len(body)
        # o centro declarado no spec passa a ser o fabricado (arredondado como a fonte o escreve)
        new_h0 = float(new_lit) if rid not in ("L4_masers_5", "L4_masers_6") else (float("%.1f" % centers[rid]))
        spec["leitores"][rid]["H0"] = new_h0
        spec["leitores"][rid]["documentary_source"] = {"path": rel, "sha256": r["sha256"]}
        r["declarado_no_spec_R5_2"] = {"H0": new_h0, "sigma": spec["leitores"][rid]["sigma"]}
    pkg = {"root": root, "spec_wrap": wrap, "spec": spec, "register": reg, "provider": provider or BG.SyntheticBackgroundProvider(**(provider_kw or {}))}
    if mutate:
        mutate(pkg)
    reg_b = json.dumps(pkg["register"], ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    _w(os.path.join(root, "spec", "REGISTRO_DH_V2_C1.json"), reg_b)
    import hashlib
    spec["registro_dh"]["sha256"] = hashlib.sha256(reg_b).hexdigest()
    spec["registro_dh"]["bytes"] = len(reg_b)
    wrap["spec"] = spec
    wrap["spec_sha256"] = hashlib.sha256(FRZ.canonical(spec)).hexdigest()
    _w(os.path.join(root, "spec", "PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json"), json.dumps(wrap, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8"))
    shutil.copyfile(REAL_FUNC, os.path.join(root, "spec", "veredito_fase9_v2_c1.py"))
    bgd = pkg["provider"].compute()
    thr = CAL.primary_thresholds(spec, bgd, spec["calibracao_de_cauda"]["modo"])
    _w(os.path.join(root, "calibracao", "CALIBRACAO_CAUDA_RECIBO.json"), json.dumps({"schema": "F9V2C1_CALIBRACAO_CAUDA_RECIBO_V1", "sintetico": True,
                                                                                     "limiares_equivalentes_P_primaria_BG1": thr}, indent=1, sort_keys=True).encode("utf-8"))
    for rel, b in (extra_files or {}).items():
        _w(os.path.join(root, *rel.split("/")), b)
    if with_freeze:
        bp = None
        if kind == "REAL":
            bp = bancada_pins or {"bancada/motor.py": {"sha256": "0" * 64, "bytes": 1}}
        rec = FRZ.make_freeze_receipt(root, kind, "TESTE-SINTETICO", "auditoria sintetica", spec["token"]["base"], bancada_pins=bp)
        rb = json.dumps(rec, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
        _w(os.path.join(root, *FRZ.FREEZE_REL.split("/")), rb)
        pkg["freeze_raw"] = rb
        if with_open:
            ob = json.dumps(FRZ.make_open_receipt(rb, {"quem": "TESTE", "texto": "abertura SINTETICA de teste do runner"}), ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
            _w(os.path.join(root, *FRZ.OPEN_REL.split("/")), ob)
    return pkg
