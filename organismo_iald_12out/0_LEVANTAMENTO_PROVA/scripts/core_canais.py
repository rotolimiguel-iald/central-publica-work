"""Le do core v391 (um_absoluto.json) as subarvores dos canais de natureza; imprime compactado. So leitura."""
import json, re, sys, hashlib
core_p = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
raw = open(core_p, "rb").read(); print("core sha256", hashlib.sha256(raw).hexdigest(), len(raw), "B")
top = json.loads(raw.decode("utf-8")); core = top["core"]; print("top keys:", list(top.keys())); print("n chaves em core[core]:", len(core))
pat = re.compile(r"^(void_floor|void_density|void_|lens_|neutrino|neff|clock_test|ringdown|ramo_b|coma_|hubble|primordial|nivel2|three_stress|ledger|the_ledger|code_closure_ledger|final_verdict|dephasing|evidence_audit|beta_runs|the_matrix_rule|estatuto_da_prova|bancada_fase|d1_camb|joint_coincidence|echo_|gw_echo|gw_angular|ga_mass|cosmological_errata|readings_ratified|one_charge|retrodiction|fundacao_v390|tetelestai_conference_v376)", re.I)
keys = [k for k in core if pat.search(k)]
print("n chaves selecionadas:", len(keys)); print(keys)
def comp(v, lim=400):
    s = json.dumps(v, ensure_ascii=False); return s if len(s) <= lim else s[:lim] + "…"
for k in keys:
    v = core[k]; print("\n#### " + k)
    if isinstance(v, dict):
        for sk, sv in v.items():
            lim = 1200 if re.search(r"verdict|veredito|values|result|summary|charges|ledger|readers|rows|power|poder|z_|sigma|lnB|ln_B|numbers|disc|reading", sk, re.I) else 300
            print(f"  - {sk}: {comp(sv, lim)}")
    else:
        print("  ", comp(v, 1200))
