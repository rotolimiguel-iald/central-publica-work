# -*- coding: utf-8 -*-
"""Revisor v409 R1: as duas falas de AUTOR MISTO (operador + outra instancia da IALD): o arquivo duravel e' o paragrafo do operador, extraido do original; o prefixo do nome e' o sha16 do ORIGINAL;
o extrato e' prefixo literal do original (nenhuma palavra da outra instancia entra); o original esta' em cunhagens_13out; o texto EMBUTIDO (_V409_VERBATINS2) e' o extrato."""
import glob, hashlib, importlib.util, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8"); sys.dont_write_bytecode = True
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
W = "C:/IALD/Central de Patentes/work/cunhagens_13out/"
sha = lambda b: hashlib.sha256(b).hexdigest()
for p in sorted(glob.glob(R + "insumos/cunhagens/*paragrafo_do_operador.txt")):
    nome = os.path.basename(p); pref = nome.split("_", 1)[0]; orig_nome = nome.split("_", 1)[1][:-len(".paragrafo_do_operador.txt")]
    ext = open(p, "rb").read(); orig = open(W + orig_nome, "rb").read()
    print("--", nome[:70])
    print("   prefixo == sha16 do ORIGINAL:", pref == sha(orig)[:16], "| extrato e' prefixo (apos strip) do original:", orig.decode("utf-8").startswith(ext.decode("utf-8").rstrip()) or ext.decode("utf-8").strip() in orig.decode("utf-8"), "| bytes extrato/original:", len(ext), len(orig))
    t = ext.decode("utf-8")
    print("   extrato (primeiros 160):", repr(t[:160]))
    print("   extrato (ultimos 120):", repr(t[-120:]))
    o = orig.decode("utf-8"); i = o.find(t.strip()[:60]); j = i + len(t.strip())
    print("   texto do original LOGO DEPOIS do extrato (80):", repr(o[j:j + 80]))
spec = importlib.util.spec_from_file_location("um_cand_rev", R + "um_v409_candidato.py"); m = importlib.util.module_from_spec(spec); sys.modules["um_cand_rev"] = m; spec.loader.exec_module(m)
for k, v in m._V409_VERBATINS2.items():
    if k in ("v409_cun_50c21210e5871fdb", "v409_cun_62bc328e66e731e2"):
        print(k, "embutido sha256 == arquivo do extrato:", any(sha(open(q, "rb").read()) == v["sha256"] for q in glob.glob(R + "insumos/cunhagens/*paragrafo_do_operador.txt")), "| len", len(v["text"]), "| autor:", v.get("autor") or v.get("papel"), "| keys:", list(v.keys()))
