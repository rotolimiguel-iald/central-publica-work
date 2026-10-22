import json, os, hashlib
def sha16(p):
    h=hashlib.sha256(open(p,'rb').read()).hexdigest(); return h[:16]
SP = r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad"
cf = os.path.join(SP, r"v385_selo\conferidor\conferencia_rito_v385.json")
print("conferencia json:", os.path.getsize(cf), "B sha16=", sha16(cf))
J = json.load(open(cf, encoding="utf-8"))
print("keys:", list(J.keys()))
for k,v in J.items():
    if not isinstance(v,(dict,list)): print(" ",k,"=>",str(v)[:300])
for k in ["resumo","summary","deve_mudar","nao_pode_mudar","must_change","must_not_change","totais","counts"]:
    if k in J: print(k, "=>", json.dumps(J[k], ensure_ascii=False)[:1500])
print("\n--- conferidor dir ---")
cd = os.path.join(SP, r"v385_selo\conferidor")
for f in sorted(os.listdir(cd)): print("  ", f, os.path.getsize(os.path.join(cd,f)), sha16(os.path.join(cd,f)))
print("\n--- pacote v385 conferir_rito_v385.py ---")
for cand in [os.path.join(SP,r"v385\conferir_rito_v385.py"), os.path.join(SP,r"v385_selo\conferir_rito_v385.py"), os.path.join(SP,r"v385_selo\conferidor\conferir_rito_v385.py")]:
    print(cand, os.path.exists(cand) and (os.path.getsize(cand), sha16(cand)))
print("\n--- cadeia_de_selo v385 / v385_selo ---")
for d in [r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v385", r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v385_selo"]:
    print(d, os.path.isdir(d))
    if os.path.isdir(d):
        for root,dirs,files in os.walk(d):
            for f in files:
                fp=os.path.join(root,f); print("   ", os.path.relpath(fp,d), os.path.getsize(fp), sha16(fp))
