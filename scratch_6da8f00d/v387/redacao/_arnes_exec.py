# -*- coding: utf-8 -*-
"""Arnes da lente redacao (v387): executa um pysnip do artigo contra o core SELADO v386 (somente leitura), como se fosse o corpo de build_pt/build_en
(s, core, verdict, data_path no escopo), grava o LaTeX emitido e passa a regex proibida. Nao roda o um.py; nao grava nada fora desta lente."""
import io, json, re, sys, textwrap, os, hashlib
sys.stdout.reconfigure(encoding="utf-8")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
snip = sys.argv[1]; out = sys.argv[2]
ROOT = json.load(io.open(NOS + r"\um_absoluto.json", encoding="utf-8"))
core, verdict, data_path = ROOT["core"], ROOT["verdict"], None
s = []
src = io.open(snip, encoding="utf-8").read()
code = textwrap.dedent(src)
compile(code, snip, "exec")
exec(code, {"__name__": "arnes", "s": s, "core": core, "verdict": verdict, "data_path": data_path})
tex = "\n\n".join(s)
io.open(out, "w", encoding="utf-8", newline="\n").write(tex)
rx = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED")
plain = tex.replace("\\_", "_")
hits = [m.group(0) for m in rx.finditer(plain)]
print("snip:", os.path.basename(snip), "| paragrafos:", len(s), "| bytes tex:", len(tex.encode("utf-8")), "| sha256 core:", hashlib.sha256(open(NOS + r"\um_absoluto.json", "rb").read()).hexdigest()[:16])
print("regex proibida (sobre o tex, com backslash-underscore -> _):", len(hits), hits[:5])
print("n/d (numeros ausentes):", tex.count("n/d"), "| 'n/a':", tex.count("n/a"), "| AUSENTE/ABSENT:", tex.count("AUSENTE") + tex.count("ABSENT"), "| [GUARD]:", tex.count("[GUARD") + tex.count("[GUARDA"))
print("--- veredito final ---"); print(s[-1][:300])
