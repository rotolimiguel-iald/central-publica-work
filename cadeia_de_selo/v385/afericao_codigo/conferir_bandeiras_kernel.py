# -*- coding: utf-8 -*-
# SO LEITURA: (d) bandeiras/escada e (e) kernel embutido do candidato vs sandbox e vs v384 do Nos
import ast, json, os, re, sys, hashlib
sys.stdout.reconfigure(encoding="utf-8")
PK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SP = os.path.dirname(PK)
KS = os.path.join(SP, "v376", "kernel_src")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
src = open(os.path.join(PK, "um_v385_candidato.py"), encoding="utf-8").read()
lines = src.splitlines(keepends=True)
def block(prefix, closer):
    i = [k for k, l in enumerate(lines) if l.startswith(prefix)]
    assert len(i) == 1, (prefix, len(i)); i = i[0]; j = i + 1
    while lines[j].rstrip("\r\n") != closer:
        j += 1
    return "".join(lines[i:j + 1])
FL = ast.literal_eval(block("_LEAN_THEOREM_FLAGS = {", "}").split("=", 1)[1].strip())
# ext_flags (indentado) dentro de uma funcao
i = [k for k, l in enumerate(lines) if l.startswith("    ext_flags = [")]; assert len(i) == 1; i = i[0]; j = i + 1
while lines[j].rstrip("\r\n") != "    ]":
    j += 1
EXT = ast.literal_eval("".join(lines[i:j + 1]).split("=", 1)[1].strip())
print("ext_flags (escada):", len(EXT), "unicos:", len(set(EXT)), "fora de _LEAN_THEOREM_FLAGS:", [f for f in EXT if f not in FL][:5])
RT = {}
exec("\n".join(l for l in open(os.path.join(PK, "v385_runtime.py"), encoding="utf-8").read().splitlines() if l.startswith(("_AXM_FLAGS_V385", "_DKS_FLAGS_V385", "]")) or l.startswith("    \"ext_")), RT)
F28 = RT["_AXM_FLAGS_V385"] + RT["_DKS_FLAGS_V385"]
print("28 em _LEAN_THEOREM_FLAGS:", sum(f in FL for f in F28), "| 28 na escada:", sum(f in EXT for f in F28))
# kernel embutido
EMB = ast.literal_eval(block("_EMBEDDED_KERNEL_FILES = {", "}").split("=", 1)[1].strip())
print("entradas no kernel embutido:", len(EMB))
aud = EMB["TGL/Audit.lean"]
printed = set(re.findall(r"^#print axioms\s+(\S+)", aud, re.M))
opens = re.findall(r"^open\s+.*$", aud, re.M)
miss = []
for f in F28:
    nm = FL[f]
    short = nm
    if nm not in printed:
        miss.append(nm)
print("nomes das 28 com '#print axioms <nome completo>' no Audit embutido: faltam", miss)
print("opens no Audit:", opens[:5])
# relatorio de axiomas do sandbox
rep = json.load(open(os.path.join(PK, "kernel", "sandbox_axiom_report_v385.json"), encoding="utf-8"))
ax = rep.get("axioms") or rep.get("axiom_report") or rep
TRIO = {"propext", "Classical.choice", "Quot.sound"}
bad = {FL[f]: ax.get(FL[f]) for f in F28 if not (isinstance(ax.get(FL[f]), list) and set(ax.get(FL[f])) <= TRIO)}
print("sandbox: as 28 com axiomas no trio (faltando/ruins):", bad)
# bytes da pedra vs sandbox
for k in ("TGLExt/TheAxiomAndTheFalseWitness.lean", "TGLExt.lean", "TGL/Audit.lean", "TGLExt/TheDarkSplit.lean"):
    p = os.path.join(KS, *k.split("/"))
    sb = open(p, "r", encoding="utf-8", newline="").read()
    print(k, "embutido == sandbox:", EMB.get(k) == sb, "sha16", hashlib.sha256(EMB.get(k, "").encode()).hexdigest()[:16], hashlib.sha256(open(p, "rb").read()).hexdigest()[:16])
# v384 do Nos: so acrescimo
raw = open(os.path.join(NOS, "um.py"), "rb").read().decode("utf-8")
l4 = raw.splitlines(keepends=True)
i = [k for k, l in enumerate(l4) if l.startswith("_EMBEDDED_KERNEL_FILES = {")][0]; j = i + 1
while l4[j].rstrip("\r\n") != "}":
    j += 1
EMB4 = ast.literal_eval("".join(l4[i:j + 1]).split("=", 1)[1].strip())
ch = sorted(k for k in EMB4 if EMB4[k] != EMB.get(k)); nw = sorted(k for k in EMB if k not in EMB4); gone = sorted(k for k in EMB4 if k not in EMB)
print("v384->v385 mudados:", ch, "novos:", nw, "sumidos:", gone)
a4, a5 = EMB4["TGL/Audit.lean"], EMB["TGL/Audit.lean"]
hdr = "import TGLExt.TheAxiomAndTheFalseWitness\nimport TGLExt.TheDarkSplit\n"
print("Audit: v385 = hdr + v384(sem \n final) + resto?", a5.startswith(hdr) and a5[len(hdr):].startswith(a4.rstrip("\n")))
resto = a5[len(hdr) + len(a4.rstrip("\n")):]
print("Audit: acrescimo no fim (linhas):", len(resto.splitlines()), "| #print axioms acrescidos:", len(re.findall(r"#print axioms", resto)))
print(resto[:300].replace("\n", " | "))
t4, t5 = EMB4["TGLExt.lean"], EMB["TGLExt.lean"]
print("TGLExt.lean acrescimo:", repr(t5[len(t4.rstrip("\n")):]))
# a pedra ja importava TheDarkSplit em algum lugar no v384?
print("TheDarkSplit ja importado no TGLExt.lean v384:", "import TGLExt.TheDarkSplit" in t4)
# token
tok = re.search(r'def finalStepNameAxioma : String :=\s*"([A-Z0-9_]+)"', EMB["TGLExt/TheAxiomAndTheFalseWitness.lean"]).group(1)
rt = open(os.path.join(PK, "v385_runtime.py"), encoding="utf-8").read()
m = re.search(r'_AXIOMA_TOKEN_V385 = \(("[^"]+")\s*\n\s*("[^"]+")\)', rt)
rtok = ast.literal_eval(m.group(1)) + ast.literal_eval(m.group(2))
print("token do kernel == token do runtime:", tok == rtok, len(tok))
