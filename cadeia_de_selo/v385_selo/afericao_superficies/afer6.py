import os, hashlib
def sha16(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
for d in [r"C:\IALD\Bancada_Um\investigacao\preregistro_dois_lados_02out", r"C:\IALD\Bancada_Um\investigacao\preregistro_pilar_quantico_03out"]:
    print("===", d, os.path.isdir(d))
    if os.path.isdir(d):
        tot=0; n=0
        for root,dirs,files in os.walk(d):
            for f in sorted(files):
                fp=os.path.join(root,f); sz=os.path.getsize(fp)
                rel=os.path.relpath(fp,d)
                if rel.startswith("evidencias_PREREGISTRO_V1"): tot+=sz; n+=1
                print(f"   {rel}  {sz:,} B  {sha16(fp)}")
        print(f"   evidencias_PREREGISTRO_V1: {n} arquivos, {tot:,} B")
