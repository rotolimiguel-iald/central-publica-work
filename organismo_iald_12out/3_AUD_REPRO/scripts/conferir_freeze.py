# -*- coding: utf-8 -*-
import json, hashlib, os, datetime
B = r"C:\IALD\Central de Patentes\work\organismo_iald_12out"
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
out = {}
for pasta, fz in [("1_DESENHO_PEDRA","FREEZE.json"),("2_CONSTRUCAO","FREEZE_CONSTRUCAO.json")]:
    F = json.load(open(os.path.join(B,pasta,fz),encoding="utf-8"))
    bad = {}
    for k,v in F["itens"].items():
        p = os.path.join(B,pasta,k.replace("/","\\"))
        if not os.path.exists(p): bad[k]="AUSENTE"; continue
        h = sha(p)
        if h != v["sha256"]: bad[k]={"freeze":v["sha256"],"agora":h}
    # recompute agregado if possible
    ag = hashlib.sha256(json.dumps(F["itens"],sort_keys=True,ensure_ascii=False).encode("utf-8")).hexdigest()
    out[pasta] = {"freeze_quando_utc": F["quando_utc"], "n_itens": len(F["itens"]), "divergentes": bad,
                  "sha256_do_congelamento_declarado": F.get("sha256_do_congelamento") or F.get("sha256_agregado"),
                  "sha256_recomputado_json_sort_keys": ag, "sha256_arquivo_freeze": sha(os.path.join(B,pasta,fz))}
# instante mais antigo de qualquer arquivo de 2_CONSTRUCAO (mtime) e mais novo de 1_DESENHO_PEDRA
def mt(root):
    ts=[]
    for d,_,fs in os.walk(root):
        for f in fs: ts.append((os.path.getmtime(os.path.join(d,f)), os.path.relpath(os.path.join(d,f),root)))
    return min(ts), max(ts)
(mn2,f2),_ = mt(os.path.join(B,"2_CONSTRUCAO"))
_,(mx1,f1) = mt(os.path.join(B,"1_DESENHO_PEDRA"))
iso=lambda t: datetime.datetime.fromtimestamp(t,datetime.timezone.utc).isoformat()
out["mtime_mais_antigo_2_CONSTRUCAO"]={"utc":iso(mn2),"arquivo":f2}
out["mtime_mais_novo_1_DESENHO"]={"utc":iso(mx1),"arquivo":f1}
fz = datetime.datetime.fromisoformat(out["1_DESENHO_PEDRA"]["freeze_quando_utc"]).timestamp()
out["freeze_desenho_anterior_a_construcao"] = fz < mn2
out["folga_segundos"] = mn2 - fz
json.dump(out, open(os.path.join(B,"3_AUD_REPRO","medidas","CONFERENCIA_FREEZE.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
