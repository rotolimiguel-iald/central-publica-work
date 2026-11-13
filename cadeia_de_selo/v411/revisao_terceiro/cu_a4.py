"""CU-A4: registro h0dn_bg1_v411 no core do ensaio: 16 checagens; valores contra o resultado publicado (clone local, so' leitura)."""
import json, os, subprocess, hashlib, math
CL = r"C:\IALD\Central_publica\central-publica-work"
p = os.path.join(CL, r"h0dn_bg1_v411_emenda_11nov\producao\RESULTADO_DA_ABERTURA_V411.json")
raw = open(p, "rb").read()
print("resultado publicado (disco do clone) sha16", hashlib.sha256(raw).hexdigest()[:16], len(raw))
# o blob no git HEAD
r = subprocess.run(["git", "-C", CL, "cat-file", "-p", "HEAD:h0dn_bg1_v411_emenda_11nov/producao/RESULTADO_DA_ABERTURA_V411.json"], capture_output=True)
print("blob HEAD == disco:", r.returncode == 0 and r.stdout == raw)
R = json.loads(raw.decode("utf-8"))
print(list(R.keys()))
res = R["resultado"]
print(list(res.keys()))
st = res["estatistica"]; print("estatistica keys", list(st.keys()))
core = json.load(open(r"C:\t\k411c\dry_v411\core_ensaio.json", encoding="utf-8"))["core"]
r4 = core["h0dn_bg1_v411"]
v = r4["values"]
print("values keys:", list(v.keys()))
print("checks ok:", [c["id"] for c in r4["mechanics"]["checks"] if not c["ok"]], r4["mechanics"]["passed"], r4["mechanics"]["n_checks"])
print("z_null pub", st.get("z_null")[:3] if isinstance(st.get("z_null"), list) else st.get("z_null"))
print("veredito pub", res["veredito"])
print("core cabeca", r4["cabeca_do_teste"][:200]); print("core outcome", r4["outcome"])
print("linha cl", r4["linha_ao_lado_cefeidas_livres"])
