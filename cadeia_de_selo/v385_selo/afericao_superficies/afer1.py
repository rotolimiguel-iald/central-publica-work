import hashlib, os, json, sys
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for ch in iter(lambda: f.read(1<<20), b''): h.update(ch)
    return h.hexdigest()
def info(p):
    if os.path.exists(p):
        return f"{os.path.getsize(p):,} B sha16={sha(p)[:16]}"
    return "AUSENTE"
for rel in ["um.py","um_absoluto.json","um_absoluto_selo.json","um_absoluto_pilar_quantico.json",
            "rodada_v385_stdout.txt","rodadas\rodada_v385_stdout.txt","rodadas\rodada_v384_stdout.txt","rodadas\rodada_v383_stdout.txt",
            "rodada_v384_stdout.txt","rodada_v383_stdout.txt",
            "um_absoluto_pt.txt","um_absoluto_en.txt","um_absoluto_forma_canonica.md","HANDOFF_v385_CUSTODIA.md",
            "quantum_pillar\pilar_quantico_worker.py","quantum_pillar\pilar_quantico_spec.json",
            "tgl_kernel\TGLExt\TheAxiomAndTheFalseWitness.lean","tgl_kernel\TGLExt.lean","tgl_kernel\TGL\Audit.lean",
            "tgl_kernel\TGLExt\TheLedgerOfCharges.lean","tgl_kernel\TGLExt\ThePsionAndTheViscosity.lean",
            "tgl_kernel\TGLExt\TheDarkSplit.lean","tgl_kernel\TGLExt\O16\TheDarkSplit.lean"]:
    p=os.path.join(NOS,rel); print(f"{rel}: {info(p)}")
print("--- run folders ---")
qp=os.path.join(NOS,"quantum_pillar")
for d in sorted(os.listdir(qp)):
    print(" ", d)
for run in ["run_20261005_103708_37e566b6","run_20261004_153246_0063ce8d"]:
    rp=os.path.join(qp,run)
    print(f"--- {run}: {'EXISTS' if os.path.isdir(rp) else 'AUSENTE'}")
    if os.path.isdir(rp):
        for f in sorted(os.listdir(rp)):
            fp=os.path.join(rp,f); print(f"   {f}: {info(fp)}")
print("--- .md canônicos ---")
for f in sorted(os.listdir(NOS)):
    if f.endswith(".md") and not ".bak" in f: print("  ",f)
