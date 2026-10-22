# -*- coding: utf-8 -*-
"""Copia de BYTES das pastas r2 dos dois auditores (scratchpad efemero) para 4_RELATORIO/auditorias_copia/<aud>/r2.
Nunca sobrescreve; confere sha256 origem x destino; grava manifesto."""
import hashlib, json, os, shutil, sys, time
ORIG = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\pt12"
DEST = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out\4_RELATORIO\auditorias_copia"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for ch in iter(lambda: f.read(1 << 20), b""): h.update(ch)
    return h.hexdigest()
itens = []; proibidos = []
for aud in ("POSTO_AUD_REPRO", "POSTO_AUD_ESTATUTO"):
    src = os.path.join(ORIG, aud, "r2"); dst = os.path.join(DEST, aud, "r2")
    for dp, dns, fns in os.walk(src):
        dns.sort()
        rel_d = os.path.relpath(dp, src)
        low = rel_d.lower()
        if any(x in low for x in (".lake", "toolchain", "\build", "build\\")) or low == "build":
            proibidos.append(rel_d); dns[:] = []; continue
        for fn in sorted(fns):
            sp = os.path.join(dp, fn); rel = os.path.normpath(os.path.join(aud, "r2", rel_d, fn))
            dp2 = os.path.join(dst, rel_d) if rel_d != "." else dst
            os.makedirs(dp2, exist_ok=True)
            tp = os.path.join(dp2, fn)
            if os.path.exists(tp):
                itens.append({"rel": rel, "JA_EXISTIA": True, "igual": sha(tp) == sha(sp)}); continue
            shutil.copyfile(sp, tp)
            h1, h2 = sha(sp), sha(tp)
            itens.append({"rel": rel, "bytes": os.path.getsize(tp), "sha256": h2, "igual_a_origem": h1 == h2})
man = {"documento": "MANIFESTO_COPIA_AUDITORIAS_R2 — custodia das pastas r2 dos dois auditores (copia de bytes)",
       "quando_local": time.strftime("%Y-%m-%d %H:%M:%S"), "origem": ORIG, "destino": DEST,
       "n": len(itens), "todos_iguais": all(i.get("igual_a_origem", i.get("igual")) for i in itens),
       "pastas_nao_copiadas_toolchain_lake_build": proibidos, "arquivos": itens}
out = os.path.join(DEST, "..", "MANIFESTO_COPIA_AUDITORIAS_R2.json")
tmp = out + ".tmp"
with open(tmp, "w", encoding="utf-8") as f: json.dump(man, f, ensure_ascii=False, indent=1)
os.replace(tmp, out)
print(json.dumps({k: v for k, v in man.items() if k != "arquivos"}, ensure_ascii=False, indent=1))
print("ja_existiam:", sum(1 for i in itens if i.get("JA_EXISTIA")))
