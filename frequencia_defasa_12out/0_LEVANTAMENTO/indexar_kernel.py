# -*- coding: utf-8 -*-
# Indexa (somente leitura) as declaracoes do kernel do Nos: arquivo, linha, tipo, nome qualificado (namespace), sha16 do arquivo.
# Exclui .bak e .lake. Saida: KERNEL_INDICE.json (nesta pasta).
import os, re, json, hashlib, sys
RAIZ = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\tgl_kernel"
AQUI = os.path.dirname(os.path.abspath(__file__))
DECL = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|nonrec|partial|unsafe)\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|axiom|opaque)\s+([^\s:(\[{]+)")
NS_OPEN = re.compile(r"^\s*namespace\s+(\S+)")
NS_END = re.compile(r"^\s*end\s+(\S+)\s*$")
SEC_OPEN = re.compile(r"^\s*(?:noncomputable\s+)?section(?:\s+(\S+))?\s*$")
out = []
files = {}
for top in ("TGLExt", "TGL"):
    base = os.path.join(RAIZ, top)
    for dp, dns, fns in os.walk(base):
        dns.sort()
        for fn in sorted(fns):
            if not fn.endswith(".lean"):
                continue
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, RAIZ).replace("\\", "/")
            with open(p, "rb") as fh:
                b = fh.read()
            files[rel] = {"sha16": hashlib.sha256(b).hexdigest()[:16], "bytes": len(b)}
            txt = b.decode("utf-8", errors="replace").splitlines()
            stack = []  # list of (kind, name)
            in_block_comment = 0
            for i, line in enumerate(txt, 1):
                s = line
                # crude block comment tracking (/- ... -/), enough for declarations at line start
                if in_block_comment:
                    in_block_comment += s.count("/-") - s.count("-/")
                    if in_block_comment > 0:
                        continue
                    in_block_comment = 0
                    continue
                if s.lstrip().startswith("/-"):
                    in_block_comment = s.count("/-") - s.count("-/")
                    if in_block_comment > 0:
                        continue
                    in_block_comment = 0
                    continue
                m = NS_OPEN.match(s)
                if m:
                    stack.append(("ns", m.group(1)))
                    continue
                m = SEC_OPEN.match(s)
                if m:
                    stack.append(("sec", m.group(1) or ""))
                    continue
                m = NS_END.match(s)
                if m:
                    nm = m.group(1)
                    for k in range(len(stack) - 1, -1, -1):
                        if stack[k][1] == nm:
                            del stack[k:]
                            break
                    continue
                if re.match(r"^\s*end\s*$", s):
                    if stack:
                        stack.pop()
                    continue
                m = DECL.match(s)
                if m:
                    kind, name = m.group(1), m.group(2)
                    ns = ".".join(n for k, n in stack if k == "ns" and n)
                    q = (ns + "." + name) if ns and not name.startswith("_root_.") else name.replace("_root_.", "")
                    out.append({"file": rel, "line": i, "kind": kind, "name": name, "qual": q,
                                "text": s.strip()[:300]})
with open(os.path.join(AQUI, "KERNEL_INDICE.json"), "w", encoding="utf-8") as fh:
    json.dump({"raiz": RAIZ, "n_arquivos": len(files), "n_declaracoes": len(out), "arquivos": files, "declaracoes": out},
              fh, ensure_ascii=False, indent=0)
print("arquivos", len(files), "declaracoes", len(out))
