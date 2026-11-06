import hashlib, json, sys, os, time
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
r2 = json.load(open(R + "revisao_terceiro/REVISAO_TERCEIRO_v409.R2.json", encoding="utf-8"))
print("candidato agora:", sha16(R + "um_v409_candidato.py"), os.path.getsize(R + "um_v409_candidato.py"))
mud = {k: (v, sha16(R + k)) for k, v in r2["arquivos_revisados"].items() if sha16(R + k) != v}
for k, (a, b) in mud.items(): print("MUDOU", k, a, "->", b)
p = json.load(open(R + "PREPARACAO_v409_PRONTA.json", encoding="utf-8")); print("PRONTA:", p["pronta"], p["candidato_sha16"], p.get("quando"), p.get("falta"))
for f in ("RELATORIO_PREPARACAO_v409.md", "PLANO_v409.md", "varredura_fock_omega_v409.py"):
    if os.path.exists(R + f): print(f, time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(R + f))), sha16(R + f))
